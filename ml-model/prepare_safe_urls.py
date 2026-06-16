import pandas as pd

# Tranco dataset read karo
df = pd.read_csv("dataset/top-1m.csv", header=None)

# Columns naam do
df.columns = ["rank", "domain"]

# Top 5000 domains lo
safe_df = df.head(5000)

# Label add karo
safe_df["label"] = 0

# Sirf domain aur label rakho
safe_df = safe_df[["domain", "label"]]

print(safe_df.head())

# Save karo
safe_df.to_csv("dataset/safe_urls.csv", index=False)

print("\nSaved Successfully!")
print("Total Safe URLs:", len(safe_df))