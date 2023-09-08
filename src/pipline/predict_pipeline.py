import sys
import pandas as pd
from src.exception import ModelException
from src.utils.main_utils import load_object
from src.constant.training_pipeline import SAVED_MODEL_DIR
from src.ml.model.estimator import ModelResolver


class PredictionPipeline:
    def __init__(self):
        pass
    
    def predict(self,feature):
        try:
            model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
            if not model_resolver.is_model_exists():
                return ("Model is not available")
            
            best_model_path = model_resolver.get_best_model_path()
            print(best_model_path)
            model = load_object(file_path=best_model_path)
            preds = model.predict(feature)[0]
            return preds
        except Exception as e:
            raise ModelException(e,sys)
    
class CustomData:
    def __init__(self,fixed_acidity:float,
                 volatile_acidity:float,
                 citric_acid:float,
                 residual_sugar:float,
                 chlorides:float,
                 free_sulfur_dioxide:float,
                 total_sulfur_dioxide:float,
                 density:float,
                 pH:float,
                 sulphates:float,
                 alcohol:float):
        self.fixed_acidity = fixed_acidity
        self.volatile_acidity = volatile_acidity
        self.citric_acid = citric_acid
        self.residual_sugar = residual_sugar
        self.chlorides = chlorides
        self.free_sulfur_dioxide = free_sulfur_dioxide
        self.total_sulfur_dioxide = total_sulfur_dioxide
        self.density = density
        self.pH = pH
        self.sulphates = sulphates
        self.alcohol = alcohol
        
        
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "fixed acidity" : [self.fixed_acidity],
                "volatile acidity" : [self.volatile_acidity],
                "citric acid" : [self.citric_acid],
                "residual sugar" : [self.residual_sugar],
                "chlorides" : [self.chlorides],
                "free sulfur dioxide" : [self.free_sulfur_dioxide],
                "total sulfur dioxide" : [self.total_sulfur_dioxide],
                "density" : [self.density],
                "pH" : [self.pH],
                "sulphates" : [self.sulphates],
                "alcohol" : [self.alcohol]
            }
            
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise ModelException(e,sys)