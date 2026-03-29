"""
    test transformation functions
"""
import pandas as pd
from src.etl.transform import transform_games

def test_transform_games():
    """
        test transform_games function
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
