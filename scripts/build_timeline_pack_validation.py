from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any
from datetime import datetime


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _high(value: float, low: float, high: float) -> float:
    if high <= low:
        return 0.0
    return _clamp((value - low) / (high - low))


def _low(value: float, low: float, high: float) -> float:
    return 1.0 - _high(value, low, high)


def _quantile(values: list[float], ratio: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = int((len(ordered) - 1) * ratio)
    return ordered[index]


def _parse_ts(value: Any) -> int:
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value or "").strip()
    if not text:
        return 0
    if text.isdigit():
        return int(text)
    return int(datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp())


def _row_ts(row: dict[str, Any]) -> int:
    for key in ("timestamp", "open_time", "time", "ts"):
        if key in row:
            return _parse_ts(row.get(key))
    return 0


def _bucket_candles(candles: list[dict[str, Any]], bucket_seconds: int) -> list[dict[str, Any]]:
    if bucket_seconds <= 0 or len(candles) < 2:
        return candles
    rows = sorted(candles, key=_row_ts)
    buckets: list[dict[str, Any]] = []
    current_rows: list[dict[str, Any]] = []
    current_bucket = None
    for row in rows:
        ts = _row_ts(row)
        if ts <= 0:
            continue
        bucket = ts - (ts % bucket_seconds)
        if current_bucket is None or bucket != current_bucket:
            if current_rows:
                buckets.append(
                    {
                        "open": current_rows[0].get("open"),
                        "high": max(float(item.get("high", 0.0) or 0.0) for item in current_rows),
                        "low": min(float(item.get("low", 0.0) or 0.0) for item in current_rows),
                        "close": current_rows[-1].get("close"),
                        "timestamp": current_bucket,
                    }
                )
            current_rows = [row]
            current_bucket = bucket
        else:
            current_rows.append(row)
    if current_rows and current_bucket is not None:
        buckets.append(
            {
                "open": current_rows[0].get("open"),
                "high": max(float(item.get("high", 0.0) or 0.0) for item in current_rows),
                "low": min(float(item.get("low", 0.0) or 0.0) for item in current_rows),
                "close": current_rows[-1].get("close"),
                "timestamp": current_bucket,
            }
        )
    return buckets


def _candles_metrics(candles: list[dict[str, Any]]) -> dict[str, float]:
    if len(candles) < 3:
        return {}
    closes = [float(row.get("close", 0.0) or 0.0) for row in candles]
    opens = [float(row.get("open", 0.0) or 0.0) for row in candles]
    highs = [float(row.get("high", 0.0) or 0.0) for row in candles]
    lows = [float(row.get("low", 0.0) or 0.0) for row in candles]
    if not closes or closes[0] <= 0.0:
        return {}
    close_to_close_diffs = [closes[index] - closes[index - 1] for index in range(1, len(closes))]
    abs_diffs = [abs(value) for value in close_to_close_diffs]
    returns = [diff / closes[index - 1] for index, diff in enumerate(close_to_close_diffs, start=1) if closes[index - 1] > 0.0]
    abs_returns = [abs(value) for value in returns]
    signs = [1 if value > 0 else -1 if value < 0 else 0 for value in returns]
    directional_path = sum(abs_diffs)
    directional_efficiency = abs(closes[-1] - closes[0]) / directional_path if directional_path > 0.0 else 0.0
    sign_flips = 0
    flip_denominator = 0
    previous_sign = 0
    for sign in signs:
        if sign == 0:
            continue
        if previous_sign != 0:
            flip_denominator += 1
            if sign != previous_sign:
                sign_flips += 1
        previous_sign = sign
    sign_flip_rate = sign_flips / flip_denominator if flip_denominator > 0 else 0.0
    mean_abs_return = mean(abs_returns) if abs_returns else 0.0
    max_abs_return = max(abs_returns) if abs_returns else 0.0
    intrabar_ranges = [max(0.0, high - low) / open_ for high, low, open_ in zip(highs, lows, opens) if open_ > 0.0]
    avg_intrabar_range = mean(intrabar_ranges) if intrabar_ranges else 0.0
    breakout_burst_ratio = max_abs_return / mean_abs_return if mean_abs_return > 0.0 else 0.0
    return {
        "candle_count": float(len(candles)),
        "net_return_pct": ((closes[-1] / closes[0]) - 1.0) * 100.0,
        "directional_efficiency": directional_efficiency,
        "sign_flip_rate": sign_flip_rate,
        "mean_abs_return_pct": mean_abs_return * 100.0,
        "max_abs_return_pct": max_abs_return * 100.0,
        "p95_abs_return_pct": _quantile(abs_returns, 0.95) * 100.0,
        "p99_abs_return_pct": _quantile(abs_returns, 0.99) * 100.0,
        "avg_intrabar_range_pct": avg_intrabar_range * 100.0,
        "breakout_burst_ratio": breakout_burst_ratio,
    }


