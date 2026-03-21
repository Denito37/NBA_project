"""
    test transformation functions
"""
import pandas as pd
from src.etl.transform import transform_games

def test_transform_games():
    """
        test transform_games function
    """
    empty_mock_data = pd.DataFrame({
        'SEASON_ID':[],
        'TEAM_NAME':[],
        'GAME_DATE':[],
        'MATCHUP':[],
        'WL':[],
        'PTS':[],
        'FGA':[],
        'FG_PCT':[],
        'FG3A':[],
        'FG3_PCT':[],
        'FTA':[],
        'FT_PCT':[],
        'PLUS_MINUS':[],
        'REB':[],
        'AST':[]
    })
    result = pd.DataFrame({
        'SEASON_ID':[],
        'TEAM_NAME':[],
        'GAME_DATE':[],
        'MATCHUP':[],
        'WL':[],
        'PTS':[],
        'FGA':[],
        'FG_PCT':[],
        'FG3A':[],
        'FG3_PCT':[],
        'FTA':[],
        'FT_PCT':[],
        'PLUS_MINUS':[]
    })
    assert transform_games(empty_mock_data) == result
