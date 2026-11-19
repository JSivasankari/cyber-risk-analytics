"""Tab 3: Leak Deep Dive (lag, credential split, data types)."""
import streamlit as st

from .credential_chart import credential_fig
from .data_class_chart import data_class_fig
from .lag_chart import lag_fig
from .styles import section_title


def render(filt):
    st.markdown("## 🔍 Leak Deep Dive")
    col1, col2 = st.columns([2, 1])
    with col1:
        section_title("Breach → Disclosure Lag (bubble = scale)")
        st.plotly_chart(lag_fig(filt), use_container_width=True)
    with col2:
        section_title("Credential vs Non-Credential")
        st.plotly_chart(credential_fig(filt), use_container_width=True)

    section_title("Top 15 Most Leaked Data Types")
    st.plotly_chart(data_class_fig(filt), use_container_width=True)

    med_lag = filt["DisclosureLagDays"].median()
    over_year = (filt["DisclosureLagDays"] > 365).mean() * 100
    st.info(f"📌 **Key Insight:** Median disclosure lag is "
            f"**{med_lag:.0f} days**. **{over_year:.1f}%** of breaches "
            f"took over 1 year to be publicly disclosed.")
