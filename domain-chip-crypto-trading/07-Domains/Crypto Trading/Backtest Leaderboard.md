# Backtest Leaderboard

This page is the benchmark-facing surface for current doctrine and strategy combinations.

- benchmark_kind: `heavy_backtest`
- contract_family: `btc_up_down_15m`
- candidate_count: `32`

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
- market_regime: `high_vol`
- profitability_score: `0.4513`
- sharpe_ratio: `-1.2215`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.048`
- contract_count: `20448`
- covered_contract_count: `20447`
- trade_count: `157`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.3967`
- walk_forward_consistency: `0.4`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- high_vol: trades=`157` win_rate=`0.4713` avg_return=`-0.0973`

### Walk-Forward Segments

- wf-1: trades=`5` profitability=`0.18` win_rate=`0.2` gate=`True`
- wf-2: trades=`27` profitability=`0.5726` win_rate=`0.5926` gate=`True`
- wf-3: trades=`21` profitability=`0.5514` win_rate=`0.5714` gate=`True`
- wf-4: trades=`80` profitability=`0.4175` win_rate=`0.4375` gate=`True`
- wf-5: trades=`24` profitability=`0.3967` win_rate=`0.4167` gate=`True`

### Stress Scenarios

- base: trades=`157` profitability=`0.4513` avg_return=`-0.0973` gate=`True`
- elevated_fees: trades=`157` profitability=`0.4313` avg_return=`-0.1373` gate=`True`
- fee_and_slippage: trades=`157` profitability=`0.4113` avg_return=`-0.1773` gate=`True`

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-session_profile=squeeze_release_window

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
- market_regime: `high_vol`
- profitability_score: `0.4497`
- sharpe_ratio: `-0.8188`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.048`
- contract_count: `20448`
- covered_contract_count: `20447`
- trade_count: `66`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.4086`
- walk_forward_consistency: `0.4`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- high_vol: trades=`66` win_rate=`0.4697` avg_return=`-0.1006`

### Walk-Forward Segments

- wf-1: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-2: trades=`13` profitability=`0.6723` win_rate=`0.6923` gate=`True`
- wf-3: trades=`13` profitability=`0.5185` win_rate=`0.5385` gate=`True`
- wf-4: trades=`26` profitability=`0.3262` win_rate=`0.3462` gate=`True`
- wf-5: trades=`14` profitability=`0.4086` win_rate=`0.4286` gate=`True`

### Stress Scenarios

- base: trades=`66` profitability=`0.4497` avg_return=`-0.1006` gate=`True`
- elevated_fees: trades=`66` profitability=`0.4297` avg_return=`-0.1406` gate=`True`
- fee_and_slippage: trades=`66` profitability=`0.4097` avg_return=`-0.1806` gate=`True`

## auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-session_profile=squeeze_release_window

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

### Regime Segments

- high_vol: trades=`66` win_rate=`0.4697` avg_return=`-0.1006`

### Walk-Forward Segments

- wf-1: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-2: trades=`13` profitability=`0.6723` win_rate=`0.6923` gate=`True`
- wf-3: trades=`13` profitability=`0.5185` win_rate=`0.5385` gate=`True`
- wf-4: trades=`30` profitability=`0.3133` win_rate=`0.3333` gate=`True`
- wf-5: trades=`10` profitability=`0.48` win_rate=`0.5` gate=`True`

### Stress Scenarios

- base: trades=`66` profitability=`0.4497` avg_return=`-0.1006` gate=`True`
- elevated_fees: trades=`66` profitability=`0.4297` avg_return=`-0.1406` gate=`True`
- fee_and_slippage: trades=`66` profitability=`0.4097` avg_return=`-0.1806` gate=`True`

## auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze

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

### Regime Segments

- high_vol: trades=`158` win_rate=`0.4684` avg_return=`-0.1033`

### Walk-Forward Segments

- wf-1: trades=`6` profitability=`0.1467` win_rate=`0.1667` gate=`True`
- wf-2: trades=`26` profitability=`0.5954` win_rate=`0.6154` gate=`True`
- wf-3: trades=`21` profitability=`0.5514` win_rate=`0.5714` gate=`True`
- wf-4: trades=`90` profitability=`0.4022` win_rate=`0.4222` gate=`True`
- wf-5: trades=`15` profitability=`0.4467` win_rate=`0.4667` gate=`True`

### Stress Scenarios

