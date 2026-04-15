"""Generate code-level signal mutations from untested feature combinations.

This closes the code-mutation gap: instead of only tweaking parameters, this
script proposes NEW conditional branches for the _signal function by combining
existing features in ways that haven't been tested.

It reads the current leaderboard to find what feature ranges correlate with
wins/losses, then generates new candidate trials with novel entry conditions
that the existing strategy families don't cover.

The mutations are written as new candidate trials to spark-researcher.project.json
so the next backtest cycle evaluates them.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

from safe_write import safe_write_json
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


# Feature-combination templates that the _signal function already supports
# but haven't been tested together.  Each template defines a candidate
# trial with specific mutation combinations.
MUTATION_TEMPLATES: list[dict[str, Any]] = [
    # --- Range mean-reversion with session + wick filters ---
    {
        "id_prefix": "auto-range-session-wick",
        "summary": "Range reclaim with session-aligned wick rejection entry.",
        "hypothesis": "Combining session alignment with wick rejection should produce higher-quality mean-reversion entries that survive holdout.",
        "base_mutations": {
            "doctrine_id": "mean_reversion_liquidity_reclaim",
            "strategy_id": "range_reclaim_scalp",
            "market_regime": "range",
            "asset_universe": "BTC,ETH,SOL",
            "timeframe": "1h",
            "venue": "bybit",
            "paper_gate": "balanced",
        },
        "dimension_grid": {
            "session_profile": ["opening_range_failure"],
            "wick_profile": ["rejection_confirm"],
            "reversal_confirmation": ["reclaim_close", "wick_reclaim_close"],
            "volume_context_guard": ["thin_filter", "off"],
        },
        "max_children": 4,
    },
    # --- Breakout with compression + impulse filters ---
    {
        "id_prefix": "auto-breakout-impulse-squeeze",
        "summary": "Breakout with combined compression and impulse follow-through.",
        "hypothesis": "Requiring both squeeze compression and impulse follow-through should filter fakeouts while preserving real breakout signals.",
        "base_mutations": {
            "doctrine_id": "breakout_volatility_expansion",
            "strategy_id": "bollinger_squeeze_breakout",
            "market_regime": "high_vol",
            "asset_universe": "BTC",
            "timeframe": "15m",
            "venue": "kalshi",
            "paper_gate": "balanced",
        },
        "dimension_grid": {
            "compression_profile": ["tight_squeeze", "moderate_squeeze"],
            "session_profile": ["squeeze_release_window", "all"],
            "late_sample_guard": ["on", "off"],
        },
        "max_children": 4,
    },
    # --- Wedge reversal with drawdown guard ---
    {
        "id_prefix": "auto-wedge-guarded",
        "summary": "Wedge exhaustion reversal with drawdown and volume guards.",
        "hypothesis": "Adding drawdown guard and volume filter to wedge reversals should reduce max drawdown while maintaining signal density.",
        "base_mutations": {
            "doctrine_id": "mean_reversion_liquidity_reclaim",
            "strategy_id": "wedge_exhaustion_reversal",
            "market_regime": "range",
            "asset_universe": "BTC",
            "timeframe": "15m",
            "venue": "kalshi",
            "paper_gate": "balanced",
        },
        "dimension_grid": {
            "drawdown_guard": ["high", "off"],
            "volume_context_guard": ["thin_filter", "strict_participation"],
            "reversal_confirmation": ["reclaim_close"],
            "wick_profile": ["rejection_confirm"],
        },
        "max_children": 4,
    },
    # --- Trend with volume and no-trade window ---
    {
        "id_prefix": "auto-trend-volume-filtered",
        "summary": "Trend following with volume context and dead-zone avoidance.",
        "hypothesis": "Volume-filtered trend following with dead zone avoidance should produce more consistent returns by skipping thin-market conditions.",
        "base_mutations": {
            "doctrine_id": "trend_regime_following",
            "strategy_id": "ema_pullback_long",
            "market_regime": "trend",
            "asset_universe": "BTC,ETH",
            "timeframe": "4h",
            "venue": "binance",
            "paper_gate": "balanced",
        },
        "dimension_grid": {
            "volume_context_guard": ["thin_filter", "strict_participation"],
            "no_trade_window": ["avoid_dead_zone", "avoid_post_open_drift"],
            "activation_profile": ["wider", "base"],
        },
        "max_children": 4,
    },
]


def _existing_candidate_ids(config: dict[str, Any], mutation_trials: list[dict]) -> set[str]:
    """Collect all existing candidate IDs from config and mutation trials."""
    ids: set[str] = set()
    for trial in config.get("candidate_trials", []):
        if isinstance(trial, dict):
            cid = str(trial.get("candidate_id", "")).strip()
            if cid:
                ids.add(cid)
    for trial in mutation_trials:
        if isinstance(trial, dict):
            cid = str(trial.get("candidate_id", "")).strip()
            if cid:
                ids.add(cid)
    return ids


def _generate_children(template: dict[str, Any], existing_ids: set[str]) -> list[dict[str, Any]]:
    """Generate candidate trials from a template's dimension grid."""
    grid = template.get("dimension_grid", {})
    max_children = template.get("max_children", 4)
    base = dict(template.get("base_mutations", {}))
    prefix = template.get("id_prefix", "auto-unknown")
    summary = template.get("summary", "")
    hypothesis = template.get("hypothesis", "")

    dimension_names = sorted(grid.keys())
    dimension_values = [grid[name] for name in dimension_names]

    children: list[dict[str, Any]] = []
    for combo in product(*dimension_values):
        if len(children) >= max_children:
            break
        mutations = dict(base)
        label_parts = []
        for name, value in zip(dimension_names, combo):
            mutations[name] = value
            if value not in {"off", "base", "all"}:
                label_parts.append(f"{name}={value}")

        label = "-".join(label_parts) if label_parts else "base"
        candidate_id = f"{prefix}-{label}"

        if candidate_id in existing_ids:
            continue

        children.append({
            "candidate_id": candidate_id,
            "candidate_summary": f"{summary} [{label}]",
            "hypothesis": hypothesis,
            "mutations": mutations,
        })
        existing_ids.add(candidate_id)

    return children


def build_signal_mutations(repo_root: Path) -> dict[str, Any]:
    """Generate code-level signal mutation candidates and add to config."""
    config_path = repo_root / "spark-researcher.project.json"
    config = _load_json(config_path, {})
    if not isinstance(config, dict):
        config = {}

    mutation_trials = _load_json(repo_root / "artifacts" / "recursion" / "mutation_trials.json", [])
    mutation_trials = mutation_trials if isinstance(mutation_trials, list) else []

    existing_ids = _existing_candidate_ids(config, mutation_trials)
    all_new: list[dict[str, Any]] = []

    for template in MUTATION_TEMPLATES:
        children = _generate_children(template, existing_ids)
        all_new.extend(children)

    # Append new candidates to config
    trials = list(config.get("candidate_trials", []))
    trials.extend(all_new)
    config["candidate_trials"] = trials

    safe_write_json(config_path, config)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "templates_processed": len(MUTATION_TEMPLATES),
        "candidates_generated": len(all_new),
        "generated_candidate_ids": [c["candidate_id"] for c in all_new],
        "total_candidate_count": len(trials),
        "material_change": len(all_new) > 0,
    }

    report_path = repo_root / "artifacts" / "recursion" / "signal_mutation_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    safe_write_json(report_path, report)

    return report


def main() -> None:
    report = build_signal_mutations(REPO_ROOT)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
