"""Meta Agent -- the self-modifiable brain of the evolution system.

DGM-H core principle: the meta-level modification procedure is itself editable.
This module generates new mutation dicts using evolvable meta-strategies,
and can modify its own strategy parameters based on performance feedback.

The meta-agent doesn't generate Python code (like full DGM-H with LLMs).
Instead, it generates mutation dicts using parameterized meta-strategies
whose parameters themselves evolve based on what works.
"""

from __future__ import annotations

import copy
import json
import math
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .population import Agent, PopulationArchive
from .performance_tracker import PerformanceTracker

# -- Known mutation space (from domain knowledge) -----------------------

# These are the mutation keys our signal engine understands
MUTATION_KEYS = {
    "doctrine_id": [
        "compression_mean_reversion",
        "trend_regime_following",
        "event_driven_fade",
        "range_session_reclaim",
        "breakout_impulse_squeeze",
        "wedge_guarded",
        # NEW - 151 Trading Strategies (Kakushadze & Serur)
        "momentum_trend_follow",
        "extreme_reversion",
        "volatility_breakout_fade",
    ],
    "strategy_id": [
        "compression_range_bounce",
        "ema_pullback_long",
        "event_fade",
        "wick_reversal",
        "bollinger_squeeze_breakout",
        "wedge_exhaustion_reversal",
        # NEW - 151 Trading Strategies (Kakushadze & Serur)
        "momentum_fade",
        "rsi_extreme_reversion",
        "ema_crossover_fade",
        "range_extreme_fade",
        "channel_breakout_fade",
        "contrarian_overextension_fade",
        "trend_pullback_entry",
        "multi_confirm_bounce",
        "vwap_reversion",
        # Session 25: 3 strategies found in backtest.py but missing from evolution
        "keltner_mean_reversion",
        "volume_exhaustion_reversal",
        "climax_reversal",
        # Session 25: 3 strategies from WF08 extract (main repo cycle 914)
        "range_reclaim_scalp",
        "intermarket_context_gate",
        "participation_gate_overlay",
    ],
    "asset_universe": ["BTC", "ETH", "SOL", "BTC,ETH", "BTC,SOL", "BTC,ETH,SOL"],
    "timeframe": ["15m", "1h", "4h"],
    "session_quality_filter": ["skip_compression_toxic", ""],
    "market_regime": ["compression", "trend", "event_driven", "range", "high_vol", "fear_shock"],
}

