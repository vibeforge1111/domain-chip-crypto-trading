"""Refresh market data by fetching recent candles from Binance.

Supports multiple symbols (BTC, ETH, SOL) and generates contracts at
multiple timeframes (15m, 1h).

Fetches daily 1m candle ZIPs from Binance public data, converts them to the
JSONL format expected by the backtest engine, and regenerates contract windows.
"""
from __future__ import annotations

import json
import urllib.request
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from safe_write import safe_write_json

REPO_ROOT = Path(__file__).resolve().parents[1]
BINANCE_BASE = "https://data.binance.vision/data/spot/daily/klines"

SYMBOLS = [
    {"symbol": "BTCUSDT", "slug": "btc"},
    {"symbol": "ETHUSDT", "slug": "eth"},
    {"symbol": "SOLUSDT", "slug": "sol"},
]

CONTRACT_TIMEFRAMES = [
    {"minutes": 15, "label": "15m", "min_candles": 15},
    {"minutes": 60, "label": "1h", "min_candles": 55},
]


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _latest_candle_ts(candle_path: Path) -> date | None:
    """Read the last line of the candle JSONL to find the most recent timestamp."""
    if not candle_path.exists():
        return None
    last_line = ""
    with candle_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                last_line = line.strip()
    if not last_line:
        return None
    try:
        row = json.loads(last_line)
        ts_raw = str(row.get("ts", ""))
        dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).astimezone(timezone.utc)
        return dt.date()
    except (json.JSONDecodeError, ValueError, KeyError):
        return None


def _dates_to_fetch(last_date: date | None, days_back: int = 3) -> list[date]:
    """Return dates that need fetching.  Start from day after last candle
    or from days_back days ago if no existing data."""
    today = date.today()
    # Binance publishes with ~1 day lag
    available_through = today - timedelta(days=1)

    if last_date is not None:
        start = last_date + timedelta(days=1)
    else:
        start = today - timedelta(days=days_back)

    days: list[date] = []
    current = start
    while current <= available_through:
        days.append(current)
        current += timedelta(days=1)
    return days


def _download_zip(symbol: str, day: date, workdir: Path) -> Path | None:
    """Download a single daily ZIP from Binance.  Returns path or None on failure."""
    stamp = day.strftime("%Y-%m-%d")
    zip_path = workdir / "zips" / f"{symbol}-1m-{stamp}.zip"
    if zip_path.exists():
        return zip_path
    url = f"{BINANCE_BASE}/{symbol}/1m/{symbol}-1m-{stamp}.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(url, zip_path)
        return zip_path
    except Exception:
        if zip_path.exists():
            zip_path.unlink()
        return None


def _parse_csv_row(parts: list[str]) -> dict[str, Any] | None:
    """Parse a single row from Binance kline CSV (no header)."""
    if len(parts) < 6:
        return None
    try:
        ts_ms = float(parts[0])
        while ts_ms > 10_000_000_000:
            ts_ms /= 1000.0
        dt = datetime.fromtimestamp(ts_ms, tz=timezone.utc)
        return {
            "ts": dt.isoformat().replace("+00:00", "Z"),
            "open": float(parts[1]),
            "high": float(parts[2]),
            "low": float(parts[3]),
            "close": float(parts[4]),
            "volume": float(parts[5]),
        }
    except (ValueError, TypeError):
        return None


def _extract_and_append(zip_path: Path, candle_path: Path) -> int:
    """Extract candles from ZIP and append to the JSONL file.  Returns count of new rows."""
    count = 0
    extract_dir = zip_path.parent.parent / "extracted" / zip_path.stem
    extract_dir.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_dir)
    except zipfile.BadZipFile:
        return 0

    candle_path.parent.mkdir(parents=True, exist_ok=True)
    with candle_path.open("a", encoding="utf-8") as out:
        for csv_path in sorted(extract_dir.glob("*.csv")):
            with csv_path.open("r", encoding="utf-8-sig") as src:
                import csv as csv_mod
                for parts in csv_mod.reader(src):
                    row = _parse_csv_row(parts)
                    if row is not None:
                        out.write(json.dumps(row, sort_keys=True) + "\n")
                        count += 1
    return count


