"""Transfer Learning — cross-regime and cross-asset pattern transfer.

DGM-H principle: meta-level improvements transfer across domains.
In our trading context, "domains" are market regimes and asset classes.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .population import Agent, PopulationArchive
from .performance_tracker import PerformanceTracker

ARCHIVE_ROOT = Path(__file__).resolve().parent.parent / "archive"


class TransferLearner:
    """Extract transferable patterns from successful agents."""

    def __init__(
        self,
        population: PopulationArchive,
        tracker: PerformanceTracker,
        archive_root: Path | None = None,
    ):
        self.population = population
        self.tracker = tracker
        self.root = archive_root or ARCHIVE_ROOT
        self.transfer_path = self.root / "transfer_log"
        self.transfer_path.mkdir(parents=True, exist_ok=True)

    def extract_transferable_patterns(self) -> list[dict]:
        """Identify mutation patterns that work across multiple regimes/assets.

        A pattern is "transferable" if it appears in elite agents across
        different regime or asset configurations.
        """
        elite = self.population.elite
        if len(elite) < 2:
            return []

        # Group elite by (regime, asset)
        by_context: dict[str, list[Agent]] = defaultdict(list)
        for agent in elite:
            regime = agent.mutations.get("extend_regimes", "compression")
            asset = agent.mutations.get("asset_universe", "BTC")
            context_key = f"{regime}|{asset}"
            by_context[context_key].append(agent)

        # Find guard mutations that appear in elite across different contexts
        guard_keys = [
            "cr_wick_guard", "cr_down_in_downtrend", "drawdown_guard",
            "volume_guard", "cr_loose_setup", "cr_downtrend_high_pos",
            "session_quality_filter",
        ]

        pattern_contexts: dict[str, set[str]] = defaultdict(set)
        pattern_fitness: dict[str, list[float]] = defaultdict(list)

        for context, agents in by_context.items():
            for agent in agents:
                for key in guard_keys:
                    val = agent.mutations.get(key)
                    if val:
                        pattern = f"{key}={val}"
                        pattern_contexts[pattern].add(context)
                        pattern_fitness[pattern].append(agent.win_rate)

        # A pattern is transferable if it appears in 2+ different contexts
        transferable = []
        for pattern, contexts in pattern_contexts.items():
            if len(contexts) >= 2:
                wrs = pattern_fitness[pattern]
                transferable.append({
                    "pattern": pattern,
                    "contexts": sorted(contexts),
                    "context_count": len(contexts),
                    "avg_wr": sum(wrs) / len(wrs),
                    "best_wr": max(wrs),
                    "occurrences": len(wrs),
                })

        transferable.sort(key=lambda x: x["avg_wr"], reverse=True)
        return transferable

    def suggest_transfers(self) -> list[dict]:
        """Suggest specific transfers: apply elite patterns to new contexts.

        For each elite agent, suggest applying its guard mutations to
        regimes/assets where it hasn't been tested yet.
        """
        patterns = self.extract_transferable_patterns()
        if not patterns:
            return []

        # Get all contexts that have been tested
        all_contexts = set()
        for agent in self.population.population:
            regime = agent.mutations.get("extend_regimes", "compression")
            asset = agent.mutations.get("asset_universe", "BTC")
            all_contexts.add(f"{regime}|{asset}")

        # Available untested contexts
        all_regimes = [
            "compression", "trend", "event_driven", "range",
            "trend,event_driven", "trend,event_driven,range",
        ]
        all_assets = ["BTC", "ETH", "SOL", "BTC,SOL", "BTC,ETH,SOL"]

        suggestions = []
        for pattern_info in patterns[:5]:  # Top 5 transferable patterns
            key, val = pattern_info["pattern"].split("=", 1)
            tested_contexts = pattern_info["contexts"]

            for regime in all_regimes:
                for asset in all_assets:
                    context = f"{regime}|{asset}"
                    if context not in tested_contexts:
                        suggestions.append({
                            "transfer_pattern": pattern_info["pattern"],
                            "source_contexts": tested_contexts,
                            "target_regime": regime,
                            "target_asset": asset,
                            "expected_wr": pattern_info["avg_wr"],
                            "confidence": min(1.0, pattern_info["occurrences"] / 10),
                        })

        # Sort by expected WR * confidence
        suggestions.sort(
            key=lambda x: x["expected_wr"] * x["confidence"],
            reverse=True,
        )

        return suggestions[:20]  # Top 20 suggestions

    def log_transfer_result(
        self,
        pattern: str,
        source_context: str,
        target_context: str,
        source_wr: float,
        target_wr: float,
    ) -> None:
        """Log a transfer attempt result for meta-learning."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pattern": pattern,
            "source_context": source_context,
            "target_context": target_context,
            "source_wr": source_wr,
            "target_wr": target_wr,
            "transfer_success": target_wr >= source_wr * 0.9,  # within 90%
            "wr_delta": target_wr - source_wr,
        }
        log_path = self.transfer_path / "transfer_results.jsonl"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def transfer_effectiveness(self) -> dict:
        """Analyze how well patterns transfer across contexts."""
        log_path = self.transfer_path / "transfer_results.jsonl"
        if not log_path.exists():
            return {}

        by_pattern: dict[str, list[dict]] = defaultdict(list)
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                by_pattern[entry["pattern"]].append(entry)

        result = {}
        for pattern, entries in by_pattern.items():
            successes = [e for e in entries if e["transfer_success"]]
            deltas = [e["wr_delta"] for e in entries]
            result[pattern] = {
                "attempts": len(entries),
                "successes": len(successes),
                "transfer_rate": len(successes) / max(1, len(entries)),
                "avg_wr_delta": sum(deltas) / len(deltas) if deltas else 0,
            }

        return result
