from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ID_PREFIX = "kxbtc15m-"
MIN_MEANINGFUL_OVERLAP_RATIO = 0.25


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _parse_contract_timestamp(contract_id: str) -> datetime | None:
    raw = str(contract_id or "").strip()
    if not raw or not raw.startswith(CONTRACT_ID_PREFIX):
        return None
    try:
        return datetime.strptime(raw[len(CONTRACT_ID_PREFIX) :], "%Y%m%d-%H%M")
    except ValueError:
        return None


def _parse_window_start(raw: str) -> datetime | None:
    value = str(raw or "").strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


def _parse_window_end(raw: str) -> datetime | None:
    start = _parse_window_start(raw)
    if start is None:
        return None
    return start + timedelta(days=1) - timedelta(minutes=1)


def _market_regime_to_regime_id(value: str) -> str:
    mapping = {
        "trend": "trend_continuation_greed",
        "range": "range_chop_mean_reversion",
        "high_vol": "fear_shock_high_alert",
        "event_driven": "event_driven_macro_transition",
        "compression": "compression_pre_breakout",
    }
    return mapping.get(str(value or "").strip(), str(value or "").strip())


def _segment_overlap_ratio(
    segment_start: datetime | None,
    segment_end: datetime | None,
    window_start: datetime | None,
    window_end: datetime | None,
) -> float:
    if segment_start is None or segment_end is None or window_start is None or window_end is None:
        return 0.0
    latest_start = max(segment_start, window_start)
    earliest_end = min(segment_end, window_end)
    if earliest_end < latest_start:
        return 0.0
    overlap_seconds = (earliest_end - latest_start).total_seconds() + 60.0
    segment_seconds = max(60.0, (segment_end - segment_start).total_seconds() + 60.0)
    return round(max(0.0, min(1.0, overlap_seconds / segment_seconds)), 4)


def _weakest_segment(row: dict[str, Any]) -> dict[str, Any]:
    result = row.get("result", {})
    result = result if isinstance(result, dict) else {}
    segments = result.get("walk_forward_stats", [])
    segments = segments if isinstance(segments, list) else []
    ranked = sorted(
        [item for item in segments if isinstance(item, dict)],
        key=lambda item: (
            float(item.get("profitability_score", 0.0) or 0.0),
            float(item.get("avg_return", 0.0) or 0.0),
        ),
    )
    return ranked[0] if ranked else {}


