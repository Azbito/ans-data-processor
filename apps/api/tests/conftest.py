import os
import sys
import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def mock_datetime_now(monkeypatch):
    class MockDateTime:
        @classmethod
        def now(cls):
            return datetime(2025, 3, 30)
    
    monkeypatch.setattr('datetime.datetime', MockDateTime)
    return MockDateTime

@pytest.fixture
def mock_db_connection(monkeypatch):
    class MockCursor:
        def __init__(self):
            self.executed_query = None
            self.fetchall_result = []
            self.fetchone_result = None
        
        def execute(self, query, params=None):
            self.executed_query = (query, params)
        
        def fetchall(self):
            return self.fetchall_result
        
        def fetchone(self):
            return self.fetchone_result
        
        def close(self):
            pass

    class MockConnection:
        def __init__(self):
            self.cursor_obj = MockCursor()
            self.autocommit = False
        
        def cursor(self):
            return self.cursor_obj
        
        def commit(self):
            pass
        
        def rollback(self):
            pass
        
        def close(self):
            pass

    def mock_get_connection():
        return MockConnection()
    
    monkeypatch.setattr('repositories.database.DatabaseRepository.get_connection', mock_get_connection)
    return MockConnection()
