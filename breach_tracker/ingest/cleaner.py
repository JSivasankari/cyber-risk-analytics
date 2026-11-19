"""Step 1b: parse the raw HIBP JSON into one tidy DataFrame."""
import pandas as pd

from .features import add_date_features, add_size_and_classes

KEEP = [
    "Name", "Title", "Domain", "BreachDate", "AddedDate",
    "PwnCount", "DataClasses", "IsVerified", "IsSensitive",
    "IsRetired", "IsSpamList", "IsFabricated", "Description",
]
FLAG_COLS = ["IsVerified", "IsSensitive", "IsRetired",
             "IsSpamList", "IsFabricated"]


def clean_breaches(raw: list) -> pd.DataFrame:
    """Select columns, engineer features, cast flags to 0/1."""
    df = pd.DataFrame(raw)
    df = df[[c for c in KEEP if c in df.columns]].copy()

    df = add_date_features(df)
    df = add_size_and_classes(df)

    for col in FLAG_COLS:
        if col in df.columns:
            df[col] = df[col].astype(int)

    return df.reset_index(drop=True)
