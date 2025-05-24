import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

Mongo_db_URL=os.getenv("MONGODB_URL")
print(Mongo_db_URL)

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from Networksecurity.exception.exception import securityException 
from Networksecurity.logging.logger import logger

class NetworkdataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise securityException(e, sys)
        
    def csv_to_json_converter(self,csv_file_path):
        try:
            logger.info("Reading CSV file from: {}".format(csv_file_path))
            data=pd.read_csv(csv_file_path)
            data.reset_index(drop=True, inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            logger.info("Successfully converted CSV to JSON with {} records.".format(len(records)))
            return records
        except Exception as e:
            raise securityException(e, sys)
        

    def insert_data_to_mongodb(self,records,database_name,collection_name):
        try:
            logger.info("Connecting to MongoDB to insert data at {}".format(Mongo_db_URL))
            self.database_name=database_name
            self.collection_name=collection_name
            self.records=records
            self.client=pymongo.MongoClient(Mongo_db_URL, tlsCAFile=ca)
            self.db=self.client[self.database_name]
            self.collection=self.db[self.collection_name] 
            logger.info("Inserting {} records into {}.{}".format(len(self.records), self.database_name, self.collection_name))
            self.collection.insert_many(self.records)
            logger.info("Data inserted successfully into {}.{}".format(self.database_name, self.collection_name))
            return len(self.records)
        except Exception as e:
            raise securityException(e, sys)


if __name__ == "__main__":
    FILE_PATH="Networkdata\phisingData.csv"
    Database="MMMdatabase"
    Collection="Network_phishingData"
    object=NetworkdataExtract()
    logger.info("Converting CSV to JSON...")
    records=object.csv_to_json_converter(csv_file_path=FILE_PATH)
    print("{}".format(records))
    logger.info("Inserting data into MongoDB...")
    no_of_records=object.insert_data_to_mongodb(records=records, database_name=Database, collection_name=Collection)
    print("{}".format(no_of_records))  
    logger.info("Data conversion completed and records successfully inserted into MongoDB.")

    