def _bucket_start(ts: datetime, minutes: int = 15) -> datetime:
    minute = (ts.minute // minutes) * minutes
    return ts.replace(minute=minute, second=0, microsecond=0)


def _rebuild_contracts(candle_path: Path, contract_path: Path, *, slug: str = "btc", minutes: int = 15, label: str = "15m", min_candles: int = 15) -> int:
    """Rebuild the full contract windows file from candles.  Returns count."""
    from collections import defaultdict

    buckets: dict[datetime, list[dict]] = defaultdict(list)
    with candle_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts_raw = str(row.get("ts", ""))
            try:
                dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).astimezone(timezone.utc)
            except ValueError:
                continue
            buckets[_bucket_start(dt, minutes)].append(row | {"_dt": dt})

    contracts: list[dict] = []
    for start in sorted(buckets):
        window = sorted(buckets[start], key=lambda r: r["_dt"])
        if len(window) < min_candles:
            continue
        open_price = float(window[0]["open"])
        close_price = float(window[-1]["close"])
        contracts.append({
            "contract_id": f"kx{slug}{label}-{start.strftime('%Y%m%d-%H%M')}",
            "open_ts": start.isoformat().replace("+00:00", "Z"),
            "close_ts": (start + timedelta(minutes=minutes)).isoformat().replace("+00:00", "Z"),
            "reference_price_open": open_price,
            "reference_price_close": close_price,
            "settlement_direction": "up" if close_price >= open_price else "down",
        })

    contract_path.parent.mkdir(parents=True, exist_ok=True)
    with contract_path.open("w", encoding="utf-8") as handle:
        for row in contracts:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    return len(contracts)


def _refresh_symbol(symbol: str, slug: str, data_root: Path, workdir: Path, *, max_days: int = 7) -> dict[str, Any]:
    """Fetch and refresh data for a single symbol."""
    candle_path = data_root / f"{slug}_1m_candles.jsonl"

    last_date = _latest_candle_ts(candle_path)
    days = _dates_to_fetch(last_date, days_back=max_days)

    fetched_days: list[str] = []
    failed_days: list[str] = []
    total_new_candles = 0

    for day in days:
        zip_path = _download_zip(symbol, day, workdir)
        if zip_path is None:
            failed_days.append(day.isoformat())
            continue
        count = _extract_and_append(zip_path, candle_path)
        if count > 0:
            fetched_days.append(day.isoformat())
            total_new_candles += count
        else:
            failed_days.append(day.isoformat())

    contract_counts: dict[str, int] = {}
    if total_new_candles > 0 or not last_date:
        for tf in CONTRACT_TIMEFRAMES:
            contract_path = data_root / f"{slug}_up_down_{tf['label']}_contracts.jsonl"
            if candle_path.exists():
                count = _rebuild_contracts(
                    candle_path, contract_path,
                    slug=slug, minutes=tf["minutes"],
                    label=tf["label"], min_candles=tf["min_candles"],
                )
                contract_counts[tf["label"]] = count

    return {
        "symbol": symbol,
        "slug": slug,
        "last_existing_date": last_date.isoformat() if last_date else None,
        "days_requested": len(days),
        "days_fetched": len(fetched_days),
        "days_failed": len(failed_days),
        "fetched_days": fetched_days,
        "failed_days": failed_days,
        "new_candle_count": total_new_candles,
        "contract_counts": contract_counts,
        "material_change": total_new_candles > 0,
    }


def refresh_market_data(repo_root: Path, *, max_days: int = 7, symbols: list[str] | None = None) -> dict[str, Any]:
    """Fetch recent Binance data and refresh the backtest dataset.

    Returns a report dict describing what was fetched.
    """
    data_root = repo_root / "data"
    workdir = data_root / "raw" / "binance"

    allowed_slugs = set(s.lower() for s in symbols) if symbols else None
    symbol_reports: list[dict[str, Any]] = []
    total_new_candles = 0

    for sym in SYMBOLS:
        if allowed_slugs and sym["slug"] not in allowed_slugs:
            continue
        report = _refresh_symbol(sym["symbol"], sym["slug"], data_root, workdir, max_days=max_days)
        symbol_reports.append(report)
        total_new_candles += report["new_candle_count"]

    report = {
        "refreshed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "symbols_refreshed": [r["slug"] for r in symbol_reports],
        "symbol_reports": symbol_reports,
        "total_new_candles": total_new_candles,
        "material_change": total_new_candles > 0,
    }

    report_path = repo_root / "artifacts" / "data" / "refresh_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    safe_write_json(report_path, report)
    return report


def main() -> None:
    report = refresh_market_data(REPO_ROOT)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
