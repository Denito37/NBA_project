"""
    transformations
"""
import pandas as pd
from src.logger import get_logger
from src.etl.extract import extract_player_id

logger = get_logger('TRANFORMATION_PROCESS: ')
game_stats_columns = ['SEASON_ID','TEAM_NAME','GAME_DATE','MATCHUP','WL','PTS',
                'FGA','FG_PCT','FG3A','FG3_PCT','FTA','FT_PCT','PLUS_MINUS']

def transform_games(data: pd.DataFrame) -> pd.DataFrame:
    """
    transform game data to contain only needed columns
    """
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


def transform_player_stats(data: pd.DataFrame, agg:bool = True) -> pd.DataFrame:
    """
        transform player data stats to enrich data on player's stats
    """
    # data point causes errors id: 1630828
    removed_id = 1630828
    players_id = extract_player_id()
    id_list = list(players_id.keys())
    if removed_id in id_list:
        id_list.remove(removed_id)
    try:
        for player_id, player_name in players_id.items():
            if  data is not None and player_id != removed_id:
                data.loc[data['PLAYER_ID'] == player_id, 'NAME'] = player_name
        if agg:
            return aggregate_stats(get_average_stats(data))
        else:
            return get_average_stats(data)
    except pd.errors.DataError as e:
        logger.exception('Data Error occurred: %s',e)
        raise
    except KeyError as e:
        logger.exception('KeyError occurred: %s',e)
        raise

# Helper Functions

def get_average_stats(data: pd.DataFrame) -> pd.DataFrame:
    """
        get average of essential stats for NBA players
    """
    points_per_field_goal = 2
    points_per_field_goal_3 = 3
    try:
        if len(data) > 0:
            FGMA = (data['FGM']/data['GP']) * points_per_field_goal
            FG3MA = (data['FG3M']/data['GP']) * points_per_field_goal_3
            FTMA = data['FTM']/data['GP']
            new_df = data.assign(
                POINTS_PG = FG3MA + FGMA + FTMA,
                MIN_PG = data['MIN']/data['GP'],
                REB_PG = data['REB']/data['GP'],
                AST_PG = data['AST']/data['GP'],
                STL_PG = data['STL']/data['GP'],
                BLK_PG = data['BLK']/data['GP'],
            )

            return new_df
    except pd.errors.DataError as e:
        logger.exception('Data Error occurred: %s',e)
        raise
    except KeyError as e:
        logger.exception('KeyError occurred: %s',e)
        raise
    except TypeError as e:
        logger.exception('TypeError occured: %s',e)
        raise
    except ZeroDivisionError as e:
        logger.exception('Error occurred: %s',e)
        raise

def aggregate_stats(data: pd.DataFrame) -> pd.DataFrame:
    """
        aggregate essential stats for NBA players
    """
    player_stats_avg_df = data.groupby('NAME',as_index=False).agg({
    'MIN_PG':'mean',
    'POINTS_PG':'mean',
    'AST_PG':'mean',
    'REB_PG':'mean',
    'STL_PG':'mean',
    'BLK_PG':'mean'
    })
    player_stats_avg_df = player_stats_avg_df.sort_values(by='POINTS_PG', ascending=False)

    return player_stats_avg_df