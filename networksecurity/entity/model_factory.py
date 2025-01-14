from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
import yaml
from networksecurity.constant import *
from dataclasses import dataclass
import importlib
from typing import List
from sklearn.metrics import precision_score,recall_score,f1_score,accuracy_score

@dataclass
class InitializedModel:
    model_serial_number:str
    model_name:str
    model_object:any
    param_grid_search:dict

@dataclass
class GridSearchedBestModel:
    model_serial_number:str
    model:any
    best_model:any
    best_parameters:any
    best_score:float


@dataclass
class ClassificationMetric:
    precision_score:float
    recall_score:float
    f1_score:float
    accuracy:float
    

@dataclass
class MetricInfoArtifact:
    model_name:str
    model_object:any
    train_data_metric:ClassificationMetric
    test_data_metric:ClassificationMetric 
    model_accuracy:float 
    index_number:int 

import mlflow

def track_mlflow(metric_info_artifact:MetricInfoArtifact):
    try:
        with mlflow.start_run(run_name=metric_info_artifact.model_name):
            mlflow.set_tag('Model name',metric_info_artifact.model_name)
            mlflow.sklearn.log_model(sk_model=metric_info_artifact.model_object,artifact_path="model",registered_model_name=metric_info_artifact.model_name)
            
            mlflow.log_metric("Train_Precision_Score",metric_info_artifact.train_data_metric.precision_score)
            mlflow.log_metric("Train_Recall_Score",metric_info_artifact.train_data_metric.recall_score)
            mlflow.log_metric("Train_F1_Score",metric_info_artifact.train_data_metric.f1_score)

            mlflow.log_metric('Test_Precision_Score',metric_info_artifact.test_data_metric.precision_score)
            mlflow.log_metric('Test_Recall_Score',metric_info_artifact.test_data_metric.recall_score)
            mlflow.log_metric('Test_F1_Score',metric_info_artifact.test_data_metric.f1_score)

            mlflow.log_metric('Model Accuracy',metric_info_artifact.model_accuracy)

    except Exception as e:
        raise NetworkSecurityException(e,sys)


def evaluate_classification_model(models_list:list,
                                  X_train:np.ndarray,
                                  X_test:np.ndarray,
                                  y_train:np.ndarray,
                                  y_test:np.ndarray,
                                  base_accuracy:float=0.6):
    try:
        metric_info_artifact=None
        index_number=0
        for model in models_list:
            model_name=type(model).__name__

            # predict
            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            train_acc=accuracy_score(y_train,y_train_pred)
            test_acc=accuracy_score(y_test,y_test_pred)

            model_accuracy=2*(train_acc*test_acc)/(train_acc+test_acc)
            diff_train_test_acc=abs(train_acc-test_acc)

            if base_accuracy<=model_accuracy and diff_train_test_acc<0.05:
                base_accuracy=model_accuracy
                train_data_metric=ClassificationMetric(precision_score=np.round(precision_score(y_train,y_train_pred),2),
                                     recall_score=np.round(recall_score(y_train,y_train_pred),2),
                                     f1_score=np.round(f1_score(y_train,y_train_pred),2),
                                     accuracy=np.round(train_acc,2))
                
                test_data_metric=ClassificationMetric(precision_score=np.round(precision_score(y_test,y_test_pred),2),
                                     recall_score=np.round(recall_score(y_test,y_test_pred),2),
                                     f1_score=np.round(f1_score(y_test,y_test_pred),2),
                                     accuracy=np.round(test_acc,2))
                
                metric_info_artifact=MetricInfoArtifact(model_name=model_name,
                                   model_object=model,
                                   train_data_metric=train_data_metric,
                                   test_data_metric=test_data_metric,
                                   model_accuracy=np.round(model_accuracy,2),
                                   index_number=index_number)
                
                track_mlflow(metric_info_artifact)
            index_number+=1  

        if not metric_info_artifact:
            raise NetworkSecurityException('No model found with higher accuracy than base accuracy') 

        return metric_info_artifact       

    except Exception as e:
        raise NetworkSecurityException(e,sys)



