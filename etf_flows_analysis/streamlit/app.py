import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(
    page_title="ETF Flows Analysis – Case Study",
    layout="wide"
)

sns.set_theme(style="whitegrid")

DATA_PATH = "etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv"

# -----------------------
# TITLE & INTRO
# -----------------------
st.title("ETF Flows Analysis – Case Study")
st.markdown(
    """
    **Objective:**  
    Analyze ETF net flows to understand **capital allocation trends**,  
    **investor sentiment**, and **regional dynamics** in the ETF market.
    """
)

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])

# -----------------------
# DATA OVERVIEW
# -----------------------
st.subheader("Dataset Overview")
st.markdown(
    """
    This dataset represents **simulated but realistic ETF net flow data (USD millions)**  
    across multiple regions and ETFs.
    """
)

st.dataframe(df)

# -----------------------
# GLOBAL NET FLOWS TREND
# -----------------------
st.subheader("Global ETF Net Flow Trend")

st.markdown(
    """
    **What this shows:**  
    Aggregated net flows across all ETFs.  
    Positive values indicate **net capital inflows**,  
    negative values indicate **outflows**.
    """
)

flows_by_date = (
    df.groupby("date", as_index=False)["net_flows_usd_m"]
    .sum()
)

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    data=flows_by_date,
    x="date",
    y="net_flows_usd_m",
    marker="o",
    ax=ax
)

ax.set_title("Total ETF Net Flows Over Time (USD Millions)")
ax.set_xlabel("Date")
ax.set_ylabel("Net Flows (USD M)")
plt.xticks(rotation=45)

st.pyplot(fig)

# -----------------------
# ETF-SPECIFIC ANALYSIS
# -----------------------
st.subheader("Net Flows by ETF")

st.markdown(
    """
    **Purpose:**  
    Compare how individual ETFs attract or lose capital over time,  
    helping identify **winners, laggards, and rotation effects**.
    """
)

selected_etf = st.selectbox(
    "Select ETF",
    sorted(df["etf_ticker"].unique())
)

etf_df = df[df["etf_ticker"] == selected_etf]

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    data=etf_df,
    x="date",
    y="net_flows_usd_m",
    marker="o",
    ax=ax
)

ax.set_title(f"Net Flows – {selected_etf} (USD Millions)")
ax.set_xlabel("Date")
ax.set_ylabel("Net Flows (USD M)")
plt.xticks(rotation=45)

st.pyplot(fig)

# -----------------------
# REGIONAL AGGREGATION
# -----------------------
st.subheader("Net Flows by Region")

st.markdown(
    """
    **Insight:**  
    Regional aggregation highlights **geographic allocation preferences**  
    and shifts in institutional demand.
    """
)

region_flows = (
    df.groupby("region", as_index=False)["net_flows_usd_m"]
    .sum()
    .sort_values("net_flows_usd_m", ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=region_flows,
    x="region",
    y="net_flows_usd_m",
    ax=ax
)

ax.set_title("Total Net Flows by Region (USD Millions)")
ax.set_xlabel("Region")
ax.set_ylabel("Net Flows (USD M)")

st.pyplot(fig)

# -----------------------
# FINAL TAKEAWAY
# -----------------------
st.subheader("Key Takeaways")

st.markdown(
    """
    - ETF flows act as a **real-time proxy for investor confidence**
    - Sustained inflows suggest **product strength and liquidity**
    - Regional patterns reveal **macro and allocation trends**
    """
)
