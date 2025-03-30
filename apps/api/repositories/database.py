import os
import psycopg2
from psycopg2.extensions import connection
from typing import Optional


class DatabaseRepository:
    @staticmethod
    def get_connection() -> connection:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host="db",
            port=5432
        )
