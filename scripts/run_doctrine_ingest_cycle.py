from __future__ import annotations

import json
from pathlib import Path

from safe_write import safe_write_json
from run_learning_loop import run_learning_loop


REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    report = run_learning_loop()
    target_root = REPO_ROOT / "artifacts" / "research"
    target_root.mkdir(parents=True, exist_ok=True)
    path = target_root / "doctrine_ingest_cycle_report.json"
    safe_write_json(path, report)
    print(path)


if __name__ == "__main__":
    main()
