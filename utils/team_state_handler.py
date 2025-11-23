import json
from utils.logger import CustomLogger
from utils.load_db import LoadDB
log = CustomLogger().get_logger(__file__)

class TeamState:
    def __init__(self,team_id):
        self.team_id = team_id
        self.team_state = LoadDB('teamstate')
        log.info('Initialized TeamState module', team_id = self.team_id)

    def load(self):
        team = self.team_state.find_one({"team_id": self.team_id})
        log.info("Loaded team_state successfully", team_id= self.team_id)
        return team

    def update(self,set=None,push=None, inc=None, indent=3):
        if set:
            self.team_state.update_one({"team_id": self.team_id},{"$set": set})
        elif push:
            self.team_state.update_one({"team_id": self.team_id},{"$push":push})
        elif inc:
            self.team_state.update_one({"team_id": self.team_id},{"$inc":inc})
        else:
            return None
        log.info("Updated team_state successfully", team_id= self.team_id, set=set, push= push, inc= inc)


if __name__=='__main__':
    state = TeamState('ce8bd811-e25e-426c-ad84-2edd8f377060')
    data = {"hints_taken":1,
            "wrong_guess":1}
    state.update(data)