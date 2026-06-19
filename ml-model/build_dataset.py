""""
Phishing Detection Dataset Builder
Sources:
  Phishing  → PhishTank (verified) + OpenPhish (community) + URLhaus
  Safe      → Tranco Top-1M + manual modern-hosting list
"""

import requests, pandas as pd, time, re, os
from urllib.parse import urlparse
import tldextract

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
OUTPUT_DIR        = "dataset"
PHISHING_TARGET   = 5000   # kitne phishing chahiye
SAFE_TARGET       = 5000   # kitne safe chahiye (balanced)
TRANCO_TOP_N      = 20000  # top-N Tranco domains consider karo

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────
# PART 1: PHISHING URLs
# ─────────────────────────────────────────

def fetch_phishtank():
    """PhishTank — verified phishing URLs (no API key needed for basic CSV)"""
    print("[PhishTank] Downloading...")
    try:
        # Public CSV (no login needed, rate limited)
        url = "http://data.phishtank.com/data/online-valid.csv"
        df  = pd.read_csv(url, usecols=["url", "verified", "online"])
        df  = df[(df["verified"] == "yes") & (df["online"] == "yes")]
        df  = df[["url"]].rename(columns={"url": "url"})
        df["label"]  = 1
        df["source"] = "phishtank"
        print(f"  → {len(df)} verified phishing URLs")
        return df
    except Exception as e:
        print(f"  [WARN] PhishTank failed: {e}")
        return pd.DataFrame(columns=["url", "label", "source"])


def fetch_openphish():
    """OpenPhish Community Feed — free, no key needed, ~300 URLs updated every 12h"""
    print("[OpenPhish] Downloading...")
    try:
        r    = requests.get("https://openphish.com/feed.txt", timeout=15)
        urls = [u.strip() for u in r.text.splitlines() if u.strip().startswith("http")]
        df   = pd.DataFrame({"url": urls, "label": 1, "source": "openphish"})
        print(f"  → {len(df)} phishing URLs")
        return df
    except Exception as e:
        print(f"  [WARN] OpenPhish failed: {e}")
        return pd.DataFrame(columns=["url", "label", "source"])


def fetch_urlhaus():
    """URLhaus (abuse.ch) — malicious URLs including phishing. Free CSV."""
    print("[URLhaus] Downloading...")
    try:
        r    = requests.get("https://urlhaus.abuse.ch/downloads/csv_online/", timeout=30)
        from io import StringIO
        # Skip comment lines
        lines  = [l for l in r.text.splitlines() if not l.startswith("#")]
        df     = pd.read_csv(StringIO("\n".join(lines)),
                             names=["id","dateadded","url","url_status",
                                    "last_online","threat","tags","urlhaus_link","reporter"])
        # Keep only phishing-tagged entries
        df = df[df["tags"].str.contains("phishing|credential", na=False, case=False)]
        df = df[df["url_status"] == "online"][["url"]]
        df["label"]  = 1
        df["source"] = "urlhaus"
        print(f"  → {len(df)} phishing URLs")
        return df
    except Exception as e:
        print(f"  [WARN] URLhaus failed: {e}")
        return pd.DataFrame(columns=["url", "label", "source"])


# ─────────────────────────────────────────
# PART 2: SAFE URLs
# ─────────────────────────────────────────

def fetch_tranco_safe(top_n=20000):
    """Tranco Top-1M → most popular = almost certainly safe"""
    print(f"[Tranco] Downloading top {top_n} domains...")
    try:
        # Latest Tranco list (permanent URL, updates daily)
        r       = requests.get("https://tranco-list.eu/top-1m.csv.zip", timeout=60)
        import zipfile, io
        zf      = zipfile.ZipFile(io.BytesIO(r.content))
        csvfile = zf.namelist()[0]
        df      = pd.read_csv(zf.open(csvfile), header=None,
                              names=["rank","domain"]).head(top_n)
        # Convert domain → HTTPS URL
        df["url"]    = "https://" + df["domain"]
        df["label"]  = 0
        df["source"] = "tranco"
        print(f"  → {len(df)} safe domains from Tranco")
        return df[["url", "label", "source"]]
    except Exception as e:
        print(f"  [WARN] Tranco failed: {e}")
        return pd.DataFrame(columns=["url", "label", "source"])


