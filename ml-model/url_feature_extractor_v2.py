from urllib.parse import urlparse
import re

def extract_features(url):

    parsed = urlparse(url)

    features = {}

    # Length
    features["url_length"] = len(url)

    # Dots
    features["num_dots"] = url.count(".")

    # Hyphens
    features["num_hyphens"] = url.count("-")

    # Digits
    features["num_digits"] = len(
        re.findall(r"\d", url)
    )

    # HTTPS
    features["has_https"] = (
        1 if parsed.scheme == "https" else 0
    )

    # Keywords
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


test_url = "https://paypal-secure-login.xyz"

print(extract_features(test_url))