"""Plot 4: disclosure lag distribution and lag by severity."""
import matplotlib.pyplot as plt
import pandas as pd

from breach_tracker.config import data_path


def run(df):
    lag_df = df.dropna(subset=["DisclosureLagDays"]).copy()
    lag_df = lag_df[lag_df["DisclosureLagDays"] >= 0]
    order = ["Critical", "High", "Medium", "Low"]
    lag_df["SeverityLabel"] = pd.Categorical(
        lag_df["SeverityLabel"], categories=order, ordered=True)
    median = lag_df["DisclosureLagDays"].median()

    fig, axes = plt.subplots(1, 2)
    axes[0].hist(lag_df["DisclosureLagDays"].clip(upper=2000),
                 bins=40, color="#8B5CF6", edgecolor="white")
    axes[0].axvline(median, color="red", linestyle="--",
                    label=f"Median: {median:.0f} days")
    axes[0].set_title("Disclosure Lag Distribution")
    axes[0].set_xlabel("Days between breach & disclosure")
    axes[0].legend()
    lag_df.boxplot(column="DisclosureLagDays", by="SeverityLabel",
                   ax=axes[1])
    axes[1].set_title("Lag by Severity")
    axes[1].set_xlabel("Severity")
    axes[1].set_ylabel("Days")
    plt.suptitle("")

    plt.suptitle("Breach-to-Disclosure Lag Analysis",
                 fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(data_path("plot_disclosure_lag.png"), bbox_inches="tight")
    plt.show()
    share = (lag_df["DisclosureLagDays"] > 365).mean() * 100
    print(f"\nKey insight: {share:.1f}% of breaches "
          f"took over 1 year to be publicly disclosed.")
