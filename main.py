from networksecurity.config.configuration import Configuration
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import Modeltrainer
from networksecurity.components.model_evaluation import ModelEvaluation
from networksecurity.components.model_pusher import ModelPusher
import sys
import mlflow

if __name__=='__main__':
    try:

        mlflow.set_experiment("Network Model - Experiment 1")
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
        #----------------------------------------------------------------#
        data_transformation_config=config.get_data_transformation_config()
        print(f'\ndata_transformation_config:{data_transformation_config}')
        data_transformation=DataTransformation(data_validation_config=data_validation_config,
                           data_validation_artifact=data_validation_artifact,
                           data_transformation_config=data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(f'\ndata_transformation_artifact:{data_transformation_artifact}')
        #----------------------------------------------------------------#
        model_trainer_config=config.get_model_trainer_config()
        print(f'\nmodel_trainer_config:{model_trainer_config}')
        model_trainer=Modeltrainer(data_transformation_artifact=data_transformation_artifact,
                     model_trainer_config=model_trainer_config)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        print(f'\nmodel_trainer_artifact:{model_trainer_artifact}')
        #----------------------------------------------------------------#
        model_evaluation_config=config.get_model_evaluation_config()
        print(f'\n model_evaluation_config:{model_evaluation_config}')
        model_evaluation=ModelEvaluation(data_validation_config=data_validation_config,
                        data_validation_artifact=data_validation_artifact,
                        model_trainer_artifact=model_trainer_artifact,
                        model_evaluation_config=model_evaluation_config)
        
        model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
        print(f'\n model_evaluation_artifact:{model_evaluation_artifact}')
        #----------------------------------------------------------------#
        model_pusher_config=config.get_model_pusher_config()
        print(f'\nmodel_pusher_config:{model_pusher_config}')
        model_pusher=ModelPusher(model_evaluation_artifact=model_evaluation_artifact,
                    model_pusher_config=model_pusher_config)
        
        model_pusher_artifact=model_pusher.initiate_model_pusher()

        print(f'\nmodel_pusher_artifact:{model_pusher_artifact}')


    except Exception as e:
        raise NetworkSecurityException(e,sys)   
    