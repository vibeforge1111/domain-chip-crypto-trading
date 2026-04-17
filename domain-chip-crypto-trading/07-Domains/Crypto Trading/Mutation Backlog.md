# Mutation Backlog

These are the current source-grounded mutation proposals.

- proposal_count: `472`

## Trend continuation with pullback confirmation

- proposal_id: `btc-15m-trend-continuation`
- card_id: `n/a`
- doctrine_family: `trend_regime_following`
- strategy_family: `pullback_then_continuation`
- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "trend_regime_following", "regime": "trend", "strategy": "pullback_then_continuation"}`
- variety_child_id: `{"paper_gate": "strict"}`
- variety_child_label: `paper_gate=strict`
- family_tested_child_count: `0`
- target_contract_family: `btc_up_down_15m`
- benchmark_priority: `high`
- surprise_score: `0.81`
- duplicate_of_proposal_id: `n/a`
- source_names: `Ed Seykota, TurtleTrader / Richard Dennis tradition, Adam H. Grimes`
- lineage_ready: `True`
- status: `research_seeded_backtest_required`
- benchmark_profitability_score: `n/a`
- benchmark_paper_trade_readiness: `n/a`
- benchmark_next_step: `n/a`
- benchmark_trade_count: `n/a`
- benchmark_minimum_trade_count: `n/a`
- benchmark_trade_count_gate_pass: `n/a`
- benchmark_walk_forward_consistency: `n/a`
- benchmark_stress_resilience: `n/a`
- thesis: Trend doctrine should survive on BTC 15m only when pullback entries occur inside a confirmed directional regime.

## Exhaustion mean reversion after impulse

- proposal_id: `btc-15m-exhaustion-mean-reversion`
- card_id: `n/a`
- doctrine_family: `mean_reversion_liquidity_reclaim`
- strategy_family: `rsi_exhaustion_reclaim`
- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "mean_reversion_liquidity_reclaim", "regime": "range", "strategy": "rsi_exhaustion_reclaim"}`
- variety_child_id: `{"paper_gate": "balanced"}`
- variety_child_label: `paper_gate=balanced`
- family_tested_child_count: `0`
- target_contract_family: `btc_up_down_15m`
- benchmark_priority: `high`
- surprise_score: `0.81`
- duplicate_of_proposal_id: `n/a`
- source_names: `Linda Bradford Raschke, StockCharts ChartSchool, TradingView Help Center`
- lineage_ready: `True`
- status: `research_seeded_backtest_required`
- benchmark_profitability_score: `n/a`
- benchmark_paper_trade_readiness: `n/a`
- benchmark_next_step: `n/a`
- benchmark_trade_count: `n/a`
- benchmark_minimum_trade_count: `n/a`
- benchmark_trade_count_gate_pass: `n/a`
- benchmark_walk_forward_consistency: `n/a`
- benchmark_stress_resilience: `n/a`
- thesis: Short-horizon reversions should only be tradable after impulse exhaustion plus reclaim confirmation.

## Momentum breakout with structure filter

- proposal_id: `btc-15m-momentum-breakout-structure`
- card_id: `n/a`
- doctrine_family: `breakout_volatility_expansion`
- strategy_family: `trend_template_breakout`
- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "breakout_volatility_expansion", "regime": "trend", "strategy": "trend_template_breakout"}`
- variety_child_id: `{"paper_gate": "strict"}`
- variety_child_label: `paper_gate=strict`
- family_tested_child_count: `0`
- target_contract_family: `btc_up_down_15m`
- benchmark_priority: `medium`
- surprise_score: `0.81`
- duplicate_of_proposal_id: `n/a`
- source_names: `Mark Minervini, Peter Brandt, StockCharts ChartSchool`
- lineage_ready: `True`
- status: `research_seeded_backtest_required`
- benchmark_profitability_score: `n/a`
- benchmark_paper_trade_readiness: `n/a`
- benchmark_next_step: `n/a`
- benchmark_trade_count: `n/a`
- benchmark_minimum_trade_count: `n/a`
- benchmark_trade_count_gate_pass: `n/a`
- benchmark_walk_forward_consistency: `n/a`
- benchmark_stress_resilience: `n/a`
- thesis: Momentum breakouts should work best when structure quality and failure containment are explicitly filtered.

## Regime-shift no-trade filter

- proposal_id: `btc-15m-regime-shift-no-trade-filter`
- card_id: `n/a`
- doctrine_family: `risk_first_asymmetric_capture`
- strategy_family: `event_avoidance_filter`
- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "risk_first_asymmetric_capture", "regime": "event_driven", "strategy": "event_avoidance_filter"}`
- variety_child_id: `{"paper_gate": "strict"}`
- variety_child_label: `paper_gate=strict`
- family_tested_child_count: `0`
- target_contract_family: `btc_up_down_15m`
- benchmark_priority: `medium`
- surprise_score: `0.81`
- duplicate_of_proposal_id: `n/a`
- source_names: `George Soros, John Murphy, Kalshi Help Center`
- lineage_ready: `True`
- status: `research_seeded_backtest_required`
- benchmark_profitability_score: `n/a`
- benchmark_paper_trade_readiness: `n/a`
- benchmark_next_step: `n/a`
- benchmark_trade_count: `n/a`
- benchmark_minimum_trade_count: `n/a`
- benchmark_trade_count_gate_pass: `n/a`
- benchmark_walk_forward_consistency: `n/a`
- benchmark_stress_resilience: `n/a`
- thesis: The best edge may come from avoiding unstable narrative or macro-shift windows rather than forcing directional exposure.

## Sizing overlay after edge calibration

