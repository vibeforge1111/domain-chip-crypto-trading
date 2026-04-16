"""Evolution Engine -- population-based strategy discovery.

Simplified from DGM-H for production use. Runs evolution cycles:
1. Generate new agent variants (meta-agent)
2. Evaluate them (staged backtest)
3. Update population archive
4. Track performance of meta-strategies
5. Save state and report progress
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .evaluator import evaluate_agent, staged_evaluate, _parallel_eval_worker
from .meta_agent import MetaAgent
from .performance_tracker import InsightSynthesizer, PerformanceTracker
from .population import Agent, PopulationArchive

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]


class EvolutionEngine:
    """Main evolution loop for trading strategies (production variant)."""

    def __init__(
        self,
        population_size: int = 20,
        children_per_generation: int = 10,
        archive_root: Path | None = None,
        trading_root: Path | None = None,
        use_staged_eval: bool = True,
        max_workers: int = 1,
    ):
        self.population_size = population_size
        self.children_per_generation = children_per_generation
        self.trading_root = trading_root or REPO_ROOT
        self.archive_root = archive_root or (REPO_ROOT / "live" / "archive")
        self.use_staged_eval = use_staged_eval
        self.max_workers = max_workers

        self.population = PopulationArchive(
            archive_root=self.archive_root,
            max_archive_size=population_size * 5,
        )
        self.tracker = PerformanceTracker(archive_root=self.archive_root)
        self.meta_agent = MetaAgent(self.population, self.tracker)
        self.synthesizer = InsightSynthesizer(self.tracker)

        # State
        self.current_generation = 0
        self._load_state()

    def _load_state(self):
        """Resume from last saved state."""
        gen_num, agents = self.population.load_latest()
        self.current_generation = gen_num
        meta_state_path = self.archive_root / "meta_agent_state.json"
        self.meta_agent.load_state(meta_state_path)
        logger.info("Loaded state: gen=%d, population=%d", gen_num, len(agents))

    def _prune_old_generations(self, keep_recent: int = 10, keep_every: int = 100):
        """Remove old generation files, keeping recent + milestones."""
        gen_files = sorted(self.population.generations_path.glob("gen_*.json"))
        for gf in gen_files:
            try:
                gen_num = int(gf.stem.split("_")[1])
            except (IndexError, ValueError):
                continue
            if gen_num >= self.current_generation - keep_recent:
                continue
            if gen_num % keep_every == 0:
                continue
            gf.unlink(missing_ok=True)

    def run_generation(self, total_generations: int | None = None) -> dict:
        """Run a single evolution generation."""
        self.current_generation += 1
        gen = self.current_generation
        started_at = datetime.now(timezone.utc)
        logger.info("=== Generation %d ===", gen)

        # 1. Generate new agents
        new_agents = self.meta_agent.generate_agents(
            count=self.children_per_generation,
            generation=gen,
            total_generations=total_generations,
        )
        logger.info("Generated %d candidates", len(new_agents))

        # 2. Evaluate (parallel if workers > 1)
        staged_stats = {"quick_reject": 0, "medium_reject": 0, "full": 0}

        if self.max_workers > 1 and len(new_agents) > 1:
            from concurrent.futures import ProcessPoolExecutor
            worker_args = [
                (agent.mutations, str(self.trading_root), self.use_staged_eval)
                for agent in new_agents
            ]
            with ProcessPoolExecutor(max_workers=self.max_workers) as pool:
                results = list(pool.map(_parallel_eval_worker, worker_args))

            for agent, fitness in zip(new_agents, results):
                agent.fitness = fitness
                if self.use_staged_eval:
                    stage = fitness.get("eval_stage", "full")
                    staged_stats[stage] = staged_stats.get(stage, 0) + 1
        else:
            for agent in new_agents:
                if self.use_staged_eval:
                    fitness = staged_evaluate(agent.mutations, runtime_root=self.trading_root)
                    stage = fitness.get("eval_stage", "full")
                    staged_stats[stage] = staged_stats.get(stage, 0) + 1
                else:
                    fitness = evaluate_agent(agent.mutations, runtime_root=self.trading_root)
                agent.fitness = fitness

        # 3. Update population + track outcomes
        improvements = 0
        for agent in new_agents:
            parent = self.population.get_parent(agent.parent_id) if agent.parent_id else None
            improved = parent is not None and agent.win_rate > parent.win_rate
            if improved:
                improvements += 1

            self.population.add_agent(agent)
            self.tracker.record_outcome(
                generation=gen,
                agent_id=agent.agent_id,
                meta_strategy=agent.meta_strategy,
                parent_id=agent.parent_id,
                mutations=agent.mutations,
                fitness=agent.fitness,
                improved_over_parent=improved,
            )

        # 4. Meta-evolution (every 3 generations)
        meta_changes = {}
        if gen % 3 == 0:
            meta_changes = self.meta_agent.evolve_meta_strategies()

        # 5. Synthesize insights (every 3 generations)
        if gen % 3 == 0:
            self.synthesizer.synthesize(gen)

        # 6. Save state
        self.population.save_generation(gen)
        self.meta_agent.save_state(self.archive_root / "meta_agent_state.json")
        self._prune_old_generations()

        finished_at = datetime.now(timezone.utc)
        duration = (finished_at - started_at).total_seconds()

        best = self.population.get_best_agent()
        report = {
            "generation": gen,
            "candidates": len(new_agents),
            "improvements": improvements,
            "improvement_rate": improvements / max(1, len(new_agents)),
            "population": self.population.summary(),
            "best_agent": best.to_dict() if best else None,
            "staged_eval": staged_stats if self.use_staged_eval else None,
            "meta_changes": meta_changes,
            "duration_seconds": round(duration, 1),
            "timestamp": finished_at.isoformat(),
        }

        # Save report
        report_path = self.archive_root / "generations" / f"report_{gen:04d}.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

        self._print_report(report)
        return report

    def run(self, generations: int = 10) -> list[dict]:
        """Run multiple generations of evolution."""
        reports = []
        for i in range(generations):
            report = self.run_generation(total_generations=generations)
            reports.append(report)
        return reports

    def seed_from_existing(self) -> int:
        """Seed population from candidate_trials in spark-researcher.project.json."""
        config_path = REPO_ROOT / "spark-researcher.project.json"
        if not config_path.exists():
            return 0
        config = json.loads(config_path.read_text(encoding="utf-8"))
        trials = config.get("candidate_trials", [])
        count = 0
        for trial in trials:
            mutations = trial.get("mutations", {})
            if not mutations:
                continue
            if self.population.is_duplicate(mutations):
                continue
            agent = Agent(
                agent_id="",
                mutations=mutations,
                meta_strategy="seed_existing",
                generation=0,
            )
            # Evaluate the seed
            if self.use_staged_eval:
                fitness = staged_evaluate(mutations, runtime_root=self.trading_root)
            else:
                fitness = evaluate_agent(mutations, runtime_root=self.trading_root)
            agent.fitness = fitness
            self.population.add_agent(agent)
            count += 1
        if count:
            self.population.save_generation(0)
        logger.info("Seeded %d agents from candidate_trials", count)
        return count

    def seed_from_pro_gen(self) -> int:
        """Seed population from pro__gen_premium.json (evolution repo agents)."""
        pro_path = REPO_ROOT / "live" / "archive" / "generations" / "pro__gen_premium.json"
        if not pro_path.exists():
            return 0
        data = json.loads(pro_path.read_text(encoding="utf-8"))
        agents_data = data.get("agents", data) if isinstance(data, dict) else data
        if not isinstance(agents_data, list):
            return 0
        count = 0
        for ad in agents_data:
            mutations = ad.get("mutations", {})
            if not mutations or self.population.is_duplicate(mutations):
                continue
            agent = Agent(
                agent_id=ad.get("agent_id", ""),
                mutations=mutations,
                meta_strategy="seed_pro",
                generation=0,
                fitness=ad.get("fitness", {}),
            )
            # If no fitness data, evaluate
            if not agent.fitness or agent.win_rate == 0:
                if self.use_staged_eval:
                    fitness = staged_evaluate(mutations, runtime_root=self.trading_root)
                else:
                    fitness = evaluate_agent(mutations, runtime_root=self.trading_root)
                agent.fitness = fitness
            self.population.add_agent(agent)
            count += 1
        if count:
            self.population.save_generation(0)
        logger.info("Seeded %d agents from pro gen", count)
        return count

    def status(self) -> dict:
        """Return current evolution status."""
        summary = self.population.summary()
        effectiveness = self.tracker.strategy_effectiveness()
        return {
            "generation": self.current_generation,
            "population": summary,
            "strategy_effectiveness": effectiveness,
            "insights": self.synthesizer.get_actionable_insights(),
        }

    def _print_report(self, report: dict) -> None:
        """Pretty-print a generation report."""
        pop = report.get("population", {})
        best = report.get("best_agent")
        staged = report.get("staged_eval")

        print(f"\n{'='*60}")
        print(f"Generation {report['generation']} Complete")
        print(f"{'='*60}")
        print(f"  Candidates: {report['candidates']}")
        print(f"  Improvements: {report['improvements']} ({report['improvement_rate']:.0%})")
        print(f"  Population: {pop.get('size', 0)} (elite={pop.get('elite', 0)}, viable={pop.get('viable', 0)})")
        if best:
            print(f"  Best: WR={best.get('fitness', {}).get('win_rate', 0):.3f} | {best.get('mutations', {}).get('strategy_id', '?')}")
        if staged:
            print(f"  Staged: quick_reject={staged.get('quick_reject', 0)}, medium_reject={staged.get('medium_reject', 0)}, full={staged.get('full', 0)}")
        print(f"  Duration: {report.get('duration_seconds', 0):.1f}s")
        print()
