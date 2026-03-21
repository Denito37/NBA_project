"""
    test extraction functions
"""
import pandas as pd
from src.etl.extract import extract_team_stats


def test_extract_team_stats():
    """
        test extract_team_stats
    """
    assert extract_team_stats() == type(pd.DataFrame)
