import yaml
from utils.logger import CustomLogger
from utils.load_db import LoadDB
from utils.config_loader import load_config
log = CustomLogger().get_logger(__file__)

# def LoadDB(collection_name:str):
#     try:
#         team_state_col = db[collection_name]
#         return team_state_col
#     except Exception as e:
#         log.error("Failed to connect db", error = str(e))

def GetRiddle(riddle_name:str):
    log.info('Initialized GetRiddle')
    image_base_url = load_config()['image_base_dir']['path']
    riddles = LoadDB("riddles")
    riddle = riddles.find_one({"id": riddle_name})
    image_file = riddle['image']
    image = f'{image_base_url}{image_file}.png'
    riddle_info = {
        "text":riddle['text'],
        "image": image
    }
    log.info('Successfully returned riddle text and image', riddle_name=riddle_name, id=riddle['id'])
    return riddle_info

def GetRiddleNames():
    riddles = LoadDB("riddles")
    names = riddles.find({}, {"_id": 0, "id":1})
    list = [r['id'] for r in names]
    return list
    

if __name__== '__main__':
    text= GetRiddle('riddle_1')
    print(text)
    print(GetRiddleNames())