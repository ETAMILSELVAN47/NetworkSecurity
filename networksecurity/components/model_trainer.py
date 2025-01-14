from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
import sys
from networksecurity.utils import load_numpy_array_data,load_object,save_object
from networksecurity.entity.model_factory import *
from typing import List

class NetworkEstimatorModel:
    def __init__(self,preprocessing_object,trained_model_object):
        try:
            self.preprocessing_object=preprocessing_object
            self.trained_model_object=trained_model_object            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self,X):
        try:
            transformed_feature=self.preprocessing_object.transform(X)
            return self.trained_model_object.predict(transformed_feature)
        except Exception as e:
            raise NetworkSecurityException(e,sys)  

    def __repr__(self):
        return f'{type(self.trained_model_object).__name__}()'   

    def __str__(self):
        return f'{type(self.trained_model_object).__name__}()'   


class Modeltrainer:
    def __init__(self,
                 data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig)->None:
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
            logging.info('Model Trainer has been started.')
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info('Obtain Transformed Train and Test File path')            
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path
            logging.info(f'train_file_path:{train_file_path}')
            logging.info(f'test_file_path:{test_file_path}')
       
            logging.info('Obtain Transformed Train and Test Array')
            
            train_arr=load_numpy_array_data(file_path=train_file_path)
            test_arr=load_numpy_array_data(file_path=test_file_path)

            logging.info('Train and Test Split')
            X_train,X_test,y_train,y_test=train_arr[:,:-1],test_arr[:,:-1],train_arr[:,-1],test_arr[:,-1]
            
            model_config_file_path=self.model_trainer_config.model_config_file_path

            model_factory=ModelFactory(model_config_file_path=model_config_file_path)

            base_accuracy=self.model_trainer_config.base_accuracy

            # train dataset best model
            best_model=model_factory.get_best_model(X=X_train,y=y_train,base_accuracy=base_accuracy)

            #get grid searched best models list
            grid_searched_best_models_list:List[GridSearchedBestModel]=model_factory.grid_searched_best_models_list

            # get models list
            models_list=[model.best_model for model in grid_searched_best_models_list]
            
            logging.info('Evaluate classification_model')
            metric_info_artifact:MetricInfoArtifact=evaluate_classification_model(models_list=models_list,
                                                                                  X_train=X_train,
                                                                                  X_test=X_test,
                                                                                  y_train=y_train,
                                                                                  y_test=y_test,
                                                                                  base_accuracy=base_accuracy)
            
            preprocessing_obj=load_object(file_path=self.data_transformation_artifact.preprocessor_obj_file_path)
            model_object=metric_info_artifact.model_object

            network_model=NetworkEstimatorModel(preprocessing_object=preprocessing_obj,
                                  trained_model_object=model_object)
            

            logging.info('save model')
            save_object(file_path=self.model_trainer_config.trained_model_file_path,
                        obj=network_model)
            
            model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                 train_data_metric=metric_info_artifact.train_data_metric,
                                 test_data_metric=metric_info_artifact.test_data_metric,
                                 is_trained=True,
                                 message="Model Trainer Completed",
                                 model_accuracy=metric_info_artifact.model_accuracy)

            
            logging.info('Model Trainer has been completed.')
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)