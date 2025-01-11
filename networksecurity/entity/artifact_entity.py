from collections import namedtuple

DataIngestionArtifact=namedtuple(typename="DataIngestionArtifact",
                                 field_names=["train_data_file_path","test_data_file_path","is_ingested","message"]
                                )


DataValidationArtifact=namedtuple(typename="DataValidationArtifact",
           field_names=["valid_train_data_file_path","valid_test_data_file_path","invalid_train_data_file_path","invalid_test_data_file_path","drift_report_file_path","validation_status","is_validated","message"])