"""Plotly figures for the Industry Risk tab."""
import plotly.express as px

from .theme import PLOTLY_DARK

LABEL_COLORS = {"Critical": "#ef4444", "High": "#f97316",
                "Medium": "#3b82f6", "Low": "#22c55e"}


def risk_bar_fig(risk_df):
    """Horizontal bars of composite risk score per industry."""
    ordered = risk_df.sort_values("RiskScore")
    fig = px.bar(
        ordered, x="RiskScore", y="Industry", orientation="h",
        color="RiskScore",
        color_continuous_scale=["#22c55e", "#f59e0b", "#ef4444"],
        text=ordered["RiskScore"].apply(lambda x: f"{x:.3f}"),
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(**PLOTLY_DARK, coloraxis_showscale=False)
    return fig


def scatter_fig(risk_df):
    """Breach count vs people affected; bubble size = risk."""
    fig = px.scatter(
        risk_df, x="BreachCount", y="TotalPwnedM",
        size="RiskScore", color="RiskLabel", text="Industry",
        color_discrete_map=LABEL_COLORS, size_max=50
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(**PLOTLY_DARK)
    return fig
