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
        
class DataValidationConfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_VADIL_DIR
        )
        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR
        )
        # for vailid train test file path
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        # for invalid train test file path
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)
        # for drift data yaml file path
        self.drift_report_file_path :str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        
        
class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path: str = os.path.join(
            self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv","npy"))
        
        self.transformed_test_file_path :str = os.path.join(
            self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv","npy"))
        
        self.transformed_object_file_path: str = os.path.join(
            self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            training_pipeline.PREPROCSSING_OBJECT_FILE_NAME)
        

class ModelTrainerconfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path: str = os.path.join(self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                         training_pipeline.MODEL_FILE_NAME)
        self.exepted_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold: float = training_pipeline.MODEL_TRAINER_OVER_FITING_UNDER_FITING_THRESHOLD