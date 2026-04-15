# CLAUDE.md - domain-chip-crypto-trading

## What This Is

A crypto trading domain chip with three autoloops for autonomous edge discovery:
1. **Doctrine Discovery** — research ingestion, hypothesis generation, doctrine card creation
2. **Backtesting** — walk-forward validation (36 features, 5 regimes, stress testing)
3. **Live Paper Trading** — real-time Binance observer pattern (15m/1h/4h)

This is a **clean fork** — no prior wins, no accumulated strategy data. Intelligence builds from zero through autoloop operation.

## Running

### Autoloop (tri-loop: learning + backtest + paper trade)
```bash
pip install -e .
crypto-autoloop run-once                    # Single cycle
crypto-autoloop run --max-cycles 50         # Continuous
crypto-autoloop lane learning               # Individual lanes
crypto-autoloop lane backtest
crypto-autoloop lane paper-trade
crypto-autoloop status                      # Check state
crypto-autoloop doctor                      # Diagnose blockers
```

### Live Paper Trading (Binance real-time)
```bash
python live/live_paper_trader.py
```
- No API key needed (public Binance klines)
- Polls every 60s, settles at timeframe boundaries
- Logs to `artifacts/paper_trade/`

### Evolution (DGM-H population search)
```bash
python live/run_evolution.py -g 10 -w 4
```

## Key Files

| File | Purpose |
|------|---------|
| `src/.../backtest.py` | 36-feature engine, 5-regime detection, walk-forward |
| `src/.../cli.py` | Deterministic evaluator, doctrine scoring |
| `src/.../autoloop.py` | Tri-loop orchestrator CLI |
| `scripts/run_autoloop_supervisor.py` | Main supervisor (schedules all 3 lanes) |
| `scripts/run_learning_loop.py` | Doctrine ingestion lane |
| `scripts/run_backtest_loop.py` | Backtest validation lane |
| `scripts/run_paper_trade_cycle.py` | Paper trade validation lane |
| `scripts/run_strategy_forge.py` | Indicator mutation discovery |
| `scripts/live_signal_engine.py` | Real-time signal generator |
| `live/live_paper_trader.py` | Binance observer + agent pool |
| `live/run_evolution.py` | DGM-H evolution loop |
| `live/hyperagent/` | Evolution engine, meta-agent, risk manager |

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
- `artifacts/paper_trade/` — paper trade history
- `artifacts/ledger/` — run logs
- `artifacts/backtests/` — backtest results

All artifacts start empty. They accumulate as autoloops run.
