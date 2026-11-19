"""Tab 4: searchable raw records with CSV download."""
import streamlit as st

COLUMNS = [
    "Title", "Year", "Industry", "PwnMillions",
    "SeverityLabel", "SeverityScore", "DisclosureLagDays",
    "IsCredentialLeak", "PrimaryDataType", "DataClassesStr",
]


def render(filt):
    st.markdown("## 📋 Raw Breach Records")
    st.caption(f"{len(filt):,} records shown based on current filters")

    search = st.text_input("🔎 Search by company name", "")
    if search:
        view_df = filt[filt["Title"].str.contains(
            search, case=False, na=False)]
    else:
        view_df = filt

    st.dataframe(
        view_df[COLUMNS].sort_values("PwnMillions", ascending=False),
        use_container_width=True, height=500, hide_index=True)

    csv = view_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download filtered data as CSV", data=csv,
        file_name="breach_tracker_filtered.csv", mime="text/csv")
