import json
from utils.logger import CustomLogger
from utils.load_db import LoadDB
log = CustomLogger().get_logger(__file__)

def AnswerChecker(riddle_name:str,your_answer:str):
    log.info('Initiated AnswerChecker module')
    riddles = LoadDB('riddles')
    correct_ans = riddles.find_one({"id":riddle_name},{"_id":0,"answer":1})["answer"]
    given_ans = your_answer.strip()
    log.info('Successfully checked the given answer', riddle_name= riddle_name, given_answer = given_ans, correct_answer = correct_ans)
    if correct_ans == given_ans:
        return "correct"
    else:
        return "wrong"
    
if __name__=="__main__":
    result = AnswerChecker('riddle_1','12345')
    print(result)