# ============================================================
# main.py - Cardiovascular Risk Prediction API (38 Features)
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

app = FastAPI(
    title="Cardiovascular Risk Prediction API",
    description="API for cardiovascular risk prediction",
    version="3.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model, scaler, and feature names
MODEL_PATH = "cardiovascular_model.pkl"
SCALER_PATH = "scaler.pkl"
FEATURES_PATH = "feature_names_fixed.pkl"

# Check files exist
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Error: '{MODEL_PATH}' not found!")
if not os.path.exists(SCALER_PATH):
    raise RuntimeError(f"Error: '{SCALER_PATH}' not found!")
if not os.path.exists(FEATURES_PATH):
    raise RuntimeError(f"Error: '{FEATURES_PATH}' not found!")

# Load all files
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_names = joblib.load(FEATURES_PATH)

print(f"✅ Model loaded with {len(feature_names)} features")
print(f"✅ First 5 features: {feature_names[:5]}")


class PredictionRequest(BaseModel):
    features: list


@app.get("/")
def read_root():
    return {
        "message": "Cardiovascular Risk Prediction API",
        "status": "healthy",
        "features_count": len(feature_names)
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": True, "features_count": len(feature_names)}


@app.get("/features")
def get_features():
    return {"features": feature_names, "count": len(feature_names)}


@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        # Check feature count
        if len(request.features) != len(feature_names):
            raise HTTPException(
                status_code=400,
                detail=f"Expected {len(feature_names)} features, got {len(request.features)}"
            )

        # Create DataFrame with correct column names
        features_df = pd.DataFrame([request.features], columns=feature_names)

        # Scale features
        features_scaled = scaler.transform(features_df)

        # Predict
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        confidence = float(max(probabilities))

        # Map: 1 = Normal, 0 = Abnormal
        result = "Normal" if prediction == 1 else "Abnormal"

        return {
            "prediction": result,
            "confidence": confidence,
            "probabilities": {
                "Abnormal": float(probabilities[0]),
                "Normal": float(probabilities[1])
            }
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)