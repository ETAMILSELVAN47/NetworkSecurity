from collections import namedtuple

DataIngestionArtifact=namedtuple(typename="DataIngestionArtifact",
                                 field_names=["train_data_file_path","test_data_file_path","is_ingested","message"]
                                )


DataValidationArtifact=namedtuple(typename="DataValidationArtifact",
           field_names=["valid_train_data_file_path","valid_test_data_file_path","invalid_train_data_file_path","invalid_test_data_file_path","drift_report_file_path","validation_status","is_validated","message"])

DataTransformationArtifact=namedtuple(typename="DataTransformationArtifact",
           field_names=["transformed_train_file_path",
                        "transformed_test_file_path",
                        "preprocessor_obj_file_path",
                        "is_transformed",
                        "message"
                        ])


ModelEvaluationArtifact=namedtuple(typename="ModelEvaluationArtifact",
           field_names=["model_file_path","is_model_accepted","message"])

ModelTrainerArtifact=namedtuple(typename="ModelTrainerArtifact",
                                field_names=["trained_model_file_path","train_data_metric","test_data_metric","is_trained","message","model_accuracy"])

ModelPusherArtifact=namedtuple(typename="ModelPusherArtifact",
           field_names=["export_model_file_path","is_model_pushed","message"])