"""Donut chart of breaches by severity."""
import plotly.express as px
from .theme import PLOTLY_DARK, SEV_COLORS


def severity_fig(filt):
    """Donut chart of breaches by severity label."""
    sev = filt["SeverityLabel"].value_counts().reset_index()
    sev.columns = ["Severity", "Count"]
    fig = px.pie(sev, names="Severity", values="Count", hole=0.55,
                 color="Severity", color_discrete_map=SEV_COLORS)
    fig.update_traces(textposition="outside", textinfo="percent+label")
    fig.update_layout(**PLOTLY_DARK, showlegend=False)
    return fig
