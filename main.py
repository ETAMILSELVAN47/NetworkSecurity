from networksecurity.config.configuration import Configuration
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import sys

if __name__=='__main__':
    try:
        config=Configuration()
        data_ingestion_config=config.get_data_ingestion_config()
        print(f'data_ingestion_config:{data_ingestion_config}')
        
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(f'\ndata_ingestion_artifact:{data_ingestion_artifact}')
        #----------------------------------------------------------------#
    except Exception as e:
        raise NetworkSecurityException(e,sys)   
    