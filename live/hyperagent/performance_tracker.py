"""Performance Tracker — learns which meta-strategies produce improvements.

DGM-H emergent capability: the system autonomously develops performance tracking
to detect patterns in success/failure and adapt strategies accordingly.

Includes InsightSynthesizer (Gap 2): extracts machine-readable insights from
the performance log that the meta-agent uses to guide future generations.
"""

from __future__ import annotations

import json
import os
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ARCHIVE_ROOT = Path(__file__).resolve().parent.parent / "archive"


class PerformanceTracker:
    """Track meta-strategy effectiveness across generations."""

    def __init__(self, archive_root: Path | None = None):
        self.root = archive_root or ARCHIVE_ROOT
        self.meta_path = self.root / "meta_improvements"
        self.meta_path.mkdir(parents=True, exist_ok=True)
        self._log_path = self.meta_path / "performance_log.jsonl"
        self._summary_path = self.meta_path / "strategy_effectiveness.json"

    # ── Recording ──────────────────────────────────────────────

    def record_outcome(
        self,
        generation: int,
        agent_id: str,
        meta_strategy: str,
        parent_id: str | None,
        mutations: dict,
        fitness: dict,
        improved_over_parent: bool,
    ) -> None:
        """Record a single evaluation outcome for meta-learning."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "generation": generation,
            "agent_id": agent_id,
            "meta_strategy": meta_strategy,
            "parent_id": parent_id,
            "mutations": mutations,
            "fitness": fitness,
            "improved": improved_over_parent,
        }
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    # ── Analysis ───────────────────────────────────────────────

    def strategy_effectiveness(self) -> dict[str, dict]:
        """Compute improvement rate and avg fitness gain per meta-strategy.

        Returns dict like:
            {"perturbation": {"attempts": 40, "improvements": 12,
                              "improvement_rate": 0.30, "avg_fitness_gain": 0.02,
                              "best_fitness": {"wr": 0.67, ...}}, ...}
        """
        if not self._log_path.exists():
            return {}

        by_strategy: dict[str, list[dict]] = defaultdict(list)
        with open(self._log_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                by_strategy[entry["meta_strategy"]].append(entry)

        result = {}
        for strategy, entries in by_strategy.items():
            improvements = [e for e in entries if e["improved"]]
            wr_values = [
                e["fitness"].get("win_rate", 0)
                for e in entries
                if "win_rate" in e.get("fitness", {})
            ]
            result[strategy] = {
                "attempts": len(entries),
                "improvements": len(improvements),
                "improvement_rate": len(improvements) / max(1, len(entries)),
                "avg_wr": statistics.mean(wr_values) if wr_values else 0,
                "best_wr": max(wr_values) if wr_values else 0,
                "generations_active": sorted(
                    set(e["generation"] for e in entries)
                ),
            }

        # Save summary
        self._summary_path.write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        return result

    def best_strategies(self, top_n: int = 3) -> list[str]:
        """Return top-N meta-strategies by improvement rate."""
        effectiveness = self.strategy_effectiveness()
        ranked = sorted(
            effectiveness.items(),
            key=lambda x: (x[1]["improvement_rate"], x[1]["avg_wr"]),
            reverse=True,
        )
        return [name for name, _ in ranked[:top_n]]

    def dead_end_patterns(self) -> list[dict]:
        """Identify mutation patterns that consistently fail.

        Returns list of mutation key-value pairs that appear in >5 failures
        with <10% improvement rate.
        """
        if not self._log_path.exists():
            return []

        mutation_pattern_outcomes: dict[str, list[bool]] = defaultdict(list)
        with open(self._log_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                for k, v in entry.get("mutations", {}).items():
                    pattern_key = f"{k}={v}"
                    mutation_pattern_outcomes[pattern_key].append(
                        entry["improved"]
                    )

        dead_ends = []
        for pattern, outcomes in mutation_pattern_outcomes.items():
            if len(outcomes) >= 5:
                rate = sum(outcomes) / len(outcomes)
                if rate < 0.10:
                    dead_ends.append(
                        {
                            "pattern": pattern,
                            "attempts": len(outcomes),
                            "improvement_rate": rate,
                        }
                    )

        return sorted(dead_ends, key=lambda x: x["attempts"], reverse=True)

    def generation_progress(self) -> list[dict]:
        """Track fitness improvement across generations."""
        if not self._log_path.exists():
            return []

        by_gen: dict[int, list[float]] = defaultdict(list)
        with open(self._log_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                wr = entry.get("fitness", {}).get("win_rate", 0)
                by_gen[entry["generation"]].append(wr)

        return [
            {
                "generation": gen,
                "population_size": len(wrs),
                "best_wr": max(wrs),
                "avg_wr": statistics.mean(wrs),
                "median_wr": statistics.median(wrs),
            }
            for gen, wrs in sorted(by_gen.items())
        ]


class InsightSynthesizer:
    """DGM-H Persistent Memory: synthesize machine-readable insights from raw data.

    Analyzes the performance log to extract structured insights that the
    meta-agent can use to guide future variant generation. Insights have
    confidence scores and decay over time if not re-validated.
    """

    def __init__(self, tracker: PerformanceTracker):
        self.tracker = tracker
        self._insights_path = tracker.meta_path / "synthesized_insights.json"

    def _load_entries(self) -> list[dict]:
        """Load all performance log entries."""
        if not self.tracker._log_path.exists():
            return []
        entries = []
        with open(self.tracker._log_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries

    def _load_insights(self) -> list[dict]:
        """Load existing insights from disk."""
        if not self._insights_path.exists():
            return []
        return json.loads(self._insights_path.read_text(encoding="utf-8"))

    def _save_insights(self, insights: list[dict]) -> None:
        """Persist insights to disk with retry for transient OS errors."""
        import time
        text = json.dumps(insights, indent=2)
        for attempt in range(3):
            try:
                tmp = self._insights_path.with_suffix(".tmp")
                tmp.write_text(text, encoding="utf-8")
                tmp.replace(self._insights_path)
                return
            except OSError:
                if attempt < 2:
                    time.sleep(0.5)
                else:
                    raise

    def synthesize(self, current_generation: int) -> list[dict]:
        """Analyze performance log and generate/update structured insights.

        Returns list of insight dicts, each with:
          - insight: human-readable description
          - type: guard_effectiveness | strategy_pattern | dead_end | regime_insight
          - evidence: supporting data
          - confidence: 0.0-1.0
          - generation_discovered: when first found
          - last_validated: when last confirmed
          - times_validated: how many times confirmed
        """
        entries = self._load_entries()
        if len(entries) < 5:
            return self._load_insights()

        existing = {i["insight"]: i for i in self._load_insights()}
        new_insights = []

        # ── 1. Guard effectiveness insights ──────────────────
        new_insights.extend(self._analyze_guards(entries, current_generation))

        # ── 2. Strategy pattern insights ─────────────────────
        new_insights.extend(self._analyze_strategies(entries, current_generation))

        # ── 3. Regime-specific insights ──────────────────────
        new_insights.extend(self._analyze_regimes(entries, current_generation))

        # ── 4. Trade count threshold insights ────────────────
        new_insights.extend(self._analyze_trade_counts(entries, current_generation))

        # Merge with existing: update validated count, apply decay
        merged = self._merge_insights(existing, new_insights, current_generation)

        self._save_insights(merged)
        return merged

    def _analyze_guards(self, entries: list[dict], gen: int) -> list[dict]:
        """Find which guard mutations correlate with elite/viable outcomes."""
        insights = []
        guard_keys = [
            "cr_wick_guard", "cr_down_in_downtrend", "drawdown_guard",
            "volume_guard", "cr_loose_setup", "cr_downtrend_high_pos",
            "session_quality_filter",
            # Confirmation guards (expanded indicators)
            "cr_atr_guard", "cr_bb_confirm", "cr_bb_squeeze",
            "cr_vwap_confirm", "cr_stoch_confirm", "cr_obv_confirm",
            "cr_macd_confirm", "cr_rsi_2h_confirm", "cr_fib_confirm",
        ]

        for guard in guard_keys:
            with_guard = [
                e for e in entries
                if e.get("mutations", {}).get(guard)
                and e["fitness"].get("win_rate", 0) > 0
            ]
            without_guard = [
                e for e in entries
                if not e.get("mutations", {}).get(guard)
                and e["fitness"].get("win_rate", 0) > 0
            ]

            if len(with_guard) >= 3 and len(without_guard) >= 3:
                avg_with = statistics.mean(
                    [e["fitness"]["win_rate"] for e in with_guard]
                )
                avg_without = statistics.mean(
                    [e["fitness"]["win_rate"] for e in without_guard]
                )
                delta = avg_with - avg_without

                if abs(delta) > 0.02:
                    direction = "improves" if delta > 0 else "hurts"
                    confidence = min(1.0, (len(with_guard) + len(without_guard)) / 20)
                    insights.append({
                        "insight": f"Guard '{guard}' {direction} WR by {abs(delta):.3f} on average",
                        "type": "guard_effectiveness",
                        "evidence": {
                            "with_guard_avg_wr": round(avg_with, 4),
                            "without_guard_avg_wr": round(avg_without, 4),
                            "with_guard_count": len(with_guard),
                            "without_guard_count": len(without_guard),
                            "delta": round(delta, 4),
                        },
                        "confidence": round(confidence, 2),
                        "generation_discovered": gen,
                        "last_validated": gen,
                        "times_validated": 1,
                        "actionable": direction == "improves",
                    })

        return insights

    def _analyze_strategies(self, entries: list[dict], gen: int) -> list[dict]:
        """Find which meta-strategies produce the best results."""
        insights = []
        by_strategy: dict[str, list[float]] = defaultdict(list)

        for e in entries:
            wr = e.get("fitness", {}).get("win_rate", 0)
            if wr > 0:
                by_strategy[e["meta_strategy"]].append(wr)

        if len(by_strategy) >= 2:
            ranked = sorted(
                by_strategy.items(),
                key=lambda x: statistics.mean(x[1]),
                reverse=True,
            )
            best_name, best_wrs = ranked[0]
            worst_name, worst_wrs = ranked[-1]

            if len(best_wrs) >= 3:
                insights.append({
                    "insight": f"Strategy '{best_name}' produces highest avg WR ({statistics.mean(best_wrs):.3f})",
                    "type": "strategy_pattern",
                    "evidence": {
                        "strategy": best_name,
                        "avg_wr": round(statistics.mean(best_wrs), 4),
                        "sample_size": len(best_wrs),
                    },
                    "confidence": round(min(1.0, len(best_wrs) / 10), 2),
                    "generation_discovered": gen,
                    "last_validated": gen,
                    "times_validated": 1,
                    "actionable": True,
                })

            if len(worst_wrs) >= 3 and statistics.mean(worst_wrs) < 0.50:
                insights.append({
                    "insight": f"Avoid strategy '{worst_name}' — avg WR only {statistics.mean(worst_wrs):.3f}",
                    "type": "dead_end",
                    "evidence": {
                        "strategy": worst_name,
                        "avg_wr": round(statistics.mean(worst_wrs), 4),
                        "sample_size": len(worst_wrs),
                    },
                    "confidence": round(min(1.0, len(worst_wrs) / 10), 2),
                    "generation_discovered": gen,
                    "last_validated": gen,
                    "times_validated": 1,
                    "actionable": True,
                })

        return insights

    def _analyze_regimes(self, entries: list[dict], gen: int) -> list[dict]:
        """Find which regime extensions produce better results."""
        insights = []
        by_regime: dict[str, list[float]] = defaultdict(list)

        for e in entries:
            wr = e.get("fitness", {}).get("win_rate", 0)
            if wr > 0:
                regime = e.get("mutations", {}).get("extend_regimes", "compression_only")
                by_regime[regime].append(wr)

        for regime, wrs in by_regime.items():
            if len(wrs) >= 3:
                avg = statistics.mean(wrs)
                elite_count = sum(1 for w in wrs if w >= 0.58)
                if elite_count >= 2 or avg >= 0.57:
                    insights.append({
                        "insight": f"Regime '{regime}' is productive: avg WR={avg:.3f}, {elite_count} elite agents",
                        "type": "regime_insight",
                        "evidence": {
                            "regime": regime,
                            "avg_wr": round(avg, 4),
                            "elite_count": elite_count,
                            "sample_size": len(wrs),
                        },
                        "confidence": round(min(1.0, len(wrs) / 8), 2),
                        "generation_discovered": gen,
                        "last_validated": gen,
                        "times_validated": 1,
                        "actionable": True,
                    })

        return insights

    def _analyze_trade_counts(self, entries: list[dict], gen: int) -> list[dict]:
        """Find trade count thresholds that correlate with quality."""
        insights = []
        elite_entries = [
            e for e in entries
            if e.get("fitness", {}).get("elite", False)
        ]
        viable_entries = [
            e for e in entries
            if e.get("fitness", {}).get("viable", False)
            and not e.get("fitness", {}).get("elite", False)
        ]

        if len(elite_entries) >= 3:
            elite_trades = [
                e["fitness"]["trade_count"] for e in elite_entries
            ]
            min_elite_trades = min(elite_trades)
            insights.append({
                "insight": f"Elite agents have {min_elite_trades}+ trades (min observed)",
                "type": "guard_effectiveness",
                "evidence": {
                    "min_trades": min_elite_trades,
                    "avg_trades": round(statistics.mean(elite_trades), 0),
                    "elite_count": len(elite_entries),
                },
                "confidence": round(min(1.0, len(elite_entries) / 5), 2),
                "generation_discovered": gen,
                "last_validated": gen,
                "times_validated": 1,
                "actionable": True,
            })

        return insights

    def _merge_insights(
        self,
        existing: dict[str, dict],
        new_insights: list[dict],
        current_generation: int,
    ) -> list[dict]:
        """Merge new insights with existing ones. Apply validation and decay."""
        for new in new_insights:
            key = new["insight"]
            if key in existing:
                old = existing[key]
                old["times_validated"] = old.get("times_validated", 0) + 1
                old["last_validated"] = current_generation
                # Boost confidence with more validations
                old["confidence"] = min(
                    1.0, old["confidence"] + 0.05,
                )
                # Update evidence with latest data
                old["evidence"] = new["evidence"]
            else:
                existing[key] = new

        # Apply decay: insights not validated in last 10 generations lose confidence
        for key, insight in list(existing.items()):
            generations_since = current_generation - insight.get("last_validated", 0)
            if generations_since > 10:
                insight["confidence"] = max(
                    0.1, insight["confidence"] - 0.05 * (generations_since - 10),
                )
            # Remove very low confidence insights
            if insight["confidence"] < 0.1:
                del existing[key]

        return sorted(
            existing.values(),
            key=lambda x: (x["confidence"], x.get("times_validated", 0)),
            reverse=True,
        )

    def get_actionable_insights(self, min_confidence: float = 0.3) -> list[dict]:
        """Return high-confidence actionable insights for meta-agent use."""
        insights = self._load_insights()
        return [
            i for i in insights
            if i.get("actionable", False) and i["confidence"] >= min_confidence
        ]

    def format_for_meta_agent(self, max_insights: int = 10) -> str:
        """Format insights as a text prompt for the meta-agent.

        Returns a human-readable summary of what the system has learned,
        suitable for inclusion in LLM prompts or as context for generation.
        """
        insights = self.get_actionable_insights()[:max_insights]
        if not insights:
            return ""

        lines = ["## Discovered Insights (from performance analysis)"]
        for i in insights:
            conf = "HIGH" if i["confidence"] >= 0.7 else "MED" if i["confidence"] >= 0.4 else "LOW"
            lines.append(
                f"- [{conf}] {i['insight']} "
                f"(validated {i.get('times_validated', 1)}x, gen {i.get('generation_discovered', '?')})"
            )

        return "\n".join(lines)
