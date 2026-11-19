"""Plot 1: breaches per year and people affected."""
import matplotlib.pyplot as plt

from breach_tracker.config import data_path


def run(df):
    yearly = df.groupby("Year").agg(
        Breaches=("Name", "count"),
        PwnMillions=("PwnMillions", "sum")
    ).reset_index().dropna(subset=["Year"])

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.bar(yearly["Year"], yearly["Breaches"], color="#3B82F6",
            alpha=0.75, label="Breach count")
    ax2.plot(yearly["Year"], yearly["PwnMillions"], color="#EF4444",
             lw=2.5, marker="o", label="People affected (M)")

    ax1.set_xlabel("Year")
    ax1.set_ylabel("Number of breaches", color="#3B82F6")
    ax2.set_ylabel("Millions affected", color="#EF4444")
    ax1.set_title("Breach Frequency & Scale Over Time",
                  fontsize=14, fontweight="bold")
    l1, n1 = ax1.get_legend_handles_labels()
    l2, n2 = ax2.get_legend_handles_labels()
    ax1.legend(l1 + l2, n1 + n2, loc="upper left")
    plt.tight_layout()
    plt.savefig(data_path("plot_yearly_trend.png"), bbox_inches="tight")
    plt.show()
