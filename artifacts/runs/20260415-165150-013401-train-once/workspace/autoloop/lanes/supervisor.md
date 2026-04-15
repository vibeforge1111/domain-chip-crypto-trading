# Supervisor Lane

## Purpose

Schedule the loop, persist state, and stop when policy or repo state says the loop is unsafe to continue.

## Runner

Foreground:

```powershell
python scripts/crypto_autoloop.py run
```

One bounded cycle:

```powershell
python scripts/crypto_autoloop.py run-once --no-commit
```

## Reads

- `docs/recursion/autoloop-policy.json`
- `artifacts/recursion/autoloop_state.json`
- tracked worktree state via `git status`

## Writes

- `artifacts/recursion/autoloop_state.json`
- `artifacts/recursion/cycle_journal.jsonl`

## Operator Rules

- stop on dirty tracked worktree unless policy changes intentionally
- prefer the smallest justified lane each cycle
- rebuild watchtower after lane activity so the current bottleneck stays visible
