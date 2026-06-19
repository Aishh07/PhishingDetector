import joblib, pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from create_features_dataset import extract_features

model = joblib.load("phishing_url_model_v2.pkl")

TEST_URLS = [
    # ── SAFE honi chahiye (Expected: 0) ───────────────────────
    ("https://www.google.com",                    0),
    ("https://www.facebook.com",                  0),
    ("https://github.com",                        0),
    ("https://portfolio.vercel.app",              0),
    ("https://myblog.netlify.app",                0),
    ("https://johnsmith.github.io",               0),
    ("https://login.github.com",                  0),
    ("https://accounts.google.com/signin",        0),
    ("https://secure.paypal.com/myaccount",       0),
    ("https://myblog.blogspot.com",               0),
    ("https://learningpython.blogspot.com",       0),
    ("https://react-starter.vercel.app",          0),
    ("https://docs-site.pages.dev",               0),

    # ── PHISHING honi chahiye (Expected: 1) ───────────────────
    ("https://paypal-login.vercel.app",           1),
    ("https://netflix-verify.netlify.app",        1),
    ("https://amazon-secure.github.io",           1),
    ("http://193.107.23.187/login",               1),
    ("https://bank-login-secure.pages.dev",       1),
    ("https://apple-id-locked.vercel.app",        1),
    ("https://instagram-verify.netlify.app",      1),
    ("https://secure-paypal-login.blogspot.com",  1),
    ("http://paypal.com.fake-login.xyz/signin",   1),
]

print(f"\n{'URL':<50} {'Exp':>5} {'Got':>10} {'Conf':>6} {'':>3}")
print("-" * 80)

correct = 0
for url, expected in TEST_URLS:
    feats        = extract_features(url)
    X            = pd.DataFrame([feats])
    pred         = int(model.predict(X)[0])
    prob         = model.predict_proba(X)[0][1]
    match        = "✅" if pred == expected else "❌"
    label        = "PHISHING" if pred == 1 else "SAFE    "
    if pred == expected:
        correct += 1
    print(f"{url:<50} {expected:>5} {label:>10}  {prob:.2f}  {match}")

total = len(TEST_URLS)
print(f"\n{'='*80}")
print(f"  Score : {correct}/{total} = {correct/total*100:.0f}%")

if correct == total:
    print("  ✅ Model ready hai — deploy karo!")
elif correct >= total * 0.85:
    print("  ⚠️  Achha hai lekin kuch URLs miss ho rahe hain")
else:
    print("  ❌ Model theek nahi — dataset aur improve karna padega")
print(f"{'='*80}")