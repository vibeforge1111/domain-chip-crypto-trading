# domain-chip-crypto-trading

Crypto trading domain chip with autonomous edge discovery through three interlocking autoloops:

1. **Doctrine Discovery** — ingest research, generate doctrine cards, discover regime-specific edges
2. **Backtesting** — walk-forward validation with 36-feature engine and 5-regime detection
3. **Live Paper Trading** — real-time Binance observer pattern across 15m/1h/4h timeframes

## Running the Full Stack

Four processes run together to form the complete autonomous system. Start them in this order.

### Step 1: Install

```bash
pip install -e .
pipx install git+https://github.com/vibeforge1111/spark-researcher.git
```

### Step 2: Start the Autoloop Supervisor (continuous)

The tri-loop orchestrator. Runs learning → backtest → paper_trade in sequence, indefinitely.

```bash
python scripts/run_autoloop_supervisor.py --max-cycles 9999
```

- Each cycle: ingests doctrine cards, runs walk-forward backtests, promotes WF≥0.8 candidates to paper trade
- Sleeps 300s between cycles by default
- Commits artifacts to git after each cycle
- This is the core process — everything else feeds into or reads from it

### Step 3: Start the Researcher Loop (autonomous)

Re-triggers Spark Researcher whenever the frontier queue drains. Evaluates fresh backtest results and queues new strategy suggestions.

```bash
python scripts/run_researcher_loop.py --interval 600 --rounds 3 --min-cycles 5
```

| Flag | Default | What it does |
|---|---|---|
| `--interval` | 600 | Seconds between frontier queue checks |
| `--rounds` | 3 | Researcher rounds per trigger |
| `--min-cycles` | 5 | Minimum autoloop cycles between triggers |

- Calls chip hooks: evaluate, suggest, packets, watchtower
- Queues suggestions to `artifacts/frontier/queue.json`
- The autoloop supervisor picks up frontier suggestions automatically

### Step 4: Start the Live Paper Trader (real-time)

Watches Binance public klines in real-time, runs elite agents against live market data.

```bash
python live/live_paper_trader.py
```

- No API key needed (public Binance klines)
- Polls every 60s, settles predictions at 15m/1h/4h boundaries
- Detects market regime from live candles
- Matches regime to strategies, invokes elite agents from `live/archive/generations/`
- Logs to `artifacts/paper_trade/` and `live/archive/live_pt_state.json`

### Step 5: Start the Dashboard (monitoring)

```bash
python live/dashboard_app.py
# → http://localhost:8502
```

- Auto-refreshes every 10 seconds
- Dark-themed with Chart.js visualizations

### Quick Reference

| Process | Command | Purpose |
|---|---|---|
| Autoloop supervisor | `python scripts/run_autoloop_supervisor.py --max-cycles 9999` | Tri-loop: learning → backtest → paper trade |
| Researcher loop | `python scripts/run_researcher_loop.py` | Re-evaluates + suggests on frontier drain |
| Live paper trader | `python live/live_paper_trader.py` | Real-time Binance signals |
| Dashboard | `python live/dashboard_app.py` | Monitoring UI on :8502 |

## How It Works Together

```
Researcher Loop (every ~10min)
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
  → Elite agents watching BTC/ETH/SOL on Binance
  → Settles predictions at 15m/1h/4h boundaries
  → Logs accuracy to paper trade history
        ↓
Dashboard (http://localhost:8502)
  → All data visible, auto-refresh 10s
  → Charts: doctrine growth, autoloop activity, WR vs WF scatter
  → Tables: top candidates, strategy diversity, self-edits queue
```

## Dashboard Sections

| Section | What it shows |
|---|---|
| Top Stats | Cycle count, best/avg win rate, approved/deferred/total |
| Cycle Activity Feed | Per-cycle lane activity, filterable by learning/backtest/paper_trade |
| Doctrine Growth | Cumulative doctrine cards + variety backlog over cycles |
| Autoloop Activity | Cards ingested + material backtest flags per cycle |
| Strategy Performance | Progress bars by strategy family (win rate) |
| Strategy Diversity | Distribution bar + Shannon diversity index |
| Researcher Health | Chip hook call counts, frontier queue size |
| Doctrine Insights | Latest cards with mechanism, priority, lineage failures |
| Self-Edit Queue | Queued candidate mutations with priority and failure modes |
| Top Candidates | Sortable table (WR/WF/Sharpe), filterable by strategy/verdict |
| Walk-Forward Gate | Coverage progress + WR vs WF scatter with 0.8 threshold |
| Autoloop Lanes | Lane status cards + cycle timeline stacked bar chart |
| Live Trading | Real-time Binance signals, agent accuracy, settlement log |

