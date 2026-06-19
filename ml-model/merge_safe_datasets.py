import pandas as pd

DATASET_DIR = "../dataset"

print("Loading datasets...")

old_safe  = pd.read_csv(f"{DATASET_DIR}/safe_urls_final.csv")
old_phish = pd.read_csv(f"{DATASET_DIR}/phishing_urls_merged.csv")

print(f"  Old safe      : {len(old_safe)}")
print(f"  Old phishing  : {len(old_phish)}")

# ── Modern safe URLs (inline — no extra file needed) ──────────
modern_safe_urls = [
    "https://github.com","https://gist.github.com","https://api.github.com",
    "https://torvalds.github.io","https://microsoft.github.io/vscode-docs",
    "https://google.github.io/material-design-icons","https://vuejs.github.io",
    "https://angular.github.io","https://bootstrap.github.io",
    "https://freecodecamp.github.io","https://hackclub.github.io",
    "https://vercel.com","https://app.vercel.com","https://nextjs.vercel.app",
    "https://vercel-commerce.vercel.app","https://portfolio-template.vercel.app",
    "https://todo-app-demo.vercel.app","https://sveltekit-demo.vercel.app",
    "https://dashboard-ui.vercel.app","https://react-starter.vercel.app",
    "https://netlify.com","https://app.netlify.com","https://docs.netlify.com",
    "https://gatsby-starter-blog.netlify.app","https://react-boilerplate.netlify.app",
    "https://vue-portfolio.netlify.app","https://svelte-kit-demo.netlify.app",
    "https://hugo-portfolio.netlify.app","https://nuxt-demo.netlify.app",
    "https://blogger.com","https://myblog.blogspot.com",
    "https://techblog2024.blogspot.com","https://learningpython.blogspot.com",
    "https://codingjourney.blogspot.com","https://devnotes.blogspot.com",
    "https://healthtips2024.blogspot.com","https://recipes101.blogspot.com",
    "https://pages.cloudflare.com","https://workers.cloudflare.com",
    "https://student-project.pages.dev","https://docs-site.pages.dev",
    "https://company-landing.pages.dev","https://portfolio-site.pages.dev",
    "https://console.firebase.google.com","https://chat-app-demo.web.app",
    "https://react-firebase.web.app","https://auth-demo.firebaseapp.com",
    "https://todo-firebase.firebaseapp.com","https://firestore-demo.firebaseapp.com",
    "https://login.github.com","https://login.microsoftonline.com",
    "https://accounts.google.com/signin","https://secure.paypal.com/signin",
    "https://auth.atlassian.com","https://signin.aws.amazon.com",
    "https://login.live.com","https://appleid.apple.com",
    "https://app.netlify.com/login","https://vercel.com/login",
    "https://npmjs.com","https://pypi.org","https://replit.com",
    "https://codesandbox.io","https://codepen.io","https://stackblitz.com",
    "https://kaggle.com","https://huggingface.co","https://streamlit.app",
    "https://gradio.app","https://readthedocs.io","https://render.com",
    "https://railway.app","https://heroku.com","https://fly.dev",
    "https://wordpress.com","https://medium.com","https://dev.to",
    "https://substack.com","https://notion.so","https://carrd.co",
    "https://webflow.com","https://ghost.io","https://hashnode.dev",
    "https://gitlab.com","https://bitbucket.org","https://glitch.me",
    "https://johnsmith.github.io","https://portfolio.vercel.app",
    "https://myblog.netlify.app","https://myproject.netlify.app",
    "https://abc.pages.dev","https://myapp.pythonanywhere.com",
    # ── Trusted domain subpages (critical edge cases) ──────────
    "https://accounts.google.com/signin",
    "https://accounts.google.com/login",
    "https://myaccount.google.com",
    "https://myaccount.google.com/security",
    "https://mail.google.com/mail",
    "https://drive.google.com/drive",
    "https://secure.paypal.com/myaccount",
    "https://secure.paypal.com/signin",
    "https://secure.paypal.com/home",
    "https://www.paypal.com/signin",
    "https://login.microsoftonline.com/common",
    "https://login.live.com/login.srf",
    "https://account.microsoft.com",
    "https://appleid.apple.com/sign-in",
    "https://appleid.apple.com/account",
    "https://signin.aws.amazon.com/signin",
    "https://console.aws.amazon.com",
    "https://www.amazon.com/ap/signin",
    "https://auth.atlassian.com/login",
    "https://id.atlassian.com/login",
    "https://github.com/login",
    "https://github.com/session",
    "https://gitlab.com/users/sign_in",
    "https://account.live.com/password/reset",
    "https://login.yahoo.com/account/login",
    "https://id.adobe.com/s/login",
    "https://login.salesforce.com",
    "https://app.hubspot.com/login",
    "https://dashboard.stripe.com/login",
    "https://app.slack.com/signin",
    "https://zoom.us/signin",
    "https://www.netflix.com/login",
    "https://www.instagram.com/accounts/login",
    "https://www.facebook.com/login",
    "https://twitter.com/i/flow/login",
    "https://www.linkedin.com/login",
]

