import requests
import pandas as pd
import json
import time
import os

HIBP_BASE = "https://haveibeenpwned.com/api/v3"
HEADERS   = {
    "User-Agent": "BreachTracker-Portfolio-Project/1.0",
    "hibp-api-key": ""          
}
DATA_DIR  = "data"

DOMAIN_INDUSTRY = {

    "linkedin": "Social Media", "facebook": "Social Media",
    "twitter": "Social Media",  "instagram": "Social Media",
    "myspace": "Social Media",  "tumblr": "Social Media",
    "snapchat": "Social Media", "reddit": "Social Media",
  
    "adobe": "Software/Tech",   "microsoft": "Software/Tech",
    "canva": "Software/Tech",   "dropbox": "Cloud Storage",
    "lastpass": "Cloud Storage","slack": "Software/Tech",
  
    "ebay": "E-Commerce",       "amazon": "E-Commerce",
    "shopify": "E-Commerce",    "etsy": "E-Commerce",
    
    "yahoo": "Email/Telecom",   "hotmail": "Email/Telecom",
    "aol": "Email/Telecom",     "att": "Email/Telecom",
  
    "zynga": "Gaming",          "steam": "Gaming",
    "sony": "Gaming",           "minecraft": "Gaming",
    "epicgames": "Gaming",
   
    "paypal": "Finance",        "capitalone": "Finance",
    "equifax": "Finance",       "experian": "Finance",
  
    "optum": "Healthcare",      "anthem": "Healthcare",
    "labcorp": "Healthcare",
   
    "chegg": "Education",       "coursera": "Education",
}

def fetch_all_breaches() -> list:
    
    url = f"{HIBP_BASE}/breaches"
    print(f"  → GET {url}")
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()

def map_industry(domain: str) -> str:
    
    d = str(domain).lower()
    for key, industry in DOMAIN_INDUSTRY.items():
        if key in d:
            return industry
    return "Other"

def clean_breaches(raw: list) -> pd.DataFrame:
    """
    Parse raw HIBP JSON list into a tidy DataFrame.
    Engineered columns:
      - Year, Month             ← from BreachDate
      - DisclosureLagDays       ← AddedDate - BreachDate
      - PwnMillions             ← PwnCount / 1_000_000
      - DataClassesStr          ← list → comma string
      - Industry                ← domain → sector mapping
    """
    df = pd.DataFrame(raw)

    keep = [
        "Name", "Title", "Domain", "BreachDate", "AddedDate",
        "PwnCount", "DataClasses", "IsVerified", "IsSensitive",
        "IsRetired", "IsSpamList", "IsFabricated", "Description"
    ]
    df = df[[c for c in keep if c in df.columns]].copy()

    df["BreachDate"] = pd.to_datetime(df["BreachDate"], errors="coerce")
    df["AddedDate"]  = pd.to_datetime(df["AddedDate"],  errors="coerce")
    df["Year"]       = df["BreachDate"].dt.year.astype("Int64")
    df["Month"]      = df["BreachDate"].dt.month.astype("Int64")
    df["Quarter"]    = df["BreachDate"].dt.quarter.astype("Int64")
    df["DisclosureLagDays"] = (df["AddedDate"].dt.tz_localize(None) - df["BreachDate"].dt.tz_localize(None)).dt.days

    df["PwnMillions"] = (df["PwnCount"] / 1_000_000).round(3)

    df["DataClassesStr"] = df["DataClasses"].apply(
        lambda x: ", ".join(x) if isinstance(x, list) else ""
    )
    df["DataClassCount"] = df["DataClasses"].apply(
        lambda x: len(x) if isinstance(x, list) else 0
    )

    df["Industry"] = df["Domain"].apply(map_industry)

    for col in ["IsVerified", "IsSensitive", "IsRetired", "IsSpamList", "IsFabricated"]:
        if col in df.columns:
            df[col] = df[col].astype(int)

    return df.reset_index(drop=True)
def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("[1/3] Fetching breaches from HIBP API...")
    raw = fetch_all_breaches()
    print(f"      ✓ {len(raw)} breaches fetched")
    raw_path = os.path.join(DATA_DIR, "breaches_raw.json")
    with open(raw_path, "w") as f:
        json.dump(raw, f, indent=2)
    print(f"      ✓ Raw saved → {raw_path}")
    print("[2/3] Cleaning and enriching data...")
    df = clean_breaches(raw)
    print(f"      ✓ Shape: {df.shape}")
    print(f"      ✓ Years: {df['Year'].min()} – {df['Year'].max()}")
    print(f"      ✓ Total people affected: {df['PwnMillions'].sum():.1f}M")
    clean_path = os.path.join(DATA_DIR, "breaches_clean.csv")
    df.to_csv(clean_path, index=False)
    print(f"[3/3] Saved → {clean_path}")
    print("\n✅ breach_pipeline.py complete. Run nlp_tagger.py next.")
    return df
if __name__ == "__main__":
    main()
