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


def _failure_modes(row: dict[str, Any]) -> list[dict[str, str]]:
    result = row.get("result", {})
    result = result if isinstance(result, dict) else {}
    metrics = row.get("metrics", {})
    metrics = metrics if isinstance(metrics, dict) else {}
    modes: list[dict[str, str]] = []
    if not bool(result.get("trade_count_gate_pass")):
        modes.append(
            {
                "mode": "sparse_signal",
                "evidence": "Trade count stays below the minimum gate, so the candidate may be a local curve rather than a repeatable contract edge.",
                "probe": "Tighten no-trade boundaries or widen the activation logic, then re-run on the same dataset to see whether trade count can rise without collapsing profitability.",
            }
        )
    if float(result.get("holdout_profitability_score", 0.0) or 0.0) < 0.5:
        modes.append(
            {
                "mode": "holdout_decay",
                "evidence": "The final holdout slice drops below break-even profitability after fees.",
                "probe": "Inspect the last walk-forward segment and add regime filters that explicitly block the failing late-sample conditions.",
            }
        )
    if float(result.get("walk_forward_consistency", 0.0) or 0.0) < 0.8:
        modes.append(
            {
                "mode": "segment_instability",
                "evidence": "Walk-forward consistency is too low across chronological splits.",
                "probe": "Split the weakest chronological segment into its own contradiction lane and mutate around the regime that failed there instead of averaging across the full sample.",
            }
        )
    if float(result.get("stress_resilience", 0.0) or 0.0) < 1.0:
        modes.append(
            {
                "mode": "execution_fragility",
                "evidence": "Edge does not survive elevated fees and slippage cleanly.",
                "probe": "Bias new mutations toward higher expected move thresholds or fewer trades so the setup can absorb venue friction.",
            }
        )
    if float(metrics.get("max_drawdown", 0.0) or 0.0) > 0.22:
        modes.append(
            {
                "mode": "drawdown_excess",
                "evidence": "Drawdown remains above the promotion boundary even when trade count is adequate.",
                "probe": "Add stricter risk-first filters or no-trade doctrine boundaries before touching sizing or paper-trade escalation.",
            }
        )
    return modes


def _weakest_segments(row: dict[str, Any]) -> list[dict[str, Any]]:
    result = row.get("result", {})
    result = result if isinstance(result, dict) else {}
    segments = result.get("walk_forward_stats", [])
    segments = segments if isinstance(segments, list) else []
    ranked = sorted(
        [item for item in segments if isinstance(item, dict)],
        key=lambda item: (
            float(item.get("profitability_score", 0.0) or 0.0),
            float(item.get("avg_return", 0.0) or 0.0),
        ),
    )
    return ranked[:2]


def _probe_packet(row: dict[str, Any]) -> dict[str, Any]:
    candidate_id = str(row.get("candidate_id", "")).strip()
    mutations = row.get("mutations", {})
    mutations = mutations if isinstance(mutations, dict) else {}
    result = row.get("result", {})
    result = result if isinstance(result, dict) else {}
    metrics = row.get("metrics", {})
    metrics = metrics if isinstance(metrics, dict) else {}
    failure_modes = _failure_modes(row)
    weakest_segments = _weakest_segments(row)
    primary_mode = failure_modes[0]["mode"] if failure_modes else "unknown"
    sparse_penalty = 0.2 if not bool(result.get("trade_count_gate_pass")) else 0.0
    holdout_penalty = min(0.25, max(0.0, 0.5 - float(result.get("holdout_profitability_score", 0.0) or 0.0)) * 1.5)
    walk_penalty = min(0.2, max(0.0, 0.8 - float(result.get("walk_forward_consistency", 0.0) or 0.0)) * 0.25)
    stress_penalty = min(0.15, max(0.0, 1.0 - float(result.get("stress_resilience", 0.0) or 0.0)) * 0.15)
    drawdown_penalty = min(0.2, max(0.0, float(metrics.get("max_drawdown", 0.0) or 0.0) - 0.22) * 0.25)
    return {
        "probe_id": f"{candidate_id}-{primary_mode}",
        "candidate_id": candidate_id,
        "source_lane": "backtest",
        "doctrine_id": mutations.get("doctrine_id"),
        "strategy_id": mutations.get("strategy_id"),
        "market_regime": mutations.get("market_regime"),
        "priority": round(min(0.99, 0.25 + sparse_penalty + holdout_penalty + walk_penalty + stress_penalty + drawdown_penalty), 4),
        "recommended_next_step": result.get("recommended_next_step"),
        "trade_count": result.get("trade_count"),
        "minimum_trade_count": result.get("minimum_trade_count"),
        "holdout_profitability_score": result.get("holdout_profitability_score"),
        "walk_forward_consistency": result.get("walk_forward_consistency"),
        "stress_resilience": result.get("stress_resilience"),
        "max_drawdown": metrics.get("max_drawdown"),
        "failure_modes": failure_modes,
        "weakest_segments": weakest_segments,
        "probe_thesis": "Use the benchmark failure surface itself as the next mutation source instead of adding a fresh doctrine blindly.",
    }


