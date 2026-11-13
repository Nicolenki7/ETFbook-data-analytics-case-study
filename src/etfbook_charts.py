"""ETFbook: hacia dónde van los flujos de los ETFs de renta variable US vs EM.

Datos: etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv
(4 ETFs × 3 meses de 2025, flujos netos en millones de USD).

Uso: python src/etfbook_charts.py
"""
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from svg_chart import AZUL, ROJO, barras

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "etf_flows_analysis" / "data" / "etf_flows_trend_analysis_2025.csv"
d = pd.read_csv(CSV)
d["date"] = pd.to_datetime(d["date"])
IMG = ROOT / "docs" / "img"
IMG.mkdir(parents=True, exist_ok=True)

print(f"1. {len(d)} filas · {d.etf_ticker.nunique()} ETFs · "
      f"{d.date.dt.month.nunique()} meses ({d.date.min():%Y-%m} → {d.date.max():%Y-%m})")

por_etf = d.groupby("etf_ticker")["net_flows_usd_m"].sum().sort_values(ascending=False)
print("\n2. flujos netos por ETF (millones USD):")
print(por_etf.round(0).to_string())
barras([(t, v, AZUL if v >= 0 else ROJO) for t, v in por_etf.items()],
       "El dinero entra en EE. UU. y sale del emergente",
       IMG / "etfbook-etf.svg",
       subtitulo="flujos netos acumulados del trimestre (millones de USD)",
       formato="{:+,.0f}")

por_region = d.groupby("region")["net_flows_usd_m"].sum()
print("\n3. por región:")
print(por_region.round(0).to_string())
por_mes = d.groupby(d["date"].dt.strftime("%Y-%m"))["net_flows_usd_m"].sum()
print("\n4. por mes:")
print(por_mes.round(0).to_string())
barras([(m, v, AZUL if v >= 0 else ROJO) for m, v in por_mes.items()],
       "El saldo neto se mantiene positivo los tres meses",
       IMG / "etfbook-mensual.svg",
       subtitulo="flujos netos del conjunto por mes (millones de USD)",
       formato="{:+,.0f}")

print(f"\n5. saldo del trimestre: {d['net_flows_usd_m'].sum():+,.0f} M USD "
      f"({d['net_flows_usd_m'].sum() / d['net_flows_usd_m'].abs().sum():.1%} del movimiento bruto)")
