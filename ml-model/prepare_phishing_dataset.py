import pandas as pd

# TXT file read karo
with open("dataset/phishing_urls.txt", "r", encoding="utf-8") as file:
    urls = file.readlines()

# Clean URLs
urls = [url.strip() for url in urls if url.strip()]

# DataFrame
df = pd.DataFrame({
    "url": urls,
    "label": 1
})

# Save CSV
df.to_csv("dataset/phishing_urls.csv", index=False)

print(df.head())
print("\nTotal Phishing URLs:", len(df))
print("Saved Successfully!")