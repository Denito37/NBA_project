"""
    test transformation functions
"""
import pandas as pd
import pytest
from nba_project.pipeline.transform import transform_games,get_average_stats,aggregate_stats

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

def test_get_average_stats_calculates_correctly():
    """
        test get_average_stats calculates per-game averages correctly
    """
    mock_data = pd.DataFrame({
        'PLAYER_ID': [1, 2],
        'FGM': [10, 15],  # Field goals made
        'FG3M': [2, 3],   # 3-pointers made
        'FTM': [8, 6],    # Free throws made
        'GP': [10, 20],   # Games played
        'MIN': [250, 400],
        'REB': [50, 80],
        'AST': [100, 150],
        'STL': [20, 30],
        'BLK': [15, 25]
    })
    
    result = get_average_stats(mock_data)
    
    # Verify per-game calculations for player 1
    # POINTS_PG = (FG3M/GP)*3 + (FGM/GP)*2 + (FTM/GP)
    expected_points_pg_p1 = (2/10)*3 + (10/10)*2 + (8/10)  # 0.6 + 2 + 0.8 = 3.4
    assert abs(result.loc[0, 'POINTS_PG'] - expected_points_pg_p1) < 0.01
    
    # Verify other calculations
    assert abs(result.loc[0, 'MIN_PG'] - 25) < 0.01
    assert abs(result.loc[0, 'REB_PG'] - 5) < 0.01
    assert abs(result.loc[0, 'AST_PG'] - 10) < 0.01


def test_aggregate_stats_groups_and_sorts():
    """
        test aggregate_stats groups by player name and sorts by POINTS_PG
    """
    mock_data = pd.DataFrame({
        'NAME': ['Player A', 'Player A', 'Player B', 'Player B'],
        'MIN_PG': [30, 32, 25, 26],
        'POINTS_PG': [20, 22, 15, 16],
        'AST_PG': [5, 6, 4, 3],
        'REB_PG': [8, 9, 7, 6],
        'STL_PG': [1.5, 1.2, 1, 0.8],
        'BLK_PG': [0.5, 0.6, 0.4, 0.3]
    })
    
    result = aggregate_stats(mock_data)
    
    # Verify grouping (should have 2 unique players)
    assert len(result) == 2
    # Verify sorted by POINTS_PG descending
    assert result.iloc[0]['NAME'] == 'Player A'
    assert result.iloc[1]['NAME'] == 'Player B'
    assert result.iloc[0]['POINTS_PG'] > result.iloc[1]['POINTS_PG']

def test_aggregate_stats_takes_mean():
    """
        test aggregate_stats correctly calculates mean of grouped stats
    """
    mock_data = pd.DataFrame({
        'NAME': ['Player A', 'Player A'],
        'MIN_PG': [30, 40],
        'POINTS_PG': [20, 30],
        'AST_PG': [5, 7],
        'REB_PG': [8, 12],
        'STL_PG': [1.5, 2.5],
        'BLK_PG': [0.5, 1.0]
    })
    
    result = aggregate_stats(mock_data)
    
    assert len(result) == 1
    assert result.loc[0, 'MIN_PG'] == 35  # (30+40)/2
    assert result.loc[0, 'POINTS_PG'] == 25  # (20+30)/2
    assert result.loc[0, 'AST_PG'] == 6  # (5+7)/2