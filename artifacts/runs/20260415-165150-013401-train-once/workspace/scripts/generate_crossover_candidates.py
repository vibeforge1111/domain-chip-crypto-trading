"""Generate crossover candidates by combining elite + mediocre parents.

Ports evolution's crossover logic (meta_agent.py) into the main trading repo.
Produces new candidate_trials entries that blend guard patterns from different
strategy families — the most effective meta-strategy (61.3% improvement rate).

Usage:
    python scripts/generate_crossover_candidates.py
    python scripts/generate_crossover_candidates.py --count 30
    python scripts/generate_crossover_candidates.py --dry-run
    python scripts/generate_crossover_candidates.py --include-mediocre --count 10
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Any

# ── Paths ────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parent.parent
CHAMPIONS_PATH = REPO / "artifacts" / "forge" / "proven_champions.json"
PROJECT_PATH = REPO / "spark-researcher.project.json"
BACKTEST_PATH = REPO / "artifacts" / "backtests" / "heavy_backtest_summary.json"

# ── Constants ────────────────────────────────────────────────────
REGIME_SETS = [
    "",
    "trend",
    "event_driven",
    "range",
    "trend,event_driven",
    "trend,event_driven,range",
    "trend,event_driven,range,high_vol,fear_shock",
]

METADATA_KEYS = {"source", "candidate_summary", "hypothesis", "family"}

# ── Import safe_write_json ───────────────────────────────────────
sys.path.insert(0, str(REPO / "scripts"))
from safe_write import safe_write_json  # noqa: E402


# ── Helpers ──────────────────────────────────────────────────────

def normalize_candidate_id(cid: str) -> str:
    """Normalize candidate ID for deduplication: lowercase, underscores to dashes."""
    return cid.replace("_", "-").lower().strip()


def short_id(candidate_id: str, max_len: int = 16) -> str:
    """Extract a short label from a candidate_id for the crossover name."""
    parts = candidate_id.split("-")
    # Take meaningful middle parts, skip generic prefixes
    meaningful = [p for p in parts if p not in ("compression", "bounce", "auto", "15m")]
    label = "-".join(meaningful[:3])
    return label[:max_len]


def mutations_hash(mutations: dict[str, Any]) -> str:
    """SHA256 of deterministically-serialized mutation dict."""
    # Sort keys, exclude metadata
    clean = {k: v for k, v in sorted(mutations.items()) if k not in METADATA_KEYS}
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()[:8]


def mutations_fingerprint(mutations: dict[str, Any]) -> str:
    """Full hash for exact deduplication (no truncation)."""
    clean = {k: v for k, v in sorted(mutations.items()) if k not in METADATA_KEYS}
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()


# ── Data Loading ─────────────────────────────────────────────────

def load_champions() -> list[dict[str, Any]]:
    """Load elite parents from proven_champions.json."""
    if not CHAMPIONS_PATH.exists():
        print(f"ERROR: Champions file not found: {CHAMPIONS_PATH}")
        sys.exit(1)
    data = json.loads(CHAMPIONS_PATH.read_text(encoding="utf-8"))
    champions = data.get("champions", [])
    if not champions:
        print("ERROR: No champions found in proven_champions.json")
        sys.exit(1)
    # Filter to only those with mutations
    valid = [c for c in champions if c.get("mutations")]
    print(f"  Loaded {len(valid)} elite parents from proven_champions.json")
    return valid


def load_backtest_index() -> dict[str, dict[str, Any]]:
    """Load heavy_backtest_summary.json into a lookup by normalized candidate_id.

    Returns dict mapping normalized_id -> {win_rate, trade_count, walk_forward_consistency}.
    """
    if not BACKTEST_PATH.exists():
        print(f"WARNING: Backtest summary not found: {BACKTEST_PATH}")
        return {}
    data = json.loads(BACKTEST_PATH.read_text(encoding="utf-8"))
    rows = data.get("rows", [])
    index: dict[str, dict[str, Any]] = {}
    for row in rows:
        cid = normalize_candidate_id(row.get("candidate_id", ""))
        metrics = row.get("metrics", {})
        result = row.get("result", {})
        index[cid] = {
            "win_rate": metrics.get("win_rate", 0.0),
            "trade_count": result.get("trade_count", 0),
            "walk_forward_consistency": result.get("walk_forward_consistency", 0.0),
        }
    return index


def load_project() -> dict[str, Any]:
    """Load spark-researcher.project.json."""
    if not PROJECT_PATH.exists():
        print(f"ERROR: Project file not found: {PROJECT_PATH}")
        sys.exit(1)
    return json.loads(PROJECT_PATH.read_text(encoding="utf-8"))


def load_mediocre_parents(
    include_below_55: bool = False,
) -> list[dict[str, Any]]:
    """Select mediocre parents by cross-referencing project.json with backtest results.

    Default: WR >= 0.55 and WR < 0.60 and trade_count >= 100.
    With --include-mediocre: WR >= 0.50.
    """
    project = load_project()
    candidates = project.get("candidate_trials", [])
    bt_index = load_backtest_index()

    wr_floor = 0.50 if include_below_55 else 0.55
    mediocre: list[dict[str, Any]] = []

    for c in candidates:
        cid = normalize_candidate_id(c.get("candidate_id", ""))
        bt = bt_index.get(cid)
        if bt is None:
            continue
        wr = bt["win_rate"]
        tc = bt["trade_count"]
        if wr_floor <= wr < 0.60 and tc >= 100:
            mediocre.append(c)

    print(f"  Loaded {len(mediocre)} mediocre parents (WR [{wr_floor:.2f}, 0.60), trades >= 100)")
    return mediocre


# ── Crossover Engine ─────────────────────────────────────────────

def strategy_counts_from_pool(pool: list[dict[str, Any]]) -> Counter:
    """Count strategy_id occurrences across a pool of parents."""
    return Counter(
        p.get("mutations", {}).get("strategy_id", "unknown")
        for p in pool
    )


def pick_minority_parent(
    pool: list[dict[str, Any]],
    counts: Counter,
) -> dict[str, Any] | None:
    """Pick a parent whose strategy_id is the LEAST common in the pool."""
    if not pool or not counts:
        return None
    # Sorted from least to most common
    least_common_strategies = [s for s, _ in counts.most_common()[::-1]]
    # Gather candidates from the rarest strategy
    for strategy in least_common_strategies:
        minority_pool = [
            p for p in pool
            if p.get("mutations", {}).get("strategy_id", "") == strategy
        ]
        if minority_pool:
            return random.choice(minority_pool)
    return random.choice(pool)


def crossover(
    parent1: dict[str, Any],
    parent2: dict[str, Any],
    population_counts: Counter,
) -> dict[str, Any]:
    """Combine mutations from two parents.

    For each mutation key in union(p1, p2):
        - 50/50 pick from either parent
    Strategy-lock: when parents have different strategy_id, child keeps
    the MINORITY parent's strategy_id and doctrine_id.
    """
    p1_mut = parent1.get("mutations", {})
    p2_mut = parent2.get("mutations", {})

    all_keys = set(p1_mut.keys()) | set(p2_mut.keys())
    child: dict[str, Any] = {}

    for key in all_keys:
        if key in METADATA_KEYS:
            continue
        if random.random() < 0.5:
            child[key] = p2_mut.get(key, p1_mut.get(key))
        else:
            child[key] = p1_mut.get(key, p2_mut.get(key))

    # Strategy-lock: minority parent's identity wins
    s1 = p1_mut.get("strategy_id", "")
    s2 = p2_mut.get("strategy_id", "")
    if s1 != s2:
        c1 = population_counts.get(s1, 0)
        c2 = population_counts.get(s2, 0)
        minority_mut = p2_mut if c2 <= c1 else p1_mut
        child["strategy_id"] = minority_mut.get("strategy_id", child.get("strategy_id", ""))
        if "doctrine_id" in minority_mut:
            child["doctrine_id"] = minority_mut["doctrine_id"]

    return child


def generate_candidate_id(
    p1_id: str,
    p2_id: str,
    child_mutations: dict[str, Any],
) -> str:
    """Build candidate ID: xover-{p1_short}-{p2_short}-{hash[:8]}."""
    s1 = short_id(p1_id)
    s2 = short_id(p2_id)
    h = mutations_hash(child_mutations)
    return f"xover-{s1}-{s2}-{h}"


def build_existing_fingerprints(project: dict[str, Any]) -> set[str]:
    """Build a set of mutation fingerprints + normalized IDs for dedup."""
    fingerprints: set[str] = set()
    normalized_ids: set[str] = set()
    for c in project.get("candidate_trials", []):
        cid = normalize_candidate_id(c.get("candidate_id", ""))
        normalized_ids.add(cid)
        muts = c.get("mutations", {})
        if muts:
            fingerprints.add(mutations_fingerprint(muts))
    return fingerprints, normalized_ids


# ── Main ─────────────────────────────────────────────────────────

def run(
    count: int = 20,
    dry_run: bool = False,
    include_mediocre: bool = False,
) -> list[dict[str, Any]]:
    """Generate crossover candidates and optionally write to project.json."""
    print("=== Crossover Candidate Generator ===\n")

    # 1. Load parents
    champions = load_champions()
    mediocre = load_mediocre_parents(include_below_55=include_mediocre)

    # Build combined pool for parent2 selection
    # Elite parents are always in the pool; mediocre are added as parent2 sources
    elite_pool = champions
    parent2_pool = list(champions) + mediocre
    if not parent2_pool:
        print("ERROR: No parent2 candidates available.")
        sys.exit(1)

    # 2. Strategy counts across entire current population (for minority logic)
    project = load_project()
    all_candidates = project.get("candidate_trials", [])
    population_counts = Counter(
        c.get("mutations", {}).get("strategy_id", "unknown")
        for c in all_candidates
        if c.get("mutations")
    )
    # Also count champions in the population view
    for ch in champions:
        sid = ch.get("mutations", {}).get("strategy_id", "unknown")
        population_counts[sid] = population_counts.get(sid, 0)

    print(f"\n  Strategy distribution in population:")
    for strat, cnt in population_counts.most_common(10):
        print(f"    {strat}: {cnt}")

    # 3. Build dedup index
    fingerprints, existing_ids = build_existing_fingerprints(project)
    print(f"\n  Existing candidates: {len(existing_ids)}")
    print(f"  Existing fingerprints: {len(fingerprints)}")

    # 4. Generate crossovers
    children: list[dict[str, Any]] = []
    attempts = 0
    max_attempts = count * 10  # allow generous retries for dedup

    while len(children) < count and attempts < max_attempts:
        attempts += 1

        # Pick parent1 (always elite)
        p1 = random.choice(elite_pool)

        # 65% of crossovers force parent2 from minority strategy
        if random.random() < 0.65:
            p2 = pick_minority_parent(parent2_pool, population_counts)
            if p2 is None:
                p2 = random.choice(parent2_pool)
        else:
            # Pick a different parent from the full pool
            candidates = [p for p in parent2_pool
                          if p.get("candidate_id", "") != p1.get("candidate_id", "")
                          and p.get("champion_id", "") != p1.get("champion_id", "")]
            if not candidates:
                candidates = parent2_pool
            p2 = random.choice(candidates)

        # Perform crossover
        child_mutations = crossover(p1, p2, population_counts)

        # Check for exact mutation duplicate
        fp = mutations_fingerprint(child_mutations)
        if fp in fingerprints:
            continue

        # Build candidate ID
        p1_id = p1.get("champion_id") or p1.get("candidate_id", "unknown")
        p2_id = p2.get("champion_id") or p2.get("candidate_id", "unknown")
        candidate_id = generate_candidate_id(p1_id, p2_id, child_mutations)

        # Check for ID collision
        norm_id = normalize_candidate_id(candidate_id)
        if norm_id in existing_ids:
            continue

        # Register in dedup sets
        fingerprints.add(fp)
        existing_ids.add(norm_id)

        child_entry = {
            "candidate_id": candidate_id,
            "candidate_summary": f"Crossover of {p1_id} x {p2_id}",
            "hypothesis": (
                "Crossover combines guard patterns from different strategy families "
                "(61.3% improvement rate in evolution)"
            ),
            "mutations": child_mutations,
        }
        children.append(child_entry)

    print(f"\n  Generated {len(children)} crossover candidates in {attempts} attempts")

    if not children:
        print("WARNING: No new unique candidates could be generated.")
        return []

    # 5. Report
    print("\n--- Generated Candidates ---")
    child_strat_counts = Counter()
    for i, child in enumerate(children, 1):
        sid = child["mutations"].get("strategy_id", "?")
        child_strat_counts[sid] += 1
        p_summary = child["candidate_summary"]
        print(f"  [{i:2d}] {child['candidate_id']}")
        print(f"       {p_summary}")
        print(f"       strategy_id={sid}")
        guard_keys = [k for k in child["mutations"] if k.startswith("cr_")]
        if guard_keys:
            print(f"       guards: {', '.join(guard_keys)}")

    print("\n  Strategy distribution in children:")
    for strat, cnt in child_strat_counts.most_common():
        print(f"    {strat}: {cnt}")

    # 6. Write (unless dry-run)
    if dry_run:
        print("\n  [DRY RUN] Not writing to project.json")
    else:
        project["candidate_trials"].extend(children)
        safe_write_json(PROJECT_PATH, project)
        total = len(project["candidate_trials"])
        print(f"\n  Wrote {len(children)} new candidates to project.json (total: {total})")

    return children


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate crossover candidates from elite + mediocre parents.",
    )
    parser.add_argument(
        "--count", type=int, default=20,
        help="Number of crossover children to generate (default: 20)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print candidates without writing to project.json",
    )
    parser.add_argument(
        "--include-mediocre", action="store_true",
        help="Also use WR 0.50-0.55 candidates as parent2 (default: only WR >= 0.55)",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducibility",
    )
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    run(
        count=args.count,
        dry_run=args.dry_run,
        include_mediocre=args.include_mediocre,
    )


if __name__ == "__main__":
    main()
