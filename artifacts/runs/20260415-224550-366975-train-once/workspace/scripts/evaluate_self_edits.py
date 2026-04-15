from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from safe_write import safe_write_json


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _summary_index(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = summary.get("rows", [])
    rows = rows if isinstance(rows, list) else []
    return {str(row.get("candidate_id", "")).strip(): row for row in rows if isinstance(row, dict)}


def _metric(row: dict[str, Any], name: str, *, result: bool = False) -> float:
    bucket = row.get("result", {}) if result else row.get("metrics", {})
    bucket = bucket if isinstance(bucket, dict) else {}
    return float(bucket.get(name, 0.0) or 0.0)


def _decision_for_item(item: dict[str, Any], parent: dict[str, Any], child: dict[str, Any]) -> dict[str, Any]:
    failure_modes = item.get("failure_modes", [])
    failure_modes = [str(mode) for mode in failure_modes if str(mode).strip()]
    parent_profit = _metric(parent, "profitability_score")
    child_profit = _metric(child, "profitability_score")
    parent_holdout = _metric(parent, "holdout_profitability_score", result=True)
    child_holdout = _metric(child, "holdout_profitability_score", result=True)
    parent_drawdown = _metric(parent, "max_drawdown")
    child_drawdown = _metric(child, "max_drawdown")
    parent_trade_count = _metric(parent, "trade_count", result=True)
    child_trade_count = _metric(child, "trade_count", result=True)
    parent_walk = _metric(parent, "walk_forward_consistency", result=True)
    child_walk = _metric(child, "walk_forward_consistency", result=True)
    parent_stress = _metric(parent, "stress_resilience", result=True)
    child_stress = _metric(child, "stress_resilience", result=True)

    target_improved = False
    if "sparse_signal" in failure_modes and child_trade_count > parent_trade_count:
        target_improved = True
    if "holdout_decay" in failure_modes and child_holdout > parent_holdout + 0.015:
        target_improved = True
    if "execution_fragility" in failure_modes and child_stress > parent_stress + 0.2:
        target_improved = True
    if "segment_instability" in failure_modes and child_walk > parent_walk + 0.2:
        target_improved = True

    catastrophic = (
        child_profit < parent_profit - 0.03
        or child_holdout < parent_holdout - 0.03
        or child_drawdown > min(0.99, parent_drawdown + 0.05)
    )
    if catastrophic:
        decision = "reject"
    elif target_improved and child_profit >= parent_profit - 0.01 and child_drawdown <= parent_drawdown:
        decision = "approve"
    else:
        decision = "defer"

    return {
        "edit_id": item.get("edit_id"),
        "parent_candidate_id": item.get("parent_candidate_id"),
        "child_candidate_id": item.get("child_candidate_id"),
        "failure_modes": failure_modes,
        "decision": decision,
        "comparison": {
            "parent_profitability_score": parent_profit,
            "child_profitability_score": child_profit,
            "parent_holdout_profitability_score": parent_holdout,
            "child_holdout_profitability_score": child_holdout,
            "parent_trade_count": parent_trade_count,
            "child_trade_count": child_trade_count,
            "parent_walk_forward_consistency": parent_walk,
            "child_walk_forward_consistency": child_walk,
            "parent_stress_resilience": parent_stress,
            "child_stress_resilience": child_stress,
            "parent_max_drawdown": parent_drawdown,
            "child_max_drawdown": child_drawdown,
        },
        "target_improved": target_improved,
        "rollback_condition": item.get("rollback_condition"),
    }


def main() -> None:
    queue = _load_json(REPO_ROOT / "artifacts" / "recursion" / "self_edit_queue.json", [])
    queue = queue if isinstance(queue, list) else []
    summary = _load_json(REPO_ROOT / "artifacts" / "backtests" / "heavy_backtest_summary.json", {})
    index = _summary_index(summary if isinstance(summary, dict) else {})
    evaluations: list[dict[str, Any]] = []
    for item in queue:
        if not isinstance(item, dict):
            continue
        parent_id = str(item.get("parent_candidate_id", "")).strip()
        child_id = str(item.get("child_candidate_id", "")).strip()
        parent = index.get(parent_id)
        child = index.get(child_id)
        if not parent or not child:
            continue
        evaluations.append(_decision_for_item(item, parent, child))
    audit = {
        "evaluation_count": len(evaluations),
        "approved_count": sum(1 for item in evaluations if item.get("decision") == "approve"),
        "deferred_count": sum(1 for item in evaluations if item.get("decision") == "defer"),
        "rejected_count": sum(1 for item in evaluations if item.get("decision") == "reject"),
        "top_approved_edit_id": next((item.get("edit_id") for item in evaluations if item.get("decision") == "approve"), None),
    }
    target_root = REPO_ROOT / "artifacts" / "recursion"
    target_root.mkdir(parents=True, exist_ok=True)
    safe_write_json(target_root / "self_edit_evaluations.json", evaluations)
    safe_write_json(target_root / "self_edit_audit.json", audit)
    print(target_root / "self_edit_evaluations.json")
    print(target_root / "self_edit_audit.json")


if __name__ == "__main__":
    main()
