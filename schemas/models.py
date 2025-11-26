from pydantic import BaseModel, Field
from typing import List, Optional,Literal

class GameAction(BaseModel):
    team_id : str
    command : Optional[Literal['start','hint','team_info']] = None
    code : Optional[str] = None

class Create_User(BaseModel):
    team_name: str
    players: List[str]
    uid: str
    password: str

class LogIn(BaseModel):
    team_id: str
    password: str
