#!/usr/bin/env python3
"""Run the DGM-H evolution engine for trading strategies.

Usage:
    # Seed from existing candidates and run 5 generations
    python run_evolution.py --seed --generations 5

    # Continue evolution from last checkpoint
    python run_evolution.py --generations 10

    # View current status
    python run_evolution.py --status

    # Run with custom population size
    python run_evolution.py --generations 5 --population-size 30 --children 15
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Ensure hyperagent package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass  # dotenv not installed, rely on shell env vars

from hyperagent.evolution_engine import EvolutionEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("evolution")


def main():
    parser = argparse.ArgumentParser(
        description="DGM-H Evolution Engine for Trading Strategies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Inspired by Hyperagents (DGM-H): https://arxiv.org/abs/2603.19461

The evolution engine applies population-based self-improvement to
trading strategy mutation discovery. Instead of manually designing
mutations, the meta-agent generates, evaluates, and evolves mutation
strategies — and can modify its own improvement mechanisms.

Examples:
    # First run: seed from existing candidates
    python run_evolution.py --seed --generations 3

    # Continue evolving
    python run_evolution.py --generations 10

    # Check what the system has learned
    python run_evolution.py --status
        """,
    )

    parser.add_argument(
        "--generations", "-g",
        type=int, default=1,
        help="Number of evolution generations to run (default: 1)",
    )
    parser.add_argument(
        "--population-size", "-p",
        type=int, default=20,
        help="Maximum population size (default: 20)",
    )
    parser.add_argument(
        "--children", "-c",
        type=int, default=10,
        help="Children to generate per generation (default: 10)",
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Seed population from existing spark-researcher candidates",
    )
    parser.add_argument(
        "--seed-champions",
        action="store_true",
        help="Seed with known champion WF=1.0 agents",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current evolution status and exit",
    )
    parser.add_argument(
        "--no-staged-eval",
        action="store_true",
        help="Disable staged evaluation (run full backtest for every candidate)",
    )
    parser.add_argument(
        "--workers", "-w",
        type=int, default=1,
        help="Number of parallel workers for evaluation (default: 1 = sequential)",
    )
    parser.add_argument(
        "--trading-root",
        type=Path,
        default=None,
        help="Override path to domain-chip-crypto-trading",
    )
    parser.add_argument(
        "--archive-root",
        type=Path,
        default=None,
        help="Override archive directory (for parallel tracks)",
    )

    args = parser.parse_args()

    # Initialize engine
    engine = EvolutionEngine(
        population_size=args.population_size,
        children_per_generation=args.children,
        trading_root=args.trading_root,
        archive_root=args.archive_root,
        use_staged_eval=not args.no_staged_eval,
        max_workers=args.workers,
    )

    # Status mode
    if args.status:
        status = engine.status()
        print(json.dumps(status, indent=2, default=str))
        return

    # Seed modes
    if args.seed:
        count = engine.seed_from_existing()
        print(f"Seeded {count} agents from existing candidates")

    if args.seed_champions:
        count = engine.seed_champion_family()
        print(f"Seeded {count} champion agents")

    # If population is empty after seeding, seed champions by default
    if not engine.population.population:
        logger.info("Empty population, seeding champion family...")
        engine.seed_champion_family()

    # Run evolution
    if args.generations > 0:
        print(f"\nStarting evolution: {args.generations} generations")
        print(f"Population size: {args.population_size}")
        print(f"Children per generation: {args.children}")
        print(f"Staged evaluation: {'ON (quick>medium>full)' if engine.use_staged_eval else 'OFF (full only)'}")
        print(f"Workers: {args.workers} ({'parallel' if args.workers > 1 else 'sequential'})")
        print(f"Trading chip: {engine.trading_root}")
        print()

        reports = engine.run(args.generations)

        # Final summary
        final = engine.status()
        pop = final["population"]
        print(f"\n{'='*60}")
        print(f"  EVOLUTION COMPLETE")
        print(f"{'='*60}")
        print(f"  Generations: {final['generation']}")
        print(f"  Population: {pop.get('size', 0)} agents")
        print(f"  Elite: {pop.get('elite', 0)}")
        print(f"  Viable: {pop.get('viable', 0)}")
        print(f"  Best WR: {pop.get('best_wr', 0):.3f}")
        print(f"  Total tested: {pop.get('total_tested', 0)}")
        print(f"  Dead ends found: {len(final.get('dead_ends', []))}")

        best_strats = final.get("best_strategies", [])
        if best_strats:
            print(f"  Best meta-strategies: {', '.join(best_strats)}")

        print(f"{'='*60}")


if __name__ == "__main__":
    main()
