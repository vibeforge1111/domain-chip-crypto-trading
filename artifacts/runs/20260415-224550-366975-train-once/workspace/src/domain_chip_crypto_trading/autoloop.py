from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
AUTOLOOP_ROOT = REPO_ROOT / "autoloop"
CONTROL_PLANE_PATH = AUTOLOOP_ROOT / "control-plane.json"
DOC_PATH = REPO_ROOT / "docs" / "CRYPTO_TRADING_AUTOLOOP.md"
MANIFEST_PATH = REPO_ROOT / "docs" / "recursion" / "autoloop-manifest.json"
POLICY_PATH = REPO_ROOT / "docs" / "recursion" / "autoloop-policy.json"
STATE_PATH = REPO_ROOT / "artifacts" / "recursion" / "autoloop_state.json"
JOURNAL_PATH = REPO_ROOT / "artifacts" / "recursion" / "cycle_journal.jsonl"
VAULT_ROOT = REPO_ROOT / "domain-chip-crypto-trading" / "07-Domains" / "Crypto Trading"

SCRIPT_MAP = {
    "status": "describe_autoloop.py",
    "supervisor": "run_autoloop_supervisor.py",
    "learning": "run_learning_loop.py",
    "backtest": "run_backtest_loop.py",
    "paper-trade": "run_paper_trade_cycle.py",
    "watchtower": "build_watchtower.py",
}

WINDOWS_RESERVED = {
    "con",
    "prn",
    "aux",
    "nul",
    "com1",
    "com2",
    "com3",
    "com4",
    "com5",
    "com6",
    "com7",
    "com8",
    "com9",
    "lpt1",
    "lpt2",
    "lpt3",
    "lpt4",
    "lpt5",
    "lpt6",
    "lpt7",
    "lpt8",
    "lpt9",
}


def _script_path(name: str) -> Path:
    return REPO_ROOT / "scripts" / SCRIPT_MAP[name]


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _policy() -> dict[str, Any]:
    data = _load_json(POLICY_PATH, {})
    return data if isinstance(data, dict) else {}


def _ignored(path: str, ignored_paths: list[str]) -> bool:
    normalized = path.replace("\\", "/").strip()
    for item in ignored_paths:
        candidate = str(item).replace("\\", "/").strip().rstrip("/")
        if not candidate:
            continue
        if normalized == candidate or normalized.startswith(candidate + "/"):
            return True
    return False


def _normalize_status_path(raw: str) -> str:
    path = raw.strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1].strip()
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
    basename = path.rsplit("/", 1)[-1].rsplit("\\", 1)[-1].split(".")[0].lower()
    if basename in WINDOWS_RESERVED:
        return ""
    return path


def _git_status_lines() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.rstrip() for line in result.stdout.splitlines() if line.strip()]


def _path_bucket(path: str) -> str:
    normalized = path.replace("\\", "/").strip("/")
    parts = [part for part in normalized.split("/") if part]
    if not parts:
        return "root"
    if len(parts) == 1:
        return parts[0]
    return "/".join(parts[:2])


def _doctor_summary(limit: int) -> dict[str, Any]:
    ignored_paths = list(_policy().get("ignored_paths", []))
    tracked_paths: list[str] = []
    untracked_paths: list[str] = []
    for line in _git_status_lines():
        status = line[:2]
        path = _normalize_status_path(line[3:])
        if not path:
            continue
        if status == "??":
            untracked_paths.append(path)
            continue
        if _ignored(path, ignored_paths):
            continue
        tracked_paths.append(path)

    tracked_buckets = Counter(_path_bucket(path) for path in tracked_paths)
    untracked_buckets = Counter(_path_bucket(path) for path in untracked_paths)
    state = _load_json(STATE_PATH, {})
    return {
        "blocked": bool(tracked_paths),
        "status": state.get("status", "unknown") if isinstance(state, dict) else "unknown",
        "dirty_tracked_count": len(tracked_paths),
        "dirty_untracked_count": len(untracked_paths),
        "top_tracked_buckets": [
            {"path": bucket, "count": count}
            for bucket, count in tracked_buckets.most_common(limit)
        ],
        "top_untracked_buckets": [
            {"path": bucket, "count": count}
            for bucket, count in untracked_buckets.most_common(limit)
        ],
        "tracked_samples": tracked_paths[:limit],
        "untracked_samples": untracked_paths[:limit],
        "ignored_paths": ignored_paths,
        "recommendation": (
            "Supervisor is blocked by tracked changes. Commit or intentionally clear tracked artifacts before running the loop."
            if tracked_paths
            else "No tracked-worktree blockage detected for the Autoloop."
        ),
    }


def _render_doctor(summary: dict[str, Any]) -> str:
    lines = [
        "Crypto Trading Autoloop Doctor",
        f"- blocked: {summary['blocked']}",
        f"- supervisor_status: {summary['status']}",
        f"- dirty_tracked_count: {summary['dirty_tracked_count']}",
        f"- dirty_untracked_count: {summary['dirty_untracked_count']}",
        "",
        "Top tracked buckets:",
    ]
    tracked_buckets = summary.get("top_tracked_buckets", [])
    if not tracked_buckets:
        lines.append("- none")
    for item in tracked_buckets:
        lines.append(f"- {item['path']}: {item['count']}")
    lines.extend(["", "Tracked samples:"])
    tracked_samples = summary.get("tracked_samples", [])
    if not tracked_samples:
        lines.append("- none")
    for item in tracked_samples:
        lines.append(f"- {item}")
    lines.extend(["", "Top untracked buckets:"])
    untracked_buckets = summary.get("top_untracked_buckets", [])
    if not untracked_buckets:
        lines.append("- none")
    for item in untracked_buckets:
        lines.append(f"- {item['path']}: {item['count']}")
    lines.extend(["", f"Recommendation: {summary['recommendation']}"])
    return "\n".join(lines)


