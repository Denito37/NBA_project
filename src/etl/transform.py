"""
    transformations
"""
import pandas as pd
from src.logger import get_logger
from src.etl.extract import extract_player_id

logger = get_logger('TRANFORMATION_PROCESS: ')
game_stats_columns = ['SEASON_ID','TEAM_NAME','GAME_DATE','MATCHUP','WL','PTS',
                'FGA','FG_PCT','FG3A','FG3_PCT','FTA','FT_PCT','PLUS_MINUS']

def transform_games(data: pd.DataFrame, season_id: str | None = None) -> pd.DataFrame:
    """
    transform game data
    """
    try:
        if season_id is not None:
            data = data.loc[data['SEASON_ID'] == season_id,:]
    except pd.errors.DataError as e:
        logger.error('Data error occured: %s', e)
    return data[game_stats_columns]


def transform_player_stats(data: pd.DataFrame, agg:bool = True) -> pd.DataFrame:
    """
        transform player data stats
    """
    try:
        removed_id = 1630828
        players_id = extract_player_id()
        id_list = list(players_id.keys())
        id_list.remove(removed_id)
        for player_id, player_name in players_id.items():
            if player_id != removed_id:
                data.loc[data['PLAYER_ID'] == player_id, 'NAME'] = player_name
        if agg:
            data = aggregate_stats(get_average_stats(data))
        else:
            data = get_average_stats(data)
    except pd.errors.DataError as e:
        logger.error('Data Error occured: %s',e)
    except KeyError as e:
        logger.error('KeyError occured: %s',e)
    return data

# Helper Functions

def get_average_stats(data: pd.DataFrame) -> pd.DataFrame:
    """
        get average of essential stats
    """
    FGMA = (data['FGM']/data['GP']) * 2
    FG3MA = (data['FG3M']/data['GP']) * 3
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

def aggregate_stats(data: pd.DataFrame) -> pd.DataFrame:
    """
        aggregate essential stats
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