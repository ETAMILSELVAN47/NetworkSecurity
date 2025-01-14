from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import (DataIngestionConfig,
                                                  DataValidationConfig,
                                                  DataTransformationConfig,
                                                  ModelTrainerConfig,
                                                  ModelEvaluationConfig,
                                                  ModelPusherConfig)

from networksecurity.entity.artifact_entity import (DataIngestionArtifact,
                                                    DataValidationArtifact,
                                                    DataTransformationArtifact,
                                                    ModelTrainerArtifact,
                                                    ModelEvaluationArtifact,
                                                    ModelPusherArtifact)

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import Modeltrainer
from networksecurity.components.model_evaluation import ModelEvaluation
from networksecurity.components.model_pusher import ModelPusher
import os,sys
from networksecurity.config.configuration import Configuration
from networksecurity.cloud import S3Sync
from networksecurity.constant import *

class Pipeline:
    def __init__(self,config:Configuration):
        try:            
            self.config=config
            self.s3_sync=S3Sync()
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info(f"{'<<'*10} Data Ingestion has been started.{'>>'*10}")
            data_ingestion_config=self.config.get_data_ingestion_config()
            logging.info(f'data_ingestion_config:{data_ingestion_config}')
            data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info(f'data_ingestion_artifact:{data_ingestion_artifact}')
            logging.info(f"{'<<'*10} Data Ingestion has been completed,{'>>'*10}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            logging.info(f"{'<<'*10} Data Validation has been started.{'>>'*10}")
            data_validation_config=self.config.get_data_validation_config()
            logging.info(f'data_validation_config:{data_validation_config}')
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                           data_validation_config=data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info(f'data_validation_artifact:{data_validation_artifact}')
            logging.info(f"{'<<'*10} Data Validation has been completed.{'>>'*10}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataIngestionArtifact)->DataTransformationArtifact:
        try:            
            logging.info(f"{'<<'*10} Data Transformation has been started.{'>>'*10}")
            data_validation_config=self.config.get_data_validation_config()            
            data_transformation_config=self.config.get_data_transformation_config()
            logging.info(f'data_transformation_config:{data_transformation_config}')
            data_transformation=DataTransformation(data_validation_config=data_validation_config,
                               data_validation_artifact=data_validation_artifact,
                               data_transformation_config=data_transformation_config)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info(f'data_transformation_artifact:{data_transformation_artifact}')
            logging.info(f"{'<<'*10} Data Transformation has been completed.{'>>'*10}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            logging.info(f"{'<<'*10} Model Trainer has been started.{'>>'*10}")
            model_trainer_config=self.config.get_model_trainer_config()     
            logging.info(f'model_trainer_config:{model_trainer_config}')       
            model_trainer=Modeltrainer(data_transformation_artifact=data_transformation_artifact,
                         model_trainer_config=model_trainer_config)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info(f'model_trainer_artifact:{model_trainer_artifact}')
            logging.info(f"{'<<'*10} Model Trainer has been completed.{'>>'*10}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,
                               model_trainer_artifact:ModelTrainerArtifact)->ModelEvaluationArtifact:
        try:
            logging.info(f"{'<<'*10} Model Evaluation has been started.{'>>'*10}")
            data_validation_config=self.config.get_data_validation_config()
            model_evaluation_config=self.config.get_model_evaluation_config()
            logging.info(f'model_evaluation_config:{model_evaluation_config}')
            model_evaluation=ModelEvaluation(data_validation_config=data_validation_config,
                            data_validation_artifact=data_validation_artifact,
                            model_trainer_artifact=model_trainer_artifact,
                            model_evaluation_config=model_evaluation_config)
            model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
            logging.info(f'model_evaluation_artifact:{model_evaluation_artifact}')
            logging.info(f"{'<<'*10} Model Evaluation has been Completed.{'>>'*10}")
            return model_evaluation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact)->ModelPusherArtifact:
        try:
            logging.info(f"{'<<'*10} Model Pusher has been started.{'>>'*10}")
            model_pusher_config=self.config.get_model_pusher_config()
            logging.info(f'model_pusher_config:{model_pusher_config}')
            model_pusher=ModelPusher(model_evaluation_artifact=model_evaluation_artifact,
                        model_pusher_config=model_pusher_config)
            model_pusher_artifact=model_pusher.initiate_model_pusher()
            logging.info(f'model_pusher_artifact:{model_pusher_artifact}')
            logging.info(f"{'<<'*10} Model Pusher has been Completed.{'>>'*10}")
            return model_pusher_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url=f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.config.training_pipeline_config.artifact_dir,
                                           aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def sync_final_model_dir_to_s3(self):
        try:
            aws_bucket_url=f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=os.path.dirname(self.config.get_model_trainer_config().trained_model_file_path),
                                           aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def run_pipeline(self):
        try:
            logging.info(f"{'<<'*10} Training Pipeline has been started.{'>>'*10}")
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact=self.start_model_evaluation(data_validation_artifact=data_validation_artifact,
                                        model_trainer_artifact=model_trainer_artifact)
            model_pusher_artifact=self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
            
            # logging.info(f"Sync Artifact and Final model Directory to S3 Bucket has been Started")
            # self.sync_artifact_dir_to_s3()
            # self.sync_final_model_dir_to_s3()
            # logging.info(f"Sync Artifact and Final model Directory to S3 Bucket has been Completed")
            
            logging.info(f"{'<<'*10} Training Pipeline has been completed.{'>>'*10}")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        