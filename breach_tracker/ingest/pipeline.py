"""Step 1 runner: fetch -> save raw JSON -> clean -> save CSV."""
import json
import os

from breach_tracker.config import DATA_DIR, data_path
from .api import fetch_all_breaches
from .cleaner import clean_breaches


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("[1/3] Fetching breaches from HIBP API...")
    raw = fetch_all_breaches()
    print(f"      ✓ {len(raw)} breaches fetched")
    raw_path = data_path("breaches_raw.json")
    with open(raw_path, "w") as f:
        json.dump(raw, f, indent=2)
    print(f"      ✓ Raw saved → {raw_path}")
    print("[2/3] Cleaning and enriching data...")
    df = clean_breaches(raw)
    print(f"      ✓ Shape: {df.shape}")
    print(f"      ✓ Years: {df['Year'].min()} – {df['Year'].max()}")
    print(f"      ✓ Total people affected: {df['PwnMillions'].sum():.1f}M")
    clean_path = data_path("breaches_clean.csv")
    df.to_csv(clean_path, index=False)
    print(f"[3/3] Saved → {clean_path}")
    print("\n✅ Step 1 complete. Next: tagging.")
    return df
