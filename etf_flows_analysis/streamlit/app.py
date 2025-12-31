# app.py
# ETF Flows Trend Dashboard – Streamlit Cloud Safe Version

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    This dashboard analyzes **ETF net capital flows** to identify:
    - Investor demand
    - Liquidity trends
    - Product attractiveness
    """
)

# -------------------------
# ETF selector
# -------------------------
etfs = sorted(df["etf_ticker"].unique())

selected_etfs = st.multiselect(
    "Select ETFs to display",
    options=etfs,
    default=etfs[:3]
)

filtered_df = df[df["etf_ticker"].isin(selected_etfs)]

# -------------------------
# Net flows chart
# -------------------------
st.subheader("Net Flows Over Time")

fig, ax = plt.subplots(figsize=(12, 5))

for etf in filtered_df["etf_ticker"].unique():
    subset = filtered_df[filtered_df["etf_ticker"] == etf]
    ax.plot(subset["date"], subset["net_flow"], label=etf)

ax.set_xlabel("Date")
ax.set_ylabel("Net Flow (USD M)")
ax.set_title("ETF Net Capital Flows")
ax.legend()

st.pyplot(fig)

# -------------------------
# Ranking logic
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
# Key insights
# -------------------------
st.markdown(
    """
    ### Key Insights
    - Positive net flows indicate **capital inflows and investor confidence**
    - ETFs consistently ranked in the top 3 tend to show **higher liquidity**
    - Sudden flow reversals may signal **market rebalancing or macro events**
    """
)
