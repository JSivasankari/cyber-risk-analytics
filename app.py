import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import subprocess
import streamlit as st
import datetime
st.caption(f"Last refreshed: {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}")

if st.button("🔄 Refresh Data"):
    subprocess.run(["python", "run_pipeline.py"])
    st.cache_data.clear()
    st.rerun()

st.set_page_config(
    page_title="Breach Tracker",
    layout="wide",
    page_icon="🔓",
    initial_sidebar_state="expanded"
)

st.markdown("""
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
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    breaches  = pd.read_csv(os.path.join(base, "data", "breaches_tagged.csv"),
                            parse_dates=["BreachDate", "AddedDate"])
    industry  = pd.read_csv(os.path.join(base, "data", "industry_risk.csv")) \
                if os.path.exists(os.path.join(base, "data", "industry_risk.csv")) \
                else None
    return breaches, industry

if not os.path.exists("data/industry_risk.csv"):
    import risk_scorer
    df_tmp = pd.read_csv("data/breaches_tagged.csv")
    risk_df_tmp = risk_scorer.compute_industry_risk(df_tmp)
    risk_df_tmp.to_csv("data/industry_risk.csv", index=False)

df, risk_df = load_data()

st.sidebar.image("https://img.icons8.com/fluency/96/lock.png", width=60)
st.sidebar.title("🔓 Breach Tracker")
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Data"):
    with st.spinner("Fetching latest breaches..."):
        import subprocess
        subprocess.run(["python", "run_pipeline.py"])
        st.cache_data.clear()
    st.success("✅ Data updated!")
    st.rerun()
st.sidebar.markdown("---")

years = sorted(df["Year"].dropna().unique().astype(int))
sel_years = st.sidebar.slider(
    "Year Range", int(min(years)), int(max(years)),
    (2010, int(max(years)))
)

sel_severity = st.sidebar.multiselect(
    "Severity Filter",
    ["Critical", "High", "Medium", "Low"],
    default=["Critical", "High", "Medium", "Low"]
)

sel_industry = st.sidebar.multiselect(
    "Industry Filter",
    sorted(df["Industry"].unique()),
    default=list(df["Industry"].unique())
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Source**")
st.sidebar.markdown("[HaveIBeenPwned API v3](https://haveibeenpwned.com/API/v3)")
st.sidebar.markdown("**Pipeline**")
st.sidebar.markdown("Python → NLP Tagger → Risk Scorer")

filt = df[
    (df["Year"] >= sel_years[0]) &
    (df["Year"] <= sel_years[1]) &
    (df["SeverityLabel"].isin(sel_severity)) &
    (df["Industry"].isin(sel_industry))
].copy()


SEV_COLORS = {
    "Critical": "#ef4444",
    "High":     "#f97316",
    "Medium":   "#3b82f6",
    "Low":      "#22c55e"
}

PLOTLY_DARK = dict(
    paper_bgcolor="#0f172a",
    plot_bgcolor="#1e293b",
    font=dict(color="#e2e8f0", size=12),
    margin=dict(t=40, b=20, l=20, r=20),
    xaxis=dict(gridcolor="#334155", zerolinecolor="#334155"),
    yaxis=dict(gridcolor="#334155", zerolinecolor="#334155"),
)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", "🏭 Industry Risk", "🔍 Leak Deep Dive", "📋 Raw Data"
])

with tab1:
    st.markdown("## 🛡️ Dark Web Breach Intelligence Dashboard")
    st.caption(f"Showing **{len(filt):,}** breaches · {sel_years[0]}–{sel_years[1]} · Source: HaveIBeenPwned API")

    k1, k2, k3, k4, k5 = st.columns(5)
    metrics = [
        (k1, "Total Breaches",       f"{len(filt):,}",                          "🔓"),
        (k2, "People Affected",      f"{filt['PwnMillions'].sum():,.0f}M",       "👥"),
        (k3, "Critical Breaches",    f"{(filt['SeverityLabel']=='Critical').sum()}", "🚨"),
        (k4, "Avg Disclosure Lag",   f"{filt['DisclosureLagDays'].mean():.0f} days", "⏱️"),
        (k5, "Credential Leaks",     f"{filt['IsCredentialLeak'].mean()*100:.0f}%",  "🔑"),
    ]
    for col, label, value, icon in metrics:
        col.markdown(f"""
        <div class="metric-card">
            <div style="font-size:1.5rem">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="section-title">Breach Frequency & Scale Over Time</div>',
                    unsafe_allow_html=True)
        yearly = filt.groupby("Year").agg(
            Breaches=("Name", "count"),
            PwnMillions=("PwnMillions", "sum")
        ).reset_index().dropna(subset=["Year"])

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=yearly["Year"], y=yearly["Breaches"],
            name="Breach Count", marker_color="#3b82f6", opacity=0.85
        ))
        fig.add_trace(go.Scatter(
            x=yearly["Year"], y=yearly["PwnMillions"],
            name="People Affected (M)", yaxis="y2",
            line=dict(color="#ef4444", width=2.5),
            mode="lines+markers", marker=dict(size=6)
        ))
        fig.update_layout(
            **PLOTLY_DARK,
            yaxis2=dict(overlaying="y", side="right",
                        gridcolor="#334155", title="Millions Affected"),
            legend=dict(bgcolor="#1e293b", bordercolor="#334155"),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Severity Distribution</div>',
                    unsafe_allow_html=True)
        sev = filt["SeverityLabel"].value_counts().reset_index()
        sev.columns = ["Severity", "Count"]
        fig2 = px.pie(sev, names="Severity", values="Count",
                      hole=0.55,
                      color="Severity",
                      color_discrete_map=SEV_COLORS)
        fig2.update_traces(textposition="outside", textinfo="percent+label")
        fig2.update_layout(**PLOTLY_DARK, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-title">Cumulative People Affected Over Time</div>',
                unsafe_allow_html=True)
    cum = filt.sort_values("Year").groupby("Year")["PwnMillions"].sum().cumsum().reset_index()
    cum.columns = ["Year", "CumulativePwnedM"]
    fig3 = px.area(cum, x="Year", y="CumulativePwnedM",
                   color_discrete_sequence=["#8b5cf6"])
    fig3.update_layout(**PLOTLY_DARK)
    fig3.update_traces(fillcolor="rgba(139,92,246,0.15)", line_color="#8b5cf6")
    st.plotly_chart(fig3, use_container_width=True)


