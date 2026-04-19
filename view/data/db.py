import sqlite3
from config import DB_PATH
from contextlib import contextmanager

# connect to database
@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()