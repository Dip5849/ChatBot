import os
import uuid
import json
from utils.logger import CustomLogger
from passlib.context import CryptContext
log = CustomLogger().get_logger(__file__)
pwd_cxt = CryptContext(schemes=['bcrypt'])

class hash():
    def bcrypt(password):
        try:
            log.info("Successfully hased the password")
            return pwd_cxt.hash(password)
        except Exception as e:
            log.error("Failed to hash the pass", error= str(e))
    
    def verify_pass(user_id,plain_pass):
        try:
            hashed_pass = ''
            with open("data/user_info/user.json") as f:
                users = json.load(f)['users']
            for user in users:
                if user['user_id'] == user_id:
                    hashed_pass = user["hashed_pass"]
            if hashed_pass == '':
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
        uid = uuid.uuid4()
        with open("data/user_info/user.json") as f:
            users = json.load(f)
        user_dict = {
            "user_id": str(uid),
            "user_name": team_name,
            "hashed_pass": team_pass
        }
        users['users'].append(user_dict)
        with open("data/user_info/user.json", 'w') as f:
            json.dump(users,f,indent=3)
        log.info("Successfully created new user", team_id=uid, team_name= team_name, player_names= player_names)
    except Exception as e:
        log.error("Failed to create new user", team_name= team_name, player_names= player_names, error = str(e))

    try:
        path = f'data/team_state/{str(uid)}.json'
        os.makedirs(os.path.dirname(path), exist_ok=True)
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
        with open(path,'w') as f:
            json.dump(team_state_dict,f,indent=3)
        log.info("Succefully created team state for new user", team_id=uid, team_name= team_name, player_names= player_names)

        return {"team_id":str(uid), "team_name": team_name}
    except Exception as e:
        log.error("Failed to create new team_state", team_name= team_name, player_names= player_names, error = str(e))
    
if __name__=="__main__":
    hashed = hash.bcrypt("123456dip")
    print(hashed)
    dict = create_user('One',hashed,['dip','eshan','you'])
    id = dict["team_id"]
    print(id)
    print(hash.verify_pass(id,"123456dip"))
        
