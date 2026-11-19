"""Turn industry statistics into the composite risk score."""
import pandas as pd

from .normalize import normalize
from .weights import W_FREQUENCY, W_LAG, W_SCALE, W_SEVERITY


def risk_label(s: float) -> str:
    """Bucket a 0-1 risk score into Critical/High/Medium/Low."""
    return ("Critical" if s > 0.70
            else "High" if s > 0.45
            else "Medium" if s > 0.25
            else "Low")


def add_risk_scores(grp: pd.DataFrame) -> pd.DataFrame:
    """Add RiskScore, RiskScorePct, RiskLabel and CredLeakRate%."""
    sev = normalize(grp["AvgSeverityScore"])
    freq = normalize(grp["BreachCount"])
    scale = normalize(grp["TotalPwnedM"])
    lag = normalize(grp["AvgLagDays"].fillna(0))

    grp["RiskScore"] = (
        W_SEVERITY * sev + W_FREQUENCY * freq
        + W_SCALE * scale + W_LAG * lag
    ).round(4)
    grp["RiskScorePct"] = (grp["RiskScore"] * 100).round(1)
    grp["RiskLabel"] = grp["RiskScore"].apply(risk_label)
    grp["CredLeakRate%"] = (
        grp["CredentialLeaks"] / grp["BreachCount"] * 100
    ).round(1)
    return grp
