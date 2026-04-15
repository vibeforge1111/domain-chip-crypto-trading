"""Strategy Forge — improve proven strategies with indicator-enriched mutations.

Four-stage loop:
  1. Generate: Read proven champions → generate indicator mutations
  2. Screen:   Backtest ONLY new mutations (WF=1.0 gate)
  3. Promote:  Winners → paper trade queue
  4. Report:   Score and summarize results

Key differences from autoloop:
  - No doctrine card discovery — only enriches existing strategies
  - Backtests ONLY forge mutations (fast: minutes vs hours)
  - Auto-commits after every stage
  - Separate artifacts/forge/ directory
"""
from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys
import time

# Fix Windows charmap encoding for background processes
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
os.environ["PYTHONIOENCODING"] = "utf-8"
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
SCRIPTS_ROOT = REPO_ROOT / "scripts"
FORGE_DIR = REPO_ROOT / "artifacts" / "forge"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from domain_chip_crypto_trading.cli import evaluate
from generate_indicator_mutations import generate_indicator_mutations
from build_paper_trade_queue import build_paper_trade_queue


def _load_json(path: Path, fallback: Any = None) -> Any:
    if fallback is None:
        fallback = {}
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git_commit(message: str) -> bool:
    """Stage forge artifacts and commit."""
    paths_to_stage = [
        "artifacts/forge/",
        "artifacts/backtests/",
        "artifacts/paper_trade/",
        "spark-researcher.project.json",
    ]
    try:
        subprocess.run(
            ["git", "add", "-f", "--", *paths_to_stage],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
        staged = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=REPO_ROOT,
        )
        if staged.returncode == 0:
            return False
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


# ── Stage 1: Generate ────────────────────────────────────────────────

def stage_generate(*, singles: bool = True, pairs: bool = True) -> dict[str, Any]:
    """Generate indicator-enriched mutations from proven champions."""
    print("[Forge] Stage 1: Generating indicator mutations...")
    report = generate_indicator_mutations(
        REPO_ROOT,
        singles=singles,
        pairs=pairs,
        append_to_config=True,
    )
    print(f"  Generated {report.get('total_generated', 0)} mutations "
          f"({report.get('single_mutations', 0)} singles, {report.get('pair_mutations', 0)} pairs)")
    return report


# ── Stage 2: Screen ──────────────────────────────────────────────────

