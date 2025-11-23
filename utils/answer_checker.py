import json
from utils.logger import CustomLogger
log = CustomLogger().get_logger(__file__)

def AnswerChecker(riddle_name:str,your_answer:str):
    log.info('Initiated AnswerChecker module')
    with open('data/riddle_library/riddles.json') as f:
        riddles = json.load(f)
    correct_ans = riddles[riddle_name]['answer']
    given_ans = your_answer.strip()
    log.info('Successfully checked the given answer', riddle_name= riddle_name, given_answer = given_ans, correct_answer = correct_ans)
    if correct_ans == given_ans:
        return "correct"
    else:
        return "wrong"
    
if __name__=="__main__":
    result = AnswerChecker('riddle_1','12345')
    print(result)