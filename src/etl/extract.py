"""
Docstring for src.extract.extract
"""
import requests
import time
import pandas as pd
from nba_api.stats.endpoints import playercareerstats, leaguegamefinder
from nba_api.stats.static import players
from src.logger import get_logger

logger = get_logger('EXTRACTION: ')


def extract_team_stats() -> pd.DataFrame:
    """
    extract data on NBA team's games
    optional team_code parameter to filter data based on what team played
    """
    try:
        team_games = leaguegamefinder.LeagueGameFinder().get_data_frames()[0]
        return team_games
    except TimeoutError as e:
        logger.exception('Timeout Error occured: %s',e)
    except requests.exceptions.ReadTimeout as e:
        logger.exception('Timeout Error occured: %s',e)


def extract_player_stats() -> pd.DataFrame:
    """
    extracts data on list of player's id provided
    optional team_code parameter to filter data based on when they player on a certain team

    """
    team_df = pd.DataFrame()
    # data point causes errors id: 1630828
    removed_id = 1630828
    player_dict = extract_player_id()
    id_list = list(player_dict.keys())
    id_list.remove(removed_id)
    try:
        for i , player in enumerate(id_list):
            if i % 10 == 0:
                time.sleep(5)
            player_career = playercareerstats.PlayerCareerStats(player_id=player)
            player_stats = player_career.career_totals_regular_season.get_data_frame()
            if not player_stats.isnull().values.any() and not player_stats.empty:
                team_df = pd.concat([team_df,player_stats], ignore_index=True)
        return team_df
    except TimeoutError as e:
        logger.exception('Timeout Error occured: %s',e)
    except KeyError as e:
        logger.exception('keyerror Error occured: %s',e)
    except requests.exceptions.ReadTimeout as e:
        logger.exception('Timeout Error occured: %s',e)

# helper functions
def extract_player_id() -> dict:
    """
        extract dictionary of all 
        active NBA players' id & full name
    """
    try:
        player_list = players.get_players()
        player_df = pd.DataFrame(player_list)
        active_player_df = player_df.loc[player_df['is_active'].eq(True)]

        return dict(zip(active_player_df['id'], active_player_df['full_name']))
    except KeyError as e:
        logger.exception('keyerror Error occured: %s',e)
    except requests.exceptions.ReadTimeout as e:
        logger.exception('Timeout Error occured: %s',e)
