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

# Autoloop paths
REPO_ROOT = BASE.parent
ARTIFACTS = REPO_ROOT / "artifacts"
RESEARCH = ARTIFACTS / "research"
RECURSION = ARTIFACTS / "recursion"
BACKTESTS = ARTIFACTS / "backtests"
PAPER_TRADE_DIR = ARTIFACTS / "paper_trade"
CHIPS_DIR = ARTIFACTS / "chips"
DOCTRINE_CARDS_DIR = REPO_ROOT / "docs" / "doctrine-cards"
DOCTRINE_PACKETS_DIR = REPO_ROOT / "docs" / "doctrine-packets"

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


# ── Legacy API routes (kept for backward compat) ─────────────────────────
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


@app.get("/api/paper-trade")
def api_paper_trade():
    data = _json(ARCHIVE / "paper_trade_results.json")
    current = []
    if isinstance(data, list):
        for d in data:
            details = d.get("paper_trade_details", {})
            current.append({
                "agent": d.get("agent_id", "?")[:8],
                "bt_wr": d.get("backtest_wr", 0),
                "pt_wr": d.get("paper_trade_wr", 0),
                "delta": d.get("delta", 0),
                "trades": d.get("paper_trade_trades", 0),
                "validation": d.get("validation", "?"),
            })
    return {"current": current}


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


@app.get("/api/regime-distribution")
def api_regime_distribution():
    """Regime distribution from doctrine cards and backtest candidates."""
    cards = []
    if DOCTRINE_CARDS_DIR.exists():
        for f in sorted(DOCTRINE_CARDS_DIR.glob("*.json")):
            try:
                cards.append(json.loads(f.read_text(encoding="utf-8")))
            except Exception:
                pass

    regime_counts = Counter()
    for c in cards:
        regime = c.get("mutation_template", {}).get("market_regime",
                 c.get("market_regime", "unknown"))
        regime_counts[regime] += 1

    bt_summary = _json(BACKTESTS / "heavy_backtest_summary.json")
    bt_regimes = Counter()
    rows = bt_summary.get("rows", []) if isinstance(bt_summary, dict) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        regime = row.get("mutations", {}).get("market_regime", "unknown")
        bt_regimes[regime] += 1

    return {
        "doctrine_regimes": dict(regime_counts),
        "backtest_regimes": dict(bt_regimes),
        "total_cards": len(cards),
        "total_candidates": len(rows),
    }


# ── Autoloop API (tri-loop: learning + backtest + paper trade) ────────────


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

    # Paper trade queue
    pt_queue = _json(PAPER_TRADE_DIR / "paper_trade_queue.json")
    pt_monitor = _json(PAPER_TRADE_DIR / "paper_trade_monitor_report.json")

    # Variety backlog
    variety = _json(RECURSION / "variety_backlog.json")
    variety_list = variety if isinstance(variety, list) else []
    variety_count = len(variety_list)

    # Mutation trials (flat list or dict with "trials" key)
    trials = _json(RECURSION / "mutation_trials.json")
    if isinstance(trials, list):
        trial_list = trials
    elif isinstance(trials, dict):
        trial_list = trials.get("trials", [])
    else:
        trial_list = []

    # Self-edit queue
    self_edits_data = _json(RECURSION / "self_edit_queue.json")
    if isinstance(self_edits_data, list):
        self_edits = self_edits_data
    elif isinstance(self_edits_data, dict):
        self_edits = self_edits_data.get("edits", [])
    else:
        self_edits = []

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
        rows = bt_summary.get("rows", [])
        if isinstance(rows, list):
            for row in rows[:30]:
                if not isinstance(row, dict):
                    continue
                m = row.get("metrics", {})
                r = row.get("result", {})
                cid = row.get("candidate_id", "?")
                candidates.append({
                    "id": cid[:50],
                    "wr": m.get("win_rate", 0),
                    "wf": r.get("walk_forward_consistency", 0),
                    "dd": m.get("max_drawdown", 0),
                    "trades": r.get("trade_count", 0),
                    "sharpe": m.get("sharpe_ratio", 0),
                    "readiness": m.get("paper_trade_readiness", 0),
                    "stress": r.get("stress_resilience", 0),
                    "next_step": r.get("recommended_next_step", ""),
                    "verdict": r.get("verdict", ""),
                    "strategy": row.get("mutations", {}).get("strategy_id", ""),
                    "doctrine": row.get("mutations", {}).get("doctrine_id", ""),
                    "regime": row.get("mutations", {}).get("market_regime", ""),
                })
    candidates.sort(key=lambda x: x.get("wr", 0), reverse=True)

    # Strategy family stats
    strategy_family_stats = {}
    for c in candidates:
        sid = c.get("strategy", "unknown")
        if sid not in strategy_family_stats:
            strategy_family_stats[sid] = {"count": 0, "wr_sum": 0, "best_wr": 0, "approved": 0}
        s = strategy_family_stats[sid]
        s["count"] += 1
        wr = c.get("wr", 0)
        s["wr_sum"] += wr
        s["best_wr"] = max(s["best_wr"], wr)
        if c.get("verdict") == "approve":
            s["approved"] += 1
    for sid, s in strategy_family_stats.items():
        s["avg_wr"] = round(s["wr_sum"] / max(s["count"], 1), 4)
        del s["wr_sum"]

    # Walk-forward scatter
    wf_scatter = [
        {"id": c["id"][:30], "wr": c["wr"], "wf": c["wf"],
         "strategy": c["strategy"], "verdict": c["verdict"]}
        for c in candidates if c["wr"] > 0
    ]

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
                 "mechanism": (c.get("mechanism", "") or "")[:120],
                 "priority": c.get("benchmark_priority", ""),
                 "failures": len(c.get("lineage_failures", []))}
                for c in cards[-8:]
            ],
        },
        "backtest": {
            "candidate_count": len(candidates),
            "top_candidate": candidates[0] if candidates else None,
            "candidates": candidates[:20],
            "variety_count": variety_count,
            "trial_count": len(trial_list),
        },
        "paper_trade": {
            "queue_count": len(pt_queue.get("candidates", [])) if isinstance(pt_queue, dict) else 0,
            "promotion_ready": pt_monitor.get("promotion_ready_count", 0) if isinstance(pt_monitor, dict) else 0,
            "significant": pt_monitor.get("statistically_significant_count", 0) if isinstance(pt_monitor, dict) else 0,
        },
        "cycle_timeline": cycle_timeline,
        "strategy_family_stats": strategy_family_stats,
        "wf_scatter": wf_scatter,
        "variety_backlog": variety_list[:15],
        "mutation_trials": trial_list[:10],
        "self_edits": self_edits[:10],
    }


@app.get("/api/candidate-history")
def api_candidate_history():
    """Per-cycle activity for growth charts — uses real journal fields."""
    journal = _jsonl_tail(RECURSION / "cycle_journal.jsonl", 60)
    cycles = []
    for c in journal:
        bt = c.get("backtest", {})
        lr = c.get("learning", {})
        cycles.append({
            "cycle": c.get("cycle_number", 0),
            "cards_added": lr.get("added_count", 0),
            "pending_variety": c.get("pending_variety_count", 0),
            "pending_packets": c.get("pending_packet_count", 0),
            "material": c.get("material_change", False),
            "learning_material": lr.get("material_change", False),
            "backtest_ran": bt.get("ran", False),
            "backtest_material": bt.get("material_change", False),
            "loops_run": c.get("loops_run", []),
        })
    return {"cycles": cycles}


@app.get("/api/strategy-diversity")
def api_strategy_diversity():
    """Strategy distribution, diversity index, regime coverage."""
    bt_summary = _json(BACKTESTS / "heavy_backtest_summary.json")
    rows = bt_summary.get("rows", []) if isinstance(bt_summary, dict) else []

    strat_stats = {}
    regime_by_strat = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        m = row.get("mutations", {})
        metrics = row.get("metrics", {})
        sid = m.get("strategy_id", "unknown")
        regime = m.get("market_regime", "unknown")
        wr = float(metrics.get("win_rate", 0))

        if sid not in strat_stats:
            strat_stats[sid] = {"count": 0, "wr_sum": 0, "best_wr": 0}
        s = strat_stats[sid]
        s["count"] += 1
        s["wr_sum"] += wr
        s["best_wr"] = max(s["best_wr"], wr)

        regime_by_strat.setdefault(sid, set()).add(regime)

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
            "regimes": sorted(regime_by_strat.get(sid, set())),
        }

    return {
        "strategies": strategies,
        "total": total,
        "diversity_index": diversity,
    }


