"""Top 15 leaked data classes."""
import pandas as pd
import plotly.express as px
from .theme import PLOTLY_DARK


def data_class_fig(filt):
    """Top 15 most frequently leaked data classes."""
    all_classes = []
    for row in filt["DataClassesStr"].dropna():
        all_classes.extend([c.strip() for c in row.split(",")])
    top = pd.Series(all_classes).value_counts().head(15).reset_index()
    top.columns = ["DataClass", "Count"]
    fig = px.bar(
        top.sort_values("Count"), x="Count", y="DataClass",
        orientation="h", color="Count",
        color_continuous_scale=["#1e40af", "#3b82f6", "#93c5fd"]
    )
    fig.update_layout(**PLOTLY_DARK, coloraxis_showscale=False)
    return fig
