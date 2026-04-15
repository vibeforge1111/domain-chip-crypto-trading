"""Track paper trade results over time.

Appends a snapshot of the current paper trade summary to a JSONL history file.
This enables trend analysis: is a candidate improving or degrading over time?
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
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


def track_paper_trade_history(repo_root: Path) -> Path:
    """Append current paper trade summary snapshot to history."""
    summary = _load_json(repo_root / "artifacts" / "paper_trade" / "paper_trade_summary.json", {})
    summary = summary if isinstance(summary, dict) else {}
    rows = summary.get("rows", [])
    rows = rows if isinstance(rows, list) else []

    snapshot = {
        "tracked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_generated_at": summary.get("generated_at"),
        "queue_count": int(summary.get("queue_count", 0) or 0),
        "executed_candidate_count": int(summary.get("executed_candidate_count", 0) or 0),
        "candidates": [],
    }

    for row in rows:
        if not isinstance(row, dict):
            continue
        snapshot["candidates"].append({
            "candidate_id": str(row.get("candidate_id", "")),
            "trade_count": int(row.get("trade_count", 0) or 0),
            "win_rate": float(row.get("win_rate", 0) or 0),
            "max_drawdown": float(row.get("max_drawdown", 0) or 0),
            "profitability_score": float(row.get("profitability_score", 0) or 0),
            "paper_trade_recommendation": str(row.get("paper_trade_recommendation", "")),
        })

    history_path = repo_root / "artifacts" / "paper_trade" / "paper_trade_history.jsonl"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(snapshot, sort_keys=True) + "\n")

    return history_path


def main() -> None:
    path = track_paper_trade_history(REPO_ROOT)
    print(f"Appended snapshot to {path}")


if __name__ == "__main__":
    main()
