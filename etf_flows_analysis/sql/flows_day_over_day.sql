SELECT
  date,
  etf_ticker,
  net_flows_usd_m,
  LAG(net_flows_usd_m) OVER (
    PARTITION BY etf_ticker
    ORDER BY date
  ) AS previous_day_flow,
  net_flows_usd_m - LAG(net_flows_usd_m) OVER (
    PARTITION BY etf_ticker
    ORDER BY date
  ) AS flow_change
FROM `etfbook_case_study.etf_flows_2025`
ORDER BY etf_ticker, date;
