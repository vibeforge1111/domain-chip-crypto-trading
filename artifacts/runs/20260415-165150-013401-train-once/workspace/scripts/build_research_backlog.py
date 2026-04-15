from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from safe_write import safe_write_json


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _approved_sources() -> list[dict[str, Any]]:
    data = _load_json(REPO_ROOT / "docs" / "research-ingest" / "approved-sources.json", [])
    return data if isinstance(data, list) else []


def _trader_candidates() -> list[dict[str, Any]]:
    data = _load_json(REPO_ROOT / "docs" / "research-ingest" / "trader-source-candidates.json", [])
    return data if isinstance(data, list) else []


def _next_to_research() -> list[dict[str, Any]]:
    data = _load_json(REPO_ROOT / "docs" / "research-ingest" / "next-to-research.json", [])
    return data if isinstance(data, list) else []


def _market_regime_intelligence() -> list[dict[str, Any]]:
    data = _load_json(REPO_ROOT / "docs" / "research-ingest" / "market-regime-intelligence.json", [])
    return data if isinstance(data, list) else []


def _packets() -> list[dict[str, Any]]:
    packet_root = REPO_ROOT / "docs" / "doctrine-packets"
    rows: list[dict[str, Any]] = []
    for path in sorted(packet_root.glob("*.json")):
        payload = _load_json(path, {})
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def _cards() -> list[dict[str, Any]]:
    card_root = REPO_ROOT / "docs" / "doctrine-cards"
    rows: list[dict[str, Any]] = []
    for path in sorted(card_root.glob("*.json")):
        payload = _load_json(path, {})
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def _canonical_host(raw: str) -> str:
    try:
        parsed = urlparse(raw)
    except ValueError:
        return ""
    host = parsed.netloc.lower().strip()
    return host[4:] if host.startswith("www.") else host


def _normalized_name(raw: str) -> str:
    return "".join(ch.lower() for ch in raw if ch.isalnum() or ch.isspace()).strip()


