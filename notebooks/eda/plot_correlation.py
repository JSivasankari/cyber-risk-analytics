"""Plot 6: correlation matrix of the numeric features."""
import matplotlib.pyplot as plt
import seaborn as sns

from breach_tracker.config import data_path

NUM_COLS = ["PwnMillions", "SeverityScore", "DisclosureLagDays",
            "DataClassCount", "IsCredentialLeak"]


def run(df):
    corr = df[NUM_COLS].dropna().corr()

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                center=0, square=True, linewidths=0.5, ax=ax)
    ax.set_title("Feature Correlation Matrix",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(data_path("plot_correlation.png"), bbox_inches="tight")
    plt.show()
