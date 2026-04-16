"""Population Archive — maintains diverse agent variants as stepping stones.

DGM-H principle: population-based exploration prevents getting trapped in local
optima. Agents that are currently suboptimal may enable future progress.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ARCHIVE_ROOT = Path(__file__).resolve().parent.parent / "archive"


@dataclass
class Agent:
    """A single agent in the population = mutation dict + metadata."""

    agent_id: str
    mutations: dict[str, Any]
    meta_strategy: str  # which meta-strategy generated this agent
    parent_id: str | None = None
    generation: int = 0
    fitness: dict[str, float] = field(default_factory=dict)
    created_at: str = ""
    children_count: int = 0

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if not self.agent_id:
            self.agent_id = self._compute_id()

    def _compute_id(self) -> str:
        """Deterministic ID from mutations."""
        content = json.dumps(self.mutations, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    @property
    def win_rate(self) -> float:
        return self.fitness.get("win_rate", 0.0)

    @property
    def wealth_factor(self) -> float:
        return self.fitness.get("wealth_factor", 0.0)

    @property
    def is_viable(self) -> bool:
        """Agent passes minimum viability gates."""
        return self.wealth_factor >= 0.8 and self.win_rate > 0.52

    @property
    def is_elite(self) -> bool:
        """Agent passes strict promotion gates."""
        return self.wealth_factor >= 1.0 and self.win_rate >= 0.58

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> Agent:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class PopulationArchive:
    """Maintains and evolves a population of agent variants."""

    def __init__(self, archive_root: Path | None = None, max_archive_size: int = 200):
        self.root = archive_root or ARCHIVE_ROOT
        self.generations_path = self.root / "generations"
        self.generations_path.mkdir(parents=True, exist_ok=True)
        self.max_archive_size = max_archive_size

        self._population: list[Agent] = []
        self._all_tested: dict[str, Agent] = {}  # agent_id → Agent (full history)

    # ── Persistence ────────────────────────────────────────────

    def save_generation(self, generation: int) -> Path:
        """Save current population to a generation file."""
        path = self.generations_path / f"gen_{generation:04d}.json"
        data = {
            "generation": generation,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "population_size": len(self._population),
            "elite_count": sum(1 for a in self._population if a.is_elite),
            "viable_count": sum(1 for a in self._population if a.is_viable),
            "best_wr": max((a.win_rate for a in self._population), default=0),
            "agents": [a.to_dict() for a in self._population],
        }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return path

    def load_generation(self, generation: int) -> list[Agent]:
        """Load a specific generation from archive."""
        path = self.generations_path / f"gen_{generation:04d}.json"
        if not path.exists():
            return []
        data = json.loads(path.read_text(encoding="utf-8"))
        self._population = [Agent.from_dict(a) for a in data["agents"]]
        for agent in self._population:
            self._all_tested[agent.agent_id] = agent
        return self._population

    def load_latest(self) -> tuple[int, list[Agent]]:
        """Load the most recent generation + any premium agent packs."""
        gen_files = sorted(self.generations_path.glob("gen_*.json"))
        pro_files = sorted(self.generations_path.glob("pro__gen_*.json"))
        if not gen_files and not pro_files:
            return 0, []

        # Load standard latest generation
        gen_num = 0
        if gen_files:
            latest = gen_files[-1]
            gen_num = int(latest.stem.split("_")[1])
            self.load_generation(gen_num)

        # Merge premium agents (non-destructive, tagged)
        for pf in pro_files:
            try:
                data = json.loads(pf.read_text(encoding="utf-8"))
                for ad in data.get("agents", []):
                    ad.setdefault("_source", "premium")
                    agent = Agent.from_dict(ad)
                    if agent.agent_id not in self._all_tested:
                        self._population.append(agent)
                        self._all_tested[agent.agent_id] = agent
            except Exception:
                pass  # skip malformed premium files

        return gen_num, self._population

    # ── Population Management ──────────────────────────────────

    def add_agent(self, agent: Agent) -> None:
        """Add an evaluated agent to the population."""
        self._population.append(agent)
        self._all_tested[agent.agent_id] = agent

        # Prune if over max size — keep best + diverse
        if len(self._population) > self.max_archive_size:
            self._prune()

    def _prune(self) -> None:
        """Prune population keeping elite, viable, and diverse agents.

        Niche preservation: minority strategies (non-dominant strategy_id)
        are protected from pruning to maintain diversity for crossover.
        """
        elite = [a for a in self._population if a.is_elite]
        viable = [a for a in self._population if a.is_viable and not a.is_elite]
        rest = [a for a in self._population if not a.is_viable]

        # Keep all elite, top viable, and some diverse rest
        viable.sort(key=lambda a: a.win_rate, reverse=True)
        rest.sort(key=lambda a: a.win_rate, reverse=True)

        keep_viable = viable[: self.max_archive_size // 2]
        remaining_slots = self.max_archive_size - len(elite) - len(keep_viable)
        keep_rest = rest[:max(0, remaining_slots)]

        kept = elite + keep_viable + keep_rest

        # Niche preservation: ensure minority strategies survive pruning
        # 50 = enough genetic diversity for crossover to find viable combos
        MIN_NICHE_SIZE = 50
        kept_ids = {a.agent_id for a in kept}
        strategy_counts: dict[str, int] = {}
        for a in kept:
            sid = a.mutations.get("strategy_id", "unknown")
            strategy_counts[sid] = strategy_counts.get(sid, 0) + 1

        # Find agents from minority strategies not yet in kept
        for a in self._population:
            sid = a.mutations.get("strategy_id", "unknown")
            if a.agent_id not in kept_ids and strategy_counts.get(sid, 0) < MIN_NICHE_SIZE:
                kept.append(a)
                kept_ids.add(a.agent_id)
                strategy_counts[sid] = strategy_counts.get(sid, 0) + 1

        self._population = kept

    @property
    def population(self) -> list[Agent]:
        return self._population

    @property
    def elite(self) -> list[Agent]:
        return [a for a in self._population if a.is_elite]

    @property
    def viable(self) -> list[Agent]:
        return [a for a in self._population if a.is_viable]

    def is_duplicate(self, mutations: dict) -> bool:
        """Check if these exact mutations were already tested."""
        agent_id = Agent(agent_id="", mutations=mutations, meta_strategy="check")._compute_id()
        return agent_id in self._all_tested

    def get_parent(self, agent_id: str) -> Agent | None:
        """Retrieve an agent by ID from the full history."""
        return self._all_tested.get(agent_id)

    def get_best_agent(self) -> Agent | None:
        """Return the highest win-rate agent in the current population."""
        if not self._population:
            return None
        return max(self._population, key=lambda a: a.win_rate)

    def diversity_score(self, mutations: dict) -> float:
        """How different is this mutation set from the current population?

        Returns 0.0 (identical to existing) to 1.0 (completely novel).
        """
        if not self._population:
            return 1.0

        all_keys = set()
        for a in self._population:
            all_keys.update(a.mutations.keys())
        all_keys.update(mutations.keys())

        if not all_keys:
            return 0.0

        distances = []
        for existing in self._population:
            matching = 0
            total = len(all_keys)
            for k in all_keys:
                v1 = mutations.get(k)
                v2 = existing.mutations.get(k)
                if v1 == v2:
                    matching += 1
            distances.append(1.0 - matching / total)

        return sum(distances) / len(distances) if distances else 1.0

    def summary(self) -> dict:
        """Return population summary statistics."""
        if not self._population:
            return {"size": 0}

        wrs = [a.win_rate for a in self._population]
        return {
            "size": len(self._population),
            "elite": len(self.elite),
            "viable": len(self.viable),
            "best_wr": max(wrs),
            "avg_wr": sum(wrs) / len(wrs),
            "strategies_used": list(
                set(a.meta_strategy for a in self._population)
            ),
            "generations_span": (
                min(a.generation for a in self._population),
                max(a.generation for a in self._population),
            ),
            "total_tested": len(self._all_tested),
        }
