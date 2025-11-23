from utils.team_state_handler import *
from utils.riddle_giver import *
from utils.config_loader import *
from utils.answer_checker import *
from utils.hint_giver import *
from datetime import datetime
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
            all_riddles = GetRiddleNames()
            solved_riddles = self.team_state["solved_riddles"]
            unsolved_riddles = [x for x in all_riddles if x not in solved_riddles]
            current_riddle = random.choice(unsolved_riddles)
            self.team_state_handler.update(set={"current_riddle" : current_riddle})
            self.log.info('Upadated current riddle for a team in TeamState', team_id= self.team_id, current_riddle=current_riddle)
            return GetRiddle(current_riddle)
        else:
            {"message":"You guys solved all the riddles"}
    
    def start(self):
        if self.team_state['start'] != 'True':
            total_riddle_num = self.riddle_config['total_riddle_num']
            all_riddles = GetRiddleNames()
            current_riddle = random.choice(all_riddles)
            self.team_state_handler.update(set={"start": "True", "current_riddle": current_riddle})
            self.log.info('Initiated the Treasure Hunt', team_id= self.team_id, current_riddle=current_riddle)
            return GetRiddle(current_riddle)
        else:
            return {"message":"You have already started the game!!!"}
        
    def verify_code(self, your_answer):
        riddle_id = self.team_state['current_riddle']
        result = AnswerChecker(riddle_id, your_answer)
        if result =='correct':
            push_data = {
                'solved_riddles' : riddle_id,
                'solved_riddles_time' : str(datetime.now().strftime("%H:%M:%S"))
            }
            inc_data = {'solved_riddle_num':1}
            self.team_state_handler.update(push=push_data,inc=inc_data)
            self.log.info("Updated Team State",team_id=self.team_id, solved_riddle= riddle_id, solved_time=str(datetime.now().strftime("%H:%M:%S")))
            self.get_next_riddle()
        else:
            if self.team_state['wrong_guess']< 3:
                inc_data = {'wrong_guess':1}
                self.team_state_handler.update(inc = inc_data)
                self.log.info("Updated Team State wrong guess",team_id=self.team_id, riddle_id=riddle_id)
                return {"message": "Your answer is wrong!!!"}
            else:
                self.team_state_handler.update(set={'wrong_guess':0})
                return {"message": "You have given 3 consecutive wrong answers!!!"}
            
    def get_hints(self):
        if self.team_state['hints_taken'] < self.riddle_config['total_hint_num']:
            hint = GetHint(self.team_state['current_riddle'])
            self.team_state_handler.update(inc={'hints_taken': 1})
            self.log.info("Successfully provied the hint", team_id=self.team_id, hint= hint)
            return {"hint":hint}
        else:
            return{"message":"You guys used up all the hints"}
            
    def get_team_state(self):
            del self.team_state["start"]
            del self.team_state["team_id"]
            log.info("Sucessfully provided team state", team_id= self.team_id, details = self.team_state)
            return self.team_state
        
if __name__=="__main__":
    team = GameEngine("ce8bd811-e25e-426c-ad84-2edd8f37")
    print(team.start())
    print(team.get_hints())

    print(team.verify_code("12345"))
    print(team.get_team_state())


            
