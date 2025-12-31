# app.py
# Streamlit ETF Flow Dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="ETF Flow Analysis",
    layout="wide"
)

# -------------------------
# Load data
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv("../data/etf_flows_2025_export.csv")

df = load_data()
df["date"] = pd.to_datetime(df["date"])

# -------------------------
# Title & description
# -------------------------
st.title("ETF Flow Analysis – 2025")
st.markdown(
    """
    This dashboard analyzes **ETF net capital flows** to identify
    investor demand, liquidity trends, and product attractiveness.
    """
)

# -------------------------
# ETF selector
# -------------------------
selected_etfs = st.multiselect(
    "Select ETF(s)",
    options=sorted(df["etf_ticker"].unique()),
    default=sorted(df["etf_ticker"].unique())[:3]
)

filtered_df = df[df["etf_ticker"].isin(selected_etfs)]

# -------------------------
# Net flows chart
# -------------------------
st.subheader("Net Flows Over Time")

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(
    data=filtered_df,
    x="date",
    y="net_flow",
    hue="etf_ticker",
    ax=ax
)

ax.set_xlabel("Date")
ax.set_ylabel("Net Flow (USD M)")
ax.set_title("ETF Net Flows")
st.pyplot(fig)

# -------------------------
# Ranking logic
# -------------------------
df["daily_rank"] = (
    df.groupby("date")["net_flow"]
      .rank(method="dense", ascending=False)
)

top_3 = df[df["daily_rank"] <= 3]

# -------------------------
# Top 3 table
# -------------------------
st.subheader("Top 3 ETFs by Daily Net Flow")
st.dataframe(
    top_3.sort_values(["date", "daily_rank"]),
    use_container_width=True
)

# -------------------------
# Key insights
# -------------------------
st.markdown(
    """
    ### Key Insights
    - Positive net flows indicate **capital inflows and investor confidence**
    - Persistent top-ranked ETFs tend to show **higher liquidity**
    - Sudden changes may reflect **market rebalancing or macro events**
    """
)
