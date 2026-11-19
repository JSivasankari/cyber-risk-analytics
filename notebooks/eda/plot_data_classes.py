"""Plot 3: top 15 most leaked data types."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from breach_tracker.config import data_path


def run(df):
    all_classes = []
    for row in df["DataClassesStr"].dropna():
        all_classes.extend([c.strip() for c in row.split(",")])
    counts = pd.Series(all_classes).value_counts().head(15)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(counts.index[::-1], counts.values[::-1],
                   color=sns.color_palette("Blues_r", len(counts)))
    ax.set_xlabel("Number of breaches containing this data class")
    ax.set_title("Top 15 Most Leaked Data Types",
                 fontsize=14, fontweight="bold")
    for bar, val in zip(bars, counts.values[::-1]):
        ax.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(data_path("plot_data_classes.png"), bbox_inches="tight")
    plt.show()
