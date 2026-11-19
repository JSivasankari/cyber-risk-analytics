"""Year-level aggregations for timeline visuals."""
import pandas as pd


def compute_yearly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Breaches, people affected and severity per year."""
    trend = df.groupby("Year").agg(
        BreachCount=("Name", "count"),
        TotalPwnedM=("PwnMillions", "sum"),
        AvgSeverityScore=("SeverityScore", "mean"),
        CredLeaks=("IsCredentialLeak", "sum"),
        UniqueIndustries=("Industry", "nunique"),
    ).reset_index()

    trend["CumulativePwnedM"] = trend["TotalPwnedM"].cumsum().round(2)
    trend["TotalPwnedM"] = trend["TotalPwnedM"].round(2)
    trend["AvgSeverityScore"] = trend["AvgSeverityScore"].round(2)

    return trend.dropna(subset=["Year"]).sort_values("Year")
