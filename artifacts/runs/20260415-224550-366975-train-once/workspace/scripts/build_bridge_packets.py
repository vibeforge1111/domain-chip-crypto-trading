from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from safe_write import safe_write_json


def _load_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def _mutations(row: dict[str, Any]) -> dict[str, str]:
    return {
        str(item.get("name", "")): str(item.get("value", ""))
        for item in row.get("applied_mutations", [])
        if isinstance(item, dict)
    }


def _metrics(row: dict[str, Any]) -> dict[str, Any]:
    metrics = row.get("metrics", {})
    return metrics if isinstance(metrics, dict) else {}


def _result(row: dict[str, Any]) -> dict[str, Any]:
    result = row.get("chip_result", {})
    return result if isinstance(result, dict) else {}


def _safe_packet_filename(run_id: str) -> str:
    raw = str(run_id).strip() or "bridge-packet"
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in raw)
    while "--" in slug:
        slug = slug.replace("--", "-")
    slug = slug.strip("-") or "bridge-packet"
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    if len(slug) > 80:
        slug = slug[:80].rstrip("-")
    return f"{slug}-{digest}.json"


def _packet_for_row(row: dict[str, Any]) -> dict[str, Any] | None:
    candidate_id = str(row.get("candidate_id", "")).strip()
    if not candidate_id or candidate_id == "global-baseline":
        return None
    mutations = _mutations(row)
    metrics = _metrics(row)
    result = _result(row)
    next_step = str(result.get("recommended_next_step", "")).strip()
    if next_step == "queue_for_paper_trade":
        candidate_kind = "benchmark_grounded_candidate"
        eligibility = "eligible_for_paper_trade"
    elif next_step == "run_contradiction_probe":
        candidate_kind = "benchmark_grounded_boundary"
        eligibility = "eligible_for_boundary_promotion"
    else:
        candidate_kind = "benchmark_grounded_candidate"
        eligibility = "benchmark_evidence_only"
    return {
        "bridge_version": "crypto-bridge.v1",
        "generated_at": str(row.get("created_at", "")),
        "source_benchmark": "backtest_benchmark",
        "candidate_id": candidate_id,
        "run_id": str(row.get("run_id", "")),
        "doctrine_id": mutations.get("doctrine_id", ""),
        "strategy_id": mutations.get("strategy_id", ""),
        "market_regime": mutations.get("market_regime", ""),
        "timeframe": mutations.get("timeframe", ""),
        "venue": mutations.get("venue", ""),
        "asset_universe": mutations.get("asset_universe", ""),
        "mutations": mutations,
        "metric_name": "profitability_score",
        "profitability_score": metrics.get("profitability_score"),
        "sharpe_ratio": metrics.get("sharpe_ratio"),
        "max_drawdown": metrics.get("max_drawdown"),
        "win_rate": metrics.get("win_rate"),
        "paper_trade_readiness": metrics.get("paper_trade_readiness"),
        "contract_count": result.get("contract_count"),
        "covered_contract_count": result.get("covered_contract_count"),
        "trade_count": result.get("trade_count"),
        "minimum_trade_count": result.get("minimum_trade_count"),
        "trade_count_gate_pass": result.get("trade_count_gate_pass"),
        "holdout_profitability_score": result.get("holdout_profitability_score"),
        "walk_forward_consistency": result.get("walk_forward_consistency"),
        "walk_forward_stats": result.get("walk_forward_stats"),
        "stress_resilience": result.get("stress_resilience"),
        "stress_stats": result.get("stress_stats"),
        "regime_stats": result.get("regime_stats"),
        "data_mode": result.get("data_mode", "score_only"),
        "promotion_candidate_kind": candidate_kind,
        "eligibility_status": eligibility,
        "recommended_next_step": next_step,
        "primary_mechanism": result.get("mechanism", ""),
        "primary_boundary": result.get("boundary", ""),
        "report_paths": [str(row.get("run_dir", "")), str(row.get("trace_path", ""))],
    }


