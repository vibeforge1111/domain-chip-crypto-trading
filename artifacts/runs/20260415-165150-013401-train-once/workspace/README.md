# domain-chip-crypto-trading

Crypto trading domain chip with three autoloops:

1. **Doctrine Discovery** — ingest research, generate doctrine cards, discover regime-specific edges
2. **Backtesting** — walk-forward validation with 36-feature engine and 5-regime detection
3. **Live Paper Trading** — real-time Binance observer pattern across 15m/1h/4h timeframes

## Quick Start

### Install
```bash
pip install -e .
```

### Run the Autoloop (doctrine discovery + backtest + paper trade)
```bash
# Single cycle
crypto-autoloop run-once

# Continuous
crypto-autoloop run --max-cycles 50 --sleep-seconds 30

# Individual lanes
crypto-autoloop lane learning
crypto-autoloop lane backtest
crypto-autoloop lane paper-trade
```

### Run Live Paper Trading (real-time Binance feed)
```bash
python live/live_paper_trader.py
```
- Polls Binance public API every 60s (no API key needed)
- Detects market regime from live candles
- Matches regime to strategies, invokes elite agents
- Settles predictions at 15m/1h/4h boundaries
- Logs to `artifacts/paper_trade/`

### Run the Dashboard (real-time monitoring UI)
```bash
python live/dashboard_app.py
# → http://localhost:8502
```
- Dark-themed shadcn/ui-inspired dashboard with auto-refresh every 10s
- **Autoloop status**: cycle timeline, lane cards (learning/backtest/paper trade), regime targeting, doctrine variety backlog, active hypotheses, failure surface
- **Live Trading**: real-time Binance settlements, strategy + agent performance, regime history

### Run Evolution (DGM-H strategy discovery)
```bash
python live/run_evolution.py -g 10 -w 4
```

### Status & Diagnostics
```bash
crypto-autoloop status
crypto-autoloop doctor
crypto-autoloop paths
```

## Architecture

```
src/domain_chip_crypto_trading/
  backtest.py       # 36-feature engine, 5 regimes, walk-forward validator
  cli.py            # Deterministic evaluator with doctrine scoring
  autoloop.py       # Tri-loop orchestrator CLI

scripts/            # 30 autoloop scripts (supervisor, learning, backtest, forge, data prep)

live/
  live_paper_trader.py          # Real-time Binance observer pattern
  run_evolution.py              # DGM-H evolution loop
  run_paper_trade.py            # Paper trade validation
  hyperagent/                   # Evolution engine, meta-agent, risk manager

autoloop/           # Control plane (lanes, runbooks, policy)
data/               # Market data (BTC/ETH/SOL candles + contracts)
docs/               # Doctrine templates, recursion policy, research sources
artifacts/          # Runtime output (cycle journal, paper trades, ledger)
```

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

## Fresh Start
This repo ships with zero learned data. All artifacts, doctrine cards, and strategy winners
are discovered by running the autoloops. The engine, feature set, and regime detection are
intact — the intelligence accumulates through operation.
