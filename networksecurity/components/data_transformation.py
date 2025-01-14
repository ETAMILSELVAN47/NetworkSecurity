from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataValidationConfig,DataTransformationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
import os
import sys
from networksecurity.constant import *
import numpy as np
import pandas as pd
from networksecurity.utils import read_yaml_file,save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,
                 data_validation_config:DataValidationConfig,
                 data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig)-> None:
        try:
            logging.info("Data Transformation has been started.")
            self.data_validation_config=data_validation_config
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def get_data_transformer_object(self)->Pipeline:
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor=Pipeline(steps=[("imputer",imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def read_data(self):
        try:
            train_file_path=self.data_validation_artifact.valid_train_data_file_path
            test_file_path=self.data_validation_artifact.valid_test_data_file_path

            train_df=pd.read_csv(train_file_path)
            test_df=pd.read_csv(test_file_path)

            return train_df,test_df
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:            
            # obtain preprocessor object
            logging.info("obtain preprocessor object") 
            preprocessor_obj=self.get_data_transformer_object()

            # Obtain train and test dataset
            logging.info("Obtain train and test dataset") 
            train_df,test_df=self.read_data()

            # Obtain the target column name
            logging.info("Obtain the target column name") 
            schema_info=read_yaml_file(file_path=self.data_validation_config.schema_file_path)
            target_column=schema_info[TARGET_COLUMN]

            # split the train data into input and target
            logging.info("split the train data into input and target") 
            input_feature_train_df=train_df.drop(columns=target_column)
            target_feature_train_df=train_df[target_column]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            # split the test data into input and target
            logging.info("split the test data into input and target") 
            input_feature_test_df=test_df.drop(columns=target_column)
            target_feature_test_df=test_df[target_column]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            
            # Transform train and test dataset
            logging.info("Transform train and test dataset") 
            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.transform(input_feature_test_df)


            # Train and Test array
            logging.info("Train and Test array") 
            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            # train and test file name
            logging.info("train and test file name") 
            train_file_name=os.path.basename(self.data_validation_artifact.valid_train_data_file_path).replace('.csv','.npy')
            test_file_name=os.path.basename(self.data_validation_artifact.valid_test_data_file_path).replace('.csv','.npy')

            train_file_path=os.path.join(self.data_transformation_config.transformed_train_dir,train_file_name)
            test_file_path=os.path.join(self.data_transformation_config.transformed_test_dir,test_file_name)

            # Save Train and Test array
            logging.info("Save Train and Test array") 
            save_numpy_array_data(file_path=train_file_path,array=train_arr)
            save_numpy_array_data(file_path=test_file_path,array=test_arr)
            
            # Save preprocessor object
            logging.info("Save preprocessor object") 
            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path,obj=preprocessor_obj)


            # Data Transformation Artifact
            logging.info("Data Transformation Artifact") 
            data_transformation_artifact=DataTransformationArtifact(transformed_train_file_path=train_file_path,
                                       transformed_test_file_path=test_file_path,
                                       preprocessor_obj_file_path=self.data_transformation_config.preprocessor_obj_file_path,
                                       is_transformed=True,
                                       message="Data Transformation Completed")

            logging.info("Data Transformation has been completed.") 
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        