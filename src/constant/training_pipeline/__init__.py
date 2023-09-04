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