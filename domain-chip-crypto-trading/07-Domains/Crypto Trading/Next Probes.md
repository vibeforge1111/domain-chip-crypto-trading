# Next Probes

This page turns the seeded catalog into an actionable next frontier.

## auto-trend-volume-filtered-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter-holdout_decay

- candidate_id: `auto-trend-volume-filtered-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter`
- doctrine: `trend_regime_following`
- strategy: `ema_pullback_long`
- market_regime: `trend`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## mut-ablate-auto-trend-volume-filtered-activation_pr-de5c86-holdout_decay

- candidate_id: `mut-ablate-auto-trend-volume-filtered-activation_pr-de5c86`
- doctrine: `trend_regime_following`
- strategy: `ema_pullback_long`
- market_regime: `trend`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## mut-ablate-auto-trend-volume-filtered-activation_pr-f32eba-holdout_decay

- candidate_id: `mut-ablate-auto-trend-volume-filtered-activation_pr-f32eba`
- doctrine: `trend_regime_following`
- strategy: `ema_pullback_long`
- market_regime: `trend`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## mut-ablate-auto-trend-volume-filtered-no_trade_wind-3af36f-holdout_decay

- candidate_id: `mut-ablate-auto-trend-volume-filtered-no_trade_wind-3af36f`
- doctrine: `trend_regime_following`
- strategy: `ema_pullback_long`
- market_regime: `trend`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## mut-ablate-auto-trend-volume-filtered-no_trade_wind-e072b8-holdout_decay

- candidate_id: `mut-ablate-auto-trend-volume-filtered-no_trade_wind-e072b8`
- doctrine: `trend_regime_following`
- strategy: `ema_pullback_long`
- market_regime: `trend`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## mut-ablate-auto-wedge-guarded-drawdown_guard=high-r-ad4069-sparse_signal

- candidate_id: `mut-ablate-auto-wedge-guarded-drawdown_guard=high-r-ad4069`
- doctrine: `mean_reversion_liquidity_reclaim`
- strategy: `wedge_exhaustion_reversal`
- market_regime: `range`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## mut-ablate-auto-wedge-guarded-reversal_confirmation-138fcb-sparse_signal

- candidate_id: `mut-ablate-auto-wedge-guarded-reversal_confirmation-138fcb`
- doctrine: `mean_reversion_liquidity_reclaim`
- strategy: `wedge_exhaustion_reversal`
- market_regime: `range`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## mut-ablate-auto-wedge-guarded-reversal_confirmation-d6abad-sparse_signal

- candidate_id: `mut-ablate-auto-wedge-guarded-reversal_confirmation-d6abad`
- doctrine: `mean_reversion_liquidity_reclaim`
- strategy: `wedge_exhaustion_reversal`
- market_regime: `range`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.
