"""Evolution Engine — the main DGM-H loop.

Orchestrates the full evolution cycle:
  1. Generate new agent variants (meta-agent)
  2. Evaluate them (task agent / backtest)
  3. Update population archive
  4. Track performance of meta-strategies
  5. Evolve meta-strategies themselves (metacognitive self-modification)
  6. Save state and report progress
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .evaluator import evaluate_agent, staged_evaluate, _parallel_eval_worker
from .llm_code_gen import LLMCodeGenerator
from .meta_agent import MetaAgent
from .performance_tracker import InsightSynthesizer, PerformanceTracker
from .population import Agent, PopulationArchive
from .self_diagnosis import SelfDiagnosis
from .self_referential import SelfReferentialEngine
from .transfer import TransferLearner
from . import spark_bridge

logger = logging.getLogger(__name__)

EVOLUTION_ROOT = Path(__file__).resolve().parent.parent
TRADING_CHIP_ROOT = EVOLUTION_ROOT.parent


class EvolutionEngine:
    """Main DGM-H evolution loop for trading strategies."""

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
        self.trading_root = trading_root or TRADING_CHIP_ROOT
        self.archive_root = archive_root or (EVOLUTION_ROOT / "archive")
        self.use_staged_eval = use_staged_eval
        self.max_workers = max_workers

        # Core components
        self.population = PopulationArchive(
            archive_root=self.archive_root,
            max_archive_size=population_size * 5,
        )
        self.tracker = PerformanceTracker(archive_root=self.archive_root)
        self.meta_agent = MetaAgent(self.population, self.tracker)
        self.transfer = TransferLearner(
            self.population, self.tracker, archive_root=self.archive_root,
        )
        self.synthesizer = InsightSynthesizer(self.tracker)
        self.diagnosis = SelfDiagnosis(archive_root=self.archive_root)
        self.code_gen = LLMCodeGenerator()
        self.self_ref = SelfReferentialEngine()
        self.transfer_interval = 5  # Run transfer suggestions every N generations
        self.insight_interval = 3  # Synthesize insights every N generations
        self.diagnosis_interval = 10  # Run self-diagnosis every N generations
        self.code_gen_interval = 5  # Generate LLM guards every N generations
        self.self_ref_interval = 10  # Self-referential strategy rewrite every N gens

        # State
        self.current_generation = 0
        self._meta_state_path = self.archive_root / "meta_agent_state.json"

        # Plateau detection
        self._plateau_best_wr = 0.0
        self._plateau_gen_start = 0
        self._plateau_shock_active = False
        self._plateau_shock_end_gen = 0
        self._PLATEAU_THRESHOLD = 100  # gens without improvement before shock
        self._SHOCK_DURATION = 50  # gens of boosted exploration

        # Load previous state if exists
        self._load_state()

    def _load_state(self) -> None:
        """Resume from last saved state."""
        gen, agents = self.population.load_latest()
        self.current_generation = gen
        self.meta_agent.load_state(self._meta_state_path)
        if agents:
            logger.info(
                "Resumed at generation %d with %d agents",
                gen, len(agents),
            )

    def _prune_old_generations(
        self, current_gen: int, keep_recent: int = 5, keep_every: int = 100,
    ) -> None:
        """Delete old gen files to prevent disk-full crashes.

        Keeps:
          - Every `keep_every`-th gen file (milestones: 100, 200, 300, ...)
          - The most recent `keep_recent` gen files
          - All report_*.json files (small, always kept)
        """
        gen_dir = self.population.generations_path
        if not gen_dir.exists():
            return

        gen_files = sorted(gen_dir.glob("gen_*.json"))
        if len(gen_files) <= keep_recent:
            return

        # Parse gen numbers from filenames
        keep_paths = set()
        for gf in gen_files[-keep_recent:]:
            keep_paths.add(gf)

        deleted = 0
        for gf in gen_files[:-keep_recent]:
            # Extract gen number: gen_0052.json -> 52
            try:
                gen_num = int(gf.stem.split("_")[1])
            except (IndexError, ValueError):
                continue
            if gen_num % keep_every == 0:
                continue  # milestone — keep
            try:
                gf.unlink()
                deleted += 1
            except OSError:
                pass

        if deleted:
            logger.info("Auto-pruned %d old gen files (kept milestones every %d + last %d)",
                        deleted, keep_every, keep_recent)

    # ── Main Evolution Loop ────────────────────────────────────

    def run_generation(
        self, total_generations: int | None = None,
    ) -> dict[str, Any]:
        """Run one generation of the evolution loop.

        This is one iteration of the DGM-H cycle:
        1. Generate variants (with compute-aware planning)
        2. Evaluate variants (with staged filtering)
        3. Update population
        4. Meta-evolve
        5. Report

        Args:
            total_generations: If provided, enables compute-aware planning
                (explore early, exploit late).

        Returns generation report dict.
        """
        self.current_generation += 1
        gen = self.current_generation
        started_at = datetime.now(timezone.utc)

        logger.info("=== Generation %d ===", gen)

        # Load PT-validated agent IDs for breeding priority
        self.meta_agent._load_pt_state(gen)

        # ── Step 1: Generate new agent variants ───────────────
        logger.info("Generating %d agent variants...", self.children_per_generation)
        new_agents = self.meta_agent.generate_agents(
            count=self.children_per_generation,
            generation=gen,
            total_generations=total_generations,
        )
        logger.info("Generated %d unique variants", len(new_agents))

        # ── Step 2: Evaluate each variant ─────────────────────
        evaluated = []
        staged_stats = {"quick_reject": 0, "medium_reject": 0, "full": 0}

        if self.max_workers > 1 and len(new_agents) > 1:
            # Parallel evaluation via ProcessPoolExecutor
            from concurrent.futures import ProcessPoolExecutor
            logger.info(
                "  Parallel evaluation: %d agents across %d workers",
                len(new_agents), self.max_workers,
            )
            worker_args = [
                (agent.mutations, str(self.trading_root), self.use_staged_eval)
                for agent in new_agents
            ]
            with ProcessPoolExecutor(max_workers=self.max_workers) as pool:
                results = list(pool.map(_parallel_eval_worker, worker_args))

            # Sequential post-processing: assign fitness, record outcomes
            for agent, fitness in zip(new_agents, results):
                if self.use_staged_eval:
                    stage = fitness.get("eval_stage", "full")
                    staged_stats[stage] = staged_stats.get(stage, 0) + 1

                agent.fitness = fitness
                evaluated.append(agent)

                improved = False
                if agent.parent_id:
                    parent = self.population.get_parent(agent.parent_id)
                    if parent:
                        improved = agent.win_rate > parent.win_rate

                self.tracker.record_outcome(
                    generation=gen,
                    agent_id=agent.agent_id,
                    meta_strategy=agent.meta_strategy,
                    parent_id=agent.parent_id,
                    mutations=agent.mutations,
                    fitness=fitness,
                    improved_over_parent=improved,
                )

                status = "ELITE" if agent.is_elite else "viable" if agent.is_viable else "weak"
                logger.info(
                    "  Agent %s [%s]: WR=%.3f WF=%.1f [%s]",
                    agent.agent_id[:8], agent.meta_strategy,
                    agent.win_rate, agent.wealth_factor, status,
                )
        else:
            # Sequential evaluation (default)
            for i, agent in enumerate(new_agents):
                logger.info(
                    "  Evaluating agent %d/%d [%s via %s]%s...",
                    i + 1, len(new_agents), agent.agent_id[:8], agent.meta_strategy,
                    " (staged)" if self.use_staged_eval else "",
                )
                try:
                    if self.use_staged_eval:
                        fitness = staged_evaluate(
                            agent.mutations,
                            runtime_root=self.trading_root,
                        )
                        stage = fitness.get("eval_stage", "full")
                        staged_stats[stage] = staged_stats.get(stage, 0) + 1
                    else:
                        fitness = evaluate_agent(
                            agent.mutations,
                            runtime_root=self.trading_root,
                        )
                    agent.fitness = fitness
                    evaluated.append(agent)

                    # Check if improved over parent
                    improved = False
                    if agent.parent_id:
                        parent = self.population.get_parent(agent.parent_id)
                        if parent:
                            improved = agent.win_rate > parent.win_rate

                    # Record outcome for meta-learning
                    self.tracker.record_outcome(
                        generation=gen,
                        agent_id=agent.agent_id,
                        meta_strategy=agent.meta_strategy,
                        parent_id=agent.parent_id,
                        mutations=agent.mutations,
                        fitness=fitness,
                        improved_over_parent=improved,
                    )

                    status = "ELITE" if agent.is_elite else "viable" if agent.is_viable else "weak"
                    logger.info(
                        "    WR=%.3f WF=%.1f DD=%.3f [%s]",
                        agent.win_rate,
                        agent.wealth_factor,
                        fitness.get("max_drawdown", 1.0),
                        status,
                    )

                except Exception as e:
                    logger.error("    FAILED: %s", e)
                    agent.fitness = {
                        "win_rate": 0, "wealth_factor": 0,
                        "max_drawdown": 1.0, "error": str(e),
                        "viable": False, "elite": False,
                    }
                    evaluated.append(agent)

        # ── Step 3: Update population ─────────────────────────
        for agent in evaluated:
            self.population.add_agent(agent)

        # ── Step 4: Meta-evolve strategies ────────────────────
        meta_changes = {}
        if gen % 3 == 0:  # Evolve meta every 3 generations
            logger.info("Meta-evolving strategies...")
            meta_changes = self.meta_agent.evolve_meta_strategies()
            for name, change in meta_changes.items():
                logger.info(
                    "  %s: %s (improvement_rate=%.2f)",
                    name, change["action"], change["rate"],
                )

        # ── Step 4a: Synthesize insights (persistent memory) ──
        insights = []
        if gen % self.insight_interval == 0:
            logger.info("Synthesizing insights from performance data...")
            insights = self.synthesizer.synthesize(gen)
            actionable = self.synthesizer.get_actionable_insights()
            if actionable:
                logger.info("  %d actionable insights:", len(actionable))
                for ins in actionable[:5]:
                    conf = "HIGH" if ins["confidence"] >= 0.7 else "MED"
                    logger.info(
                        "    [%s] %s (validated %dx)",
                        conf, ins["insight"], ins.get("times_validated", 1),
                    )

        # ── Step 4a-ii: Self-diagnosis & gate calibration ──────
        diagnosis_report = {}
        if gen % self.diagnosis_interval == 0 and gen >= self.diagnosis_interval:
            logger.info("Running self-diagnosis...")
            diagnosis_report = self.diagnosis.diagnose(self.tracker._log_path)
            if diagnosis_report.get("status") != "insufficient_data":
                holdout = diagnosis_report.get("backtest_holdout_correlation", {})
                if holdout.get("status") == "analyzed":
                    logger.info(
                        "  Holdout correlation: MAE=%.3f, bias=%s (%.3f), pass_rate=%.0f%%",
                        holdout.get("mean_absolute_error", 0),
                        holdout.get("bias_direction", "?"),
                        holdout.get("systematic_bias", 0),
                        holdout.get("holdout_pass_rate", 0) * 100,
                    )
                wf = diagnosis_report.get("walk_forward_bias", {})
                if wf.get("status") == "analyzed":
                    logger.info(
                        "  Walk-forward bias: %s (temporal_bias=%.3f)",
                        wf.get("bias_type", "?"),
                        wf.get("temporal_bias", 0),
                    )
                recs = diagnosis_report.get("gate_recommendations", {})
                if recs:
                    logger.info("  Gate recommendations:")
                    for name, rec in recs.items():
                        logger.info("    %s: %s", name, rec.get("reason", rec.get("recommendation", "")))

                # Auto-calibrate gates
                self.diagnosis.auto_calibrate(self.tracker._log_path)

        # ── Step 4b: Transfer learning ─────────────────────────
        transfer_suggestions = []
        if gen % self.transfer_interval == 0 and len(self.population.elite) >= 2:
            logger.info("Running transfer learning analysis...")
            patterns = self.transfer.extract_transferable_patterns()
            if patterns:
                logger.info(
                    "  Found %d transferable patterns", len(patterns),
                )
                for p in patterns[:3]:
                    logger.info(
                        "    %s: %d contexts, avg WR=%.3f",
                        p["pattern"], p["context_count"], p["avg_wr"],
                    )

            suggestions = self.transfer.suggest_transfers()
            if suggestions:
                # Create agents from top transfer suggestions
                transfer_count = min(3, len(suggestions))
                logger.info(
                    "  Generating %d transfer candidates...", transfer_count,
                )
                for suggestion in suggestions[:transfer_count]:
                    key, val = suggestion["transfer_pattern"].split("=", 1)
                    transfer_mutations = {
                        "doctrine_id": "compression_mean_reversion",
                        "strategy_id": "compression_range_bounce",
                        "asset_universe": suggestion["target_asset"],
                        "session_quality_filter": "skip_compression_toxic",
                        key: val,
                    }
                    if suggestion["target_regime"]:
                        transfer_mutations["extend_regimes"] = suggestion["target_regime"]

                    if not self.population.is_duplicate(transfer_mutations):
                        agent = Agent(
                            agent_id="",
                            mutations=transfer_mutations,
                            meta_strategy="transfer",
                            generation=gen,
                        )
                        # Evaluate the transfer candidate
                        try:
                            if self.use_staged_eval:
                                fitness = staged_evaluate(
                                    agent.mutations, runtime_root=self.trading_root,
                                )
                            else:
                                fitness = evaluate_agent(
                                    agent.mutations, runtime_root=self.trading_root,
                                )
                            agent.fitness = fitness
                            self.population.add_agent(agent)
                            evaluated.append(agent)

                            # Log transfer result
                            source_ctx = suggestion["source_contexts"][0] if suggestion["source_contexts"] else "unknown"
                            target_ctx = f"{suggestion['target_regime']}|{suggestion['target_asset']}"
                            self.transfer.log_transfer_result(
                                pattern=suggestion["transfer_pattern"],
                                source_context=source_ctx,
                                target_context=target_ctx,
                                source_wr=suggestion["expected_wr"],
                                target_wr=fitness.get("win_rate", 0),
                            )
                            logger.info(
                                "    Transfer %s→%s: WR=%.3f (expected %.3f)",
                                source_ctx, target_ctx,
                                fitness.get("win_rate", 0),
                                suggestion["expected_wr"],
                            )
                        except Exception as e:
                            logger.error("    Transfer eval failed: %s", e)

                transfer_suggestions = suggestions[:transfer_count]

        # ── Step 4c: LLM code generation ─────────────────────
        generated_guards = []
        if (
            self.code_gen.available
            and gen % self.code_gen_interval == 0
            and gen >= self.code_gen_interval
        ):
            logger.info("Generating LLM guard functions...")
            actionable = self.synthesizer.get_actionable_insights()

            # Extract champion's guard config for synergy mode
            champion_guards = {}
            try:
                best_agent = self.population.get_best_agent()
                if best_agent:
                    champion_guards = {
                        k: v for k, v in best_agent.mutations.items()
                        if k.startswith("cr_") or k.endswith("_guard")
                        or k.endswith("_filter") or k == "session_quality_filter"
                    }
            except Exception:
                pass

            for i in range(self.code_gen.max_guards_per_generation):
                # Alternate: synergy mode for odd iterations, normal for even
                use_synergy = bool(champion_guards) and (i % 2 == 1)
                guard_meta = self.code_gen.generate_guard(
                    insights=actionable,
                    generation=gen,
                    synergy_mode=use_synergy,
                    champion_guards=champion_guards if use_synergy else None,
                )
                if guard_meta:
                    generated_guards.append(guard_meta)
                    # Create a candidate agent that uses this guard
                    guard_mutations = {
                        "doctrine_id": "compression_mean_reversion",
                        "strategy_id": "compression_range_bounce",
                        "asset_universe": "BTC",
                        "session_quality_filter": "skip_compression_toxic",
                        "extend_regimes": "trend,event_driven,range,high_vol,fear_shock",
                        "llm_guard_id": guard_meta["guard_id"],
                    }
                    agent = Agent(
                        agent_id="",
                        mutations=guard_mutations,
                        meta_strategy="llm_code_gen",
                        generation=gen,
                    )
                    # Evaluate (staged)
                    try:
                        if self.use_staged_eval:
                            fitness = staged_evaluate(
                                agent.mutations, runtime_root=self.trading_root,
                            )
                        else:
                            fitness = evaluate_agent(
                                agent.mutations, runtime_root=self.trading_root,
                            )
                        agent.fitness = fitness
                        self.population.add_agent(agent)
                        evaluated.append(agent)
                        logger.info(
                            "  LLM guard %s: WR=%.3f WF=%.1f [%s]",
                            guard_meta["guard_id"][:8],
                            fitness.get("win_rate", 0),
                            fitness.get("wealth_factor", 0),
                            "ELITE" if agent.is_elite else "viable" if agent.is_viable else "weak",
                        )
                    except Exception as e:
                        logger.error("  LLM guard eval failed: %s", e)

            if generated_guards:
                logger.info("  Generated %d LLM guards", len(generated_guards))

        # ── Step 4d: Self-referential strategy rewrite ─────────
        new_strategies = []
        if (
            self.self_ref.available
            and gen % self.self_ref_interval == 0
            and gen >= self.self_ref_interval
        ):
            logger.info("Running self-referential strategy analysis...")
            effectiveness = self.tracker.strategy_effectiveness()
            actions = self.self_ref.analyze_strategy_performance(effectiveness)
            needs_work = {
                name: action for name, action in actions.items()
                if action in ("rewrite", "replace")
            }
            if needs_work:
                logger.info(
                    "  Strategies needing work: %s",
                    ", ".join(f"{n}={a}" for n, a in needs_work.items()),
                )

            # Generate a new evolved strategy
            actionable = self.synthesizer.get_actionable_insights()
            strategy_meta = self.self_ref.generate_new_strategy(
                effectiveness=effectiveness,
                insights=actionable,
                generation=gen,
            )
            if strategy_meta:
                new_strategies.append(strategy_meta)
                logger.info(
                    "  Generated new strategy: %s",
                    strategy_meta["strategy_id"],
                )

            # Prune consistently failing custom strategies
            active = self.self_ref.list_active_strategies()
            for sid in active:
                stats = effectiveness.get(sid, {})
                if stats.get("attempts", 0) >= 10 and stats.get("improvement_rate", 0) < 0.05:
                    self.self_ref.prune_strategy(sid)
                    logger.info("  Pruned failing strategy: %s", sid)

        # ── Step 4e: Paper trade status (read from PT daemon) ──
        paper_trade_results = []
        if (
            gen % self.diagnosis_interval == 0
            and gen >= self.diagnosis_interval
        ):
            pt_state_path = self.archive_root / "pt_state.json"
            if pt_state_path.exists():
                try:
                    import json as _json
                    pt_state = _json.loads(
                        pt_state_path.read_text(encoding="utf-8")
                    )
                    idx = pt_state.get("agent_pt_index", {})
                    cov = pt_state.get("coverage", {})
                    daemon_status = pt_state.get("daemon_status", "unknown")

                    # Report top 10 PT agents
                    top_pt = sorted(
                        idx.items(),
                        key=lambda x: x[1].get("pt_score", 0),
                        reverse=True,
                    )[:10]

                    if top_pt:
                        logger.info(
                            "PT daemon %s: %d agents tested (%.1f%% coverage)",
                            daemon_status,
                            cov.get("tested_agents", 0),
                            cov.get("coverage_pct", 0) * 100,
                        )
                        for aid, data in top_pt:
                            paper_trade_results.append({
                                "agent_id": aid,
                                "backtest_wr": round(data.get("bt_wr", 0), 4),
                                "paper_trade_wr": round(
                                    data.get("pt_wr_avg", 0), 4,
                                ),
                                "delta": round(data.get("pt_delta_avg", 0), 4),
                                "trades": data.get("pt_trades_total", 0),
                                "pt_score": data.get("pt_score", 0),
                                "status": data.get("status", "unknown"),
                            })
                            logger.info(
                                "  %s: BT=%.3f PT=%.3f delta=%+.3f "
                                "score=%.3f [%s]",
                                aid[:8],
                                data.get("bt_wr", 0),
                                data.get("pt_wr_avg", 0),
                                data.get("pt_delta_avg", 0),
                                data.get("pt_score", 0),
                                data.get("status", "?"),
                            )
                except Exception as e:
                    logger.debug("Could not read PT state: %s", e)

        # ── Step 5: Save state ────────────────────────────────
        gen_path = self.population.save_generation(gen)
        self.meta_agent.save_state(self._meta_state_path)

        # ── Step 5b: Auto-prune old gen files to prevent disk full ───
        self._prune_old_generations(gen, keep_recent=5, keep_every=100)

        # ── Step 6: Build report ──────────────────────────────
        finished_at = datetime.now(timezone.utc)
        elapsed = (finished_at - started_at).total_seconds()

        report = {
            "generation": gen,
            "started_at": started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "elapsed_seconds": elapsed,
            "variants_generated": len(new_agents),
            "variants_evaluated": len(evaluated),
            "new_elite": sum(1 for a in evaluated if a.is_elite),
            "new_viable": sum(1 for a in evaluated if a.is_viable),
            "staged_eval": staged_stats if self.use_staged_eval else None,
            "compute_phase": getattr(self.meta_agent, "_compute_phase", "unknown"),
            "transfer_candidates": len(transfer_suggestions),
            "transfer_effectiveness": self.transfer.transfer_effectiveness() if transfer_suggestions else {},
            "insights_count": len(insights),
            "actionable_insights": len(self.synthesizer.get_actionable_insights()),
            "self_diagnosis": diagnosis_report if diagnosis_report else None,
            "llm_guards_generated": len(generated_guards),
            "self_ref_strategies": len(new_strategies),
            "active_custom_strategies": len(self.self_ref.list_active_strategies()),
            "paper_trade_results": paper_trade_results if paper_trade_results else None,
            "population_summary": self.population.summary(),
            "meta_changes": meta_changes,
            "strategy_effectiveness": self.tracker.strategy_effectiveness(),
            "generation_progress": self.tracker.generation_progress(),
            "dead_end_count": len(self.tracker.dead_end_patterns()),
            "saved_to": str(gen_path),
        }

        # Save generation report
        report_path = self.archive_root / "generations" / f"report_{gen:04d}.json"
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

        # ── Spark Bridge: emit insights ─────────────────────────
        try:
            spark_bridge.emit_tier1_pulse(gen, report)
            if insights:
                spark_bridge.emit_tier2_patterns(
                    gen, insights, self.tracker.dead_end_patterns(),
                )
            champion_data = spark_bridge.detect_champion_change(report)
            if champion_data:
                spark_bridge.emit_tier3_breakthrough(
                    gen, "new_champion", champion_data,
                )
            if paper_trade_results:
                for pt in paper_trade_results:
                    if pt.get("status") == "validated":
                        spark_bridge.emit_tier3_breakthrough(
                            gen, "paper_trade_validation", pt,
                        )
        except Exception as e:
            logger.debug("Spark bridge error (non-fatal): %s", e)

        # ── Plateau Detection & Temperature Shock ────────────────
        try:
            pop_best = report.get("population_summary", {}).get("best_wr", 0)
            if pop_best > self._plateau_best_wr:
                self._plateau_best_wr = pop_best
                self._plateau_gen_start = gen
                if self._plateau_shock_active:
                    logger.info(
                        "Plateau broken! New best WR=%.4f -- ending shock early",
                        pop_best,
                    )
                    self._plateau_shock_active = False

            plateau_gens = gen - self._plateau_gen_start

            if (
                not self._plateau_shock_active
                and plateau_gens >= self._PLATEAU_THRESHOLD
                and gen > self._plateau_shock_end_gen
            ):
                # Activate temperature shock
                self._plateau_shock_active = True
                self._plateau_shock_end_gen = gen + self._SHOCK_DURATION
                for name, params in self.meta_agent.strategy_params.items():
                    params.temperature = max(params.temperature, 2.0)
                    params.diversity_weight = max(params.diversity_weight, 0.95)
                    params.exploitation_weight = 1.0 - params.diversity_weight
                logger.info(
                    "PLATEAU SHOCK ACTIVATED (stagnant %d gens): "
                    "temperature=2.0+, diversity=0.95 for %d gens",
                    plateau_gens, self._SHOCK_DURATION,
                )
            elif self._plateau_shock_active and gen >= self._plateau_shock_end_gen:
                # Deactivate shock
                self._plateau_shock_active = False
                logger.info("Plateau shock ended (ran %d gens)", self._SHOCK_DURATION)
        except Exception as e:
            logger.debug("Plateau detection error (non-fatal): %s", e)

        self._print_report(report)
        return report

    def run(self, generations: int = 10) -> list[dict]:
        """Run multiple generations of evolution."""
        pop_summary = self.population.summary()
        spark_bridge.init_bridge(
            current_best_wr=pop_summary.get("best_wr", 0),
            current_best_id="",
        )

        total = self.current_generation + generations
        reports = []
        for i in range(generations):
            report = self.run_generation(total_generations=total)
            reports.append(report)

            # Log progress
            pop = self.population.summary()
            logger.info(
                "Generation %d complete: %d elite, %d viable, best WR=%.3f",
                self.current_generation,
                pop.get("elite", 0),
                pop.get("viable", 0),
                pop.get("best_wr", 0),
            )

        return reports

    # ── Seed Population ────────────────────────────────────────

    def seed_from_existing(self) -> int:
        """Seed the population from existing spark-researcher candidates.

        Imports the current project.json candidates as generation 0.
        Returns number of agents seeded.
        """
        config_path = self.trading_root / "spark-researcher.project.json"
        if not config_path.exists():
            logger.warning("No spark-researcher.project.json found at %s", config_path)
            return 0

        config = json.loads(config_path.read_text(encoding="utf-8"))
        candidates = config.get("candidate_trials", [])

        seeded = 0
        for candidate in candidates:
            mutations = candidate.get("mutations", {})
            if not mutations:
                continue

            agent = Agent(
                agent_id="",
                mutations=mutations,
                meta_strategy="seed_existing",
                generation=0,
            )

            if not self.population.is_duplicate(mutations):
                self.population.add_agent(agent)
                seeded += 1

        if seeded > 0:
            self.population.save_generation(0)
            logger.info("Seeded %d agents from existing candidates", seeded)

        return seeded

    def seed_champion_family(self) -> int:
        """Seed with the known champion and its WF=1.0 variants.

        These are our empirically validated elite agents.
        Evaluates each seed agent so the population has real fitness scores.
        """
        champions = [
            {
                "name": "champion",
                "mutations": {
                    "doctrine_id": "compression_mean_reversion",
                    "strategy_id": "compression_range_bounce",
                    "asset_universe": "BTC",
                    "session_quality_filter": "skip_compression_toxic",
                },
            },
            {
                "name": "loose-setup",
                "mutations": {
                    "doctrine_id": "compression_mean_reversion",
                    "strategy_id": "compression_range_bounce",
                    "asset_universe": "BTC",
                    "session_quality_filter": "skip_compression_toxic",
                    "cr_loose_setup": "skip_marginal",
                },
            },
            {
                "name": "wick-guard",
                "mutations": {
                    "doctrine_id": "compression_mean_reversion",
                    "strategy_id": "compression_range_bounce",
                    "asset_universe": "BTC,SOL",
                    "session_quality_filter": "skip_compression_toxic",
                    "cr_wick_guard": "reject_high",
                },
            },
            {
                "name": "down-in-downtrend",
                "mutations": {
                    "doctrine_id": "compression_mean_reversion",
                    "strategy_id": "compression_range_bounce",
                    "asset_universe": "BTC,SOL",
                    "session_quality_filter": "skip_compression_toxic",
                    "cr_down_in_downtrend": "skip_deep",
                },
            },
            {
                "name": "btc-noncomp-toxic-wick",
                "mutations": {
                    "doctrine_id": "compression_mean_reversion",
                    "strategy_id": "compression_range_bounce",
                    "asset_universe": "BTC",
                    "session_quality_filter": "skip_compression_toxic",
                    "cr_wick_guard": "reject_high",
                    "extend_regimes": "trend,event_driven,range,high_vol,fear_shock",
                },
            },
        ]

        seeded = 0
        for champ in champions:
            if self.population.is_duplicate(champ["mutations"]):
                continue

            agent = Agent(
                agent_id="",
                mutations=champ["mutations"],
                meta_strategy="seed_champion",
                generation=0,
            )

            # Evaluate seed agents so population has real fitness
            logger.info("Evaluating seed agent: %s", champ["name"])
            try:
                fitness = evaluate_agent(agent.mutations, self.trading_root)
                agent.fitness = fitness
                logger.info(
                    "  %s: WR=%.3f WF=%.1f DD=%.3f trades=%d",
                    champ["name"],
                    fitness.get("win_rate", 0),
                    fitness.get("wealth_factor", 0),
                    fitness.get("max_drawdown", 1),
                    fitness.get("trade_count", 0),
                )
            except Exception as e:
                logger.error("  %s evaluation failed: %s", champ["name"], e)

            self.population.add_agent(agent)
            seeded += 1

        if seeded > 0:
            self.population.save_generation(0)
            logger.info("Seeded and evaluated %d champion agents", seeded)

        return seeded

    # ── Status & Reporting ─────────────────────────────────────

    def status(self) -> dict:
        """Return current evolution status."""
        return {
            "generation": self.current_generation,
            "population": self.population.summary(),
            "strategy_effectiveness": self.tracker.strategy_effectiveness(),
            "generation_progress": self.tracker.generation_progress(),
            "dead_ends": self.tracker.dead_end_patterns(),
            "best_strategies": self.tracker.best_strategies(),
            "actionable_insights": self.synthesizer.get_actionable_insights(),
            "insights_summary": self.synthesizer.format_for_meta_agent(),
            "transfer_effectiveness": self.transfer.transfer_effectiveness(),
            "calibrated_gates": self.diagnosis.get_calibrated_gates(),
            "active_custom_strategies": self.self_ref.list_active_strategies(),
            "meta_state": {
                name: params.to_dict()
                for name, params in self.meta_agent.strategy_params.items()
            },
        }

    def _print_report(self, report: dict) -> None:
        """Pretty-print a generation report."""
        print(f"\n{'='*60}")
        print(f"  GENERATION {report['generation']} REPORT")
        print(f"{'='*60}")
        print(f"  Elapsed: {report['elapsed_seconds']:.1f}s")
        print(f"  Evaluated: {report['variants_evaluated']} variants")
        staged = report.get("staged_eval")
        if staged:
            print(f"  Staged eval: {staged.get('quick_reject', 0)} quick-rejected, "
                  f"{staged.get('medium_reject', 0)} medium-rejected, "
                  f"{staged.get('full', 0)} full-evaluated")
        print(f"  New elite: {report['new_elite']}")
        print(f"  New viable: {report['new_viable']}")

        pop = report["population_summary"]
        if pop.get("size", 0) > 0:
            print(f"\n  Population: {pop['size']} agents")
            print(f"    Elite: {pop.get('elite', 0)}")
            print(f"    Viable: {pop.get('viable', 0)}")
            print(f"    Best WR: {pop.get('best_wr', 0):.3f}")
            print(f"    Avg WR: {pop.get('avg_wr', 0):.3f}")

        effectiveness = report.get("strategy_effectiveness", {})
        if effectiveness:
            print(f"\n  Meta-Strategy Effectiveness:")
            for name, stats in sorted(
                effectiveness.items(),
                key=lambda x: x[1].get("improvement_rate", 0),
                reverse=True,
            ):
                print(
                    f"    {name}: {stats['improvement_rate']:.0%} improvement "
                    f"({stats['improvements']}/{stats['attempts']}), "
                    f"avg WR={stats['avg_wr']:.3f}"
                )

        if report.get("meta_changes"):
            print(f"\n  Meta-Evolution Changes:")
            for name, change in report["meta_changes"].items():
                print(f"    {name}: {change['action']}")

        progress = report.get("generation_progress", [])
        if len(progress) > 1:
            first = progress[0]["best_wr"]
            last = progress[-1]["best_wr"]
            delta = last - first
            print(f"\n  Progress: best WR {first:.3f} -> {last:.3f} ({delta:+.3f})")

        print(f"{'='*60}\n")
