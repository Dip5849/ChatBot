from utils.team_state_handler import *
from utils.riddle_giver import *
from utils.config_loader import *
from utils.answer_checker import *
from utils.hint_giver import *
import random
from utils.logger import CustomLogger

class GameEngine:
    def __init__(self,team_id):
        self.team_id = team_id
        self.riddle_config = load_config()['riddle_config']
        self.team_state_handler = TeamState(self.team_id)
        self.team_state= self.team_state_handler.load()
        self.log = CustomLogger().get_logger(__file__)
        self.log.info("Initiated GameEngine module", team_id= team_id)
    
    def get_next_riddle(self):
        total_riddle_num = self.riddle_config['total_riddle_num']
        if self.team_state["solved_riddle_num"] <= total_riddle_num:
            all_riddles = list(load_riddle_library().keys())
            solved_riddles = self.team_state["solved_riddles"]
            unsolved_riddles = [x for x in all_riddles if x not in solved_riddles]
            current_riddle = random.choice(unsolved_riddles)
            self.team_state["current_riddle"] = current_riddle
            self.team_state_handler.update(self.team_state)
            self.log.info('Upadated current riddle for a team in TeamState', team_id= self.team_id, current_riddle=current_riddle)
            return GetRiddle(current_riddle)
        else:
            {"message":"You guys solved all the riddles"}
    
    def start(self):
        if self.team_state['start'] != 'True':
            total_riddle_num = self.riddle_config['total_riddle_num']
            all_riddles = list(load_riddle_library().keys())
            current_riddle = random.choice(all_riddles)
            self.team_state["current_riddle"] = current_riddle
            self.team_state["start"] = 'True'
            self.team_state_handler.update(self.team_state)
            self.log.info('Initiated the Treasure Hunt', team_id= self.team_id, current_riddle=current_riddle)
            return GetRiddle(current_riddle)
        else:
            return {"message":"You already started the game!!!"}
        
    def verify_code(self, your_answer):
        riddle_id = self.team_state['current_riddle']
        result = AnswerChecker(riddle_id, your_answer)
        if result =='correct':
            self.team_state['solved_riddle_num'] += 1
            self.team_state['solved_riddles'].append(riddle_id)
            self.team_state_handler.update(self.team_state)
            self.get_next_riddle()
        else:
            if self.team_state['wrong_guess']< 3:
                self.team_state['wrong_guess'] += 1
                self.team_state_handler.update(self.team_state)
                return {"message": "Your answer is wrong!!!"}
            else:
                self.team_state['wrong_guess'] = 0
                self.team_state_handler.update(self.team_state)
                return {"message": "Your answer is wrong!!!"}
            
    def get_hints(self):
        if self.team_state['hints_taken'] < self.riddle_config['total_hint_num']:
            hint = GetHint(self.team_state['current_riddle'])
            self.team_state['hints_taken'] += 1
            self.log.info("Successfully provied the hint", team_id=self.team_id, hint= hint)
            return {"hint":hint}
        else:
            return{"message":"You guys used up all the hints"}
            
    def get_team_state(self):
            del self.team_state["start"]
            log.info("Sucessfully provided team state", team_id= self.team_id, details = self.team_state)
            return self.team_state
        
if __name__=="__main__":
    team = GameEngine('bdd0e7e3-4fbf-431d-b17b-170621a215dc')
    print(team.start())
    print(team.get_hints())
    print(team.verify_code("12345"))
    print(team.get_team_state())


            
