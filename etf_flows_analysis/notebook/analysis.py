# analysis.py
# ETF Flows Trend Analysis 2025

import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Load data
# -------------------------
DATA_PATH = "etf_flows_analysis/data/etf_flows_trend_analysis_2025.csv"

df = pd.read_csv(DATA_PATH)

print("Data loaded correctly")
print(df.head())

# -------------------------
# Basic preparation
# -------------------------
df["date"] = pd.to_datetime(df["date"])

# -------------------------
# Daily ranking using window logic
# -------------------------
df["daily_rank"] = (
    df.groupby("date")["net_flow"]
      .rank(method="dense", ascending=False)
)

print("\nDaily ranking sample:")
print(df.sort_values(["date", "daily_rank"]).head(10))

# -------------------------
# Aggregate total flows per ETF
# -------------------------
total_flows = (
    df.groupby("etf_ticker", as_index=False)["net_flow"]
      .sum()
      .sort_values("net_flow", ascending=False)
)

print("\nTotal net flows per ETF:")
print(total_flows)

# -------------------------
# Plot net flows over time
# -------------------------
plt.figure(figsize=(12, 6))

for etf in df["etf_ticker"].unique():
    subset = df[df["etf_ticker"] == etf]
    plt.plot(subset["date"], subset["net_flow"], label=etf)

plt.title("ETF Net Flows Over Time (2025)")
plt.xlabel("Date")
plt.ylabel("Net Flow (USD M)")
plt.legend()
plt.tight_layout()
plt.show()
