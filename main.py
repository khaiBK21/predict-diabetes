import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from loguru import logger
from pydantic import BaseModel

# Intialize instance
app = FastAPI()

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
    pred = model.predict()

# Predict cache
@app.post("/predict_cache")
def predict_cache(data):
    if str(data) in cache:
        logger.info("Getting result from cache ...")
        return cache[str(data)]
    else:
        logger.info("Making predictions ...")
        logger.info(data)
        pred = model.predict()
        cache[str(data)] = [pred[0]]

        return {"result": [pred[0]]}