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

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-2b883eb130

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- market_regime: `trend`
- profitability_score: `0.54`
- sharpe_ratio: `0.4029`
- max_drawdown: `0.99`
- paper_trade_readiness: `0.359`
- contract_count: `5448`
- covered_contract_count: `5447`
- trade_count: `25`
- minimum_trade_count: `25`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.73`
- walk_forward_consistency: `0.4`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- trend: trades=`25` win_rate=`0.56` avg_return=`0.08`

### Walk-Forward Segments

- wf-1: trades=`2` profitability=`0.48` win_rate=`0.5` gate=`False`
- wf-2: trades=`6` profitability=`0.48` win_rate=`0.5` gate=`True`
- wf-3: trades=`5` profitability=`0.18` win_rate=`0.2` gate=`True`
- wf-4: trades=`8` profitability=`0.73` win_rate=`0.75` gate=`True`
- wf-5: trades=`4` profitability=`0.73` win_rate=`0.75` gate=`False`

### Stress Scenarios

- base: trades=`25` profitability=`0.54` avg_return=`0.08` gate=`True`
- elevated_fees: trades=`25` profitability=`0.52` avg_return=`0.04` gate=`True`
- fee_and_slippage: trades=`25` profitability=`0.5` avg_return=`-0.0` gate=`True`

## auto-wedge-guarded-drawdown_guard=high-reversal_confirmation=reclaim_close-volume_context_guard=thin_filter-w-1fccb6d1f0

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `wedge_exhaustion_reversal`
- market_regime: `range`
- profitability_score: `0.6189`
- sharpe_ratio: `1.4851`
- max_drawdown: `0.4417`
- paper_trade_readiness: `0.544`
- contract_count: `21792`
- covered_contract_count: `21791`
- trade_count: `36`
- minimum_trade_count: `160`
- trade_count_gate_pass: `False`
- holdout_profitability_score: `0.48`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `run_contradiction_probe`

### Regime Segments

- range: trades=`36` win_rate=`0.6389` avg_return=`0.2378`

### Walk-Forward Segments

- wf-1: trades=`9` profitability=`0.7578` win_rate=`0.7778` gate=`False`
- wf-2: trades=`5` profitability=`0.58` win_rate=`0.6` gate=`False`
- wf-3: trades=`9` profitability=`0.4244` win_rate=`0.4444` gate=`False`
- wf-4: trades=`7` profitability=`0.8371` win_rate=`0.8571` gate=`False`
- wf-5: trades=`6` profitability=`0.48` win_rate=`0.5` gate=`False`

### Stress Scenarios

- base: trades=`36` profitability=`0.6189` avg_return=`0.2378` gate=`False`
- elevated_fees: trades=`36` profitability=`0.5989` avg_return=`0.1978` gate=`False`
- fee_and_slippage: trades=`36` profitability=`0.5789` avg_return=`0.1578` gate=`False`

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

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compression-bre-8610bf593b

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
- wf-4: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`
- wf-5: trades=`0` profitability=`0.0` win_rate=`0.0` gate=`False`

### Stress Scenarios

- base: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- elevated_fees: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
- fee_and_slippage: trades=`0` profitability=`0.0` avg_return=`0.0` gate=`False`
