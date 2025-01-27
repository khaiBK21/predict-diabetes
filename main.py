import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from loguru import logger
from pydantic import BaseModel

# Intialize instance
app = FastAPI()

# Define request body
class DiabetesMeasure(BaseModel):
    Pregnancies: int = 6
    Glucose: int = (
        148
    )
    BloodPressure: int = 72
    SkinThickness: int = 35
    Insulin: int = 0
    BMI: float = 33.6
    DiabetesPedigreeFunction: float = 0.627
    Age: int = 50

# Load model
model = joblib.load("./models/model.pkl")

# Check if api works
@app.get("/")
def check_health():
    return {"status": "OK"}

# initialize cache
cache = {}

# Predict
@app.post("/predict")
def predict(data):
    logger.info("Make predictions ...")
    logger.info(data)
    logger.info(jsonable_encoder(data))
    logger.info(pd.DataFrame(jsonable_encoder(data), index=[0]))
    pred = model.predict(pd.DataFrame(jsonable_encoder(data), index=[0]))[0]
    return {"Has diabetes": ["Yes", "No"][pred]}

# Predict cache
@app.post("/predict_cache")
def predict_cache(data):
    if str(data) in cache:
        logger.info("Getting result from cache ...")
        return cache[str(data)]
    else:
        logger.info("Make predictions ...")
        logger.info(data)
        logger.info(jsonable_encoder(data))
        logger.info(pd.DataFrame(jsonable_encoder(data), index=[0]))
        pred = model.predict(pd.DataFrame(jsonable_encoder(data), index=[0]))[0]
        result = {"Has diabetes": ["Yes", "No"][pred]}
        cache[str(data)] = result
        return result