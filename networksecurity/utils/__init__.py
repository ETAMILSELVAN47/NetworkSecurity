import yaml
import sys
from networksecurity.exception.exception import NetworkSecurityException
import os


def read_yaml_file(file_path:str)->dict:
    '''
    Reads a YAML file and return the contents as a dictionary
    file_path: str
    '''
    try:
        with open(file=file_path,mode='rb') as yaml_file:
            return yaml.safe_load(stream=yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)        
        yaml.dump(data=content,stream=open(file=file_path,mode='w'))
    except Exception as e:
        raise NetworkSecurityException(e,sys)    