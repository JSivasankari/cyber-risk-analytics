"""Cumulative people-affected area chart."""
import plotly.express as px

from .theme import PLOTLY_DARK


def cumulative_fig(filt):
    """Running total of people affected, year by year."""
    cum = (filt.sort_values("Year").groupby("Year")["PwnMillions"]
           .sum().cumsum().reset_index())
    cum.columns = ["Year", "CumulativePwnedM"]
    fig = px.area(cum, x="Year", y="CumulativePwnedM",
                  color_discrete_sequence=["#8b5cf6"])
    fig.update_layout(**PLOTLY_DARK)
    fig.update_traces(fillcolor="rgba(139,92,246,0.15)",
                      line_color="#8b5cf6")
    return fig
