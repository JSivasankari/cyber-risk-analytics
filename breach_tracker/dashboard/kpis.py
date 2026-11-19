"""The five headline KPI cards on the Overview tab."""
import streamlit as st

CARD = """
        <div class="metric-card">
            <div style="font-size:1.5rem">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>"""


def render_kpis(filt):
    """Draw Total / People / Critical / Lag / Credential cards."""
    cols = st.columns(5)
    lag = filt['DisclosureLagDays'].mean()
    cred = filt['IsCredentialLeak'].mean() * 100
    crit = (filt['SeverityLabel'] == 'Critical').sum()
    metrics = [
        ("Total Breaches", f"{len(filt):,}", "🔓"),
        ("People Affected", f"{filt['PwnMillions'].sum():,.0f}M", "👥"),
        ("Critical Breaches", f"{crit}", "🚨"),
        ("Avg Disclosure Lag", f"{lag:.0f} days", "⏱️"),
        ("Credential Leaks", f"{cred:.0f}%", "🔑"),
    ]
    for col, (label, value, icon) in zip(cols, metrics):
        col.markdown(CARD.format(icon=icon, value=value, label=label),
                     unsafe_allow_html=True)
