import os
import yaml
from utils.logger import CustomLogger
log = CustomLogger().get_logger(__file__)

def ImageHandler(riddle_name):
    log.info('Initialized ImageHandler')
    with open('config/config.yaml') as f:
        file = yaml.safe_load(f)
    base_dir = file['image_base_dir']['path']
    file = f'{riddle_name}.png'
    image_path = os.path.join(base_dir,file)
    log.info('Returned image path successfully', image_path=image_path, riddle_name=riddle_name)
    return image_path

if __name__=="__main__":
    path = ImageHandler('riddle_1')
    print(path)
