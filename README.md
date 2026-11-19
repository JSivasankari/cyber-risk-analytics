# 🔓 Cyber Risk Analytics Dashboard (Breach Tracker)

End-to-end data project: pull real breach records from the
HaveIBeenPwned (HIBP) API, score their severity, rank industries by
risk, and explore everything in a Streamlit dashboard.

## What it does
- Fetches 1,000+ real breach records via the HIBP API v3
- Scores severity with a weighted keyword matcher (50 data-class weights)
- Industry risk = `0.35×severity + 0.25×frequency + 0.25×scale + 0.15×disclosure_lag`
- Exports a Power BI-ready Excel workbook (4 formatted sheets)
- Interactive dashboard: Overview · Industry Risk · Leak Deep Dive · Raw Data

## Key insight
On the bundled snapshot, the **median disclosure lag is ~142 days** and
**~35% of breaches took over a year** to be disclosed (mean ≈ 493 days).

## Run it
```bash
pip install -r requirements.txt
python run_pipeline.py                  # fetch -> tag -> score -> Excel
python -m streamlit run app.py          # dashboard
python -m notebooks.eda.run_all         # optional: EDA charts -> data/
```

## Project map 
```
app.py                  Streamlit entry: wires the dashboard together
run_pipeline.py         Runs steps 1-3 in order
breach_tracker/
  config.py             Paths, API URL, headers
  ingest/               STEP 1 - fetch & clean
    api.py              Calls the HIBP API
    industry_map.py     Domain -> industry lookup
    features.py         Year/Month/Lag, PwnMillions, Industry columns
    cleaner.py          Select columns + build the tidy DataFrame
    pipeline.py         Step runner (saves raw JSON + clean CSV)
  tagging/              STEP 2 - severity "NLP" tagging
    weights/            One file per data category (passwords, health...)
    severity.py         Score 0-10 + Critical/High/Medium/Low label
    credentials.py      Credential-leak flag
    datatype.py         Most dangerous data class in a breach
    tier.py             Risk tier 1-4 (severity + scale)
    report.py, pipeline.py
  risk/                 STEP 3 - industry scoring + Excel
    weights.py          0.35 / 0.25 / 0.25 / 0.15
    normalize.py        Min-max scaling
    industry_agg.py     Group-by statistics
    industry_score.py   Composite score + labels
    industry.py         Orchestrates the industry table
    trend.py, matrix.py Yearly trend, data-class matrix
    excel_*.py          Workbook styling (theme/cells/columns)
    pipeline.py         Writes data/breaches_final.xlsx
  dashboard/            Streamlit UI
    theme.py, styles.py Colours + CSS
    data.py, filters.py, sidebar.py, refresh.py
    kpis.py             Headline cards
    *_chart.py          One Plotly figure per file
    tab_*.py            One file per dashboard tab
notebooks/eda/          One file per EDA plot (matplotlib/seaborn)
data/                   Raw JSON, clean/tagged CSV, Excel output
```

## Points
- **Pipeline design:** 3 independent stages, each reads a file and writes
  a file, so any stage can be re-run or tested alone.
- **Scoring:** min-max normalise four metrics, then weight them;
  weights are in one file so they are easy to tune.
- **Why modular:** small single-purpose files, easy to explain/test.
- **Known limitations:** the domain→industry map covers
  only ~36 keywords, so ~97% of breaches fall under "Other"; severity
  uses substring matching, not true NLP.

## Tech stack
Python · Pandas · Streamlit · Plotly · openpyxl · matplotlib/seaborn · HIBP API v3
