from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _parse_ts(raw: str) -> datetime:
    value = str(raw).strip()
    if value.endswith("Z"):
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    if "T" in value:
        return datetime.fromisoformat(value).astimezone(timezone.utc)
    return datetime.fromisoformat(value + "T00:00:00+00:00").astimezone(timezone.utc)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def _filtered_candles(rows: list[dict[str, Any]], start: datetime, end: datetime) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    for row in rows:
        ts_raw = row.get("ts")
        if ts_raw in {None, ""}:
            continue
        ts = _parse_ts(str(ts_raw))
        if start <= ts < end:
            filtered.append(row)
    return filtered


def _filtered_contracts(rows: list[dict[str, Any]], start: datetime, end: datetime) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    for row in rows:
        open_raw = row.get("open_ts")
        close_raw = row.get("close_ts")
        if open_raw in {None, ""} or close_raw in {None, ""}:
            continue
        open_ts = _parse_ts(str(open_raw))
        close_ts = _parse_ts(str(close_raw))
        if start <= open_ts and close_ts <= end:
            filtered.append(row)
    return filtered


def main() -> None:
    parser = argparse.ArgumentParser(prog="prepare_paper_trade_dataset")
    parser.add_argument("--source-root", default="data")
    parser.add_argument("--output-root", default="data")
    parser.add_argument("--start", required=True, help="inclusive UTC date or timestamp")
    parser.add_argument("--end", required=True, help="exclusive UTC date or timestamp")
    args = parser.parse_args()

    source_root = Path(args.source_root)
    output_root = Path(args.output_root)
    candle_path = source_root / "btc_1m_candles.jsonl"
    contract_path = source_root / "btc_up_down_15m_contracts.jsonl"
    if not candle_path.exists() or not contract_path.exists():
        raise SystemExit("source benchmark dataset not found")

    start = _parse_ts(args.start)
    end = _parse_ts(args.end)
    if end <= start:
        raise SystemExit("--end must be after --start")

    candles = _filtered_candles(_load_jsonl(candle_path), start, end)
    contracts = _filtered_contracts(_load_jsonl(contract_path), start, end)
    if not candles or not contracts:
        raise SystemExit("no paper-trade rows found in requested window")

    paper_candle_path = output_root / "paper_trade_btc_1m_candles.jsonl"
    paper_contract_path = output_root / "paper_trade_btc_up_down_15m_contracts.jsonl"
    _write_jsonl(paper_candle_path, candles)
    _write_jsonl(paper_contract_path, contracts)
    print(paper_candle_path)
    print(paper_contract_path)


if __name__ == "__main__":
    main()