with tab2:
    st.markdown("## 🏭 Industry Risk Analysis")
    st.caption("Composite risk score = 0.35×severity + 0.25×frequency + 0.25×scale + 0.15×disclosure lag")

    if risk_df is not None:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown('<div class="section-title">Composite Risk Score by Industry</div>',
                        unsafe_allow_html=True)
            fig4 = px.bar(
                risk_df.sort_values("RiskScore"),
                x="RiskScore", y="Industry",
                orientation="h",
                color="RiskScore",
                color_continuous_scale=["#22c55e", "#f59e0b", "#ef4444"],
                text=risk_df.sort_values("RiskScore")["RiskScore"].apply(lambda x: f"{x:.3f}"),
            )
            fig4.update_traces(textposition="outside")
            fig4.update_layout(**PLOTLY_DARK, coloraxis_showscale=False)
            st.plotly_chart(fig4, use_container_width=True)

        with col2:
            st.markdown('<div class="section-title">Breach Count vs Total People Affected</div>',
                        unsafe_allow_html=True)
            fig5 = px.scatter(
                risk_df,
                x="BreachCount", y="TotalPwnedM",
                size="RiskScore", color="RiskLabel",
                text="Industry",
                color_discrete_map={
                    "Critical": "#ef4444", "High": "#f97316",
                    "Medium": "#3b82f6",   "Low": "#22c55e"
                },
                size_max=50
            )
            fig5.update_traces(textposition="top center")
            fig5.update_layout(**PLOTLY_DARK)
            st.plotly_chart(fig5, use_container_width=True)

        st.markdown('<div class="section-title">Full Industry Risk Matrix</div>',
                    unsafe_allow_html=True)
        display_cols = {
            "Industry": "Industry",
            "RiskLabel": "Risk Level",
            "RiskScorePct": "Risk Score %",
            "BreachCount": "Breaches",
            "TotalPwnedM": "Total Pwned (M)",
            "AvgSeverityScore": "Avg Severity",
            "CredLeakRate%": "Cred Leak %",
            "AvgLagDays": "Avg Lag (days)"
        }
        show_cols = [c for c in display_cols.keys() if c in risk_df.columns]
        st.dataframe(
            risk_df[show_cols].rename(columns=display_cols),
            use_container_width=True,
            hide_index=True
        )

