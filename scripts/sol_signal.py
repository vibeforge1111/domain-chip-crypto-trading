"""Quick SOL compression signal checker for live trading.

Usage:
    python scripts/sol_signal.py              # Single check
    python scripts/sol_signal.py --watch      # Continuous (every 5 min)
    python scripts/sol_signal.py --bankroll 500  # Custom bankroll
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from domain_chip_crypto_trading.backtest import (
    _candles, _contracts, _window_candles, _feature_row,
    _detected_regime, _signal, data_paths,
)

MUTATIONS = {
    "asset_universe": "BTC,SOL",
    "direction_filter": "long_only",
    "doctrine_id": "compression_mean_reversion",
    "execution_buffer": "high",
    "market_regime": "compression",
    "paper_gate": "balanced",
    "session_quality_filter": "skip_compression_toxic",
    "strategy_id": "compression_range_bounce",
    "timeframe": "15m",
    "venue": "bybit",
}

# Paper trade stats for position sizing (updated Session 15e)
# BTC backtest WR=0.645, SOL backtest WR=0.572 (7mo)
# SOL paper trade WR=0.583-0.639 (30d) — edge is recency-driven
BACKTEST_WR = 0.645
SOL_PAPER_WR = 0.583


def _kelly_quarter(wr: float) -> float:
    edge = wr - (1 - wr)
    return max(0, edge * 0.25)


def check_sol() -> dict:
    candle_path, contract_path = data_paths(REPO_ROOT, asset="sol", timeframe="15m")
    if not candle_path.exists():
        return {"error": "No SOL candle data"}

    candles = _candles(candle_path)
    contracts = _contracts(contract_path)
    if not candles or not contracts:
        return {"error": "No data loaded"}

    candle_times = [c.ts.timestamp() for c in candles]
    latest = contracts[-1]
    lookback = _window_candles(candles, candle_times, latest)

    if len(lookback) < 5:
        return {"error": "Insufficient lookback candles"}

    features = _feature_row(lookback, latest)
    regime = _detected_regime(features)
    signal = _signal(MUTATIONS, features)
    hour = latest.open_ts.hour

    # SOL best/weak hours from paper trade analysis
    # Dead zone: 12-15 UTC = 30% WR in paper trades
    best_hours = {0, 1, 4, 6, 9, 10, 16}
    dead_zone = {12, 13, 14, 15}
    weak_hours = {22}

    hour_quality = "BEST" if hour in best_hours else ("DEAD_ZONE" if hour in dead_zone else ("WEAK" if hour in weak_hours else "OK"))

    return {
        "asset": "SOL",
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "contract": latest.contract_id,
        "open_ts": latest.open_ts.isoformat().replace("+00:00", "Z"),
        "hour_utc": hour,
        "hour_quality": hour_quality,
        "regime": regime,
        "signal": signal,
        "features": {
            "compression_ratio": round(features.get("compression_ratio", 0), 4),
            "rsi": round(features.get("rsi", 0), 1),
            "volume_ratio": round(features.get("volume_ratio", 0), 3),
            "momentum": round(features.get("momentum", 0), 6),
            "lower_wick": round(features.get("lower_wick_ratio", 0), 3),
            "session_hour": hour,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="SOL compression signal checker")
    parser.add_argument("--watch", action="store_true", help="Continuous monitoring")
    parser.add_argument("--interval", type=int, default=300, help="Watch interval (seconds)")
    parser.add_argument("--bankroll", type=float, default=100.0, help="Bankroll for sizing")
    args = parser.parse_args()

    kelly_q = _kelly_quarter(SOL_PAPER_WR)
    position = round(args.bankroll * kelly_q, 2)

    if args.watch:
        print(f"[SOL SIGNAL WATCH] Bankroll=${args.bankroll} Position=${position} (Kelly/4={kelly_q:.1%})")
        print(f"{'='*72}")
        while True:
            r = check_sol()
            if "error" in r:
                print(f"[ERROR] {r['error']}")
            else:
                sig = r["signal"].upper()
                marker = ">>>" if sig in ("UP", "DOWN") else "   "
                hq = r["hour_quality"]
                print(f"{marker} [{r['checked_at']}] {r['contract']} h={r['hour_utc']:02d}({hq}) regime={r['regime']} signal={sig}")
                if sig in ("UP", "DOWN"):
                    print(f"    ACTION: Buy {sig} on Kalshi kxsol15m | Position: ${position}")
            time.sleep(args.interval)
    else:
        r = check_sol()
        if "error" in r:
            print(f"ERROR: {r['error']}")
            return

        print(f"\n{'='*50}")
        print(f"  SOL COMPRESSION SIGNAL CHECK")
        print(f"{'='*50}")
        print(f"  Time:     {r['checked_at']}")
        print(f"  Contract: {r['contract']}")
        print(f"  Hour:     {r['hour_utc']:02d} UTC ({r['hour_quality']})")
        print(f"  Regime:   {r['regime']}")
        print(f"  Signal:   {r['signal'].upper()}")
        print()
        f = r["features"]
        print(f"  Features:")
        print(f"    Compression: {f['compression_ratio']}")
        print(f"    RSI:         {f['rsi']}")
        print(f"    Volume:      {f['volume_ratio']}")
        print(f"    Momentum:    {f['momentum']}")
        print(f"    Lower Wick:  {f['lower_wick']}")
        print()
        print(f"  Position Sizing:")
        print(f"    SOL Paper WR:  {SOL_PAPER_WR:.1%} (31 trades)")
        print(f"    Quarter Kelly: {kelly_q:.1%}")
        print(f"    ${args.bankroll} bankroll = ${position} per trade")

        if r["signal"] in ("up", "down"):
            print(f"\n  >>> TRADE: Buy {r['signal'].upper()} on Kalshi <<<")
        else:
            print(f"\n  No trade (signal={r['signal']})")


if __name__ == "__main__":
    main()
