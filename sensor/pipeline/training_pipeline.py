from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from sensor.exception import SensorException
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from sensor.logger import logging
import sys, os

from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation

from sensor.components.model_trainer import ModelTrainer
from sensor.entity.artifact_entity import ModelTrainerArtifact
from sensor.entity.config_entity import ModelTrainerConfig

from sensor.components.model_evaluation import ModelEvaluation
from sensor.entity.artifact_entity import ModelEvaluationArtifact,ModelPusherArtifact
from  sensor.entity.config_entity import ModelEvaluationConfig,ModelPusherConfig

from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.components.model_pusher import ModelPusher

from sensor.cloud_storage.s3_syncer import S3Sync
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME


class TrainingPipeline: 

    is_pipeline_running=False
    self.s3_sync = S3Sync()


    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self)->DataIngestionArtifact:
        try: 
            self.data_ingestion_config= DataIngestionConfig(training_pipeline_config=
                                                            self.training_pipeline_config) 
            logging.info("Starting Data Ingestion ")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e: 
            raise SensorException(e,sys)
        

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=
                                                          self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()

            return data_validation_artifact

        except Exception as e: 
            raise SensorException(e,sys)
        
        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:

        try: 
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=data_transformation_config)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()

            return data_transformation_artifact

        except Exception as e: 
            raise SensorException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try: 
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=
                                                      self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e,sys)
        
    


    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,
                               model_trainer_artifact:ModelTrainerArtifact):
        try: 
            model_eval_config = ModelEvaluationConfig(self.training_pipeline_config)
            model_eval = ModelEvaluation(model_eval_config,data_validation_artifact,
                                         model_trainer_artifact)
            model_eval_artifact = model_eval.initiate_model_evaluation()

            return model_eval_artifact 

        except Exception as e: 
            raise SensorException(e,sys)
        
    
        
    def start_model_pusher(self,model_eval_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config=
                                                    self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config,model_eval_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info("Model Pusher artifact completed in the training pipeline")
            return model_pusher_artifact

        except Exception as e: 
            raise SensorException(e,sys)

    



        
    def run_pipeline(self):
        try:
            TrainingPipeline.is_pipeline_running = True

            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()

            data_validation_artifact  = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact)
            
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=
                                                                          data_validation_artifact)
            
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            model_eval_artifact = self.start_model_evaluation(data_validation_artifact,
                                                              model_trainer_artifact)
            
            if not model_eval_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            
            model_pusher_artifact = self.start_model_pusher(model_eval_artifact)
            TrainingPipeline.is_pipeline_running = False
            

        except Exception as e:
            TrainingPipeline.is_pipeline_running = False
            raise SensorException(e,sys) 
        

