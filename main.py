        
from src.pipline.training_pipeline import TrainPipeline
from src.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI, UploadFile, File
from src.pipline.training_pipeline import TrainPipeline
from src.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI, UploadFile, File
from src.constant.application import APP_HOST, APP_PORT
from fastapi import FastAPI
from fastapi import FastAPI
import uvicorn
import sys
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from src.pipline.predict_pipeline import CustomData,PredictionPipeline
from src.logger import logging
from uvicorn import run as app_run

fixed_acidity:float=7.4
volatile_acidity:float =0.700
citric_acid:float = 0.00
residual_sugar:float =1.9
chlorides:float =0.076
free_sulfur_dioxide:float =11.0
total_sulfur_dioxid:float =34.0
density:float =0.99780
pH:float =3.51
sulphates:float =0.56
alcohol:float = 9.4

app = FastAPI()


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

@app.post("/predict")
async def predict_route(fixed_acidity:float,volatile_acidity:float,citric_acid:float,residual_sugar:float,chlorides:float,free_sulfur_dioxide:float,total_sulfur_dioxid:float,density:float,pH:float,sulphates:float,alcohol:float):
    try:
        #get data from user csv file
        data = CustomData(fixed_acidity=fixed_acidity,
                 volatile_acidity=volatile_acidity,
                 citric_acid=citric_acid,
                 residual_sugar=residual_sugar,
                 chlorides=chlorides,
                 free_sulfur_dioxide=free_sulfur_dioxide,
                 total_sulfur_dioxid=total_sulfur_dioxid,
                 density=density,
                 pH=pH,
                 sulphates=sulphates,
                 alcohol=alcohol)
        pred_data = data.get_data_as_data_frame()
        print(pred_data)
        
        predict_pipeline = PredictionPipeline()
        results = predict_pipeline.predict(pred_data)
        results =+ 3
        return Response(f"Wine Quality is {results}")
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
