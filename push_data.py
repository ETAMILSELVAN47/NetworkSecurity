import os
import sys
import json
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import numpy as np
import pandas as pd
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import certifi

load_dotenv()

ca=certifi.where()

DATABASE='Tamilselvan0'
COLLECTION='Network_Data'
CSV_DATA_FILE_PATH='Network_Data\phisingData.csv'

class NetworkDataExtract():
    def __init__(self):
        try:
            self.mongo_db_url=os.getenv(key='MONGO_DB_URL')
            self.database=DATABASE
            self.collection=COLLECTION
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(self,file_path:str):
        try:
            if os.path.isfile(path=file_path):
                data=pd.read_csv(file_path)
                records=json.loads(data.to_json(orient='records'))
                return records
            else:
                raise NetworkSecurityException(f'File not found {file_path}',sys)                
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
    
    def insert_data_mongodb(self,records):
        try:
            self.mongo_client=MongoClient(self.mongo_db_url)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(documents=records)
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    


if __name__=='__main__':
    network_obj=NetworkDataExtract()
    records=network_obj.csv_to_json_converter(file_path=CSV_DATA_FILE_PATH)
    print(f'records:{records}')
    if len(records)>0:
        total_records=network_obj.insert_data_mongodb(records=records)
        print(f'No.of.Records:{total_records}')