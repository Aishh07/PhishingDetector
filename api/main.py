from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib, pandas as pd
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ml-model"))
from create_features_dataset import extract_features

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml-model", "phishing_url_model_v2.pkl")
model = joblib.load(MODEL_PATH)

class URLRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"status": "Phishing Detector API running"}

@app.post("/predict")
def predict(req: URLRequest):
    url   = req.url.strip()
    feats = extract_features(url)
    X     = pd.DataFrame([feats])
    pred  = int(model.predict(X)[0])
    prob  = round(float(model.predict_proba(X)[0][1]), 4)
    risk  = "high" if prob > 0.7 else "medium" if prob > 0.4 else "low"
    return {
        "url"       : url,
        "prediction": pred,
        "label"     : "phishing" if pred == 1 else "safe",
        "confidence": prob,
        "risk"      : risk,
    }