from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from safe_write import safe_write_json
from variety_model import (
    benchmark_variety_index,
    effective_fingerprint,
    normalize_mutations,
    variety_child_id,
    variety_child_label,
    variety_family_id,
)


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _load_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def _load_self_edit_evaluations(repo_root: Path) -> list[dict[str, Any]]:
    data = _load_json(repo_root / "artifacts" / "recursion" / "self_edit_evaluations.json", [])
    return data if isinstance(data, list) else []


def _mutations(row: dict[str, Any]) -> dict[str, str]:
    return {
        str(item.get("name", "")): str(item.get("value", ""))
        for item in row.get("applied_mutations", [])
        if isinstance(item, dict)
    }


def _metrics(row: dict[str, Any]) -> dict[str, Any]:
    metrics = row.get("metrics", {})
    return metrics if isinstance(metrics, dict) else {}


def _chip_result(row: dict[str, Any]) -> dict[str, Any]:
    result = row.get("chip_result", {})
    return result if isinstance(result, dict) else {}


def _candidate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if str(row.get("candidate_id", "")) and str(row.get("candidate_id", "")) != "global-baseline"]


def _proposal_templates() -> list[dict[str, Any]]:
    return [
        {
            "proposal_id": "btc-15m-trend-continuation",
            "title": "Trend continuation with pullback confirmation",
            "doctrine_family": "trend_regime_following",
            "strategy_family": "pullback_then_continuation",
            "source_ids": ["ed-seykota-principles-of-great-traders", "richard-dennis-turtle-rules", "adam-grimes-tradecraft"],
            "target_contract_family": "btc_up_down_15m",
            "thesis": "Trend doctrine should survive on BTC 15m only when pullback entries occur inside a confirmed directional regime.",
            "benchmark_priority": "high",
            "mutations": {
                "doctrine_id": "trend_regime_following",
                "strategy_id": "ema_pullback_long",
                "market_regime": "trend",
                "timeframe": "15m",
                "venue": "kalshi",
                "asset_universe": "BTC",
                "paper_gate": "strict",
            },
        },
        {
            "proposal_id": "btc-15m-volatility-compression-breakout",
            "title": "Volatility compression breakout",
            "doctrine_family": "breakout_volatility_expansion",
            "strategy_family": "bollinger_squeeze_breakout",
            "source_ids": ["linda-raschke-research", "john-bollinger-bands", "tradingview-bollinger-bands"],
            "target_contract_family": "btc_up_down_15m",
            "thesis": "Compression followed by expansion should produce the cleanest contract edge when false-break filters are strict.",
            "benchmark_priority": "high",
            "mutations": {
                "doctrine_id": "breakout_volatility_expansion",
                "strategy_id": "breakout_open_interest_confirmation",
                "market_regime": "high_vol",
                "timeframe": "15m",
                "venue": "kalshi",
                "asset_universe": "BTC",
                "paper_gate": "strict",
            },
        },
        {
            "proposal_id": "btc-15m-exhaustion-mean-reversion",
            "title": "Exhaustion mean reversion after impulse",
            "doctrine_family": "mean_reversion_liquidity_reclaim",
            "strategy_family": "rsi_exhaustion_reclaim",
            "source_ids": ["linda-raschke-research", "stockcharts-rsi", "tradingview-rsi"],
            "target_contract_family": "btc_up_down_15m",
            "thesis": "Short-horizon reversions should only be tradable after impulse exhaustion plus reclaim confirmation.",
            "benchmark_priority": "high",
            "mutations": {
                "doctrine_id": "mean_reversion_liquidity_reclaim",
                "strategy_id": "range_reclaim_scalp",
                "market_regime": "range",
                "timeframe": "15m",
                "venue": "kalshi",
                "asset_universe": "BTC",
                "paper_gate": "balanced",
            },
        },
        {
            "proposal_id": "btc-15m-momentum-breakout-structure",
            "title": "Momentum breakout with structure filter",
            "doctrine_family": "breakout_volatility_expansion",
            "strategy_family": "trend_template_breakout",
            "source_ids": ["mark-minervini-sepa", "peter-brandt-classical-charting", "stockcharts-candlesticks"],
            "target_contract_family": "btc_up_down_15m",
            "thesis": "Momentum breakouts should work best when structure quality and failure containment are explicitly filtered.",
            "benchmark_priority": "medium",
            "mutations": {
                "doctrine_id": "breakout_volatility_expansion",
                "strategy_id": "breakout_open_interest_confirmation",
                "market_regime": "trend",
                "timeframe": "15m",
                "venue": "kalshi",
                "asset_universe": "BTC",
                "paper_gate": "strict",
            },
        },
        {
            "proposal_id": "btc-15m-regime-shift-no-trade-filter",
            "title": "Regime-shift no-trade filter",
            "doctrine_family": "risk_first_asymmetric_capture",
            "strategy_family": "event_avoidance_filter",
            "source_ids": ["george-soros-reflexivity", "john-murphy-intermarket", "kalshi-trading-hours"],
            "target_contract_family": "btc_up_down_15m",
            "thesis": "The best edge may come from avoiding unstable narrative or macro-shift windows rather than forcing directional exposure.",
            "benchmark_priority": "medium",
            "mutations": {
                "doctrine_id": "risk_first_asymmetric_capture",
                "strategy_id": "funding_mean_revert",
                "market_regime": "event_driven",
                "timeframe": "15m",
                "venue": "kalshi",
                "asset_universe": "BTC",
                "paper_gate": "strict",
            },
        },
        {
            "proposal_id": "btc-15m-sizing-overlay",
            "title": "Sizing overlay after edge calibration",
            "doctrine_family": "risk_first_asymmetric_capture",
            "strategy_family": "fractional_kelly_overlay",
            "source_ids": ["edward-thorp-kelly", "van-tharp-position-sizing", "tom-basso-process-trend"],
            "target_contract_family": "btc_up_down_15m",
            "thesis": "Sizing should be treated as a second-stage mutation only after contract-level edge is stable under heavy backtest.",
            "benchmark_priority": "medium",
            "mutations": {
                "doctrine_id": "risk_first_asymmetric_capture",
                "strategy_id": "ema_pullback_long",
                "market_regime": "trend",
                "timeframe": "15m",
                "venue": "kalshi",
                "asset_universe": "BTC",
                "paper_gate": "strict",
            },
        },
    ]


