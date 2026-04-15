# Regime Taxonomy and Confidence

This page explains how the chip decides what kind of market BTC is in. We do not use only `bullish`, `bearish`, or `choppy`; we classify by path behavior, volatility shape, and execution conditions.

## What We Measure

- `directional_efficiency`: how straight the market path is versus noisy back-and-forth travel
- `sign_flip_rate`: how often short-horizon returns reverse direction
- `mean_abs_return_pct` and `p99_abs_return_pct`: how violent the minute and daily moves are
- `breakout_burst_ratio`: whether moves arrive in shock bursts or steadier continuation
- `4h` metrics: execution-window behavior, which matters more than 1m noise alone
- `1d net_return_pct` and `1d directional_efficiency`: whether the broader path is persistent, balanced, or unstable

## Confidence Levels

- `validated_match`: the extracted pack behaves like the regime it claims to represent
- `mixed_proxy`: the pack is usable, but it shares traits with another regime and should be treated cautiously
- `mismatch_review`: the pack is mislabeled and should not drive benchmark routing
- `pending_extract`: the regime idea exists, but the dataset is not ready yet

## Current Regime Varieties

These are the current market-condition varieties the chip cares about beyond simple bullish/bearish/choppy labels:

- `trend_continuation_greed`: directional persistence, breakout acceptance, shallow pullbacks, greed dominating hesitation
- `range_chop_mean_reversion`: two-way flow, weak follow-through, reclaim and fade setups outperform breakout chase
- `fear_shock_high_alert`: abrupt volatility bursts, fear dominating, execution fragility amplified
- `compression_pre_breakout`: low directional conviction before a release window, where quality matters more than participation
- `event_driven_macro_transition`: headline or macro-sensitive windows where structure can change faster than pattern persistence

Potential subtypes that are starting to matter but are not yet first-class benchmark regimes:

- `greed_dominant` vs `fear_dominant` state overlays
- `high_vol` expansion that is not necessarily panic
- `chop_transition` where the market rotates out of trend but has not settled into clean balance

## Timing Intelligence Read

This chip is trying to understand timing in three layers at once:

- broad state: is BTC acting like trend, balance, fear-shock, compression, or event transition?
- execution state: do the 4h and 15m windows support participation or abstention?
- pattern state: should we route toward continuation, reclaim, reversal, squeeze, or no-trade logic?

The important point is that `bullish`, `bearish`, and `choppy` are not enough. Two bullish periods can require different patterns if one is greed-driven continuation and the other is event-fragile with shock bursts.
