import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

INPUT_FILE  = "../dataset/features_dataset_v2.csv"
OUTPUT_MODEL = "phishing_url_model_v2.pkl"

print(f"Loading: {INPUT_FILE}")
df = pd.read_csv(INPUT_FILE).dropna()
print(f"  Rows     : {len(df)}")
print(f"  Features : {df.shape[1]-1}")

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print(f"\nTrain: {len(X_train)} | Test: {len(X_test)}")

print("\nTraining RandomForest... (2-3 min)")
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)

# ── Evaluation ────────────────────────────────────────────────
y_pred = model.predict(X_test)
print("\n" + "="*45)
print("  RESULTS")
print("="*45)
print(classification_report(y_test, y_pred,
      target_names=["Safe","Phishing"]))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ── Feature importance ────────────────────────────────────────
print("\nTop 10 Feature Importance:")
imp = pd.Series(model.feature_importances_, index=X.columns)
print(imp.nlargest(10).to_string())

# ── Save ──────────────────────────────────────────────────────
joblib.dump(model, OUTPUT_MODEL)
print(f"\n  MODEL SAVED → {OUTPUT_MODEL}")