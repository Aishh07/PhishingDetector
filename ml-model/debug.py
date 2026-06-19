import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from create_features_dataset import extract_features

urls = [
    "https://accounts.google.com/signin",
    "https://secure.paypal.com/myaccount",
    "https://paypal-login.vercel.app",
]

for url in urls:
    f = extract_features(url)
    print(f"\n{url}")
    print(f"  is_trusted_domain  : {f['is_trusted_domain']}")
    print(f"  legit_brand_domain : {f['legit_brand_domain']}")
    print(f"  contains_secure    : {f['contains_secure']}")
    print(f"  contains_account   : {f['contains_account']}")
    print(f"  contains_signin    : {f['contains_signin']}")