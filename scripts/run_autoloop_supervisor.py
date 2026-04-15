from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from run_backtest_loop import run_backtest_loop
from run_learning_loop import run_learning_loop
from run_paper_trade_cycle import run_paper_trade_loop
from refresh_market_data import refresh_market_data
from prepare_paper_trade_dataset import _load_jsonl, _parse_ts, _filtered_candles, _filtered_contracts, _write_jsonl
from paper_trade_monitor import run_paper_trade_monitor
from track_paper_trade_history import track_paper_trade_history
from safe_write import safe_write_json


REPO_ROOT = Path(__file__).resolve().parents[1]

PAPER_TRADE_LOOKBACK_DAYS = 30


PAPER_TRADE_ASSETS = ["btc", "eth", "sol"]
PAPER_TRADE_TIMEFRAMES = ["15m", "1h"]


def _refresh_paper_trade_dataset() -> bool:
    """Regenerate paper trade datasets using the last PAPER_TRADE_LOOKBACK_DAYS of data."""
    data_root = REPO_ROOT / "data"
    any_refreshed = False
    try:
        end = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        start = end - timedelta(days=PAPER_TRADE_LOOKBACK_DAYS)
        for asset in PAPER_TRADE_ASSETS:
            candle_path = data_root / f"{asset}_1m_candles.jsonl"
            if not candle_path.exists():
                continue
            candles = _filtered_candles(_load_jsonl(candle_path), start, end)
            if not candles:
                continue
            _write_jsonl(data_root / f"paper_trade_{asset}_1m_candles.jsonl", candles)
            for tf in PAPER_TRADE_TIMEFRAMES:
                contract_path = data_root / f"{asset}_up_down_{tf}_contracts.jsonl"
                if not contract_path.exists():
                    continue
                contracts = _filtered_contracts(_load_jsonl(contract_path), start, end)
                if contracts:
                    _write_jsonl(data_root / f"paper_trade_{asset}_up_down_{tf}_contracts.jsonl", contracts)
                    any_refreshed = True
    except Exception:
        pass
    return any_refreshed


DEFAULT_POLICY = {
    "sleep_seconds": 300,
    "max_cycles": 0,
    "max_noop_streak": 8,
    "stop_on_dirty_tracked_worktree": True,
    "commit_if_material_change": True,
    "ignored_paths": [
        ".obsidian",
        "artifacts/recursion/autoloop_state.json",
        "artifacts/recursion/cycle_journal.jsonl",
    ],
    "loops": {
        "learning": {
            "enabled": True,
            "every_n_cycles": 6,
            "trigger_pending_packets": True,
        },
        "backtest": {
            "enabled": True,
            "every_n_cycles": 1,
            "trigger_pending_variety": True,
        },
        "paper_trade": {
            "enabled": True,
            "every_n_cycles": 1,
            "trigger_queue_presence": True,
        },
    },
}


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _write_json(path: Path, payload: Any) -> None:
    safe_write_json(path, payload)


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def _policy() -> dict[str, Any]:
    path = REPO_ROOT / "docs" / "recursion" / "autoloop-policy.json"
    data = _load_json(path, {})
    if not isinstance(data, dict):
        return dict(DEFAULT_POLICY)
    merged = dict(DEFAULT_POLICY)
    merged.update({key: value for key, value in data.items() if key != "loops"})
    loops = json.loads(json.dumps(DEFAULT_POLICY["loops"]))
    raw_loops = data.get("loops", {})
    if isinstance(raw_loops, dict):
        for loop_name, loop_policy in raw_loops.items():
            if loop_name in loops and isinstance(loop_policy, dict):
                loops[loop_name].update(loop_policy)
    research_ingest = data.get("research_ingest")
    if isinstance(research_ingest, dict):
        loops["learning"]["enabled"] = bool(research_ingest.get("enabled", True))
        loops["learning"]["every_n_cycles"] = int(research_ingest.get("every_n_cycles", 6) or 6)
        loops["learning"]["trigger_pending_packets"] = True
    merged["loops"] = loops
    return merged


