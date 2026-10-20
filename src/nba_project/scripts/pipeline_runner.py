import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder
from nba_project.pipeline.logger import get_logger
from nba_project.pipeline.extract import Extract
from nba_project.pipeline.transform import transform_games
from nba_project.pipeline.load import Load
from nba_project.config import POSTGRESQL_URL

logger = get_logger('ETL_PROCESS')

class Pipeline:
    def __init__(self, source, destination):
        self.extract = Extract(source)
        self.load= Load(destination)
    
    def run(self,table_name) -> None:
        logger.info("ETL Pipeline Starting...")

        data: pd.DataFrame = self.extract.extract_data()
        cleaned_data: pd.DataFrame = transform_games(data)
        self.load.load_to_sql(table_name,cleaned_data)

        logger.info("Data Loaded")


if __name__ == "__main__":
    source:pd.DataFrame = leaguegamefinder.LeagueGameFinder().get_data_frames()[0]
    test_destination:str = "sqlite:///NBA.db"
    NBA_Pipeline = Pipeline(source, test_destination)
    NBA_Pipeline.run("NBA_Games")