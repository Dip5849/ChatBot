import json
from utils.logger import CustomLogger
from utils.load_db import LoadDB
log = CustomLogger().get_logger(__file__)

def GetHint(riddle_name):
    log.info('Initiated GetHint module')
    hints = LoadDB("hints")
    hint_list = hints.find_one({"riddle_name":riddle_name})["hints"]
    hint = hint_list[0]
    log.info('Hint was given successfully', hint = hint, riddle_name = riddle_name)
    return hint
    

if __name__=="__main__":
    hint = GetHint('riddle_1')
    print(hint)