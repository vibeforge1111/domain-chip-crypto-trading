#!/usr/bin/env python3
"""Paper trade validation for elite agents.

Supports two modes:
  One-shot:  python run_paper_trade.py --top 5 --save
  Daemon:    python run_paper_trade.py --daemon --interval 120 --batch-size 5

The daemon mode runs continuously alongside evolution, testing many
agents and building PT coverage across the elite population.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

from hyperagent.population import PopulationArchive

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("paper_trade")

EVOLUTION_ROOT = Path(__file__).resolve().parent
ARCHIVE_ROOT = EVOLUTION_ROOT / "archive"

# Resolve trading root lazily to avoid import-time failures
_trading_root_cache: Path | None = None


def _get_trading_root(override: Path | None = None) -> Path:
    global _trading_root_cache
    if override:
        return override
    if _trading_root_cache is None:
        from hyperagent.evaluator import TRADING_CHIP_ROOT
        _trading_root_cache = TRADING_CHIP_ROOT
    return _trading_root_cache


def _import_pt_func(trading_root: Path):
    """Import run_paper_trade_validation from the backtest engine."""
    sys.path.insert(0, str(trading_root / "src"))
    from domain_chip_crypto_trading.backtest import run_paper_trade_validation
    return run_paper_trade_validation


def _safe_jsonl_append(path: Path, entry: dict):
    """Append a single JSONL entry with minimal lock window."""
    line = json.dumps(entry) + "\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())


def _atomic_json_write(path: Path, data):
    """Write JSON atomically via tmp + replace (with Windows retry)."""
    import time as _time
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    for attempt in range(5):
        try:
            tmp.replace(path)
            return
        except PermissionError:
            if attempt < 4:
                _time.sleep(1 + attempt)
            else:
                # Last resort: direct write instead of atomic replace
                path.write_text(json.dumps(data, indent=2), encoding="utf-8")
                try:
                    tmp.unlink(missing_ok=True)
                except OSError:
                    pass


# ── PT Score & Status ──────────────────────────────────────────

def compute_pt_score(entry: dict) -> float:
    """Composite PT score combining WR, trade count, consistency, and delta."""
    pt_wr = entry.get("pt_wr_avg", 0)
    trades = entry.get("pt_trades_total", 0)
    std = entry.get("pt_wr_std", 1.0)
    delta = entry.get("pt_delta_avg", 0)

    wr_component = min(1.0, pt_wr / 0.80)
    trade_component = min(1.0, trades / 50)
    consistency = max(0, 1.0 - std * 10)
    delta_component = 0.5 + min(0.5, max(-0.5, delta * 5))

    return round(
        wr_component * 0.35
        + trade_component * 0.25
        + consistency * 0.20
        + delta_component * 0.20,
        4,
    )


def classify_status(entry: dict) -> str:
    """Classify agent PT status: needs_more_data / validated / live_ready."""
    run_count = entry.get("run_count", 0)
    trades = entry.get("pt_trades_total", 0)
    delta = entry.get("pt_delta_avg", 0)
    pt_wr = entry.get("pt_wr_avg", 0)
    std = entry.get("pt_wr_std", 1.0)

    if run_count < 3 or trades < 15:
        return "needs_more_data"
    if delta <= -0.03:
        return "needs_more_data"
    # validated
    if pt_wr >= 0.65 and trades >= 30 and std < 0.05:
        return "live_ready"
    return "validated"


# ── Paper Trade Daemon ─────────────────────────────────────────

class PaperTradeDaemon:
    """Continuous paper trade validation running alongside evolution."""

    def __init__(
        self,
        interval: int = 120,
        batch_size: int = 5,
        archive_root: Path | None = None,
        trading_root: Path | None = None,
        filter_tf: str | None = None,
    ):
        self.interval = interval
        self.batch_size = batch_size
        self.archive_root = archive_root or ARCHIVE_ROOT
        self.trading_root = trading_root or _get_trading_root()
        self.filter_tf = filter_tf  # e.g. "15m", "1h" -- None = all
        # Use separate state/results files per timeframe to avoid conflicts
        suffix = f"_{filter_tf}" if filter_tf else ""
        self.state_path = self.archive_root / f"pt_state{suffix}.json"
        self.history_path = self.archive_root / "paper_trade_history.jsonl"  # shared, append-only
        self.results_path = self.archive_root / f"paper_trade_results{suffix}.json"
        self.insights_path = self.archive_root / f"pt_insights{suffix}.jsonl"
        self.cycle_count = 0
        self._agent_index: dict[str, dict] = {}
        self._pt_func = None

    def run(self):
        """Main daemon loop -- runs until KeyboardInterrupt."""
        self._pt_func = _import_pt_func(self.trading_root)
        self._load_state()

        tf_label = self.filter_tf or "all"
        logger.info(
            "PT Daemon started. interval=%ds, batch=%d, tf=%s, pid=%d",
            self.interval, self.batch_size, tf_label, os.getpid(),
        )
        logger.info("  Archive: %s", self.archive_root)
        logger.info("  Trading: %s", self.trading_root)
        logger.info("  State: %s", self.state_path.name)
        logger.info(
            "  Loaded state: %d agents in index, %d cycles completed",
            len(self._agent_index), self.cycle_count,
        )

        self._save_state("running")

        try:
            while True:
                self._run_cycle()
                logger.info(
                    "Cycle %d complete. Next in %ds. Coverage: %d agents tested.",
                    self.cycle_count, self.interval, len(self._agent_index),
                )
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logger.info("PT Daemon stopped by user after %d cycles", self.cycle_count)
            self._save_state("stopped")

    def _run_cycle(self):
        """One PT cycle: select agents, test them, record results."""
        # 1. Load current population (fresh read each cycle, retry on file conflicts)
        import time as _time
        pop = PopulationArchive(
            archive_root=self.archive_root, max_archive_size=100,
        )
        for attempt in range(3):
            try:
                gen_num, _ = pop.load_latest()
                break
            except (json.JSONDecodeError, OSError) as e:
                if attempt < 2:
                    logger.warning("Population load failed (attempt %d): %s - retrying in 5s", attempt + 1, e)
                    _time.sleep(5)
                else:
                    logger.error("Population load failed after 3 attempts: %s - skipping cycle", e)
                    return

        elite = pop.elite
        if not elite:
            logger.warning("No elite agents found. Skipping cycle.")
            return

        # 2. Select candidates
        candidates = self._select_candidates(elite, gen_num)
        if not candidates:
            logger.info("No new candidates to test this cycle.")
            return

        logger.info(
            "Cycle %d: testing %d agents (gen %d, %d elite total)",
            self.cycle_count + 1, len(candidates), gen_num, len(elite),
        )

        # 3. Paper trade each candidate
        cycle_results = []
        for agent in candidates:
            aid = agent.agent_id
            bt_wr = agent.win_rate
            try:
                pt_result = self._pt_func(
                    agent.mutations, self.trading_root, max_contracts=960,
                )
            except Exception as e:
                logger.error("  PT failed for %s: %s", aid[:8], e)
                continue

            if pt_result.get("status") == "pending_data":
                logger.info("  %s: pending data (skipped)", aid[:8])
                continue

            pt_wr = pt_result.get("win_rate", 0)
            pt_trades = pt_result.get("trade_count", 0)
            delta = pt_wr - bt_wr

            # Update agent index
            bt_trades = agent.fitness.get("trade_count", 0) if agent.fitness else 0
            self._update_agent_index(
                aid, bt_wr, pt_wr, pt_trades, delta, gen_num,
                agent.mutations, agent.meta_strategy, bt_trades=bt_trades,
            )

            cycle_results.append({
                "agent_id": aid,
                "backtest_wr": round(bt_wr, 4),
                "paper_trade_wr": round(pt_wr, 4),
                "delta": round(delta, 4),
                "paper_trade_trades": pt_trades,
                "validation": "PASS" if delta > -0.02 else "WARN" if delta > -0.05 else "FAIL",
            })

            status = self._agent_index[aid]["status"]
            logger.info(
                "  %s: BT=%.3f PT=%.3f delta=%+.3f trades=%d [%s]",
                aid[:8], bt_wr, pt_wr, delta, pt_trades, status,
            )

        # 4. Append to history
        if cycle_results:
            history_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "generation": gen_num,
                "source": "pt_daemon",
                "cycle": self.cycle_count + 1,
                "agents": cycle_results,
            }
            _safe_jsonl_append(self.history_path, history_entry)

        # 5. Update results.json (top 20 by PT score)
        self._update_results()

        # 6. Save daemon state
        self.cycle_count += 1
        self._save_state("running", total_elite=len(elite))

        # 7. PT insights every 10 cycles
        if self.cycle_count % 10 == 0:
            self._synthesize_pt_insights()

    def _select_candidates(self, elite, current_gen: int):
        """Priority-based agent selection for paper trading.

        Priority 1: Elite agents never paper traded (by BT WR desc)
        Priority 2: Stale agents (not tested in 100+ gens, by BT WR desc)
        Priority 3: Recently bred elite (born in last 50 gens, by BT WR desc)

        If filter_tf is set, only considers agents matching that timeframe.
        """
        tested_ids = set(self._agent_index.keys())

        never_tested = []
        stale = []
        fresh_elite = []

        for agent in elite:
            # Timeframe filter
            if self.filter_tf:
                agent_tf = agent.mutations.get("timeframe", "") if agent.mutations else ""
                if agent_tf != self.filter_tf:
                    continue
            aid = agent.agent_id
            if aid not in tested_ids:
                never_tested.append(agent)
            else:
                entry = self._agent_index[aid]
                gens_since = current_gen - entry.get("last_tested_gen", 0)
                if gens_since > 100:
                    stale.append(agent)
                elif agent.generation > current_gen - 50:
                    fresh_elite.append(agent)

        # Sort each pool by BT win rate descending
        never_tested.sort(key=lambda a: a.win_rate, reverse=True)
        stale.sort(key=lambda a: a.win_rate, reverse=True)
        fresh_elite.sort(key=lambda a: a.win_rate, reverse=True)

        pool = never_tested + stale + fresh_elite
        return pool[: self.batch_size]

    def _update_agent_index(
        self,
        agent_id: str,
        bt_wr: float,
        pt_wr: float,
        pt_trades: int,
        delta: float,
        gen: int,
        mutations: dict | None = None,
        meta_strategy: str = "",
        bt_trades: int = 0,
    ):
        """Update the running PT index for an agent."""
        if agent_id not in self._agent_index:
            self._agent_index[agent_id] = {
                "run_count": 0,
                "pt_wr_history": [],
                "pt_trades_total": 0,
                "bt_trades": bt_trades,
                "bt_wr": bt_wr,
                "meta_strategy": meta_strategy,
                "mutations": mutations or {},
                "first_tested_gen": gen,
            }
        if bt_trades:
            self._agent_index[agent_id]["bt_trades"] = bt_trades

        entry = self._agent_index[agent_id]
        entry["run_count"] += 1
        entry["pt_wr_history"].append(round(pt_wr, 4))
        entry["pt_trades_total"] += pt_trades
        entry["bt_wr"] = bt_wr
        entry["last_tested_gen"] = gen
        entry["last_tested_ts"] = datetime.now(timezone.utc).isoformat()

        # Compute running stats
        wrs = entry["pt_wr_history"]
        entry["pt_wr_avg"] = round(sum(wrs) / len(wrs), 4)
        if len(wrs) > 1:
            mean = entry["pt_wr_avg"]
            entry["pt_wr_std"] = round(
                math.sqrt(sum((w - mean) ** 2 for w in wrs) / (len(wrs) - 1)), 4,
            )
        else:
            entry["pt_wr_std"] = 0.0
        entry["pt_delta_avg"] = round(entry["pt_wr_avg"] - bt_wr, 4)

        # Compute composite score and status
        entry["pt_score"] = compute_pt_score(entry)
        entry["status"] = classify_status(entry)

    def _update_results(self):
        """Write top 20 PT agents to paper_trade_results.json."""
        scored = []
        for aid, entry in self._agent_index.items():
            if entry.get("run_count", 0) >= 1:
                scored.append({
                    "agent_id": aid,
                    "meta_strategy": entry.get("meta_strategy", ""),
                    "bt_wr": entry["bt_wr"],
                    "pt_wr_avg": entry.get("pt_wr_avg", 0),
                    "pt_wr_std": entry.get("pt_wr_std", 0),
                    "pt_trades_total": entry.get("pt_trades_total", 0),
                    "run_count": entry.get("run_count", 0),
                    "pt_delta_avg": entry.get("pt_delta_avg", 0),
                    "pt_score": entry.get("pt_score", 0),
                    "status": entry.get("status", "needs_more_data"),
                    "last_tested_ts": entry.get("last_tested_ts", ""),
                    "pt_wr_history": entry.get("pt_wr_history", []),
                    "mutations": entry.get("mutations", {}),
                })

        scored.sort(key=lambda x: x["pt_score"], reverse=True)
        _atomic_json_write(self.results_path, scored[:20])

    def _save_state(self, status: str, total_elite: int | None = None):
        """Write daemon state to pt_state.json."""
        tested_count = len(self._agent_index)
        elite_count = total_elite or tested_count  # approximate if unknown

        # Build a slim agent index (keep key trading info, drop full mutations)
        slim_index = {}
        _KEEP_MUTATION_KEYS = {"asset_universe", "timeframe", "strategy_id"}
        for aid, entry in self._agent_index.items():
            slim = {k: v for k, v in entry.items() if k != "mutations"}
            m = entry.get("mutations", {})
            if m:
                slim["asset"] = m.get("asset_universe", "?")
                slim["timeframe"] = m.get("timeframe", "?")
                slim["strategy"] = m.get("strategy_id", "?")
            slim_index[aid] = slim

        state = {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "daemon_status": status,
            "daemon_pid": os.getpid(),
            "cycle_count": self.cycle_count,
            "cycle_interval_seconds": self.interval,
            "batch_size": self.batch_size,
            "coverage": {
                "total_elite": elite_count,
                "tested_agents": tested_count,
                "coverage_pct": round(
                    tested_count / max(1, elite_count), 4,
                ),
            },
            "agent_pt_index": slim_index,
        }
        _atomic_json_write(self.state_path, state)

    def _load_state(self):
        """Load previous daemon state if it exists."""
        if self.state_path.exists():
            try:
                state = json.loads(self.state_path.read_text(encoding="utf-8"))
                self.cycle_count = state.get("cycle_count", 0)
                # Restore agent index
                for aid, entry in state.get("agent_pt_index", {}).items():
                    self._agent_index[aid] = entry
                logger.info(
                    "Loaded previous state: %d cycles, %d agents indexed",
                    self.cycle_count, len(self._agent_index),
                )
            except Exception as e:
                logger.warning("Could not load pt_state.json: %s", e)

        # Backfill asset/timeframe/strategy from population for old entries
        needs_backfill = [
            aid for aid, d in self._agent_index.items()
            if not d.get("asset") or d["asset"] == "?"
        ]
        if needs_backfill:
            try:
                pop = PopulationArchive(
                    archive_root=self.archive_root, max_archive_size=100,
                )
                pop.load_latest()
                pop_lookup = {a.agent_id: a for a in pop.elite}
                filled = 0
                for aid in needs_backfill:
                    agent = pop_lookup.get(aid)
                    if agent and agent.mutations:
                        m = agent.mutations
                        self._agent_index[aid]["asset"] = m.get("asset_universe", "?")
                        self._agent_index[aid]["timeframe"] = m.get("timeframe", "?")
                        self._agent_index[aid]["strategy"] = m.get("strategy_id", "?")
                        self._agent_index[aid]["mutations"] = m
                        filled += 1
                if filled:
                    logger.info("Backfilled asset/tf/strategy for %d/%d agents", filled, len(needs_backfill))
            except Exception as e:
                logger.warning("Could not backfill agent metadata: %s", e)

    def _synthesize_pt_insights(self):
        """Extract patterns from PT data every 10 cycles."""
        insights = []

        # Which guards appear in top PT agents
        top_pt = sorted(
            self._agent_index.items(),
            key=lambda x: x[1].get("pt_score", 0),
            reverse=True,
        )[:20]

        guard_counts: dict[str, int] = {}
        for _aid, data in top_pt:
            mutations = data.get("mutations", {})
            for k, v in mutations.items():
                if k.startswith("cr_") or k.endswith("_guard") or k.endswith("_filter"):
                    key = f"{k}={v}"
                    guard_counts[key] = guard_counts.get(key, 0) + 1

        if guard_counts:
            top_guards = sorted(guard_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            insights.append({
                "type": "pt_guard_pattern",
                "insight": f"Top PT guards: {', '.join(g[0] for g in top_guards)}",
                "guards": dict(top_guards),
                "cycle": self.cycle_count,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        # PT > BT correlation
        deltas = [
            d.get("pt_delta_avg", 0)
            for d in self._agent_index.values()
            if d.get("run_count", 0) >= 2
        ]
        if deltas:
            avg_delta = sum(deltas) / len(deltas)
            insights.append({
                "type": "pt_calibration",
                "insight": f"Avg PT delta: {avg_delta:+.3f} across {len(deltas)} agents",
                "avg_delta": round(avg_delta, 4),
                "agents_with_2plus_runs": len(deltas),
                "cycle": self.cycle_count,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        # Status distribution
        statuses: dict[str, int] = {}
        for entry in self._agent_index.values():
            s = entry.get("status", "needs_more_data")
            statuses[s] = statuses.get(s, 0) + 1
        if statuses:
            insights.append({
                "type": "pt_status_distribution",
                "insight": f"Status: {statuses}",
                "statuses": statuses,
                "cycle": self.cycle_count,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        for ins in insights:
            _safe_jsonl_append(self.insights_path, ins)
        if insights:
            logger.info("  Synthesized %d PT insights", len(insights))


# ── One-Shot Mode (original) ──────────────────────────────────

def run_one_shot(args):
    """Original one-shot paper trade validation."""
    trading_root = args.trading_root or _get_trading_root()
    run_paper_trade_validation = _import_pt_func(trading_root)

    pop = PopulationArchive(archive_root=ARCHIVE_ROOT, max_archive_size=100)
    pop.load_latest()

    elite = pop.elite
    if not elite:
        print("No elite agents found in population.")
        sys.exit(0)

    elite_sorted = sorted(elite, key=lambda a: a.win_rate, reverse=True)
    top_agents = elite_sorted[: args.top]

    print(f"\nPaper Trade Validation: Top {len(top_agents)} Elite Agents")
    print(f"Trading data: {trading_root}")
    print(f"{'='*70}")
    print(
        f"{'Agent ID':<12} {'Strategy':<18} {'BT WR':>7} {'PT WR':>7} "
        f"{'Delta':>7} {'PT Trades':>9} {'Status'}"
    )
    print(f"{'-'*70}")

    results = []
    for agent in top_agents:
        bt_wr = agent.win_rate
        pt_readiness = (
            agent.fitness.get("paper_trade_readiness", 0) if agent.fitness else 0
        )
        pt_result = run_paper_trade_validation(
            agent.mutations, trading_root, max_contracts=960,
        )
        pt_wr = pt_result.get("win_rate", 0)
        pt_trades = pt_result.get("trade_count", 0)
        pt_status = pt_result.get("status", "unknown")
        delta = pt_wr - bt_wr

        if pt_status == "pending_data":
            status_str = "NO DATA"
        elif delta > -0.02:
            status_str = "PASS"
        elif delta > -0.05:
            status_str = "WARN"
        else:
            status_str = "FAIL"

        print(
            f"{agent.agent_id[:12]:<12} {agent.meta_strategy:<18} "
            f"{bt_wr:>7.3f} {pt_wr:>7.3f} {delta:>+7.3f} {pt_trades:>9} {status_str}"
        )

        results.append({
            "agent_id": agent.agent_id,
            "meta_strategy": agent.meta_strategy,
            "mutations": agent.mutations,
            "backtest_wr": round(bt_wr, 4),
            "paper_trade_wr": round(pt_wr, 4),
            "delta": round(delta, 4),
            "paper_trade_trades": pt_trades,
            "paper_trade_status": pt_status,
            "validation": status_str,
            "paper_trade_readiness": round(pt_readiness, 3),
            "paper_trade_details": {
                k: v for k, v in pt_result.items() if k not in ("decisions",)
            },
        })

    print(f"{'='*70}")

    valid_results = [r for r in results if r["paper_trade_status"] != "pending_data"]
    if valid_results:
        avg_delta = sum(r["delta"] for r in valid_results) / len(valid_results)
        pass_count = sum(1 for r in valid_results if r["validation"] == "PASS")
        print(f"\nSummary: {pass_count}/{len(valid_results)} passed")
        print(f"Average BT->PT delta: {avg_delta:+.3f}")

        if avg_delta < -0.03:
            print("WARNING: Significant over-estimation bias detected.")
        elif avg_delta > 0.01:
            print("Paper trade WR exceeds backtest - conservative estimates.")
        else:
            print("Backtest and paper trade are well-calibrated.")
    else:
        print("\nNo paper trade data available.")

    if args.save and results:
        save_path = ARCHIVE_ROOT / "paper_trade_results.json"
        save_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"\nResults saved to {save_path}")

        history_path = ARCHIVE_ROOT / "paper_trade_history.jsonl"
        history_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "one_shot",
            "top_n": args.top,
            "pass_count": pass_count if valid_results else 0,
            "total_validated": len(valid_results) if valid_results else 0,
            "avg_delta": round(avg_delta, 4) if valid_results else None,
            "agents": [
                {
                    "agent_id": r["agent_id"],
                    "backtest_wr": r["backtest_wr"],
                    "paper_trade_wr": r["paper_trade_wr"],
                    "delta": r["delta"],
                    "paper_trade_trades": r["paper_trade_trades"],
                    "validation": r["validation"],
                }
                for r in results
            ],
        }
        with open(history_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(history_entry) + "\n")
        print(f"History appended to {history_path}")


# ── Status Command ─────────────────────────────────────────────

def show_status():
    """Print current PT daemon state."""
    state_path = ARCHIVE_ROOT / "pt_state.json"
    if not state_path.exists():
        print("No PT state file found. Daemon has not been run yet.")
        return

    state = json.loads(state_path.read_text(encoding="utf-8"))
    cov = state.get("coverage", {})
    idx = state.get("agent_pt_index", {})

    print(f"\nPT Daemon Status")
    print(f"{'='*60}")
    print(f"  Status:     {state.get('daemon_status', 'unknown')}")
    print(f"  PID:        {state.get('daemon_pid', '?')}")
    print(f"  Cycles:     {state.get('cycle_count', 0)}")
    print(f"  Interval:   {state.get('cycle_interval_seconds', '?')}s")
    print(f"  Batch size: {state.get('batch_size', '?')}")
    print(f"  Updated:    {state.get('last_updated', '?')}")
    print(f"\nCoverage")
    print(f"  Elite total:   {cov.get('total_elite', '?')}")
    print(f"  Agents tested: {cov.get('tested_agents', 0)}")
    print(f"  Coverage:      {cov.get('coverage_pct', 0):.1%}")

    # Status breakdown
    statuses: dict[str, int] = {}
    for entry in idx.values():
        s = entry.get("status", "needs_more_data")
        statuses[s] = statuses.get(s, 0) + 1
    print(f"\nAgent Status")
    for s in ["live_ready", "validated", "needs_more_data"]:
        print(f"  {s}: {statuses.get(s, 0)}")

    # Top 5 by PT score
    top5 = sorted(idx.items(), key=lambda x: x[1].get("pt_score", 0), reverse=True)[:5]
    if top5:
        print(f"\nTop 5 by PT Score")
        print(f"  {'Agent':<12} {'BT WR':>7} {'PT WR':>7} {'Score':>6} {'Runs':>5} {'Status'}")
        for aid, data in top5:
            print(
                f"  {aid[:12]:<12} {data.get('bt_wr',0):>7.3f} "
                f"{data.get('pt_wr_avg',0):>7.3f} {data.get('pt_score',0):>6.3f} "
                f"{data.get('run_count',0):>5} {data.get('status','?')}"
            )
    print()


# ── CLI Entry Point ────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Paper trade validation for elite agents",
    )
    parser.add_argument(
        "--top", "-n", type=int, default=5,
        help="Number of top elite agents to paper trade (default: 5)",
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Save results to archive/paper_trade_results.json",
    )
    parser.add_argument(
        "--trading-root", type=Path, default=None,
        help="Override path to domain-chip-crypto-trading",
    )
    # Daemon mode
    parser.add_argument(
        "--daemon", action="store_true",
        help="Run continuously alongside evolution",
    )
    parser.add_argument(
        "--interval", type=int, default=120,
        help="Seconds between PT cycles in daemon mode (default: 120)",
    )
    parser.add_argument(
        "--batch-size", type=int, default=5,
        help="Agents per cycle in daemon mode (default: 5)",
    )
    parser.add_argument(
        "--filter-tf", type=str, default=None,
        help="Only paper trade agents with this timeframe (e.g. 15m, 1h, 4h). "
             "Run multiple daemons with different --filter-tf for parallel coverage.",
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Show current PT daemon state and exit",
    )

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.daemon:
        daemon = PaperTradeDaemon(
            interval=args.interval,
            batch_size=args.batch_size,
            trading_root=args.trading_root or _get_trading_root(),
            filter_tf=args.filter_tf,
        )
        daemon.run()
    else:
        run_one_shot(args)


if __name__ == "__main__":
    main()
