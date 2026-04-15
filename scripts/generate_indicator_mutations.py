"""Generate indicator-enriched mutations from proven champions.

Reads artifacts/forge/proven_champions.json and produces candidate trials
that combine each champion's base mutation dict with new indicator guards
(ADX, CCI, Keltner, Williams %R, CMF).

Output: artifacts/forge/indicator_mutations.json  (for forge screening)
Also appends new candidates to spark-researcher.project.json so the
standard backtest pipeline can evaluate them too.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

FORGE_DIR = REPO_ROOT / "artifacts" / "forge"

# ── Strategy-to-prefix mapping ──────────────────────────────────────
# Each strategy family uses a unique prefix for its indicator guard mutations.
# The shared _apply_indicator_guards() in backtest.py reads {prefix}_adx_guard etc.
STRATEGY_GUARD_PREFIXES: dict[str, str] = {
    "compression_range_bounce": "cr",
    "multi_confirm_bounce": "mcb",
    "vwap_reversion": "vr",
    "participation_gate_overlay": "pg",
    "range_extreme_fade": "rf",
    "channel_breakout_fade": "cb",
    "rsi_extreme_reversion": "re",
    "intermarket_context_gate": "im",
    # Session 26: newly wired strategies
    "bollinger_squeeze_breakout": "bs",
    "contrarian_overextension_fade": "co",
    "trend_pullback_entry": "tp",
    "momentum_fade": "mf",
    "ema_crossover_fade": "ef",
    "keltner_mean_reversion": "km",
    # Session 26: new quant strategies
    "momentum_zscore_reversal": "mz",
    "linreg_deviation_reversion": "lr",
    "ou_adaptive_entry": "ou",
    "macd_histogram_reversal": "mh",
}

# ── Indicator guard templates ────────────────────────────────────────
# Each template defines a guard suffix and its possible values.
# "off" is always implicit (champion as-is), so we only list active values.
# Actual mutation key = "{prefix}_{suffix}", e.g. "cr_adx_guard", "mcb_adx_guard".
INDICATOR_GUARD_TEMPLATES: list[dict[str, Any]] = [
    {
        "suffix": "adx_guard",
        "name": "ADX trend filter",
        "values": [
            "skip_no_trend",       # ADX < 20 → no trend, skip
            "skip_strong_trend",   # ADX > 40 → overextended trend, skip
            "skip_extreme_trend",  # ADX > 50 → very extreme, skip
            "require_di_aligned",  # +DI/-DI must match predicted direction
        ],
    },
    {
        "suffix": "cci_guard",
        "name": "CCI mean reversion filter",
        "values": [
            "skip_dead_zone",      # CCI in -50 to +50 → no momentum, skip
            "skip_narrow",         # CCI in -100 to +100 → wider dead zone
            "skip_extreme",        # CCI > 200 or < -200 → too extreme, skip
            "require_aligned",     # CCI must confirm direction
        ],
    },
    {
        "suffix": "keltner_guard",
        "name": "Keltner Channel filter",
        "values": [
            "skip_inside",         # price inside channel (0.2-0.8), skip
            "skip_narrow_channel", # channel width < 1%, skip
            "require_extreme",     # price must be at channel extreme
        ],
    },
    {
        "suffix": "williams_guard",
        "name": "Williams %R filter",
        "values": [
            "skip_neutral",        # %R in -80 to -20 → neutral, skip
            "skip_wide_neutral",   # %R in -70 to -30 → wider neutral
            "require_aligned",     # %R must be at extreme matching direction
        ],
    },
    {
        "suffix": "cmf_guard",
        "name": "CMF volume flow filter",
        "values": [
            "require_aligned",     # CMF must match predicted direction
            "require_strong",      # CMF must strongly match (>0.05)
            "skip_weak_flow",      # CMF in -0.05 to 0.05 → no conviction
        ],
    },
]


def _prefix_for_champion(champion: dict[str, Any]) -> str:
    """Determine the indicator guard prefix for a champion based on its strategy_id."""
    strategy_id = champion.get("mutations", {}).get("strategy_id", "")
    return STRATEGY_GUARD_PREFIXES.get(strategy_id, "cr")


def _indicator_guards_for_prefix(prefix: str) -> list[dict[str, Any]]:
    """Build concrete guard defs with prefixed keys for a given strategy prefix."""
    return [
        {
            "key": f"{prefix}_{tmpl['suffix']}",
            "name": tmpl["name"],
            "values": tmpl["values"],
        }
        for tmpl in INDICATOR_GUARD_TEMPLATES
    ]


# Legacy alias for backward compatibility
INDICATOR_GUARDS: list[dict[str, Any]] = _indicator_guards_for_prefix("cr")


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _normalize_candidate_id(cid: str) -> str:
    """Normalize candidate ID for dedup: underscore/hyphen variants are identical."""
    return cid.replace("_", "-").lower().strip()


def _existing_candidate_ids(config: dict[str, Any]) -> set[str]:
    """Collect all existing candidate IDs from project config (normalized for dedup)."""
    ids: set[str] = set()
    for trial in config.get("candidate_trials", []):
        if isinstance(trial, dict):
            cid = str(trial.get("candidate_id", "")).strip()
            if cid:
                ids.add(_normalize_candidate_id(cid))
    return ids


def _generate_single_guard_mutations(
    champion: dict[str, Any],
    existing_ids: set[str],
) -> list[dict[str, Any]]:
    """Generate mutations adding ONE new indicator guard to a champion."""
    champ_id = champion["champion_id"]
    base_mutations = dict(champion["mutations"])
    prefix = _prefix_for_champion(champion)
    guards = _indicator_guards_for_prefix(prefix)
    children: list[dict[str, Any]] = []

    for guard in guards:
        key = guard["key"]
        # Strip prefix + underscore for readable candidate ID
        guard_label = key[len(prefix) + 1:]  # e.g. "adx_guard" from "mcb_adx_guard"
        for value in guard["values"]:
            candidate_id = f"forge-{champ_id}-{guard_label.replace('_', '-')}-{value.replace('_', '-')}"
            if _normalize_candidate_id(candidate_id) in existing_ids:
                continue

            mutations = dict(base_mutations)
            mutations[key] = value
            mutations["source"] = "forge"

            children.append({
                "candidate_id": candidate_id,
                "candidate_summary": f"Forge: {champ_id} + {guard['name']} ({value})",
                "hypothesis": f"Adding {guard['name']} guard ({value}) to proven champion {champ_id} (WR={champion.get('backtest_wr', '?')}, WF={champion.get('wf', '?')}) may improve edge by filtering trades where {guard['name']} contradicts the setup.",
                "mutations": mutations,
                "forge_metadata": {
                    "base_champion": champ_id,
                    "indicator_guard": key,
                    "guard_value": value,
                    "family": champion.get("family", "unknown"),
                },
            })
            existing_ids.add(_normalize_candidate_id(candidate_id))

    return children


def _generate_pair_guard_mutations(
    champion: dict[str, Any],
    existing_ids: set[str],
    max_pairs: int = 20,
) -> list[dict[str, Any]]:
    """Generate mutations adding TWO indicator guards (selected pairs only).

    Only generates pairs from different indicator families to avoid redundancy.
    Limits output to max_pairs per champion to keep backtest manageable.
    """
    champ_id = champion["champion_id"]
    base_mutations = dict(champion["mutations"])
    prefix = _prefix_for_champion(champion)
    children: list[dict[str, Any]] = []

    # Only pair guards from different indicators, pick best value per indicator
    best_values = {
        f"{prefix}_adx_guard": ["skip_strong_trend", "require_di_aligned"],
        f"{prefix}_cci_guard": ["skip_dead_zone", "require_aligned"],
        f"{prefix}_keltner_guard": ["skip_inside", "require_extreme"],
        f"{prefix}_williams_guard": ["skip_neutral", "require_aligned"],
        f"{prefix}_cmf_guard": ["require_aligned", "skip_weak_flow"],
    }

    keys = sorted(best_values.keys())
    prefix_strip = f"{prefix}_"
    for i, key_a in enumerate(keys):
        for key_b in keys[i + 1:]:
            for val_a, val_b in product(best_values[key_a][:1], best_values[key_b][:1]):
                if len(children) >= max_pairs:
                    return children

                label_a = f"{key_a.replace(prefix_strip, '')}-{val_a.replace('_', '-')}"
                label_b = f"{key_b.replace(prefix_strip, '')}-{val_b.replace('_', '-')}"
                candidate_id = f"forge-{champ_id}-pair-{label_a}+{label_b}"

                if _normalize_candidate_id(candidate_id) in existing_ids:
                    continue

                mutations = dict(base_mutations)
                mutations[key_a] = val_a
                mutations[key_b] = val_b
                mutations["source"] = "forge"

                children.append({
                    "candidate_id": candidate_id,
                    "candidate_summary": f"Forge pair: {champ_id} + {key_a}={val_a} + {key_b}={val_b}",
                    "hypothesis": f"Pairing two indicator guards on champion {champ_id} to test whether combined filtering improves WR without crashing WF. Higher trade count champions ({champion.get('backtest_trades', '?')} trades) can absorb more filtering.",
                    "mutations": mutations,
                    "forge_metadata": {
                        "base_champion": champ_id,
                        "indicator_guards": [key_a, key_b],
                        "guard_values": [val_a, val_b],
                        "family": champion.get("family", "unknown"),
                        "pair_mutation": True,
                    },
                })
                existing_ids.add(_normalize_candidate_id(candidate_id))

    return children


def generate_indicator_mutations(
    repo_root: Path,
    singles: bool = True,
    pairs: bool = True,
    append_to_config: bool = True,
) -> dict[str, Any]:
    """Generate all indicator-enriched mutations from proven champions."""
    champions_path = FORGE_DIR / "proven_champions.json"
    champions_data = _load_json(champions_path, {})
    champions = champions_data.get("champions", [])

    if not champions:
        return {"error": "No champions found", "material_change": False}

    config_path = repo_root / "spark-researcher.project.json"
    config = _load_json(config_path, {})
    if not isinstance(config, dict):
        config = {}

    existing_ids = _existing_candidate_ids(config)
    all_new: list[dict[str, Any]] = []

    for champion in champions:
        if singles:
            single_mutations = _generate_single_guard_mutations(champion, existing_ids)
            all_new.extend(single_mutations)
        if pairs:
            # Only pair mutations for high-trade-count champions (can absorb filtering)
            trades = champion.get("backtest_trades", 0)
            if trades >= 500:
                pair_mutations = _generate_pair_guard_mutations(champion, existing_ids)
                all_new.extend(pair_mutations)

    # Write forge-specific output
    forge_output = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "champions_processed": len(champions),
        "single_mutations": sum(1 for c in all_new if not c.get("forge_metadata", {}).get("pair_mutation")),
        "pair_mutations": sum(1 for c in all_new if c.get("forge_metadata", {}).get("pair_mutation")),
        "total_generated": len(all_new),
        "candidates": all_new,
    }
    FORGE_DIR.mkdir(parents=True, exist_ok=True)
    forge_path = FORGE_DIR / "indicator_mutations.json"
    forge_path.write_text(json.dumps(forge_output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Append to mutation_trials instead of researcher config
    if append_to_config and all_new:
        trials_path = repo_root / "artifacts" / "recursion" / "mutation_trials.json"
        trials_path.parent.mkdir(parents=True, exist_ok=True)
        existing_trials = json.loads(trials_path.read_text(encoding="utf-8")) if trials_path.exists() else []
        existing_trials = existing_trials if isinstance(existing_trials, list) else []
        for candidate in all_new:
            trial = {k: v for k, v in candidate.items() if k != "forge_metadata"}
            existing_trials.append(trial)
        safe_write_json(trials_path, existing_trials)

    report = {
        "generated_at": forge_output["generated_at"],
        "champions_processed": len(champions),
        "single_mutations": forge_output["single_mutations"],
        "pair_mutations": forge_output["pair_mutations"],
        "total_generated": len(all_new),
        "material_change": len(all_new) > 0,
        "appended_to_config": append_to_config and len(all_new) > 0,
    }

    report_path = FORGE_DIR / "indicator_mutation_report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return report


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate indicator-enriched mutations from proven champions")
    parser.add_argument("--no-pairs", action="store_true", help="Skip pair guard mutations")
    parser.add_argument("--no-config", action="store_true", help="Don't append to spark-researcher.project.json")
    parser.add_argument("--singles-only", action="store_true", help="Only single indicator guards")
    args = parser.parse_args()

    report = generate_indicator_mutations(
        REPO_ROOT,
        singles=True,
        pairs=not args.no_pairs and not args.singles_only,
        append_to_config=not args.no_config,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
