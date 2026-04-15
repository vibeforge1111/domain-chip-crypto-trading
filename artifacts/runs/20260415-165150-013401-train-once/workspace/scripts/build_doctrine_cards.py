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


def _existing_cards(card_root: Path) -> dict[str, dict[str, Any]]:
    cards: dict[str, dict[str, Any]] = {}
    if not card_root.exists():
        return cards
    for path in sorted(card_root.glob("*.json")):
        payload = _load_json(path, {})
        if not isinstance(payload, dict):
            continue
        card_id = str(payload.get("card_id", "")).strip()
        if card_id:
            cards[card_id] = payload
    return cards


def _packet_library(packet_root: Path) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    if not packet_root.exists():
        return packets
    for path in sorted(packet_root.glob("*.json")):
        payload = _load_json(path, {})
        if not isinstance(payload, dict):
            continue
        packet_id = str(payload.get("packet_id", "")).strip()
        card_id = str(payload.get("card_id", "")).strip()
        if packet_id and card_id:
            packets.append(payload)
    packets.sort(
        key=lambda item: (
            int(item.get("ingest_priority", 999) or 999),
            str(item.get("packet_id", "")),
        )
    )
    return packets


def _approved_source_ids() -> set[str]:
    payload = _load_json(REPO_ROOT / "docs" / "research-ingest" / "approved-sources.json", [])
    payload = payload if isinstance(payload, list) else []
    return {
        str(item.get("source_id", "")).strip()
        for item in payload
        if isinstance(item, dict) and str(item.get("source_id", "")).strip()
    }


def _policy() -> dict[str, Any]:
    data = _load_json(REPO_ROOT / "docs" / "recursion" / "loop-policy.json", {})
    return data if isinstance(data, dict) else {}


def _eligible_packets(
    packets: list[dict[str, Any]],
    existing_card_ids: set[str],
    approved_source_ids: set[str],
    required_source_count: int,
) -> list[dict[str, Any]]:
    eligible: list[dict[str, Any]] = []
    for item in packets:
        card_id = str(item.get("card_id", "")).strip()
        packet_status = str(item.get("packet_status", "")).strip()
        source_ids = [str(source_id).strip() for source_id in item.get("source_ids", []) if str(source_id).strip()]
        if not card_id or card_id in existing_card_ids:
            continue
        if packet_status != "ready_for_card_ingest":
            continue
        if len(source_ids) < required_source_count:
            continue
        if all(source_id in approved_source_ids for source_id in source_ids):
            eligible.append(item)
    return eligible


def _packet_to_card(packet: dict[str, Any]) -> dict[str, Any]:
    card = {
        "card_id": packet.get("card_id"),
        "proposal_id": packet.get("proposal_id"),
        "title": packet.get("title"),
        "doctrine_family": packet.get("doctrine_family"),
        "strategy_family": packet.get("strategy_family"),
        "source_ids": packet.get("source_ids", []),
        "target_contract_family": packet.get("target_contract_family"),
        "benchmark_priority": packet.get("benchmark_priority"),
        "research_thesis": packet.get("research_thesis"),
        "root_lesson": packet.get("root_lesson"),
        "counterfactual": packet.get("counterfactual"),
        "ghost_improvement_check": packet.get("ghost_improvement_check"),
        "rollback_condition": packet.get("rollback_condition"),
        "mutation_template": packet.get("mutation_template", {}),
        "status": "candidate_card",
        "source_count": len(packet.get("source_ids", [])),
        "ingested_from": "doctrine_packet",
        "source_packet_id": packet.get("packet_id"),
        "trader": packet.get("trader"),
        "mechanism": packet.get("mechanism"),
        "setup_definition": packet.get("setup_definition"),
        "no_trade_boundaries": packet.get("no_trade_boundaries", []),
        "lineage_failures": packet.get("lineage_failures", []),
    }
    return card


def main() -> None:
    policy = _policy()
    research_lane = policy.get("research_lane", {}) if isinstance(policy.get("research_lane"), dict) else {}
    max_new = int(research_lane.get("max_new_mutations_per_cycle", 3) or 3)
    required_source_count = int(research_lane.get("required_source_count_per_mutation", 2) or 2)

    packet_root = REPO_ROOT / "docs" / "doctrine-packets"
    card_root = REPO_ROOT / "docs" / "doctrine-cards"
    card_root.mkdir(parents=True, exist_ok=True)

    packets = _packet_library(packet_root)
    existing = _existing_cards(card_root)
    approved_source_ids = _approved_source_ids()
    eligible = _eligible_packets(packets, set(existing.keys()), approved_source_ids, required_source_count)
    selected = eligible[:max_new]

    written: list[str] = []
    for item in selected:
        card = _packet_to_card(item)
        path = card_root / f"{card['card_id']}.json"
        safe_write_json(path, card)
        written.append(path.name)

    remaining = _eligible_packets(packets, set(existing.keys()) | {str(item.get("card_id", "")) for item in selected}, approved_source_ids, required_source_count)
    report = {
        "packet_count": len(packets),
        "eligible_packet_count": len(eligible),
        "max_new_mutations_per_cycle": max_new,
        "required_source_count_per_mutation": required_source_count,
        "existing_card_count": len(existing),
        "added_count": len(written),
        "added_cards": written,
        "remaining_packet_count": len(remaining),
    }
    target_root = REPO_ROOT / "artifacts" / "research"
    target_root.mkdir(parents=True, exist_ok=True)
    path = target_root / "doctrine_ingest_report.json"
    safe_write_json(path, report)
    print(path)


if __name__ == "__main__":
    main()
