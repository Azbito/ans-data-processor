from psycopg2 import sql
from typing import List, Dict, Any, Tuple
from .database import DatabaseRepository
from utils.get_last_period_range import get_last_period_range


class AnalyticsRepository:
    @staticmethod
    def get_top_expenses_by_period(period: str = 'quarterly', limit: int = 10) -> List[Dict[Any, Any]]:
        db_connection = None
        cursor = None
        try:
            db_connection = DatabaseRepository.get_connection()
            cursor = db_connection.cursor()

            sample_accounts_query = sql.SQL("""
                SELECT DISTINCT cd_conta_contabil, descricao 
                FROM accountings 
                WHERE descricao ILIKE %s
                LIMIT 5
            """)

            cursor.execute(sample_accounts_query, ('%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR %',))
            sample_accounts = cursor.fetchall()

            start_date, end_date = get_last_period_range(period)

            query = sql.SQL("""
                SELECT 
                    o.razao_social,
                    o.registro_ans,
                    SUM(dc.vl_saldo_final) as despesa
                FROM 
                    operators o
                    INNER JOIN accountings dc ON o.registro_ans = dc.reg_ans
                WHERE 
                    dc.data BETWEEN %s AND %s
                    AND dc.descricao ILIKE %s
                GROUP BY
                    o.razao_social,
                    o.registro_ans
                ORDER BY 
                    despesa DESC
                LIMIT %s
            """)

            cursor.execute(query, (
                start_date.date(),
                end_date.date(),
                '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR %',
                limit
            ))
            rows = cursor.fetchall()
            print(f"Query returned {len(rows)} results for period {period}")
            if rows:
                print("First result:", rows[0])

            results = []
            for row in rows:
                results.append({
                    "razao_social": row[0],
                    "registro_ans": row[1],
                    "valor_despesa": float(row[2]) if row[2] else 0
                })

            if not results:
                results = [{
                    "debug_info": "No results found",
                    "date_range": {
                        "start": start_date.date().isoformat(),
                        "end": end_date.date().isoformat(),
                        "period": period
                    },
                    "sample_accounts": [
                        {"cd_conta_contabil": acc[0], "descricao": acc[1]} 
                        for acc in sample_accounts
                    ] if sample_accounts else []
                }]

            db_connection.commit()
            return results

        except Exception as e:
            print(f"Error in analytics query for period {period}:", str(e))
            if db_connection:
                db_connection.rollback()
            return [{"error": str(e)}]
        finally:
            if cursor:
                cursor.close()
            if db_connection:
                db_connection.close()