@app.get("/api/researcher-health")
def api_researcher_health():
    """Chip hook call counts, frontier queue, failure data."""
    hook_calls = {}
    if CHIPS_DIR.exists():
        chip_dir = CHIPS_DIR / "domain-chip-crypto-trading"
        if chip_dir.exists():
            for hook in ["evaluate", "suggest", "packets", "watchtower"]:
                hook_dir = chip_dir / hook
                if hook_dir.exists():
                    logs = sorted(hook_dir.glob("*.log"))
                    hook_calls[hook] = {
                        "count": len(logs),
                        "last": logs[-1].name if logs else None,
                    }

    frontier = _json(ARTIFACTS / "frontier" / "queue.json")
    queue_trials = frontier.get("candidate_trials", []) if isinstance(frontier, dict) else []

    return {
        "hook_calls": hook_calls,
        "frontier_queue_size": len(queue_trials),
        "frontier_candidates": [
            {"id": t.get("candidate_id", "?")[:40], "hypothesis": t.get("hypothesis", "")[:80]}
            for t in queue_trials[:5]
        ],
    }


@app.get("/api/cycle-feed")
def api_cycle_feed(n: int = Query(50, le=100)):
    """Last N cycle entries with lane activity details."""
    journal = _jsonl_tail(RECURSION / "cycle_journal.jsonl", n)
    entries = []
    for c in reversed(journal):
        entry = {
            "cycle": c.get("cycle_number", 0),
            "timestamp": c.get("timestamp", ""),
            "material": c.get("material_change", False),
            "lanes": {},
        }
        for lane in ["learning", "backtest", "paper_trade"]:
            ld = c.get(lane, {})
            entry["lanes"][lane] = {
                "ran": bool(ld),
                "material": ld.get("material_change", False),
                "details": ld.get("summary", ld.get("result", "")),
            }
        entries.append(entry)
    return {"entries": entries}


# ── HTML dashboard ───────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def dashboard_html():
    return HTML_PAGE


@app.get("/evolution-viz", response_class=HTMLResponse)
def evolution_viz_page():
    return EVOLUTION_VIZ_PAGE


