from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from safe_write import safe_write_json
from build_doctrine_cards import (
    REPO_ROOT,
    _approved_source_ids,
    _eligible_packets,
    _existing_cards,
    _packet_library,
    _packet_to_card,
    _policy,
)


def reconcile_doctrine_state(repo_root: Path | None = None, *, repair: bool = False) -> tuple[Path, dict[str, Any]]:
    root = repo_root or REPO_ROOT
    policy = _policy()
    research_lane = policy.get("research_lane", {}) if isinstance(policy.get("research_lane"), dict) else {}
    required_source_count = int(research_lane.get("required_source_count_per_mutation", 2) or 2)

    packet_root = root / "docs" / "doctrine-packets"
    card_root = root / "docs" / "doctrine-cards"
    card_root.mkdir(parents=True, exist_ok=True)

    packets = _packet_library(packet_root)
    existing = _existing_cards(card_root)
    approved_source_ids = _approved_source_ids()
    eligible = _eligible_packets(packets, set(existing.keys()), approved_source_ids, required_source_count)

    repaired_cards: list[str] = []
    if repair:
        for packet in eligible:
            card = _packet_to_card(packet)
            path = card_root / f"{card['card_id']}.json"
            safe_write_json(path, card)
            repaired_cards.append(path.name)
        existing = _existing_cards(card_root)
        eligible = _eligible_packets(packets, set(existing.keys()), approved_source_ids, required_source_count)

    payload = {
        "packet_count": len(packets),
        "card_count": len(existing),
        "required_source_count_per_mutation": required_source_count,
        "repair_mode": repair,
        "eligible_missing_card_count": len(eligible),
        "eligible_missing_cards": [str(item.get("card_id", "")) for item in eligible],
        "repaired_count": len(repaired_cards),
        "repaired_cards": repaired_cards,
        "state_consistent": len(eligible) == 0,
    }
    target = root / "artifacts" / "research" / "doctrine_reconciliation_report.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    safe_write_json(target, payload)
    return target, payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Reconcile eligible doctrine packets with tracked doctrine cards.")
    parser.add_argument("--repair", action="store_true", help="Write any missing eligible doctrine cards from packets.")
    args = parser.parse_args()
    path, _ = reconcile_doctrine_state(REPO_ROOT, repair=args.repair)
    print(path)


if __name__ == "__main__":
    main()
