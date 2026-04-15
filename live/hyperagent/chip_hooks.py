"""Chip hooks for Spark Researcher integration (spark-hook-io.v1).

Entry point called by Spark Researcher:
  python live/hyperagent/chip_hooks.py evaluate --input hook_input.json --output hook_output.json
  python live/hyperagent/chip_hooks.py suggest  --input hook_input.json --output hook_output.json
  python live/hyperagent/chip_hooks.py packets  --input hook_input.json --output hook_output.json
  python live/hyperagent/chip_hooks.py watchtower --input hook_input.json --output hook_output.json

Reads REAL autoloop artifacts (backtest summary, autoloop state, doctrine cards,
mutation trials) to provide grounded responses to each hook.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ARTIFACTS = REPO_ROOT / "artifacts"
BACKTEST_SUMMARY = ARTIFACTS / "backtests" / "heavy_backtest_summary.json"
AUTOLOOP_STATE = ARTIFACTS / "recursion" / "autoloop_state.json"
MUTATION_TRIALS = ARTIFACTS / "recursion" / "mutation_trials.json"
VARIETY_BACKLOG = ARTIFACTS / "recursion" / "variety_backlog.json"
CONTRADICTION_PROBES = ARTIFACTS / "recursion" / "contradiction_probes.json"
DOCTRINE_CARDS = REPO_ROOT / "docs" / "doctrine-cards"


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def _write(path: str, payload: dict) -> None:
    Path(path).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _load_json(path: Path, fallback: Any = None) -> Any:
    if fallback is None:
        fallback = {}
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return fallback


def _mutations(payload: dict) -> dict[str, str]:
    candidate = payload.get("candidate", {})
    raw = candidate.get("mutations", {}) if isinstance(candidate, dict) else {}
    return {str(k): str(v) for k, v in raw.items()}


# ── Data loaders ─────────────────────────────────────────────────────────


def _load_backtest_rows() -> list[dict]:
    """Load all candidate rows from heavy_backtest_summary.json."""
    data = _load_json(BACKTEST_SUMMARY)
    rows = data.get("rows", []) if isinstance(data, dict) else []
    return [r for r in rows if isinstance(r, dict)]


def _load_autoloop_state() -> dict:
    return _load_json(AUTOLOOP_STATE)


def _load_doctrine_cards() -> list[dict]:
    """Load all doctrine card JSON files."""
    cards = []
    if not DOCTRINE_CARDS.exists():
        return cards
    for path in sorted(DOCTRINE_CARDS.glob("*.json")):
        card = _load_json(path)
        if isinstance(card, dict) and card.get("card_id"):
            cards.append(card)
    return cards


def _load_variety_backlog() -> list[dict]:
    data = _load_json(VARIETY_BACKLOG, [])
    return data if isinstance(data, list) else []


def _load_contradiction_probes() -> list[dict]:
    data = _load_json(CONTRADICTION_PROBES, [])
    return data if isinstance(data, list) else []


def _find_candidate(rows: list[dict], candidate_id: str, strategy_id: str, doctrine_id: str) -> dict | None:
    """Find a matching candidate row by ID or strategy+doctrine combo."""
    if candidate_id:
        for row in rows:
            if row.get("candidate_id") == candidate_id:
                return row
    if strategy_id or doctrine_id:
        for row in rows:
            muts = row.get("mutations", {})
            if strategy_id and muts.get("strategy_id") != strategy_id:
                continue
            if doctrine_id and muts.get("doctrine_id") != doctrine_id:
                continue
            return row
    return None


# ── EVALUATE ──────────────────────────────────────────────────────────────


def evaluate(payload: dict) -> dict:
    """Evaluate a candidate using real backtest results from the autoloop."""
    muts = _mutations(payload)
    candidate_id = payload.get("candidate", {}).get("candidate_id", "")
    strategy_id = muts.get("strategy_id", "")
    doctrine_id = muts.get("doctrine_id", "")

    rows = _load_backtest_rows()
    match = _find_candidate(rows, candidate_id, strategy_id, doctrine_id)

    if match:
        metrics = match.get("metrics", {})
        result = match.get("result", {})
        wr = float(metrics.get("win_rate", 0))
        wf = float(result.get("walk_forward_consistency", 0))
        sharpe = float(metrics.get("sharpe_ratio", 0))
        max_dd = float(metrics.get("max_drawdown", 1.0))
        profit = float(metrics.get("profitability_score", 0))
        trade_count = int(result.get("trade_count", 0))
        confidence = float(metrics.get("verdict_confidence", 0))
        readiness = float(metrics.get("paper_trade_readiness", 0))
        mechanism = result.get("mechanism", "")
        boundary = result.get("boundary", "")
        regime_stats = result.get("regime_stats", {})
        stress_stats = result.get("stress_stats", {})
        wf_stats = result.get("walk_forward_stats", [])
    else:
        # No match — return zeroed metrics so the researcher knows
        wr, wf, sharpe, max_dd = 0.0, 0.0, 0.0, 1.0
        profit, trade_count, confidence, readiness = 0.0, 0, 0.3, 0.0
        mechanism = "No matching candidate found in backtest summary."
        boundary = "Candidate has not been backtested yet."
        regime_stats, stress_stats, wf_stats = {}, {}, []

    # Verdict logic matching autoloop gates
    if wr >= 0.58 and wf >= 0.8:
        verdict = "approve"
        next_step = "queue_for_paper_trade"
    elif wr >= 0.52 and wf >= 0.6:
        verdict = "defer"
        next_step = "hold_for_more_backtest_evidence"
    else:
        verdict = "reject"
        next_step = "run_contradiction_probe"

    stdout = "\n".join([
        f"profitability_score: {profit}",
        f"sharpe_ratio: {sharpe}",
        f"max_drawdown: {max_dd}",
        f"win_rate: {wr}",
        f"walk_forward_consistency: {wf}",
        f"trade_count: {trade_count}",
        f"paper_trade_readiness: {readiness}",
        f"verdict: {verdict}",
    ])

    return {
        "returncode": 0,
        "stdout": stdout,
        "stderr": "",
        "metrics": {
            "profitability_score": profit,
            "sharpe_ratio": sharpe,
            "max_drawdown": max_dd,
            "win_rate": wr,
            "walk_forward_consistency": wf,
            "paper_trade_readiness": readiness,
            "verdict_confidence": confidence,
        },
        "result": {
            "claim": "Evaluated against real walk-forward backtest data from the autoloop.",
            "verdict": verdict,
            "mechanism": mechanism,
            "boundary": boundary,
            "recommended_next_step": next_step,
            "evidence_lane": "backtest_benchmark",
            "trade_count": trade_count,
            "walk_forward_consistency": wf,
            "walk_forward_stats": wf_stats,
            "regime_stats": regime_stats,
            "stress_stats": stress_stats,
        },
    }


# ── SUGGEST ───────────────────────────────────────────────────────────────


def suggest(payload: dict) -> dict:
    """Suggest next candidates based on backtest results and variety gaps."""
    rows = _load_backtest_rows()
    variety = _load_variety_backlog()

    # Sort candidates by win rate descending
    ranked = sorted(rows, key=lambda r: float(r.get("metrics", {}).get("win_rate", 0)), reverse=True)

    # Collect strategy families and their best results
    family_best: dict[str, dict] = {}
    for row in ranked:
        strat = row.get("mutations", {}).get("strategy_id", "unknown")
        if strat not in family_best:
            family_best[strat] = row

    # Find under-explored regimes
    explored_regimes: set[str] = set()
    for row in rows:
        regime = row.get("mutations", {}).get("market_regime", "")
        if regime:
            explored_regimes.add(regime)

    suggestions = []

    # 1. Cross-mutations of top performers
    top_two = ranked[:2]
    if len(top_two) == 2:
        a_muts = top_two[0].get("mutations", {})
        b_muts = top_two[1].get("mutations", {})
        cross_muts = dict(a_muts)
        cross_muts["doctrine_id"] = b_muts.get("doctrine_id", a_muts.get("doctrine_id", ""))
        suggestions.append({
            "candidate_id": f"suggest-cross-{a_muts.get('strategy_id', 'x')}-{b_muts.get('doctrine_id', 'y')}",
            "candidate_summary": f"Cross-pollinate top strategy ({a_muts.get('strategy_id', '')}) with runner-up doctrine ({b_muts.get('doctrine_id', '')}).",
            "hypothesis": "Cross-mutation of the two best-performing candidates may combine their strengths.",
            "mutations": cross_muts,
        })

    # 2. Variety backlog entries
    for item in variety[:2]:
        if not isinstance(item, dict):
            continue
        strat = item.get("strategy_id", "")
        regime = item.get("market_regime", "")
        if not strat:
            continue
        suggestions.append({
            "candidate_id": f"suggest-variety-{strat}-{regime}",
            "candidate_summary": f"Explore {strat} in {regime} regime (from variety backlog).",
            "hypothesis": f"Under-explored combination: {strat} x {regime}.",
            "mutations": {
                "strategy_id": strat,
                "market_regime": regime,
                "asset_universe": "BTC",
                "timeframe": "15m",
            },
        })

    # 3. Flip the worst performer's doctrine
    if ranked:
        worst = ranked[-1]
        w_muts = dict(worst.get("mutations", {}))
        best_doctrine = ranked[0].get("mutations", {}).get("doctrine_id", "")
        if best_doctrine and w_muts.get("doctrine_id") != best_doctrine:
            w_muts["doctrine_id"] = best_doctrine
            suggestions.append({
                "candidate_id": f"suggest-flip-{w_muts.get('strategy_id', 'x')}-{best_doctrine}",
                "candidate_summary": f"Apply best-performing doctrine to worst-performing strategy.",
                "hypothesis": "If doctrine matters more than strategy, the worst performer may improve with the best doctrine.",
                "mutations": w_muts,
            })

    # Baseline metric from top candidate
    baseline_wr = float(ranked[0].get("metrics", {}).get("win_rate", 0)) if ranked else 0.0

    limit = max(1, int(payload.get("limit", 3) or 3))
    reasons = [
        f"Top candidate WR: {baseline_wr:.1%} — room for improvement via cross-mutation.",
        f"{len(family_best)} strategy families explored — variety gaps remain.",
        f"Walk-forward gate (>=0.8) blocks all current candidates — structural changes needed.",
    ]

    return {
        "baseline_metric": round(baseline_wr, 4),
        "reasons": reasons[:limit],
        "suggestions": suggestions[:limit],
    }


# ── PACKETS ───────────────────────────────────────────────────────────────


def packets(payload: dict) -> dict:
    """Generate knowledge documents from autoloop state for researcher memory."""
    state = _load_autoloop_state()
    rows = _load_backtest_rows()
    cards = _load_doctrine_cards()
    probes = _load_contradiction_probes()

    cycle_count = int(state.get("cycle_count", 0))
    ranked = sorted(rows, key=lambda r: float(r.get("metrics", {}).get("win_rate", 0)), reverse=True)

    docs = []

    # 1. Benchmark evidence — top candidate metrics
    if ranked:
        top = ranked[0]
        m = top.get("metrics", {})
        r = top.get("result", {})
        top_lines = [
            "# Autoloop Benchmark Evidence",
            "",
            f"- cycle_count: {cycle_count}",
            f"- candidate_count: {len(rows)}",
            f"- top_candidate: {top.get('candidate_id', 'unknown')}",
            f"- win_rate: {float(m.get('win_rate', 0)):.1%}",
            f"- sharpe_ratio: {float(m.get('sharpe_ratio', 0)):.4f}",
            f"- max_drawdown: {float(m.get('max_drawdown', 1)):.2%}",
            f"- walk_forward_consistency: {float(r.get('walk_forward_consistency', 0)):.1%}",
            f"- trade_count: {int(r.get('trade_count', 0))}",
            f"- verdict: {r.get('verdict', 'unknown')}",
            "",
            "## Top 5 Candidates",
            "",
            "| Candidate | WR | Sharpe | WF | Verdict |",
            "|-----------|-----|--------|-----|---------|",
        ]
        for c in ranked[:5]:
            cm = c.get("metrics", {})
            cr = c.get("result", {})
            cid = c.get("candidate_id", "?")
            if len(cid) > 40:
                cid = cid[:37] + "..."
            top_lines.append(
                f"| {cid} | {float(cm.get('win_rate', 0)):.1%} "
                f"| {float(cm.get('sharpe_ratio', 0)):.2f} "
                f"| {float(cr.get('walk_forward_consistency', 0)):.0%} "
                f"| {cr.get('verdict', '?')} |"
            )

        docs.append({
            "kind": "benchmark_evidence",
            "slug": "crypto-autoloop-benchmark",
            "title": "Autoloop Benchmark Evidence",
            "content": "\n".join(top_lines),
            "memory_tier": "durable",
        })

    # 2. Grounded doctrine — what the autoloop has learned
    strategy_stats: dict[str, list[float]] = {}
    for row in rows:
        strat = row.get("mutations", {}).get("strategy_id", "unknown")
        wr = float(row.get("metrics", {}).get("win_rate", 0))
        strategy_stats.setdefault(strat, []).append(wr)

    doctrine_lines = [
        "# Grounded Doctrine",
        "",
        f"Based on {len(rows)} backtested candidates across {cycle_count} autoloop cycles.",
        "",
        "## Strategy Family Performance",
        "",
        "| Strategy | Candidates | Best WR | Avg WR |",
        "|----------|-----------|---------|--------|",
    ]
    for strat, wrs in sorted(strategy_stats.items(), key=lambda x: max(x[1]), reverse=True):
        doctrine_lines.append(
            f"| {strat} | {len(wrs)} | {max(wrs):.1%} | {sum(wrs)/len(wrs):.1%} |"
        )

    if cards:
        doctrine_lines.extend([
            "",
            f"## Doctrine Cards ({len(cards)} total)",
            "",
        ])
        for card in cards[:10]:
            doctrine_lines.append(f"- **{card.get('card_id', '?')}**: {card.get('title', card.get('summary', ''))}")

    docs.append({
        "kind": "grounded_doctrine",
        "slug": "crypto-autoloop-doctrine",
        "title": "Autoloop Grounded Doctrine",
        "content": "\n".join(doctrine_lines),
        "memory_tier": "durable",
    })

    # 3. Grounded boundary — dead ends and contradictions
    dead_ends = [r for r in rows if r.get("result", {}).get("verdict") == "reject"]
    boundary_lines = [
        "# Grounded Boundary (Dead Ends)",
        "",
        f"{len(dead_ends)} of {len(rows)} candidates rejected.",
        "",
        "## Common Rejection Patterns",
        "",
    ]
    reject_strategies: dict[str, int] = {}
    for r in dead_ends:
        strat = r.get("mutations", {}).get("strategy_id", "unknown")
        reject_strategies[strat] = reject_strategies.get(strat, 0) + 1
    for strat, count in sorted(reject_strategies.items(), key=lambda x: x[1], reverse=True)[:5]:
        boundary_lines.append(f"- {strat}: {count} rejections")

    if probes:
        boundary_lines.extend([
            "",
            f"## Active Contradictions ({len(probes)})",
            "",
        ])
        for p in probes[:5]:
            if isinstance(p, dict):
                boundary_lines.append(f"- {p.get('probe_id', '?')}: priority {float(p.get('priority', 0)):.2f}")

    docs.append({
        "kind": "grounded_boundary",
        "slug": "crypto-autoloop-dead-ends",
        "title": "Autoloop Dead-End Patterns",
        "content": "\n".join(boundary_lines),
        "memory_tier": "durable",
    })

    return {"documents": docs}


# ── WATCHTOWER ────────────────────────────────────────────────────────────


def watchtower(payload: dict) -> dict:
    """Generate Obsidian-compatible monitoring page from autoloop state."""
    state = _load_autoloop_state()
    rows = _load_backtest_rows()

    cycle_count = int(state.get("cycle_count", 0))
    noop_streak = int(state.get("noop_streak", 0))
    last_finished = state.get("last_cycle_finished_at", "unknown")
    top_candidate_id = state.get("last_top_candidate_id", "none")

    ranked = sorted(rows, key=lambda r: float(r.get("metrics", {}).get("win_rate", 0)), reverse=True)

    # Leaderboard table
    leader_rows = []
    for row in ranked[:10]:
        m = row.get("metrics", {})
        r = row.get("result", {})
        cid = row.get("candidate_id", "?")
        if len(cid) > 50:
            cid = cid[:47] + "..."
        leader_rows.append(
            f"| {cid} | {float(m.get('win_rate', 0)):.1%} "
            f"| {float(m.get('sharpe_ratio', 0)):.2f} "
            f"| {float(r.get('walk_forward_consistency', 0)):.0%} "
            f"| {r.get('verdict', '?')} |"
        )
    leader_table = "\n".join(
        ["| Candidate | WR | Sharpe | WF | Verdict |",
         "|-----------|-----|--------|-----|---------|"]
        + leader_rows
    )

    pages = [
        {
            "path": "07-Domains/Crypto Trading Autoloop/Home.md",
            "content": "\n".join([
                "# Crypto Trading Autoloop",
                "",
                f"- chip: `domain-chip-crypto-trading`",
                f"- cycles: `{cycle_count}`",
                f"- candidates: `{len(rows)}`",
                f"- noop_streak: `{noop_streak}`",
                f"- last_cycle: `{last_finished}`",
                f"- top_candidate: `{top_candidate_id}`",
                "",
                "## Candidate Leaderboard",
                "",
                leader_table,
                "",
                "## Lanes",
                "",
                f"- Learning: last cycle {state.get('last_learning_cycle', 'never')}",
                f"- Backtest: last cycle {state.get('last_backtest_cycle', 'never')}",
                f"- Paper Trade: last cycle {state.get('last_paper_trade_cycle', 'never')}",
                f"- Pending packets: {state.get('pending_packet_count', 0)}",
                f"- Paper trade queue: {state.get('paper_trade_queue_count', 0)}",
            ]),
        },
    ]

    return {"pages": pages}


# ── CLI ───────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="Crypto trading autoloop chip hooks")
    parser.add_argument("hook", choices=["evaluate", "suggest", "packets", "watchtower"])
    parser.add_argument("--input", required=True, help="Input JSON file path")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    args = parser.parse_args()

    payload = _load(args.input)

    dispatch = {
        "evaluate": evaluate,
        "suggest": suggest,
        "packets": packets,
        "watchtower": watchtower,
    }

    result = dispatch[args.hook](payload)
    _write(args.output, result)


if __name__ == "__main__":
    main()
