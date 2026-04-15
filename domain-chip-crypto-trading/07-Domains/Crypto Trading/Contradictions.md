# Contradictions

This page is the trading equivalent of a `why it lost` surface.

Track failure shapes here when a combination looks exciting but should not be promoted.

## auto-trend-volume-filtered-no_trade_window=avoid_dead_zone-volume_context_guard=thin_filter

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- priority: `0.99`
- holdout_profitability_score: `0.3133`
- walk_forward_consistency: `0.2`
- stress_resilience: `0.0`
- max_drawdown: `0.99`
- contradiction: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Failure Modes

- holdout_decay: The final holdout slice drops below break-even profitability after fees.
- segment_instability: Walk-forward consistency is too low across chronological splits.
- execution_fragility: Edge does not survive elevated fees and slippage cleanly.
- drawdown_excess: Drawdown remains above the promotion boundary even when trade count is adequate.

### Weakest Segments

- wf-5: profitability=`0.3133` avg_return=`-0.3733` trades=`6`
- wf-2: profitability=`0.355` avg_return=`-0.29` trades=`8`

## btc-15m-volatility-compression-breakout-psychology_no_chase-variety-session-stability-filter

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

- wf-1: profitability=`0.0` avg_return=`0.0` trades=`0`
- wf-4: profitability=`0.2467` avg_return=`-0.5067` trades=`15`

## auto-range-session-wick-reversal_confirmation=reclaim_close-session_profile=opening_range_failure-volume_context_guard=thin_filter-wick_profile=rejection_confirm

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `range_reclaim_scalp`
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

## auto-range-session-wick-reversal_confirmation=reclaim_close-session_profile=opening_range_failure-wick_profile=rejection_confirm

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `range_reclaim_scalp`
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

## auto-range-session-wick-reversal_confirmation=wick_reclaim_close-session_profile=opening_range_failure-volume_context_guard=thin_filter-wick_profile=rejection_confirm

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `range_reclaim_scalp`
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

## auto-range-session-wick-reversal_confirmation=wick_reclaim_close-session_profile=opening_range_failure-wick_profile=rejection_confirm

- doctrine_id: `mean_reversion_liquidity_reclaim`
- strategy_id: `range_reclaim_scalp`
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

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-late_sample_guard=on-session_profile=squeeze_release_window

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
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

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-late_sample_guard=on

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `bollinger_squeeze_breakout`
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
