# Flywheel

This chip should run three governing loops connected by explicit handoff packets.

Pass sequence:

1. learning loop ingests doctrine packets into doctrine cards
2. backtest loop benchmarks, mutates, and writes bridge packets
3. paper-trade loop validates only bridge-approved candidates
4. watchtower refreshes the shared operator surface

Loop split:

- `learning_loop`: research packet -> doctrine card
- `backtest_loop`: doctrine card -> benchmark -> contradiction -> bridge
- `paper_trade_loop`: bridge-approved queue -> outer validation -> demotion or live-readiness review

Anti-patterns:

- strategy churn without doctrine anchors
- optimizing on PnL alone
- collapsing backtest and paper-trade truth into one lane
- promoting exciting curves as doctrine before extracting boundaries
