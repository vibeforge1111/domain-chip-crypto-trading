from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from domain_chip_crypto_trading.cli import watchtower


def _load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def render_watchtower(repo_root: Path) -> list[Path]:
    ledger_path = repo_root / "artifacts" / "ledger" / "runs.jsonl"
    target_root = repo_root / "domain-chip-crypto-trading"
    rows = _load_rows(ledger_path)
    payload = {
        "summary": {"run_count": len(rows)},
        "ledger_rows": rows,
        "runtime_root": str(repo_root),
        "config_path": str(repo_root / "spark-researcher.project.json"),
    }
    response = watchtower(payload)
    pages = response.get("pages", [])
    written: list[Path] = []
    for page in pages:
        relative = Path(*str(page.get("path", "")).split("/"))
        path = target_root / relative
        content = str(page.get("content", ""))
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            sanitized = content.rstrip().replace("\x00", "") + "\n"
            path.write_text(sanitized, encoding="utf-8")
        except OSError:
            continue
        written.append(path)
    return written


def main() -> None:
    for path in render_watchtower(REPO_ROOT):
        print(path)


if __name__ == "__main__":
    main()
