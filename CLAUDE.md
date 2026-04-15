# CLAUDE.md - domain-chip-crypto-trading

## What This Is

A crypto trading domain chip with three autoloops for autonomous edge discovery:
1. **Doctrine Discovery** — research ingestion, hypothesis generation, doctrine card creation
2. **Backtesting** — walk-forward validation (36 features, 5 regimes, stress testing)
3. **Live Paper Trading** — real-time Binance observer pattern (15m/1h/4h)

This is a **clean fork** — no prior wins, no accumulated strategy data. Intelligence builds from zero through autoloop operation.

## Running the Full Stack

Four processes run together. Start them in this order.

### 1. Install dependencies (once)
```bash
pip install -e .
pipx install git+https://github.com/vibeforge1111/spark-researcher.git
```

### 2. Start the Autoloop Supervisor (continuous)
The tri-loop orchestrator. Runs learning → backtest → paper_trade in sequence, indefinitely.
```bash
python scripts/run_autoloop_supervisor.py --max-cycles 9999
```
- Each cycle: ingests doctrine cards, runs walk-forward backtests, promotes WF≥0.8 candidates to paper trade
- Sleeps 300s between cycles by default
- Commits artifacts to git after each cycle

### 3. Start the Researcher Loop (autonomous)
Re-triggers Spark Researcher whenever the frontier queue drains. Evaluates fresh backtest results and queues new suggestions.
```bash
python scripts/run_researcher_loop.py --interval 600 --rounds 3 --min-cycles 5
```
- Checks frontier queue every 10 minutes
- Waits for at least 5 autoloop cycles between triggers
- Calls chip hooks: evaluate, suggest, packets, watchtower
- Queues suggestions to `artifacts/frontier/queue.json`

### 4. Start the Live Paper Trader (real-time)
Watches Binance public klines in real-time, runs elite agents against live data.
```bash
python live/live_paper_trader.py
```
- No API key needed (public Binance klines)
- Polls every 60s, settles at 15m/1h/4h boundaries
- Loads viable+elite agents from `live/archive/generations/`
- Logs to `artifacts/paper_trade/` and `live/archive/live_pt_state.json`

### 5. Start the Dashboard (monitoring)
```bash
python live/dashboard_app.py
```
- Opens at http://localhost:8502
- Auto-refreshes every 10 seconds
- Shows: doctrine growth, autoloop activity, strategy diversity, WF gate, top candidates, self-edits, researcher health, live trading

### Quick Reference
| Process | Command | Runs |
|---|---|---|
| Autoloop supervisor | `python scripts/run_autoloop_supervisor.py --max-cycles 9999` | Continuous |
| Researcher loop | `python scripts/run_researcher_loop.py` | Continuous (triggers on frontier drain) |
| Live paper trader | `python live/live_paper_trader.py` | Continuous (polls Binance) |
| Dashboard | `python live/dashboard_app.py` | Continuous (serves :8502) |

### Individual Lane Commands (debugging)
```bash
crypto-autoloop run-once                    # Single cycle
crypto-autoloop lane learning               # Individual lanes
crypto-autoloop lane backtest
crypto-autoloop lane paper-trade
crypto-autoloop status                      # Check state
crypto-autoloop doctor                      # Diagnose blockers
```

### One-shot Researcher (alternative to loop)
```bash
spark-researcher autoloop --command autoloop --rounds 3
spark-researcher summary
```

## How It Works Together

```
Researcher Loop (every 10min)
  → calls chip hooks (evaluate, suggest, packets, watchtower)
  → evaluates latest backtest results
  → queues suggestions to frontier queue
        ↓
Autoloop Supervisor (continuous, ~5min/cycle)
  → Learning: ingests doctrine cards from research packets
  → Backtest: tests candidates against walk-forward gate (WF≥0.8)
  → Paper Trade: promotes passing candidates for live validation
  → Commits artifacts after each cycle
        ↓
Live Paper Trader (real-time)
  → 7+ agents watching BTC/ETH/SOL on Binance
  → Settles predictions at 15m/1h/4h boundaries
  → Logs accuracy to paper trade history
        ↓
Dashboard (http://localhost:8502)
  → All data visible, auto-refresh 10s
  → Charts: doctrine growth, autoloop activity, WR vs WF scatter
  → Tables: top candidates (sortable), strategy diversity, self-edits
```

