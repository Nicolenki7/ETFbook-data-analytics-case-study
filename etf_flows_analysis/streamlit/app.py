# app.py
# ETF Flows Trend Dashboard – Streamlit Native Charts (Cloud Safe)

import streamlit as st
import pandas as pd

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="ETF Flow Analysis 2025",
    layout="wide"
)

# -------------------------
# Load data
# -------------------------
@st.cache_data
def load_data():
    DATA_PATH = "etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv"
    return pd.read_csv(DATA_PATH)

df = load_data()
df["date"] = pd.to_datetime(df["date"])

# -------------------------
# Title & description
# -------------------------
st.title("ETF Net Flow Analysis – 2025")

st.markdown(
    """
    Interactive analysis of **ETF net capital flows** to understand
    investor demand, liquidity trends and product attractiveness.
    """
)

# -------------------------
# ETF selector
# -------------------------
etfs = sorted(df["etf_ticker"].unique())

selected_etfs = st.multiselect(
    "Select ETF(s)",
    options=etfs,
    default=etfs[:3]
)

filtered_df = df[df["etf_ticker"].isin(selected_etfs)]

# -------------------------
# Net flows chart (native Streamlit)
# -------------------------
st.subheader("Net Flows Over Time")

pivot_df = (
    filtered_df
    .pivot(index="date", columns="etf_ticker", values="net_flow")
    .sort_index()
)

st.line_chart(pivot_df)

# -------------------------
# Ranking logic (window function emulation)
# -------------------------
df["daily_rank"] = (
    df.groupby("date")["net_flow"]
      .rank(method="dense", ascending=False)
)

top_3_daily = df[df["daily_rank"] <= 3]

# -------------------------
# Top 3 table
# -------------------------
st.subheader("Top 3 ETFs by Daily Net Flow")

st.dataframe(
    top_3_daily.sort_values(["date", "daily_rank"]),
    use_container_width=True
)

# -------------------------
# Business insights
# -------------------------
st.markdown(
    """
    ### Key Insights
    - Positive net flows indicate **capital inflows and investor confidence**
    - ETFs consistently ranked in the top positions tend to show **higher liquidity**
    - Flow reversals often reflect **market rebalancing or macroeconomic events**
    """
)
