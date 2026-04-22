"""
Entry point for ETL pipeline
"""
import asyncio
import pandas as pd
from typing import Callable
from src.logger import get_logger
from src.etl.extract import extract_team_stats, extract_player_stats
from src.etl.transform import transform_games, transform_player_stats
from src.etl.load import load_to_sql

logger = get_logger('ETL_PROCESS')

async def team_pipeline(extract: Callable[[str|None], pd.DataFrame]
                , transform: Callable[[pd.DataFrame], pd.DataFrame]
                , load: Callable[[str, pd.DataFrame],None]
                , table_name:str
                ) -> None:
    """
        pipeline function
    """
    nba_data = extract()
    cleaned_data = transform(nba_data)
    await load(table_name,cleaned_data)

async def player_pipeline(extract: Callable[[str|None], pd.DataFrame]
                , transform: Callable[[pd.DataFrame, bool | None], pd.DataFrame]
                , load: Callable[[str, pd.DataFrame],None]
                , table_name:str
                , agg:bool = True
                ) -> None:
    """
        pipeline function
    """
    nba_data = extract()
    cleaned_data = transform(nba_data,agg)
    await load(table_name,cleaned_data)

def main():
    """
    ETL Pipeline
    """
    try:
        logger.info("Starting ETL job...")

        asyncio.run(
            team_pipeline(
                extract_team_stats,
                transform_games,
                load_to_sql,
                'Team_data'
            )
        )
        asyncio.run(
            player_pipeline(
                extract_player_stats,
                transform_player_stats,
                load_to_sql,
                'Player_stats',
                agg=True
            )
        )

        logger.info("ETL job completed successfully")
    except TimeoutError as e:
        logger.exception('Pipeline failed: %s',e)

if __name__ == "__main__":
    main()
