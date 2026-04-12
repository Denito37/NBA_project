"""
Docstring for view.report
"""
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np

st.title('NBA Performace Report')

# connect to database
conn = sqlite3.connect('NBA.db')

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

teams = pd.read_sql(
    """
    SELECT DISTINCT TEAM_NAME
    FROM Team_data
    WHERE SEASON_ID = 22025
    """
,conn)
NBA_teams = list(teams.values)
NBA_teams = sorted(NBA_teams)
NBA_teams = np.array(NBA_teams).flatten().tolist()

players = pd.read_sql(
    """
        SELECT DISTINCT NAME
        FROM Player_stats
    """
,conn)
NBA_players = sorted(list(players.values))
NBA_players = np.array(NBA_players).flatten().tolist()
# Tabs
tab1, tab2 = st.tabs(['Teams', 'Players'])

# Team Tab
with tab1:
    choice = st.selectbox("Select Team",(NBA_teams))
    # Query Database
    team_df = pd.read_sql_query(f"""
                                SELECT * 
                                FROM Team_data
                                WHERE TEAM_NAME = '{choice}'
                                """
                                ,conn)
    team_win_count_L10 = pd.read_sql_query(f"""
                                        SELECT COUNT(WL) AS TOTAL_WINS
                                        FROM (SELECT * FROM Team_data WHERE TEAM_NAME = '{choice}' LIMIT 10) AS LAST_TEN
                                        WHERE WL = "W" AND TEAM_NAME = '{choice}'
                                        """
                                        ,conn)
    FG_PCT_AVG_L10 = pd.read_sql_query(f"""
                                        SELECT AVG(FG_PCT) AS AVERAGE_FG
                                        FROM (SELECT * FROM Team_data WHERE TEAM_NAME = '{choice}' LIMIT 10) AS LAST_TEN
                                        WHERE TEAM_NAME = '{choice}'
                                        """
                                        ,conn)
    FG_PCT_AVG = pd.read_sql_query(f"""
                                    SELECT AVG(FG_PCT) AS AVERAGE
                                    FROM Team_data
                                    WHERE TEAM_NAME = '{choice}'
                                    """
                                    ,conn)
    FG3_PCT_AVG_L10 = pd.read_sql_query(f"""
                                        SELECT AVG(FG3_PCT) AS AVERAGE_FG
                                        FROM (SELECT * FROM Team_data WHERE TEAM_NAME = '{choice}' LIMIT 10) AS LAST_TEN
                                        WHERE TEAM_NAME = '{choice}'
                                        """
                                        ,conn)
    FG3_PCT_AVG = pd.read_sql_query(f"""
                                    SELECT AVG(FG3_PCT) AS AVERAGE
                                    FROM Team_data
                                    WHERE TEAM_NAME = '{choice}'
                                    """
                                    ,conn)
    st.caption(f'{choice} Game data 2015 - present')

    wins = team_win_count_L10.values[0][0]
    losses = 10 - team_win_count_L10.values[0][0]
    PCT_change = np.round((FG_PCT_AVG_L10.values - FG_PCT_AVG.values), decimals=3)
    PCT3_change = np.round((FG3_PCT_AVG_L10.values - FG3_PCT_AVG.values), decimals=3)

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric(
        label= 'Last 10 Games',
        value= f'{wins} W - {losses} L',
        )
    metric2.metric(
        label='FG_PCT Last 10 Average',
        value= np.round(FG_PCT_AVG_L10.values, decimals=3),
        delta= float(PCT_change[0][0])
    )
    metric3.metric(
        label='FG3_PCT Last 10 Average',
        value= np.round(FG3_PCT_AVG_L10.values, decimals=3),
        delta= float(PCT3_change[0][0])
    )
    st.scatter_chart(
        team_df,
        x = 'PTS',
        y = 'FG_PCT',
    )
    st.caption('Data Table')
    st.dataframe(team_df)

# Player Tab
with tab2:
    choice = st.selectbox("Select Player", (NBA_players))
    st.caption(f"{choice}'s player data")
    player_df = pd.read_sql_query(
        f"""
            SELECT *
            FROM Player_stats
            WHERE NAME = '{choice}'
        """,conn
    )
    PPG = pd.read_sql_query(
            f"""
                SELECT AVG(POINTS_PG)
                FROM Player_stats
                WHERE NAME = '{choice}'
            """
        ,conn)
    ASTPG = pd.read_sql_query(
            f"""
                SELECT AVG(AST_PG)
                FROM Player_stats
                WHERE NAME = '{choice}'
            """
        ,conn)
    REBPG = pd.read_sql_query(
            f"""
                SELECT AVG(REB_PG)
                FROM Player_stats
                WHERE NAME = '{choice}'
            """
        ,conn)
    AVG_PPG = pd.read_sql_query(
            """
                SELECT AVG(POINTS_PG)
                FROM Player_stats
            """
        ,conn)
    AVG_APG = pd.read_sql_query(
            """
                SELECT AVG(AST_PG)
                FROM Player_stats
            """
        ,conn)
    AVG_RPG = pd.read_sql_query(
            """
                SELECT AVG(REB_PG)
                FROM Player_stats
            """
        ,conn)
    PPG_CHANGE = np.round((PPG.values - AVG_PPG.values),decimals=3)
    APG_CHANGE = np.round((ASTPG.values - AVG_APG.values),decimals=3)
    RPG_CHANGE = np.round((REBPG.values - AVG_RPG.values),decimals=3)

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric(
        label='Points PG',
        value= np.round(PPG.values, decimals=3),
        delta= float(PPG_CHANGE[0][0])
    )
    metric2.metric(
        label='Assits PG',
        value= np.round(ASTPG.values, decimals=3),
        delta= float(APG_CHANGE[0][0])
    )
    metric3.metric(
        label='Rebounds PG',
        value= np.round(REBPG.values, decimals=3),
        delta= float(RPG_CHANGE[0][0])
    )
    st.bar_chart(
        melt_table(player_df),
        x='STATS',
        y = 'VALUE',
        color='STATS'
    )