from pydantic import BaseModel, Field
from typing import List, Optional,Literal

class GameAction(BaseModel):
    team_id : str
    command : Optional[Literal['start','code','team_info']]
    code : Optional[str]

class Create_User(BaseModel):
    team_name: str
    players: List[str]
    password: str

class LogIn(BaseModel):
    team_id: str
    password: str
