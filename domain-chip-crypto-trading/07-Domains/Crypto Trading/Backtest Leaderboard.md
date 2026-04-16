# Backtest Leaderboard

This page is the benchmark-facing surface for current doctrine and strategy combinations.

- benchmark_kind: `heavy_backtest`
- contract_family: `btc_up_down_15m`
- candidate_count: `9`

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-8400e6c02b

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.5063`
- sharpe_ratio: `0.0551`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.1479`
- contract_count: `5448`
- covered_contract_count: `5447`
- trade_count: `19`
- minimum_trade_count: `25`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.3133`
- walk_forward_consistency: `0.4`
- stress_resilience: `0.3333`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- trend: trades=`19` win_rate=`0.5263` avg_return=`0.0126`

### Walk-Forward Segments

- wf-1: trades=`2` profitability=`0.48` win_rate=`0.5` gate=`False`
- wf-2: trades=`5` profitability=`0.58` win_rate=`0.6` gate=`True`
- wf-3: trades=`3` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-4: trades=`6` profitability=`0.8133` win_rate=`0.8333` gate=`True`
- wf-5: trades=`3` profitability=`0.3133` win_rate=`0.3333` gate=`False`

### Stress Scenarios

- base: trades=`19` profitability=`0.5063` avg_return=`0.0126` gate=`False`
- elevated_fees: trades=`19` profitability=`0.4863` avg_return=`-0.0274` gate=`False`
- fee_and_slippage: trades=`19` profitability=`0.4663` avg_return=`-0.0674` gate=`False`

## auto-trend-volume-filtered-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter-probe-holdout_decay

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.5017`
- sharpe_ratio: `0.0167`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.1154`
- contract_count: `5448`
- covered_contract_count: `5447`
- trade_count: `23`
- minimum_trade_count: `25`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.3133`
- walk_forward_consistency: `0.2`
- stress_resilience: `0.3333`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- trend: trades=`23` win_rate=`0.5217` avg_return=`0.0035`

### Walk-Forward Segments

- wf-1: trades=`2` profitability=`0.48` win_rate=`0.5` gate=`False`
- wf-2: trades=`7` profitability=`0.4086` win_rate=`0.4286` gate=`True`
- wf-3: trades=`4` profitability=`0.23` win_rate=`0.25` gate=`False`
- wf-4: trades=`7` profitability=`0.8371` win_rate=`0.8571` gate=`True`
- wf-5: trades=`3` profitability=`0.3133` win_rate=`0.3333` gate=`False`

### Stress Scenarios

- base: trades=`23` profitability=`0.5017` avg_return=`0.0035` gate=`False`
- elevated_fees: trades=`23` profitability=`0.4817` avg_return=`-0.0365` gate=`False`
- fee_and_slippage: trades=`23` profitability=`0.4617` avg_return=`-0.0765` gate=`False`

## baseline

- doctrine_id: `n/a`
- strategy_id: `n/a`
- market_regime: `n/a`
- profitability_score: `0.0`
- sharpe_ratio: `0.0`
- max_drawdown: `0.0`
- paper_trade_readiness: `0.17`
- contract_count: `21696`
- covered_contract_count: `21695`
- trade_count: `0`
- minimum_trade_count: `433`
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
- wf-4: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`

## auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-late_sample_guard=on-probe-sparse_signal

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
- wf-4: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`

## auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-late_sample_guard=on-session_profile=squee-1183d97024

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
- wf-4: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-breakout-de03826d09

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
- wf-4: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`

## btc-15m-volatility-compression-breakout-psychology_no_chase-variety-session-stability-filter-variety-executio-747ed0b865

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
- wf-4: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-momentum-breakout-structure-psy-dc69343ca7

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `breakout_open_interest_confirmation`
- market_regime: `trend`
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
- wf-4: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
