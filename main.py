from networksecurity.config.configuration import Configuration
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
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
        data_validation_config=config.get_data_validation_config()
        print(f'\ndata_validation_config:{data_validation_config}')
        data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                       data_validation_config=data_validation_config)
        data_validation_artifact=data_validation.initiate_data_validation()
        print(f'\ndata_validation_artifact:{data_validation_artifact}')
    except Exception as e:
        raise NetworkSecurityException(e,sys)   
    