- proposal_id: `btc-15m-sizing-overlay`
- card_id: `n/a`
- doctrine_family: `risk_first_asymmetric_capture`
- strategy_family: `fractional_kelly_overlay`
- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "risk_first_asymmetric_capture", "regime": "trend", "strategy": "fractional_kelly_overlay"}`
- variety_child_id: `{"paper_gate": "strict"}`
- variety_child_label: `paper_gate=strict`
- family_tested_child_count: `0`
- target_contract_family: `btc_up_down_15m`
- benchmark_priority: `medium`
- surprise_score: `0.81`
- duplicate_of_proposal_id: `n/a`
- source_names: `Edward O. Thorp, Van Tharp, Tom Basso`
- lineage_ready: `True`
- status: `research_seeded_backtest_required`
- benchmark_profitability_score: `n/a`
- benchmark_paper_trade_readiness: `n/a`
- benchmark_next_step: `n/a`
- benchmark_trade_count: `n/a`
- benchmark_minimum_trade_count: `n/a`
- benchmark_trade_count_gate_pass: `n/a`
- benchmark_walk_forward_consistency: `n/a`
- benchmark_stress_resilience: `n/a`
- thesis: Sizing should be treated as a second-stage mutation only after contract-level edge is stable under heavy backtest.

## Volatility compression breakout

- proposal_id: `btc-15m-volatility-compression-breakout`
- card_id: `n/a`
- doctrine_family: `breakout_volatility_expansion`
- strategy_family: `bollinger_squeeze_breakout`
- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "breakout_volatility_expansion", "regime": "high_vol", "strategy": "bollinger_squeeze_breakout"}`
- variety_child_id: `{"paper_gate": "strict"}`
- variety_child_label: `paper_gate=strict`
- family_tested_child_count: `2`
- target_contract_family: `btc_up_down_15m`
- benchmark_priority: `high`
- surprise_score: `0.81`
- duplicate_of_proposal_id: `n/a`
- source_names: `Linda Bradford Raschke, John Bollinger, TradingView Help Center`
- lineage_ready: `True`
- status: `research_seeded_backtest_required`
- benchmark_profitability_score: `n/a`
- benchmark_paper_trade_readiness: `n/a`
- benchmark_next_step: `n/a`
- benchmark_trade_count: `n/a`
- benchmark_minimum_trade_count: `n/a`
- benchmark_trade_count_gate_pass: `n/a`
- benchmark_walk_forward_consistency: `n/a`
- benchmark_stress_resilience: `n/a`
- thesis: Compression followed by expansion should produce the cleanest contract edge when false-break filters are strict.

## Auto-generated: sparse_signal fix for auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-bre-638dc4d18d

- proposal_id: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-bre-638dc4d18d-sparse_signal`
- card_id: `dc-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto--043ff10e-sparse_signal`
- doctrine_family: `breakout_volatility_expansion`
- strategy_family: `breakout_expansion_confirmation`
- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "breakout_volatility_expansion", "regime": "high_vol", "strategy": "breakout_expansion_confirmation"}`
- variety_child_id: `{"activation_profile": "wider", "paper_gate": "balanced"}`
- variety_child_label: `activation_profile=wider, paper_gate=balanced`
- family_tested_child_count: `0`
- target_contract_family: `btc_up_down_15m`
- benchmark_priority: `medium`
- surprise_score: `0.69`
- duplicate_of_proposal_id: `n/a`
- source_names: `Recursive Flywheel, John Bollinger`
- lineage_ready: `True`
- status: `research_seeded_backtest_required`
- benchmark_profitability_score: `n/a`
- benchmark_paper_trade_readiness: `n/a`
- benchmark_next_step: `n/a`
- benchmark_trade_count: `n/a`
- benchmark_minimum_trade_count: `n/a`
- benchmark_trade_count_gate_pass: `n/a`
- benchmark_walk_forward_consistency: `n/a`
- benchmark_stress_resilience: `n/a`
- thesis: The breakout_volatility_expansion doctrine with breakout_open_interest_confirmation strategy produces too few trades in high_vol regime. Wider activation or a different feature combination is needed to capture more valid setups without destroying edge quality.

## Auto-generated: sparse_signal fix for auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compressio-8cb2a13b86

- proposal_id: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compressio-8cb2a13b86-sparse_signal`
- card_id: `dc-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto--0d853ea1-sparse_signal`
- doctrine_family: `breakout_volatility_expansion`
- strategy_family: `breakout_expansion_confirmation`
- variety_family_id: `{"contract": "btc_up_down_15m", "doctrine": "breakout_volatility_expansion", "regime": "high_vol", "strategy": "breakout_expansion_confirmation"}`
- variety_child_id: `{"activation_profile": "wider", "paper_gate": "balanced"}`
- variety_child_label: `activation_profile=wider, paper_gate=balanced`
- family_tested_child_count: `0`
- target_contract_family: `btc_up_down_15m`
- benchmark_priority: `medium`
- surprise_score: `0.69`
- duplicate_of_proposal_id: `auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-bre-638dc4d18d-sparse_signal`
- source_names: `Recursive Flywheel, John Bollinger`
- lineage_ready: `True`
- status: `duplicate_effective_mutation`
- benchmark_profitability_score: `n/a`
- benchmark_paper_trade_readiness: `n/a`
- benchmark_next_step: `n/a`
- benchmark_trade_count: `n/a`
- benchmark_minimum_trade_count: `n/a`
- benchmark_trade_count_gate_pass: `n/a`
- benchmark_walk_forward_consistency: `n/a`
- benchmark_stress_resilience: `n/a`
- thesis: The breakout_volatility_expansion doctrine with breakout_open_interest_confirmation strategy produces too few trades in high_vol regime. Wider activation or a different feature combination is needed to capture more valid setups without destroying edge quality.
