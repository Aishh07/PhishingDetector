import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier

df = pd.read_csv("dataset/Phishing_Legitimate_full.csv")

X = df.drop(["CLASS_LABEL", "id"], axis=1)
y = df["CLASS_LABEL"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))

import joblib

joblib.dump(model, "ml-model/phishing_model.pkl")

print("Model Saved Successfully!")