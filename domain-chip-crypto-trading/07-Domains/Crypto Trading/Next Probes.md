# Next Probes

This page turns the seeded catalog into an actionable next frontier.

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter-holdout_decay

- candidate_id: `auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter`
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

## auto-wedge-guarded-reversal_confirmation=reclaim_close-volume_context_guard=strict_participation-wick_profile=rejection_confirm-sparse_signal

- candidate_id: `auto-wedge-guarded-reversal_confirmation=reclaim_close-volume_context_guard=strict_participation-wick_profile=rejection_confirm`
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

## btc-15m-volatility-compression-breakout-psychology_no_chase-variety-session-stability-filter-variety-executio-804e7c3cfc-sparse_signal

- candidate_id: `btc-15m-volatility-compression-breakout-psychology_no_chase-variety-session-stability-filter-variety-executio-804e7c3cfc`
- doctrine: `breakout_volatility_expansion`
- strategy: `breakout_open_interest_confirmation`
- market_regime: `high_vol`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## baseline-sparse_signal

- candidate_id: `baseline`
- doctrine: `n/a`
- strategy: `n/a`
- market_regime: `n/a`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.

## auto-range-session-wick-reversal_confirmation=reclaim_close-session_profile=opening_range_failure-volume_context_guard=thin_filter-wick_profile=rejection_confirm-sparse_signal

- candidate_id: `auto-range-session-wick-reversal_confirmation=reclaim_close-session_profile=opening_range_failure-volume_context_guard=thin_filter-wick_profile=rejection_confirm`
- doctrine: `mean_reversion_liquidity_reclaim`
- strategy: `range_reclaim_scalp`
- market_regime: `range`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.

## auto-range-session-wick-reversal_confirmation=reclaim_close-session_profile=opening_range_failure-wick_profile=rejection_confirm-sparse_signal

- candidate_id: `auto-range-session-wick-reversal_confirmation=reclaim_close-session_profile=opening_range_failure-wick_profile=rejection_confirm`
- doctrine: `mean_reversion_liquidity_reclaim`
- strategy: `range_reclaim_scalp`
- market_regime: `range`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.

## auto-range-session-wick-reversal_confirmation=wick_reclaim_close-session_profile=opening_range_failure-volume_context_guard=thin_filter-wick_profile=rejection_confirm-sparse_signal

- candidate_id: `auto-range-session-wick-reversal_confirmation=wick_reclaim_close-session_profile=opening_range_failure-volume_context_guard=thin_filter-wick_profile=rejection_confirm`
- doctrine: `mean_reversion_liquidity_reclaim`
- strategy: `range_reclaim_scalp`
- market_regime: `range`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
