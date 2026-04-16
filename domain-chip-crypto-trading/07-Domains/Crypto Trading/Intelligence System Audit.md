# Intelligence System Audit

This page explains how the current intelligence layers connect into benchmarking, what is genuinely working, and where the system is still thin or untrusted.

## Current Wiring

The intended path is:

1. market-regime intelligence defines candidate market-condition families
2. timeline-pack validation proves whether a claimed regime slice is actually trustworthy
3. pattern-regime pairing maps which pattern families should fit or be avoided in each validated regime
4. market-psychology overlays reshape those patterns with expectation, crowding, sell-the-news, reflexivity, and second-order effects
5. event-window review uses the same psychology layer to decide whether event windows belong in shock, transition, or unresolved lanes
6. mutation trials translate those hints into benchmarkable child variants
7. backtests decide whether the translated children survive or fail

## Smoke Status

- validated_regime_count: `0`
- pattern_count: `0`
- classified_event_candidates: `0`
- regime_mismatch_count: `0`
- benchmark_top_candidate: `auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-47aa842e1d`
- benchmark_top_profitability: `0.5356`
- benchmark_top_readiness: `0.3252`
- benchmark_top_drawdown: `0.99`

## Where The System Is Actually Intelligent

- it no longer treats all bullish or bearish periods as the same market state
- it can distinguish validated trend, range, fear, and compression regimes from weaker event-transition guesses
- it can map pattern families to those regimes with explicit avoid lists
- it can express psychology as benchmark mutations instead of leaving it as note-only theory
- it can reject event windows and psychology variants honestly when they collapse into sparse or unstable backtest behavior

## Where The System Is Still Not Intelligent Enough

- event-driven macro transition is still mostly research design, not validated routing truth
- the strongest psychology benchmark children are still sparse and mostly reject cleanly rather than improve the frontier
- intermarket context exists as doctrine logic, but not yet as strong live data in the benchmark path
- fear and greed is still only a weak overlay label, not a decisive measured input lane
- backtest leadership is still overconcentrated in the range/reclaim family

## What The Current Pages Mean Operationally

- `Regime Taxonomy and Confidence`: explains what the regime labels mean and how much to trust them
- `Timeline Pack Validation`: says whether the claimed market-condition slices are real or mislabeled
- `Pattern Regime Pairing`: says which pattern families belong in which market states and what psychology should modify
- `Event Window Review`: says whether a macro or catalyst window should be treated as shock, transition, or unresolved
- `Backtest Leaderboard`: says whether the translated variants survive benchmark reality

## Current Translation Into Backtesting

The translation into benchmark mutations is real in three ways right now:

- trend or breakout patterns can become `no_chase_after_crowded_good_news` plus `delayed_confirmation` children
- opening-range failure fade can become a `sell_the_news_failure_fade` child
- event-driven asymmetric or no-trade logic can become `wait_for_follow_through` children

What that means in practice:

- psychology is being used to reduce participation, delay entries, or demand cleaner failure confirmation
- psychology is not yet being used to create richer timing ladders, cross-asset gates, or adaptive sizing curves

## Honest Findings

- validated regime routing is real enough to trust for trend, range, fear, and compression
- psychology-aware event review is useful and honest, but still not good enough to produce a trusted event benchmark regime
- psychology-aware benchmark mutations are connected correctly now, but the first batch mostly failed because trade density collapsed
- the system is strongest at identifying what not to trust yet
- the system is weakest when it needs to explain macro transition with cross-asset context and second-order timing

## Hardening Priorities

1. keep event windows narrow and session-aware rather than broad and story-driven
2. add explicit cross-asset or macro context inputs before trusting event-transition routing
3. keep psychology mutations focused on preserving trade count while improving timing, not just on blocking entries
4. benchmark by validated regime packs more aggressively so blended totals stop dominating operator attention
5. keep the Obsidian surfaces readable enough that a human can trace regime -> pattern -> psychology -> mutation -> benchmark result without opening code
