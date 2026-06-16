import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# Dataset load
df = pd.read_csv("dataset/Phishing_Legitimate_full.csv")

# Features
X = df.drop(["CLASS_LABEL", "id"], axis=1)

# Target
y = df["CLASS_LABEL"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

# Training
model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)

# Results
print("\nAccuracy:")
print(accuracy_score(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))