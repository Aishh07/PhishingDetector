import pandas as pd
from urllib.parse import urlparse
import re


def extract_features(url):

    parsed = urlparse(url)

    features = {}

    # URL Length
    features["url_length"] = len(url)

    # Number of Dots
    features["num_dots"] = url.count(".")

    # Number of Hyphens
    features["num_hyphens"] = url.count("-")

    # Number of Digits
    features["num_digits"] = len(
        re.findall(r"\d", url)
    )

    # HTTPS
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

    # Underscore
    features["num_underscore"] = url.count("_")

    # Percent Symbol
    features["num_percent"] = url.count("%")

    # Hash Symbol
    features["num_hash"] = url.count("#")

    # Suspicious Keywords
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


df = pd.read_csv("dataset/final_dataset.csv")

rows = []

for _, row in df.iterrows():

    features = extract_features(row["url"])

    features["label"] = row["label"]

    rows.append(features)

feature_df = pd.DataFrame(rows)

feature_df.to_csv(
    "dataset/features_dataset.csv",
    index=False
)

print(feature_df.head())

print("\nTotal Records:", len(feature_df))