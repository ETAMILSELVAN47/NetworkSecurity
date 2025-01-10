import os
import logging
from datetime import datetime

LOG_FILE_DIR='logs'
LOG_FILE_NAME=f"{datetime.now().strftime(format='%d-%B-%Y %H-%M-%S')}.log"
LOG_FILE_PATH=os.path.join(os.getcwd(),LOG_FILE_DIR,LOG_FILE_NAME)

os.makedirs(LOG_FILE_DIR,exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE_PATH,
    format='%(asctime)s-%(filename)s-%(lineno)d-%(levelname)s-%(message)s',
    datefmt='%d-%B-%Y %H:%M:%S'   
)


# if __name__=='__main__':
#     logging.info('Logging has been started.')