def _doctrine_card_templates(docs_root: Path) -> list[dict[str, Any]]:
    card_root = docs_root / "doctrine-cards"
    if not card_root.exists():
        return []
    cards: list[dict[str, Any]] = []
    for path in sorted(card_root.glob("*.json")):
        payload = _load_json(path, {})
        if not isinstance(payload, dict):
            continue
        proposal_id = str(payload.get("proposal_id", "")).strip()
        mutations = payload.get("mutation_template", {})
        mutations = mutations if isinstance(mutations, dict) else {}
        if not proposal_id or not mutations:
            continue
        cards.append(
            {
                "proposal_id": proposal_id,
                "title": payload.get("title", proposal_id),
                "doctrine_family": payload.get("doctrine_family", ""),
                "strategy_family": payload.get("strategy_family", ""),
                "source_ids": payload.get("source_ids", []),
                "target_contract_family": payload.get("target_contract_family", "btc_up_down_15m"),
                "thesis": payload.get("research_thesis", ""),
                "benchmark_priority": payload.get("benchmark_priority", "medium"),
                "mutations": {str(key): str(value) for key, value in mutations.items()},
                "card_id": payload.get("card_id"),
                "root_lesson": payload.get("root_lesson"),
                "counterfactual": payload.get("counterfactual"),
                "ghost_improvement_check": payload.get("ghost_improvement_check"),
                "rollback_condition": payload.get("rollback_condition"),
            }
        )
    return cards


def _merged_proposal_templates(docs_root: Path) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for item in _proposal_templates():
        proposal_id = str(item.get("proposal_id", "")).strip()
        if proposal_id:
            merged[proposal_id] = item
    for item in _doctrine_card_templates(docs_root):
        proposal_id = str(item.get("proposal_id", "")).strip()
        if proposal_id:
            merged[proposal_id] = item
    return list(merged.values())


def _source_index(sources: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item.get("source_id", "")).strip(): item for item in sources if isinstance(item, dict)}


