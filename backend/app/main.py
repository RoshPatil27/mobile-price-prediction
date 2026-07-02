"""
Mobile Price Range Prediction API
==================================

A small FastAPI service that wraps the trained scikit-learn model and
exposes it over HTTP so the React frontend (or any other client) can
request predictions.

Run locally:
    uvicorn app.main:app --reload --port 8000

Then open:
    https://mobile-price-api.onrender.com/docs   (interactive Swagger UI)
"""

import json
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ModelInfoResponse, PhoneSpecs, PredictionResponse

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"

app = FastAPI(
    title="Mobile Price Range Prediction API",
    description="Predicts a mobile phone's price range (0=Low Cost to 3=Very High Cost) from its hardware specifications.",
    version="1.0.0",
)

# Allow the React dev server (and any frontend) to call this API.
# For production, replace "*" with your deployed frontend's exact origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Load model artifacts once at startup
# ---------------------------------------------------------------------------
model = joblib.load(MODEL_DIR / "model.pkl")
scaler = joblib.load(MODEL_DIR / "scaler.pkl")

with open(MODEL_DIR / "feature_names.json") as f:
    FEATURE_NAMES = json.load(f)

with open(MODEL_DIR / "metrics.json") as f:
    METRICS = json.load(f)

CLASS_LABELS = METRICS["class_labels"]  # {"0": "Low Cost", ...}


@app.get("/", tags=["Health"])
def root():
    return {
        "service": "Mobile Price Range Prediction API",
        "status": "ok",
        "model": METRICS["best_model"],
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}


@app.get("/model-info", response_model=ModelInfoResponse, tags=["Model"])
def model_info():
    """Return metadata about the trained model: which algorithm was
    selected and how every candidate model performed during training."""
    return METRICS


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(specs: PhoneSpecs):
    """Predict the price range for a phone given its hardware specs."""
    try:
        # Ensure the feature order exactly matches what the model was trained on
        row = pd.DataFrame([specs.model_dump()])[FEATURE_NAMES]
        scaled = scaler.transform(row)

        pred = int(model.predict(scaled)[0])

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(scaled)[0]
        else:
            # Fallback for models without predict_proba: one-hot the prediction
            proba = [1.0 if i == pred else 0.0 for i in range(len(CLASS_LABELS))]

        probabilities = {CLASS_LABELS[str(i)]: round(float(p), 4) for i, p in enumerate(proba)}

        return PredictionResponse(
            price_range=pred,
            label=CLASS_LABELS[str(pred)],
            confidence=round(float(proba[pred]), 4),
            probabilities=probabilities,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
