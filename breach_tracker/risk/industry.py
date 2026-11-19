"""Industry risk table = aggregate + score + tidy rounding."""
import pandas as pd

from .industry_agg import aggregate_by_industry
from .industry_score import add_risk_scores

ROUND_COLS = ["TotalPwnedM", "AvgPwnedM", "MaxPwnedM",
              "AvgSeverityScore", "MaxSeverityScore",
              "AvgLagDays", "MaxLagDays"]


def compute_industry_risk(df: pd.DataFrame) -> pd.DataFrame:
    """Composite risk score per industry (higher lag = higher risk).

    R = 0.35*norm(avg_severity) + 0.25*norm(breach_count)
      + 0.25*norm(total_pwned_millions) + 0.15*norm(avg_lag)
    """
    grp = add_risk_scores(aggregate_by_industry(df))

    for col in ROUND_COLS:
        grp[col] = grp[col].round(2)

    return grp.sort_values("RiskScore", ascending=False).reset_index(drop=True)
