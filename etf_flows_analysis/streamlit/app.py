import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(
    page_title="ETF Flows Analysis – Case Study",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2a5298;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------
# CARGAR DATOS (RUTA ORIGINAL)
# -----------------------
@st.cache_data
def load_data():
    # MANTENGO TU RUTA ORIGINAL
    DATA_PATH = "etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv"
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# -----------------------
# TÍTULO
# -----------------------
st.title("ETF Flows Analysis – Case Study")
st.markdown("**Objective:** Analyze ETF net flows to understand capital allocation trends, investor sentiment, and regional dynamics")

# -----------------------
# KPIs MEJORADOS
# -----------------------
col1, col2, col3, col4 = st.columns(4)

total_flows = df["net_flows_usd_m"].sum()
avg_flow = df["net_flows_usd_m"].mean()
top_etf = df.groupby("etf_ticker")["net_flows_usd_m"].sum().idxmax()
flow_volatility = df["net_flows_usd_m"].std()

with col1:
    st.metric("Total Net Flows", f"${total_flows:,.0f}M")
with col2:
    st.metric("Average Flow", f"${avg_flow:,.0f}M")
with col3:
    st.metric("Top ETF", top_etf)
with col4:
    st.metric("Volatility", f"${flow_volatility:,.0f}M")

# -----------------------
# VISUALIZACIONES MEJORADAS
# -----------------------
st.subheader("📈 Global ETF Net Flow Trend")

# Gráfico interactivo con Plotly
flows_by_date = df.groupby("date", as_index=False)["net_flows_usd_m"].sum()

fig = px.line(flows_by_date, x="date", y="net_flows_usd_m", 
              title="Total ETF Net Flows Over Time",
              markers=True)
fig.update_traces(line_color="#1f77b4", line_width=3)
st.plotly_chart(fig, use_container_width=True)

# Análisis por ETF
st.subheader("🔍 Individual ETF Analysis")
selected_etf = st.selectbox("Select ETF", sorted(df["etf_ticker"].unique()))
etf_df = df[df["etf_ticker"] == selected_etf]

if not etf_df.empty:
    fig_etf = px.line(etf_df, x="date", y="net_flows_usd_m",
                      title=f"Net Flows – {selected_etf}",
                      markers=True)
    st.plotly_chart(fig_etf, use_container_width=True)

# Análisis regional
st.subheader("🌍 Regional Analysis")
region_flows = df.groupby("region", as_index=False)["net_flows_usd_m"].sum()

fig_region = px.bar(region_flows, x="region", y="net_flows_usd_m",
                    title="Net Flows by Region")
st.plotly_chart(fig_region, use_container_width=True)

# -----------------------
# TAKEAWAYS
# -----------------------
st.subheader("💡 Key Takeaways")
st.markdown("""
- ETF flows act as a **real-time proxy for investor confidence**
- Sustained inflows suggest **product strength and liquidity** 
- Regional patterns reveal **macro and allocation trends**
""")
