from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _timeline_pack_payload(repo_root: Path) -> dict[str, Any]:
    payload = _load_json(repo_root / "artifacts" / "research" / "timeline_packs.json", {})
    return payload if isinstance(payload, dict) else {}


def _timeline_pack_validation(repo_root: Path) -> dict[str, Any]:
    payload = _load_json(repo_root / "artifacts" / "research" / "timeline_pack_validation.json", {})
    return payload if isinstance(payload, dict) else {}


def _regime_match_review(repo_root: Path) -> dict[str, Any]:
    payload = _load_json(repo_root / "artifacts" / "research" / "regime_match_review.json", {})
    return payload if isinstance(payload, dict) else {}


def _futurelog_rows(backlog: dict[str, Any]) -> list[dict[str, Any]]:
    rows = backlog.get("futurelog_rows", [])
    return rows if isinstance(rows, list) else []


def _candidate_rows(backlog: dict[str, Any]) -> list[dict[str, Any]]:
    rows = backlog.get("candidate_rows", [])
    return rows if isinstance(rows, list) else []


def _style_rows(backlog: dict[str, Any]) -> list[dict[str, Any]]:
    rows = backlog.get("style_rows", [])
    return rows if isinstance(rows, list) else []


def _regime_rows(backlog: dict[str, Any]) -> list[dict[str, Any]]:
    rows = backlog.get("regime_rows", [])
    return rows if isinstance(rows, list) else []


def _futurelog_queue_rows(backlog: dict[str, Any]) -> list[dict[str, Any]]:
    queue_rows: list[dict[str, Any]] = []
    for item in _futurelog_rows(backlog):
        if not isinstance(item, dict):
            continue
        queue_rows.append(
            {
                "queue_id": str(item.get("item_id", "")).strip(),
                "queue_kind": "futurelog",
                "priority_score": round(1.0 - min(0.8, (int(item.get("priority", 9) or 9) - 1) * 0.1), 4),
                "priority_tier": int(item.get("priority", 9) or 9),
                "status": str(item.get("status", "")).strip(),
                "title": str(item.get("title", "")).strip(),
                "recommended_action": "packet_research" if "packet" in str(item.get("status", "")) or "packeting" in str(item.get("status", "")) else "research_design",
                "style_families": item.get("style_families", []),
                "source_names": item.get("source_names", []),
                "target_regimes": item.get("target_regimes", []),
                "reason": str(item.get("why_now", "")).strip(),
                "expected_child_shapes": item.get("expected_child_shapes", []),
            }
        )
    return queue_rows


def _undercovered_style_queue_rows(backlog: dict[str, Any]) -> list[dict[str, Any]]:
    queue_rows: list[dict[str, Any]] = []
    candidate_index: dict[str, list[str]] = {}
    for item in _candidate_rows(backlog):
        if not isinstance(item, dict):
            continue
        style = str(item.get("style_family", "")).strip()
        status = str(item.get("status", "")).strip()
        if style and status == "approved_waiting_packet":
            candidate_index.setdefault(style, []).append(str(item.get("name", "")).strip())
    for item in _style_rows(backlog):
        if not isinstance(item, dict):
            continue
        coverage = str(item.get("coverage_status", "")).strip()
        if coverage != "approved_but_unpacketed":
            continue
        style = str(item.get("style_family", "")).strip()
        queue_rows.append(
            {
                "queue_id": f"style-{style}",
                "queue_kind": "undercovered_style",
                "priority_score": 0.72,
                "priority_tier": 2,
                "status": coverage,
                "title": style,
                "recommended_action": "packet_missing_style",
                "style_families": [style] if style else [],
                "source_names": candidate_index.get(style, []),
                "target_regimes": [],
                "reason": "Approved sources exist for this style family, but no packet or doctrine card covers it yet.",
                "expected_child_shapes": [],
            }
        )
    return queue_rows


def _regime_gap_queue_rows(backlog: dict[str, Any]) -> list[dict[str, Any]]:
    queue_rows: list[dict[str, Any]] = []
    for item in _regime_rows(backlog):
        if not isinstance(item, dict):
            continue
        status = str(item.get("status", "")).strip()
        if status not in {"needs_more_archive_data", "partially_covered"}:
            continue
        research_gaps = item.get("research_gaps", [])
        research_gaps = research_gaps if isinstance(research_gaps, list) else []
        queue_rows.append(
            {
                "queue_id": str(item.get("regime_id", "")).strip(),
                "queue_kind": "regime_gap",
                "priority_score": 0.84 if status == "needs_more_archive_data" else 0.68,
                "priority_tier": int(item.get("priority", 9) or 9),
                "status": status,
                "title": str(item.get("label", "")).strip(),
                "recommended_action": "archive_timeline_pack" if status == "needs_more_archive_data" else "regime_specific_packet",
                "style_families": [],
                "source_names": [],
                "target_regimes": [str(item.get("regime_id", "")).strip()],
                "reason": str(item.get("market_character", "")).strip(),
                "expected_child_shapes": research_gaps,
            }
        )
    return queue_rows


