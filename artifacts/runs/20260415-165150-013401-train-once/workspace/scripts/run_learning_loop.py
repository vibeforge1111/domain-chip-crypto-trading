from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from build_pattern_regime_map import build_pattern_regime_map
from build_regime_match_review import build_regime_match_review
from build_research_backlog import build_research_backlog
from build_research_scout_queue import build_research_scout_queue
from build_timeline_pack_validation import build_timeline_pack_validation
from build_timeline_packs import build_timeline_packs
from build_doctrine_cards import main as build_doctrine_cards
from reconcile_doctrine_state import reconcile_doctrine_state
from build_watchtower import render_watchtower
from build_doctrine_from_contradictions import build_doctrine_from_contradictions
from safe_write import safe_write_json


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _pending_packet_count() -> int:
    packet_root = REPO_ROOT / "docs" / "doctrine-packets"
    card_root = REPO_ROOT / "docs" / "doctrine-cards"
    packet_ids = set()
    for path in sorted(packet_root.glob("*.json")):
        payload = _load_json(path, {})
        if not isinstance(payload, dict):
            continue
        if str(payload.get("packet_status", "")).strip() != "ready_for_card_ingest":
            continue
        card_id = str(payload.get("card_id", "")).strip()
        if card_id:
            packet_ids.add(card_id)
    card_ids = set()
    for path in sorted(card_root.glob("*.json")):
        payload = _load_json(path, {})
        if not isinstance(payload, dict):
            continue
        card_id = str(payload.get("card_id", "")).strip()
        if card_id:
            card_ids.add(card_id)
    return len(packet_ids - card_ids)


def _card_count() -> int:
    return len(list((REPO_ROOT / "docs" / "doctrine-cards").glob("*.json")))


def _research_backlog_snapshot() -> dict[str, int]:
    report = _load_json(REPO_ROOT / "artifacts" / "research" / "research_backlog.json", {})
    report = report if isinstance(report, dict) else {}
    return {
        "ready_for_source_ingest_count": int(report.get("ready_for_source_ingest_count", 0) or 0),
        "approved_waiting_packet_count": int(report.get("approved_waiting_packet_count", 0) or 0),
    }


def run_learning_loop() -> dict[str, Any]:
    started_at = datetime.now(timezone.utc)
    doctrine_gen_report = build_doctrine_from_contradictions(REPO_ROOT)
    build_research_backlog(REPO_ROOT)
    build_timeline_packs(REPO_ROOT)
    build_timeline_pack_validation(REPO_ROOT)
    build_regime_match_review(REPO_ROOT)
    build_pattern_regime_map(REPO_ROOT)
    build_research_scout_queue(REPO_ROOT)
    before = {
        "card_count": _card_count(),
        "pending_packet_count": _pending_packet_count(),
        **_research_backlog_snapshot(),
        "doctrine_packets_generated": int(doctrine_gen_report.get("packets_generated", 0) or 0),
    }
    build_doctrine_cards()
    _, reconciliation = reconcile_doctrine_state(REPO_ROOT, repair=True)
    build_research_backlog(REPO_ROOT)
    build_timeline_packs(REPO_ROOT)
    build_timeline_pack_validation(REPO_ROOT)
    build_regime_match_review(REPO_ROOT)
    build_pattern_regime_map(REPO_ROOT)
    build_research_scout_queue(REPO_ROOT)
    render_watchtower(REPO_ROOT)
    ingest_report = _load_json(REPO_ROOT / "artifacts" / "research" / "doctrine_ingest_report.json", {})
    ingest_report = ingest_report if isinstance(ingest_report, dict) else {}
    after = {
        "card_count": _card_count(),
        "pending_packet_count": _pending_packet_count(),
        **_research_backlog_snapshot(),
        "added_count": int(ingest_report.get("added_count", 0) or 0),
        "added_cards": ingest_report.get("added_cards", []),
        "reconciliation_repaired_count": int(reconciliation.get("repaired_count", 0) or 0),
        "reconciliation_repaired_cards": reconciliation.get("repaired_cards", []),
        "state_consistent": bool(reconciliation.get("state_consistent")),
        "eligible_missing_card_count": int(reconciliation.get("eligible_missing_card_count", 0) or 0),
    }
    material_reasons: list[str] = []
    if after["card_count"] != before["card_count"]:
        material_reasons.append("card_count")
    if after["pending_packet_count"] != before["pending_packet_count"]:
        material_reasons.append("pending_packet_count")
    if after["ready_for_source_ingest_count"] != before["ready_for_source_ingest_count"]:
        material_reasons.append("ready_for_source_ingest_count")
    if after["approved_waiting_packet_count"] != before["approved_waiting_packet_count"]:
        material_reasons.append("approved_waiting_packet_count")
    if after["added_count"] > 0:
        material_reasons.append("added_count")
    if after["reconciliation_repaired_count"] > 0:
        material_reasons.append("reconciliation_repaired_count")
    if not after["state_consistent"]:
        material_reasons.append("inconsistent_doctrine_state")
    finished_at = datetime.now(timezone.utc)
    report = {
        "loop_kind": "learning",
        "started_at": started_at.isoformat().replace("+00:00", "Z"),
        "finished_at": finished_at.isoformat().replace("+00:00", "Z"),
        "duration_seconds": round((finished_at - started_at).total_seconds(), 3),
        "before": before,
        "after": after,
        "material_change": bool(material_reasons),
        "material_reasons": material_reasons,
        "reconciliation": reconciliation,
    }
    target = REPO_ROOT / "artifacts" / "research" / "learning_loop_report.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    safe_write_json(target, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one bounded doctrine learning loop.")
    parser.parse_args()
    report = run_learning_loop()
    print(REPO_ROOT / "artifacts" / "research" / "learning_loop_report.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
