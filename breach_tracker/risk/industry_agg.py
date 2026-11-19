"""Group breaches by industry and compute raw statistics."""
import pandas as pd


def aggregate_by_industry(df: pd.DataFrame) -> pd.DataFrame:
    """One row per industry with counts, sums, means and maxes."""
    return df.groupby("Industry").agg(
        BreachCount=("Name", "count"),
        TotalPwnedM=("PwnMillions", "sum"),
        AvgPwnedM=("PwnMillions", "mean"),
        MaxPwnedM=("PwnMillions", "max"),
        AvgSeverityScore=("SeverityScore", "mean"),
        MaxSeverityScore=("SeverityScore", "max"),
        CredentialLeaks=("IsCredentialLeak", "sum"),
        AvgLagDays=("DisclosureLagDays", "mean"),
        MaxLagDays=("DisclosureLagDays", "max"),
        CriticalBreaches=("SeverityLabel",
                          lambda x: (x == "Critical").sum()),
        HighBreaches=("SeverityLabel", lambda x: (x == "High").sum()),
        YearFirstSeen=("Year", "min"),
        YearLastSeen=("Year", "max"),
    ).reset_index()
