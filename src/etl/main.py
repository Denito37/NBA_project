"""
Entry point for ETL pipeline
"""
from src.utils.logger import get_logger
from src.etl.extract.extract import extract_players_stats, extract_team_stats
from src.etl.transform.transform import transform_player_stats, transform_games
from src.etl.load.load import load_to_sql

logger = get_logger('ETL_PROCESS')

def pipeline(extract, transform, load, table_name) -> None:
    """
        pipeline function
    """
    data = extract
    cleaned_data = transform(data)
    load(table_name,cleaned_data)

    return 0

def main():
    """
    ETL Pipeline
    """
    try:
        logger.info("Starting ETL job...")

        pipeline(
            extract_team_stats('NYK'),
            transform_games,
            load_to_sql,
            'Team_data'
        )
        pipeline(
            extract_players_stats([],'NYK'),
            transform_player_stats,
            load_to_sql,
            'Player_data'
        )
        logger.info("ETL job completed successfully")
    except TimeoutError as e:
        logger.error('Pipeline failed: %s',e)

if __name__ == "__main__":
    main()
