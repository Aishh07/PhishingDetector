import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report
)
from xgboost import XGBClassifier
import joblib

# Load dataset
df = pd.read_csv("dataset/features_dataset.csv")

# Features
X = df.drop("label", axis=1)

# Target
y = df["label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1
)

# Train
model.fit(X_train, y_train)

# Predict
pred = model.predict(X_test)

# Accuracy
print("Accuracy:", accuracy_score(y_test, pred))
print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        pred
    )
)

# Save model
joblib.dump(
    model,
    "ml-model/phishing_url_model.pkl"
)

print("Model Saved!")