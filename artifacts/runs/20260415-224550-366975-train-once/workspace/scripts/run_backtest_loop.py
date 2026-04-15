from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from build_bridge_packets import build_bridge_packets
from build_contradiction_probes import main as build_contradiction_probes
from build_segment_regime_review import build_segment_regime_review
from build_mutation_trials import main as build_mutation_trials
from build_recursion_packets import build_recursion_packets
from build_self_edit_queue import main as build_self_edit_queue
from build_watchtower import render_watchtower
from evaluate_self_edits import main as evaluate_self_edits
from run_heavy_backtest_benchmark import main as run_heavy_backtest_benchmark
from build_paper_trade_queue import build_paper_trade_queue
from safe_write import safe_write_json
from build_signal_mutations import build_signal_mutations


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _summary_snapshot() -> dict[str, Any]:
    summary = _load_json(REPO_ROOT / "artifacts" / "backtests" / "heavy_backtest_summary.json", {})
    summary = summary if isinstance(summary, dict) else {}
    rows = summary.get("rows", [])
    rows = rows if isinstance(rows, list) else []
    top_row = rows[0] if rows and isinstance(rows[0], dict) else {}
    metrics = top_row.get("metrics", {}) if isinstance(top_row.get("metrics"), dict) else {}
    result = top_row.get("result", {}) if isinstance(top_row.get("result"), dict) else {}
    return {
        "candidate_count": int(summary.get("candidate_count", 0) or 0),
        "top_candidate_id": str(summary.get("top_candidate_id", "") or ""),
        "top_profitability_score": round(float(metrics.get("profitability_score", 0.0) or 0.0), 4),
        "top_paper_trade_readiness": round(float(metrics.get("paper_trade_readiness", 0.0) or 0.0), 4),
        "top_max_drawdown": round(float(metrics.get("max_drawdown", 0.0) or 0.0), 4),
        "top_holdout_profitability_score": round(float(result.get("holdout_profitability_score", 0.0) or 0.0), 4),
        "top_walk_forward_consistency": round(float(result.get("walk_forward_consistency", 0.0) or 0.0), 4),
        "top_stress_resilience": round(float(result.get("stress_resilience", 0.0) or 0.0), 4),
        "top_recommended_next_step": str(result.get("recommended_next_step", "") or ""),
    }


def _self_edit_snapshot() -> dict[str, Any]:
    audit = _load_json(REPO_ROOT / "artifacts" / "recursion" / "self_edit_audit.json", {})
    audit = audit if isinstance(audit, dict) else {}
    return {
        "evaluation_count": int(audit.get("evaluation_count", 0) or 0),
        "approved_count": int(audit.get("approved_count", 0) or 0),
        "deferred_count": int(audit.get("deferred_count", 0) or 0),
        "rejected_count": int(audit.get("rejected_count", 0) or 0),
        "top_approved_edit_id": audit.get("top_approved_edit_id"),
    }


def _loop_snapshot() -> dict[str, Any]:
    return {
        "benchmark": _summary_snapshot(),
        "self_edit_audit": _self_edit_snapshot(),
    }


