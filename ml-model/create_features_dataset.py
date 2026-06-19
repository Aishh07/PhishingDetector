import pandas as pd
import re, math, collections
from urllib.parse import urlparse
import tldextract

INPUT_FILE  = "../dataset/final_dataset_v2.csv"
OUTPUT_FILE = "../dataset/features_dataset_v2.csv"

KNOWN_BRANDS = [
    "paypal","netflix","facebook","instagram","google","amazon",
    "apple","microsoft","twitter","whatsapp","bank","secure",
    "verify","account","login","update","signin","ebay","steam",
    "discord","binance","coinbase","chase","wellsfargo","tiktok"
]

LEGIT_HOSTING = [
    "github.io","vercel.app","netlify.app","blogspot.com",
    "pages.dev","web.app","firebaseapp.com","glitch.me",
    "replit.com","pythonanywhere.com","onrender.com","railway.app"
]

TRUSTED_DOMAINS = [
    "google.com","google.co.in","facebook.com","microsoft.com",
    "apple.com","amazon.com","paypal.com","twitter.com",
    "instagram.com","linkedin.com","github.com","gitlab.com",
    "netflix.com","spotify.com","adobe.com","salesforce.com",
    "atlassian.com","dropbox.com","slack.com","zoom.us",
    "cloudflare.com","accounts.google.com","login.microsoftonline.com",
    "secure.paypal.com","appleid.apple.com","signin.aws.amazon.com",
]

def entropy(s):
    if not s: return 0.0
    c = collections.Counter(s)
    t = len(s)
    return -sum((v/t)*math.log2(v/t) for v in c.values())

def extract_features(url: str) -> dict:
    feats = {}
    try:
        parsed    = urlparse(url)
        ext       = tldextract.extract(url)
        hostname  = parsed.netloc.lower()
        path      = parsed.path.lower()
        subdomain = ext.subdomain.lower()
        full_url  = url.lower()
        registered = f"{ext.domain}.{ext.suffix}".lower()

        # ── Purane features ────────────────────────────────────
        feats["url_length"]        = len(url)
        feats["num_dots"]          = url.count(".")
        feats["num_hyphens"]       = url.count("-")
        feats["num_digits"]        = sum(c.isdigit() for c in url)
        feats["has_https"]         = int(parsed.scheme == "https")
        feats["hostname_length"]   = len(hostname)
        feats["path_length"]       = len(path)
        feats["subdomain_count"]   = len(subdomain.split(".")) if subdomain else 0
        feats["at_symbol"]         = int("@" in url)
        feats["num_underscore"]    = url.count("_")
        feats["num_percent"]       = url.count("%")
        feats["num_hash"]          = url.count("#")
        feats["contains_login"]    = int("login"   in full_url)
        feats["contains_verify"]   = int("verify"  in full_url)
        feats["contains_secure"]   = int("secure"  in full_url)
        feats["contains_bank"]     = int("bank"    in full_url)
        feats["contains_account"]  = int("account" in full_url)
        feats["contains_update"]   = int("update"  in full_url)
        feats["contains_paypal"]   = int("paypal"  in full_url)
        feats["contains_signin"]   = int("signin"  in full_url)

        # ── Naye features ──────────────────────────────────────
        on_legit_host = any(hostname.endswith(h) for h in LEGIT_HOSTING)
        brand_in_url  = any(b in subdomain or b in path for b in KNOWN_BRANDS)
        feats["brand_on_legit_host"] = int(on_legit_host and brand_in_url)

        feats["has_ip_host"] = int(bool(
            re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname.split(":")[0])
        ))

        feats["path_entropy"] = round(entropy(path), 4)

        suspicious_tlds = {
            "xyz","top","club","online","site","tk","ml",
            "ga","cf","gq","pw","cc","su","buzz","icu"
        }
        feats["suspicious_tld"]    = int(ext.suffix in suspicious_tlds)
        feats["subdomain_depth"]   = subdomain.count(".") + 1 if subdomain else 0
        feats["digit_ratio_host"]  = (
            sum(c.isdigit() for c in hostname) / len(hostname)
            if hostname else 0
        )
        feats["double_slash_path"] = int("//" in path)
        feats["num_special_chars"] = sum(
            url.count(c) for c in ["?","=","&","%","@","!","~"]
        )

        feats["is_trusted_domain"] = int(
            any(hostname.endswith(td) for td in TRUSTED_DOMAINS)
        )

        real_brand_domain = any(
            b in registered for b in [
                "google","facebook","paypal","apple","amazon",
                "microsoft","netflix","instagram","twitter","github"
            ]
        )
        feats["legit_brand_domain"] = int(real_brand_domain)

    except Exception:
        feats = {k: 0 for k in [
            "url_length","num_dots","num_hyphens","num_digits","has_https",
            "hostname_length","path_length","subdomain_count","at_symbol",
            "num_underscore","num_percent","num_hash","contains_login",
            "contains_verify","contains_secure","contains_bank",
            "contains_account","contains_update","contains_paypal",
            "contains_signin","brand_on_legit_host","has_ip_host",
            "path_entropy","suspicious_tld","subdomain_depth",
            "digit_ratio_host","double_slash_path","num_special_chars",
            "is_trusted_domain","legit_brand_domain",
        ]}

    return feats   # ← try/except ke BAHAR


if __name__ == "__main__":
    print(f"Loading: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE).dropna(subset=["url"])
    print(f"  Total rows: {len(df)}")
    print(f"  Extracting features... (5-10 min lagega)")

    records = []
    for i, row in df.iterrows():
        f = extract_features(str(row["url"]))
        if f is None:
            continue
        f["label"] = int(row["label"])
        records.append(f)
        if i % 10000 == 0:
            print(f"  {i}/{len(df)} done...")

    out = pd.DataFrame(records)
    out.to_csv(OUTPUT_FILE, index=False)

    print(f"\n{'='*45}")
    print(f"  SAVED → features_dataset_v2.csv")
    print(f"  Rows     : {out.shape[0]}")
    print(f"  Features : {out.shape[1]-1}")
    print(f"  Label 0  : {(out['label']==0).sum()}")
    print(f"  Label 1  : {(out['label']==1).sum()}")
    print(f"{'='*45}")