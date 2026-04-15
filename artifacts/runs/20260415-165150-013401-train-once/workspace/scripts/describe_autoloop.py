from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
AUTOLOOP_ROOT = REPO_ROOT / "autoloop"
CONTROL_PLANE_PATH = AUTOLOOP_ROOT / "control-plane.json"


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _ready_packet_count(packet_root: Path) -> int:
    ready = 0
    for path in packet_root.glob("*.json"):
        payload = _load_json(path, {})
        if isinstance(payload, dict) and str(payload.get("packet_status", "")).strip() == "ready_for_card_ingest":
            ready += 1
    return ready


def _lane_policy(policy: dict[str, Any], lane_id: str) -> dict[str, Any]:
    lanes = policy.get("loops", {})
    if not isinstance(lanes, dict):
        return {}
    lane = lanes.get(lane_id, {})
    return lane if isinstance(lane, dict) else {}


def _blocked_paths_from_reason(reason: str | None) -> list[str]:
    if not reason:
        return []
    prefix = "tracked worktree is dirty:"
    if not reason.startswith(prefix):
        return []
    raw = reason[len(prefix) :].strip()
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _build_summary() -> dict[str, Any]:
    manifest = _load_json(REPO_ROOT / "docs" / "recursion" / "autoloop-manifest.json", {})
    policy = _load_json(REPO_ROOT / "docs" / "recursion" / "autoloop-policy.json", {})
    state = _load_json(REPO_ROOT / "artifacts" / "recursion" / "autoloop_state.json", {})
    backtest_report = _load_json(REPO_ROOT / "artifacts" / "backtests" / "backtest_loop_report.json", {})
    learning_report = _load_json(REPO_ROOT / "artifacts" / "research" / "learning_loop_report.json", {})
    paper_trade_queue = _load_json(REPO_ROOT / "artifacts" / "paper_trade" / "paper_trade_queue.json", {})

    doctrine_card_count = len(list((REPO_ROOT / "docs" / "doctrine-cards").glob("*.json")))
    doctrine_packet_count = len(list((REPO_ROOT / "docs" / "doctrine-packets").glob("*.json")))
    ready_packet_count = _ready_packet_count(REPO_ROOT / "docs" / "doctrine-packets")

    after = backtest_report.get("after", {}) if isinstance(backtest_report.get("after"), dict) else {}
    benchmark = after.get("benchmark", {}) if isinstance(after.get("benchmark"), dict) else {}
    learning_after = learning_report.get("after", {}) if isinstance(learning_report.get("after"), dict) else {}

    queue_rows = paper_trade_queue.get("rows", []) if isinstance(paper_trade_queue, dict) else []
    queue_count = int(paper_trade_queue.get("queue_count", 0) or 0) if isinstance(paper_trade_queue, dict) else 0

    blocked_reason = state.get("reason")
    blocked_paths = _blocked_paths_from_reason(str(blocked_reason) if blocked_reason else None)

    summary = {
        "autoloop": {
            "id": manifest.get("autoloop_id", "unknown"),
            "name": manifest.get("name", "unknown"),
            "mission": manifest.get("mission", ""),
            "governing_candidate_unit": manifest.get("governing_candidate_unit", "unknown"),
            "primary_contract_family": manifest.get("primary_contract_family", "unknown"),
            "assets": manifest.get("assets", []),
            "timeframes": manifest.get("timeframes", []),
        },
        "status": {
            "status": state.get("status", "active"),
            "cycle_count": int(state.get("cycle_count", 0) or 0),
            "noop_streak": int(state.get("noop_streak", 0) or 0),
            "last_learning_cycle": int(state.get("last_learning_cycle", 0) or 0),
            "last_backtest_cycle": int(state.get("last_backtest_cycle", 0) or 0),
            "last_paper_trade_cycle": int(state.get("last_paper_trade_cycle", 0) or 0),
            "last_top_candidate_id": state.get("last_top_candidate_id"),
            "blocked_reason": blocked_reason,
            "blocked_path_count": len(blocked_paths),
            "blocked_path_sample": blocked_paths[:10],
        },
        "inventory": {
            "doctrine_card_count": doctrine_card_count,
            "doctrine_packet_count": doctrine_packet_count,
            "ready_packet_count": ready_packet_count,
            "learning_added_count": int(learning_after.get("added_count", 0) or 0),
            "benchmark_candidate_count": int(benchmark.get("candidate_count", 0) or 0),
            "benchmark_top_candidate_id": benchmark.get("top_candidate_id"),
            "benchmark_top_next_step": benchmark.get("top_recommended_next_step"),
            "paper_trade_queue_count": queue_count,
            "paper_trade_top_candidate_id": queue_rows[0].get("candidate_id") if queue_rows else None,
        },
        "policy": {
            lane_id: {
                "enabled": bool(_lane_policy(policy, lane_id).get("enabled", True)),
                "every_n_cycles": int(_lane_policy(policy, lane_id).get("every_n_cycles", 1) or 1),
            }
            for lane_id in ("learning", "backtest", "paper_trade")
        },
        "operator_surface": manifest.get("operator_surface", {}),
    }
    operator_surface = summary["operator_surface"]
    if isinstance(operator_surface, dict):
        operator_surface["autoloop_root"] = str(AUTOLOOP_ROOT.relative_to(REPO_ROOT))
        operator_surface["control_plane"] = str(CONTROL_PLANE_PATH.relative_to(REPO_ROOT))
    return summary


