"""'Refresh Data' buttons: re-run the pipeline and reload the app."""
import datetime
import subprocess

import streamlit as st


def top_bar():
    """Last-refreshed caption and a refresh button at the page top."""
    now = datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')
    st.caption(f"Last refreshed: {now}")

    if st.button("🔄 Refresh Data"):
        subprocess.run(["python", "run_pipeline.py"])
        st.cache_data.clear()
        st.rerun()


def sidebar_button():
    """Refresh button in the sidebar, with a spinner and success note."""
    if st.sidebar.button("🔄 Refresh Data"):
        with st.spinner("Fetching latest breaches..."):
            subprocess.run(["python", "run_pipeline.py"])
            st.cache_data.clear()
        st.success("✅ Data updated!")
        st.rerun()
