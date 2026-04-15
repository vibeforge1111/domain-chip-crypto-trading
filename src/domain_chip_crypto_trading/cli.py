from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from domain_chip_crypto_trading.backtest import run_backtest

BASE = {"profitability_score": 0.34, "sharpe_ratio": 0.72, "max_drawdown": 0.24, "win_rate": 0.48, "doctrine_fit": 0.31}
DOCTRINES = {
    "trend_regime_following": {"p": 0.18, "s": 0.52, "d": 0.08, "w": 0.03, "f": 0.12, "lesson": "Trend doctrine works when regime filters are explicit.", "boundary": "Weak in chop without a regime filter."},
    "mean_reversion_liquidity_reclaim": {"p": 0.13, "s": 0.37, "d": 0.05, "w": 0.06, "f": 0.11, "lesson": "Liquidity reclaims monetize rotation if exits stay disciplined.", "boundary": "Fails when expansion is mistaken for reclaim."},
    "breakout_volatility_expansion": {"p": 0.16, "s": 0.31, "d": 0.11, "w": 0.01, "f": 0.10, "lesson": "Breakout doctrine pays in violent expansion with strict false-break filters.", "boundary": "Punishes loose risk during fakeouts."},
    "risk_first_asymmetric_capture": {"p": 0.14, "s": 0.44, "d": 0.04, "w": 0.02, "f": 0.14, "lesson": "Asymmetric capture works when downside truncation is encoded first.", "boundary": "Undertrades if the doctrine becomes too selective."},
}
STRATEGIES = {
    "ema_pullback_long": {"p": 0.17, "s": 0.39, "d": 0.07, "w": 0.04, "f": 0.09},
    "range_reclaim_scalp": {"p": 0.12, "s": 0.34, "d": 0.05, "w": 0.07, "f": 0.08},
    "breakout_open_interest_confirmation": {"p": 0.16, "s": 0.28, "d": 0.10, "w": 0.02, "f": 0.08},
    "funding_mean_revert": {"p": 0.11, "s": 0.30, "d": 0.04, "w": 0.05, "f": 0.07},
    "bollinger_squeeze_breakout": {"p": 0.15, "s": 0.32, "d": 0.09, "w": 0.03, "f": 0.09},
    "wedge_exhaustion_reversal": {"p": 0.13, "s": 0.35, "d": 0.06, "w": 0.06, "f": 0.10},
}
REGIMES = {"trend": {"p": 0.08, "s": 0.12, "d": 0.02, "f": 0.06}, "range": {"p": 0.05, "s": 0.07, "d": 0.01, "f": 0.05}, "high_vol": {"p": 0.07, "s": 0.02, "d": 0.06, "f": 0.03}, "event_driven": {"p": 0.06, "s": 0.04, "d": 0.05, "f": 0.04}}
TIMEFRAMES = {"15m": {"p": 0.03, "s": 0.00, "d": 0.06, "w": 0.02}, "1h": {"p": 0.05, "s": 0.05, "d": 0.03, "w": 0.03}, "4h": {"p": 0.07, "s": 0.08, "d": 0.02, "w": 0.01}}
VENUES = {"binance": {"p": 0.03, "s": 0.03, "d": 0.01}, "bybit": {"p": 0.02, "s": 0.02, "d": 0.02}, "hyperliquid": {"p": 0.04, "s": 0.03, "d": 0.04}}
PAIRS = {"trend_regime_following|ema_pullback_long": 0.12, "mean_reversion_liquidity_reclaim|range_reclaim_scalp": 0.11, "breakout_volatility_expansion|breakout_open_interest_confirmation": 0.10, "risk_first_asymmetric_capture|funding_mean_revert": 0.08, "breakout_volatility_expansion|bollinger_squeeze_breakout": 0.10, "mean_reversion_liquidity_reclaim|wedge_exhaustion_reversal": 0.09}
REGIME_MATCH = {"trend_regime_following|trend": 0.08, "mean_reversion_liquidity_reclaim|range": 0.08, "breakout_volatility_expansion|high_vol": 0.09, "risk_first_asymmetric_capture|event_driven": 0.07}


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def _write(path: str, payload: dict) -> None:
    Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _mutations(payload: dict) -> dict[str, str]:
    candidate = payload.get("candidate", {})
    raw = candidate.get("mutations", {}) if isinstance(candidate, dict) else {}
    return {str(key): str(value) for key, value in raw.items()}


def _clamp(value: float) -> float:
    return round(max(0.0, min(0.99, value)), 4)


def _asset_bonus(raw: str) -> float:
    assets = [item.strip() for item in raw.split(",") if item.strip()]
    majors = sum(1 for asset in assets if asset in {"BTC", "ETH", "SOL"})
    return min(0.04, len(assets) * 0.01) + (majors * 0.008)


def _score(mutations: dict[str, str]) -> dict[str, float | str]:
    doctrine_id = mutations.get("doctrine_id", "")
    strategy_id = mutations.get("strategy_id", "")
    regime = mutations.get("market_regime", "")
    timeframe = mutations.get("timeframe", "")
    venue = mutations.get("venue", "")
    doctrine = DOCTRINES.get(doctrine_id, {})
    strategy = STRATEGIES.get(strategy_id, {})
    regime_spec = REGIMES.get(regime, {})
    timeframe_spec = TIMEFRAMES.get(timeframe, {})
    venue_spec = VENUES.get(venue, {})
    synergy = PAIRS.get(doctrine_id + "|" + strategy_id, -0.02 if doctrine_id and strategy_id else 0.0)
    regime_match = REGIME_MATCH.get(doctrine_id + "|" + regime, -0.03 if doctrine_id and regime else 0.0)
    profit = _clamp(BASE["profitability_score"] + doctrine.get("p", 0.0) + strategy.get("p", 0.0) + regime_spec.get("p", 0.0) + timeframe_spec.get("p", 0.0) + venue_spec.get("p", 0.0) + synergy + regime_match + _asset_bonus(mutations.get("asset_universe", "")))
    sharpe = _clamp(BASE["sharpe_ratio"] + doctrine.get("s", 0.0) + strategy.get("s", 0.0) + regime_spec.get("s", 0.0) + timeframe_spec.get("s", 0.0) + venue_spec.get("s", 0.0))
    drawdown = round(max(0.02, min(0.95, BASE["max_drawdown"] + doctrine.get("d", 0.0) + strategy.get("d", 0.0) + regime_spec.get("d", 0.0) + timeframe_spec.get("d", 0.0) + venue_spec.get("d", 0.0) - doctrine.get("f", 0.0) * 0.3)), 4)
    win_rate = _clamp(BASE["win_rate"] + doctrine.get("w", 0.0) + strategy.get("w", 0.0) + timeframe_spec.get("w", 0.0))
    doctrine_fit = _clamp(BASE["doctrine_fit"] + doctrine.get("f", 0.0) + strategy.get("f", 0.0) + regime_spec.get("f", 0.0) + max(0.0, synergy * 0.6))
    readiness = _clamp(profit * 0.4 + sharpe * 0.25 + doctrine_fit * 0.2 + win_rate * 0.15 - drawdown * 0.35)
    gate = 0.78 if mutations.get("paper_gate", "strict") == "strict" else 0.72
    if readiness >= gate and drawdown <= 0.22:
        verdict, next_step = "approve", "queue_for_paper_trade"
    elif profit >= 0.66 and doctrine_fit >= 0.60:
        verdict, next_step = "defer", "hold_for_more_backtest_evidence"
    else:
        verdict, next_step = "reject", "run_contradiction_probe"
    return {"profitability_score": profit, "sharpe_ratio": sharpe, "max_drawdown": drawdown, "win_rate": win_rate, "paper_trade_readiness": readiness, "verdict_confidence": _clamp(0.4 + profit * 0.25 + sharpe * 0.2 + doctrine_fit * 0.15 - drawdown * 0.1), "verdict": verdict, "recommended_next_step": next_step, "lesson": doctrine.get("lesson", "Baseline only. Add a doctrine before promoting any strategy claim."), "boundary": doctrine.get("boundary", "Passive baseline is not doctrine and should not be promoted.")}


def _row_mutations(row: dict[str, Any]) -> dict[str, str]:
    return {
        str(item.get("name", "")): str(item.get("value", ""))
        for item in row.get("applied_mutations", [])
        if isinstance(item, dict)
    }


def _row_metrics(row: dict[str, Any]) -> dict[str, Any]:
    metrics = row.get("metrics", {})
    return metrics if isinstance(metrics, dict) else {}


def _row_chip_result(row: dict[str, Any]) -> dict[str, Any]:
    result = row.get("chip_result", {})
    return result if isinstance(result, dict) else {}


def _rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = payload.get("ledger_rows", [])
    return [row for row in rows if isinstance(row, dict)]


def _candidate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if str(row.get("candidate_id", "")) != "global-baseline"]


def _sort_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            float(_row_metrics(row).get("profitability_score", 0.0) or 0.0),
            float(_row_metrics(row).get("paper_trade_readiness", 0.0) or 0.0),
        ),
        reverse=True,
    )


def _autoloop_state(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "recursion", "autoloop_state.json", fallback={})
    return data if isinstance(data, dict) else {}


def _benchmark_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    summary = _heavy_benchmark_summary(payload)
    rows = summary.get("rows", []) if isinstance(summary.get("rows"), list) else []
    return [row for row in rows if isinstance(row, dict)]


def _benchmark_mutations(row: dict[str, Any]) -> dict[str, str]:
    raw = row.get("mutations", {})
    if isinstance(raw, dict):
        return {str(key): str(value) for key, value in raw.items() if value not in {None, ""}}
    return _row_mutations(row)


def _benchmark_metrics(row: dict[str, Any]) -> dict[str, Any]:
    metrics = row.get("metrics", {})
    return metrics if isinstance(metrics, dict) else _row_metrics(row)


def _benchmark_result(row: dict[str, Any]) -> dict[str, Any]:
    result = row.get("result", {})
    return result if isinstance(result, dict) else _row_chip_result(row)


def _rank_benchmark_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            float(_benchmark_metrics(row).get("win_rate", 0.0) or 0.0),
            float(_benchmark_result(row).get("walk_forward_consistency", 0.0) or 0.0),
            float(_benchmark_metrics(row).get("sharpe_ratio", 0.0) or 0.0),
            float(_benchmark_metrics(row).get("profitability_score", 0.0) or 0.0),
        ),
        reverse=True,
    )


def _safe_proposed_mutations(payload: dict[str, Any], proposed: dict[str, Any]) -> dict[str, str]:
    # This project still runs through the wrapper/train-once path with no mutable parameter
    # contract, so hook suggestions must stay informational until the runtime can apply them safely.
    return {}


def _suggestion_entry(
    payload: dict[str, Any],
    *,
    candidate_id: str,
    candidate_summary: str,
    hypothesis: str,
    proposed_mutations: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "candidate_id": candidate_id,
        "candidate_summary": candidate_summary,
        "hypothesis": hypothesis,
        "mutations": _safe_proposed_mutations(payload, proposed_mutations),
    }
    combined_metadata = {
        "proposed_mutations": {str(key): str(value) for key, value in proposed_mutations.items() if value not in {None, ""}},
    }
    if isinstance(metadata, dict):
        combined_metadata.update(metadata)
    entry["metadata"] = combined_metadata
    return entry


def _line(value: Any) -> str:
    return "n/a" if value in {None, ""} else str(value)


def _promotion_packets(payload: dict[str, Any]) -> list[dict[str, Any]]:
    runtime_root_raw = str(payload.get("runtime_root", "")).strip()
    if not runtime_root_raw:
        return []
    packet_root = Path(runtime_root_raw) / "artifacts" / "promotion" / "benchmark_grounded"
    if not packet_root.exists():
        return []
    packets: list[dict[str, Any]] = []
    for path in sorted(packet_root.glob("*.json")):
        try:
            packet = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(packet, dict):
            packets.append(packet)
    return packets


def _approved_sources(payload: dict[str, Any]) -> list[dict[str, Any]]:
    runtime_root_raw = str(payload.get("runtime_root", "")).strip()
    if not runtime_root_raw:
        return []
    path = Path(runtime_root_raw) / "docs" / "research-ingest" / "approved-sources.json"
    if not path.exists():
        return []
    try:
        payload_data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return payload_data if isinstance(payload_data, list) else []


def _research_backlog(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "research", "research_backlog.json", fallback={})
    return data if isinstance(data, dict) else {}


def _doctrine_cards(payload: dict[str, Any]) -> list[dict[str, Any]]:
    runtime_root_raw = str(payload.get("runtime_root", "")).strip()
    if not runtime_root_raw:
        return []
    card_root = Path(runtime_root_raw) / "docs" / "doctrine-cards"
    if not card_root.exists():
        return []
    cards: list[dict[str, Any]] = []
    for path in sorted(card_root.glob("*.json")):
        try:
            card = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(card, dict):
            cards.append(card)
    return cards


def _doctrine_packets(payload: dict[str, Any]) -> list[dict[str, Any]]:
    runtime_root_raw = str(payload.get("runtime_root", "")).strip()
    if not runtime_root_raw:
        return []
    packet_root = Path(runtime_root_raw) / "docs" / "doctrine-packets"
    if not packet_root.exists():
        return []
    packets: list[dict[str, Any]] = []
    for path in sorted(packet_root.glob("*.json")):
        try:
            packet = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(packet, dict):
            packets.append(packet)
    packets.sort(
        key=lambda item: (
            int(item.get("ingest_priority", 999) or 999),
            str(item.get("packet_id", "")),
        )
    )
    return packets


def _json_artifact(payload: dict[str, Any], *relative_parts: str, fallback: Any) -> Any:
    runtime_root_raw = str(payload.get("runtime_root", "")).strip()
    if not runtime_root_raw:
        return fallback
    path = Path(runtime_root_raw).joinpath(*relative_parts)
    if not path.exists():
        return fallback
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback
    return data


def _specialization_path_manifest() -> dict[str, Any]:
    path = Path("specialization-path.json")
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _default_scenario() -> dict[str, Any]:
    manifest = _specialization_path_manifest()
    benchmark = manifest.get("benchmarkProfile", {}) if isinstance(manifest.get("benchmarkProfile"), dict) else {}
    scenario_id = str(benchmark.get("defaultScenario", "")).strip()
    if not scenario_id:
        return {}
    path = Path("benchmarks") / "scenarios" / f"{scenario_id}.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _strongest_and_weakest_labels(metrics: dict[str, Any]) -> tuple[str, str]:
    dimensions = {
        "profitability_score": float(metrics.get("profitability_score", 0.0) or 0.0),
        "sharpe_ratio": float(metrics.get("sharpe_ratio", 0.0) or 0.0),
        "paper_trade_readiness": float(metrics.get("paper_trade_readiness", 0.0) or 0.0),
        "win_rate": float(metrics.get("win_rate", 0.0) or 0.0),
        "doctrine_fit": float(metrics.get("doctrine_fit", 0.0) or 0.0),
        "max_drawdown": 1.0 - float(metrics.get("max_drawdown", 0.0) or 0.0),
    }
    ordered = sorted(dimensions.items(), key=lambda item: item[1], reverse=True)
    strongest = ordered[0][0] if ordered else "profitability_score"
    weakest = ordered[-1][0] if ordered else "max_drawdown"
    return strongest, weakest


def _swarm_publication_packet(candidate_id: str, metrics: dict[str, Any], mutations: dict[str, str]) -> dict[str, Any]:
    manifest = _specialization_path_manifest()
    scenario = _default_scenario()
    strongest_label, weakest_label = _strongest_and_weakest_labels(metrics)
    publication_ready = str(metrics.get("recommended_next_step", "")) == "queue_for_paper_trade"
    boundary = str(metrics.get("boundary", ""))
    lesson = str(metrics.get("lesson", ""))
    return {
        "schema_version": "spark-benchmark-win-packet.v1",
        "packet_kind": "benchmark_candidate_publication",
        "specialization_path_key": str(manifest.get("pathKey", "trading-crypto")),
        "specialization_label": "Crypto Trading",
        "scenario_id": str(scenario.get("scenario_id", "")),
        "scenario_pack": str(scenario.get("scenario_pack", "")),
        "scenario_track": str(scenario.get("scenario_track", "")),
        "candidate_id": candidate_id,
        "candidate_path": str(scenario.get("candidate_path", "benchmarks/trading-crypto-candidate.json")),
        "baseline_mutations": scenario.get("baseline_mutations", {}) if isinstance(scenario.get("baseline_mutations"), dict) else {},
        "candidate_mutations": mutations,
        "metrics": {
            "profitability_score": metrics.get("profitability_score"),
            "sharpe_ratio": metrics.get("sharpe_ratio"),
            "max_drawdown": metrics.get("max_drawdown"),
            "win_rate": metrics.get("win_rate"),
            "paper_trade_readiness": metrics.get("paper_trade_readiness"),
            "verdict_confidence": metrics.get("verdict_confidence"),
        },
        "benchmark_verdict": str(metrics.get("verdict", "")),
        "recommended_next_step": str(metrics.get("recommended_next_step", "")),
        "swarm_publication_ready": publication_ready,
        "promotion_candidate_kind": "paper_trade_candidate" if publication_ready else "contradiction_surface",
        "insight_summary": f"Crypto Trading scored {metrics.get('paper_trade_readiness')} on {scenario.get('scenario_id', 'the default scenario')}, led by {strongest_label} while {weakest_label} remains the next frontier.",
        "insight_mechanism": lesson,
        "insight_boundary": boundary,
    }


def _recursion_policy(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "docs", "recursion", "loop-policy.json", fallback={})
    return data if isinstance(data, dict) else {}


