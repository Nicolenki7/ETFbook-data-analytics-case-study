import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="ETF Flows Analysis", layout="wide")

st.title("ETF Flows Analysis – Case Study")

# Debug info
st.write("📁 Working directory:", Path.cwd())

DATA_PATH = Path("etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv")
st.write("📄 CSV path:", DATA_PATH)

if not DATA_PATH.exists():
    st.error("❌ CSV file not found")
    st.stop()

df = pd.read_csv(DATA_PATH)

st.success("✅ CSV loaded correctly")
st.write("Rows:", len(df))

st.subheader("Sample data")
st.dataframe(df.head(10))

# Example simple visualization (no matplotlib)
st.subheader("Net Flow Trend")
st.line_chart(
    df.groupby("date")["net_flow_usd"].sum()
)
