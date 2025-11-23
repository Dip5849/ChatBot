from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.logger import CustomLogger
log = CustomLogger().get_logger(__file__)
uri = "mongodb+srv://dip58:7hnWb6zHIGnT9j87@cluster0.zuxcv9y.mongodb.net/?appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

def LoadDB(collection_name:str):
    try:
        db = client["RiddleDB"]
        team_state_col = db[collection_name]
        log.info("Successfully connected to db", db_name= collection_name)
        return team_state_col
    except Exception as e:
        log.error("Failed to connect db", error = str(e))
