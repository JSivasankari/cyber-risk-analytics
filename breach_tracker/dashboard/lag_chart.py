"""Disclosure lag scatter."""
import plotly.express as px
from .theme import PLOTLY_DARK, SEV_COLORS


def lag_fig(filt):
    """Disclosure lag over time; bubble size = people affected."""
    lag_df = filt.dropna(subset=["DisclosureLagDays"]).copy()
    lag_df = lag_df[lag_df["DisclosureLagDays"] >= 0]
    fig = px.scatter(
        lag_df, x="BreachDate", y="DisclosureLagDays",
        size="PwnMillions", color="SeverityLabel",
        color_discrete_map=SEV_COLORS,
        hover_data=["Title", "Industry", "PwnMillions"], size_max=40
    )
    fig.update_layout(**PLOTLY_DARK, hovermode="closest")
    return fig
