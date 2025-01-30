# Read more about OpenTelemetry here:
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
from loguru import logger
from time import time
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from prometheus_client import start_http_server
import pandas as pd
from pydantic import BaseModel
import joblib

# Start Prometheus client
start_http_server(port=8099, addr="0.0.0.0")

# Service name is required for most backends
resource = Resource(attributes={SERVICE_NAME: "predict-diabetes"})

# Exporter to export metrics to Prometheus
reader = PrometheusMetricReader()

# Meter is responsible for creating and recording metrics
provider = MeterProvider(resource=resource, metric_readers=[reader])
set_meter_provider(provider)
meter = metrics.get_meter("diabetes", "0.1.2")

# Create your first counter
counter = meter.create_counter(
    name="diabetes_request_counter",
    description="Number of diabetes requests"
)

histogram = meter.create_histogram(
    name="diabetes_response_histogram",
    description="diabetes response histogram",
    unit="seconds",
)

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

# Intialize instance
app = FastAPI()

# Check if api works
@app.get("/")
def check_health():
    return {"status": "OK"}

# Predict
@app.post("/predict")
def predict(data):
    # starting time
    starting_time = time()

    logger.info("Making predictions...")
    logger.info(data)
    logger.info(jsonable_encoder(data))
    logger.info(pd.DataFrame(jsonable_encoder(data), index=[0]))
    pred = model.predict(pd.DataFrame(jsonable_encoder(data), index=[0]))[0]

    # Labels for all metrics
    label = {"api": "/predict"}

    # Increase the counter
    counter.add(1, label)

    # Mark the end of the response
    ending_time = time()
    elapsed_time = ending_time - starting_time

    # Add histogram
    logger.info("Elapsed time: ", elapsed_time)
    logger.info(elapsed_time)
    histogram.record(elapsed_time, label)

    return {"Has diabetes": ["Yes", "No"][pred]}