def _tracked_status_lines() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.rstrip() for line in result.stdout.splitlines() if line.strip()]


def _ignored(path: str, ignored_paths: list[str]) -> bool:
    normalized = path.replace("\\", "/").strip()
    for item in ignored_paths:
        candidate = str(item).replace("\\", "/").strip().rstrip("/")
        if not candidate:
            continue
        if normalized == candidate or normalized.startswith(candidate + "/"):
            return True
    return False


_WINDOWS_RESERVED = {"con", "prn", "aux", "nul", "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9", "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9"}


def _normalize_status_path(raw: str) -> str:
    path = raw.strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1].strip()
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]
    basename = path.rsplit("/", 1)[-1].rsplit("\\", 1)[-1].split(".")[0].lower()
    if basename in _WINDOWS_RESERVED:
        return ""
    return path


def _dirty_tracked_paths(ignored_paths: list[str]) -> list[str]:
    paths: list[str] = []
    for line in _tracked_status_lines():
        status = line[:2]
        path = _normalize_status_path(line[3:])
        if status == "??":
            continue
        if _ignored(path, ignored_paths):
            continue
        paths.append(path)
    return paths


def _relevant_status_paths(ignored_paths: list[str]) -> list[str]:
    paths: list[str] = []
    for line in _tracked_status_lines():
        path = _normalize_status_path(line[3:])
        if not path or _ignored(path, ignored_paths):
            continue
        paths.append(path)
    deduped: list[str] = []
    for path in paths:
        if path not in deduped:
            deduped.append(path)
    return deduped


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _pending_packet_count() -> int:
    card_root = REPO_ROOT / "docs" / "doctrine-cards"
    packet_root = REPO_ROOT / "docs" / "doctrine-packets"
    card_ids = set()
    packet_ids = set()
    for path in sorted(card_root.glob("*.json")):
        payload = _load_json(path, {})
        if isinstance(payload, dict) and str(payload.get("card_id", "")).strip():
            card_ids.add(str(payload.get("card_id", "")).strip())
    for path in sorted(packet_root.glob("*.json")):
        payload = _load_json(path, {})
        if not isinstance(payload, dict):
            continue
        if str(payload.get("packet_status", "")).strip() != "ready_for_card_ingest":
            continue
        if str(payload.get("card_id", "")).strip():
            packet_ids.add(str(payload.get("card_id", "")).strip())
    return len(packet_ids - card_ids)


def _paper_trade_queue_count() -> int:
    queue = _load_json(REPO_ROOT / "artifacts" / "paper_trade" / "paper_trade_queue.json", {})
    queue_count = int(queue.get("queue_count", 0) or 0) if isinstance(queue, dict) else 0
    if queue_count > 0:
        return queue_count
    summary = _load_json(REPO_ROOT / "artifacts" / "paper_trade" / "paper_trade_summary.json", {})
    return int(summary.get("queue_count", 0) or 0) if isinstance(summary, dict) else 0


def _contradiction_probe_count() -> int:
    probes = _load_json(REPO_ROOT / "artifacts" / "recursion" / "contradiction_probes.json", [])
    probes = probes if isinstance(probes, list) else []
    return len([p for p in probes if isinstance(p, dict) and float(p.get("priority", 0) or 0) >= 0.3])


def _pending_variety_count() -> int:
    rows = _load_json(REPO_ROOT / "artifacts" / "recursion" / "variety_backlog.json", [])
    rows = rows if isinstance(rows, list) else []
    return sum(
        int(item.get("pending_proposal_count", 0) or 0) + int(item.get("suggested_child_target_count", 0) or 0)
        for item in rows
        if isinstance(item, dict)
    )