def _recommendation(summary: dict[str, Any]) -> str:
    status = str(summary.get("status", {}).get("status", "active"))
    ready_packets = int(summary.get("inventory", {}).get("ready_packet_count", 0) or 0)
    queue_count = int(summary.get("inventory", {}).get("paper_trade_queue_count", 0) or 0)
    benchmark_next = str(summary.get("inventory", {}).get("benchmark_top_next_step", "") or "")

    if status == "blocked":
        return "Supervisor is blocked. Review tracked artifact changes before resuming the autoloop."
    if ready_packets > 0:
        return "Learning is the current bottleneck. Ingest ready doctrine packets into doctrine cards."
    if queue_count > 0:
        return "Paper trade has queued candidates. Outer validation is the current bottleneck."
    if benchmark_next:
        return f"Backtest remains the active decision surface. Current top next step: {benchmark_next}."
    return "No dominant bottleneck detected. Refresh watchtower and run one bounded supervisor cycle."


def _render_text(summary: dict[str, Any]) -> str:
    autoloop = summary["autoloop"]
    status = summary["status"]
    inventory = summary["inventory"]
    policy = summary["policy"]
    operator_surface = summary["operator_surface"]

    lines = [
        f"Autoloop: {autoloop['name']}",
        f"Status: {status['status']} | cycle {status['cycle_count']} | noop streak {status['noop_streak']}",
        f"Governing unit: {autoloop['governing_candidate_unit']}",
        f"Scope: contract family={autoloop['primary_contract_family']} | assets={', '.join(autoloop['assets'])} | timeframes={', '.join(autoloop['timeframes'])}",
        "",
        "Lanes:",
        f"- learning: every {policy['learning']['every_n_cycles']} cycles | enabled={policy['learning']['enabled']}",
        f"- backtest: every {policy['backtest']['every_n_cycles']} cycles | enabled={policy['backtest']['enabled']}",
        f"- paper_trade: every {policy['paper_trade']['every_n_cycles']} cycles | enabled={policy['paper_trade']['enabled']}",
        "",
        "Inventory:",
        f"- doctrine cards: {inventory['doctrine_card_count']}",
        f"- doctrine packets: {inventory['doctrine_packet_count']}",
        f"- ready packets: {inventory['ready_packet_count']}",
        f"- benchmark candidates: {inventory['benchmark_candidate_count']}",
        f"- benchmark leader: {inventory['benchmark_top_candidate_id'] or 'n/a'}",
        f"- benchmark next step: {inventory['benchmark_top_next_step'] or 'n/a'}",
        f"- paper-trade queue: {inventory['paper_trade_queue_count']}",
        f"- top queued candidate: {inventory['paper_trade_top_candidate_id'] or 'n/a'}",
        "",
        "Operator Surface:",
        f"- autoloop root: {operator_surface.get('autoloop_root', 'n/a')}",
        f"- control plane: {operator_surface.get('control_plane', 'n/a')}",
        f"- watchtower builder: {operator_surface.get('watchtower_builder', 'n/a')}",
        f"- status script: {operator_surface.get('status_script', 'n/a')}",
        f"- vault root: {operator_surface.get('vault_root', 'n/a')}",
        "",
        f"Recommendation: {_recommendation(summary)}",
    ]
    blocked_reason = status.get("blocked_reason")
    if blocked_reason:
        blocked_path_count = int(status.get("blocked_path_count", 0) or 0)
        blocked_path_sample = status.get("blocked_path_sample", [])
        lines.extend(["", f"Blocked reason: {blocked_reason.split(':', 1)[0]}"])
        if blocked_path_count > 0:
            lines.append(f"- dirty tracked paths: {blocked_path_count}")
        for path in blocked_path_sample:
            lines.append(f"- sample path: {path}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Describe the current crypto-trading autoloop state.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    summary = _build_summary()
    if args.format == "json":
        print(json.dumps(summary, indent=2, sort_keys=True))
        return
    print(_render_text(summary))


if __name__ == "__main__":
    main()
