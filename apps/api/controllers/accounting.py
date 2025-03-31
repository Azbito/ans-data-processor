from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Optional
import pandas as pd
import io
from datetime import datetime, date
from decimal import Decimal
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
                            **entry.dict(exclude_unset=True),
                            'data': entry.data.isoformat() if isinstance(entry.data, (date, datetime)) else str(entry.data),
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
                        **entry.dict(exclude_unset=True),
                        'data': entry.data.isoformat() if isinstance(entry.data, (date, datetime)) else str(entry.data),
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
            content = await file.read()
            
            data_frame = pd.read_csv(
                io.StringIO(content.decode()),
                sep=';',
                decimal=',',
                thousands='.'
            )

            entries = []
            for _, row in data_frame.iterrows():
                entry = AccountingEntry(
                    data=row['data'],
                    reg_ans=str(row['reg_ans']),
                    cd_conta_contabil=row['cd_conta_contabil'],
                    descricao=row['descricao'],
                    vl_saldo_inicial=Decimal(str(row['vl_saldo_inicial'])),
                    vl_saldo_final=Decimal(str(row['vl_saldo_final']))
                )
                entries.append(entry)

            db_connection = DatabaseRepository.get_connection()

            try:
                inserted = AccountingRepository.bulk_insert(entries)
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
