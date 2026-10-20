import sqlite3
from contextlib import contextmanager

DB_PATH = "NBA.db"
URL = 'sqlite:///NBA.db'

# connect to database
@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()