class ModelFactory:
    def __init__(self,
                 model_config_file_path:str)->None:
        try:
            self.model_config=ModelFactory.read_params(file_path=model_config_file_path)
            self.grid_search_cv_module=self.model_config[GRID_SEARCH_KEY][MODULE_KEY]
            self.grid_search_class_name=self.model_config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_search_property_data=dict(self.model_config[GRID_SEARCH_KEY][PARAMS_KEY])

            self.models_initialization_config=self.model_config[MODEL_SELECTION_KEY]

            self.initialized_models_list=None
            self.grid_searched_best_models_list=None

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_params(file_path:str)->dict:
        try:
            with open(file=file_path,mode='r') as yaml_file:
                return yaml.safe_load(stream=yaml_file)
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
    @staticmethod
    def class_for_name(module_name:str,class_name:str):
        try:
            module=importlib.import_module(module_name)
            class_ref=getattr(module,class_name)
            return class_ref
        except Exception as e:
            raise NetworkSecurityException(e,sys)  

    @staticmethod
    def update_property_of_class(instance_ref:object,property_data:dict):
        try:
            if not isinstance(property_data,dict):
                raise NetworkSecurityException('property_data should be a dictionary',sys)
            for key,value in property_data.items():
                setattr(instance_ref,key,value)
            return instance_ref    
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_initialized_models_list(self,)->List[InitializedModel]:
        try:
            self.initialized_models_list=list()

            for model_serial_number in list(self.models_initialization_config.keys()):
                model_initialization_config=self.models_initialization_config[model_serial_number]
                model_obj_ref=ModelFactory.class_for_name(module_name=model_initialization_config[MODULE_KEY],
                                                          class_name=model_initialization_config[CLASS_KEY])
                model=model_obj_ref()

                if PARAMS_KEY in model_initialization_config:
                    model_obj_property_data=dict(model_initialization_config[PARAMS_KEY])  
                    model=ModelFactory.update_property_of_class(instance_ref=model,
                                                                property_data=model_obj_property_data) 
                param_grid_search=dict(model_initialization_config[SEARCH_PARAM_GRID_KEY])

                model_name=type(model).__name__

                initialized_model_list=InitializedModel(model_serial_number=model_serial_number,
                                                            model_name=model_name,
                                                            model_object=model,
                                                            param_grid_search=param_grid_search)
                
                self.initialized_models_list.append(initialized_model_list)

            return self.initialized_models_list    

        except Exception as e:
            raise NetworkSecurityException(e,sys) 

    def execute_grid_search_operation(self,
                                      initialized_model:InitializedModel,
                                      input_feature:np.ndarray,
                                      output_feature:np.ndarray)->GridSearchedBestModel:
        try:
            grid_search_cv_ref=ModelFactory.class_for_name(module_name=self.grid_search_cv_module,
                                                           class_name=self.grid_search_class_name)
            
            grid_search_cv=grid_search_cv_ref(estimator=initialized_model.model_object,
                                              param_grid=initialized_model.param_grid_search)
            
            grid_search_cv=ModelFactory.update_property_of_class(instance_ref=grid_search_cv,
                                                  property_data=self.grid_search_property_data)
            
            grid_search_cv.fit(input_feature,output_feature)

            grid_searched_best_model=GridSearchedBestModel(model_serial_number=initialized_model.model_serial_number,
                                                           model=initialized_model.model_object,
                                                           best_model=grid_search_cv.best_estimator_,
                                                           best_parameters=grid_search_cv.best_params_,
                                                           best_score=grid_search_cv.best_score_)
            return grid_searched_best_model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_best_parameter_search_for_initialized_model(self,
                                                             initialized_model:InitializedModel,
                                                             input_feature:np.ndarray,
                                                             output_feature:np.ndarray
                                                             )->GridSearchedBestModel:
        try:
            return self.execute_grid_search_operation(initialized_model=initialized_model,
                                                      input_feature=input_feature,
                                                      output_feature=output_feature
                                                      )
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_best_parameter_search_for_initialzed_models(self,
                                                             initialized_models_list:List[InitializedModel],
                                                             input_feature:np.ndarray,
                                                             output_feature:np.ndarray,
                                                             )->List[GridSearchedBestModel]:
        try:
            self.grid_searched_best_models_list=list()
            for initialized_model in initialized_models_list:
                grid_searched_best_model=self.initiate_best_parameter_search_for_initialized_model(initialized_model=initialized_model,
                                                                          input_feature=input_feature,
                                                                          output_feature=output_feature)
                
                self.grid_searched_best_models_list.append(grid_searched_best_model)

            return self.grid_searched_best_models_list    
        except Exception as e:
            raise NetworkSecurityException(e,sys)             
    
    def get_best_model_from_grid_searched_best_models_list(self,
                                                           grid_searched_best_models_list:List[GridSearchedBestModel],
                                                           base_accuracy:float=0.6
                                                           )->GridSearchedBestModel:
        try:
            best_model= None

            for grid_searched_best_model in grid_searched_best_models_list:
                if base_accuracy<grid_searched_best_model.best_score:
                    base_accuracy=grid_searched_best_model.best_score
               
                    best_model=grid_searched_best_model.best_model
            
            if not best_model:
                raise NetworkSecurityException('No best model found on training dataset whose accuracy is higher than base accuracy',sys)
            
            return best_model


        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_best_model(self,X,y,base_accuracy:float=0.6)->GridSearchedBestModel:
        try:
            initialized_models_list=self.get_initialized_models_list()

            grid_searched_best_models_list=self.initiate_best_parameter_search_for_initialzed_models(initialized_models_list=initialized_models_list,
                                                                      input_feature=X,
                                                                      output_feature=y)
            
            return self.get_best_model_from_grid_searched_best_models_list(grid_searched_best_models_list=grid_searched_best_models_list,
                                                                           base_accuracy=base_accuracy)
        except Exception as e:
            raise NetworkSecurityException(e,sys)    