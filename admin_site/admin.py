import json
from utils.load_db import LoadDB
from utils.logger import CustomLogger
log = CustomLogger().get_logger(__file__)


def fetch_all_team_info():
    try:
        log.info("Fetching all team data")
        states = LoadDB('teamstate')
        all_info = states.find({},{"_id":0,
            "team_name": 1,
            "team_id": 1,
            "players": 1,
            "hints_taken": 1,
            "solved_riddle_num": 1,
            "solved_riddles": 1,
            "solved_riddles_time": 1,
            "current_riddle": 1,
            "wrong_guess": 1,
            "start": 1
            })
        info = {"info": [i for i in all_info]}
        log.info("Returned all team data", info = info)
        return info
    except Exception as e:
        log.error("Failed to fetch all data", error = str(e))
        
        
if __name__=="__main__":
    print(fetch_all_team_info())
