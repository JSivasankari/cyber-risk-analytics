"""Bars + line: breaches and people affected per year."""
import plotly.graph_objects as go
from .theme import PLOTLY_DARK


def freq_scale_fig(filt):
    """Bars = breaches per year, line = people affected (millions)."""
    yearly = filt.groupby("Year").agg(
        Breaches=("Name", "count"),
        PwnMillions=("PwnMillions", "sum")
    ).reset_index().dropna(subset=["Year"])

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=yearly["Year"], y=yearly["Breaches"],
        name="Breach Count", marker_color="#3b82f6", opacity=0.85
    ))
    fig.add_trace(go.Scatter(
        x=yearly["Year"], y=yearly["PwnMillions"],
        name="People Affected (M)", yaxis="y2",
        line=dict(color="#ef4444", width=2.5),
        mode="lines+markers", marker=dict(size=6)
    ))
    fig.update_layout(
        **PLOTLY_DARK,
        yaxis2=dict(overlaying="y", side="right",
                    gridcolor="#334155", title="Millions Affected"),
        legend=dict(bgcolor="#1e293b", bordercolor="#334155"),
        hovermode="x unified"
    )
    return fig