# ── Evolution graph API (kept for viz page) ──────────────────────────────
@app.get("/api/evolution-graph")
def api_evolution_graph(
    gen_start: int = Query(None),
    gen_end: int = Query(None),
    min_wr: float = Query(0.0),
    strategy: str = Query(""),
):
    """Return nodes + edges for evolution visualization from backtest candidates."""
    bt_summary = _json(BACKTESTS / "heavy_backtest_summary.json")
    rows = bt_summary.get("rows", []) if isinstance(bt_summary, dict) else []

    nodes = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        m = row.get("mutations", {})
        metrics = row.get("metrics", {})
        result = row.get("result", {})
        wr = float(metrics.get("win_rate", 0))
        if wr < min_wr:
            continue
        sid = m.get("strategy_id", "")
        if strategy and sid != strategy:
            continue
        cid = row.get("candidate_id", f"c{i}")[:8]
        nodes.append({
            "id": cid,
            "gen": i,
            "wr": round(wr, 4),
            "wf": round(float(result.get("walk_forward_consistency", 0)), 2),
            "trades": int(result.get("trade_count", 0)),
            "strategy": sid,
            "asset": m.get("asset_universe", "BTC"),
            "tf": m.get("timeframe", "15m"),
            "meta_strategy": m.get("doctrine_id", "?"),
            "elite": result.get("verdict") == "approve",
            "viable": wr >= 0.52,
            "improved": False,
        })

    strategies_list = sorted(set(n["strategy"] for n in nodes))
    return {
        "nodes": nodes,
        "edges": [],
        "gen_range": [0, len(nodes)],
        "node_count": len(nodes),
        "edge_count": 0,
        "strategies": strategies_list,
    }


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
  @keyframes fadeUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
  .fade-up { animation: fadeUp 0.4s ease-out both; }

  body { background: #0E1018; color: #F0F0F4; font-family: 'DM Sans', system-ui, sans-serif; }
  .card { background: #181C26; border: 1px solid #222430; border-radius: 6px; }
  .badge { padding: 2px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 500; }
  .badge-emerald { background: rgba(47,202,148,0.15); color: #3DDDA4; }
  .badge-sky { background: rgba(104,168,216,0.15); color: #68A8D8; }
  .badge-muted { background: #14161E; color: #6A7080; border: 1px solid #222430; }
  .badge-amber { background: rgba(232,184,109,0.15); color: #E8B86D; }
  .badge-red { background: rgba(224,136,120,0.15); color: #E08878; }
  .pulse { animation: pulse 2s cubic-bezier(.4,0,.6,1) infinite; }
  @keyframes pulse { 0%,100% { opacity:1 } 50% { opacity:.5 } }
  .progress-bar { height: 6px; border-radius: 3px; background: #222430; overflow: hidden; }
  .progress-fill { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
  .section-title { font-size: 0.6875rem; font-weight: 600; color: #6A7080; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem; }
  .stat-label { font-size: 0.8rem; color: #6A7080; font-weight: 500; letter-spacing: 0.05em; }
  .stat-value { font-size: 1.75rem; font-weight: 700; letter-spacing: -0.02em; }
  .tab-btn { padding: 4px 12px; border-radius: 5px; font-size: 0.75rem; font-weight: 500; background: transparent; color: #6A7080; border: 1px solid transparent; cursor: pointer; transition: all 0.2s; }
  .tab-btn:hover { color: #F0F0F4; background: #1E2230; }
  .tab-active { background: #222430 !important; color: #F0F0F4 !important; border-color: #2A2E3C !important; }
  .feed-item { border-left: 3px solid transparent; transition: all 0.15s; padding: 6px 8px 6px 12px; border-radius: 0 4px 4px 0; }
  .feed-item:hover { background: #1E2230; }
  .filter-select { background: #141820; border: 1px solid #222430; color: #8890B0; font-size: 0.75rem; padding: 4px 8px; border-radius: 6px; font-family: 'DM Sans', system-ui, sans-serif; cursor: pointer; }
  .filter-select:focus { outline: 1px solid #2A2E3C; }
  .strat-bar-seg { height: 100%; display: inline-block; transition: width 0.6s; position: relative; }
  .strat-bar-seg:hover::after { content: attr(data-tip); position: absolute; bottom: 110%; left: 50%; transform: translateX(-50%); background: #141820; color: #F0F0F4; font-size: 0.65rem; padding: 2px 6px; border-radius: 4px; white-space: nowrap; pointer-events: none; z-index: 10; }
  table tbody tr { transition: background 0.15s; }
  table tbody tr:hover { background: #1E2230; }
  canvas { max-height: 200px; }

  ::-webkit-scrollbar { width: 8px; height: 8px; }
  ::-webkit-scrollbar-track { background: #141820; border-radius: 4px; }
  ::-webkit-scrollbar-thumb { background: #2A2E3C; border-radius: 4px; }
  ::-webkit-scrollbar-thumb:hover { background: #3A3F50; }
  * { scrollbar-width: thin; scrollbar-color: #2A2E3C #141820; }
</style>
</head>
<body class="min-h-screen p-6">

<!-- HEADER -->
<div class="flex items-center justify-between mb-6">
  <div>
    <h1 class="text-2xl font-bold tracking-tight">Spark Domain Chip <span style="color:#2FCA94">Crypto Trading</span></h1>
    <p class="text-sm" style="color: #8890B0;">Autoloop doctrine discovery + walk-forward backtesting + live paper trading</p>
    <a href="/evolution-viz" class="text-xs" style="color:#6A7080;text-decoration:none;margin-top:2px;display:inline-block" onmouseover="this.style.color='#2FCA94'" onmouseout="this.style.color='#6A7080'">Evolution Graph &rarr;</a>
  </div>
  <div class="flex items-center gap-3">
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 rounded-full pulse" style="background:#2FCA94"></span>
      <span class="text-sm font-medium" style="color:#2FCA94">Live</span>
    </div>
    <span id="clock" class="text-xs" style="color:#8890B0">--:--:--</span>
  </div>
</div>

<!-- TOP STAT CARDS -->
<div class="grid grid-cols-6 gap-3 mb-6" id="top-stats">
  <div class="card p-4">
    <div class="stat-label">Cycle</div>
    <div class="stat-value" id="s-cycle">--</div>
  </div>
  <div class="card p-4">
    <div class="stat-label">Best Win Rate</div>
    <div class="stat-value" style="color:#2FCA94" id="s-best-wr">--</div>
  </div>
  <div class="card p-4">
    <div class="stat-label">Avg Win Rate</div>
    <div class="stat-value" id="s-avg-wr">--</div>
  </div>
  <div class="card p-4">
    <div class="stat-label">Approved</div>
    <div class="stat-value" style="color:#2FCA94" id="s-approved">0</div>
    <div class="text-xs mt-1" style="color:#6A7080">WR>=58% & WF>=0.8</div>
  </div>
  <div class="card p-4">
    <div class="stat-label">Deferred</div>
    <div class="stat-value" style="color:#E8B86D" id="s-deferred">0</div>
  </div>
  <div class="card p-4">
    <div class="stat-label">Total Candidates</div>
    <div class="stat-value" style="color:#68A8D8" id="s-total">--</div>
  </div>
</div>

<!-- MAIN GRID: Activity Feed | Charts | Panels -->
<div class="grid grid-cols-12 gap-4 mb-4">

  <!-- LEFT: Cycle Activity Feed (5 cols) -->
  <div class="col-span-5">
    <div class="card p-5 h-full" style="display:flex;flex-direction:column">
      <div class="flex items-center justify-between mb-3">
        <div class="section-title mb-0">Cycle Activity Feed</div>
        <div class="flex items-center gap-2">
          <span class="text-xs" style="color:#6A7080" id="feed-count"></span>
          <select id="feed-filter" onchange="renderCycleFeed()" class="filter-select">
            <option value="">All</option>
            <option value="material">Material Only</option>
            <option value="learning">Learning</option>
            <option value="backtest">Backtest</option>
          </select>
        </div>
      </div>
      <div id="cycle-feed" style="overflow-y:auto;flex:1;max-height:460px" class="space-y-0.5"></div>
    </div>
  </div>

  <!-- MIDDLE: Charts (4 cols) -->
  <div class="col-span-4 space-y-4">
    <div class="card p-5">
      <div class="section-title">Doctrine Growth</div>
      <canvas id="candidateGrowthChart"></canvas>
    </div>
    <div class="card p-5">
      <div class="section-title">Autoloop Activity</div>
      <canvas id="backtestProdChart"></canvas>
    </div>
  </div>

  <!-- RIGHT: Panels (3 cols) -->
  <div class="col-span-3 space-y-4">
    <!-- Strategy Family Performance -->
    <div class="card p-5">
      <div class="section-title">Strategy Performance</div>
      <div id="strategy-performance" class="space-y-3"></div>
    </div>
    <!-- Researcher Health -->
    <div class="card p-5">
      <div class="section-title">Researcher Health</div>
      <div id="researcher-health" class="space-y-2"></div>
    </div>
  </div>
</div>

<!-- STRATEGY DIVERSITY + DOCTRINE INSIGHTS -->
<div class="grid grid-cols-12 gap-4 mb-4">
  <!-- Strategy Diversity -->
  <div class="col-span-7">
    <div class="card p-5">
      <div class="flex items-center justify-between mb-3">
        <div class="section-title mb-0">Strategy Diversity</div>
        <div class="flex items-center gap-2">
          <span class="text-xs" style="color:#6A7080">Index:</span>
          <span class="text-sm font-bold" id="diversity-index" style="color:#2FCA94">--</span>
        </div>
      </div>
      <div id="strategy-bar" style="height:28px;border-radius:6px;overflow:hidden;display:flex;margin-bottom:12px;background:#141820"></div>
      <div id="strategy-list" class="space-y-1.5" style="max-height:240px;overflow-y:auto"></div>
    </div>
  </div>

  <!-- Doctrine Insights -->
  <div class="col-span-5">
    <div class="card p-5">
      <div class="section-title">Doctrine Insights</div>
      <div id="doctrine-insights" class="grid grid-cols-2 gap-2"></div>
    </div>
  </div>
</div>

<!-- SELF-EDITS QUEUE -->
<div class="mb-4">
  <div class="card p-5">
    <div class="flex items-center justify-between mb-3">
      <div class="section-title mb-0">Self-Edit Queue <span class="text-xs font-normal" style="color:#6A7080">(Queued Mutations)</span></div>
      <span class="text-xs" style="color:#6A7080" id="self-edit-count"></span>
    </div>
    <div id="self-edits" class="grid grid-cols-3 gap-2"></div>
  </div>
</div>

<!-- TOP CANDIDATES TABLE -->
<div class="mb-4">
  <div class="card p-5">
    <div class="flex items-center justify-between mb-4">
      <div class="section-title mb-0">Top Candidates</div>
      <div class="flex items-center gap-3">
        <select id="cand-filter-strategy" onchange="renderTopCandidates()" class="filter-select">
          <option value="">All Strategies</option>
        </select>
        <select id="cand-filter-verdict" onchange="renderTopCandidates()" class="filter-select">
          <option value="">All Verdicts</option>
          <option value="approve">Approve</option>
          <option value="defer">Defer</option>
          <option value="reject">Reject</option>
        </select>
        <span class="text-xs" style="color:#6A7080" id="cand-count"></span>
      </div>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-sm" id="cand-table">
        <thead>
          <tr class="text-left" style="color:#6A7080; border-bottom:1px solid #222430;">
            <th class="pb-2 pr-3 font-medium">#</th>
            <th class="pb-2 pr-3 font-medium cursor-pointer" onclick="sortCandidates('wr')">Win Rate</th>
            <th class="pb-2 pr-3 font-medium cursor-pointer" onclick="sortCandidates('wf')">WF</th>
            <th class="pb-2 pr-3 font-medium cursor-pointer" onclick="sortCandidates('sharpe')">Sharpe</th>
            <th class="pb-2 pr-3 font-medium">Drawdown</th>
            <th class="pb-2 pr-3 font-medium cursor-pointer" onclick="sortCandidates('trades')">Trades</th>
            <th class="pb-2 pr-3 font-medium">Strategy</th>
            <th class="pb-2 pr-3 font-medium">Doctrine</th>
            <th class="pb-2 pr-3 font-medium">Regime</th>
            <th class="pb-2 pr-3 font-medium cursor-pointer" onclick="sortCandidates('readiness')">Readiness</th>
            <th class="pb-2 font-medium">Verdict</th>
          </tr>
        </thead>
        <tbody id="cand-body"></tbody>
      </table>
    </div>
  </div>
</div>

<!-- WALK-FORWARD GATE -->
<div class="mb-4">
  <div class="card p-5">
    <div class="flex items-center justify-between mb-3">
      <div class="section-title mb-0">Walk-Forward Gate</div>
      <div class="flex items-center gap-2">
        <span class="text-xs" style="color:#6A7080" id="wf-summary"></span>
      </div>
    </div>
    <div class="grid grid-cols-2 gap-4">
      <div>
        <div class="text-xs mb-2" style="color:#6A7080">WF Coverage <span class="font-mono" id="wf-coverage-pct"></span></div>
        <div class="progress-bar" style="height:10px">
          <div class="progress-fill" id="wf-coverage-bar" style="width:0%;background:linear-gradient(90deg,#2FCA94,#68A8D8)"></div>
        </div>
        <div class="flex justify-between mt-2 text-xs" style="color:#6A7080">
          <span id="wf-passed">0 passed</span>
          <span id="wf-total">0 total</span>
        </div>
      </div>
      <div>
        <div class="text-xs mb-2" style="color:#6A7080">Win Rate vs Walk-Forward Consistency</div>
        <canvas id="wfScatterChart" style="max-height:180px"></canvas>
      </div>
    </div>
  </div>
</div>

<!-- AUTOLOOP TRI-LOOP (lane details) -->
<div class="mb-4" id="autoloop-section">
  <div class="card p-5">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="section-title mb-0">Autoloop Lanes</div>
        <span id="autoloop-status-badge" class="text-xs px-2 py-0.5 rounded" style="background:#222430;color:#6A7080">--</span>
      </div>
      <div class="flex gap-4 text-xs" style="color:#6A7080">
        <span>Noop: <span id="al-noop" class="font-mono" style="color:#F0F0F4">--</span></span>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-3 mb-4">
      <div class="card p-3" style="background:#141820">
        <div class="text-xs mb-1" style="color:#6A7080">Learning Lane</div>
        <div class="flex items-baseline gap-2">
          <span id="al-doctrine-cards" class="text-lg font-mono font-bold" style="color:#2FCA94">--</span>
          <span class="text-xs" style="color:#6A7080">doctrine cards</span>
        </div>
        <div class="text-xs mt-1" style="color:#6A7080"><span id="al-doctrine-packets" class="font-mono">--</span> packets</div>
      </div>
      <div class="card p-3" style="background:#141820">
        <div class="text-xs mb-1" style="color:#6A7080">Backtest Lane</div>
        <div class="flex items-baseline gap-2">
          <span id="al-bt-candidates" class="text-lg font-mono font-bold" style="color:#68A8D8">--</span>
          <span class="text-xs" style="color:#6A7080">candidates</span>
        </div>
        <div class="text-xs mt-1" style="color:#6A7080"><span id="al-variety" class="font-mono">--</span> variety &middot; <span id="al-trials" class="font-mono">--</span> trials</div>
      </div>
      <div class="card p-3" style="background:#141820">
        <div class="text-xs mb-1" style="color:#6A7080">Paper Trade Lane</div>
        <div class="flex items-baseline gap-2">
          <span id="al-pt-queue" class="text-lg font-mono font-bold" style="color:#E8B86D">--</span>
          <span class="text-xs" style="color:#6A7080">in queue</span>
        </div>
        <div class="text-xs mt-1" style="color:#6A7080"><span id="al-pt-ready" class="font-mono">--</span> ready &middot; <span id="al-pt-sig" class="font-mono">--</span> significant</div>
      </div>
    </div>

    <!-- Cycle timeline chart + recent doctrine cards -->
    <div class="grid grid-cols-2 gap-4">
      <div>
        <div class="text-xs mb-2" style="color:#6A7080">Cycle Timeline <span class="font-mono" id="al-timeline-range"></span></div>
        <canvas id="al-cycle-chart" height="120"></canvas>
      </div>
      <div>
        <div class="text-xs mb-2" style="color:#6A7080">Recent Doctrine Cards</div>
        <div id="al-doctrine-list" class="flex flex-wrap gap-2" style="max-height:180px;overflow-y:auto"></div>
      </div>
    </div>
  </div>
</div>

<!-- LIVE TRADING SECTION -->
<div class="mb-4" id="live-pt-section">
  <div class="card p-5">
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
    <div class="grid grid-cols-6 gap-3 mb-4">
      <div class="card p-3" style="background:#141820"><div class="stat-label">Settlements</div><div class="stat-value text-sm" style="color:#68A8D8" id="live-settlements">--</div></div>
      <div class="card p-3" style="background:#141820"><div class="stat-label">Trades</div><div class="stat-value text-sm" style="color:#68A8D8" id="live-trades-count">--</div></div>
      <div class="card p-3" style="background:#141820"><div class="stat-label">Wins</div><div class="stat-value text-sm" style="color:#2FCA94" id="live-wins-count">--</div></div>
      <div class="card p-3" style="background:#141820"><div class="stat-label">Losses</div><div class="stat-value text-sm" style="color:#E08878" id="live-losses-count">--</div></div>
      <div class="card p-3" style="background:#141820"><div class="stat-label">Win Rate</div><div class="stat-value text-sm" id="live-accuracy">--</div></div>
      <div class="card p-3" style="background:#141820"><div class="stat-label">Agents / Strats</div><div class="stat-value text-sm" id="live-agents-strats">--</div></div>
    </div>
    <div class="mb-4">
      <div class="text-xs font-medium mb-2" style="color:#8890B0">Active Contracts</div>
      <div id="live-contracts" class="grid gap-2" style="grid-template-columns:repeat(auto-fill,minmax(280px,1fr))">
        <div style="padding:12px;text-align:center;color:#6A7080;font-size:0.8rem">Start: <span style="font-family:'DM Mono',monospace;color:#8890B0">python live_paper_trader.py --assets BTC --per-strategy 3</span></div>
      </div>
    </div>
    <div class="mb-4">
      <div class="text-xs font-medium mb-2" style="color:#8890B0">Recent Settlements</div>
      <div id="live-settlements-list" style="max-height:200px;overflow-y:auto;"></div>
    </div>
  </div>
</div>

<!-- FOOTER -->
<div class="mt-6 flex items-center justify-between text-xs" style="color: #6A7080;">
  <span>Spark Domain Chip: Crypto Trading &middot; Autoloop + Researcher + Live Paper Trading</span>
  <span id="footer-status">Connecting...</span>
</div>

<script>
// ── Constants ─────────────────────────────────────
const C = {
  emerald: '#2FCA94', sky: '#68A8D8', amber: '#E8B86D', red: '#E08878',
  violet: '#a78bfa', muted: '#6A7080', fg: '#F0F0F4',
  gridLine: '#1E2230', cardBg: '#141820',
};

const STRAT_COLORS = {
  wedge_exhaustion_reversal: '#2FCA94', ema_pullback_long: '#68A8D8',
  bollinger_squeeze_breakout: '#E8B86D', range_reclaim_rotation: '#a78bfa',
  ema_trend_continuation: '#f472b6', momentum_breakout: '#22d3ee',
  funding_mean_revert: '#f97316', rsi_extreme_reversion: '#e879f9',
  compression_range_bounce: '#38bdf8', channel_breakout_fade: '#a3e635',
};

function stratColor(s) { return STRAT_COLORS[s] || C.muted; }

const CHART_DEFAULTS = {
  responsive: true, maintainAspectRatio: false,
  plugins: { legend: { display: true, position: 'top',
    labels: { color: C.muted, boxWidth: 8, padding: 8, font: { size: 10, family: 'DM Sans' } }
  }},
  scales: {
    x: { grid: { color: C.gridLine }, ticks: { color: C.muted, font: { size: 9, family: 'DM Mono' }, maxTicksLimit: 10 } },
    y: { grid: { color: C.gridLine }, ticks: { color: C.muted, font: { size: 9 } } },
  }
};

// ── State ─────────────────────────────────────────
let _autoloopData = null;
let _cycleFeedData = null;
let _candidateSort = { field: 'wr', asc: false };
let _chartInstances = {};
let _livePeriod = 'alltime';
let _lastLivePtData = null;

async function fetchJSON(url) {
  try { const r = await fetch(url); return await r.json(); } catch { return null; }
}

function destroyChart(key) {
  if (_chartInstances[key]) { _chartInstances[key].destroy(); _chartInstances[key] = null; }
}

// ── Top Stats ─────────────────────────────────────
function renderTopStats(data) {
  if (!data) return;
  const s = data.state || {};
  const bt = data.backtest || {};
  const cands = bt.candidates || [];

  document.getElementById('s-cycle').textContent = s.cycle_count || 0;
  document.getElementById('s-total').textContent = bt.candidate_count || 0;

  if (cands.length > 0) {
    const wrs = cands.map(c => c.wr);
    document.getElementById('s-best-wr').textContent = (Math.max(...wrs) * 100).toFixed(1) + '%';
    document.getElementById('s-avg-wr').textContent = (wrs.reduce((a,b)=>a+b,0) / wrs.length * 100).toFixed(1) + '%';
  }

  const approved = cands.filter(c => c.verdict === 'approve').length;
  const deferred = cands.filter(c => c.verdict === 'defer').length;
  document.getElementById('s-approved').textContent = approved;
  document.getElementById('s-deferred').textContent = deferred;
}

// ── Cycle Activity Feed ───────────────────────────
function renderCycleFeed() {
  const data = _cycleFeedData;
  if (!data) return;
  const filter = document.getElementById('feed-filter').value;
  let entries = data.entries || [];

  if (filter === 'material') entries = entries.filter(e => e.material);
  else if (filter === 'learning') entries = entries.filter(e => e.lanes.learning && e.lanes.learning.material);
  else if (filter === 'backtest') entries = entries.filter(e => e.lanes.backtest && e.lanes.backtest.material);

  document.getElementById('feed-count').textContent = entries.length + ' cycles';
  const el = document.getElementById('cycle-feed');

  el.innerHTML = entries.map(e => {
    const borderColor = e.material ? C.emerald : '#222430';
    const lanes = e.lanes || {};
    const lBadge = lanes.learning && lanes.learning.material ? '<span class="badge badge-emerald" style="font-size:0.6rem;padding:1px 6px">Learn</span>' : '';
    const bBadge = lanes.backtest && lanes.backtest.material ? '<span class="badge badge-sky" style="font-size:0.6rem;padding:1px 6px">Backtest</span>' : '';
    const pBadge = lanes.paper_trade && lanes.paper_trade.material ? '<span class="badge badge-amber" style="font-size:0.6rem;padding:1px 6px">Paper</span>' : '';
    const materialBadge = e.material ? '<span style="font-size:0.6rem;color:#2FCA94;font-weight:600">MATERIAL</span>' : '';
    let time = '';
    try { const t = new Date(e.timestamp); time = t.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'}); } catch {}

    return '<div class="feed-item" style="border-left-color:' + borderColor + '">' +
      '<div class="flex justify-between items-center">' +
        '<div class="flex items-center gap-2">' +
          '<span class="font-mono text-xs" style="color:#8890B0">C' + e.cycle + '</span>' +
          lBadge + bBadge + pBadge + materialBadge +
        '</div>' +
        '<span class="text-xs" style="color:#6A7080">' + time + '</span>' +
      '</div></div>';
  }).join('');
}

// ── Candidate Growth Chart ────────────────────────
function renderCandidateGrowth(data) {
  if (!data || !data.cycles || data.cycles.length === 0) return;
  destroyChart('candidateGrowth');
  const ctx = document.getElementById('candidateGrowthChart').getContext('2d');
  const cycles = data.cycles;
  const labels = cycles.map(c => 'C' + c.cycle);

  // Cumulative doctrine cards ingested
  let cumCards = 0;
  const cardsData = [];
  for (const c of cycles) {
    cumCards += c.cards_added || 0;
    cardsData.push(cumCards);
  }

  _chartInstances.candidateGrowth = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        { label: 'Doctrine Cards (cumul.)', data: cardsData, borderColor: C.emerald, backgroundColor: C.emerald + '15', fill: true, tension: 0.3, pointRadius: 0, borderWidth: 1.5 },
        { label: 'Variety Backlog', data: cycles.map(c => c.pending_variety || 0), borderColor: C.amber, backgroundColor: 'transparent', tension: 0.3, pointRadius: 0, borderWidth: 1.5 },
        { label: 'Pending Packets', data: cycles.map(c => c.pending_packets || 0), borderColor: C.muted, backgroundColor: 'transparent', tension: 0.3, pointRadius: 0, borderWidth: 1, borderDash: [4,2] },
      ]
    },
    options: CHART_DEFAULTS,
  });
}

// ── Autoloop Activity Chart ──────────────────────
function renderBacktestProduction(data) {
  if (!data || !data.cycles || data.cycles.length === 0) return;
  destroyChart('backtestProd');
  const ctx = document.getElementById('backtestProdChart').getContext('2d');
  const cycles = data.cycles;

  _chartInstances.backtestProd = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: cycles.map(c => 'C' + c.cycle),
      datasets: [
        { label: 'Cards Added', data: cycles.map(c => c.cards_added || 0), backgroundColor: C.emerald + '80', barPercentage: 0.7 },
        { label: 'BT Material', data: cycles.map(c => c.backtest_material ? 1 : 0), backgroundColor: C.sky + '60', barPercentage: 0.7 },
      ]
    },
    options: {
      ...CHART_DEFAULTS,
      plugins: { legend: { labels: { color: C.muted, font: { size: 9 } } } },
      scales: { ...CHART_DEFAULTS.scales, y: { ...CHART_DEFAULTS.scales.y, max: 5 } },
    },
  });
}

// ── Strategy Performance (progress bars) ──────────
function renderStrategyPerformance(stats) {
  const el = document.getElementById('strategy-performance');
  if (!stats || Object.keys(stats).length === 0) {
    el.innerHTML = '<div class="text-xs" style="color:#6A7080">No data yet</div>';
    return;
  }
  const sorted = Object.entries(stats).sort((a,b) => b[1].best_wr - a[1].best_wr);
  el.innerHTML = sorted.map(([name, d]) => {
    const pct = (d.avg_wr * 100).toFixed(1);
    const best = (d.best_wr * 100).toFixed(1);
    const color = stratColor(name);
    const label = name.replace(/_/g, ' ');
    return '<div>' +
      '<div class="flex justify-between items-baseline mb-1">' +
        '<span class="text-xs font-medium" style="max-width:140px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + label + '</span>' +
        '<span class="text-xs font-semibold" style="color:' + color + '">' + pct + '%</span>' +
      '</div>' +
      '<div class="progress-bar"><div class="progress-fill" style="width:' + Math.min(pct * 1.5, 100) + '%;background:' + color + '"></div></div>' +
      '<div class="text-xs mt-0.5" style="color:#6A7080">' + d.count + ' candidates &middot; best ' + best + '%</div>' +
    '</div>';
  }).join('');
}

// ── Researcher Health ─────────────────────────────
function renderResearcherHealth(data) {
  const el = document.getElementById('researcher-health');
  if (!data) { el.innerHTML = '<div class="text-xs" style="color:#6A7080">No chip data</div>'; return; }

  const hooks = data.hook_calls || {};
  const hookHtml = Object.entries(hooks).map(([name, d]) =>
    '<div class="flex justify-between text-xs"><span style="color:#8890B0">' + name + '</span><span class="font-mono" style="color:#F0F0F4">' + d.count + ' calls</span></div>'
  ).join('');

  el.innerHTML = hookHtml +
    '<div class="flex justify-between text-xs mt-2 pt-2" style="border-top:1px solid #222430">' +
      '<span style="color:#8890B0">Frontier Queue</span>' +
      '<span class="font-mono" style="color:' + (data.frontier_queue_size > 0 ? C.amber : C.emerald) + '">' + data.frontier_queue_size + '</span>' +
    '</div>';
}

// ── Strategy Diversity ────────────────────────────
function renderStrategyDiversity(data) {
  if (!data) return;
  const strats = data.strategies || {};
  const total = data.total || 1;

  document.getElementById('diversity-index').textContent = data.diversity_index.toFixed(2);

  // Stacked bar
  const barEl = document.getElementById('strategy-bar');
  barEl.innerHTML = Object.entries(strats).map(([sid, s]) => {
    const c = stratColor(sid);
    return '<div class="strat-bar-seg" data-tip="' + sid.replace(/_/g,' ') + ': ' + (s.pct*100).toFixed(0) + '%" style="width:' + (s.pct*100) + '%;background:' + c + '"></div>';
  }).join('');

  // Strategy list
  const listEl = document.getElementById('strategy-list');
  listEl.innerHTML = Object.entries(strats).map(([sid, s]) => {
    const c = stratColor(sid);
    const regimes = (s.regimes || []).map(r =>
      '<span style="display:inline-block;padding:1px 5px;border-radius:3px;font-size:0.6rem;background:#141820;color:#6A7080;border:1px solid #222430">' + r + '</span>'
    ).join(' ');
    return '<div class="flex items-center justify-between py-1" style="border-bottom:1px solid #1E2230">' +
      '<div class="flex items-center gap-2">' +
        '<span style="width:8px;height:8px;border-radius:50%;background:' + c + ';display:inline-block"></span>' +
        '<span class="text-xs" style="color:#F0F0F4">' + sid.replace(/_/g,' ') + '</span>' +
      '</div>' +
      '<div class="flex items-center gap-3 text-xs">' +
        '<span style="color:#6A7080">' + s.count + '</span>' +
        '<span style="color:' + c + ';font-weight:600">' + (s.avg_wr*100).toFixed(1) + '%</span>' +
        regimes +
      '</div></div>';
  }).join('');
}

// ── Doctrine Insights ─────────────────────────────
function renderDoctrineInsights(cards) {
  const el = document.getElementById('doctrine-insights');
  if (!cards || cards.length === 0) { el.innerHTML = '<div class="text-xs" style="color:#6A7080">No doctrine cards yet</div>'; return; }

  el.innerHTML = cards.slice(0, 6).map(c => {
    const doctrine = (c.doctrine || '').replace(/_/g, ' ');
    const strategy = (c.strategy || '').replace(/_/g, ' ');
    const regime = c.regime || '';
    const mechanism = (c.mechanism || '').substring(0, 80);
    const priority = c.priority || '';
    const failures = c.failures || 0;
    const priBadge = priority === 'high' ? 'badge-emerald' : priority === 'medium' ? 'badge-amber' : 'badge-muted';
    return '<div class="p-3 rounded-lg" style="background:#141820;border:1px solid #222430">' +
      '<div class="flex items-center justify-between mb-1">' +
        '<span class="text-xs font-semibold" style="color:#2FCA94">' + doctrine + '</span>' +
        (priority ? '<span class="badge ' + priBadge + '" style="font-size:0.6rem">' + priority + '</span>' : '') +
      '</div>' +
      '<div class="text-xs" style="color:#8890B0">' + strategy + '</div>' +
      (regime ? '<div class="text-xs mt-0.5" style="color:#6A7080">regime: ' + regime + '</div>' : '') +
      (mechanism ? '<div class="text-xs mt-1" style="color:#6A7080;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + mechanism + '</div>' : '') +
      (failures > 0 ? '<div class="text-xs mt-1" style="color:#E08878">' + failures + ' lineage failure' + (failures !== 1 ? 's' : '') + '</div>' : '') +
    '</div>';
  }).join('');
}

// ── Self-Edits Queue ─────────────────────────────
function renderSelfEdits(edits) {
  const el = document.getElementById('self-edits');
  const countEl = document.getElementById('self-edit-count');
  if (!edits || edits.length === 0) {
    el.innerHTML = '<div class="text-xs" style="color:#6A7080">No self-edits queued</div>';
    countEl.textContent = '0 queued';
    return;
  }
  countEl.textContent = edits.length + ' queued';
  el.innerHTML = edits.map(e => {
    const parent = (e.parent_candidate_id || '').replace(/^auto-/, '').substring(0, 30);
    const editId = (e.edit_id || '').substring(0, 25);
    const priority = (e.priority || 0).toFixed(2);
    const failures = (e.failure_modes || []).slice(0, 3);
    const allowed = (e.allowed_edits || []).slice(0, 3);
    return '<div class="p-3 rounded-lg" style="background:#141820;border:1px solid #222430">' +
      '<div class="flex items-center justify-between mb-1">' +
        '<span class="text-xs font-semibold" style="color:#68A8D8">' + editId + '</span>' +
        '<span class="badge badge-amber" style="font-size:0.6rem">p=' + priority + '</span>' +
      '</div>' +
      '<div class="text-xs" style="color:#8890B0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">from: ' + parent + '</div>' +
      (failures.length > 0 ? '<div class="text-xs mt-1" style="color:#E08878">' + failures.map(f => f.replace(/_/g,' ')).join(', ') + '</div>' : '') +
      (allowed.length > 0 ? '<div class="text-xs mt-1" style="color:#6A7080">edits: ' + allowed.map(a => a.replace(/\./g,' ')).join(', ') + '</div>' : '') +
    '</div>';
  }).join('');
}

// ── Top Candidates Table ──────────────────────────
function sortCandidates(field) {
  if (_candidateSort.field === field) _candidateSort.asc = !_candidateSort.asc;
  else { _candidateSort.field = field; _candidateSort.asc = false; }
  renderTopCandidates();
}

function renderTopCandidates() {
  if (!_autoloopData) return;
  const cands = [...(_autoloopData.backtest.candidates || [])];
  const filterStrat = document.getElementById('cand-filter-strategy').value;
  const filterVerdict = document.getElementById('cand-filter-verdict').value;

  let filtered = cands;
  if (filterStrat) filtered = filtered.filter(c => c.strategy === filterStrat);
  if (filterVerdict) filtered = filtered.filter(c => c.verdict === filterVerdict);

  const { field, asc } = _candidateSort;
  filtered.sort((a, b) => {
    const va = a[field] || 0, vb = b[field] || 0;
    return asc ? va - vb : vb - va;
  });

  document.getElementById('cand-count').textContent = filtered.length + ' of ' + cands.length;

  // Populate strategy filter options
  const stratSelect = document.getElementById('cand-filter-strategy');
  const strategies = [...new Set(cands.map(c => c.strategy).filter(Boolean))].sort();
  const curStrat = stratSelect.value;
  stratSelect.innerHTML = '<option value="">All Strategies</option>' +
    strategies.map(s => '<option value="' + s + '"' + (s===curStrat?' selected':'') + '>' + s.replace(/_/g,' ') + '</option>').join('');

  const tbody = document.getElementById('cand-body');
  tbody.innerHTML = filtered.map((c, i) => {
    const rank = i + 1;
    const rankHtml = rank <= 3 ? '<span style="color:' + C.emerald + ';font-weight:700">' + rank + '</span>' : rank;
    const wrColor = c.wr >= 0.6 ? C.emerald : c.wr >= 0.52 ? C.sky : C.muted;
    const verdictBadge = c.verdict === 'approve' ? '<span class="badge badge-emerald" style="font-size:0.65rem;padding:2px 8px">Approve</span>'
      : c.verdict === 'defer' ? '<span class="badge badge-amber" style="font-size:0.65rem;padding:2px 8px">Defer</span>'
      : '<span class="badge badge-muted" style="font-size:0.65rem;padding:2px 8px">Reject</span>';
    const p = 'padding:6px 8px 6px 0;';
    return '<tr style="border-bottom:1px solid #1E2230">' +
      '<td style="' + p + '">' + rankHtml + '</td>' +
      '<td style="' + p + 'color:' + wrColor + ';font-weight:700">' + (c.wr*100).toFixed(1) + '%</td>' +
      '<td style="' + p + 'color:#8890B0">' + (c.wf ? c.wf.toFixed(2) : '--') + '</td>' +
      '<td style="' + p + 'color:#8890B0">' + (c.sharpe ? c.sharpe.toFixed(2) : '--') + '</td>' +
      '<td style="' + p + 'color:#8890B0">' + (c.dd ? (c.dd*100).toFixed(1) + '%' : '--') + '</td>' +
      '<td style="' + p + '">' + (c.trades || '--') + '</td>' +
      '<td style="' + p + 'font-size:0.8rem">' + (c.strategy || '').replace(/_/g,' ') + '</td>' +
      '<td style="' + p + 'font-size:0.8rem;color:#8890B0">' + (c.doctrine || '').replace(/_/g,' ') + '</td>' +
      '<td style="' + p + 'font-size:0.8rem;color:#6A7080">' + (c.regime || '') + '</td>' +
      '<td style="' + p + 'color:' + (c.readiness >= 0.8 ? C.emerald : C.muted) + '">' + (c.readiness ? c.readiness.toFixed(2) : '--') + '</td>' +
      '<td style="' + p + '">' + verdictBadge + '</td>' +
    '</tr>';
  }).join('');
}

// ── Walk-Forward Gate ─────────────────────────────
let _wfScatterInstance = null;
function renderWfGate(scatter) {
  if (!scatter || scatter.length === 0) return;

  const passed = scatter.filter(s => s.wf >= 0.8).length;
  const total = scatter.length;
  const pct = (passed / total * 100).toFixed(0);

  document.getElementById('wf-summary').textContent = passed + ' of ' + total + ' pass WF >= 0.8';
  document.getElementById('wf-coverage-pct').textContent = pct + '%';
  document.getElementById('wf-coverage-bar').style.width = pct + '%';
  document.getElementById('wf-passed').textContent = passed + ' passed';
  document.getElementById('wf-total').textContent = total + ' total';

  // Scatter chart
  destroyChart('wfScatter');
  const ctx = document.getElementById('wfScatterChart');
  if (!ctx) return;

  _chartInstances.wfScatter = new Chart(ctx.getContext('2d'), {
    type: 'scatter',
    data: {
      datasets: [
        { label: 'WF >= 0.8 (diagonal)', data: [{x:40,y:0.8},{x:70,y:0.8}], type:'line', borderColor:'#2FCA9444', borderDash:[4,4], borderWidth:1, pointRadius:0, fill:false },
        {
          label: 'Candidates',
          data: scatter.map(s => ({x: s.wr*100, y: s.wf})),
          backgroundColor: scatter.map(s => s.wf >= 0.8 ? C.emerald + '80' : C.muted + '60'),
          borderColor: scatter.map(s => s.wf >= 0.8 ? C.emerald : C.muted),
          pointRadius: 5, pointHoverRadius: 7, borderWidth: 1,
        },
      ]
    },
    options: {
      ...CHART_DEFAULTS,
      plugins: { legend: { display: false } },
      scales: {
        x: { ...CHART_DEFAULTS.scales.x, title: {display:true, text:'Win Rate %', color:C.muted, font:{size:9}}, min: 40, max: 70 },
        y: { ...CHART_DEFAULTS.scales.y, title: {display:true, text:'Walk-Forward', color:C.muted, font:{size:9}}, min: 0, max: 1 },
      },
    },
  });
}

// ── Autoloop Lanes ────────────────────────────────
let alCycleChartInstance = null;
function renderAutoloopLanes(data) {
  if (!data) return;
  const s = data.state || {};
  const doc = data.doctrine || {};
  const bt = data.backtest || {};
  const pt = data.paper_trade || {};

  const badge = document.getElementById('autoloop-status-badge');
  const st = s.status || 'unknown';
  badge.textContent = st;
  badge.style.color = st === 'running' ? C.emerald : st === 'idle' ? C.amber : C.muted;
  badge.style.border = '1px solid ' + (st === 'running' ? C.emerald : st === 'idle' ? C.amber : '#2A2E3C');

  document.getElementById('al-noop').textContent = s.noop_streak || 0;
  document.getElementById('al-doctrine-cards').textContent = doc.card_count || 0;
  document.getElementById('al-doctrine-packets').textContent = doc.packet_count || 0;
  document.getElementById('al-bt-candidates').textContent = bt.candidate_count || 0;
  document.getElementById('al-variety').textContent = bt.variety_count || 0;
  document.getElementById('al-trials').textContent = bt.trial_count || 0;
  document.getElementById('al-pt-queue').textContent = pt.queue_count || 0;
  document.getElementById('al-pt-ready').textContent = pt.promotion_ready || 0;
  document.getElementById('al-pt-sig').textContent = pt.significant || 0;

  // Cycle timeline
  const timeline = data.cycle_timeline || [];
  if (timeline.length > 0) {
    document.getElementById('al-timeline-range').textContent = '(C' + timeline[0].cycle + '-C' + timeline[timeline.length-1].cycle + ')';
    if (alCycleChartInstance) alCycleChartInstance.destroy();
    const ctx = document.getElementById('al-cycle-chart').getContext('2d');
    alCycleChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: timeline.map(c => 'C' + c.cycle),
        datasets: [
          { label: 'Learning', data: timeline.map(c => c.learning ? 1 : 0), backgroundColor: C.emerald, barPercentage: 0.8 },
          { label: 'Backtest', data: timeline.map(c => c.backtest ? 1 : 0), backgroundColor: C.sky, barPercentage: 0.8 },
          { label: 'Paper Trade', data: timeline.map(c => c.paper_trade ? 1 : 0), backgroundColor: C.amber, barPercentage: 0.8 },
        ]
      },
      options: { ...CHART_DEFAULTS,
        scales: {
          x: { stacked: true, grid: { display: false }, ticks: { color: C.muted, font: { size: 9, family: 'DM Mono' }, maxRotation: 0 } },
          y: { stacked: true, display: false, max: 3 },
        }
      }
    });
  }

  // Recent doctrine cards
  const docList = document.getElementById('al-doctrine-list');
  const recentCards = doc.recent_cards || [];
  if (recentCards.length > 0) {
    docList.innerHTML = recentCards.map(c => {
      const doctrine = (c.doctrine || '').replace(/_/g, ' ');
      const strategy = (c.strategy || '').replace(/_/g, ' ');
      return '<div class="card px-3 py-2" style="background:#141820;min-width:160px;max-width:240px">' +
        '<div class="text-xs font-semibold" style="color:#2FCA94">' + doctrine + '</div>' +
        '<div class="text-xs" style="color:#8890B0">' + strategy + '</div>' +
      '</div>';
    }).join('');
  }
}

// ── Live Trading ──────────────────────────────────
const REGIME_COLORS = { compression:'#68A8D8', range:'#68A8D8', trend:'#D8C868', event_driven:'#f43f5e', high_vol:'#f97316', fear_shock:'#E08878' };

document.addEventListener('DOMContentLoaded', function() {
  const tabs = document.getElementById('live-period-tabs');
  if (!tabs) return;
  tabs.addEventListener('click', function(e) {
    const btn = e.target.closest('.live-period-tab');
    if (!btn) return;
    _livePeriod = btn.dataset.period;
    tabs.querySelectorAll('.live-period-tab').forEach(t => { t.style.background='transparent'; t.style.color=C.muted; });
    btn.style.background='#222430'; btn.style.color=C.fg;
    if (_lastLivePtData) renderLivePt(_lastLivePtData);
  });
});

function renderLivePt(data) {
  if (!data) return;
  _lastLivePtData = data;

  const statusBadge = document.getElementById('live-pt-status-badge');
  statusBadge.innerHTML = data.status === 'running'
    ? '<span class="badge badge-emerald">LIVE</span>'
    : '<span class="badge badge-sky">OFFLINE</span>';

  const ps = (data.period_stats || {})[_livePeriod] || {};
  document.getElementById('live-settlements').textContent = ps.settlements || 0;
  document.getElementById('live-trades-count').textContent = ps.trades || 0;
  document.getElementById('live-wins-count').textContent = ps.wins || 0;
  document.getElementById('live-losses-count').textContent = ps.losses || 0;
  const acc = ps.accuracy || 0;
  const accEl = document.getElementById('live-accuracy');
  accEl.textContent = ps.trades > 0 ? acc + '%' : '--';
  accEl.style.color = acc >= 50 ? C.emerald : (ps.trades > 0 ? C.red : C.muted);
  document.getElementById('live-agents-strats').textContent = (data.agents_loaded || 0) + ' / ' + (data.strategies_loaded || 0);

  // Contracts
  const contractsDiv = document.getElementById('live-contracts');
  const contracts = data.current_contracts || {};
  const keys = Object.keys(contracts).sort();
  if (keys.length > 0) {
    contractsDiv.innerHTML = keys.map(key => {
      const c = contracts[key];
      const preds = c.predictions || {};
      const entries = Object.entries(preds);
      const longs = entries.filter(([,p]) => p === 'up').length;
      const shorts = entries.filter(([,p]) => p === 'down').length;
      const skips = entries.filter(([,p]) => p === 'skip').length;
      const tf = c.timeframe || '?';
      const regime = c.regime || 'unknown';
      const asset = key.split(':')[0] || '?';
      return '<div class="card p-3" style="background:#141820">' +
        '<div class="flex items-center justify-between mb-1">' +
          '<span class="text-xs font-semibold">' + asset + ' ' + tf + '</span>' +
          '<span class="text-xs" style="color:#6A7080">' + regime + '</span>' +
        '</div>' +
        '<div class="flex items-center gap-2">' +
          (longs > 0 ? '<span class="badge badge-emerald" style="font-size:0.6rem">' + longs + ' LONG</span>' : '') +
          (shorts > 0 ? '<span class="badge badge-red" style="font-size:0.6rem">' + shorts + ' SHORT</span>' : '') +
          '<span style="font-size:0.6rem;color:#6A7080">' + skips + ' skip</span>' +
        '</div></div>';
    }).join('');
  } else {
    contractsDiv.innerHTML = '<div style="padding:12px;text-align:center;color:#6A7080;font-size:0.8rem">Start: <span style="font-family:DM Mono,monospace;color:#8890B0">python live_paper_trader.py --assets BTC --per-strategy 3</span></div>';
  }

  // Settlements
  const settlementsDiv = document.getElementById('live-settlements-list');
  const settlements = (data.recent_settlements || []).reverse();
  if (settlements.length > 0) {
    settlementsDiv.innerHTML = settlements.slice(0, 15).map(s => {
      const agents = s.agents || {};
      const trades = Object.values(agents).filter(a => a.prediction !== 'skip');
      const correct = trades.filter(a => a.correct).length;
      const total = trades.length;
      const accuracy = total > 0 ? (correct / total * 100).toFixed(0) : 0;
      const dirColor = s.direction === 'up' ? C.emerald : C.red;
      let ts = '';
      try { ts = new Date(s.ts).toLocaleTimeString(); } catch {}
      return '<div class="flex items-center gap-2 py-1" style="border-bottom:1px solid #1E2230;font-size:0.75rem">' +
        '<span style="color:#6A7080;min-width:60px">' + ts + '</span>' +
        '<span style="font-weight:600">' + (s.asset || '?') + '</span>' +
        '<span style="color:' + dirColor + ';font-weight:700">' + (s.direction || '?').toUpperCase() + '</span>' +
        '<span style="margin-left:auto;color:' + (total > 0 && correct/total >= 0.5 ? C.emerald : C.red) + '">' +
          (total > 0 ? correct + '/' + total + ' (' + accuracy + '%)' : 'skip') +
        '</span></div>';
    }).join('');
  }
}

// ── Main Loop ─────────────────────────────────────
async function refresh() {
  const [autoloop, cycleFeed, candidateHistory, stratDiversity, researcherHealth, livePt] = await Promise.all([
    fetchJSON('/api/autoloop-status'),
    fetchJSON('/api/cycle-feed'),
    fetchJSON('/api/candidate-history'),
    fetchJSON('/api/strategy-diversity'),
    fetchJSON('/api/researcher-health'),
    fetchJSON('/api/live-pt'),
  ]);

  _autoloopData = autoloop;
  _cycleFeedData = cycleFeed;

  if (autoloop) {
    renderTopStats(autoloop);
    renderAutoloopLanes(autoloop);
    renderStrategyPerformance(autoloop.strategy_family_stats);
    renderDoctrineInsights(autoloop.doctrine ? autoloop.doctrine.recent_cards : []);
    renderTopCandidates();
    renderSelfEdits(autoloop.self_edits);
    renderWfGate(autoloop.wf_scatter);
  }

  if (cycleFeed) renderCycleFeed();
  if (candidateHistory) {
    renderCandidateGrowth(candidateHistory);
    renderBacktestProduction(candidateHistory);
  }
  if (stratDiversity) renderStrategyDiversity(stratDiversity);
  if (researcherHealth) renderResearcherHealth(researcherHealth);
  renderLivePt(livePt);

  document.getElementById('clock').textContent = new Date().toLocaleTimeString();
  document.getElementById('footer-status').textContent = 'Last update: ' + new Date().toLocaleTimeString();
}

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
  #tooltip { display:none; position:absolute; background:#141820; border:1px solid #2A2E3C; border-radius:8px; padding:12px; font-size:0.75rem; pointer-events:none; z-index:100; max-width:300px; }
  ::-webkit-scrollbar { width: 8px; }
  ::-webkit-scrollbar-track { background: #141820; }
  ::-webkit-scrollbar-thumb { background: #2A2E3C; border-radius: 4px; }
  * { scrollbar-width: thin; scrollbar-color: #2A2E3C #141820; }
</style>
</head>
<body>
<div class="ctrl-bar" style="border-bottom-width:2px">
  <a href="/" style="color:#6A7080;text-decoration:none;font-size:0.8rem" onmouseover="this.style.color='#2FCA94'" onmouseout="this.style.color='#6A7080'">&larr; Dashboard</a>
  <h1 style="font-size:1.25rem;font-weight:700;margin:0">Strategy Evolution Graph</h1>
  <div style="margin-left:auto;display:flex;gap:12px;align-items:center">
    <span class="ctrl-label" id="viz-nodes">-- nodes</span>
    <span class="ctrl-label" id="viz-edges">-- edges</span>
  </div>
</div>
<div class="ctrl-bar" style="background:#0E1018">
  <div style="display:flex;align-items:center;gap:6px">
    <span class="ctrl-label">Min WR:</span>
    <input type="range" id="c-min-wr" min="0" max="75" value="0" step="1" style="width:90px;accent-color:#2FCA94">
    <span class="ctrl-label" id="c-min-wr-lbl">0%</span>
  </div>
  <div style="display:flex;align-items:center;gap:6px">
    <span class="ctrl-label">Strategy:</span>
    <select id="c-strategy" class="ctrl-input" style="min-width:140px"><option value="">All</option></select>
  </div>
  <button onclick="loadGraph()" class="ctrl-btn" style="margin-left:auto">Load Graph</button>
</div>
<div id="graph-wrap" style="flex:1;position:relative;overflow:hidden">
  <canvas id="gc"></canvas>
  <div id="tooltip"></div>
  <div id="loading" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#6A7080;font-size:0.85rem">
    Click "Load Graph" to visualize candidates
  </div>
</div>
<script>
const STRAT_COLORS = {
  wedge_exhaustion_reversal:'#2FCA94', ema_pullback_long:'#68A8D8',
  bollinger_squeeze_breakout:'#E8B86D', range_reclaim_rotation:'#a78bfa',
  ema_trend_continuation:'#f472b6', momentum_breakout:'#22d3ee',
  funding_mean_revert:'#f97316', rsi_extreme_reversion:'#e879f9',
};

let transform = d3.zoomIdentity;
let graphNodes = [], graphEdges = [], hoveredNode = null, simulation = null;

document.getElementById('c-min-wr').addEventListener('input', function() {
  document.getElementById('c-min-wr-lbl').textContent = this.value + '%';
});

async function loadGraph() {
  const mw = parseInt(document.getElementById('c-min-wr').value) / 100;
  const st = document.getElementById('c-strategy').value;
  let url = '/api/evolution-graph?min_wr=' + mw;
  if (st) url += '&strategy=' + st;

  document.getElementById('loading').textContent = 'Loading...';
  document.getElementById('loading').style.display = 'flex';

  try {
    const resp = await fetch(url);
    const data = await resp.json();
    document.getElementById('viz-nodes').textContent = data.node_count + ' nodes';
    document.getElementById('viz-edges').textContent = data.edge_count + ' edges';

    const sel = document.getElementById('c-strategy');
    const cur = sel.value;
    sel.innerHTML = '<option value="">All (' + data.strategies.length + ')</option>';
    data.strategies.forEach(s => {
      const o = document.createElement('option'); o.value = s; o.textContent = s.replace(/_/g,' ');
      if (s === cur) o.selected = true; sel.appendChild(o);
    });

    document.getElementById('loading').style.display = 'none';
    initGraph(data);
  } catch(err) {
    document.getElementById('loading').textContent = 'Error: ' + err.message;
  }
}

function nodeRadius(n) { return 3 + Math.max(0, (n.wr - 0.4)) * 20; }

function initGraph(data) {
  const canvas = document.getElementById('gc');
  const wrap = document.getElementById('graph-wrap');
  canvas.width = wrap.clientWidth; canvas.height = wrap.clientHeight;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const nodes = data.nodes.map(n => ({...n}));
  graphNodes = nodes;

  if (simulation) simulation.stop();
  simulation = d3.forceSimulation(nodes)
    .force('charge', d3.forceManyBody().strength(-15).distanceMax(200))
    .force('center', d3.forceCenter(W/2, H/2))
    .force('collide', d3.forceCollide(d => nodeRadius(d) + 2))
    .force('x', d3.forceX(W/2).strength(0.02))
    .force('y', d3.forceY(H/2).strength(0.02))
    .alphaDecay(0.02)
    .on('tick', () => {
      ctx.save(); ctx.clearRect(0,0,W,H);
      ctx.translate(transform.x, transform.y); ctx.scale(transform.k, transform.k);
      for (const n of nodes) {
        const r = nodeRadius(n);
        const c = STRAT_COLORS[n.strategy] || '#6A7080';
        ctx.globalAlpha = n.elite ? 1 : n.viable ? 0.6 : 0.25;
        ctx.fillStyle = c;
        ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI*2); ctx.fill();
        if (n.elite) { ctx.strokeStyle='rgba(255,255,255,0.3)'; ctx.lineWidth=1; ctx.stroke(); }
      }
      ctx.globalAlpha = 1; ctx.restore();
    });

  d3.select(canvas).call(d3.zoom().scaleExtent([0.15,10]).on('zoom', ev => { transform = ev.transform; }));

  canvas.onmousemove = function(ev) {
    const rect = canvas.getBoundingClientRect();
    const mx = (ev.clientX - rect.left - transform.x) / transform.k;
    const my = (ev.clientY - rect.top - transform.y) / transform.k;
    let hit = null;
    for (const n of nodes) { const dx=n.x-mx, dy=n.y-my; if (dx*dx+dy*dy < (nodeRadius(n)+3)**2) { hit=n; break; } }
    const tip = document.getElementById('tooltip');
    if (hit) {
      tip.style.display='block';
      tip.style.left = Math.min(ev.clientX-rect.left+14, W-300) + 'px';
      tip.style.top = Math.min(ev.clientY-rect.top-10, H-120) + 'px';
      tip.innerHTML = '<div style="font-weight:700;margin-bottom:4px">' + hit.id + '</div>' +
        '<div style="color:#8890B0">' + hit.strategy.replace(/_/g,' ') + '</div>' +
        '<div style="margin-top:4px">WR <span style="color:#2FCA94;font-weight:700">' + (hit.wr*100).toFixed(1) + '%</span> | WF ' + hit.wf.toFixed(2) + ' | ' + hit.trades + ' trades</div>';
    } else { tip.style.display='none'; }
  };
}

window.addEventListener('DOMContentLoaded', () => { loadGraph(); });
</script>
</body>
</html>
"""


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8502)
