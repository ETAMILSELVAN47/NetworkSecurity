from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelPusherConfig
from networksecurity.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact
import os,sys
import shutil


class ModelPusher:
    def __init__(self,
                 model_evaluation_artifact:ModelEvaluationArtifact,
                 model_pusher_config:ModelPusherConfig)->None:
        try:
            self.model_evaluation_artifact=model_evaluation_artifact
            self.model_pusher_config=model_pusher_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def export_model(self)->ModelPusherArtifact:
        try:
            evaluated_model_file_path=self.model_evaluation_artifact.model_file_path
            export_model_dir_path=self.model_pusher_config.export_model_dir_path
            model_file_name=os.path.basename(evaluated_model_file_path)

            export_model_file_path=os.path.join(export_model_dir_path,model_file_name)

            os.makedirs(export_model_dir_path,exist_ok=True)

            shutil.copy(src=evaluated_model_file_path,dst=export_model_file_path)

            model_pusher_artifact=ModelPusherArtifact(export_model_file_path=export_model_dir_path,
                                is_model_pushed=True,
                                message='Model Pusher Completed')


            return model_pusher_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            return self.export_model()
        except Exception as e:
            raise NetworkSecurityException(e,sys)    