"""Wrapper for spark-researcher: runs crypto-autoloop run-once from project root
and emits metrics in a format the researcher can parse."""
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def main():
    # Always run from project root, not isolated workspace
    result = subprocess.run(
        [sys.executable, "-m", "domain_chip_crypto_trading.autoloop", "run-once"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=300,
    )

    # Forward output
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    # Parse the cycle journal for latest metrics
    summary_path = PROJECT_ROOT / "artifacts" / "backtests" / "heavy_backtest_summary.json"
    state_path = PROJECT_ROOT / "artifacts" / "recursion" / "autoloop_state.json"

    metrics = {"win_rate": 0.0, "walk_forward": 0.0, "trades": 0}

    if summary_path.exists():
        try:
            summary = json.loads(summary_path.read_text())
            candidates = summary.get("candidates", [])
            if candidates:
                best = max(candidates, key=lambda c: c.get("win_rate", 0))
                metrics["win_rate"] = best.get("win_rate", 0)
                metrics["walk_forward"] = best.get("walk_forward", 0)
                metrics["trades"] = best.get("trades", 0)
        except Exception:
            pass

    if state_path.exists():
        try:
            state = json.loads(state_path.read_text())
            metrics["cycle"] = state.get("cycle_number", 0)
        except Exception:
            pass

    # Emit metrics in researcher-parseable format
    print(f"\n--- METRICS ---")
    print(f"win_rate: {metrics['win_rate']}")
    print(f"walk_forward: {metrics['walk_forward']}")
    print(f"trades: {metrics['trades']}")

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
