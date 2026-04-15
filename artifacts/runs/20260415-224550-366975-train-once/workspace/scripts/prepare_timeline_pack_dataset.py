from __future__ import annotations

import argparse
import csv
import json
import shutil
import urllib.request
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from build_pattern_regime_map import build_pattern_regime_map
from build_regime_match_review import build_regime_match_review
from build_timeline_pack_validation import build_timeline_pack_validation


REPO_ROOT = Path(__file__).resolve().parents[1]
BINANCE_BASE_URL = "https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1m"


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _parse_ts(raw: str) -> datetime | None:
    value = str(raw).strip()
    if not value:
        return None
    numeric_candidate = value.replace(".", "", 1)
    if numeric_candidate.isdigit():
        try:
            numeric = float(value)
        except ValueError:
            return None
        while numeric > 10_000_000_000:
            numeric = numeric / 1000.0
        return datetime.fromtimestamp(numeric, tz=timezone.utc)
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(value)
    except (ValueError, OSError):
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _parse_date(raw: str, *, end_of_day: bool = False) -> datetime | None:
    value = str(raw).strip()
    if not value:
        return None
    try:
        base = datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    return base + timedelta(days=1) - timedelta(minutes=1) if end_of_day else base


def _load_timeline_pack(pack_id: str) -> dict[str, Any]:
    payload = _load_json(REPO_ROOT / "artifacts" / "research" / "timeline_packs.json", {})
    payload = payload if isinstance(payload, dict) else {}
    rows = payload.get("rows", [])
    rows = rows if isinstance(rows, list) else []
    for row in rows:
        if isinstance(row, dict) and str(row.get("pack_id", "")).strip() == pack_id:
            return row
    return {}


def _fetch_archive_csv(pack_id: str, start: datetime, end: datetime, repo_root: Path) -> Path:
    raw_root = repo_root / "data" / "raw" / "binance" / "timeline-packs" / pack_id
    zip_root = raw_root / "zips"
    extract_root = raw_root / "extracted"
    merged_csv = raw_root / f"{pack_id}.csv"
    # Reuse a previously merged archive when a pack is narrowed or revalidated.
    if merged_csv.exists():
        return merged_csv
    merged_inputs: list[Path] = []
    for current in _dates(start, end):
        stamp = current.strftime("%Y-%m-%d")
        zip_path = zip_root / f"BTCUSDT-1m-{stamp}.zip"
        url = f"{BINANCE_BASE_URL}/BTCUSDT-1m-{stamp}.zip"
        _download(url, zip_path)
        merged_inputs.extend(_extract(zip_path, extract_root / stamp))
    _merge(sorted(merged_inputs), merged_csv)
    return merged_csv


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def _row_from_mapping(row: dict[str, Any]) -> dict[str, Any] | None:
    ts_value = row.get("timestamp") or row.get("ts") or row.get("open_time")
    ts = _parse_ts(str(ts_value or ""))
    if ts is None:
        return None
    try:
        return {
            "ts": ts,
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": float(row.get("volume", 0.0)),
        }
    except (KeyError, TypeError, ValueError):
        return None


def _row_from_sequence(parts: list[str]) -> dict[str, Any] | None:
    if len(parts) < 6:
        return None
    ts = _parse_ts(parts[0])
    if ts is None:
        return None
    try:
        return {
            "ts": ts,
            "open": float(parts[1]),
            "high": float(parts[2]),
            "low": float(parts[3]),
            "close": float(parts[4]),
            "volume": float(parts[5]),
        }
    except (TypeError, ValueError):
        return None


