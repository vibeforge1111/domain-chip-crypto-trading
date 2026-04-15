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


def _allowed_edit_modes(probe: dict[str, Any]) -> list[str]:
    modes = probe.get("failure_modes", [])
    modes = modes if isinstance(modes, list) else []
    allowed: list[str] = []
    mode_names = {str(item.get("mode", "")).strip() for item in modes if isinstance(item, dict)}
    if "sparse_signal" in mode_names:
        allowed.append("activation_profile.wider")
    if "holdout_decay" in mode_names:
        allowed.append("late_sample_guard.on")
    if "execution_fragility" in mode_names:
        allowed.append("execution_buffer.high")
    return allowed


def _child_candidate_id(probe: dict[str, Any]) -> str:
    candidate_id = str(probe.get("candidate_id", "")).strip()
    failure_modes = probe.get("failure_modes", [])
    failure_modes = failure_modes if isinstance(failure_modes, list) else []
    primary_mode = "probe"
    if failure_modes and isinstance(failure_modes[0], dict):
        primary_mode = str(failure_modes[0].get("mode", "probe")).strip() or "probe"
    return f"{candidate_id}-probe-{primary_mode}"


def _queue_priority(probe: dict[str, Any]) -> float:
    priority = float(probe.get("priority", 0.0) or 0.0)
    trade_count = float(probe.get("trade_count", 0.0) or 0.0)
    minimum_trade_count = float(probe.get("minimum_trade_count", 0.0) or 0.0)
    walk_forward = float(probe.get("walk_forward_consistency", 0.0) or 0.0)
    holdout = float(probe.get("holdout_profitability_score", 0.0) or 0.0)
    if minimum_trade_count and trade_count >= minimum_trade_count and walk_forward >= 0.8 and holdout < 0.5:
        priority += 1.0
    return round(priority, 4)


def main() -> None:
    probe_path = REPO_ROOT / "artifacts" / "recursion" / "contradiction_probes.json"
    probes = _load_json(probe_path, [])
    probes = probes if isinstance(probes, list) else []
    queue: list[dict[str, Any]] = []
    for probe in probes:
        if not isinstance(probe, dict):
            continue
        candidate_id = str(probe.get("candidate_id", "")).strip()
        if "-probe-" in candidate_id:
            continue
        allowed = _allowed_edit_modes(probe)
        if not allowed:
            continue
        queue.append(
            {
                "edit_id": f"self-edit-{probe.get('probe_id')}",
                "parent_candidate_id": candidate_id,
                "child_candidate_id": _child_candidate_id(probe),
                "priority": _queue_priority(probe),
                "failure_modes": [item.get("mode") for item in probe.get("failure_modes", []) if isinstance(item, dict)],
                "allowed_edits": allowed,
                "root_lesson": probe.get("probe_thesis"),
                "counterfactual": "Without a bounded self-edit mutation, the loop keeps rediscovering the same failure surface without testing a concrete repair.",
                "ghost_improvement_check": "Approve only if the child improves the targeted failure metric without hiding behind lower trade count or worse drawdown.",
                "rollback_condition": "Reject if the child worsens profitability, drawdown, holdout behavior, or robustness versus the parent.",
                "status": "queued_for_self_edit_eval",
            }
        )
    queue.sort(key=lambda item: float(item.get("priority", 0.0) or 0.0), reverse=True)
    queue = queue[:6]
    target_root = REPO_ROOT / "artifacts" / "recursion"
    target_root.mkdir(parents=True, exist_ok=True)
    path = target_root / "self_edit_queue.json"
    safe_write_json(path, queue)
    print(path)


if __name__ == "__main__":
    main()
