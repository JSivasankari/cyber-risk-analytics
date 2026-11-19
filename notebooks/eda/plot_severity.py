"""Plot 2: breach count and share by severity."""
import matplotlib.pyplot as plt

from breach_tracker.config import data_path

ORDER = ["Critical", "High", "Medium", "Low"]
COLORS = {"Critical": "#EF4444", "High": "#F97316",
          "Medium": "#3B82F6", "Low": "#22C55E"}


def run(df):
    counts = df["SeverityLabel"].value_counts().reindex(ORDER)
    colors = [COLORS[s] for s in counts.index]

    fig, axes = plt.subplots(1, 2)
    axes[0].bar(counts.index, counts.values, color=colors)
    axes[0].set_title("Breach Count by Severity")
    axes[0].set_ylabel("Count")
    axes[1].pie(counts.values, labels=counts.index, colors=colors,
                autopct="%1.1f%%", startangle=90,
                wedgeprops={"edgecolor": "white", "linewidth": 2})
    axes[1].set_title("Severity Share")

    plt.suptitle("Breach Severity Distribution",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(data_path("plot_severity.png"), bbox_inches="tight")
    plt.show()
