import streamlit as st
import pandas as pd

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(
    page_title="ETF Flows Analysis – Case Study",
    layout="wide"
)

DATA_PATH = "etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv"

# -----------------------
# LOAD DATA
# -----------------------
st.title("ETF Flows Analysis – Case Study")

st.write("📁 Working directory:", DATA_PATH)

df = pd.read_csv(DATA_PATH)

st.success("✅ CSV loaded correctly")
st.write(f"Rows: {len(df)}")

# -----------------------
# SHOW SAMPLE DATA
# -----------------------
st.subheader("Sample data")
st.dataframe(df.head())

# -----------------------
# DATA PREP
# -----------------------
df["date"] = pd.to_datetime(df["date"])

# -----------------------
# NET FLOWS TREND (GLOBAL)
# -----------------------
st.subheader("Net Flow Trend (All ETFs)")

flows_by_date = (
    df.groupby("date")["net_flows_usd_m"]
    .sum()
    .reset_index()
)

st.line_chart(
    data=flows_by_date,
    x="date",
    y="net_flows_usd_m"
)

# -----------------------
# ETF SELECTOR
# -----------------------
st.subheader("Net Flows by ETF")

selected_etf = st.selectbox(
    "Select ETF ticker",
    sorted(df["etf_ticker"].unique())
)

filtered_df = df[df["etf_ticker"] == selected_etf]

st.line_chart(
    data=filtered_df,
    x="date",
    y="net_flows_usd_m"
)

# -----------------------
# REGION VIEW
# -----------------------
st.subheader("Net Flows by Region")

region_agg = (
    df.groupby("region")["net_flows_usd_m"]
    .sum()
    .reset_index()
)

st.bar_chart(
    data=region_agg,
    x="region",
    y="net_flows_usd_m"
)