# Modern hosting platforms — tumhari exact problem ka solution
MODERN_SAFE_URLS = {
    # ── GitHub Pages (legit projects) ──────────────────────────────
    "github_pages": [
        "https://torvalds.github.io",
        "https://microsoft.github.io/vscode-docs",
        "https://google.github.io/material-design-icons",
        "https://facebook.github.io/react",
        "https://vuejs.github.io",
        "https://angular.github.io",
        "https://bootstrap.github.io",
        "https://tailwindcss.github.io",
        "https://reactjs.github.io",
        "https://twbs.github.io/bootstrap",
        "https://freecodecamp.github.io",
        "https://hackclub.github.io",
        "https://odin-project.github.io",
        "https://cs50.github.io",
        "https://portfolio-template.github.io",
        "https://resume-template.github.io",
        "https://johnpapa.github.io",
        "https://sindresorhus.github.io",
        "https://github.com",
        "https://gist.github.com",
        "https://raw.githubusercontent.com",
        "https://api.github.com",
        "https://education.github.com",
        "https://skills.github.com",
    ],
    # ── Vercel (legit deployments) ─────────────────────────────────
    "vercel": [
        "https://nextjs.vercel.app",
        "https://vercel-commerce.vercel.app",
        "https://portfolio-template.vercel.app",
        "https://todo-app-demo.vercel.app",
        "https://sveltekit-demo.vercel.app",
        "https://dashboard-ui.vercel.app",
        "https://ai-chatbot.vercel.app",
        "https://react-starter.vercel.app",
        "https://blog-template.vercel.app",
        "https://docs-template.vercel.app",
        "https://v0-demo.vercel.app",
        "https://commerce.vercel.app",
        "https://app.vercel.com",
        "https://vercel.com",
        "https://vercel.com/docs",
    ],
    # ── Netlify (legit deployments) ────────────────────────────────
    "netlify": [
        "https://gatsby-starter-blog.netlify.app",
        "https://react-boilerplate.netlify.app",
        "https://vue-portfolio.netlify.app",
        "https://angular-demo.netlify.app",
        "https://svelte-kit-demo.netlify.app",
        "https://hugo-portfolio.netlify.app",
        "https://eleventy-blog.netlify.app",
        "https://nuxt-demo.netlify.app",
        "https://astro-blog.netlify.app",
        "https://remix-demo.netlify.app",
        "https://app.netlify.com",
        "https://netlify.com",
        "https://docs.netlify.com",
    ],
    # ── Blogspot (legit blogs) ─────────────────────────────────────
    "blogspot": [
        "https://techcrunch.blogspot.com",
        "https://devnotes2024.blogspot.com",
        "https://learningpython.blogspot.com",
        "https://codingjourney.blogspot.com",
        "https://studymaterial.blogspot.com",
        "https://photographylife.blogspot.com",
        "https://traveldiary.blogspot.com",
        "https://healthtips2024.blogspot.com",
        "https://recipes101.blogspot.com",
        "https://myblog.blogspot.com",
        "https://blogger.com",
    ],
    # ── Cloudflare Pages ──────────────────────────────────────────
    "pages_dev": [
        "https://workers.cloudflare.com",
        "https://pages.cloudflare.com",
        "https://dash.cloudflare.com",
        "https://student-project.pages.dev",
        "https://docs-site.pages.dev",
        "https://company-landing.pages.dev",
        "https://portfolio-site.pages.dev",
        "https://api-demo.pages.dev",
    ],
    # ── Firebase / Google ──────────────────────────────────────────
    "firebase": [
        "https://console.firebase.google.com",
        "https://chat-app-demo.web.app",
        "https://react-firebase.web.app",
        "https://auth-demo.firebaseapp.com",
        "https://todo-firebase.firebaseapp.com",
        "https://accounts.google.com",
        "https://mail.google.com",
        "https://drive.google.com",
        "https://docs.google.com",
        "https://sites.google.com",
    ],
    # ── Login/Auth pages (legit — critical edge case) ─────────────
    "login_pages": [
        "https://login.github.com",
        "https://login.microsoftonline.com",
        "https://accounts.google.com/signin",
        "https://secure.paypal.com/signin",
        "https://auth.atlassian.com",
        "https://signin.aws.amazon.com",
        "https://login.live.com",
        "https://appleid.apple.com",
        "https://id.adobe.com",
        "https://login.salesforce.com",
        "https://app.netlify.com/login",
        "https://vercel.com/login",
        "https://dashboard.render.com/login",
        "https://console.cloud.google.com",
        "https://portal.azure.com",
    ],
    # ── Developer / CDN / API domains ─────────────────────────────
    "dev_platforms": [
        "https://api.github.com",
        "https://cdn.jsdelivr.net",
        "https://cdnjs.cloudflare.com",
        "https://unpkg.com",
        "https://npmjs.com",
        "https://pypi.org",
        "https://registry.npmjs.org",
        "https://replit.com",
        "https://glitch.me",
        "https://codesandbox.io",
        "https://codepen.io",
        "https://stackblitz.com",
        "https://jsfiddle.net",
        "https://kaggle.com",
        "https://huggingface.co",
        "https://streamlit.app",
        "https://gradio.app",
        "https://readthedocs.io",
        "https://gitbook.io",
        "https://deepnote.com",
        "https://mybinder.org",
        "https://pythonanywhere.com",
        "https://render.com",
        "https://railway.app",
        "https://fly.dev",
        "https://heroku.com",
    ],
    # ── E-commerce / SaaS platforms ───────────────────────────────
    "ecommerce": [
        "https://myshopify.com",
        "https://admin.shopify.com",
        "https://checkout.stripe.com",
        "https://gumroad.com",
        "https://lemonsqueezy.com",
        "https://payhip.com",
        "https://ko-fi.com",
        "https://buymeacoffee.com",
    ],
    # ── Personal/Portfolio (common patterns) ──────────────────────
    "portfolio": [
        "https://about.me",
        "https://notion.site",
        "https://notion.so",
        "https://carrd.co",
        "https://webflow.io",
        "https://framer.site",
        "https://substack.com",
        "https://medium.com",
        "https://dev.to",
        "https://hashnode.dev",
        "https://ghost.io",
        "https://wordpress.com",
        "https://wixsite.com",
        "https://tumblr.com",
    ],
}