def _paper_trade_failure_modes(row: dict[str, Any]) -> list[dict[str, str]]:
    modes: list[dict[str, str]] = []
    trade_count = int(row.get("trade_count", 0) or 0)
    sample_contract_count = int(row.get("sample_contract_count", 0) or 0)
    if sample_contract_count and trade_count < max(8, sample_contract_count // 10):
        modes.append(
            {
                "mode": "shadow_participation_sparse",
                "evidence": "The paper-trade slice produced too few live-like decisions, so the candidate may only look good when benchmark participation is averaged across a much larger sample.",
                "probe": "Tighten entry quality around the exact paper-trade shadow windows and add session or reclaim filters that reduce skip-heavy drift without opening the floodgates.",
            }
        )
    if float(row.get("max_drawdown", 0.0) or 0.0) > 0.3:
        modes.append(
            {
                "mode": "shadow_drawdown_excess",
                "evidence": "The shadow paper-trade slice experienced live-like drawdown far beyond the bridge comfort zone.",
                "probe": "Bias new mutations toward stricter drawdown guards, edge-only participation, and stronger reversal confirmation before trying to widen trade count again.",
            }
        )
    if float(row.get("profitability_score", 0.0) or 0.0) < 0.5 or str(row.get("paper_trade_recommendation", "")) == "demote_to_benchmark":
        modes.append(
            {
                "mode": "paper_trade_demotion",
                "evidence": "The candidate failed outer validation and was demoted back to benchmark refinement.",
                "probe": "Use the shadow slice as a direct contradiction packet and mutate the candidate around live-like execution, abstention, and session timing instead of relying on the older blended benchmark alone.",
            }
        )
    return modes


def _paper_trade_probes() -> list[dict[str, Any]]:
    summary_path = REPO_ROOT / "artifacts" / "paper_trade" / "paper_trade_summary.json"
    queue_path = REPO_ROOT / "artifacts" / "paper_trade" / "paper_trade_queue.json"
    summary = _load_json(summary_path, {})
    summary = summary if isinstance(summary, dict) else {}
    queue = _load_json(queue_path, {})
    queue = queue if isinstance(queue, dict) else {}
    summary_rows = summary.get("rows", [])
    summary_rows = summary_rows if isinstance(summary_rows, list) else []
    queue_rows = queue.get("rows", [])
    queue_rows = queue_rows if isinstance(queue_rows, list) else []
    queue_index: dict[str, dict[str, Any]] = {}
    for row in queue_rows:
        if not isinstance(row, dict):
            continue
        candidate_id = str(row.get("candidate_id", "")).strip()
        if candidate_id:
            queue_index[candidate_id] = row
    probes: list[dict[str, Any]] = []
    for row in summary_rows:
        if not isinstance(row, dict):
            continue
        candidate_id = str(row.get("candidate_id", "")).strip()
        if not candidate_id:
            continue
        failure_modes = _paper_trade_failure_modes(row)
        if not failure_modes:
            continue
        queue_row = queue_index.get(candidate_id, {})
        primary_mode = failure_modes[0]["mode"]
        profitability_penalty = min(0.25, max(0.0, 0.5 - float(row.get("profitability_score", 0.0) or 0.0)) * 1.5)
        drawdown_penalty = min(0.25, max(0.0, float(row.get("max_drawdown", 0.0) or 0.0) - 0.22) * 0.35)
        sparse_penalty = 0.2 if int(row.get("trade_count", 0) or 0) < max(8, int(row.get("sample_contract_count", 0) or 0) // 10) else 0.0
        probes.append(
            {
                "probe_id": f"{candidate_id}-{primary_mode}-paper-trade",
                "candidate_id": candidate_id,
                "source_lane": "paper_trade",
                "doctrine_id": queue_row.get("doctrine_id"),
                "strategy_id": queue_row.get("strategy_id"),
                "market_regime": queue_row.get("market_regime"),
                "priority": round(min(0.99, 0.35 + profitability_penalty + drawdown_penalty + sparse_penalty), 4),
                "recommended_next_step": "run_contradiction_probe",
                "trade_count": row.get("trade_count"),
                "minimum_trade_count": max(8, int(row.get("sample_contract_count", 0) or 0) // 10),
                "holdout_profitability_score": row.get("profitability_score"),
                "walk_forward_consistency": 0.0,
                "stress_resilience": 0.0,
                "max_drawdown": row.get("max_drawdown"),
                "failure_modes": failure_modes,
                "weakest_segments": [
                    {
                        "segment_id": "paper-trade-shadow",
                        "start_contract_id": row.get("start_contract_id"),
                        "end_contract_id": row.get("end_contract_id"),
                        "profitability_score": row.get("profitability_score"),
                        "trade_count": row.get("trade_count"),
                        "trade_count_gate_pass": int(row.get("trade_count", 0) or 0) >= max(8, int(row.get("sample_contract_count", 0) or 0) // 10),
                        "win_rate": row.get("win_rate"),
                        "avg_return": row.get("profitability_score"),
                    }
                ],
                "probe_thesis": "Use the paper-trade demotion itself as a contradiction packet so the next mutation learns from live-like failure instead of only blended backtest residue.",
            }
        )
    return probes


def main() -> None:
    summary_path = REPO_ROOT / "artifacts" / "backtests" / "heavy_backtest_summary.json"
    summary = _load_json(summary_path, {})
    rows = summary.get("rows", [])
    rows = rows if isinstance(rows, list) else []
    probes = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("candidate_id", "")).strip() == "global-baseline":
            continue
        result = row.get("result", {})
        result = result if isinstance(result, dict) else {}
        if str(result.get("recommended_next_step", "")) != "run_contradiction_probe":
            continue
        probes.append(_probe_packet(row))
    probes.extend(_paper_trade_probes())
    probes.sort(key=lambda item: float(item.get("priority", 0.0) or 0.0), reverse=True)
    target_root = REPO_ROOT / "artifacts" / "recursion"
    target_root.mkdir(parents=True, exist_ok=True)
    path = target_root / "contradiction_probes.json"
    safe_write_json(path, probes)
    print(path)


if __name__ == "__main__":
    main()
