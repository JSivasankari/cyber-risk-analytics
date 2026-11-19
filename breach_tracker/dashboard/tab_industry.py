"""Tab 2: Industry Risk (bar, scatter and full matrix table)."""
import streamlit as st

from .industry_charts import risk_bar_fig, scatter_fig
from .styles import section_title

DISPLAY_COLS = {
    "Industry": "Industry",
    "RiskLabel": "Risk Level",
    "RiskScorePct": "Risk Score %",
    "BreachCount": "Breaches",
    "TotalPwnedM": "Total Pwned (M)",
    "AvgSeverityScore": "Avg Severity",
    "CredLeakRate%": "Cred Leak %",
    "AvgLagDays": "Avg Lag (days)"
}


def render(risk_df):
    st.markdown("## 🏭 Industry Risk Analysis")
    st.caption("Composite risk score = 0.35×severity + 0.25×frequency "
               "+ 0.25×scale + 0.15×disclosure lag")
    if risk_df is None:
        return
    col1, col2 = st.columns([1, 1])
    with col1:
        section_title("Composite Risk Score by Industry")
        st.plotly_chart(risk_bar_fig(risk_df), use_container_width=True)
    with col2:
        section_title("Breach Count vs Total People Affected")
        st.plotly_chart(scatter_fig(risk_df), use_container_width=True)

    section_title("Full Industry Risk Matrix")
    show_cols = [c for c in DISPLAY_COLS if c in risk_df.columns]
    st.dataframe(risk_df[show_cols].rename(columns=DISPLAY_COLS),
                 use_container_width=True, hide_index=True)
