from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os 
import json
from datetime import datetime
import sys 
from sensor.logger import logging
#from sensor.utils import dump_csv_file_to_mongodb_collection
from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.utils.main_utils import load_object,read_yaml_file
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.pipeline import training_pipeline
from sensor.constant.training_pipeline import SAVED_MODEL_DIR


from fastapi import FastAPI
from sensor.constant.application import APP_HOST,APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Response
import pandas as pd 

app = FastAPI()
origins = ["*"]
#corss origin resource sharing 
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")



@app.get("/train")
async def train():
    try: 

        training_pipeline_ = TrainingPipeline() 
        if training_pipeline_.is_pipeline_running:
            return Response("Training pipeling is already running.")
        training_pipeline_.run_pipeline()
        return Response("Training Sucessfully Completed!")
    except Exception as e: 
        return Response(f"Error Occurred! {e}")



@app.get("/predict")
async def predict(): 
    try:
        data = pd.read_csv(r"C:\Users\pc\Desktop\_Machine_Learning_Projects\LiveSensor\_testdata.csv")
        #convert it into dataframe 
        df = pd.DataFrame(data)
        df  = df.drop(columns=['br_000','bq_000','bp_000','ab_000','cr_000','bo_000','bn_000'],axis=1)

        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)

        best_model_path = model_resolver.get_best_model_path()
        model =load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        print(df.head())
        data = df['predicted_column']

        #get the prediction output as you want 
        return {
            "message": "Predicted Successfully!",
            "data": data
        }
    

    except Exception as e: 
        raise SensorException(e,sys)






def main():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
    except Exception as e: 
        print(e)
        logging.exception(e)
    

if __name__ == "__main__": 
    try: 
        app_run(app,host=APP_HOST,port=APP_PORT)
        
       
    except Exception as e: 
        raise SensorException(e,sys)