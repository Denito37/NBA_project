"""
Docstring for src.extract.extract
"""
from nba_api.stats.endpoints import playercareerstats, leaguegamefinder
from nba_api.stats.static import teams, players
import pandas as pd

def extract_team_stats(team_code:str) -> pd.DataFrame:
    """
    extract data on NBA team's games
    """
    try:
        data = pd.DataFrame(teams.get_teams())
        team_id = data.loc[data['abbreviation'] == team_code,'id']
        team_games = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id).get_data_frames()[0]
    except TimeoutError as e:
        print(f'Timeout Error occured: {e}')

    return team_games

def extract_players() -> pd.DataFrame:
    """
    extract data on all players
    """
    try:
        data = pd.DataFrame(players.get_players())
    except TimeoutError as e:
        print(f'Timeout Error occured: {e}')
    return data

def extract_players_stats(players_id:list[str], team_code:str = '') -> pd.DataFrame:
    """
    extracts data on list of player's id provided
    optional team_code parameter to filter data based on when they player on a certain team

    """
    try:
        team_df = pd.DataFrame()
        for player in players_id:
            player_career = playercareerstats.PlayerCareerStats(player_id=player)
            player_stats = player_career.career_totals_regular_season.get_data_frame()
            if team_code != '':
                player_team_stats = player_stats.loc[player_stats['TEAM_ABBREVIATION'] == team_code]
                team_df = pd.concat([team_df,player_team_stats], ignore_index=True)
            else:
                team_df = pd.concat([team_df,player_stats], ignore_index=True)
    except TimeoutError as e:
        print(f'Timeout Error occured: {e}')
    return team_df
