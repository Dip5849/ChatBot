from fastapi import FastAPI
import pydantic
from schemas.models import *
from src.game_engine.engine import GameEngine
from utils.user_and_pass_handler import *



app = FastAPI()

@app.post("/game")
async def game_action(payload: GameAction):
    team_id = payload.team_id
    command = payload.command
    engine = GameEngine(team_id)

    if command == "start":
        return engine.start()
    elif command == "team_info":
        return engine.get_team_state()
    elif command == "hint":
        return engine.get_hints()
    else:
        return engine.verify_code(payload.code) 

@app.post("/user/create_user")
async def create_users(payload:Create_User):
    team_name = payload.team_name
    hashed_pass = hash.bcrypt(payload.password)
    player_names = payload.players
    create_user(team_name, hashed_pass, player_names)

@app.post("/user/login")
async def login(payload:LogIn):
    hash.verify_pass(payload.team_id,payload.password)
    

