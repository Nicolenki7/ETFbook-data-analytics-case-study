import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
st.set_page_config(page_title="ETF Central", page_icon="📊", layout="wide")

# ---------- CACHE ----------
@st.cache_data
def load_data():
    df = pd.read_csv("etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ---------- SIDEBAR – FILTROS GLOBALES ----------
with st.sidebar:
    st.title("🔧 Central de Filtros")
    date_range = st.date_input("Rango de fechas", [df["date"].min(), df["date"].max()])
    region_opts = st.multiselect("Región(es)", df["region"].unique(), default=df["region"].unique())
    etf_opts = st.multiselect("ETF(s)", df["etf_ticker"].unique(), default=df["etf_ticker"].unique())

mask = (df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1])) & \
       (df["region"].isin(region_opts)) & (df["etf_ticker"].isin(etf_opts))
df_f = df[mask]

# ---------- KPIs TOP ----------
st.markdown("## 📊 Central de Mando – ETF Flow Analytics")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
total = df_f["net_flows_usd_m"].sum()
avg = df_f["net_flows_usd_m"].mean()
top_et = df_f.groupby("etf_ticker")["net_flows_usd_m"].sum().idxmax()
volat = df_f["net_flows_usd_m"].std()
sharpe = avg / volat if volat else 0

kpi1.metric("Total Flows", f"${total:,.0f}M")
kpi2.metric("Average", f"${avg:,.0f}M")
kpi3.metric("Top ETF", top_et)
kpi4.metric("Volatility", f"${volat:,.0f}M")
kpi5.metric("Sharpe-like", f"{sharpe:.2f}")

# ---------- GRAFICOS CENTRALES ----------
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown("### 🔥 Serie Temporal – Flujos Globales")
    ts = df_f.groupby("date", as_index=False)["net_flows_usd_m"].sum()
    fig_ts = px.line(ts, x="date", y="net_flows_usd_m", markers=True, height=350)
    fig_ts.update_traces(line_width=3)
    st.plotly_chart(fig_ts, use_container_width=True)

with c2:
    st.markdown("### 🌍 Distribución Regional")
    reg = df_f.groupby("region", as_index=False)["net_flows_usd_m"].sum()
    fig_reg = px.pie(reg, names="region", values="net_flows_usd_m", hole=0.5, height=350)
    st.plotly_chart(fig_reg, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown("### 📈 Ranking por ETF")
    etf_rank = df_f.groupby("etf_ticker", as_index=False)["net_flows_usd_m"].sum().sort_values("net_flows_usd_m")
    fig_bar = px.bar(etf_rank, x="net_flows_usd_m", y="etf_ticker", orientation="h", text_auto=True, height=350)
    st.plotly_chart(fig_bar, use_container_width=True)

with c4:
    st.markdown("### 🧮 Correlación entre ETFs")
    pivot = df_f.pivot_table(values="net_flows_usd_m", index="date", columns="etf_ticker", fill_value=0)
    corr = pivot.corr()
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", height=350)
    st.plotly_chart(fig_corr, use_container_width=True)

# ---------- Heatmap mensual ----------
st.markdown("### 📅 Heatmap – Flujos Mensuales por ETF")
df_f["year_month"] = df_f["date"].dt.to_period("M").astype(str)
heat = df_f.groupby(["year_month", "etf_ticker"])["net_flows_usd_m"].sum().unstack(fill_value=0)
fig_heat = px.imshow(heat, text_auto=True, aspect="auto", color_continuous_scale="Blues", height=400)
st.plotly_chart(fig_heat, use_container_width=True)

# ---------- Scatter: Flow vs Volatilidad ----------
st.markdown("### 🔍 Flow vs Volatilidad (última ventana móvil)")
window = st.slider("Días para ventana móvil", 5, 30, 10, 5)
roll = df_f.set_index("date").groupby("etf_ticker")["net_flows_usd_m"].rolling(window).agg(["mean", "std"]).reset_index()
roll.columns = ["etf_ticker", "date", "mean_flow", "std_flow"]
fig_scat = px.scatter(roll, x="std_flow", y="mean_flow", color="etf_ticker", size="mean_flow".abs(), hover_data=["date"], height=400)
fig_scat.update_layout(xaxis_title="Volatilidad (σ)", yaxis_title="Flujo medio (USD M)")
st.plotly_chart(fig_scat, use_container_width=True)

# ---------- Takeaways ----------
st.markdown("---")
st.markdown("**💡 Insights clave:** ETF flows actúan como proxy de confianza; la persistencia de flujos positivos refuerza liquidez y fuerza del producto.")