## Individual Commands (debugging)

```bash
# Single autoloop cycle
crypto-autoloop run-once

# Run individual lanes
crypto-autoloop lane learning
crypto-autoloop lane backtest
crypto-autoloop lane paper-trade

# Diagnostics
crypto-autoloop status
crypto-autoloop doctor
crypto-autoloop paths

# One-shot researcher (instead of loop)
spark-researcher autoloop --command autoloop --rounds 3
spark-researcher summary
spark-researcher failures
spark-researcher beliefs
spark-researcher candidates
```

## Architecture

```
src/domain_chip_crypto_trading/
  backtest.py       # 36-feature engine, 5 regimes, walk-forward validator
  cli.py            # Deterministic evaluator with doctrine scoring
  autoloop.py       # Tri-loop orchestrator CLI

scripts/
  run_autoloop_supervisor.py   # Main supervisor (schedules all 3 lanes)
  run_researcher_loop.py       # Researcher trigger loop (frontier-drain based)
  run_learning_loop.py         # Doctrine ingestion lane
  run_backtest_loop.py         # Backtest validation lane
  run_paper_trade_cycle.py     # Paper trade validation lane
  researcher_run.py            # Spark Researcher wrapper (emits metrics)

live/
  dashboard_app.py             # Real-time monitoring dashboard
  live_paper_trader.py         # Binance observer + agent pool
  hyperagent/chip_hooks.py     # Chip hooks (evaluate, suggest, packets, watchtower)

autoloop/           # Control plane (lanes, runbooks, policy)
data/               # Market data (BTC/ETH/SOL candles + contracts)
docs/               # Doctrine cards, packets, templates, research sources
artifacts/          # Runtime output (see below)
```

## Artifacts (Runtime State)

| Path | Purpose |
|---|---|
| `artifacts/recursion/autoloop_state.json` | Supervisor state (cycle count, noop streak) |
| `artifacts/recursion/cycle_journal.jsonl` | Immutable cycle log |
| `artifacts/recursion/variety_backlog.json` | Uncovered strategy combinations |
| `artifacts/recursion/self_edit_queue.json` | Queued candidate mutations |
| `artifacts/recursion/mutation_trials.json` | Mutation trial records |
| `artifacts/frontier/queue.json` | Researcher suggestion queue |
| `artifacts/backtests/heavy_backtest_summary.json` | Latest backtest results |
| `artifacts/paper_trade/` | Paper trade queue, history, monitor |
| `artifacts/chips/` | Chip hook I/O logs |
| `docs/doctrine-cards/` | Generated doctrine cards |
| `docs/doctrine-packets/` | Generated doctrine packets |

All artifacts start empty. They accumulate as autoloops run.

## Regimes

| Regime | Description |
|--------|-------------|
| Compression | Tight range, low vol — mean reversion territory |
| Trend | Directional slope, consistent closes |
| Range | Oscillating 1.2-2.5% range |
| Event-Driven | Volatility spike + news |
| Fear Shock | Extreme vol + gap moves |

## Features (36)

Price, volatility, momentum, trend, micro-structure, and context features.
See `backtest.py` for full definitions.

## Data

- BTC/ETH/SOL 1-minute candles
- 15m and 1h contract windows
- Separate paper-trade validation sets
- Fetch fresh data: `python scripts/fetch_binance_1m_range.py`

## Chip Integration

This repo implements the `spark-chip.v1` contract via `spark-chip.json` and `live/hyperagent/chip_hooks.py`:

| Hook | Purpose |
|---|---|
| `evaluate` | Scores current backtest results, returns metrics |
| `suggest` | Proposes next candidates (cross-pollination, variety backlog, worst-flip) |
| `packets` | Returns doctrine packets for research ingestion |
| `watchtower` | Reports failure surfaces and contradiction probes |

Config: `spark-researcher.project.json` — baseline-only, no `mutable_parameters`. The autoloop discovers candidates internally through its doctrine/mutation pipeline. The researcher observes, evaluates, and suggests — it doesn't inject its own mutations.

## Fresh Start

This repo ships with zero learned data. All artifacts, doctrine cards, and strategy winners
are discovered by running the autoloops. The engine, feature set, and regime detection are
intact — the intelligence accumulates through operation.
