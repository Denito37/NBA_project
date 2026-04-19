import streamlit as st
import pandas as pd
import numpy as np
from data import queries

def render_team_tab(teams: pd.DataFrame, conn):
    
    NBA_TEAMS = sorted(list(teams.values))
    NBA_TEAMS = np.array(NBA_TEAMS).flatten().tolist()
    selected_team = st.selectbox("Select Team", NBA_TEAMS)

    st.caption(f'{selected_team} Game data 2015 - present')

    _display_team_metrics(selected_team,conn)

    _display_team_chart(teams)

    _display_team_data(teams)

def _display_team_metrics(team: str, conn):
    wins = queries.get_team_l10_wins(team,conn)
    losses = 10 - wins

    FG_PCT_l10 = queries.get_team_stat_l10('FG_PCT',team,conn)
    FG_PCT = queries.get_team_stat('FG_PCT',team,conn)

    FG3_PCT_l10 = queries.get_team_stat_l10('FG3_PCT',team,conn)
    FG3_PCT = queries.get_team_stat('FG3_PCT',team,conn)

    PCT_change = np.round((FG_PCT_l10 - FG_PCT),decimals=3)
    PCT3_change = np.round((FG3_PCT_l10 - FG3_PCT),decimals=3)

    last_10_games,last_10_FG_PCT,last_10_FG3_PCT = st.columns(3)
    last_10_games.metric(
        label= 'Last 10 Games',
        value=f'{wins}W - {losses}L'
    )
    last_10_FG_PCT.metric(
        label='FG_PCT Last 10 Average',
        value= np.round(FG_PCT_l10, decimals=3),
        delta=float(PCT_change)
    )
    last_10_FG3_PCT.metric(
        label='FG3_PCT Last 10 Average',
        value= np.round(FG3_PCT_l10, decimals=3),
        delta=float(PCT3_change)
    )

def _display_team_chart(team: pd.DataFrame):
    st.scatter_chart(
        team,
        x='PTS',
        y='FG_PCT'
    )

def _display_team_data(team: pd.DataFrame):
    st.caption('DATA Table')
    st.dataframe(team)