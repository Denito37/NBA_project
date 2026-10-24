import requests
import pandas as pd
from typing import Any
from nba_project.pipeline.logger import get_logger

logger = get_logger('EXTRACTION: ')

class Extract:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def extract_data(self) -> pd.DataFrame:
        """
            extract data from API library functions \n
            Note: function must return data as a pandas dataframe 
        """
        try:
            data:pd.DataFrame = self.endpoint
            if data is None or data.empty:
                logger.warning("data is empty")
            return data
        except TimeoutError as e:
                logger.exception('Timeout Error occured: %s',e)
        except requests.exceptions.ReadTimeout as e:
            logger.exception('Timeout Error occured: %s',e)

    def extract_api(self) -> dict[str,Any]:
        """
            extract data from a REST API \n
            Note: function must return data as JSON
        """
        ...