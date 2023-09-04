from src.exception import ModelException
from src.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
import sys,os
from pandas import DataFrame
from src.data_access.winedata import WineData
from sklearn.model_selection import train_test_split


class DataIngenstion:
    
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        
        
    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export mongo db collection record as data frame in to feature
        """
        try:
            logging.info("export data from mongo db to feature store")
            wine_data = WineData()
            dataframe = wine_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            
            feature_store_file_path = self.data_ingestion_config.feature_stor_file_path
            
            # creating folder
            
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            
            return dataframe
            
        except Exception as e:
            raise ModelException(e,sys)

    
    def split_data_as_train_test_split(self, dataframe:DataFrame) -> None:
        """
        Feature store dataset will be split into train and test file
        """
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42
            )
            logging.info("Preformed train test split on dataset")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            
            dir_path = os.path.dirname(self.data_ingestion_config.trainig_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info(f"Exporting train and test file path")
            
            train_set.to_csv(self.data_ingestion_config.trainig_file_path,index=False,header=True)
            
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            
            logging.info(f"Exported train and test file path")
        except Exception as e:
            raise  ModelException(e,sys)
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test_split(dataframe=dataframe)
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.trainig_file_path,
                                  test_file_path=self.data_ingestion_config.testing_file_path)
            
            return data_ingestion_artifact
        except Exception as e:
            raise ModelException(e,sys)