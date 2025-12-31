import streamlit as st
import pandas as pd

# ---------------------------------
# STREAMLIT CONFIG
# ---------------------------------
st.set_page_config(
    page_title="ETF Flows Analysis – Case Study",
    layout="wide"
)

DATA_PATH = "etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv"

# ---------------------------------
# LOAD DATA
# ---------------------------------
st.title("ETF Flows Analysis – Case Study")

st.write("📄 CSV path:", DATA_PATH)

df = pd.read_csv(DATA_PATH)

st.success("✅ CSV loaded correctly")
st.write("Rows:", len(df))

# ---------------------------------
# BASIC CHECK (NO FAIL)
# ---------------------------------
st.subheader("Detected columns")
st.write(df.columns.tolist())

# ---------------------------------
# PREP DATA
# ---------------------------------
df["date"] = pd.to_datetime(df["date"])

# ---------------------------------
# GLOBAL NET FLOWS TREND
# ---------------------------------
st.subheader("Net Flow Trend (All ETFs)")

flows_by_date = (
    df.groupby("date", as_index=False)["net_flows_usd_m"]
    .sum()
)

st.line_chart(
    flows_by_date,
    x="date",
    y="net_flows_usd_m"
)

# ---------------------------------
# ETF-SPECIFIC VIEW
# ---------------------------------
st.subheader("Net Flows by ETF")

selected_etf = st.selectbox(
    "Select ETF ticker",
    sorted(df["etf_ticker"].unique())
)

etf_df = df[df["etf_ticker"] == selected_etf]

st.line_chart(
    etf_df,
    x="date",
    y="net_flows_usd_m"
)

# ---------------------------------
# REGION AGGREGATION
# ---------------------------------
st.subheader("Net Flows by Region")

region_flows = (
    df.groupby("region", as_index=False)["net_flows_usd_m"]
    .sum()
)

st.bar_chart(
    region_flows,
    x="region",
    y="net_flows_usd_m"
)