# Guard mutations (continuous or categorical)
GUARD_MUTATIONS = {
    # Original 6
    "cr_wick_guard": ["reject_high", "reject_moderate", ""],
    "cr_down_in_downtrend": ["skip_deep", "skip", ""],
    "drawdown_guard": ["moderate", "tight", ""],
    "volume_guard": ["moderate", "tight", ""],
    "cr_loose_setup": ["skip_marginal", "skip_marginal_strict", ""],
    "cr_downtrend_high_pos": ["skip", "skip_strict", ""],
    # High priority (strong empirical evidence)
    "cr_bounce_confirm": ["require_late_turn", "require_late_turn_strict", ""],  # 90.9% WR interaction
    "cr_volume_cap": ["spike_skip", "moderate_cap", ""],  # 0% WR kill zone at high vol
    "cr_wick_downtrend": ["skip", "skip_broad", ""],  # WR=0.662 after filter
    # Medium priority
    "cr_compression_deadzone": ["skip_mid", ""],  # 47.8% WR dead zone
    "cr_impulse_reversal": ["skip_reversal", "skip_reversal_gentle", ""],
    "cr_wick_near_high": ["skip", "skip_strict", ""],
    "cr_weak_reclaim": ["skip_weak", "skip_weak_broad", ""],
    # Lower priority
    "cr_body_wick_conflict": ["skip", ""],
    "cr_flat_trend": ["skip_flat", "skip_flat_tight", ""],
    "cr_rsi_band": ["sweet_spot", "tight_sweet", ""],
    # -- NEW: 151 Trading Strategies guards --
    # Contrarian overextension fade
    "co_momentum_threshold": ["standard", "extreme", ""],
    "co_reclaim_floor": ["standard", "strict", ""],
    "co_fear_shock_allow": ["off", "allow"],
    # Trend pullback entry
    "tp_trend_strength": ["standard", "strong", ""],
    "tp_pullback_depth": ["shallow", "deep", ""],
    "tp_wick_confirm": ["off", "require"],
    # Range extreme fade
    "rf_location_threshold": ["standard", "extreme", ""],
    "rf_range_floor": ["standard", "wide", ""],
    "rf_volume_guard": ["off", "skip_spike"],
    # RSI extreme reversion
    "re_rsi_threshold": ["extreme", "deep_extreme", ""],
    "re_wick_confirm": ["off", "require_wick"],
    "re_momentum_cap": ["standard", "tight", ""],
    # Momentum continuation
    "mc_momentum_floor": ["standard", "aggressive", "conservative"],
    "mc_rsi_band": ["wide", "standard", "tight"],
    "mc_volume_confirm": ["off", "require_above_avg"],
    # EMA crossover follow
    "ec_gap_ceiling": ["standard", "wide", ""],
    "ec_impulse_confirm": ["off", "require_late"],
    "ec_volatility_floor": ["off", "minimum"],
    # Channel breakout momentum
    "cb_momentum_floor": ["standard", "aggressive", ""],
    "cb_volatility_floor": ["standard", "low", ""],
    "cb_volume_confirm": ["standard", "strict"],
    # -- NEW: Confirmation guards (expanded indicators) --
    "cr_atr_guard": ["skip_high_atr", "skip_very_high", ""],
    "cr_bb_confirm": ["require_extreme", "require_moderate", ""],
    "cr_bb_squeeze": ["require_squeeze", "require_tight", ""],
    "cr_vwap_confirm": ["require_discount", "require_distance", ""],
    "cr_stoch_confirm": ["require_oversold", "require_turning", ""],
    "cr_obv_confirm": ["require_aligned", "require_strong", ""],
    "cr_macd_confirm": ["require_decel", "require_turn", ""],
    "cr_rsi_2h_confirm": ["require_aligned", "require_extreme", ""],
    "cr_fib_confirm": ["near_fib", "strict_fib", ""],
    # VWAP reversion strategy
    "vr_deviation_threshold": ["standard", "wide", ""],
    "vr_atr_cap": ["standard", "tight", ""],
    # -- NEW: Forge indicator guards (from sibling repo edge research) --
    # These indicators are already computed in backtest.py but never used in evolution
    "cr_cci_guard": ["skip_dead_zone", "skip_extreme", "require_aligned", "skip_narrow", ""],
    "cr_williams_guard": ["skip_neutral", "skip_wide_neutral", "require_aligned", ""],
    "cr_adx_guard": ["skip_no_trend", ""],
    "cr_keltner_guard": ["require_extreme", "skip_inside", ""],
    "cr_cmf_guard": ["skip_weak_flow", ""],
    # -- Session 25: Quant indicator guards (Renaissance-inspired) --
    "cr_hurst_guard": ["skip_random", "skip_trending", "require_mean_revert", ""],
    "cr_entropy_guard": ["skip_high_entropy", "skip_very_high", ""],
    "cr_autocorr_guard": ["skip_positive", "skip_negative", ""],
    "cr_volume_delta_guard": ["skip_against_delta", "require_aligned", ""],
    "cr_rv_ratio_guard": ["skip_expanding", "skip_contracting", ""],
    "cr_parkinson_guard": ["skip_high_vol", "skip_low_vol", ""],
}

# Profile-level mutations (strategy configs from _signal)
PROFILE_MUTATIONS = {
    # Original 5
    "activation_profile": ["base", "conservative", "aggressive"],
    "compression_profile": ["base", "tight", "loose"],
    "no_trade_window": ["off", "asian", "close"],
    "volume_context_guard": ["off", "require_above_avg", "skip_spike"],
    "counter_trend_guard": ["off", "skip_strong", "skip_moderate"],
    # Session 25: 13 hidden profile mutations discovered in backtest.py _signal()
    "execution_buffer": ["base", "high"],
    "late_sample_guard": ["off", "on"],
    "direction_filter": ["all", "long_only", "short_only"],
    "session_profile": ["all", "squeeze_release_window", "trend_quality_window",
                        "opening_range_failure", "triple_screen_alignment",
                        "trend_session_alignment"],
    "impulse_profile": ["base", "expansion_follow_through", "pivot_release",
                        "opening_reversal", "adaptive_efficiency"],
    "reversal_confirmation": ["base", "reclaim_close", "edge_reclaim_close",
                              "wick_reclaim_close"],
    "bounce_confirmation": ["off", "close_location", "strong_bounce"],
    "range_edge_profile": ["base", "local_extreme_only"],
    "wick_profile": ["base", "rejection_confirm"],
    "chase_policy": ["base", "no_chase_after_crowded_good_news"],
    "follow_through_profile": ["base", "delayed_confirmation"],
    "catalyst_failure_mode": ["base", "sell_the_news_failure_fade"],
    "event_interpretation_policy": ["base", "wait_for_follow_through"],
}

