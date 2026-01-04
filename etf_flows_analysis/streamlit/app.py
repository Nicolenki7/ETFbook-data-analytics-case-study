import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# ---------- CONFIG ----------
st.set_page_config(page_title="ETF Central", page_icon="📊", layout="wide")

# ---------- CACHE ----------
@st.cache_data
def load_data():
    df = pd.read_csv("etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ---------- TÍTULO ----------
st.markdown("## 📊 Central de Mando – ETF Flow Analytics")

# ---------- BOTONES INTERACTIVOS (centro) ----------
st.markdown("### 🎛️ Filtros rápidos")
c1, c2, c3, c4 = st.columns(4)
region_opts = c1.multiselect("Región", df["region"].unique(), default=df["region"].unique())
etf_opts = c2.multiselect("ETF", df["etf_ticker"].unique(), default=df["etf_ticker"].unique())
date_ini = c3.date_input("Desde", df["date"].min())
date_fin = c4.date_input("Hasta", df["date"].max())

# ---------- FILTRO ----------
mask = (df["date"] >= pd.to_datetime(date_ini)) & (df["date"] <= pd.to_datetime(date_fin)) & \
       (df["region"].isin(region_opts)) & (df["etf_ticker"].isin(etf_opts))
df_f = df[mask]

# ---------- KPIs ----------
st.markdown("---")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
total = df_f["net_flows_usd_m"].sum()
avg = df_f["net_flows_usd_m"].mean()
top_et = df_f.groupby("etf_ticker")["net_flows_usd_m"].sum().idxmax() if not df_f.empty else "-"
volat = df_f["net_flows_usd_m"].std()

kpi1.metric("Total Flows", f"${total:,.0f}M")
kpi2.metric("Average", f"${avg:,.0f}M")
kpi3.metric("Top ETF", top_et)
kpi4.metric("Volatility", f"${volat:,.0f}M")

# ---------- GRAFICOS ----------
st.markdown("---")
c1, c2 = st.columns([3, 2])

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

# ---------- TABLA RESUMEN ----------
st.markdown("### 📋 Tabla de datos filtrados")
st.dataframe(df_f.style.highlight_max(axis=0, color="#d6f4d6"))

# ---------- TAKEAWAYS ----------
st.markdown("---")
st.markdown("**💡 Insights clave:** ETF flows actúan como proxy de confianza; la persistencia de flujos positivos refuerza liquidez y fuerza del producto.")
