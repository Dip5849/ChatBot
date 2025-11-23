import json


def fetch_all_team_info():
    all_info = {"info":[]}
    with open("data/user_info/user.json", 'r') as f:
        users = json.load(f)["users"]
    for user in users:
        user_id = user["user_id"]
        path = f"data/team_state/{user_id}.json"
        with open(path,'r') as f:
            info = json.load(f)
        all_info["info"].append(info)
    return all_info
        
if __name__=="__main__":
    print(fetch_all_team_info())
