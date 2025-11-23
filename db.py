from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.logger import CustomLogger
log = CustomLogger().get_logger(__file__)
uri = "mongodb+srv://dip58:7hnWb6zHIGnT9j87@cluster0.zuxcv9y.mongodb.net/?appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["RiddleDB"]

def LoadDB(collection_name:str):
    try:
        team_state_col = db[collection_name]
        return team_state_col
    except Exception as e:
        log.error("Failed to connect db", error = str(e))

riddles = LoadDB('user')
riddle = riddles.insert_one(
   {
         "user_id": "ce8bd811-e25e-426c-ad84-2edd8f377060",
         "user_name": "One",
         "hashed_pass": "$2b$12$8bc2KTxKmsg4WcGUbQ7IBu73SIyb0YDnAxCK3Io0Xn7D0NZn8iwcS"
      }
)