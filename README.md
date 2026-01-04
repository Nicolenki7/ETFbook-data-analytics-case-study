# 📊 ETF Flow Analytics – Case Study  

A **real-time, interactive dashboard** that visualises Exchange-Traded-Fund (ETF) net-flows to uncover capital-allocation trends, investor sentiment and regional dynamics.  
Built in **pure Python** and deployed on **Streamlit Cloud**.

🔗 **Live App**: [https://etfbook-data-analytics-case.streamlit.app](https://etfbook-data-analytics-case.streamlit.app)

---

## 🎯 Objective
- Analyse monthly ETF net-flows (USD millions) across regions and tickers
- Identify winners / laggards and rotation effects
- Provide an executive-ready, button-driven command centre

---

## 🚀 Features
| Feature | Description |
|---------|-------------|
| **KPI Cards** | Total flows, average, top ETF, volatility |
| **Interactive Buttons** | One-click filter per ETF (no drop-downs) |
| **Regional Share** | Bar + % labels for instant interpretation |
| **Time-Series** | Plotly line with markers and trend-line |
| **ETF Ranking** | Horizontal bar, auto-labelled |
| **Correlation Heat-map** | Quick visual check for diversification |
| **Clean Data Table** | Monetised values, no zebra stripes |

---

## 🛠️ Tech Stack
- **Frontend / Framework**: Streamlit (Python)
- **Data**: Simulated but realistic monthly flows (CSV)
- **Visualisation**: Plotly (interactive), Pandas styling
- **Deployment**: Streamlit Cloud (free tier)

---

## 📁 Project Structure
etfbook-data-analytics-case-study/
├── app.py                              # Dashboard entry-point
├── requirements.txt                    # 4-lightweight deps
├── README.md                           # This file
└── etf_flows_analysis/
└── data/
└── etf_flows_trend_analysis_2025.csv
Copy

---

## ⚙️ Local Installation

git clone https://github.com/<your-user>/etfbook-data-analytics-case-study.git
cd etfbook-data-analytics-case-study
pip install -r requirements.txt
streamlit run app.py

Open [http://localhost:8501](http://localhost:8501) in your browser.

## 🧪 Sample Data

| date       | etf_ticker | net_flows_usd_m | region |
|------------|------------|-----------------|--------|
| 2025-01-31 | SPY        | 5,200           | US     |
| 2025-02-28 | QQQ        | 5,100           | US     |
| 2025-03-31 | IEMG       | -800            | EM     |

*Data are synthetic but mirror realistic institutional flows.*

---

## 📈 How to Use the Dashboard

1. Select region(s) in the sidebar.  
2. Click ETF buttons to add / remove tickers instantly.  
3. Read KPIs for a 5-second executive summary.  
4. Explore trends, rankings and correlations in the charts.  
5. Export insights or screenshots directly from Plotly tool-bar.

---

## 🚦 Performance Notes

- `@st.cache_data` prevents re-loading the CSV on every interaction.  
- All computations are vectorised (Pandas/NumPy) → sub-second response.  
- Plotly figures are built once and reused (no re-renders).

---

## 🔍 Key Insights (Demo)

- US ETFs capture ~87 % of total flows (home bias / liquidity premium).  
- QQQ shows Feb spike → possible earnings-season effect.  
- Cross-ETF correlation &lt; 0.35 → diversification still effective.

---

## 🧩 Next Steps (Road-map)

- [ ] Connect to live **yfinance** or **Bloomberg API**  
- [ ] Add Sharpe, Sortino, VaR analytics  
- [ ] Monte-Carlo flow projections  
- [ ] Dark-mode toggle

---

## 🤝 Contributing

Feel free to open issues or submit PRs. For major changes please discuss first via issue.

---

## 📄 License

MIT © 2025 – Open for personal and commercial use.

---

**🔗 Visualise now**: [https://etfbook-data-analytics-case.streamlit.app](https://etfbook-data-analytics-case.streamlit.app)
