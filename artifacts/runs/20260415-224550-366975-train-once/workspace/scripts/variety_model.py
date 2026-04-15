from __future__ import annotations

import json
from typing import Any


EFFECTIVE_MUTATION_KEYS = (
    "doctrine_id",
    "strategy_id",
    "market_regime",
    "activation_profile",
    "execution_buffer",
    "late_sample_guard",
    "drawdown_guard",
    "session_profile",
    "impulse_profile",
    "compression_profile",
    "reversal_confirmation",
    "no_trade_window",
    "range_edge_profile",
    "wick_profile",
    "chase_policy",
    "follow_through_profile",
    "catalyst_failure_mode",
    "event_interpretation_policy",
    "paper_gate",
)

VARIETY_FAMILY_MUTATION_KEYS = (
    "doctrine_id",
    "strategy_id",
    "market_regime",
)

VARIETY_CHILD_MUTATION_KEYS = tuple(
    key for key in EFFECTIVE_MUTATION_KEYS if key not in VARIETY_FAMILY_MUTATION_KEYS
)


def normalize_mutations(raw: Any) -> dict[str, str]:
    if not isinstance(raw, dict):
        return {}
    return {
        str(key): str(value)
        for key, value in raw.items()
        if str(key).strip() and str(value).strip()
    }


def effective_fingerprint(mutations: dict[str, str]) -> str:
    normalized = {
        key: str(mutations.get(key, ""))
        for key in EFFECTIVE_MUTATION_KEYS
        if str(mutations.get(key, "")).strip()
    }
    return json.dumps(normalized, sort_keys=True)


def variety_family_id(
    mutations: dict[str, str],
    *,
    doctrine_family: str = "",
    strategy_family: str = "",
    target_contract_family: str = "",
) -> str:
    normalized = normalize_mutations(mutations)
    contract_label = target_contract_family
    if not contract_label:
        venue = normalized.get("venue", "unknown")
        timeframe = normalized.get("timeframe", "unknown")
        asset_universe = normalized.get("asset_universe", "")
        if venue == "kalshi" and timeframe == "15m" and "BTC" in {item.strip() for item in asset_universe.split(",") if item.strip()}:
            contract_label = "btc_up_down_15m"
        else:
            contract_label = f"{venue}:{timeframe}"
    family_payload = {
        "contract": contract_label,
        "doctrine": doctrine_family or normalized.get("doctrine_id", "unknown"),
        "strategy": strategy_family or normalized.get("strategy_id", "unknown"),
        "regime": normalized.get("market_regime", "unknown"),
    }
    return json.dumps(family_payload, sort_keys=True)


def variety_child_mutations(mutations: dict[str, str]) -> dict[str, str]:
    normalized = normalize_mutations(mutations)
    return {
        key: normalized[key]
        for key in VARIETY_CHILD_MUTATION_KEYS
        if key in normalized and str(normalized[key]).strip()
    }


def variety_child_id(mutations: dict[str, str]) -> str:
    child = variety_child_mutations(mutations)
    if not child:
        return "base"
    return json.dumps(child, sort_keys=True)


def variety_child_label(mutations: dict[str, str]) -> str:
    child = variety_child_mutations(mutations)
    if not child:
        return "base"
    return ", ".join(f"{key}={value}" for key, value in sorted(child.items()))


def row_mutations(row: dict[str, Any]) -> dict[str, str]:
    return normalize_mutations(row.get("mutations", {}))


def sort_metric_tuple(row: dict[str, Any]) -> tuple[float, float, float, float]:
    metrics = row.get("metrics", {}) if isinstance(row.get("metrics"), dict) else {}
    result = row.get("result", {}) if isinstance(row.get("result"), dict) else {}
    return (
        float(metrics.get("profitability_score", 0.0) or 0.0),
        float(result.get("holdout_profitability_score", 0.0) or 0.0),
        float(metrics.get("paper_trade_readiness", 0.0) or 0.0),
        -float(metrics.get("max_drawdown", 0.0) or 0.0),
    )


def benchmark_variety_index(summary: dict[str, Any]) -> dict[str, Any]:
    rows = summary.get("rows", []) if isinstance(summary, dict) else []
    rows = rows if isinstance(rows, list) else []
    by_candidate_id: dict[str, dict[str, Any]] = {}
    by_fingerprint: dict[str, dict[str, Any]] = {}
    by_family: dict[str, dict[str, Any]] = {}
    by_family_child: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        candidate_id = str(row.get("candidate_id", "")).strip()
        mutations = row_mutations(row)
        family_id = variety_family_id(mutations)
        child_id = variety_child_id(mutations)
        fingerprint = effective_fingerprint(mutations)
        if candidate_id:
            by_candidate_id[candidate_id] = row
        if fingerprint:
            by_fingerprint[fingerprint] = row
        family_bucket = by_family.setdefault(
            family_id,
            {
                "family_id": family_id,
                "rows": [],
                "tested_child_ids": set(),
                "tested_fingerprints": set(),
                "top_row": None,
            },
        )
        family_bucket["rows"].append(row)
        family_bucket["tested_child_ids"].add(child_id)
        if fingerprint:
            family_bucket["tested_fingerprints"].add(fingerprint)
        if family_bucket["top_row"] is None or sort_metric_tuple(row) > sort_metric_tuple(family_bucket["top_row"]):
            family_bucket["top_row"] = row
        by_family_child[f"{family_id}::{child_id}"] = row
    return {
        "by_candidate_id": by_candidate_id,
        "by_fingerprint": by_fingerprint,
        "by_family": by_family,
        "by_family_child": by_family_child,
    }
