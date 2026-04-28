"""
    test load with SQLite
"""
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from src.logger import get_logger

logger = get_logger('LOADING_PROCESS: ')
URL = 'sqlite:///NBA.db'
engine = create_engine(URL)

with engine.connect() as conn:
    conn.execute(text('PRAGMA journal_mod = WAL;'))

Base = declarative_base()
Base.metadata.create_all(engine)

async def load_to_sql(table_name: str, data_frame: pd.DataFrame) -> None:
    """
        load data to sql database
    """
    if data_frame is not None and len(data_frame) > 0:
        data_frame.to_sql(
            name = table_name,
            con=engine,
            if_exists='replace',
            index=False
        )
    else:
        logger.warning('No data loaded')
        raise
