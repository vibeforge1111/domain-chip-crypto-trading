# Backtest Leaderboard

This page is the benchmark-facing surface for current doctrine and strategy combinations.

- benchmark_kind: `heavy_backtest`
- contract_family: `btc_up_down_15m`
- candidate_count: `61`

## evo-2215db84ffa5

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `range_reclaim_scalp`
- market_regime: `range`
- profitability_score: `0.7447`
- sharpe_ratio: `3.3638`
- max_drawdown: `0.1971`
- paper_trade_readiness: `0.9292`
- contract_count: `5472`
- covered_contract_count: `5471`
- trade_count: `34`
- minimum_trade_count: `34`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.7578`
- walk_forward_consistency: `1.0`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `hold_for_more_backtest_evidence`

### Regime Segments

- range: trades=`34` win_rate=`0.7647` avg_return=`0.4894`

### Walk-Forward Segments

- wf-1: trades=`9` profitability=`0.98` win_rate=`1.0` gate=`True`
- wf-2: trades=`14` profitability=`0.6943` win_rate=`0.7143` gate=`True`
- wf-3: trades=`11` profitability=`0.6164` win_rate=`0.6364` gate=`True`

### Stress Scenarios

- base: trades=`34` profitability=`0.7447` avg_return=`0.4894` gate=`True`
- elevated_fees: trades=`34` profitability=`0.7247` avg_return=`0.4494` gate=`True`
- fee_and_slippage: trades=`34` profitability=`0.7047` avg_return=`0.4094` gate=`True`

## evo-b9e50a49482a

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `bollinger_squeeze_breakout`
- market_regime: `range`
- profitability_score: `0.7009`
- sharpe_ratio: `2.9375`
- max_drawdown: `0.1898`
- paper_trade_readiness: `0.9063`
- contract_count: `5472`
- covered_contract_count: `5471`
- trade_count: `43`
- minimum_trade_count: `34`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.7073`
- walk_forward_consistency: `1.0`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `queue_for_paper_trade`

### Regime Segments

- range: trades=`43` win_rate=`0.7209` avg_return=`0.4019`

### Walk-Forward Segments

- wf-1: trades=`15` profitability=`0.78` win_rate=`0.8` gate=`True`
- wf-2: trades=`15` profitability=`0.7133` win_rate=`0.7333` gate=`True`
- wf-3: trades=`13` profitability=`0.5954` win_rate=`0.6154` gate=`True`

### Stress Scenarios

- base: trades=`43` profitability=`0.7009` avg_return=`0.4019` gate=`True`
- elevated_fees: trades=`43` profitability=`0.6809` avg_return=`0.3619` gate=`True`
- fee_and_slippage: trades=`43` profitability=`0.6609` avg_return=`0.3219` gate=`True`

## evo-39f616d7578a

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `contrarian_overextension_fade`
- market_regime: `range`
- profitability_score: `0.7009`
- sharpe_ratio: `2.9375`
- max_drawdown: `0.1898`
- paper_trade_readiness: `0.9063`
- contract_count: `5472`
- covered_contract_count: `5471`
- trade_count: `43`
- minimum_trade_count: `34`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.7073`
- walk_forward_consistency: `1.0`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `queue_for_paper_trade`

### Regime Segments

- range: trades=`43` win_rate=`0.7209` avg_return=`0.4019`

### Walk-Forward Segments

- wf-1: trades=`15` profitability=`0.78` win_rate=`0.8` gate=`True`
- wf-2: trades=`15` profitability=`0.7133` win_rate=`0.7333` gate=`True`
- wf-3: trades=`13` profitability=`0.5954` win_rate=`0.6154` gate=`True`

### Stress Scenarios

- base: trades=`43` profitability=`0.7009` avg_return=`0.4019` gate=`True`
- elevated_fees: trades=`43` profitability=`0.6809` avg_return=`0.3619` gate=`True`
- fee_and_slippage: trades=`43` profitability=`0.6609` avg_return=`0.3219` gate=`True`

## evo-0b50e57fc788

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `ema_crossover_fade`
- market_regime: `range`
- profitability_score: `0.7009`
- sharpe_ratio: `2.9375`
- max_drawdown: `0.1898`
- paper_trade_readiness: `0.9063`
- contract_count: `5472`
- covered_contract_count: `5471`
- trade_count: `43`
- minimum_trade_count: `34`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.7073`
- walk_forward_consistency: `1.0`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `queue_for_paper_trade`

### Regime Segments

- range: trades=`43` win_rate=`0.7209` avg_return=`0.4019`

### Walk-Forward Segments

- wf-1: trades=`15` profitability=`0.78` win_rate=`0.8` gate=`True`
- wf-2: trades=`15` profitability=`0.7133` win_rate=`0.7333` gate=`True`
- wf-3: trades=`13` profitability=`0.5954` win_rate=`0.6154` gate=`True`

### Stress Scenarios

- base: trades=`43` profitability=`0.7009` avg_return=`0.4019` gate=`True`
- elevated_fees: trades=`43` profitability=`0.6809` avg_return=`0.3619` gate=`True`
- fee_and_slippage: trades=`43` profitability=`0.6609` avg_return=`0.3219` gate=`True`

