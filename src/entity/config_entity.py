from datetime import datetime
import os
from src.constant.training_pipeline import PIPELINE_NAME, ARTIFACT_DIR
from src.constant import training_pipeline

class TrainingPipelineConfig:
    
    def __init__(self, timestamp=datetime.now()):
        
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name:str = PIPELINE_NAME
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, timestamp)
        self.timestamp :str = timestamp
        

class DataIngestionConfig:
    
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )
        
        self.feature_stor_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURES_STORE_DIR, training_pipeline.FILE_NAME
        )
        
        self.trainig_file_path : str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
        )
        
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME
        )
        
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name : str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        pass
        
        