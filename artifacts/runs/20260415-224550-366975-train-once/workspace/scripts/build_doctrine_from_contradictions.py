"""Generate doctrine packets from contradiction probes.

This closes the recursive gap: failures -> contradictions -> doctrine packets -> learning loop -> new cards -> new candidates -> new failures.

Without this script the learning loop starves (pending_packet_count stays 0) because doctrine packets were only created manually.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from safe_write import safe_write_json

REPO_ROOT = Path(__file__).resolve().parents[1]

FAILURE_MODE_TO_DOCTRINE_TEMPLATE: dict[str, dict[str, Any]] = {
    "sparse_signal": {
        "research_thesis_template": "The {doctrine_id} doctrine with {strategy_id} strategy produces too few trades in {market_regime} regime. Wider activation or a different feature combination is needed to capture more valid setups without destroying edge quality.",
        "root_lesson_template": "Sparse signal means the entry logic is too restrictive or misaligned with the regime. Wider activation must be paired with quality filters to avoid diluting the edge.",
        "mutation_overrides": {"activation_profile": "wider"},
    },
    "holdout_decay": {
        "research_thesis_template": "The {doctrine_id} doctrine loses edge in the most recent data segment. Late-sample guards or regime-adaptive thresholds should stabilize holdout performance for {strategy_id}.",
        "root_lesson_template": "Holdout decay signals regime drift. The fix is not curve-fitting the latest segment but adding guards that skip unstable conditions.",
        "mutation_overrides": {"late_sample_guard": "on", "volume_context_guard": "thin_filter"},
    },
    "drawdown_excess": {
        "research_thesis_template": "The {doctrine_id} doctrine with {strategy_id} hits excessive drawdown ({max_drawdown:.0%}) in {market_regime} regime. Tighter risk filters must reduce drawdown below 20% while maintaining trade density.",
        "root_lesson_template": "Drawdown excess means the strategy takes trades in conditions where the risk-reward is unfavorable. Reduce participation in high-volatility or thin-volume environments.",
        "mutation_overrides": {"drawdown_guard": "high", "execution_buffer": "high"},
    },
    "segment_instability": {
        "research_thesis_template": "The {doctrine_id} doctrine shows inconsistent walk-forward performance. Some segments are profitable while others collapse. Regime-conditional entry thresholds should improve consistency.",
        "root_lesson_template": "Segment instability means the edge is regime-dependent but the entry logic is regime-blind. Add regime detection or session filters.",
        "mutation_overrides": {"session_profile": "squeeze_release_window"},
    },
    "execution_fragility": {
        "research_thesis_template": "The {doctrine_id} doctrine's edge does not survive elevated fees and slippage for {strategy_id}. Higher expected-move thresholds or fewer trades should absorb venue friction.",
        "root_lesson_template": "If the edge disappears under realistic execution costs, it was never a real edge. Require larger expected moves or tighter entry criteria.",
        "mutation_overrides": {"execution_buffer": "high", "activation_profile": "stricter"},
    },
}

DOCTRINE_FAMILIES = {
    "trend_regime_following": {
        "strategy_family": "ema_trend_continuation",
        "default_strategy_id": "ema_pullback_long",
        "secondary_source": "ed-seykota-principles-of-great-traders",
    },
    "mean_reversion_liquidity_reclaim": {
        "strategy_family": "range_reclaim_rotation",
        "default_strategy_id": "range_reclaim_scalp",
        "secondary_source": "wyckoff-springs-upthrusts",
    },
    "breakout_volatility_expansion": {
        "strategy_family": "breakout_expansion_confirmation",
        "default_strategy_id": "bollinger_squeeze_breakout",
        "secondary_source": "john-bollinger-bands",
    },
    "risk_first_asymmetric_capture": {
        "strategy_family": "asymmetric_capture",
        "default_strategy_id": "funding_mean_revert",
        "secondary_source": "edward-thorp-kelly",
    },
}


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _existing_packet_ids(packet_root: Path) -> set[str]:
    ids: set[str] = set()
    for path in packet_root.glob("*.json"):
        payload = _load_json(path, {})
        if isinstance(payload, dict):
            pid = str(payload.get("packet_id", "")).strip()
            if pid:
                ids.add(pid)
    return ids


def _build_packet(probe: dict[str, Any], failure_mode: str) -> dict[str, Any] | None:
    template_entry = FAILURE_MODE_TO_DOCTRINE_TEMPLATE.get(failure_mode)
    if not template_entry:
        return None

    candidate_id = str(probe.get("candidate_id", "")).strip()
    doctrine_id = str(probe.get("doctrine_id", "")).strip()
    strategy_id = str(probe.get("strategy_id", "")).strip()
    market_regime = str(probe.get("market_regime", "")).strip()
    max_drawdown = float(probe.get("max_drawdown", 0) or 0)
    trade_count = int(probe.get("trade_count", 0) or 0)

    if not candidate_id or not doctrine_id:
        return None

    # Truncate long candidate IDs to avoid Windows MAX_PATH on filenames
    id_slug = f"{candidate_id}-{failure_mode}"
    if len(id_slug) > 80:
        short_hash = hashlib.sha256(id_slug.encode()).hexdigest()[:8]
        id_slug = f"{candidate_id[:60]}-{short_hash}-{failure_mode}"
    packet_id = f"dp-auto-{id_slug}"
    card_id = f"dc-auto-{id_slug}"

    format_vars = {
        "doctrine_id": doctrine_id,
        "strategy_id": strategy_id or "unknown",
        "market_regime": market_regime or "unknown",
        "max_drawdown": max_drawdown,
        "trade_count": trade_count,
        "candidate_id": candidate_id,
    }

    doctrine_family_info = DOCTRINE_FAMILIES.get(doctrine_id, {})

    base_mutations = {
        "doctrine_id": doctrine_id,
        "strategy_id": strategy_id or doctrine_family_info.get("default_strategy_id", ""),
        "market_regime": market_regime,
        "asset_universe": "BTC",
        "timeframe": "15m",
        "venue": "kalshi",
        "paper_gate": "balanced",
    }
    base_mutations.update(template_entry.get("mutation_overrides", {}))

    failure_details = probe.get("failure_modes", [])
    lineage_failures = []
    for fd in failure_details:
        if isinstance(fd, dict):
            lineage_failures.append(f"{fd.get('mode', 'unknown')}: {fd.get('evidence', '')}")
        elif isinstance(fd, str):
            lineage_failures.append(fd)

    return {
        "packet_id": packet_id,
        "card_id": card_id,
        "packet_status": "ready_for_card_ingest",
        "title": f"Auto-generated: {failure_mode} fix for {candidate_id}",
        "research_thesis": template_entry["research_thesis_template"].format(**format_vars),
        "root_lesson": template_entry["root_lesson_template"].format(**format_vars),
        "doctrine_family": doctrine_id,
        "strategy_family": doctrine_family_info.get("strategy_family", strategy_id),
        "target_contract_family": "btc_up_down_15m",
        "mechanism": f"Generated from contradiction probe on {candidate_id} targeting {failure_mode} failure surface.",
        "setup_definition": f"Apply {failure_mode}-targeted mutation overrides to {candidate_id} signal logic and benchmark.",
        "mutation_template": base_mutations,
        "lineage_failures": lineage_failures[:5],
        "counterfactual": f"Without addressing {failure_mode}, this candidate family will remain stuck at the current benchmark quality.",
        "ghost_improvement_check": f"Reject if the mutation does not materially improve the {failure_mode} metric while maintaining profitability.",
        "rollback_condition": f"Rollback if profitability drops below parent or if the fix introduces a new failure mode.",
        "no_trade_boundaries": [
            f"Skip conditions identified by the {failure_mode} probe as contributing to poor performance."
        ],
        "benchmark_priority": "high" if failure_mode in {"holdout_decay", "drawdown_excess"} else "medium",
        "ingest_priority": 150 if failure_mode in {"holdout_decay", "drawdown_excess"} else 100,
        "proposal_id": f"auto-{candidate_id}-{failure_mode}",
        "source_ids": ["autoloop_contradiction_probe", doctrine_family_info.get("secondary_source", "autoloop_contradiction_probe")],
        "source_urls": [],
        "trader": "recursive_flywheel",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "generation_source": "build_doctrine_from_contradictions",
    }


def build_doctrine_from_contradictions(repo_root: Path) -> dict[str, Any]:
    probes = _load_json(repo_root / "artifacts" / "recursion" / "contradiction_probes.json", [])
    probes = probes if isinstance(probes, list) else []

    packet_root = repo_root / "docs" / "doctrine-packets"
    packet_root.mkdir(parents=True, exist_ok=True)
    existing_ids = _existing_packet_ids(packet_root)

    generated: list[str] = []
    skipped_duplicate: list[str] = []
    skipped_no_template: list[str] = []

    for probe in probes:
        if not isinstance(probe, dict):
            continue

        priority = float(probe.get("priority", 0) or 0)
        if priority < 0.3:
            continue

        failure_modes = probe.get("failure_modes", [])
        if isinstance(failure_modes, list):
            mode_ids = []
            for fm in failure_modes:
                if isinstance(fm, dict):
                    mode_ids.append(str(fm.get("mode", "")).strip())
                elif isinstance(fm, str):
                    mode_ids.append(fm.strip())
        else:
            mode_ids = []

        primary_mode = mode_ids[0] if mode_ids else ""
        if not primary_mode:
            continue

        packet = _build_packet(probe, primary_mode)
        if packet is None:
            skipped_no_template.append(str(probe.get("candidate_id", "")))
            continue

        packet_id = packet["packet_id"]
        if packet_id in existing_ids:
            skipped_duplicate.append(packet_id)
            continue

        path = packet_root / f"{packet_id}.json"
        safe_write_json(path, packet)
        existing_ids.add(packet_id)
        generated.append(packet_id)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "probes_analyzed": len(probes),
        "packets_generated": len(generated),
        "generated_packet_ids": generated,
        "skipped_duplicate_count": len(skipped_duplicate),
        "skipped_no_template_count": len(skipped_no_template),
    }

    report_path = repo_root / "artifacts" / "recursion" / "doctrine_generation_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    safe_write_json(report_path, report)

    return report


def main() -> None:
    report = build_doctrine_from_contradictions(REPO_ROOT)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
