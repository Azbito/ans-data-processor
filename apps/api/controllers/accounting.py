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
            
            print("\nCSV Content:")
            print(content[:500].decode()) 
            print("\n")
            
            try:
                
                data_frame = pd.read_csv(
                    io.StringIO(content.decode()),
                    sep=';',
                    decimal=',',
                    thousands='.'
                )
                
                
                data_frame.columns = data_frame.columns.str.lower()
                
                
                expected_columns = {
                    'data': str,
                    'reg_ans': int,
                    'cd_conta_contabil': int,
                    'descricao': str,
                    'vl_saldo_inicial': float,
                    'vl_saldo_final': float
                }
                
                
                missing_columns = [col for col in expected_columns.keys() if col not in data_frame.columns]
                if missing_columns:
                    raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
                
                
                for col, dtype in expected_columns.items():
                    if dtype == str:
                        data_frame[col] = data_frame[col].astype(str)
                    elif dtype == int:
                        data_frame[col] = pd.to_numeric(data_frame[col], errors='coerce').fillna(0).astype(int)
                    elif dtype == float:
                        data_frame[col] = pd.to_numeric(data_frame[col], errors='coerce').fillna(0.0)
                
                print("\nDataFrame Preview:")
                print(data_frame.head())
                print("\n")
                
                
                data_frame['data'] = pd.to_datetime(data_frame['data'], format='%Y-%m-%d', errors='coerce')
                
                entries = []
                for _, row in data_frame.iterrows():
                    if pd.isna(row['data']):
                        continue
                    
                    entry = AccountingEntry(
                        data=row['data'].to_pydatetime().date(),
                        reg_ans=row['reg_ans'],
                        cd_conta_contabil=row['cd_conta_contabil'],
                        descricao=row['descricao'],
                        vl_saldo_inicial=Decimal(str(row['vl_saldo_inicial'])),
                        vl_saldo_final=Decimal(str(row['vl_saldo_final']))
                    )
                    entries.append(entry)

                
                entries_dict = [entry.dict() for entry in entries]

                db_connection = DatabaseRepository.get_connection()

                try:
                    inserted = AccountingRepository.bulk_insert(entries_dict)
                    db_connection.commit()

                    return JSONResponse(
                        content={
                            "message": f"Successfully imported {inserted} accounting records",
                            "total_rows": len(data_frame),
                            "imported_rows": inserted
                        },
                        status_code=200
                    )
                except Exception as e:
                    db_connection.rollback()
                    raise HTTPException(status_code=500, detail=str(e))
                finally:
                    db_connection.close()
            
            except Exception as e:
                print(f"Error processing CSV: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": str(e),
                        "message": "Failed to process CSV file. Please check the file format and content."
                    }
                )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