# Regime extension (the Session 18 discovery)
REGIME_SETS = [
    "",  # default (compression only)
    "trend",
    "event_driven",
    "range",
    "trend,event_driven",
    "trend,event_driven,range",
    "trend,event_driven,range,high_vol,fear_shock",
]


@dataclass
class MetaStrategyParams:
    """Evolvable parameters for a meta-strategy.

    These parameters control HOW the meta-strategy generates new mutations.
    The meta-agent can modify these based on performance feedback.
    """

    mutation_rate: float = 0.3  # probability of mutating each key
    crossover_rate: float = 0.5  # probability of taking from parent2 in crossover
    guard_add_prob: float = 0.2  # probability of adding a new guard
    guard_remove_prob: float = 0.1  # probability of removing a guard
    regime_extend_prob: float = 0.15  # probability of extending regimes
    diversity_weight: float = 0.8  # foraging mode: heavily reward novelty
    exploitation_weight: float = 0.2  # 20% exploit, 80% explore
    temperature: float = 1.0  # selection temperature (higher = more random)

    def mutate_self(self, learning_rate: float = 0.05) -> MetaStrategyParams:
        """Self-modify: small random perturbations to meta-parameters.

        This is the metacognitive self-modification from DGM-H.
        """
        new_params = copy.deepcopy(self)
        for attr in [
            "mutation_rate", "crossover_rate", "guard_add_prob",
            "guard_remove_prob", "regime_extend_prob", "diversity_weight",
            "temperature",
        ]:
            current = getattr(new_params, attr)
            delta = random.gauss(0, learning_rate)
            setattr(new_params, attr, max(0.01, min(0.99, current + delta)))

        # Keep exploitation + diversity = 1.0
        new_params.exploitation_weight = 1.0 - new_params.diversity_weight
        return new_params

    def to_dict(self) -> dict:
        return {
            k: v for k, v in self.__dict__.items()
        }

    @classmethod
    def from_dict(cls, d: dict) -> MetaStrategyParams:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class MetaAgent:
    """The meta-level agent that generates new mutation strategies.

    Implements multiple meta-strategies, each with evolvable parameters.
    Tracks which strategies work and adapts accordingly.
    """

    def __init__(
        self,
        population: PopulationArchive,
        tracker: PerformanceTracker,
    ):
        self.population = population
        self.tracker = tracker

        # Each meta-strategy has its own evolvable parameters
        self.strategy_params: dict[str, MetaStrategyParams] = {
            "perturbation": MetaStrategyParams(mutation_rate=0.25),
            "crossover": MetaStrategyParams(crossover_rate=0.5),
            "feature_guided": MetaStrategyParams(mutation_rate=0.15, guard_add_prob=0.4),
            "regime_transfer": MetaStrategyParams(regime_extend_prob=0.5),
            "dead_end_avoidance": MetaStrategyParams(mutation_rate=0.2),
            "random_exploration": MetaStrategyParams(mutation_rate=0.6, temperature=2.0),
        }

        # Strategy selection weights (evolve based on effectiveness)
        self._strategy_weights: dict[str, float] = {
            name: 1.0 for name in self.strategy_params
        }

    # -- Agent Generation -----------------------------------------------

    def generate_agents(
        self,
        count: int = 10,
        generation: int = 0,
        total_generations: int | None = None,
    ) -> list[Agent]:
        """Generate a batch of new agent variants using meta-strategies.

        Selects meta-strategies probabilistically based on their effectiveness,
        then uses each strategy to generate new mutation dicts.

        If total_generations is provided, applies compute-aware planning:
        - Early (0-30%): explore broadly (high temperature, more random)
        - Middle (30-70%): balanced
        - Late (70-100%): exploit best strategies (low temperature, top strategies)
        """
        # Apply compute-aware planning if we know the budget
        if total_generations and total_generations > 0:
            self._apply_compute_planning(generation, total_generations)

        agents = []
        dead_ends = {p["pattern"] for p in self.tracker.dead_end_patterns()}

        # Reserve 80% of slots for minority-strategy foraging.
        # Only 20% of compute goes to refining dominant strategies.
        minority_slots = max(2, count * 8 // 10)
        normal_slots = count - minority_slots

        # -- Phase 1: minority-reserved slots --
        pop = self.population.population
        if pop:
            strategy_counts: dict[str, int] = {}
            for a in pop:
                sid = a.mutations.get("strategy_id", "")
                strategy_counts[sid] = strategy_counts.get(sid, 0) + 1
            sorted_strats = sorted(strategy_counts, key=strategy_counts.get, reverse=True)
            top2 = set(sorted_strats[:2]) if len(sorted_strats) >= 2 else set()
            minority_pop = [a for a in pop if a.mutations.get("strategy_id", "") not in top2]

            for _ in range(minority_slots * 2):
                if len(agents) >= minority_slots:
                    break
                strategy_name = self._select_strategy()
                params = self.strategy_params[strategy_name]
                # Force parent from minority pool
                parent = None
                if minority_pop:
                    cands = random.sample(minority_pop, min(3, len(minority_pop)))
                    parent = max(cands, key=lambda a: a.win_rate)
                if parent is None:
                    parent = self._select_parent(params)
                new_mutations = self._apply_strategy(
                    strategy_name, params, parent, dead_ends
                )
                if self.population.is_duplicate(new_mutations):
                    continue
                agent = Agent(
                    agent_id="",
                    mutations=new_mutations,
                    meta_strategy=strategy_name,
                    parent_id=parent.agent_id if parent else None,
                    generation=generation,
                )
                agents.append(agent)

        # -- Phase 2: normal slots --
        max_attempts = normal_slots * 2
        for _ in range(max_attempts):
            if len(agents) >= count:
                break

            # Select meta-strategy (weighted by effectiveness)
            strategy_name = self._select_strategy()
            params = self.strategy_params[strategy_name]

            # Select parent(s)
            parent = self._select_parent(params)

            # Generate new mutations using the selected strategy
            new_mutations = self._apply_strategy(
                strategy_name, params, parent, dead_ends
            )

            # Skip if duplicate
            if self.population.is_duplicate(new_mutations):
                continue

            agent = Agent(
                agent_id="",  # auto-computed from mutations
                mutations=new_mutations,
                meta_strategy=strategy_name,
                parent_id=parent.agent_id if parent else None,
                generation=generation,
            )
            agents.append(agent)

        return agents

    def _apply_compute_planning(
        self, generation: int, total_generations: int
    ) -> None:
        """DGM-H compute-aware planning: adjust exploration vs exploitation.

        Early runs explore broadly to discover the fitness landscape.
        Late runs exploit the best-known strategies for refinement.
        """
        progress = generation / max(1, total_generations)

        if progress < 0.3:
            # Early: explore broadly -- boost random exploration, high temperature
            self._compute_phase = "explore"
            self.strategy_params["random_exploration"].temperature = 2.5
            self.strategy_params["perturbation"].temperature = 1.5
            self.strategy_params["perturbation"].mutation_rate = min(
                0.5, self.strategy_params["perturbation"].mutation_rate * 1.3
            )
            # Give exploration strategies a weight boost
            self._strategy_weights["random_exploration"] = max(
                1.0, self._strategy_weights.get("random_exploration", 1.0)
            )
        elif progress > 0.7:
            # Late: exploit best -- focus on top strategies, low temperature
            self._compute_phase = "exploit"
            best = self.tracker.best_strategies(top_n=2)
            for name in self.strategy_params:
                if name in best:
                    self.strategy_params[name].temperature = max(
                        0.3, self.strategy_params[name].temperature * 0.7
                    )
                    self._strategy_weights[name] = max(
                        1.5, self._strategy_weights.get(name, 1.0) * 1.2
                    )
                else:
                    # Penalize non-top strategies late in the run
                    self._strategy_weights[name] = max(
                        0.2, self._strategy_weights.get(name, 1.0) * 0.5
                    )
            # Reduce random exploration late
            self.strategy_params["random_exploration"].temperature = 0.5
            self._strategy_weights["random_exploration"] = 0.2
        else:
            # Middle: balanced -- standard behavior
            self._compute_phase = "balanced"

    # -- Meta-Strategy Implementations ----------------------------------

    def _apply_strategy(
        self,
        strategy_name: str,
        params: MetaStrategyParams,
        parent: Agent | None,
        dead_ends: set[str],
    ) -> dict[str, Any]:
        """Apply a meta-strategy to generate new mutations."""
        if strategy_name == "perturbation":
            return self._perturbation(params, parent, dead_ends)
        elif strategy_name == "crossover":
            return self._crossover(params, parent, dead_ends)
        elif strategy_name == "feature_guided":
            return self._feature_guided(params, parent, dead_ends)
        elif strategy_name == "regime_transfer":
            return self._regime_transfer(params, parent, dead_ends)
        elif strategy_name == "dead_end_avoidance":
            return self._dead_end_avoidance(params, parent, dead_ends)
        elif strategy_name == "random_exploration":
            return self._random_exploration(params, dead_ends)
        else:
            return self._perturbation(params, parent, dead_ends)

    def _perturbation(
        self, params: MetaStrategyParams, parent: Agent | None, dead_ends: set
    ) -> dict:
        """Small random changes to parent mutation values."""
        if parent is None:
            return self._random_exploration(params, dead_ends)

        mutations = copy.deepcopy(parent.mutations)

        # Mutate each key with probability mutation_rate
        for key, options in {**MUTATION_KEYS, **GUARD_MUTATIONS}.items():
            if random.random() < params.mutation_rate:
                mutations[key] = random.choice(options)

        # Profile mutations at half rate
        for key, options in PROFILE_MUTATIONS.items():
            if random.random() < params.mutation_rate * 0.5:
                mutations[key] = random.choice(options)

        # Maybe extend regimes
        if random.random() < params.regime_extend_prob:
            mutations["extend_regimes"] = random.choice(REGIME_SETS)

        return self._filter_dead_ends(mutations, dead_ends)

    def _crossover(
        self, params: MetaStrategyParams, parent: Agent | None, dead_ends: set
    ) -> dict:
        """Combine mutations from two successful parents.

        Strategy-locked crossover: when parents have different strategy_ids,
        the child inherits strategy_id and doctrine_id from the minority
        parent (less common strategy in the population). This lets the
        dominant strategy's optimised guards flow into minority strategies
        instead of always absorbing them.
        """
        # 85% of crossovers force a minority-strategy parent (foraging mode)
        force_niche = random.random() < 0.85
        parents = self._select_parents(2, force_niche=force_niche)
        if len(parents) < 2:
            return self._perturbation(params, parent, dead_ends)

        p1, p2 = parents[0].mutations, parents[1].mutations
        child = {}

        # All keys from both parents
        all_keys = set(p1.keys()) | set(p2.keys())
        for key in all_keys:
            if random.random() < params.crossover_rate:
                child[key] = p2.get(key, p1.get(key))
            else:
                child[key] = p1.get(key, p2.get(key))

        # Strategy-lock: if parents have different strategies, child keeps
        # the minority strategy's identity keys (strategy_id + doctrine_id).
        # This prevents competitive exclusion where the dominant strategy
        # always absorbs alternatives.
        s1 = p1.get("strategy_id", "")
        s2 = p2.get("strategy_id", "")
        if s1 != s2:
            pop = self.population.population
            c1 = sum(1 for a in pop if a.mutations.get("strategy_id") == s1)
            c2 = sum(1 for a in pop if a.mutations.get("strategy_id") == s2)
            minority = p2 if c2 <= c1 else p1
            child["strategy_id"] = minority["strategy_id"]
            if "doctrine_id" in minority:
                child["doctrine_id"] = minority["doctrine_id"]

        return self._filter_dead_ends(child, dead_ends)

    def _feature_guided(
        self, params: MetaStrategyParams, parent: Agent | None, dead_ends: set
    ) -> dict:
        """Use domain knowledge to guide mutation direction.

        Encodes our empirical findings:
        - Removal guards (wick, volume, toxic) > additive confirmations
        - Gentle guards (<30 trade removal) > aggressive ones
        - WF=1.0 is non-negotiable
        """
        if parent is None:
            # 20% chance: start from new strategies to force exploration
            if random.random() < 0.20:
                new_strategy = random.choice([
                    "multi_confirm_bounce", "vwap_reversion",
                ])
                mutations = {
                    "doctrine_id": "compression_mean_reversion",
                    "strategy_id": new_strategy,
                    "asset_universe": random.choice(["BTC", "ETH", "BTC,ETH"]),
                    "session_quality_filter": "skip_compression_toxic",
                }
                if new_strategy == "vwap_reversion":
                    mutations["vr_deviation_threshold"] = random.choice(["standard", "wide"])
                    mutations["vr_atr_cap"] = random.choice(["standard", "tight"])
            else:
                mutations = {
                    "doctrine_id": "compression_mean_reversion",
                    "strategy_id": "compression_range_bounce",
                    "asset_universe": random.choice(["BTC", "BTC,SOL", "BTC,ETH,SOL"]),
                    "session_quality_filter": "skip_compression_toxic",
                }
        else:
            mutations = copy.deepcopy(parent.mutations)

        # Feature-guided: prefer adding gentle removal guards
        # 30% of the time, specifically pick a new confirmation guard
        _NEW_CONFIRM_GUARDS = [
            "cr_atr_guard", "cr_bb_confirm", "cr_bb_squeeze",
            "cr_vwap_confirm", "cr_stoch_confirm", "cr_obv_confirm",
            "cr_macd_confirm", "cr_rsi_2h_confirm", "cr_fib_confirm",
        ]

        if random.random() < params.guard_add_prob:
            if random.random() < 0.30:
                guard = random.choice(_NEW_CONFIRM_GUARDS)
            else:
                guard = random.choice(list(GUARD_MUTATIONS.keys()))
            options = [o for o in GUARD_MUTATIONS[guard] if o]  # exclude empty
            if options:
                mutations[guard] = random.choice(options)

        # Feature-guided: sometimes add a profile mutation
        if random.random() < params.guard_add_prob * 0.5:
            profile = random.choice(list(PROFILE_MUTATIONS.keys()))
            options = [o for o in PROFILE_MUTATIONS[profile] if o != "base" and o != "off"]
            if options:
                mutations[profile] = random.choice(options)

        # Feature-guided: sometimes remove a guard (test if it's helping)
        if random.random() < params.guard_remove_prob:
            active_guards = [
                k for k in GUARD_MUTATIONS
                if k in mutations and mutations[k]
            ]
            if active_guards:
                mutations[random.choice(active_guards)] = ""

        return self._filter_dead_ends(mutations, dead_ends)

    def _regime_transfer(
        self, params: MetaStrategyParams, parent: Agent | None, dead_ends: set
    ) -> dict:
        """Apply successful patterns from one regime to another.

        DGM-H transfer learning: meta-level improvements transfer across domains.
        In our case, "domains" = market regimes.
        """
        # Find elite agents and transfer their guard patterns to new regimes
        elite = self.population.elite
        if not elite:
            return self._random_exploration(params, dead_ends)

        # 45% chance: source from minority-strategy elite for diversity
        source = None
        if random.random() < 0.45:
            strategy_counts: dict[str, int] = {}
            for a in elite:
                sid = a.mutations.get("strategy_id", "")
                strategy_counts[sid] = strategy_counts.get(sid, 0) + 1
            if len(strategy_counts) > 1:
                dominant = max(strategy_counts, key=strategy_counts.get)
                minority_elite = [a for a in elite
                                  if a.mutations.get("strategy_id", "") != dominant]
                if minority_elite:
                    source = random.choice(minority_elite)

        if source is None:
            source = random.choice(elite)
        mutations = copy.deepcopy(source.mutations)

        # Change regime while keeping the guards
        mutations["extend_regimes"] = random.choice(
            [r for r in REGIME_SETS if r != mutations.get("extend_regimes", "")]
        )

        # Maybe change asset
        if random.random() < 0.3:
            mutations["asset_universe"] = random.choice(MUTATION_KEYS["asset_universe"])

        return self._filter_dead_ends(mutations, dead_ends)

    def _dead_end_avoidance(
        self, params: MetaStrategyParams, parent: Agent | None, dead_ends: set
    ) -> dict:
        """Steer away from known failure modes.

        Uses performance tracker's dead_end_patterns to avoid repeating failures.
        """
        if parent is None:
            mutations = self._random_exploration(params, dead_ends)
        else:
            mutations = copy.deepcopy(parent.mutations)

        # Aggressively filter dead ends
        mutations = self._filter_dead_ends(mutations, dead_ends)

        # Additionally, perturbate away from dead-end-adjacent values
        for pattern in dead_ends:
            if "=" in pattern:
                key, val = pattern.split("=", 1)
                if key in mutations and str(mutations[key]) == val:
                    # Replace with a different value
                    if key in MUTATION_KEYS:
                        alternatives = [
                            o for o in MUTATION_KEYS[key] if str(o) != val
                        ]
                        if alternatives:
                            mutations[key] = random.choice(alternatives)
                    elif key in GUARD_MUTATIONS:
                        alternatives = [
                            o for o in GUARD_MUTATIONS[key] if str(o) != val
                        ]
                        if alternatives:
                            mutations[key] = random.choice(alternatives)
                    elif key in PROFILE_MUTATIONS:
                        alternatives = [
                            o for o in PROFILE_MUTATIONS[key] if str(o) != val
                        ]
                        if alternatives:
                            mutations[key] = random.choice(alternatives)

        return mutations

    def _random_exploration(
        self, params: MetaStrategyParams, dead_ends: set
    ) -> dict:
        """Pure exploration: random mutation dict from scratch."""
        mutations = {
            "doctrine_id": random.choice(MUTATION_KEYS["doctrine_id"]),
            "strategy_id": random.choice(MUTATION_KEYS["strategy_id"]),
            "asset_universe": random.choice(MUTATION_KEYS["asset_universe"]),
            "timeframe": random.choice(MUTATION_KEYS["timeframe"]),
        }

        # Random guards
        for guard, options in GUARD_MUTATIONS.items():
            if random.random() < params.guard_add_prob:
                mutations[guard] = random.choice(options)

        # Random profiles (lower probability)
        for profile, options in PROFILE_MUTATIONS.items():
            if random.random() < params.guard_add_prob * 0.3:
                mutations[profile] = random.choice(options)

        # Random regime extension
        if random.random() < params.regime_extend_prob:
            mutations["extend_regimes"] = random.choice(REGIME_SETS)

        return self._filter_dead_ends(mutations, dead_ends)

    # -- Selection ------------------------------------------------------

    def _select_strategy(self) -> str:
        """Select a meta-strategy using softmax weighted by effectiveness."""
        # Update weights from performance tracker
        effectiveness = self.tracker.strategy_effectiveness()
        for name in self._strategy_weights:
            if name in effectiveness:
                rate = effectiveness[name]["improvement_rate"]
                # Blend historical rate with base weight
                self._strategy_weights[name] = 0.5 + rate
            else:
                # Unexplored strategies get exploration bonus
                self._strategy_weights[name] = 1.0

        # Softmax selection
        names = list(self._strategy_weights.keys())
        weights = [self._strategy_weights[n] for n in names]
        total = sum(weights)
        probs = [w / total for w in weights]

        return random.choices(names, weights=probs, k=1)[0]

    def _select_parent(self, params: MetaStrategyParams) -> Agent | None:
        """Select a parent agent for reproduction.

        DGM-H: probabilistic, weighted by fitness, with diversity incentives.
        Downweights agents with many children.
        20% chance of selecting from minority strategies to maintain diversity.
        """
        pop = self.population.population
        if not pop:
            return None

        # 80% chance: select from minority strategies (foraging mode)
        if random.random() < 0.80:
            strategy_counts: dict[str, int] = {}
            for a in pop:
                sid = a.mutations.get("strategy_id", "")
                strategy_counts[sid] = strategy_counts.get(sid, 0) + 1
            if len(strategy_counts) > 1:
                # Exclude top-2 dominant strategies to give minorities a real chance
                sorted_strats = sorted(strategy_counts, key=strategy_counts.get, reverse=True)
                top2 = set(sorted_strats[:2])
                minority = [a for a in pop
                            if a.mutations.get("strategy_id", "") not in top2]
                if minority:
                    # Tournament among minorities (size 3)
                    candidates = random.sample(minority, min(3, len(minority)))
                    parent = max(candidates, key=lambda a: a.win_rate)
                    parent.children_count += 1
                    return parent

        # Standard fitness-proportional selection
        scores = []
        for agent in pop:
            fitness_score = agent.win_rate * params.exploitation_weight
            children_penalty = 1.0 / (1.0 + agent.children_count * 0.1)
            diversity_bonus = params.diversity_weight * (
                1.0 / (1.0 + agent.children_count)
            )
            scores.append(
                (fitness_score + diversity_bonus) * children_penalty
            )

        # Temperature-controlled selection
        if params.temperature > 0:
            exp_scores = [
                math.exp(s / params.temperature) for s in scores
            ]
            total = sum(exp_scores)
            probs = [e / total for e in exp_scores]
        else:
            probs = [1.0 if s == max(scores) else 0.0 for s in scores]
            total = sum(probs)
            probs = [p / total for p in probs]

        parent = random.choices(pop, weights=probs, k=1)[0]
        parent.children_count += 1
        return parent

    def _select_parents(self, n: int, force_niche: bool = False) -> list[Agent]:
        """Select n distinct parents.

        If force_niche=True, the first parent is drawn exclusively from
        minority strategies (non-dominant strategy_id). This ensures
        non-dominant strategies get crossover opportunities even when they
        represent <1% of the population.
        """
        pop = self.population.population
        if len(pop) < n:
            return pop

        parents = []
        used_ids = set()

        # Niche selection: first parent from minority strategy (exclude top-2)
        if force_niche:
            strategy_counts: dict[str, int] = {}
            for a in pop:
                sid = a.mutations.get("strategy_id", "")
                strategy_counts[sid] = strategy_counts.get(sid, 0) + 1
            sorted_strats = sorted(strategy_counts, key=strategy_counts.get, reverse=True)
            top2 = set(sorted_strats[:2])

            minority = [a for a in pop
                        if a.mutations.get("strategy_id", "") not in top2]
            if minority:
                candidates = random.sample(minority, min(3, len(minority)))
                best = max(candidates, key=lambda a: a.win_rate)
                parents.append(best)
                used_ids.add(best.agent_id)

        # Fill remaining parent slots with tournament selection
        for _ in range(n - len(parents)):
            candidates = random.sample(pop, min(3, len(pop)))
            candidates = [c for c in candidates if c.agent_id not in used_ids]
            if not candidates:
                break
            best = max(candidates, key=lambda a: a.win_rate)
            parents.append(best)
            used_ids.add(best.agent_id)

        return parents

    # -- Helpers ---------------------------------------------------------

    # Keys that must never be stripped by dead-end filtering
    _PROTECTED_KEYS = {"strategy_id", "asset_universe", "timeframe"}

    def _filter_dead_ends(self, mutations: dict, dead_ends: set) -> dict:
        """Remove mutation values that are known dead ends.

        Protected keys (strategy_id, asset_universe, timeframe) are never
        stripped as removing them produces malformed agents. doctrine_id is
        allowed to permute via dead-end filtering to enable cross-doctrine
        discovery (Gen 405 found extreme_reversion on CRB = +2% WR).
        """
        filtered = {}
        for k, v in mutations.items():
            pattern = f"{k}={v}"
            if pattern not in dead_ends or k in self._PROTECTED_KEYS:
                filtered[k] = v
        return filtered

    # -- Meta-Evolution (Self-Modification) -----------------------------

    def evolve_meta_strategies(self) -> dict[str, Any]:
        """Self-modify meta-strategy parameters based on performance.

        This is the DGM-H metacognitive self-modification: the system
        modifies its own improvement mechanisms.

        Returns summary of changes made.
        """
        effectiveness = self.tracker.strategy_effectiveness()
        changes = {}

        for name, params in self.strategy_params.items():
            if name not in effectiveness:
                continue

            stats = effectiveness[name]

            # If strategy has been tried enough (>10 attempts)
            if stats["attempts"] >= 10:
                rate = stats["improvement_rate"]

                if rate > 0.3:
                    # Successful strategy: fine-tune (small perturbation)
                    new_params = params.mutate_self(learning_rate=0.02)
                    changes[name] = {"action": "fine_tune", "rate": rate}
                elif rate < 0.1:
                    # Failing strategy: big perturbation to escape local optima
                    new_params = params.mutate_self(learning_rate=0.15)
                    changes[name] = {"action": "escape_local_optima", "rate": rate}
                else:
                    # Moderate: standard self-modification
                    new_params = params.mutate_self(learning_rate=0.05)
                    changes[name] = {"action": "standard_evolve", "rate": rate}

                self.strategy_params[name] = new_params

        return changes

    # -- Persistence ----------------------------------------------------

    def save_state(self, path: Path) -> None:
        """Save meta-agent state (strategy params + weights)."""
        state = {
            "strategy_params": {
                name: params.to_dict()
                for name, params in self.strategy_params.items()
            },
            "strategy_weights": self._strategy_weights,
        }
        path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    def load_state(self, path: Path) -> None:
        """Load meta-agent state from disk."""
        if not path.exists():
            return
        state = json.loads(path.read_text(encoding="utf-8"))
        for name, params_dict in state.get("strategy_params", {}).items():
            if name in self.strategy_params:
                self.strategy_params[name] = MetaStrategyParams.from_dict(params_dict)
        self._strategy_weights = state.get("strategy_weights", self._strategy_weights)
