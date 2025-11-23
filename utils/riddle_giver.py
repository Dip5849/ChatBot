import json
from utils.logger import CustomLogger
log = CustomLogger().get_logger(__file__)

def GetRiddle(riddle_name:str):
    log.info('Initialized GetRiddle')
    with open('data/riddle_library/riddles.json') as f:
        riddles = json.load(f)
    riddle = riddles[riddle_name]
    image_file = riddle['image']
    image = f'{image_file}.png'
    riddle_info = {
        "text":riddle['text'],
        "image": image
    }
    log.info('Successfully returned riddle text and image', riddle_name=riddle_name, id=riddle['id'])
    return riddle_info

def load_riddle_library():
    with open('data/riddle_library/riddles.json') as f:
        riddles = json.load(f)
    return riddles
if __name__== '__main__':
    text= GetRiddle('riddle_1')
    print(text)