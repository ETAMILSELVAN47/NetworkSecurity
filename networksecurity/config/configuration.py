from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.constant import *
from networksecurity.utils import read_yaml_file
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig



class Configuration:
    def __init__(self,
                 config_file_path:str=CONFIG_FILE_PATH,
                 current_time_stamp:str=CURRENT_TIME_STAMP)-> None:
        try:
            self.config_info=read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config=self.get_training_pipeline_config()
            self.timestamp=current_time_stamp
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_ingestion_config(self)-> DataIngestionConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir=os.path.join(artifact_dir,
                                                     DATA_INGESTION_DIR_KEY,
                                                     self.timestamp)
            data_ingestion_config=self.config_info[DATA_INGESTION_CONFIG_KEY]

            database_name=data_ingestion_config[DATA_INGESTION_DATABASE_NAME_KEY]
            collection_name=data_ingestion_config[DATA_INGESTION_COLLECTION_NAME_KEY]
            raw_data_dir=os.path.join(data_ingestion_artifact_dir,
                                      data_ingestion_config[DATA_INGESTION_RAW_DATA_DIR_KEY])
            raw_data_file_name=data_ingestion_config[DATA_INGESTION_RAW_DATA_FILE_NAME_KEY]

            ingested_data_dir=os.path.join(data_ingestion_artifact_dir,
                                           data_ingestion_config[DATA_INGESTION_INGESTED_DATA_DIR_KEY])
            
            ingested_train_data_dir=os.path.join(ingested_data_dir,
                                                 data_ingestion_config[DATA_INGESTION_INGESTED_TRAIN_DATA_DIR_KEY])
            
            ingested_test_data_dir=os.path.join(ingested_data_dir,
                                                data_ingestion_config[DATA_INGESTION_INGESTED_TEST_DATA_DIR_KEY]
                                                )
            ingested_train_data_file_name=data_ingestion_config[DATA_INGESTION_INGESTED_TRAIN_DATA_FILE_NAME_KEY]
            ingested_test_data_file_name=data_ingestion_config[DATA_INGESTION_INGESTED_TEST_DATA_FILE_NAME_KEY]
            
            train_test_split_ratio= data_ingestion_config[DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO]
            
            data_ingestion_config=DataIngestionConfig(database_name=database_name,
                                                      collection_name=collection_name,
                                                      raw_data_dir=raw_data_dir,
                                                      raw_data_file_name=raw_data_file_name,
                                                      ingested_data_dir=ingested_data_dir,
                                                      ingested_train_data_dir=ingested_train_data_dir,
                                                      ingested_test_data_dir=ingested_test_data_dir,
                                                      ingested_train_data_file_name=ingested_train_data_file_name,
                                                      ingested_test_data_file_name=ingested_test_data_file_name,
                                                      train_test_split_ratio=train_test_split_ratio)
            return data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)    


    def get_data_validation_config(self)->DataValidationConfig:
        try:

            artifact_dir=self.training_pipeline_config.artifact_dir
            data_validation_artifact_dir=os.path.join(artifact_dir,
                                                      DATA_VALIDATION_DIR_KEY,
                                                      self.timestamp)
            
            data_validation_config=self.config_info[DATA_VALIDATION_CONFIG_KEY]

            schema_file_path=os.path.join(data_validation_config[DATA_VALIDATION_SCHEMA_DIR_KEY],
                                          data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])

            valid_data_dir=os.path.join(data_validation_artifact_dir,
                                        data_validation_config[DATA_VALIDATION_VALID_DATA_DIR_KEY]
                                        )
            
            invalid_data_dir=os.path.join(data_validation_artifact_dir,
                                          data_validation_config[DATA_VALIDATION_INVALID_DATA_DIR_KEY]
                                          )
            
            
            
            drift_report_file_path=os.path.join(data_validation_artifact_dir,
                                                data_validation_config[DATA_VALIDATION_DRIFT_REPORT_DIR_KEY],
                                                data_validation_config[DATA_VALIDATION_REPORT_FILE_NAME_KEY])


            data_validation_config=DataValidationConfig(
                                 schema_file_path=schema_file_path,
                                 valid_data_dir=valid_data_dir,
                                 invalid_data_dir=invalid_data_dir,
                                 drift_report_file_path=drift_report_file_path)
            
            return data_validation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)        
        
    def get_training_pipeline_config(self)-> TrainingPipelineConfig:
        try:
            training_pipeline_config=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir=os.path.join(
                training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )
            training_pipeline_config=TrainingPipelineConfig(artifact_dir=artifact_dir)

            return training_pipeline_config
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)    


