import os
from datetime import datetime
import numpy as np

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

# Data Validation related Variable
COLUMNS_KEY= "columns"
NUMERICAL_COLUMNS_KEY= "numerical_columns"
DATA_VALIDATION_DIR_KEY= "data_validation"
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_DIR_KEY= "schema_dir"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY= "schema_file_name"
DATA_VALIDATION_VALID_DATA_DIR_KEY= "valid_data_dir"
DATA_VALIDATION_INVALID_DATA_DIR_KEY= "invalid_data_dir"
DATA_VALIDATION_DRIFT_REPORT_DIR_KEY= "drift_report_dir"
DATA_VALIDATION_REPORT_FILE_NAME_KEY= "report_file_name"

# Data Transformation related variable
DATA_TRANSFORMATION_DIR_NAME= "data_transformation"
DATA_TRANSFORMATION_CONFIG_KEY= "data_transformation_config"
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY= "transformed_dir"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY= "transformed_train_dir"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY= "transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSOR_DIR_KEY= "preprocessor_dir"
DATA_TRANSFORMATION_PREPROCESSOR_OBJ_FILE_NAME_KEY= "preprocessor_object_file_name"

DATA_TRANSFORMATION_IMPUTER_PARAMS:dict={
                                        "missing_values":np.nan,
                                        "n_neighbors":3,
                                        "weights":"uniform"}



# Model Trainer Related Variable
MODEL_TRAINER_DIR_NAME= "model_trainer"
MODEL_TRAINER_CONFIG_KEY= "model_trainer_config"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY= "trained_model_dir"
MODEL_TRAINER_MODEL_FILE_NAME_KEY= "model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY= "base_accuracy"
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY= "model_config_dir"
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY= "model_config_file_name"
MODEL_TRAINER_DIFF_TEST_TRAIN_ACC_KEY= "diff_test_train_acc"

GRID_SEARCH_KEY= "grid_search"
MODULE_KEY= "module"
CLASS_KEY= "class"
PARAMS_KEY= "params"
SEARCH_PARAM_GRID_KEY= "search_param_grid"
MODEL_SELECTION_KEY= "model_selection"

TARGET_COLUMN= "target_column_name"


# Model Evaluation Related Variable
MODEL_EVALUATION_DIR_NAME= "model_evaluation"
MODEL_EVALUATION_CONFIG_KEY= "model_evaluation_config"
MODEL_EVALUATION_FILE_NAME_KEY= "model_evaluation_file_name"

# Model Pusher Related Variable
MODEL_PUSHER_DIR_NAME= "model_pusher"
MODEL_PUSHER_CONFIG_KEY= "model_pusher_config"
MODEL_PUSHER_MODEL_EXPORT_DIR_KEY= "model_export_dir"

BEST_MODEL_KEY= "best_model"
MODEL_PATH_KEY= "model_path"
HISTORY_KEY= "history"


TRAINING_BUCKET_NAME= "networksecurityts"