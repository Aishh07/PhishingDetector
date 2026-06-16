import pandas as pd

# Safe URLs
safe_df = pd.read_csv("dataset/safe_urls_final.csv")

phish_df = pd.read_csv("dataset/phishing_urls_merged.csv")

# Balance dataset
safe_df = safe_df.sample(
    n=len(phish_df),
    random_state=42
)

# Merge
final_df = pd.concat([safe_df, phish_df])

# Shuffle
final_df = final_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Save
final_df.to_csv(
    "dataset/final_dataset.csv",
    index=False
)

print(final_df.head())
print("\nTotal Records:", len(final_df))
print("\nLabel Distribution:")
print(final_df["label"].value_counts())