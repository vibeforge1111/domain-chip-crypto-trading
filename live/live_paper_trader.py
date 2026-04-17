"""Live Paper Trader — real-time predictions against Binance market data.

Uses an Observer pattern: MarketObserver detects the current market regime,
StrategyRegistry matches it to relevant strategies, and AgentPool invokes
only the agents whose strategies fit the current conditions.

No API key needed, no real money involved. Pure observation + prediction.

Usage:
    python live_paper_trader.py --assets BTC --per-strategy 3
    python live_paper_trader.py --assets BTC,ETH,SOL --per-strategy 5 --daemon
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import tempfile
import time
from collections import deque
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Callable

import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Path setup — same pattern as evaluator.py
# ---------------------------------------------------------------------------
TRADING_CHIP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TRADING_CHIP_ROOT / "src"))
sys.path.insert(0, str(TRADING_CHIP_ROOT))

from domain_chip_crypto_trading.backtest import (
    Candle,
    ContractWindow,
    _detected_regime,
    _feature_row,
    _signal,
    _wider_context,
    _window_candles,
)
from hyperagent.population import PopulationArchive
from hyperagent.evaluator import _load_guard_for_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

ARCHIVE_DIR = Path(__file__).resolve().parent / "archive"
LOG_PATH = ARCHIVE_DIR / "live_pt_log.jsonl"
STATE_PATH = ARCHIVE_DIR / "live_pt_state.json"


# ═══════════════════════════════════════════════════════════════════════════
# BinanceFeed — polls public klines endpoint
# ═══════════════════════════════════════════════════════════════════════════

class BinanceFeed:
    SYMBOLS = {"BTC": "BTCUSDT", "ETH": "ETHUSDT", "SOL": "SOLUSDT"}
    BASE_URL = "https://api.binance.com/api/v3/klines"

    def fetch_candles(self, asset: str, limit: int = 5) -> list[Candle]:
        symbol = self.SYMBOLS.get(asset.upper())
        if not symbol:
            logger.warning("Unknown asset %s", asset)
            return []
        url = f"{self.BASE_URL}?symbol={symbol}&interval=1m&limit={limit}"
        for attempt in range(2):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "DGM-H-LivePT/1.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode())
                candles = []
                for row in data:
                    # Binance kline: [open_time, open, high, low, close, volume, ...]
                    ts = datetime.fromtimestamp(row[0] / 1000, tz=timezone.utc)
                    candles.append(Candle(
                        ts=ts,
                        open=float(row[1]),
                        high=float(row[2]),
                        low=float(row[3]),
                        close=float(row[4]),
                        volume=float(row[5]),
                    ))
                return candles
            except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
                if attempt == 0:
                    logger.warning("Binance fetch failed (retrying): %s", e)
                    time.sleep(2)
                else:
                    logger.error("Binance fetch failed after retry: %s", e)
        return []


# ═══════════════════════════════════════════════════════════════════════════
# CandleBuffer — rolling deque of 1m candles per asset
# ═══════════════════════════════════════════════════════════════════════════

class CandleBuffer:
    def __init__(self, max_size: int = 300):
        self._candles: deque[Candle] = deque(maxlen=max_size)
        self._seen_ts: set[float] = set()

    def append(self, candles: list[Candle]) -> int:
        added = 0
        for c in candles:
            ts_key = c.ts.timestamp()
            if ts_key not in self._seen_ts:
                self._candles.append(c)
                self._seen_ts.add(ts_key)
                added += 1
                # Keep seen_ts bounded to maxlen
                if len(self._seen_ts) > self._candles.maxlen * 2:
                    oldest_ts = min(self._seen_ts)
                    self._seen_ts.discard(oldest_ts)
        return added

    def get_candles(self) -> list[Candle]:
        return list(self._candles)

    def get_candle_times(self) -> list[float]:
        return [c.ts.timestamp() for c in self._candles]

    def ready(self) -> bool:
        return len(self._candles) >= 26  # minimum for MACD in _feature_row

    def __len__(self) -> int:
        return len(self._candles)


# ═══════════════════════════════════════════════════════════════════════════
# ContractSimulator — synthetic contracts from live prices (multi-timeframe)
# ═══════════════════════════════════════════════════════════════════════════

# Timeframe config: candle count and settlement boundaries
TIMEFRAMES = {
    "15m": {"candles": 15, "minutes": 15},
    "1h":  {"candles": 60, "minutes": 60},
    "4h":  {"candles": 240, "minutes": 240},
}


class ContractSimulator:
    @staticmethod
    def create_contract(
        candles_window: list[Candle], asset: str, timeframe: str = "15m",
    ) -> ContractWindow | None:
        if len(candles_window) < 2:
            return None
        open_price = candles_window[0].open
        close_price = candles_window[-1].close
        direction = "up" if close_price > open_price else "down"
        open_ts = candles_window[0].ts
        close_ts = candles_window[-1].ts
        ts_str = open_ts.strftime("%Y%m%d-%H%M")
        contract_id = f"live-{asset.lower()}-{timeframe}-{ts_str}"
        return ContractWindow(
            contract_id=contract_id,
            open_ts=open_ts,
            close_ts=close_ts,
            reference_price_open=open_price,
            reference_price_close=close_price,
            settlement_direction=direction,
        )


# ═══════════════════════════════════════════════════════════════════════════
# MarketObserver — detects regime from live candle data
# ═══════════════════════════════════════════════════════════════════════════

class MarketObserver:
    """Runs once per 15m boundary to classify market regime."""

    @staticmethod
    def observe(
        candles: list[Candle],
        candle_times: list[float],
        contract: ContractWindow,
    ) -> dict[str, Any]:
        lookback = _window_candles(candles, candle_times, contract)
        if len(lookback) < 5:
            return {"regime": "unknown", "features": {}}
        features = _feature_row(lookback, contract)
        features.update(_wider_context(candles, candle_times, contract))
        regime = _detected_regime(features)
        return {"regime": regime, "features": features}


# ═══════════════════════════════════════════════════════════════════════════
# StrategyRegistry — maps regimes to strategies
# ═══════════════════════════════════════════════════════════════════════════

# Default regime mapping (from _signal() hardcoded gates in backtest.py)
STRATEGY_REGIMES: dict[str, set[str]] = {
    "compression_range_bounce": {"compression"},
    "rsi_extreme_reversion": {"compression", "range", "event_driven", "trend", "high_vol"},
    "multi_confirm_bounce": {"compression", "range"},  # no event_driven in code
    "vwap_reversion": {"range", "compression", "event_driven"},
    "range_extreme_fade": {"range", "compression"},
    "momentum_fade": {"trend", "high_vol", "event_driven"},
    "ema_crossover_fade": {"trend", "range", "event_driven"},
    "channel_breakout_fade": {"high_vol", "event_driven", "range"},
    "contrarian_overextension_fade": {"event_driven", "high_vol"},
    "trend_pullback_entry": {"trend", "event_driven", "high_vol"},
    "bollinger_squeeze_breakout": {"high_vol", "trend", "range", "compression"},
    # Session 25: 3 strategies exist in backtest but were missing from observer
    "keltner_mean_reversion": {"high_vol", "event_driven"},
    "volume_exhaustion_reversal": {"event_driven", "high_vol"},
    "climax_reversal": {"range", "event_driven", "high_vol"},
    # Session 25: strategies from WF08 extract
    "range_reclaim_scalp": {"range", "compression"},  # alias of range_extreme_fade
    "intermarket_context_gate": {"event_driven", "high_vol", "compression"},
    "participation_gate_overlay": {"compression", "range", "event_driven", "trend", "high_vol"},
}


class StrategyRegistry:
    """Maps detected regime to the strategies that accept it."""

    def strategies_for_regime(self, regime: str) -> list[str]:
        if regime == "unknown":
            return []
        return [s for s, regimes in STRATEGY_REGIMES.items() if regime in regimes]


# ═══════════════════════════════════════════════════════════════════════════
# AgentPool — loads elite agents grouped by strategy, invokes on demand
# ═══════════════════════════════════════════════════════════════════════════

class AgentPool:
    """Loads top N agents per strategy+timeframe from the population archive."""

    def __init__(self, per_strategy: int = 5, include_viable: bool = True):
        self.per_strategy = per_strategy
        self.include_viable = include_viable
        # Keyed by "strategy_id" — agents within include timeframe info
        self.agents_by_strategy: dict[str, list[dict[str, Any]]] = {}
        # Keyed by "strategy_id:timeframe" for timeframe-specific lookup
        self.agents_by_strat_tf: dict[str, list[dict[str, Any]]] = {}
        self.all_agents: list[dict[str, Any]] = []
        self.timeframes_loaded: set[str] = set()

    @staticmethod
    def _live_score(agent) -> float:
        """Composite score for live trading: balance WR with trade frequency.

        Agents that trade more often are preferred for live, since ultra-selective
        agents skip everything in real-time conditions.
        """
        wr = agent.win_rate
        tc = agent.fitness.get("trade_count", 0)
        # Normalize trade count (cap at 200 for scoring purposes)
        tc_norm = min(tc, 200) / 200.0
        # 60% WR weight + 40% trade frequency weight
        return wr * 0.6 + tc_norm * 0.4

    def load_agents(self) -> int:
        archive = PopulationArchive()
        archive.load_latest()

        if self.include_viable:
            # Include viable agents (WR > 52%, WF >= 0.8) — they trade more often
            candidates = sorted(archive.viable, key=self._live_score, reverse=True)
            pool_label = "viable+elite"
        else:
            candidates = sorted(archive.elite, key=lambda a: a.win_rate, reverse=True)
            pool_label = "elite"
        elite = candidates  # keep variable name for downstream code

        # Group by strategy + timeframe
        by_strat_tf: dict[str, list] = {}
        for agent in elite:
            sid = agent.mutations.get("strategy_id", "unknown")
            tf = agent.mutations.get("timeframe", "15m")
            key = f"{sid}:{tf}"
            by_strat_tf.setdefault(key, []).append(agent)

        self.agents_by_strategy = {}
        self.agents_by_strat_tf = {}
        self.all_agents = []
        self.timeframes_loaded = set()

        for key, agents in sorted(by_strat_tf.items()):
            sid, tf = key.rsplit(":", 1)
            selected = agents[:self.per_strategy]
            cfgs = []
            for agent in selected:
                guard_fn = _load_guard_for_agent(agent.mutations)
                cfg = {
                    "agent_id": agent.agent_id[:8],
                    "full_id": agent.agent_id,
                    "mutations": agent.mutations,
                    "guard_fn": guard_fn,
                    "bt_wr": agent.win_rate,
                    "strategy": sid,
                    "timeframe": tf,
                }
                cfgs.append(cfg)
                self.all_agents.append(cfg)
            self.agents_by_strat_tf[key] = cfgs
            self.agents_by_strategy.setdefault(sid, []).extend(cfgs)
            self.timeframes_loaded.add(tf)

            guard_count = sum(1 for c in cfgs if c["guard_fn"])
            best_wr = cfgs[0]["bt_wr"] * 100 if cfgs else 0
            logger.info(
                "  %-30s %-4s %d agents (best %.1f%%, %d guarded)",
                sid, tf, len(cfgs), best_wr, guard_count,
            )

        logger.info(
            "  TOTAL: %d agents (%s pool) across %d strategy:timeframe combos, timeframes: %s",
            len(self.all_agents), pool_label, len(self.agents_by_strat_tf),
            sorted(self.timeframes_loaded),
        )
        return len(self.all_agents)

    def get_agents(self, strategy_ids: list[str], timeframe: str | None = None) -> list[dict[str, Any]]:
        """Return agents for given strategies, optionally filtered by timeframe."""
        result = []
        for sid in strategy_ids:
            if timeframe:
                key = f"{sid}:{timeframe}"
                result.extend(self.agents_by_strat_tf.get(key, []))
            else:
                result.extend(self.agents_by_strategy.get(sid, []))
        return result


# ═══════════════════════════════════════════════════════════════════════════
# TradeLogger — writes settlements to JSONL + maintains state JSON
# ═══════════════════════════════════════════════════════════════════════════

class TradeLogger:
    def __init__(self, log_path: Path = LOG_PATH, state_path: Path = STATE_PATH):
        self.log_path = log_path
        self.state_path = state_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_settlement(self, entry: dict[str, Any]) -> None:
        line = json.dumps(entry, default=str) + "\n"
        # Atomic append
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(line)
        except OSError as e:
            logger.error("Failed to write log: %s", e)

    def save_state(self, state: dict[str, Any]) -> None:
        tmp = self.state_path.with_suffix(".tmp")
        try:
            tmp.write_text(json.dumps(state, indent=2, default=str), encoding="utf-8")
            tmp.replace(self.state_path)
        except OSError as e:
            logger.error("Failed to write state: %s", e)
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass

    def load_log(self) -> list[dict[str, Any]]:
        if not self.log_path.exists():
            return []
        entries = []
        for line in self.log_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return entries

    def get_stats(self) -> dict[str, dict[str, Any]]:
        entries = self.load_log()
        stats: dict[str, dict[str, Any]] = {}
        for entry in entries:
            agents = entry.get("agents", {})
            for agent_id, result in agents.items():
                if agent_id not in stats:
                    stats[agent_id] = {
                        "live_trades": 0, "live_wins": 0,
                        "skips": 0, "bt_wr": result.get("bt_wr", 0),
                    }
                pred = result.get("prediction", "skip")
                if pred == "skip":
                    stats[agent_id]["skips"] += 1
                else:
                    stats[agent_id]["live_trades"] += 1
                    if result.get("correct"):
                        stats[agent_id]["live_wins"] += 1
        # Compute win rates
        for agent_id, s in stats.items():
            trades = s["live_trades"]
            s["live_wr"] = s["live_wins"] / trades if trades > 0 else 0.0
            s["delta"] = s["live_wr"] - s["bt_wr"]
        return stats


# ═══════════════════════════════════════════════════════════════════════════
# LivePaperTrader — main daemon
# ═══════════════════════════════════════════════════════════════════════════

class LivePaperTrader:
    # 4h boundary hours (UTC)
    _4H_HOURS = {0, 4, 8, 12, 16, 20}

    def __init__(self, assets: list[str], per_strategy: int = 10, include_viable: bool = True):
        self.assets = [a.upper() for a in assets]
        self.feed = BinanceFeed()
        # 300 candles = 5 hours of 1m data (enough for 4h contracts + lookback)
        self.buffers: dict[str, CandleBuffer] = {a: CandleBuffer(300) for a in self.assets}
        self.observer = MarketObserver()
        self.registry = StrategyRegistry()
        self.pool = AgentPool(per_strategy=per_strategy, include_viable=include_viable)
        self.simulator = ContractSimulator()
        self.logger = TradeLogger()
        # Keyed by "asset:timeframe" -> pending contract info
        self.pending: dict[str, dict[str, Any]] = {}
        self.started_at = datetime.now(timezone.utc)
        self.total_settlements = 0
        self.regime_history: list[str] = []
        self._last_eval_minute: int | None = None  # prevent double-eval
        self._last_reload_hour: int | None = None  # hourly agent reload

    def warmup(self) -> None:
        logger.info("Warming up candle buffers (300 x 1m candles per asset)...")
        for asset in self.assets:
            candles = self.feed.fetch_candles(asset, limit=300)
            self.buffers[asset].append(candles)
            if candles:
                span_min = (candles[-1].ts - candles[0].ts).total_seconds() / 60
                logger.info(
                    "  %s: %d candles loaded (%.0f min span, latest=%s)",
                    asset, len(candles), span_min,
                    candles[-1].ts.strftime("%H:%M:%S UTC"),
                )
            else:
                logger.warning("  %s: NO candles fetched!", asset)

    def run(self) -> None:
        self.warmup()
        n = self.pool.load_agents()
        if n == 0:
            logger.error("No agents loaded. Check population archive.")
            return
        tfs = sorted(self.pool.timeframes_loaded)
        logger.info("Loaded %d agents. Timeframes: %s. Starting on %s", n, tfs, self.assets)
        logger.info("Settlements: 15m=every 15min, 1h=every hour, 4h=every 4 hours")
        logger.info("Press Ctrl+C to stop.\n")

        self._save_state()

        try:
            while True:
                self._tick()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("\nStopped by user. Total settlements: %d", self.total_settlements)

    def _tick(self) -> None:
        now = datetime.now(timezone.utc)

        # 0. Hourly agent reload — pick up new agents from evolution
        if now.minute == 0 and self._last_reload_hour != now.hour:
            self._last_reload_hour = now.hour
            old_count = len(self.pool.all_agents)
            new_count = self.pool.load_agents()
            if new_count != old_count:
                logger.info("Agent reload: %d -> %d agents", old_count, new_count)

        # 1. Fetch latest candles
        for asset in self.assets:
            new = self.feed.fetch_candles(asset, limit=5)
            added = self.buffers[asset].append(new)
            if added > 0:
                logger.debug("%s: +%d candles (buffer=%d)", asset, added, len(self.buffers[asset]))

        # 2. Check for boundaries (15m is the base tick)
        current_minute = now.hour * 60 + now.minute
        if now.minute % 15 == 0 and self._last_eval_minute != current_minute:
            self._last_eval_minute = current_minute

            # Determine which timeframes to evaluate this boundary
            active_tfs = ["15m"]
            if now.minute == 0:
                active_tfs.append("1h")
                if now.hour in self._4H_HOURS:
                    active_tfs.append("4h")

            logger.info("--- %s UTC | timeframes: %s ---", now.strftime("%Y-%m-%d %H:%M"), active_tfs)

            for asset in self.assets:
                if not self.buffers[asset].ready():
                    logger.warning("%s: buffer not ready (%d candles)", asset, len(self.buffers[asset]))
                    continue

                for tf in active_tfs:
                    # Only process if we have agents for this timeframe
                    if tf not in self.pool.timeframes_loaded:
                        continue
                    # Settle previous contract
                    self._settle(asset, tf, now)
                    # Evaluate new contract
                    self._evaluate(asset, tf, now)

            self._save_state()

    def _evaluate(self, asset: str, tf: str, now: datetime) -> None:
        candles = self.buffers[asset].get_candles()
        candle_times = self.buffers[asset].get_candle_times()

        # Get candles for contract window based on timeframe
        tf_minutes = TIMEFRAMES[tf]["minutes"]
        tf_candles = TIMEFRAMES[tf]["candles"]
        recent = [c for c in candles if c.ts >= now - timedelta(minutes=tf_minutes + 1)]
        if len(recent) < max(10, tf_candles // 2):
            recent = candles[-tf_candles:] if len(candles) >= tf_candles else candles

        contract = self.simulator.create_contract(recent, asset, timeframe=tf)
        if contract is None:
            logger.warning("%s/%s: could not create contract", asset, tf)
            return

        # 1. Observer detects regime (once per boundary, reuse for all TFs)
        observation = self.observer.observe(candles, candle_times, contract)
        regime = observation["regime"]
        features = observation["features"]
        if tf == "15m":  # only log regime once per boundary
            self.regime_history.append(regime)
            if len(self.regime_history) > 200:
                self.regime_history = self.regime_history[-200:]

        # 2. Registry matches strategies for this regime
        matched_strategies = self.registry.strategies_for_regime(regime)

        # 3. Pool returns agents for matched strategies AND this timeframe
        agents = self.pool.get_agents(matched_strategies, timeframe=tf)

        if not agents:
            return  # no agents for this strategy:timeframe combo

        # Run matched agents
        predictions: dict[str, dict[str, Any]] = {}
        for agent_cfg in agents:
            prediction = _signal(agent_cfg["mutations"], features)

            # Apply guard if present
            guard_applied = False
            original = prediction
            if agent_cfg["guard_fn"] is not None and prediction != "skip":
                try:
                    prediction = agent_cfg["guard_fn"](features, prediction)
                    if prediction != original:
                        guard_applied = True
                except Exception as e:
                    logger.debug("Guard error for %s: %s", agent_cfg["agent_id"], e)

            predictions[agent_cfg["agent_id"]] = {
                "agent_id": agent_cfg["agent_id"],
                "prediction": prediction,
                "original": original,
                "guard_applied": guard_applied,
                "bt_wr": agent_cfg["bt_wr"],
                "strategy": agent_cfg["strategy"],
                "timeframe": tf,
            }

        # Count predictions
        longs = sum(1 for r in predictions.values() if r["prediction"] == "up")
        shorts = sum(1 for r in predictions.values() if r["prediction"] == "down")
        skips = sum(1 for r in predictions.values() if r["prediction"] == "skip")

        pending_key = f"{asset}:{tf}"
        self.pending[pending_key] = {
            "contract": contract,
            "predictions": predictions,
            "evaluated_at": now,
            "regime": regime,
            "timeframe": tf,
            "strategies_matched": matched_strategies,
        }

        logger.info(
            "  %s/%s | regime=%s | %d agents | %d long, %d short, %d skip",
            asset, tf, regime, len(agents), longs, shorts, skips,
        )

    def _settle(self, asset: str, tf: str, now: datetime) -> None:
        pending_key = f"{asset}:{tf}"
        pending = self.pending.pop(pending_key, None)
        if pending is None:
            return

        contract: ContractWindow = pending["contract"]
        predictions: dict[str, dict[str, Any]] = pending["predictions"]

        # Get actual settlement from boundary-aligned price vs contract open
        candles = self.buffers[asset].get_candles()
        if not candles:
            logger.warning("%s: no candles for settlement", asset)
            return

        # Use the candle closest to the settlement boundary (now) rather than
        # blindly taking the latest buffer entry, which may overshoot by 1-2min
        boundary_ts = now.timestamp()
        tail = candles[-10:] if len(candles) >= 10 else candles
        settle_candle = min(tail, key=lambda c: abs(c.ts.timestamp() - boundary_ts))
        current_price = settle_candle.close
        settle_drift_sec = abs(settle_candle.ts.timestamp() - boundary_ts)
        open_price = contract.reference_price_open
        actual_direction = "up" if current_price > open_price else "down"

        # Score each agent
        agents_result: dict[str, dict[str, Any]] = {}
        correct_count = 0
        trade_count = 0
        for agent_id, pred_info in predictions.items():
            prediction = pred_info["prediction"]
            if prediction == "skip":
                agents_result[agent_id] = {
                    "prediction": "skip",
                    "correct": None,
                    "bt_wr": pred_info["bt_wr"],
                    "strategy": pred_info.get("strategy", "?"),
                }
            else:
                is_correct = prediction == actual_direction
                if is_correct:
                    correct_count += 1
                trade_count += 1
                agents_result[agent_id] = {
                    "prediction": prediction,
                    "correct": is_correct,
                    "bt_wr": pred_info["bt_wr"],
                    "strategy": pred_info.get("strategy", "?"),
                }

        # Log settlement
        entry = {
            "ts": now.isoformat(),
            "asset": asset,
            "timeframe": tf,
            "contract_id": contract.contract_id,
            "open_price": open_price,
            "close_price": current_price,
            "settle_candle_ts": settle_candle.ts.isoformat(),
            "settle_drift_sec": round(settle_drift_sec, 1),
            "direction": actual_direction,
            "regime": pending.get("regime", "unknown"),
            "strategies_invoked": pending.get("strategies_matched", []),
            "agents": agents_result,
        }
        self.logger.log_settlement(entry)
        self.total_settlements += 1

        accuracy = correct_count / trade_count * 100 if trade_count > 0 else 0
        delta_pct = (current_price - open_price) / open_price * 100
        logger.info(
            "  %s/%s SETTLED: %s (%.2f%%) | $%.2f > $%.2f | %d/%d correct (%.0f%%)",
            asset, tf, actual_direction.upper(), delta_pct,
            open_price, current_price,
            correct_count, trade_count, accuracy,
        )

    def _save_state(self) -> None:
        stats = self.logger.get_stats()

        # Build current predictions view (keyed by "asset:timeframe")
        current_contracts = {}
        for pending_key, pending in self.pending.items():
            contract: ContractWindow = pending["contract"]
            preds = {
                aid: r["prediction"]
                for aid, r in pending["predictions"].items()
            }
            current_contracts[pending_key] = {
                "contract_id": contract.contract_id,
                "open_price": contract.reference_price_open,
                "evaluated_at": pending["evaluated_at"].isoformat(),
                "timeframe": pending.get("timeframe", "15m"),
                "regime": pending.get("regime", "unknown"),
                "strategies_matched": pending.get("strategies_matched", []),
                "agents_invoked": len(pending["predictions"]),
                "predictions": preds,
            }

        # Build agent stats with BT comparison -- include historical agents from log
        agent_stats = {}
        # Current pool agents
        pool_lookup = {cfg["agent_id"]: cfg for cfg in self.pool.all_agents}
        # Merge: all agents from stats (log) + all from current pool
        all_agent_ids = set(stats.keys()) | set(pool_lookup.keys())
        for aid in all_agent_ids:
            s = stats.get(aid, {})
            cfg = pool_lookup.get(aid)
            agent_stats[aid] = {
                "bt_wr": round((cfg["bt_wr"] if cfg else s.get("bt_wr", 0)), 4),
                "live_wr": round(s.get("live_wr", 0), 4),
                "live_trades": s.get("live_trades", 0),
                "live_wins": s.get("live_wins", 0),
                "skips": s.get("skips", 0),
                "delta": round(s.get("delta", 0), 4),
                "strategy": cfg["strategy"] if cfg else "unknown",
                "timeframe": cfg.get("timeframe", "15m") if cfg else "15m",
            }

        # Strategy summary
        strategies_summary = {}
        for sid, agents in self.pool.agents_by_strategy.items():
            strategies_summary[sid] = {
                "agents": len(agents),
                "best_wr": round(agents[0]["bt_wr"], 4) if agents else 0,
                "regimes": sorted(STRATEGY_REGIMES.get(sid, set())),
            }

        state = {
            "status": "running",
            "started_at": self.started_at.isoformat(),
            "assets": self.assets,
            "agents_loaded": len(self.pool.all_agents),
            "strategies_loaded": len(self.pool.agents_by_strategy),
            "total_settlements": self.total_settlements,
            "current_contracts": current_contracts,
            "agent_stats": agent_stats,
            "strategies": strategies_summary,
            "regime_history": self.regime_history[-20:],
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }
        self.logger.save_state(state)


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(description="Live Paper Trader - observer pattern with regime detection")
    parser.add_argument("--assets", default="BTC,ETH,SOL", help="Comma-separated assets (default: BTC,ETH,SOL)")
    parser.add_argument("--per-strategy", type=int, default=10, help="Top N agents per strategy:tf combo (default: 10)")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon (same as default, for clarity)")
    parser.add_argument(
        "--include-viable", action="store_true", default=True,
        help="Include viable agents (WR>52%%), not just elite (default: True)",
    )
    parser.add_argument(
        "--elite-only", action="store_true", default=False,
        help="Only use elite agents (WR>=58%%, WF=1.0). Overrides --include-viable",
    )
    args = parser.parse_args()

    assets = [a.strip().upper() for a in args.assets.split(",")]
    valid_assets = [a for a in assets if a in BinanceFeed.SYMBOLS]
    if not valid_assets:
        print(f"No valid assets. Choose from: {list(BinanceFeed.SYMBOLS.keys())}")
        sys.exit(1)

    per_strategy = getattr(args, "per_strategy", 10)
    include_viable = not args.elite_only
    pool_label = "viable+elite" if include_viable else "elite only"

    print("=" * 60)
    print("  DGM-H Live Paper Trader (Observer Pattern)")
    print("=" * 60)
    print(f"  Assets:       {valid_assets}")
    print(f"  Per strategy: top {per_strategy} agents ({pool_label})")
    print(f"  Strategies:   {len(STRATEGY_REGIMES)} registered")
    print(f"  Source:       Binance public API (no key needed)")
    print(f"  Timeframes:   15m (every 15min), 1h (hourly), 4h (every 4h)")
    print(f"  Settle:       at each timeframe boundary")
    print(f"  Log:          {LOG_PATH}")
    print(f"  State:        {STATE_PATH}")
    print("=" * 60)
    print()

    trader = LivePaperTrader(
        assets=valid_assets, per_strategy=per_strategy,
        include_viable=include_viable,
    )
    trader.run()


if __name__ == "__main__":
    main()
