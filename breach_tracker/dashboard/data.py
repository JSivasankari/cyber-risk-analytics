"""Load the tagged breach data and the industry risk table."""
import os

import pandas as pd
import streamlit as st

from breach_tracker.config import data_path
from breach_tracker.risk.industry import compute_industry_risk


def ensure_industry_risk():
    """Build data/industry_risk.csv once if it does not exist yet."""
    if not os.path.exists(data_path("industry_risk.csv")):
        tagged = pd.read_csv(data_path("breaches_tagged.csv"))
        risk = compute_industry_risk(tagged)
        risk.to_csv(data_path("industry_risk.csv"), index=False)


@st.cache_data
def load_data():
    """Return (breaches DataFrame, industry risk DataFrame or None)."""
    breaches = pd.read_csv(data_path("breaches_tagged.csv"),
                           parse_dates=["BreachDate", "AddedDate"])
    industry_file = data_path("industry_risk.csv")
    industry = (pd.read_csv(industry_file)
                if os.path.exists(industry_file) else None)
    return breaches, industry
