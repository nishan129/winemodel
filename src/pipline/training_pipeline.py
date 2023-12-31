from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerconfig, ModelEvauationConfig, ModelPusherConfig
from src.exception import ModelException
import sys
from src.logger import logging
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from src.components.data_ingestion import DataIngenstion
from src.components.data_validation import DataValidationArtifact, DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher
from src.constant.s3_bucket import TRAINING_BUCKET_NAME
from src.cloud_storage.s3_syncer import S3Sync
from src.constant.training_pipeline import SAVED_MODEL_DIR
class TrainPipeline:
    
    def __init__(self):
        is_pipeline_running = False
        self.training_pipeline_config = TrainingPipelineConfig()
        
        
        #self.training_pipeline_config = training_pipeline_config
        
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info('Starting data ingestion')
            data_ingestion = DataIngenstion(data_ingestion_config=self.data_ingestion_config)
            data_ingesntion_artifact = data_ingestion.initiate_data_ingestion()
            
            logging.info(f'Data ingestion completed and artifact: {data_ingesntion_artifact}')
            return data_ingesntion_artifact
        except Exception as e:
            raise ModelException(e,sys)
        
      
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("start data validation")
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=data_validation_config)
            data_validation_artifact =data_validation.initiate_data_validation()
            logging.info("data validation is completed")
            return data_validation_artifact
        except Exception as e:
            raise ModelException(e,sys)  
        
        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                     data_transformation_config=data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise ModelException(e,sys)
        
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerconfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                         data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise ModelException(e,sys)
        
        
    def start_model_evaluation(self,data_validation_artifact,
                               model_trainer_artifact:ModelTrainerArtifact):
        try:
            model_evaluation_config = ModelEvauationConfig(training_pipeline_config=self.training_pipeline_config)
            model_evaluation = ModelEvaluation(model_eval_config=model_evaluation_config,
                                               data_validation_artifact=data_validation_artifact,
                                               model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise ModelException(e,sys)
        
        
    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(trainig_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config=model_pusher_config,
                                       model_eval_artifact=model_evaluation_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise ModelException(e,sys)
          
    def sync_artifact_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            S3Sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_buket_url)
        except Exception as e:
            raise ModelException(e,sys)
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            S3Sync.sync_folder_to_s3(folder=SAVED_MODEL_DIR, aws_bucket_url=aws_buket_url)
        except Exception as e:
            raise ModelException(e,sys)   
           
    def run_pipeline(self):
        try:
            TrainPipeline.is_pipeline_running = True
            
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_validation_artifact=data_validation_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact)
            
            if not model_evaluation_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
            
            TrainPipeline.is_pipeline_running= False
                        
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            
        except Exception as e:
            TrainPipeline.is_pipeline_running= False
            raise ModelException(e,sys)