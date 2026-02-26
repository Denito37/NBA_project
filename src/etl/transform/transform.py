"""
    transformations
"""
import pandas as pd

games_columns = ['SEASON_ID','TEAM_NAME','GAME_DATE','MATCHUP','WL','PTS','PLUS_MINUS']
players_columns = ['id','full_name','is_active','team']
player_stats_columns = ['PLAYER_ID','NAME','SEASON_ID','TEAM_ABBREVIATION',
                        'PLAYER_AGE','FGM','FG3M','REB','AST','GS','GP']

def transform_games(data:pd.DataFrame, season_id:str|None = None):
    """
    transform game data
    """
    try:
        if season_id is not None:
            data = data.loc[data['SEASON_ID'] == season_id,:]
    except pd.errors.DataError as e:
        print(f'Data error occured: {e}')
    return data[games_columns]

def transform_player(data:pd.DataFrame, players_list:list[str]|None = None):
    """
        transform player data
    """
    try:
        if players_list is not None:
            data = data.loc[data['full_name'].isin(players_list),:]  
    except pd.errors.DataError as e:
        print(f'Data Error occured: {e}')
    return data[players_columns]

def transform_player_stats(data:pd.DataFrame,players_list:list[str]|None = None):
    """
        transform player data stats
    """
    try:
        if players_list is not None:
            players_id = get_players_id(data, players_list)
            for player_id, player_name in players_id.items():
                data.loc[data['PLAYER_ID'] == player_id, 'NAME'] = player_name
    except pd.errors.DataError as e:
        print(f'Data Error occured: {e}')
    return data[player_stats_columns]

def get_players_id(data:pd.DataFrame,players_list:list[str]):
    """
        get dictionary of player's names & their id
    """
    player_id = [data['id'].loc[data['full_name'] == player] for player in players_list]
    player_id = [id.values[0] for id in player_id]

    id_to_name = dict(zip(player_id,players_list))

    return id_to_name

def get_average_stats():
    """
        get
    """
    