def _loop_due(loop_name: str, state: dict[str, Any], policy: dict[str, Any], cycle_number: int, disabled_loops: set[str]) -> bool:
    if loop_name in disabled_loops:
        return False
    loop_policy = policy.get("loops", {}).get(loop_name, {})
    if not isinstance(loop_policy, dict) or not bool(loop_policy.get("enabled", True)):
        return False
    every_n = max(1, int(loop_policy.get("every_n_cycles", 1) or 1))
    last_cycle = int(state.get(f"last_{loop_name}_cycle", 0) or 0)
    if loop_name == "learning" and bool(loop_policy.get("trigger_pending_packets", True)) and last_cycle > 0 and _pending_packet_count() <= 0 and _contradiction_probe_count() <= 0:
        return False
    if loop_name == "backtest" and bool(loop_policy.get("trigger_pending_variety", True)) and last_cycle > 0 and _pending_variety_count() <= 0:
        return False
    if loop_name == "paper_trade" and bool(loop_policy.get("trigger_queue_presence", True)) and last_cycle > 0 and _paper_trade_queue_count() <= 0:
        return False
    if last_cycle <= 0 or cycle_number - last_cycle >= every_n:
        return True
    if loop_name == "learning" and bool(loop_policy.get("trigger_pending_packets", True)) and (_pending_packet_count() > 0 or _contradiction_probe_count() > 0):
        return True
    if loop_name == "backtest" and bool(loop_policy.get("trigger_pending_variety", True)) and _pending_variety_count() > 0:
        return True
    if loop_name == "paper_trade" and bool(loop_policy.get("trigger_queue_presence", True)) and _paper_trade_queue_count() > 0:
        return True
    return False


def _stage_paths(paths: list[str]) -> None:
    if not paths:
        return
    # Batch to avoid Windows command-line length limit (WinError 206)
    batch_size = 40
    for i in range(0, len(paths), batch_size):
        batch = paths[i : i + batch_size]
        subprocess.run(["git", "add", "-f", "--", *batch], cwd=REPO_ROOT, check=True)


def _commit_message(cycle_number: int, loop_reports: dict[str, dict[str, Any]]) -> str:
    learning = loop_reports.get("learning", {})
    backtest = loop_reports.get("backtest", {})
    paper_trade = loop_reports.get("paper_trade", {})
    added_count = int(learning.get("after", {}).get("added_count", 0) or 0)
    if added_count > 0:
        return f"Tri-loop cycle {cycle_number}: ingest {added_count} cards"
    benchmark = backtest.get("after", {}).get("benchmark", {}) if isinstance(backtest.get("after"), dict) else {}
    top_candidate_id = str(benchmark.get("top_candidate_id", "") or "")
    if top_candidate_id:
        return f"Tri-loop cycle {cycle_number}: backtest {top_candidate_id}"
    paper_after = paper_trade.get("after", {}) if isinstance(paper_trade.get("after"), dict) else {}
    queue_count = int(paper_after.get("queue_count", 0) or 0)
    return f"Tri-loop cycle {cycle_number}: paper-trade q{queue_count}"


def _maybe_commit(cycle_number: int, loop_reports: dict[str, dict[str, Any]], policy: dict[str, Any]) -> str | None:
    paths = _relevant_status_paths(list(policy.get("ignored_paths", [])))
    if not paths:
        return None
    _stage_paths(paths)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_ROOT)
    if staged.returncode == 0:
        return None
    message = _commit_message(cycle_number, loop_reports)
    subprocess.run(["git", "commit", "-m", message], cwd=REPO_ROOT, check=True)
    return message


def _state_path() -> Path:
    return REPO_ROOT / "artifacts" / "recursion" / "autoloop_state.json"


def _journal_path() -> Path:
    return REPO_ROOT / "artifacts" / "recursion" / "cycle_journal.jsonl"


def _state() -> dict[str, Any]:
    data = _load_json(_state_path(), {})
    return data if isinstance(data, dict) else {}


def _persist_state(payload: dict[str, Any]) -> None:
    _write_json(_state_path(), payload)


