"""Generate targeted mutations for mediocre candidates based on research findings.

Three mutation types:
1. Regime Extension  — expand regime coverage for single-regime candidates
2. Threshold Relaxation — loosen tight parameters that may be over-filtering
3. Guard Removal Ablation — remove each guard to test whether it helps or hurts

Reads:
  - spark-researcher.project.json  (candidate_trials)
  - artifacts/backtests/heavy_backtest_summary.json  (rows, for backtest metrics)

Writes:
  - Updated spark-researcher.project.json  (appended candidates)
  - artifacts/targeted_mutations/targeted_mutations_report.json  (run log)

Usage:
  python scripts/generate_targeted_mutations.py
  python scripts/generate_targeted_mutations.py --dry-run
  python scripts/generate_targeted_mutations.py --type regime_extension
  python scripts/generate_targeted_mutations.py --type guard_ablation --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from safe_write import safe_write_json  # noqa: E402

# ── Paths ───────────────────────────────────────────────────────────
CONFIG_PATH = REPO_ROOT / "spark-researcher.project.json"
SUMMARY_PATH = REPO_ROOT / "artifacts" / "backtests" / "heavy_backtest_summary.json"
OUTPUT_DIR = REPO_ROOT / "artifacts" / "targeted_mutations"

# ── Regime Extension Targets ────────────────────────────────────────
# Each entry: (strategy_id, current_market_regime, new_extend_regimes)
# "current_market_regime" is used to match existing candidates that are
# limited to that regime.  Empty string matches candidates with blank/missing
# market_regime.
REGIME_EXTENSION_TARGETS: list[dict[str, str]] = [
    {
        "strategy_id": "momentum_zscore_reversal",
        "current_regime": "trend",
        "new_extend_regimes": "trend,event_driven,high_vol",
    },
    {
        "strategy_id": "rsi_extreme_reversion",
        "current_regime": "",
        "new_extend_regimes": "compression,high_vol",
    },
    {
        "strategy_id": "vwap_reversion",
        "current_regime": "event_driven",
        "new_extend_regimes": "event_driven,range",
    },
    {
        "strategy_id": "intermarket_context_gate",
        "current_regime": "event_driven",
        "new_extend_regimes": "event_driven,trend",
    },
    {
        "strategy_id": "ou_adaptive_entry",
        "current_regime": "compression",
        "new_extend_regimes": "compression,range,event_driven",
    },
]

# ── Threshold Relaxation Targets ────────────────────────────────────
# Each entry: (strategy_id, parameter_key, current_value, relaxed_value)
THRESHOLD_RELAXATION_TARGETS: list[dict[str, str]] = [
    {
        "strategy_id": "ou_adaptive_entry",
        "param_key": "ou_halflife_cap",
        "current_value": "standard",
        "relaxed_value": "relaxed",
    },
    {
        "strategy_id": "ou_adaptive_entry",
        "param_key": "ou_hurst_gate",
        "current_value": "on",
        "relaxed_value": "off",
    },
]

# ── Guard key patterns for ablation ────────────────────────────────
GUARD_KEY_SUFFIXES = ("_guard", "_filter")


# ════════════════════════════════════════════════════════════════════
# Helpers
# ════════════════════════════════════════════════════════════════════

def _load_json(path: Path, fallback: Any = None) -> Any:
    """Load JSON with safe fallback."""
    if fallback is None:
        fallback = {}
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return fallback


def _normalize_candidate_id(cid: str) -> str:
    """Normalize candidate ID for dedup: underscore -> hyphen, lowercase."""
    return cid.replace("_", "-").lower().strip()


def _existing_candidate_ids(config: dict[str, Any]) -> set[str]:
    """Collect all existing candidate IDs (normalized) from project config."""
    ids: set[str] = set()
    for trial in config.get("candidate_trials", []):
        if isinstance(trial, dict):
            cid = str(trial.get("candidate_id", "")).strip()
            if cid:
                ids.add(_normalize_candidate_id(cid))
    return ids


def _short_hash(payload: str, length: int = 6) -> str:
    """Return a short hex hash of the payload string."""
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:length]


def _make_candidate_id(mutation_type: str, base_id: str, distinguisher: str) -> str:
    """Build candidate ID: mut-{type}-{base_short}-{hash[:6]}."""
    # Shorten base_id to keep overall length reasonable
    base_short = base_id[:40] if len(base_id) > 40 else base_id
    raw = f"{mutation_type}|{base_id}|{distinguisher}"
    h = _short_hash(raw)
    return f"mut-{mutation_type}-{base_short}-{h}"


def _is_guard_key(key: str) -> bool:
    """Check if a mutation key looks like a guard/filter key."""
    return any(key.endswith(suffix) for suffix in GUARD_KEY_SUFFIXES)


def _build_summary_index(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index heavy backtest rows by candidate_id for quick lookup."""
    index: dict[str, dict[str, Any]] = {}
    rows = summary.get("rows", [])
    if not isinstance(rows, list):
        return index
    for row in rows:
        if not isinstance(row, dict):
            continue
        cid = str(row.get("candidate_id", "")).strip()
        if cid:
            index[cid] = row
    return index


