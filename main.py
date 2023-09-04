from src.configuration.mongo_db_connection import MongoDBClient
from src.exception import ModelException
import os,sys
from src.logger import logging
from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from src.pipline.training_pipeline import TrainPipeline

if __name__ == '__main__':
    try:
        train = TrainPipeline()
        train.run_pipeline()
        
        
    except Exception as e:
        raise ModelException(e,sys)
    
    