## evo-c2a6f9889332

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `ema_crossover_fade`
- market_regime: `range`
- profitability_score: `0.7009`
- sharpe_ratio: `2.9375`
- max_drawdown: `0.1898`
- paper_trade_readiness: `0.9063`
- contract_count: `5472`
- covered_contract_count: `5471`
- trade_count: `43`
- minimum_trade_count: `34`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.7073`
- walk_forward_consistency: `1.0`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `queue_for_paper_trade`

### Regime Segments

- range: trades=`43` win_rate=`0.7209` avg_return=`0.4019`

### Walk-Forward Segments

- wf-1: trades=`15` profitability=`0.78` win_rate=`0.8` gate=`True`
- wf-2: trades=`15` profitability=`0.7133` win_rate=`0.7333` gate=`True`
- wf-3: trades=`13` profitability=`0.5954` win_rate=`0.6154` gate=`True`

### Stress Scenarios

- base: trades=`43` profitability=`0.7009` avg_return=`0.4019` gate=`True`
- elevated_fees: trades=`43` profitability=`0.6809` avg_return=`0.3619` gate=`True`
- fee_and_slippage: trades=`43` profitability=`0.6609` avg_return=`0.3219` gate=`True`

## evo-631b6131cc0e

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `ema_crossover_fade`
- market_regime: `range`
- profitability_score: `0.7009`
- sharpe_ratio: `2.9375`
- max_drawdown: `0.1898`
- paper_trade_readiness: `0.9063`
- contract_count: `5472`
- covered_contract_count: `5471`
- trade_count: `43`
- minimum_trade_count: `34`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.7073`
- walk_forward_consistency: `1.0`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `queue_for_paper_trade`

### Regime Segments

- range: trades=`43` win_rate=`0.7209` avg_return=`0.4019`

### Walk-Forward Segments

- wf-1: trades=`15` profitability=`0.78` win_rate=`0.8` gate=`True`
- wf-2: trades=`15` profitability=`0.7133` win_rate=`0.7333` gate=`True`
- wf-3: trades=`13` profitability=`0.5954` win_rate=`0.6154` gate=`True`

### Stress Scenarios

- base: trades=`43` profitability=`0.7009` avg_return=`0.4019` gate=`True`
- elevated_fees: trades=`43` profitability=`0.6809` avg_return=`0.3619` gate=`True`
- fee_and_slippage: trades=`43` profitability=`0.6609` avg_return=`0.3219` gate=`True`

## evo-03404ed9a2fd

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `momentum_fade`
- market_regime: `range`
- profitability_score: `0.7009`
- sharpe_ratio: `2.9375`
- max_drawdown: `0.1898`
- paper_trade_readiness: `0.9063`
- contract_count: `5472`
- covered_contract_count: `5471`
- trade_count: `43`
- minimum_trade_count: `34`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.7073`
- walk_forward_consistency: `1.0`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `queue_for_paper_trade`

### Regime Segments

- range: trades=`43` win_rate=`0.7209` avg_return=`0.4019`

### Walk-Forward Segments

- wf-1: trades=`15` profitability=`0.78` win_rate=`0.8` gate=`True`
- wf-2: trades=`15` profitability=`0.7133` win_rate=`0.7333` gate=`True`
- wf-3: trades=`13` profitability=`0.5954` win_rate=`0.6154` gate=`True`

### Stress Scenarios

- base: trades=`43` profitability=`0.7009` avg_return=`0.4019` gate=`True`
- elevated_fees: trades=`43` profitability=`0.6809` avg_return=`0.3619` gate=`True`
- fee_and_slippage: trades=`43` profitability=`0.6609` avg_return=`0.3219` gate=`True`

## evo-db8c569c5718

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `multi_confirm_bounce`
- market_regime: `range`
- profitability_score: `0.7009`
- sharpe_ratio: `2.9375`
- max_drawdown: `0.1898`
- paper_trade_readiness: `0.9063`
- contract_count: `5472`
- covered_contract_count: `5471`
- trade_count: `43`
- minimum_trade_count: `34`
- trade_count_gate_pass: `True`
- holdout_profitability_score: `0.7073`
- walk_forward_consistency: `1.0`
- stress_resilience: `1.0`
- data_mode: `contract_window_backtest`
- recommended_next_step: `queue_for_paper_trade`

### Regime Segments

- range: trades=`43` win_rate=`0.7209` avg_return=`0.4019`

### Walk-Forward Segments

- wf-1: trades=`15` profitability=`0.78` win_rate=`0.8` gate=`True`
- wf-2: trades=`15` profitability=`0.7133` win_rate=`0.7333` gate=`True`
- wf-3: trades=`13` profitability=`0.5954` win_rate=`0.6154` gate=`True`

### Stress Scenarios

- base: trades=`43` profitability=`0.7009` avg_return=`0.4019` gate=`True`
- elevated_fees: trades=`43` profitability=`0.6809` avg_return=`0.3619` gate=`True`
- fee_and_slippage: trades=`43` profitability=`0.6609` avg_return=`0.3219` gate=`True`
