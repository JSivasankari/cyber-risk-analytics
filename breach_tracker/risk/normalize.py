"""Min-max scaling used to put every metric on a 0-1 range."""
import pandas as pd


def normalize(series: pd.Series) -> pd.Series:
    """(x - min) / (max - min); constant series become 0.5."""
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - lo) / (hi - lo)
