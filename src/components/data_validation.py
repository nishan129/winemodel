from src.logger import logging
from src.exception import ModelException
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
import pandas as pd
import sys,os
from src.utils.main_utils import write_yaml_file
from scipy.stats import ks_2samp

class DataValidation:
    
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            logging.info("Data validation all parameter is set")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            
        except Exception as e:
            raise ModelException(e,sys)
    
    def detect_dataset_drift(self,base_df, current_df, threshold=0.05)->bool:
        try:
            logging.info("Data drift detect is start")
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold<= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    column:{
                        "p_value":float(is_same_dist.pvalue),
                        "drift_status":is_found     
                    }})
            drift_report_file_path =self.data_validation_config.drift_report_file_path
            
            #create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            logging.info("Data drift process is End")
            return status
        except Exception as e:
            raise ModelException(e,sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ModelException(e,sys)
    
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Train and test file is defind")
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            # Reading data from train and test file path
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            logging.info("data validation train and test file is completed")
        except Exception as e:
            raise ModelException(e,sys)