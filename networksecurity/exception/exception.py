import sys
from networksecurity.logging.logger import logging

class NetworkSecurityException(Exception):
    def __init__(self,error_message:str,error_detail:sys):
        _,_,exc_tb=error_detail.exc_info()
        filename=exc_tb.tb_frame.f_code.co_filename
        line_no=exc_tb.tb_lineno
        self.error_message=f'Error occured in the filename {filename}, lineno {line_no} and error is {error_message}'
        logging.info(self.error_message)

    def __str__(self):        
        return self.error_message


if __name__=='__main__':
    try:
        a=1/0
    except Exception as e:
        # obj=NetworkSecurityException(e,sys)
        # logging.info(obj.error_message)
        raise NetworkSecurityException(e,sys)  