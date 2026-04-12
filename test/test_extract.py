"""
    test extraction functions
"""
import pandas as pd
from unittest.mock import patch
from src.etl.extract import extract_team_stats,extract_player_id,extract_player_stats

def test_extract_team_stats_returns_dataframe():
    """
        test extract_team_stats returned type
    """
    with patch('src.etl.extract.leaguegamefinder.LeagueGameFinder') as mock:
        mock_df = pd.DataFrame({'GAME_ID': [1, 2], 'TEAM_NAME': ['Lakers', 'Celtics']})
        mock.return_value.get_data_frames.return_value = [mock_df]

        result = extract_team_stats()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

def test_extract_player_stats_returns_dataframe():
    """
        test extract_player_stats returned type
    """
    with patch('src.etl.extract.extract_player_id') as mock_ids, \
        patch('src.etl.extract.playercareerstats.PlayerCareerStats') as mock_stats:
        
        mock_ids.return_value = {123: 'Player One', 1630828: 'Player Two'}
        mock_df = pd.DataFrame({'PLAYER_ID': [123], 'PTS': [1000]})
        mock_stats.return_value.career_totals_regular_season.get_data_frame.return_value = mock_df

        result = extract_player_stats()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

def test_extract_player_id_returns_dict():
    """
        test extract_player_id returned type
    """
    with patch('src.etl.extract.players.get_players') as mock:
        mock.return_value = [
            {'id': 1, 'full_name': 'Player A', 'is_active': True},
            {'id': 2, 'full_name': 'Player B', 'is_active': False}
        ]

        result = extract_player_id()
        assert isinstance(result, dict)
        assert result == {1: 'Player A'}