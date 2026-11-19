"""Custom CSS and small HTML helpers for the Streamlit page."""
import streamlit as st

CSS = """
<style>
    .main { background-color: #0f172a; }
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #f1f5f9; }
    .metric-label { font-size: 0.85rem; color: #94a3b8; margin-top: 4px; }
    .section-title {
        font-size: 1.1rem; font-weight: 600;
        color: #e2e8f0; margin: 1rem 0 0.5rem;
        border-left: 3px solid #3b82f6;
        padding-left: 10px;
    }
</style>
"""


def inject_css():
    """Add the dashboard CSS to the page."""
    st.markdown(CSS, unsafe_allow_html=True)


def section_title(text: str):
    """Blue-bar heading used above every chart."""
    st.markdown(f'<div class="section-title">{text}</div>',
                unsafe_allow_html=True)
