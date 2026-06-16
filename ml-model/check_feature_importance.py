import joblib
import pandas as pd

model = joblib.load(
    "ml-model/phishing_url_model.pkl"
)

feature_names = [
    "url_length",
    "num_dots",
    "num_hyphens",
    "num_digits",
    "has_https",
    "hostname_length",
    "path_length",
    "subdomain_count",
    "at_symbol",
    "num_underscore",
    "num_percent",
    "num_hash",
    "contains_login",
    "contains_verify",
    "contains_secure",
    "contains_bank",
    "contains_account",
    "contains_update",
    "contains_paypal",
    "contains_signin"
]

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print(importance_df)