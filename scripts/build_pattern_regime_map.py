from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _psychology_overlays(repo_root: Path) -> list[dict[str, Any]]:
    data = _load_json(repo_root / "docs" / "research-ingest" / "market-psychology-overlays.json", [])
    return data if isinstance(data, list) else []


def _overlay_ids_for_regime(regime_id: str) -> list[str]:
    mapping: dict[str, list[str]] = {
        "trend_continuation_greed": [
            "expectation_already_priced",
            "sell_the_news_risk",
            "narrative_reflexive_tailwind",
            "crowded_position_unwind",
        ],
        "range_chop_mean_reversion": [
            "edge_only_participation_psychology",
            "crowded_position_unwind",
        ],
        "fear_shock_high_alert": [
            "panic_then_liquidity_reversal",
            "crowded_position_unwind",
            "edge_only_participation_psychology",
        ],
        "compression_pre_breakout": [
            "expectation_already_priced",
            "edge_only_participation_psychology",
        ],
        "event_driven_macro_transition": [
            "expectation_already_priced",
            "policy_liquidity_tailwind",
            "narrative_reflexive_tailwind",
            "edge_only_participation_psychology",
        ],
    }
    return mapping.get(regime_id, [])


def _mutation_hints_for_pattern(pattern: str) -> list[str]:
    hints: dict[str, list[str]] = {
        "trend pullback continuation": [
            "disable chase entries when sell_the_news_risk is high",
            "require repeated dip acceptance when narrative_reflexive_tailwind is present",
        ],
        "vcp breakout": [
            "tighten breakout-quality gates when crowded_position_unwind is high",
            "downgrade continuation if expectation_already_priced is active near catalysts",
        ],
        "adaptive trend filter": [
            "favor delayed participation when policy_liquidity_tailwind matters more than first reaction",
            "skip when edge_only_participation_psychology says catalyst interpretation is unresolved",
        ],
        "liquidity reclaim": [
            "favor reclaim only after crowding unwind is evident",
            "avoid reclaim in shock windows unless panic_then_liquidity_reversal is already shifting",
        ],
        "rsi exhaustion reclaim": [
            "use only when edge_only_participation_psychology does not flag unstable follow-through",
            "avoid if event surprise remains unresolved after the first session",
        ],
        "opening-range failure fade": [
            "upgrade after failed catalyst continuation in sell_the_news conditions",
            "avoid if policy or macro event is still unresolved intraday",
        ],
        "event avoidance filter": [
            "expand no-trade windows when expectation_state is highly_anticipated_and_narrated",
            "keep abstention active when crowding_risk is high and second_order_horizon extends beyond intraday",
        ],
        "reflexive no-trade window": [
            "stay out while narrative and price are feeding each other without stable structure",
            "prefer delayed re-entry only after second-order consequences begin to dominate",
        ],
        "climax reversal with strict confirmation": [
            "only activate after crowding unwind and failed continuation are both visible",
            "avoid if policy_tailwind suggests the first panic leg is not the durable regime",
        ],
        "macro no-trade filter": [
            "skip first reaction when expectation_vs_transition_split is unresolved",
            "separate announcement shock from follow-through before re-enabling participation",
        ],
        "intermarket context gate": [
            "require cross-asset confirmation before calling a transition regime tradable",
            "deprioritize BTC-only continuation when macro interpretation is fragmented",
        ],
        "risk-throttle sizing overlay": [
            "shrink size when crowding_risk is high even if the catalyst is directionally supportive",
            "reduce exposure while second_order_horizon is longer than the current holding horizon",
        ],
        "carter squeeze release": [
            "treat scheduled surprise windows as fake-break prone unless path confirms release quality",
        ],
        "bollinger squeeze breakout": [
            "avoid headline-driven releases when compression is only post-shock noise, not pre-break quality",
        ],
        "vcp pivot breakout": [
            "require clean post-event stabilization before breakout participation",
        ],
    }
    return hints.get(pattern, [])


