# 🛡️ PhishingDetector

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi)
![scikit-learn](https://img.shields.io/badge/RandomForest-ML_Model-orange?style=for-the-badge&logo=scikit-learn)
![Chrome](https://img.shields.io/badge/Chrome-Extension-yellow?style=for-the-badge&logo=googlechrome)
![Render](https://img.shields.io/badge/Deployed-Render-purple?style=for-the-badge)
![Accuracy](https://img.shields.io/badge/Test_Accuracy-100%25-brightgreen?style=for-the-badge)

**Real-time phishing URL detection — Chrome Extension + ML Backend**

[🌐 Live API](https://phishingdetector-fe2z.onrender.com) &nbsp;|&nbsp; [📖 API Docs](https://phishingdetector-fe2z.onrender.com/docs)

</div>

---

## What it does

PhishingDetector scans any URL in real time and tells you whether it is **safe or phishing** — directly inside Chrome, powered by a Machine Learning model trained on 150,000+ real-world URLs.

---

## How it works

```
Browser Tab URL
      │
      ▼
Chrome Extension  ──POST /predict──▶  FastAPI (Render)
                                             │
                                             ▼
                                   Feature Extraction
                                   (30 URL features)
                                             │
                                             ▼
                                   Random Forest Model
                                             │
                                             ▼
                              { label, confidence, risk }
                                             │
      ◀──────────────────────────────────────┘
  🟢 SAFE / 🚨 PHISHING displayed in popup
```

---

## Live API

**Base URL:** `https://phishingdetector-fe2z.onrender.com`

```
POST /predict
Content-Type: application/json

{ "url": "https://paypal-login.vercel.app" }
```

```json
{
  "url": "https://paypal-login.vercel.app",
  "prediction": 1,
  "label": "phishing",
  "confidence": 0.7081,
  "risk": "high"
}
```

---

## Dataset

| Source | Type | Count |
|--------|------|-------|
| PhishTank | Phishing | 65,770 |
| OpenPhish | Phishing | 300 |
| URLhaus | Phishing | 3+ |
| Tranco Top-1M | Safe | 75,000 |
| Modern hosting (manual) | Safe | 128 |
| Hard negative edge cases | Both | 166 |
| **Total** | **Balanced** | **150,192** |

---

## ML Model

**Algorithm:** Random Forest (200 trees, max_depth=20)

**30 engineered features across 5 categories:**

| Category | Features |
|----------|----------|
| URL structure | length, dots, hyphens, digits, https |
| Hostname | length, subdomains, depth, digit ratio, IP detection |
| Path | length, entropy, double slash |
| Keywords | login, verify, secure, bank, account, paypal, signin |
| Security signals | brand_on_legit_host, is_trusted_domain, suspicious_tld, special chars |

**Most impactful custom feature:**

```python
# Catches: paypal-login.vercel.app  → PHISHING
# Allows:  portfolio.vercel.app     → SAFE

brand_on_legit_host = (
    hostname.endswith("vercel.app")  # legit hosting platform
    AND "paypal" in subdomain        # brand name spoofed
)
```

---

## Results

```
              precision    recall   f1-score
        Safe       1.00      1.00       1.00
    Phishing       1.00      1.00       1.00
    accuracy                            1.00   (30,039 test samples)

Confusion Matrix:
  False Positives: 4   (safe marked phishing)
  False Negatives: 3   (phishing missed)
```

**Real-world test — 22/22 correct ✅**

| URL | Result | Confidence |
|-----|--------|------------|
| https://www.google.com | ✅ SAFE | 3% |
| https://github.com | ✅ SAFE | 0% |
| https://accounts.google.com/signin | ✅ SAFE | 13% |
| https://secure.paypal.com/myaccount | ✅ SAFE | 21% |
| https://portfolio.vercel.app | ✅ SAFE | 11% |
| https://paypal-login.vercel.app | 🚨 PHISHING | 71% |
| https://netflix-verify.netlify.app | 🚨 PHISHING | 75% |
| https://amazon-secure.github.io | 🚨 PHISHING | 59% |
| http://193.107.23.187/login | 🚨 PHISHING | 92% |
| https://secure-paypal-login.blogspot.com | 🚨 PHISHING | 97% |

---

## Key Challenges Solved

**1. Model learning platform bias**
> Platforms like `vercel.app`, `netlify.app`, `github.io` appeared only in phishing data → model incorrectly flagged all subdomains as phishing.
> Fixed by adding 128+ legitimate subdomains from these platforms to safe dataset.

**2. Feature dominance causing overfitting**
> `path_length` alone had 99.8% feature importance — model ignoring all other signals.
> Fixed by engineering 10 new diverse features, reducing `path_length` importance to 24.9%.

**3. False positives on real login pages**
> `accounts.google.com/signin` was flagged as phishing due to keywords `account` + `signin`.
> Fixed by adding `is_trusted_domain` feature and including real login pages in training data.

---

## Tech Stack

| Layer | Tech |
|-------|------|
| ML Model | scikit-learn RandomForest |
| Feature Engineering | Python, tldextract, urllib |
| Backend API | FastAPI + Uvicorn |
| Deployment | Render |
| Extension | Chrome Extension (JS, HTML, CSS) |
| Data Sources | PhishTank, OpenPhish, URLhaus, Tranco |

---

## Project Structure

```
PhishingDetector/
├── api/
│   └── main.py                      # FastAPI backend
├── chrome-extension/
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js                     # Extension logic
├── ml-model/
│   ├── build_dataset.py             # Dataset collection
│   ├── merge_safe_datasets.py       # Dataset balancing
│   ├── create_features_dataset.py   # 30-feature extraction
│   ├── train_url_model.py           # Model training
│   ├── test_model.py                # Evaluation
│   └── phishing_url_model_v2.pkl   # Trained model
└── requirements.txt
```

---

## Run Locally

```bash
git clone https://github.com/Aishh07/PhishingDetector.git
cd PhishingDetector
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Load extension: `chrome://extensions/` → Developer mode → Load unpacked → select `chrome-extension/`

---

<div align="center">
Made by <a href="https://github.com/Aishh07">Aishh07</a>
</div>
