from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import sys
from networksecurity.utils import read_yaml_file,write_yaml_file
import pandas as pd
from networksecurity.constant import *
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig)-> None:
        try:
            logging.info("Data Validation has been started")
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_info=read_yaml_file(file_path=self.data_validation_config.schema_file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def read_data(self):
        try:
            logging.info('Read the Train and Test Dataset')
            train_file_path=self.data_ingestion_artifact.train_data_file_path
            test_file_path=self.data_ingestion_artifact.test_data_file_path

            train_df=pd.read_csv(train_file_path)
            test_df=pd.read_csv(test_file_path)

            return train_df,test_df
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
    def validate_no_of_columns(self,train_df:pd.DataFrame,test_df:pd.DataFrame):
        try:
            logging.info('Validate No.of.Columns')
            schema_info=self.schema_info[COLUMNS_KEY]
            required_no_of_columns=len(schema_info)

            train_df_no_of_columns=train_df.shape[1]
            test_df_no_of_columns=test_df.shape[1]

            logging.info(f'Required No.of.Columns:{required_no_of_columns}')
            logging.info(f'Train Dataset No.of.Columns:{train_df_no_of_columns}')
            logging.info(f'Test Dataset No.of.Columns:{test_df_no_of_columns}')

            if required_no_of_columns!=train_df_no_of_columns:
                raise NetworkSecurityException('Train datset not have all the columns',sys)
            
            if required_no_of_columns!=test_df_no_of_columns:
                raise NetworkSecurityException('Test dataset not have all the columns',sys )

        except Exception as e:
            raise NetworkSecurityException(e,sys)  

    def is_numerical_columns_exist(self,train_df:pd.DataFrame,test_df:pd.DataFrame):
        try:
            logging.info('Checking numerical columns exists or not')
            numerical_columns_list=self.schema_info[NUMERICAL_COLUMNS_KEY]

            train_df_columns_list=train_df.select_dtypes(exclude='object').columns.to_list()
            test_df_columns_list=test_df.select_dtypes(exclude='object').columns.to_list()

            if set(numerical_columns_list)!=set(train_df_columns_list):
                raise NetworkSecurityException('Numerical Columns not present in the Train dataset',sys)
            
            if set(numerical_columns_list)!=set(test_df_columns_list):
                raise NetworkSecurityException('Numerical columns not present in the Test Dataset',sys)

        except Exception as e:
            raise NetworkSecurityException(e,sys)  
        
    def detect_data_drift(self,train_df:pd.DataFrame,test_df:pd.DataFrame,threshold:float=0.05):
        try:
            logging.info('Detect the dataset drift')
            report=dict()
            for col in train_df.columns.to_list():
                d1=train_df[col]
                d2=test_df[col]
                is_same_dist=ks_2samp(d1,d2)

                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                report.update({col:
                               {
                                "p-value":float(is_same_dist.pvalue),
                                "is_found":is_found   
                               }})        

            drift_report_file_path=self.data_validation_config.drift_report_file_path

            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path,content=report,replace=True)

        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
    def initiate_data_validation(self)->DataValidationArtifact:        
        try:
            # read the data
            train_df,test_df=self.read_data()

            # validate no.of.columns
            self.validate_no_of_columns(train_df=train_df,test_df=test_df)

            # is numerical columns exist
            self.is_numerical_columns_exist(train_df=train_df,test_df=test_df)

            # is data drift found?
            self.detect_data_drift(train_df=train_df,test_df=test_df)

            train_file_name=os.path.basename(self.data_ingestion_artifact.train_data_file_path)
            test_file_name=os.path.basename(self.data_ingestion_artifact.test_data_file_path)

            train_file_path=os.path.join(self.data_validation_config.valid_data_dir,
                                        train_file_name)
            test_file_path=os.path.join(self.data_validation_config.valid_data_dir,
                                        test_file_name)
            
            os.makedirs(self.data_validation_config.valid_data_dir,exist_ok=True)

            train_df.to_csv(train_file_path,index=False,header=True)
            test_df.to_csv(test_file_path,index=False,header=True)

            data_validation_artifact=DataValidationArtifact(validation_status=True,
                                   valid_train_data_file_path=train_file_path,
                                   valid_test_data_file_path=test_file_path,
                                   invalid_train_data_file_path=None,
                                   invalid_test_data_file_path=None,
                                   drift_report_file_path=self.data_validation_config.drift_report_file_path,
                                   is_validated=True,
                                   message="Data Validation Completed")
            logging.info('Data Validation has been completed.')
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
