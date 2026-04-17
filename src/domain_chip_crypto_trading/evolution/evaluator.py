"""Evaluator (Task Agent) -- wraps existing backtest infrastructure.

This is the task-level agent in DGM-H terms. It doesn't modify itself;
it evaluates candidate mutation dicts using the existing backtest engine.

Supports staged evaluation (DGM-H Gap 3): quick -> medium -> full filtering
to save ~3x compute by killing bad candidates early.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)

# Repo root: evolution/ is 3 levels below repo root
# __file__ -> evolution/evaluator.py
# parents[0] -> evolution/
# parents[1] -> domain_chip_crypto_trading/
# parents[2] -> src/
# parents[3] -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]

# Staged evaluation thresholds
QUICK_CONTRACT_LIMIT = 2000
MEDIUM_CONTRACT_LIMIT = 8000
QUICK_WR_THRESHOLD = 0.50
QUICK_MIN_TRADES = 25  # raised from 10 -- filter out noise agents with tiny samples
MEDIUM_WR_THRESHOLD = 0.54
MEDIUM_MIN_TRADES = 40  # raised from 15 -- need statistical significance

# Feature key mapping: guard expects -> backtest provides
_GUARD_FEATURE_MAP = {
    "momentum_score": "momentum",
    "body_ratio": "body_bias",       # abs() applied
    "volatility_regime": "volatility",
    "rsi_14": "rsi",
    "trend_strength": "ema_gap_ratio",  # abs() applied
    "bb_position": "close_location",
    "range_pct": "range_width",
    "ema_slope": "ema_gap_ratio",
    "atr_ratio": "atr_ratio",
    "bb_pct_b": "bb_pct_b",
    "vwap_deviation": "vwap_deviation",
    "stoch_k": "stoch_k",
    "stoch_d": "stoch_d",
    "obv_slope": "obv_slope",
    "macd_histogram": "macd_histogram",
    "rsi_2h": "rsi_2h",
    # Session 25: Quant indicators
    "hurst_exp": "hurst_exp",
    "shannon_entropy": "shannon_entropy",
    "autocorr_1": "autocorr_1",
    "volume_delta": "volume_delta",
    "rv_ratio": "rv_ratio",
    "parkinson_vol": "parkinson_vol",
}

_ABS_KEYS = {"body_ratio", "trend_strength"}

# Prediction term mapping: backtest uses up/down, guards use long/short
_PRED_TO_GUARD = {"up": "long", "down": "short", "skip": "skip"}
_PRED_FROM_GUARD = {"long": "up", "short": "down", "skip": "skip"}


def _make_guard_adapter(raw_guard_fn: Callable) -> Callable:
    """Wrap a raw guard function to translate feature keys and prediction terms.

    The backtest uses feature keys like 'momentum', 'rsi', 'body_bias' and
    predictions like 'up'/'down'. LLM-generated guards expect 'momentum_score',
    'rsi_14', 'body_ratio' and 'long'/'short'. This adapter bridges both.
    """
    def adapted_guard(features: dict, prediction: str) -> str:
        # Build guard-compatible feature dict
        guard_features = dict(features)  # start with all backtest features
        for guard_key, bt_key in _GUARD_FEATURE_MAP.items():
            val = features.get(bt_key, 0.0)
            if guard_key in _ABS_KEYS:
                val = abs(val)
            guard_features[guard_key] = val

        # Provide defaults for keys not in backtest (legacy guards only)
        guard_features.setdefault("close_vs_open", features.get("body_bias", 0.0))
        guard_features.setdefault("high_vs_close", features.get("upper_wick_ratio", 0.0))
        guard_features.setdefault("low_vs_close", features.get("lower_wick_ratio", 0.0))

        # Translate prediction terms
        guard_pred = _PRED_TO_GUARD.get(prediction, prediction)

        try:
            result = raw_guard_fn(guard_features, guard_pred)
        except Exception:
            return prediction  # guard error -> pass through

        # Translate back
        return _PRED_FROM_GUARD.get(result, result)

    return adapted_guard


def _load_guard_for_agent(mutations: dict[str, Any]) -> Callable | None:
    """Load and adapt a guard function if the agent has an llm_guard_id.

    In the production repo, LLM code generation is not available.
    Always returns None -- guards are applied via mutation config only.
    """
    return None


def _extract_fitness(result: dict[str, Any]) -> dict[str, Any]:
    """Extract standardized fitness dict from raw backtest result.

    The CLI evaluate() does not return win_rate at the top level.
    It lives inside each walk_forward_stats segment. We compute
    a trade-weighted average across all segments.
    """
    wf_stats = result.get("walk_forward_stats", [])

    # Compute win_rate from walk-forward segments (trade-weighted average)
    win_rate = result.get("win_rate", 0)
    if not win_rate and wf_stats:
        total_trades = 0
        weighted_wr = 0.0
        for seg in wf_stats:
            tc = seg.get("trade_count", 0)
            wr = seg.get("win_rate", 0)
            weighted_wr += wr * tc
            total_trades += tc
        if total_trades > 0:
            win_rate = weighted_wr / total_trades

    fitness = {
        "win_rate": win_rate,
        "wealth_factor": result.get("walk_forward_consistency", 0),
        "max_drawdown": result.get("max_drawdown", 1.0),
        "sharpe_ratio": result.get("sharpe_ratio", 0),
        "trade_count": result.get("trade_count", 0),
        "profitability_score": result.get("profitability_score", 0),
        "holdout_profitability": result.get("holdout_profitability_score", 0),
        "stress_resilience": result.get("stress_resilience", 0),
        "paper_trade_readiness": result.get("paper_trade_readiness", 0),
        "verdict": result.get("verdict", "unknown"),
        "walk_forward_stats": wf_stats,
    }

    if "regime_stats" in result:
        fitness["regime_stats"] = result["regime_stats"]

    # Derived viability flags
    fitness["viable"] = (
        fitness["wealth_factor"] >= 0.8
        and fitness["win_rate"] > 0.52
        and fitness["trade_count"] >= 30
    )
    fitness["elite"] = (
        fitness["wealth_factor"] >= 1.0
        and fitness["win_rate"] >= 0.58
        and fitness["trade_count"] >= 50
    )

    return fitness


def evaluate_agent(
    mutations: dict[str, Any],
    runtime_root: Path | None = None,
    contract_limit: int | None = None,
) -> dict[str, Any]:
    """Evaluate a mutation dict using the existing backtest engine.

    Args:
        mutations: The mutation dict to evaluate.
        runtime_root: Override for the data/artifacts root directory.
        contract_limit: If set, limit backtest to this many contracts.

    Returns:
        Fitness dict with keys: win_rate, wealth_factor, max_drawdown, sharpe_ratio,
        trade_count, regime_stats, viable, elite.
    """
    root = runtime_root or REPO_ROOT

    try:
        from domain_chip_crypto_trading.cli import evaluate
    except ImportError:
        return _fallback_evaluate(mutations, root)

    payload = {"runtime_root": str(root), "candidate": {"mutations": mutations}}
    if contract_limit:
        payload["contract_limit"] = contract_limit

    try:
        outcome = evaluate(payload)
    except Exception as e:
        logger.error("evaluate() raised: %s", e)
        return {
            "win_rate": 0, "wealth_factor": 0, "max_drawdown": 1.0,
            "sharpe_ratio": 0, "trade_count": 0, "error": str(e),
            "viable": False, "elite": False,
        }

    # Extract fitness from the cli.evaluate() result structure
    result = outcome.get("result", outcome)
    return _extract_fitness(result)


def staged_evaluate(
    mutations: dict[str, Any],
    runtime_root: Path | None = None,
    quick_wr_threshold: float = QUICK_WR_THRESHOLD,
    medium_wr_threshold: float = MEDIUM_WR_THRESHOLD,
) -> dict[str, Any]:
    """DGM-H staged evaluation: quick -> medium -> full.

    Three-stage filtering saves ~3x compute by killing bad candidates early:
      Stage 1 (Quick):  2,000 contracts -- reject if WR < 0.50 or trades < 10
      Stage 2 (Medium): 8,000 contracts -- reject if WR < 0.54 or trades < 15
      Stage 3 (Full):   All contracts   -- complete evaluation

    Returns fitness dict with additional 'eval_stage' key showing which stage
    was reached and 'stages_passed' showing progression.
    """
    root = runtime_root or REPO_ROOT
    stages_passed = []

    # Scale trade floors by timeframe (1h/4h have fewer contracts)
    tf = str(mutations.get("timeframe", "15m"))
    tf_scale = {"15m": 1.0, "1h": 0.5, "4h": 0.25}.get(tf, 1.0)
    has_regime = bool(mutations.get("market_regime", ""))
    regime_scale = 0.7 if has_regime else 1.0
    scaled_quick_min = max(5, int(QUICK_MIN_TRADES * tf_scale * regime_scale))
    scaled_medium_min = max(8, int(MEDIUM_MIN_TRADES * tf_scale * regime_scale))

    # -- Stage 1: Quick screen (2,000 contracts) --------------------
    quick_result = evaluate_agent(
        mutations, root, contract_limit=QUICK_CONTRACT_LIMIT,
    )

    quick_wr = quick_result.get("win_rate", 0)
    quick_trades = quick_result.get("trade_count", 0)

    if quick_wr < quick_wr_threshold or quick_trades < scaled_quick_min:
        quick_result["eval_stage"] = "quick_reject"
        quick_result["stages_passed"] = []
        quick_result["rejection_reason"] = (
            f"Quick screen failed: WR={quick_wr:.3f} (need {quick_wr_threshold}), "
            f"trades={quick_trades} (need {scaled_quick_min})"
        )
        logger.debug(
            "Quick reject: WR=%.3f trades=%d", quick_wr, quick_trades,
        )
        return quick_result

    stages_passed.append("quick")
    logger.debug("Quick pass: WR=%.3f trades=%d", quick_wr, quick_trades)

    # -- Stage 2: Medium screen (8,000 contracts) -------------------
    medium_result = evaluate_agent(
        mutations, root, contract_limit=MEDIUM_CONTRACT_LIMIT,
    )

    medium_wr = medium_result.get("win_rate", 0)
    medium_trades = medium_result.get("trade_count", 0)

    if medium_wr < medium_wr_threshold or medium_trades < scaled_medium_min:
        medium_result["eval_stage"] = "medium_reject"
        medium_result["stages_passed"] = stages_passed
        medium_result["rejection_reason"] = (
            f"Medium screen failed: WR={medium_wr:.3f} (need {medium_wr_threshold}), "
            f"trades={medium_trades} (need {scaled_medium_min})"
        )
        logger.debug(
            "Medium reject: WR=%.3f trades=%d", medium_wr, medium_trades,
        )
        return medium_result

    stages_passed.append("medium")
    logger.debug("Medium pass: WR=%.3f trades=%d", medium_wr, medium_trades)

    # -- Stage 3: Full evaluation (all contracts) -------------------
    full_result = evaluate_agent(mutations, root)
    full_result["eval_stage"] = "full"
    full_result["stages_passed"] = stages_passed + ["full"]
    logger.debug(
        "Full eval: WR=%.3f trades=%d",
        full_result.get("win_rate", 0),
        full_result.get("trade_count", 0),
    )

    return full_result


def evaluate_batch(
    mutation_list: list[dict[str, Any]],
    runtime_root: Path | None = None,
    staged: bool = False,
) -> list[dict[str, Any]]:
    """Evaluate a batch of mutation dicts.

    Args:
        mutation_list: List of mutation dicts to evaluate.
        runtime_root: Override root directory.
        staged: If True, use staged evaluation for each candidate.
    """
    eval_fn = staged_evaluate if staged else evaluate_agent
    return [eval_fn(m, runtime_root) for m in mutation_list]


def _parallel_eval_worker(args: tuple) -> dict[str, Any]:
    """Top-level worker for ProcessPoolExecutor (must be picklable).

    Args:
        args: Tuple of (mutations_dict, runtime_root_str, use_staged)

    Returns:
        Fitness dict from evaluation.
    """
    mutations, runtime_root_str, use_staged = args
    root = Path(runtime_root_str)
    try:
        if use_staged:
            return staged_evaluate(mutations, runtime_root=root)
        else:
            return evaluate_agent(mutations, runtime_root=root)
    except Exception as e:
        return {
            "win_rate": 0, "wealth_factor": 0, "max_drawdown": 1.0,
            "sharpe_ratio": 0, "trade_count": 0, "error": str(e),
            "viable": False, "elite": False,
        }


def _fallback_evaluate(mutations: dict, root: Path) -> dict:
    """Fallback: run backtest via subprocess if import fails."""
    import subprocess
    import tempfile

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        json.dump(mutations, f)
        tmp_path = f.name

    try:
        cmd = [
            sys.executable,
            str(root / "src" / "domain_chip_crypto_trading" / "backtest.py"),
            "--mutations-file",
            tmp_path,
            "--runtime-root",
            str(root),
            "--output-json",
        ]
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(root),
        )
        if proc.returncode == 0:
            return json.loads(proc.stdout)
        else:
            return {
                "win_rate": 0,
                "wealth_factor": 0,
                "max_drawdown": 1.0,
                "sharpe_ratio": 0,
                "trade_count": 0,
                "error": proc.stderr[:500],
                "viable": False,
                "elite": False,
            }
    finally:
        Path(tmp_path).unlink(missing_ok=True)
