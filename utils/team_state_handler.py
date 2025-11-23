import json
from utils.logger import CustomLogger
log = CustomLogger().get_logger(__file__)

class TeamState:
    def __init__(self,team_id):
        self.team_id = team_id

    def load(self):
        log.info('Initialized TeamState module', team_id = self.team_id)
        path = f'data/team_state/{self.team_id}.json'
        with open(path) as f:
            teams = json.load(f)
        return teams

    def update(self,data,indent=3):
        path = f'data/team_state/{self.team_id}.json'
        with open(path,'w') as f:
            json.dump(data,f,indent=indent)


if __name__=='__main__':
    state = TeamState('team_1').load()
    print(state['players'])