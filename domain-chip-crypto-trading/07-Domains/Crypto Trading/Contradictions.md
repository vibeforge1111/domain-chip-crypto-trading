# Contradictions

This page is the trading equivalent of a `why it lost` surface.

Track failure shapes here when a combination looks exciting but should not be promoted.

## evo-4c38dbff5283

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `event_fade`
- priority: `0.99`
- holdout_profitability_score: `0.0`
- walk_forward_consistency: `0.3333`
- stress_resilience: `0.0`
- max_drawdown: `0.7`
- contradiction: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Failure Modes

- sparse_signal: Trade count stays below the minimum gate, so the candidate may be a local curve rather than a repeatable contract edge.
- holdout_decay: The final holdout slice drops below break-even profitability after fees.
- segment_instability: Walk-forward consistency is too low across chronological splits.
- execution_fragility: Edge does not survive elevated fees and slippage cleanly.
- drawdown_excess: Drawdown remains above the promotion boundary even when trade count is adequate.

### Weakest Segments

- wf-3: profitability=`0.0` avg_return=`-1.04` trades=`1`
- wf-1: profitability=`0.5633` avg_return=`0.1267` trades=`12`

## evo-ec1fefe30b2a

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `wick_reversal`
- priority: `0.99`
- holdout_profitability_score: `0.0`
- walk_forward_consistency: `0.3333`
- stress_resilience: `0.0`
- max_drawdown: `0.7`
- contradiction: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Failure Modes

- sparse_signal: Trade count stays below the minimum gate, so the candidate may be a local curve rather than a repeatable contract edge.
- holdout_decay: The final holdout slice drops below break-even profitability after fees.
- segment_instability: Walk-forward consistency is too low across chronological splits.
- execution_fragility: Edge does not survive elevated fees and slippage cleanly.
- drawdown_excess: Drawdown remains above the promotion boundary even when trade count is adequate.

### Weakest Segments

- wf-3: profitability=`0.0` avg_return=`-1.04` trades=`1`
- wf-1: profitability=`0.5633` avg_return=`0.1267` trades=`12`

## evo-a86ccc4f88a9

- doctrine_id: `wedge_guarded`
- strategy_id: `volume_exhaustion_reversal`
- priority: `0.99`
- holdout_profitability_score: `0.98`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- max_drawdown: `0.99`
- contradiction: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Failure Modes

- sparse_signal: Trade count stays below the minimum gate, so the candidate may be a local curve rather than a repeatable contract edge.
- segment_instability: Walk-forward consistency is too low across chronological splits.
- execution_fragility: Edge does not survive elevated fees and slippage cleanly.
- drawdown_excess: Drawdown remains above the promotion boundary even when trade count is adequate.

### Weakest Segments

- wf-3: profitability=`0.23` avg_return=`-0.54` trades=`4`
- wf-1: profitability=`0.3436` avg_return=`-0.3127` trades=`11`

## evo-a4b9dff257b0

- doctrine_id: `wedge_guarded`
- strategy_id: `volume_exhaustion_reversal`
- priority: `0.99`
- holdout_profitability_score: `0.98`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- max_drawdown: `0.99`
- contradiction: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Failure Modes

- sparse_signal: Trade count stays below the minimum gate, so the candidate may be a local curve rather than a repeatable contract edge.
- segment_instability: Walk-forward consistency is too low across chronological splits.
- execution_fragility: Edge does not survive elevated fees and slippage cleanly.
- drawdown_excess: Drawdown remains above the promotion boundary even when trade count is adequate.

### Weakest Segments

- wf-3: profitability=`0.23` avg_return=`-0.54` trades=`4`
- wf-1: profitability=`0.3436` avg_return=`-0.3127` trades=`11`

## evo-7b515aab8fbd

- doctrine_id: `wedge_guarded`
- strategy_id: `volume_exhaustion_reversal`
- priority: `0.99`
- holdout_profitability_score: `0.98`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- max_drawdown: `0.99`
- contradiction: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Failure Modes

- sparse_signal: Trade count stays below the minimum gate, so the candidate may be a local curve rather than a repeatable contract edge.
- segment_instability: Walk-forward consistency is too low across chronological splits.
- execution_fragility: Edge does not survive elevated fees and slippage cleanly.
- drawdown_excess: Drawdown remains above the promotion boundary even when trade count is adequate.

### Weakest Segments

- wf-3: profitability=`0.23` avg_return=`-0.54` trades=`4`
- wf-1: profitability=`0.3436` avg_return=`-0.3127` trades=`11`

## btc-15m-volatility-compression-breakout-psychology_no_chase

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `breakout_open_interest_confirmation`
- priority: `0.99`
- holdout_profitability_score: `0.3133`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- max_drawdown: `0.99`
- contradiction: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Failure Modes

- sparse_signal: Trade count stays below the minimum gate, so the candidate may be a local curve rather than a repeatable contract edge.
- holdout_decay: The final holdout slice drops below break-even profitability after fees.
- segment_instability: Walk-forward consistency is too low across chronological splits.
- execution_fragility: Edge does not survive elevated fees and slippage cleanly.
- drawdown_excess: Drawdown remains above the promotion boundary even when trade count is adequate.

### Weakest Segments

- wf-3: profitability=`0.0` avg_return=`-1.04` trades=`2`
- wf-2: profitability=`0.0` avg_return=`0.0` trades=`0`

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-breakout-impulse-squeeze-compression_profile=moderate_squee-6cb7125f43

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
- priority: `0.99`
- holdout_profitability_score: `0.0`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- max_drawdown: `0.99`
- contradiction: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Failure Modes

- sparse_signal: Trade count stays below the minimum gate, so the candidate may be a local curve rather than a repeatable contract edge.
- holdout_decay: The final holdout slice drops below break-even profitability after fees.
- segment_instability: Walk-forward consistency is too low across chronological splits.
- execution_fragility: Edge does not survive elevated fees and slippage cleanly.
- drawdown_excess: Drawdown remains above the promotion boundary even when trade count is adequate.

### Weakest Segments

- wf-2: profitability=`0.0` avg_return=`-1.04` trades=`1`
- wf-3: profitability=`0.0` avg_return=`-1.04` trades=`3`

## baseline

- doctrine_id: `n/a`
- strategy_id: `n/a`
- priority: `0.99`
- holdout_profitability_score: `0.0`
- walk_forward_consistency: `0.0`
- stress_resilience: `0.0`
- max_drawdown: `0.0`
- contradiction: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Failure Modes

- sparse_signal: Trade count stays below the minimum gate, so the candidate may be a local curve rather than a repeatable contract edge.
- holdout_decay: The final holdout slice drops below break-even profitability after fees.
- segment_instability: Walk-forward consistency is too low across chronological splits.
- execution_fragility: Edge does not survive elevated fees and slippage cleanly.

### Weakest Segments

- wf-1: profitability=`0.0` avg_return=`0.0` trades=`0`
- wf-2: profitability=`0.0` avg_return=`0.0` trades=`0`

## Anti-Patterns

- high PnL with unstable drawdown
- strategy wins that do not transfer across adjacent regimes
- doctrine labels attached after the fact to justify a curve fit
- paper-trade enthusiasm outrunning benchmark evidence
