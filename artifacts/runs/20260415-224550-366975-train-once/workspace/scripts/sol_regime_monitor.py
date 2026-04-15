"""SOL compression regime change detector.

Monitors whether SOL's compression dynamics are shifting.
Key metric: close_location distribution. If it moves from mean=0.178 toward
BTC-like 0.500, our long-biased edge may be eroding.

Session 15e finding: SOL's edge is recency-driven, not structural.
This monitor tracks whether the conditions that produce the edge still hold.

Usage:
    python scripts/sol_regime_monitor.py               # Check current regime health
    python scripts/sol_regime_monitor.py --window 7    # Last 7 days
    python scripts/sol_regime_monitor.py --window 30   # Last 30 days (default)
    python scripts/sol_regime_monitor.py --historical  # Full historical comparison
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, stdev

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from domain_chip_crypto_trading.backtest import (
    _candles,
    _contracts,
    _window_candles,
    _feature_row,
    _wider_context,
    _detected_regime,
    _signal,
    data_paths,
)

# Baseline from Session 15e (full 7-month SOL data)
BASELINE = {
    "close_location_mean": 0.178,
    "close_location_std": 0.145,
    "rsi_mean": 50.4,
    "rsi_std": 14.8,
    "up_bias_pct": 96.0,  # 96% of trades are UP
    "compression_pct": 45.2,  # 8849/19584 = 45.2% of contracts are compression
    "up_wr_historical": 0.568,
    "trades_per_day_30d": 1.2,  # ~36 trades / 30 days
}

# Alert thresholds
ALERT_THRESHOLDS = {
    "close_location_mean_max": 0.35,  # If mean rises above 0.35, signal quality degrades
    "up_bias_pct_min": 70.0,  # If UP bias drops below 70%, strategy assumptions break
    "compression_pct_min": 30.0,  # If compression regime frequency drops, fewer signals
    "trades_per_day_min": 0.5,  # If signal generation dries up
}


def analyze_window(
    candles: list,
    contracts: list,
    candle_times: list[float],
    start_ts: datetime | None = None,
    mutations: dict | None = None,
) -> dict:
    """Analyze SOL compression features over a window of contracts."""
    if mutations is None:
        mutations = {
            "doctrine_id": "compression_mean_reversion",
            "strategy_id": "compression_range_bounce",
            "market_regime": "compression",
            "session_quality_filter": "skip_compression_toxic",
            "execution_buffer": "high",
            "drawdown_guard": "moderate",
        }

    close_locs = []
    rsi_vals = []
    compression_count = 0
    total_count = 0
    up_signals = 0
    down_signals = 0
    skip_signals = 0
    up_wins = 0
    down_wins = 0

    for contract in contracts:
        if start_ts and contract.open_ts < start_ts:
            continue
        total_count += 1
        window = _window_candles(candles, candle_times, contract)
        if len(window) < 5:
            continue
        features = _feature_row(window, contract)
        features.update(_wider_context(candles, candle_times, contract))
        regime = _detected_regime(features)

        if regime == "compression":
            compression_count += 1
            close_locs.append(features.get("close_location", 0.5))
            rsi_vals.append(features["rsi"])

            sig = _signal(mutations, features)
            actual = contract.settlement_direction
            if sig == "up":
                up_signals += 1
                if actual == "up":
                    up_wins += 1
            elif sig == "down":
                down_signals += 1
                if actual == "down":
                    down_wins += 1
            else:
                skip_signals += 1

    total_trades = up_signals + down_signals
    result = {
        "total_contracts": total_count,
        "compression_contracts": compression_count,
        "compression_pct": round(compression_count / max(1, total_count) * 100, 1),
    }

    if close_locs:
        result["close_location_mean"] = round(mean(close_locs), 3)
        result["close_location_std"] = round(stdev(close_locs) if len(close_locs) > 1 else 0, 3)
        result["rsi_mean"] = round(mean(rsi_vals), 1)
        result["rsi_std"] = round(stdev(rsi_vals) if len(rsi_vals) > 1 else 0, 1)
        result["close_loc_below_022"] = round(sum(1 for v in close_locs if v < 0.22) / len(close_locs) * 100, 1)
        result["close_loc_above_078"] = round(sum(1 for v in close_locs if v > 0.78) / len(close_locs) * 100, 1)

    result["up_signals"] = up_signals
    result["down_signals"] = down_signals
    result["skip_signals"] = skip_signals
    result["total_trades"] = total_trades

    if total_trades > 0:
        result["up_bias_pct"] = round(up_signals / total_trades * 100, 1)
        total_wins = up_wins + down_wins
        result["win_rate"] = round(total_wins / total_trades, 3)
        result["up_wr"] = round(up_wins / max(1, up_signals), 3)
        result["down_wr"] = round(down_wins / max(1, down_signals), 3) if down_signals > 0 else None

    return result


def check_alerts(stats: dict, window_days: int) -> list[dict]:
    """Check if any alert thresholds are breached."""
    alerts = []

    cl_mean = stats.get("close_location_mean", 0)
    if cl_mean > ALERT_THRESHOLDS["close_location_mean_max"]:
        alerts.append({
            "level": "WARNING",
            "metric": "close_location_mean",
            "value": cl_mean,
            "threshold": ALERT_THRESHOLDS["close_location_mean_max"],
            "baseline": BASELINE["close_location_mean"],
            "message": f"SOL close_location mean shifted to {cl_mean:.3f} (baseline: {BASELINE['close_location_mean']:.3f}). "
                       "UP entry quality may be degrading — close_location is less extreme.",
        })

    up_bias = stats.get("up_bias_pct", 100)
    if up_bias < ALERT_THRESHOLDS["up_bias_pct_min"]:
        alerts.append({
            "level": "WARNING",
            "metric": "up_bias_pct",
            "value": up_bias,
            "threshold": ALERT_THRESHOLDS["up_bias_pct_min"],
            "baseline": BASELINE["up_bias_pct"],
            "message": f"SOL UP bias dropped to {up_bias:.1f}% (baseline: {BASELINE['up_bias_pct']:.1f}%). "
                       "Strategy assumptions about long-biased compression may be breaking.",
        })

    comp_pct = stats.get("compression_pct", 0)
    if comp_pct < ALERT_THRESHOLDS["compression_pct_min"]:
        alerts.append({
            "level": "WARNING",
            "metric": "compression_pct",
            "value": comp_pct,
            "threshold": ALERT_THRESHOLDS["compression_pct_min"],
            "baseline": BASELINE["compression_pct"],
            "message": f"SOL compression regime frequency dropped to {comp_pct:.1f}% (baseline: {BASELINE['compression_pct']:.1f}%). "
                       "Fewer signals being generated.",
        })

    trades = stats.get("total_trades", 0)
    trades_per_day = trades / max(1, window_days)
    if trades_per_day < ALERT_THRESHOLDS["trades_per_day_min"]:
        alerts.append({
            "level": "INFO",
            "metric": "trades_per_day",
            "value": round(trades_per_day, 2),
            "threshold": ALERT_THRESHOLDS["trades_per_day_min"],
            "baseline": BASELINE["trades_per_day_30d"],
            "message": f"SOL generating only {trades_per_day:.2f} trades/day (baseline: {BASELINE['trades_per_day_30d']:.1f}). "
                       "May indicate regime shift or reduced compression.",
        })

    return alerts


def main():
    parser = argparse.ArgumentParser(description="SOL compression regime change detector")
    parser.add_argument("--window", type=int, default=30, help="Analysis window in days (default: 30)")
    parser.add_argument("--historical", action="store_true", help="Compare full history vs recent window")
    args = parser.parse_args()

    candle_path, contract_path = data_paths(REPO_ROOT, asset="sol", timeframe="15m")
    if not candle_path.exists():
        print("ERROR: No SOL data found.")
        return

    candles = _candles(candle_path)
    contracts = _contracts(contract_path)
    candle_times = [c.ts.timestamp() for c in candles]

    print("=" * 72)
    print("SOL COMPRESSION REGIME MONITOR")
    print("=" * 72)
    print(f"Data range: {candles[0].ts.date()} to {candles[-1].ts.date()}")
    print(f"Total: {len(candles)} candles, {len(contracts)} contracts")
    print()

    if args.historical:
        # Full historical analysis
        print("--- FULL HISTORY ---")
        full = analyze_window(candles, contracts, candle_times)
        _print_stats(full, "Full History")
        print()

    # Recent window
    window_start = datetime.now(timezone.utc) - timedelta(days=args.window)
    recent = analyze_window(candles, contracts, candle_times, start_ts=window_start)
    _print_stats(recent, f"Last {args.window} Days")
    print()

    # Check alerts
    alerts = check_alerts(recent, args.window)
    if alerts:
        print("--- ALERTS ---")
        for alert in alerts:
            print(f"  [{alert['level']}] {alert['metric']}: {alert['value']} (threshold: {alert['threshold']}, baseline: {alert['baseline']})")
            print(f"           {alert['message']}")
        print()
    else:
        print("--- NO ALERTS --- Regime is stable.")
        print()

    # Delta from baseline
    print("--- BASELINE COMPARISON ---")
    cl_mean = recent.get("close_location_mean", 0)
    cl_delta = cl_mean - BASELINE["close_location_mean"]
    up_bias = recent.get("up_bias_pct", 0)
    up_delta = up_bias - BASELINE["up_bias_pct"]
    comp_pct = recent.get("compression_pct", 0)
    comp_delta = comp_pct - BASELINE["compression_pct"]
    print(f"  close_location mean: {cl_mean:.3f} (baseline: {BASELINE['close_location_mean']:.3f}, delta: {cl_delta:+.3f})")
    print(f"  UP bias:             {up_bias:.1f}% (baseline: {BASELINE['up_bias_pct']:.1f}%, delta: {up_delta:+.1f}pp)")
    print(f"  compression %:       {comp_pct:.1f}% (baseline: {BASELINE['compression_pct']:.1f}%, delta: {comp_delta:+.1f}pp)")
    wr = recent.get("win_rate", 0)
    wr_delta = wr - BASELINE["up_wr_historical"]
    print(f"  win_rate:            {wr:.3f} (baseline: {BASELINE['up_wr_historical']:.3f}, delta: {wr_delta:+.3f})")

    # Save report
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "window_days": args.window,
        "stats": recent,
        "baseline": BASELINE,
        "alerts": alerts,
    }
    out_path = REPO_ROOT / "artifacts" / "regime_monitor" / "sol_regime_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\nReport saved: {out_path}")


def _print_stats(stats: dict, label: str):
    print(f"  {label}:")
    print(f"    Contracts:     {stats.get('total_contracts', 0)}")
    print(f"    Compression:   {stats.get('compression_contracts', 0)} ({stats.get('compression_pct', 0):.1f}%)")
    print(f"    Trades:        {stats.get('total_trades', 0)} (UP: {stats.get('up_signals', 0)}, DOWN: {stats.get('down_signals', 0)})")
    if stats.get("total_trades", 0) > 0:
        print(f"    UP bias:       {stats.get('up_bias_pct', 0):.1f}%")
        print(f"    Win rate:      {stats.get('win_rate', 0):.3f} (UP: {stats.get('up_wr', 0):.3f}, DOWN: {stats.get('down_wr', 'n/a')})")
    cl = stats.get("close_location_mean")
    if cl is not None:
        print(f"    Close loc:     mean={cl:.3f}, std={stats.get('close_location_std', 0):.3f}")
        print(f"                   <0.22: {stats.get('close_loc_below_022', 0):.1f}%, >0.78: {stats.get('close_loc_above_078', 0):.1f}%")
    rsi = stats.get("rsi_mean")
    if rsi is not None:
        print(f"    RSI:           mean={rsi:.1f}, std={stats.get('rsi_std', 0):.1f}")


if __name__ == "__main__":
    main()
