"""Paper trade statistical significance monitor.

Reads the current paper trade summary and computes:
- Trades needed for 95% confidence (binomial test)
- Current sample size vs required
- Estimated days to reach significance at current trade rate
- Per-candidate readiness assessment
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from safe_write import safe_write_json

REPO_ROOT = Path(__file__).resolve().parents[1]

Z_95 = 1.96
MARGIN_OF_ERROR = 0.05
MIN_MEANINGFUL_TRADES = 40
PROFITABLE_WR_THRESHOLD = 0.54


def _load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def _trades_for_significance(win_rate: float, z: float = Z_95, margin: float = MARGIN_OF_ERROR) -> int:
    """Minimum trades needed for a binomial proportion CI of +/- margin at given z."""
    p = max(0.01, min(0.99, win_rate))
    n = (z ** 2 * p * (1 - p)) / (margin ** 2)
    return max(MIN_MEANINGFUL_TRADES, math.ceil(n))


def _estimate_days_to_target(current_trades: int, target_trades: int, data_days: float) -> float | None:
    """Estimate days remaining to reach target trade count at current rate."""
    if current_trades <= 0 or data_days <= 0:
        return None
    rate_per_day = current_trades / data_days
    remaining = target_trades - current_trades
    if remaining <= 0:
        return 0.0
    return round(remaining / rate_per_day, 1)


def _candidate_assessment(row: dict[str, Any], data_days: float) -> dict[str, Any]:
    """Assess a single paper trade candidate."""
    candidate_id = str(row.get("candidate_id", ""))
    trade_count = int(row.get("trade_count", 0) or 0)
    win_rate = float(row.get("win_rate", 0.5) or 0.5)
    max_drawdown = float(row.get("max_drawdown", 1.0) or 1.0)
    profitability = float(row.get("profitability_score", 0.5) or 0.5)
    recommendation = str(row.get("paper_trade_recommendation", ""))

    target_trades = _trades_for_significance(win_rate)
    days_remaining = _estimate_days_to_target(trade_count, target_trades, data_days)
    has_enough = trade_count >= target_trades

    # Confidence interval on win rate (Wilson score interval simplified)
    if trade_count > 0:
        se = math.sqrt(win_rate * (1 - win_rate) / trade_count)
        wr_lower = max(0, win_rate - Z_95 * se)
        wr_upper = min(1, win_rate + Z_95 * se)
    else:
        wr_lower = 0.0
        wr_upper = 1.0

    # Dynamic drawdown gate for paper trade (cumulative equity DD).
    # Paper trade DD is much larger than per-window backtest DD (0.74-0.99
    # vs 0.05-0.15) because it's computed over the entire 30-day window.
    # Use paper-trade-appropriate base: 0.80 (not backtest's 0.22).
    # At 500 trades: dd_gate = 0.80. DD=0.99 = effectively blown up.
    _dd_ref_n = 500
    _dd_base_pt = 0.80
    dd_gate = min(0.99, _dd_base_pt * (_dd_ref_n / max(1, trade_count)) ** 0.5) if trade_count > 0 else _dd_base_pt

    # Readiness assessment
    if has_enough and wr_lower > 0.5 and max_drawdown <= dd_gate:
        readiness = "ready_for_promotion_review"
    elif has_enough and win_rate > PROFITABLE_WR_THRESHOLD:
        readiness = "statistically_significant_positive"
    elif has_enough:
        readiness = "statistically_significant_marginal"
    elif trade_count >= MIN_MEANINGFUL_TRADES // 2:
        readiness = "accumulating_approaching_significance"
    else:
        readiness = "accumulating_early"

    return {
        "candidate_id": candidate_id,
        "trade_count": trade_count,
        "win_rate": round(win_rate, 4),
        "win_rate_ci_lower": round(wr_lower, 4),
        "win_rate_ci_upper": round(wr_upper, 4),
        "max_drawdown": round(max_drawdown, 4),
        "dd_gate": round(dd_gate, 4),
        "profitability_score": round(profitability, 4),
        "target_trades_for_significance": target_trades,
        "trades_remaining": max(0, target_trades - trade_count),
        "estimated_days_remaining": days_remaining,
        "has_statistical_significance": has_enough,
        "readiness": readiness,
        "paper_trade_recommendation": recommendation,
    }


def run_paper_trade_monitor(repo_root: Path) -> dict[str, Any]:
    """Generate paper trade monitoring report."""
    summary = _load_json(repo_root / "artifacts" / "paper_trade" / "paper_trade_summary.json", {})
    summary = summary if isinstance(summary, dict) else {}
    rows = summary.get("rows", [])
    rows = rows if isinstance(rows, list) else []

    # Estimate data window duration from contract IDs
    data_days = 14.0  # default
    for row in rows:
        start_id = str(row.get("start_contract_id", ""))
        end_id = str(row.get("end_contract_id", ""))
        sample_count = int(row.get("sample_contract_count", 0) or 0)
        if sample_count > 0:
            # 96 contracts per day (15m intervals)
            data_days = max(1.0, sample_count / 96.0)
            break

    assessments = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        assessments.append(_candidate_assessment(row, data_days))

    # Sort by readiness (most ready first)
    readiness_order = {
        "ready_for_promotion_review": 0,
        "statistically_significant_positive": 1,
        "statistically_significant_marginal": 2,
        "accumulating_approaching_significance": 3,
        "accumulating_early": 4,
    }
    assessments.sort(key=lambda a: (readiness_order.get(a["readiness"], 9), -a["trade_count"]))

    ready_count = sum(1 for a in assessments if a["has_statistical_significance"])
    promotion_ready = sum(1 for a in assessments if a["readiness"] == "ready_for_promotion_review")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "data_window_days": round(data_days, 1),
        "total_candidates": len(assessments),
        "statistically_significant_count": ready_count,
        "promotion_ready_count": promotion_ready,
        "candidates": assessments,
    }

    report_path = repo_root / "artifacts" / "paper_trade" / "paper_trade_monitor_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    safe_write_json(report_path, report)
    return report


def main() -> None:
    report = run_paper_trade_monitor(REPO_ROOT)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
