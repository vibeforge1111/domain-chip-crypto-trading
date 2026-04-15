from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _parse_iso_date(raw: str) -> datetime | None:
    value = str(raw).strip()
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _parse_iso_ts(raw: str) -> datetime | None:
    value = str(raw).strip()
    if not value:
        return None
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(value).astimezone(timezone.utc)
    except ValueError:
        return None


def _data_bounds(repo_root: Path) -> dict[str, dict[str, str]]:
    bounds: dict[str, dict[str, str]] = {}
    candle_path = repo_root / "data" / "btc_1m_candles.jsonl"
    contract_path = repo_root / "data" / "btc_up_down_15m_contracts.jsonl"
    candle_min: datetime | None = None
    candle_max: datetime | None = None
    if candle_path.exists():
        for line in candle_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = _parse_iso_ts(payload.get("ts", ""))
            if ts is None:
                continue
            candle_min = ts if candle_min is None or ts < candle_min else candle_min
            candle_max = ts if candle_max is None or ts > candle_max else candle_max
    contract_min: datetime | None = None
    contract_max: datetime | None = None
    if contract_path.exists():
        for line in contract_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            open_ts = _parse_iso_ts(payload.get("open_ts", ""))
            close_ts = _parse_iso_ts(payload.get("close_ts", ""))
            if open_ts is not None:
                contract_min = open_ts if contract_min is None or open_ts < contract_min else contract_min
            if close_ts is not None:
                contract_max = close_ts if contract_max is None or close_ts > contract_max else contract_max
    if candle_min and candle_max:
        bounds["candles"] = {
            "start": candle_min.isoformat().replace("+00:00", "Z"),
            "end": candle_max.isoformat().replace("+00:00", "Z"),
        }
    if contract_min and contract_max:
        bounds["contracts"] = {
            "start": contract_min.isoformat().replace("+00:00", "Z"),
            "end": contract_max.isoformat().replace("+00:00", "Z"),
        }
    return bounds


def _window_coverage(window: dict[str, Any], bounds: dict[str, dict[str, str]]) -> str:
    start = _parse_iso_date(window.get("start_date", ""))
    end = _parse_iso_date(window.get("end_date", ""))
    candle_bounds = bounds.get("candles", {})
    candle_start = _parse_iso_ts(candle_bounds.get("start", "")) if isinstance(candle_bounds, dict) else None
    candle_end = _parse_iso_ts(candle_bounds.get("end", "")) if isinstance(candle_bounds, dict) else None
    if start is None or end is None or candle_start is None or candle_end is None:
        return "coverage_unknown"
    if start >= candle_start and end <= candle_end:
        return "ready_for_dataset_extract"
    return "needs_data_extension"


def build_timeline_packs(repo_root: Path | None = None) -> Path:
    root = repo_root or REPO_ROOT
    regime_rows = _load_json(root / "docs" / "research-ingest" / "market-regime-intelligence.json", [])
    regime_rows = regime_rows if isinstance(regime_rows, list) else []
    bounds = _data_bounds(root)

    rows: list[dict[str, Any]] = []
    for regime in regime_rows:
        if not isinstance(regime, dict):
            continue
        regime_id = str(regime.get("regime_id", "")).strip()
        label = str(regime.get("label", "")).strip()
        fit_patterns = regime.get("fit_patterns", [])
        fit_patterns = fit_patterns if isinstance(fit_patterns, list) else []
        avoid_patterns = regime.get("avoid_patterns", [])
        avoid_patterns = avoid_patterns if isinstance(avoid_patterns, list) else []
        research_gaps = regime.get("research_gaps", [])
        research_gaps = research_gaps if isinstance(research_gaps, list) else []
        windows = regime.get("benchmark_window_targets", [])
        windows = windows if isinstance(windows, list) else []
        for window in windows:
            if not isinstance(window, dict):
                continue
            source_status = str(window.get("status", "")).strip()
            if source_status in {"retired_proxy", "rejected_proxy"}:
                continue
            window_id = str(window.get("window_id", "")).strip()
            start_date = str(window.get("start_date", "")).strip()
            end_date = str(window.get("end_date", "")).strip()
            rows.append(
                {
                    "pack_id": f"{regime_id}--{window_id}",
                    "regime_id": regime_id,
                    "regime_label": label,
                    "window_id": window_id,
                    "start_date": start_date,
                    "end_date": end_date,
                    "source_status": source_status,
                    "coverage_status": _window_coverage(window, bounds),
                    "reason": str(window.get("reason", "")).strip(),
                    "market_character": str(regime.get("market_character", "")).strip(),
                    "fit_patterns": fit_patterns,
                    "avoid_patterns": avoid_patterns,
                    "research_gaps": research_gaps,
                    "target_paths": {
                        "candles": f"data/timeline-packs/{regime_id}--{window_id}/btc_1m_candles.jsonl",
                        "contracts": f"data/timeline-packs/{regime_id}--{window_id}/btc_up_down_15m_contracts.jsonl",
                        "metadata": f"data/timeline-packs/{regime_id}--{window_id}/metadata.json",
                    },
                }
            )
    rows.sort(
        key=lambda item: (
            0 if str(item.get("coverage_status", "")) == "ready_for_dataset_extract" else 1,
            str(item.get("regime_id", "")),
            str(item.get("window_id", "")),
        )
    )
    payload = {
        "bounds": bounds,
        "pack_count": len(rows),
        "rows": rows,
        "top_rows": rows[:12],
    }
    target = root / "artifacts" / "research" / "timeline_packs.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def main() -> None:
    path = build_timeline_packs(REPO_ROOT)
    print(path)


if __name__ == "__main__":
    main()
