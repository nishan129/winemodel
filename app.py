from src.exception import ModelException
import os,sys
from src.logger import logging
from src.pipline.training_pipeline import TrainPipeline
from src.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI, UploadFile, File
from src.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response, FileResponse
from src.ml.model.estimator import ModelResolver
from src.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
env_file_path=os.path.join(os.getcwd(),"env.yaml")

# def set_env_variable(env_file_path):

#     if os.getenv('MONGO_DB_URL',None) is None:
#         env_config = read_yaml_file(env_file_path)
#         os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.run_pipeline:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict")
async def predict_route(fixed_acidity:float,volatile_acidity:float,citric_acid:float,residual_sugar:float,chlorides:float,free_sulfur_dioxide:float,sulfur_dioxide:float,density:float,pH:float,sulphates:float,alcohol:float):
    try:
        #get data from user csv file
        data = [fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,sulfur_dioxide,density,pH,sulphates,alcohol]
        
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        print(best_model_path)
        model = load_object(file_path=best_model_path)
        y_pred = model.predict([data])
        df = y_pred + 3
        
        #decide how to return file to user.
        return FileResponse(df)
    except Exception as e:
        raise Response(f"Error Occured! {e}")

def main():
    try:
        #set_env_variable(env_file_path)
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__=="__main__":
    #main()
    
    # set_env_variable(env_file_path)
    app_run(app, host=APP_HOST, port=APP_PORT)