def _material_delta(previous: dict[str, Any], current: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    previous_benchmark = previous.get("benchmark", {}) if isinstance(previous, dict) else {}
    current_benchmark = current.get("benchmark", {})
    previous_self_edit = previous.get("self_edit_audit", {}) if isinstance(previous, dict) else {}
    current_self_edit = current.get("self_edit_audit", {})
    if previous_benchmark.get("top_candidate_id") != current_benchmark.get("top_candidate_id"):
        reasons.append("top_candidate_changed")
    if previous_benchmark.get("top_recommended_next_step") != current_benchmark.get("top_recommended_next_step"):
        reasons.append("top_next_step_changed")
    thresholds = {
        "candidate_count": 1.0,
        "top_profitability_score": 0.005,
        "top_paper_trade_readiness": 0.01,
        "top_max_drawdown": 0.01,
        "top_holdout_profitability_score": 0.01,
        "top_walk_forward_consistency": 0.1,
        "top_stress_resilience": 0.1,
    }
    for field, threshold in thresholds.items():
        previous_value = float(previous_benchmark.get(field, 0.0) or 0.0)
        current_value = float(current_benchmark.get(field, 0.0) or 0.0)
        if abs(current_value - previous_value) >= threshold:
            reasons.append(field)
    for field in ["evaluation_count", "approved_count", "deferred_count", "rejected_count"]:
        if int(previous_self_edit.get(field, 0) or 0) != int(current_self_edit.get(field, 0) or 0):
            reasons.append(field)
    if previous_self_edit.get("top_approved_edit_id") != current_self_edit.get("top_approved_edit_id"):
        reasons.append("top_approved_edit_id")
    deduped: list[str] = []
    for reason in reasons:
        if reason not in deduped:
            deduped.append(reason)
    return bool(deduped), deduped


def _git_tracked_diff_exists() -> bool:
    result = subprocess.run(["git", "status", "--short"], cwd=REPO_ROOT, check=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.strip() and not line.strip().endswith(".obsidian/"):
            return True
    return False


def _commit_if_needed(report: dict[str, Any]) -> str | None:
    if not bool(report.get("material_change")) or not _git_tracked_diff_exists():
        return None
    benchmark = report.get("after", {}).get("benchmark", {})
    self_edit = report.get("after", {}).get("self_edit_audit", {})
    top_candidate_id = str(benchmark.get("top_candidate_id", "") or "unknown-candidate")
    approved_count = int(self_edit.get("approved_count", 0) or 0)
    message = f"Backtest loop sync: {top_candidate_id} a{approved_count}"
    subprocess.run(["git", "add", "-u"], cwd=REPO_ROOT, check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_ROOT)
    if staged.returncode == 0:
        return None
    subprocess.run(["git", "commit", "-m", message], cwd=REPO_ROOT, check=True)
    return message


def run_backtest_loop(*, commit_if_material_change: bool = False, persist_report_on_noop: bool = False) -> dict[str, Any]:
    started_at = datetime.now(timezone.utc)
    previous_report = _load_json(REPO_ROOT / "artifacts" / "backtests" / "backtest_loop_report.json", {})
    before_snapshot = _loop_snapshot()
    previous_snapshot = previous_report.get("after", before_snapshot) if isinstance(previous_report, dict) else before_snapshot

    signal_mutation_report = build_signal_mutations(REPO_ROOT)
    run_heavy_backtest_benchmark()
    build_bridge_packets(REPO_ROOT)
    build_recursion_packets(REPO_ROOT)
    build_contradiction_probes()

    # Snapshot mutation trials before generating new ones
    _mt_path = REPO_ROOT / "artifacts" / "recursion" / "mutation_trials.json"
    _pre_ids = set()
    _pre_data = _load_json(_mt_path, [])
    if isinstance(_pre_data, list):
        _pre_ids = {str(t.get("candidate_id", "")) for t in _pre_data if isinstance(t, dict)}

    build_mutation_trials()

    # Only re-benchmark if mutation_trials changed (saves ~190s per cycle)
    _post_data = _load_json(_mt_path, [])
    _post_ids = set()
    if isinstance(_post_data, list):
        _post_ids = {str(t.get("candidate_id", "")) for t in _post_data if isinstance(t, dict)}
    if _post_ids != _pre_ids:
        run_heavy_backtest_benchmark()

    build_bridge_packets(REPO_ROOT)
    build_paper_trade_queue(REPO_ROOT)
    build_recursion_packets(REPO_ROOT)
    build_contradiction_probes()
    build_self_edit_queue()
    evaluate_self_edits()
    build_recursion_packets(REPO_ROOT)
    build_segment_regime_review(REPO_ROOT)
    render_watchtower(REPO_ROOT)

    after_snapshot = _loop_snapshot()
    material_change, material_reasons = _material_delta(previous_snapshot, after_snapshot)
    finished_at = datetime.now(timezone.utc)
    report = {
        "loop_kind": "backtest",
        "started_at": started_at.isoformat().replace("+00:00", "Z"),
        "finished_at": finished_at.isoformat().replace("+00:00", "Z"),
        "duration_seconds": round((finished_at - started_at).total_seconds(), 3),
        "before": before_snapshot,
        "after": after_snapshot,
        "material_change": material_change,
        "material_reasons": material_reasons,
        "commit_message": None,
    }
    if commit_if_material_change:
        report["commit_message"] = _commit_if_needed(report)
    target = REPO_ROOT / "artifacts" / "backtests" / "backtest_loop_report.json"
    if material_change or persist_report_on_noop or not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        safe_write_json(target, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one bounded BTC backtest loop.")
    parser.add_argument("--commit-if-material-change", action="store_true")
    parser.add_argument("--persist-report-on-noop", action="store_true")
    args = parser.parse_args()
    report = run_backtest_loop(
        commit_if_material_change=args.commit_if_material_change,
        persist_report_on_noop=args.persist_report_on_noop,
    )
    print(REPO_ROOT / "artifacts" / "backtests" / "backtest_loop_report.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
