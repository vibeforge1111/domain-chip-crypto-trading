# Next Probes

This page turns the seeded catalog into an actionable next frontier.

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-8400e6c02b-sparse_signal

- candidate_id: `auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-8400e6c02b`
- doctrine: `trend_regime_following`
- strategy: `ema_pullback_long`
- market_regime: `trend`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## auto-trend-volume-filtered-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter-probe-holdout_decay-sparse_signal

- candidate_id: `auto-trend-volume-filtered-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter-probe-holdout_decay`
- doctrine: `trend_regime_following`
- strategy: `ema_pullback_long`
- market_regime: `trend`
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

## auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-late_sample_guard=on-probe-sparse_signal-sparse_signal

- candidate_id: `auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-late_sample_guard=on-probe-sparse_signal`
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

## auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-late_sample_guard=on-session_profile=squee-1183d97024-sparse_signal

- candidate_id: `auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-late_sample_guard=on-session_profile=squee-1183d97024`
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

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-breakout-de03826d09-sparse_signal

- candidate_id: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-breakout-de03826d09`
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

## btc-15m-volatility-compression-breakout-psychology_no_chase-variety-session-stability-filter-variety-executio-747ed0b865-sparse_signal

- candidate_id: `btc-15m-volatility-compression-breakout-psychology_no_chase-variety-session-stability-filter-variety-executio-747ed0b865`
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
