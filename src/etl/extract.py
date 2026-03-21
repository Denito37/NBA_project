"""
Docstring for src.extract.extract
"""
from nba_api.stats.endpoints import playercareerstats, leaguegamefinder
from nba_api.stats.static import players
import pandas as pd
from src.logger import get_logger

logger = get_logger('EXTRACTION STARTED')


def extract_team_stats() -> pd.DataFrame:
    """
    extract data on NBA team's games
    optional team_code parameter to filter data based on what team played
    """
    try:
        team_games = leaguegamefinder.LeagueGameFinder().get_data_frames()[0]
    except TimeoutError as e:
        logger.error('Timeout Error occured: %s',e)
        raise

    return team_games

def extract_player_stats() -> pd.DataFrame:
    """
    extracts data on list of player's id provided
    optional team_code parameter to filter data based on when they player on a certain team

    """
    try:
        player_dict = extract_player_id()
        id_list = list(player_dict.keys())
        team_df = pd.DataFrame()
        for player in id_list:
            player_career = playercareerstats.PlayerCareerStats(player_id=player)
            player_stats = player_career.career_totals_regular_season.get_data_frame()
            team_df = pd.concat([team_df,player_stats], ignore_index=True)
    except TimeoutError as e:
        logger.error('Timeout Error occured: %s',e)
        raise
    return team_df

# helper functions
def extract_player_id():
    """
        extract dictionary of all active players in the NBA ids
    """
    player_list = players.get_players()
    player_df = pd.DataFrame(player_list)
    active_player_df = player_df.loc[player_df['is_active'] == True]

    return dict(zip(active_player_df['id'], active_player_df['full_name']))
