# Next Probes

This page turns the seeded catalog into an actionable next frontier.

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compressio-17198cff45-sparse_signal

- candidate_id: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compressio-17198cff45`
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

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compressio-e2b0edf047-sparse_signal

- candidate_id: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compressio-e2b0edf047`
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

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-variety-late-sample-guard-plus-session-filter-sparse_signal

- candidate_id: `auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-variety-late-sample-guard-plus-session-filter`
- doctrine: `breakout_volatility_expansion`
- strategy: `bollinger_squeeze_breakout`
- market_regime: `high_vol`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-momentum-breakout-structure-psy-dc69343ca7-sparse_signal

- candidate_id: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-momentum-breakout-structure-psy-dc69343ca7`
- doctrine: `breakout_volatility_expansion`
- strategy: `breakout_open_interest_confirmation`
- market_regime: `trend`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.

## auto-wedge-guarded-drawdown_guard=high-reversal_confirmation=reclaim_close-volume_context_guard=thin_filter-w-1fccb6d1f0-sparse_signal

- candidate_id: `auto-wedge-guarded-drawdown_guard=high-reversal_confirmation=reclaim_close-volume_context_guard=thin_filter-w-1fccb6d1f0`
- doctrine: `mean_reversion_liquidity_reclaim`
- strategy: `wedge_exhaustion_reversal`
- market_regime: `range`
- priority: `0.8854`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=stri-6b92847572-segment_instability

- candidate_id: `auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=stri-6b92847572`
- doctrine: `trend_regime_following`
- strategy: `ema_pullback_long`
- market_regime: `trend`
- priority: `0.6425`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-044fc241ff-segment_instability

- candidate_id: `auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-044fc241ff`
- doctrine: `trend_regime_following`
- strategy: `ema_pullback_long`
- market_regime: `trend`
- priority: `0.5425`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.
