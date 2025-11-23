import os
import uuid
import json
from utils.logger import CustomLogger
from passlib.context import CryptContext
from utils.load_db import LoadDB
log = CustomLogger().get_logger(__file__)
pwd_cxt = CryptContext(schemes=['bcrypt'])

class hash():
    def __init__(self):
        self.usersDB = LoadDB("user")

    def bcrypt(password):
        try:
            log.info("Successfully hased the password")
            return pwd_cxt.hash(password)
        except Exception as e:
            log.error("Failed to hash the pass", error= str(e))
    
    def verify_pass(self,user_id,plain_pass):
        try:
            hashed_pass = self.usersDB.find_one({"user_id":user_id})['hashed_pass']
            if hashed_pass == None:
                return {"message":"No user found"}
                
            result = pwd_cxt.verify(plain_pass,hashed_pass)

            if result:
                log.info("Successfully verified the password", result= "Login Successful")
                return {"message":"Login Successful"}
            else:
                log.info("Successfully verified the password", result= "Incorrect password")
                return {"message":"Incorrect password"}
        except Exception as e:
            log.error("Failed to verify password", error= str(e))
        
def create_user(team_name,team_pass,player_names):
    try:
        usersDB = LoadDB("user")
        uid = uuid.uuid4()
        user_dict = {
            "user_id": str(uid),
            "user_name": team_name,
            "hashed_pass": team_pass
        }
        usersDB.insert_one(user_dict)
        log.info("Successfully created new user", team_id=uid, team_name= team_name, player_names= player_names)
    except Exception as e:
        log.error("Failed to create new user", team_name= team_name, player_names= player_names, error = str(e))

    try:
        team_state_dict = {
            "team_name": team_name,
            "team_id": str(uid),
            "players": [x for x in player_names],
            "hints_taken": 0,
            "solved_riddle_num": 0,
            "solved_riddles": [],
            "solved_riddles_time": [],
            "current_riddle": "",
            "wrong_guess": 0,
            "start": "False"
            }
        team_stateDB = LoadDB("teamstate")
        team_stateDB.insert_one(team_state_dict)
        log.info("Succefully created team state for new user", team_id=uid, team_name= team_name, player_names= player_names)

        return {"team_id":str(uid), "team_name": team_name}
    except Exception as e:
        log.error("Failed to create new team_state", team_name= team_name, player_names= player_names, error = str(e))
    
if __name__=="__main__":
    hashed = hash.bcrypt("123456dip")
    print(hashed)
    dict = create_user('One',hashed,['dip','eshan','you'])
    uid = dict["team_id"]
    print(id)
    print(hash().verify_pass(user_id=uid,plain_pass="123456dip"))
        