- base: trades=`158` profitability=`0.4484` avg_return=`-0.1033` gate=`True`
- elevated_fees: trades=`158` profitability=`0.4284` avg_return=`-0.1433` gate=`True`
- fee_and_slippage: trades=`158` profitability=`0.4084` avg_return=`-0.1833` gate=`True`

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

### Regime Segments

- trend: trades=`25` win_rate=`0.52` avg_return=`-0.0`

### Walk-Forward Segments

- wf-1: trades=`2` profitability=`0.48` win_rate=`0.5` gate=`False`
- wf-2: trades=`7` profitability=`0.4086` win_rate=`0.4286` gate=`True`
- wf-3: trades=`4` profitability=`0.23` win_rate=`0.25` gate=`False`
- wf-4: trades=`8` profitability=`0.73` win_rate=`0.75` gate=`True`
- wf-5: trades=`4` profitability=`0.48` win_rate=`0.5` gate=`False`

### Stress Scenarios

- base: trades=`25` profitability=`0.5` avg_return=`-0.0` gate=`True`
- elevated_fees: trades=`25` profitability=`0.48` avg_return=`-0.04` gate=`True`
- fee_and_slippage: trades=`25` profitability=`0.46` avg_return=`-0.08` gate=`True`

## auto-trend-volume-filtered-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter

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

### Regime Segments

- trend: trades=`29` win_rate=`0.4828` avg_return=`-0.0745`

### Walk-Forward Segments

- wf-1: trades=`2` profitability=`0.48` win_rate=`0.5` gate=`False`
- wf-2: trades=`8` profitability=`0.355` win_rate=`0.375` gate=`True`
- wf-3: trades=`5` profitability=`0.38` win_rate=`0.4` gate=`True`
- wf-4: trades=`8` profitability=`0.73` win_rate=`0.75` gate=`True`
- wf-5: trades=`6` profitability=`0.3133` win_rate=`0.3333` gate=`True`

### Stress Scenarios

- base: trades=`29` profitability=`0.4628` avg_return=`-0.0745` gate=`True`
- elevated_fees: trades=`29` profitability=`0.4428` avg_return=`-0.1145` gate=`True`
- fee_and_slippage: trades=`29` profitability=`0.4228` avg_return=`-0.1545` gate=`True`

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.4615`
- sharpe_ratio: `-0.4006`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.024`
- contract_count: `5112`
- covered_contract_count: `5111`
- trade_count: `27`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.4086`
- walk_forward_consistency: `0.2`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- trend: trades=`27` win_rate=`0.4815` avg_return=`-0.077`

### Walk-Forward Segments

- wf-1: trades=`2` profitability=`0.48` win_rate=`0.5` gate=`False`
- wf-2: trades=`7` profitability=`0.4086` win_rate=`0.4286` gate=`True`
- wf-3: trades=`6` profitability=`0.3133` win_rate=`0.3333` gate=`True`
- wf-4: trades=`5` profitability=`0.78` win_rate=`0.8` gate=`True`
- wf-5: trades=`7` profitability=`0.4086` win_rate=`0.4286` gate=`True`

### Stress Scenarios

- base: trades=`27` profitability=`0.4615` avg_return=`-0.077` gate=`True`
- elevated_fees: trades=`27` profitability=`0.4415` avg_return=`-0.117` gate=`True`
- fee_and_slippage: trades=`27` profitability=`0.4215` avg_return=`-0.157` gate=`True`

## auto-trend-volume-filtered-no_trade_window=avoid_post_open_drift-volume_context_guard=thin_filter

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

### Regime Segments

- trend: trades=`35` win_rate=`0.4286` avg_return=`-0.1829`

### Walk-Forward Segments

- wf-1: trades=`2` profitability=`0.48` win_rate=`0.5` gate=`False`
- wf-2: trades=`12` profitability=`0.23` win_rate=`0.25` gate=`True`
- wf-3: trades=`6` profitability=`0.3133` win_rate=`0.3333` gate=`True`
- wf-4: trades=`10` profitability=`0.68` win_rate=`0.7` gate=`True`
- wf-5: trades=`5` profitability=`0.38` win_rate=`0.4` gate=`True`

### Stress Scenarios

- base: trades=`35` profitability=`0.4086` avg_return=`-0.1829` gate=`True`
- elevated_fees: trades=`35` profitability=`0.3886` avg_return=`-0.2229` gate=`True`
- fee_and_slippage: trades=`35` profitability=`0.3686` avg_return=`-0.2629` gate=`True`
