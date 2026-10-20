import pandas as pd
from nba_project.pipeline.logger import get_logger

logger = get_logger('TRANFORMATION_PROCESS: ')
game_stats_columns = ['SEASON_ID','TEAM_NAME','GAME_DATE','MATCHUP','WL','PTS',
                'FGA','FG_PCT','FG3A','FG3_PCT','FTA','FT_PCT','PLUS_MINUS']

def transform_games(data: pd.DataFrame) -> pd.DataFrame:
    cleaned_data = []
    try:
        if data is not None:
            cleaned_data = data[game_stats_columns]
        return cleaned_data
    except pd.errors.DataError as e:
        logger.exception('Data error occurred: %s', e)
        raise
    except KeyError as e:
        logger.exception('KeyError occurred: %s',e)
        raise