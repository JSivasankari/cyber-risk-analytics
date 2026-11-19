"""Streamlit entry point:  python -m streamlit run app.py"""
import streamlit as st

from breach_tracker.dashboard import (
    data, refresh, styles, tab_industry, tab_leak, tab_overview, tab_raw,
)
from breach_tracker.dashboard.filters import apply_filters
from breach_tracker.dashboard.sidebar import render_sidebar

refresh.top_bar()

st.set_page_config(
    page_title="Breach Tracker",
    layout="wide",
    page_icon="🔓",
    initial_sidebar_state="expanded"
)
styles.inject_css()

data.ensure_industry_risk()
df, risk_df = data.load_data()

sel_years, sel_severity, sel_industry = render_sidebar(df)
filt = apply_filters(df, sel_years, sel_severity, sel_industry)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", "🏭 Industry Risk", "🔍 Leak Deep Dive", "📋 Raw Data"
])
with tab1:
    tab_overview.render(filt, sel_years)
with tab2:
    tab_industry.render(risk_df)
with tab3:
    tab_leak.render(filt)
with tab4:
    tab_raw.render(filt)
