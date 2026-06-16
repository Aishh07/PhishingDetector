from urllib.parse import urlparse

def extract_features(url):
    parsed = urlparse(url)

    features = {
        "url_length": len(url),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "has_https": 1 if parsed.scheme == "https" else 0,
        "contains_login": 1 if "login" in url.lower() else 0
    }

    return features


test_urls = [
    "https://google.com",
    "https://github.com",
    "https://paypa1-login-secure.xyz/account",
    "http://bank-account-verify-update.net"
]

for url in test_urls:
    print("\nURL:", url)
    print(extract_features(url))