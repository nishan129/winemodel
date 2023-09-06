import os

# define common constant variable for training pipeline
TARGET_COLUMN = 'quality'
PIPELINE_NAME = 'src'
ARTIFACT_DIR = 'artifact'
FILE_NAME = 'wine.csv'

TRAIN_FILE_NAME = 'train.csv'
TEST_FILE_NAME = 'test.csv'

PREPROCSSING_OBJECT_FILE_NAME = 'preprocessing.pkl'
MODEL_FILE_NAME = 'model.pkl'
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = 'winedata'
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURES_STORE_DIR : str = 'feature_store'
DATA_INGESTION_INGESTED_DIR : str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION : float = 0.2


"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VADIL_DIR: str = 'validated'
DATA_VALIDATION_INVALID_DIR: str = 'invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = 'report.yaml'

"""
Data Transoformation related constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_DATA_DIR: str = 'transformed'
DATA_TRANSFORMATION_TRANSFORMED_DIR: str = 'transformed_objects'

"""
Model Trainer related constant start with MODEL TRAINER VAR NAME
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = 'trained_models'
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FITING_UNDER_FITING_THRESHOLD: float = 0.02