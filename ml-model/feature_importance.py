import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBClassifier

# Dataset
df = pd.read_csv("dataset/Phishing_Legitimate_full.csv")

X = df.drop(["CLASS_LABEL", "id"], axis=1)
y = df["CLASS_LABEL"]

# Train model
model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1
)

model.fit(X, y)

# Importance
importance = model.feature_importances_

feature_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
})

feature_df = feature_df.sort_values(
    by="Importance",
    ascending=False
)

print(feature_df.head(10))

# Plot
plt.figure(figsize=(10,6))
plt.barh(
    feature_df["Feature"][:10],
    feature_df["Importance"][:10]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 10 Important Features")
plt.tight_layout()

plt.show()