def _loop_summary(loop_name: str, report: dict[str, Any]) -> dict[str, Any]:
    after = report.get("after", {})
    after = after if isinstance(after, dict) else {}
    summary = {
        "ran": bool(report),
        "material_change": bool(report.get("material_change")),
        "material_reasons": report.get("material_reasons", []),
    }
    if loop_name == "learning":
        summary["added_count"] = int(after.get("added_count", 0) or 0)
        summary["pending_packet_count"] = int(after.get("pending_packet_count", 0) or 0)
    elif loop_name == "backtest":
        benchmark = after.get("benchmark", {}) if isinstance(after.get("benchmark"), dict) else {}
        summary["top_candidate_id"] = benchmark.get("top_candidate_id")
        summary["top_recommended_next_step"] = benchmark.get("top_recommended_next_step")
    elif loop_name == "paper_trade":
        summary["queue_count"] = int(after.get("queue_count", 0) or 0)
        summary["executed_candidate_count"] = int(after.get("executed_candidate_count", 0) or 0)
        summary["top_recommendation"] = after.get("top_recommendation")
    return summary


def _maybe_promote_candidates(repo_root: Path, monitor_report: dict[str, Any]) -> int:
    """Promote paper-trade-ready candidates to proven_champions.json."""
    candidates = monitor_report.get("candidates", [])
    ready = [c for c in candidates if c.get("readiness") == "ready_for_promotion_review"]
    if not ready:
        return 0

    champions_path = repo_root / "artifacts" / "forge" / "proven_champions.json"
    champions_data = json.loads(champions_path.read_text(encoding="utf-8")) if champions_path.exists() else {"champions": []}
    existing_ids = {ch.get("candidate_id", "") for ch in champions_data.get("champions", [])}

    # Load project config for mutations lookup
    config_path = repo_root / "spark-researcher.project.json"
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    mutations_by_id = {}
    for trial in config.get("candidate_trials", []):
        mutations_by_id[trial.get("candidate_id", "")] = trial.get("mutations", {})

    promoted = 0
    for c in ready:
        cid = c.get("candidate_id", "")
        if cid in existing_ids or not cid:
            continue
        mutations = mutations_by_id.get(cid, {})
        strategy_id = mutations.get("strategy_id", "unknown")
        champion_entry = {
            "champion_id": cid,
            "candidate_id": cid,
            "family": strategy_id,
            "asset": mutations.get("asset_universe", "BTC"),
            "backtest_wr": 0,
            "backtest_trades": 0,
            "backtest_dd": 0,
            "backtest_sharpe": 0,
            "paper_wr": c.get("win_rate", 0),
            "paper_trades": c.get("trade_count", 0),
            "paper_dd": c.get("max_drawdown", 1.0),
            "wf": 0,
            "mechanism": f"Paper-trade promoted ({c.get('win_rate', 0):.3f} WR, {c.get('trade_count', 0)} trades)",
            "promoted_from": "paper_trade",
            "promoted_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "mutations": mutations,
        }
        champions_data["champions"].append(champion_entry)
        existing_ids.add(cid)
        promoted += 1

    if promoted > 0:
        champions_data["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        safe_write_json(champions_path, champions_data)

    return promoted


def _run_supervisor_cycle(cycle_number: int, state: dict[str, Any], policy: dict[str, Any], *, no_commit: bool, disabled_loops: set[str]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    ignored_paths = list(policy.get("ignored_paths", []))
    dirty_paths = _dirty_tracked_paths(ignored_paths)
    if dirty_paths and not no_commit:
        # Auto-commit leftover dirty files from previous cycle instead of crashing
        _stage_paths(dirty_paths)
        staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO_ROOT)
        if staged.returncode != 0:
            subprocess.run(["git", "commit", "-m", f"Tri-loop cycle {cycle_number}: commit leftover artifacts"], cwd=REPO_ROOT, check=True)
    elif dirty_paths and no_commit:
        raise RuntimeError(f"tracked worktree is dirty: {', '.join(dirty_paths)}")

    head_before = _git_head()
    loop_reports: dict[str, dict[str, Any]] = {}
    loops_run: list[str] = []

    data_refresh_due = "data_refresh" not in disabled_loops and (int(state.get("last_data_refresh_cycle", 0) or 0) <= 0 or cycle_number - int(state.get("last_data_refresh_cycle", 0) or 0) >= 6)
    if data_refresh_due:
        try:
            refresh_report = refresh_market_data(REPO_ROOT, max_days=3)
            loop_reports["data_refresh"] = refresh_report
            loops_run.append("data_refresh")
        except Exception:
            pass

    # Always refresh paper trade datasets so the latest data is available
    try:
        _refresh_paper_trade_dataset()
    except Exception:
        pass

    if _loop_due("learning", state, policy, cycle_number, disabled_loops):
        loop_reports["learning"] = run_learning_loop()
        loops_run.append("learning")
    learning_added_cards = int(loop_reports.get("learning", {}).get("after", {}).get("added_count", 0) or 0) > 0
    if learning_added_cards or _loop_due("backtest", state, policy, cycle_number, disabled_loops):
        loop_reports["backtest"] = run_backtest_loop(commit_if_material_change=False, persist_report_on_noop=False)
        loops_run.append("backtest")
    if _paper_trade_queue_count() > 0 or _loop_due("paper_trade", state, policy, cycle_number, disabled_loops):
        loop_reports["paper_trade"] = run_paper_trade_loop()
        loops_run.append("paper_trade")
        try:
            track_paper_trade_history(REPO_ROOT)
            monitor_report = run_paper_trade_monitor(REPO_ROOT)
            loop_reports["paper_trade_monitor"] = monitor_report
            promotion_count = _maybe_promote_candidates(REPO_ROOT, monitor_report)
            if promotion_count > 0:
                loop_reports["promotions"] = {"count": promotion_count}
        except Exception:
            pass

    commit_message = None
    if not no_commit and bool(policy.get("commit_if_material_change", True)):
        commit_message = _maybe_commit(cycle_number, loop_reports, policy)
    head_after = _git_head()
    journal_entry = {
        "cycle_number": cycle_number,
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "loops_run": loops_run,
        "learning": _loop_summary("learning", loop_reports.get("learning", {})) if "learning" in loop_reports else {"ran": False},
        "backtest": _loop_summary("backtest", loop_reports.get("backtest", {})) if "backtest" in loop_reports else {"ran": False},
        "paper_trade": _loop_summary("paper_trade", loop_reports.get("paper_trade", {})) if "paper_trade" in loop_reports else {"ran": False},
        "pending_packet_count": _pending_packet_count(),
        "pending_variety_count": _pending_variety_count(),
        "paper_trade_queue_count": _paper_trade_queue_count(),
        "paper_trade_monitor": {
            "significant": int(loop_reports.get("paper_trade_monitor", {}).get("statistically_significant_count", 0) or 0),
            "promotion_ready": int(loop_reports.get("paper_trade_monitor", {}).get("promotion_ready_count", 0) or 0),
            "promoted": int(loop_reports.get("promotions", {}).get("count", 0) or 0),
        } if "paper_trade_monitor" in loop_reports else None,
        "commit_message": commit_message,
        "git_head_before": head_before,
        "git_head_after": head_after,
    }
    journal_entry["material_change"] = any(
        bool(loop_reports.get(loop_name, {}).get("material_change")) for loop_name in loop_reports
    )
    journal_entry["finished_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return journal_entry, loop_reports


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the bounded crypto tri-loop supervisor in the foreground.")
    parser.add_argument("--max-cycles", type=int, default=None, help="Override the max supervisor cycle count. Use 0 for infinite.")
    parser.add_argument("--sleep-seconds", type=int, default=None, help="Override the sleep between supervisor cycles.")
    parser.add_argument("--no-commit", action="store_true", help="Never commit from the supervisor run.")
    parser.add_argument("--disable-learning-loop", action="store_true", help="Skip the learning loop.")
    parser.add_argument("--disable-backtest-loop", action="store_true", help="Skip the backtest loop.")
    parser.add_argument("--disable-paper-trade-loop", action="store_true", help="Skip the paper-trade loop.")
    parser.add_argument("--disable-doctrine-ingest", action="store_true", help="Compatibility alias for --disable-learning-loop.")
    args = parser.parse_args()

    policy = _policy()
    if args.max_cycles is not None:
        policy["max_cycles"] = args.max_cycles
    if args.sleep_seconds is not None:
        policy["sleep_seconds"] = args.sleep_seconds

    state = _state()
    cycle_number = int(state.get("cycle_count", 0) or 0)
    noop_streak = int(state.get("noop_streak", 0) or 0)
    max_cycles = int(policy.get("max_cycles", 0) or 0)
    max_noop_streak = max(1, int(policy.get("max_noop_streak", 8) or 8))
    sleep_seconds = max(0, int(policy.get("sleep_seconds", 300) or 300))
    executed_cycles = 0
    disabled_loops = {
        loop_name
        for loop_name, disabled in {
            "learning": args.disable_learning_loop or args.disable_doctrine_ingest,
            "backtest": args.disable_backtest_loop,
            "paper_trade": args.disable_paper_trade_loop,
        }.items()
        if disabled
    }

    try:
        while max_cycles <= 0 or executed_cycles < max_cycles:
            cycle_number += 1
            executed_cycles += 1
            journal_entry, loop_reports = _run_supervisor_cycle(
                cycle_number,
                state,
                policy,
                no_commit=args.no_commit,
                disabled_loops=disabled_loops,
            )
            _append_jsonl(_journal_path(), journal_entry)
            material_change = bool(journal_entry.get("material_change"))
            noop_streak = 0 if material_change else noop_streak + 1
            state = {
                "cycle_count": cycle_number,
                "noop_streak": noop_streak,
                "last_cycle_started_at": journal_entry.get("started_at"),
                "last_cycle_finished_at": journal_entry.get("finished_at"),
                "last_commit_message": journal_entry.get("commit_message"),
                "last_material_change": material_change,
                "last_learning_cycle": cycle_number if journal_entry.get("learning", {}).get("ran") else int(state.get("last_learning_cycle", 0) or 0),
                "last_backtest_cycle": cycle_number if journal_entry.get("backtest", {}).get("ran") else int(state.get("last_backtest_cycle", 0) or 0),
                "last_paper_trade_cycle": cycle_number if journal_entry.get("paper_trade", {}).get("ran") else int(state.get("last_paper_trade_cycle", 0) or 0),
                "last_data_refresh_cycle": cycle_number if "data_refresh" in journal_entry.get("loops_run", []) else int(state.get("last_data_refresh_cycle", 0) or 0),
                "pending_packet_count": journal_entry.get("pending_packet_count"),
                "paper_trade_queue_count": journal_entry.get("paper_trade_queue_count"),
                "last_top_candidate_id": journal_entry.get("backtest", {}).get("top_candidate_id"),
            }
            _persist_state(state)
            print(json.dumps(journal_entry, indent=2, sort_keys=True))

            if noop_streak >= max_noop_streak and int(journal_entry.get("pending_packet_count", 0) or 0) <= 0 and int(journal_entry.get("paper_trade_queue_count", 0) or 0) <= 0:
                break
            if max_cycles > 0 and executed_cycles >= max_cycles:
                break
            time.sleep(sleep_seconds)
    except KeyboardInterrupt:
        interrupted = {
            "cycle_count": cycle_number,
            "noop_streak": noop_streak,
            "interrupted_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "interrupted",
        }
        _persist_state({**state, **interrupted})
        print(json.dumps(interrupted, indent=2, sort_keys=True))
    except RuntimeError as error:
        blocked = {
            "cycle_count": cycle_number,
            "noop_streak": noop_streak,
            "blocked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "status": "blocked",
            "reason": str(error),
        }
        _persist_state({**state, **blocked})
        print(json.dumps(blocked, indent=2, sort_keys=True))
        raise


if __name__ == "__main__":
    main()
