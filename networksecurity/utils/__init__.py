import yaml
import sys
from networksecurity.exception.exception import NetworkSecurityException


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