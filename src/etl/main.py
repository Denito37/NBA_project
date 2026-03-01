"""
Entry point for ETL pipeline
"""
import asyncio
from typing import Callable
import pandas as pd
from src.utils.logger import get_logger
from src.etl.extract.extract import extract_team_stats
from src.etl.transform.transform import transform_games
from src.etl.load.load import load_to_sql

logger = get_logger('ETL_PROCESS')

async def pipeline(extract: Callable[[str|None], pd.DataFrame]
                , transform: Callable[[pd.DataFrame, str|None], pd.DataFrame]
                , load: Callable[[str, pd.DataFrame],None]
                , table_name:str) -> None:
    """
        pipeline function
    """
    nba_data = extract()
    cleaned_data = transform(nba_data)
    await load(table_name,cleaned_data)

def main():
    """
    ETL Pipeline
    """
    try:
        logger.info("Starting ETL job...")
        asyncio.run(
            pipeline(
                extract_team_stats,
                transform_games,
                load_to_sql,
                'Team_data'
            )
        )

        logger.info("ETL job completed successfully")
    except TimeoutError as e:
        logger.error('Pipeline failed: %s',e)

if __name__ == "__main__":
    main()