def _metric_bundle(candles: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    if not candles:
        return {}
    return {
        "1m": _candles_metrics(candles),
        "15m": _candles_metrics(_bucket_candles(candles, 15 * 60)),
        "4h": _candles_metrics(_bucket_candles(candles, 4 * 60 * 60)),
        "1d": _candles_metrics(_bucket_candles(candles, 24 * 60 * 60)),
    }


def _regime_scores(metrics_by_timeframe: dict[str, dict[str, float]]) -> dict[str, float]:
    if not metrics_by_timeframe:
        return {}
    metrics_15m = metrics_by_timeframe.get("15m", {})
    metrics_4h = metrics_by_timeframe.get("4h", {})
    metrics_1d = metrics_by_timeframe.get("1d", {})
    net_return_pct_1d = float(metrics_1d.get("net_return_pct", 0.0) or 0.0)
    net_return_abs_pct_1d = abs(net_return_pct_1d)
    return {
        "trend_continuation_greed": round(
            mean(
                [
                    _high(net_return_pct_1d, 8.0, 40.0),
                    _high(float(metrics_1d.get("directional_efficiency", 0.0) or 0.0), 0.12, 0.36),
                    _high(float(metrics_4h.get("directional_efficiency", 0.0) or 0.0), 0.05, 0.18),
                    _low(float(metrics_4h.get("sign_flip_rate", 0.0) or 0.0), 0.5, 0.62),
                ]
            ),
            4,
        ),
        "range_chop_mean_reversion": round(
            mean(
                [
                    _low(net_return_abs_pct_1d, 1.0, 10.0),
                    _low(float(metrics_1d.get("directional_efficiency", 0.0) or 0.0), 0.03, 0.18),
                    _high(float(metrics_4h.get("sign_flip_rate", 0.0) or 0.0), 0.5, 0.58),
                    _low(float(metrics_4h.get("directional_efficiency", 0.0) or 0.0), 0.02, 0.1),
                ]
            ),
            4,
        ),
        "fear_shock_high_alert": round(
            mean(
                [
                    _low(net_return_pct_1d, -4.0, -22.0),
                    _high(float(metrics_1d.get("mean_abs_return_pct", 0.0) or 0.0), 1.8, 3.4),
                    _high(float(metrics_1d.get("p99_abs_return_pct", 0.0) or 0.0), 6.0, 12.5),
                    _high(float(metrics_4h.get("avg_intrabar_range_pct", 0.0) or 0.0), 1.5, 2.3),
                ]
            ),
            4,
        ),
        "compression_pre_breakout": round(
            mean(
                [
                    _low(net_return_abs_pct_1d, 4.0, 18.0),
                    _low(float(metrics_4h.get("mean_abs_return_pct", 0.0) or 0.0), 0.55, 1.1),
                    _low(float(metrics_4h.get("avg_intrabar_range_pct", 0.0) or 0.0), 1.1, 2.2),
                    _low(float(metrics_1d.get("directional_efficiency", 0.0) or 0.0), 0.1, 0.3),
                ]
            ),
            4,
        ),
        "event_driven_macro_transition": round(
            mean(
                [
                    _high(float(metrics_1d.get("p99_abs_return_pct", 0.0) or 0.0), 6.0, 12.0),
                    _high(float(metrics_4h.get("avg_intrabar_range_pct", 0.0) or 0.0), 1.5, 2.6),
                    _high(float(metrics_15m.get("sign_flip_rate", 0.0) or 0.0), 0.52, 0.6),
                    _high(float(metrics_4h.get("breakout_burst_ratio", 0.0) or 0.0), 3.2, 6.0),
                ]
            ),
            4,
        ),
    }


def _validation_status(claimed_regime_id: str, regime_scores: dict[str, float]) -> tuple[str, str, float]:
    if not regime_scores:
        return ("pending_extract", "", 0.0)
    predicted_regime_id = max(regime_scores, key=regime_scores.get)
    claimed_score = float(regime_scores.get(claimed_regime_id, 0.0) or 0.0)
    predicted_score = float(regime_scores.get(predicted_regime_id, 0.0) or 0.0)
    if claimed_regime_id == predicted_regime_id and claimed_score >= 0.62:
        return ("validated_match", predicted_regime_id, claimed_score)
    if claimed_score >= 0.55 and predicted_score - claimed_score <= 0.08:
        return ("mixed_proxy", predicted_regime_id, claimed_score)
    return ("mismatch_review", predicted_regime_id, claimed_score)


def _validation_notes(
    pack: dict[str, Any],
    metrics: dict[str, float],
    metrics_by_timeframe: dict[str, dict[str, float]],
    status: str,
    predicted_regime_id: str,
) -> list[str]:
    notes: list[str] = []
    if not metrics:
        return ["Dataset has not been extracted yet."]
    directional_efficiency = metrics.get("directional_efficiency", 0.0)
    sign_flip_rate = metrics.get("sign_flip_rate", 0.0)
    burst_ratio = metrics.get("breakout_burst_ratio", 0.0)
    avg_intrabar_range_pct = metrics.get("avg_intrabar_range_pct", 0.0)
    metrics_4h = metrics_by_timeframe.get("4h", {})
    metrics_1d = metrics_by_timeframe.get("1d", {})
    if directional_efficiency >= 0.55:
        notes.append("Directional path is strong enough to support continuation-style testing.")
    elif directional_efficiency <= 0.3:
        notes.append("Directional path is weak, which favors fade and reclaim logic over chase entries.")
    if sign_flip_rate >= 0.55:
        notes.append("Return sign flips are frequent, which supports chop / rotation framing.")
    if burst_ratio >= 4.0 or avg_intrabar_range_pct >= 0.2:
        notes.append("Burst and range behavior are elevated, so execution-fragile or shock-sensitive doctrines matter more.")
    if metrics_1d:
        notes.append(
            "Higher-timeframe summary: "
            f"1d net `{round(float(metrics_1d.get('net_return_pct', 0.0) or 0.0), 4)}` pct, "
            f"1d directional_efficiency `{round(float(metrics_1d.get('directional_efficiency', 0.0) or 0.0), 4)}`."
        )
    if metrics_4h:
        notes.append(
            "Execution window summary: "
            f"4h mean_abs_return_pct `{round(float(metrics_4h.get('mean_abs_return_pct', 0.0) or 0.0), 4)}`, "
            f"4h sign_flip_rate `{round(float(metrics_4h.get('sign_flip_rate', 0.0) or 0.0), 4)}`."
        )
    if status == "mismatch_review":
        notes.append(f"Observed behavior currently looks closer to `{predicted_regime_id}` than the claimed regime.")
    return notes


def build_timeline_pack_validation(repo_root: Path | None = None) -> Path:
    root = repo_root or REPO_ROOT
    payload = _load_json(root / "artifacts" / "research" / "timeline_packs.json", {})
    payload = payload if isinstance(payload, dict) else {}
    rows = payload.get("rows", [])
    rows = rows if isinstance(rows, list) else []
    validation_rows: list[dict[str, Any]] = []
    for pack in rows:
        if not isinstance(pack, dict):
            continue
        pack_id = str(pack.get("pack_id", "")).strip()
        dataset_root = root / "data" / "timeline-packs" / pack_id
        metadata_path = dataset_root / "metadata.json"
        candle_path = dataset_root / "btc_1m_candles.jsonl"
        contract_path = dataset_root / "btc_up_down_15m_contracts.jsonl"
        metadata = _load_json(metadata_path, {})
        metadata = metadata if isinstance(metadata, dict) else {}
        candles = _load_jsonl(candle_path)
        metrics_by_timeframe = _metric_bundle(candles)
        metrics = metrics_by_timeframe.get("1m", {})
        regime_scores = _regime_scores(metrics_by_timeframe)
        status, predicted_regime_id, claimed_score = _validation_status(str(pack.get("regime_id", "")).strip(), regime_scores)
        validation_rows.append(
            {
                "pack_id": pack_id,
                "regime_id": pack.get("regime_id"),
                "regime_label": pack.get("regime_label"),
                "window_id": pack.get("window_id"),
                "source_status": pack.get("source_status"),
                "coverage_status": pack.get("coverage_status"),
                "dataset_ready": metadata_path.exists() and candle_path.exists() and contract_path.exists(),
                "validation_status": status,
                "predicted_regime_id": predicted_regime_id,
                "claimed_regime_score": round(claimed_score, 4),
                "predicted_regime_score": round(float(regime_scores.get(predicted_regime_id, 0.0) or 0.0), 4) if predicted_regime_id else 0.0,
                "regime_scores": regime_scores,
                "observed_metrics": metrics,
                "observed_metrics_by_timeframe": metrics_by_timeframe,
                "candle_count": int(metadata.get("candle_count", 0) or 0),
                "contract_count": int(metadata.get("contract_count", 0) or 0),
                "notes": _validation_notes(pack, metrics, metrics_by_timeframe, status, predicted_regime_id),
            }
        )
    counts = {"validated_match": 0, "mixed_proxy": 0, "mismatch_review": 0, "pending_extract": 0}
    for row in validation_rows:
        status = str(row.get("validation_status", "")).strip()
        counts[status] = counts.get(status, 0) + 1
    result = {
        "pack_count": len(validation_rows),
        "validated_match_count": counts.get("validated_match", 0),
        "mixed_proxy_count": counts.get("mixed_proxy", 0),
        "mismatch_review_count": counts.get("mismatch_review", 0),
        "pending_extract_count": counts.get("pending_extract", 0),
        "rows": validation_rows,
        "top_rows": validation_rows[:12],
    }
    target = root / "artifacts" / "research" / "timeline_pack_validation.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def main() -> None:
    path = build_timeline_pack_validation(REPO_ROOT)
    print(path)


if __name__ == "__main__":
    main()
