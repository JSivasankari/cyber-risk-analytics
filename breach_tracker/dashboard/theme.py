"""Colour palette and shared Plotly layout for the dark theme."""

SEV_COLORS = {
    "Critical": "#ef4444",
    "High": "#f97316",
    "Medium": "#3b82f6",
    "Low": "#22c55e",
}

PLOTLY_DARK = dict(
    paper_bgcolor="#0f172a",
    plot_bgcolor="#1e293b",
    font=dict(color="#e2e8f0", size=12),
    margin=dict(t=40, b=20, l=20, r=20),
    xaxis=dict(gridcolor="#334155", zerolinecolor="#334155"),
    yaxis=dict(gridcolor="#334155", zerolinecolor="#334155"),
)