def build_pattern_regime_map(repo_root: Path | None = None) -> Path:
    root = repo_root or REPO_ROOT
    regimes = _load_json(root / "docs" / "research-ingest" / "market-regime-intelligence.json", [])
    regimes = regimes if isinstance(regimes, list) else []
    overlay_rows = _psychology_overlays(root)
    overlay_lookup = {
        str(item.get("overlay_id", "")).strip(): item
        for item in overlay_rows
        if isinstance(item, dict) and str(item.get("overlay_id", "")).strip()
    }
    validation = _load_json(root / "artifacts" / "research" / "timeline_pack_validation.json", {})
    validation = validation if isinstance(validation, dict) else {}
    validation_rows = validation.get("rows", [])
    validation_rows = validation_rows if isinstance(validation_rows, list) else []

    validation_by_regime: dict[str, list[dict[str, Any]]] = {}
    for row in validation_rows:
        if not isinstance(row, dict):
            continue
        validation_by_regime.setdefault(str(row.get("regime_id", "")).strip(), []).append(row)

    regime_rows: list[dict[str, Any]] = []
    pattern_index: dict[str, dict[str, Any]] = {}

    for regime in regimes:
        if not isinstance(regime, dict):
            continue
        regime_id = str(regime.get("regime_id", "")).strip()
        fit_patterns = regime.get("fit_patterns", [])
        fit_patterns = fit_patterns if isinstance(fit_patterns, list) else []
        avoid_patterns = regime.get("avoid_patterns", [])
        avoid_patterns = avoid_patterns if isinstance(avoid_patterns, list) else []
        rows = validation_by_regime.get(regime_id, [])
        validated = [row for row in rows if str(row.get("validation_status", "")).strip() == "validated_match"]
        mixed = [row for row in rows if str(row.get("validation_status", "")).strip() == "mixed_proxy"]
        mismatched = [row for row in rows if str(row.get("validation_status", "")).strip() == "mismatch_review"]
        ready = [row for row in rows if bool(row.get("dataset_ready"))]
        regime_rows.append(
            {
                "regime_id": regime_id,
                "regime_label": regime.get("label"),
                "market_character": regime.get("market_character"),
                "fit_patterns": fit_patterns,
                "avoid_patterns": avoid_patterns,
                "research_gaps": regime.get("research_gaps", []),
                "validated_pack_ids": [str(row.get("pack_id", "")).strip() for row in validated],
                "mixed_pack_ids": [str(row.get("pack_id", "")).strip() for row in mixed],
                "mismatch_pack_ids": [str(row.get("pack_id", "")).strip() for row in mismatched],
                "dataset_ready_pack_ids": [str(row.get("pack_id", "")).strip() for row in ready],
                "psychology_overlay_ids": _overlay_ids_for_regime(regime_id),
                "psychology_overlay_labels": [
                    str(overlay_lookup.get(overlay_id, {}).get("label", overlay_id))
                    for overlay_id in _overlay_ids_for_regime(regime_id)
                ],
                "regime_readiness": (
                    "validated"
                    if validated
                    else "mixed_proxy"
                    if mixed
                    else "needs_review"
                    if mismatched
                    else "needs_extract"
                ),
            }
        )
        for pattern in fit_patterns:
            key = str(pattern).strip()
            if not key:
                continue
            pattern_index.setdefault(
                key,
                {
                    "pattern": key,
                    "fit_regimes": [],
                    "avoid_regimes": [],
                    "validated_pack_ids": [],
                    "mixed_pack_ids": [],
                    "psychology_mutation_hints": _mutation_hints_for_pattern(key),
                },
            )
            pattern_index[key]["fit_regimes"].append(regime_id)
            pattern_index[key]["validated_pack_ids"].extend(str(row.get("pack_id", "")).strip() for row in validated)
            pattern_index[key]["mixed_pack_ids"].extend(str(row.get("pack_id", "")).strip() for row in mixed)
        for pattern in avoid_patterns:
            key = str(pattern).strip()
            if not key:
                continue
            pattern_index.setdefault(
                key,
                {
                    "pattern": key,
                    "fit_regimes": [],
                    "avoid_regimes": [],
                    "validated_pack_ids": [],
                    "mixed_pack_ids": [],
                    "psychology_mutation_hints": _mutation_hints_for_pattern(key),
                },
            )
            pattern_index[key]["avoid_regimes"].append(regime_id)

    pattern_rows = sorted(pattern_index.values(), key=lambda item: str(item.get("pattern", "")))
    payload = {
        "regime_count": len(regime_rows),
        "pattern_count": len(pattern_rows),
        "regime_rows": regime_rows,
        "pattern_rows": pattern_rows,
        "top_regime_rows": regime_rows[:8],
        "top_pattern_rows": pattern_rows[:12],
    }
    target = root / "artifacts" / "research" / "pattern_regime_map.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def main() -> None:
    path = build_pattern_regime_map(REPO_ROOT)
    print(path)


if __name__ == "__main__":
    main()
