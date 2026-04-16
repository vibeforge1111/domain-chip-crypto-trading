# Backtest Leaderboard

This page is the benchmark-facing surface for current doctrine and strategy combinations.

- benchmark_kind: `heavy_backtest`
- contract_family: `btc_up_down_15m`
- candidate_count: `9`

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-session_profile=squeeze_release_window-probe--821460728b

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
- market_regime: `high_vol`
- profitability_score: `0.4497`
- sharpe_ratio: `-0.8188`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.048`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `66`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.5356`
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

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-da0da700c6

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.5`
- sharpe_ratio: `-0.0`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.1118`
- contract_count: `5448`
- covered_contract_count: `5447`
- trade_count: `25`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.3133`
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
- wf-4: trades=`9` profitability=`0.7578` win_rate=`0.7778` gate=`True`
- wf-5: trades=`3` profitability=`0.3133` win_rate=`0.3333` gate=`False`

### Stress Scenarios

- base: trades=`25` profitability=`0.5` avg_return=`-0.0` gate=`True`
- elevated_fees: trades=`25` profitability=`0.48` avg_return=`-0.04` gate=`True`
- fee_and_slippage: trades=`25` profitability=`0.46` avg_return=`-0.08` gate=`True`

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-bre-cc1112fef9

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `breakout_open_interest_confirmation`
- market_regime: `high_vol`
- profitability_score: `0.2903`
- sharpe_ratio: `-2.4404`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.0`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `29`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.23`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- high_vol: trades=`29` win_rate=`0.3103` avg_return=`-0.4193`

### Walk-Forward Segments

- wf-1: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-2: trades=`3` profitability=`0.6467` win_rate=`0.6667` gate=`False`
- wf-3: trades=`4` profitability=`0.23` win_rate=`0.25` gate=`False`
- wf-4: trades=`18` profitability=`0.2578` win_rate=`0.2778` gate=`True`
- wf-5: trades=`4` profitability=`0.23` win_rate=`0.25` gate=`False`

### Stress Scenarios

- base: trades=`29` profitability=`0.2903` avg_return=`-0.4193` gate=`True`
- elevated_fees: trades=`29` profitability=`0.2703` avg_return=`-0.4593` gate=`True`
- fee_and_slippage: trades=`29` profitability=`0.2503` avg_return=`-0.4993` gate=`True`

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

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-probe-holdout_decay

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

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-breakout-dc981423b5

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

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-regime-shift-no-trade-filter-psychol-97c83571b5

- doctrine_id: `risk_first_asymmetric_capture`
- strategy_id: `funding_mean_revert`
- market_regime: `event_driven`
- profitability_score: `0.0`
- sharpe_ratio: `0.0`
- max_drawdown: `0.0`
- paper_trade_readiness: `0.17`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `0`
- minimum_trade_count: `59`
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
