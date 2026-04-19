import streamlit as st
import pandas as pd
import numpy as np
from data import queries


def render_player_tab(players:pd.DataFrame,conn):
    player_names = queries.get_players(conn)
    NBA_players = sorted(list(player_names.values))
    NBA_players = np.array(NBA_players).flatten().tolist()
    selected_player = st.selectbox("Select Player",NBA_players)

    st.caption(f"{selected_player}'s player data")

    _display_player_metrics(selected_player,conn)

    _display_player_chart(players)


def _display_player_metrics(player:str,conn):
    PPG = queries.get_player_PPG(player,conn)
    APG = queries.get_player_APG(player,conn)
    RPG = queries.get_player_RPG(player,conn)

    AVG_PPG = queries.get_avg_player_PPG(conn)
    AVG_APG = queries.get_avg_player_APG(conn)
    AVG_RPG = queries.get_avg_player_RPG(conn)

    PPG_CHANGE = np.round((PPG-AVG_PPG),decimals=3)
    APG_CHANGE = np.round((APG-AVG_APG),decimals=3)
    RPG_CHANGE = np.round((RPG-AVG_RPG),decimals=3)

    Points_PG,Assists_PG,Rebounds_PG = st.columns(3)
    Points_PG.metric(
        label='Points PG',
        value=np.round(PPG,decimals=3),
        delta=float(PPG_CHANGE[0][0])
    )
    Assists_PG.metric(
        label='Assists PG',
        value=np.round(APG,decimals=3),
        delta=float(APG_CHANGE[0][0])
    )
    Rebounds_PG.metric(
        label='Rebounds PG',
        value=np.round(RPG,decimals=3),
        delta=float(RPG_CHANGE[0][0])
    )

def _display_player_chart(players:pd.DataFrame):
    st.bar_chart(
        melt_table(players),
        x='STATS',
        y='VALUE',
        color='STATS'
    )

def melt_table(data: pd.DataFrame) -> pd.DataFrame:
    """
        create table of each stat of a player as a row
    """
    data = data.melt(
    id_vars='NAME',
    var_name='STATS',
    value_name='VALUE'
    )
    return data