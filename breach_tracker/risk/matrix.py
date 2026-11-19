"""Data-class frequency table (one row per breach x data class)."""
import pandas as pd


def compute_data_class_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten DataClassesStr, then count by class/industry/severity."""
    rows = []
    for _, row in df.iterrows():
        if not isinstance(row["DataClassesStr"], str):
            continue
        for cls in row["DataClassesStr"].split(","):
            cls = cls.strip()
            if cls:
                rows.append({
                    "BreachName": row["Name"],
                    "Year": row.get("Year"),
                    "Industry": row.get("Industry"),
                    "SeverityLabel": row.get("SeverityLabel"),
                    "DataClass": cls,
                })
    matrix = pd.DataFrame(rows)
    return matrix.groupby(["DataClass", "Industry", "SeverityLabel"]).agg(
        Frequency=("BreachName", "count")
    ).reset_index().sort_values("Frequency", ascending=False)
