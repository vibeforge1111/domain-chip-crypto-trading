# Backtest Leaderboard

This page is the benchmark-facing surface for current doctrine and strategy combinations.

- benchmark_kind: `heavy_backtest`
- contract_family: `btc_up_down_15m`
- candidate_count: `9`

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=stri-6b92847572

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.4467`
- sharpe_ratio: `-0.7171`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.072`
- contract_count: `5448`
- covered_contract_count: `5447`
- trade_count: `45`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.58`
- walk_forward_consistency: `0.6`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- trend: trades=`45` win_rate=`0.4667` avg_return=`-0.1067`

### Walk-Forward Segments

- wf-1: trades=`2` profitability=`0.48` win_rate=`0.5` gate=`False`
- wf-2: trades=`12` profitability=`0.48` win_rate=`0.5` gate=`True`
- wf-3: trades=`8` profitability=`0.23` win_rate=`0.25` gate=`True`
- wf-4: trades=`18` profitability=`0.48` win_rate=`0.5` gate=`True`
- wf-5: trades=`5` profitability=`0.58` win_rate=`0.6` gate=`True`

### Stress Scenarios

- base: trades=`45` profitability=`0.4467` avg_return=`-0.1067` gate=`True`
- elevated_fees: trades=`45` profitability=`0.4267` avg_return=`-0.1467` gate=`True`
- fee_and_slippage: trades=`45` profitability=`0.4067` avg_return=`-0.1867` gate=`True`

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-variety-session-stability-filter

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
- market_regime: `high_vol`
- profitability_score: `0.58`
- sharpe_ratio: `0.8165`
- max_drawdown: `0.7143`
- paper_trade_readiness: `0.5273`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `25`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.6467`
- walk_forward_consistency: `0.4`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `hold_for_more_backtest_evidence`

### Regime Segments

- high_vol: trades=`25` win_rate=`0.6` avg_return=`0.16`

### Walk-Forward Segments

- wf-1: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-2: trades=`6` profitability=`0.8133` win_rate=`0.8333` gate=`True`
- wf-3: trades=`2` profitability=`0.48` win_rate=`0.5` gate=`False`
- wf-4: trades=`14` profitability=`0.48` win_rate=`0.5` gate=`True`
- wf-5: trades=`3` profitability=`0.6467` win_rate=`0.6667` gate=`False`

### Stress Scenarios

- base: trades=`25` profitability=`0.58` avg_return=`0.16` gate=`True`
- elevated_fees: trades=`25` profitability=`0.56` avg_return=`0.12` gate=`True`
- fee_and_slippage: trades=`25` profitability=`0.54` avg_return=`0.08` gate=`True`

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=thin-491eee90bf

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.48`
- sharpe_ratio: `-0.2263`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.0947`
- contract_count: `5448`
- covered_contract_count: `5447`
- trade_count: `32`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.48`
- walk_forward_consistency: `0.4`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- trend: trades=`32` win_rate=`0.5` avg_return=`-0.04`

### Walk-Forward Segments

- wf-1: trades=`2` profitability=`0.48` win_rate=`0.5` gate=`False`
- wf-2: trades=`8` profitability=`0.355` win_rate=`0.375` gate=`True`
- wf-3: trades=`6` profitability=`0.3133` win_rate=`0.3333` gate=`True`
- wf-4: trades=`10` profitability=`0.68` win_rate=`0.7` gate=`True`
- wf-5: trades=`6` profitability=`0.48` win_rate=`0.5` gate=`True`

### Stress Scenarios

- base: trades=`32` profitability=`0.48` avg_return=`-0.04` gate=`True`
- elevated_fees: trades=`32` profitability=`0.46` avg_return=`-0.08` gate=`True`
- fee_and_slippage: trades=`32` profitability=`0.44` avg_return=`-0.12` gate=`True`

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

- wf-1: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-2: trades=`1` profitability=`0.98` win_rate=`1.0` gate=`False`
- wf-3: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-4: trades=`2` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`3` profitability=`0.3133` avg_return=`-0.3733` gate=`False`
- elevated_fees: trades=`3` profitability=`0.2933` avg_return=`-0.4133` gate=`False`
- fee_and_slippage: trades=`3` profitability=`0.2733` avg_return=`-0.4533` gate=`False`

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

- wf-1: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-2: trades=`1` profitability=`0.98` win_rate=`1.0` gate=`False`
- wf-3: trades=`1` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-4: trades=`2` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`1` profitability=`0.0` win_rate=`0.0` gate=`False`

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
- wf-4: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`

## auto-auto-baseline-sparse_signal-probe-sparse_signal-sparse_signal-probe-sparse_signal-variety-late-sample-gu-2bc78501ec

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
- wf-4: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

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
- wf-4: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
