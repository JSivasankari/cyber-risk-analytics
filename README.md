# 🔓 Cyber Risk Analytics Dashboard

Real-time breach intelligence dashboard built on the API.

## What it does
- Fetches 999+ real breach records via HIBP API
- Scores severity using NLP (35-weight keyword matcher)
- Computes industry risk score: `0.35×severity + 0.25×frequency + 0.25×scale + 0.15×disclosure_lag`
- Visualizes everything on an interactive Streamlit dashboard

## Key Insight
Median disclosure lag is **400+ days** — companies take over a year on average to tell users their data was stolen.

## Run it
```bash
pip install -r requirements.txt
python run_pipeline.py
python -m streamlit run app.py
```

## Tech Stack
Python · Pandas · Streamlit · Plotly · HIBP API v3

