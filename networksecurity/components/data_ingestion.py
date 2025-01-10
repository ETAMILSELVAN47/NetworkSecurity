from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import pymongo
from dotenv import load_dotenv
load_dotenv()
import certifi
ca=certifi.where()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self)->pd.DataFrame:
        try:
            logging.info('Read data from Mongo DB')
            mongo_db_url=MONGO_DB_URL
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(mongo_db_url)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df.drop(columns="_id",inplace=True)

            df.replace({"na":np.nan},inplace=True)  

            return df  

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_data_into_feature_store(self,dataframe:pd.DataFrame)-> pd.DataFrame:
        try:
            logging.info('Store the raw data')
            raw_data_dir=self.data_ingestion_config.raw_data_dir
            raw_data_file_name=self.data_ingestion_config.raw_data_file_name

            raw_data_file_path=os.path.join(raw_data_dir,raw_data_file_name)

            os.makedirs(raw_data_dir,exist_ok=True)

            dataframe.to_csv(raw_data_file_path,index=False,header=True)

            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def split_data_into_train_test(self,dataframe:pd.DataFrame):
        try:
            logging.info('Split the data into Train and Test')
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)

            ingested_train_data_dir=self.data_ingestion_config.ingested_train_data_dir
            ingested_train_data_file_name=self.data_ingestion_config.ingested_train_data_file_name

            train_data_file_path=os.path.join(ingested_train_data_dir,ingested_train_data_file_name)

            ingested_test_data_dir=self.data_ingestion_config.ingested_test_data_dir
            ingested_test_data_file_name=self.data_ingestion_config.ingested_test_data_file_name
             
            test_data_file_path=os.path.join(ingested_test_data_dir,ingested_test_data_file_name)

            os.makedirs(ingested_train_data_dir,exist_ok=True)
            os.makedirs(ingested_test_data_dir,exist_ok=True)

            train_set.to_csv(train_data_file_path,index=False,header=True)
            test_set.to_csv(test_data_file_path,index=False,header=True) 

            return train_data_file_path,test_data_file_path

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info('Data Ingestion has been started.')
            # Read data from Mongo DB            
            df=self.export_collection_as_dataframe()
            # Store the raw data            
            df=self.export_data_into_feature_store(dataframe=df)
            # Split the data into Train and Test            
            train_data_file_path,test_data_file_path=self.split_data_into_train_test(dataframe=df)

            data_ingestion_artifact=DataIngestionArtifact(train_data_file_path=train_data_file_path,
                                                          test_data_file_path=test_data_file_path,
                                                          is_ingested=True,
                                                          message='Data Ingestion Completed')
            logging.info('Data Ingestion has been completed.')

            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
