"""
Entry point for ETL pipeline
"""
from src.utils.logger import get_logger
from src.extract.extract import extract
from src.transform.transform import transform
from src.load.load import load_to_sql

logger = get_logger('ETL_PROCESS')

def main():
    """
    ETL Pipeline
    """
    try:
        logger.info("Starting ETL job...")

        data = extract()

        cleaned_data = transform(data)

        load_to_sql(cleaned_data)
        
        logger.info("ETL job completed successfully")
    except Exception as e:
        logger.error(f'Pipeline failed: {e}')

if __name__ == "__main__":
    main()
