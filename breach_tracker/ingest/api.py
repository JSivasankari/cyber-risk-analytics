"""Step 1a: download every known breach from the HIBP API."""
import requests

from breach_tracker.config import HEADERS, HIBP_BASE


def fetch_all_breaches() -> list:
    """GET /breaches and return the raw JSON list."""
    url = f"{HIBP_BASE}/breaches"
    print(f"  → GET {url}")
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()
