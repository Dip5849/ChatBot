from fastapi import FastAPI
import pydantic
from schemas.models import *
from src.game_engine.engine import GameEngine
from utils.user_and_pass_handler import *
from admin_site.admin import *
from utils.riddle_giver import get_all_riddles
from utils.team_state_handler import TeamState
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials= True,
    allow_methods = ['*'],
    allow_headers = ["*"]
)
app.mount("/images", StaticFiles(directory="data/images"), name="images")

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
    uid = payload.uid
    return create_user(team_name, hashed_pass, player_names,uid)

@app.post("/user/login")
async def login(payload:LogIn):
    team_id = payload.team_id
    password = payload.password
    return hash().verify_pass(team_id, password)

@app.post("/isPenalty")
async def is_penalty(team_id: str, isPenalty:bool):
    team_state_handler = TeamState(team_id)
    if team_state_handler.load() == None:
        return {"message":"No user found"}
    team_state_handler.update(set={"isPenalty": isPenalty})
    return {"message": f"Penalty status updated to {isPenalty} successfully"}

@app.get("/riddles")
async def all_riddles(mandatory:bool):
    return get_all_riddles(mandatory)

@app.get("/info")
async def all_info():
    return fetch_all_team_info()

@app.get("/health")
def health():
    return{"status":"ok"}
    

