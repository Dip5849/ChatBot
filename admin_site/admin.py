import json
from utils.load_db import LoadDB


def fetch_all_team_info():
    states = LoadDB('teamstate')
    all_info = states.find()
    info = [i for i in all_info]
    return info
        
if __name__=="__main__":
    print(fetch_all_team_info())
