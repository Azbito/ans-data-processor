from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class AccountingEntry(BaseModel):
    data: date
    reg_ans: int
    cd_conta_contabil: int
    descricao: str
    vl_saldo_inicial: Decimal
    vl_saldo_final: Decimal
