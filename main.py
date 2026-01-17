from sensor.exception import SensorException
import os 
from datetime import datetime
import sys 
from sensor.logger import logging
#from sensor.utils import dump_csv_file_to_mongodb_collection
from sensor.pipeline.training_pipeline import TrainingPipeline

# def test_exception(): 
#     try:
#         logging.info("Running a function code which will give error")
#         a=1/0
#     except Exception as e: 
#         raise SensorException(e,sys)
    

if __name__ == "__main__": 
    try: 

        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
    except Exception as e: 
        raise SensorException(e,sys)