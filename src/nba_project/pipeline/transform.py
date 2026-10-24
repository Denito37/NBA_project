import pandas as pd
from nba_project.pipeline.model import NBA_Games
from pydantic import ValidationError
from nba_project.pipeline.logger import get_logger

logger = get_logger('TRANFORMATION_PROCESS: ')

def filter_cols(data: pd.DataFrame, cols:list[str]) -> pd.DataFrame:
    """
        transform dataframe to include only selected columns
    """
    cleaned_data = []
    try:
        if data is not None:
            cleaned_data = data[cols]
        return cleaned_data
    except pd.errors.DataError as e:
        logger.exception('Data error occurred: %s', e)
        raise
    except KeyError as e:
        logger.exception('KeyError occurred: %s',e)
        raise

def get_team_averages(data: pd.DataFrame) -> pd.DataFrame:
    """
        transform dataframe to be the average stats of each team each season
    """
    ...

def validate_data(data:pd.DataFrame):
    """
        validate data in dataframe
    """
    ...