# Plan de ejecucion

## Estado actual
- Datos: `etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv` — 12 filas, 4 ETFs (SPY, QQQ, IVV, IEMG) por 3 cierres mensuales (2025-01-31, 2025-02-28, 2025-03-31), columnas `date, etf_ticker, net_flows_usd_m, region`.
- SQL para BigQuery: 4 consultas (ranking, day-over-day con `LAG`, top 3 diario con `DENSE_RANK`, exploracion inicial).
- `notebook/analysis.py` (pandas + matplotlib), `streamlit/app.py` (Plotly) e informe generado en `docs/report.html`.

## Problemas detectados (verificados sobre el codigo versionado)
1. `analysis.py` usa `df["net_flow"]`, pero la columna real se llama `net_flows_usd_m`: el script falla con `KeyError` en la primera agregacion.
2. `analysis.py` termina en `plt.show()`: no guarda ninguna figura, asi que no deja artefacto reproducible.
3. Las rutas del CSV son relativas a la raiz del repo; ejecutar desde `notebook/` o `streamlit/` rompe la carga.
4. El README promete volatilidad, correlaciones y analisis diario, pero el CSV tiene 3 fechas mensuales y el codigo no calcula ni volatilidad ni correlacion.
5. Los importes son multiplos exactos de 100 y hay solo 3 cortes temporales: el archivo funciona como ejemplo, no es un extracto de mercado.

## Proximos pasos
1. Corregir el nombre de columna y agregar `--out docs/flow_chart.png` en `analysis.py`.
2. Resolver rutas con `Path(__file__).resolve().parents[...]` para que funcione desde cualquier cwd.
3. `tests/test_data_contract.py` + `.github/workflows/data-contract.yml` con el mismo patron que Customer-Churn y ETL_Egatur.
4. Ajustar el README a lo que el codigo hace hoy; si se quiere volatilidad y correlacion, primero ampliar el dataset a frecuencia diaria.
5. Verificar que `requirements.txt` cubra matplotlib (lo usa `analysis.py`) y fijar versiones.

## Criterio de aceptacion
- `python etf_flows_analysis/notebook/analysis.py` corre sin error, guarda el PNG y el test de contrato pasa en CI.

## Riesgos
- Extraer conclusiones de inversion con 12 filas de ejemplo seria enganoso: el informe es descriptivo, no una recomendacion.
