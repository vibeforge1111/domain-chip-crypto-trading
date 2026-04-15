"""Safe JSON file writing for Windows — avoids Errno 22 / PermissionError.

Usage:
    from safe_write import safe_write_json
    safe_write_json(path, payload)
"""
from __future__ import annotations

import json
import tempfile
import time
from pathlib import Path
from typing import Any


def safe_write_json(
    path: Path | str,
    data: Any,
    *,
    indent: int = 2,
    sort_keys: bool = True,
    trailing_newline: bool = True,
    default: Any = None,
) -> None:
    """Write JSON to *path* with retry logic for Windows file locking.

    Strategy:
    1. Try atomic temp-file-then-rename (fastest, safest).
    2. If rename fails (PermissionError — file locked by git/antivirus),
       retry direct write with short backoff.
    3. If all retries fail, raise the original error.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(data, indent=indent, sort_keys=sort_keys, default=default)
    if trailing_newline:
        content += "\n"

    # Attempt 1: atomic rename
    tmp_fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with open(tmp_fd, "w", encoding="utf-8") as f:
            f.write(content)
        Path(tmp_path).replace(path)
        return  # success
    except (PermissionError, OSError):
        Path(tmp_path).unlink(missing_ok=True)

    # Attempt 2-4: direct write with retry + backoff
    last_err: Exception | None = None
    for attempt in range(3):
        try:
            path.write_text(content, encoding="utf-8")
            return  # success
        except (PermissionError, OSError) as exc:
            last_err = exc
            time.sleep(0.2 * (attempt + 1))

    if last_err is not None:
        raise last_err
