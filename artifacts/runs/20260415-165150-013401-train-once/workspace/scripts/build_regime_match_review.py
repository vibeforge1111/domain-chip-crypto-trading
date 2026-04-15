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


def build_regime_match_review(repo_root: Path | None = None) -> Path:
    root = repo_root or REPO_ROOT
    validation = _load_json(root / "artifacts" / "research" / "timeline_pack_validation.json", {})
    validation = validation if isinstance(validation, dict) else {}
    validation_rows = validation.get("rows", [])
    validation_rows = validation_rows if isinstance(validation_rows, list) else []
    timeline_packs = _load_json(root / "artifacts" / "research" / "timeline_packs.json", {})
    timeline_packs = timeline_packs if isinstance(timeline_packs, dict) else {}
    timeline_rows = timeline_packs.get("rows", [])
    timeline_rows = timeline_rows if isinstance(timeline_rows, list) else []

    extension_index: dict[str, list[str]] = {}
    for row in timeline_rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("coverage_status", "")).strip() != "needs_data_extension":
            continue
        regime_id = str(row.get("regime_id", "")).strip()
        pack_id = str(row.get("pack_id", "")).strip()
        if regime_id and pack_id:
            extension_index.setdefault(regime_id, []).append(pack_id)

    review_rows: list[dict[str, Any]] = []
    for row in validation_rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("validation_status", "")).strip() != "mismatch_review":
            continue
        regime_id = str(row.get("regime_id", "")).strip()
        predicted_regime_id = str(row.get("predicted_regime_id", "")).strip()
        replacement_pack_ids = extension_index.get(regime_id, [])
        review_rows.append(
            {
                "review_id": f"review-{row.get('pack_id', 'unknown')}",
                "pack_id": row.get("pack_id"),
                "claimed_regime_id": regime_id,
                "predicted_regime_id": predicted_regime_id,
                "claimed_regime_score": row.get("claimed_regime_score"),
                "predicted_regime_score": row.get("predicted_regime_score"),
                "recommended_action": "extend_archive_data" if replacement_pack_ids else "research_design",
                "review_outcome": "replace_proxy_with_archive_window" if replacement_pack_ids else "add_new_window_targets_or_relabel_proxy",
                "replacement_pack_ids": replacement_pack_ids,
                "notes": row.get("notes", []),
            }
        )

    payload = {
        "review_count": len(review_rows),
        "rows": review_rows,
        "top_rows": review_rows[:12],
    }
    target = root / "artifacts" / "research" / "regime_match_review.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def main() -> None:
    path = build_regime_match_review(REPO_ROOT)
    print(path)


if __name__ == "__main__":
    main()
