import os
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder
from nba_project.pipeline.extract import Extract
from nba_project.pipeline.load import Load
from nba_project.pipeline.transform import filter_cols
from nba_project.pipeline.logger import get_logger
from dotenv import load_dotenv

load_dotenv()
SUPABASE_PW = os.getenv("SUPABASE_PW")
SUPABASE_ID = os.getenv("SUPABASE_ID")

logger = get_logger('ETL_PROCESS')

game_stats_columns = [
    'SEASON_ID',
    'TEAM_NAME',
    'GAME_DATE',
    'MATCHUP',
    'WL',
    'PTS',
    'FGA',
    'FG_PCT',
    'FG3A',
    'FG3_PCT',
    'FTA',
    'FT_PCT',
    'PLUS_MINUS'
    ]

class Pipeline:
    def __init__(self, source, destination):
        self.extract = Extract(source)
        self.load= Load(destination)
    
    def run(self,table_name) -> None:
        logger.info("ETL Pipeline Starting...")

        data: pd.DataFrame = self.extract.extract_data()
        cleaned_data: pd.DataFrame = filter_cols(data,game_stats_columns)
        self.load.load_to_sql(table_name,cleaned_data)

        logger.info("Data Loaded")


if __name__ == "__main__":
    source:pd.DataFrame = leaguegamefinder.LeagueGameFinder().get_data_frames()[0]
    destination = f"postgresql://postgres:{SUPABASE_PW}@db.{SUPABASE_ID}.supabase.co:5432/postgres"
    test_destination:str = "sqlite:///NBA.db"
    NBA_Pipeline = Pipeline(source, destination)
    NBA_Pipeline.run("NBA_Games")