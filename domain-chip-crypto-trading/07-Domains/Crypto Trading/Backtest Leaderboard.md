# Backtest Leaderboard

This page is the benchmark-facing surface for current doctrine and strategy combinations.

- benchmark_kind: `heavy_backtest`
- contract_family: `btc_up_down_15m`
- candidate_count: `9`

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-5d7170b7b6

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.4961`
- sharpe_ratio: `-0.0431`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.1653`
- contract_count: `5448`
- covered_contract_count: `5447`
- trade_count: `31`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.48`
- walk_forward_consistency: `0.6667`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- trend: trades=`31` win_rate=`0.5161` avg_return=`-0.0077`

### Walk-Forward Segments

- wf-1: trades=`8` profitability=`0.605` win_rate=`0.625` gate=`True`
- wf-2: trades=`9` profitability=`0.4244` win_rate=`0.4444` gate=`True`
- wf-3: trades=`14` profitability=`0.48` win_rate=`0.5` gate=`True`

### Stress Scenarios

- base: trades=`31` profitability=`0.4961` avg_return=`-0.0077` gate=`True`
- elevated_fees: trades=`31` profitability=`0.4761` avg_return=`-0.0477` gate=`True`
- fee_and_slippage: trades=`31` profitability=`0.4561` avg_return=`-0.0877` gate=`True`

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-8f1ca8f191

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.4592`
- sharpe_ratio: `-0.5663`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.08`
- contract_count: `5448`
- covered_contract_count: `5447`
- trade_count: `48`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.58`
- walk_forward_consistency: `0.6667`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- trend: trades=`48` win_rate=`0.4792` avg_return=`-0.0817`

### Walk-Forward Segments

- wf-1: trades=`13` profitability=`0.5185` win_rate=`0.5385` gate=`True`
- wf-2: trades=`13` profitability=`0.2877` win_rate=`0.3077` gate=`True`
- wf-3: trades=`22` profitability=`0.5255` win_rate=`0.5455` gate=`True`

### Stress Scenarios

- base: trades=`48` profitability=`0.4592` avg_return=`-0.0817` gate=`True`
- elevated_fees: trades=`48` profitability=`0.4392` avg_return=`-0.1217` gate=`True`
- fee_and_slippage: trades=`48` profitability=`0.4192` avg_return=`-0.1617` gate=`True`

## btc-15m-volatility-compression-breakout-psychology_no_chase

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `breakout_open_interest_confirmation`
- market_regime: `high_vol`
- profitability_score: `0.3133`
- sharpe_ratio: `-0.6859`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.0`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `3`
- minimum_trade_count: `25`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.3133`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- high_vol: trades=`3` win_rate=`0.3333` avg_return=`-0.3733`

### Walk-Forward Segments

- wf-1: trades=`1` profitability=`0.98` win_rate=`1.0` gate=`False`
- wf-2: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-3: trades=`2` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`3` profitability=`0.3133` avg_return=`-0.3733` gate=`False`
- elevated_fees: trades=`3` profitability=`0.2933` avg_return=`-0.4133` gate=`False`
- fee_and_slippage: trades=`3` profitability=`0.2733` avg_return=`-0.4533` gate=`False`

## auto-auto-auto-auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-late_sample_guard=on-sparse-43bb8ee0ac

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

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compressio-17198cff45

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `breakout_open_interest_confirmation`
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

## auto-auto-baseline-sparse_signal-probe-sparse_signal-sparse_signal-probe-sparse_signal-variety-late-sample-gu-8d2488e327

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

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-variety-late-sample-guard-plus-session-filter

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
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
