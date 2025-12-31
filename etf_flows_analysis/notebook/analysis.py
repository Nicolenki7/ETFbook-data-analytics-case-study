# analysis.py
# ETF Flows Analysis - Standalone Script

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# Load data
# -------------------------
DATA_PATH = "../data/etf_flows_2025_export.csv"

df = pd.read_csv(DATA_PATH)

print("Data loaded successfully")
print(df.head())

# -------------------------
# Basic checks
# -------------------------
print("\nColumns:")
print(df.columns)

df["date"] = pd.to_datetime(df["date"])

# -------------------------
# Ranking ETFs by daily net flow
# -------------------------
df["daily_rank"] = (
    df.groupby("date")["net_flow"]
      .rank(method="dense", ascending=False)
)

print("\nDaily ranking sample:")
print(df.sort_values(["date", "daily_rank"]).head(10))

# -------------------------
# Top 3 ETFs per day
# -------------------------
top_3_daily = df[df["daily_rank"] <= 3]

print("\nTop 3 ETFs per day:")
print(top_3_daily.head(10))

# -------------------------
# Plot net flows over time
# -------------------------
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=df,
    x="date",
    y="net_flow",
    hue="etf_ticker"
)
plt.title("ETF Net Flows Over Time")
plt.xlabel("Date")
plt.ylabel("Net Flow (USD M)")
plt.tight_layout()
plt.show()

# -------------------------
# Plot Top 3 ETFs only
# -------------------------
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=top_3_daily,
    x="date",
    y="net_flow",
    hue="etf_ticker"
)
plt.title("Top 3 ETFs by Daily Net Flow")
plt.xlabel("Date")
plt.ylabel("Net Flow (USD M)")
plt.tight_layout()
plt.show()
