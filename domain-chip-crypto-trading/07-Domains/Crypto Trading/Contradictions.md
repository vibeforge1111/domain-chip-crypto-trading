# Contradictions

This page is the trading equivalent of a `why it lost` surface.

Track failure shapes here when a combination looks exciting but should not be promoted.

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

## auto-auto-auto-auto-breakout-impulse-squeeze-compression_profile=moderate_squeeze-late_sample_guard=on-sparse-43bb8ee0ac

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

## auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-auto-btc-15m-volatility-compressio-17198cff45

- doctrine_id: `breakout_volatility_expansion`
- strategy_id: `breakout_open_interest_confirmation`
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

## auto-auto-baseline-sparse_signal-probe-sparse_signal-sparse_signal-probe-sparse_signal-variety-late-sample-gu-8d2488e327

- doctrine_id: `None`
- strategy_id: `None`
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

## auto-breakout-impulse-squeeze-compression_profile=tight_squeeze-variety-late-sample-guard-plus-session-filter

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

## auto-auto-auto-auto-auto-baseline-sparse_signal-probe-sparse_signal-sparse_signal-probe-sparse_signal-variety-late-samp-c05f1ad400-sparse_signal-sparse_signal

- doctrine_id: `None`
- strategy_id: `None`
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

## auto-trend-volume-filtered-activation_profile=wider-no_trade_window=avoid_post_open_drift-volume_context_guar-5d7170b7b6

- doctrine_id: `trend_regime_following`
- strategy_id: `ema_pullback_long`
- priority: `0.6558`
- holdout_profitability_score: `0.48`
- walk_forward_consistency: `0.6667`
- stress_resilience: `0.0`
- max_drawdown: `0.99`
- contradiction: Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.

### Failure Modes

- holdout_decay: The final holdout slice drops below break-even profitability after fees.
- segment_instability: Walk-forward consistency is too low across chronological splits.
- execution_fragility: Edge does not survive elevated fees and slippage cleanly.
- drawdown_excess: Drawdown remains above the promotion boundary even when trade count is adequate.

### Weakest Segments

- wf-2: profitability=`0.4244` avg_return=`-0.1511` trades=`9`
- wf-3: profitability=`0.48` avg_return=`-0.04` trades=`14`

## Anti-Patterns

- high PnL with unstable drawdown
- strategy wins that do not transfer across adjacent regimes
- doctrine labels attached after the fact to justify a curve fit
- paper-trade enthusiasm outrunning benchmark evidence
