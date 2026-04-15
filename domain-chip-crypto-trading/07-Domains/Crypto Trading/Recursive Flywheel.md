# Recursive Flywheel

This page governs self-improvement for `BTC up/down 15m`.

Research may generate mutation proposals.
Heavy backtesting is the only benchmark lane allowed to ground them.

- contract_family: `n/a`
- current_decision: `reject`
- stability_score: `0.38`
- queued_heavy_backtests: `9`
- queued_self_edits: `6`
- approved_self_edits: `1`

## Loop

1. ingest trader and indicator research
2. convert research into bounded mutation proposals
3. rank proposals by surprise score
4. run heavy backtests on BTC up/down contract windows
5. derive bounded self-edits from contradiction probes
6. approve only self-edits that beat their parent failures under benchmark review
7. bridge only grounded combinations into paper trade
8. feed contradictions and paper-trade outcomes back into the next cycle

## Heavy Backtest Policy

- mode: `n/a`
- min_contract_windows: `n/a`
- walk_forward_splits: `n/a`
- holdout_policy: `n/a`
- fee_model: `n/a`
- slippage_model: `n/a`
