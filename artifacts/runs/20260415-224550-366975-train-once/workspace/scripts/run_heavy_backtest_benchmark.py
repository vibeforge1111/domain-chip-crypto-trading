from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from safe_write import safe_write_json

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from domain_chip_crypto_trading.cli import evaluate


def _backtest_code_hash() -> str:
    """Hash the signal engine source to detect code changes that invalidate cached results."""
    backtest_path = SRC_ROOT / "domain_chip_crypto_trading" / "backtest.py"
    if not backtest_path.exists():
        return "unknown"
    content = backtest_path.read_bytes()
    return hashlib.sha256(content).hexdigest()[:16]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_optional_trials(path: Path) -> list[dict]:
    if not path.exists():
        return []
    payload = _load_json(path)
    return payload if isinstance(payload, list) else []


def _load_optional_object(path: Path) -> dict:
    if not path.exists():
        return {}
    payload = _load_json(path)
    return payload if isinstance(payload, dict) else {}


def _validation_index(path: Path) -> dict[str, dict]:
    payload = _load_optional_object(path)
    rows = payload.get("rows", []) if isinstance(payload.get("rows"), list) else []
    index: dict[str, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        regime_id = str(row.get("regime_id", "")).strip()
        if not regime_id:
            continue
        bucket = index.setdefault(
            regime_id,
            {
                "validated_match_count": 0,
                "mixed_proxy_count": 0,
                "mismatch_review_count": 0,
                "dataset_ready_count": 0,
            },
        )
        status = str(row.get("validation_status", "")).strip()
        status_key = {
            "validated_match": "validated_match_count",
            "mixed_proxy": "mixed_proxy_count",
            "mismatch_review": "mismatch_review_count",
        }.get(status)
        if status_key:
            bucket[status_key] += 1
        if bool(row.get("dataset_ready")):
            bucket["dataset_ready_count"] += 1
    return index


def _regime_validation_for(market_regime: str, index: dict[str, dict]) -> tuple[str, dict]:
    aliases = {
        "range": ["range_chop_mean_reversion"],
        "trend": ["trend_continuation_greed"],
        "high_vol": ["compression_pre_breakout", "fear_shock_high_alert"],
        "fear_shock": ["fear_shock_high_alert"],
        "compression": ["compression_pre_breakout"],
        "event_driven": ["event_driven_macro_transition"],
    }
    candidates = aliases.get(market_regime, [market_regime] if market_regime else ["unknown"])
    best_regime_id = "unknown"
    best_row = {
        "validated_match_count": 0,
        "mixed_proxy_count": 0,
        "mismatch_review_count": 0,
        "dataset_ready_count": 0,
    }
    best_score = (-1, -1, -1)
    for regime_id in candidates:
        row = index.get(
            regime_id,
            {
                "validated_match_count": 0,
                "mixed_proxy_count": 0,
                "mismatch_review_count": 0,
                "dataset_ready_count": 0,
            },
        )
        score = (
            int(row.get("validated_match_count", 0) or 0),
            int(row.get("mixed_proxy_count", 0) or 0),
            int(row.get("dataset_ready_count", 0) or 0),
        )
        if score > best_score:
            best_score = score
            best_regime_id = regime_id
            best_row = row
    return best_regime_id, best_row


def _mutation_key(mutations: dict) -> str:
    """Stable cache key for a set of mutations."""
    return json.dumps(mutations, sort_keys=True)


def main() -> None:
    config_path = REPO_ROOT / "spark-researcher.project.json"
    config = _load_json(config_path)
    validation_index = _validation_index(REPO_ROOT / "artifacts" / "research" / "timeline_pack_validation.json")
    trials = list(config.get("candidate_trials", []))
    trials.extend(_load_optional_trials(REPO_ROOT / "artifacts" / "recursion" / "mutation_trials.json"))

    # Incremental benchmarking: reuse cached results when mutations unchanged
    summary_path = REPO_ROOT / "artifacts" / "backtests" / "heavy_backtest_summary.json"
    existing = _load_optional_object(summary_path)
    current_code_hash = _backtest_code_hash()
    previous_code_hash = existing.get("backtest_code_hash", "")
    cache: dict[str, dict] = {}
    if previous_code_hash == current_code_hash:
        for row in (existing.get("rows", []) if isinstance(existing.get("rows"), list) else []):
            if isinstance(row, dict) and isinstance(row.get("mutations"), dict):
                cache[_mutation_key(row["mutations"])] = row

    rows: list[dict] = []
    evaluated_count = 0
    cached_count = 0
    for trial in trials:
        if not isinstance(trial, dict):
            continue
        mutations = trial.get("mutations", {})
        mutations = mutations if isinstance(mutations, dict) else {}
        key = _mutation_key(mutations)

        cached_row = cache.get(key)
        if cached_row is not None:
            row = dict(cached_row)
            row["candidate_id"] = trial.get("candidate_id")
            row["candidate_summary"] = trial.get("candidate_summary")
            row["hypothesis"] = trial.get("hypothesis")
            rows.append(row)
            cached_count += 1
            continue

        payload = {
            "runtime_root": str(REPO_ROOT),
            "candidate": trial,
        }
        outcome = evaluate(payload)
        metrics = outcome.get("metrics", {})
        result = outcome.get("result", {})
        regime_id = str(mutations.get("market_regime", "")).strip()
        resolved_regime_id, validation = _regime_validation_for(regime_id, validation_index)
        result["regime_validation"] = {
            "market_regime": regime_id or "unknown",
            "regime_id": resolved_regime_id,
            **validation,
            "validated_regime_support": validation.get("validated_match_count", 0) > 0,
        }
        row = {
            "candidate_id": trial.get("candidate_id"),
            "candidate_summary": trial.get("candidate_summary"),
            "hypothesis": trial.get("hypothesis"),
            "mutations": mutations,
            "metrics": metrics,
            "result": result,
        }
        rows.append(row)
        cache[key] = row
        evaluated_count += 1
    rows.sort(
        key=lambda row: (
            bool((row.get("result", {}) or {}).get("trade_count_gate_pass")),
            int((((row.get("result", {}) or {}).get("regime_validation", {}) or {}).get("validated_match_count", 0) or 0)),
            float((row.get("result", {}) or {}).get("walk_forward_consistency", 0.0) or 0.0),
            float((row.get("result", {}) or {}).get("stress_resilience", 0.0) or 0.0),
            float((row.get("metrics", {}) or {}).get("profitability_score", 0.0) or 0.0),
            float((row.get("metrics", {}) or {}).get("paper_trade_readiness", 0.0) or 0.0),
        ),
        reverse=True,
    )
    summary = {
        "benchmark_kind": "heavy_backtest",
        "contract_family": "btc_up_down_15m",
        "candidate_count": len(rows),
        "top_candidate_id": rows[0]["candidate_id"] if rows else None,
        "backtest_code_hash": current_code_hash,
        "incremental_stats": {
            "evaluated": evaluated_count,
            "cached": cached_count,
        },
        "rows": rows,
    }
    target_root = REPO_ROOT / "artifacts" / "backtests"
    target_root.mkdir(parents=True, exist_ok=True)
    path = target_root / "heavy_backtest_summary.json"
    safe_write_json(path, summary)
    print(path)


if __name__ == "__main__":
    main()
