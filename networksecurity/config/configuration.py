from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.constant import *
from networksecurity.utils import read_yaml_file
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig
from networksecurity.entity.config_entity import DataTransformationConfig,ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig


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

    def get_data_transformation_config(self)->DataTransformationConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir

            data_transformation_artifact_dir=os.path.join(artifact_dir,
                                                          DATA_TRANSFORMATION_DIR_NAME,
                                                          self.timestamp )
            
            data_transformation_config=self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]
            
            transformed_train_dir=os.path.join(data_transformation_artifact_dir,
                                                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
                                                data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY])
        

            transformed_test_dir=os.path.join(data_transformation_artifact_dir,
                                              data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
                                              data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY])

            preprocessor_obj_file_path=os.path.join(data_transformation_artifact_dir,
                                                    data_transformation_config[DATA_TRANSFORMATION_PREPROCESSOR_DIR_KEY],
                                                    data_transformation_config[DATA_TRANSFORMATION_PREPROCESSOR_OBJ_FILE_NAME_KEY])
            

            data_transformation_config=DataTransformationConfig(transformed_train_dir=transformed_train_dir,
                                     transformed_test_dir=transformed_test_dir,
                                     preprocessor_obj_file_path=preprocessor_obj_file_path)
            
            return data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e,sys) 

    def get_model_trainer_config(self)->ModelTrainerConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir

            model_trainer_artifact_dir=os.path.join(artifact_dir,
                                                    MODEL_TRAINER_DIR_NAME,
                                                    self.timestamp)
            
            model_trainer_config=self.config_info[MODEL_TRAINER_CONFIG_KEY]

            trained_model_file_path=os.path.join(model_trainer_artifact_dir,
                                                 model_trainer_config[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
                                                 model_trainer_config[MODEL_TRAINER_MODEL_FILE_NAME_KEY])
            
            base_accuracy=model_trainer_config[MODEL_TRAINER_BASE_ACCURACY_KEY]

            model_config_file_path=os.path.join(model_trainer_config[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
                                                model_trainer_config[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY])

            model_trainer_config=ModelTrainerConfig(trained_model_file_path=trained_model_file_path,
                               base_accuracy=base_accuracy,
                               model_config_file_path=model_config_file_path)
            
            return model_trainer_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir

            model_evaluation_artifact_dir=os.path.join(artifact_dir,
                                                       MODEL_EVALUATION_DIR_NAME)
            
            model_evaluation_config=self.config_info[MODEL_EVALUATION_CONFIG_KEY]

            model_evaluation_file_path=os.path.join(model_evaluation_artifact_dir,                                                    
                                                    model_evaluation_config[MODEL_EVALUATION_FILE_NAME_KEY])

            model_evaluation_config=ModelEvaluationConfig(model_evaluation_file_path=model_evaluation_file_path,
                                                         timestamp=self.timestamp)
            
            return model_evaluation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)       

    def get_model_pusher_config(self)->ModelPusherConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir

            model_pusher_config=self.config_info[MODEL_PUSHER_CONFIG_KEY]

            model_pusher_artifact_dir=os.path.join(artifact_dir,
                                                   MODEL_PUSHER_DIR_NAME,
                                                   model_pusher_config[MODEL_PUSHER_MODEL_EXPORT_DIR_KEY]                                                   
                                                )
            
            model_pusher_config=ModelPusherConfig(export_model_dir_path=model_pusher_artifact_dir)

            return model_pusher_config
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