def _packet_for_benchmark_row(row: dict[str, Any], generated_at: str) -> dict[str, Any] | None:
    candidate_id = str(row.get("candidate_id", "")).strip()
    if not candidate_id or candidate_id == "global-baseline":
        return None
    metrics = row.get("metrics", {})
    metrics = metrics if isinstance(metrics, dict) else {}
    mutations = row.get("mutations", {})
    mutations = mutations if isinstance(mutations, dict) else {}
    result = row.get("result", {})
    result = result if isinstance(result, dict) else {}
    next_step = str(result.get("recommended_next_step", "")).strip()
    if next_step == "queue_for_paper_trade":
        candidate_kind = "benchmark_grounded_candidate"
        eligibility = "eligible_for_paper_trade"
    elif next_step == "run_contradiction_probe":
        candidate_kind = "benchmark_grounded_boundary"
        eligibility = "eligible_for_boundary_promotion"
    else:
        candidate_kind = "benchmark_grounded_candidate"
        eligibility = "benchmark_evidence_only"
    return {
        "bridge_version": "crypto-bridge.v1",
        "generated_at": generated_at,
        "source_benchmark": "backtest_benchmark",
        "candidate_id": candidate_id,
        "run_id": "heavy-backtest-" + candidate_id,
        "doctrine_id": mutations.get("doctrine_id", ""),
        "strategy_id": mutations.get("strategy_id", ""),
        "market_regime": mutations.get("market_regime", ""),
        "timeframe": mutations.get("timeframe", ""),
        "venue": mutations.get("venue", ""),
        "asset_universe": mutations.get("asset_universe", ""),
        "mutations": mutations,
        "metric_name": "profitability_score",
        "profitability_score": metrics.get("profitability_score"),
        "sharpe_ratio": metrics.get("sharpe_ratio"),
        "max_drawdown": metrics.get("max_drawdown"),
        "win_rate": metrics.get("win_rate"),
        "paper_trade_readiness": metrics.get("paper_trade_readiness"),
        "contract_count": result.get("contract_count"),
        "covered_contract_count": result.get("covered_contract_count"),
        "trade_count": result.get("trade_count"),
        "minimum_trade_count": result.get("minimum_trade_count"),
        "trade_count_gate_pass": result.get("trade_count_gate_pass"),
        "holdout_profitability_score": result.get("holdout_profitability_score"),
        "walk_forward_consistency": result.get("walk_forward_consistency"),
        "walk_forward_stats": result.get("walk_forward_stats"),
        "stress_resilience": result.get("stress_resilience"),
        "stress_stats": result.get("stress_stats"),
        "regime_stats": result.get("regime_stats"),
        "data_mode": result.get("data_mode", "contract_window_backtest"),
        "promotion_candidate_kind": candidate_kind,
        "eligibility_status": eligibility,
        "recommended_next_step": next_step,
        "primary_mechanism": result.get("mechanism", ""),
        "primary_boundary": result.get("boundary", ""),
        "report_paths": ["artifacts/backtests/heavy_backtest_summary.json"],
    }


def _benchmark_packets(repo_root: Path) -> list[dict[str, Any]]:
    summary_path = repo_root / "artifacts" / "backtests" / "heavy_backtest_summary.json"
    if not summary_path.exists():
        return []
    try:
        payload = json.loads(summary_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        return []
    generated_at = summary_path.stat().st_mtime_ns
    packets: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        packet = _packet_for_benchmark_row(row, str(generated_at))
        if packet is not None:
            packets.append(packet)
    return packets


def build_bridge_packets(repo_root: Path) -> list[Path]:
    ledger_path = repo_root / "artifacts" / "ledger" / "runs.jsonl"
    target_root = repo_root / "artifacts" / "promotion" / "benchmark_grounded"
    target_root.mkdir(parents=True, exist_ok=True)
    for path in target_root.glob("*.json"):
        path.unlink()
    written: list[Path] = []
    benchmark_packets = _benchmark_packets(repo_root)
    if benchmark_packets:
        for packet in benchmark_packets:
            path = target_root / _safe_packet_filename(str(packet.get("run_id", "")))
            safe_write_json(path, packet)
            written.append(path)
        return written
    for row in _load_rows(ledger_path):
        packet = _packet_for_row(row)
        if packet is None:
            continue
        path = target_root / _safe_packet_filename(str(packet.get("run_id", "")))
        safe_write_json(path, packet)
        written.append(path)
    return written


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    build_bridge_packets(repo_root)


if __name__ == "__main__":
    main()
