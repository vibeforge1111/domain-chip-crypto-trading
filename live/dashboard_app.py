"""
Spark Domain Chip: Crypto Trading - Real-Time Monitor
================================================
shadcn/ui-inspired dark dashboard with live auto-refresh.

Run:  python dashboard_app.py
Open: http://localhost:8502
"""

import json
import glob
import math
import os
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone, timedelta

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

BASE = Path(__file__).parent
ARCHIVE = BASE / "archive"
GENERATIONS = ARCHIVE / "generations"
META = ARCHIVE / "meta_improvements"
DIAG = ARCHIVE / "self_diagnosis"

app = FastAPI(title="Spark Domain Chip: Crypto Trading API")


# ── helpers ──────────────────────────────────────────────────────────────
def _json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def _jsonl_tail(path, n=200):
    try:
        lines = []
        with open(path) as f:
            for line in f:
                s = line.strip()
                if s:
                    lines.append(s)
        return [json.loads(l) for l in lines[-n:]]
    except Exception:
        return []


def _latest_reports(n=100):
    reps = sorted(glob.glob(str(GENERATIONS / "report_*.json")))
    out = []
    for p in reps[-n:]:
        try:
            with open(p) as f:
                out.append(json.load(f))
        except Exception:
            pass
    return out


# ── API routes ───────────────────────────────────────────────────────────
@app.get("/api/status")
def api_status():
    reports = sorted(glob.glob(str(GENERATIONS / "report_*.json")))
    if not reports:
        return {"generation": 0}
    r = _json(reports[-1])
    ps = r.get("population_summary", {})
    se = r.get("strategy_effectiveness", {})
    return {
        "generation": r.get("generation", 0),
        "best_wr": ps.get("best_wr", 0),
        "avg_wr": ps.get("avg_wr", 0),
        "elite": ps.get("elite", 0),
        "viable": ps.get("viable", 0),
        "total": ps.get("size", 0),
        "new_elite": r.get("new_elite", 0),
        "new_viable": r.get("new_viable", 0),
        "elapsed": r.get("elapsed_seconds", 0),
        "methods": {
            k: {
                "attempts": v.get("attempts", 0),
                "improvements": v.get("improvements", 0),
                "rate": v.get("improvement_rate", 0),
                "avg_wr": v.get("avg_wr", 0),
                "best_wr": v.get("best_wr", 0),
            }
            for k, v in se.items()
        },
    }


@app.get("/api/recent-elites")
def api_recent_elites():
    entries = _jsonl_tail(META / "performance_log.jsonl", 500)
    elites = []
    for e in reversed(entries):
        f = e.get("fitness", {})
        if f.get("elite"):
            m = e.get("mutations", {})
            elites.append({
                "gen": e.get("generation", 0),
                "agent": e.get("agent_id", "?")[:8],
                "strategy": e.get("meta_strategy", "?"),
                "strat_id": m.get("strategy_id", "?"),
                "wr": f.get("win_rate", 0),
                "wf": f.get("wealth_factor", 0),
                "trades": f.get("trade_count", 0),
                "ts": e.get("timestamp", ""),
                "tf": m.get("timeframe", "?"),
                "asset": m.get("asset_universe", "?"),
            })
            if len(elites) >= 15:
                break
    return elites


@app.get("/api/population-history")
def api_pop_history():
    reps = _latest_reports(120)
    return [
        {
            "gen": r.get("generation", 0),
            "elite": r.get("population_summary", {}).get("elite", 0),
            "viable": r.get("population_summary", {}).get("viable", 0),
            "total": r.get("population_summary", {}).get("size", 0),
            "new_elite": r.get("new_elite", 0),
        }
        for r in reps
    ]


def _pt_lookup():
    """Build agent_id[:8] -> latest paper trade data from history."""
    entries = _jsonl_tail(ARCHIVE / "paper_trade_history.jsonl", 500)
    lookup = {}
    for entry in entries:
        for a in entry.get("agents", []):
            aid = a.get("agent_id", "")[:8]
            if aid:
                lookup[aid] = {
                    "pt_wr": a.get("paper_trade_wr", 0),
                    "pt_trades": a.get("trades", 0),
                    "pt_delta": a.get("delta", 0),
                    "pt_gen": entry.get("generation", 0),
                }
    return lookup


# ── perf log cache (avoids re-reading 85MB file every refresh) ───────────
_perf_cache = {"mtime": 0, "data": []}


def _get_perf_log(n=2000):
    """Read last n entries from performance_log.jsonl with mtime caching."""
    path = META / "performance_log.jsonl"
    try:
        mt = path.stat().st_mtime
    except Exception:
        return []
    if mt == _perf_cache["mtime"] and len(_perf_cache["data"]) >= n:
        return _perf_cache["data"][-n:]
    data = _jsonl_tail(path, n)
    _perf_cache.update(mtime=mt, data=data)
    return data[-n:]


@app.get("/api/paper-trade")
def api_paper_trade():
    """Detailed paper trade data: current results + history timeline."""
    # Current detailed results
    data = _json(ARCHIVE / "paper_trade_results.json")
    current = []
    if isinstance(data, list):
        for d in data:
            details = d.get("paper_trade_details", {})
            regime_stats = details.get("regime_stats", {})
            current.append({
                "agent": d.get("agent_id", "?")[:8],
                "bt_wr": d.get("backtest_wr", 0),
                "pt_wr": d.get("paper_trade_wr", 0),
                "delta": d.get("delta", 0),
                "trades": d.get("paper_trade_trades", 0),
                "validation": d.get("validation", "?"),
                "readiness": d.get("paper_trade_readiness", 0),
                "recommendation": details.get("paper_trade_recommendation", ""),
                "sharpe": details.get("sharpe_ratio", 0),
                "max_drawdown": details.get("max_drawdown", 0),
                "regimes": {k: {"trades": v.get("trades", 0), "wr": v.get("win_rate", 0)}
                            for k, v in regime_stats.items()},
                "boundary": details.get("boundary", ""),
            })

    # History timeline (last 50 entries for charting)
    history_raw = _jsonl_tail(ARCHIVE / "paper_trade_history.jsonl", 50)
    history = []
    for entry in history_raw:
        gen = entry.get("generation", 0)
        for a in entry.get("agents", []):
            history.append({
                "gen": gen,
                "agent": a.get("agent_id", "")[:8],
                "bt_wr": a.get("backtest_wr", 0),
                "pt_wr": a.get("paper_trade_wr", 0),
                "delta": a.get("delta", 0),
                "trades": a.get("trades", 0),
                "ts": entry.get("timestamp", ""),
            })

    # Summary stats
    all_history = _jsonl_tail(ARCHIVE / "paper_trade_history.jsonl", 500)
    unique_agents = set()
    total_runs = 0
    all_deltas = []
    for entry in all_history:
        for a in entry.get("agents", []):
            unique_agents.add(a.get("agent_id", "")[:8])
            total_runs += 1
            all_deltas.append(a.get("delta", 0))
    avg_delta = sum(all_deltas) / len(all_deltas) if all_deltas else 0
    positive_pct = sum(1 for d in all_deltas if d >= 0) / len(all_deltas) if all_deltas else 0

    return {
        "current": current,
        "history": history,
        "summary": {
            "unique_agents": len(unique_agents),
            "total_runs": total_runs,
            "avg_delta": round(avg_delta, 4),
            "positive_pct": round(positive_pct, 4),
            "total_entries": len(all_history),
        },
    }


@app.get("/api/pt-dashboard")
def api_pt_dashboard():
    """Enhanced PT data: daemon status, coverage, leaderboard, scatter.

    Aggregates across multiple PT daemons (pt_state.json, pt_state_1h.json,
    pt_state_15m.json, pt_state_4h.json) for full coverage view.
    """
    # Discover all pt_state files (supports parallel daemons per timeframe)
    state_files = sorted(ARCHIVE.glob("pt_state*.json"))
    if not state_files:
        return {
            "daemon": {"status": "not_started", "cycles": 0, "interval": 0},
            "coverage": {"total_elite": 0, "tested_agents": 0, "coverage_pct": 0},
            "status_counts": {"needs_more_data": 0, "validated": 0, "live_ready": 0},
            "leaderboard": [],
            "scatter": [],
            "daemons": [],
        }

    # Merge agent indexes from all state files
    idx = {}
    daemons = []
    total_cycles = 0
    latest_update = ""
    total_elite = 0

    for sf in state_files:
        state = _json(sf)
        if not state:
            continue
        # Merge agent index (later files overwrite if same agent appears)
        for aid, data in state.get("agent_pt_index", {}).items():
            if aid not in idx or data.get("pt_score", 0) > idx[aid].get("pt_score", 0):
                idx[aid] = data

        cycles = state.get("cycle_count", 0)
        total_cycles += cycles
        cov = state.get("coverage", {})
        total_elite = max(total_elite, cov.get("total_elite", 0))

        ts = state.get("last_updated", "")
        if ts > latest_update:
            latest_update = ts

        # Track each daemon's info
        tf_label = sf.stem.replace("pt_state_", "").replace("pt_state", "all")
        daemons.append({
            "timeframe": tf_label,
            "status": state.get("daemon_status", "unknown"),
            "cycles": cycles,
            "tested": cov.get("tested_agents", 0),
        })

    # Status counts
    status_counts = {"needs_more_data": 0, "validated": 0, "live_ready": 0}
    for data in idx.values():
        s = data.get("status", "needs_more_data")
        if s in status_counts:
            status_counts[s] += 1

    tested_count = len(idx)
    coverage = {
        "total_elite": total_elite,
        "tested_agents": tested_count,
        "coverage_pct": round(tested_count / max(1, total_elite), 4),
    }

    # Top 20 leaderboard by PT score
    leaderboard = sorted(
        [
            {
                "agent": aid[:8],
                "bt_wr": data.get("bt_wr", 0),
                "pt_wr_avg": data.get("pt_wr_avg", 0),
                "pt_wr_std": round(data.get("pt_wr_std", 0), 4),
                "pt_delta_avg": data.get("pt_delta_avg", 0),
                "pt_score": data.get("pt_score", 0),
                "bt_trades": data.get("bt_trades", 0),
                "pt_trades_total": data.get("pt_trades_total", 0),
                "run_count": data.get("run_count", 0),
                "status": data.get("status", "needs_more_data"),
                "meta_strategy": data.get("meta_strategy", ""),
                "asset": data.get("asset", "?"),
                "timeframe": data.get("timeframe", "?"),
                "strategy": data.get("strategy", "?"),
            }
            for aid, data in idx.items()
        ],
        key=lambda x: x.get("pt_score", 0),
        reverse=True,
    )[:20]

    # BT vs PT scatter data
    scatter = [
        {
            "agent": aid[:8],
            "bt_wr": data.get("bt_wr", 0),
            "pt_wr": data.get("pt_wr_avg", 0),
            "trades": data.get("pt_trades_total", 0),
            "status": data.get("status", "unknown"),
        }
        for aid, data in idx.items()
        if data.get("run_count", 0) >= 1
    ]

    # Find most recent daemon status for the header
    running_count = sum(1 for d in daemons if d["status"] == "running")
    daemon_status = "running" if running_count > 0 else "stopped"

    return {
        "daemon": {
            "status": daemon_status,
            "pid": None,
            "cycles": total_cycles,
            "interval": 90,
            "last_updated": latest_update,
            "active_daemons": running_count,
            "daemon_count": len(daemons),
        },
        "coverage": coverage,
        "status_counts": status_counts,
        "leaderboard": leaderboard,
        "scatter": scatter,
        "daemons": daemons,
    }


@app.get("/api/health")
def api_health():
    b = _json(DIAG / "bias_analysis.json")
    h = b.get("backtest_holdout_correlation", {})
    w = b.get("walk_forward_bias", {})
    return {
        "mae": h.get("mean_absolute_error", 0),
        "bias": h.get("systematic_bias", 0),
        "bias_dir": h.get("bias_direction", "?"),
        "pass_rate": h.get("holdout_pass_rate", 0),
        "temporal": w.get("temporal_bias", 0),
        "bias_type": w.get("bias_type", "?"),
        "ts": b.get("timestamp", ""),
    }


@app.get("/api/live-pt")
def api_live_pt():
    """Live paper trading state + settlement history with period stats."""
    state = _json(ARCHIVE / "live_pt_state.json")
    log_path = ARCHIVE / "live_pt_log.jsonl"
    all_settlements = _jsonl_tail(log_path, 500)

    now = datetime.utcnow().isoformat()
    day_ago = (datetime.utcnow() - timedelta(hours=24)).isoformat()
    week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()

    def _compute_stats(entries):
        trades = 0; wins = 0; skips = 0
        strategy_stats = {}
        for e in entries:
            for aid, a in (e.get("agents") or {}).items():
                strat = a.get("strategy", "?")
                if strat not in strategy_stats:
                    strategy_stats[strat] = {"trades": 0, "wins": 0, "skips": 0}
                if a.get("prediction") == "skip":
                    skips += 1
                    strategy_stats[strat]["skips"] += 1
                else:
                    trades += 1
                    strategy_stats[strat]["trades"] += 1
                    if a.get("correct"):
                        wins += 1
                        strategy_stats[strat]["wins"] += 1
        return {
            "trades": trades, "wins": wins, "losses": trades - wins,
            "skips": skips,
            "accuracy": round(wins / trades * 100, 1) if trades else 0,
            "settlements": len(entries),
            "strategy_stats": strategy_stats,
        }

    daily = [e for e in all_settlements if e.get("ts", "") >= day_ago]
    weekly = [e for e in all_settlements if e.get("ts", "") >= week_ago]

    return {
        "status": state.get("status", "stopped"),
        "started_at": state.get("started_at", ""),
        "assets": state.get("assets", []),
        "agents_loaded": state.get("agents_loaded", 0),
        "strategies_loaded": state.get("strategies_loaded", 0),
        "total_settlements": state.get("total_settlements", 0),
        "current_contracts": state.get("current_contracts", {}),
        "agent_stats": state.get("agent_stats", {}),
        "strategies": state.get("strategies", {}),
        "regime_history": state.get("regime_history", [])[-20:],
        "last_updated": state.get("last_updated", ""),
        "period_stats": {
            "daily": _compute_stats(daily),
            "weekly": _compute_stats(weekly),
            "alltime": _compute_stats(all_settlements),
        },
        "recent_settlements": all_settlements[-30:],
    }


@app.get("/api/insights")
def api_insights():
    data = _json(META / "synthesized_insights.json")
    if not isinstance(data, list):
        return []
    out = []
    for i in data:
        out.append({
            "text": i.get("insight", ""),
            "type": i.get("type", ""),
            "validated": i.get("times_validated", 0),
            "confidence": i.get("confidence", 0),
            "delta": i.get("evidence", {}).get("delta", 0),
            "gen": i.get("generation_discovered", 0),
        })
    out.sort(key=lambda x: x["validated"], reverse=True)
    return out[:10]


@app.get("/api/top-agents")
def api_top_agents(period: str = Query("all")):
    """Return top agents filtered by time period: session, today, week, all."""
    # Determine how many lines to read based on period
    n = {"session": 2000, "today": 5000, "week": 10000, "all": 20000}.get(period, 20000)
    entries = _jsonl_tail(META / "performance_log.jsonl", n)

    # Time filter
    now = datetime.now(timezone.utc)
    if period == "session":
        # Find the latest generation, assume session started ~500 gens ago
        if entries:
            max_gen = max(e.get("generation", 0) for e in entries)
            cutoff_gen = max_gen - 500
            entries = [e for e in entries if e.get("generation", 0) >= cutoff_gen]
    elif period == "today":
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        entries = [e for e in entries if _parse_ts(e.get("timestamp", "")) >= today_start]
    elif period == "week":
        week_start = now - timedelta(days=7)
        entries = [e for e in entries if _parse_ts(e.get("timestamp", "")) >= week_start]

    # Load paper trade lookup
    pt = _pt_lookup()

    # Filter elite only and build result
    agents = []
    for e in entries:
        f = e.get("fitness", {})
        if not f.get("elite"):
            continue
        m = e.get("mutations", {})
        # Count walk-forward segments passed
        wf_stats = f.get("walk_forward_stats", [])
        wf_passed = sum(1 for s in wf_stats if s.get("trade_count_gate_pass")) if wf_stats else 0
        wf_total = len(wf_stats) if wf_stats else 5
        # Key guards (non-strategy mutations)
        skip_keys = {"strategy_id", "doctrine_id", "asset_universe", "timeframe", "extend_regimes",
                     "activation_profile", "compression_profile", "no_trade_window",
                     "volume_context_guard", "counter_trend_guard", "llm_guard_id"}
        guards = {k: v for k, v in m.items() if k not in skip_keys}
        top_guards = list(guards.items())[:4]

        aid = e.get("agent_id", "?")[:8]
        pt_data = pt.get(aid, {})
        agents.append({
            "agent": aid,
            "gen": e.get("generation", 0),
            "method": e.get("meta_strategy", "?"),
            "strategy": m.get("strategy_id", "?"),
            "asset": m.get("asset_universe", "?"),
            "tf": m.get("timeframe", "?"),
            "wr": f.get("win_rate", 0),
            "wf": f.get("wealth_factor", 0),
            "trades": f.get("trade_count", 0),
            "sharpe": f.get("sharpe_ratio", 0),
            "drawdown": f.get("max_drawdown", 0),
            "validation": f"{wf_passed}/{wf_total}",
            "guards": top_guards,
            "ts": e.get("timestamp", ""),
            "pt_wr": pt_data.get("pt_wr"),
            "pt_trades": pt_data.get("pt_trades"),
            "pt_delta": pt_data.get("pt_delta"),
        })

    # Sort by win rate descending
    agents.sort(key=lambda x: x["wr"], reverse=True)
    return {"agents": agents, "total": len(agents)}