with tab3:
    st.markdown("## 🔍 Leak Deep Dive")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="section-title">Breach → Disclosure Lag (bubble = scale)</div>',
                    unsafe_allow_html=True)
        lag_df = filt.dropna(subset=["DisclosureLagDays"]).copy()
        lag_df = lag_df[lag_df["DisclosureLagDays"] >= 0]
        fig6 = px.scatter(
            lag_df,
            x="BreachDate", y="DisclosureLagDays",
            size="PwnMillions", color="SeverityLabel",
            color_discrete_map=SEV_COLORS,
            hover_data=["Title", "Industry", "PwnMillions"],
            size_max=40
        )
        fig6.update_layout(**PLOTLY_DARK, hovermode="closest")
        st.plotly_chart(fig6, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Credential vs Non-Credential</div>',
                    unsafe_allow_html=True)
        cred = filt["IsCredentialLeak"].map({1: "Credential Leak", 0: "Non-Credential"})
        cred_counts = cred.value_counts().reset_index()
        cred_counts.columns = ["Type", "Count"]
        fig7 = px.pie(cred_counts, names="Type", values="Count",
                      hole=0.5,
                      color="Type",
                      color_discrete_map={
                          "Credential Leak": "#ef4444",
                          "Non-Credential":  "#3b82f6"
                      })
        fig7.update_layout(**PLOTLY_DARK, showlegend=True)
        st.plotly_chart(fig7, use_container_width=True)

    st.markdown('<div class="section-title">Top 15 Most Leaked Data Types</div>',
                unsafe_allow_html=True)
    all_classes = []
    for row in filt["DataClassesStr"].dropna():
        all_classes.extend([c.strip() for c in row.split(",")])
    class_counts = pd.Series(all_classes).value_counts().head(15).reset_index()
    class_counts.columns = ["DataClass", "Count"]

    fig8 = px.bar(
        class_counts.sort_values("Count"),
        x="Count", y="DataClass", orientation="h",
        color="Count",
        color_continuous_scale=["#1e40af", "#3b82f6", "#93c5fd"]
    )
    fig8.update_layout(**PLOTLY_DARK, coloraxis_showscale=False)
    st.plotly_chart(fig8, use_container_width=True)

    med_lag = filt["DisclosureLagDays"].median()
    over_year = (filt["DisclosureLagDays"] > 365).mean() * 100
    st.info(f"📌 **Key Insight:** Median disclosure lag is **{med_lag:.0f} days**. "
            f"**{over_year:.1f}%** of breaches took over 1 year to be publicly disclosed.")

with tab4:
    st.markdown("## 📋 Raw Breach Records")
    st.caption(f"{len(filt):,} records shown based on current filters")

    search = st.text_input("🔎 Search by company name", "")
    view_df = filt[filt["Title"].str.contains(search, case=False, na=False)] if search else filt

    st.dataframe(
        view_df[[
            "Title", "Year", "Industry", "PwnMillions",
            "SeverityLabel", "SeverityScore", "DisclosureLagDays",
            "IsCredentialLeak", "PrimaryDataType", "DataClassesStr"
        ]].sort_values("PwnMillions", ascending=False),
        use_container_width=True,
        height=500,
        hide_index=True
    )

    csv = view_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download filtered data as CSV",
        data=csv,
        file_name="breach_tracker_filtered.csv",
        mime="text/csv"
    )
