import os
from datetime import datetime

CONFIG_DIR="config"
CONFIG_FILE_NAME="config.yaml"
CONFIG_FILE_PATH=os.path.join(CONFIG_DIR,CONFIG_FILE_NAME)

CURRENT_TIME_STAMP=f"{datetime.now().strftime(format='%d-%B-%Y %H-%M-%S')}"




# Training Pipeline Related Variable
TRAINING_PIPELINE_CONFIG_KEY= "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY= "pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY= "artifact_dir"

# Data Ingestion Related Variable
DATA_INGESTION_CONFIG_KEY= "data_ingestion_config"
DATA_INGESTION_DATABASE_NAME_KEY= "database_name"
DATA_INGESTION_COLLECTION_NAME_KEY= "collection_name"
DATA_INGESTION_DIR_KEY= "data_ingestion"
DATA_INGESTION_RAW_DATA_DIR_KEY= "raw_data_dir"
DATA_INGESTION_RAW_DATA_FILE_NAME_KEY= "raw_data_file_name"
DATA_INGESTION_INGESTED_DATA_DIR_KEY= "ingested_data_dir"
DATA_INGESTION_INGESTED_TRAIN_DATA_DIR_KEY= "ingested_train_data_dir"
DATA_INGESTION_INGESTED_TEST_DATA_DIR_KEY= "ingested_test_data_dir"
DATA_INGESTION_INGESTED_TRAIN_DATA_FILE_NAME_KEY= "ingested_train_data_file_name"
DATA_INGESTION_INGESTED_TEST_DATA_FILE_NAME_KEY= "ingested_test_data_file_name"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO= "train_test_split_ratio"