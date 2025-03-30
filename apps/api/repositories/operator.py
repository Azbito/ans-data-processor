from psycopg2 import sql
from typing import List, Tuple, Optional
from models.operator import Operator
from .database import DatabaseRepository
import base64
import json
from psycopg2.extras import execute_values

class OperatorRepository:
    @staticmethod
    def create_table():
        db_connection = None
        cursor = None
        try:
            db_connection = DatabaseRepository.get_connection()
            cursor = db_connection.cursor()

            query = """
            CREATE TABLE IF NOT EXISTS operators (
                registro_ans VARCHAR PRIMARY KEY,
                cnpj VARCHAR,
                razao_social VARCHAR,
                nome_fantasia VARCHAR,
                modalidade VARCHAR,
                logradouro VARCHAR,
                numero VARCHAR,
                complemento VARCHAR,
                bairro VARCHAR,
                cidade VARCHAR,
                uf VARCHAR,
                cep VARCHAR,
                ddd VARCHAR,
                telefone VARCHAR,
                fax VARCHAR,
                endereco_eletronico VARCHAR,
                representante VARCHAR,
                cargo_representante VARCHAR,
                regiao_de_comercializacao VARCHAR,
                data_registro_ans DATE
            )
            """
            cursor.execute(query)
            db_connection.commit()
        finally:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()

    @staticmethod
    def _encode_cursor(last_item: Operator) -> str:
        cursor_data = {
            "registro_ans": last_item.registro_ans
        }
        return base64.b64encode(json.dumps(cursor_data).encode()).decode()

    @staticmethod
    def _decode_cursor(cursor: str) -> dict:
        try:
            return json.loads(base64.b64decode(cursor.encode()).decode())
        except:
            return None

    @staticmethod
    def get_all(limit: int = 50, cursor: Optional[str] = None) -> Tuple[List[Operator], Optional[str]]:
        db_connection = None
        cursor_obj = None
        try:
            db_connection = DatabaseRepository.get_connection()
            cursor_obj = db_connection.cursor()

            if cursor:
                cursor_data = OperatorRepository._decode_cursor(cursor)
                query = sql.SQL("""
                    SELECT * FROM operators 
                    WHERE registro_ans > %s
                    ORDER BY registro_ans
                    LIMIT %s
                """)
                cursor_obj.execute(query, (cursor_data["registro_ans"], limit + 1))
            else:
                query = sql.SQL("""
                    SELECT * FROM operators
                    ORDER BY registro_ans
                    LIMIT %s
                """)
                cursor_obj.execute(query, (limit + 1,))

            rows = cursor_obj.fetchall()

            operators = []
            for row in rows[:limit]:
                operator = Operator(
                    registro_ans=row[0],
                    cnpj=row[1],
                    razao_social=row[2],
                    nome_fantasia=row[3],
                    modalidade=row[4],
                    logradouro=row[5],
                    numero=row[6],
                    complemento=row[7],
                    bairro=row[8],
                    cidade=row[9],
                    uf=row[10],
                    cep=row[11],
                    ddd=row[12],
                    telefone=row[13],
                    fax=row[14],
                    endereco_eletronico=row[15],
                    representante=row[16],
                    cargo_representante=row[17],
                    regiao_de_comercializacao=row[18],
                    data_registro_ans=row[19]
                )
                operators.append(operator)

            next_cursor = None
            if len(rows) > limit and operators:
                next_cursor = OperatorRepository._encode_cursor(operators[-1])

            return operators, next_cursor
        finally:
            if cursor_obj:
                cursor_obj.close()
            if db_connection:
                db_connection.close()

    @staticmethod
    def get_by_id(registro_ans: int) -> Optional[Operator]:
        db_connection = None
        cursor = None
        try:
            db_connection = DatabaseRepository.get_connection()
            cursor = db_connection.cursor()

            query = sql.SQL("""
                SELECT * FROM operators
                WHERE registro_ans = %s
            """)
            cursor.execute(query, (registro_ans,))
            row = cursor.fetchone()

            if row:
                return Operator(
                    registro_ans=row[0],
                    cnpj=row[1],
                    razao_social=row[2],
                    nome_fantasia=row[3],
                    modalidade=row[4],
                    logradouro=row[5],
                    numero=row[6],
                    complemento=row[7],
                    bairro=row[8],
                    cidade=row[9],
                    uf=row[10],
                    cep=row[11],
                    ddd=row[12],
                    telefone=row[13],
                    fax=row[14],
                    endereco_eletronico=row[15],
                    representante=row[16],
                    cargo_representante=row[17],
                    regiao_de_comercializacao=row[18],
                    data_registro_ans=row[19]
                )
            return None
        finally:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()

    @staticmethod
    def bulk_insert(operators: List[dict]) -> int:
        if not operators:
            return 0

        db_connection = None
        cursor = None
        try:
            db_connection = DatabaseRepository.get_connection()
            cursor = db_connection.cursor()

            columns = [
                'registro_ans', 'cnpj', 'razao_social', 'nome_fantasia',
                'modalidade', 'logradouro', 'numero', 'complemento',
                'bairro', 'cidade', 'uf', 'cep', 'ddd', 'telefone',
                'fax', 'endereco_eletronico', 'representante',
                'cargo_representante', 'regiao_de_comercializacao', 'data_registro_ans'
            ]

            values = [[operator[col] for col in columns] for operator in operators]

            insert_query = sql.SQL("""
                INSERT INTO operators ({columns})
                VALUES %s
                ON CONFLICT (registro_ans) DO UPDATE SET
                    cnpj = EXCLUDED.cnpj,
                    razao_social = EXCLUDED.razao_social,
                    nome_fantasia = EXCLUDED.nome_fantasia,
                    modalidade = EXCLUDED.modalidade,
                    logradouro = EXCLUDED.logradouro,
                    numero = EXCLUDED.numero,
                    complemento = EXCLUDED.complemento,
                    bairro = EXCLUDED.bairro,
                    cidade = EXCLUDED.cidade,
                    uf = EXCLUDED.uf,
                    cep = EXCLUDED.cep,
                    ddd = EXCLUDED.ddd,
                    telefone = EXCLUDED.telefone,
                    fax = EXCLUDED.fax,
                    endereco_eletronico = EXCLUDED.endereco_eletronico,
                    representante = EXCLUDED.representante,
                    cargo_representante = EXCLUDED.cargo_representante,
                    regiao_de_comercializacao = EXCLUDED.regiao_de_comercializacao,
                    data_registro_ans = EXCLUDED.data_registro_ans
            """).format(
                columns=sql.SQL(', ').join(map(sql.Identifier, columns))
            )

            execute_values(cursor, insert_query, values)
            db_connection.commit()
            
            return len(operators)
        finally:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()
