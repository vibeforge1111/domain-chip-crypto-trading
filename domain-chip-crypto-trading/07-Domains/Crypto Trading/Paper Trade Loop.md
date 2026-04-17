# Paper Trade Loop

This loop owns outer validation on bridge-approved candidates only.

- material_change: `True`
- queue_count: `2733`
- executed_candidate_count: `2733`
- pending_data_count: `0`
- top_recommendation: `collect_more_paper_data`

Loop contract:

- consume only bridge-approved queue artifacts
- validate execution and live-like timing separately from backtests
- demote weak candidates back to the backtest loop
- never auto-promote straight to live trading
