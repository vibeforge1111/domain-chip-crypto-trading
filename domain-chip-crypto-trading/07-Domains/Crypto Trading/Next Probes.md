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

## auto-auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-session_profile=squeeze_release_windo-cb857460ce-sparse_signal

- candidate_id: `auto-auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-session_profile=squeeze_release_windo-cb857460ce`
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

## auto-auto-baseline-sparse_signal-probe-sparse_signal-sparse_signal-probe-sparse_signal-variety-late-sample-gu-27bd822c72-sparse_signal

- candidate_id: `auto-auto-baseline-sparse_signal-probe-sparse_signal-sparse_signal-probe-sparse_signal-variety-late-sample-gu-27bd822c72`
- doctrine: `None`
- strategy: `None`
- market_regime: `None`
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

## auto-auto-auto-auto-baseline-sparse_signal-probe-sparse_signal-sparse_signal-probe-sparse_signal-variety-late-samp-c05f1ad400-sparse_signal-sparse_signal

- candidate_id: `auto-auto-auto-auto-baseline-sparse_signal-probe-sparse_signal-sparse_signal-probe-sparse_signal-variety-late-samp-c05f1ad400-sparse_signal`
- doctrine: `None`
- strategy: `None`
- market_regime: `None`
- priority: `0.99`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- sparse_signal: Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.
- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-5d7170b7b6-holdout_decay

- candidate_id: `auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-5d7170b7b6`
- doctrine: `trend_regime_following`
- strategy: `ema_pullback_long`
- market_regime: `trend`
- priority: `0.6558`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- holdout_decay: Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.
- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-8f1ca8f191-segment_instability

- candidate_id: `auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-8f1ca8f191`
- doctrine: `trend_regime_following`
- strategy: `ema_pullback_long`
- market_regime: `trend`
- priority: `0.6258`
- why: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Probe Actions

- segment_instability: Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.
- execution_fragility: Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.
- drawdown_excess: Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.