# ════════════════════════════════════════════════════════════════════
# Mutation generators
# ════════════════════════════════════════════════════════════════════

def _generate_regime_extensions(
    trials: list[dict[str, Any]],
    existing_ids: set[str],
    summary_index: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Generate regime extension mutations."""
    new_candidates: list[dict[str, Any]] = []

    for target in REGIME_EXTENSION_TARGETS:
        target_strategy = target["strategy_id"]
        target_regime = target["current_regime"]
        new_regimes = target["new_extend_regimes"]

        # Find matching base candidates
        for trial in trials:
            if not isinstance(trial, dict):
                continue
            mutations = trial.get("mutations", {})
            if not isinstance(mutations, dict):
                continue

            strategy_id = mutations.get("strategy_id", "")
            if strategy_id != target_strategy:
                continue

            # Match on current regime: check both market_regime and extend_regimes
            market_regime = mutations.get("market_regime", "")
            extend_regimes = mutations.get("extend_regimes", "")

            # For blank current_regime targets, match candidates with no extend_regimes
            # or with market_regime matching compression (default)
            if target_regime == "":
                # Match candidates that have no extend_regimes set, or have
                # only compression/blank market_regime
                if extend_regimes and extend_regimes != market_regime:
                    continue
            else:
                # Match candidates whose primary regime matches the target
                if market_regime != target_regime:
                    continue
                # Skip candidates that already cover the target regimes
                if extend_regimes:
                    existing_regime_set = set(r.strip() for r in extend_regimes.split(","))
                    new_regime_set = set(r.strip() for r in new_regimes.split(","))
                    if new_regime_set.issubset(existing_regime_set):
                        continue

            base_id = str(trial.get("candidate_id", ""))
            distinguisher = f"extend-{new_regimes.replace(',', '-')}"
            candidate_id = _make_candidate_id("regime", base_id, distinguisher)

            if _normalize_candidate_id(candidate_id) in existing_ids:
                continue

            # Build new mutations
            new_mutations = dict(mutations)
            new_mutations["extend_regimes"] = new_regimes
            # Update market_regime to first regime in the list (primary)
            primary_regime = new_regimes.split(",")[0].strip()
            if not new_mutations.get("market_regime"):
                new_mutations["market_regime"] = primary_regime

            # Pull backtest metrics for hypothesis context if available
            bt_row = summary_index.get(base_id, {})
            bt_metrics = bt_row.get("metrics", {})
            wr_str = f"WR={bt_metrics.get('win_rate', '?')}" if bt_metrics else "no backtest"

            new_candidates.append({
                "candidate_id": candidate_id,
                "candidate_summary": f"Targeted regime extension on {base_id}",
                "hypothesis": (
                    f"Extending {target_strategy} from {target_regime or 'default'} regime "
                    f"to [{new_regimes}]. Base candidate ({wr_str}) may improve with broader "
                    f"regime coverage — universal mean reversion works across regimes."
                ),
                "mutations": new_mutations,
            })
            existing_ids.add(_normalize_candidate_id(candidate_id))

            # Only produce one mutation per target+base pair (use first match)
            break

    return new_candidates


def _generate_threshold_relaxations(
    trials: list[dict[str, Any]],
    existing_ids: set[str],
    summary_index: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Generate threshold relaxation mutations."""
    new_candidates: list[dict[str, Any]] = []

    for target in THRESHOLD_RELAXATION_TARGETS:
        target_strategy = target["strategy_id"]
        param_key = target["param_key"]
        current_value = target["current_value"]
        relaxed_value = target["relaxed_value"]

        for trial in trials:
            if not isinstance(trial, dict):
                continue
            mutations = trial.get("mutations", {})
            if not isinstance(mutations, dict):
                continue

            strategy_id = mutations.get("strategy_id", "")
            if strategy_id != target_strategy:
                continue

            # Only target candidates that currently have the tight value
            if mutations.get(param_key) != current_value:
                continue

            base_id = str(trial.get("candidate_id", ""))
            distinguisher = f"{param_key}={relaxed_value}"
            candidate_id = _make_candidate_id("relax", base_id, distinguisher)

            if _normalize_candidate_id(candidate_id) in existing_ids:
                continue

            new_mutations = dict(mutations)
            new_mutations[param_key] = relaxed_value

            bt_row = summary_index.get(base_id, {})
            bt_metrics = bt_row.get("metrics", {})
            wr_str = f"WR={bt_metrics.get('win_rate', '?')}" if bt_metrics else "no backtest"

            new_candidates.append({
                "candidate_id": candidate_id,
                "candidate_summary": f"Targeted threshold relaxation on {base_id}",
                "hypothesis": (
                    f"Relaxing {param_key} from '{current_value}' to '{relaxed_value}' "
                    f"on {base_id} ({wr_str}). Tight parameters may be over-filtering, "
                    f"removing valid trades that could improve WF and trade count."
                ),
                "mutations": new_mutations,
            })
            existing_ids.add(_normalize_candidate_id(candidate_id))

    return new_candidates


def _generate_guard_ablations(
    trials: list[dict[str, Any]],
    existing_ids: set[str],
    summary_index: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Generate guard removal ablation mutations.

    For each candidate that has guard/filter keys, produce a variant with
    each guard removed.  This tests whether each guard is actually helping.
    """
    new_candidates: list[dict[str, Any]] = []

    for trial in trials:
        if not isinstance(trial, dict):
            continue
        mutations = trial.get("mutations", {})
        if not isinstance(mutations, dict):
            continue

        # Find all guard keys in this candidate's mutations
        guard_keys = [k for k in mutations if _is_guard_key(k)]
        if not guard_keys:
            continue

        base_id = str(trial.get("candidate_id", ""))
        bt_row = summary_index.get(base_id, {})
        bt_metrics = bt_row.get("metrics", {})
        wr_str = f"WR={bt_metrics.get('win_rate', '?')}" if bt_metrics else "no backtest"

        for guard_key in guard_keys:
            guard_value = mutations[guard_key]

            # Skip guards that are already "off" or empty — no point ablating
            if str(guard_value).lower() in ("off", "", "none", "disabled"):
                continue

            distinguisher = f"remove-{guard_key}"
            candidate_id = _make_candidate_id("ablate", base_id, distinguisher)

            if _normalize_candidate_id(candidate_id) in existing_ids:
                continue

            # Copy mutations WITHOUT the guard key
            new_mutations = {k: v for k, v in mutations.items() if k != guard_key}

            new_candidates.append({
                "candidate_id": candidate_id,
                "candidate_summary": f"Targeted guard ablation on {base_id}: remove {guard_key}",
                "hypothesis": (
                    f"Removing {guard_key}='{guard_value}' from {base_id} ({wr_str}). "
                    f"If this guard is hurting more than helping, removal should increase "
                    f"trade count and possibly improve WF consistency."
                ),
                "mutations": new_mutations,
            })
            existing_ids.add(_normalize_candidate_id(candidate_id))

    return new_candidates


# ════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════

def generate_targeted_mutations(
    mutation_types: list[str],
    dry_run: bool = False,
) -> dict[str, Any]:
    """Generate targeted mutations and optionally append to project config.

    Parameters
    ----------
    mutation_types : list[str]
        Which mutation types to run.  Subset of:
        ["regime_extension", "threshold_relaxation", "guard_ablation"]
    dry_run : bool
        If True, print candidates but do not write to disk.

    Returns
    -------
    dict  —  summary report
    """
    config = _load_json(CONFIG_PATH, {})
    if not isinstance(config, dict):
        config = {}
    trials = config.get("candidate_trials", [])
    if not isinstance(trials, list):
        trials = []

    summary = _load_json(SUMMARY_PATH, {})
    summary_index = _build_summary_index(summary)

    existing_ids = _existing_candidate_ids(config)
    all_new: list[dict[str, Any]] = []
    counts: dict[str, int] = {}

    if "regime_extension" in mutation_types:
        regime_candidates = _generate_regime_extensions(trials, existing_ids, summary_index)
        all_new.extend(regime_candidates)
        counts["regime_extension"] = len(regime_candidates)

    if "threshold_relaxation" in mutation_types:
        relax_candidates = _generate_threshold_relaxations(trials, existing_ids, summary_index)
        all_new.extend(relax_candidates)
        counts["threshold_relaxation"] = len(relax_candidates)

    if "guard_ablation" in mutation_types:
        ablation_candidates = _generate_guard_ablations(trials, existing_ids, summary_index)
        all_new.extend(ablation_candidates)
        counts["guard_ablation"] = len(ablation_candidates)

    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    report = {
        "generated_at": generated_at,
        "mutation_types": mutation_types,
        "dry_run": dry_run,
        "total_generated": len(all_new),
        "counts_by_type": counts,
        "existing_candidates_before": len(trials),
        "candidates": [
            {
                "candidate_id": c["candidate_id"],
                "candidate_summary": c["candidate_summary"],
                "hypothesis": c["hypothesis"],
            }
            for c in all_new
        ],
    }

    if dry_run:
        print(f"\n=== DRY RUN — {len(all_new)} targeted mutations generated ===\n")
        for c in all_new:
            print(f"  {c['candidate_id']}")
            print(f"    {c['candidate_summary']}")
            print(f"    hypothesis: {c['hypothesis'][:120]}...")
            print()
        print(json.dumps(report, indent=2, sort_keys=True))
        return report

    # Append to mutation_trials instead of researcher config
    if all_new:
        trials_path = REPO_ROOT / "artifacts" / "recursion" / "mutation_trials.json"
        trials_path.parent.mkdir(parents=True, exist_ok=True)
        existing_trials = json.loads(trials_path.read_text(encoding="utf-8")) if trials_path.exists() else []
        existing_trials = existing_trials if isinstance(existing_trials, list) else []
        existing_trials.extend(all_new)
        safe_write_json(trials_path, existing_trials)

    # Write report
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = OUTPUT_DIR / "targeted_mutations_report.json"
    safe_write_json(report_path, report)

    print(f"Generated {len(all_new)} targeted mutations:")
    for type_name, count in counts.items():
        print(f"  {type_name}: {count}")
    print(f"Total candidates now: {len(trials)}")
    if all_new:
        print(f"\nAppended to: {CONFIG_PATH}")
        print(f"Report at:   {report_path}")
    else:
        print("\nNo new mutations generated (all targets already covered or no matches).")

    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate targeted mutations for mediocre candidates based on research findings.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print mutations without writing to disk.",
    )
    parser.add_argument(
        "--type",
        choices=["regime_extension", "threshold_relaxation", "guard_ablation", "all"],
        default="all",
        dest="mutation_type",
        help="Which mutation type to generate (default: all).",
    )
    args = parser.parse_args()

    if args.mutation_type == "all":
        mutation_types = ["regime_extension", "threshold_relaxation", "guard_ablation"]
    else:
        mutation_types = [args.mutation_type]

    report = generate_targeted_mutations(mutation_types, dry_run=args.dry_run)
    if not args.dry_run:
        print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