def _load_candles(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    raw_lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not raw_lines:
        return rows
    first_line = raw_lines[0].strip().lower()
    headered = any(token in first_line for token in ["timestamp", "open,", "close,", "open_time"])
    if headered:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                parsed = _row_from_mapping(row)
                if parsed is not None:
                    rows.append(parsed)
    else:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            for parts in reader:
                parsed = _row_from_sequence(parts)
                if parsed is not None:
                    rows.append(parsed)
    rows.sort(key=lambda item: item["ts"])
    return rows


def _bucket_start(ts: datetime, minutes: int = 15) -> datetime:
    minute = (ts.minute // minutes) * minutes
    return ts.replace(minute=minute, second=0, microsecond=0)


def _contract_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[datetime, list[dict[str, Any]]] = {}
    for row in rows:
        buckets.setdefault(_bucket_start(row["ts"]), []).append(row)
    contracts: list[dict[str, Any]] = []
    for start in sorted(buckets):
        window = sorted(buckets[start], key=lambda item: item["ts"])
        if len(window) < 15:
            continue
        open_price = float(window[0]["open"])
        close_price = float(window[-1]["close"])
        contracts.append(
            {
                "contract_id": f"kxbtc15m-{start.strftime('%Y%m%d-%H%M')}",
                "open_ts": start.isoformat().replace("+00:00", "Z"),
                "close_ts": (start + timedelta(minutes=15)).isoformat().replace("+00:00", "Z"),
                "reference_price_open": open_price,
                "reference_price_close": close_price,
                "settlement_direction": "up" if close_price >= open_price else "down",
                "market_source": "derived_from_minute_candles",
            }
        )
    return contracts


def _dates(start: datetime, end: datetime) -> list[datetime]:
    days: list[datetime] = []
    current = start
    while current.date() <= end.date():
        days.append(current)
        current = current + timedelta(days=1)
    return days


def _download(url: str, path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, path)


def _extract(zip_path: Path, target_dir: Path) -> list[Path]:
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(target_dir)
    return sorted(target_dir.glob("*.csv"))


def _merge(csv_paths: list[Path], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        for path in csv_paths:
            with path.open("r", encoding="utf-8-sig", newline="") as source:
                for line in source:
                    handle.write(line)


def prepare_timeline_pack_dataset(pack_id: str, repo_root: Path | None = None, *, fetch_if_needed: bool = False) -> Path:
    root = repo_root or REPO_ROOT
    pack = _load_timeline_pack(pack_id)
    if not pack:
        raise SystemExit(f"Unknown pack_id: {pack_id}")

    start = _parse_date(pack.get("start_date", ""))
    end = _parse_date(pack.get("end_date", ""), end_of_day=True)
    if start is None or end is None:
        raise SystemExit(f"Invalid date range for pack_id: {pack_id}")

    coverage_status = str(pack.get("coverage_status", "")).strip()
    if coverage_status == "needs_data_extension" and fetch_if_needed:
        merged_csv = _fetch_archive_csv(pack_id, start, end, root)
        raw_rows = _load_candles(merged_csv)
        candle_rows = [
            {
                "ts": item["ts"].isoformat().replace("+00:00", "Z"),
                "open": item["open"],
                "high": item["high"],
                "low": item["low"],
                "close": item["close"],
                "volume": item["volume"],
            }
            for item in raw_rows
            if start <= item["ts"] <= end
        ]
        contract_rows = _contract_rows([item for item in raw_rows if start <= item["ts"] <= end])
        source_paths = {
            "candles": str(merged_csv.relative_to(root)),
            "contracts": "derived_from_fetched_minute_candles",
        }
        if merged_csv.parent.exists():
            shutil.rmtree(merged_csv.parent, ignore_errors=True)
    else:
        candle_source = root / "data" / "btc_1m_candles.jsonl"
        contract_source = root / "data" / "btc_up_down_15m_contracts.jsonl"
        if not candle_source.exists() or not contract_source.exists():
            raise SystemExit("Base BTC dataset missing. Expected data/btc_1m_candles.jsonl and data/btc_up_down_15m_contracts.jsonl.")

        candle_rows = []
        for line in candle_source.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            payload = json.loads(line)
            ts = _parse_ts(payload.get("ts", ""))
            if ts is None or ts < start or ts > end:
                continue
            candle_rows.append(payload)

        contract_rows = []
        for line in contract_source.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            payload = json.loads(line)
            open_ts = _parse_ts(payload.get("open_ts", ""))
            close_ts = _parse_ts(payload.get("close_ts", ""))
            if open_ts is None or close_ts is None:
                continue
            if open_ts < start or close_ts > end + timedelta(minutes=15):
                continue
            contract_rows.append(payload)
        source_paths = {
            "candles": str(candle_source.relative_to(root)),
            "contracts": str(contract_source.relative_to(root)),
        }

    target_root = root / "data" / "timeline-packs" / pack_id
    candle_target = target_root / "btc_1m_candles.jsonl"
    contract_target = target_root / "btc_up_down_15m_contracts.jsonl"
    metadata_target = target_root / "metadata.json"
    _write_jsonl(candle_target, candle_rows)
    _write_jsonl(contract_target, contract_rows)
    metadata = {
        "pack_id": pack_id,
        "regime_id": pack.get("regime_id"),
        "regime_label": pack.get("regime_label"),
        "window_id": pack.get("window_id"),
        "start_date": pack.get("start_date"),
        "end_date": pack.get("end_date"),
        "coverage_status": pack.get("coverage_status"),
        "candle_count": len(candle_rows),
        "contract_count": len(contract_rows),
        "source_paths": source_paths,
        "source_mode": "fetched_binance_archive" if coverage_status == "needs_data_extension" and fetch_if_needed else "base_dataset_slice",
    }
    metadata_target.parent.mkdir(parents=True, exist_ok=True)
    metadata_target.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    build_timeline_pack_validation(root)
    build_regime_match_review(root)
    build_pattern_regime_map(root)
    return target_root


def prepare_all_ready_timeline_packs(repo_root: Path | None = None, *, fetch_if_needed: bool = False) -> list[Path]:
    root = repo_root or REPO_ROOT
    payload = _load_json(root / "artifacts" / "research" / "timeline_packs.json", {})
    payload = payload if isinstance(payload, dict) else {}
    rows = payload.get("rows", [])
    rows = rows if isinstance(rows, list) else []
    written: list[Path] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        coverage_status = str(row.get("coverage_status", "")).strip()
        if coverage_status not in {"ready_for_dataset_extract", "needs_data_extension"}:
            continue
        if coverage_status == "needs_data_extension" and not fetch_if_needed:
            continue
        pack_id = str(row.get("pack_id", "")).strip()
        if not pack_id:
            continue
        written.append(prepare_timeline_pack_dataset(pack_id, root, fetch_if_needed=fetch_if_needed))
    return written


def main() -> None:
    parser = argparse.ArgumentParser(prog="prepare_timeline_pack_dataset")
    parser.add_argument("--pack-id")
    parser.add_argument("--all-ready", action="store_true")
    parser.add_argument("--fetch-if-needed", action="store_true")
    args = parser.parse_args()
    if args.all_ready:
        for path in prepare_all_ready_timeline_packs(REPO_ROOT, fetch_if_needed=args.fetch_if_needed):
            print(path)
        return
    if not args.pack_id:
        raise SystemExit("Pass --pack-id <pack_id> or --all-ready.")
    path = prepare_timeline_pack_dataset(args.pack_id, REPO_ROOT, fetch_if_needed=args.fetch_if_needed)
    print(path)


if __name__ == "__main__":
    main()
