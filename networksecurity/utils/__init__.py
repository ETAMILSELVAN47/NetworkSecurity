import yaml
import sys
from networksecurity.exception.exception import NetworkSecurityException
import os
import pickle
import numpy as np
import pandas as pd
from networksecurity.constant import *


def read_yaml_file(file_path:str)->dict:
    '''
    Reads a YAML file and return the contents as a dictionary
    file_path: str
    '''
    try:
        with open(file=file_path,mode='rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path:str,content:object=dict(),replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)        
        yaml.dump(data=content,stream=open(file=file_path,mode='w'))
    except Exception as e:
        raise NetworkSecurityException(e,sys)    
    

def save_numpy_array_data(file_path:str,array:np.ndarray)->None:
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file=file_path,mode='wb') as file_obj:
            np.save(file=file_obj,arr=array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array_data(file_path:str)->np.ndarray:
    try:        
        with open(file=file_path,mode='rb') as file_obj:
            return np.load(file=file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)    
    
def save_object(file_path:str,obj)->None:
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file=file_path,mode='wb') as file_obj:
            pickle.dump(obj=obj,file=file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)   

def load_object(file_path:str):
    try:
        with open(file=file_path,mode='rb') as file_obj:
            return pickle.load(file=file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)     
    

def load_data(file_path:str,schema_file_path:str)->pd.DataFrame:
    try:
        schema_info=read_yaml_file(file_path=schema_file_path)

        schema=schema_info[COLUMNS_KEY]
        
        df=pd.read_csv(file_path)
        
        error_message=None
        for column in df.columns.to_list():
            if column in list(schema.keys()):
                df[column].astype(schema[column])
            else:
                error_message=f'{error_message} \n Column {column} is not present in the schema'

        if error_message:
            raise Exception(error_message)

        return df            

    except Exception as e:
        raise NetworkSecurityException(e,sys)    