from utils.team_state_handler import *
from utils.riddle_giver import *
from utils.config_loader import *
from utils.answer_checker import *
from utils.hint_giver import *
from datetime import datetime
import random
from utils.logger import CustomLogger
import traceback

class GameEngine:
    def __init__(self,team_id):
        try:
            self.team_id = team_id
            self.riddle_config = load_config()['riddle_config']
            self.team_state_handler = TeamState(self.team_id)
            # self.team_state= self.team_state_handler.load()
            self.log = CustomLogger().get_logger(__file__)
            self.log.info("Initiated GameEngine module", team_id= team_id)
        except Exception as e:
            self.log.error("worng", error= str(e))
            traceback.print_exc()
    
    def get_next_riddle(self):
        try:
            self.log.info("Initiated get_next_riddle module")
            self.team_state = self.team_state_handler.load()
            total_riddle_num = self.riddle_config['total_riddle_num']
            total_normal_riddle_num = self.riddle_config['total_normal_riddle_num']
            
            if self.team_state["solved_riddle_num"] == total_riddle_num:
                    return {"message":"Congratulations guys !!!\n You have solved all 9 clues. \nThat takes sharp thinking, patience and real skill — and you proved you’ve got all of it. \n\nFor the final clue.... pls go to BUET Cafeteria."}
            
            self.log.info("for check", solved_riddles=self.team_state["solved_riddle_num"], total_riddle_num=total_normal_riddle_num )
            if self.team_state["solved_riddle_num"] < total_normal_riddle_num :
                self.log.info("for check", solved_riddles=self.team_state["solved_riddle_num"], total_riddle_num=total_normal_riddle_num )
                self.log.info("Giving normal random riddle", team_id=self.team_id)
                all_riddles = GetRiddleNames()
                solved_riddles = self.team_state["solved_riddles"]
                unsolved_riddles = [x for x in all_riddles if x not in solved_riddles]
                current_riddle = random.choice(unsolved_riddles)
                self.team_state_handler.update(set={"current_riddle" : current_riddle})
                self.log.info('Upadated current riddle for a team in TeamState', team_id= self.team_id, current_riddle=current_riddle)
                self.log.info("Provided normal random riddle", team_id=self.team_id)
                return GetRiddle(current_riddle)
            
            if self.team_state["solved_riddle_num"] >= total_normal_riddle_num:

                self.log.info("Giving a mandatory riddle", team_id=self.team_id)
                index = int( self.team_state["solved_riddle_num"] - total_normal_riddle_num )
                db = LoadDB("mandatory_riddles")
                riddles = db.find()
                riddle = list(riddles)[index]
                # riddles = [x for x in riddles_db]
                
                current_riddle = riddle['id']
                self.team_state_handler.update(set={"current_riddle" : current_riddle})
                self.log.info("Provided a mandatory riddle", team_id=self.team_id, riddle={
                    "text":riddle['text'],
                    "image":riddle['image']
                } )
                path = load_config()["image_base_dir"]['path']
                image = f"{path}{riddle['image']}.png"
                return {
                    "text":riddle['text'],
                    "image":image
                    }
            return {"message":"something is wrong"}
        except Exception as e:
            self.log.error("error", error=str(e))
            traceback.print_exc()
    
    def start(self):
        try:
            self.team_state = self.team_state_handler.load()
            if self.team_state ==None:
                return {"message":"No user found"}

            if not self.team_state['start']: 
                total_riddle_num = self.riddle_config['total_riddle_num']
                all_riddles = GetRiddleNames()
                current_riddle = random.choice(all_riddles)
                self.team_state_handler.update(set={"start": True, "current_riddle": current_riddle})
                self.log.info('Initiated the Treasure Hunt', team_id= self.team_id, current_riddle=current_riddle)
                return GetRiddle(current_riddle)
            else:
                try:
                    current = self.team_state["current_riddle"]
                    return GetRiddle(current)
                except Exception as e:
                    self.log.error("wrong", error= str(e))

                return GetMandatoryRiddle(current)
        except Exception as e:
            self.log.error("wrong", error= str(e))
            traceback.print_exc()
        
    def verify_code(self, your_answer):
        try:
            self.team_state_handler = TeamState(self.team_id)
            self.team_state = self.team_state_handler.load()
            total_normal_riddle_num = self.riddle_config['total_normal_riddle_num']

            if self.team_state == None:
                return {"message":"No user found"}
            
            if self.team_state["isPenalty"] == True:
                return {"message":"You are in penalty period. Please wait for 30 minutes or Go to BUET cafeteria to reset the penalty."}

            riddle_id = self.team_state['current_riddle']
            if self.team_state["solved_riddle_num"] < total_normal_riddle_num:
                result = AnswerChecker(riddle_id, your_answer,"riddles")
            else:
                result = AnswerChecker(riddle_id, your_answer,"mandatory_riddles")

            if result =='correct':
                push_data = {
                    'solved_riddles' : riddle_id,
                    'solved_riddles_time' : str(datetime.now().strftime("%H:%M:%S"))
                }
                inc_data = {'solved_riddle_num':1}
                self.team_state_handler.update(push=push_data,inc=inc_data)
                self.log.info("Updated Team State",team_id=self.team_id, solved_riddle= riddle_id, solved_time=str(datetime.now().strftime("%H:%M:%S")))
                
                return self.get_next_riddle()
            else:
                total_wrong_guess = self.riddle_config['total_wrong_guess']
                if self.team_state['wrong_guess']< int(total_wrong_guess - 1):
                    inc_data = {'wrong_guess':1}
                    self.team_state_handler.update(inc = inc_data)
                    self.log.info("Updated Team State wrong guess",team_id=self.team_id, riddle_id=riddle_id)
                    
                    return {"message": "Your answer is wrong!!!"}
                else:
                    self.team_state_handler.update(set={'wrong_guess':0})
                    self.team_state_handler.update(set={"isPenalty": True})
                    
                    return {"message": "You have given 3 consecutive wrong answers!!! \nPlease wait for 30 minutes befor trying again or Go to BUET cafeteria to reset the penalty."}
        except Exception as e:
            traceback.print_exc()
            
    # def get_hints(self):
    #     self.team_state = self.team_state_handler.load()
    #     if self.team_state == None:
    #         return {"message":"No user found"}

    #     if self.team_state['hints_taken'] < self.riddle_config['total_hint_num']:
    #         hint = GetHint(self.team_state['current_riddle'])
    #         self.team_state_handler.update(inc={'hints_taken': 1})
    #         self.log.info("Successfully provied the hint", team_id=self.team_id, hint= hint)
    #         return {"hint":hint}
    #     else:
    #         self.team_state_handler.update(set={'hints_taken': 0})
    #         return{"message":"You guys used up all the hints"}
            
    def get_team_state(self):
            try:
                db = LoadDB("teamstate")
                info = db.find_one({"team_id": self.team_id},{
                "_id":0,
                "start": 0
                })
                if info == None:
                    return {"message":"No user found"}
                self.log.info("Sucessfully provided team state", team_id= self.team_id, details = info)
                return info
            except Exception as e:
                self.log.error("Something is wrong", error= str(e))
                traceback.print_exc()
        
# if __name__=="__main__":
#     team = GameEngine("62b3cc1e-c947-4e4d-a3f8-c65e731c80fc")
#     # print(team.start())
#     # print(team.get_hints())

#     # print(team.verify_code("12345"))
#     print(team.get_team_state())


            
