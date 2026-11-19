"""Step 3 runner: score industries and export the Excel workbook."""
import pandas as pd

from breach_tracker.config import data_path
from .excel_style import style_excel
from .industry import compute_industry_risk
from .matrix import compute_data_class_matrix
from .trend import compute_yearly_trend


def main():
    output_path = data_path("breaches_final.xlsx")
    print("[1/5] Loading tagged breach data...")
    df = pd.read_csv(data_path("breaches_tagged.csv"))
    print(f"      ✓ {len(df)} records loaded")
    print("[2/5] Computing industry risk scores...")
    risk_df = compute_industry_risk(df)
    print(f"      ✓ {len(risk_df)} industries scored")
    cols = ["Industry", "RiskScore", "RiskLabel", "BreachCount"]
    print(risk_df[cols].head(8).to_string(index=False))
    print("[3/5] Computing yearly trend data...")
    trend_df = compute_yearly_trend(df)
    print("[4/5] Computing data class frequency matrix...")
    matrix_df = compute_data_class_matrix(df)
    print(f"[5/5] Writing Excel workbook → {output_path}")
    sheets = {"Breaches": df, "IndustryRisk": risk_df,
              "YearlyTrend": trend_df, "DataClassMatrix": matrix_df}
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for name, frame in sheets.items():
            frame.to_excel(writer, sheet_name=name, index=False)
    print("      Applying professional Excel formatting...")
    style_excel(output_path)
    print(f"\n✅ Done! {output_path} exported with {len(sheets)} sheets.")
