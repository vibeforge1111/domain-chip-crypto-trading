from __future__ import annotations

import argparse
import urllib.request
import zipfile
from datetime import date, datetime, timedelta
from pathlib import Path


BASE_URL = "https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1m"


def _dates(start: date, end: date) -> list[date]:
    days: list[date] = []
    current = start
    while current <= end:
        days.append(current)
        current += timedelta(days=1)
    return days


def _download(url: str, path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, path)


def _extract(zip_path: Path, target_dir: Path) -> list[Path]:
    if target_dir.exists():
        for item in target_dir.glob("*"):
            if item.is_file():
                item.unlink()
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


def main() -> None:
    parser = argparse.ArgumentParser(prog="fetch_binance_1m_range")
    parser.add_argument("--start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="YYYY-MM-DD")
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--workdir", default="data/raw/binance")
    args = parser.parse_args()

    start = datetime.strptime(args.start, "%Y-%m-%d").date()
    end = datetime.strptime(args.end, "%Y-%m-%d").date()
    workdir = Path(args.workdir)
    zip_root = workdir / "zips"
    extract_root = workdir / "extracted"
    merged_inputs: list[Path] = []
    for current in _dates(start, end):
        stamp = current.strftime("%Y-%m-%d")
        zip_path = zip_root / f"BTCUSDT-1m-{stamp}.zip"
        url = f"{BASE_URL}/BTCUSDT-1m-{stamp}.zip"
        _download(url, zip_path)
        merged_inputs.extend(_extract(zip_path, extract_root / stamp))
    _merge(sorted(merged_inputs), Path(args.output_csv))
    print(args.output_csv)


if __name__ == "__main__":
    main()