def stage_screen(wf_gate: float = 0.8, min_trades: int = 0) -> dict[str, Any]:
    """Backtest ONLY forge mutations. Filter by WF gate only."""
    print("[Forge] Stage 2: Screening forge mutations via backtest...")

    # Load forge candidates from indicator_mutations.json OR from config
    mutations_path = FORGE_DIR / "indicator_mutations.json"
    mutations_data = _load_json(mutations_path)
    candidates = mutations_data.get("candidates", [])

    # Fallback: if indicator_mutations.json is empty (dedup skipped all),
    # load forge candidates from project config (source=forge)
    if not candidates:
        config_path = REPO_ROOT / "spark-researcher.project.json"
        config = _load_json(config_path)
        candidates = [
            t for t in config.get("candidate_trials", [])
            if isinstance(t, dict) and t.get("mutations", {}).get("source") == "forge"
        ]

    if not candidates:
        print("  No candidates to screen.")
        return {"screened": 0, "winners": [], "material_change": False}

    # Load existing screen results to support incremental screening
    screen_path = FORGE_DIR / "screen_results.json"
    existing_screen = _load_json(screen_path)
    cache: dict[str, dict] = {}
    for row in existing_screen.get("rows", []):
        if isinstance(row, dict) and row.get("candidate_id"):
            cache[row["candidate_id"]] = row

    rows: list[dict[str, Any]] = []
    evaluated = 0
    cached = 0
    winners: list[dict[str, Any]] = []

    for i, candidate in enumerate(candidates):
        cid = candidate.get("candidate_id", f"unknown-{i}")
        mutations = candidate.get("mutations", {})

        # Check cache
        if cid in cache:
            rows.append(cache[cid])
            cached += 1
            result = cache[cid].get("result", {})
            if float(result.get("walk_forward_consistency", 0) or 0) >= wf_gate:
                winners.append(cache[cid])
            continue

        # Run backtest
        try:
            payload = {
                "runtime_root": str(REPO_ROOT),
                "candidate": candidate,
            }
            outcome = evaluate(payload)
            metrics = outcome.get("metrics", {})
            result = outcome.get("result", {})

            row = {
                "candidate_id": cid,
                "mutations": mutations,
                "metrics": metrics,
                "result": result,
                "forge_metadata": candidate.get("forge_metadata", {}),
                "screened_at": _now_iso(),
            }
            rows.append(row)
            evaluated += 1

            wf = float(result.get("walk_forward_consistency", 0) or 0)
            wr = float(metrics.get("win_rate", 0) or 0)
            trades = int(result.get("trade_count", 0) or 0)

            status = "PASS" if wf >= wf_gate and trades >= min_trades else "FAIL"
            print(f"  [{evaluated}/{len(candidates)}] {cid}: WR={wr:.3f}, WF={wf:.1f}, "
                  f"trades={trades} → {status}")

            if wf >= wf_gate and trades >= min_trades:
                winners.append(row)

        except Exception as exc:
            print(f"  [{evaluated}/{len(candidates)}] {cid}: ERROR — {exc}")
            rows.append({
                "candidate_id": cid,
                "mutations": mutations,
                "error": str(exc),
                "screened_at": _now_iso(),
            })
            evaluated += 1

    # Save screen results
    screen_output = {
        "screened_at": _now_iso(),
        "total_screened": len(rows),
        "evaluated": evaluated,
        "cached": cached,
        "wf_gate": wf_gate,
        "min_trades": min_trades,
        "winner_count": len(winners),
        "rows": rows,
    }
    _write_json(screen_path, screen_output)

    print(f"  Screen complete: {len(winners)} winners from {len(rows)} candidates "
          f"({evaluated} evaluated, {cached} cached)")

    return {
        "screened": len(rows),
        "evaluated": evaluated,
        "cached": cached,
        "winners": winners,
        "material_change": len(winners) > 0,
    }


# ── Stage 3: Promote ─────────────────────────────────────────────────

def stage_promote(winners: list[dict[str, Any]]) -> dict[str, Any]:
    """Promote winning forge candidates to paper trade queue."""
    print(f"[Forge] Stage 3: Promoting {len(winners)} winners to paper trade...")

    if not winners:
        print("  No winners to promote.")
        return {"promoted": 0, "material_change": False}

    promoted = 0
    for winner in winners:
        cid = winner.get("candidate_id", "unknown")
        mutations = winner.get("mutations", {})
        metrics = winner.get("metrics", {})
        result = winner.get("result", {})

        # Write a bridge packet so build_paper_trade_queue picks it up
        packet = {
            "candidate_id": cid,
            "run_id": f"forge-{_now_iso()}",
            "doctrine_id": str(mutations.get("doctrine_id", "")),
            "strategy_id": str(mutations.get("strategy_id", "")),
            "market_regime": str(mutations.get("market_regime", "")),
            "timeframe": str(mutations.get("timeframe", "15m")),
            "venue": str(mutations.get("venue", "bybit")),
            "asset_universe": str(mutations.get("asset_universe", "")),
            "mutations": mutations,
            "profitability_score": metrics.get("profitability_score"),
            "paper_trade_readiness": metrics.get("paper_trade_readiness"),
            "max_drawdown": metrics.get("max_drawdown"),
            "trade_count": result.get("trade_count"),
            "minimum_trade_count": result.get("minimum_trade_count"),
            "trade_count_gate_pass": result.get("trade_count_gate_pass"),
            "holdout_profitability_score": result.get("holdout_profitability_score"),
            "walk_forward_consistency": result.get("walk_forward_consistency"),
            "stress_resilience": result.get("stress_resilience"),
            "eligibility_status": "forge_promoted",
            "recommended_next_step": "paper_trade_validation",
            "primary_mechanism": result.get("mechanism", "forge indicator enrichment"),
            "primary_boundary": result.get("boundary", ""),
            "forge_metadata": winner.get("forge_metadata", {}),
        }

        packet_dir = REPO_ROOT / "artifacts" / "bridge_packets"
        packet_dir.mkdir(parents=True, exist_ok=True)
        packet_path = packet_dir / f"{cid}.json"
        _write_json(packet_path, packet)
        promoted += 1
        print(f"  Promoted: {cid}")

    # Rebuild paper trade queue to include new candidates
    try:
        build_paper_trade_queue(REPO_ROOT)
        print(f"  Paper trade queue rebuilt.")
    except Exception as exc:
        print(f"  Warning: queue rebuild failed: {exc}")

    return {"promoted": promoted, "material_change": promoted > 0}


