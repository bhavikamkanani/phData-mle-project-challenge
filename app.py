import json
import pathlib
import pickle

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_DIR = pathlib.Path("model")
MODEL_PATH = MODEL_DIR / "model.pkl"
FEATURES_PATH = MODEL_DIR / "model_features.json"
DEMOGRAPHICS_PATH = pathlib.Path("data/zipcode_demographics.csv")

# Load trained model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Load feature list
with open(FEATURES_PATH, "r") as f:
    MODEL_FEATURES = json.load(f)

# Load demographics data
demographics = pd.read_csv(DEMOGRAPHICS_PATH, dtype={"zipcode": str})


# -------------------
# Define FastAPI app
# -------------------
app = FastAPI(title="House Price Prediction API", version="1.0")


class HouseFeatures(BaseModel):
    bedrooms: float
    bathrooms: float
    sqft_living: float
    sqft_lot: float
    floors: float
    sqft_above: float
    sqft_basement: float
    zipcode: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(input_data: HouseFeatures):

    df = pd.DataFrame([input_data.dict()])
    df = df.merge(demographics, how="left", on="zipcode").drop(columns="zipcode")

    df = df.reindex(columns=MODEL_FEATURES, fill_value=0)

    prediction = model.predict(df)[0]

    return {
        "prediction": float(prediction),
        "model_version": "v4",
    }
