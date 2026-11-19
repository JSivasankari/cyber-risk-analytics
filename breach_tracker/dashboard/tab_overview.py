"""Tab 1: Overview (KPIs, trend, severity split, cumulative)."""
import streamlit as st

from .cumulative_chart import cumulative_fig
from .kpis import render_kpis
from .freq_scale_chart import freq_scale_fig
from .severity_chart import severity_fig
from .styles import section_title


def render(filt, sel_years):
    st.markdown("## 🛡️ Dark Web Breach Intelligence Dashboard")
    st.caption(f"Showing **{len(filt):,}** breaches · "
               f"{sel_years[0]}–{sel_years[1]} · "
               "Source: HaveIBeenPwned API")
    render_kpis(filt)

    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        section_title("Breach Frequency & Scale Over Time")
        st.plotly_chart(freq_scale_fig(filt), use_container_width=True)
    with col2:
        section_title("Severity Distribution")
        st.plotly_chart(severity_fig(filt), use_container_width=True)

    section_title("Cumulative People Affected Over Time")
    st.plotly_chart(cumulative_fig(filt), use_container_width=True)
