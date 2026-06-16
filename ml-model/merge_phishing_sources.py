import pandas as pd

old_urls = open(
    "dataset/phishing_urls.txt",
    encoding="utf-8"
).read().splitlines()

new_urls = open(
    "dataset/openphish_urls.txt",
    encoding="utf-8"
).read().splitlines()

all_urls = list(
    set(old_urls + new_urls)
)

df = pd.DataFrame({
    "url": all_urls,
    "label": 1
})

df.to_csv(
    "dataset/phishing_urls_merged.csv",
    index=False
)

print(df.head())
print("\nTotal URLs:", len(df))