## Key Files

| File | Purpose |
|------|---------|
| `scripts/run_autoloop_supervisor.py` | Main supervisor (schedules all 3 lanes) |
| `scripts/run_researcher_loop.py` | Researcher trigger loop (frontier-drain based) |
| `scripts/run_learning_loop.py` | Doctrine ingestion lane |
| `scripts/run_backtest_loop.py` | Backtest validation lane |
| `scripts/run_paper_trade_cycle.py` | Paper trade validation lane |
| `live/live_paper_trader.py` | Binance observer + agent pool |
| `live/dashboard_app.py` | Real-time monitoring dashboard |
| `live/hyperagent/chip_hooks.py` | Spark Researcher chip hooks (evaluate, suggest, packets, watchtower) |
| `src/.../backtest.py` | 36-feature engine, 5-regime detection, walk-forward |
| `src/.../cli.py` | Deterministic evaluator, doctrine scoring |
| `src/.../autoloop.py` | Tri-loop orchestrator CLI |
| `spark-researcher.project.json` | Spark Researcher config (baseline-only, no mutable_parameters) |
| `spark-chip.json` | Chip contract definition |

## Architecture

### Autoloop Tri-Loop
```
Learning Loop → doctrine cards from research packets
    ↓
Backtest Loop → walk-forward test candidates (WF>=0.8 gate)
    ↓
Paper Trade Loop → outer validation on held-out data
    ↓
(repeat)
```

### Live Paper Trader (Observer Pattern)
```
Binance API (public) → CandleBuffer (300 rolling) → MarketObserver (regime)
    → StrategyRegistry (match) → AgentPool (elite agents) → Predict
    → Settle at boundary → TradeLogger (JSONL + JSON state)
```

### Regime Detection
- Compression, Trend, Range, Event-Driven, Fear Shock
- Features: close_location, range_pct, atr, rsi, macd, ema_gap_ratio, compression_ratio, etc.

## Data
- `data/` contains BTC/ETH/SOL 1m candles + 15m/1h contract windows
- Separate paper-trade validation sets (different date ranges)
- Fetch fresh data: `python scripts/fetch_binance_1m_range.py`

## Artifacts (Runtime State)
- `artifacts/recursion/autoloop_state.json` — supervisor state
- `artifacts/recursion/cycle_journal.jsonl` — immutable cycle log
- `artifacts/recursion/variety_backlog.json` — uncovered strategy combinations
- `artifacts/recursion/self_edit_queue.json` — queued candidate mutations
- `artifacts/recursion/mutation_trials.json` — mutation trial records
- `artifacts/frontier/queue.json` — researcher suggestion queue
- `artifacts/backtests/heavy_backtest_summary.json` — latest backtest results
- `artifacts/paper_trade/` — paper trade history + queue + monitor
- `artifacts/chips/` — chip hook I/O logs (evaluate, suggest, packets, watchtower)
- `artifacts/ledger/` — run logs
- `docs/doctrine-cards/` — generated doctrine cards (~200+)
- `docs/doctrine-packets/` — generated doctrine packets (~200+)

All artifacts start empty. They accumulate as autoloops run.

## Dashboard (http://localhost:8502)

Sections (top to bottom):
1. **Top Stats** — cycle count, best WR, avg WR, approved/deferred/total
2. **Cycle Activity Feed** — filterable by lane (learning/backtest/paper_trade/material)
3. **Doctrine Growth Chart** — cumulative cards ingested + variety backlog over cycles
4. **Autoloop Activity Chart** — cards added per cycle + material backtest flags
5. **Strategy Family Performance** — progress bars by strategy (WR)
6. **Researcher Health** — chip hook call counts, frontier queue size
7. **Strategy Diversity** — stacked distribution bar + diversity index
8. **Doctrine Insights** — latest cards with mechanism, priority, failure count
9. **Self-Edit Queue** — queued mutations with priority and failure modes
10. **Top Candidates Table** — sortable by WR/WF/Sharpe, filterable by strategy/verdict
11. **Walk-Forward Gate** — coverage progress + WR vs WF scatter chart
12. **Autoloop Lanes** — lane status cards + cycle timeline chart
13. **Live Trading** — real-time Binance paper trade signals and accuracy
