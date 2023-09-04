from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from src.exception import ModelException
import sys
from src.logger import logging
from src.entity.artifact_entity import DataIngestionArtifact
from src.components.data_ingestion import DataIngenstion
class TrainPipeline:
    
    def __init__(self):
        
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
        
      
    def start_data_validatio(self):
        try:
            pass
        except Exception as e:
            raise ModelException(e,sys)  
        
        
    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise ModelException(e,sys)
        
        
    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise ModelException(e,sys)
        
        
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise ModelException(e,sys)
        
        
    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise ModelException(e,sys)
          
          
    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            
        except Exception as e:
            raise ModelException(e,sys)