def _run_python_script(script: Path, args: list[str]) -> int:
    result = subprocess.run([sys.executable, str(script), *args], cwd=REPO_ROOT)
    return int(result.returncode)


def _print_json(path: Path) -> int:
    payload = _load_json(path, None)
    if payload is None:
        print(f"Missing file: {path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _print_paths() -> int:
    lines = [
        "Crypto Trading Autoloop Paths",
        f"- autoloop_root: {AUTOLOOP_ROOT.relative_to(REPO_ROOT)}",
        f"- control_plane: {CONTROL_PLANE_PATH.relative_to(REPO_ROOT)}",
        f"- operator_doc: {DOC_PATH.relative_to(REPO_ROOT)}",
        f"- manifest: {MANIFEST_PATH.relative_to(REPO_ROOT)}",
        f"- policy: {POLICY_PATH.relative_to(REPO_ROOT)}",
        f"- state: {STATE_PATH.relative_to(REPO_ROOT)}",
        f"- journal: {JOURNAL_PATH.relative_to(REPO_ROOT)}",
        f"- vault_root: {VAULT_ROOT.relative_to(REPO_ROOT)}",
        f"- status_script: {_script_path('status').relative_to(REPO_ROOT)}",
        f"- supervisor_script: {_script_path('supervisor').relative_to(REPO_ROOT)}",
    ]
    print("\n".join(lines))
    return 0


def _print_control_plane() -> int:
    return _print_json(CONTROL_PLANE_PATH)


def _run_status(json_mode: bool) -> int:
    args = ["--format", "json" if json_mode else "text"]
    return _run_python_script(_script_path("status"), args)


def _run_watchtower() -> int:
    return _run_python_script(_script_path("watchtower"), [])


def _run_lane(lane: str) -> int:
    return _run_python_script(_script_path(lane), [])


def _run_supervisor_from_args(args: argparse.Namespace, *, once: bool) -> int:
    script_args: list[str] = []
    if once:
        script_args.extend(["--max-cycles", "1", "--sleep-seconds", "0"])
    elif args.max_cycles is not None:
        script_args.extend(["--max-cycles", str(args.max_cycles)])
    if not once and args.sleep_seconds is not None:
        script_args.extend(["--sleep-seconds", str(args.sleep_seconds)])
    if args.no_commit:
        script_args.append("--no-commit")
    if args.disable_learning:
        script_args.append("--disable-learning-loop")
    if args.disable_backtest:
        script_args.append("--disable-backtest-loop")
    if args.disable_paper_trade:
        script_args.append("--disable-paper-trade-loop")
    return _run_python_script(_script_path("supervisor"), script_args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crypto-autoloop",
        description="Operator shell for the crypto-trading Autoloop.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="Show the current Autoloop status.")
    status_parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")

    doctor_parser = subparsers.add_parser("doctor", help="Summarize the dirty-worktree blocker.")
    doctor_parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    doctor_parser.add_argument("--limit", type=int, default=10, help="Limit bucket and sample output.")

    subparsers.add_parser("paths", help="Show the main Autoloop file landmarks.")
    subparsers.add_parser("control-plane", help="Print the operator control-plane JSON.")
    subparsers.add_parser("manifest", help="Print the Autoloop manifest JSON.")
    subparsers.add_parser("policy", help="Print the Autoloop policy JSON.")
    subparsers.add_parser("watchtower", help="Refresh the crypto-trading watchtower vault.")

    lane_parser = subparsers.add_parser("lane", help="Run one Autoloop lane directly.")
    lane_parser.add_argument(
        "lane",
        choices=["learning", "backtest", "paper-trade"],
        help="Lane to run.",
    )

    run_parser = subparsers.add_parser("run", help="Run the foreground Autoloop supervisor.")
    run_parser.add_argument("--max-cycles", type=int, default=None, help="Override supervisor cycle count.")
    run_parser.add_argument("--sleep-seconds", type=int, default=None, help="Override supervisor sleep.")
    run_parser.add_argument("--no-commit", action="store_true", help="Never commit from this run.")
    run_parser.add_argument("--disable-learning", action="store_true", help="Skip the learning lane.")
    run_parser.add_argument("--disable-backtest", action="store_true", help="Skip the backtest lane.")
    run_parser.add_argument("--disable-paper-trade", action="store_true", help="Skip the paper-trade lane.")

    run_once_parser = subparsers.add_parser("run-once", help="Run one bounded supervisor cycle.")
    run_once_parser.add_argument("--no-commit", action="store_true", help="Never commit from this run.")
    run_once_parser.add_argument("--disable-learning", action="store_true", help="Skip the learning lane.")
    run_once_parser.add_argument("--disable-backtest", action="store_true", help="Skip the backtest lane.")
    run_once_parser.add_argument("--disable-paper-trade", action="store_true", help="Skip the paper-trade lane.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "status":
        return _run_status(args.json)
    if args.command == "doctor":
        summary = _doctor_summary(max(1, int(args.limit or 10)))
        if args.json:
            print(json.dumps(summary, indent=2, sort_keys=True))
            return 0
        print(_render_doctor(summary))
        return 0
    if args.command == "paths":
        return _print_paths()
    if args.command == "control-plane":
        return _print_control_plane()
    if args.command == "manifest":
        return _print_json(MANIFEST_PATH)
    if args.command == "policy":
        return _print_json(POLICY_PATH)
    if args.command == "watchtower":
        return _run_watchtower()
    if args.command == "lane":
        return _run_lane(args.lane)
    if args.command == "run":
        return _run_supervisor_from_args(args, once=False)
    if args.command == "run-once":
        return _run_supervisor_from_args(args, once=True)
    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
