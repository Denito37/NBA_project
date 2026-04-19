"""
Entry Point for Streamlit NBA Dashboard
"""
import streamlit as st
import pandas as pd
from components import player_tab
from components import team_tab
from data.db import get_db_connection
from data import queries
from config import SEASON_ID


def main():
    st.title('NBA Team Performance Dashboard')

    with get_db_connection() as conn:
        teams:pd.DataFrame = queries.get_teams(SEASON_ID,conn)
        players:pd.DataFrame = queries.get_players_stats(conn)

        tab1,tab2 = st.tabs(['Teams', 'Players'])

        with tab1: 
            team_tab.render_team_tab(teams,conn)

        with tab2:
            player_tab.render_player_tab(players,conn)

if __name__ == "__main__":
    main()