#!/usr/bin/env python3
"""CLI entry point for the population-based evolution engine.

Runs DGM-H-inspired evolution of trading strategies using staged evaluation,
meta-strategy self-modification, and population-based search.

Usage:
    # Run 10 generations with 4 parallel workers
    python scripts/run_evolution.py -g 10 -w 4

    # Quick test (1 gen, sequential, verbose)
    python scripts/run_evolution.py -g 1 -v

    # Seed from proven agents first, then evolve
    python scripts/run_evolution.py --seed -g 20 -w 4

    # Check current evolution status
    python scripts/run_evolution.py --status
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Ensure repo root is on sys.path for imports
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from domain_chip_crypto_trading.evolution.engine import EvolutionEngine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Population-based evolution of trading strategies",
    )
    parser.add_argument(
        "-g", "--generations", type=int, default=10,
        help="Number of generations to run (default: 10)",
    )
    parser.add_argument(
        "-p", "--population-size", type=int, default=20,
        help="Max population size (default: 20)",
    )
    parser.add_argument(
        "-c", "--children", type=int, default=10,
        help="Candidates per generation (default: 10)",
    )
    parser.add_argument(
        "-w", "--workers", type=int, default=1,
        help="Parallel eval workers (default: 1 = sequential)",
    )
    parser.add_argument(
        "--no-staged", action="store_true",
        help="Disable staged evaluation (run full backtest on every candidate)",
    )
    parser.add_argument(
        "--seed", action="store_true",
        help="Seed population from candidate_trials + pro_gen before evolving",
    )
    parser.add_argument(
        "--seed-only", action="store_true",
        help="Only seed population (no evolution)",
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Print current evolution status and exit",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    engine = EvolutionEngine(
        population_size=args.population_size,
        children_per_generation=args.children,
        use_staged_eval=not args.no_staged,
        max_workers=args.workers,
    )

    # -- Status mode --
    if args.status:
        status = engine.status()
        print(json.dumps(status, indent=2, default=str))
        return

    # -- Seed mode --
    if args.seed or args.seed_only:
        print("Seeding population from existing agents...")
        n1 = engine.seed_from_existing()
        n2 = engine.seed_from_pro_gen()
        print(f"  Seeded {n1} from candidate_trials, {n2} from pro_gen")
        pop = engine.population.summary()
        print(f"  Population: {pop.get('size', 0)} agents ({pop.get('elite', 0)} elite, {pop.get('viable', 0)} viable)")
        if args.seed_only:
            return

    # -- Evolution mode --
    print(f"\nStarting evolution: {args.generations} generations, "
          f"{args.children} candidates/gen, {args.workers} workers, "
          f"staged={'off' if args.no_staged else 'on'}")
    print(f"Population cap: {args.population_size}")
    print()

    reports = engine.run(generations=args.generations)

    # -- Summary --
    if reports:
        last = reports[-1]
        pop = last.get("population", {})
        best = last.get("best_agent")
        total_improvements = sum(r["improvements"] for r in reports)
        total_candidates = sum(r["candidates"] for r in reports)
        total_duration = sum(r.get("duration_seconds", 0) for r in reports)

        print(f"\n{'='*60}")
        print(f"Evolution Complete: {len(reports)} generations")
        print(f"{'='*60}")
        print(f"  Total candidates: {total_candidates}")
        print(f"  Total improvements: {total_improvements} ({total_improvements/max(1,total_candidates):.0%})")
        print(f"  Final population: {pop.get('size', 0)} (elite={pop.get('elite', 0)}, viable={pop.get('viable', 0)})")
        if best:
            print(f"  Best agent: WR={best.get('fitness', {}).get('win_rate', 0):.3f} | {best.get('mutations', {}).get('strategy_id', '?')}")
        print(f"  Total duration: {total_duration:.0f}s ({total_duration/60:.1f}min)")
        print()


if __name__ == "__main__":
    main()
