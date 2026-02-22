"""
Entry point for ETL pipeline
"""
from src.utils.logger import get_logger
from src.etl.extract.extract import extract_players_stats, extract_team_stats
from src.etl.transform.transform import transform
from src.etl.load.load import load_to_sql

logger = get_logger('ETL_PROCESS')

def main():
    """
    ETL Pipeline
    """
    try:
        logger.info("Starting ETL job...")

        knicks_team_data = extract_team_stats('NYK')
        player_data = extract_players_stats([],'NYK')

        cleaned_team_data = transform(knicks_team_data)
        cleaned_player_data = transform(player_data)

        load_to_sql(cleaned_team_data)
        load_to_sql(cleaned_player_data)
        
        logger.info("ETL job completed successfully")
    except TimeoutError as e:
        logger.error('Pipeline failed: %s',e)

if __name__ == "__main__":
    main()
