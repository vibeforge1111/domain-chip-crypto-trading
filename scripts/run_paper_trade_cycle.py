from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from build_paper_trade_queue import build_paper_trade_queue
from build_watchtower import render_watchtower
from safe_write import safe_write_json

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
import sys

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from domain_chip_crypto_trading.backtest import run_paper_trade_validation


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _paper_trade_snapshot(repo_root: Path) -> dict[str, Any]:
    summary = _load_json(repo_root / "artifacts" / "paper_trade" / "paper_trade_summary.json", {})
    summary = summary if isinstance(summary, dict) else {}
    rows = summary.get("rows", [])
    rows = rows if isinstance(rows, list) else []
    top_row = rows[0] if rows and isinstance(rows[0], dict) else {}
    return {
        "queue_count": int(summary.get("queue_count", 0) or 0),
        "executed_candidate_count": int(summary.get("executed_candidate_count", 0) or 0),
        "pending_data_count": int(summary.get("pending_data_count", 0) or 0),
        "top_candidate_id": str(top_row.get("candidate_id", "") or ""),
        "top_status": str(top_row.get("status", "") or ""),
        "top_recommendation": str(top_row.get("paper_trade_recommendation", "") or ""),
    }


def _material_delta(previous: dict[str, Any], current: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    for field in ["queue_count", "executed_candidate_count", "pending_data_count"]:
        if int(previous.get(field, 0) or 0) != int(current.get(field, 0) or 0):
            reasons.append(field)
    for field in ["top_candidate_id", "top_status", "top_recommendation"]:
        if previous.get(field) != current.get(field):
            reasons.append(field)
    return bool(reasons), reasons


def _load_ledger(ledger_path: Path) -> list[dict[str, Any]]:
    """Load existing trade decisions from the cumulative ledger."""
    if not ledger_path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            if isinstance(row, dict):
                entries.append(row)
        except json.JSONDecodeError:
            continue
    return entries


def _append_to_ledger(ledger_path: Path, new_entries: list[dict[str, Any]]) -> None:
    """Append new trade decisions to the cumulative ledger."""
    if not new_entries:
        return
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        for entry in new_entries:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")


def _ledger_summary(all_entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute aggregate stats from the full cumulative ledger.

    Uses the same formulas as backtest.py _profitability/_equity_drawdown
    to ensure consistency between validation and ledger stats.
    """
    trades = [e for e in all_entries if e.get("prediction") != "skip"]
    if not trades:
        return {
            "trade_count": 0,
            "win_rate": 0.0,
            "profitability_score": 0.0,
            "max_drawdown": 0.0,
        }
    wins = sum(1 for t in trades if t.get("correct"))
    returns = [t.get("realized_return", 0.0) for t in trades]

    # Profitability: same as backtest.py _profitability()
    avg_return = sum(returns) / len(returns)
    profitability_score = round(max(0.0, min(0.99, 0.5 + avg_return / 2.0)), 4)

    # Drawdown: same as backtest.py _equity_drawdown()
    equity = 0.0
    peak = 0.0
    worst = 0.0
    for r in returns:
        equity += r
        peak = max(peak, equity)
        worst = min(worst, equity - peak)
    if peak <= 0.0 and worst < 0.0:
        max_dd = min(0.99, abs(worst) / max(1.0, abs(worst)))
    elif peak <= 0.0:
        max_dd = 0.0
    else:
        max_dd = min(0.99, abs(worst) / peak)

    # Regime stats
    regime_buckets: dict[str, dict[str, Any]] = {}
    for t in trades:
        regime = t.get("detected_regime", "unknown")
        bucket = regime_buckets.setdefault(regime, {"trades": 0, "wins": 0, "returns": []})
        bucket["trades"] += 1
        if t.get("correct"):
            bucket["wins"] += 1
        bucket["returns"].append(t.get("realized_return", 0.0))
    regime_stats = {}
    for regime, bucket in regime_buckets.items():
        avg_ret = sum(bucket["returns"]) / max(1, len(bucket["returns"]))
        regime_stats[regime] = {
            "trades": bucket["trades"],
            "win_rate": round(bucket["wins"] / max(1, bucket["trades"]), 4),
            "avg_return": round(avg_ret, 4),
        }

    trade_count = len(trades)
    win_rate = round(wins / trade_count, 4)

    # Paper-trade recommendation: same logic as backtest.py
    _dd_ref_n = 500
    _dd_base = 0.22
    dd_gate = min(0.8, _dd_base * (_dd_ref_n / max(1, trade_count)) ** 0.5)
    recommendation = (
        "advance_toward_live_readiness"
        if profitability_score >= 0.53 and win_rate >= 0.53 and max_dd <= dd_gate and trade_count >= 20
        else "collect_more_paper_data"
        if trade_count < 30 or (profitability_score >= 0.48 and win_rate >= 0.45)
        else "demote_to_benchmark"
    )

    return {
        "trade_count": trade_count,
        "win_rate": win_rate,
        "profitability_score": profitability_score,
        "max_drawdown": round(max_dd, 4),
        "regime_stats": regime_stats,
        "paper_trade_recommendation": recommendation,
    }


def run_paper_trade_cycle(repo_root: Path, max_candidates_per_cycle: int = 50) -> Path:
    queue_path = build_paper_trade_queue(repo_root)
    queue_payload = _load_json(queue_path, {})
    queue_payload = queue_payload if isinstance(queue_payload, dict) else {}
    queue_rows = queue_payload.get("rows", [])
    queue_rows = queue_rows if isinstance(queue_rows, list) else []

    paper_root = repo_root / "artifacts" / "paper_trade"
    ledger_root = paper_root / "ledger"
    ledger_root.mkdir(parents=True, exist_ok=True)
    runs_root = paper_root / "runs"
    runs_root.mkdir(parents=True, exist_ok=True)
    for path in runs_root.glob("*.json"):
        path.unlink()

    # Rotate through queue: prioritize candidates with fewest ledger trades,
    # so new candidates get evaluated while established ones accumulate slower
    rotation_path = paper_root / "rotation_offset.json"
    rotation_state = _load_json(rotation_path, {})
    rotation_state = rotation_state if isinstance(rotation_state, dict) else {}
    offset = int(rotation_state.get("offset", 0) or 0)

    if len(queue_rows) > max_candidates_per_cycle:
        # Sort by ledger trade count (ascending) so under-evaluated candidates go first
        for row in queue_rows:
            cid = str(row.get("candidate_id", "")).strip()
            ledger_file = ledger_root / f"{cid}.jsonl"
            row["_ledger_trades"] = sum(1 for _ in open(ledger_file, encoding="utf-8")) if ledger_file.exists() else 0
        queue_rows.sort(key=lambda r: r.get("_ledger_trades", 0))
        # Apply rotation offset for diversity across cycles
        rotated = queue_rows[offset:] + queue_rows[:offset]
        queue_rows = rotated[:max_candidates_per_cycle]
        next_offset = (offset + max_candidates_per_cycle) % max(1, len(rotated))
        safe_write_json(rotation_path, {"offset": next_offset, "total": len(rotated)})

    summary_rows: list[dict[str, Any]] = []
    for row in queue_rows:
        if not isinstance(row, dict):
            continue
        candidate_id = str(row.get("candidate_id", "")).strip()
        if not candidate_id:
            continue
        mutations = row.get("mutations", {})
        mutations = mutations if isinstance(mutations, dict) else {}
        result = run_paper_trade_validation(mutations, repo_root, max_contracts=1500)

        # Cumulative ledger: merge new decisions into persistent trade log
        ledger_path = ledger_root / f"{candidate_id}.jsonl"
        existing_entries = _load_ledger(ledger_path)
        seen_ids = {e.get("contract_id") for e in existing_entries}
        new_decisions = [
            d for d in result.get("decisions", [])
            if d.get("contract_id") and d["contract_id"] not in seen_ids
        ]
        _append_to_ledger(ledger_path, new_decisions)
        # Recompute stats from the full ledger
        all_entries = existing_entries + new_decisions
        ledger_stats = _ledger_summary(all_entries)

        record = {
            "candidate_id": candidate_id,
            "run_id": row.get("run_id"),
            "doctrine_id": row.get("doctrine_id"),
            "strategy_id": row.get("strategy_id"),
            "mutations": mutations,
            "bridge_profitability_score": row.get("profitability_score"),
            "bridge_paper_trade_readiness": row.get("paper_trade_readiness"),
            "bridge_max_drawdown": row.get("max_drawdown"),
            "paper_trade_result": result,
            "ledger_new_trades": len([d for d in new_decisions if d.get("prediction") != "skip"]),
            "ledger_total_trades": ledger_stats["trade_count"],
        }
        path = runs_root / f"{candidate_id}.json"
        safe_write_json(path, record)

        # Use ledger stats for the summary (cumulative across cycles)
        ledger_rec = ledger_stats.get("paper_trade_recommendation", "collect_more_paper_data")
        boundary = (
            "Paper-trade slice supports live-readiness review."
            if ledger_rec == "advance_toward_live_readiness"
            else "Paper-trade slice is still thin or unstable; do not treat it as live-ready."
            if ledger_rec == "collect_more_paper_data"
            else "Paper-trade slice failed to confirm the bridge candidate."
        )
        summary_rows.append(
            {
                "candidate_id": candidate_id,
                "status": result.get("status"),
                "paper_trade_recommendation": ledger_rec,
                "sample_contract_count": result.get("sample_contract_count"),
                "trade_count": ledger_stats["trade_count"],
                "win_rate": ledger_stats["win_rate"],
                "profitability_score": ledger_stats["profitability_score"],
                "max_drawdown": ledger_stats["max_drawdown"],
                "regime_stats": ledger_stats.get("regime_stats", result.get("regime_stats")),
                "start_contract_id": result.get("start_contract_id"),
                "end_contract_id": result.get("end_contract_id"),
                "boundary": boundary,
                "ledger_total_entries": len(all_entries),
                "ledger_new_this_cycle": len(new_decisions),
                "assets_evaluated": result.get("assets_evaluated", []),
            }
        )

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "contract_family": "multi_asset",
        "queue_count": len(queue_rows),
        "executed_candidate_count": sum(1 for row in summary_rows if str(row.get("status", "")) == "executed"),
        "pending_data_count": sum(1 for row in summary_rows if str(row.get("status", "")) == "pending_data"),
        "rows": summary_rows,
    }
    summary_path = paper_root / "paper_trade_summary.json"
    safe_write_json(summary_path, summary)
    return summary_path


def run_paper_trade_loop() -> dict[str, Any]:
    started_at = datetime.now(timezone.utc)
    previous_report = _load_json(REPO_ROOT / "artifacts" / "paper_trade" / "paper_trade_loop_report.json", {})
    before_snapshot = _paper_trade_snapshot(REPO_ROOT)
    previous_snapshot = previous_report.get("after", before_snapshot) if isinstance(previous_report, dict) else before_snapshot
    run_paper_trade_cycle(REPO_ROOT)
    render_watchtower(REPO_ROOT)
    after_snapshot = _paper_trade_snapshot(REPO_ROOT)
    material_change, material_reasons = _material_delta(previous_snapshot, after_snapshot)
    finished_at = datetime.now(timezone.utc)
    report = {
        "loop_kind": "paper_trade",
        "started_at": started_at.isoformat().replace("+00:00", "Z"),
        "finished_at": finished_at.isoformat().replace("+00:00", "Z"),
        "duration_seconds": round((finished_at - started_at).total_seconds(), 3),
        "before": before_snapshot,
        "after": after_snapshot,
        "material_change": material_change,
        "material_reasons": material_reasons,
    }
    path = REPO_ROOT / "artifacts" / "paper_trade" / "paper_trade_loop_report.json"
    safe_write_json(path, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one bounded BTC paper-trade loop.")
    parser.parse_args()
    report = run_paper_trade_loop()
    print(REPO_ROOT / "artifacts" / "paper_trade" / "paper_trade_loop_report.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
