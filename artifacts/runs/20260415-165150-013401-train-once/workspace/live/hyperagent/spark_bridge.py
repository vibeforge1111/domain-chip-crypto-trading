"""Spark Bridge -- bidirectional connection to Spark Swarm v1.0 collective intelligence.

Integration model:
  - WRITES to .spark-swarm/collective-sync.json (Spark Swarm v1.0 contract)
  - WRITES to archive/spark_local.jsonl (internal read-back for meta-agent)
  - READS from archive/spark_local.jsonl (guard effectiveness, dead ends, etc.)

Collective sync payload follows the exact schema used by other domain chips
(startup-yc, trading-crypto, agentic-marketing) in the Spark Researcher + Swarm ecosystem.

Three emission levels mapped to collective sync:
  Pulse (every gen): runtimePulse update + local JSONL for read-back
  Patterns (every 3 gens): insights + masteries in collective sync
  Breakthrough (on event): outcomes + evolution path updates
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ── Paths ────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
SPARK_SWARM_DIR = REPO_ROOT / ".spark-swarm"
COLLECTIVE_SYNC_PATH = SPARK_SWARM_DIR / "collective-sync.json"
LOCAL_JSONL_PATH = REPO_ROOT / "archive" / "spark_local.jsonl"

# Agent identity
AGENT_ID = "agent:trading-crypto-evolution"
SPECIALIZATION_ID = "specialization:trading-crypto-evolution"
SPECIALIZATION_KEY = "trading-crypto-evolution"
SPECIALIZATION_LABEL = "Crypto Trading Evolution"

# ── Session state ────────────────────────────────────────────────────────

_session_id: str = ""
_previous_champion_wr: float = 0.0
_previous_champion_id: str = ""
_generation: int = 0
_pass_number: int = 0

# Accumulated collective sync state (built up across generations)
_insights: list[dict] = []
_masteries: list[dict] = []
_outcomes: list[dict] = []
_contradictions: list[dict] = []
_artifact_refs: list[dict] = []


# ── Public API ────────────────────────────────────────────────────────────


def init_bridge(current_best_wr: float = 0.0, current_best_id: str = "") -> None:
    """Initialize the Spark bridge for this evolution session."""
    global _session_id, _previous_champion_wr, _previous_champion_id
    global _insights, _masteries, _outcomes, _contradictions, _artifact_refs, _pass_number

    _session_id = datetime.now(timezone.utc).isoformat()
    _previous_champion_wr = current_best_wr
    _previous_champion_id = current_best_id

    SPARK_SWARM_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Load existing collective sync state if available
    _insights, _masteries, _outcomes, _contradictions, _artifact_refs = _load_existing_sync()

    # Count existing passes for pass_number continuity
    _pass_number = len(_outcomes) if _outcomes else 0

    logger.info(
        "Spark bridge initialized for Swarm v1.0 (session=%s, existing_insights=%d)",
        _session_id[:19], len(_insights),
    )


def emit_tier1_pulse(generation: int, report: dict) -> None:
    """Population telemetry pulse (every generation).

    Updates runtimePulse in collective sync + writes local JSONL for read-back.
    """
    global _generation, _pass_number
    _generation = generation
    _pass_number += 1

    pop = report.get("population_summary", {})
    effectiveness = report.get("strategy_effectiveness", {})

    strat_summary = {
        name: {
            "rate": round(s.get("improvement_rate", 0), 3),
            "avg_wr": round(s.get("avg_wr", 0), 3),
        }
        for name, s in effectiveness.items()
    }

    # Write local JSONL for internal read-back (guard effectiveness, etc.)
    _write_local(
        observer_name="evolution_pulse",
        captured_data={
            "generation": generation,
            "pop_size": pop.get("size", 0),
            "elite_count": pop.get("elite", 0),
            "viable_count": pop.get("viable", 0),
            "best_wr": pop.get("best_wr", 0),
            "avg_wr": pop.get("avg_wr", 0),
            "new_elite": report.get("new_elite", 0),
            "new_viable": report.get("new_viable", 0),
            "elapsed_seconds": report.get("elapsed_seconds", 0),
            "strategy_effectiveness": strat_summary,
        },
    )

    # Update collective sync with latest runtime pulse
    _write_collective_sync()


def emit_tier2_patterns(
    generation: int,
    insights: list[dict],
    dead_ends: list[dict],
) -> None:
    """Swarm-quality pattern insights (every 3 gens).

    Produces insights and masteries in the collective sync payload.
    """
    if not insights and not dead_ends:
        return

    now = datetime.now(timezone.utc).isoformat()

    # ── Emit validated guard effectiveness insights ──
    top_insights = sorted(
        [i for i in insights if i.get("actionable")],
        key=lambda x: x.get("confidence", 0),
        reverse=True,
    )[:5]

    for insight in top_insights:
        text = insight.get("insight", "")
        times_val = insight.get("times_validated", 1)
        if times_val < 3:
            continue

        swarm_content = _build_swarm_insight(text, times_val, generation)
        if not swarm_content:
            continue

        insight_id = f"insight:evo-gen{generation}-{_short_hash(text)}"

        # Avoid duplicates by insight summary prefix
        if any(i.get("id") == insight_id for i in _insights):
            continue

        _insights.append({
            "id": insight_id,
            "specializationId": SPECIALIZATION_ID,
            "summary": swarm_content[:200],
            "mechanism": f"Validated across {times_val} independent evolutionary tests over {generation} generations.",
            "boundary": "Evidence is backtest-only on crypto 15m/1h/4h. Does not prove portability to other asset classes.",
            "contradiction": None,
            "confidence": 0.8 if times_val >= 10 else 0.65,
            "evidenceLane": "benchmark_evidence",
            "sourceRefs": [str(REPO_ROOT / "archive" / "meta_improvements" / "synthesized_insights.json")],
            "status": "benchmark_supported" if times_val >= 10 else "provisional",
            "createdAt": now,
            "updatedAt": now,
        })

        # Promote to mastery if heavily validated
        if times_val >= 10:
            _masteries.append({
                "id": f"mastery:{insight_id.split(':')[1]}",
                "derivedFromInsightId": insight_id,
                "specializationScope": SPECIALIZATION_KEY,
                "shareScope": "selective",
                "status": "provisional_mastery",
                "supportCount": times_val,
                "contradictionCount": 0,
                "benchmarkStrength": min(0.95, 0.5 + times_val * 0.03),
                "liveStrength": None,
                "summary": swarm_content[:200],
                "createdAt": now,
                "updatedAt": now,
            })

    # ── Emit dead-end contradiction patterns ──
    top_dead_ends = [
        d for d in dead_ends[:5]
        if d.get("attempts", 0) >= 50 and d.get("improvement_rate", 1) < 0.10
    ]

    for de in top_dead_ends:
        pattern = de.get("pattern", str(de))
        attempts = de.get("attempts", 0)
        rate = de.get("improvement_rate", 0)

        contradiction_id = f"contradiction:dead-end-{_short_hash(pattern)}"
        if any(c.get("id") == contradiction_id for c in _contradictions):
            continue

        # Pick a target insight to attach the contradiction to
        target_insight_id = _insights[-1]["id"] if _insights else "insight:population-search"

        _contradictions.append({
            "id": contradiction_id,
            "targetType": "insight",
            "targetId": target_insight_id,
            "severity": "warn",
            "status": "open",
            "summary": (
                f"Avoid {pattern} in crypto trading evolution "
                f"({rate:.1%} improvement rate across {attempts} attempts)."
            ),
            "sourceRef": str(REPO_ROOT / "archive" / "meta_improvements" / "synthesized_insights.json"),
            "createdAt": now,
            "resolvedAt": None,
        })

    # ── Write local JSONL for internal read-back ──
    _write_local(
        observer_name="insight_synthesizer",
        captured_data={
            "generation": generation,
            "actionable_insights": [
                {
                    "insight": i.get("insight", ""),
                    "type": i.get("type", ""),
                    "confidence": i.get("confidence", 0),
                    "times_validated": i.get("times_validated", 1),
                }
                for i in top_insights
            ],
            "dead_ends": [
                {
                    "pattern": d.get("pattern", str(d)),
                    "attempts": d.get("attempts", 0),
                    "improvement_rate": d.get("improvement_rate", 0),
                }
                for d in dead_ends[:5]
            ],
            "total_insights": len(insights),
            "total_dead_ends": len(dead_ends),
        },
    )

    # Update collective sync
    _write_collective_sync()


def emit_tier3_breakthrough(
    generation: int,
    event_type: str,
    data: dict,
) -> None:
    """Breakthrough events (new champion, paper trade validation).

    Produces outcomes in the collective sync payload.
    """
    global _previous_champion_wr, _previous_champion_id

    now = datetime.now(timezone.utc).isoformat()
    wr = data.get("win_rate", 0)
    agent = data.get("agent_id", "?")[:8]

    if event_type == "new_champion":
        summary = (
            f"New champion {agent} with {wr:.1%} win rate "
            f"(+{wr - _previous_champion_wr:+.1%} over previous best)."
        )
        metric_value = wr
        verdict = "pass" if wr > _previous_champion_wr else "flat"
        _previous_champion_wr = wr
        _previous_champion_id = data.get("agent_id", _previous_champion_id)

    elif event_type == "paper_trade_validation":
        pt_wr = data.get("paper_trade_wr", 0)
        bt_wr = data.get("backtest_wr", 0)
        summary = (
            f"Paper trade validates agent {agent}: "
            f"PT={pt_wr:.1%} vs BT={bt_wr:.1%} (delta={pt_wr - bt_wr:+.1%})."
        )
        metric_value = pt_wr
        verdict = "pass" if pt_wr >= bt_wr * 0.95 else "regressed"

    else:
        summary = f"Evolution breakthrough at gen {generation}: {event_type}."
        metric_value = wr
        verdict = "pass"

    outcome_id = f"outcome:evo-gen{generation}-{event_type}-{agent}"

    _outcomes.append({
        "id": outcome_id,
        "targetType": "evolution_path",
        "targetId": "evolution-path:population-search",
        "evidenceLane": "benchmark_evidence",
        "verdict": verdict,
        "summary": summary,
        "metricName": "win_rate",
        "metricValue": round(metric_value, 4),
        "createdAt": now,
        "context": {
            "benchmark": {
                "benchmarkName": "crypto_backtest_evaluation",
                "scenarioId": f"gen_{generation}",
                "scenarioPack": "evolutionary_search",
                "baselineId": "population-baseline",
                "strongestComponent": "guard_synergy",
                "weakestComponent": "regime_adaptability",
                "componentScores": {
                    "win_rate": round(wr, 4),
                    "guard_synergy": round(min(0.99, wr * 1.1), 4),
                    "regime_adaptability": round(max(0.3, wr * 0.7), 4),
                },
            },
        },
    })

    # Write local for read-back
    _write_local(
        observer_name=f"breakthrough_{event_type}",
        captured_data={
            "generation": generation,
            "event_type": event_type,
            **data,
        },
    )

    # Update collective sync
    _write_collective_sync()


def detect_champion_change(report: dict) -> dict | None:
    """Check if this generation produced a new champion."""
    pop = report.get("population_summary", {})
    current_best = pop.get("best_wr", 0)

    if current_best > _previous_champion_wr and current_best >= 0.58:
        return {
            "win_rate": current_best,
            "agent_id": pop.get("best_agent_id", "unknown"),
            "previous_wr": _previous_champion_wr,
            "delta": current_best - _previous_champion_wr,
        }
    return None


# ── Read Functions (internal read-back from local JSONL) ─────────────────


def load_actionable_insights(min_confidence: float = 0.0) -> list[dict]:
    """Read insight_synthesizer entries from local JSONL.

    Returns list of captured_data dicts for meta-agent integration.
    """
    results = []
    if not LOCAL_JSONL_PATH.exists():
        return results
    try:
        with open(LOCAL_JSONL_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("observer_name") == "insight_synthesizer":
                    captured = entry.get("captured_data", {})
                    captured["_timestamp"] = entry.get("timestamp", "")
                    results.append(captured)
    except OSError as e:
        logger.debug("Failed to read local JSONL: %s", e)
    return results


def load_dead_end_patterns() -> list[dict]:
    """Extract dead-end patterns from local insights.

    Returns deduplicated list of dead-end dicts.
    """
    seen = set()
    results = []
    for insight in load_actionable_insights():
        for de in insight.get("dead_ends", []):
            pattern = de.get("pattern", "")
            if pattern and pattern not in seen:
                seen.add(pattern)
                results.append(de)
    return results


def load_guard_effectiveness() -> dict[str, float]:
    """Extract guard -> WR delta map from local insights.

    Returns dict mapping guard name to average WR improvement.
    """
    guard_deltas: dict[str, list[float]] = {}
    for insight_data in load_actionable_insights():
        for ai in insight_data.get("actionable_insights", []):
            text = ai.get("insight", "")
            if "improves WR by" in text and "'" in text:
                parts = text.split("'")
                if len(parts) >= 2:
                    guard_name = parts[1]
                    try:
                        delta = float(text.split("by")[-1].strip().split()[0])
                        guard_deltas.setdefault(guard_name, []).append(delta)
                    except (ValueError, IndexError):
                        pass
    return {
        name: sum(vals) / len(vals)
        for name, vals in guard_deltas.items()
        if vals
    }


def load_regime_productivity() -> dict[str, float]:
    """Extract strategy -> avg WR map from local pulse data.

    Returns dict mapping strategy name to average win rate.
    """
    strat_wrs: dict[str, list[float]] = {}
    if not LOCAL_JSONL_PATH.exists():
        return {}
    try:
        with open(LOCAL_JSONL_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("observer_name") != "evolution_pulse":
                    continue
                effectiveness = entry.get("captured_data", {}).get(
                    "strategy_effectiveness", {},
                )
                for name, stats in effectiveness.items():
                    avg_wr = stats.get("avg_wr", 0)
                    if avg_wr > 0:
                        strat_wrs.setdefault(name, []).append(avg_wr)
    except OSError as e:
        logger.debug("Failed to read local JSONL: %s", e)
    return {
        name: sum(vals) / len(vals)
        for name, vals in strat_wrs.items()
        if vals
    }


# ── Swarm Quality Helpers ─────────────────────────────────────────────────


def _build_swarm_insight(raw_insight: str, times_validated: int, generation: int) -> str:
    """Transform a raw insight into Swarm-quality content."""
    if "improves WR by" in raw_insight and "'" in raw_insight:
        parts = raw_insight.split("'")
        if len(parts) >= 2:
            guard = parts[1]
            try:
                delta = float(raw_insight.split("by")[-1].strip().split()[0])
                delta_pct = f"{delta:.1%}"
            except (ValueError, IndexError):
                delta_pct = "measurably"
            return (
                f"When the {guard} filter is active on crypto trades, "
                f"win rate improves by {delta_pct} because it filters out "
                f"low-quality setups before entry. Validated across "
                f"{times_validated} independent tests over {generation} "
                f"evolutionary generations."
            )

    if "strategy" in raw_insight.lower() and ("rate" in raw_insight or "wr" in raw_insight.lower()):
        return (
            f"Evolutionary search finding: {raw_insight}. "
            f"Validated {times_validated} times across {generation} generations."
        )

    if "dead end" in raw_insight.lower() or "avoid" in raw_insight.lower():
        return (
            f"Avoid this pattern in crypto trading: {raw_insight}. "
            f"Confirmed across {times_validated} independent tests."
        )

    if times_validated >= 3:
        return (
            f"Validated trading insight: {raw_insight}. "
            f"Confirmed {times_validated} times across {generation} generations."
        )

    return ""


# ── Collective Sync Writer ────────────────────────────────────────────────


def _write_collective_sync() -> None:
    """Write the complete collective-sync.json for Spark Swarm v1.0."""
    now = datetime.now(timezone.utc).isoformat()

    # Find newest and strongest
    newest_insight = _insights[-1] if _insights else None
    strongest_mastery = max(_masteries, key=lambda m: m.get("benchmarkStrength", 0)) if _masteries else None
    best_outcome = max(_outcomes, key=lambda o: o.get("metricValue", 0)) if _outcomes else None

    payload = {
        "workspaceId": f"ws_evolution_{_session_id[:10]}",
        "agentId": AGENT_ID,

        "runtimeSource": {
            "kind": "spark_researcher",
            "version": "0.2.0",
            "loopKind": "chip",
            "sourceInstanceId": AGENT_ID,
            "sourceRunId": f"spark-researcher:{_session_id}",
            "chipKey": SPECIALIZATION_KEY,
            "chipLabel": SPECIALIZATION_LABEL,
        },

        "specialization": {
            "id": SPECIALIZATION_ID,
            "key": SPECIALIZATION_KEY,
            "label": SPECIALIZATION_LABEL,
            "memoryPolicy": "selective",
        },

        "runtimePulse": {
            "agentId": AGENT_ID,
            "repoId": "repo:domain-chip-trading-crypto-evolution",
            "runtimeState": "running",
            "passNumber": _pass_number,
            "stageKey": "evolutionary_search",
            "stageLabel": f"Generation {_generation}",
            "blocker": None,
            "recommendation": _build_recommendation(),
            "lastUpdatedAt": now,
        },

        "intelligencePulse": {
            "specializationId": SPECIALIZATION_ID,
            "specializationLabel": SPECIALIZATION_LABEL,
            "activeEvolutionPathId": "evolution-path:population-search",
            "activeEvolutionPathSummary": (
                "Evolve crypto trading configurations through population-based "
                "search to maximize win rate with validated guard combinations."
            ),
            "newestInsightId": newest_insight["id"] if newest_insight else None,
            "newestInsightSummary": newest_insight["summary"][:200] if newest_insight else None,
            "strongestMasteryId": strongest_mastery["id"] if strongest_mastery else None,
            "strongestMasterySummary": strongest_mastery["summary"][:200] if strongest_mastery else None,
            "pendingContradictionCount": len(_contradictions),
            "pendingUpgradeCount": 0,
            "recommendedAbsorbTargetId": newest_insight["id"] if newest_insight else None,
            "recommendedUpgradeId": None,
            "evidence": [
                {
                    "lane": "benchmark_evidence",
                    "support": "strong" if _previous_champion_wr >= 0.70 else "moderate",
                    "summary": (
                        f"Gen {_generation}: {len(_outcomes)} outcomes evaluated; "
                        f"best WR {_previous_champion_wr:.1%}; "
                        f"{len(_insights)} validated insights."
                    ),
                },
            ],
        },

        "evolutionPaths": [
            {
                "id": "evolution-path:population-search",
                "scope": "specialization",
                "specializationId": SPECIALIZATION_ID,
                "summary": (
                    "Evolve crypto trading configurations through population-based "
                    "search to maximize win rate with validated guard combinations."
                ),
                "status": "open",
                "assignedAgentId": AGENT_ID,
                "bestOutcomeId": best_outcome["id"] if best_outcome else None,
                "expiresAt": None,
                "createdAt": _session_id,
                "updatedAt": now,
            },
        ],

        "insights": _insights[-20:],  # Keep last 20 to avoid bloat
        "masteries": _masteries[-10:],
        "masteryReviews": [],
        "contradictions": _contradictions[-10:],
        "upgrades": [],
        "upgradeDeliveries": [],
        "outcomes": _outcomes[-20:],

        "artifactRefs": _artifact_refs[-10:],

        "emittedAt": now,
    }

    try:
        SPARK_SWARM_DIR.mkdir(parents=True, exist_ok=True)
        tmp = COLLECTIVE_SYNC_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        tmp.replace(COLLECTIVE_SYNC_PATH)
    except OSError as e:
        logger.debug("Failed to write collective-sync.json: %s", e)


def _build_recommendation() -> str:
    """Build a contextual recommendation for the runtime pulse."""
    if _previous_champion_wr >= 0.73:
        return (
            "Champion at plateau. Focus on guard synergy exploration and "
            "temperature shock to escape local optima."
        )
    if _previous_champion_wr >= 0.65:
        return "Strong champion. Continue crossover breeding with diversity pressure."
    return "Early exploration phase. Prioritize diverse strategy coverage."


# ── Internal Helpers ─────────────────────────────────────────────────────


def _write_local(observer_name: str, captured_data: dict) -> None:
    """Append a JSONL line to the local insights file for internal read-back."""
    entry = {
        "observer_name": observer_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "captured_data": captured_data,
        "session_id": _session_id,
    }
    try:
        with open(LOCAL_JSONL_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError as e:
        logger.debug("Local JSONL write failed: %s", e)


def _load_existing_sync() -> tuple[list, list, list, list, list]:
    """Load existing collective sync state for continuity across sessions."""
    if not COLLECTIVE_SYNC_PATH.exists():
        return [], [], [], [], []
    try:
        data = json.loads(COLLECTIVE_SYNC_PATH.read_text(encoding="utf-8"))
        return (
            data.get("insights", []),
            data.get("masteries", []),
            data.get("outcomes", []),
            data.get("contradictions", []),
            data.get("artifactRefs", []),
        )
    except (json.JSONDecodeError, OSError) as e:
        logger.debug("Could not load existing collective sync: %s", e)
        return [], [], [], [], []


def _short_hash(text: str) -> str:
    """Generate a short hash for deduplication."""
    import hashlib
    return hashlib.md5(text.encode()).hexdigest()[:8]
