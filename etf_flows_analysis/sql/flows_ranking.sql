SELECT
  etf_ticker,
  SUM(net_flows_usd_m) AS total_net_flows_usd_m
FROM `etfbook_case_study.etf_flows_2025`
GROUP BY etf_ticker
ORDER BY total_net_flows_usd_m DESC;

SELECT
  date,
  etf_ticker,
  net_flows_usd_m,
  RANK() OVER (
    PARTITION BY date
    ORDER BY net_flows_usd_m DESC
  ) AS flow_rank
FROM `etfbook_case_study.etf_flows_2025`
ORDER BY date, flow_rank;

WITH ranked_flows AS (
  SELECT
    date,
    etf_ticker,
    net_flows_usd_m,
    DENSE_RANK() OVER (
      PARTITION BY date
      ORDER BY net_flows_usd_m DESC
    ) AS rank
  FROM `etfbook_case_study.etf_flows_2025`
);
