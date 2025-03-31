from psycopg2 import sql
from typing import List, Tuple, Optional
from models.accounting import AccountingEntry
from .database import DatabaseRepository
from psycopg2.extras import execute_values
import base64
import json
from datetime import datetime, date
from decimal import Decimal
from utils.json_encoder import JSONEncoder

class AccountingRepository:
    TABLE_NAME = "accountings"

    @classmethod
    def create_table(cls):
        db_connection = None
        cursor = None
        
        try:
            db_connection = DatabaseRepository.get_connection()
            cursor = db_connection.cursor()

            create_table_query = sql.SQL(
                """
                CREATE TABLE IF NOT EXISTS {table} (
                    data DATE,
                    reg_ans VARCHAR,
                    cd_conta_contabil VARCHAR(50),
                    descricao VARCHAR(255),
                    vl_saldo_inicial DECIMAL(18, 2),
                    vl_saldo_final DECIMAL(18, 2)
                )
                """
            ).format(table=sql.Identifier(cls.TABLE_NAME))

            cursor.execute(create_table_query)
            db_connection.commit()
        finally:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()

    @classmethod
    def _encode_cursor(cls, last_item: AccountingEntry) -> str:
        cursor_data = {
            "data": last_item.data.isoformat() if isinstance(last_item.data, (datetime, date)) else str(last_item.data), 
            "reg_ans": str(last_item.reg_ans),  
            "cd_conta_contabil": last_item.cd_conta_contabil
        }
        return base64.b64encode(json.dumps(cursor_data, cls=JSONEncoder).encode()).decode()


    @classmethod
    def _decode_cursor(cls, cursor: str) -> dict:
        try:
            return json.loads(base64.b64decode(cursor.encode()).decode())
        except:
            return None

    @classmethod
    def get_all(cls, limit: int = 50, cursor: Optional[str] = None) -> Tuple[List[AccountingEntry], Optional[str]]:
        db_connection = None
        cursor_obj = None
        try:
            db_connection = DatabaseRepository.get_connection()
            cursor_obj = db_connection.cursor()

            if cursor:
                cursor_data = cls._decode_cursor(cursor)
                if cursor_data:
                    query = sql.SQL("""
                        SELECT * FROM {table}
                        WHERE (data, reg_ans::VARCHAR, cd_conta_contabil) > (%s, %s, %s)
                        ORDER BY data, reg_ans, cd_conta_contabil
                        LIMIT %s
                    """).format(table=sql.Identifier(cls.TABLE_NAME))
                    cursor_obj.execute(query, (
                        cursor_data["data"],
                        str(cursor_data["reg_ans"]),  
                        cursor_data["cd_conta_contabil"],
                        limit + 1 
                    ))
                else:
                    query = sql.SQL("""
                        SELECT * FROM {table}
                        ORDER BY data, reg_ans, cd_conta_contabil
                        LIMIT %s
                    """).format(table=sql.Identifier(cls.TABLE_NAME))
                    cursor_obj.execute(query, (limit + 1,))
            else:
                query = sql.SQL("""
                    SELECT * FROM {table}
                    ORDER BY data, reg_ans, cd_conta_contabil
                    LIMIT %s
                """).format(table=sql.Identifier(cls.TABLE_NAME))
                cursor_obj.execute(query, (limit + 1,))

            rows = cursor_obj.fetchall()

            entries = []
            for row in rows[:limit]: 
                entry = AccountingEntry(
                    data=row[0],
                    reg_ans=row[1],
                    cd_conta_contabil=row[2],
                    descricao=row[3],
                    vl_saldo_inicial=row[4],
                    vl_saldo_final=row[5]
                )
                entries.append(entry)

            next_cursor = None
            if len(rows) > limit:
                next_cursor = cls._encode_cursor(entries[-1])

            return entries, next_cursor
        finally:
            if cursor_obj:
                cursor_obj.close()
            if db_connection:
                db_connection.close()

    @classmethod
    def get_by_operator(cls, reg_ans: int) -> List[AccountingEntry]:
        db_connection = None
        cursor = None
        try:
            db_connection = DatabaseRepository.get_connection()
            cursor = db_connection.cursor()

            query = sql.SQL("""
                SELECT * FROM {table}
                WHERE reg_ans = %s
                ORDER BY data, cd_conta_contabil
            """).format(table=sql.Identifier(cls.TABLE_NAME))

            cursor.execute(query, (str(reg_ans),))  
            rows = cursor.fetchall()

            entries = []
            for row in rows:
                entry = AccountingEntry(
                    data=row[0],
                    reg_ans=row[1],
                    cd_conta_contabil=row[2],
                    descricao=row[3],
                    vl_saldo_inicial=row[4],
                    vl_saldo_final=row[5]
                )
                entries.append(entry)

            return entries
        finally:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()

    @classmethod
    def bulk_insert(cls, entries: List[dict]) -> int:
        if not entries:
            return 0

        db_connection = None
        cursor = None
        try:
            db_connection = DatabaseRepository.get_connection()
            cursor = db_connection.cursor()

            columns = ['data', 'reg_ans', 'cd_conta_contabil', 'descricao', 'vl_saldo_inicial', 'vl_saldo_final']
            
            for entry in entries:
                entry['reg_ans'] = str(entry['reg_ans'])

            values = [[entry[col] for col in columns] for entry in entries]

            insert_query = sql.SQL("""
                INSERT INTO {table} ({columns})
                VALUES %s
            """).format(
                table=sql.Identifier(cls.TABLE_NAME),
                columns=sql.SQL(', ').join(map(sql.Identifier, columns))
            )

            execute_values(cursor, insert_query, values)
            db_connection.commit()
            
            inserted = len(entries)
            return inserted
        finally:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()
