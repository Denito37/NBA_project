"""
Docstring for src.extract.extract
"""
import requests
import time
import pandas as pd
from nba_api.stats.endpoints import playercareerstats, leaguegamefinder
from nba_api.stats.static import players
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
            data = self.endpoint
            if data is None or data.empty:
                logger.warning("data is empty")
            return data
        except TimeoutError as e:
                logger.exception('Timeout Error occured: %s',e)
        except requests.exceptions.ReadTimeout as e:
            logger.exception('Timeout Error occured: %s',e)


# OLD FUNCTIONS
def extract_team_stats() -> pd.DataFrame:
    """
    extract data on NBA team's games
    """
    try:
        team_games:pd.DataFrame = leaguegamefinder.LeagueGameFinder().get_data_frames()[0]
        if team_games is None or team_games.empty:
            logger.warning('Teams data is empty')
        return team_games
    except TimeoutError as e:
        logger.exception('Timeout Error occured: %s',e)
    except requests.exceptions.ReadTimeout as e:
        logger.exception('Timeout Error occured: %s',e)


def extract_player_stats() -> pd.DataFrame:
    """
    extracts data on list of player's id provided

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
