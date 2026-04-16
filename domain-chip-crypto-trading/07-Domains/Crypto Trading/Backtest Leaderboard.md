# Backtest Leaderboard

This page is the benchmark-facing surface for current doctrine and strategy combinations.

- benchmark_kind: `heavy_backtest`
- contract_family: `btc_up_down_15m`
- candidate_count: `9`

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-variety-session-stability-filter

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
- market_regime: `high_vol`
- profitability_score: `0.58`
- sharpe_ratio: `0.8165`
- max_drawdown: `0.7143`
- paper_trade_readiness: `0.5993`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `25`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.6467`
- walk_forward_consistency: `1.0`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `hold_for_more_backtest_evidence`

### Regime Segments

- high_vol: trades=`25` win_rate=`0.6` avg_return=`0.16`

### Walk-Forward Segments

- wf-1: trades=`4` profitability=`0.73` win_rate=`0.75` gate=`True`
- wf-2: trades=`4` profitability=`0.73` win_rate=`0.75` gate=`True`
- wf-3: trades=`17` profitability=`0.5094` win_rate=`0.5294` gate=`True`

### Stress Scenarios

- base: trades=`25` profitability=`0.58` avg_return=`0.16` gate=`True`
- elevated_fees: trades=`25` profitability=`0.56` avg_return=`0.12` gate=`True`
- fee_and_slippage: trades=`25` profitability=`0.54` avg_return=`0.08` gate=`True`

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-c969a92d4e

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.4648`
- sharpe_ratio: `-0.404`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.04`
- contract_count: `5448`
- covered_contract_count: `5447`
- trade_count: `33`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.3133`
- walk_forward_consistency: `0.3333`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- trend: trades=`33` win_rate=`0.4848` avg_return=`-0.0703`

### Walk-Forward Segments

- wf-1: trades=`8` profitability=`0.605` win_rate=`0.625` gate=`True`
- wf-2: trades=`10` profitability=`0.38` win_rate=`0.4` gate=`True`
- wf-3: trades=`15` profitability=`0.4467` win_rate=`0.4667` gate=`True`

### Stress Scenarios

- base: trades=`33` profitability=`0.4648` avg_return=`-0.0703` gate=`True`
- elevated_fees: trades=`33` profitability=`0.4448` avg_return=`-0.1103` gate=`True`
- fee_and_slippage: trades=`33` profitability=`0.4248` avg_return=`-0.1503` gate=`True`

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=stri-a6c463789f

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.4316`
- sharpe_ratio: `-0.7651`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.04`
- contract_count: `5448`
- covered_contract_count: `5447`
- trade_count: `31`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.3133`
- walk_forward_consistency: `0.3333`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- trend: trades=`31` win_rate=`0.4516` avg_return=`-0.1368`

### Walk-Forward Segments

- wf-1: trades=`7` profitability=`0.5514` win_rate=`0.5714` gate=`True`
- wf-2: trades=`10` profitability=`0.38` win_rate=`0.4` gate=`True`
- wf-3: trades=`14` profitability=`0.4086` win_rate=`0.4286` gate=`True`

### Stress Scenarios

- base: trades=`31` profitability=`0.4316` avg_return=`-0.1368` gate=`True`
- elevated_fees: trades=`31` profitability=`0.4116` avg_return=`-0.1768` gate=`True`
- fee_and_slippage: trades=`31` profitability=`0.3916` avg_return=`-0.2168` gate=`True`

## auto-auto-auto-auto-auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-late_sample_guard=on-s-24c83905d3

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
- market_regime: `high_vol`
- profitability_score: `0.18`
- sharpe_ratio: `-1.7889`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.0`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `5`
- minimum_trade_count: `25`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.0`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- high_vol: trades=`5` win_rate=`0.2` avg_return=`-0.64`

### Walk-Forward Segments

- wf-1: trades=`1` profitability=`0.98` win_rate=`1.0` gate=`False`
- wf-2: trades=`1` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-3: trades=`3` profitability=`0.0` win_rate=`0.0` gate=`True`

### Stress Scenarios

- base: trades=`5` profitability=`0.18` avg_return=`-0.64` gate=`False`
- elevated_fees: trades=`5` profitability=`0.16` avg_return=`-0.68` gate=`False`
- fee_and_slippage: trades=`5` profitability=`0.14` avg_return=`-0.72` gate=`False`

## baseline

- doctrine_id: `n/a`
- strategy_id: `n/a`
- market_regime: `n/a`
- profitability_score: `0.0`
- sharpe_ratio: `0.0`
- max_drawdown: `0.0`
- paper_trade_readiness: `0.17`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `0`
- minimum_trade_count: `435`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.0`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Walk-Forward Segments

- wf-1: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-2: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-3: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`

## auto-auto-baseline-sparse_signal-probe-sparse_signal-sparse_signal-probe-sparse_signal-variety-late-sample-gu-18a3cf4db3

- doctrine_id: `None`
- strategy_id: `None`
- market_regime: `None`
- profitability_score: `0.0`
- sharpe_ratio: `0.0`
- max_drawdown: `0.0`
- paper_trade_readiness: `0.17`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `0`
- minimum_trade_count: `435`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.0`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Walk-Forward Segments

- wf-1: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-2: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-3: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`

## btc-15m-volatility-compression-breakout-psychology_no_chase-variety-late-sample-guard-plus-session-filter

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `breakout_open_interest_confirmation`
- market_regime: `high_vol`
- profitability_score: `0.0`
- sharpe_ratio: `0.0`
- max_drawdown: `0.0`
- paper_trade_readiness: `0.17`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `0`
- minimum_trade_count: `25`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.0`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Walk-Forward Segments

- wf-1: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-2: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-3: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compressio-f3947c981e

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `breakout_open_interest_confirmation`
- market_regime: `high_vol`
- profitability_score: `0.0`
- sharpe_ratio: `0.0`
- max_drawdown: `0.0`
- paper_trade_readiness: `0.17`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `0`
- minimum_trade_count: `25`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.0`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Walk-Forward Segments

- wf-1: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-2: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-3: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
