from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class AccountingEntry(BaseModel):
    data: date
    reg_ans: str
    cd_conta_contabil: str
    descricao: str
    vl_saldo_inicial: Decimal
    vl_saldo_final: Decimal
