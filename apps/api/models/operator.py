from pydantic import BaseModel
from datetime import date

class Operator(BaseModel):
    registro_ans: int
    cnpj: str
    razao_social: str
    nome_fantasia: str
    modalidade: str
    logradouro: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    uf: str
    cep: int
    ddd: int
    telefone: int
    fax: int
    endereco_eletronico: str
    representante: str
    cargo_representante: str
    regiao_de_comercializacao: int
    data_registro_ans: date
