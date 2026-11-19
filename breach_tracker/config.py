"""Central settings: file paths, API endpoint and request headers."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")

HIBP_BASE = "https://haveibeenpwned.com/api/v3"
HEADERS = {
    "User-Agent": "BreachTracker-Portfolio-Project/1.0",
    "hibp-api-key": "",
}


def data_path(filename: str) -> str:
    """Return the full path of a file inside the data/ folder."""
    return os.path.join(DATA_DIR, filename)