def build_segment_regime_review(repo_root: Path | None = None) -> Path:
    root = repo_root or REPO_ROOT
    benchmark = _load_json(root / "artifacts" / "backtests" / "heavy_backtest_summary.json", {})
    timeline_packs = _load_json(root / "artifacts" / "research" / "timeline_packs.json", {})
    validation = _load_json(root / "artifacts" / "research" / "timeline_pack_validation.json", {})

    benchmark_rows = benchmark.get("rows", []) if isinstance(benchmark.get("rows"), list) else []
    timeline_rows = timeline_packs.get("rows", []) if isinstance(timeline_packs.get("rows"), list) else []
    validation_rows = validation.get("rows", []) if isinstance(validation.get("rows"), list) else []

    validation_by_pack: dict[str, dict[str, Any]] = {}
    for row in validation_rows:
        if not isinstance(row, dict):
            continue
        pack_id = str(row.get("pack_id", "")).strip()
        if pack_id:
            validation_by_pack[pack_id] = row

    pack_index: dict[str, dict[str, Any]] = {}
    for row in timeline_rows:
        if not isinstance(row, dict):
            continue
        pack_id = str(row.get("pack_id", "")).strip()
        if not pack_id:
            continue
        validation_row = validation_by_pack.get(pack_id, {})
        pack_index[pack_id] = {
            "pack_id": pack_id,
            "regime_id": str(row.get("regime_id", "")).strip(),
            "regime_label": row.get("regime_label"),
            "window_id": row.get("window_id"),
            "start_date": row.get("start_date"),
            "end_date": row.get("end_date"),
            "source_status": row.get("source_status"),
            "coverage_status": row.get("coverage_status"),
            "validation_status": validation_row.get("validation_status"),
            "claimed_regime_score": validation_row.get("claimed_regime_score"),
            "predicted_regime_id": validation_row.get("predicted_regime_id"),
            "predicted_regime_score": validation_row.get("predicted_regime_score"),
            "dataset_ready": bool(validation_row.get("dataset_ready")),
            "notes": validation_row.get("notes", []),
        }

    review_rows: list[dict[str, Any]] = []
    overlap_regimes: Counter[str] = Counter()

    for row in benchmark_rows[:8]:
        if not isinstance(row, dict):
            continue
        weakest = _weakest_segment(row)
        if not weakest:
            continue
        mutations = row.get("mutations", {})
        mutations = mutations if isinstance(mutations, dict) else {}
        result = row.get("result", {})
        result = result if isinstance(result, dict) else {}
        regime_validation = result.get("regime_validation", {})
        regime_validation = regime_validation if isinstance(regime_validation, dict) else {}

        segment_start = _parse_contract_timestamp(str(weakest.get("start_contract_id", "")))
        segment_end = _parse_contract_timestamp(str(weakest.get("end_contract_id", "")))
        claimed_regime_id = _market_regime_to_regime_id(str(mutations.get("market_regime", "")))

        overlaps: list[dict[str, Any]] = []
        for pack in pack_index.values():
            ratio = _segment_overlap_ratio(
                segment_start,
                segment_end,
                _parse_window_start(str(pack.get("start_date", ""))),
                _parse_window_end(str(pack.get("end_date", ""))),
            )
            if ratio <= 0.0:
                continue
            pack_payload = dict(pack)
            pack_payload["overlap_ratio"] = ratio
            overlaps.append(pack_payload)

        overlaps.sort(
            key=lambda item: (
                float(item.get("overlap_ratio", 0.0) or 0.0),
                1.0 if str(item.get("validation_status", "")).strip() == "validated_match" else 0.0,
                float(item.get("predicted_regime_score", 0.0) or 0.0),
            ),
            reverse=True,
        )
        strongest = overlaps[0] if overlaps else {}
        strongest_ratio = float(strongest.get("overlap_ratio", 0.0) or 0.0) if strongest else 0.0
        strongest_regime_id = str(strongest.get("regime_id", "")).strip()
        if strongest_regime_id and strongest_ratio >= MIN_MEANINGFUL_OVERLAP_RATIO:
            overlap_regimes[strongest_regime_id] += 1

        diagnosis = "no_overlap_evidence"
        recommended_action = "design a dedicated timeline pack before mutating this failure further."
        if strongest and strongest_ratio >= MIN_MEANINGFUL_OVERLAP_RATIO:
            validation_status = str(strongest.get("validation_status", "")).strip()
            if strongest_regime_id == claimed_regime_id and validation_status == "validated_match":
                diagnosis = "segment_matches_claimed_regime"
                recommended_action = "Keep the mutation family inside the claimed regime and improve execution or timing rather than rerouting the doctrine."
            elif strongest_regime_id != claimed_regime_id and validation_status == "validated_match":
                diagnosis = "regime_drift_detected"
                recommended_action = (
                    f"Treat this failure as `{strongest_regime_id}` drift and mutate around that regime instead of tightening the current `{claimed_regime_id}` filters."
                )
            elif validation_status == "mixed_proxy":
                diagnosis = "mixed_overlap_proxy"
                recommended_action = "Narrow the segment or timeline pack further before trusting a routing decision."
            else:
                diagnosis = "overlap_needs_review"
                recommended_action = "Review the overlapping pack labels before turning this segment into a doctrine or mutation lane."

        review_rows.append(
            {
                "candidate_id": row.get("candidate_id"),
                "candidate_market_regime": mutations.get("market_regime"),
                "claimed_regime_id": claimed_regime_id,
                "validated_regime_support": bool(regime_validation.get("validated_regime_support")),
                "weakest_segment_id": weakest.get("segment_id"),
                "weakest_profitability_score": weakest.get("profitability_score"),
                "weakest_avg_return": weakest.get("avg_return"),
                "weakest_trade_count": weakest.get("trade_count"),
                "segment_start_contract_id": weakest.get("start_contract_id"),
                "segment_end_contract_id": weakest.get("end_contract_id"),
                "segment_start": segment_start.isoformat(timespec="minutes") if segment_start else None,
                "segment_end": segment_end.isoformat(timespec="minutes") if segment_end else None,
                "strongest_overlap_pack_id": strongest.get("pack_id") if strongest_ratio >= MIN_MEANINGFUL_OVERLAP_RATIO else None,
                "strongest_overlap_regime_id": strongest_regime_id if strongest_ratio >= MIN_MEANINGFUL_OVERLAP_RATIO else None,
                "strongest_overlap_validation_status": strongest.get("validation_status") if strongest_ratio >= MIN_MEANINGFUL_OVERLAP_RATIO else None,
                "strongest_overlap_ratio": strongest.get("overlap_ratio") if strongest_ratio >= MIN_MEANINGFUL_OVERLAP_RATIO else None,
                "strongest_overlap_predicted_regime_id": strongest.get("predicted_regime_id") if strongest_ratio >= MIN_MEANINGFUL_OVERLAP_RATIO else None,
                "strongest_overlap_predicted_regime_score": strongest.get("predicted_regime_score") if strongest_ratio >= MIN_MEANINGFUL_OVERLAP_RATIO else None,
                "overlap_candidates": overlaps[:3],
                "diagnosis": diagnosis,
                "recommended_action": recommended_action,
            }
        )

    diagnosis_counts = Counter(str(row.get("diagnosis", "")).strip() for row in review_rows)
    top_overlap_regime = overlap_regimes.most_common(1)[0][0] if overlap_regimes else None

    payload = {
        "review_id": "segment-regime-review-v1",
        "row_count": len(review_rows),
        "rows": review_rows,
        "summary": {
            "regime_drift_count": diagnosis_counts.get("regime_drift_detected", 0),
            "segment_match_count": diagnosis_counts.get("segment_matches_claimed_regime", 0),
            "mixed_overlap_count": diagnosis_counts.get("mixed_overlap_proxy", 0),
            "needs_review_count": diagnosis_counts.get("overlap_needs_review", 0),
            "no_overlap_count": diagnosis_counts.get("no_overlap_evidence", 0),
            "top_overlap_regime_id": top_overlap_regime,
            "top_candidate_id": benchmark.get("top_candidate_id"),
        },
    }
    target = root / "artifacts" / "research" / "segment_regime_review.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def main() -> None:
    path = build_segment_regime_review(REPO_ROOT)
    print(path)


if __name__ == "__main__":
    main()
