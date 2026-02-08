from src.utils.logger import get_logger
from src.extract.extract import extract
from src.transform.transform import transform

logger = get_logger('ETL_PROCESS')

def main():
    try:
        logger.info("Starting ETL job...")

        data = extract()

        cleaned_data = transform(data)

        print(cleaned_data)

        logger.info("ETL job completed successfully")
    except Exception as e:
        logger.error(f'Pipeline failed: {e}')

if __name__ == "__main__":
    main()