# ── Stage 4: Report ──────────────────────────────────────────────────

def stage_report(
    gen_report: dict[str, Any],
    screen_report: dict[str, Any],
    promote_report: dict[str, Any],
    cycle_number: int,
) -> dict[str, Any]:
    """Generate forge cycle summary report."""
    print("[Forge] Stage 4: Generating report...")

    winners = screen_report.get("winners", [])
    report = {
        "forge_cycle": cycle_number,
        "completed_at": _now_iso(),
        "stages": {
            "generate": {
                "mutations_created": gen_report.get("total_generated", 0),
                "champions_processed": gen_report.get("champions_processed", 0),
            },
            "screen": {
                "total_screened": screen_report.get("screened", 0),
                "evaluated": screen_report.get("evaluated", 0),
                "cached": screen_report.get("cached", 0),
                "winners": len(winners),
            },
            "promote": {
                "promoted": promote_report.get("promoted", 0),
            },
        },
        "winners": [
            {
                "candidate_id": w.get("candidate_id"),
                "win_rate": (w.get("metrics", {}) or {}).get("win_rate"),
                "walk_forward_consistency": (w.get("result", {}) or {}).get("walk_forward_consistency"),
                "trade_count": (w.get("result", {}) or {}).get("trade_count"),
                "max_drawdown": (w.get("metrics", {}) or {}).get("max_drawdown"),
                "sharpe_ratio": (w.get("metrics", {}) or {}).get("sharpe_ratio"),
                "base_champion": (w.get("forge_metadata", {}) or {}).get("base_champion"),
                "indicator_guard": (w.get("forge_metadata", {}) or {}).get("indicator_guard"),
            }
            for w in winners
        ],
        "material_change": len(winners) > 0,
    }

    _write_json(FORGE_DIR / "forge_cycle_report.json", report)

    # Append to forge journal
    journal_path = FORGE_DIR / "forge_journal.jsonl"
    with open(journal_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(report, sort_keys=True) + "\n")

    print(f"  Forge cycle {cycle_number} complete: "
          f"{gen_report.get('total_generated', 0)} generated → "
          f"{screen_report.get('screened', 0)} screened → "
          f"{len(winners)} winners → "
          f"{promote_report.get('promoted', 0)} promoted")

    return report


# ── State management ─────────────────────────────────────────────────

def _forge_state_path() -> Path:
    return FORGE_DIR / "forge_state.json"


def _load_forge_state() -> dict[str, Any]:
    return _load_json(_forge_state_path())


def _save_forge_state(state: dict[str, Any]) -> None:
    _write_json(_forge_state_path(), state)


# ── Main forge loop ──────────────────────────────────────────────────

