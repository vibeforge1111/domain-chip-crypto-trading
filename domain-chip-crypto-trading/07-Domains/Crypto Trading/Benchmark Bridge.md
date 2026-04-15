# Benchmark Bridge

Backtesting is the benchmark lane for this chip.

This page plays the same role as the startup chip's promotion bridge page, but for trading combinations.

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-8f1ca8f191

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.5`
- sharpe_ratio: `-0.0`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.1452`
- contract_count: `5424`
- covered_contract_count: `5423`
- trade_count: `25`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.48`
- walk_forward_consistency: `0.2`
- stress_resilience: `0.3333`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`
- promotion_candidate_kind: `benchmark_grounded_boundary`
- eligibility_status: `eligible_for_boundary_promotion`
- primary_mechanism: Backtested on 25 active BTC 1h contract decisions across 5423 covered windows. Fallback used because requested timeframe `4h` unavailable.
- primary_boundary: Insufficient heavy-backtest breadth or unstable returns still block promotion.

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.4628`
- sharpe_ratio: `-0.4013`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.024`
- contract_count: `5424`
- covered_contract_count: `5423`
- trade_count: `29`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.3133`
- walk_forward_consistency: `0.2`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`
- promotion_candidate_kind: `benchmark_grounded_boundary`
- eligibility_status: `eligible_for_boundary_promotion`
- primary_mechanism: Backtested on 29 active BTC 1h contract decisions across 5423 covered windows. Fallback used because requested timeframe `4h` unavailable.
- primary_boundary: Insufficient heavy-backtest breadth or unstable returns still block promotion.

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-session_profile=squeeze_release_window

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
- market_regime: `high_vol`
- profitability_score: `0.4497`
- sharpe_ratio: `-0.8188`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.048`
- contract_count: `21696`
- covered_contract_count: `21695`
- trade_count: `66`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.48`
- walk_forward_consistency: `0.4`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`
- promotion_candidate_kind: `benchmark_grounded_boundary`
- eligibility_status: `eligible_for_boundary_promotion`
- primary_mechanism: Backtested on 66 active BTC 15m contract decisions across 21695 covered windows.
- primary_boundary: Insufficient heavy-backtest breadth or unstable returns still block promotion.

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
- market_regime: `high_vol`
- profitability_score: `0.4484`
- sharpe_ratio: `-1.301`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.048`
- contract_count: `21696`
- covered_contract_count: `21695`
- trade_count: `158`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.4467`
- walk_forward_consistency: `0.4`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`
- promotion_candidate_kind: `benchmark_grounded_boundary`
- eligibility_status: `eligible_for_boundary_promotion`
- primary_mechanism: Backtested on 158 active BTC 15m contract decisions across 21695 covered windows.
- primary_boundary: Insufficient heavy-backtest breadth or unstable returns still block promotion.

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guard=thin_filter

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.4086`
- sharpe_ratio: `-1.093`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.024`
- contract_count: `5424`
- covered_contract_count: `5423`
- trade_count: `35`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.38`
- walk_forward_consistency: `0.2`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`
- promotion_candidate_kind: `benchmark_grounded_boundary`
- eligibility_status: `eligible_for_boundary_promotion`
- primary_mechanism: Backtested on 35 active BTC 1h contract decisions across 5423 covered windows. Fallback used because requested timeframe `4h` unavailable.
- primary_boundary: Insufficient heavy-backtest breadth or unstable returns still block promotion.

## auto-wedge-guarded-drawdown_guard=high-reversal_confirmation=reclaim_close-volume_context_guard=strict_participation-wick_profile=rejection_confirm

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `wedge_exhaustion_reversal`
- market_regime: `range`
- profitability_score: `0.6127`
- sharpe_ratio: `1.6358`
- max_drawdown: `0.4379`
- paper_trade_readiness: `0.6232`
- contract_count: `21696`
- covered_contract_count: `21695`
- trade_count: `49`
- minimum_trade_count: `161`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.48`
- walk_forward_consistency: `0.0`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`
- promotion_candidate_kind: `benchmark_grounded_boundary`
- eligibility_status: `eligible_for_boundary_promotion`
- primary_mechanism: Backtested on 49 active BTC 15m contract decisions across 21695 covered windows.
- primary_boundary: Insufficient heavy-backtest breadth or unstable returns still block promotion.

## auto-wedge-guarded-drawdown_guard=high-reversal_confirmation=reclaim_close-volume_context_guard=thin_filter-wick_profile=rejection_confirm

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `wedge_exhaustion_reversal`
- market_regime: `range`
- profitability_score: `0.6026`
- sharpe_ratio: `1.5416`
- max_drawdown: `0.5263`
- paper_trade_readiness: `0.5887`
- contract_count: `21696`
- covered_contract_count: `21695`
- trade_count: `53`
- minimum_trade_count: `161`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.48`
- walk_forward_consistency: `0.0`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`
- promotion_candidate_kind: `benchmark_grounded_boundary`
- eligibility_status: `eligible_for_boundary_promotion`
- primary_mechanism: Backtested on 53 active BTC 15m contract decisions across 21695 covered windows.
- primary_boundary: Insufficient heavy-backtest breadth or unstable returns still block promotion.

## auto-wedge-guarded-reversal_confirmation=reclaim_close-volume_context_guard=thin_filter-wick_profile=rejection_confirm

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `wedge_exhaustion_reversal`
- market_regime: `range`
- profitability_score: `0.5356`
- sharpe_ratio: `0.7436`
- max_drawdown: `0.7961`
- paper_trade_readiness: `0.3509`
- contract_count: `21696`
- covered_contract_count: `21695`
- trade_count: `108`
- minimum_trade_count: `161`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.4244`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.6667`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`
- promotion_candidate_kind: `benchmark_grounded_boundary`
- eligibility_status: `eligible_for_boundary_promotion`
- primary_mechanism: Backtested on 108 active BTC 15m contract decisions across 21695 covered windows.
- primary_boundary: Insufficient heavy-backtest breadth or unstable returns still block promotion.

## Recommended Next-Step Ladder

- `store_as_benchmark_evidence`
- `promote_as_doctrine_candidate`
- `promote_as_boundary_candidate`
- `queue_for_paper_trade`
