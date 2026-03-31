"""
    transformations
"""
import pandas as pd
from src.logger import get_logger
from src.etl.extract import extract_player_id

logger = get_logger('TRANFORMATION_PROCESS: ')
game_stats_columns = ['SEASON_ID','TEAM_NAME','GAME_DATE','MATCHUP','WL','PTS',
                'FGA','FG_PCT','FG3A','FG3_PCT','FTA','FT_PCT','PLUS_MINUS']
player_stats_columns = ['PLAYER_ID','NAME','SEASON_ID','TEAM_ABBREVIATION',
                        'PLAYER_AGE','FGM','FG3M','REB','AST','GS','GP']

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


def transform_player_stats(data: pd.DataFrame) -> pd.DataFrame:
    """
        transform player data stats
    """
    try:
        players_id = extract_player_id()
        id_list = list(players_id.keys())
        id_list = sorted(id_list)
        removed_id = id_list.pop(289)
        for player_id, player_name in players_id.items():
            if player_id != removed_id:
                data.loc[data['PLAYER_ID'] == player_id, 'NAME'] = player_name
        data = data[player_stats_columns]
    except pd.errors.DataError as e:
        logger.error('Data Error occured: %s',e)
    except KeyError as e:
        logger.error('KeyError occured: %s',e)
    return get_average_stats(data)

# Helper Functions

def get_average_stats(data: pd.DataFrame) -> pd.DataFrame:
    """
        get average of essential stats
    """
    data['FGMA'] = (data['FGM']/data['GP']) * 2
    data['FG3MA'] = (data['FG3M']/data['GP']) * 3
    data['FTMA'] = data['FTM']/data['GP']
    data['POINTS_PG'] = data['FG3MA'] + data['FGMA'] + data['FTMA']
    data['REB_PG'] = data['REB']/data['GP']
    data['AST_PG'] = data['AST']/data['GP']

    player_stats_avg_df = data.groupby('NAME',as_index=False).agg({
    'REB_PG':'mean',
    'AST_PG':'mean',
    'POINTS_PG': 'mean',
    })
    player_stats_avg_df = player_stats_avg_df.sort_values(by='POINTS_PG', ascending=False)

    return player_stats_avg_df
