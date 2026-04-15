# Recursion Audit

This page mirrors the recursive-evolution guardrail packet.

- decision: `reject`
- stability_score: `0.48`
- top_bottleneck: Heavy backtests now include walk-forward and stress checks, but the top gated candidates still fail on drawdown, holdout strength, or robustness under fee/slippage pressure.

## Benchmark Summary

- candidate_count: `33`
- top_candidate_id: `auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-session_profile=squeeze_release_window`
- contract_family: `btc_up_down_15m`

## Self Edit Summary

- evaluation_count: `0`
- approved_count: `0`
- deferred_count: `0`
- rejected_count: `0`

## Guardrails

- complexity_gate: `pass`
- human_gate: `pass`
- lineage_gate: `fail`
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
- evidence: `Heavy-backtest summary currently covers 33 candidates; this must keep shifting toward BTC-specific mutation trials.`

### golden_demo_collapse

- severity: `warn`
- status: `contained`
- evidence: `Walk-forward consistency stays weak for: auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-8f1ca8f191, auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter, auto-trend-volume-filtered-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter | Stress resilience remains below threshold for: auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-session_profile=squeeze_release_window, auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-session_profile=squeeze_release_window, auto-breakout-impulse-squeeze-compression_profile=tight_squeeze`

## Required Fixes

- Keep extending the BTC dataset across more market regimes while separating sparse high-profit variants from scalable ones.
- Record lineage failures per mutation proposal before self-edit or doctrine promotion.
- Benchmark every proposed mutation on holdout windows, walk-forward splits, and fee/slippage stress before paper-trade escalation.

## Next Experiments

- Extend the BTC 1m plus contract-window dataset into additional months and more violent market regimes.
- Use walk-forward and stress failures to design the next BTC 15m mutation probes instead of adding doctrine breadth blindly.
- Run the top three backlog proposals through the heavy-backtest queue before adding more doctrine families.
