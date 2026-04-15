# Learning Lane

## Purpose

Convert source-grounded research into doctrine packets and doctrine cards.

## Runner

```powershell
python scripts/crypto_autoloop.py lane learning
```

## Reads

- `docs/research-ingest/*.json`
- `docs/doctrine-packets/*.json`

## Writes

- `docs/doctrine-cards/*.json`
- `artifacts/research/learning_loop_report.json`

## Operator Rules

- ingest only source-grounded packets
- keep research design separate from benchmark claims
- feed cards forward into backtest; do not shortcut to promotion
