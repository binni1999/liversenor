from dotenv import load_dotenv
import pymongo 
import os
from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variable import MONGODB_URL_KEY
import logging 
import certifi
ca = certifi.where()

load_dotenv()

class MongoDBClient: 
    client = None 

    def __init__(self,database_name:str=DATABASE_NAME)-> None: 
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY) 
                logging.info(f"Retrieved MongoDB URL: {mongo_db_url}")
                if "localhost" in mongo_db_url: 
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
                else: 
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca) #TLS/SSL certificate

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise e

