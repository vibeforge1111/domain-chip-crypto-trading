from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _load_packet(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _queue_row(packet: dict[str, Any], packet_path: Path) -> dict[str, Any]:
    mutations = packet.get("mutations", {})
    mutations = mutations if isinstance(mutations, dict) else {}
    return {
        "candidate_id": str(packet.get("candidate_id", "")),
        "run_id": str(packet.get("run_id", "")),
        "doctrine_id": str(packet.get("doctrine_id", "")),
        "strategy_id": str(packet.get("strategy_id", "")),
        "market_regime": str(packet.get("market_regime", "")),
        "timeframe": str(packet.get("timeframe", "")),
        "venue": str(packet.get("venue", "")),
        "asset_universe": str(packet.get("asset_universe", "")),
        "mutations": {str(key): str(value) for key, value in mutations.items()},
        "profitability_score": packet.get("profitability_score"),
        "paper_trade_readiness": packet.get("paper_trade_readiness"),
        "max_drawdown": packet.get("max_drawdown"),
        "trade_count": packet.get("trade_count"),
        "minimum_trade_count": packet.get("minimum_trade_count"),
        "trade_count_gate_pass": packet.get("trade_count_gate_pass"),
        "holdout_profitability_score": packet.get("holdout_profitability_score"),
        "walk_forward_consistency": packet.get("walk_forward_consistency"),
        "stress_resilience": packet.get("stress_resilience"),
        "eligibility_status": packet.get("eligibility_status"),
        "recommended_next_step": packet.get("recommended_next_step"),
        "primary_mechanism": packet.get("primary_mechanism"),
        "primary_boundary": packet.get("primary_boundary"),
        "bridge_packet_path": str(packet_path.relative_to(packet_path.parents[2])),
        "queue_status": "queued",
    }


def _pilot_queue_row(packet: dict[str, Any], relative_path: str) -> dict[str, Any]:
    mutations = packet.get("mutations", {})
    mutations = mutations if isinstance(mutations, dict) else {}
    return {
        "candidate_id": str(packet.get("candidate_id", "")),
        "run_id": str(packet.get("run_id", "")),
        "doctrine_id": str(packet.get("doctrine_id", "")),
        "strategy_id": str(packet.get("strategy_id", "")),
        "market_regime": str(packet.get("market_regime", "")),
        "timeframe": str(packet.get("timeframe", "")),
        "venue": str(packet.get("venue", "")),
        "asset_universe": str(packet.get("asset_universe", "")),
        "mutations": {str(key): str(value) for key, value in mutations.items()},
        "profitability_score": packet.get("profitability_score"),
        "paper_trade_readiness": packet.get("paper_trade_readiness"),
        "max_drawdown": packet.get("max_drawdown"),
        "trade_count": packet.get("trade_count"),
        "minimum_trade_count": packet.get("minimum_trade_count"),
        "trade_count_gate_pass": packet.get("trade_count_gate_pass"),
        "holdout_profitability_score": packet.get("holdout_profitability_score"),
        "walk_forward_consistency": packet.get("walk_forward_consistency"),
        "stress_resilience": packet.get("stress_resilience"),
        "eligibility_status": str(packet.get("eligibility_status", "pilot_override_best_candidate")),
        "recommended_next_step": str(packet.get("recommended_next_step", "paper_trade_pilot")),
        "primary_mechanism": packet.get("primary_mechanism"),
        "primary_boundary": packet.get("primary_boundary"),
        "bridge_packet_path": relative_path,
        "queue_status": str(packet.get("queue_status", "pilot_queued")),
        "queue_origin": str(packet.get("queue_origin", "manual_best_candidate_pilot")),
    }


def _pilot_rows(repo_root: Path) -> list[dict[str, Any]]:
    pilot_path = repo_root / "artifacts" / "paper_trade" / "pilot_queue_requests.json"
    if not pilot_path.exists():
        return []
    packet = _load_packet(pilot_path)
    if not packet:
        return []
    rows = packet.get("rows", [])
    rows = rows if isinstance(rows, list) else []
    relative_path = str(pilot_path.relative_to(repo_root))
    queue_rows: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        queue_rows.append(_pilot_queue_row(row, relative_path))
    return queue_rows


def _forge_rows(repo_root: Path) -> list[dict[str, Any]]:
    """Load forge-promoted candidates from bridge_packets directory."""
    forge_bridge = repo_root / "artifacts" / "bridge_packets"
    if not forge_bridge.exists():
        return []
    rows: list[dict[str, Any]] = []
    for path in sorted(forge_bridge.glob("forge-*.json")):
        packet = _load_packet(path)
        if not packet:
            continue
        row = _queue_row(packet, path)
        row["queue_origin"] = "forge"
        rows.append(row)
    return rows


def build_paper_trade_queue(repo_root: Path) -> Path:
    bridge_root = repo_root / "artifacts" / "promotion" / "benchmark_grounded"
    target_root = repo_root / "artifacts" / "paper_trade"
    target_root.mkdir(parents=True, exist_ok=True)
    queue_path = target_root / "paper_trade_queue.json"
    queue_rows: list[dict[str, Any]] = []
    if bridge_root.exists():
        for path in sorted(bridge_root.glob("*.json")):
            packet = _load_packet(path)
            if not packet:
                continue
            if str(packet.get("recommended_next_step", "")) != "queue_for_paper_trade":
                continue
            queue_rows.append(_queue_row(packet, path))
    queue_rows.extend(_pilot_rows(repo_root))
    queue_rows.extend(_forge_rows(repo_root))
    queue_rows.sort(
        key=lambda row: (
            float(row.get("paper_trade_readiness", 0.0) or 0.0),
            float(row.get("profitability_score", 0.0) or 0.0),
            -float(row.get("max_drawdown", 0.0) or 0.0),
        ),
        reverse=True,
    )
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "contract_family": "btc_up_down_15m",
        "queue_count": len(queue_rows),
        "rows": queue_rows,
    }
    # Write to temp file then rename to avoid Errno 22 on Windows (file lock / concurrent access)
    content = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    tmp_fd, tmp_path = tempfile.mkstemp(dir=queue_path.parent, suffix=".tmp")
    try:
        with open(tmp_fd, "w", encoding="utf-8") as f:
            f.write(content)
        Path(tmp_path).replace(queue_path)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise
    return queue_path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    path = build_paper_trade_queue(repo_root)
    print(path)


if __name__ == "__main__":
    main()
