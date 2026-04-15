"""Live signal engine for the compression-bounce-wick-skip-toxic strategy.

Generates real-time trading signals by:
1. Loading the latest candle data
2. Running the signal engine against current market conditions
3. Outputting actionable trade signals with position sizing

Usage:
    python scripts/live_signal_engine.py                    # Check current signal
    python scripts/live_signal_engine.py --watch             # Continuous monitoring
    python scripts/live_signal_engine.py --backtest-latest   # Backtest recent performance
    python scripts/live_signal_engine.py --all-strategies    # Check all approved strategies
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from domain_chip_crypto_trading.backtest import (
    _candles,
    _contracts,
    _window_candles,
    _feature_row,
    _detected_regime,
    _signal,
    run_backtest,
    run_paper_trade_validation,
    data_paths,
    paper_trade_data_paths,
)


# Champion strategy mutations
STRATEGIES = {
    "compression-bounce-wick-skip-toxic": {
        "asset_universe": "BTC,SOL",
        "doctrine_id": "compression_mean_reversion",
        "execution_buffer": "high",
        "market_regime": "compression",
        "paper_gate": "balanced",
        "session_quality_filter": "skip_compression_toxic",
        "strategy_id": "compression_range_bounce",
        "timeframe": "15m",
        "venue": "bybit",
    },
    "compression-bounce-wick-skip-toxic-tight-squeeze": {
        "asset_universe": "BTC,ETH,SOL",
        "compression_profile": "tight_squeeze",
        "doctrine_id": "compression_mean_reversion",
        "execution_buffer": "high",
        "market_regime": "compression",
        "paper_gate": "balanced",
        "session_quality_filter": "skip_compression_toxic",
        "strategy_id": "compression_range_bounce",
        "timeframe": "15m",
        "venue": "bybit",
    },
    "compression-bounce-wick-toxic-thin": {
        "asset_universe": "BTC,ETH,SOL",
        "doctrine_id": "compression_mean_reversion",
        "execution_buffer": "high",
        "market_regime": "compression",
        "paper_gate": "balanced",
        "session_quality_filter": "skip_compression_toxic",
        "strategy_id": "compression_range_bounce",
        "timeframe": "15m",
        "venue": "bybit",
        "volume_context_guard": "thin_filter",
    },
    # Session 15 WF=1.0 candidates
    "compression-bounce-loose-setup": {
        "asset_universe": "BTC,SOL",
        "cr_loose_setup": "skip_marginal",
        "doctrine_id": "compression_mean_reversion",
        "execution_buffer": "high",
        "market_regime": "compression",
        "paper_gate": "balanced",
        "session_quality_filter": "skip_compression_toxic",
        "strategy_id": "compression_range_bounce",
        "timeframe": "15m",
        "venue": "bybit",
    },
    "compression-bounce-down-in-downtrend": {
        "asset_universe": "BTC,SOL",
        "cr_down_in_downtrend": "skip_deep",
        "doctrine_id": "compression_mean_reversion",
        "execution_buffer": "high",
        "market_regime": "compression",
        "paper_gate": "balanced",
        "session_quality_filter": "skip_compression_toxic",
        "strategy_id": "compression_range_bounce",
        "timeframe": "15m",
        "venue": "bybit",
    },
    "compression-bounce-downtrend-high-pos": {
        "asset_universe": "BTC,SOL",
        "cr_downtrend_high_pos": "skip",
        "doctrine_id": "compression_mean_reversion",
        "execution_buffer": "high",
        "market_regime": "compression",
        "paper_gate": "balanced",
        "session_quality_filter": "skip_compression_toxic",
        "strategy_id": "compression_range_bounce",
        "timeframe": "15m",
        "venue": "bybit",
    },
    "compression-bounce-wick-guard": {
        "asset_universe": "BTC,SOL",
        "cr_wick_guard": "reject_high",
        "doctrine_id": "compression_mean_reversion",
        "execution_buffer": "high",
        "market_regime": "compression",
        "paper_gate": "balanced",
        "session_quality_filter": "skip_compression_toxic",
        "strategy_id": "compression_range_bounce",
        "timeframe": "15m",
        "venue": "bybit",
    },
    "compression-bounce-volume-cap": {
        "asset_universe": "BTC,SOL",
        "cr_volume_cap": "spike_skip",
        "doctrine_id": "compression_mean_reversion",
        "execution_buffer": "high",
        "market_regime": "compression",
        "paper_gate": "balanced",
        "session_quality_filter": "skip_compression_toxic",
        "strategy_id": "compression_range_bounce",
        "timeframe": "15m",
        "venue": "bybit",
    },
}

# Backtest performance for position sizing
STRATEGY_STATS = {
    "compression-bounce-wick-skip-toxic": {"backtest_wr": 0.645, "backtest_dd": 0.094, "sharpe": 3.89, "wf": 1.0},
    "compression-bounce-wick-skip-toxic-tight-squeeze": {"backtest_wr": 0.665, "backtest_dd": 0.085, "sharpe": 3.92, "wf": 0.6},
    "compression-bounce-wick-toxic-thin": {"backtest_wr": 0.643, "backtest_dd": 0.139, "sharpe": 3.32, "wf": 0.6},
    # Session 15 WF=1.0 candidates (BTC backtest)
    "compression-bounce-loose-setup": {"backtest_wr": 0.665, "backtest_dd": 0.091, "sharpe": 4.28, "wf": 1.0},
    "compression-bounce-down-in-downtrend": {"backtest_wr": 0.660, "backtest_dd": 0.085, "sharpe": 4.04, "wf": 1.0},
    "compression-bounce-downtrend-high-pos": {"backtest_wr": 0.668, "backtest_dd": 0.085, "sharpe": 4.44, "wf": 1.0},
    "compression-bounce-wick-guard": {"backtest_wr": 0.651, "backtest_dd": 0.095, "sharpe": 3.61, "wf": 1.0},
    "compression-bounce-volume-cap": {"backtest_wr": 0.654, "backtest_dd": 0.092, "sharpe": 4.06, "wf": 1.0},
}


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _kelly_fraction(win_rate: float, payout_ratio: float = 1.0) -> float:
    """Kelly criterion for optimal position sizing."""
    if win_rate <= 0 or win_rate >= 1:
        return 0.0
    edge = win_rate * payout_ratio - (1 - win_rate)
    if edge <= 0:
        return 0.0
    return edge / payout_ratio


def _ledger_stats(strategy_id: str) -> dict[str, Any]:
    """Read cumulative ledger stats for a strategy."""
    ledger_path = REPO_ROOT / "artifacts" / "paper_trade" / "ledger" / f"{strategy_id}.jsonl"
    if not ledger_path.exists():
        return {}
    trades = []
    for line in ledger_path.read_text(encoding="utf-8").strip().split("\n"):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("prediction") == "skip":
            continue
        trades.append(entry)

    if not trades:
        return {"trade_count": 0}

    wins = sum(1 for t in trades if t.get("correct"))
    wr = round(wins / len(trades), 4) if trades else 0
    returns = [t.get("realized_return", 0) for t in trades]
    cumulative = round(sum(returns), 2)

    # Max drawdown calculation
    peak = 0.0
    running = 0.0
    max_dd = 0.0
    for r in returns:
        running += r
        if running > peak:
            peak = running
        dd = peak - running
        if dd > max_dd:
            max_dd = dd

    # Per-asset breakdown
    asset_stats: dict[str, dict[str, Any]] = {}
    for t in trades:
        a = t.get("asset", "unknown")
        if a not in asset_stats:
            asset_stats[a] = {"wins": 0, "total": 0}
        asset_stats[a]["total"] += 1
        if t.get("correct"):
            asset_stats[a]["wins"] += 1
    for a, s in asset_stats.items():
        s["win_rate"] = round(s["wins"] / s["total"], 4) if s["total"] > 0 else 0

    # Recent performance (last 20 trades)
    recent = trades[-20:]
    recent_wins = sum(1 for t in recent if t.get("correct"))
    recent_wr = round(recent_wins / len(recent), 4) if recent else 0

    return {
        "trade_count": len(trades),
        "win_rate": wr,
        "cumulative_return": cumulative,
        "max_drawdown_absolute": round(max_dd, 2),
        "recent_20_win_rate": recent_wr,
        "recent_20_count": len(recent),
        "per_asset": asset_stats,
        "latest_trade": trades[-1].get("contract_id", "") if trades else "",
        "latest_trade_ts": trades[-1].get("open_ts", "") if trades else "",
    }


def _position_size(bankroll: float, strategy_id: str, confidence: float = 1.0) -> float:
    """Calculate position size using fractional Kelly."""
    stats = STRATEGY_STATS.get(strategy_id, {})
    wr = stats.get("backtest_wr", 0.5)
    kelly = _kelly_fraction(wr)
    # Use quarter-Kelly for conservative sizing
    fraction = kelly * 0.25 * confidence
    return round(bankroll * fraction, 2)


def check_current_signal(strategy_id: str = "compression-bounce-wick-skip-toxic", asset: str = "btc") -> dict[str, Any]:
    """Check the current signal for a given strategy and asset."""
    mutations = STRATEGIES.get(strategy_id, {})
    if not mutations:
        return {"error": f"Unknown strategy: {strategy_id}"}

    candle_path, contract_path = data_paths(REPO_ROOT, asset=asset, timeframe="15m")
    if not candle_path.exists():
        return {"error": f"No candle data for {asset}"}

    candles = _candles(candle_path)
    if not candles:
        return {"error": "No candles loaded"}

    # Get the last few contracts to analyze current conditions
    contracts = _contracts(contract_path)
    if not contracts:
        return {"error": "No contracts loaded"}

    # Analyze the most recent contracts
    candle_times = [c.ts.timestamp() for c in candles]
    recent_contracts = contracts[-10:]
    signals = []

    for contract in recent_contracts:
        lookback = _window_candles(candles, candle_times, contract)
        if len(lookback) < 5:
            continue
        features = _feature_row(lookback, contract)
        regime = _detected_regime(features)
        signal = _signal(mutations, features)
        actual = contract.settlement_direction

        signals.append({
            "contract_id": contract.contract_id,
            "open_ts": contract.open_ts.isoformat().replace("+00:00", "Z"),
            "regime": regime,
            "signal": signal,
            "actual": actual,
            "correct": signal == actual if signal != "skip" else None,
            "features": {
                "compression_ratio": round(features.get("compression_ratio", 0), 4),
                "close_location": round(features.get("close_location", 0), 4),
                "rsi": round(features.get("rsi", 0), 1),
                "volume_ratio": round(features.get("volume_ratio", 0), 3),
                "momentum": round(features.get("momentum", 0), 6),
                "lower_wick_ratio": round(features.get("lower_wick_ratio", 0), 3),
                "upper_wick_ratio": round(features.get("upper_wick_ratio", 0), 3),
                "session_hour": int(features.get("session_hour", 0)),
            },
        })

    # Calculate recent performance
    active_signals = [s for s in signals if s["signal"] != "skip"]
    recent_wr = 0
    if active_signals:
        wins = sum(1 for s in active_signals if s.get("correct"))
        recent_wr = round(wins / len(active_signals), 3)

    latest = signals[-1] if signals else {}
    stats = STRATEGY_STATS.get(strategy_id, {})

    return {
        "strategy_id": strategy_id,
        "asset": asset.upper(),
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "latest_signal": latest.get("signal", "unknown"),
        "latest_regime": latest.get("regime", "unknown"),
        "latest_contract": latest.get("contract_id", ""),
        "latest_features": latest.get("features", {}),
        "recent_10_signals": signals,
        "recent_active_count": len(active_signals),
        "recent_win_rate": recent_wr,
        "backtest_stats": stats,
        "position_sizing": {
            "kelly_full": round(_kelly_fraction(stats.get("backtest_wr", 0.5)), 4),
            "kelly_quarter": round(_kelly_fraction(stats.get("backtest_wr", 0.5)) * 0.25, 4),
            "example_100_bankroll": _position_size(100, strategy_id),
            "example_1000_bankroll": _position_size(1000, strategy_id),
        },
    }


def full_strategy_report() -> dict[str, Any]:
    """Generate a full P&L report across all approved strategies."""
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "strategies": {},
        "portfolio_signals": [],
    }

    # Load paper trade monitor for readiness data
    monitor = _load_json(REPO_ROOT / "artifacts" / "paper_trade" / "paper_trade_monitor_report.json", {})
    monitor_candidates = {c["candidate_id"]: c for c in monitor.get("candidates", [])}

    for strategy_id, mutations in STRATEGIES.items():
        # Run backtest
        bt = run_backtest(mutations, REPO_ROOT)

        strategy_report = {
            "strategy_id": strategy_id,
            "mutations": mutations,
        }

        if bt:
            strategy_report["backtest"] = {
                "win_rate": bt.get("win_rate", 0),
                "profitability_score": bt.get("profitability_score", 0),
                "max_drawdown": bt.get("max_drawdown", 0),
                "trade_count": bt.get("trade_count", 0),
                "walk_forward_consistency": bt.get("walk_forward_consistency", 0),
                "stress_resilience": bt.get("stress_resilience", 0),
                "paper_trade_readiness": bt.get("paper_trade_readiness", 0),
                "verdict": bt.get("verdict", "unknown"),
                "sharpe_ratio": bt.get("sharpe_ratio", 0),
            }

        # Use cumulative ledger stats instead of re-running paper trade
        ledger = _ledger_stats(strategy_id)
        if ledger.get("trade_count", 0) > 0:
            mc = monitor_candidates.get(strategy_id, {})
            strategy_report["paper_trade_cumulative"] = {
                "trade_count": ledger["trade_count"],
                "win_rate": ledger["win_rate"],
                "cumulative_return": ledger["cumulative_return"],
                "max_drawdown_absolute": ledger["max_drawdown_absolute"],
                "recent_20_win_rate": ledger["recent_20_win_rate"],
                "per_asset": ledger["per_asset"],
                "latest_trade": ledger["latest_trade"],
                "readiness": mc.get("readiness", "unknown"),
                "recommendation": mc.get("paper_trade_recommendation", "unknown"),
                "trades_remaining": mc.get("trades_remaining", 0),
                "estimated_days_remaining": mc.get("estimated_days_remaining", 0),
                "win_rate_ci": [mc.get("win_rate_ci_lower", 0), mc.get("win_rate_ci_upper", 0)],
            }

        report["strategies"][strategy_id] = strategy_report

        # Get current signals for each asset
        raw_universe = mutations.get("asset_universe", "BTC")
        assets = [a.strip().lower() for a in raw_universe.split(",") if a.strip()]
        for asset in assets:
            sig = check_current_signal(strategy_id, asset)
            if sig.get("latest_signal") and sig["latest_signal"] != "skip":
                report["portfolio_signals"].append({
                    "strategy_id": strategy_id,
                    "asset": asset.upper(),
                    "signal": sig["latest_signal"],
                    "regime": sig.get("latest_regime", ""),
                    "contract": sig.get("latest_contract", ""),
                })

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Live signal engine for crypto trading strategies.")
    parser.add_argument("--strategy", type=str, default="compression-bounce-wick-skip-toxic",
                        help="Strategy to check")
    parser.add_argument("--asset", type=str, default="btc", help="Asset to check")
    parser.add_argument("--all-strategies", action="store_true", help="Run full strategy report")
    parser.add_argument("--watch", action="store_true", help="Continuous monitoring mode")
    parser.add_argument("--interval", type=int, default=300, help="Watch interval in seconds")
    parser.add_argument("--bankroll", type=float, default=1000.0, help="Bankroll for position sizing")
    args = parser.parse_args()

    if args.all_strategies:
        report = full_strategy_report()
        report_path = REPO_ROOT / "artifacts" / "live_signals" / "full_strategy_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        print("\n" + "=" * 72)
        print("FULL STRATEGY P&L REPORT")
        print("=" * 72)
        for sid, sdata in report["strategies"].items():
            bt = sdata.get("backtest", {})
            ptc = sdata.get("paper_trade_cumulative", {})
            print(f"\n{sid}:")
            if bt:
                print(f"  Backtest:    WR={bt.get('win_rate',0):.3f}  DD={bt.get('max_drawdown',0):.3f}  WF={bt.get('walk_forward_consistency',0):.1f}  Sharpe={bt.get('sharpe_ratio',0):.2f}  [{bt.get('verdict','?')}]")
            if ptc:
                print(f"  Paper Trade: WR={ptc.get('win_rate',0):.3f}  trades={ptc.get('trade_count',0)}  cum_return={ptc.get('cumulative_return',0):+.2f}  recent20_WR={ptc.get('recent_20_win_rate',0):.3f}  [{ptc.get('recommendation','?')}]")
                pa = ptc.get("per_asset", {})
                if pa:
                    parts = [f"{a.upper()}={s.get('win_rate',0):.3f}({s.get('total',0)})" for a, s in pa.items()]
                    print(f"               Per-asset: {', '.join(parts)}")
                print(f"               Readiness: {ptc.get('readiness','?')}  trades_remaining={ptc.get('trades_remaining',0)}  est_days={ptc.get('estimated_days_remaining',0):.0f}")

        if report.get("portfolio_signals"):
            print(f"\nACTIVE SIGNALS:")
            for sig in report["portfolio_signals"]:
                print(f"  {sig['strategy_id']} | {sig['asset']} | {sig['signal'].upper()} | {sig['regime']} | {sig['contract']}")
        else:
            print("\nNo active signals right now.")

        print(f"\nReport saved: {report_path}")
        return

    if args.watch:
        print(f"[watch] Monitoring {args.strategy} on {args.asset.upper()} every {args.interval}s...")
        while True:
            result = check_current_signal(args.strategy, args.asset)
            ts = result.get("checked_at", "")
            sig = result.get("latest_signal", "?")
            regime = result.get("latest_regime", "?")
            contract = result.get("latest_contract", "")
            pos = _position_size(args.bankroll, args.strategy)
            print(f"[{ts}] {args.asset.upper()} regime={regime} signal={sig.upper()} contract={contract} position=${pos:.2f}")
            time.sleep(args.interval)
    else:
        result = check_current_signal(args.strategy, args.asset)
        print("\n" + "=" * 72)
        print(f"LIVE SIGNAL CHECK: {args.strategy}")
        print("=" * 72)
        print(f"Asset: {result.get('asset', '?')}")
        print(f"Checked: {result.get('checked_at', '?')}")
        print(f"Latest Signal: {result.get('latest_signal', '?').upper()}")
        print(f"Latest Regime: {result.get('latest_regime', '?')}")
        print(f"Latest Contract: {result.get('latest_contract', '?')}")
        print()
        features = result.get("latest_features", {})
        if features:
            print("Market Features:")
            print(f"  Compression Ratio: {features.get('compression_ratio', '?')}")
            print(f"  Close Location:    {features.get('close_location', '?')}")
            print(f"  RSI:               {features.get('rsi', '?')}")
            print(f"  Volume Ratio:      {features.get('volume_ratio', '?')}")
            print(f"  Momentum:          {features.get('momentum', '?')}")
            print(f"  Lower Wick:        {features.get('lower_wick_ratio', '?')}")
            print(f"  Upper Wick:        {features.get('upper_wick_ratio', '?')}")
            print(f"  Session Hour:      {features.get('session_hour', '?')}")
        print()
        stats = result.get("backtest_stats", {})
        print(f"Backtest Edge: WR={stats.get('backtest_wr', '?')} DD={stats.get('backtest_dd', '?')} Sharpe={stats.get('sharpe', '?')}")
        print(f"Recent 10 Active: {result.get('recent_active_count', 0)} trades, WR={result.get('recent_win_rate', '?')}")
        print()
        ps = result.get("position_sizing", {})
        print("Position Sizing (Quarter-Kelly):")
        print(f"  Full Kelly:     {ps.get('kelly_full', '?'):.1%}")
        print(f"  Quarter Kelly:  {ps.get('kelly_quarter', '?'):.1%}")
        print(f"  $100 bankroll:  ${ps.get('example_100_bankroll', 0):.2f}")
        print(f"  $1000 bankroll: ${ps.get('example_1000_bankroll', 0):.2f}")

        # Save signal
        sig_path = REPO_ROOT / "artifacts" / "live_signals" / "latest_signal.json"
        sig_path.parent.mkdir(parents=True, exist_ok=True)
        sig_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"\nSignal saved: {sig_path}")


if __name__ == "__main__":
    main()
