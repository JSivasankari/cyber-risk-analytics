"""Run every EDA step:  python -m notebooks.eda.run_all"""
from . import (common, insights, plot_correlation, plot_data_classes,
               plot_heatmap, plot_lag, plot_severity, plot_yearly, summary)


def main():
    df, risk_df = common.load()
    summary.run(df)
    plot_yearly.run(df)
    plot_severity.run(df)
    plot_data_classes.run(df)
    plot_lag.run(df)
    plot_heatmap.run(risk_df)
    plot_correlation.run(df)
    insights.run()


if __name__ == "__main__":
    main()