def _mutation_backlog(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = _json_artifact(payload, "artifacts", "recursion", "mutation_backlog.json", fallback=[])
    return data if isinstance(data, list) else []


def _heavy_backtest_queue(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = _json_artifact(payload, "artifacts", "recursion", "heavy_backtest_queue.json", fallback=[])
    return data if isinstance(data, list) else []


def _variety_backlog(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = _json_artifact(payload, "artifacts", "recursion", "variety_backlog.json", fallback=[])
    return data if isinstance(data, list) else []


def _contradiction_probes(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = _json_artifact(payload, "artifacts", "recursion", "contradiction_probes.json", fallback=[])
    return data if isinstance(data, list) else []


def _self_edit_queue(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = _json_artifact(payload, "artifacts", "recursion", "self_edit_queue.json", fallback=[])
    return data if isinstance(data, list) else []


def _self_edit_evaluations(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = _json_artifact(payload, "artifacts", "recursion", "self_edit_evaluations.json", fallback=[])
    return data if isinstance(data, list) else []


def _self_edit_audit(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "recursion", "self_edit_audit.json", fallback={})
    return data if isinstance(data, dict) else {}


def _recursion_audit(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "recursion", "recursion_audit.json", fallback={})
    return data if isinstance(data, dict) else {}


def _heavy_benchmark_summary(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "backtests", "heavy_backtest_summary.json", fallback={})
    return data if isinstance(data, dict) else {}


def _paper_trade_queue_artifact(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "paper_trade", "paper_trade_queue.json", fallback={})
    return data if isinstance(data, dict) else {}


def _paper_trade_summary(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "paper_trade", "paper_trade_summary.json", fallback={})
    return data if isinstance(data, dict) else {}


def _learning_loop_report(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "research", "learning_loop_report.json", fallback={})
    return data if isinstance(data, dict) else {}


def _backtest_loop_report(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "backtests", "backtest_loop_report.json", fallback={})
    return data if isinstance(data, dict) else {}


def _paper_trade_loop_report(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "paper_trade", "paper_trade_loop_report.json", fallback={})
    return data if isinstance(data, dict) else {}


def _research_scout_queue(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "research", "research_scout_queue.json", fallback={})
    return data if isinstance(data, dict) else {}


def _timeline_packs(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "research", "timeline_packs.json", fallback={})
    return data if isinstance(data, dict) else {}


def _timeline_pack_validation(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "research", "timeline_pack_validation.json", fallback={})
    return data if isinstance(data, dict) else {}


def _segment_regime_review(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "research", "segment_regime_review.json", fallback={})
    return data if isinstance(data, dict) else {}


def _pattern_regime_map(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "research", "pattern_regime_map.json", fallback={})
    return data if isinstance(data, dict) else {}


def _regime_match_review(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "research", "regime_match_review.json", fallback={})
    return data if isinstance(data, dict) else {}


def _data_intelligence_layers(payload: dict[str, Any]) -> list[dict[str, Any]]:
    runtime_root_raw = str(payload.get("runtime_root", "")).strip()
    if not runtime_root_raw:
        return []
    path = Path(runtime_root_raw) / "docs" / "research-ingest" / "data-intelligence-layers.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def _market_psychology_overlays(payload: dict[str, Any]) -> list[dict[str, Any]]:
    runtime_root_raw = str(payload.get("runtime_root", "")).strip()
    if not runtime_root_raw:
        return []
    path = Path(runtime_root_raw) / "docs" / "research-ingest" / "market-psychology-overlays.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def _market_psychology_case_studies(payload: dict[str, Any]) -> list[dict[str, Any]]:
    runtime_root_raw = str(payload.get("runtime_root", "")).strip()
    if not runtime_root_raw:
        return []
    path = Path(runtime_root_raw) / "docs" / "research-ingest" / "market-psychology-case-studies.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def _event_window_candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    runtime_root_raw = str(payload.get("runtime_root", "")).strip()
    if not runtime_root_raw:
        return []
    path = Path(runtime_root_raw) / "docs" / "research-ingest" / "event-window-candidates.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def _event_regime_classification_rubric(payload: dict[str, Any]) -> dict[str, Any]:
    runtime_root_raw = str(payload.get("runtime_root", "")).strip()
    if not runtime_root_raw:
        return {}
    path = Path(runtime_root_raw) / "docs" / "research-ingest" / "event-regime-classification-rubric.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _event_window_review(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "research", "event_window_review.json", fallback={})
    return data if isinstance(data, dict) else {}


def _intelligence_benchmark(payload: dict[str, Any]) -> dict[str, Any]:
    data = _json_artifact(payload, "artifacts", "research", "intelligence_benchmark.json", fallback={})
    return data if isinstance(data, dict) else {}


def evaluate(payload: dict) -> dict:
    runtime_root = Path(str(payload.get("runtime_root", "")).strip() or ".").resolve()
    metrics = run_backtest(_mutations(payload), runtime_root) or _score(_mutations(payload))
    stdout = "\n".join(
        [
            "profitability_score: " + str(metrics["profitability_score"]),
            "sharpe_ratio: " + str(metrics["sharpe_ratio"]),
            "max_drawdown: " + str(metrics["max_drawdown"]),
            "win_rate: " + str(metrics["win_rate"]),
            "paper_trade_readiness: " + str(metrics["paper_trade_readiness"]),
            "verdict_confidence: " + str(metrics["verdict_confidence"]),
        ]
    )
    result = {
        "claim": "Backtest profitability must be judged with drawdown, regime fit, and paper-trade readiness.",
        "verdict": metrics["verdict"],
        "mechanism": metrics["lesson"],
        "boundary": metrics["boundary"],
        "recommended_next_step": metrics["recommended_next_step"],
        "evidence_lane": "backtest_benchmark",
    }
    if "contract_count" in metrics:
        result["contract_count"] = metrics["contract_count"]
        result["covered_contract_count"] = metrics.get("covered_contract_count")
        result["trade_count"] = metrics.get("trade_count")
        result["minimum_trade_count"] = metrics.get("minimum_trade_count")
        result["trade_count_gate_pass"] = metrics.get("trade_count_gate_pass")
        result["holdout_profitability_score"] = metrics.get("holdout_profitability_score")
        result["walk_forward_consistency"] = metrics.get("walk_forward_consistency")
        result["walk_forward_stats"] = metrics.get("walk_forward_stats")
        result["stress_resilience"] = metrics.get("stress_resilience")
        result["stress_stats"] = metrics.get("stress_stats")
        result["regime_stats"] = metrics.get("regime_stats")
        result["data_mode"] = metrics.get("data_mode")
        result["requested_asset_universe"] = metrics.get("requested_asset_universe")
        result["requested_timeframe"] = metrics.get("requested_timeframe")
        result["evaluated_asset"] = metrics.get("evaluated_asset")
        result["evaluated_timeframe"] = metrics.get("evaluated_timeframe")
        result["data_fallback_reason"] = metrics.get("data_fallback_reason")
    return {
        "returncode": 0,
        "stdout": stdout,
        "stderr": "",
        "metrics": {
            "profitability_score": metrics["profitability_score"],
            "sharpe_ratio": metrics["sharpe_ratio"],
            "max_drawdown": metrics["max_drawdown"],
            "win_rate": metrics["win_rate"],
            "paper_trade_readiness": metrics["paper_trade_readiness"],
            "verdict_confidence": metrics["verdict_confidence"],
        },
        "result": result,
    }


def suggest(payload: dict) -> dict:
    rows = _benchmark_rows(payload)
    variety = _variety_backlog(payload)
    probes = _contradiction_probes(payload)
    ranked = _rank_benchmark_rows(rows)
    top = ranked[0] if ranked else {}
    top_metrics = _benchmark_metrics(top) if top else {}
    top_result = _benchmark_result(top) if top else {}
    top_mutations = _benchmark_mutations(top) if top else {}

    suggestions: list[dict[str, Any]] = []

    if len(ranked) >= 2:
        runner_up = ranked[1]
        runner_mutations = _benchmark_mutations(runner_up)
        proposed = dict(top_mutations)
        for key in ("doctrine_id", "strategy_id", "market_regime", "timeframe", "venue", "asset_universe", "paper_gate"):
            if runner_mutations.get(key) and proposed.get(key) != runner_mutations.get(key):
                proposed[key] = runner_mutations[key]
                break
        suggestions.append(
            _suggestion_entry(
                payload,
                candidate_id=f"cross-{top.get('candidate_id', 'leader')}-{runner_up.get('candidate_id', 'runner-up')}",
                candidate_summary=(
                    f"Cross the current leader `{top.get('candidate_id', 'unknown')}` with one mutation from "
                    f"`{runner_up.get('candidate_id', 'unknown')}` instead of adding a fresh doctrine blindly."
                ),
                hypothesis=(
                    "The benchmark already has a better frontier than the baseline-only loop. "
                    "Use the runner-up's strongest differing mutation as the next bounded probe."
                ),
                proposed_mutations=proposed,
                metadata={
                    "source": "top_cross_pollination",
                    "leader_candidate_id": top.get("candidate_id"),
                    "runner_up_candidate_id": runner_up.get("candidate_id"),
                },
            )
        )

    for item in variety:
        if len(suggestions) >= 3:
            break
        if not isinstance(item, dict):
            continue
        child_targets = item.get("suggested_child_targets", [])
        proposed = {}
        label = "variety child"
        if isinstance(child_targets, list) and child_targets:
            first_target = child_targets[0]
            if isinstance(first_target, dict):
                maybe_mutations = first_target.get("mutations", {})
                if isinstance(maybe_mutations, dict):
                    proposed = maybe_mutations
                label = str(first_target.get("label") or first_target.get("variety_child_label") or label)
        if not proposed:
            pending_labels = item.get("pending_child_labels", [])
            if isinstance(pending_labels, list) and pending_labels:
                label = str(pending_labels[0])
        suggestions.append(
            _suggestion_entry(
                payload,
                candidate_id=f"variety-{_line(item.get('strategy_family')).replace(' ', '-').lower()}-{_line(item.get('doctrine_family')).replace(' ', '-').lower()}",
                candidate_summary=(
                    f"Explore the uncovered variety backlog for `{_line(item.get('strategy_family'))}` under "
                    f"`{_line(item.get('doctrine_family'))}`."
                ),
                hypothesis=(
                    f"Variety backlog is still open on `{label}`. Closing those uncovered child combinations is "
                    "higher-signal than generic indicator churn."
                ),
                proposed_mutations=proposed,
                metadata={
                    "source": "variety_backlog",
                    "status": item.get("status"),
                    "target_contract_family": item.get("target_contract_family"),
                    "variety_family_id": item.get("variety_family_id"),
                },
            )
        )

    for probe in probes:
        if len(suggestions) >= 3:
            break
        if not isinstance(probe, dict):
            continue
        failure_modes = probe.get("failure_modes", [])
        top_mode = failure_modes[0] if isinstance(failure_modes, list) and failure_modes and isinstance(failure_modes[0], dict) else {}
        proposed = {
            "doctrine_id": probe.get("doctrine_id"),
            "strategy_id": probe.get("strategy_id"),
            "market_regime": probe.get("market_regime"),
        }
        suggestions.append(
            _suggestion_entry(
                payload,
                candidate_id=f"probe-{_line(probe.get('probe_id')).replace(' ', '-').lower()}",
                candidate_summary=(
                    f"Treat `{_line(probe.get('candidate_id'))}` as an explicit contradiction lane, "
                    "not a candidate to promote prematurely."
                ),
                hypothesis=(
                    f"Current failure surface is `{_line(top_mode.get('mode'))}`. "
                    f"{_line(top_mode.get('probe') or probe.get('probe_thesis'))}"
                ),
                proposed_mutations=proposed,
                metadata={
                    "source": "contradiction_probe",
                    "priority": probe.get("priority"),
                    "recommended_next_step": probe.get("recommended_next_step"),
                },
            )
        )

    if not suggestions:
        fallback = [
            _suggestion_entry(
                payload,
                candidate_id="bollinger-highvol-hyperliquid-1h",
                candidate_summary="Rotate into a higher-volatility breakout lane that actually improves the benchmark frontier.",
                hypothesis="The current trend/EMA baseline is too flat on this scenario, so a volatility-expansion doctrine with a squeeze breakout should lift profitability without relying on the stalled continuation template.",
                proposed_mutations={
                    "doctrine_id": "breakout_volatility_expansion",
                    "strategy_id": "bollinger_squeeze_breakout",
                    "market_regime": "high_vol",
                    "timeframe": "1h",
                    "venue": "hyperliquid",
                    "asset_universe": "BTC,ETH",
                    "paper_gate": "balanced",
                },
                metadata={"source": "static_fallback"},
            ),
            _suggestion_entry(
                payload,
                candidate_id="range-funding-ethsol-1h",
                candidate_summary="Probe whether funding dislocations work better under a range doctrine.",
                hypothesis="If the baseline is overfit to trend continuation, a range/funding lane should improve trade density and reduce flat benchmark outcomes.",
                proposed_mutations={
                    "doctrine_id": "mean_reversion_liquidity_reclaim",
                    "strategy_id": "funding_mean_revert",
                    "market_regime": "range",
                    "timeframe": "1h",
                    "venue": "bybit",
                    "asset_universe": "ETH,SOL",
                    "paper_gate": "balanced",
                },
                metadata={"source": "static_fallback"},
            ),
            _suggestion_entry(
                payload,
                candidate_id="riskfirst-ema-btc-4h",
                candidate_summary="Transfer the strongest risk doctrine onto a slower continuation expression.",
                hypothesis="Cross-pollination should raise paper-trade readiness if risk doctrine is genuinely portable, even if profitability only improves modestly.",
                proposed_mutations={
                    "doctrine_id": "risk_first_asymmetric_capture",
                    "strategy_id": "ema_pullback_long",
                    "market_regime": "trend",
                    "timeframe": "4h",
                    "venue": "binance",
                    "asset_universe": "BTC",
                    "paper_gate": "strict",
                },
                metadata={"source": "static_fallback"},
            ),
        ]
        suggestions.extend(fallback)

    limit = max(1, int(payload.get("limit", 3) or 3))
    cycle_count = int(_autoloop_state(payload).get("cycle_count", 0) or 0)
    variety_open = sum(1 for item in variety if isinstance(item, dict) and str(item.get("status", "")).endswith("pending"))
    reasons = [
        (
            f"Top benchmark candidate `{_line(top.get('candidate_id'))}` is at "
            f"WR `{float(top_metrics.get('win_rate', 0.0) or 0.0):.1%}` with "
            f"WF `{float(top_result.get('walk_forward_consistency', 0.0) or 0.0):.0%}` after `{cycle_count}` cycles."
        ),
        (
            f"`{variety_open}` variety families are still uncovered, so the next useful probes should come from "
            "known doctrine x strategy gaps rather than arbitrary indicator churn."
        ),
        (
            f"`{len(probes)}` contradiction probes are active; the next loop should mutate around failure surfaces, "
            "not promote on backtest residue alone."
        ),
    ]

    return {
        "baseline_metric": round(float(top_metrics.get("win_rate", 0.0) or 0.0), 4) if top else None,
        "reasons": reasons[:limit],
        "suggestions": suggestions[:limit],
    }


def packets(payload: dict) -> dict:
    state = _autoloop_state(payload)
    rows = _benchmark_rows(payload)
    cards = _doctrine_cards(payload)
    probes = _contradiction_probes(payload)
    summary = _heavy_benchmark_summary(payload)
    ranked = _rank_benchmark_rows(rows)
    cycle_count = int(state.get("cycle_count", 0) or 0)
    docs: list[dict[str, Any]] = []

    if ranked:
        top = ranked[0]
        top_metrics = _benchmark_metrics(top)
        top_result = _benchmark_result(top)
        contract_family = _line(summary.get("contract_family"))
        top_lines = [
            "# Autoloop Benchmark Evidence",
            "",
            f"- cycle_count: {cycle_count}",
            f"- candidate_count: {len(rows)}",
            f"- contract_family: {contract_family}",
            f"- top_candidate: {top.get('candidate_id', 'unknown')}",
            f"- win_rate: {float(top_metrics.get('win_rate', 0.0) or 0.0):.1%}",
            f"- sharpe_ratio: {float(top_metrics.get('sharpe_ratio', 0.0) or 0.0):.4f}",
            f"- max_drawdown: {float(top_metrics.get('max_drawdown', 1.0) or 1.0):.2%}",
            f"- walk_forward_consistency: {float(top_result.get('walk_forward_consistency', 0.0) or 0.0):.1%}",
            f"- trade_count: {int(top_result.get('trade_count', 0) or 0)}",
            f"- verdict: {top_result.get('verdict', 'unknown')}",
            "",
            "## Top 5 Candidates",
            "",
            "| Candidate | WR | Sharpe | WF | Verdict |",
            "|-----------|----|--------|----|---------|",
        ]
        for row in ranked[:5]:
            metrics = _benchmark_metrics(row)
            result = _benchmark_result(row)
            candidate_id = str(row.get("candidate_id", "?"))
            if len(candidate_id) > 44:
                candidate_id = candidate_id[:41] + "..."
            top_lines.append(
                f"| {candidate_id} | "
                f"{float(metrics.get('win_rate', 0.0) or 0.0):.1%} | "
                f"{float(metrics.get('sharpe_ratio', 0.0) or 0.0):.2f} | "
                f"{float(result.get('walk_forward_consistency', 0.0) or 0.0):.0%} | "
                f"{_line(result.get('verdict'))} |"
            )
        docs.append(
            {
                "kind": "benchmark_evidence",
                "slug": "crypto-autoloop-benchmark",
                "title": "Autoloop Benchmark Evidence",
                "content": "\n".join(top_lines),
                "memory_tier": "durable",
            }
        )

    strategy_stats: dict[str, list[float]] = {}
    doctrine_stats: dict[str, list[float]] = {}
    for row in rows:
        mutations = _benchmark_mutations(row)
        metrics = _benchmark_metrics(row)
        strategy_stats.setdefault(mutations.get("strategy_id", "unknown"), []).append(float(metrics.get("win_rate", 0.0) or 0.0))
        doctrine_stats.setdefault(mutations.get("doctrine_id", "unknown"), []).append(float(metrics.get("win_rate", 0.0) or 0.0))
    doctrine_lines = [
        "# Grounded Doctrine",
        "",
        f"Based on {len(rows)} heavy-backtest candidates across {cycle_count} autoloop cycles.",
        "",
        "## Strategy Family Performance",
        "",
        "| Strategy | Candidates | Best WR | Avg WR |",
        "|----------|------------|---------|--------|",
    ]
    for strategy_id, win_rates in sorted(strategy_stats.items(), key=lambda item: max(item[1]) if item[1] else 0.0, reverse=True)[:8]:
        doctrine_lines.append(
            f"| {strategy_id} | {len(win_rates)} | {max(win_rates):.1%} | {sum(win_rates)/len(win_rates):.1%} |"
        )
    doctrine_lines.extend([
        "",
        "## Doctrine Family Performance",
        "",
        "| Doctrine | Candidates | Best WR | Avg WR |",
        "|----------|------------|---------|--------|",
    ])
    for doctrine_id, win_rates in sorted(doctrine_stats.items(), key=lambda item: max(item[1]) if item[1] else 0.0, reverse=True)[:8]:
        doctrine_lines.append(
            f"| {doctrine_id} | {len(win_rates)} | {max(win_rates):.1%} | {sum(win_rates)/len(win_rates):.1%} |"
        )
    if cards:
        doctrine_lines.extend([
            "",
            f"## Doctrine Cards ({len(cards)} total)",
            "",
        ])
        for card in cards[:10]:
            doctrine_lines.append(
                f"- **{_line(card.get('card_id'))}**: {_line(card.get('title') or card.get('root_lesson') or card.get('mechanism'))}"
            )
    docs.append(
        {
            "kind": "grounded_doctrine",
            "slug": "crypto-autoloop-doctrine",
            "title": "Autoloop Grounded Doctrine",
            "content": "\n".join(doctrine_lines),
            "memory_tier": "durable",
        }
    )

    dead_ends = [row for row in rows if str(_benchmark_result(row).get("verdict", "")) == "reject"]
    reject_strategies: dict[str, int] = {}
    for row in dead_ends:
        strategy_id = _benchmark_mutations(row).get("strategy_id", "unknown")
        reject_strategies[strategy_id] = reject_strategies.get(strategy_id, 0) + 1
    boundary_lines = [
        "# Grounded Boundary (Dead Ends)",
        "",
        f"{len(dead_ends)} of {len(rows)} heavy-backtest candidates are currently rejected.",
        "",
        "## Common Rejection Patterns",
        "",
    ]
    for strategy_id, count in sorted(reject_strategies.items(), key=lambda item: item[1], reverse=True)[:5]:
        boundary_lines.append(f"- {strategy_id}: {count} rejections")
    if probes:
        boundary_lines.extend([
            "",
            f"## Active Contradictions ({len(probes)})",
            "",
        ])
        for probe in probes[:5]:
            if not isinstance(probe, dict):
                continue
            failure_modes = probe.get("failure_modes", [])
            top_mode = failure_modes[0] if isinstance(failure_modes, list) and failure_modes and isinstance(failure_modes[0], dict) else {}
            boundary_lines.append(
                f"- {_line(probe.get('probe_id'))}: {_line(top_mode.get('mode') or probe.get('recommended_next_step'))} "
                f"(priority {float(probe.get('priority', 0.0) or 0.0):.2f})"
            )
    docs.append(
        {
            "kind": "grounded_boundary",
            "slug": "crypto-autoloop-dead-ends",
            "title": "Autoloop Dead-End Patterns",
            "content": "\n".join(boundary_lines),
            "memory_tier": "durable",
        }
    )

    candidate = payload.get("candidate", {}) if isinstance(payload.get("candidate"), dict) else {}
    candidate_id = str(candidate.get("candidate_id", "global-baseline"))
    mutations = _mutations(payload)
    metrics = _score(mutations)
    publication_packet = _swarm_publication_packet(candidate_id, metrics, mutations)
    docs.append(
        {
            "kind": "benchmark_win_packet",
            "slug": "crypto-swarm-publication-" + candidate_id,
            "title": candidate_id + " Swarm Publication Packet",
            "content": json.dumps(publication_packet, indent=2, sort_keys=True),
            "memory_tier": "raw_run",
        }
    )
    return {"documents": docs, "publication_packet": publication_packet}


def _home_page(rows: list[dict[str, Any]]) -> str:
    candidates = _candidate_rows(rows)
    paper_ready = sum(1 for row in candidates if str(_row_chip_result(row).get("recommended_next_step", "")) == "queue_for_paper_trade")
    contradiction_count = sum(1 for row in candidates if str(_row_chip_result(row).get("recommended_next_step", "")) == "run_contradiction_probe")
    return "\n".join(
        [
            "# Crypto Trading Domain",
            "",
            "- chip: `domain-chip-crypto-trading`",
            "- evaluation: `backtest benchmark first, paper trade second`",
            f"- total_runs: `{len(rows)}`",
            f"- tested_candidates: `{len(candidates)}`",
            f"- paper_trade_ready: `{paper_ready}`",
            f"- contradiction_surfaces: `{contradiction_count}`",
            "",
            "## Benchmark Context",
            "",
            "- [[07-Domains/Crypto Trading/Backtest Leaderboard]]",
            "- [[07-Domains/Crypto Trading/Doctrine Registry]]",
            "- [[07-Domains/Crypto Trading/Strategy Catalog]]",
            "- [[07-Domains/Crypto Trading/Benchmark Bridge]]",
            "- [[07-Domains/Crypto Trading/Learning Loop]]",
            "- [[07-Domains/Crypto Trading/Backtest Loop]]",
            "- [[07-Domains/Crypto Trading/Paper Trade Queue]]",
            "- [[07-Domains/Crypto Trading/Paper Trade Outcomes]]",
            "- [[07-Domains/Crypto Trading/Paper Trade Loop]]",
            "- [[07-Domains/Crypto Trading/Contradictions]]",
            "- [[07-Domains/Crypto Trading/Next Probes]]",
            "- [[07-Domains/Crypto Trading/Research Sources]]",
            "- [[07-Domains/Crypto Trading/Next to Research]]",
            "- [[07-Domains/Crypto Trading/Research Scout Queue]]",
            "- [[07-Domains/Crypto Trading/Market Regime Intelligence]]",
            "- [[07-Domains/Crypto Trading/Timeline Packs]]",
            "- [[07-Domains/Crypto Trading/Timeline Pack Validation]]",
            "- [[07-Domains/Crypto Trading/Regime Match Review]]",
            "- [[07-Domains/Crypto Trading/Pattern Regime Pairing]]",
            "- [[07-Domains/Crypto Trading/Doctrine Cards]]",
        "- [[07-Domains/Crypto Trading/Recursive Flywheel]]",
        "- [[07-Domains/Crypto Trading/Mutation Backlog]]",
        "- [[07-Domains/Crypto Trading/Heavy Backtest Queue]]",
        "- [[07-Domains/Crypto Trading/Self Edit Queue]]",
        "- [[07-Domains/Crypto Trading/Recursion Audit]]",
            "- [[07-Domains/Crypto Trading/Flywheel]]",
            "- [[07-Domains/Crypto Trading/Loop Progression]]",
            "",
            "## Current Read",
            "",
            "- backtest should decide whether the mechanism is real inside a fixed lane",
            "- the bridge should decide whether the result deserves promotion",
            "- paper trade should answer operational realism, not benchmark truth",
            "- regime-aware strategy selection should beat one-recipe-fits-all benchmarking",
            "- recursion should only mutate the loop through source-grounded proposals and heavy-backtest evidence",
        ]
    )


def _leaderboard_page(rows: list[dict[str, Any]], benchmark_summary: dict[str, Any]) -> str:
    lines = ["# Backtest Leaderboard", "", "This page is the benchmark-facing surface for current doctrine and strategy combinations.", ""]
    benchmark_rows = benchmark_summary.get("rows", []) if isinstance(benchmark_summary.get("rows"), list) else []
    if benchmark_rows:
        lines.extend(
            [
                f"- benchmark_kind: `{_line(benchmark_summary.get('benchmark_kind'))}`",
                f"- contract_family: `{_line(benchmark_summary.get('contract_family'))}`",
                f"- candidate_count: `{_line(benchmark_summary.get('candidate_count'))}`",
                "",
            ]
        )
        for item in benchmark_rows[:8]:
            if not isinstance(item, dict):
                continue
            metrics = item.get("metrics", {}) if isinstance(item.get("metrics"), dict) else {}
            mutations = item.get("mutations", {}) if isinstance(item.get("mutations"), dict) else {}
            result = item.get("result", {}) if isinstance(item.get("result"), dict) else {}
            regime_stats = result.get("regime_stats", {}) if isinstance(result.get("regime_stats"), dict) else {}
            lines.extend(
                [
                    f"## {item.get('candidate_id', 'unknown')}",
                    "",
                    f"- doctrine_id: `{_line(mutations.get('doctrine_id'))}`",
                    f"- strategy_id: `{_line(mutations.get('strategy_id'))}`",
                    f"- market_regime: `{_line(mutations.get('market_regime'))}`",
                    f"- profitability_score: `{_line(metrics.get('profitability_score'))}`",
                    f"- sharpe_ratio: `{_line(metrics.get('sharpe_ratio'))}`",
                    f"- max_drawdown: `{_line(metrics.get('max_drawdown'))}`",
                    f"- paper_trade_readiness: `{_line(metrics.get('paper_trade_readiness'))}`",
                    f"- contract_count: `{_line(result.get('contract_count'))}`",
                    f"- covered_contract_count: `{_line(result.get('covered_contract_count'))}`",
                    f"- trade_count: `{_line(result.get('trade_count'))}`",
                    f"- minimum_trade_count: `{_line(result.get('minimum_trade_count'))}`",
                    f"- trade_count_gate_pass: `{_line(result.get('trade_count_gate_pass'))}`",
                    f"- holdout_profitability_score: `{_line(result.get('holdout_profitability_score'))}`",
                    f"- walk_forward_consistency: `{_line(result.get('walk_forward_consistency'))}`",
                    f"- stress_resilience: `{_line(result.get('stress_resilience'))}`",
                    f"- data_mode: `{_line(result.get('data_mode'))}`",
                    f"- recommended_next_step: `{_line(result.get('recommended_next_step'))}`",
                    "",
                ]
            )
            walk_forward_stats = result.get("walk_forward_stats", []) if isinstance(result.get("walk_forward_stats"), list) else []
            if regime_stats:
                lines.append("### Regime Segments")
                lines.append("")
                for regime, stats in regime_stats.items():
                    if not isinstance(stats, dict):
                        continue
                    lines.append(f"- {regime}: trades=`{_line(stats.get('trade_count'))}` win_rate=`{_line(stats.get('win_rate'))}` avg_return=`{_line(stats.get('avg_return'))}`")
                lines.append("")
            if walk_forward_stats:
                lines.append("### Walk-Forward Segments")
                lines.append("")
                for stats in walk_forward_stats:
                    if not isinstance(stats, dict):
                        continue
                    lines.append(
                        f"- {_line(stats.get('segment_id'))}: trades=`{_line(stats.get('trade_count'))}` profitability=`{_line(stats.get('profitability_score'))}` win_rate=`{_line(stats.get('win_rate'))}` gate=`{_line(stats.get('trade_count_gate_pass'))}`"
                    )
                lines.append("")
            stress_stats = result.get("stress_stats", {}) if isinstance(result.get("stress_stats"), dict) else {}
            if stress_stats:
                lines.append("### Stress Scenarios")
                lines.append("")
                for label, stats in stress_stats.items():
                    if not isinstance(stats, dict):
                        continue
                    lines.append(
                        f"- {label}: trades=`{_line(stats.get('trade_count'))}` profitability=`{_line(stats.get('profitability_score'))}` avg_return=`{_line(stats.get('avg_return'))}` gate=`{_line(stats.get('trade_count_gate_pass'))}`"
                    )
                lines.append("")
        return "\n".join(lines)
    ranked = _sort_rows(_candidate_rows(rows))
    if not ranked:
        lines.append("- No benchmark candidate rows recorded yet.")
        return "\n".join(lines)
    for row in ranked[:8]:
        metrics = _row_metrics(row)
        mutations = _row_mutations(row)
        result = _row_chip_result(row)
        lines.extend(
            [
                f"## {row.get('candidate_id', 'unknown')}",
                "",
                f"- doctrine_id: `{_line(mutations.get('doctrine_id'))}`",
                f"- strategy_id: `{_line(mutations.get('strategy_id'))}`",
                f"- market_regime: `{_line(mutations.get('market_regime'))}`",
                f"- profitability_score: `{_line(metrics.get('profitability_score'))}`",
                f"- sharpe_ratio: `{_line(metrics.get('sharpe_ratio'))}`",
                f"- max_drawdown: `{_line(metrics.get('max_drawdown'))}`",
                f"- paper_trade_readiness: `{_line(metrics.get('paper_trade_readiness'))}`",
                f"- contract_count: `{_line(result.get('contract_count'))}`",
                f"- covered_contract_count: `{_line(result.get('covered_contract_count'))}`",
                f"- trade_count: `{_line(result.get('trade_count'))}`",
                f"- data_mode: `{_line(result.get('data_mode'))}`",
                "",
            ]
        )
    return "\n".join(lines)


def _research_sources_page(sources: list[dict[str, Any]]) -> str:
    lines = [
        "# Research Sources",
        "",
        "These are the current approved doctrine-building sources for `BTC up/down 15m`.",
        "",
        f"- approved_source_count: `{len(sources)}`",
        "",
    ]
    if not sources:
        lines.append("- No approved sources configured yet.")
        return "\n".join(lines)
    for item in sources:
        title = str(item.get("title", "unknown"))
        author = str(item.get("author", "unknown"))
        url = str(item.get("url", ""))
        direct_access = str(item.get("direct_access", "")).strip()
        tags = item.get("doctrine_tags", [])
        tags = tags if isinstance(tags, list) else []
        block = [
            f"## {title}",
            "",
            f"- author: `{author}`",
            f"- style_family: `{_line(item.get('style_family'))}`",
            f"- source_type: `{_line(item.get('source_type'))}`",
            f"- doctrine_tags: `{', '.join(str(tag) for tag in tags)}`",
            f"- why_relevant: {item.get('why_relevant', 'n/a')}",
        ]
        if direct_access:
            block.append(f"- direct_access: {direct_access}")
        block.extend(
            [
                f"- source: {url}",
                "",
            ]
        )
        lines.extend(block)
    return "\n".join(lines)


def _research_backlog_page(backlog: dict[str, Any]) -> str:
    candidate_rows = backlog.get("candidate_rows", []) if isinstance(backlog.get("candidate_rows"), list) else []
    style_rows = backlog.get("style_rows", []) if isinstance(backlog.get("style_rows"), list) else []
    lines = [
        "# Research Backlog",
        "",
        "This page tracks source and trader expansion before those ideas become doctrine packets or cards.",
        "",
        f"- approved_source_count: `{_line(backlog.get('approved_source_count'))}`",
        f"- trader_candidate_count: `{_line(backlog.get('trader_candidate_count'))}`",
        f"- ready_for_source_ingest_count: `{_line(backlog.get('ready_for_source_ingest_count'))}`",
        f"- approved_waiting_packet_count: `{_line(backlog.get('approved_waiting_packet_count'))}`",
        f"- packet_count: `{_line(backlog.get('packet_count'))}`",
        f"- card_count: `{_line(backlog.get('card_count'))}`",
        f"- next_to_research_count: `{_line(backlog.get('next_to_research_count'))}`",
        f"- regime_intelligence_count: `{_line(backlog.get('regime_intelligence_count'))}`",
        "",
        "## Top Ready Candidates",
        "",
    ]
    if not candidate_rows:
        lines.append("- No research backlog artifacts recorded yet.")
    for item in candidate_rows[:8]:
        lines.extend(
            [
                f"### {item.get('name', 'unknown')}",
                "",
                f"- status: `{_line(item.get('status'))}`",
                f"- style_family: `{_line(item.get('style_family'))}`",
                f"- priority_tier: `{_line(item.get('priority_tier'))}`",
                f"- access_type: `{_line(item.get('access_type'))}`",
                f"- access_url: `{_line(item.get('access_url'))}`",
                f"- methodology_access: `{_line(item.get('methodology_access'))}`",
                "",
            ]
        )
    lines.extend(["## Style Coverage", ""])
    for item in style_rows[:8]:
        lines.extend(
            [
                f"### {item.get('style_family', 'unknown')}",
                "",
                f"- coverage_status: `{_line(item.get('coverage_status'))}`",
                f"- approved_source_count: `{_line(item.get('approved_source_count'))}`",
                f"- packet_count: `{_line(item.get('packet_count'))}`",
                f"- card_count: `{_line(item.get('card_count'))}`",
                "",
            ]
        )
    return "\n".join(lines)


def _next_to_research_page(backlog: dict[str, Any]) -> str:
    rows = backlog.get("futurelog_rows", []) if isinstance(backlog.get("futurelog_rows"), list) else []
    lines = [
        "# Next to Research",
        "",
        "This page is the futurelog for doctrine scouting. It should capture what deserves research next before it becomes packet backlog or mutation backlog.",
        "",
        f"- futurelog_count: `{_line(backlog.get('next_to_research_count'))}`",
        "",
    ]
    if not rows:
        lines.append("- No futurelog items recorded yet.")
        return "\n".join(lines)
    for item in rows:
        style_families = item.get("style_families", [])
        style_families = style_families if isinstance(style_families, list) else []
        source_names = item.get("source_names", [])
        source_names = source_names if isinstance(source_names, list) else []
        target_regimes = item.get("target_regimes", [])
        target_regimes = target_regimes if isinstance(target_regimes, list) else []
        child_shapes = item.get("expected_child_shapes", [])
        child_shapes = child_shapes if isinstance(child_shapes, list) else []
        lines.extend(
            [
                f"## {item.get('title', 'unknown')}",
                "",
                f"- item_id: `{_line(item.get('item_id'))}`",
                f"- priority: `{_line(item.get('priority'))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- style_families: `{', '.join(str(value) for value in style_families)}`",
                f"- source_names: `{', '.join(str(value) for value in source_names)}`",
                f"- target_regimes: `{', '.join(str(value) for value in target_regimes)}`",
                f"- expected_child_shapes: `{', '.join(str(value) for value in child_shapes)}`",
                f"- why_now: {item.get('why_now', 'n/a')}",
                "",
            ]
        )
    return "\n".join(lines)


def _market_regime_intelligence_page(backlog: dict[str, Any]) -> str:
    rows = backlog.get("regime_rows", []) if isinstance(backlog.get("regime_rows"), list) else []
    lines = [
        "# Market Regime Intelligence",
        "",
        "This page tracks which pattern families should be tested in which BTC market conditions, and which timeline packs still need archive expansion.",
        "",
        f"- regime_intelligence_count: `{_line(backlog.get('regime_intelligence_count'))}`",
        "",
    ]
    if not rows:
        lines.append("- No regime intelligence recorded yet.")
        return "\n".join(lines)
    for item in rows:
        fit_patterns = item.get("fit_patterns", [])
        fit_patterns = fit_patterns if isinstance(fit_patterns, list) else []
        avoid_patterns = item.get("avoid_patterns", [])
        avoid_patterns = avoid_patterns if isinstance(avoid_patterns, list) else []
        research_gaps = item.get("research_gaps", [])
        research_gaps = research_gaps if isinstance(research_gaps, list) else []
        windows = item.get("benchmark_window_targets", [])
        windows = windows if isinstance(windows, list) else []
        lines.extend(
            [
                f"## {item.get('label', 'unknown')}",
                "",
                f"- regime_id: `{_line(item.get('regime_id'))}`",
                f"- priority: `{_line(item.get('priority'))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- market_character: {item.get('market_character', 'n/a')}",
                f"- fit_patterns: `{', '.join(str(value) for value in fit_patterns)}`",
                f"- avoid_patterns: `{', '.join(str(value) for value in avoid_patterns)}`",
                f"- research_gaps: `{', '.join(str(value) for value in research_gaps)}`",
                "",
                "### Benchmark Window Targets",
                "",
            ]
        )
        for window in windows:
            if not isinstance(window, dict):
                continue
            lines.extend(
                [
                    f"- `{_line(window.get('window_id'))}` | `{_line(window.get('status'))}` | `{_line(window.get('start_date'))}` -> `{_line(window.get('end_date'))}` | {window.get('reason', 'n/a')}",
                ]
            )
        lines.append("")
    return "\n".join(lines)


def _regime_taxonomy_confidence_page(backlog: dict[str, Any], validation: dict[str, Any]) -> str:
    regime_rows = backlog.get("regime_rows", []) if isinstance(backlog.get("regime_rows"), list) else []
    validation_rows = validation.get("rows", []) if isinstance(validation.get("rows"), list) else []
    validation_by_regime: dict[str, list[dict[str, Any]]] = {}
    for row in validation_rows:
        if not isinstance(row, dict):
            continue
        validation_by_regime.setdefault(str(row.get("regime_id", "")).strip(), []).append(row)

    lines = [
        "# Regime Taxonomy and Confidence",
        "",
        "This page explains how the chip decides what kind of market BTC is in. We do not use only `bullish`, `bearish`, or `choppy`; we classify by path behavior, volatility shape, and execution conditions.",
        "",
        "## What We Measure",
        "",
        "- `directional_efficiency`: how straight the market path is versus noisy back-and-forth travel",
        "- `sign_flip_rate`: how often short-horizon returns reverse direction",
        "- `mean_abs_return_pct` and `p99_abs_return_pct`: how violent the minute and daily moves are",
        "- `breakout_burst_ratio`: whether moves arrive in shock bursts or steadier continuation",
        "- `4h` metrics: execution-window behavior, which matters more than 1m noise alone",
        "- `1d net_return_pct` and `1d directional_efficiency`: whether the broader path is persistent, balanced, or unstable",
        "",
        "## Confidence Levels",
        "",
        "- `validated_match`: the extracted pack behaves like the regime it claims to represent",
        "- `mixed_proxy`: the pack is usable, but it shares traits with another regime and should be treated cautiously",
        "- `mismatch_review`: the pack is mislabeled and should not drive benchmark routing",
        "- `pending_extract`: the regime idea exists, but the dataset is not ready yet",
        "",
        "## Current Regime Varieties",
        "",
        "These are the current market-condition varieties the chip cares about beyond simple bullish/bearish/choppy labels:",
        "",
        "- `trend_continuation_greed`: directional persistence, breakout acceptance, shallow pullbacks, greed dominating hesitation",
        "- `range_chop_mean_reversion`: two-way flow, weak follow-through, reclaim and fade setups outperform breakout chase",
        "- `fear_shock_high_alert`: abrupt volatility bursts, fear dominating, execution fragility amplified",
        "- `compression_pre_breakout`: low directional conviction before a release window, where quality matters more than participation",
        "- `event_driven_macro_transition`: headline or macro-sensitive windows where structure can change faster than pattern persistence",
        "",
        "Potential subtypes that are starting to matter but are not yet first-class benchmark regimes:",
        "",
        "- `greed_dominant` vs `fear_dominant` state overlays",
        "- `high_vol` expansion that is not necessarily panic",
        "- `chop_transition` where the market rotates out of trend but has not settled into clean balance",
        "",
    ]
    for item in regime_rows:
        if not isinstance(item, dict):
            continue
        regime_id = str(item.get("regime_id", "")).strip()
        rows = validation_by_regime.get(regime_id, [])
        validated = [row for row in rows if str(row.get("validation_status", "")).strip() == "validated_match"]
        mixed = [row for row in rows if str(row.get("validation_status", "")).strip() == "mixed_proxy"]
        mismatch = [row for row in rows if str(row.get("validation_status", "")).strip() == "mismatch_review"]
        fit_patterns = item.get("fit_patterns", [])
        fit_patterns = fit_patterns if isinstance(fit_patterns, list) else []
        avoid_patterns = item.get("avoid_patterns", [])
        avoid_patterns = avoid_patterns if isinstance(avoid_patterns, list) else []
        lines.extend(
            [
                f"## {item.get('label', 'unknown')}",
                "",
                f"- regime_id: `{_line(regime_id)}`",
                f"- current_status: `{_line(item.get('status'))}`",
                f"- validated_pack_count: `{len(validated)}`",
                f"- mixed_pack_count: `{len(mixed)}`",
                f"- mismatch_pack_count: `{len(mismatch)}`",
                f"- confidence_read: `high`" if validated else f"- confidence_read: `medium`" if mixed else f"- confidence_read: `low`" if mismatch else f"- confidence_read: `design-only`",
                f"- what_we_are_trying_to_understand: {item.get('market_character', 'n/a')}",
                f"- fit_patterns: `{', '.join(str(value) for value in fit_patterns)}`",
                f"- avoid_patterns: `{', '.join(str(value) for value in avoid_patterns)}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Timing Intelligence Read",
            "",
            "This chip is trying to understand timing in three layers at once:",
            "",
            "- broad state: is BTC acting like trend, balance, fear-shock, compression, or event transition?",
            "- execution state: do the 4h and 15m windows support participation or abstention?",
            "- pattern state: should we route toward continuation, reclaim, reversal, squeeze, or no-trade logic?",
            "",
            "The important point is that `bullish`, `bearish`, and `choppy` are not enough. Two bullish periods can require different patterns if one is greed-driven continuation and the other is event-fragile with shock bursts.",
        ]
    )
    return "\n".join(lines)


def _research_scout_queue_page(queue: dict[str, Any]) -> str:
    rows = queue.get("rows", []) if isinstance(queue.get("rows"), list) else []
    lines = [
        "# Research Scout Queue",
        "",
        "This page is the ranked scout feed that should drive the research automation before it invents anything new.",
        "",
        f"- queue_count: `{_line(queue.get('queue_count'))}`",
        f"- generated_from: `{_line(queue.get('generated_from'))}`",
        "",
    ]
    if not rows:
        lines.append("- No research scout queue rows recorded yet.")
        return "\n".join(lines)
    for item in rows[:12]:
        style_families = item.get("style_families", [])
        style_families = style_families if isinstance(style_families, list) else []
        source_names = item.get("source_names", [])
        source_names = source_names if isinstance(source_names, list) else []
        target_regimes = item.get("target_regimes", [])
        target_regimes = target_regimes if isinstance(target_regimes, list) else []
        expected = item.get("expected_child_shapes", [])
        expected = expected if isinstance(expected, list) else []
        replacement_pack_ids = item.get("replacement_pack_ids", [])
        replacement_pack_ids = replacement_pack_ids if isinstance(replacement_pack_ids, list) else []
        lines.extend(
            [
                f"## {item.get('title', 'unknown')}",
                "",
                f"- queue_id: `{_line(item.get('queue_id'))}`",
                f"- queue_kind: `{_line(item.get('queue_kind'))}`",
                f"- priority_score: `{_line(item.get('priority_score'))}`",
                f"- priority_tier: `{_line(item.get('priority_tier'))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- recommended_action: `{_line(item.get('recommended_action'))}`",
                f"- style_families: `{', '.join(str(value) for value in style_families)}`",
                f"- source_names: `{', '.join(str(value) for value in source_names)}`",
                f"- target_regimes: `{', '.join(str(value) for value in target_regimes)}`",
                f"- expected_child_shapes: `{', '.join(str(value) for value in expected)}`",
                f"- dataset_ready: `{_line(item.get('dataset_ready'))}`",
                f"- validation_status: `{_line(item.get('validation_status'))}`",
                f"- predicted_regime_id: `{_line(item.get('predicted_regime_id'))}`",
                f"- review_outcome: `{_line(item.get('review_outcome'))}`",
                f"- replacement_pack_ids: `{', '.join(str(value) for value in replacement_pack_ids)}`",
                f"- reason: {item.get('reason', 'n/a')}",
                "",
            ]
        )
    return "\n".join(lines)


def _data_intelligence_layers_page(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Data and Intelligence Layers",
        "",
        "This page tracks the external data and intelligence layers that can improve regime timing, context, and execution realism without pretending they replace backtests or paper trade.",
        "",
        f"- layer_count: `{len(rows)}`",
        "",
        "## Design Rule",
        "",
        "- base market data should stay simple and trustworthy",
        "- context layers should explain when a pattern should be filtered, not force trades by themselves",
        "- venue layers exist for execution truth, not alpha inflation",
        "- manual event classification is still required where APIs are too noisy or too generic",
        "",
    ]
    if not rows:
        lines.append("- No data or intelligence layers recorded yet.")
        return "\n".join(lines)
    for item in rows:
        helps_with = item.get("helps_with", [])
        helps_with = helps_with if isinstance(helps_with, list) else []
        best_for_regimes = item.get("best_for_regimes", [])
        best_for_regimes = best_for_regimes if isinstance(best_for_regimes, list) else []
        signals = item.get("signals", [])
        signals = signals if isinstance(signals, list) else []
        urls = item.get("source_urls", [])
        urls = urls if isinstance(urls, list) else []
        lines.extend(
            [
                f"## {item.get('label', 'unknown')}",
                "",
                f"- layer_id: `{_line(item.get('layer_id'))}`",
                f"- layer_type: `{_line(item.get('layer_type'))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- confidence: `{_line(item.get('confidence'))}`",
                f"- api_kind: `{_line(item.get('api_kind'))}`",
                f"- cost_profile: `{_line(item.get('cost_profile'))}`",
                f"- best_for_regimes: `{', '.join(str(value) for value in best_for_regimes)}`",
                f"- helps_with: `{', '.join(str(value) for value in helps_with)}`",
                f"- signals: `{', '.join(str(value) for value in signals)}`",
                f"- why_it_matters: {item.get('why_it_matters', 'n/a')}",
                f"- source_urls: `{', '.join(str(value) for value in urls)}`",
                "",
            ]
        )
    return "\n".join(lines)


def _market_psychology_overlays_page(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Market Psychology Overlays",
        "",
        "This page tracks the human-response overlays that sit above pure price structure: expectation, crowding, sell-the-news risk, reflexivity, and second-order consequences.",
        "",
        f"- overlay_count: `{len(rows)}`",
        "",
        "## Design Rule",
        "",
        "- psychology should explain why the same event resolves differently in different regimes",
        "- overlays should filter or reshape participation, not override observed path evidence",
        "- first reaction and durable consequence should be treated separately",
        "",
    ]
    if not rows:
        lines.append("- No market psychology overlays recorded yet.")
        return "\n".join(lines)
    for item in rows:
        what_it_changes = item.get("what_it_changes", [])
        what_it_changes = what_it_changes if isinstance(what_it_changes, list) else []
        watch_for = item.get("watch_for", [])
        watch_for = watch_for if isinstance(watch_for, list) else []
        best_used_in = item.get("best_used_in", [])
        best_used_in = best_used_in if isinstance(best_used_in, list) else []
        urls = item.get("source_urls", [])
        urls = urls if isinstance(urls, list) else []
        lines.extend(
            [
                f"## {item.get('label', 'unknown')}",
                "",
                f"- overlay_id: `{_line(item.get('overlay_id'))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- confidence: `{_line(item.get('confidence'))}`",
                f"- best_used_in: `{', '.join(str(value) for value in best_used_in)}`",
                f"- core_rule: {item.get('core_rule', 'n/a')}",
                f"- what_it_changes: `{', '.join(str(value) for value in what_it_changes)}`",
                f"- watch_for: `{', '.join(str(value) for value in watch_for)}`",
                f"- danger_if_missed: {item.get('danger_if_missed', 'n/a')}",
                f"- source_urls: `{', '.join(str(value) for value in urls)}`",
                "",
            ]
        )
    return "\n".join(lines)


def _market_psychology_case_studies_page(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Market Psychology Cases",
        "",
        "This page captures event and regime examples where human interpretation, expectation, and second-order consequences mattered more than the first headline reaction alone.",
        "",
        f"- case_count: `{len(rows)}`",
        "",
    ]
    if not rows:
        lines.append("- No market psychology case studies recorded yet.")
        return "\n".join(lines)
    for item in rows:
        lessons = item.get("primary_lessons", [])
        lessons = lessons if isinstance(lessons, list) else []
        overlays = item.get("psychology_overlays", [])
        overlays = overlays if isinstance(overlays, list) else []
        implications = item.get("regime_implications", [])
        implications = implications if isinstance(implications, list) else []
        urls = item.get("source_urls", [])
        urls = urls if isinstance(urls, list) else []
        lines.extend(
            [
                f"## {item.get('label', 'unknown')}",
                "",
                f"- case_id: `{_line(item.get('case_id'))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- market_phase: `{_line(item.get('market_phase'))}`",
                f"- summary: {item.get('summary', 'n/a')}",
                f"- primary_lessons: `{', '.join(str(value) for value in lessons)}`",
                f"- psychology_overlays: `{', '.join(str(value) for value in overlays)}`",
                f"- regime_implications: `{', '.join(str(value) for value in implications)}`",
                f"- source_urls: `{', '.join(str(value) for value in urls)}`",
                "",
            ]
        )
    return "\n".join(lines)


def _event_window_candidates_page(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Event Window Candidates",
        "",
        "This page tracks concrete macro or headline windows we may use to design the missing event-driven timing regime. These are not trusted benchmark packs yet; they are candidate windows that need classification work.",
        "",
        f"- candidate_count: `{len(rows)}`",
        "",
        "## Design Rule",
        "",
        "- event windows should be classified before they are benchmarked",
        "- transition and panic shock are not the same thing",
        "- scheduled macro releases and BTC-specific repricing events should be compared explicitly",
        "",
    ]
    if not rows:
        lines.append("- No event window candidates recorded yet.")
        return "\n".join(lines)
    for item in rows:
        signals = item.get("what_to_measure", [])
        signals = signals if isinstance(signals, list) else []
        urls = item.get("source_urls", [])
        urls = urls if isinstance(urls, list) else []
        lines.extend(
            [
                f"## {item.get('label', 'unknown')}",
                "",
                f"- candidate_id: `{_line(item.get('candidate_id'))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- proposed_classification: `{_line(item.get('proposed_classification'))}`",
                f"- classification_confidence: `{_line(item.get('classification_confidence'))}`",
                f"- event_type: `{_line(item.get('event_type'))}`",
                f"- start_date: `{_line(item.get('start_date'))}`",
                f"- end_date: `{_line(item.get('end_date'))}`",
                f"- use_case: {item.get('use_case', 'n/a')}",
                f"- reason_to_track: {item.get('reason_to_track', 'n/a')}",
                f"- what_to_measure: `{', '.join(str(value) for value in signals)}`",
                f"- source_urls: `{', '.join(str(value) for value in urls)}`",
                "",
            ]
        )
    return "\n".join(lines)


def _event_regime_classification_rubric_page(payload: dict[str, Any]) -> str:
    signals = payload.get("signals", [])
    signals = signals if isinstance(signals, list) else []
    rules = payload.get("classification_rules", [])
    rules = rules if isinstance(rules, list) else []
    design_rules = payload.get("design_rules", [])
    design_rules = design_rules if isinstance(design_rules, list) else []
    next_actions = payload.get("next_actions", {})
    next_actions = next_actions if isinstance(next_actions, dict) else {}
    lines = [
        "# Event Regime Classification Rubric",
        "",
        "This page defines how candidate event windows should be classified before they become benchmark packs.",
        "",
        f"- rubric_id: `{_line(payload.get('rubric_id'))}`",
        f"- purpose: {payload.get('purpose', 'n/a')}",
        "",
        "## Design Rules",
        "",
    ]
    for item in design_rules:
        lines.append(f"- {item}")
    lines.extend(["", "## Signals", ""])
    for item in signals:
        if not isinstance(item, dict):
            continue
        lines.extend(
            [
                f"### {item.get('signal_id', 'unknown')}",
                "",
                f"- priority: `{_line(item.get('priority'))}`",
                f"- role: {item.get('role', 'n/a')}",
                "",
            ]
        )
    lines.extend(["## Classification Rules", ""])
    for item in rules:
        if not isinstance(item, dict):
            continue
        conditions = item.get("conditions", [])
        conditions = conditions if isinstance(conditions, list) else []
        lines.extend(
            [
                f"### {item.get('label', 'unknown')}",
                "",
            ]
        )
        for condition in conditions:
            lines.append(f"- {condition}")
        lines.append("")
    lines.extend(["## Next Actions", ""])
    for key, value in next_actions.items():
        lines.append(f"- `{key}` -> {value}")
    return "\n".join(lines)


def _event_window_review_page(payload: dict[str, Any]) -> str:
    rows = payload.get("rows", []) if isinstance(payload.get("rows"), list) else []
    lines = [
        "# Event Window Review",
        "",
        "This page applies the event-regime rubric to current candidate windows so only credible candidates move toward timeline-pack extraction.",
        "",
        f"- candidate_count: `{_line(payload.get('candidate_count'))}`",
        f"- classified_count: `{_line(payload.get('classified_count'))}`",
        f"- mixed_review_count: `{_line(payload.get('mixed_review_count'))}`",
        f"- needs_narrowing_count: `{_line(payload.get('needs_narrowing_count'))}`",
        "",
    ]
    if not rows:
        lines.append("- No event window review rows recorded yet.")
        return "\n".join(lines)
    for item in rows:
        notes = item.get("notes", [])
        notes = notes if isinstance(notes, list) else []
        signals = item.get("what_to_measure", [])
        signals = signals if isinstance(signals, list) else []
        overlays = item.get("psychology_overlay_ids", [])
        overlays = overlays if isinstance(overlays, list) else []
        lines.extend(
            [
                f"## {item.get('label', 'unknown')}",
                "",
                f"- candidate_id: `{_line(item.get('candidate_id'))}`",
                f"- event_type: `{_line(item.get('event_type'))}`",
                f"- proposed_classification: `{_line(item.get('proposed_classification'))}`",
                f"- predicted_classification: `{_line(item.get('predicted_classification'))}`",
                f"- proposed_score: `{_line(item.get('proposed_score'))}`",
                f"- predicted_score: `{_line(item.get('predicted_score'))}`",
                f"- mixed_score: `{_line(item.get('mixed_score'))}`",
                f"- review_status: `{_line(item.get('review_status'))}`",
                f"- recommended_action: `{_line(item.get('recommended_action'))}`",
                f"- fear_greed_role: `{_line(item.get('fear_greed_role'))}`",
                f"- expectation_state: `{_line(item.get('expectation_state'))}`",
                f"- psychology_read: `{_line(item.get('psychology_read'))}`",
                f"- crowding_risk: `{_line(item.get('crowding_risk'))}`",
                f"- second_order_horizon: `{_line(item.get('second_order_horizon'))}`",
                f"- psychology_overlay_ids: `{', '.join(str(value) for value in overlays)}`",
                f"- what_to_measure: `{', '.join(str(value) for value in signals)}`",
                "",
            ]
        )
        if notes:
            lines.append("### Notes")
            lines.append("")
            for note in notes:
                lines.append(f"- {note}")
            lines.append("")
    return "\n".join(lines)


def _intelligence_system_audit_page(
    pattern_map: dict[str, Any],
    event_window_review: dict[str, Any],
    backtest_loop_report: dict[str, Any],
    timeline_pack_validation: dict[str, Any],
) -> str:
    regime_rows = pattern_map.get("regime_rows", []) if isinstance(pattern_map.get("regime_rows"), list) else []
    pattern_rows = pattern_map.get("pattern_rows", []) if isinstance(pattern_map.get("pattern_rows"), list) else []
    validated_regimes = [
        item for item in regime_rows if isinstance(item, dict) and str(item.get("regime_readiness", "")).strip() == "validated"
    ]
    event_rows = event_window_review.get("rows", []) if isinstance(event_window_review.get("rows"), list) else []
    classified_event_rows = [
        item for item in event_rows if isinstance(item, dict) and str(item.get("review_status", "")).strip() == "classified_candidate"
    ]
    validation_rows = (
        timeline_pack_validation.get("rows", []) if isinstance(timeline_pack_validation.get("rows"), list) else []
    )
    mismatch_rows = [
        item for item in validation_rows if isinstance(item, dict) and str(item.get("validation_status", "")).strip() == "mismatch_review"
    ]
    benchmark = backtest_loop_report.get("after", {}).get("benchmark", {})
    benchmark = benchmark if isinstance(benchmark, dict) else {}

    lines = [
        "# Intelligence System Audit",
        "",
        "This page explains how the current intelligence layers connect into benchmarking, what is genuinely working, and where the system is still thin or untrusted.",
        "",
        "## Current Wiring",
        "",
        "The intended path is:",
        "",
        "1. market-regime intelligence defines candidate market-condition families",
        "2. timeline-pack validation proves whether a claimed regime slice is actually trustworthy",
        "3. pattern-regime pairing maps which pattern families should fit or be avoided in each validated regime",
        "4. market-psychology overlays reshape those patterns with expectation, crowding, sell-the-news, reflexivity, and second-order effects",
        "5. event-window review uses the same psychology layer to decide whether event windows belong in shock, transition, or unresolved lanes",
        "6. mutation trials translate those hints into benchmarkable child variants",
        "7. backtests decide whether the translated children survive or fail",
        "",
        "## Smoke Status",
        "",
        f"- validated_regime_count: `{len(validated_regimes)}`",
        f"- pattern_count: `{_line(pattern_map.get('pattern_count'))}`",
        f"- classified_event_candidates: `{len(classified_event_rows)}`",
        f"- regime_mismatch_count: `{len(mismatch_rows)}`",
        f"- benchmark_top_candidate: `{_line(benchmark.get('top_candidate_id'))}`",
        f"- benchmark_top_profitability: `{_line(benchmark.get('top_profitability_score'))}`",
        f"- benchmark_top_readiness: `{_line(benchmark.get('top_paper_trade_readiness'))}`",
        f"- benchmark_top_drawdown: `{_line(benchmark.get('top_max_drawdown'))}`",
        "",
        "## Where The System Is Actually Intelligent",
        "",
        "- it no longer treats all bullish or bearish periods as the same market state",
        "- it can distinguish validated trend, range, fear, and compression regimes from weaker event-transition guesses",
        "- it can map pattern families to those regimes with explicit avoid lists",
        "- it can express psychology as benchmark mutations instead of leaving it as note-only theory",
        "- it can reject event windows and psychology variants honestly when they collapse into sparse or unstable backtest behavior",
        "",
        "## Where The System Is Still Not Intelligent Enough",
        "",
        "- event-driven macro transition is still mostly research design, not validated routing truth",
        "- the strongest psychology benchmark children are still sparse and mostly reject cleanly rather than improve the frontier",
        "- intermarket context exists as doctrine logic, but not yet as strong live data in the benchmark path",
        "- fear and greed is still only a weak overlay label, not a decisive measured input lane",
        "- backtest leadership is still overconcentrated in the range/reclaim family",
        "",
        "## What The Current Pages Mean Operationally",
        "",
        "- `Regime Taxonomy and Confidence`: explains what the regime labels mean and how much to trust them",
        "- `Timeline Pack Validation`: says whether the claimed market-condition slices are real or mislabeled",
        "- `Pattern Regime Pairing`: says which pattern families belong in which market states and what psychology should modify",
        "- `Event Window Review`: says whether a macro or catalyst window should be treated as shock, transition, or unresolved",
        "- `Backtest Leaderboard`: says whether the translated variants survive benchmark reality",
        "",
        "## Current Translation Into Backtesting",
        "",
        "The translation into benchmark mutations is real in three ways right now:",
        "",
        "- trend or breakout patterns can become `no_chase_after_crowded_good_news` plus `delayed_confirmation` children",
        "- opening-range failure fade can become a `sell_the_news_failure_fade` child",
        "- event-driven asymmetric or no-trade logic can become `wait_for_follow_through` children",
        "",
        "What that means in practice:",
        "",
        "- psychology is being used to reduce participation, delay entries, or demand cleaner failure confirmation",
        "- psychology is not yet being used to create richer timing ladders, cross-asset gates, or adaptive sizing curves",
        "",
        "## Honest Findings",
        "",
        "- validated regime routing is real enough to trust for trend, range, fear, and compression",
        "- psychology-aware event review is useful and honest, but still not good enough to produce a trusted event benchmark regime",
        "- psychology-aware benchmark mutations are connected correctly now, but the first batch mostly failed because trade density collapsed",
        "- the system is strongest at identifying what not to trust yet",
        "- the system is weakest when it needs to explain macro transition with cross-asset context and second-order timing",
        "",
        "## Hardening Priorities",
        "",
        "1. keep event windows narrow and session-aware rather than broad and story-driven",
        "2. add explicit cross-asset or macro context inputs before trusting event-transition routing",
        "3. keep psychology mutations focused on preserving trade count while improving timing, not just on blocking entries",
        "4. benchmark by validated regime packs more aggressively so blended totals stop dominating operator attention",
        "5. keep the Obsidian surfaces readable enough that a human can trace regime -> pattern -> psychology -> mutation -> benchmark result without opening code",
        "",
    ]
    return "\n".join(lines)


def _intelligence_benchmark_page(payload: dict[str, Any]) -> str:
    rows = payload.get("rows", []) if isinstance(payload.get("rows"), list) else []
    summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
    lines = [
        "# Intelligence Benchmark",
        "",
        "This page scores the intelligence layer itself: regime truth, event-classification quality, psychology mutation viability, and whether the benchmark is leaning on grounded market conditions.",
        "",
        f"- benchmark_id: `{_line(payload.get('benchmark_id'))}`",
        f"- row_count: `{_line(payload.get('row_count'))}`",
        f"- validated_regime_count: `{_line(summary.get('validated_regime_count'))}` / `{_line(summary.get('regime_family_count'))}`",
        f"- classified_event_count: `{_line(summary.get('classified_event_count'))}` / `{_line(summary.get('event_candidate_count'))}`",
        f"- psychology_candidate_count: `{_line(summary.get('psychology_candidate_count'))}`",
        f"- current_top_candidate: `{_line(summary.get('top_candidate_id'))}`",
        "",
    ]
    if not rows:
        lines.append("- No intelligence benchmark rows recorded yet.")
        return "\n".join(lines)
    for item in rows:
        lines.extend(
            [
                f"## {item.get('label', 'unknown')}",
                "",
                f"- metric_id: `{_line(item.get('metric_id'))}`",
                f"- score: `{_line(item.get('score'))}`",
                f"- good_direction: `{_line(item.get('good_direction'))}`",
                f"- evidence: {item.get('evidence', 'n/a')}",
                f"- gap_read: {item.get('gap_read', 'n/a')}",
                "",
            ]
        )
    priorities = payload.get("hardening_priorities", [])
    priorities = priorities if isinstance(priorities, list) else []
    lines.extend(["## Hardening Priorities", ""])
    for item in priorities:
        lines.append(f"- {item}")
    return "\n".join(lines)


def _system_state_page(
    benchmark_summary: dict[str, Any],
    intelligence_benchmark: dict[str, Any],
    paper_trade_summary: dict[str, Any],
) -> str:
    top_candidate = _line(benchmark_summary.get("top_candidate_id"))
    candidate_count = _line(benchmark_summary.get("candidate_count"))
    queue_count = _line(paper_trade_summary.get("queue_count"))
    executed_count = _line(paper_trade_summary.get("executed_candidate_count"))
    summary = intelligence_benchmark.get("summary", {}) if isinstance(intelligence_benchmark.get("summary"), dict) else {}
    validated_regimes = _line(summary.get("validated_regime_count"))
    regime_family_count = _line(summary.get("regime_family_count"))
    classified_events = _line(summary.get("classified_event_count"))
    event_candidate_count = _line(summary.get("event_candidate_count"))
    lines = [
        "# System State",
        "",
        "This page is the shortest honest read on the current crypto trading system.",
        "",
        "## What The System Is",
        "",
        "- research-first recursive trading intelligence stack",
        "- heavy backtest as the inner benchmark lane",
        "- paper trade as the outer validation lane",
        "- regime, psychology, and event layers used to condition pattern testing",
        "",
        "## What Is Real Now",
        "",
        f"- active benchmark candidate count: `{candidate_count}`",
        f"- current top benchmark candidate: `{top_candidate}`",
        f"- validated regime families: `{validated_regimes}` / `{regime_family_count}`",
        f"- classified event candidates: `{classified_events}` / `{event_candidate_count}`",
        "- contradiction, mutation, and self-edit lanes are operational",
        "",
        "## What Is Not Yet Strong Enough",
        "",
        f"- paper-trade queue count: `{queue_count}`",
        f"- executed paper-trade candidates: `{executed_count}`",
        "- event transition logic is still weaker than trend/range/fear/compression",
        "- psychology mutations still preserve too little trade density",
        "- timeline-pack truth is still materially incomplete",
        "",
        "## Best Current Mode",
        "",
        "- use the system to observe what regimes, patterns, and doctrines survive heavy benchmark scrutiny",
        "- use paper trade as a falsifier only when a candidate actually clears the bridge",
        "- prefer research and regime truth over broad automation churn when the frontier is stagnant",
        "",
        "## What Not To Overtrust",
        "",
        "- blended leaderboard strength without regime support",
        "- event-window labels that have not validated cleanly",
        "- psychology variants that improve theory but collapse trade count",
    ]
    return "\n".join(lines)


def _operator_guide_page(
    benchmark_summary: dict[str, Any],
    intelligence_benchmark: dict[str, Any],
    backtest_loop_report: dict[str, Any],
    paper_trade_summary: dict[str, Any],
) -> str:
    summary = intelligence_benchmark.get("summary", {}) if isinstance(intelligence_benchmark.get("summary"), dict) else {}
    rows = intelligence_benchmark.get("rows", []) if isinstance(intelligence_benchmark.get("rows"), list) else []
    hardening_priorities = intelligence_benchmark.get("hardening_priorities", []) if isinstance(intelligence_benchmark.get("hardening_priorities"), list) else []
    top_candidate = _line(benchmark_summary.get("top_candidate_id"))
    loop_decision = _line(backtest_loop_report.get("top_next_step"))
    queue_count = _line(paper_trade_summary.get("queue_count"))
    lines = [
        "# Operator Guide",
        "",
        "## Read In This Order",
        "",
        "- [[07-Domains/Crypto Trading/System State]]",
        "- [[07-Domains/Crypto Trading/State Audit 2026-03-15]]",
        "- [[07-Domains/Crypto Trading/Intelligence Benchmark]]",
        "- [[07-Domains/Crypto Trading/Pattern Regime Pairing]]",
        "- [[07-Domains/Crypto Trading/Backtest Leaderboard]]",
        "",
        "## How To Use The System Today",
        "",
        "- treat heavy backtest as the source of truth for candidate survival",
        "- treat regime validation as a trust multiplier, not decoration",
        "- treat paper trade as a falsifier for bridge-cleared candidates, not a vanity lane",
        "- when the frontier stalls, inspect research and regime gaps before adding more mutations",
        "",
        "## Current Practical Read",
        "",
        f"- current benchmark leader: `{top_candidate}`",
        f"- current backtest loop bias: `{loop_decision}`",
        f"- current paper-trade queue: `{queue_count}`",
        "",
        "## Where To Look For Weakness",
        "",
    ]
    for row in rows:
        if not isinstance(row, dict):
            continue
        lines.append(f"- `{_line(row.get('metric_id'))}`: score=`{_line(row.get('score'))}` -> {_line(row.get('gap_read'))}")
    lines.extend(
        [
            "",
            "## What To Do Next",
            "",
        ]
    )
    for item in hardening_priorities:
        lines.append(f"- {_line(item)}")
    lines.extend(
        [
            "",
            "## Do Not Do",
            "",
            "- do not treat profitable residue as doctrine without bridge support",
            "- do not force paper trade when the queue is empty for legitimate reasons",
            "- do not trust event-driven routing as much as trend/range/fear until validation improves",
        ]
    )
    return "\n".join(lines)


def _timeline_packs_page(payload: dict[str, Any]) -> str:
    rows = payload.get("rows", []) if isinstance(payload.get("rows"), list) else []
    bounds = payload.get("bounds", {}) if isinstance(payload.get("bounds"), dict) else {}
    lines = [
        "# Timeline Packs",
        "",
        "This page tracks concrete regime-window extraction targets so archive data expansion becomes an operational lane rather than a note.",
        "",
        f"- pack_count: `{_line(payload.get('pack_count'))}`",
        f"- candle_bounds: `{_line((bounds.get('candles') or {}).get('start'))}` -> `{_line((bounds.get('candles') or {}).get('end'))}`",
        f"- contract_bounds: `{_line((bounds.get('contracts') or {}).get('start'))}` -> `{_line((bounds.get('contracts') or {}).get('end'))}`",
        "",
    ]
    if not rows:
        lines.append("- No timeline packs recorded yet.")
        return "\n".join(lines)
    for item in rows[:12]:
        fit_patterns = item.get("fit_patterns", [])
        fit_patterns = fit_patterns if isinstance(fit_patterns, list) else []
        avoid_patterns = item.get("avoid_patterns", [])
        avoid_patterns = avoid_patterns if isinstance(avoid_patterns, list) else []
        target_paths = item.get("target_paths", {})
        target_paths = target_paths if isinstance(target_paths, dict) else {}
        lines.extend(
            [
                f"## {item.get('regime_label', 'unknown')} / {item.get('window_id', 'window')}",
                "",
                f"- pack_id: `{_line(item.get('pack_id'))}`",
                f"- regime_id: `{_line(item.get('regime_id'))}`",
                f"- source_status: `{_line(item.get('source_status'))}`",
                f"- coverage_status: `{_line(item.get('coverage_status'))}`",
                f"- start_date: `{_line(item.get('start_date'))}`",
                f"- end_date: `{_line(item.get('end_date'))}`",
                f"- fit_patterns: `{', '.join(str(value) for value in fit_patterns)}`",
                f"- avoid_patterns: `{', '.join(str(value) for value in avoid_patterns)}`",
                f"- reason: {item.get('reason', 'n/a')}",
                f"- target_candles_path: `{_line(target_paths.get('candles'))}`",
                f"- target_contracts_path: `{_line(target_paths.get('contracts'))}`",
                "",
            ]
        )
    return "\n".join(lines)


def _timeline_pack_validation_page(payload: dict[str, Any]) -> str:
    rows = payload.get("rows", []) if isinstance(payload.get("rows"), list) else []
    lines = [
        "# Timeline Pack Validation",
        "",
        "This page checks whether extracted timeline packs actually behave like the regime they claim to represent.",
        "",
        f"- pack_count: `{_line(payload.get('pack_count'))}`",
        f"- validated_match_count: `{_line(payload.get('validated_match_count'))}`",
        f"- mixed_proxy_count: `{_line(payload.get('mixed_proxy_count'))}`",
        f"- mismatch_review_count: `{_line(payload.get('mismatch_review_count'))}`",
        f"- pending_extract_count: `{_line(payload.get('pending_extract_count'))}`",
        "",
    ]
    if not rows:
        lines.append("- No timeline pack validation rows recorded yet.")
        return "\n".join(lines)
    for item in rows[:12]:
        metrics = item.get("observed_metrics", {}) if isinstance(item.get("observed_metrics"), dict) else {}
        metrics_by_timeframe = item.get("observed_metrics_by_timeframe", {}) if isinstance(item.get("observed_metrics_by_timeframe"), dict) else {}
        metrics_4h = metrics_by_timeframe.get("4h", {}) if isinstance(metrics_by_timeframe.get("4h"), dict) else {}
        metrics_1d = metrics_by_timeframe.get("1d", {}) if isinstance(metrics_by_timeframe.get("1d"), dict) else {}
        notes = item.get("notes", [])
        notes = notes if isinstance(notes, list) else []
        lines.extend(
            [
                f"## {item.get('pack_id', 'unknown')}",
                "",
                f"- claimed_regime: `{_line(item.get('regime_id'))}`",
                f"- predicted_regime: `{_line(item.get('predicted_regime_id'))}`",
                f"- validation_status: `{_line(item.get('validation_status'))}`",
                f"- claimed_regime_score: `{_line(item.get('claimed_regime_score'))}`",
                f"- predicted_regime_score: `{_line(item.get('predicted_regime_score'))}`",
                f"- dataset_ready: `{_line(item.get('dataset_ready'))}`",
                f"- candle_count: `{_line(item.get('candle_count'))}`",
                f"- contract_count: `{_line(item.get('contract_count'))}`",
                f"- directional_efficiency: `{_line(metrics.get('directional_efficiency'))}`",
                f"- sign_flip_rate: `{_line(metrics.get('sign_flip_rate'))}`",
                f"- mean_abs_return_pct: `{_line(metrics.get('mean_abs_return_pct'))}`",
                f"- max_abs_return_pct: `{_line(metrics.get('max_abs_return_pct'))}`",
                f"- breakout_burst_ratio: `{_line(metrics.get('breakout_burst_ratio'))}`",
                f"- 4h_directional_efficiency: `{_line(metrics_4h.get('directional_efficiency'))}`",
                f"- 4h_mean_abs_return_pct: `{_line(metrics_4h.get('mean_abs_return_pct'))}`",
                f"- 1d_net_return_pct: `{_line(metrics_1d.get('net_return_pct'))}`",
                f"- 1d_directional_efficiency: `{_line(metrics_1d.get('directional_efficiency'))}`",
                f"- 1d_p99_abs_return_pct: `{_line(metrics_1d.get('p99_abs_return_pct'))}`",
                "",
            ]
        )
        if notes:
            lines.append("### Validation Notes")
            lines.append("")
            for note in notes:
                lines.append(f"- {note}")
            lines.append("")
    return "\n".join(lines)


def _regime_match_review_page(payload: dict[str, Any]) -> str:
    rows = payload.get("rows", []) if isinstance(payload.get("rows"), list) else []
    lines = [
        "# Regime Match Review",
        "",
        "This page holds extracted proxy packs that do not validate cleanly as their claimed market condition.",
        "",
        f"- review_count: `{_line(payload.get('review_count'))}`",
        "",
    ]
    if not rows:
        lines.append("- No regime-match review rows recorded yet.")
        return "\n".join(lines)
    for item in rows:
        replacement_pack_ids = item.get("replacement_pack_ids", [])
        replacement_pack_ids = replacement_pack_ids if isinstance(replacement_pack_ids, list) else []
        notes = item.get("notes", [])
        notes = notes if isinstance(notes, list) else []
        lines.extend(
            [
                f"## {item.get('pack_id', 'unknown')}",
                "",
                f"- claimed_regime_id: `{_line(item.get('claimed_regime_id'))}`",
                f"- predicted_regime_id: `{_line(item.get('predicted_regime_id'))}`",
                f"- claimed_regime_score: `{_line(item.get('claimed_regime_score'))}`",
                f"- predicted_regime_score: `{_line(item.get('predicted_regime_score'))}`",
                f"- recommended_action: `{_line(item.get('recommended_action'))}`",
                f"- review_outcome: `{_line(item.get('review_outcome'))}`",
                f"- replacement_pack_ids: `{', '.join(str(value) for value in replacement_pack_ids) or 'n/a'}`",
                "",
            ]
        )
        if notes:
            lines.append("### Notes")
            lines.append("")
            for note in notes:
                lines.append(f"- {note}")
            lines.append("")
    return "\n".join(lines)


def _segment_regime_review_page(payload: dict[str, Any]) -> str:
    rows = payload.get("rows", []) if isinstance(payload.get("rows"), list) else []
    summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
    lines = [
        "# Segment Regime Review",
        "",
        "This page checks whether each top benchmark row is failing inside its claimed market condition or drifting into a different validated regime.",
        "",
        f"- row_count: `{_line(payload.get('row_count'))}`",
        f"- regime_drift_count: `{_line(summary.get('regime_drift_count'))}`",
        f"- segment_match_count: `{_line(summary.get('segment_match_count'))}`",
        f"- mixed_overlap_count: `{_line(summary.get('mixed_overlap_count'))}`",
        f"- needs_review_count: `{_line(summary.get('needs_review_count'))}`",
        f"- no_overlap_count: `{_line(summary.get('no_overlap_count'))}`",
        f"- top_overlap_regime_id: `{_line(summary.get('top_overlap_regime_id'))}`",
        f"- top_candidate_id: `{_line(summary.get('top_candidate_id'))}`",
        "",
    ]
    if not rows:
        lines.append("- No segment-regime review rows recorded yet.")
        return "\n".join(lines)
    for item in rows:
        overlaps = item.get("overlap_candidates", [])
        overlaps = overlaps if isinstance(overlaps, list) else []
        lines.extend(
            [
                f"## {item.get('candidate_id', 'unknown')} / {item.get('weakest_segment_id', 'segment')}",
                "",
                f"- claimed_regime_id: `{_line(item.get('claimed_regime_id'))}`",
                f"- candidate_market_regime: `{_line(item.get('candidate_market_regime'))}`",
                f"- validated_regime_support: `{_line(item.get('validated_regime_support'))}`",
                f"- weakest_profitability_score: `{_line(item.get('weakest_profitability_score'))}`",
                f"- weakest_avg_return: `{_line(item.get('weakest_avg_return'))}`",
                f"- weakest_trade_count: `{_line(item.get('weakest_trade_count'))}`",
                f"- segment_start: `{_line(item.get('segment_start'))}`",
                f"- segment_end: `{_line(item.get('segment_end'))}`",
                f"- strongest_overlap_pack_id: `{_line(item.get('strongest_overlap_pack_id'))}`",
                f"- strongest_overlap_regime_id: `{_line(item.get('strongest_overlap_regime_id'))}`",
                f"- strongest_overlap_validation_status: `{_line(item.get('strongest_overlap_validation_status'))}`",
                f"- strongest_overlap_ratio: `{_line(item.get('strongest_overlap_ratio'))}`",
                f"- diagnosis: `{_line(item.get('diagnosis'))}`",
                f"- recommended_action: {item.get('recommended_action', 'n/a')}",
                "",
            ]
        )
        if overlaps:
            lines.append("### Overlap Candidates")
            lines.append("")
            for overlap in overlaps:
                if not isinstance(overlap, dict):
                    continue
                lines.append(
                    "- "
                    + f"`{_line(overlap.get('pack_id'))}` "
                    + f"regime=`{_line(overlap.get('regime_id'))}` "
                    + f"status=`{_line(overlap.get('validation_status'))}` "
                    + f"overlap=`{_line(overlap.get('overlap_ratio'))}`"
                )
            lines.append("")
    return "\n".join(lines)


def _pattern_regime_pairing_page(payload: dict[str, Any]) -> str:
    regime_rows = payload.get("regime_rows", []) if isinstance(payload.get("regime_rows"), list) else []
    pattern_rows = payload.get("pattern_rows", []) if isinstance(payload.get("pattern_rows"), list) else []
    lines = [
        "# Pattern Regime Pairing",
        "",
        "This page maps pattern families to the market conditions they should be used in or avoided in, grounded by validated timeline packs.",
        "",
        f"- regime_count: `{_line(payload.get('regime_count'))}`",
        f"- pattern_count: `{_line(payload.get('pattern_count'))}`",
        "",
        "## By Regime",
        "",
    ]
    if not regime_rows:
        lines.append("- No pattern/regime map rows recorded yet.")
        return "\n".join(lines)
    for item in regime_rows:
        fit_patterns = item.get("fit_patterns", [])
        fit_patterns = fit_patterns if isinstance(fit_patterns, list) else []
        avoid_patterns = item.get("avoid_patterns", [])
        avoid_patterns = avoid_patterns if isinstance(avoid_patterns, list) else []
        overlay_labels = item.get("psychology_overlay_labels", [])
        overlay_labels = overlay_labels if isinstance(overlay_labels, list) else []
        lines.extend(
            [
                f"### {item.get('regime_label', 'unknown')}",
                "",
                f"- regime_id: `{_line(item.get('regime_id'))}`",
                f"- regime_readiness: `{_line(item.get('regime_readiness'))}`",
                f"- validated_pack_ids: `{', '.join(str(value) for value in item.get('validated_pack_ids', [])) or 'n/a'}`",
                f"- mixed_pack_ids: `{', '.join(str(value) for value in item.get('mixed_pack_ids', [])) or 'n/a'}`",
                f"- mismatch_pack_ids: `{', '.join(str(value) for value in item.get('mismatch_pack_ids', [])) or 'n/a'}`",
                f"- fit_patterns: `{', '.join(str(value) for value in fit_patterns) or 'n/a'}`",
                f"- avoid_patterns: `{', '.join(str(value) for value in avoid_patterns) or 'n/a'}`",
                f"- psychology_overlays: `{', '.join(str(value) for value in overlay_labels) or 'n/a'}`",
                f"- market_character: {item.get('market_character', 'n/a')}",
                "",
            ]
        )
    lines.extend(["## By Pattern", ""])
    for item in pattern_rows[:20]:
        hints = item.get("psychology_mutation_hints", [])
        hints = hints if isinstance(hints, list) else []
        lines.extend(
            [
                f"### {item.get('pattern', 'unknown')}",
                "",
                f"- fit_regimes: `{', '.join(str(value) for value in item.get('fit_regimes', [])) or 'n/a'}`",
                f"- avoid_regimes: `{', '.join(str(value) for value in item.get('avoid_regimes', [])) or 'n/a'}`",
                f"- validated_pack_ids: `{', '.join(str(value) for value in item.get('validated_pack_ids', [])) or 'n/a'}`",
                f"- mixed_pack_ids: `{', '.join(str(value) for value in item.get('mixed_pack_ids', [])) or 'n/a'}`",
                f"- psychology_mutation_hints: `{', '.join(str(value) for value in hints) or 'n/a'}`",
                "",
            ]
        )
    return "\n".join(lines)


def _doctrine_cards_page(cards: list[dict[str, Any]]) -> str:
    lines = [
        "# Doctrine Cards",
        "",
        "These are the tracked research-to-doctrine cards waiting to earn or lose credibility through the benchmark loop.",
        "",
        f"- doctrine_card_count: `{len(cards)}`",
        "",
    ]
    if not cards:
        lines.append("- No doctrine cards recorded yet.")
        return "\n".join(lines)
    for item in cards:
        mutation_template = item.get("mutation_template", {}) if isinstance(item.get("mutation_template"), dict) else {}
        lines.extend(
            [
                f"## {item.get('title', 'unknown')}",
                "",
                f"- card_id: `{_line(item.get('card_id'))}`",
                f"- proposal_id: `{_line(item.get('proposal_id'))}`",
                f"- doctrine_family: `{_line(item.get('doctrine_family'))}`",
                f"- strategy_family: `{_line(item.get('strategy_family'))}`",
                f"- benchmark_priority: `{_line(item.get('benchmark_priority'))}`",
                f"- source_ids: `{', '.join(str(source_id) for source_id in item.get('source_ids', []))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- thesis: {item.get('research_thesis', 'n/a')}",
                f"- rollback_condition: {item.get('rollback_condition', 'n/a')}",
                f"- mutations: `{json.dumps(mutation_template, sort_keys=True)}`",
                "",
            ]
        )
    return "\n".join(lines)


def _doctrine_packets_page(packets: list[dict[str, Any]], cards: list[dict[str, Any]]) -> str:
    existing_card_ids = {str(item.get("card_id", "")) for item in cards if isinstance(item, dict)}
    lines = [
        "# Doctrine Packets",
        "",
        "These are the tracked source-grounded trader doctrine packets that feed the card ingest lane.",
        "",
        f"- doctrine_packet_count: `{len(packets)}`",
        "",
    ]
    if not packets:
        lines.append("- No doctrine packets recorded yet.")
        return "\n".join(lines)
    for item in packets:
        mutation_template = item.get("mutation_template", {}) if isinstance(item.get("mutation_template"), dict) else {}
        lines.extend(
            [
                f"## {item.get('title', 'unknown')}",
                "",
                f"- packet_id: `{_line(item.get('packet_id'))}`",
                f"- card_id: `{_line(item.get('card_id'))}`",
                f"- trader: `{_line(item.get('trader'))}`",
                f"- benchmark_priority: `{_line(item.get('benchmark_priority'))}`",
                f"- ingest_priority: `{_line(item.get('ingest_priority'))}`",
                f"- packet_status: `{_line(item.get('packet_status'))}`",
                f"- card_present: `{str(item.get('card_id')) in existing_card_ids}`",
                f"- source_ids: `{', '.join(str(source_id) for source_id in item.get('source_ids', []))}`",
                f"- root_lesson: {item.get('root_lesson', 'n/a')}",
                f"- mechanism: {item.get('mechanism', 'n/a')}",
                f"- setup_definition: {item.get('setup_definition', 'n/a')}",
                f"- rollback_condition: {item.get('rollback_condition', 'n/a')}",
                f"- mutations: `{json.dumps(mutation_template, sort_keys=True)}`",
                "",
            ]
        )
    return "\n".join(lines)


def _doctrine_registry_page(rows: list[dict[str, Any]]) -> str:
    lines = ["# Doctrine Registry", "", "This page is the crypto equivalent of startup benchmark doctrine pages.", ""]
    ranked = _sort_rows(_candidate_rows(rows))
    best_by_doctrine: dict[str, dict[str, Any]] = {}
    for row in ranked:
        doctrine_id = _row_mutations(row).get("doctrine_id", "")
        if doctrine_id and doctrine_id not in best_by_doctrine:
            best_by_doctrine[doctrine_id] = row
    for doctrine_id, doctrine in DOCTRINES.items():
        row = best_by_doctrine.get(doctrine_id)
        mutations = _row_mutations(row) if row else {}
        metrics = _row_metrics(row) if row else {}
        lines.extend(
            [
                f"## {doctrine_id}",
                "",
                f"- mechanism: {doctrine['lesson']}",
                f"- strongest_pair: `{_line(mutations.get('strategy_id'))}`",
                f"- current_regime_fit: `{_line(mutations.get('market_regime'))}`",
                f"- profitability_score: `{_line(metrics.get('profitability_score'))}`",
                f"- boundary: {doctrine['boundary']}",
                "",
            ]
        )
    return "\n".join(lines)


def _strategy_catalog_page(rows: list[dict[str, Any]]) -> str:
    lines = ["# Strategy Catalog", "", "Strategies should be treated as expressions of doctrine, not standalone truth claims.", ""]
    ranked = _sort_rows(_candidate_rows(rows))
    best_by_strategy: dict[str, dict[str, Any]] = {}
    for row in ranked:
        strategy_id = _row_mutations(row).get("strategy_id", "")
        if strategy_id and strategy_id not in best_by_strategy:
            best_by_strategy[strategy_id] = row
    for strategy_id in STRATEGIES:
        row = best_by_strategy.get(strategy_id)
        mutations = _row_mutations(row) if row else {}
        metrics = _row_metrics(row) if row else {}
        lines.extend(
            [
                f"## {strategy_id}",
                "",
                f"- best_fit_doctrine: `{_line(mutations.get('doctrine_id'))}`",
                f"- preferred_regime: `{_line(mutations.get('market_regime'))}`",
                f"- timeframe: `{_line(mutations.get('timeframe'))}`",
                f"- profitability_score: `{_line(metrics.get('profitability_score'))}`",
                "",
            ]
        )
    return "\n".join(lines)


def _loop_progression_page(rows: list[dict[str, Any]], learning_report: dict[str, Any], backtest_report: dict[str, Any], paper_trade_loop_report: dict[str, Any]) -> str:
    candidates = _candidate_rows(rows)
    paper_ready = any(str(_row_chip_result(row).get("recommended_next_step", "")) == "queue_for_paper_trade" for row in candidates)
    state = "paper_trade_ready" if paper_ready else "backtest_benchmark_first"
    reason = "at least one combination cleared the paper-trade gate" if paper_ready else "the chip has benchmark candidates, but no combination has cleared the paper-trade gate yet"
    learning_after = learning_report.get("after", {}) if isinstance(learning_report.get("after"), dict) else {}
    backtest_after = backtest_report.get("after", {}) if isinstance(backtest_report.get("after"), dict) else {}
    paper_trade_after = paper_trade_loop_report.get("after", {}) if isinstance(paper_trade_loop_report.get("after"), dict) else {}
    return "\n".join(
        [
            "# Loop Progression",
            "",
            "This page mirrors the startup chip standard: one loop, one current state, one next bottleneck.",
            "",
            f"- current_state: `{state}`",
            f"- reason: `{reason}`",
            "",
            "## Current Flywheel Read",
            "",
            f"- learning_loop_status: `{'active' if learning_report else 'seeded'}`",
            f"- learning_pending_packets: `{_line(learning_after.get('pending_packet_count'))}`",
            f"- backtest_loop_status: `{'active' if backtest_report else 'ready'}`",
            f"- contradiction_probe_status: `{'active' if candidates else 'idle'}`",
            f"- paper_trade_loop_status: `{'active' if paper_trade_loop_report else 'idle'}`",
            f"- paper_trade_queue_status: `{'non_empty' if int(paper_trade_after.get('queue_count', 0) or 0) > 0 else 'empty'}`",
            "",
            "## What Should Happen Next",
            "",
            "1. let the learning loop ingest only source-grounded doctrine packets",
            "2. let the backtest loop benchmark, mutate, and reject ideas quickly",
            "3. escalate only `queue_for_paper_trade` combinations into the paper-trade loop",
            "4. use paper-trade outcomes as outer-validation evidence without rewriting benchmark facts",
        ]
    )


def _benchmark_bridge_page(rows: list[dict[str, Any]], packets: list[dict[str, Any]]) -> str:
    lines = [
        "# Benchmark Bridge",
        "",
        "Backtesting is the benchmark lane for this chip.",
        "",
        "This page plays the same role as the startup chip's promotion bridge page, but for trading combinations.",
        "",
    ]
    ranked_packets = sorted(
        packets,
        key=lambda packet: (
            bool(packet.get("trade_count_gate_pass")),
            float(packet.get("profitability_score", 0.0) or 0.0),
            float(packet.get("paper_trade_readiness", 0.0) or 0.0),
        ),
        reverse=True,
    )
    if not ranked_packets:
        lines.append("- No bridge-visible benchmark packets recorded yet.")
    for packet in ranked_packets[:8]:
        lines.extend(
            [
                f"## {packet.get('candidate_id', 'unknown')}",
                "",
                f"- doctrine_id: `{_line(packet.get('doctrine_id'))}`",
                f"- strategy_id: `{_line(packet.get('strategy_id'))}`",
                f"- market_regime: `{_line(packet.get('market_regime'))}`",
                f"- profitability_score: `{_line(packet.get('profitability_score'))}`",
                f"- sharpe_ratio: `{_line(packet.get('sharpe_ratio'))}`",
                f"- max_drawdown: `{_line(packet.get('max_drawdown'))}`",
                f"- paper_trade_readiness: `{_line(packet.get('paper_trade_readiness'))}`",
                f"- contract_count: `{_line(packet.get('contract_count'))}`",
                f"- covered_contract_count: `{_line(packet.get('covered_contract_count'))}`",
                f"- trade_count: `{_line(packet.get('trade_count'))}`",
                f"- minimum_trade_count: `{_line(packet.get('minimum_trade_count'))}`",
                f"- trade_count_gate_pass: `{_line(packet.get('trade_count_gate_pass'))}`",
                f"- holdout_profitability_score: `{_line(packet.get('holdout_profitability_score'))}`",
                f"- walk_forward_consistency: `{_line(packet.get('walk_forward_consistency'))}`",
                f"- stress_resilience: `{_line(packet.get('stress_resilience'))}`",
                f"- data_mode: `{_line(packet.get('data_mode'))}`",
                f"- recommended_next_step: `{_line(packet.get('recommended_next_step'))}`",
                f"- promotion_candidate_kind: `{_line(packet.get('promotion_candidate_kind'))}`",
                f"- eligibility_status: `{_line(packet.get('eligibility_status'))}`",
                f"- primary_mechanism: {packet.get('primary_mechanism', 'n/a')}",
                f"- primary_boundary: {packet.get('primary_boundary', 'n/a')}",
                "",
            ]
        )
    lines.extend(
        [
            "## Recommended Next-Step Ladder",
            "",
            "- `store_as_benchmark_evidence`",
            "- `promote_as_doctrine_candidate`",
            "- `promote_as_boundary_candidate`",
            "- `queue_for_paper_trade`",
        ]
    )
    return "\n".join(lines)


def _paper_trade_queue_page(queue_artifact: dict[str, Any], summary: dict[str, Any]) -> str:
    queue_packets = queue_artifact.get("rows", [])
    queue_packets = queue_packets if isinstance(queue_packets, list) else []
    lines = [
        "# Paper Trade Queue",
        "",
        "Paper trade is outer validation, not part of the benchmark itself.",
        "",
        "Default queue source:",
        "",
        "- `queue_for_paper_trade`",
        "- explicit `pilot_override_best_candidate` rows may be added for manual shadow validation without changing the benchmark bridge",
        "",
        "## Queue Rules",
        "",
        "- verify execution realism",
        "- test slippage and sequencing assumptions",
        "- confirm that doctrine still holds under a slower live-like loop",
        "- do not use paper trade to rewrite benchmark facts",
        "- do not treat pilot rows as bridge-approved promotions",
        "",
        "## Current Queue",
        "",
        f"- queue_count: `{_line(queue_artifact.get('queue_count', len(queue_packets)))}`",
        f"- executed_candidate_count: `{_line(summary.get('executed_candidate_count', 0))}`",
        f"- pending_data_count: `{_line(summary.get('pending_data_count', 0))}`",
    ]
    if not queue_packets:
        lines.extend(
            [
                "- status: `waiting_for bridge-approved candidates`",
                "- next_requirement: `a benchmark packet must clear queue_for_paper_trade before this lane activates`",
            ]
        )
    else:
        for packet in queue_packets:
            lines.extend(
                [
                    "",
                    f"### {packet.get('candidate_id', 'unknown')}",
                    "",
                    f"- doctrine_id: `{_line(packet.get('doctrine_id'))}`",
                    f"- strategy_id: `{_line(packet.get('strategy_id'))}`",
                    f"- paper_trade_readiness: `{_line(packet.get('paper_trade_readiness'))}`",
                    f"- max_drawdown: `{_line(packet.get('max_drawdown'))}`",
                    f"- eligibility_status: `{_line(packet.get('eligibility_status'))}`",
                    f"- queue_status: `{_line(packet.get('queue_status'))}`",
                    f"- queue_origin: `{_line(packet.get('queue_origin'))}`",
                    f"- bridge_packet_path: `{_line(packet.get('bridge_packet_path'))}`",
                ]
            )
    return "\n".join(lines)


def _paper_trade_outcomes_page(summary: dict[str, Any]) -> str:
    rows = summary.get("rows", [])
    rows = rows if isinstance(rows, list) else []
    lines = [
        "# Paper Trade Outcomes",
        "",
        "This page is the slower outer-validation surface. It should confirm or demote bridge-approved candidates without rewriting the benchmark record.",
        "Pilot rows may appear here too, but they remain manual shadow evidence rather than proof of bridge approval.",
        "",
        f"- queue_count: `{_line(summary.get('queue_count', 0))}`",
        f"- executed_candidate_count: `{_line(summary.get('executed_candidate_count', 0))}`",
        f"- pending_data_count: `{_line(summary.get('pending_data_count', 0))}`",
        "",
        "## Outcome Rules",
        "",
        "- use only bridge-approved candidates here",
        "- paper-trade data must be separate from benchmark data",
        "- a weak paper-trade slice demotes the candidate back to benchmark refinement",
        "- a strong paper-trade slice only advances live-readiness review; it does not auto-promote to live trading",
        "",
        "## Current Outcomes",
        "",
    ]
    if not rows:
        lines.append("- No paper-trade outcomes recorded yet.")
    for row in rows:
        if not isinstance(row, dict):
            continue
        lines.extend(
            [
                f"### {row.get('candidate_id', 'unknown')}",
                "",
                f"- status: `{_line(row.get('status'))}`",
                f"- paper_trade_recommendation: `{_line(row.get('paper_trade_recommendation'))}`",
                f"- sample_contract_count: `{_line(row.get('sample_contract_count'))}`",
                f"- trade_count: `{_line(row.get('trade_count'))}`",
                f"- profitability_score: `{_line(row.get('profitability_score'))}`",
                f"- max_drawdown: `{_line(row.get('max_drawdown'))}`",
                f"- win_rate: `{_line(row.get('win_rate'))}`",
                f"- boundary: {row.get('boundary', 'n/a')}",
                "",
            ]
        )
    return "\n".join(lines)


def _learning_loop_page(report: dict[str, Any]) -> str:
    after = report.get("after", {}) if isinstance(report.get("after"), dict) else {}
    return "\n".join(
        [
            "# Learning Loop",
            "",
            "This loop owns doctrine packet ingestion, doctrine card creation, and learning-surface refreshes.",
            "",
            f"- material_change: `{_line(report.get('material_change'))}`",
            f"- added_count: `{_line(after.get('added_count'))}`",
            f"- card_count: `{_line(after.get('card_count'))}`",
            f"- pending_packet_count: `{_line(after.get('pending_packet_count'))}`",
            "",
            "Loop contract:",
            "",
            "- read only source-grounded doctrine packets",
            "- create bounded doctrine cards",
            "- do not benchmark or paper trade directly",
            "- feed new cards into the backtest loop",
        ]
    )


def _backtest_loop_page(report: dict[str, Any]) -> str:
    after = report.get("after", {}) if isinstance(report.get("after"), dict) else {}
    benchmark = after.get("benchmark", {}) if isinstance(after.get("benchmark"), dict) else {}
    self_edit = after.get("self_edit_audit", {}) if isinstance(after.get("self_edit_audit"), dict) else {}
    return "\n".join(
        [
            "# Backtest Loop",
            "",
            "This loop owns heavy benchmark evaluation, contradiction extraction, mutation generation, and self-edit review.",
            "",
            f"- material_change: `{_line(report.get('material_change'))}`",
            f"- candidate_count: `{_line(benchmark.get('candidate_count'))}`",
            f"- top_candidate_id: `{_line(benchmark.get('top_candidate_id'))}`",
            f"- top_recommended_next_step: `{_line(benchmark.get('top_recommended_next_step'))}`",
            f"- approved_self_edits: `{_line(self_edit.get('approved_count'))}`",
            "",
            "Loop contract:",
            "",
            "- benchmark fast and reject weak ideas quickly",
            "- generate contradiction probes and bounded child mutations",
            "- write bridge packets for paper-trade eligibility",
            "- do not treat paper-trade evidence as benchmark truth",
        ]
    )


def _paper_trade_loop_page(report: dict[str, Any]) -> str:
    after = report.get("after", {}) if isinstance(report.get("after"), dict) else {}
    return "\n".join(
        [
            "# Paper Trade Loop",
            "",
            "This loop owns outer validation on bridge-approved candidates only.",
            "",
            f"- material_change: `{_line(report.get('material_change'))}`",
            f"- queue_count: `{_line(after.get('queue_count'))}`",
            f"- executed_candidate_count: `{_line(after.get('executed_candidate_count'))}`",
            f"- pending_data_count: `{_line(after.get('pending_data_count'))}`",
            f"- top_recommendation: `{_line(after.get('top_recommendation'))}`",
            "",
            "Loop contract:",
            "",
            "- consume only bridge-approved queue artifacts",
            "- validate execution and live-like timing separately from backtests",
            "- demote weak candidates back to the backtest loop",
            "- never auto-promote straight to live trading",
        ]
    )


def _contradictions_page(rows: list[dict[str, Any]], probes: list[dict[str, Any]]) -> str:
    lines = [
        "# Contradictions",
        "",
        "This page is the trading equivalent of a `why it lost` surface.",
        "",
        "Track failure shapes here when a combination looks exciting but should not be promoted.",
        "",
    ]
    if probes:
        for probe in probes[:8]:
            failure_modes = probe.get("failure_modes", [])
            failure_modes = failure_modes if isinstance(failure_modes, list) else []
            weakest_segments = probe.get("weakest_segments", [])
            weakest_segments = weakest_segments if isinstance(weakest_segments, list) else []
            lines.extend(
                [
                    f"## {probe.get('candidate_id', 'unknown')}",
                    "",
                    f"- doctrine_id: `{_line(probe.get('doctrine_id'))}`",
                    f"- strategy_id: `{_line(probe.get('strategy_id'))}`",
                    f"- priority: `{_line(probe.get('priority'))}`",
                    f"- holdout_profitability_score: `{_line(probe.get('holdout_profitability_score'))}`",
                    f"- walk_forward_consistency: `{_line(probe.get('walk_forward_consistency'))}`",
                    f"- stress_resilience: `{_line(probe.get('stress_resilience'))}`",
                    f"- max_drawdown: `{_line(probe.get('max_drawdown'))}`",
                    f"- contradiction: {probe.get('probe_thesis', 'n/a')}",
                    "",
                ]
            )
            if failure_modes:
                lines.append("### Failure Modes")
                lines.append("")
                for item in failure_modes:
                    if not isinstance(item, dict):
                        continue
                    lines.append(f"- {_line(item.get('mode'))}: {item.get('evidence', 'n/a')}")
                lines.append("")
            if weakest_segments:
                lines.append("### Weakest Segments")
                lines.append("")
                for item in weakest_segments:
                    if not isinstance(item, dict):
                        continue
                    lines.append(
                        f"- {_line(item.get('segment_id'))}: profitability=`{_line(item.get('profitability_score'))}` avg_return=`{_line(item.get('avg_return'))}` trades=`{_line(item.get('trade_count'))}`"
                    )
                lines.append("")
    else:
        contradiction_rows = [row for row in _candidate_rows(rows) if str(_row_chip_result(row).get("recommended_next_step", "")) == "run_contradiction_probe"]
        if not contradiction_rows:
            lines.append("- No contradiction probes recorded yet.")
        for row in _sort_rows(contradiction_rows):
            mutations = _row_mutations(row)
            metrics = _row_metrics(row)
            result = _row_chip_result(row)
            lines.extend(
                [
                    f"## {row.get('candidate_id', 'unknown')}",
                    "",
                    f"- doctrine_id: `{_line(mutations.get('doctrine_id'))}`",
                    f"- strategy_id: `{_line(mutations.get('strategy_id'))}`",
                    f"- profitability_score: `{_line(metrics.get('profitability_score'))}`",
                    f"- max_drawdown: `{_line(metrics.get('max_drawdown'))}`",
                    f"- contradiction: {result.get('boundary', 'n/a')}",
                    "",
                ]
            )
    lines.extend(
        [
            "## Anti-Patterns",
            "",
            "- high PnL with unstable drawdown",
            "- strategy wins that do not transfer across adjacent regimes",
            "- doctrine labels attached after the fact to justify a curve fit",
            "- paper-trade enthusiasm outrunning benchmark evidence",
        ]
    )
    return "\n".join(lines)


def _next_probes_page(payload: dict[str, Any], probes: list[dict[str, Any]]) -> str:
    lines = ["# Next Probes", "", "This page turns the seeded catalog into an actionable next frontier.", ""]
    if probes:
        for probe in probes[:8]:
            failure_modes = probe.get("failure_modes", [])
            failure_modes = failure_modes if isinstance(failure_modes, list) else []
            lines.extend(
                [
                    f"## {probe.get('probe_id', 'unknown')}",
                    "",
                    f"- candidate_id: `{_line(probe.get('candidate_id'))}`",
                    f"- doctrine: `{_line(probe.get('doctrine_id'))}`",
                    f"- strategy: `{_line(probe.get('strategy_id'))}`",
                    f"- market_regime: `{_line(probe.get('market_regime'))}`",
                    f"- priority: `{_line(probe.get('priority'))}`",
                    f"- why: {probe.get('probe_thesis', 'n/a')}",
                    "",
                ]
            )
            if failure_modes:
                lines.append("### Probe Actions")
                lines.append("")
                for item in failure_modes:
                    if not isinstance(item, dict):
                        continue
                    lines.append(f"- {_line(item.get('mode'))}: {item.get('probe', 'n/a')}")
                lines.append("")
        return "\n".join(lines)
    suggestions = suggest({"limit": 6}).get("suggestions", [])
    for item in suggestions:
        mutations = item.get("mutations", {}) if isinstance(item.get("mutations"), dict) else {}
        lines.extend(
            [
                f"## {item.get('candidate_id', 'unknown')}",
                "",
                f"- doctrine: `{_line(mutations.get('doctrine_id'))}`",
                f"- strategy: `{_line(mutations.get('strategy_id'))}`",
                f"- market_regime: `{_line(mutations.get('market_regime'))}`",
                f"- why: {item.get('hypothesis', 'n/a')}",
                "",
            ]
        )
    return "\n".join(lines)


def _recursive_flywheel_page(payload: dict[str, Any], audit: dict[str, Any], queue: list[dict[str, Any]], self_edit_queue: list[dict[str, Any]], self_edit_audit: dict[str, Any]) -> str:
    policy = _recursion_policy(payload)
    benchmark_lane = policy.get("benchmark_lane", {}) if isinstance(policy.get("benchmark_lane"), dict) else {}
    lines = [
        "# Recursive Flywheel",
        "",
        "This page governs self-improvement for `BTC up/down 15m`.",
        "",
        "Research may generate mutation proposals.",
        "Heavy backtesting is the only benchmark lane allowed to ground them.",
        "",
        f"- contract_family: `{_line(policy.get('contract_family'))}`",
        f"- current_decision: `{_line(audit.get('decision'))}`",
        f"- stability_score: `{_line(audit.get('stability_score'))}`",
        f"- queued_heavy_backtests: `{len(queue)}`",
        f"- queued_self_edits: `{len(self_edit_queue)}`",
        f"- approved_self_edits: `{_line(self_edit_audit.get('approved_count'))}`",
        "",
        "## Loop",
        "",
        "1. ingest trader and indicator research",
        "2. convert research into bounded mutation proposals",
        "3. rank proposals by surprise score",
        "4. run heavy backtests on BTC up/down contract windows",
        "5. derive bounded self-edits from contradiction probes",
        "6. approve only self-edits that beat their parent failures under benchmark review",
        "7. bridge only grounded combinations into paper trade",
        "8. feed contradictions and paper-trade outcomes back into the next cycle",
        "",
        "## Heavy Backtest Policy",
        "",
        f"- mode: `{_line(benchmark_lane.get('mode'))}`",
        f"- min_contract_windows: `{_line(benchmark_lane.get('min_contract_windows'))}`",
        f"- walk_forward_splits: `{_line(benchmark_lane.get('walk_forward_splits'))}`",
        f"- holdout_policy: `{_line(benchmark_lane.get('holdout_policy'))}`",
        f"- fee_model: `{_line(benchmark_lane.get('fee_model'))}`",
        f"- slippage_model: `{_line(benchmark_lane.get('slippage_model'))}`",
    ]
    return "\n".join(lines)


def _self_edit_queue_page(queue: list[dict[str, Any]], evaluations: list[dict[str, Any]], audit: dict[str, Any]) -> str:
    lines = [
        "# Self Edit Queue",
        "",
        "This queue holds bounded benchmark-driven self-edits.",
        "",
        f"- queue_count: `{len(queue)}`",
        f"- approved_count: `{_line(audit.get('approved_count'))}`",
        f"- deferred_count: `{_line(audit.get('deferred_count'))}`",
        f"- rejected_count: `{_line(audit.get('rejected_count'))}`",
        "",
    ]
    evaluation_index = {
        str(item.get("edit_id", "")): item
        for item in evaluations
        if isinstance(item, dict)
    }
    if not queue:
        lines.append("- No self-edit queue artifacts recorded yet.")
        return "\n".join(lines)
    for item in queue[:8]:
        evaluation = evaluation_index.get(str(item.get("edit_id", "")), {})
        comparison = evaluation.get("comparison", {}) if isinstance(evaluation.get("comparison"), dict) else {}
        lines.extend(
            [
                f"## {item.get('edit_id', 'unknown')}",
                "",
                f"- parent_candidate_id: `{_line(item.get('parent_candidate_id'))}`",
                f"- child_candidate_id: `{_line(item.get('child_candidate_id'))}`",
                f"- priority: `{_line(item.get('priority'))}`",
                f"- allowed_edits: `{', '.join(str(edit) for edit in item.get('allowed_edits', []))}`",
                f"- decision: `{_line(evaluation.get('decision'))}`",
                f"- target_improved: `{_line(evaluation.get('target_improved'))}`",
                f"- child_profitability_score: `{_line(comparison.get('child_profitability_score'))}`",
                f"- child_holdout_profitability_score: `{_line(comparison.get('child_holdout_profitability_score'))}`",
                f"- child_trade_count: `{_line(comparison.get('child_trade_count'))}`",
                "",
            ]
        )
    return "\n".join(lines)


def _mutation_backlog_page(backlog: list[dict[str, Any]]) -> str:
    lines = [
        "# Mutation Backlog",
        "",
        "These are the current source-grounded mutation proposals.",
        "",
        f"- proposal_count: `{len(backlog)}`",
        "",
    ]
    if not backlog:
        lines.append("- No mutation backlog artifacts recorded yet.")
        return "\n".join(lines)
    for item in backlog[:8]:
        benchmark_result = item.get("benchmark_result", {}) if isinstance(item.get("benchmark_result"), dict) else {}
        lines.extend(
            [
                f"## {item.get('title', 'unknown')}",
                "",
                f"- proposal_id: `{_line(item.get('proposal_id'))}`",
                f"- card_id: `{_line(item.get('card_id'))}`",
                f"- doctrine_family: `{_line(item.get('doctrine_family'))}`",
                f"- strategy_family: `{_line(item.get('strategy_family'))}`",
                f"- variety_family_id: `{_line(item.get('variety_family_id'))}`",
                f"- variety_child_id: `{_line(item.get('variety_child_id'))}`",
                f"- variety_child_label: `{_line(item.get('variety_child_label'))}`",
                f"- family_tested_child_count: `{_line(item.get('family_tested_child_count'))}`",
                f"- target_contract_family: `{_line(item.get('target_contract_family'))}`",
                f"- benchmark_priority: `{_line(item.get('benchmark_priority'))}`",
                f"- surprise_score: `{_line(item.get('surprise_score'))}`",
                f"- duplicate_of_proposal_id: `{_line(item.get('duplicate_of_proposal_id'))}`",
                f"- source_names: `{', '.join(str(name) for name in item.get('source_names', []))}`",
                f"- lineage_ready: `{_line(item.get('lineage_ready'))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- benchmark_profitability_score: `{_line((item.get('benchmark_metrics') or {}).get('profitability_score'))}`",
                f"- benchmark_paper_trade_readiness: `{_line((item.get('benchmark_metrics') or {}).get('paper_trade_readiness'))}`",
                f"- benchmark_next_step: `{_line((item.get('benchmark_result') or {}).get('recommended_next_step'))}`",
                f"- benchmark_trade_count: `{_line(benchmark_result.get('trade_count'))}`",
                f"- benchmark_minimum_trade_count: `{_line(benchmark_result.get('minimum_trade_count'))}`",
                f"- benchmark_trade_count_gate_pass: `{_line(benchmark_result.get('trade_count_gate_pass'))}`",
                f"- benchmark_walk_forward_consistency: `{_line(benchmark_result.get('walk_forward_consistency'))}`",
                f"- benchmark_stress_resilience: `{_line(benchmark_result.get('stress_resilience'))}`",
                f"- thesis: {item.get('research_thesis', 'n/a')}",
                "",
            ]
        )
    return "\n".join(lines)


def _heavy_backtest_queue_page(queue: list[dict[str, Any]]) -> str:
    lines = [
        "# Heavy Backtest Queue",
        "",
        "This queue is the benchmark gate for recursive improvement.",
        "",
        f"- queue_count: `{len(queue)}`",
        "",
    ]
    if not queue:
        lines.append("- No heavy-backtest queue artifacts recorded yet.")
        return "\n".join(lines)
    for item in queue:
        plan = item.get("benchmark_plan", {}) if isinstance(item.get("benchmark_plan"), dict) else {}
        metrics = item.get("required_metrics", {}) if isinstance(item.get("required_metrics"), dict) else {}
        lines.extend(
            [
                f"## {item.get('title', 'unknown')}",
                "",
                f"- proposal_id: `{_line(item.get('proposal_id'))}`",
                f"- benchmark_priority: `{_line(item.get('benchmark_priority'))}`",
                f"- surprise_score: `{_line(item.get('surprise_score'))}`",
                f"- variety_family_id: `{_line(item.get('variety_family_id'))}`",
                f"- variety_child_id: `{_line(item.get('variety_child_id'))}`",
                f"- variety_child_label: `{_line(item.get('variety_child_label'))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- min_contract_windows: `{_line(plan.get('min_contract_windows'))}`",
                f"- walk_forward_splits: `{_line(plan.get('walk_forward_splits'))}`",
                f"- holdout_policy: `{_line(plan.get('holdout_policy'))}`",
                f"- profitability_score_min: `{_line(metrics.get('profitability_score_min'))}`",
                f"- sharpe_ratio_min: `{_line(metrics.get('sharpe_ratio_min'))}`",
                f"- max_drawdown_max: `{_line(metrics.get('max_drawdown_max'))}`",
                f"- paper_trade_readiness_min: `{_line(metrics.get('paper_trade_readiness_min'))}`",
                "",
            ]
        )
    return "\n".join(lines)


def _variety_backlog_page(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Variety Backlog",
        "",
        "This page tracks doctrine -> strategy families and the uncovered child varieties still worth testing.",
        "",
        f"- family_count: `{len(rows)}`",
        f"- pending_family_count: `{sum(1 for item in rows if int(item.get('pending_proposal_count', 0) or 0) > 0 or int(item.get('suggested_child_target_count', 0) or 0) > 0)}`",
        "",
    ]
    if not rows:
        lines.append("- No variety backlog artifacts recorded yet.")
        return "\n".join(lines)
    for item in rows[:10]:
        lines.extend(
            [
                f"## {item.get('doctrine_family', 'unknown')} -> {item.get('strategy_family', 'unknown')}",
                "",
                f"- variety_family_id: `{_line(item.get('variety_family_id'))}`",
                f"- target_contract_family: `{_line(item.get('target_contract_family'))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- tested_child_count: `{_line(item.get('tested_child_count'))}`",
                f"- benchmarked_candidate_count: `{_line(item.get('benchmarked_candidate_count'))}`",
                f"- pending_proposal_count: `{_line(item.get('pending_proposal_count'))}`",
                f"- pending_proposal_ids: `{', '.join(str(value) for value in item.get('pending_proposal_ids', [])) or 'n/a'}`",
                f"- pending_child_labels: `{ ' | '.join(str(value) for value in item.get('pending_child_labels', [])) or 'n/a'}`",
                f"- suggested_child_target_count: `{_line(item.get('suggested_child_target_count'))}`",
                f"- suggested_child_targets: `{ ' | '.join(str(target.get('variety_child_label', '')) for target in item.get('suggested_child_targets', []) if isinstance(target, dict)) or 'n/a'}`",
                f"- contradiction_modes: `{', '.join(str(value) for value in item.get('contradiction_modes', [])) or 'n/a'}`",
                f"- top_candidate_id: `{_line(item.get('top_candidate_id'))}`",
                f"- top_profitability_score: `{_line(item.get('top_profitability_score'))}`",
                f"- top_recommended_next_step: `{_line(item.get('top_recommended_next_step'))}`",
                "",
            ]
        )
    return "\n".join(lines)


def _recursion_audit_page(audit: dict[str, Any]) -> str:
    lines = [
        "# Recursion Audit",
        "",
        "This page mirrors the recursive-evolution guardrail packet.",
        "",
        f"- decision: `{_line(audit.get('decision'))}`",
        f"- stability_score: `{_line(audit.get('stability_score'))}`",
        f"- top_bottleneck: {audit.get('top_bottleneck', 'n/a')}",
        "",
        "## Benchmark Summary",
        "",
        f"- candidate_count: `{_line((audit.get('benchmark_summary') or {}).get('candidate_count'))}`",
        f"- top_candidate_id: `{_line((audit.get('benchmark_summary') or {}).get('top_candidate_id'))}`",
        f"- contract_family: `{_line((audit.get('benchmark_summary') or {}).get('contract_family'))}`",
        "",
        "## Self Edit Summary",
        "",
        f"- evaluation_count: `{_line((audit.get('self_edit_summary') or {}).get('evaluation_count'))}`",
        f"- approved_count: `{_line((audit.get('self_edit_summary') or {}).get('approved_count'))}`",
        f"- deferred_count: `{_line((audit.get('self_edit_summary') or {}).get('deferred_count'))}`",
        f"- rejected_count: `{_line((audit.get('self_edit_summary') or {}).get('rejected_count'))}`",
        "",
        "## Guardrails",
        "",
    ]
    guardrails = audit.get("guardrail_status", {})
    guardrails = guardrails if isinstance(guardrails, dict) else {}
    for key, value in guardrails.items():
        lines.append(f"- {key}: `{_line(value)}`")
    anti_patterns = audit.get("anti_patterns_detected", [])
    anti_patterns = anti_patterns if isinstance(anti_patterns, list) else []
    lines.extend(["", "## Anti-Patterns", ""])
    if not anti_patterns:
        lines.append("- none")
    for item in anti_patterns:
        if not isinstance(item, dict):
            continue
        lines.extend(
            [
                f"### {item.get('tag', 'unknown')}",
                "",
                f"- severity: `{_line(item.get('severity'))}`",
                f"- status: `{_line(item.get('status'))}`",
                f"- evidence: `{' | '.join(str(piece) for piece in item.get('evidence', []))}`",
                "",
            ]
        )
    fixes = audit.get("required_fixes_before_approve", [])
    fixes = fixes if isinstance(fixes, list) else []
    lines.extend(["## Required Fixes", ""])
    for item in fixes:
        lines.append(f"- {item}")
    experiments = audit.get("next_experiments", [])
    experiments = experiments if isinstance(experiments, list) else []
    lines.extend(["", "## Next Experiments", ""])
    for item in experiments:
        lines.append(f"- {item}")
    return "\n".join(lines)


def watchtower(payload: dict) -> dict:
    rows = _rows(payload)
    packets = _promotion_packets(payload)
    sources = _approved_sources(payload)
    research_backlog = _research_backlog(payload)
    doctrine_packets = _doctrine_packets(payload)
    cards = _doctrine_cards(payload)
    backlog = _mutation_backlog(payload)
    queue = _heavy_backtest_queue(payload)
    variety_backlog = _variety_backlog(payload)
    probes = _contradiction_probes(payload)
    self_edit_queue = _self_edit_queue(payload)
    self_edit_evaluations = _self_edit_evaluations(payload)
    self_edit_audit = _self_edit_audit(payload)
    audit = _recursion_audit(payload)
    benchmark_summary = _heavy_benchmark_summary(payload)
    paper_trade_queue = _paper_trade_queue_artifact(payload)
    paper_trade_summary = _paper_trade_summary(payload)
    learning_loop_report = _learning_loop_report(payload)
    backtest_loop_report = _backtest_loop_report(payload)
    paper_trade_loop_report = _paper_trade_loop_report(payload)
    research_scout_queue = _research_scout_queue(payload)
    timeline_packs = _timeline_packs(payload)
    timeline_pack_validation = _timeline_pack_validation(payload)
    segment_regime_review = _segment_regime_review(payload)
    pattern_regime_map = _pattern_regime_map(payload)
    regime_match_review = _regime_match_review(payload)
    data_intelligence_layers = _data_intelligence_layers(payload)
    market_psychology_overlays = _market_psychology_overlays(payload)
    market_psychology_case_studies = _market_psychology_case_studies(payload)
    event_window_candidates = _event_window_candidates(payload)
    event_regime_rubric = _event_regime_classification_rubric(payload)
    event_window_review = _event_window_review(payload)
    intelligence_benchmark = _intelligence_benchmark(payload)
    pages = [
        {"path": "00-Home.md", "content": "\n".join(["# Domain Chip Crypto Trading", "", "This vault is the operator surface for `domain-chip-crypto-trading`.", "", "Start here:", "", "- [[07-Domains/Crypto Trading/Home]]", "- [[07-Domains/Crypto Trading/System State]]", "- [[07-Domains/Crypto Trading/Operator Guide]]", "- [[07-Domains/Crypto Trading/State Audit 2026-03-15]]", "- [[07-Domains/Crypto Trading/24 Hour Plan 2026-03-15]]", "- [[07-Domains/Crypto Trading/Intelligence System Audit]]", "- [[07-Domains/Crypto Trading/Intelligence Benchmark]]", "- [[07-Domains/Crypto Trading/Loop Progression]]", "- [[07-Domains/Crypto Trading/Learning Loop]]", "- [[07-Domains/Crypto Trading/Backtest Loop]]", "- [[07-Domains/Crypto Trading/Backtest Leaderboard]]", "- [[07-Domains/Crypto Trading/Doctrine Registry]]", "- [[07-Domains/Crypto Trading/Strategy Catalog]]", "- [[07-Domains/Crypto Trading/Benchmark Bridge]]", "- [[07-Domains/Crypto Trading/Paper Trade Queue]]", "- [[07-Domains/Crypto Trading/Paper Trade Outcomes]]", "- [[07-Domains/Crypto Trading/Paper Trade Loop]]", "- [[07-Domains/Crypto Trading/Contradictions]]", "- [[07-Domains/Crypto Trading/Next Probes]]", "- [[07-Domains/Crypto Trading/Research Sources]]", "- [[07-Domains/Crypto Trading/Research Backlog]]", "- [[07-Domains/Crypto Trading/Next to Research]]", "- [[07-Domains/Crypto Trading/Research Scout Queue]]", "- [[07-Domains/Crypto Trading/Market Regime Intelligence]]", "- [[07-Domains/Crypto Trading/Regime Taxonomy and Confidence]]", "- [[07-Domains/Crypto Trading/Data and Intelligence Layers]]", "- [[07-Domains/Crypto Trading/Market Psychology Overlays]]", "- [[07-Domains/Crypto Trading/Market Psychology Cases]]", "- [[07-Domains/Crypto Trading/Event Window Candidates]]", "- [[07-Domains/Crypto Trading/Event Regime Classification Rubric]]", "- [[07-Domains/Crypto Trading/Event Window Review]]", "- [[07-Domains/Crypto Trading/Timeline Packs]]", "- [[07-Domains/Crypto Trading/Timeline Pack Validation]]", "- [[07-Domains/Crypto Trading/Segment Regime Review]]", "- [[07-Domains/Crypto Trading/Regime Match Review]]", "- [[07-Domains/Crypto Trading/Pattern Regime Pairing]]", "- [[07-Domains/Crypto Trading/Doctrine Packets]]", "- [[07-Domains/Crypto Trading/Doctrine Cards]]", "- [[07-Domains/Crypto Trading/Recursive Flywheel]]", "- [[07-Domains/Crypto Trading/Variety Backlog]]", "- [[07-Domains/Crypto Trading/Mutation Backlog]]", "- [[07-Domains/Crypto Trading/Heavy Backtest Queue]]", "- [[07-Domains/Crypto Trading/Self Edit Queue]]", "- [[07-Domains/Crypto Trading/Recursion Audit]]", "", "Operator rules:", "", "- research backlog widens the doctrine frontier", "- next-to-research keeps future scouting distinct from active packet backlog", "- research scout queue ranks what the automation should consume next", "- regime intelligence maps pattern families to the market conditions they should be tested in", "- regime taxonomy explains the timing and confidence logic behind those labels", "- data and intelligence layers show which external signals deserve trust and what they should influence", "- psychology overlays explain why the same catalyst can resolve differently depending on expectation, crowding, and second-order effects", "- psychology cases should preserve market-memory examples where first reaction and durable consequence diverged", "- event window candidates make macro timing design explicit before benchmarking it", "- event-regime rubric defines how transition and shock should be separated before pack extraction", "- event-window review should decide which candidates become packs and which must stay in research design", "- timeline packs turn regime windows into concrete dataset extraction work", "- validation proves whether a pack actually matches its claimed regime", "- segment-regime review checks whether weak walk-forward slices are still inside the claimed regime or drifting into a different validated market condition", "- regime-match review routes mislabeled proxy packs into relabel or archive-extension work", "- pattern-regime pairing should be grounded in validated packs, not labels alone", "- learning feeds doctrine cards", "- backtest is the inner benchmark lane", "- paper trade is the slower outer validation lane", "- recursion may propose changes, but only heavy-backtest evidence can ground them", "- do not treat profitable residue as doctrine without a bridge decision", "- promote combinations, not isolated indicator tweaks"])} ,
        {"path": "07-Domains/Crypto Trading/Home.md", "content": _home_page(rows)},
        {"path": "07-Domains/Crypto Trading/System State.md", "content": _system_state_page(benchmark_summary, intelligence_benchmark, paper_trade_summary)},
        {"path": "07-Domains/Crypto Trading/Operator Guide.md", "content": _operator_guide_page(benchmark_summary, intelligence_benchmark, backtest_loop_report, paper_trade_summary)},
        {"path": "07-Domains/Crypto Trading/Flywheel.md", "content": "\n".join(["# Flywheel", "", "This chip should run three governing loops connected by explicit handoff packets.", "", "Pass sequence:", "", "1. learning loop ingests doctrine packets into doctrine cards", "2. backtest loop benchmarks, mutates, and writes bridge packets", "3. paper-trade loop validates only bridge-approved candidates", "4. watchtower refreshes the shared operator surface", "", "Loop split:", "", "- `learning_loop`: research packet -> doctrine card", "- `backtest_loop`: doctrine card -> benchmark -> contradiction -> bridge", "- `paper_trade_loop`: bridge-approved queue -> outer validation -> demotion or live-readiness review", "", "Anti-patterns:", "", "- strategy churn without doctrine anchors", "- optimizing on PnL alone", "- collapsing backtest and paper-trade truth into one lane", "- promoting exciting curves as doctrine before extracting boundaries"])} ,
        {"path": "07-Domains/Crypto Trading/Loop Progression.md", "content": _loop_progression_page(rows, learning_loop_report, backtest_loop_report, paper_trade_loop_report)},
        {"path": "07-Domains/Crypto Trading/Learning Loop.md", "content": _learning_loop_page(learning_loop_report)},
        {"path": "07-Domains/Crypto Trading/Backtest Loop.md", "content": _backtest_loop_page(backtest_loop_report)},
        {"path": "07-Domains/Crypto Trading/Backtest Leaderboard.md", "content": _leaderboard_page(rows, benchmark_summary)},
        {"path": "07-Domains/Crypto Trading/Doctrine Registry.md", "content": _doctrine_registry_page(rows)},
        {"path": "07-Domains/Crypto Trading/Strategy Catalog.md", "content": _strategy_catalog_page(rows)},
        {"path": "07-Domains/Crypto Trading/Benchmark Bridge.md", "content": _benchmark_bridge_page(rows, packets)},
        {"path": "07-Domains/Crypto Trading/Paper Trade Queue.md", "content": _paper_trade_queue_page(paper_trade_queue, paper_trade_summary)},
        {"path": "07-Domains/Crypto Trading/Paper Trade Outcomes.md", "content": _paper_trade_outcomes_page(paper_trade_summary)},
        {"path": "07-Domains/Crypto Trading/Paper Trade Loop.md", "content": _paper_trade_loop_page(paper_trade_loop_report)},
        {"path": "07-Domains/Crypto Trading/Contradictions.md", "content": _contradictions_page(rows, probes)},
        {"path": "07-Domains/Crypto Trading/Next Probes.md", "content": _next_probes_page(payload, probes)},
        {"path": "07-Domains/Crypto Trading/Research Sources.md", "content": _research_sources_page(sources)},
        {"path": "07-Domains/Crypto Trading/Research Backlog.md", "content": _research_backlog_page(research_backlog)},
        {"path": "07-Domains/Crypto Trading/Next to Research.md", "content": _next_to_research_page(research_backlog)},
        {"path": "07-Domains/Crypto Trading/Research Scout Queue.md", "content": _research_scout_queue_page(research_scout_queue)},
        {"path": "07-Domains/Crypto Trading/Market Regime Intelligence.md", "content": _market_regime_intelligence_page(research_backlog)},
        {"path": "07-Domains/Crypto Trading/Regime Taxonomy and Confidence.md", "content": _regime_taxonomy_confidence_page(research_backlog, timeline_pack_validation)},
        {"path": "07-Domains/Crypto Trading/Data and Intelligence Layers.md", "content": _data_intelligence_layers_page(data_intelligence_layers)},
        {"path": "07-Domains/Crypto Trading/Market Psychology Overlays.md", "content": _market_psychology_overlays_page(market_psychology_overlays)},
        {"path": "07-Domains/Crypto Trading/Market Psychology Cases.md", "content": _market_psychology_case_studies_page(market_psychology_case_studies)},
        {"path": "07-Domains/Crypto Trading/Event Window Candidates.md", "content": _event_window_candidates_page(event_window_candidates)},
        {"path": "07-Domains/Crypto Trading/Event Regime Classification Rubric.md", "content": _event_regime_classification_rubric_page(event_regime_rubric)},
        {"path": "07-Domains/Crypto Trading/Event Window Review.md", "content": _event_window_review_page(event_window_review)},
        {"path": "07-Domains/Crypto Trading/Intelligence System Audit.md", "content": _intelligence_system_audit_page(pattern_regime_map, event_window_review, backtest_loop_report, timeline_pack_validation)},
        {"path": "07-Domains/Crypto Trading/Intelligence Benchmark.md", "content": _intelligence_benchmark_page(intelligence_benchmark)},
        {"path": "07-Domains/Crypto Trading/Timeline Packs.md", "content": _timeline_packs_page(timeline_packs)},
        {"path": "07-Domains/Crypto Trading/Timeline Pack Validation.md", "content": _timeline_pack_validation_page(timeline_pack_validation)},
        {"path": "07-Domains/Crypto Trading/Segment Regime Review.md", "content": _segment_regime_review_page(segment_regime_review)},
        {"path": "07-Domains/Crypto Trading/Regime Match Review.md", "content": _regime_match_review_page(regime_match_review)},
        {"path": "07-Domains/Crypto Trading/Pattern Regime Pairing.md", "content": _pattern_regime_pairing_page(pattern_regime_map)},
        {"path": "07-Domains/Crypto Trading/Doctrine Packets.md", "content": _doctrine_packets_page(doctrine_packets, cards)},
        {"path": "07-Domains/Crypto Trading/Doctrine Cards.md", "content": _doctrine_cards_page(cards)},
        {"path": "07-Domains/Crypto Trading/Recursive Flywheel.md", "content": _recursive_flywheel_page(payload, audit, queue, self_edit_queue, self_edit_audit)},
        {"path": "07-Domains/Crypto Trading/Variety Backlog.md", "content": _variety_backlog_page(variety_backlog)},
        {"path": "07-Domains/Crypto Trading/Mutation Backlog.md", "content": _mutation_backlog_page(backlog)},
        {"path": "07-Domains/Crypto Trading/Heavy Backtest Queue.md", "content": _heavy_backtest_queue_page(queue)},
        {"path": "07-Domains/Crypto Trading/Self Edit Queue.md", "content": _self_edit_queue_page(self_edit_queue, self_edit_evaluations, self_edit_audit)},
        {"path": "07-Domains/Crypto Trading/Recursion Audit.md", "content": _recursion_audit_page(audit)},
    ]
    return {"pages": pages}


def main() -> None:
    parser = argparse.ArgumentParser(prog="domain_chip_crypto_trading")
    parser.add_argument("hook", choices=["evaluate", "suggest", "packets", "watchtower"])
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    payload = _load(args.input)
    response = evaluate(payload) if args.hook == "evaluate" else suggest(payload) if args.hook == "suggest" else packets(payload) if args.hook == "packets" else watchtower(payload)
    _write(args.output, response)


if __name__ == "__main__":
    main()
