"""Sidebar: branding, refresh button, filters and data-source notes."""
import streamlit as st

from .refresh import sidebar_button

LEVELS = ["Critical", "High", "Medium", "Low"]


def render_sidebar(df):
    """Draw the sidebar and return (years, severities, industries)."""
    st.sidebar.image("https://img.icons8.com/fluency/96/lock.png", width=60)
    st.sidebar.title("🔓 Breach Tracker")
    st.sidebar.markdown("---")
    sidebar_button()
    st.sidebar.markdown("---")

    years = sorted(df["Year"].dropna().unique().astype(int))
    sel_years = st.sidebar.slider(
        "Year Range", int(min(years)), int(max(years)),
        (2010, int(max(years))))
    sel_severity = st.sidebar.multiselect(
        "Severity Filter", LEVELS, default=LEVELS)
    sel_industry = st.sidebar.multiselect(
        "Industry Filter", sorted(df["Industry"].unique()),
        default=list(df["Industry"].unique()))

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Data Source**")
    st.sidebar.markdown("[HaveIBeenPwned API v3](https://haveibeenpwned.com/API/v3)")
    st.sidebar.markdown("**Pipeline**")
    st.sidebar.markdown("Python → NLP Tagger → Risk Scorer")
    return sel_years, sel_severity, sel_industry

