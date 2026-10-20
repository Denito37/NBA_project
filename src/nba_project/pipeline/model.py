from pydantic.dataclasses import dataclass
from datetime import date

@dataclass
class NBA_Games:
    Season_id:str
    Team_name:str
    Game_date:date
    MatchUp:str
    WL:str
    PTS:int
    FGA:int
    FG_PCT:float
    FG3A:int
    FG3_PCT:float
    FTA:int
    FT_PCT:float
    PLUS_MINUS:float