# ── Hard negative phishing (brand spoof on legit hosting) ─────
hard_phish_urls = [
    "https://paypal-secure-login.vercel.app",
    "https://netflix-account-verify.vercel.app",
    "https://amazon-order-confirm.vercel.app",
    "https://facebook-login-2024.vercel.app",
    "https://apple-id-locked.vercel.app",
    "https://instagram-verify-account.vercel.app",
    "https://microsoft-support.vercel.app",
    "https://google-security-alert.vercel.app",
    "https://bank-login-secure.vercel.app",
    "https://discord-nitro-free.vercel.app",
    "https://paypal-verify-2024.netlify.app",
    "https://netflix-billing-update.netlify.app",
    "https://amazon-security-alert.netlify.app",
    "https://apple-icloud-login.netlify.app",
    "https://microsoft-account-verify.netlify.app",
    "https://instagram-login-confirm.netlify.app",
    "https://facebook-account-recovery.netlify.app",
    "https://google-account-suspended.netlify.app",
    "https://chase-bank-online.netlify.app",
    "https://steam-account-verify.netlify.app",
    "https://paypal-phish.github.io/login",
    "https://netflix-support.github.io/verify",
    "https://amazon-secure.github.io/signin",
    "https://apple-id-verify.github.io",
    "https://google-security.github.io/alert",
    "https://facebook-phishing.github.io/recover",
    "https://bankofamerica-secure.github.io/login",
    "https://paypal-login-secure.pages.dev",
    "https://netflix-account.pages.dev/verify",
    "https://apple-support-login.pages.dev",
    "https://instagram-2fa-verify.pages.dev",
    "https://paypal-alert2024.blogspot.com/login",
    "https://netflix-phish.blogspot.com/verify",
    "https://banklogin-secure.blogspot.com",
    "https://paypal-secure.web.app",
    "https://google-account-locked.web.app",
    "https://facebook-login.web.app",
    "https://netflix-verify.web.app",
]

modern_df = pd.DataFrame({"url": modern_safe_urls,  "label": 0})
hard_df   = pd.DataFrame({"url": hard_phish_urls,   "label": 1})

print(f"  Modern safe   : {len(modern_df)}")
print(f"  Hard phishing : {len(hard_df)}")

# ── Combine safe ──────────────────────────────────────────────
combined_safe = pd.concat([
    old_safe[["url","label"]],
    modern_df,
], ignore_index=True).drop_duplicates(subset="url")

# ── Combine phishing ──────────────────────────────────────────
combined_phish = pd.concat([
    old_phish[["url","label"]],
    hard_df,
], ignore_index=True).drop_duplicates(subset="url")

print(f"\nAfter merge:")
print(f"  Total safe     : {len(combined_safe)}")
print(f"  Total phishing : {len(combined_phish)}")

# ── Balance ───────────────────────────────────────────────────
n = min(len(combined_safe), len(combined_phish))
final = pd.concat([
    combined_safe.sample(n=n, random_state=42),
    combined_phish.sample(n=n, random_state=42),
]).sample(frac=1, random_state=42).reset_index(drop=True)

# ── Save ──────────────────────────────────────────────────────
out = f"{DATASET_DIR}/final_dataset_v2.csv"
final.to_csv(out, index=False)

print(f"\n{'='*45}")
print(f"  SAVED → final_dataset_v2.csv")
print(f"  Total : {len(final)}")
print(f"  Safe  : {(final['label']==0).sum()}")
print(f"  Phish : {(final['label']==1).sum()}")
print(f"{'='*45}")