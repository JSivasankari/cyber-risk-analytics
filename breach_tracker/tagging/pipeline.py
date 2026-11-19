"""Step 2 runner: load clean CSV -> tag every breach -> save CSV."""
import pandas as pd

from breach_tracker.config import data_path
from .credentials import tag_credential_leak
from .report import print_tag_summary
from .datatype import get_primary_data_type
from .severity import compute_severity_score, tag_severity_label
from .tier import get_risk_tier


def tag_breaches(df: pd.DataFrame) -> pd.DataFrame:
    """Add the 5 NLP-style tag columns to the breach table."""
    classes = df["DataClassesStr"]
    df["SeverityScore"] = classes.apply(compute_severity_score)
    df["SeverityLabel"] = df["SeverityScore"].apply(tag_severity_label)
    df["IsCredentialLeak"] = classes.apply(tag_credential_leak)
    df["PrimaryDataType"] = classes.apply(get_primary_data_type)
    df["RiskTier"] = df.apply(
        lambda r: get_risk_tier(r["SeverityScore"], r.get("PwnMillions", 0)),
        axis=1,
    )
    return df


def main():
    output_path = data_path("breaches_tagged.csv")
    print("[1/3] Loading clean breach data...")
    df = pd.read_csv(data_path("breaches_clean.csv"))
    print(f"      ✓ {len(df)} records loaded")
    print("[2/3] Applying NLP severity tagging...")
    df = tag_breaches(df)
    print_tag_summary(df)
    print(f"[3/3] Saving tagged data → {output_path}")
    df.to_csv(output_path, index=False)
    print("\n✅ Step 2 complete. Next: risk scoring.")
    return df
