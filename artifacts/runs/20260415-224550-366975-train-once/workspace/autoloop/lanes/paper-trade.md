# Paper-Trade Lane

## Purpose

Validate only bridge-approved candidates on slower outer-validation data.

## Runner

```powershell
python scripts/crypto_autoloop.py lane paper-trade
```

## Reads

- `artifacts/promotion/benchmark_grounded/*.json`
- `data/paper_trade_*`

## Writes

- `artifacts/paper_trade/paper_trade_queue.json`
- `artifacts/paper_trade/paper_trade_summary.json`
- `artifacts/paper_trade/paper_trade_loop_report.json`

## Operator Rules

- consume only bridge-approved candidates
- never treat paper-trade output as a replacement for backtest truth
- demote weak candidates back into refinement instead of promoting by default
