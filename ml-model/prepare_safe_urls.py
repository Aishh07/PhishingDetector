import pandas as pd

# Tranco dataset read karo
df = pd.read_csv("dataset/top-1m.csv", header=None)

# Columns naam do
df.columns = ["rank", "domain"]

# Top 5000 domains lo
safe_df = df.head(75000)

# Label add karo
safe_df["label"] = 0

# Sirf domain aur label rakho
safe_df = safe_df[["domain", "label"]]

safe_df = safe_df.rename(
    columns={"domain": "url"}
)

safe_df["url"] = "https://" + safe_df["url"].astype(str)

print(safe_df.head())

# Save karo
safe_df.to_csv(
    "dataset/safe_urls_final.csv",
    index=False
)
