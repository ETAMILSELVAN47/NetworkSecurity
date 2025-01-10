from collections import namedtuple

DataIngestionConfig=namedtuple(typename="DataIngestionConfig",
           field_names=["database_name","collection_name","raw_data_dir","raw_data_file_name","ingested_data_dir","ingested_train_data_dir","ingested_test_data_dir","ingested_train_data_file_name","ingested_test_data_file_name","train_test_split_ratio"])


TrainingPipelineConfig=namedtuple(typename="TrainingPipelineConfig",
                                  field_names=["artifact_dir"])

