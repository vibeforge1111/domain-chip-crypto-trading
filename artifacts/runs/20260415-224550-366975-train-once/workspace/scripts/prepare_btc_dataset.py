from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def _parse_ts(raw: str) -> datetime:
    value = raw.strip()
    if value.endswith("Z"):
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    if "T" in value:
        return datetime.fromisoformat(value).astimezone(timezone.utc)
    numeric = float(value)
    while numeric > 10_000_000_000:
        numeric = numeric / 1000.0
    return datetime.fromtimestamp(numeric, tz=timezone.utc)


def _bucket_start(ts: datetime, minutes: int = 15) -> datetime:
    minute = (ts.minute // minutes) * minutes
    return ts.replace(minute=minute, second=0, microsecond=0)


def _row_from_mapping(row: dict[str, Any]) -> dict[str, Any] | None:
    ts_value = row.get("timestamp") or row.get("ts") or row.get("open_time")
    if ts_value in {None, ""}:
        return None
    try:
        return {
            "ts": _parse_ts(str(ts_value)),
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
    try:
        return {
            "ts": _parse_ts(parts[0]),
            "open": float(parts[1]),
            "high": float(parts[2]),
            "low": float(parts[3]),
            "close": float(parts[4]),
            "volume": float(parts[5]),
        }
    except (TypeError, ValueError):
        return None


def _load_candles(path: Path) -> list[dict]:
    rows: list[dict] = []
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


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def _candle_rows(rows: list[dict]) -> list[dict]:
    return [
        {
            "ts": item["ts"].isoformat().replace("+00:00", "Z"),
            "open": item["open"],
            "high": item["high"],
            "low": item["low"],
            "close": item["close"],
            "volume": item["volume"],
        }
        for item in rows
    ]


def _contract_rows(rows: list[dict]) -> list[dict]:
    buckets: dict[datetime, list[dict]] = defaultdict(list)
    for row in rows:
        buckets[_bucket_start(row["ts"])].append(row)
    contracts: list[dict] = []
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


def main() -> None:
    parser = argparse.ArgumentParser(prog="prepare_btc_dataset")
    parser.add_argument("--candles-csv", required=True)
    parser.add_argument("--output-root", default="data")
    args = parser.parse_args()
    raw_rows = _load_candles(Path(args.candles_csv))
    output_root = Path(args.output_root)
    candle_path = output_root / "btc_1m_candles.jsonl"
    contract_path = output_root / "btc_up_down_15m_contracts.jsonl"
    _write_jsonl(candle_path, _candle_rows(raw_rows))
    _write_jsonl(contract_path, _contract_rows(raw_rows))
    print(candle_path)
    print(contract_path)


if __name__ == "__main__":
    main()
