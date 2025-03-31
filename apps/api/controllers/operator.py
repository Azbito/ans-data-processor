from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Optional
import pandas as pd
import io
from datetime import datetime
from models.operator import Operator
from repositories.operator import OperatorRepository

router = APIRouter()


class OperatorController:
    @staticmethod
    def get_all_operators(limit: int = 50, cursor: Optional[str] = None) -> JSONResponse:
        try:
            operators, next_cursor = OperatorRepository.get_all(limit, cursor)
            return JSONResponse(content={
                "data": [
                    {
                        **op.dict(),
                        'data_registro_ans': op.data_registro_ans.isoformat() if op.data_registro_ans else None
                    } 
                for op in operators
            ],
                "next_cursor": next_cursor
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_operator(registro_ans: int) -> JSONResponse:
        try:
            operator = OperatorRepository.get_by_id(registro_ans)
            if not operator:
                raise HTTPException(status_code=404, detail="Not found")
            return JSONResponse(content={
                **operator.dict(),
                'data_registro_ans': operator.data_registro_ans.isoformat() if operator.data_registro_ans else None
            })
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def import_operators(file: UploadFile) -> JSONResponse:
        try:
            content = await file.read()
            
            data_frame = pd.read_csv(
                io.BytesIO(content),
                sep=";",
                encoding="utf-8",
                decimal=",",
                parse_dates=["Data_Registro_ANS"]
            )

            column_mapping = {
                "Registro_ANS": "registro_ans",
                "CNPJ": "cnpj",
                "Razao_Social": "razao_social",
                "Nome_Fantasia": "nome_fantasia",
                "Modalidade": "modalidade",
                "Logradouro": "logradouro",
                "Numero": "numero",
                "Complemento": "complemento",
                "Bairro": "bairro",
                "Cidade": "cidade",
                "UF": "uf",
                "CEP": "cep",
                "DDD": "ddd",
                "Telefone": "telefone",
                "Fax": "fax",
                "Endereco_eletronico": "endereco_eletronico",
                "Representante": "representante",
                "Cargo_Representante": "cargo_representante",
                "Regiao_de_Comercializacao": "regiao_de_comercializacao",
                "Data_Registro_ANS": "data_registro_ans"
            }
            data_frame = data_frame.rename(columns=column_mapping)

            data_frame = data_frame.fillna("")
            
            operators = []
            for record in data_frame.to_dict('records'):
                try:
                    operator = Operator(**record)
                    operators.append(operator)
                except Exception as e:
                    print(f"Error processing record: {record}, Error: {str(e)}")
                    continue
            
            inserted = OperatorRepository.bulk_insert(operators)
            
            return JSONResponse(
                content={"message": f"Successfully imported {inserted} operator records"},
                status_code=200
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
