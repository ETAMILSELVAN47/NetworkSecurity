from collections import namedtuple

DataIngestionArtifact=namedtuple(typename="DataIngestionArtifact",
                                 field_names=["train_data_file_path","test_data_file_path","is_ingested","message"]
                                )