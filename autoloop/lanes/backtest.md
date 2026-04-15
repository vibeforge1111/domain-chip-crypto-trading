# Backtest Lane

## Purpose

Benchmark doctrine-backed strategy candidates, extract contradictions, and write promotion bridge packets.

## Runner

```powershell
python scripts/crypto_autoloop.py lane backtest
```

## Reads

- `benchmarks/trading-crypto-candidate.json`
- `docs/doctrine-cards/*.json`
- `data/*.jsonl`

## Writes

- `artifacts/backtests/backtest_loop_report.json`
- `artifacts/promotion/benchmark_grounded/*.json`
- `artifacts/recursion/*.json`

## Operator Rules

- treat backtest as the inner truth surface
- optimize for risk-adjusted profitability, not raw PnL
- write contradictions and bridge packets explicitly
- mutation work must stay benchmark-grounded
