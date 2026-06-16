import pandas as pd

df = pd.read_csv("dataset/safe_urls.csv")

df["url"] = "https://" + df["domain"]

df = df[["url", "label"]]

df.to_csv("dataset/safe_urls_final.csv", index=False)

print(df.head())
print("Saved!")