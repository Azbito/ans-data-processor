from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Optional
import pandas as pd
import io
from datetime import datetime
from models.accounting import AccountingEntry
from repositories.accounting import AccountingRepository
from repositories.database import DatabaseRepository

router = APIRouter()


class AccountingController:
    @staticmethod
    def get_all_accounting(limit: int = 50, cursor: Optional[str] = None) -> JSONResponse:
        try:
            db_connection = DatabaseRepository.get_connection()
            try:
                entries, next_cursor = AccountingRepository.get_all(limit, cursor)
                db_connection.commit()
                return JSONResponse(content={
                    "data": [
                        {
                            **entry.dict(),
                            'data': entry.data.isoformat() if entry.data else None,
                            'vl_saldo_inicial': float(entry.vl_saldo_inicial) if entry.vl_saldo_inicial else None,
                            'vl_saldo_final': float(entry.vl_saldo_final) if entry.vl_saldo_final else None
                        }
                        for entry in entries
                    ],
                    "next_cursor": next_cursor
                })
            except Exception as e:
                db_connection.rollback()
                raise HTTPException(status_code=500, detail=str(e))
            finally:
                db_connection.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_accounting(reg_ans: int) -> JSONResponse:
        try:
            db_connection = DatabaseRepository.get_connection()
            try:
                entries = AccountingRepository.get_by_operator(reg_ans)
                db_connection.commit()
                return JSONResponse(content=[
                    {
                        **entry.dict(),
                        'data': entry.data.isoformat() if entry.data else None,
                        'vl_saldo_inicial': float(entry.vl_saldo_inicial) if entry.vl_saldo_inicial else None,
                        'vl_saldo_final': float(entry.vl_saldo_final) if entry.vl_saldo_final else None
                    }
                    for entry in entries
                ])
            except Exception as e:
                db_connection.rollback()
                raise HTTPException(status_code=500, detail=str(e))
            finally:
                db_connection.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def import_accounting(file: UploadFile) -> JSONResponse:
        try:
            db_connection = DatabaseRepository.get_connection()
            try:
                content = await file.read()
                
                data_frame = pd.read_csv(
                    io.BytesIO(content),
                    sep=";",
                    encoding="utf-8",
                    decimal=",",
                    parse_dates=["DATA"]
                )

                column_mapping = {
                    "DATA": "data",
                    "REG_ANS": "reg_ans",
                    "CD_CONTA_CONTABIL": "cd_conta_contabil",
                    "DESCRICAO": "descricao",
                    "VL_SALDO_INICIAL": "vl_saldo_inicial",
                    "VL_SALDO_FINAL": "vl_saldo_final"
                }
                data_frame = data_frame.rename(columns=column_mapping)

                data_frame = data_frame.fillna("")
                
                data_frame['reg_ans'] = data_frame['reg_ans'].astype(int)
                
                data_frame['vl_saldo_inicial'] = pd.to_numeric(data_frame['vl_saldo_inicial'], errors='coerce')
                data_frame['vl_saldo_final'] = pd.to_numeric(data_frame['vl_saldo_final'], errors='coerce')
                
                inserted = AccountingRepository.bulk_insert(data_frame.to_dict('records'))
                
                db_connection.commit()
                return JSONResponse(
                    content={"message": f"Successfully imported {inserted} accounting records"},
                    status_code=200
                )
            except Exception as e:
                db_connection.rollback()
                raise HTTPException(status_code=500, detail=str(e))
            finally:
                db_connection.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