# ── activity feed + strategy diversity + evolution graph ─────────────────

_GUARD_SKIP_KEYS = {
    "strategy_id", "doctrine_id", "asset_universe", "timeframe", "extend_regimes",
    "activation_profile", "compression_profile", "no_trade_window",
    "volume_context_guard", "counter_trend_guard", "llm_guard_id", "market_regime",
}


@app.get("/api/activity-feed")
def api_activity_feed(n: int = Query(80, le=200)):
    """Return last N agent evaluations from performance log, newest first."""
    entries = _get_perf_log(n)
    result = []
    for e in reversed(entries[-n:]):
        m = e.get("mutations", {})
        f = e.get("fitness", {})
        guards = [f"{k}={v}" for k, v in m.items()
                  if k not in _GUARD_SKIP_KEYS and v]
        status = "elite" if f.get("elite") else ("viable" if f.get("viable") else "reject")
        result.append({
            "agent": e.get("agent_id", "?")[:8],
            "gen": e.get("generation", 0),
            "meta_strategy": e.get("meta_strategy", "?"),
            "parent": (e.get("parent_id") or "")[:8],
            "strategy": m.get("strategy_id", "?"),
            "asset": m.get("asset_universe", "?"),
            "tf": m.get("timeframe", "?"),
            "wr": round(f.get("win_rate", 0), 4),
            "wf": round(f.get("wealth_factor", 0), 2),
            "trades": f.get("trade_count", 0),
            "status": status,
            "eval_stage": f.get("eval_stage", "full"),
            "improved": e.get("improved", False),
            "guards": guards[:6],
            "ts": e.get("timestamp", ""),
        })
    return {"entries": result}


@app.get("/api/strategy-diversity")
def api_strategy_diversity():
    """Return strategy distribution, diversity index, and mutation activity."""
    entries = _get_perf_log(2000)
    strat_stats = {}
    recent = entries[-100:] if len(entries) >= 100 else entries

    guard_added = Counter()
    guard_removed = Counter()

    for e in entries:
        m = e.get("mutations", {})
        f = e.get("fitness", {})
        sid = m.get("strategy_id", "unknown")
        if sid not in strat_stats:
            strat_stats[sid] = {"count": 0, "wr_sum": 0, "best_wr": 0,
                                "elite": 0, "viable": 0, "recent": 0}
        s = strat_stats[sid]
        s["count"] += 1
        wr = f.get("win_rate", 0)
        s["wr_sum"] += wr
        s["best_wr"] = max(s["best_wr"], wr)
        if f.get("elite"):
            s["elite"] += 1
        if f.get("viable"):
            s["viable"] += 1

    for e in recent:
        m = e.get("mutations", {})
        sid = m.get("strategy_id", "unknown")
        if sid in strat_stats:
            strat_stats[sid]["recent"] += 1
        for k, v in m.items():
            if k in _GUARD_SKIP_KEYS:
                continue
            if v == "" or v is None:
                guard_removed[k] += 1
            else:
                guard_added[k] += 1

    total = max(sum(s["count"] for s in strat_stats.values()), 1)
    probs = [s["count"] / total for s in strat_stats.values() if s["count"] > 0]
    entropy = -sum(p * math.log(p) for p in probs if p > 0)
    max_ent = math.log(len(probs)) if len(probs) > 1 else 1
    diversity = round(entropy / max_ent, 4) if max_ent > 0 else 0

    strategies = {}
    for sid, s in sorted(strat_stats.items(), key=lambda x: x[1]["count"], reverse=True):
        strategies[sid] = {
            "count": s["count"],
            "pct": round(s["count"] / total, 4),
            "avg_wr": round(s["wr_sum"] / max(s["count"], 1), 4),
            "best_wr": round(s["best_wr"], 4),
            "elite_count": s["elite"],
            "recent_births": s["recent"],
        }

    return {
        "strategies": strategies,
        "total_agents": total,
        "diversity_index": diversity,
        "mutation_activity": {
            "most_added": guard_added.most_common(8),
            "most_removed": guard_removed.most_common(8),
        },
    }


@app.get("/api/evolution-graph")
def api_evolution_graph(
    gen_start: int = Query(None),
    gen_end: int = Query(None),
    min_wr: float = Query(0.0),
    strategy: str = Query(""),
):
    """Return nodes + edges for evolution visualization, capped at 2000 nodes."""
    # Determine latest gen
    reports = sorted(glob.glob(str(GENERATIONS / "report_*.json")))
    latest_gen = 0
    if reports:
        try:
            latest_gen = int(Path(reports[-1]).stem.split("_")[-1])
        except Exception:
            pass

    if gen_end is None:
        gen_end = latest_gen
    if gen_start is None:
        gen_start = max(0, gen_end - 100)

    est_lines = max(2000, (gen_end - gen_start + 1) * 15)
    entries = _get_perf_log(est_lines)

    filtered = []
    for e in entries:
        g = e.get("generation", 0)
        if g < gen_start or g > gen_end:
            continue
        f = e.get("fitness", {})
        if f.get("win_rate", 0) < min_wr:
            continue
        m = e.get("mutations", {})
        sid = m.get("strategy_id", "")
        if strategy and sid != strategy:
            continue
        filtered.append(e)

    if len(filtered) > 2000:
        filtered.sort(key=lambda x: x.get("fitness", {}).get("win_rate", 0), reverse=True)
        filtered = filtered[:2000]

    node_ids = set()
    nodes = []
    for e in filtered:
        aid = e.get("agent_id", "")[:8]
        node_ids.add(aid)
        m = e.get("mutations", {})
        f = e.get("fitness", {})
        nodes.append({
            "id": aid,
            "gen": e.get("generation", 0),
            "wr": round(f.get("win_rate", 0), 4),
            "wf": round(f.get("wealth_factor", 0), 2),
            "trades": f.get("trade_count", 0),
            "strategy": m.get("strategy_id", "?"),
            "asset": m.get("asset_universe", "?"),
            "tf": m.get("timeframe", "?"),
            "meta_strategy": e.get("meta_strategy", "?"),
            "elite": f.get("elite", False),
            "viable": f.get("viable", False),
            "improved": e.get("improved", False),
        })

    edges = []
    for e in filtered:
        pid = (e.get("parent_id") or "")[:8]
        aid = e.get("agent_id", "")[:8]
        if pid and pid in node_ids and aid in node_ids and pid != aid:
            edges.append({"source": pid, "target": aid})

    strategies_list = sorted(set(n["strategy"] for n in nodes))

    return {
        "nodes": nodes,
        "edges": edges,
        "gen_range": [gen_start, gen_end],
        "node_count": len(nodes),
        "edge_count": len(edges),
        "strategies": strategies_list,
    }


def _parse_ts(ts_str):
    """Parse ISO timestamp, return min datetime on failure."""
    try:
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except Exception:
        return datetime.min.replace(tzinfo=timezone.utc)


# ── Autoloop API (tri-loop: learning + backtest + paper trade) ────────────
REPO_ROOT = BASE.parent
ARTIFACTS = REPO_ROOT / "artifacts"
RESEARCH = ARTIFACTS / "research"
RECURSION = ARTIFACTS / "recursion"
BACKTESTS = ARTIFACTS / "backtests"
PAPER_TRADE_DIR = ARTIFACTS / "paper_trade"
DOCTRINE_CARDS_DIR = REPO_ROOT / "docs" / "doctrine-cards"
DOCTRINE_PACKETS_DIR = REPO_ROOT / "docs" / "doctrine-packets"


@app.get("/api/autoloop-status")
def api_autoloop_status():
    """Tri-loop autoloop state: cycle count, lane status, candidates."""
    state = _json(RECURSION / "autoloop_state.json")
    journal_path = RECURSION / "cycle_journal.jsonl"
    recent_cycles = _jsonl_tail(journal_path, 20)

    # Doctrine cards
    cards = []
    if DOCTRINE_CARDS_DIR.exists():
        for f in sorted(DOCTRINE_CARDS_DIR.glob("*.json")):
            try:
                cards.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                pass

    # Doctrine packets
    packets = []
    if DOCTRINE_PACKETS_DIR.exists():
        for f in sorted(DOCTRINE_PACKETS_DIR.glob("*.json")):
            try:
                packets.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                pass

    # Backtest summary
    bt_summary = _json(BACKTESTS / "heavy_backtest_summary.json")
    bt_report = _json(BACKTESTS / "backtest_loop_report.json")

    # Paper trade queue
    pt_queue = _json(PAPER_TRADE_DIR / "paper_trade_queue.json")
    pt_monitor = _json(PAPER_TRADE_DIR / "paper_trade_monitor_report.json")

    # Variety backlog
    variety = _json(RECURSION / "variety_backlog.json")
    variety_count = len(variety) if isinstance(variety, list) else variety.get("count", 0)

    # Mutation trials
    trials = _json(RECURSION / "mutation_trials.json")
    trial_count = len(trials.get("trials", [])) if isinstance(trials, dict) else 0

    # Build cycle timeline for chart
    cycle_timeline = []
    for c in recent_cycles:
        entry = {"cycle": c.get("cycle_number", 0)}
        for lane in ["learning", "backtest", "paper_trade"]:
            lane_data = c.get(lane, {})
            entry[lane] = lane_data.get("material_change", False)
        entry["material"] = c.get("material_change", False)
        cycle_timeline.append(entry)

    # Top candidates from backtest
    candidates = []
    if isinstance(bt_summary, dict):
        for cid, cdata in list(bt_summary.items())[:20]:
            if isinstance(cdata, dict):
                candidates.append({
                    "id": cid[:50],
                    "wr": cdata.get("win_rate", 0),
                    "wf": cdata.get("walk_forward_consistency", 0),
                    "dd": cdata.get("max_drawdown", 0),
                    "trades": cdata.get("trade_count", 0),
                    "sharpe": cdata.get("sharpe_ratio", 0),
                    "readiness": cdata.get("paper_trade_readiness", 0),
                    "stress": cdata.get("stress_resilience", 0),
                    "next_step": cdata.get("recommended_next_step", ""),
                })
    candidates.sort(key=lambda x: x.get("wr", 0), reverse=True)

    return {
        "state": {
            "status": state.get("status", "unknown"),
            "cycle_count": state.get("cycle_count", 0),
            "last_finished": state.get("last_cycle_finished_at", ""),
            "last_material": state.get("last_material_change", False),
            "noop_streak": state.get("noop_streak", 0),
            "top_candidate": state.get("last_top_candidate_id", ""),
            "blocked_at": state.get("blocked_at"),
            "reason": state.get("reason"),
        },
        "doctrine": {
            "card_count": len(cards),
            "packet_count": len(packets),
            "recent_cards": [
                {"id": c.get("card_id", c.get("id", "?")),
                 "doctrine": c.get("doctrine_family", c.get("doctrine_id", "?")),
                 "strategy": c.get("strategy_family", c.get("strategy_id", "?")),
                 "regime": c.get("mutation_template", {}).get("market_regime", c.get("market_regime", "?")),
                 "title": c.get("title", "")}
                for c in cards[-8:]
            ],
        },
        "backtest": {
            "candidate_count": len(candidates),
            "top_candidate": candidates[0] if candidates else None,
            "candidates": candidates[:10],
            "variety_count": variety_count,
            "trial_count": trial_count,
        },
        "paper_trade": {
            "queue_count": len(pt_queue.get("candidates", [])) if isinstance(pt_queue, dict) else 0,
            "promotion_ready": pt_monitor.get("promotion_ready_count", 0) if isinstance(pt_monitor, dict) else 0,
            "significant": pt_monitor.get("statistically_significant_count", 0) if isinstance(pt_monitor, dict) else 0,
        },
        "cycle_timeline": cycle_timeline,
    }


@app.get("/api/regime-distribution")
def api_regime_distribution():
    """Regime distribution from backtest data and SOL monitor."""
    # Read from pattern_regime_map if available
    prm = _json(RESEARCH / "pattern_regime_map.json")
    regime_map = {}
    if isinstance(prm, dict):
        for pattern_id, pdata in prm.items():
            if isinstance(pdata, dict):
                for regime, count in pdata.get("regime_counts", {}).items():
                    regime_map[regime] = regime_map.get(regime, 0) + count

    # Read learning loop report for recent regime data
    learning_report = _json(RESEARCH / "learning_loop_report.json")

    return {
        "regimes": regime_map,
        "learning_report": {
            "card_count": learning_report.get("after", {}).get("card_count", 0),
            "packet_count": learning_report.get("before", {}).get("pending_packet_count", 0),
            "consistent": learning_report.get("after", {}).get("state_consistent", True),
        },
    }


# ── HTML dashboard ───────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def dashboard_html():
    return HTML_PAGE


@app.get("/evolution-viz", response_class=HTMLResponse)
def evolution_viz_page():
    return EVOLUTION_VIZ_PAGE


HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Spark Domain Chip: Crypto Trading</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<script>
tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: { sans: ['DM Sans', 'system-ui', 'sans-serif'], mono: ['DM Mono', 'monospace'] },
      colors: {
        border: '#222430',
        ring: '#2A2E3C',
        background: '#0E1018',
        foreground: '#F0F0F4',
        card: { DEFAULT: '#181C26', foreground: '#F0F0F4' },
        muted: { DEFAULT: '#222430', foreground: '#8890B0' },
        accent: { DEFAULT: '#2FCA94', foreground: '#0E1018' },
        emerald: { 400: '#2FCA94', 500: '#22B841' },
        violet: { 400: '#68A8D8', 500: '#5090C0' },
        sky: { 400: '#68A8D8', 500: '#5090C0' },
      }
    }
  }
}
</script>
<style>
  /* Spark Swarm Design System */
  @keyframes fadeUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
  .fade-up { animation: fadeUp 0.4s ease-out both; }
  .fade-up:nth-child(1) { animation-delay: 0s; }
  .fade-up:nth-child(2) { animation-delay: 0.15s; }
  .fade-up:nth-child(3) { animation-delay: 0.3s; }
  .fade-up:nth-child(4) { animation-delay: 0.45s; }
  .fade-up:nth-child(5) { animation-delay: 0.6s; }
  .fade-up:nth-child(6) { animation-delay: 0.75s; }

  body { background: #0E1018; color: #F0F0F4; font-family: 'DM Sans', system-ui, sans-serif; }
  .card { background: #181C26; border: 1px solid #222430; border-radius: 6px; }
  .badge { padding: 3px 8px; border-radius: 3px; font-size: 0.75rem; font-weight: 500; font-family: 'DM Mono', monospace; border: 1px solid #222430; }
  .badge-emerald { background: #14161E; color: #3DDDA4; border-color: #222430; }
  .badge-violet { background: #14161E; color: #68A8D8; border-color: #222430; }
  .badge-sky { background: #14161E; color: #68A8D8; border-color: #222430; }
  .badge-muted { background: #14161E; color: #6A7080; border-color: #222430; }
  .pulse { animation: pulse 2s cubic-bezier(.4,0,.6,1) infinite; }
  @keyframes pulse { 0%,100% { opacity:1 } 50% { opacity:.5 } }
  .progress-bar { height: 6px; border-radius: 3px; background: #222430; overflow: hidden; }
  .progress-fill { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
  .feed-item { border-left: 2px solid transparent; transition: all 0.3s; }
  .feed-item:hover { background: #1E2230; }
  .stat-label { font-size: 0.8rem; color: #8890B0; font-weight: 500; letter-spacing: 0.05em; font-family: 'DM Mono', monospace; }
  .stat-value { font-size: 1.75rem; font-weight: 700; letter-spacing: -0.02em; font-family: 'DM Mono', monospace; }
  .section-title { font-size: 0.6875rem; font-weight: 600; color: #6A7080; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem; }
  canvas { max-height: 200px; }
  .tab-btn { padding: 4px 12px; border-radius: 5px; font-size: 0.75rem; font-weight: 500; background: transparent; color: #6A7080; border: 1px solid transparent; cursor: pointer; transition: all 0.2s; }
  .tab-btn:hover { color: #F0F0F4; background: #1E2230; }
  .tab-active { background: #222430 !important; color: #F0F0F4 !important; border-color: #2A2E3C !important; }
  #agents-table th { user-select: none; white-space: nowrap; }
  #agents-table th.sortable:hover { color: #F0F0F4; }
  #agents-table td { padding: 6px 12px 6px 0; white-space: nowrap; border-bottom: 1px solid #1E2230; }
  table tbody tr { transition: transform 0.15s, background 0.15s; }
  table tbody tr:hover { background: #1E2230; transform: translateX(3px); }
  .filter-select {
  background: #141820;
  border: 1px solid #222430;
  color: #8890B0;
  font-size: 0.75rem;
  padding: 4px 8px;
  border-radius: 5px;
  font-family: 'DM Sans', system-ui, sans-serif;
  cursor: pointer;
}
.filter-select:focus { outline: 1px solid #2A2E3C; }
.guard-tag { display: inline-block; padding: 1px 6px; border-radius: 3px; font-size: 0.65rem; background: #14161E; color: #6A7080; margin: 1px 2px; border: 1px solid #222430; font-family: 'DM Mono', monospace; }
.act-entry { padding: 6px 8px 6px 12px; border-left: 3px solid transparent; border-radius: 0 4px 4px 0; transition: background 0.15s; }
.act-entry:hover { background: #1E2230; }
.act-mono { font-family: 'DM Mono', monospace; font-size: 0.7rem; letter-spacing: -0.02em; }
.strat-bar-seg { height: 100%; display: inline-block; transition: width 0.6s; position: relative; }
.strat-bar-seg:hover::after { content: attr(data-tip); position: absolute; bottom: 110%; left: 50%; transform: translateX(-50%); background: #181C26; color: #F0F0F4; font-size: 0.65rem; padding: 2px 6px; border-radius: 3px; white-space: nowrap; pointer-events: none; z-index: 10; border: 1px solid #222430; }
.mut-bar { height: 10px; border-radius: 3px; background: #1a3d2e; transition: width 0.4s; }
.mut-bar-rm { background: #3d1a1a; }
</style>
</head>
<body class="min-h-screen p-6">

<!-- HEADER -->
<div class="flex items-center justify-between mb-8">
  <div>
    <h1 class="text-2xl font-bold tracking-tight">Spark Domain Chip <span style="color:#2FCA94">Crypto Trading</span></h1>
    <p class="text-sm text-muted-foreground" style="color: #8890B0;">Autoloop doctrine discovery + backtesting + live paper trading</p>
    <a href="/evolution-viz" class="text-xs" style="color:#6A7080;text-decoration:none;margin-top:2px;display:inline-block" onmouseover="this.style.color='#2FCA94'" onmouseout="this.style.color='#6A7080'">Evolution Graph &rarr;</a>
  </div>
  <div class="flex items-center gap-3">
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 rounded-full bg-emerald-500 pulse"></span>
      <span class="text-sm font-medium text-emerald-400">Live</span>
    </div>
    <span id="clock" class="text-xs" style="color: #8890B0;">--:--:--</span>
  </div>
</div>

<!-- TOP METRICS -->
<div class="grid grid-cols-6 gap-3 mb-6" id="metrics">
  <div class="card p-4 fade-up">
    <div class="stat-label">Generation</div>
    <div class="stat-value" id="m-gen">--</div>
  </div>
  <div class="card p-4 fade-up">
    <div class="stat-label">Best Win Rate</div>
    <div class="stat-value text-emerald-400" id="m-best-wr">--</div>
  </div>
  <div class="card p-4 fade-up">
    <div class="stat-label">Avg Win Rate</div>
    <div class="stat-value" id="m-avg-wr">--</div>
  </div>
  <div class="card p-4 fade-up">
    <div class="stat-label">Elite Agents</div>
    <div class="stat-value text-violet-400" id="m-elite">--</div>
    <div class="text-xs mt-1" style="color: #8890B0;" id="m-elite-delta"></div>
  </div>
  <div class="card p-4 fade-up">
    <div class="stat-label">Viable Agents</div>
    <div class="stat-value text-sky-400" id="m-viable">--</div>
  </div>
  <div class="card p-4 fade-up">
    <div class="stat-label">Total Population</div>
    <div class="stat-value" id="m-total">--</div>
  </div>
</div>

<!-- MAIN GRID -->
<div class="grid grid-cols-12 gap-4">

  <!-- LEFT: Live Feed (5 cols) -->
  <div class="col-span-5">
    <div class="card p-5 h-full">
      <div class="section-title">Recent Elite Agents</div>
      <div id="feed" class="space-y-1 overflow-y-auto" style="max-height: 520px;"></div>
    </div>
  </div>

  <!-- MIDDLE: Charts (4 cols) -->
  <div class="col-span-4 space-y-4">
    <div class="card p-5">
      <div class="section-title">Population Growth</div>
      <canvas id="popChart"></canvas>
    </div>
    <div class="card p-5">
      <div class="section-title">Elite Production</div>
      <canvas id="eliteChart"></canvas>
    </div>
  </div>

  <!-- RIGHT: Status panels (3 cols) -->
  <div class="col-span-3 space-y-4">

    <!-- Methods -->
    <div class="card p-5">
      <div class="section-title">Search Methods</div>
      <div id="methods" class="space-y-3"></div>
    </div>

    <!-- Health -->
    <div class="card p-5">
      <div class="section-title">System Health</div>
      <div id="health" class="grid grid-cols-2 gap-3"></div>
    </div>
  </div>
</div>

<!-- ACTIVITY FEED + STRATEGY DIVERSITY -->
<div class="mt-4">
  <div class="grid grid-cols-12 gap-4">
    <!-- Activity Feed -->
    <div class="col-span-7">
      <div class="card p-5" style="max-height:620px;display:flex;flex-direction:column">
        <div class="flex items-center justify-between mb-3">
          <div class="section-title mb-0">Activity Feed</div>
          <div class="flex items-center gap-2">
            <span class="text-xs" style="color:#6A7080" id="feed-count"></span>
            <select id="feed-filter" onchange="renderActivityFeed()" class="filter-select">
              <option value="">All</option>
              <option value="elite">Elite</option>
              <option value="viable">Viable+</option>
              <option value="improved">Improved</option>
            </select>
          </div>
        </div>
        <div id="activity-feed" style="overflow-y:auto;flex:1" class="space-y-0.5"></div>
      </div>
    </div>
    <!-- Strategy Diversity -->
    <div class="col-span-5 space-y-4">
      <div class="card p-5">
        <div class="flex items-center justify-between mb-3">
          <div class="section-title mb-0">Strategy Diversity</div>
          <div class="flex items-center gap-2">
            <span class="text-xs" style="color:#6A7080">Index:</span>
            <span class="text-sm font-bold" id="diversity-index" style="color:#2FCA94">--</span>
          </div>
        </div>
        <div id="strategy-bar" style="height:28px;border-radius:6px;overflow:hidden;display:flex;margin-bottom:12px;background:#1E2230"></div>
        <div id="strategy-list" class="space-y-1.5" style="max-height:260px;overflow-y:auto"></div>
      </div>
      <div class="card p-5">
        <div class="section-title">Mutation Activity <span class="text-xs font-normal" style="color:#6A7080">(last 100 agents)</span></div>
        <div id="mutation-activity" class="grid grid-cols-2 gap-4"></div>
      </div>
    </div>
  </div>
</div>

<!-- LIVE TRADING SECTION (real-time Binance data) -->
<div class="mt-4" id="live-pt-section">
  <div class="card p-5">
    <!-- Header row: title + status + period tabs -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="section-title mb-0">Live Trading <span class="text-xs font-normal" style="color:#6A7080">(Real-Time Binance)</span></div>
        <div id="live-pt-status-badge"></div>
      </div>
      <div class="flex items-center gap-2">
        <div class="flex" style="background:#141820;border-radius:6px;padding:2px;gap:2px" id="live-period-tabs">
          <button class="live-period-tab" data-period="daily" style="padding:3px 10px;border-radius:4px;font-size:0.7rem;border:none;cursor:pointer;background:transparent;color:#6A7080">Daily</button>
          <button class="live-period-tab" data-period="weekly" style="padding:3px 10px;border-radius:4px;font-size:0.7rem;border:none;cursor:pointer;background:transparent;color:#6A7080">Weekly</button>
          <button class="live-period-tab active" data-period="alltime" style="padding:3px 10px;border-radius:4px;font-size:0.7rem;border:none;cursor:pointer;background:#222430;color:#F0F0F4">All-Time</button>
        </div>
        <span class="text-xs" style="color:#6A7080" id="live-pt-updated"></span>
      </div>
    </div>

    <!-- Summary stats row (changes with period tab) -->
    <div class="grid grid-cols-6 gap-3 mb-4">
      <div class="card p-3" style="background:#141820">
        <div class="stat-label">Settlements</div>
        <div class="stat-value text-sm text-violet-400" id="live-settlements">--</div>
      </div>
      <div class="card p-3" style="background:#141820">
        <div class="stat-label">Trades</div>
        <div class="stat-value text-sm text-sky-400" id="live-trades-count">--</div>
      </div>
      <div class="card p-3" style="background:#141820">
        <div class="stat-label">Wins</div>
        <div class="stat-value text-sm" style="color:#2FCA94" id="live-wins-count">--</div>
      </div>
      <div class="card p-3" style="background:#141820">
        <div class="stat-label">Losses</div>
        <div class="stat-value text-sm" style="color:#E08878" id="live-losses-count">--</div>
      </div>
      <div class="card p-3" style="background:#141820">
        <div class="stat-label">Win Rate</div>
        <div class="stat-value text-sm" id="live-accuracy">--</div>
      </div>
      <div class="card p-3" style="background:#141820">
        <div class="stat-label">Agents / Strategies</div>
        <div class="stat-value text-sm" id="live-agents-strats">--</div>
      </div>
    </div>

    <!-- Current contracts (multi-timeframe) -->
    <div class="mb-4">
      <div class="text-xs font-medium mb-2" style="color:#8890B0">Active Contracts</div>
      <div id="live-contracts" class="grid gap-2" style="grid-template-columns:repeat(auto-fill,minmax(280px,1fr))">
        <div style="padding:12px;text-align:center;color:#6A7080;font-size:0.8rem">
          Start: <span style="font-family:'DM Mono',monospace;color:#8890B0">python live_paper_trader.py --assets BTC --per-strategy 3</span>
        </div>
      </div>
    </div>

    <!-- Regime history strip -->
    <div class="mb-4">
      <div class="text-xs font-medium mb-2" style="color:#8890B0">Regime History</div>
      <div id="live-regime-history" class="flex items-center gap-1 flex-wrap" style="min-height:24px"></div>
    </div>

    <!-- Strategy performance table -->
    <div class="mb-4">
      <div class="text-xs font-medium mb-2" style="color:#8890B0">Strategy Performance</div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left" style="color:#6A7080; border-bottom:1px solid #222430;">
              <th class="pb-2 pr-4 font-medium">Strategy</th>
              <th class="pb-2 pr-4 font-medium">Agents</th>
              <th class="pb-2 pr-4 font-medium">Trades</th>
              <th class="pb-2 pr-4 font-medium">Wins</th>
              <th class="pb-2 pr-4 font-medium">Losses</th>
              <th class="pb-2 pr-4 font-medium">Win Rate</th>
              <th class="pb-2 font-medium">Regimes</th>
            </tr>
          </thead>
          <tbody id="live-strategy-table"></tbody>
        </table>
      </div>
    </div>

    <!-- Agent performance table -->
    <div class="mb-4">
      <div class="text-xs font-medium mb-2" style="color:#8890B0">Agent Performance</div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left" style="color:#6A7080; border-bottom:1px solid #222430;">
              <th class="pb-2 pr-4 font-medium">Agent</th>
              <th class="pb-2 pr-4 font-medium">Strategy</th>
              <th class="pb-2 pr-4 font-medium">TF</th>
              <th class="pb-2 pr-4 font-medium">BT WR</th>
              <th class="pb-2 pr-4 font-medium">Live WR</th>
              <th class="pb-2 pr-4 font-medium">Delta</th>
              <th class="pb-2 pr-4 font-medium">Trades</th>
              <th class="pb-2 pr-4 font-medium">Wins</th>
              <th class="pb-2 font-medium">Skips</th>
            </tr>
          </thead>
          <tbody id="live-agent-table"></tbody>
        </table>
      </div>
    </div>

    <!-- Recent settlements -->
    <div>
      <div class="text-xs font-medium mb-2" style="color:#8890B0">Recent Settlements</div>
      <div id="live-settlements-list" style="max-height:250px;overflow-y:auto;"></div>
    </div>
  </div>
</div>

<!-- HOLDOUT BACKTEST SECTION (formerly "Paper Trade" - same historical data as BT) -->
<div class="mt-4">
  <!-- Holdout BT Top Metrics Row -->
  <div class="grid grid-cols-6 gap-3 mb-4">
    <div class="card p-4">
      <div class="flex items-center gap-2 mb-1">
        <div class="stat-label">Daemon</div>
        <div id="pt-daemon-status"></div>
      </div>
      <div class="stat-value" id="pt-cycles-display">--</div>
      <div class="text-xs mt-1" style="color:#6A7080" id="pt-daemon-detail">cycles</div>
    </div>
    <div class="card p-4">
      <div class="stat-label">Agents Tested</div>
      <div class="stat-value text-violet-400" id="pt-unique">--</div>
      <div class="text-xs mt-1" style="color:#6A7080" id="pt-coverage-detail">of -- elite</div>
    </div>
    <div class="card p-4">
      <div class="stat-label">Avg Holdout Delta</div>
      <div class="stat-value text-emerald-400" id="pt-avg-delta">--</div>
      <div class="text-xs mt-1" style="color:#6A7080">Holdout vs Backtest</div>
    </div>
    <div class="card p-4">
      <div class="stat-label">Needs Data</div>
      <div class="stat-value" style="color:#6A7080" id="pt-count-needs">--</div>
    </div>
    <div class="card p-4">
      <div class="stat-label">Validated</div>
      <div class="stat-value text-sky-400" id="pt-count-validated">--</div>
    </div>
    <div class="card p-4">
      <div class="stat-label">Live Ready</div>
      <div class="stat-value text-emerald-400" id="pt-count-live">--</div>
    </div>
  </div>

  <!-- Coverage bar -->
  <div class="card p-4 mb-4">
    <div class="flex items-center justify-between mb-2">
      <span class="text-xs font-medium" style="color:#8890B0" id="pt-coverage-label">Coverage: -- of -- elite tested</span>
      <div class="flex items-center gap-3">
        <span class="text-xs font-semibold text-violet-400" id="pt-coverage-pct">--%</span>
        <span id="pt-summary-badges"></span>
      </div>
    </div>
    <div class="progress-bar" style="height:8px">
      <div class="progress-fill" id="pt-coverage-bar" style="width:0%;background:linear-gradient(90deg,#68A8D8,#2FCA94)"></div>
    </div>
  </div>

  <!-- PT Charts: side-by-side on top -->
  <div class="grid grid-cols-2 gap-4 mb-4">
    <div class="card p-5">
      <div class="section-title">Backtest vs Holdout BT</div>
      <canvas id="ptScatterChart" style="max-height:220px;"></canvas>
    </div>
    <div class="card p-5">
      <div class="section-title">Holdout BT Win Rate Over Time</div>
      <canvas id="ptChart" style="max-height:220px;"></canvas>
    </div>
  </div>

  <!-- PT Leaderboard: full width like Top Agents -->
  <div class="card p-5">
    <div class="flex items-center justify-between mb-4">
      <div class="section-title mb-0">Holdout Backtest Leaderboard</div>
      <div class="flex items-center gap-2">
        <span class="text-xs" style="color:#6A7080">Top 20 by Holdout Score (same-period BT, not live)</span>
      </div>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-sm" id="pt-table">
        <thead>
          <tr class="text-left" style="color:#6A7080; border-bottom:1px solid #222430;">
            <th class="pb-2 pr-4 font-medium">#</th>
            <th class="pb-2 pr-4 font-medium">Holdout WR</th>
            <th class="pb-2 pr-4 font-medium">BT Win Rate</th>
            <th class="pb-2 pr-4 font-medium">Delta</th>
            <th class="pb-2 pr-4 font-medium">Agent</th>
            <th class="pb-2 pr-4 font-medium">Strategy</th>
            <th class="pb-2 pr-4 font-medium">Asset</th>
            <th class="pb-2 pr-4 font-medium">TF</th>
            <th class="pb-2 pr-4 font-medium">Score</th>
            <th class="pb-2 pr-4 font-medium">BT Trades</th>
            <th class="pb-2 pr-4 font-medium">Holdout Trades</th>
            <th class="pb-2 pr-4 font-medium">Runs</th>
            <th class="pb-2 pr-4 font-medium">Consistency</th>
            <th class="pb-2 font-medium">Status</th>
          </tr>
        </thead>
        <tbody id="pt-leaderboard"></tbody>
      </table>
    </div>
    <div id="pt-table-count" class="text-xs mt-3" style="color:#6A7080;"></div>
  </div>
</div>

<!-- TOP AGENTS -->
<div class="mt-4">
  <div class="card p-5">
    <div class="flex items-center justify-between mb-4">
      <div class="section-title mb-0">Top Agents</div>
      <div class="flex items-center gap-4">
        <div class="flex gap-1" id="agent-tabs">
          <button onclick="switchTab('session')" data-tab="session" class="tab-btn tab-active">This Session</button>
          <button onclick="switchTab('today')" data-tab="today" class="tab-btn">Today</button>
          <button onclick="switchTab('week')" data-tab="week" class="tab-btn">This Week</button>
          <button onclick="switchTab('all')" data-tab="all" class="tab-btn">All Time</button>
        </div>
        <div class="flex items-center gap-1" style="border-left:1px solid #222430; padding-left:12px;">
          <span class="text-xs" style="color:#6A7080; margin-right:4px;">Show</span>
          <button onclick="setPageSize(20)" data-size="20" class="tab-btn page-btn tab-active">20</button>
          <button onclick="setPageSize(50)" data-size="50" class="tab-btn page-btn">50</button>
          <button onclick="setPageSize(100)" data-size="100" class="tab-btn page-btn">100</button>
        </div>
      </div>
    </div>
    <div class="flex items-center gap-3 mb-3 mt-2" id="filter-bar">
      <span class="text-xs" style="color:#6A7080">Filter:</span>
      <select id="filter-strategy" onchange="renderAgents()" class="filter-select">
        <option value="">All Strategies</option>
      </select>
      <select id="filter-asset" onchange="renderAgents()" class="filter-select">
        <option value="">All Assets</option>
      </select>
      <select id="filter-tf" onchange="renderAgents()" class="filter-select">
        <option value="">All Timeframes</option>
      </select>
      <select id="filter-method" onchange="renderAgents()" class="filter-select">
        <option value="">All Methods</option>
      </select>
      <button onclick="clearFilters()" class="tab-btn text-xs">Clear</button>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-sm" id="agents-table">
        <thead>
          <tr class="text-left" style="color:#6A7080; border-bottom:1px solid #222430;">
            <th class="pb-2 pr-3 font-medium">#</th>
            <th class="pb-2 pr-3 font-medium cursor-pointer" onclick="sortAgents('wr')">BT Win Rate</th>
            <th class="pb-2 pr-3 font-medium cursor-pointer" onclick="sortAgents('pt_wr')">Holdout WR</th>
            <th class="pb-2 pr-3 font-medium">Agent</th>
            <th class="pb-2 pr-3 font-medium">Gen</th>
            <th class="pb-2 pr-3 font-medium">Strategy</th>
            <th class="pb-2 pr-3 font-medium">Asset</th>
            <th class="pb-2 pr-3 font-medium">TF</th>
            <th class="pb-2 pr-3 font-medium cursor-pointer" onclick="sortAgents('wf')">WF</th>
            <th class="pb-2 pr-3 font-medium cursor-pointer" onclick="sortAgents('trades')">Trades</th>
            <th class="pb-2 pr-3 font-medium cursor-pointer" onclick="sortAgents('sharpe')">Sharpe</th>
            <th class="pb-2 pr-3 font-medium">Drawdown</th>
            <th class="pb-2 pr-3 font-medium">Validation</th>
            <th class="pb-2 pr-3 font-medium">Method</th>
            <th class="pb-2 font-medium">Key Guards</th>
          </tr>
        </thead>
        <tbody id="agents-body"></tbody>
      </table>
    </div>
    <div id="agents-count" class="text-xs mt-3" style="color:#6A7080;"></div>
  </div>
</div>

<!-- Insights (compact, below agents) -->
<div class="mt-4">
  <div class="card p-5">
    <div class="section-title">Guard Discoveries</div>
    <div id="insights" class="grid grid-cols-3 gap-2"></div>
  </div>
</div>

<!-- AUTOLOOP TRI-LOOP SECTION -->
<div class="mt-4" id="autoloop-section">
  <!-- Autoloop header + status -->
  <div class="card p-5">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="section-title mb-0">Autoloop <span class="text-xs font-normal" style="color:#6A7080">(Doctrine Discovery + Backtest + Paper Trade)</span></div>
        <span id="autoloop-status-badge" class="text-xs px-2 py-0.5 rounded" style="background:#222430;color:#6A7080">--</span>
      </div>
      <div class="flex gap-4 text-xs" style="color:#6A7080">
        <span>Cycle: <span id="al-cycle" class="font-mono" style="color:#F0F0F4">--</span></span>
        <span>Noop: <span id="al-noop" class="font-mono" style="color:#F0F0F4">--</span></span>
      </div>
    </div>

    <!-- Lane status cards -->
    <div class="grid grid-cols-3 gap-3 mb-4">
      <!-- Learning Lane -->
      <div class="card p-3" style="background:#141820">
        <div class="text-xs mb-1" style="color:#6A7080">Learning Lane</div>
        <div class="flex items-baseline gap-2">
          <span id="al-doctrine-cards" class="text-lg font-mono font-bold" style="color:#2FCA94">--</span>
          <span class="text-xs" style="color:#6A7080">doctrine cards</span>
        </div>
        <div class="text-xs mt-1" style="color:#6A7080">
          <span id="al-doctrine-packets" class="font-mono">--</span> packets
        </div>
      </div>

      <!-- Backtest Lane -->
      <div class="card p-3" style="background:#141820">
        <div class="text-xs mb-1" style="color:#6A7080">Backtest Lane</div>
        <div class="flex items-baseline gap-2">
          <span id="al-bt-candidates" class="text-lg font-mono font-bold" style="color:#68A8D8">--</span>
          <span class="text-xs" style="color:#6A7080">candidates</span>
        </div>
        <div class="text-xs mt-1" style="color:#6A7080">
          <span id="al-variety" class="font-mono">--</span> variety &middot;
          <span id="al-trials" class="font-mono">--</span> trials
        </div>
      </div>

      <!-- Paper Trade Lane -->
      <div class="card p-3" style="background:#141820">
        <div class="text-xs mb-1" style="color:#6A7080">Paper Trade Lane</div>
        <div class="flex items-baseline gap-2">
          <span id="al-pt-queue" class="text-lg font-mono font-bold" style="color:#E8B86D">--</span>
          <span class="text-xs" style="color:#6A7080">in queue</span>
        </div>
        <div class="text-xs mt-1" style="color:#6A7080">
          <span id="al-pt-ready" class="font-mono">--</span> ready &middot;
          <span id="al-pt-sig" class="font-mono">--</span> significant
        </div>
      </div>
    </div>

    <!-- Cycle timeline + top candidates side by side -->
    <div class="grid grid-cols-2 gap-4">
      <!-- Cycle timeline chart -->
      <div>
        <div class="text-xs mb-2" style="color:#6A7080">Cycle Timeline <span class="font-mono" id="al-timeline-range"></span></div>
        <canvas id="al-cycle-chart" height="120"></canvas>
      </div>

      <!-- Top backtest candidates -->
      <div>
        <div class="text-xs mb-2" style="color:#6A7080">Top Backtest Candidates</div>
        <div style="max-height:180px;overflow-y:auto">
          <table class="w-full text-xs">
            <thead><tr style="color:#6A7080">
              <th class="text-left pb-1">Candidate</th>
              <th class="text-right pb-1">WR</th>
              <th class="text-right pb-1">WF</th>
              <th class="text-right pb-1">DD</th>
              <th class="text-right pb-1">Trades</th>
              <th class="text-right pb-1">Ready</th>
            </tr></thead>
            <tbody id="al-candidates-table"></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Recent doctrine cards -->
    <div class="mt-4">
      <div class="text-xs mb-2" style="color:#6A7080">Recent Doctrine Cards</div>
      <div id="al-doctrine-list" class="flex flex-wrap gap-2"></div>
    </div>
  </div>
</div>

<!-- FOOTER -->
<div class="mt-6 flex items-center justify-between text-xs" style="color: #6A7080;">
  <span>Spark Domain Chip: Crypto Trading &middot; Autoloop + Evolution + Live Paper Trading &middot; Built with Claude Code</span>
  <span id="footer-status">Connecting...</span>
</div>

<script>
// ── State ─────────────────────────────────────────
let popChartInstance = null;
let eliteChartInstance = null;
let prevElite = 0;

const CHART_COLORS = {
  emerald: '#2FCA94',
  violet: '#68A8D8',
  sky: '#68A8D8',
  muted: '#8890B0',
  border: '#222430',
  gridLine: '#1E2230',
};

const CHART_DEFAULTS = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: true, position: 'top',
    labels: { color: CHART_COLORS.muted, boxWidth: 8, padding: 12, font: { size: 11, family: 'DM Sans' } }
  }},
  scales: {
    x: { grid: { color: CHART_COLORS.gridLine }, ticks: { color: CHART_COLORS.muted, font: { size: 10, family: 'DM Mono' }, maxTicksLimit: 8 } },
    y: { grid: { color: CHART_COLORS.gridLine }, ticks: { color: CHART_COLORS.muted, font: { size: 10, family: 'DM Mono' } } },
  }
};

// ── Fetch helpers ─────────────────────────────────
async function fetchJSON(url) {
  try { const r = await fetch(url); return await r.json(); } catch { return null; }
}

// ── Render functions ──────────────────────────────

function renderMetrics(d) {
  document.getElementById('m-gen').textContent = d.generation.toLocaleString();
  document.getElementById('m-best-wr').textContent = (d.best_wr * 100).toFixed(1) + '%';
  document.getElementById('m-avg-wr').textContent = (d.avg_wr * 100).toFixed(1) + '%';
  document.getElementById('m-elite').textContent = d.elite.toLocaleString();
  document.getElementById('m-viable').textContent = d.viable.toLocaleString();
  document.getElementById('m-total').textContent = d.total.toLocaleString();

  const delta = d.elite - prevElite;
  if (prevElite > 0 && delta > 0) {
    document.getElementById('m-elite-delta').textContent = '+' + delta + ' this batch';
  }
  prevElite = d.elite;
}

function renderMethods(methods) {
  const el = document.getElementById('methods');
  const sorted = Object.entries(methods).sort((a, b) => b[1].rate - a[1].rate);
  el.innerHTML = sorted.map(([name, d]) => {
    const pct = (d.rate * 100).toFixed(0);
    const color = d.rate >= 0.5 ? CHART_COLORS.emerald : d.rate >= 0.2 ? CHART_COLORS.sky : d.rate >= 0.1 ? CHART_COLORS.violet : CHART_COLORS.muted;
    const label = name.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    return `
      <div>
        <div class="flex justify-between items-baseline mb-1">
          <span class="text-sm font-medium">${label}</span>
          <span class="text-sm font-semibold" style="color:${color}">${pct}%</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" style="width:${Math.min(pct, 100)}%;background:${color}"></div>
        </div>
        <div class="text-xs mt-0.5" style="color:#6A7080">${d.improvements.toLocaleString()}/${d.attempts.toLocaleString()} &middot; avg ${(d.avg_wr*100).toFixed(1)}%</div>
      </div>`;
  }).join('');
}

function renderFeed(elites) {
  const el = document.getElementById('feed');
  el.innerHTML = elites.map(a => {
    const wr = (a.wr * 100).toFixed(1);
    let borderColor, badge;
    if (a.wr >= 0.65) { borderColor = CHART_COLORS.emerald; badge = '<span class="badge badge-emerald">Exceptional</span>'; }
    else if (a.wr >= 0.60) { borderColor = CHART_COLORS.sky; badge = '<span class="badge badge-sky">Strong</span>'; }
    else { borderColor = '#2A2E3C'; badge = '<span class="badge badge-muted">Elite</span>'; }
    let time = '';
    try { const t = new Date(a.ts); time = t.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit',second:'2-digit'}); } catch {}
    const strat = (a.strat_id || a.strategy || '').replace(/_/g, ' ');
    const assetShort = (a.asset || '?').split(' ')[0];
    const tf = a.tf || '?';
    return `
      <div class="feed-item px-3 py-2 rounded-lg" style="border-left-color:${borderColor}">
        <div class="flex justify-between items-center">
          <div>
            <span class="font-semibold text-sm" style="color:${borderColor}">${wr}%</span>
            <span class="text-xs ml-2" style="color:#6A7080">Agent ${a.agent}</span>
            ${badge}
          </div>
          <span class="text-xs" style="color:#6A7080">${time}</span>
        </div>
        <div class="text-xs mt-0.5" style="color:#6A7080">Gen ${a.gen} &middot; ${strat} &middot; ${assetShort}/${tf} &middot; ${a.trades} trades &middot; WF ${a.wf.toFixed(1)}</div>
      </div>`;
  }).join('');
}

let ptChartInstance = null;
let ptScatterInstance = null;

function renderPaperTrade(data) {
  if (!data || !data.summary) return;
  const { history, summary } = data;

  // Total runs shown in daemon detail
  const runsEl = document.getElementById('pt-daemon-detail');
  if (runsEl && summary.total_runs) {
    const existing = runsEl.textContent;
    if (!existing.includes('runs')) runsEl.textContent = existing + ' | ' + summary.total_runs + ' total runs';
  }

  // PT timeline chart
  renderPtChart(history);
}

function renderPtDashboard(data) {
  if (!data) return;
  const { daemon, coverage, status_counts, leaderboard, scatter } = data;

  // Daemon status: pulse dot in the card
  const dsEl = document.getElementById('pt-daemon-status');
  const statusColor = daemon.status === 'running' ? CHART_COLORS.emerald : daemon.status === 'stopped' ? '#E08878' : '#D8C868';
  const pulse = daemon.status === 'running' ? 'animation:pulse 2s infinite;' : '';
  dsEl.innerHTML = '<span style="width:8px;height:8px;border-radius:50%;background:' + statusColor + ';display:inline-block;' + pulse + '"></span>';

  // Cycles display
  document.getElementById('pt-cycles-display').textContent = daemon.cycles || 0;
  const activeDaemons = daemon.active_daemons || (daemon.status === 'running' ? 1 : 0);
  const daemonLabel = activeDaemons > 1
    ? activeDaemons + ' daemons (' + daemon.interval + 's interval)'
    : daemon.status === 'running' ? 'cycles (' + daemon.interval + 's interval)' : daemon.status || 'not started';
  // Show per-TF breakdown if multiple daemons
  const daemonsList = data.daemons || [];
  let daemonDetail = daemonLabel;
  if (daemonsList.length > 1) {
    const tfLabels = daemonsList.filter(d => d.status === 'running').map(d => d.timeframe).join(', ');
    if (tfLabels) daemonDetail += ' | TF: ' + tfLabels;
  }
  document.getElementById('pt-daemon-detail').textContent = daemonDetail;

  // Coverage metrics
  const tested = coverage.tested_agents || 0;
  const total = coverage.total_elite || 0;
  const pct = coverage.coverage_pct || 0;
  document.getElementById('pt-unique').textContent = tested.toLocaleString();
  document.getElementById('pt-coverage-detail').textContent = 'of ' + total.toLocaleString() + ' elite';
  document.getElementById('pt-coverage-label').textContent = 'Coverage: ' + tested.toLocaleString() + ' of ' + total.toLocaleString() + ' elite tested';
  document.getElementById('pt-coverage-pct').textContent = (pct * 100).toFixed(1) + '%';
  document.getElementById('pt-coverage-bar').style.width = Math.min(100, pct * 100) + '%';

  // Avg delta from scatter data
  if (scatter && scatter.length) {
    const deltas = scatter.map(s => s.pt_wr - s.bt_wr);
    const avg = deltas.reduce((a,b) => a+b, 0) / deltas.length;
    const sign = avg >= 0 ? '+' : '';
    document.getElementById('pt-avg-delta').textContent = sign + (avg * 100).toFixed(1) + '%';
  }

  // Status counts
  document.getElementById('pt-count-needs').textContent = status_counts.needs_more_data || 0;
  document.getElementById('pt-count-validated').textContent = status_counts.validated || 0;
  document.getElementById('pt-count-live').textContent = status_counts.live_ready || 0;

  // Summary badge on coverage bar
  const badgesEl = document.getElementById('pt-summary-badges');
  const liveCount = status_counts.live_ready || 0;
  const valCount = status_counts.validated || 0;
  if (liveCount > 0) {
    badgesEl.innerHTML = '<span class="badge badge-emerald">' + liveCount + ' Live-Ready</span>';
  } else if (valCount > 0) {
    badgesEl.innerHTML = '<span class="badge badge-sky">' + valCount + ' Validated</span>';
  } else if (tested > 0) {
    badgesEl.innerHTML = '<span class="badge" style="background:#1E2230;color:#6A7080">Building Coverage</span>';
  } else {
    badgesEl.innerHTML = '';
  }

  // Leaderboard table - styled like Top Agents
  const tbody = document.getElementById('pt-leaderboard');
  if (leaderboard && leaderboard.length) {
    tbody.innerHTML = leaderboard.map((d, i) => {
      const rank = i + 1;
      const rankHtml = rank <= 3 ? '<span style="color:' + CHART_COLORS.emerald + ';font-weight:700">' + rank + '</span>' : rank;

      // PT WR color coding like Top Agents BT WR
      const ptWr = (d.pt_wr_avg * 100).toFixed(1);
      const ptColor = d.pt_wr_avg >= 0.80 ? CHART_COLORS.emerald : d.pt_wr_avg >= 0.70 ? CHART_COLORS.sky : d.pt_wr_avg >= 0.60 ? CHART_COLORS.violet : '#8890B0';

      const deltaColor = d.pt_delta_avg >= 0 ? CHART_COLORS.emerald : '#E08878';
      const deltaSign = d.pt_delta_avg >= 0 ? '+' : '';

      const scoreColor = d.pt_score >= 0.8 ? CHART_COLORS.emerald : d.pt_score >= 0.6 ? CHART_COLORS.sky : CHART_COLORS.muted;

      // Consistency: show std as a bar concept
      const consistencyHtml = d.run_count <= 1
        ? '<span style="color:#6A7080">--</span>'
        : '<span style="color:' + (d.pt_wr_std < 0.05 ? CHART_COLORS.emerald : d.pt_wr_std < 0.10 ? '#D8C868' : '#E08878') + '">&plusmn;' + (d.pt_wr_std*100).toFixed(1) + '%</span>';

      const strat = (d.strategy || '?').replace(/_/g, ' ');
      const asset = (d.asset || '?').split(',')[0].toUpperCase();
      const tf = d.timeframe || '?';

      const statusBadge = d.status === 'live_ready'
        ? '<span class="badge badge-emerald" style="padding:3px 12px;white-space:nowrap">Live Ready</span>'
        : d.status === 'validated'
        ? '<span class="badge badge-sky" style="padding:3px 12px;white-space:nowrap">Validated</span>'
        : '<span class="badge badge-muted" style="padding:3px 12px;white-space:nowrap">Needs Data</span>';

      const p = 'padding:6px 12px 6px 0;';
      return '<tr style="border-bottom:1px solid #1E2230">' +
        '<td style="' + p + '">' + rankHtml + '</td>' +
        '<td style="' + p + 'color:' + ptColor + ';font-weight:700;font-size:0.875rem">' + ptWr + '%</td>' +
        '<td style="' + p + 'color:#8890B0">' + (d.bt_wr*100).toFixed(1) + '%</td>' +
        '<td style="' + p + 'color:' + deltaColor + '">' + deltaSign + (d.pt_delta_avg*100).toFixed(1) + '%</td>' +
        '<td style="' + p + 'font-family:DM Mono,monospace;font-size:0.75rem;color:#8890B0">' + d.agent + '</td>' +
        '<td style="' + p + 'font-size:0.8rem">' + strat + '</td>' +
        '<td style="' + p + '">' + asset + '</td>' +
        '<td style="' + p + '">' + tf + '</td>' +
        '<td style="' + p + 'font-weight:600;color:' + scoreColor + '">' + d.pt_score.toFixed(3) + '</td>' +
        '<td style="' + p + 'color:#6A7080">' + (d.bt_trades || '--') + '</td>' +
        '<td style="' + p + '">' + d.pt_trades_total + '</td>' +
        '<td style="' + p + '">' + d.run_count + '</td>' +
        '<td style="' + p + '">' + consistencyHtml + '</td>' +
        '<td style="' + p + '">' + statusBadge + '</td>' +
        '</tr>';
    }).join('');
  } else {
    tbody.innerHTML = '<tr><td colspan="14" style="padding:24px;text-align:center;color:#6A7080">Start the holdout BT daemon: <span style="font-family:DM Mono,monospace;color:#8890B0">python run_paper_trade.py --daemon</span></td></tr>';
  }

  // Table count
  const countEl = document.getElementById('pt-table-count');
  if (countEl) countEl.textContent = 'Showing ' + leaderboard.length + ' of ' + tested + ' holdout-tested agents';

  // Scatter chart
  renderPtScatter(scatter);
}

function renderPtScatter(scatter) {
  const ctx = document.getElementById('ptScatterChart');
  if (!ctx || !scatter || !scatter.length) return;
  if (ptScatterInstance) ptScatterInstance.destroy();

  const colorMap = { live_ready: CHART_COLORS.emerald, validated: CHART_COLORS.sky, needs_more_data: CHART_COLORS.muted };
  const datasets = [
    { label: 'BT = Holdout (diagonal)', data: [{x:50,y:50},{x:85,y:85}], type:'line', borderColor:'#222430', borderDash:[4,4], borderWidth:1, pointRadius:0, fill:false },
    ...['live_ready','validated','needs_more_data'].map(status => ({
      label: status.replace(/_/g,' '),
      data: scatter.filter(s => s.status === status).map(s => ({x:s.bt_wr*100, y:s.pt_wr*100})),
      backgroundColor: colorMap[status] + '80',
      borderColor: colorMap[status],
      pointRadius: 4, pointHoverRadius: 6, borderWidth: 1,
    })),
  ];

  ptScatterInstance = new Chart(ctx.getContext('2d'), {
    type: 'scatter',
    data: { datasets },
    options: {
      ...CHART_DEFAULTS,
      plugins: { ...CHART_DEFAULTS.plugins, legend: { ...CHART_DEFAULTS.plugins.legend, position:'bottom', labels:{...CHART_DEFAULTS.plugins.legend.labels, boxWidth:6, padding:6, font:{size:8,family:'Inter'}} } },
      scales: {
        x: { ...CHART_DEFAULTS.scales.x, title:{display:true, text:'BT Win Rate %', color:CHART_COLORS.muted, font:{size:8}}, min:50, max:85 },
        y: { ...CHART_DEFAULTS.scales.y, title:{display:true, text:'Holdout Win Rate %', color:CHART_COLORS.muted, font:{size:8}}, min:50, max:85 },
      },
    },
  });
}

function renderPtChart(history) {
  const ctx = document.getElementById('ptChart');
  if (!ctx) return;
  if (ptChartInstance) ptChartInstance.destroy();

  const byAgent = {};
  for (const h of history) {
    if (!byAgent[h.agent]) byAgent[h.agent] = [];
    byAgent[h.agent].push(h);
  }

  const datasets = [];
  const agentColors = [CHART_COLORS.emerald, CHART_COLORS.violet, CHART_COLORS.sky, '#D8C868', '#f472b6', '#fb923c', '#a3e635', '#22d3ee', '#e879f9', '#E08878'];
  let colorIdx = 0;
  const allGens = new Set();
  for (const [agent, points] of Object.entries(byAgent)) {
    const c = agentColors[colorIdx++ % agentColors.length];
    points.forEach(p => allGens.add(p.gen));
    datasets.push({
      label: agent,
      data: points.map(p => ({ x: p.gen, y: p.pt_wr * 100 })),
      borderColor: c, backgroundColor: c + '30',
      pointRadius: 3, pointHoverRadius: 5, borderWidth: 2, tension: 0.2, fill: false,
    });
  }
  const labels = [...allGens].sort((a, b) => a - b);

  ptChartInstance = new Chart(ctx.getContext('2d'), {
    type: 'line',
    data: { labels, datasets },
    options: {
      ...CHART_DEFAULTS,
      plugins: { ...CHART_DEFAULTS.plugins, legend: { ...CHART_DEFAULTS.plugins.legend, position:'bottom', labels:{...CHART_DEFAULTS.plugins.legend.labels, boxWidth:6, padding:8, font:{size:9,family:'Inter'}} } },
      scales: {
        x: { ...CHART_DEFAULTS.scales.x, type:'linear', title:{display:true, text:'Generation', color:CHART_COLORS.muted, font:{size:9}} },
        y: { ...CHART_DEFAULTS.scales.y, title:{display:true, text:'Holdout Win Rate %', color:CHART_COLORS.muted, font:{size:9}}, min:50 },
      },
    },
  });
}

function renderHealth(d) {
  const el = document.getElementById('health');
  const items = [
    { label: 'Prediction Error', value: (d.mae * 100).toFixed(1) + '%', color: '' },
    { label: 'Systematic Bias', value: (d.bias * 100).toFixed(1) + '%', color: d.bias < 0.02 ? CHART_COLORS.emerald : '' },
    { label: 'Pass Rate', value: (d.pass_rate * 100).toFixed(0) + '%', color: CHART_COLORS.emerald },
    { label: 'Temporal Bias', value: (d.temporal * 100).toFixed(1) + '%', color: d.temporal < 0.03 ? CHART_COLORS.emerald : '#D8C868' },
  ];
  el.innerHTML = items.map(i => `
    <div>
      <div class="stat-label">${i.label}</div>
      <div class="text-lg font-semibold" ${i.color ? `style="color:${i.color}"` : ''}>${i.value}</div>
    </div>
  `).join('');
}

function renderInsights(data) {
  const el = document.getElementById('insights');
  el.innerHTML = data.slice(0, 6).map(i => {
    const text = i.text.length > 90 ? i.text.slice(0, 90) + '...' : i.text;
    const deltaStr = i.delta ? `+${(i.delta*100).toFixed(1)}%` : '';
    return `
      <div class="p-3 rounded-lg" style="background:#141820;border:1px solid #1E2230">
        <div class="text-xs leading-relaxed" style="color:#8890B0">${text}</div>
        <div class="flex gap-3 mt-1.5">
          <span class="text-xs font-medium" style="color:${CHART_COLORS.violet}">Validated ${i.validated}x</span>
          ${deltaStr ? `<span class="text-xs font-medium" style="color:${CHART_COLORS.emerald}">${deltaStr} WR</span>` : ''}
        </div>
      </div>`;
  }).join('');
}

function renderPopChart(data) {
  const ctx = document.getElementById('popChart').getContext('2d');
  const labels = data.map(d => d.gen);
  if (popChartInstance) popChartInstance.destroy();
  popChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        { label: 'Elite', data: data.map(d => d.elite), borderColor: CHART_COLORS.violet, backgroundColor: CHART_COLORS.violet + '15', fill: true, tension: 0.3, pointRadius: 0, borderWidth: 1.5 },
        { label: 'Viable', data: data.map(d => d.viable), borderColor: CHART_COLORS.sky, backgroundColor: 'transparent', tension: 0.3, pointRadius: 0, borderWidth: 1.5 },
        { label: 'Total', data: data.map(d => d.total), borderColor: CHART_COLORS.muted, backgroundColor: 'transparent', tension: 0.3, pointRadius: 0, borderWidth: 1, borderDash: [4, 2] },
      ]
    },
    options: { ...CHART_DEFAULTS, plugins: { ...CHART_DEFAULTS.plugins, legend: { ...CHART_DEFAULTS.plugins.legend } } }
  });
}

function renderEliteChart(data) {
  const ctx = document.getElementById('eliteChart').getContext('2d');
  const labels = data.map(d => d.gen);
  if (eliteChartInstance) eliteChartInstance.destroy();
  eliteChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'New Elite', data: data.map(d => d.new_elite), backgroundColor: CHART_COLORS.emerald + '60', borderColor: CHART_COLORS.emerald, borderWidth: 1, borderRadius: 2 },
      ]
    },
    options: { ...CHART_DEFAULTS, plugins: { ...CHART_DEFAULTS.plugins, legend: { display: false } } }
  });
}

// ── Top Agents ────────────────────────────────────
// ── Activity Feed + Strategy Diversity ─────────────────────────────
const STRATEGY_COLORS = {
  compression_range_bounce:'#68A8D8', rsi_extreme_reversion:'#f472b6',
  range_extreme_fade:'#68A8D8', ema_crossover_fade:'#D8C868',
  momentum_fade:'#f97316', channel_breakout_fade:'#22d3ee',
  ema_pullback_long:'#a3e635', event_fade:'#f43f5e',
  wick_reversal:'#e879f9', bollinger_squeeze_breakout:'#fb923c',
  wedge_exhaustion_reversal:'#2FCA94', trend_pullback_entry:'#818cf8',
  multi_confirm_bounce:'#14b8a6', vwap_reversion:'#d946ef',
  contrarian_overextension_fade:'#D8C868', keltner_mean_reversion:'#06b6d4',
  volume_exhaustion_reversal:'#ec4899', climax_reversal:'#68A8D8',
  range_reclaim_scalp:'#22B841', intermarket_context_gate:'#f59e0b',
  participation_gate_overlay:'#6366f1', unknown:'#6A7080',
};
const META_COLORS = {
  crossover:'#2FCA94', perturbation:'#68A8D8', feature_guided:'#68A8D8',
  regime_transfer:'#D8C868', random_exploration:'#6A7080', dead_end_avoidance:'#E08878',
  seed_wf08_import:'#d946ef', seed_quant_strategy:'#14b8a6',
};
let _actFeedData = [];

function renderActivityFeed(data) {
  if (data) _actFeedData = data;
  const filter = document.getElementById('feed-filter').value;
  let entries = _actFeedData;
  if (filter === 'elite') entries = entries.filter(e => e.status === 'elite');
  else if (filter === 'viable') entries = entries.filter(e => e.status !== 'reject');
  else if (filter === 'improved') entries = entries.filter(e => e.improved);
  document.getElementById('feed-count').textContent = entries.length + ' agents';
  const el = document.getElementById('activity-feed');
  el.innerHTML = entries.slice(0, 80).map(e => {
    const sc = STRATEGY_COLORS[e.strategy] || '#6A7080';
    const mc = META_COLORS[e.meta_strategy] || '#6A7080';
    const wrColor = e.status === 'elite' ? '#2FCA94' : e.status === 'viable' ? '#68A8D8' : '#8890B0';
    const statusBadge = e.status === 'elite' ? '<span class="badge badge-emerald">ELITE</span>'
      : e.status === 'viable' ? '<span class="badge badge-sky">VIABLE</span>'
      : '<span class="badge badge-muted">' + (e.eval_stage === 'quick_reject' ? 'QUICK' : e.eval_stage === 'medium_reject' ? 'MED' : 'SUB') + '</span>';
    const impBadge = e.improved ? ' <span style="color:#34d399;font-size:0.65rem">&#9650;</span>' : '';
    return '<div class="act-entry" style="border-left-color:' + mc + '">' +
      '<div class="flex items-center justify-between">' +
        '<div class="flex items-center gap-2">' +
          '<span class="act-mono" style="color:#8890B0">' + e.agent + '</span>' +
          '<span style="font-size:0.65rem;color:#6A7080">Gen ' + e.gen + '</span>' +
          '<span style="font-size:0.6rem;color:' + mc + '">' + e.meta_strategy.replace(/_/g,' ') + '</span>' +
          (e.parent ? '<span style="font-size:0.6rem;color:#6A7080">&larr; ' + e.parent + '</span>' : '') +
        '</div>' +
        '<div class="flex items-center gap-2">' + statusBadge + impBadge + '</div>' +
      '</div>' +
      '<div class="flex items-center gap-2 mt-0.5">' +
        '<span style="font-size:0.7rem;font-weight:600;color:' + sc + '">' + e.strategy.replace(/_/g,' ') + '</span>' +
        '<span class="badge badge-muted" style="font-size:0.6rem">' + e.asset + '/' + e.tf + '</span>' +
        '<span style="font-size:0.75rem;font-weight:700;color:' + wrColor + '">' + (e.wr * 100).toFixed(1) + '%</span>' +
        '<span style="font-size:0.65rem;color:#6A7080">' + e.trades + 't</span>' +
      '</div>' +
    '</div>';
  }).join('');
}

function renderStrategyDiversity(data) {
  // Diversity index
  const idx = data.diversity_index;
  const idxEl = document.getElementById('diversity-index');
  idxEl.textContent = idx.toFixed(3);
  idxEl.style.color = idx > 0.5 ? '#2FCA94' : idx > 0.3 ? '#D8C868' : '#E08878';

  // Stacked bar
  const bar = document.getElementById('strategy-bar');
  bar.innerHTML = '';
  const strats = Object.entries(data.strategies);
  strats.forEach(([sid, s]) => {
    if (s.pct < 0.005) return;
    const seg = document.createElement('div');
    seg.className = 'strat-bar-seg';
    seg.style.width = (s.pct * 100) + '%';
    seg.style.background = STRATEGY_COLORS[sid] || '#6A7080';
    seg.setAttribute('data-tip', sid.replace(/_/g,' ') + ': ' + s.count);
    bar.appendChild(seg);
  });

  // Strategy list
  const list = document.getElementById('strategy-list');
  const maxCount = strats.length ? strats[0][1].count : 1;
  list.innerHTML = strats.map(([sid, s]) => {
    const c = STRATEGY_COLORS[sid] || '#6A7080';
    const wrColor = s.avg_wr >= 0.58 ? '#2FCA94' : s.avg_wr >= 0.52 ? '#68A8D8' : '#8890B0';
    return '<div class="flex items-center gap-2" style="font-size:0.75rem">' +
      '<div style="width:8px;height:8px;border-radius:50%;background:' + c + ';flex-shrink:0"></div>' +
      '<div style="flex:1;min-width:0">' +
        '<div class="flex items-center justify-between">' +
          '<span style="color:#F0F0F4;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + sid.replace(/_/g,' ') + '</span>' +
          '<span style="color:#6A7080;flex-shrink:0">' + s.count + '</span>' +
        '</div>' +
        '<div class="flex items-center gap-3" style="color:#6A7080;font-size:0.65rem">' +
          '<span>avg <span style="color:' + wrColor + ';font-weight:600">' + (s.avg_wr * 100).toFixed(1) + '%</span></span>' +
          '<span>best <span style="color:#2FCA94">' + (s.best_wr * 100).toFixed(1) + '%</span></span>' +
          '<span>elite ' + s.elite_count + '</span>' +
          '<span>new ' + s.recent_births + '</span>' +
        '</div>' +
      '</div>' +
    '</div>';
  }).join('');
}

function renderMutationActivity(data) {
  const el = document.getElementById('mutation-activity');
  if (!data) { el.innerHTML = ''; return; }
  const maxA = data.most_added.length ? data.most_added[0][1] : 1;
  const maxR = data.most_removed.length ? data.most_removed[0][1] : 1;
  const renderCol = (title, items, max, rmClass) =>
    '<div>' +
    '<div style="font-size:0.7rem;font-weight:600;color:#8890B0;margin-bottom:6px">' + title + '</div>' +
    items.map(([k, v]) =>
      '<div style="margin-bottom:3px">' +
        '<div class="flex items-center justify-between" style="font-size:0.65rem;color:#6A7080">' +
          '<span>' + k.replace(/^cr_/, '').replace(/_/g,' ') + '</span><span>' + v + '</span>' +
        '</div>' +
        '<div class="mut-bar' + (rmClass ? ' mut-bar-rm' : '') + '" style="width:' + Math.round(v / max * 100) + '%"></div>' +
      '</div>'
    ).join('') +
    '</div>';
  el.innerHTML = renderCol('Most Added', data.most_added, maxA, false) +
                 renderCol('Most Removed', data.most_removed, maxR, true);
}

// ── Agent Table ───────────────────────────────────────────────────
let currentTab = 'session';
let agentsData = [];
let agentsTotal = 0;
let sortField = 'wr';
let sortAsc = false;
let pageSize = 20;

async function switchTab(period) {
  currentTab = period;
  document.querySelectorAll('#agent-tabs .tab-btn').forEach(b => {
    b.classList.toggle('tab-active', b.dataset.tab === period);
  });
  await loadAgents();
}

function setPageSize(n) {
  pageSize = n;
  document.querySelectorAll('.page-btn').forEach(b => {
    b.classList.toggle('tab-active', b.dataset.size === String(n));
  });
  renderAgents();
}

async function loadAgents() {
  const data = await fetchJSON('/api/top-agents?period=' + currentTab);
  if (data && data.agents) { agentsData = data.agents; agentsTotal = data.total; populateFilters(); renderAgents(); }
}

function fillSelect(id, values, defaultLabel) {
  const sel = document.getElementById(id);
  const cur = sel.value;
  sel.innerHTML = '<option value="">' + defaultLabel + '</option>' +
    values.map(v => '<option value="' + v + '"' + (v === cur ? ' selected' : '') + '>' + v.replace(/_/g, ' ') + '</option>').join('');
}

function populateFilters() {
  const strats = [...new Set(agentsData.map(a => a.strategy))].filter(Boolean).sort();
  const assets = [...new Set(agentsData.map(a => (a.asset||'').split(' ')[0]).filter(Boolean))].sort();
  const tfs = [...new Set(agentsData.map(a => a.tf || '?'))].sort();
  const methods = [...new Set(agentsData.map(a => a.method))].filter(Boolean).sort();
  fillSelect('filter-strategy', strats, 'All Strategies');
  fillSelect('filter-asset', assets, 'All Assets');
  fillSelect('filter-tf', tfs, 'All Timeframes');
  fillSelect('filter-method', methods, 'All Methods');
}

function clearFilters() {
  document.getElementById('filter-strategy').value = '';
  document.getElementById('filter-asset').value = '';
  document.getElementById('filter-tf').value = '';
  document.getElementById('filter-method').value = '';
  renderAgents();
}

function sortAgents(field) {
  if (sortField === field) { sortAsc = !sortAsc; } else { sortField = field; sortAsc = false; }
  renderAgents();
}

function renderAgents() {
  // Apply filters
  let filtered = agentsData;
  const fStrat = document.getElementById('filter-strategy').value;
  const fAsset = document.getElementById('filter-asset').value;
  const fTf = document.getElementById('filter-tf').value;
  const fMethod = document.getElementById('filter-method').value;
  if (fStrat) filtered = filtered.filter(a => a.strategy === fStrat);
  if (fAsset) filtered = filtered.filter(a => (a.asset||'').split(' ')[0] === fAsset);
  if (fTf) filtered = filtered.filter(a => a.tf === fTf);
  if (fMethod) filtered = filtered.filter(a => a.method === fMethod);

  const sorted = [...filtered].sort((a, b) => {
    const va = a[sortField] || 0, vb = b[sortField] || 0;
    return sortAsc ? va - vb : vb - va;
  }).slice(0, pageSize);
  const tbody = document.getElementById('agents-body');
  tbody.innerHTML = sorted.map((a, i) => {
    const wr = (a.wr * 100).toFixed(1);
    const wrColor = a.wr >= 0.70 ? CHART_COLORS.emerald : a.wr >= 0.65 ? CHART_COLORS.sky : a.wr >= 0.60 ? CHART_COLORS.violet : '#8890B0';
    const wf = typeof a.wf === 'number' ? a.wf.toFixed(1) : a.wf;
    const sharpe = typeof a.sharpe === 'number' ? a.sharpe.toFixed(2) : '--';
    const dd = typeof a.drawdown === 'number' ? (a.drawdown * 100).toFixed(1) + '%' : '--';
    const strat = (a.strategy || '').replace(/_/g, ' ');
    const method = (a.method || '').replace(/_/g, ' ');
    const guardHtml = (a.guards || []).map(g => {
      const k = g[0].replace(/^cr_/, '').replace(/_/g, ' ');
      return '<span class="guard-tag">' + k + '=' + g[1] + '</span>';
    }).join('');
    const rank = i + 1;
    const rankBadge = rank <= 3 ? '<span style="color:' + CHART_COLORS.emerald + ';font-weight:700">' + rank + '</span>' : rank;
    // Paper trade column
    let ptHtml;
    if (a.pt_wr != null) {
      const ptWr = (a.pt_wr * 100).toFixed(1);
      const ptDelta = a.pt_delta != null ? a.pt_delta : (a.pt_wr - a.wr);
      const deltaSign = ptDelta >= 0 ? '+' : '';
      const deltaColor = ptDelta >= 0 ? CHART_COLORS.emerald : '#E08878';
      ptHtml = '<span style="color:' + CHART_COLORS.emerald + ';font-weight:700">' + ptWr + '%</span>' +
        '<span style="font-size:0.65rem;margin-left:4px;color:' + deltaColor + '">' + deltaSign + (ptDelta*100).toFixed(1) + '%</span>' +
        '<span style="font-size:0.6rem;margin-left:3px;color:#6A7080">' + a.pt_trades + 't</span>';
    } else {
      ptHtml = '<span style="color:#6A7080;font-size:0.75rem">--</span>';
    }

    return '<tr>' +
      '<td>' + rankBadge + '</td>' +
      '<td style="color:' + wrColor + ';font-weight:700;font-size:0.875rem">' + wr + '%</td>' +
      '<td>' + ptHtml + '</td>' +
      '<td style="font-family:DM Mono,monospace;font-size:0.75rem;color:#8890B0">' + a.agent + '</td>' +
      '<td>' + a.gen + '</td>' +
      '<td style="font-size:0.8rem">' + strat + '</td>' +
      '<td>' + (a.asset || '').split(' ')[0] + '</td>' +
      '<td style="font-size:0.8rem">' + (a.tf || '?') + '</td>' +
      '<td>' + wf + '</td>' +
      '<td>' + a.trades + '</td>' +
      '<td>' + sharpe + '</td>' +
      '<td>' + dd + '</td>' +
      '<td><span class="badge badge-' + (a.validation === '5/5' ? 'emerald' : 'sky') + '">' + a.validation + '</span></td>' +
      '<td style="font-size:0.75rem;color:#8890B0">' + method + '</td>' +
      '<td>' + guardHtml + '</td>' +
      '</tr>';
  }).join('');
  const countEl = document.getElementById('agents-count');
  const periodLabel = {session:'this session', today:'today', week:'this week', all:'all time'}[currentTab] || currentTab;
  const filterNote = (fStrat || fAsset || fTf || fMethod) ? ' (filtered from ' + agentsData.length + ')' : '';
  if (countEl) countEl.textContent = 'Showing ' + sorted.length + ' of ' + filtered.length + ' elite agents (' + periodLabel + ')' + filterNote;
}

// ── Live Paper Trading renderer ─────────────────────────────────────
let _livePeriod = 'alltime';
let _lastLivePtData = null;

const REGIME_COLORS = {
  compression: '#68A8D8',
  range: '#68A8D8',
  trend: '#D8C868',
  event_driven: '#f43f5e',
  high_vol: '#f97316',
  fear_shock: '#E08878',
};

function regimeBadge(regime) {
  const c = REGIME_COLORS[regime] || '#6A7080';
  return '<span style="display:inline-block;padding:1px 6px;border-radius:3px;font-size:0.65rem;font-weight:600;background:' + c + '22;color:' + c + '">' + (regime || '?').replace(/_/g, ' ') + '</span>';
}

function tfBadge(tf) {
  const colors = { '15m': '#68A8D8', '1h': '#68A8D8', '4h': '#D8C868' };
  const c = colors[tf] || '#6A7080';
  return '<span style="display:inline-block;padding:1px 5px;border-radius:3px;font-size:0.6rem;font-weight:700;background:' + c + '22;color:' + c + '">' + (tf || '?') + '</span>';
}

// Set up period tab clicks (once)
document.addEventListener('DOMContentLoaded', function() {
  const tabs = document.getElementById('live-period-tabs');
  if (!tabs) return;
  tabs.addEventListener('click', function(e) {
    const btn = e.target.closest('.live-period-tab');
    if (!btn) return;
    _livePeriod = btn.dataset.period;
    tabs.querySelectorAll('.live-period-tab').forEach(t => {
      t.style.background = 'transparent';
      t.style.color = '#6A7080';
    });
    btn.style.background = '#222430';
    btn.style.color = '#F0F0F4';
    if (_lastLivePtData) renderLivePt(_lastLivePtData);
  });
});

function renderLivePt(data) {
  if (!data) return;
  _lastLivePtData = data;
  const section = document.getElementById('live-pt-section');
  if (!section) return;

  // Status badge
  const statusBadge = document.getElementById('live-pt-status-badge');
  if (data.status === 'running') {
    statusBadge.innerHTML = '<span class="badge badge-emerald">LIVE</span>';
  } else {
    statusBadge.innerHTML = '<span class="badge badge-sky">OFFLINE</span>';
  }

  // Updated time
  const updatedEl = document.getElementById('live-pt-updated');
  if (data.last_updated) {
    const d = new Date(data.last_updated);
    updatedEl.textContent = d.toLocaleTimeString();
  }

  // Period stats
  const ps = (data.period_stats || {})[_livePeriod] || {};
  document.getElementById('live-settlements').textContent = ps.settlements || 0;
  document.getElementById('live-trades-count').textContent = ps.trades || 0;
  document.getElementById('live-wins-count').textContent = ps.wins || 0;
  document.getElementById('live-losses-count').textContent = ps.losses || 0;
  const acc = ps.accuracy || 0;
  const accEl = document.getElementById('live-accuracy');
  accEl.textContent = ps.trades > 0 ? acc + '%' : '--';
  accEl.style.color = acc >= 50 ? '#2FCA94' : (ps.trades > 0 ? '#E08878' : '#6A7080');
  document.getElementById('live-agents-strats').textContent =
    (data.agents_loaded || 0) + ' / ' + (data.strategies_loaded || 0);

  // Current contracts (multi-timeframe)
  const contractsDiv = document.getElementById('live-contracts');
  const contracts = data.current_contracts || {};
  const contractKeys = Object.keys(contracts).sort();
  if (contractKeys.length > 0) {
    contractsDiv.innerHTML = contractKeys.map(key => {
      const c = contracts[key];
      const preds = c.predictions || {};
      const predEntries = Object.entries(preds);
      const longs = predEntries.filter(([,p]) => p === 'up').length;
      const shorts = predEntries.filter(([,p]) => p === 'down').length;
      const skips = predEntries.filter(([,p]) => p === 'skip').length;
      const parts = key.split(':');
      const asset = parts[0] || '?';
      const tf = c.timeframe || parts[1] || '?';
      const regime = c.regime || 'unknown';
      const matched = (c.strategies_matched || []).length;
      return '<div class="card p-3" style="background:#141820">' +
        '<div class="flex items-center justify-between mb-2">' +
          '<div class="flex items-center gap-2">' +
            '<span class="text-xs font-semibold" style="color:#F0F0F4">' + asset + '</span>' +
            tfBadge(tf) + regimeBadge(regime) +
          '</div>' +
          '<span class="text-xs" style="color:#6A7080">' + matched + ' strategies</span>' +
        '</div>' +
        '<div class="flex items-center gap-2">' +
          '<span style="font-size:0.75rem;color:#6A7080">$' + (c.open_price || 0).toLocaleString(undefined, {minimumFractionDigits:2}) + '</span>' +
          '<span style="margin-left:auto"></span>' +
          (longs > 0 ? '<span class="badge badge-emerald">' + longs + ' LONG</span>' : '') +
          (shorts > 0 ? '<span class="badge" style="background:rgba(224,136,120,0.15);color:#E08878;font-size:0.65rem;padding:2px 6px;border-radius:4px">' + shorts + ' SHORT</span>' : '') +
          '<span style="font-size:0.65rem;color:#6A7080">' + skips + ' skip</span>' +
        '</div></div>';
    }).join('');
  } else if (data.status !== 'running') {
    contractsDiv.innerHTML = '<div style="padding:12px;text-align:center;color:#6A7080;font-size:0.8rem">Start: <span style="font-family:DM Mono,monospace;color:#8890B0">python live_paper_trader.py --assets BTC --per-strategy 3</span></div>';
  } else {
    contractsDiv.innerHTML = '<div style="padding:8px;text-align:center;color:#6A7080;font-size:0.8rem">Waiting for next boundary...</div>';
  }

  // Regime history strip
  const rhDiv = document.getElementById('live-regime-history');
  const rh = data.regime_history || [];
  if (rh.length > 0) {
    rhDiv.innerHTML = rh.map(r => {
      const c = REGIME_COLORS[r] || '#6A7080';
      return '<span title="' + r + '" style="display:inline-block;width:18px;height:18px;border-radius:4px;background:' + c + '33;border:1px solid ' + c + '66"></span>';
    }).join('') +
    '<span style="font-size:0.65rem;color:#6A7080;margin-left:6px">latest: ' + (rh[rh.length-1] || '?').replace(/_/g,' ') + '</span>';
  } else {
    rhDiv.innerHTML = '<span style="font-size:0.7rem;color:#6A7080">No regime data yet</span>';
  }

  // Strategy performance table
  const stratStats = ps.strategy_stats || {};
  const strategies = data.strategies || {};
  const stratTbody = document.getElementById('live-strategy-table');
  const stratRows = Object.keys(strategies).sort((a, b) => {
    return (stratStats[b] || {}).trades - (stratStats[a] || {}).trades || 0;
  });
  if (stratRows.length > 0) {
    stratTbody.innerHTML = stratRows.map(sid => {
      const info = strategies[sid] || {};
      const ss = stratStats[sid] || { trades: 0, wins: 0, skips: 0 };
      const losses = ss.trades - ss.wins;
      const wr = ss.trades > 0 ? (ss.wins / ss.trades * 100).toFixed(1) + '%' : '--';
      const wrColor = ss.trades > 0 ? (ss.wins/ss.trades >= 0.5 ? '#2FCA94' : '#E08878') : '#6A7080';
      const regimes = (info.regimes || []).map(r => regimeBadge(r)).join(' ');
      return '<tr style="border-bottom:1px solid #1E2230">' +
        '<td class="py-1 pr-4" style="font-size:0.8rem">' + sid.replace(/_/g, ' ') + '</td>' +
        '<td class="py-1 pr-4" style="color:#8890B0">' + (info.agents || 0) + '</td>' +
        '<td class="py-1 pr-4" style="color:#38bdf8">' + ss.trades + '</td>' +
        '<td class="py-1 pr-4" style="color:#2FCA94">' + ss.wins + '</td>' +
        '<td class="py-1 pr-4" style="color:#E08878">' + losses + '</td>' +
        '<td class="py-1 pr-4" style="font-weight:700;color:' + wrColor + '">' + wr + '</td>' +
        '<td class="py-1" style="font-size:0.7rem">' + regimes + '</td>' +
        '</tr>';
    }).join('');
  } else {
    stratTbody.innerHTML = '<tr><td colspan="7" style="padding:12px;text-align:center;color:#6A7080">No strategies loaded</td></tr>';
  }

  // Agent performance table
  const agentStats = data.agent_stats || {};
  const agentRows = Object.entries(agentStats).sort((a, b) => (b[1].live_trades || 0) - (a[1].live_trades || 0));
  const agentTbody = document.getElementById('live-agent-table');
  if (agentRows.length > 0) {
    agentTbody.innerHTML = agentRows.map(([aid, s]) => {
      const btWr = (s.bt_wr * 100).toFixed(1);
      const liveWr = s.live_trades > 0 ? (s.live_wr * 100).toFixed(1) + '%' : '--';
      const delta = s.live_trades > 0 ? ((s.delta >= 0 ? '+' : '') + (s.delta * 100).toFixed(1) + '%') : '--';
      const deltaColor = s.delta >= 0 ? CHART_COLORS.emerald : '#E08878';
      const strat = (s.strategy || '').replace(/_/g, ' ');
      const tf = s.timeframe || '?';
      return '<tr style="border-bottom:1px solid #1E2230">' +
        '<td class="py-1 pr-4" style="font-family:DM Mono,monospace;font-size:0.75rem;color:#8890B0">' + aid + '</td>' +
        '<td class="py-1 pr-4" style="font-size:0.8rem">' + strat + '</td>' +
        '<td class="py-1 pr-4">' + tfBadge(tf) + '</td>' +
        '<td class="py-1 pr-4">' + btWr + '%</td>' +
        '<td class="py-1 pr-4" style="font-weight:700;color:' + (s.live_trades > 0 ? CHART_COLORS.emerald : '#6A7080') + '">' + liveWr + '</td>' +
        '<td class="py-1 pr-4" style="color:' + (s.live_trades > 0 ? deltaColor : '#6A7080') + '">' + delta + '</td>' +
        '<td class="py-1 pr-4">' + (s.live_trades || 0) + '</td>' +
        '<td class="py-1 pr-4">' + (s.live_wins || 0) + '</td>' +
        '<td class="py-1">' + (s.skips || 0) + '</td>' +
        '</tr>';
    }).join('');
  } else {
    agentTbody.innerHTML = '<tr><td colspan="9" style="padding:12px;text-align:center;color:#6A7080">No agents loaded yet</td></tr>';
  }

  // Recent settlements
  const settlementsDiv = document.getElementById('live-settlements-list');
  const settlements = (data.recent_settlements || []).reverse();
  if (settlements.length > 0) {
    settlementsDiv.innerHTML = settlements.map(s => {
      const agents = s.agents || {};
      const trades = Object.values(agents).filter(a => a.prediction !== 'skip');
      const correct = trades.filter(a => a.correct).length;
      const total = trades.length;
      const accuracy = total > 0 ? (correct / total * 100).toFixed(0) : 0;
      const dirColor = s.direction === 'up' ? CHART_COLORS.emerald : '#E08878';
      const priceDelta = s.close_price && s.open_price ? ((s.close_price - s.open_price) / s.open_price * 100).toFixed(3) : '?';
      const ts = new Date(s.ts).toLocaleTimeString();
      const tf = s.timeframe || '15m';
      const regime = s.regime || '';
      const tradingStrats = [...new Set(trades.map(t => t.strategy).filter(Boolean))];
      return '<div class="flex items-center gap-2 py-1" style="border-bottom:1px solid #1E2230;font-size:0.75rem">' +
        '<span style="color:#6A7080;min-width:60px">' + ts + '</span>' +
        '<span style="font-weight:600;min-width:28px">' + (s.asset || '?') + '</span>' +
        tfBadge(tf) +
        (regime ? regimeBadge(regime) : '') +
        '<span style="color:' + dirColor + ';font-weight:700;min-width:35px">' + (s.direction || '?').toUpperCase() + '</span>' +
        '<span style="color:#6A7080">' + priceDelta + '%</span>' +
        (tradingStrats.length > 0 ? '<span style="font-size:0.65rem;color:#6A7080">' + tradingStrats.map(s=>s.replace(/_/g,' ')).join(', ') + '</span>' : '') +
        '<span style="margin-left:auto;color:' + (total > 0 && correct/total >= 0.5 ? CHART_COLORS.emerald : (total > 0 ? '#E08878' : '#6A7080')) + '">' +
          (total > 0 ? correct + '/' + total + ' (' + accuracy + '%)' : 'all skip') +
        '</span>' +
        '</div>';
    }).join('');
  } else {
    settlementsDiv.innerHTML = '<div style="padding:8px;text-align:center;color:#6A7080;font-size:0.75rem">No settlements yet</div>';
  }
}

// ── Autoloop rendering ────────────────────────────
let alCycleChartInstance = null;

function renderAutoloop(data) {
  if (!data) return;
  const s = data.state || {};
  const doc = data.doctrine || {};
  const bt = data.backtest || {};
  const pt = data.paper_trade || {};

  // Status badge
  const badge = document.getElementById('autoloop-status-badge');
  const st = s.status || 'unknown';
  badge.textContent = st;
  badge.style.color = st === 'running' ? '#2FCA94' : st === 'idle' ? '#E8B86D' : '#6A7080';
  badge.style.borderColor = st === 'running' ? '#2FCA94' : st === 'idle' ? '#E8B86D' : '#2A2E3C';
  badge.style.border = '1px solid';

  // Cycle + noop
  document.getElementById('al-cycle').textContent = s.cycle_count || 0;
  document.getElementById('al-noop').textContent = s.noop_streak || 0;

  // Learning lane
  document.getElementById('al-doctrine-cards').textContent = doc.card_count || 0;
  document.getElementById('al-doctrine-packets').textContent = doc.packet_count || 0;

  // Backtest lane
  document.getElementById('al-bt-candidates').textContent = bt.candidate_count || 0;
  document.getElementById('al-variety').textContent = bt.variety_count || 0;
  document.getElementById('al-trials').textContent = bt.trial_count || 0;

  // Paper trade lane
  document.getElementById('al-pt-queue').textContent = pt.queue_count || 0;
  document.getElementById('al-pt-ready').textContent = pt.promotion_ready || 0;
  document.getElementById('al-pt-sig').textContent = pt.significant || 0;

  // Cycle timeline chart
  const timeline = data.cycle_timeline || [];
  if (timeline.length > 0) {
    const labels = timeline.map(c => 'C' + c.cycle);
    const learningData = timeline.map(c => c.learning ? 1 : 0);
    const backtestData = timeline.map(c => c.backtest ? 1 : 0);
    const ptData = timeline.map(c => c.paper_trade ? 1 : 0);

    document.getElementById('al-timeline-range').textContent =
      '(C' + timeline[0].cycle + ' - C' + timeline[timeline.length-1].cycle + ')';

    if (alCycleChartInstance) alCycleChartInstance.destroy();
    const ctx = document.getElementById('al-cycle-chart').getContext('2d');
    alCycleChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          { label: 'Learning', data: learningData, backgroundColor: '#2FCA94', barPercentage: 0.8 },
          { label: 'Backtest', data: backtestData, backgroundColor: '#68A8D8', barPercentage: 0.8 },
          { label: 'Paper Trade', data: ptData, backgroundColor: '#E8B86D', barPercentage: 0.8 },
        ]
      },
      options: {
        ...CHART_DEFAULTS,
        plugins: { legend: { display: true, position: 'top',
          labels: { color: '#6A7080', boxWidth: 8, padding: 8, font: { size: 10, family: 'DM Sans' } }
        }},
        scales: {
          x: { stacked: true, grid: { display: false }, ticks: { color: '#6A7080', font: { size: 9, family: 'DM Mono' }, maxRotation: 0 } },
          y: { stacked: true, display: false, max: 3 },
        }
      }
    });
  }

  // Top candidates table
  const tbody = document.getElementById('al-candidates-table');
  const cands = bt.candidates || [];
  if (cands.length > 0) {
    tbody.innerHTML = cands.map(c => {
      const wr = (c.wr * 100).toFixed(1);
      const wrColor = c.wr >= 0.6 ? '#2FCA94' : c.wr >= 0.5 ? '#68A8D8' : '#6A7080';
      const wf = c.wf ? c.wf.toFixed(2) : '--';
      const dd = c.dd ? (c.dd * 100).toFixed(1) + '%' : '--';
      const ready = c.readiness ? (c.readiness >= 0.8 ? 'Yes' : 'No') : '--';
      const readyColor = c.readiness >= 0.8 ? '#2FCA94' : '#6A7080';
      const name = c.id.replace(/_/g, ' ').substring(0, 30);
      return '<tr style="border-bottom:1px solid #1E2230">' +
        '<td class="py-1 text-left" style="color:#8890B0">' + name + '</td>' +
        '<td class="py-1 text-right font-mono" style="color:' + wrColor + '">' + wr + '%</td>' +
        '<td class="py-1 text-right font-mono" style="color:#8890B0">' + wf + '</td>' +
        '<td class="py-1 text-right font-mono" style="color:#8890B0">' + dd + '</td>' +
        '<td class="py-1 text-right font-mono" style="color:#8890B0">' + (c.trades || '--') + '</td>' +
        '<td class="py-1 text-right font-mono" style="color:' + readyColor + '">' + ready + '</td>' +
        '</tr>';
    }).join('');
  } else {
    tbody.innerHTML = '<tr><td colspan="6" class="py-2 text-center" style="color:#6A7080">No candidates yet — run backtest loop</td></tr>';
  }

  // Recent doctrine cards
  const docList = document.getElementById('al-doctrine-list');
  const recentCards = doc.recent_cards || [];
  if (recentCards.length > 0) {
    docList.innerHTML = recentCards.map(c => {
      const doctrine = (c.doctrine || '').replace(/_/g, ' ');
      const strategy = (c.strategy || '').replace(/_/g, ' ');
      const regime = c.regime || '';
      const title = c.title || '';
      return '<div class="card px-3 py-2" style="background:#141820;min-width:180px;max-width:280px">' +
        '<div class="text-xs font-semibold" style="color:#2FCA94">' + doctrine + '</div>' +
        '<div class="text-xs" style="color:#8890B0">' + strategy + '</div>' +
        (regime ? '<div class="text-xs mt-0.5" style="color:#6A7080">regime: ' + regime + '</div>' : '') +
        (title ? '<div class="text-xs mt-1 truncate" style="color:#6A7080;max-width:260px" title="' + title.replace(/"/g,'&quot;') + '">' + title.substring(0, 60) + (title.length > 60 ? '...' : '') + '</div>' : '') +
        '</div>';
    }).join('');
  } else {
    docList.innerHTML = '<div class="text-xs" style="color:#6A7080">No doctrine cards yet — run learning loop</div>';
  }
}

// ── Main loop ─────────────────────────────────────
async function refresh() {
  const [status, elites, popHist, pt, ptDash, health, insights, livePt, actFeed, stratDiv, autoloop] = await Promise.all([
    fetchJSON('/api/status'),
    fetchJSON('/api/recent-elites'),
    fetchJSON('/api/population-history'),
    fetchJSON('/api/paper-trade'),
    fetchJSON('/api/pt-dashboard'),
    fetchJSON('/api/health'),
    fetchJSON('/api/insights'),
    fetchJSON('/api/live-pt'),
    fetchJSON('/api/activity-feed?n=80'),
    fetchJSON('/api/strategy-diversity'),
    fetchJSON('/api/autoloop-status'),
  ]);

  if (status) { renderMetrics(status); renderMethods(status.methods || {}); }
  if (elites) renderFeed(elites);
  if (popHist && popHist.length) { renderPopChart(popHist); renderEliteChart(popHist); }
  if (pt) renderPaperTrade(pt);
  if (ptDash) renderPtDashboard(ptDash);
  if (health) renderHealth(health);
  if (insights) renderInsights(insights);
  renderLivePt(livePt);
  if (actFeed) renderActivityFeed(actFeed.entries);
  if (stratDiv) { renderStrategyDiversity(stratDiv); renderMutationActivity(stratDiv.mutation_activity); }
  if (autoloop) renderAutoloop(autoloop);

  // Refresh agents table
  await loadAgents();

  document.getElementById('clock').textContent = new Date().toLocaleTimeString();
  document.getElementById('footer-status').textContent = 'Last update: ' + new Date().toLocaleTimeString();
}

// Run on load and every 10 seconds
refresh();
setInterval(refresh, 10000);
</script>
</body>
</html>
"""


EVOLUTION_VIZ_PAGE = r"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Evolution Graph - Spark Domain Chip</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://d3js.org/d3.v7.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
  body { margin:0; background:#0E1018; color:#F0F0F4; font-family:'DM Sans',system-ui,sans-serif; display:flex; flex-direction:column; height:100vh; }
  .ctrl-bar { padding:12px 20px; border-bottom:1px solid #222430; display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
  .ctrl-input { background:#141820; border:1px solid #222430; color:#8890B0; font-size:0.75rem; padding:5px 8px; border-radius:6px; font-family:'DM Sans',system-ui,sans-serif; }
  .ctrl-input:focus { outline:1px solid #2A2E3C; }
  .ctrl-label { font-size:0.7rem; color:#6A7080; }
  .ctrl-btn { padding:5px 16px; border-radius:6px; font-size:0.75rem; font-weight:600; background:#222430; color:#F0F0F4; border:1px solid #2A2E3C; cursor:pointer; transition:all 0.2s; }
  .ctrl-btn:hover { background:#2A2E3C; }
  #tooltip { display:none; position:absolute; background:#141820; border:1px solid #2A2E3C; border-radius:8px; padding:12px; font-size:0.75rem; pointer-events:none; z-index:100; max-width:300px; border-color:#2A2E3C; }
  .badge-e { background:#14161E; border:1px solid #222430; color:#3DDDA4; padding:1px 6px; border-radius:4px; font-size:0.65rem; font-weight:600; }
  .badge-v { background:#14161E; border:1px solid #222430; color:#68A8D8; padding:1px 6px; border-radius:4px; font-size:0.65rem; font-weight:600; }
  .badge-s { background:#222430; color:#8890B0; padding:1px 6px; border-radius:4px; font-size:0.65rem; }
  .legend-dot { width:10px; height:10px; border-radius:50%; display:inline-block; }
</style>
</head>
<body>
<!-- Header -->
<div class="ctrl-bar" style="border-bottom-width:2px">
  <a href="/" style="color:#6A7080;text-decoration:none;font-size:0.8rem" onmouseover="this.style.color='#2FCA94'" onmouseout="this.style.color='#6A7080'">&larr; Dashboard</a>
  <h1 style="font-size:1.25rem;font-weight:700;margin:0">Strategy Evolution Graph</h1>
  <div style="margin-left:auto;display:flex;gap:12px;align-items:center">
    <span class="ctrl-label" id="viz-nodes">-- nodes</span>
    <span class="ctrl-label" id="viz-edges">-- edges</span>
    <span class="ctrl-label" id="viz-gens">Gen --</span>
  </div>
</div>

<!-- Controls -->
<div class="ctrl-bar" style="background:#0E1018">
  <div style="display:flex;align-items:center;gap:6px">
    <span class="ctrl-label">Gen Range:</span>
    <input type="number" id="c-gen-start" class="ctrl-input" style="width:72px" placeholder="start">
    <span style="color:#6A7080">-</span>
    <input type="number" id="c-gen-end" class="ctrl-input" style="width:72px" placeholder="end">
  </div>
  <div style="display:flex;align-items:center;gap:6px">
    <span class="ctrl-label">Min WR:</span>
    <input type="range" id="c-min-wr" min="0" max="75" value="0" step="1" style="width:90px;accent-color:#a78bfa">
    <span class="ctrl-label" id="c-min-wr-lbl">0%</span>
  </div>
  <div style="display:flex;align-items:center;gap:6px">
    <span class="ctrl-label">Strategy:</span>
    <select id="c-strategy" class="ctrl-input" style="min-width:140px"><option value="">All</option></select>
  </div>
  <div style="display:flex;align-items:center;gap:6px">
    <span class="ctrl-label">Layout:</span>
    <select id="c-layout" class="ctrl-input">
      <option value="force">Force</option>
      <option value="timeline">Timeline</option>
    </select>
  </div>
  <div style="display:flex;align-items:center;gap:6px">
    <span class="ctrl-label">Effects:</span>
    <select id="c-effects" class="ctrl-input">
      <option value="full">Full</option>
      <option value="subtle" selected>Subtle</option>
      <option value="off">Off</option>
    </select>
  </div>
  <button onclick="loadGraph()" class="ctrl-btn" style="margin-left:auto">Load Graph</button>
</div>

<!-- Canvas -->
<div id="graph-wrap" style="flex:1;position:relative;overflow:hidden">
  <canvas id="gc"></canvas>
  <div id="tooltip"></div>
  <div id="loading" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#6A7080;font-size:0.85rem">
    Click "Load Graph" to visualize evolution
  </div>
</div>

<!-- Legend -->
<div class="ctrl-bar" style="gap:10px;flex-wrap:wrap;padding:8px 20px" id="legend"></div>

<script>
const STRATEGY_COLORS = {
  compression_range_bounce:'#68A8D8', rsi_extreme_reversion:'#f472b6',
  range_extreme_fade:'#68A8D8', ema_crossover_fade:'#D8C868',
  momentum_fade:'#f97316', channel_breakout_fade:'#22d3ee',
  ema_pullback_long:'#a3e635', event_fade:'#f43f5e',
  wick_reversal:'#e879f9', bollinger_squeeze_breakout:'#fb923c',
  wedge_exhaustion_reversal:'#2FCA94', trend_pullback_entry:'#818cf8',
  multi_confirm_bounce:'#14b8a6', vwap_reversion:'#d946ef',
  contrarian_overextension_fade:'#D8C868', keltner_mean_reversion:'#06b6d4',
  volume_exhaustion_reversal:'#ec4899', climax_reversal:'#68A8D8',
  range_reclaim_scalp:'#22B841', intermarket_context_gate:'#f59e0b',
  participation_gate_overlay:'#6366f1',
};

let simulation = null;
let transform = d3.zoomIdentity;
let graphNodes = [];
let graphEdges = [];
let hoveredNode = null;
let animating = false;
let animCtx = null, animW = 0, animH = 0, animTlMeta = null;

document.getElementById('c-min-wr').addEventListener('input', function() {
  document.getElementById('c-min-wr-lbl').textContent = this.value + '%';
});

function animate() {
  if (!animating) return;
  drawCanvas(animCtx, animW, animH, graphNodes, graphEdges, animTlMeta);
  requestAnimationFrame(animate);
}

async function loadGraph() {
  animating = false; // stop previous animation loop
  const gs = document.getElementById('c-gen-start').value;
  const ge = document.getElementById('c-gen-end').value;
  const mw = parseInt(document.getElementById('c-min-wr').value) / 100;
  const st = document.getElementById('c-strategy').value;
  let url = '/api/evolution-graph?';
  if (gs) url += 'gen_start=' + gs + '&';
  if (ge) url += 'gen_end=' + ge + '&';
  if (mw > 0) url += 'min_wr=' + mw + '&';
  if (st) url += 'strategy=' + st + '&';

  document.getElementById('loading').textContent = 'Loading...';
  document.getElementById('loading').style.display = 'flex';

  try {
    const resp = await fetch(url);
    const data = await resp.json();
    document.getElementById('viz-nodes').textContent = data.node_count + ' nodes';
    document.getElementById('viz-edges').textContent = data.edge_count + ' edges';
    document.getElementById('viz-gens').textContent = 'Gen ' + data.gen_range[0] + '-' + data.gen_range[1];

    // Populate strategy filter
    const sel = document.getElementById('c-strategy');
    const cur = sel.value;
    sel.innerHTML = '<option value="">All (' + data.strategies.length + ')</option>';
    data.strategies.forEach(s => {
      const o = document.createElement('option');
      o.value = s; o.textContent = s.replace(/_/g,' ');
      if (s === cur) o.selected = true;
      sel.appendChild(o);
    });

    // Legend
    const leg = document.getElementById('legend');
    leg.innerHTML = data.strategies.map(s =>
      '<div style="display:flex;align-items:center;gap:4px">' +
        '<span class="legend-dot" style="background:' + (STRATEGY_COLORS[s]||'#6A7080') + '"></span>' +
        '<span style="font-size:0.65rem;color:#8890B0">' + s.replace(/_/g,' ') + '</span>' +
      '</div>'
    ).join('');

    document.getElementById('loading').style.display = 'none';
    initGraph(data);
  } catch(err) {
    document.getElementById('loading').textContent = 'Error: ' + err.message;
  }
}

function nodeRadius(n) {
  return 2.5 + Math.max(0, (n.wr - 0.4)) * 18;
}

function initGraph(data) {
  const canvas = document.getElementById('gc');
  const wrap = document.getElementById('graph-wrap');
  canvas.width = wrap.clientWidth;
  canvas.height = wrap.clientHeight;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;

  const nodes = data.nodes.map(n => ({...n}));
  const edges = data.edges.map(e => ({...e}));

  // Staggered fade-in birth times
  const now = Date.now();
  const genMin = data.gen_range[0];
  nodes.forEach(n => {
    n._birthTime = now + (n.gen - genMin) * 3;
  });

  graphNodes = nodes;
  graphEdges = edges;

  const nodeMap = {};
  nodes.forEach(n => { nodeMap[n.id] = n; });
  const validEdges = edges.filter(e => nodeMap[e.source] && nodeMap[e.target]);
  graphEdges = validEdges;

  if (simulation) simulation.stop();
  animating = false;
  transform = d3.zoomIdentity;

  const layout = document.getElementById('c-layout').value;

  if (layout === 'timeline') {
    const genMin = data.gen_range[0], genMax = data.gen_range[1];
    const xScale = d3.scaleLinear().domain([genMin, genMax]).range([60, W - 60]);
    const stratIdx = {};
    data.strategies.forEach((s, i) => { stratIdx[s] = i; });
    const yScale = d3.scaleLinear().domain([-1, data.strategies.length]).range([50, H - 50]);

    nodes.forEach(n => {
      n.x = xScale(n.gen) + (Math.random() - 0.5) * 15;
      n.y = yScale(stratIdx[n.strategy] || 0) + (Math.random() - 0.5) * 25;
      n.fx = n.x;
      n.fy = n.y;
    });

    simulation = d3.forceSimulation(nodes)
      .force('collide', d3.forceCollide(d => nodeRadius(d) + 1))
      .alphaDecay(0.05)
      .on('tick', () => drawCanvas(ctx, W, H, nodes, validEdges, layout === 'timeline' ? {xScale, genMin, genMax, strategies: data.strategies, yScale} : null));

  } else {
    simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(validEdges).id(d => d.id).distance(25).strength(0.4))
      .force('charge', d3.forceManyBody().strength(-12).distanceMax(180))
      .force('center', d3.forceCenter(W / 2, H / 2))
      .force('collide', d3.forceCollide(d => nodeRadius(d) + 1.5))
      .force('x', d3.forceX(W / 2).strength(0.015))
      .force('y', d3.forceY(H / 2).strength(0.015))
      .alphaDecay(0.02)
      .on('tick', () => drawCanvas(ctx, W, H, nodes, validEdges, null));
  }

  // Store animation context for rAF loop
  animCtx = ctx; animW = W; animH = H;
  animTlMeta = layout === 'timeline' ? {xScale: null, genMin: data.gen_range[0], genMax: data.gen_range[1], strategies: data.strategies} : null;
  animating = true;
  animate();

  // Zoom
  const zoom = d3.zoom().scaleExtent([0.15, 10]).on('zoom', ev => {
    transform = ev.transform;
  });
  d3.select(canvas).call(zoom);

  // Hover
  canvas.onmousemove = function(ev) {
    const rect = canvas.getBoundingClientRect();
    const mx = (ev.clientX - rect.left - transform.x) / transform.k;
    const my = (ev.clientY - rect.top - transform.y) / transform.k;
    let hit = null;
    for (const n of nodes) {
      const dx = n.x - mx, dy = n.y - my;
      const r = nodeRadius(n) + 3;
      if (dx*dx + dy*dy < r*r) { hit = n; break; }
    }
    hoveredNode = hit;
    const tip = document.getElementById('tooltip');
    if (hit) {
      tip.style.display = 'block';
      tip.style.left = Math.min(ev.clientX - rect.left + 14, W - 300) + 'px';
      tip.style.top = Math.min(ev.clientY - rect.top - 10, H - 120) + 'px';
      const sb = hit.elite ? '<span class="badge-e">ELITE</span>' : hit.viable ? '<span class="badge-v">VIABLE</span>' : '<span class="badge-s">Sub</span>';
      tip.innerHTML =
        '<div style="font-weight:700;margin-bottom:4px;font-size:0.85rem">' + hit.id + ' ' + sb + '</div>' +
        '<div style="color:#8890B0;margin-bottom:4px">Gen ' + hit.gen + ' | ' + hit.meta_strategy.replace(/_/g,' ') + '</div>' +
        '<div style="margin-bottom:2px"><span style="color:' + (STRATEGY_COLORS[hit.strategy]||'#6A7080') + ';font-weight:600">' + hit.strategy.replace(/_/g,' ') + '</span></div>' +
        '<div style="display:flex;gap:12px;margin-top:4px">' +
          '<div>WR <span style="color:#34d399;font-weight:700;font-size:0.9rem">' + (hit.wr*100).toFixed(1) + '%</span></div>' +
          '<div>WF <span style="font-weight:600">' + hit.wf.toFixed(1) + '</span></div>' +
          '<div>Trades <span style="font-weight:600">' + hit.trades + '</span></div>' +
        '</div>' +
        '<div style="color:#6A7080;margin-top:4px">' + hit.asset + '/' + hit.tf + '</div>';
    } else {
      tip.style.display = 'none';
    }
  };
  canvas.onmouseleave = () => { hoveredNode = null; document.getElementById('tooltip').style.display = 'none'; };
}

function drawCanvas(ctx, W, H, nodes, edges, tlMeta) {
  ctx.save();
  ctx.clearRect(0, 0, W, H);
  ctx.translate(transform.x, transform.y);
  ctx.scale(transform.k, transform.k);

  const now = Date.now();
  const fx = document.getElementById('c-effects').value; // 'full', 'subtle', 'off'
  const pulse = 0.5 + 0.5 * Math.sin(now / 1000);

  // Timeline axes
  if (tlMeta) {
    ctx.strokeStyle = '#1E2230';
    ctx.lineWidth = 0.5;
    ctx.beginPath();
    ctx.moveTo(40, 0); ctx.lineTo(40, H);
    ctx.moveTo(0, H - 30); ctx.lineTo(W, H - 30);
    ctx.stroke();
  }

  // Edges - slightly brighter base
  ctx.strokeStyle = fx === 'full' ? 'hsla(240, 5%, 40%, 0.22)' : 'hsla(240, 5%, 30%, 0.15)';
  ctx.lineWidth = fx === 'full' ? 0.6 : 0.4;
  for (const e of edges) {
    const s = typeof e.source === 'object' ? e.source : null;
    const t = typeof e.target === 'object' ? e.target : null;
    if (s && t) {
      ctx.beginPath();
      ctx.moveTo(s.x, s.y);
      ctx.lineTo(t.x, t.y);
      ctx.stroke();
    }
  }

  // Edge flow particles - 3 staggered particles per edge, strategy-colored
  if (fx !== 'off') {
    const particleCount = fx === 'full' ? 3 : 1;
    const particleSize = fx === 'full' ? 2.0 : 1.4;
    const particleAlpha = fx === 'full' ? 0.55 : 0.3;
    const speed = 3500; // ms per loop

    for (const e of edges) {
      const s = typeof e.source === 'object' ? e.source : null;
      const t = typeof e.target === 'object' ? e.target : null;
      if (!s || !t) continue;

      // Color particle by target node strategy
      const tNode = nodes.find(n => n.id === (t.id || t));
      const pc = tNode ? (STRATEGY_COLORS[tNode.strategy] || '#6A7080') : '#6A7080';

      for (let i = 0; i < particleCount; i++) {
        const offset = i / particleCount;
        const pt = ((now % speed) / speed + offset) % 1;
        const px = s.x + (t.x - s.x) * pt;
        const py = s.y + (t.y - s.y) * pt;

        // Glow trail (full mode only)
        if (fx === 'full') {
          ctx.save();
          ctx.shadowColor = pc;
          ctx.shadowBlur = 4;
          ctx.globalAlpha = particleAlpha * 0.6;
          ctx.fillStyle = pc;
          ctx.beginPath();
          ctx.arc(px, py, particleSize + 1, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        }

        // Core dot
        ctx.globalAlpha = particleAlpha;
        ctx.fillStyle = pc;
        ctx.beginPath();
        ctx.arc(px, py, particleSize, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
      }
    }
  }

  // Nodes
  for (const n of nodes) {
    const r = nodeRadius(n);
    const c = STRATEGY_COLORS[n.strategy] || '#6A7080';

    // Fade-in
    const age = now - (n._birthTime || 0);
    const fadeIn = fx === 'off' ? 1 : Math.min(1, Math.max(0, age / 800));

    if (n.elite) {
      ctx.save();
      if (fx !== 'off') {
        ctx.shadowColor = c;
        ctx.shadowBlur = fx === 'full' ? (6 + pulse * 8) : (4 + pulse * 6);
      }
      ctx.globalAlpha = fadeIn;
      ctx.fillStyle = c;
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;
      ctx.strokeStyle = 'rgba(255,255,255,0.3)';
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.restore();
    } else if (n.viable) {
      ctx.globalAlpha = 0.6 * fadeIn;
      ctx.fillStyle = c;
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
    } else {
      ctx.globalAlpha = 0.25 * fadeIn;
      ctx.fillStyle = c;
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
    }
  }

  // Hover highlight ring + connected edges
  if (fx !== 'off' && hoveredNode && hoveredNode.x !== undefined) {
    const hc = STRATEGY_COLORS[hoveredNode.strategy] || '#6A7080';
    const hr = nodeRadius(hoveredNode) + 4 + Math.sin(now / 300) * 2;
    ctx.beginPath();
    ctx.arc(hoveredNode.x, hoveredNode.y, hr, 0, Math.PI * 2);
    ctx.strokeStyle = hc;
    ctx.lineWidth = 1.5;
    ctx.globalAlpha = 0.6;
    ctx.stroke();
    ctx.globalAlpha = 1;

    // Highlight connected edges
    ctx.strokeStyle = hc;
    ctx.lineWidth = 1;
    ctx.globalAlpha = 0.4;
    for (const e of edges) {
      const s = typeof e.source === 'object' ? e.source : null;
      const t = typeof e.target === 'object' ? e.target : null;
      if (s && t && (s.id === hoveredNode.id || t.id === hoveredNode.id)) {
        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(t.x, t.y);
        ctx.stroke();
      }
    }
    ctx.globalAlpha = 1;
  }

  ctx.restore();
}

// Resize handler
window.addEventListener('resize', () => {
  const canvas = document.getElementById('gc');
  const wrap = document.getElementById('graph-wrap');
  canvas.width = wrap.clientWidth;
  canvas.height = wrap.clientHeight;
  if (graphNodes.length) drawCanvas(canvas.getContext('2d'), canvas.width, canvas.height, graphNodes, graphEdges, null);
});

// Auto-load on page load
window.addEventListener('DOMContentLoaded', () => {
  loadGraph();
});
</script>
</body>
</html>
"""


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8502)
