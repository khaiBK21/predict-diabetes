# Read more about OpenTelemetry here:
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from pydantic import BaseModel
import joblib
from loguru import logger
import pandas as pd

set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "predict-diabetes"}))
)
tracer = get_tracer_provider().get_tracer("diabetes", "0.1.2")

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
get_tracer_provider().add_span_processor(span_processor)

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
    logger.info("Make predictions ...")
    logger.info(data)
    logger.info(jsonable_encoder(data))
    logger.info(pd.DataFrame(jsonable_encoder(data), index=[0]))
    pred = model.predict(pd.DataFrame(jsonable_encoder(data), index=[0]))[0]
    return {"Has diabetes": ["Yes", "No"][pred]}