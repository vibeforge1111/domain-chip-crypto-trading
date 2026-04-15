# Daily Ops

This is the short operator loop for crypto trading.

## Daily Rhythm

1. `python scripts/crypto_autoloop.py status`
2. `python scripts/crypto_autoloop.py doctor`
3. Run the smallest justified lane:
   - `learning` if doctrine packets are ready
   - `paper-trade` if queue exists
   - otherwise `backtest`
4. Refresh watchtower:

```powershell
python scripts/crypto_autoloop.py watchtower
```

## If You Want Supervised Operation

```powershell
python scripts/crypto_autoloop.py run --no-commit
```

Use commits only when the tracked worktree is intentionally clean and the loop should persist material changes.
