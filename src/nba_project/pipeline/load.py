import pandas as pd
from sqlalchemy import create_engine
from nba_project.pipeline.logger import get_logger

logger = get_logger('LOADING_PROCESS: ')

class Load:
    def __init__(self, db_path):
        self.destination = db_path
        self.engine = create_engine(self.destination)

    def load_to_sql(
                        self,
                        table_name: str,
                        data_frame: pd.DataFrame
                        ) -> None:
        """
            load data into an SQL database \n
            Note: data must be in a dataframe
        """
        
        if data_frame is not None and len(data_frame) > 0:
            data_frame.to_sql(
                        name = table_name,
                        con=self.engine,
                        if_exists='replace',
                        index=False
                    )
        else:
            logger.info('No data loaded')