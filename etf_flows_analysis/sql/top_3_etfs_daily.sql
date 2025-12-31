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
)

SELECT *
FROM ranked_flows
WHERE rank <= 3
ORDER BY date, rank;
