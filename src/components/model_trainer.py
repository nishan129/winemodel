from src.exception import ModelException
from src.logger import logging
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerconfig
from src.ml.metric.classification_metric import get_classification_score
from src.utils.main_utils import load_numpy_array_data, load_object, save_object
from src.ml.model.estimator import Model
from sklearn.linear_model import LogisticRegression
import os
import sys
from xgboost import XGBClassifier

class ModelTrainer:
    
    def __init__(self,model_trainer_config:ModelTrainerconfig,
                 data_transformation_artifact:DataTransformationArtifact):
        
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise ModelException(e,sys)
        
    # def perform_hyper_parameter_tuning(self):
    #     pass
        
    def train_model(self, x_train,y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train,y_train)
            return xgb_clf
        except Exception as e:
            raise ModelException(e,sys)
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            logging.info("Loding data from transformed file path")
            # loding training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            x_train,y_train,x_test,y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )
            
            model = self.train_model(x_train=x_train,y_train=y_train)
            y_train_pred = model.predict(x_train)
            classification_train_metric =get_classification_score(y_true=y_train,y_pred=y_train_pred)
            
            if classification_train_metric.f1_score<=self.model_trainer_config.exepted_accuracy:
                raise Exception("Train Model is not good to provide exepted accuracy")
            
            
            test_pred = model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test,y_pred=test_pred)
            
            
            # check overfiting and underfiting
            diff = abs(classification_train_metric.f1_score - classification_test_metric.f1_score)
            
            if diff>self.model_trainer_config.overfitting_underfitting_threshold:
                #raise Exception("Model is not good try to do more experiments")
                pass
            
            
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            wine_model = Model(preprocessor=preprocessor, model=model)
            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=wine_model)
            
            # model trainer artifact
            
            model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                 train_metric_artifact=classification_train_metric,test_metric_artifact=classification_test_metric)
            
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise ModelException(e,sys)