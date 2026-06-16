from fastapi import FastAPI
from pydantic import BaseModel

import joblib
import pandas as pd

from urllib.parse import urlparse
import re

app = FastAPI()

# Load model once
model = joblib.load("ml-model/phishing_url_model.pkl")


class URLRequest(BaseModel):
    url: str


def extract_features(url):

    parsed = urlparse(url)

    features = {}

    features["url_length"] = len(url)
    features["num_dots"] = url.count(".")
    features["num_hyphens"] = url.count("-")
    features["num_digits"] = len(
        re.findall(r"\d", url)
    )

    features["has_https"] = (
        1 if parsed.scheme == "https" else 0
    )

    # Hostname Length
    features["hostname_length"] = len(
    parsed.netloc
    )

    # Path Length
    features["path_length"] = len(
    parsed.path
    )

    # Subdomain Count
    features["subdomain_count"] = max(
    0,
    len(parsed.netloc.split(".")) - 2
    )

    # @ Symbol
    features["at_symbol"] = 1 if "@" in url else 0

    # Underscore Count
    features["num_underscore"] = url.count("_")

    # Percent Count
    features["num_percent"] = url.count("%")

    # Hash Count
    features["num_hash"] = url.count("#")

    suspicious_words = [
        "login",
        "verify",
        "secure",
        "bank",
        "account",
        "update",
        "paypal",
        "signin"
    ]

    for word in suspicious_words:
        features[f"contains_{word}"] = (
            1 if word in url.lower() else 0
        )

    return features


@app.get("/")
def home():
    return {
        "message": "Phishing Detector API Running"
    }


@app.post("/predict")
def predict(data: URLRequest):

    features = extract_features(data.url)

    df = pd.DataFrame([features])

    prediction = model.predict(df)[0]

    confidence = float(
        max(model.predict_proba(df)[0])
    )

    return {
        "url": data.url,
        "prediction":
            "PHISHING"
            if prediction == 1
            else "SAFE",

        "confidence":
            round(confidence * 100, 2)
    }