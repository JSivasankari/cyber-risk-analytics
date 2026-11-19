"""Credential vs non-credential donut."""
import plotly.express as px
from .theme import PLOTLY_DARK


def credential_fig(filt):
    """Donut: credential leaks vs everything else."""
    cred = filt["IsCredentialLeak"].map(
        {1: "Credential Leak", 0: "Non-Credential"})
    counts = cred.value_counts().reset_index()
    counts.columns = ["Type", "Count"]
    fig = px.pie(counts, names="Type", values="Count", hole=0.5,
                 color="Type",
                 color_discrete_map={"Credential Leak": "#ef4444",
                                     "Non-Credential": "#3b82f6"})
    fig.update_layout(**PLOTLY_DARK, showlegend=True)
    return fig
