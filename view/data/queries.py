import pandas as pd

# Team_data Queries
def get_teams(current_season: str, conn) -> pd.DataFrame:
    query = "SELECT DISTINCT TEAM_NAME FROM Team_data WHERE SEASON_ID = ?"
    return pd.read_sql_query(query, conn, params=(current_season,))

def get_team(team_name: str, conn) -> pd.DataFrame:
    query = "SELECT * FROM Team_data WHERE TEAM_NAME = ?"
    return pd.read_sql_query(query, conn, params=(team_name,))

def get_team_l10_wins(team_name: str, conn) -> int:
    query = """SELECT COUNT(WL) AS TOTAL_WINS FROM 
               (SELECT * FROM Team_data WHERE TEAM_NAME = ? LIMIT 10) AS LAST_TEN
                WHERE WL = 'W'"""
    return pd.read_sql_query(query, conn, params=(team_name,)).values[0][0]

def get_avg_team_stat(stat_name:str, conn) -> float:
    query = "SELECT AVG(?) FROM Team_data"
    return pd.read_sql_query(query,conn,params=(stat_name,)).values

def get_team_stat(stat_name:str,team_name:str,conn) -> float:
    query = "SELECT AVG(?) FROM Team_data WHERE TEAM_NAME = ?"
    return pd.read_sql_query(query,conn,params=(stat_name,team_name)).values

def get_team_stat_l10(stat_name:str,team_name:str,conn) -> float:
    query = "SELECT AVG(?) FROM (SELECT * FROM Team_data WHERE TEAM_NAME = ? LIMIT 10) AS LAST_TEN"
    return pd.read_sql_query(query,conn,params=(stat_name,team_name)).values

# Player_stats Queries
def get_players(conn) -> pd.DataFrame:
    query = " SELECT DISTINCT NAME FROM Player_stats"
    return pd.read_sql_query(query, conn)

def get_players_stats(conn) -> pd.DataFrame:
    query = " SELECT * FROM Player_stats"
    return pd.read_sql_query(query, conn)

def get_player(player_name:str, conn)-> pd.DataFrame:
    query = "SELECT * FROM Player_stats WHERE NAME = ?"
    return pd.read_sql_query(query,conn,params=(player_name,))

def get_avg_player_PPG(conn) -> float:
    query ="SELECT AVG(POINTS_PG) FROM Player_stats"
    return pd.read_sql_query(query,conn).values

def get_avg_player_APG(conn) -> float:
    query ="SELECT AVG(AST_PG) FROM Player_stats"
    return pd.read_sql_query(query,conn).values

def get_avg_player_RPG(conn) -> float:
    query ="SELECT AVG(REB_PG) FROM Player_stats"
    return pd.read_sql_query(query,conn).values

def get_player_PPG(player_name:str,conn) -> float:
    query = "SELECT AVG(POINTS_PG) FROM Player_stats WHERE NAME = ?"
    return pd.read_sql_query(query,conn,params=[player_name]).values

def get_player_APG(player_name:str,conn) -> float:
    query = "SELECT AVG(AST_PG) FROM Player_stats WHERE NAME = ?"
    return pd.read_sql_query(query,conn,params=[player_name]).values

def get_player_RPG(player_name:str,conn) -> float:
    query = "SELECT AVG(REB_PG) FROM Player_stats WHERE NAME = ?"
    return pd.read_sql_query(query,conn,params=[player_name]).values
