import json
from utils.logger import CustomLogger
log = CustomLogger().get_logger(__file__)

def GetHint(riddle_name):
    log.info('Initiated GetHint module')
    with open('data/hint_library/hints.json') as f:
        hint_library = json.load(f)
    hints = hint_library[riddle_name]['hints']
    hint = hints[0]
    log.info('Hint was given successfully', hint = hint, riddle_name = riddle_name)
    return hint
    

if __name__=="__main__":
    hint = GetHint('riddle_1')
    print(hint)