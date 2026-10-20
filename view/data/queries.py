import pandas as pd

NBA_GAMES_TABLE = "NBA_Games"

# Team_data Queries
def get_team_stats(conn) -> pd.DataFrame:
    query = f""" 
            SELECT *
            FROM {NBA_GAMES_TABLE}
        """
    return pd.read_sql_query(query,conn)

def get_teams(current_season: str, conn) -> pd.DataFrame:
    query = f"SELECT DISTINCT TEAM_NAME FROM {NBA_GAMES_TABLE} WHERE SEASON_ID = ?"
    return pd.read_sql_query(query, conn, params=(current_season,))

def get_team(team_name: str, conn) -> pd.DataFrame:
    query = f"SELECT * FROM {NBA_GAMES_TABLE} WHERE TEAM_NAME = ?"
    return pd.read_sql_query(query, conn, params=(team_name,))

def get_team_l10_wins(team_name: str, conn) -> int:
    query = f"""SELECT COUNT(WL) AS TOTAL_WINS FROM 
               (SELECT * FROM {NBA_GAMES_TABLE} WHERE TEAM_NAME = ? LIMIT 10) AS LAST_TEN
                WHERE WL = 'W'"""
    return pd.read_sql_query(query, conn, params=(team_name,)).values[0][0]

def get_avg_team_stat(stat_name:str, conn) -> float:
    query = f"SELECT AVG(?) FROM {NBA_GAMES_TABLE}"
    return pd.read_sql_query(query,conn,params=(stat_name,)).values

def get_team_stat(stat_name:str,team_name:str,conn) -> float:
    query = f"SELECT AVG(?) FROM {NBA_GAMES_TABLE} WHERE TEAM_NAME = ?"
    return pd.read_sql_query(query,conn,params=(stat_name,team_name)).values

def get_team_stat_l10(stat_name:str,team_name:str,conn) -> float:
    query = f"SELECT AVG(?) FROM (SELECT * FROM {NBA_GAMES_TABLE} WHERE TEAM_NAME = ? LIMIT 10) AS LAST_TEN"
    return pd.read_sql_query(query,conn,params=(stat_name,team_name)).values