"""Shared EDA setup: plot theme and data loading."""
import os
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from breach_tracker.config import data_path

warnings.filterwarnings("ignore")
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams.update({"figure.dpi": 130, "figure.figsize": (12, 5)})


def load():
    """Return (breaches, industry risk or None)."""
    df = pd.read_csv(data_path("breaches_tagged.csv"),
                     parse_dates=["BreachDate", "AddedDate"])
    risk_file = data_path("industry_risk.csv")
    risk_df = pd.read_csv(risk_file) if os.path.exists(risk_file) else None
    return df, risk_df
