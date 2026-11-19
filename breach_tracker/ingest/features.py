"""Feature engineering: turn raw breach columns into analysis columns."""
import pandas as pd

from .industry_map import map_industry


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """Year / Month / Quarter and DisclosureLagDays (Added - Breach)."""
    df["BreachDate"] = pd.to_datetime(df["BreachDate"], errors="coerce")
    df["AddedDate"] = pd.to_datetime(df["AddedDate"], errors="coerce")
    df["Year"] = df["BreachDate"].dt.year.astype("Int64")
    df["Month"] = df["BreachDate"].dt.month.astype("Int64")
    df["Quarter"] = df["BreachDate"].dt.quarter.astype("Int64")
    added = df["AddedDate"].dt.tz_localize(None)
    breached = df["BreachDate"].dt.tz_localize(None)
    df["DisclosureLagDays"] = (added - breached).dt.days
    return df


def add_size_and_classes(df: pd.DataFrame) -> pd.DataFrame:
    """PwnMillions, DataClassesStr, DataClassCount and Industry."""
    df["PwnMillions"] = (df["PwnCount"] / 1_000_000).round(3)
    df["DataClassesStr"] = df["DataClasses"].apply(
        lambda x: ", ".join(x) if isinstance(x, list) else ""
    )
    df["DataClassCount"] = df["DataClasses"].apply(
        lambda x: len(x) if isinstance(x, list) else 0
    )
    df["Industry"] = df["Domain"].apply(map_industry)
    return df
