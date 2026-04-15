# Loop Progression

This page mirrors the startup chip standard: one loop, one current state, one next bottleneck.

- current_state: `backtest_benchmark_first`
- reason: `the chip has benchmark candidates, but no combination has cleared the paper-trade gate yet`

## Current Flywheel Read

- learning_loop_status: `active`
- learning_pending_packets: `0`
- backtest_loop_status: `active`
- contradiction_probe_status: `idle`
- paper_trade_loop_status: `active`
- paper_trade_queue_status: `empty`

## What Should Happen Next

1. let the learning loop ingest only source-grounded doctrine packets
2. let the backtest loop benchmark, mutate, and reject ideas quickly
3. escalate only `queue_for_paper_trade` combinations into the paper-trade loop
4. use paper-trade outcomes as outer-validation evidence without rewriting benchmark facts
