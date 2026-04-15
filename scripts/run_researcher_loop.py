"""
Researcher loop — triggers spark-researcher whenever the frontier queue is drained.

The autoloop supervisor consumes frontier suggestions and runs backtests.
This script waits for the queue to empty, then re-triggers the researcher
so it can evaluate fresh results and suggest the next round of probes.

Usage:
    python scripts/run_researcher_loop.py
    python scripts/run_researcher_loop.py --interval 600   # check every 10 min
    python scripts/run_researcher_loop.py --rounds 3       # researcher rounds per trigger
"""

import argparse
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FRONTIER = REPO_ROOT / "artifacts" / "frontier" / "queue.json"
STATE = REPO_ROOT / "artifacts" / "recursion" / "autoloop_state.json"


def frontier_queue_size() -> int:
    try:
        data = json.loads(FRONTIER.read_text(encoding="utf-8"))
        return len(data.get("candidate_trials", []))
    except Exception:
        return 0


def current_cycle() -> int:
    try:
        data = json.loads(STATE.read_text(encoding="utf-8"))
        return data.get("cycle_count", 0)
    except Exception:
        return 0


def run_researcher(rounds: int = 3) -> bool:
    """Run spark-researcher autoloop. Returns True if it completed ok."""
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] Triggering researcher ({rounds} rounds)...")
    try:
        result = subprocess.run(
            ["spark-researcher", "autoloop", "--command", "autoloop", "--rounds", str(rounds)],
            cwd=str(REPO_ROOT),
            timeout=300,
            capture_output=True,
            text=True,
        )
        ts2 = datetime.now(timezone.utc).strftime("%H:%M:%S")
        if result.returncode == 0:
            # Parse suggestion count from output
            try:
                data = json.loads(result.stdout)
                total_suggestions = sum(
                    r.get("suggestions", {}).get("suggestion_count", 0)
                    for r in data.get("history", [])
                )
                print(f"[{ts2}] Researcher done — {total_suggestions} suggestions queued")
            except Exception:
                print(f"[{ts2}] Researcher done (exit 0)")
            return True
        else:
            print(f"[{ts2}] Researcher failed (exit {result.returncode})")
            if result.stderr:
                for line in result.stderr.strip().split("\n")[-3:]:
                    print(f"  {line}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[{ts}] Researcher timed out (300s)")
        return False


def main():
    parser = argparse.ArgumentParser(description="Researcher loop — re-triggers on frontier drain")
    parser.add_argument("--interval", type=int, default=600, help="Seconds between checks (default: 600)")
    parser.add_argument("--rounds", type=int, default=3, help="Researcher rounds per trigger (default: 3)")
    parser.add_argument("--min-cycles", type=int, default=5, help="Min autoloop cycles between triggers (default: 5)")
    args = parser.parse_args()

    print(f"Researcher loop started — interval={args.interval}s, rounds={args.rounds}, min_cycles={args.min_cycles}")
    print(f"Watching frontier: {FRONTIER}")
    print()

    last_trigger_cycle = current_cycle()

    while True:
        qsize = frontier_queue_size()
        cycle = current_cycle()
        cycles_since = cycle - last_trigger_cycle
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")

        if qsize == 0 and cycles_since >= args.min_cycles:
            print(f"[{ts}] Frontier empty, {cycles_since} cycles since last trigger — firing researcher")
            ok = run_researcher(args.rounds)
            if ok:
                last_trigger_cycle = cycle
            qsize = frontier_queue_size()
            print(f"[{ts}] Frontier now has {qsize} candidates. Sleeping {args.interval}s...")
        elif qsize > 0:
            print(f"[{ts}] Frontier has {qsize} candidates (cycle {cycle}) — autoloop still processing. Sleeping {args.interval}s...")
        else:
            print(f"[{ts}] Frontier empty but only {cycles_since}/{args.min_cycles} cycles since last trigger. Sleeping {args.interval}s...")

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