def build_modern_safe():
    """Flatten the modern safe URL dict into a dataframe"""
    rows = []
    for category, urls in MODERN_SAFE_URLS.items():
        for url in urls:
            rows.append({"url": url, "label": 0, "source": f"manual_{category}"})
    df = pd.DataFrame(rows)
    print(f"[Manual] {len(df)} modern-hosting safe URLs across {len(MODERN_SAFE_URLS)} categories")
    return df


# ─────────────────────────────────────────
# PART 3: HARD NEGATIVE EXAMPLES
# These are the most important rows in your dataset
# Platform + brand keyword in path → PHISHING (label=1)
# ─────────────────────────────────────────

HARD_NEGATIVES_PHISHING = [
    # vercel phishing
    "https://paypal-secure-login.vercel.app",
    "https://netflix-account-verify.vercel.app",
    "https://amazon-order-confirm.vercel.app",
    "https://facebook-login-2024.vercel.app",
    "https://apple-id-locked.vercel.app",
    "https://instagram-verify-account.vercel.app",
    "https://microsoft-support.vercel.app",
    "https://google-security-alert.vercel.app",
    "https://bank-login-secure.vercel.app",
    "https://steam-trade-verify.vercel.app",
    "https://discord-nitro-free.vercel.app",
    "https://binance-wallet-verify.vercel.app",
    "https://coinbase-secure-login.vercel.app",
    "https://whatsapp-update-verify.vercel.app",
    "https://ebay-account-suspended.vercel.app",
    # netlify phishing
    "https://paypal-verify-2024.netlify.app",
    "https://netflix-billing-update.netlify.app",
    "https://amazon-security-alert.netlify.app",
    "https://apple-icloud-login.netlify.app",
    "https://microsoft-account-verify.netlify.app",
    "https://instagram-login-confirm.netlify.app",
    "https://facebook-account-recovery.netlify.app",
    "https://google-account-suspended.netlify.app",
    "https://chase-bank-online.netlify.app",
    "https://wellsfargo-secure.netlify.app",
    "https://steam-account-verify.netlify.app",
    "https://crypto-wallet-login.netlify.app",
    "https://tiktok-verify-account.netlify.app",
    "https://twitter-verify-identity.netlify.app",
    "https://linkedin-account-verify.netlify.app",
    # github.io phishing
    "https://paypal-phish.github.io/login",
    "https://netflix-support.github.io/verify",
    "https://amazon-secure.github.io/signin",
    "https://apple-id-verify.github.io",
    "https://google-security.github.io/alert",
    "https://facebook-phishing.github.io/recover",
    "https://instagram-supp.github.io/verify",
    "https://bankofamerica-secure.github.io/login",
    "https://coinbase-phish.github.io/wallet",
    "https://discord-phish.github.io/verify",
    # pages.dev phishing
    "https://paypal-login-secure.pages.dev",
    "https://netflix-account.pages.dev/verify",
    "https://amazon-prime-offer.pages.dev",
    "https://apple-support-login.pages.dev",
    "https://instagram-2fa-verify.pages.dev",
    # blogspot phishing
    "https://paypal-alert2024.blogspot.com/login",
    "https://netflix-phish.blogspot.com/verify",
    "https://amazon-deals-fake.blogspot.com",
    "https://banklogin-secure.blogspot.com",
    "https://crypto-wallet-phish.blogspot.com",
    # web.app / firebase phishing
    "https://paypal-secure.web.app",
    "https://google-account-locked.web.app",
    "https://facebook-login.web.app",
    "https://instagram-clone-phish.web.app",
    "https://netflix-verify.web.app",
]

