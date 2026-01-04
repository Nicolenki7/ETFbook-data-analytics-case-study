import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# ---------- BOTONES INTERACTIVOS ----------
st.markdown("### 🎛️ Filtros rápidos")
c1, c2 = st.columns([1, 3])
region_opts = c1.multiselect("Región", df["region"].unique(), default=df["region"].unique())

# Botones para ETFs
st.markdown("### Selección de ETF (botones)")
all_etfs = df["etf_ticker"].unique()
cols = st.columns(len(all_etfs))
selected = []
for etf, col in zip(all_etfs, cols):
    if col.button(etf, key=etf):
        selected.append(etf)
# Si ningún botón → mostrar todos
if not selected:
    selected = list(all_etfs)

# ---------- FILTRO ----------
df_f = df[df["region"].isin(region_opts) & df["etf_ticker"].isin(selected)]

# ---------- KPIs ----------
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
c1, c2 = st.columns([3, 2])

with c1:
    st.markdown("### 🔥 Serie Temporal – Flujos Globales")
    ts = df_f.groupby("date", as_index=False)["net_flows_usd_m"].sum()
    fig_ts = px.line(ts, x="date", y="net_flows_usd_m", markers=True, height=350)
    fig_ts.update_traces(line_width=3)
    st.plotly_chart(fig_ts, use_container_width=True)

with c2:
    st.markdown("### 🌍 Distribución Regional (%)")
    reg = df_f.groupby("region", as_index=False)["net_flows_usd_m"].sum()
    reg["%"] = reg["net_flows_usd_m"] / reg["net_flows_usd_m"].sum() * 100
    fig_reg = px.bar(reg, x="region", y="net_flows_usd_m", text=reg["%"].apply(lambda x: f"{x:.1f}%"), height=350)
    fig_reg.update_traces(marker_color=["#636EFA", "#EF553B", "#00CC96", "#AB63FA"]))
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
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", height=350, color_continuous_scale="RdBu")
    st.plotly_chart(fig_corr, use_container_width=True)

# ---------- TABLA LIMPIA ----------
st.markdown("### 📋 Datos filtrados")
fmt_df = df_f.copy()
fmt_df["net_flows_usd_m"] = fmt_df["net_flows_usd_m"].apply(lambda x: f"${x:,.0f}M")
st.dataframe(fmt_df.style.set_properties(**{"background-color": "#f5f7fa", "color": "#1e3c72"}), use_container_width=True)

# ---------- TAKEAWAYS ----------
st.markdown("---")
st.markdown("**💡 Insights clave:** ETF flows actúan como proxy de confianza; la persistencia de flujos positivos refuerza liquidez y fuerza del producto.")
