from src.exception import ModelException
from src.logger import logging
import sys

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline

from src.constant.training_pipeline import TARGET_COLUMN
from src.entity.artifact_entity import (
    DataTransformationArtifact, DataValidationArtifact
)
from src.entity.config_entity import DataTransformationConfig
from src.utils.main_utils import save_numpy_array_data, save_object

class DataTransformation:
    
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        """
        :param data_validation_artifact: Output refrence of data validation artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise ModelException(e,sys)
        
    @staticmethod    
    def read_data(file_path) -> pd.DataFrame:
        try:
            logging.info("Reading data from path start")
            return pd.read_csv(file_path)
        except Exception as e:
            raise ModelException(e,sys)
      
    @classmethod    
    def get_data_transformer_object(cls) -> Pipeline:
        try:
            logging.info("get_data_transformer_object is called")
            robust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy='constant',fill_value=0)
            preprocessor = Pipeline(
                steps=[("Imputer", simple_imputer),# replce missing value with zero
                       ("robust_scaler", robust_scaler)# scale data to use robust scaler and handle outliers
                    ])

            return preprocessor
        except Exception as e:
            raise ModelException(e,sys)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")
            train_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path
            )
            test_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_test_file_path
            )
            preprocessor = DataTransformation.get_data_transformer_object()
    
            #Training data frame
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN] -3
            
            #Test data frame
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN] -3
            
            #preprocessing data
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_features = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_test_features = preprocessor.fit_transform(input_feature_test_df)
            
            
            smt = SMOTE(random_state=42)
            
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                transformed_input_train_features,target_feature_train_df
            )
            
            
            # input_feature_test_final, target_feature_test_final = smt.fit_resample(
            #     transformed_input_test_feature, target_feature_test_df
            # ) this is comment because there data poinst is vary small so smot not resample it so this code is comment
            logging.info("Data resampling is complete")
            
            train_arr = np.c_[input_feature_train_final,np.array(target_feature_train_final)]
            test_arr = np.c_[transformed_input_test_features,np.array(target_feature_test_df)]
            
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
            
            #preparing artifact 
            data_transformation_artifact =  DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            
            logging.info(f"Data transformation is completed and artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise ModelException(e,sys)