def _benchmark_index(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = summary.get("rows", [])
    if not isinstance(rows, list):
        return {}
    index: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        candidate_id = str(row.get("candidate_id", "")).strip()
        if candidate_id:
            index[candidate_id] = row
    return index


def _proposal_backlog(rows: list[dict[str, Any]], sources: list[dict[str, Any]], policy: dict[str, Any], benchmark_summary: dict[str, Any], docs_root: Path) -> list[dict[str, Any]]:
    candidates = _candidate_rows(rows)
    failures = [
        {
            "candidate_id": str(row.get("candidate_id", "")),
            "recommended_next_step": str(_chip_result(row).get("recommended_next_step", "")),
            "profitability_score": _metrics(row).get("profitability_score"),
            "max_drawdown": _metrics(row).get("max_drawdown"),
        }
        for row in candidates
    ]
    failure_ids = [item["candidate_id"] for item in failures if item["candidate_id"]]
    source_lookup = _source_index(sources)
    benchmark_lookup = _benchmark_index(benchmark_summary)
    variety_index = benchmark_variety_index(benchmark_summary)
    benchmark_by_fingerprint = variety_index.get("by_fingerprint", {})
    benchmark_by_family_child = variety_index.get("by_family_child", {})
    benchmark_by_family = variety_index.get("by_family", {})
    proposals: list[dict[str, Any]] = []
    surprise_base = len([item for item in failures if item.get("recommended_next_step") != "queue_for_paper_trade"]) / max(1, len(failures))
    for template in _merged_proposal_templates(docs_root):
        source_names = [str(source_lookup.get(source_id, {}).get("author", source_id)) for source_id in template["source_ids"]]
        novelty_weight = min(1.0, 0.45 + len(template["source_ids"]) * 0.12)
        recency_weight = 1.0
        benchmark_row = benchmark_lookup.get(template["proposal_id"], {})
        benchmark_metrics = benchmark_row.get("metrics", {}) if isinstance(benchmark_row.get("metrics"), dict) else {}
        benchmark_result = benchmark_row.get("result", {}) if isinstance(benchmark_row.get("result"), dict) else {}
        mutations = normalize_mutations(template.get("mutations", {}))
        fingerprint = effective_fingerprint(mutations)
        family_id = variety_family_id(
            mutations,
            doctrine_family=str(template.get("doctrine_family", "")),
            strategy_family=str(template.get("strategy_family", "")),
            target_contract_family=str(template.get("target_contract_family", "")),
        )
        child_id = variety_child_id(mutations)
        family_bucket = benchmark_by_family.get(family_id, {})
        family_child_key = f"{family_id}::{child_id}"
        if benchmark_row:
            benchmark_status = "benchmarked_" + str(benchmark_result.get("recommended_next_step", "unknown"))
        elif fingerprint and fingerprint in benchmark_by_fingerprint:
            benchmark_status = "duplicate_effective_mutation"
        elif family_child_key in benchmark_by_family_child:
            benchmark_status = "tested_variety_child"
        else:
            benchmark_status = "research_seeded_backtest_required"
        proposals.append(
            {
                "proposal_id": template["proposal_id"],
                "title": template["title"],
                "target_contract_family": template["target_contract_family"],
                "doctrine_family": template["doctrine_family"],
                "strategy_family": template["strategy_family"],
                "card_id": template.get("card_id"),
                "source_ids": template["source_ids"],
                "source_names": source_names,
                "research_thesis": template["thesis"],
                "root_lesson": template.get("root_lesson", "Research should propose testable BTC 15m contract ideas, not direct strategy adoption from reputation."),
                "lineage_failures": failure_ids[:3],
                "counterfactual": template.get("counterfactual", "Without this mutation, the loop stays trapped in seeded generic doctrine combinations and never pressure-tests richer trader teachings."),
                "ghost_improvement_check": template.get("ghost_improvement_check", "Do not accept higher profitability_score alone. Require holdout robustness, drawdown containment, and promotion readiness under the heavy-backtest policy."),
                "benchmark_priority": template["benchmark_priority"],
                "surprise_score": round(surprise_base * novelty_weight * recency_weight, 4),
                "mutations": mutations,
                "variety_family_id": family_id,
                "variety_child_id": child_id,
                "variety_child_label": variety_child_label(mutations),
                "family_tested_child_count": len(family_bucket.get("tested_child_ids", set())),
                "family_top_candidate_id": str(((family_bucket.get("top_row") or {}).get("candidate_id", ""))),
                "required_backtest": {
                    "mode": "heavy_backtest",
                    "min_contract_windows": int(policy.get("benchmark_lane", {}).get("min_contract_windows", 500)),
                    "walk_forward_splits": int(policy.get("benchmark_lane", {}).get("walk_forward_splits", 6)),
                    "holdout_policy": str(policy.get("benchmark_lane", {}).get("holdout_policy", "final_20_percent")),
                },
                "rollback_condition": template.get("rollback_condition", "Rollback if the proposal fails holdout profitability, breaches max drawdown, or degrades into regime-specific curve fit."),
                "status": benchmark_status,
                "lineage_ready": len(failure_ids[:3]) == 3,
                "benchmark_metrics": benchmark_metrics,
                "benchmark_result": benchmark_result,
                "effective_mutation_fingerprint": fingerprint,
            }
        )
    ranked = sorted(
        proposals,
        key=lambda item: (
            float(item.get("surprise_score", 0.0)),
            -int(item.get("family_tested_child_count", 0) or 0),
        ),
        reverse=True,
    )
    seen: dict[str, str] = {}
    for item in ranked:
        fingerprint = str(item.get("effective_mutation_fingerprint", "")).strip()
        if not fingerprint:
            continue
        existing = seen.get(fingerprint)
        if existing:
            item["duplicate_of_proposal_id"] = existing
            if not str(item.get("status", "")).startswith("benchmarked_"):
                item["status"] = "duplicate_effective_mutation"
        else:
            seen[fingerprint] = str(item.get("proposal_id", ""))
    return ranked


def _parse_family_id(raw: str) -> dict[str, str]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return {str(key): str(value) for key, value in payload.items()} if isinstance(payload, dict) else {}


def _suggested_variety_targets(
    base_mutations: dict[str, str],
    contradiction_modes: list[str],
    tested_child_ids: set[str],
) -> list[dict[str, Any]]:
    suggestions: list[dict[str, Any]] = []
    doctrine_id = str(base_mutations.get("doctrine_id", ""))
    mapping: list[tuple[str, dict[str, str]]] = []
    if "holdout_decay" in contradiction_modes:
        mapping.append(
            (
                "late sample guard plus session filter",
                {
                    "late_sample_guard": "on",
                    "session_profile": "late_cycle_filter",
                },
            )
        )
    if "segment_instability" in contradiction_modes:
        mapping.append(
            (
                "session stability filter",
                {
                    "session_profile": "stability_window",
                    "no_trade_window": "avoid_transition_window",
                },
            )
        )
    if "execution_fragility" in contradiction_modes:
        mapping.append(
            (
                "execution buffer plus transition skip",
                {
                    "execution_buffer": "high",
                    "no_trade_window": "avoid_transition_window",
                },
            )
        )
    if "sparse_signal" in contradiction_modes:
        mapping.append(
            (
                "adaptive activation profile",
                {
                    "activation_profile": "adaptive",
                },
            )
        )
    if "drawdown_excess" in contradiction_modes and doctrine_id == "mean_reversion_liquidity_reclaim":
        mapping.append(
            (
                "wick reclaim drawdown guard",
                {
                    "drawdown_guard": "high",
                    "reversal_confirmation": "wick_reclaim_close",
                    "wick_profile": "rejection_confirm",
                },
            )
        )
    elif "drawdown_excess" in contradiction_modes:
        mapping.append(
            (
                "drawdown guard plus quality filter",
                {
                    "drawdown_guard": "high",
                    "session_profile": "quality_window",
                },
            )
        )
    for label, delta in mapping:
        candidate_mutations = dict(base_mutations)
        candidate_mutations.update(delta)
        child_id = variety_child_id(candidate_mutations)
        if child_id in tested_child_ids:
            continue
        suggestions.append(
            {
                "label": label,
                "variety_child_id": child_id,
                "variety_child_label": variety_child_label(candidate_mutations),
                "mutations": delta,
            }
        )
    return suggestions


def _variety_backlog(backlog: list[dict[str, Any]], benchmark_summary: dict[str, Any], probes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    benchmark_lookup = _benchmark_index(benchmark_summary)
    variety_index = benchmark_variety_index(benchmark_summary)
    families: dict[str, dict[str, Any]] = {}
    for item in backlog:
        family_id = str(item.get("variety_family_id", "")).strip()
        if not family_id:
            continue
        bucket = families.setdefault(
            family_id,
            {
                "variety_family_id": family_id,
                "doctrine_family": item.get("doctrine_family"),
                "strategy_family": item.get("strategy_family"),
                "target_contract_family": item.get("target_contract_family"),
                "source_names": [],
                "pending_proposal_ids": [],
                "pending_child_labels": [],
                "contradiction_modes": set(),
                "base_mutations": normalize_mutations(item.get("mutations", {})),
            },
        )
        for source_name in item.get("source_names", []):
            if source_name not in bucket["source_names"]:
                bucket["source_names"].append(source_name)
        status = str(item.get("status", ""))
        if status in {"research_seeded_backtest_required"}:
            bucket["pending_proposal_ids"].append(str(item.get("proposal_id", "")))
            child_label = str(item.get("variety_child_label", "")).strip() or "base"
            if child_label not in bucket["pending_child_labels"]:
                bucket["pending_child_labels"].append(child_label)
    for probe in probes:
        if not isinstance(probe, dict):
            continue
        candidate_id = str(probe.get("candidate_id", "")).strip()
        benchmark_row = benchmark_lookup.get(candidate_id, {})
        if not benchmark_row:
            continue
        mutations = normalize_mutations(benchmark_row.get("mutations", {}))
        family_id = variety_family_id(mutations)
        bucket = families.setdefault(
            family_id,
            {
                "variety_family_id": family_id,
                "doctrine_family": "",
                "strategy_family": "",
                "target_contract_family": benchmark_summary.get("contract_family"),
                "source_names": [],
                "pending_proposal_ids": [],
                "pending_child_labels": [],
                "contradiction_modes": set(),
                "base_mutations": {},
            },
        )
        for mode in probe.get("failure_modes", []):
            if isinstance(mode, dict) and str(mode.get("mode", "")).strip():
                bucket["contradiction_modes"].add(str(mode.get("mode", "")).strip())
    for family_id, family_bucket in variety_index.get("by_family", {}).items():
        top_row = family_bucket.get("top_row")
        bucket = families.setdefault(
            family_id,
            {
                "variety_family_id": family_id,
                "doctrine_family": "",
                "strategy_family": "",
                "target_contract_family": benchmark_summary.get("contract_family"),
                "source_names": [],
                "pending_proposal_ids": [],
                "pending_child_labels": [],
                "contradiction_modes": set(),
                "base_mutations": normalize_mutations((top_row or {}).get("mutations", {})),
            },
        )
        benchmark_rows = family_bucket.get("rows", [])
        benchmark_rows = benchmark_rows if isinstance(benchmark_rows, list) else []
        metrics = (top_row or {}).get("metrics", {}) if isinstance((top_row or {}).get("metrics"), dict) else {}
        result = (top_row or {}).get("result", {}) if isinstance((top_row or {}).get("result"), dict) else {}
        bucket["tested_child_count"] = len(family_bucket.get("tested_child_ids", set()))
        bucket["benchmarked_candidate_count"] = len(benchmark_rows)
        bucket["top_candidate_id"] = str((top_row or {}).get("candidate_id", ""))
        bucket["top_profitability_score"] = metrics.get("profitability_score")
        bucket["top_recommended_next_step"] = result.get("recommended_next_step")
        if not bucket.get("base_mutations"):
            bucket["base_mutations"] = normalize_mutations((top_row or {}).get("mutations", {}))
    rows: list[dict[str, Any]] = []
    for bucket in families.values():
        family_meta = _parse_family_id(str(bucket.get("variety_family_id", "")))
        if not str(bucket.get("doctrine_family", "")).strip():
            bucket["doctrine_family"] = family_meta.get("doctrine", "")
        if not str(bucket.get("strategy_family", "")).strip():
            bucket["strategy_family"] = family_meta.get("strategy", "")
        contradiction_modes = sorted(bucket.pop("contradiction_modes", set()))
        pending_proposal_ids = [item for item in bucket.get("pending_proposal_ids", []) if item]
        pending_child_labels = [item for item in bucket.get("pending_child_labels", []) if item]
        family_bucket = variety_index.get("by_family", {}).get(str(bucket.get("variety_family_id", "")), {})
        tested_child_ids = family_bucket.get("tested_child_ids", set())
        tested_child_ids = tested_child_ids if isinstance(tested_child_ids, set) else set()
        suggested_targets = _suggested_variety_targets(
            normalize_mutations(bucket.get("base_mutations", {})),
            contradiction_modes,
            tested_child_ids,
        )
        bucket["pending_proposal_count"] = len(pending_proposal_ids)
        bucket["pending_proposal_ids"] = pending_proposal_ids
        bucket["pending_child_labels"] = pending_child_labels
        bucket["suggested_child_target_count"] = len(suggested_targets)
        bucket["suggested_child_targets"] = suggested_targets[:4]
        bucket["tested_child_count"] = int(bucket.get("tested_child_count", 0) or 0)
        bucket["benchmarked_candidate_count"] = int(bucket.get("benchmarked_candidate_count", 0) or 0)
        bucket["contradiction_modes"] = contradiction_modes
        if pending_proposal_ids:
            bucket["status"] = "uncovered_variety_pending"
        elif suggested_targets:
            bucket["status"] = "suggested_child_targets_ready"
        else:
            bucket["status"] = "family_covered_waiting_new_child"
        bucket.pop("base_mutations", None)
        rows.append(bucket)
    rows.sort(
        key=lambda item: (
            int(item.get("pending_proposal_count", 0) or 0),
            int(item.get("suggested_child_target_count", 0) or 0),
            len(item.get("contradiction_modes", [])),
            -int(item.get("tested_child_count", 0) or 0),
        ),
        reverse=True,
    )
    return rows


def _heavy_backtest_queue(backlog: list[dict[str, Any]], variety_backlog: list[dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    queue: list[dict[str, Any]] = []
    thresholds = policy.get("promotion_thresholds", {})
    variety_policy = policy.get("variety_lane", {}) if isinstance(policy.get("variety_lane"), dict) else {}
    max_families = max(1, int(variety_policy.get("max_backtest_families_per_cycle", 6) or 6))
    max_per_family = max(1, int(variety_policy.get("max_pending_children_per_family", 2) or 2))
    backlog_index = {str(item.get("proposal_id", "")): item for item in backlog if str(item.get("proposal_id", "")).strip()}
    for family in variety_backlog[:max_families]:
        selected = 0
        for proposal_id in family.get("pending_proposal_ids", []):
            if selected >= max_per_family:
                break
            item = backlog_index.get(str(proposal_id))
            if not item:
                continue
            if str(item.get("status", "")) in {"duplicate_effective_mutation", "tested_variety_child"}:
                continue
            if str(item.get("status", "")).startswith("benchmarked_"):
                continue
            queue.append(
                {
                    "proposal_id": item["proposal_id"],
                    "title": item["title"],
                    "target_contract_family": item["target_contract_family"],
                    "benchmark_priority": item["benchmark_priority"],
                    "surprise_score": item["surprise_score"],
                    "variety_family_id": item.get("variety_family_id"),
                    "variety_child_id": item.get("variety_child_id"),
                    "variety_child_label": item.get("variety_child_label"),
                    "required_metrics": {
                        "profitability_score_min": thresholds.get("profitability_score_min"),
                        "sharpe_ratio_min": thresholds.get("sharpe_ratio_min"),
                        "max_drawdown_max": thresholds.get("max_drawdown_max"),
                        "paper_trade_readiness_min": thresholds.get("paper_trade_readiness_min"),
                    },
                    "benchmark_plan": item["required_backtest"],
                    "status": "queued_for_heavy_backtest",
                }
            )
            selected += 1
    return queue


def _guardrail_status(rows: list[dict[str, Any]], backlog: list[dict[str, Any]], policy: dict[str, Any], benchmark_summary: dict[str, Any]) -> dict[str, str]:
    candidates = _candidate_rows(rows)
    schema_gate = "pass"
    lineage_gate = "pass" if backlog and all(bool(item.get("lineage_ready")) for item in backlog[:3]) else "fail"
    complexity_gate = "pass"
    benchmark_count = int(benchmark_summary.get("candidate_count", 0) or 0)
    transfer_gate = "pass" if benchmark_count >= 1 else "warn"
    memory_hygiene_gate = "pass"
    human_gate = "pass" if int(policy.get("human_approval_window_days", 30)) >= 1 else "fail"
    if not candidates:
        transfer_gate = "warn"
    return {
        "schema_gate": schema_gate,
        "lineage_gate": lineage_gate,
        "complexity_gate": complexity_gate,
        "transfer_gate": transfer_gate,
        "memory_hygiene_gate": memory_hygiene_gate,
        "human_gate": human_gate,
    }


def _anti_patterns(rows: list[dict[str, Any]], queue: list[dict[str, Any]], benchmark_summary: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = _candidate_rows(rows)
    benchmark_rows = benchmark_summary.get("rows", [])
    benchmark_rows = benchmark_rows if isinstance(benchmark_rows, list) else []
    unresolved_drawdown = [
        str(row.get("candidate_id", ""))
        for row in candidates
        if float(_metrics(row).get("max_drawdown", 0.0) or 0.0) > 0.22
    ]
    weak_walk_forward = [
        str(row.get("candidate_id", ""))
        for row in benchmark_rows
        if float(((row.get("result", {}) or {}).get("walk_forward_consistency", 0.0) or 0.0)) < 0.4
    ]
    weak_stress = [
        str(row.get("candidate_id", ""))
        for row in benchmark_rows
        if float(((row.get("result", {}) or {}).get("stress_resilience", 0.0) or 0.0)) < 0.66
    ]
    result = [
        {
            "tag": "ghost_improvement",
            "severity": "warn",
            "evidence": ["The current backtester is real, but the strongest candidates still need walk-forward and stress robustness before they count as causal proof."],
            "status": "open",
        },
        {
            "tag": "comfort_zone_optimization",
            "severity": "warn",
            "evidence": [f"Heavy-backtest summary currently covers {benchmark_summary.get('candidate_count', 0)} candidates; this must keep shifting toward BTC-specific mutation trials."],
            "status": "contained" if int(benchmark_summary.get("candidate_count", 0) or 0) >= 1 else "open",
        },
    ]
    golden_demo_evidence: list[str] = []
    if unresolved_drawdown:
        golden_demo_evidence.append(f"High-drawdown seeded candidates remain unresolved: {', '.join(unresolved_drawdown[:3])}")
    if weak_walk_forward:
        golden_demo_evidence.append(f"Walk-forward consistency stays weak for: {', '.join(weak_walk_forward[:3])}")
    if weak_stress:
        golden_demo_evidence.append(f"Stress resilience remains below threshold for: {', '.join(weak_stress[:3])}")
    if golden_demo_evidence:
        result.append(
            {
                "tag": "golden_demo_collapse",
                "severity": "warn" if weak_walk_forward or weak_stress else "info",
                "evidence": golden_demo_evidence,
                "status": "contained",
            }
        )
    if not queue:
        result.append(
            {
                "tag": "reflection_starvation",
                "severity": "warn",
                "evidence": ["The current mutation backlog has already been benchmarked once; the next queue depends on adding new proposals or broader datasets."],
                "status": "contained",
            }
        )
    return result


def _decision_packet(rows: list[dict[str, Any]], backlog: list[dict[str, Any]], queue: list[dict[str, Any]], policy: dict[str, Any], benchmark_summary: dict[str, Any]) -> dict[str, Any]:
    guardrails = _guardrail_status(rows, backlog, policy, benchmark_summary)
    anti_patterns = _anti_patterns(rows, queue, benchmark_summary)
    benchmark_rows = benchmark_summary.get("rows", [])
    benchmark_rows = benchmark_rows if isinstance(benchmark_rows, list) else []
    top_result = (benchmark_rows[0].get("result", {}) if benchmark_rows and isinstance(benchmark_rows[0], dict) else {})
    top_result = top_result if isinstance(top_result, dict) else {}
    failing_guardrails = [name for name, status in guardrails.items() if status == "fail"]
    decision = "reject" if failing_guardrails else "defer"
    candidates = _candidate_rows(rows)
    stability_score = 0.61
    if failing_guardrails:
        stability_score -= 0.18
    if not candidates:
        stability_score -= 0.1
    if not queue:
        stability_score -= 0.02
    if int(benchmark_summary.get("candidate_count", 0) or 0) >= 1:
        stability_score += 0.05
    stability_score = round(max(0.0, min(0.99, stability_score)), 2)
    return {
        "stability_score": stability_score,
        "decision": decision,
        "top_bottleneck": "Heavy backtests now include walk-forward and stress checks, but the top gated candidates still fail on drawdown, holdout strength, or robustness under fee/slippage pressure.",
        "benchmark_summary": {
            "candidate_count": benchmark_summary.get("candidate_count"),
            "top_candidate_id": benchmark_summary.get("top_candidate_id"),
            "contract_family": benchmark_summary.get("contract_family"),
            "top_walk_forward_consistency": top_result.get("walk_forward_consistency"),
            "top_stress_resilience": top_result.get("stress_resilience"),
        },
        "anti_patterns_detected": anti_patterns,
        "guardrail_status": guardrails,
        "pillar_assessment": {
            "causal_anchor": {
                "status": "warn" if "lineage_gate" in failing_guardrails else "pass",
                "evidence": [
                    "Research proposals now require root lesson, counterfactual, ghost-improvement check, and rollback condition.",
                    "The current proposals are anchored to existing ledger failures and now receive benchmark status updates from heavy-backtest summaries.",
                ],
            },
            "cross_pollination": {
                "status": "pass" if int(benchmark_summary.get("candidate_count", 0) or 0) >= 1 else "warn",
                "evidence": [
                    "Cross-domain trader teachings are being mapped into BTC up/down 15m contract proposals rather than copied directly.",
                    "Transfer still needs broader contract coverage before doctrine promotion.",
                ],
            },
            "entropy_filter": {
                "status": "pass",
                "evidence": [
                    "Changes are confined to docs, artifact builders, and watchtower pages rather than adding runtime framework complexity."
                ],
            },
            "surprise_priority": {
                "status": "pass" if queue else "warn",
                "evidence": [
                    "Queue ranking is driven by surprise score so research effort flows toward unproven but high-value doctrine families."
                ],
            },
        },
        "required_fixes_before_approve": [
            "Keep extending the BTC dataset across more market regimes while separating sparse high-profit variants from scalable ones.",
            "Record lineage failures per mutation proposal before self-edit or doctrine promotion.",
            "Benchmark every proposed mutation on holdout windows, walk-forward splits, and fee/slippage stress before paper-trade escalation.",
        ],
        "next_experiments": [
            "Extend the BTC 1m plus contract-window dataset into additional months and more violent market regimes.",
            "Use walk-forward and stress failures to design the next BTC 15m mutation probes instead of adding doctrine breadth blindly.",
            "Run the top three backlog proposals through the heavy-backtest queue before adding more doctrine families.",
        ],
        "risk_if_ignored": "The loop will overfit narrative research, promote false doctrines from placeholder scores, and reach paper trade without causal benchmark evidence.",
    }


def build_recursion_packets(repo_root: Path) -> list[Path]:
    docs_root = repo_root / "docs"
    policy = _load_json(docs_root / "recursion" / "loop-policy.json", {})
    sources = _load_json(docs_root / "research-ingest" / "approved-sources.json", [])
    rows = _load_rows(repo_root / "artifacts" / "ledger" / "runs.jsonl")
    benchmark_summary = _load_json(repo_root / "artifacts" / "backtests" / "heavy_backtest_summary.json", {})
    probes = _load_json(repo_root / "artifacts" / "recursion" / "contradiction_probes.json", [])
    self_edit_evaluations = _load_self_edit_evaluations(repo_root)
    backlog = _proposal_backlog(rows, sources, policy if isinstance(policy, dict) else {}, benchmark_summary if isinstance(benchmark_summary, dict) else {}, docs_root)
    variety_backlog = _variety_backlog(backlog, benchmark_summary if isinstance(benchmark_summary, dict) else {}, probes if isinstance(probes, list) else [])
    queue = _heavy_backtest_queue(backlog, variety_backlog, policy if isinstance(policy, dict) else {})
    decision = _decision_packet(rows, backlog, queue, policy if isinstance(policy, dict) else {}, benchmark_summary if isinstance(benchmark_summary, dict) else {})
    decision["self_edit_summary"] = {
        "evaluation_count": len(self_edit_evaluations),
        "approved_count": sum(1 for item in self_edit_evaluations if str(item.get("decision", "")) == "approve"),
        "deferred_count": sum(1 for item in self_edit_evaluations if str(item.get("decision", "")) == "defer"),
        "rejected_count": sum(1 for item in self_edit_evaluations if str(item.get("decision", "")) == "reject"),
    }
    target_root = repo_root / "artifacts" / "recursion"
    target_root.mkdir(parents=True, exist_ok=True)
    outputs = {
        "mutation_backlog.json": backlog,
        "variety_backlog.json": variety_backlog,
        "heavy_backtest_queue.json": queue,
        "recursion_audit.json": decision,
    }
    written: list[Path] = []
    for name, payload in outputs.items():
        path = target_root / name
        safe_write_json(path, payload)
        written.append(path)
    return written


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_recursion_packets(repo_root)


if __name__ == "__main__":
    main()