def _timeline_pack_queue_rows(repo_root: Path) -> list[dict[str, Any]]:
    payload = _timeline_pack_payload(repo_root)
    validation_payload = _timeline_pack_validation(repo_root)
    rows = payload.get("rows", [])
    rows = rows if isinstance(rows, list) else []
    validation_rows = validation_payload.get("rows", [])
    validation_rows = validation_rows if isinstance(validation_rows, list) else []
    validation_index = {
        str(item.get("pack_id", "")).strip(): item
        for item in validation_rows
        if isinstance(item, dict) and str(item.get("pack_id", "")).strip()
    }
    queue_rows: list[dict[str, Any]] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        coverage_status = str(item.get("coverage_status", "")).strip()
        if coverage_status not in {"ready_for_dataset_extract", "needs_data_extension"}:
            continue
        pack_id = str(item.get("pack_id", "")).strip()
        validation = validation_index.get(pack_id, {})
        dataset_ready = bool(validation.get("dataset_ready"))
        validation_status = str(validation.get("validation_status", "")).strip()
        if dataset_ready and validation_status == "validated_match":
            continue
        if dataset_ready and validation_status == "mismatch_review":
            continue
        if coverage_status == "ready_for_dataset_extract":
            if not dataset_ready:
                recommended_action = "prepare_timeline_pack"
                priority_score = 0.88
            elif validation_status == "mixed_proxy":
                recommended_action = "research_design"
                priority_score = 0.82
            else:
                continue
        else:
            recommended_action = "extend_archive_data"
            priority_score = 0.8
        queue_rows.append(
            {
                "queue_id": pack_id,
                "queue_kind": "timeline_pack",
                "priority_score": priority_score,
                "priority_tier": 1 if coverage_status == "ready_for_dataset_extract" else 2,
                "status": coverage_status,
                "title": str(item.get("regime_label", "")).strip(),
                "recommended_action": recommended_action,
                "style_families": [],
                "source_names": [],
                "target_regimes": [str(item.get("regime_id", "")).strip()],
                "reason": str(item.get("reason", "")).strip(),
                "expected_child_shapes": item.get("research_gaps", []),
                "pack_id": pack_id,
                "window_id": str(item.get("window_id", "")).strip(),
                "target_paths": item.get("target_paths", {}),
                "dataset_ready": dataset_ready,
                "validation_status": validation_status or "pending_extract",
                "claimed_regime_score": validation.get("claimed_regime_score"),
                "predicted_regime_id": validation.get("predicted_regime_id"),
            }
        )
    return queue_rows


def _regime_match_review_rows(repo_root: Path) -> list[dict[str, Any]]:
    payload = _regime_match_review(repo_root)
    rows = payload.get("rows", [])
    rows = rows if isinstance(rows, list) else []
    queue_rows: list[dict[str, Any]] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        queue_rows.append(
            {
                "queue_id": str(item.get("review_id", "")).strip(),
                "queue_kind": "regime_match_review",
                "priority_score": 0.92 if str(item.get("recommended_action", "")).strip() == "extend_archive_data" else 0.86,
                "priority_tier": 1,
                "status": "mismatch_review",
                "title": str(item.get("pack_id", "")).strip(),
                "recommended_action": str(item.get("recommended_action", "")).strip(),
                "style_families": [],
                "source_names": [],
                "target_regimes": [str(item.get("claimed_regime_id", "")).strip()],
                "reason": "Extracted proxy pack does not currently validate as its claimed regime.",
                "expected_child_shapes": [],
                "pack_id": str(item.get("pack_id", "")).strip(),
                "predicted_regime_id": str(item.get("predicted_regime_id", "")).strip(),
                "claimed_regime_score": item.get("claimed_regime_score"),
                "replacement_pack_ids": item.get("replacement_pack_ids", []),
                "review_outcome": str(item.get("review_outcome", "")).strip(),
            }
        )
    return queue_rows


def build_research_scout_queue(repo_root: Path | None = None) -> Path:
    root = repo_root or REPO_ROOT
    backlog = _load_json(root / "artifacts" / "research" / "research_backlog.json", {})
    backlog = backlog if isinstance(backlog, dict) else {}

    rows = []
    rows.extend(_futurelog_queue_rows(backlog))
    rows.extend(_undercovered_style_queue_rows(backlog))
    rows.extend(_regime_gap_queue_rows(backlog))
    rows.extend(_regime_match_review_rows(root))
    rows.extend(_timeline_pack_queue_rows(root))
    rows.sort(
        key=lambda item: (
            -float(item.get("priority_score", 0.0) or 0.0),
            int(item.get("priority_tier", 9) or 9),
            str(item.get("title", "")),
        )
    )
    payload = {
        "generated_from": "artifacts/research/research_backlog.json",
        "queue_count": len(rows),
        "rows": rows,
        "top_rows": rows[:12],
    }
    target = root / "artifacts" / "research" / "research_scout_queue.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def main() -> None:
    path = build_research_scout_queue(REPO_ROOT)
    print(path)


if __name__ == "__main__":
    main()