HARD_NEGATIVES_SAFE = [
    # These LOOK like phishing but are safe — model must learn this
    "https://login.github.com/session",
    "https://accounts.google.com/o/oauth2/auth",
    "https://signin.aws.amazon.com/console",
    "https://secure.paypal.com/myaccount/summary",
    "https://auth.atlassian.com/login",
    "https://login.microsoftonline.com/common",
    "https://appleid.apple.com/auth/authorize",
    "https://id.adobe.com/s/login",
    "https://login.salesforce.com",
    "https://app.netlify.com/signup",
    "https://vercel.com/login",
    "https://dashboard.render.com/login",
    "https://console.firebase.google.com/u/0/",
    "https://studio.firebase.google.com",
    "https://myaccount.google.com/security",
    "https://business.facebook.com/overview",
    "https://developer.twitter.com/en/portal/dashboard",
    "https://netlify.app/login",
    "https://support.apple.com/account",
    "https://amazon.com/gp/sign-in",
]


def build_hard_negatives():
    phish_df = pd.DataFrame({
        "url":    HARD_NEGATIVES_PHISHING,
        "label":  1,
        "source": "hard_negative_phishing"
    })
    safe_df = pd.DataFrame({
        "url":    HARD_NEGATIVES_SAFE,
        "label":  0,
        "source": "hard_negative_safe"
    })
    df = pd.concat([phish_df, safe_df])
    print(f"[Hard negatives] {len(phish_df)} phishing + {len(safe_df)} safe edge cases")
    return df


# ─────────────────────────────────────────
# PART 4: BUILD + CLEAN + BALANCE
# ─────────────────────────────────────────

def clean_url(url: str) -> str:
    """Basic URL normalisation"""
    url = url.strip()
    if not url.startswith("http"):
        url = "https://" + url
    return url


def is_valid_url(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except:
        return False


def build_full_dataset():
    print("=" * 55)
    print("  Phishing Detection Dataset Builder")
    print("=" * 55)

    # --- Fetch all sources ---
    phish_frames = [fetch_phishtank(), fetch_openphish(), fetch_urlhaus()]
    safe_frames  = [fetch_tranco_safe(TRANCO_TOP_N), build_modern_safe()]
    hard         = build_hard_negatives()

    phish_df = pd.concat(phish_frames, ignore_index=True)
    safe_df  = pd.concat(safe_frames,  ignore_index=True)

    # --- Combine everything ---
    all_df = pd.concat([phish_df, safe_df, hard], ignore_index=True)

    # --- Clean ---
    all_df["url"] = all_df["url"].apply(clean_url)
    all_df = all_df[all_df["url"].apply(is_valid_url)]
    all_df = all_df.drop_duplicates(subset="url")

    # --- Balance: equal phishing and safe ---
    phishing_final = all_df[all_df["label"] == 1].sample(
        min(PHISHING_TARGET, (all_df["label"]==1).sum()), random_state=42
    )
    safe_final = all_df[all_df["label"] == 0].sample(
        min(SAFE_TARGET, (all_df["label"]==0).sum()), random_state=42
    )

    final = pd.concat([phishing_final, safe_final]).sample(
        frac=1, random_state=42
    ).reset_index(drop=True)

    # --- Save ---
    final.to_csv(f"{OUTPUT_DIR}/dataset_full.csv", index=False)

    # Save hard negatives separately for targeted eval
    hard.to_csv(f"{OUTPUT_DIR}/hard_negatives.csv", index=False)

    # Save modern safe separately (tumhara original fix)
    build_modern_safe().to_csv(f"{OUTPUT_DIR}/safe_modern_sites.csv", index=False)

    # --- Report ---
    print("\n" + "=" * 55)
    print("  DATASET SUMMARY")
    print("=" * 55)
    print(f"  Total URLs        : {len(final)}")
    print(f"  Phishing (label=1): {(final['label']==1).sum()}")
    print(f"  Safe     (label=0): {(final['label']==0).sum()}")
    print(f"\n  Source breakdown:")
    print(final["source"].value_counts().to_string())
    print(f"\n  Saved to: {OUTPUT_DIR}/dataset_full.csv")
    return final


if __name__ == "__main__":
    df = build_full_dataset()