def build_research_backlog(repo_root: Path | None = None) -> Path:
    root = repo_root or REPO_ROOT
    approved = _approved_sources()
    candidates = _trader_candidates()
    next_to_research = _next_to_research()
    regime_rows = _market_regime_intelligence()
    packets = _packets()
    cards = _cards()

    approved_urls = {str(item.get("url", "")).strip() for item in approved if isinstance(item, dict)}
    approved_hosts = {_canonical_host(str(item.get("url", "")).strip()) for item in approved if isinstance(item, dict)}
    approved_authors = {_normalized_name(str(item.get("author", "")).strip()) for item in approved if isinstance(item, dict)}
    approved_styles = [str(item.get("style_family", "")).strip() for item in approved if isinstance(item, dict)]
    packet_source_ids = {
        str(source_id).strip()
        for packet in packets
        if isinstance(packet, dict)
        for source_id in packet.get("source_ids", [])
        if str(source_id).strip()
    }
    packet_card_ids = {str(item.get("card_id", "")).strip() for item in cards if isinstance(item, dict)}

    style_counts: dict[str, dict[str, Any]] = {}
    for item in approved:
        if not isinstance(item, dict):
            continue
        style = str(item.get("style_family", "")).strip()
        if not style:
            continue
        bucket = style_counts.setdefault(style, {"approved_source_count": 0, "packet_count": 0, "card_count": 0})
        bucket["approved_source_count"] += 1
    for packet in packets:
        if not isinstance(packet, dict):
            continue
        trader = str(packet.get("trader", "")).strip()
        matching_sources = [item for item in approved if isinstance(item, dict) and str(item.get("author", "")).strip() in {trader, trader.replace(" Analytics", "")}]
        styles = {str(item.get("style_family", "")).strip() for item in matching_sources if str(item.get("style_family", "")).strip()}
        if not styles:
            styles = {
                str(item.get("style_family", "")).strip()
                for item in approved
                if isinstance(item, dict) and str(item.get("source_id", "")).strip() in {str(source_id).strip() for source_id in packet.get("source_ids", [])}
            }
        for style in styles:
            bucket = style_counts.setdefault(style, {"approved_source_count": 0, "packet_count": 0, "card_count": 0})
            bucket["packet_count"] += 1
            if str(packet.get("card_id", "")).strip() in packet_card_ids:
                bucket["card_count"] += 1

    candidate_rows: list[dict[str, Any]] = []
    for item in candidates:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        url = str(item.get("access_url", "")).strip()
        style = str(item.get("style_family", "")).strip()
        normalized_name = _normalized_name(name.replace(" / ", " ").replace("-", " "))
        approved_present = (
            url in approved_urls
            or _canonical_host(url) in approved_hosts
            or any(normalized_name and normalized_name in author for author in approved_authors)
        )
        packet_present = any(
            isinstance(packet, dict) and str(packet.get("trader", "")).strip() == name
            for packet in packets
        )
        if packet_present:
            status = "packet_present"
        elif approved_present:
            status = "approved_waiting_packet"
        else:
            status = "ready_for_source_ingest"
        candidate_rows.append(
            {
                "name": name,
                "access_url": url,
                "access_type": item.get("access_type"),
                "style_family": style,
                "priority_tier": int(item.get("priority_tier", 9) or 9),
                "methodology_access": item.get("methodology_access"),
                "status": status,
            }
        )
    candidate_rows.sort(
        key=lambda row: (
            0 if str(row.get("status")) == "ready_for_source_ingest" else 1 if str(row.get("status")) == "approved_waiting_packet" else 2,
            int(row.get("priority_tier", 9) or 9),
            str(row.get("name", "")),
        )
    )

    style_rows = []
    for style, counts in sorted(style_counts.items()):
        row = {"style_family": style, **counts}
        if counts["packet_count"] <= 0:
            row["coverage_status"] = "approved_but_unpacketed"
        elif counts["card_count"] < counts["packet_count"]:
            row["coverage_status"] = "packet_backlog_available"
        else:
            row["coverage_status"] = "covered"
        style_rows.append(row)
    style_rows.sort(
        key=lambda row: (
            0 if str(row.get("coverage_status")) == "approved_but_unpacketed" else 1 if str(row.get("coverage_status")) == "packet_backlog_available" else 2,
            int(row.get("approved_source_count", 0) or 0),
            str(row.get("style_family", "")),
        )
    )

    futurelog_rows: list[dict[str, Any]] = []
    for item in next_to_research:
        if not isinstance(item, dict):
            continue
        futurelog_rows.append(
            {
                "item_id": str(item.get("item_id", "")).strip(),
                "title": str(item.get("title", "")).strip(),
                "priority": int(item.get("priority", 9) or 9),
                "status": str(item.get("status", "")).strip(),
                "style_families": item.get("style_families", []),
                "source_names": item.get("source_names", []),
                "why_now": str(item.get("why_now", "")).strip(),
                "target_regimes": item.get("target_regimes", []),
                "expected_child_shapes": item.get("expected_child_shapes", []),
            }
        )
    futurelog_rows.sort(
        key=lambda row: (
            int(row.get("priority", 9) or 9),
            str(row.get("status", "")),
            str(row.get("title", "")),
        )
    )

    normalized_regime_rows: list[dict[str, Any]] = []
    for item in regime_rows:
        if not isinstance(item, dict):
            continue
        windows = item.get("benchmark_window_targets", [])
        windows = windows if isinstance(windows, list) else []
        normalized_regime_rows.append(
            {
                "regime_id": str(item.get("regime_id", "")).strip(),
                "label": str(item.get("label", "")).strip(),
                "priority": int(item.get("priority", 9) or 9),
                "status": str(item.get("status", "")).strip(),
                "market_character": str(item.get("market_character", "")).strip(),
                "fit_patterns": item.get("fit_patterns", []),
                "avoid_patterns": item.get("avoid_patterns", []),
                "benchmark_window_targets": windows,
                "research_gaps": item.get("research_gaps", []),
            }
        )
    normalized_regime_rows.sort(
        key=lambda row: (
            int(row.get("priority", 9) or 9),
            str(row.get("status", "")),
            str(row.get("label", "")),
        )
    )

    payload = {
        "approved_source_count": len(approved),
        "trader_candidate_count": len(candidate_rows),
        "ready_for_source_ingest_count": sum(1 for row in candidate_rows if str(row.get("status")) == "ready_for_source_ingest"),
        "approved_waiting_packet_count": sum(1 for row in candidate_rows if str(row.get("status")) == "approved_waiting_packet"),
        "packet_count": len(packets),
        "card_count": len(cards),
        "candidate_rows": candidate_rows,
        "style_rows": style_rows,
        "next_to_research_count": len(futurelog_rows),
        "regime_intelligence_count": len(normalized_regime_rows),
        "futurelog_rows": futurelog_rows,
        "regime_rows": normalized_regime_rows,
        "top_ready_candidates": candidate_rows[:8],
        "top_undercovered_styles": style_rows[:8],
        "top_futurelog_items": futurelog_rows[:8],
        "top_regime_rows": normalized_regime_rows[:8],
    }

    target = root / "artifacts" / "research" / "research_backlog.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    safe_write_json(target, payload)
    return target


def main() -> None:
    path = build_research_backlog(REPO_ROOT)
    print(path)


if __name__ == "__main__":
    main()
