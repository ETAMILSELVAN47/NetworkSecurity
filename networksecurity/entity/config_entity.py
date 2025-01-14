from collections import namedtuple

DataIngestionConfig=namedtuple(typename="DataIngestionConfig",
           field_names=["database_name","collection_name","raw_data_dir","raw_data_file_name","ingested_data_dir","ingested_train_data_dir","ingested_test_data_dir","ingested_train_data_file_name","ingested_test_data_file_name","train_test_split_ratio"])



DataValidationConfig=namedtuple(typename="DataValidationConfig",
           field_names=["schema_file_path","valid_data_dir","invalid_data_dir","drift_report_file_path"])


DataTransformationConfig=namedtuple(typename="DataTransformationConfig",
           field_names=["transformed_train_dir",
                        "transformed_test_dir",
                        "preprocessor_obj_file_path"])

ModelTrainerConfig=namedtuple(typename="ModelTrainerConfig",
           field_names=["trained_model_file_path","base_accuracy","model_config_file_path"])

TrainingPipelineConfig=namedtuple(typename="TrainingPipelineConfig",
                                  field_names=["artifact_dir"])

ModelEvaluationConfig=namedtuple(typename="ModelEvaluationConfig",
           field_names=["model_evaluation_file_path","timestamp"])


ModelPusherConfig=namedtuple(typename="ModelPusherConfig",
           field_names=["export_model_dir_path"])


