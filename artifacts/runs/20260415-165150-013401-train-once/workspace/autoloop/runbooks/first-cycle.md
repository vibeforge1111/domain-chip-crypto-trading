# First Cycle

Use this when bringing up the crypto-trading Autoloop or re-orienting after changes.

## Sequence

1. Inspect state:

```powershell
python scripts/crypto_autoloop.py status
python scripts/crypto_autoloop.py doctor
```

2. If the supervisor is not blocked, run one bounded cycle:

```powershell
python scripts/crypto_autoloop.py run-once --no-commit
```

3. Refresh the operator surface:

```powershell
python scripts/crypto_autoloop.py watchtower
```

## What To Check

- whether ready doctrine packets are piling up
- whether the benchmark leader is still the right candidate family
- whether the paper-trade queue contains only bridge-approved candidates
- whether the watchtower shows the same bottleneck as `status`
