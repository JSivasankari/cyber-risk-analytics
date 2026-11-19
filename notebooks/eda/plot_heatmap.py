"""Plot 5: industry risk heatmap (needs industry_risk.csv)."""
import matplotlib.pyplot as plt
import seaborn as sns

from breach_tracker.config import data_path

RENAME = {
    "AvgSeverityScore": "Avg Severity", "BreachCount": "Breach Count",
    "TotalPwnedM": "Total Pwned (M)", "AvgLagDays": "Avg Lag (days)",
    "RiskScore": "Risk Score",
}


def run(risk_df):
    if risk_df is None:
        return
    pivot = risk_df.set_index("Industry")[list(RENAME)].rename(
        columns=RENAME)
    pivot_norm = (pivot - pivot.min()) / (pivot.max() - pivot.min())

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(pivot_norm, annot=pivot.round(1), fmt="g",
                cmap="YlOrRd", linewidths=0.5,
                cbar_kws={"label": "Normalized value"}, ax=ax)
    ax.set_title("Industry Risk Heatmap\n"
                 "(normalized values, raw annotations)",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(data_path("plot_industry_heatmap.png"),
                bbox_inches="tight")
    plt.show()
