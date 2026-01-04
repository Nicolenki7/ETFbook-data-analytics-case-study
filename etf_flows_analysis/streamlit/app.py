import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------- CONFIG ----------
st.set_page_config(page_title="ETF Flow Dashboard", page_icon="📊", layout="wide")

# ---------- CACHE ----------
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv("etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ---------- HEADER ----------
st.markdown("## 📊 ETF Flow Analytics – Command Center")

# ---------- CONTROLS ----------
st.markdown("### 🎛️ Quick Filters")
c1, c2 = st.columns([1, 3])
region_sel = c1.multiselect("Region(s)", df["region"].unique(), default=df["region"].unique())

etf_buttons = st.columns(len(df["etf_ticker"].unique()))
selected = [etf for etf, col in zip(df["etf_ticker"].unique(), etf_buttons) if col.button(etf, key=etf)]
if not selected:
    selected = list(df["etf_ticker"].unique())

# ---------- FILTER ----------
df_f = df[df["region"].isin(region_sel) & df["etf_ticker"].isin(selected)]

# ---------- KPIs ----------
st.markdown("---")
k1, k2, k3, k4 = st.columns(4)
total = df_f["net_flows_usd_m"].sum()
avg   = df_f["net_flows_usd_m"].mean()
top   = df_f.groupby("etf_ticker")["net_flows_usd_m"].sum().idxmax() if not df_f.empty else "-"
vol   = df_f["net_flows_usd_m"].std()

k1.metric("Total Net Flows", f"${total:,.0f}M")
k2.metric("Average Flow",    f"${avg:,.0f}M")
k3.metric("Top ETF",         top)
k4.metric("Flow Volatility", f"${vol:,.0f}M")

# ---------- CHARTS ----------
st.markdown("---")
c1, c2 = st.columns([3, 2])

with c1:
    st.markdown("### 🔥 Global Flow Trend (USD Millions)")
    ts = df_f.groupby("date", as_index=False)["net_flows_usd_m"].sum()
    fig = px.line(ts, x="date", y="net_flows_usd_m", markers=True, height=350)
    fig.update_traces(line_width=3)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### 🌍 Regional Share")
    reg = df_f.groupby("region", as_index=False)["net_flows_usd_m"].sum()
    reg["pct"] = reg["net_flows_usd_m"] / reg["net_flows_usd_m"].sum() * 100
    fig = px.bar(reg, x="region", y="net_flows_usd_m", text=reg["pct"].apply(lambda x: f"{x:.1f}%"), height=350)
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown("### 📈 ETF Ranking")
    rank = df_f.groupby("etf_ticker", as_index=False)["net_flows_usd_m"].sum().sort_values("net_flows_usd_m")
    fig = px.bar(rank, x="net_flows_usd_m", y="etf_ticker", orientation="h", text_auto=True, height=350)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.markdown("### 🧮 Cross-ETF Correlation")
    pivot = df_f.pivot_table(values="net_flows_usd_m", index="date", columns="etf_ticker", fill_value=0)
    corr = pivot.corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", height=350, color_continuous_scale="RdBu")
    st.plotly_chart(fig, use_container_width=True)

# ---------- CLEAN TABLE ----------
st.markdown("### 📋 Filtered Dataset (USD Millions)")
money_fmt = df_f.copy()
money_fmt["net_flows_usd_m"] = money_fmt["net_flows_usd_m"].apply(lambda x: f"${x:,.0f}M")
st.dataframe(money_fmt, use_container_width=True)

# ---------- CLOSING ----------
st.markdown("---")
st.markdown("**💡 Key Takeaways:** ETF flows are a real-time proxy for investor confidence. Sustained inflows signal product strength and reveal macro allocation trends.")
