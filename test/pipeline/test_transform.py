"""
    test transformation functions
"""
import pandas as pd
import pytest
from nba_project.pipeline.transform import transform_games

def test_transform_games_column_filter():
    """
        test transform_games function column filtering
    """
    mock_data = pd.DataFrame({
        'SEASON_ID':['22025'],
        'TEAM_NAME':['NYK'],
        'GAME_DATE':['3'],
        'MATCHUP':['NYK@BOS'],
        'WL':['W'],
        'PTS':['98'],
        'FGA':['50'],
        'FG_PCT':['0.9'],
        'FG3A':['0'],
        'FG3_PCT':['0'],
        'FTA':['0'],
        'FT_PCT':['0'],
        'PLUS_MINUS':['56'],
        'REB':['9'],
        'AST':['12']
    })
    result = pd.DataFrame({
        'SEASON_ID':['22025'],
        'TEAM_NAME':['NYK'],
        'GAME_DATE':['3'],
        'MATCHUP':['NYK@BOS'],
        'WL':['W'],
        'PTS':['98'],
        'FGA':['50'],
        'FG_PCT':['0.9'],
        'FG3A':['0'],
        'FG3_PCT':['0'],
        'FTA':['0'],
        'FT_PCT':['0'],
        'PLUS_MINUS':['56'],
    })
    pd.testing.assert_frame_equal(transform_games(mock_data),result)


def test_transform_games_handles_missing_columns():
    """
        test transform_games handles KeyError when columns are missing
    """
    incomplete_data = pd.DataFrame({
        'SEASON_ID': ['22025'],
        'TEAM_NAME': ['NYK'],
        # Missing required columns
    })
    
    with pytest.raises(KeyError):
        transform_games(incomplete_data)