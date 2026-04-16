from __future__ import annotations

import hashlib
import json
from pathlib import Path

from safe_write import safe_write_json
from variety_model import (
    benchmark_variety_index,
    effective_fingerprint,
    normalize_mutations,
    variety_child_id,
    variety_child_label,
    variety_family_id,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


TRIAL_MAP = {
    "btc-15m-trend-continuation": {
        "doctrine_id": "trend_regime_following",
        "strategy_id": "ema_pullback_long",
        "market_regime": "trend",
        "timeframe": "15m",
        "venue": "kalshi",
        "asset_universe": "BTC",
        "paper_gate": "strict",
    },
    "btc-15m-volatility-compression-breakout": {
        "doctrine_id": "breakout_volatility_expansion",
        "strategy_id": "breakout_open_interest_confirmation",
        "market_regime": "high_vol",
        "timeframe": "15m",
        "venue": "kalshi",
        "asset_universe": "BTC",
        "paper_gate": "strict",
    },
    "btc-15m-exhaustion-mean-reversion": {
        "doctrine_id": "mean_reversion_liquidity_reclaim",
        "strategy_id": "range_reclaim_scalp",
        "market_regime": "range",
        "timeframe": "15m",
        "venue": "kalshi",
        "asset_universe": "BTC",
        "paper_gate": "balanced",
    },
    "btc-15m-momentum-breakout-structure": {
        "doctrine_id": "breakout_volatility_expansion",
        "strategy_id": "breakout_open_interest_confirmation",
        "market_regime": "trend",
        "timeframe": "15m",
        "venue": "kalshi",
        "asset_universe": "BTC",
        "paper_gate": "strict",
    },
    "btc-15m-regime-shift-no-trade-filter": {
        "doctrine_id": "risk_first_asymmetric_capture",
        "strategy_id": "funding_mean_revert",
        "market_regime": "event_driven",
        "timeframe": "15m",
        "venue": "kalshi",
        "asset_universe": "BTC",
        "paper_gate": "strict",
    },
    "btc-15m-sizing-overlay": {
        "doctrine_id": "risk_first_asymmetric_capture",
        "strategy_id": "ema_pullback_long",
        "market_regime": "trend",
        "timeframe": "15m",
        "venue": "kalshi",
        "asset_universe": "BTC",
        "paper_gate": "strict",
    },
    "range-reclaim-majors-1h": {
        "doctrine_id": "mean_reversion_liquidity_reclaim",
        "strategy_id": "range_reclaim_scalp",
        "market_regime": "range",
        "timeframe": "1h",
        "venue": "bybit",
        "asset_universe": "BTC,ETH,SOL",
        "paper_gate": "balanced",
    },
}


def _load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return payload if isinstance(payload, list) else []


def _load_object(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_probe_json(path: Path) -> list[dict]:
    return _load_json(path)


def _load_summary_index(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    rows = payload.get("rows", []) if isinstance(payload, dict) else []
    rows = rows if isinstance(rows, list) else []
    index: dict[str, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        candidate_id = str(row.get("candidate_id", "")).strip()
        mutations = row.get("mutations", {})
        if candidate_id and isinstance(mutations, dict):
            index[candidate_id] = {str(k): str(v) for k, v in mutations.items()}
    return index


def _load_pattern_map(path: Path) -> dict:
    return _load_object(path)


def _cap_id(candidate_id: str, max_len: int = 120) -> str:
    """Truncate pathologically long candidate IDs with a hash suffix."""
    if len(candidate_id) <= max_len:
        return candidate_id
    prefix = candidate_id[:max_len - 11]
    suffix = hashlib.sha256(candidate_id.encode()).hexdigest()[:10]
    return f"{prefix}-{suffix}"


def _slugify(raw: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in raw)
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "variety"


def _probe_modes(item: dict) -> list[str]:
    modes = item.get("failure_modes", [])
    if not isinstance(modes, list):
        return []
    return [str(mode.get("mode", "")).strip() for mode in modes if isinstance(mode, dict)]


def _derived_mutations(base: dict[str, str], modes: list[str]) -> dict[str, str]:
    mutations = dict(base)
    doctrine_id = mutations.get("doctrine_id", "")
    if "sparse_signal" in modes:
        mutations["activation_profile"] = "wider" if doctrine_id != "mean_reversion_liquidity_reclaim" else "stricter"
    if "holdout_decay" in modes:
        mutations["late_sample_guard"] = "on"
        if doctrine_id == "mean_reversion_liquidity_reclaim":
            mutations["activation_profile"] = "stricter"
    if "execution_fragility" in modes:
        mutations["execution_buffer"] = "high"
        if doctrine_id == "mean_reversion_liquidity_reclaim":
            mutations["no_trade_window"] = "avoid_post_open_drift"
        elif doctrine_id == "risk_first_asymmetric_capture":
            mutations["no_trade_window"] = "avoid_reflexive_burst"
        else:
            mutations["no_trade_window"] = "avoid_dead_zone"
    if "paper_trade_demotion" in modes:
        mutations["execution_buffer"] = "high"
        mutations["late_sample_guard"] = "on"
        if doctrine_id == "mean_reversion_liquidity_reclaim":
            mutations["session_profile"] = "opening_range_failure"
            mutations["reversal_confirmation"] = "edge_reclaim_close"
    if "shadow_participation_sparse" in modes:
        if doctrine_id == "mean_reversion_liquidity_reclaim":
            mutations["range_edge_profile"] = "local_extreme_only"
            mutations["wick_profile"] = "rejection_confirm"
        else:
            mutations["activation_profile"] = "wider"
    if "shadow_drawdown_excess" in modes:
        mutations["drawdown_guard"] = "high"
        if doctrine_id == "mean_reversion_liquidity_reclaim":
            mutations["range_edge_profile"] = "local_extreme_only"
            mutations["wick_profile"] = "rejection_confirm"
    return mutations


def _derived_trials(probes: list[dict], summary_index: dict[str, dict]) -> list[dict]:
    trials: list[dict] = []
    for item in probes:
        if not isinstance(item, dict):
            continue
        candidate_id = str(item.get("candidate_id", "")).strip()
        base = TRIAL_MAP.get(candidate_id) or summary_index.get(candidate_id)
        if not base:
            continue
        modes = _probe_modes(item)
        mutations = _derived_mutations(base, modes)
        primary_mode = modes[0] if modes else "probe"
        if mutations != base:
            trials.append(
                {
                    "candidate_id": _cap_id(f"{candidate_id}-probe-{primary_mode}"),
                    "candidate_summary": f"{candidate_id} contradiction probe",
                    "hypothesis": str(item.get("probe_thesis", "")),
                    "mutations": normalize_mutations(mutations),
                    "source_names": ["benchmark_contradiction_probe"],
                    "proposal_origin": "contradiction_probe",
                }
            )
        if base.get("doctrine_id") == "mean_reversion_liquidity_reclaim" and "paper_trade_demotion" in modes:
            pilot_guard_mutations = dict(mutations)
            pilot_guard_mutations["drawdown_guard"] = "high"
            pilot_guard_mutations["range_edge_profile"] = "local_extreme_only"
            pilot_guard_mutations["wick_profile"] = "rejection_confirm"
            trials.append(
                {
                    "candidate_id": _cap_id(f"{candidate_id}-probe-paper_trade_demotion"),
                    "candidate_summary": f"{candidate_id} paper-trade demotion recovery probe",
                    "hypothesis": "Use the shadow demotion to produce a stricter mean-reversion child that prioritizes edge-only participation and drawdown containment under live-like timing.",
                    "mutations": normalize_mutations(pilot_guard_mutations),
                    "source_names": ["paper_trade_contradiction_probe"],
                    "proposal_origin": "contradiction_probe",
                }
            )
        if (
            base.get("doctrine_id") == "mean_reversion_liquidity_reclaim"
            and "drawdown_excess" in modes
            and float(item.get("trade_count", 0.0) or 0.0) >= float(item.get("minimum_trade_count", 0.0) or 0.0)
        ):
            drawdown_mutations = dict(mutations)
            drawdown_mutations["drawdown_guard"] = "high"
            drawdown_mutations["range_edge_profile"] = "local_extreme_only"
            drawdown_mutations["wick_profile"] = "rejection_confirm"
            trials.append(
                {
                    "candidate_id": _cap_id(f"{candidate_id}-probe-drawdown_excess"),
                    "candidate_summary": f"{candidate_id} drawdown recovery probe",
                    "hypothesis": "Use stricter mean-reversion drawdown guards to preserve holdout gains while reducing downside excursions.",
                    "mutations": normalize_mutations(drawdown_mutations),
                    "source_names": ["benchmark_contradiction_probe"],
                    "proposal_origin": "contradiction_probe",
                }
            )
        if (
            base.get("doctrine_id") == "mean_reversion_liquidity_reclaim"
            and "holdout_decay" in modes
            and float(item.get("trade_count", 0.0) or 0.0) >= float(item.get("minimum_trade_count", 0.0) or 0.0)
        ):
            edge_reclaim_mutations = dict(mutations)
            edge_reclaim_mutations["range_edge_profile"] = "local_extreme_only"
            edge_reclaim_mutations["reversal_confirmation"] = "edge_reclaim_close"
            trials.append(
                {
                    "candidate_id": _cap_id(f"{candidate_id}-probe-edge_reclaim_quality"),
                    "candidate_summary": f"{candidate_id} edge reclaim quality probe",
                    "hypothesis": "Require local-range edge participation plus reclaim quality to reduce sloppy mean-reversion entries without discarding the whole holdout-repair branch.",
                    "mutations": normalize_mutations(edge_reclaim_mutations),
                    "source_names": ["benchmark_contradiction_probe"],
                    "proposal_origin": "contradiction_probe",
                }
            )
    return trials


def _variety_trials(variety_backlog: list[dict], summary_index: dict[str, dict]) -> list[dict]:
    trials: list[dict] = []
    for item in variety_backlog:
        if not isinstance(item, dict):
            continue
        base_candidate_id = str(item.get("top_candidate_id", "")).strip()
        if not base_candidate_id:
            continue
        base = summary_index.get(base_candidate_id)
        if not base:
            continue
        targets = item.get("suggested_child_targets", [])
        targets = targets if isinstance(targets, list) else []
        for index, target in enumerate(targets[:2], start=1):
            if not isinstance(target, dict):
                continue
            delta = target.get("mutations", {})
            delta = normalize_mutations(delta)
            if not delta:
                continue
            mutations = dict(base)
            mutations.update(delta)
            label = str(target.get("label", "")).strip() or f"target-{index}"
            trials.append(
                {
                    "candidate_id": _cap_id(f"{base_candidate_id}-variety-{_slugify(label)}"),
                    "candidate_summary": f"{base_candidate_id} suggested child variety",
                    "hypothesis": f"Test the next uncovered child variety for {base_candidate_id}: {label}.",
                    "mutations": normalize_mutations(mutations),
                    "source_names": ["variety_backlog"],
                    "proposal_origin": "variety_backlog",
                }
            )
    return trials


def _load_guard_rankings() -> dict[str, dict[str, str | float]]:
    """Load proven guard effectiveness from pro insights pack.

    Returns dict of {guard_name: {value: str, delta: float}} sorted by delta.
    Returns empty dict if pack not installed.
    """
    import re

    insights_path = REPO_ROOT / "packs" / "pro-insights-v1" / "synthesized_insights.json"
    if not insights_path.exists():
        return {}
    try:
        insights = json.loads(insights_path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    # Dedupe by guard name, keep highest delta
    best: dict[str, dict] = {}
    for item in insights:
        if item.get("type") != "guard_effectiveness" or not item.get("actionable"):
            continue
        m = re.match(r"Guard '([^']+)'", item.get("insight", ""))
        if not m:
            continue
        name = m.group(1)
        delta = item.get("evidence", {}).get("delta", 0)
        if name not in best or delta > best[name]["delta"]:
            best[name] = {"delta": delta, "evidence": item["evidence"]}

    # Map guard names to their most effective values (from pro agent census)
    PROVEN_GUARD_VALUES = {
        "session_quality_filter": "skip_compression_toxic",
        "cr_loose_setup": "skip_marginal",
        "cr_wick_guard": "reject_high",
        "volume_guard": "moderate",
        "cr_downtrend_high_pos": "skip",
        "cr_down_in_downtrend": "skip_deep",
        "cr_compression_deadzone": "skip_mid",
        "counter_trend_guard": "skip_moderate",
        "drawdown_guard": "moderate",
        "cr_weak_reclaim": "skip_weak",
        "cr_impulse_reversal": "skip_reversal_gentle",
        "volume_context_guard": "skip_spike",
    }

    result = {}
    for name, info in sorted(best.items(), key=lambda x: -x[1]["delta"]):
        value = PROVEN_GUARD_VALUES.get(name)
        if value:
            result[name] = {"value": value, "delta": info["delta"]}
    return result


def _pro_insight_trials(summary_index: dict[str, dict]) -> list[dict]:
    """Generate trials seeded by proven guard effectiveness from pro insights.

    For each existing candidate, tries adding the top proven guards it's missing.
    """
    guard_rankings = _load_guard_rankings()
    if not guard_rankings:
        return []

    # Take top 5 guards by delta
    top_guards = list(guard_rankings.items())[:5]
    trials: list[dict] = []

    for cid, base in summary_index.items():
        for guard_name, info in top_guards:
            guard_value = info["value"]
            delta = info["delta"]
            # Skip if candidate already has this guard with the same value
            if base.get(guard_name) == guard_value:
                continue
            # Skip if candidate already has ANY value for this guard (don't override)
            if base.get(guard_name):
                continue
            mutations = dict(base)
            mutations[guard_name] = guard_value
            trials.append(
                {
                    "candidate_id": _cap_id(f"{cid}-pro-guard-{guard_name}"),
                    "candidate_summary": f"Pro insight: add {guard_name}={guard_value} (proven +{delta:.1%} WR)",
                    "hypothesis": f"Evolution system proved {guard_name}={guard_value} improves WR by {delta:.1%} across {info.get('evidence', {}).get('with_guard_count', '?')} agents. Seed this guard into {cid}.",
                    "mutations": normalize_mutations(mutations),
                    "source_names": ["pro_insights_guard_effectiveness"],
                    "proposal_origin": "pro_insights",
                }
            )

    return trials


def _psychology_trials(backlog: list[dict], pattern_map: dict) -> list[dict]:
    trials: list[dict] = []
    pattern_rows = pattern_map.get("pattern_rows", []) if isinstance(pattern_map.get("pattern_rows"), list) else []
    hint_index = {
        str(item.get("pattern", "")).strip(): item.get("psychology_mutation_hints", [])
        for item in pattern_rows
        if isinstance(item, dict)
    }
    for item in backlog:
        if not isinstance(item, dict) or _status_blocks_trial(item):
            continue
        proposal_id = str(item.get("proposal_id", "")).strip()
        title = str(item.get("title", "")).strip().lower()
        mutations = normalize_mutations(_backlog_mutations(item))
        if not mutations:
            continue
        doctrine_id = mutations.get("doctrine_id", "")
        market_regime = mutations.get("market_regime", "")
        strategy_family = str(item.get("strategy_family", "")).strip().lower()
        source_hints: list[str] = []
        child_suffix = ""
        child_hypothesis = ""
        if doctrine_id in {"trend_regime_following", "breakout_volatility_expansion"} and market_regime in {"trend", "high_vol"}:
            mutations["chase_policy"] = "no_chase_after_crowded_good_news"
            mutations["follow_through_profile"] = "delayed_confirmation"
            child_suffix = "psychology_no_chase"
            source_hints = hint_index.get("trend pullback continuation", []) + hint_index.get("vcp breakout", [])
            child_hypothesis = "Convert the psychology overlay into a no-chase, delayed-confirmation child so crowded good-news continuation is not treated as immediate breakout edge."
        elif doctrine_id == "mean_reversion_liquidity_reclaim" and ("opening-range failure fade" in title or "opening_range_failure_fade" in strategy_family or mutations.get("session_profile") == "opening_range_failure"):
            mutations["catalyst_failure_mode"] = "sell_the_news_failure_fade"
            child_suffix = "psychology_sell_the_news"
            source_hints = hint_index.get("opening-range failure fade", [])
            child_hypothesis = "Convert the psychology overlay into a failed-continuation fade child so mean reversion activates only after crowded catalyst continuation breaks."
        elif doctrine_id == "risk_first_asymmetric_capture" or market_regime == "event_driven":
            mutations["event_interpretation_policy"] = "wait_for_follow_through"
            child_suffix = "psychology_wait_followthrough"
            source_hints = hint_index.get("macro no-trade filter", []) + hint_index.get("risk-throttle sizing overlay", []) + hint_index.get("intermarket context gate", [])
            child_hypothesis = "Convert the psychology overlay into a delayed event-interpretation child so macro/event setups stay abstinent until follow-through proves the regime."
        if not child_suffix:
            continue
        trials.append(
            {
                "candidate_id": _cap_id(f"{proposal_id}-{child_suffix}"),
                "candidate_summary": f"{proposal_id} psychology mutation",
                "hypothesis": child_hypothesis,
                "mutations": mutations,
                "source_names": ["psychology_pattern_regime_map", *[str(item) for item in source_hints[:2]]],
                "proposal_origin": "psychology_pattern_map",
            }
        )
    return trials


def _backlog_mutations(item: dict) -> dict[str, str]:
    raw = item.get("mutations", {})
    if isinstance(raw, dict) and raw:
        return {str(key): str(value) for key, value in raw.items()}
    proposal_id = str(item.get("proposal_id", ""))
    fallback = TRIAL_MAP.get(proposal_id, {})
    return {str(key): str(value) for key, value in fallback.items()}


def _status_blocks_trial(item: dict) -> bool:
    status = str(item.get("status", "")).strip()
    return status.startswith("benchmarked_") or status in {
        "duplicate_effective_mutation",
        "tested_variety_child",
    }


def _enrich_trial(item: dict) -> dict:
    trial = dict(item)
    mutations = normalize_mutations(trial.get("mutations", {}))
    trial["mutations"] = mutations
    family_id = variety_family_id(mutations)
    child_id = variety_child_id(mutations)
    trial["variety_family_id"] = family_id
    trial["variety_child_id"] = child_id
    trial["variety_child_label"] = variety_child_label(mutations)
    trial["effective_mutation_fingerprint"] = effective_fingerprint(mutations)
    return trial


def _dedupe_trials(trials: list[dict]) -> tuple[list[dict], list[dict]]:
    priority = {
        "contradiction_probe": 0,
        "pro_insights": 1,
        "psychology_pattern_map": 2,
        "variety_backlog": 3,
        "mutation_backlog": 4,
    }
    ordered = sorted(
        trials,
        key=lambda item: (
            priority.get(str(item.get("proposal_origin", "")), 9),
            str(item.get("candidate_id", "")),
        ),
    )
    kept: list[dict] = []
    deduped: list[dict] = []
    seen: dict[str, str] = {}
    for item in ordered:
        fingerprint = str(item.get("effective_mutation_fingerprint", "")).strip()
        if not fingerprint:
            kept.append(item)
            continue
        existing_candidate_id = seen.get(fingerprint)
        if existing_candidate_id:
            deduped.append(
                {
                    "candidate_id": str(item.get("candidate_id", "")),
                    "proposal_origin": str(item.get("proposal_origin", "")),
                    "duplicate_of_candidate_id": existing_candidate_id,
                    "effective_mutation_fingerprint": fingerprint,
                }
            )
            continue
        seen[fingerprint] = str(item.get("candidate_id", ""))
        kept.append(item)
    return kept, deduped


def _filter_tested_trials(trials: list[dict], benchmark_summary: dict, policy: dict) -> tuple[list[dict], list[dict]]:
    variety_index = benchmark_variety_index(benchmark_summary)
    by_candidate_id = variety_index.get("by_candidate_id", {})
    by_fingerprint = variety_index.get("by_fingerprint", {})
    by_family_child = variety_index.get("by_family_child", {})
    variety_policy = policy.get("variety_lane", {}) if isinstance(policy.get("variety_lane"), dict) else {}
    max_total = max(1, int(variety_policy.get("max_mutation_trials_per_cycle", 8) or 8))
    max_per_family = max(1, int(variety_policy.get("max_pending_children_per_family", 2) or 2))
    reserved_psychology_slots = min(2, max_total)
    # Lane-based allocation: ensure variety backlog items get fair share of slots.
    # Without this, higher-priority contradiction probes starve variety exploration.
    variety_trial_count = sum(1 for t in trials if str(t.get("proposal_origin", "")) == "variety_backlog")
    reserved_variety_slots = min(max(0, max_total * 2 // 5), variety_trial_count) if variety_trial_count > 0 else 0
    # Pro insights lane: proven guard seeding from evolution system
    pro_trial_count = sum(1 for t in trials if str(t.get("proposal_origin", "")) == "pro_insights")
    reserved_pro_slots = min(2, pro_trial_count) if pro_trial_count > 0 else 0
    # Per-origin caps to ensure diversity across lanes
    max_probe_slots = max_total - reserved_variety_slots - reserved_psychology_slots - reserved_pro_slots

    gated: list[dict] = []
    kept: list[dict] = []
    family_counts: dict[str, int] = {}
    origin_counts: dict[str, int] = {}
    ordered = sorted(
        trials,
        key=lambda item: (
            {
                "contradiction_probe": 0,
                "pro_insights": 1,
                "variety_backlog": 2,
                "psychology_pattern_map": 3,
                "mutation_backlog": 4,
            }.get(str(item.get("proposal_origin", "")), 9),
            str(item.get("variety_family_id", "")),
            str(item.get("candidate_id", "")),
        ),
    )
    for item in ordered:
        candidate_id = str(item.get("candidate_id", "")).strip()
        family_id = str(item.get("variety_family_id", "")).strip()
        child_id = str(item.get("variety_child_id", "")).strip()
        fingerprint = str(item.get("effective_mutation_fingerprint", "")).strip()
        family_child_key = f"{family_id}::{child_id}" if family_id else ""
        proposal_origin = str(item.get("proposal_origin", "")).strip()
        gate_reason = ""
        if candidate_id and candidate_id in by_candidate_id:
            gate_reason = "candidate_already_benchmarked"
        elif fingerprint and fingerprint in by_fingerprint:
            gate_reason = "effective_mutation_already_benchmarked"
        elif family_child_key and family_child_key in by_family_child:
            gate_reason = "variety_child_already_benchmarked"
        elif family_id and family_counts.get(family_id, 0) >= max_per_family:
            gate_reason = "family_budget_exhausted"
        elif proposal_origin == "contradiction_probe" and origin_counts.get("contradiction_probe", 0) >= max_probe_slots:
            gate_reason = "probe_lane_exhausted"
        elif proposal_origin == "variety_backlog" and origin_counts.get("variety_backlog", 0) >= reserved_variety_slots:
            gate_reason = "variety_lane_exhausted"
        elif proposal_origin == "pro_insights" and origin_counts.get("pro_insights", 0) >= reserved_pro_slots:
            gate_reason = "pro_insights_lane_exhausted"
        elif proposal_origin == "psychology_pattern_map" and origin_counts.get("psychology_pattern_map", 0) >= reserved_psychology_slots:
            gate_reason = "psychology_lane_exhausted"
        elif len(kept) >= max_total:
            gate_reason = "cycle_budget_exhausted"
        if gate_reason:
            gated.append(
                {
                    "candidate_id": candidate_id,
                    "proposal_origin": proposal_origin,
                    "variety_family_id": family_id,
                    "variety_child_id": child_id,
                    "effective_mutation_fingerprint": fingerprint,
                    "gate_reason": gate_reason,
                }
            )
            continue
        kept.append(item)
        origin_counts[proposal_origin] = origin_counts.get(proposal_origin, 0) + 1
        if family_id:
            family_counts[family_id] = family_counts.get(family_id, 0) + 1
    return kept, gated


def main() -> None:
    backlog_path = REPO_ROOT / "artifacts" / "recursion" / "mutation_backlog.json"
    probe_path = REPO_ROOT / "artifacts" / "recursion" / "contradiction_probes.json"
    variety_backlog_path = REPO_ROOT / "artifacts" / "recursion" / "variety_backlog.json"
    summary_path = REPO_ROOT / "artifacts" / "backtests" / "heavy_backtest_summary.json"
    policy_path = REPO_ROOT / "docs" / "recursion" / "loop-policy.json"
    pattern_map_path = REPO_ROOT / "artifacts" / "research" / "pattern_regime_map.json"
    backlog = _load_json(backlog_path)
    probes = _load_probe_json(probe_path)
    variety_backlog = _load_json(variety_backlog_path)
    summary_index = _load_summary_index(summary_path)
    benchmark_summary = _load_object(summary_path)
    policy = _load_object(policy_path)
    pattern_map = _load_pattern_map(pattern_map_path)
    trials: list[dict] = []
    for item in backlog:
        if not isinstance(item, dict):
            continue
        if _status_blocks_trial(item):
            continue
        proposal_id = str(item.get("proposal_id", ""))
        mutations = _backlog_mutations(item)
        if not mutations:
            continue
        trials.append(
            {
                "candidate_id": proposal_id,
                "candidate_summary": str(item.get("title", proposal_id)),
                "hypothesis": str(item.get("research_thesis", "")),
                "mutations": normalize_mutations(mutations),
                "source_names": item.get("source_names", []),
                "proposal_origin": "mutation_backlog",
            }
        )
    trials.extend(_derived_trials(probes, summary_index))
    trials.extend(_variety_trials(variety_backlog, summary_index))
    trials.extend(_psychology_trials(backlog, pattern_map))
    trials.extend(_pro_insight_trials(summary_index))
    trials = [_enrich_trial(item) for item in trials]
    trials, deduped = _dedupe_trials(trials)
    trials, gated = _filter_tested_trials(trials, benchmark_summary, policy)
    target_root = REPO_ROOT / "artifacts" / "recursion"
    target_root.mkdir(parents=True, exist_ok=True)
    trials_path = target_root / "mutation_trials.json"
    safe_write_json(trials_path, trials)
    dedupe_path = target_root / "mutation_trial_dedupe_report.json"
    dedupe_payload = {
        "kept_count": len(trials),
        "deduped_count": len(deduped),
        "deduped_trials": deduped,
        "gated_count": len(gated),
        "gated_trials": gated,
    }
    safe_write_json(dedupe_path, dedupe_payload)
    print(trials_path)
    print(dedupe_path)


if __name__ == "__main__":
    main()
