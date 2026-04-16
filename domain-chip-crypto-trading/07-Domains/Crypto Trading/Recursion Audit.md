# Recursion Audit

This page mirrors the recursive-evolution guardrail packet.

- decision: `defer`
- stability_score: `0.66`
- top_bottleneck: Heavy backtests now include walk-forward and stress checks, but the top gated candidates still fail on drawdown, holdout strength, or robustness under fee/slippage pressure.

## Benchmark Summary

- candidate_count: `9`
- top_candidate_id: `auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-session_profile=squeeze_release_window-variet-2cc3bf4fed`
- contract_family: `btc_up_down_15m`

## Self Edit Summary

- evaluation_count: `0`
- approved_count: `0`
- deferred_count: `0`
- rejected_count: `0`

## Guardrails

- complexity_gate: `pass`
- human_gate: `pass`
- lineage_gate: `pass`
- memory_hygiene_gate: `pass`
- schema_gate: `pass`
- transfer_gate: `pass`

## Anti-Patterns

### ghost_improvement

- severity: `warn`
- status: `open`
- evidence: `The current backtester is real, but the strongest candidates still need walk-forward and stress robustness before they count as causal proof.`

### comfort_zone_optimization

- severity: `warn`
- status: `contained`
- evidence: `Heavy-backtest summary currently covers 9 candidates; this must keep shifting toward BTC-specific mutation trials.`

### golden_demo_collapse

- severity: `warn`
- status: `contained`
- evidence: `High-drawdown seeded candidates remain unresolved: bollinger-highvol-hyperliquid-1h, range-funding-ethsol-1h | Walk-forward consistency stays weak for: auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-d2310cb7de, btc-15m-volatility-compression-breakout-psychology_no_chase-variety-session-stability-filter-variety-executio-ad7f50ffda, baseline | Stress resilience remains below threshold for: auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-session_profile=squeeze_release_window-variet-2cc3bf4fed, auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-8400e6c02b, auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-d2310cb7de`

## Required Fixes

- Keep extending the BTC dataset across more market regimes while separating sparse high-profit variants from scalable ones.
- Record lineage failures per mutation proposal before self-edit or doctrine promotion.
- Benchmark every proposed mutation on holdout windows, walk-forward splits, and fee/slippage stress before paper-trade escalation.

## Next Experiments

- Extend the BTC 1m plus contract-window dataset into additional months and more violent market regimes.
- Use walk-forward and stress failures to design the next BTC 15m mutation probes instead of adding doctrine breadth blindly.
- Run the top three backlog proposals through the heavy-backtest queue before adding more doctrine families.