def run_forge_cycle(
    cycle_number: int,
    *,
    singles: bool = True,
    pairs: bool = True,
    wf_gate: float = 0.8,
    min_trades: int = 50,
    auto_commit: bool = True,
) -> dict[str, Any]:
    """Run a single forge cycle (generate → screen → promote → report)."""
    started_at = _now_iso()
    t0 = time.time()

    # Stage 1: Generate
    gen_report = stage_generate(singles=singles, pairs=pairs)
    if auto_commit:
        _git_commit(f"Forge cycle {cycle_number}: generate {gen_report.get('total_generated', 0)} mutations")

    # Stage 2: Screen
    screen_report = stage_screen(wf_gate=wf_gate, min_trades=min_trades)
    if auto_commit:
        _git_commit(f"Forge cycle {cycle_number}: screen {screen_report.get('screened', 0)} candidates")

    # Stage 3: Promote
    winners = screen_report.get("winners", [])
    promote_report = stage_promote(winners)
    if auto_commit:
        _git_commit(f"Forge cycle {cycle_number}: promote {promote_report.get('promoted', 0)} winners")

    # Stage 4: Report
    report = stage_report(gen_report, screen_report, promote_report, cycle_number)
    elapsed = time.time() - t0

    # Update forge state
    state = _load_forge_state()
    state["cycle_count"] = cycle_number
    state["last_cycle_at"] = _now_iso()
    state["last_winners"] = len(winners)
    state["total_screened"] = state.get("total_screened", 0) + screen_report.get("evaluated", 0)
    state["total_promoted"] = state.get("total_promoted", 0) + promote_report.get("promoted", 0)
    state["elapsed_seconds"] = round(elapsed, 1)
    _save_forge_state(state)

    if auto_commit:
        _git_commit(f"Forge cycle {cycle_number}: complete ({len(winners)} winners, {elapsed:.0f}s)")

    print(f"\n{'='*60}")
    print(f"Forge cycle {cycle_number} finished in {elapsed:.0f}s")
    print(f"{'='*60}\n")

    return report


def run_forge_loop(
    max_cycles: int = 1,
    sleep_seconds: int = 60,
    **kwargs: Any,
) -> None:
    """Run multiple forge cycles."""
    state = _load_forge_state()
    start_cycle = int(state.get("cycle_count", 0) or 0) + 1

    for i in range(max_cycles):
        cycle_number = start_cycle + i
        print(f"\n{'#'*60}")
        print(f"# Forge Cycle {cycle_number}")
        print(f"{'#'*60}\n")

        try:
            run_forge_cycle(cycle_number, **kwargs)
        except Exception as exc:
            print(f"Forge cycle {cycle_number} failed: {exc}")
            import traceback
            traceback.print_exc()

        if i < max_cycles - 1:
            print(f"Sleeping {sleep_seconds}s before next cycle...")
            time.sleep(sleep_seconds)


def main() -> None:
    parser = argparse.ArgumentParser(description="Strategy Forge — improve proven strategies with indicator mutations")
    parser.add_argument("--cycles", type=int, default=1, help="Number of forge cycles to run (default: 1)")
    parser.add_argument("--sleep", type=int, default=60, help="Sleep seconds between cycles (default: 60)")
    parser.add_argument("--wf-gate", type=float, default=1.0, help="Walk-forward consistency gate (default: 1.0)")
    parser.add_argument("--min-trades", type=int, default=0, help="Minimum trade count gate (default: 0, WF is sole gate)")
    parser.add_argument("--no-pairs", action="store_true", help="Skip pair guard mutations")
    parser.add_argument("--no-commit", action="store_true", help="Skip git commits")
    args = parser.parse_args()

    run_forge_loop(
        max_cycles=args.cycles,
        sleep_seconds=args.sleep,
        singles=True,
        pairs=not args.no_pairs,
        wf_gate=args.wf_gate,
        min_trades=args.min_trades,
        auto_commit=not args.no_commit,
    )


if __name__ == "__main__":
    main()
