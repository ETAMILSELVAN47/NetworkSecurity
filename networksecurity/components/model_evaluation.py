from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
from networksecurity.entity.config_entity import DataValidationConfig,ModelEvaluationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,ModelTrainerArtifact,ModelEvaluationArtifact,DataValidationArtifact
from networksecurity.utils import load_data,read_yaml_file,write_yaml_file,load_object
from networksecurity.constant import *
from networksecurity.entity.model_factory import *

class ModelEvaluation:
    def __init__(self,                 
                 data_validation_config:DataValidationConfig,
                 data_validation_artifact:DataValidationArtifact,
                 model_trainer_artifact:ModelTrainerArtifact,
                 model_evaluation_config:ModelEvaluationConfig)->None:
        try:
            self.data_validation_config=data_validation_config
            self.data_validation_artifact=data_validation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_evaluation_config=model_evaluation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_best_model(self):
        try:
            model=None

            model_evaluation_file_path=self.model_evaluation_config.model_evaluation_file_path

            if not os.path.exists(model_evaluation_file_path):
                write_yaml_file(file_path=model_evaluation_file_path)
                return model
            
            model_eval_content=read_yaml_file(file_path=model_evaluation_file_path)
            model_eval_content=dict() if model_eval_content is None else model_eval_content

            if BEST_MODEL_KEY in model_eval_content:
                model_file_path=model_eval_content[BEST_MODEL_KEY][MODEL_PATH_KEY]
                model=load_object(file_path=model_evaluation_file_path)
            
            return model
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
    def update_evaluation_report(self,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            model_eval_content=read_yaml_file(file_path=self.model_evaluation_config.model_evaluation_file_path)
            model_eval_content=dict() if model_eval_content is None else model_eval_content

            eval_result={
                BEST_MODEL_KEY:
                {MODEL_PATH_KEY:model_evaluation_artifact.model_file_path}
                        }
            
            previous_best_model=None
            if BEST_MODEL_KEY in model_eval_content:
                previous_best_model=model_eval_content[BEST_MODEL_KEY]

            if previous_best_model is not None:
               model_history={self.model_evaluation_config.timestamp:previous_best_model} 
               if HISTORY_KEY in model_eval_content:
                   model_eval_content[HISTORY_KEY].update(model_history)                  
               else:
                   history={HISTORY_KEY:model_history}
                   eval_result.update(history)

            model_eval_content.update(eval_result)
            
            write_yaml_file(file_path=self.model_evaluation_config.model_evaluation_file_path,content=model_eval_content)

        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        

    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            #train and test file path
            train_file_path=self.data_validation_artifact.valid_train_data_file_path
            test_file_path=self.data_validation_artifact.valid_test_data_file_path

            schema_file_path=self.data_validation_config.schema_file_path

            #Train and Test data
            train_df=load_data(file_path=train_file_path,schema_file_path=schema_file_path)
            test_df=load_data(file_path=test_file_path,schema_file_path=schema_file_path)

            schema_info=read_yaml_file(file_path=schema_file_path)
            target_column=schema_info[TARGET_COLUMN]

            #Train - Input and target
            X_train=train_df.drop(columns=target_column).values
            y_train=train_df[target_column].replace(-1,0).values
            #Test - Input and target
            X_test=test_df.drop(columns=target_column).values
            y_test=test_df[target_column].replace(-1,0).values

            model=self.get_best_model()

            if model is None:
                model_evaluation_artifact=ModelEvaluationArtifact(model_file_path=self.model_trainer_artifact.trained_model_file_path,
                                        is_model_accepted=True,
                                        message="Model Evaluation Completed")
                
                self.update_evaluation_report(model_evaluation_artifact=model_evaluation_artifact)
                return model_evaluation_artifact
            
            trained_model_object=load_object(file_path=self.model_trainer_artifact.trained_model_file_path)
            
            models_list=[model,trained_model_object]

            metric_info_atrifact:MetricInfoArtifact=evaluate_classification_model(models_list=models_list,
                                                                                  X_train=X_train,
                                                                                  X_test=X_test,
                                                                                  y_train=y_train,
                                                                                  y_test=y_test,
                                                                                  base_accuracy=self.model_trainer_artifact.model_accuracy)

            if metric_info_atrifact is None:
                model_evaluation_artifact=ModelEvaluationArtifact(model_file_path=self.model_trainer_artifact.trained_model_file_path,
                                                                  is_model_accepted=False,
                                                                  message="Model evaluation completed")
                return model_evaluation_artifact

            
            if metric_info_atrifact.index_number==1:
               model_evaluation_artifact=ModelEvaluationArtifact(model_file_path=self.model_trainer_artifact.trained_model_file_path,
                                                                 is_model_accepted=True,
                                                                 message="Model evaluation completed") 
               self.update_evaluation_report(model_evaluation_artifact=model_evaluation_artifact)
               return model_evaluation_artifact
            
            else:
                model_evaluation_artifact=ModelEvaluationArtifact(model_file_path=self.model_trainer_artifact.trained_model_file_path,
                                                                  is_model_accepted=False,
                                                                  message="Model evaluation completed")
                
                return model_evaluation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)    