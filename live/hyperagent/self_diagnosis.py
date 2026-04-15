"""Self-Diagnosis — detect evaluation bias and auto-calibrate gates.

DGM-H Gap 7: The system detects when its evaluation criteria don't predict
real-world (holdout/paper-trade) performance, and auto-calibrates gates.

Uses walk-forward holdout split as a proxy for paper-trade divergence:
- Compares full-backtest WR vs holdout-segment WR
- Detects systematic over/under-estimation
- Calibrates viability/elite gates per regime
- Flags agents whose backtest performance is unreliable
"""

from __future__ import annotations

import json
import logging
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SelfDiagnosis:
    """Detect evaluation bias and auto-calibrate viability/elite gates."""

    def __init__(self, archive_root: Path):
        self.archive_root = archive_root
        self.diagnosis_path = archive_root / "self_diagnosis"
        self.diagnosis_path.mkdir(parents=True, exist_ok=True)
        self._calibration_path = self.diagnosis_path / "gate_calibration.json"
        self._bias_log_path = self.diagnosis_path / "bias_analysis.json"

    # ── Core Analysis ─────────────────────────────────────────

    def diagnose(self, performance_log_path: Path) -> dict[str, Any]:
        """Run full self-diagnosis on the evaluation pipeline.

        Analyzes:
        1. Backtest-vs-holdout correlation (do full metrics predict holdout?)
        2. Walk-forward consistency bias (are we over-fitting to early data?)
        3. Regime-specific gate accuracy (do gates work equally across regimes?)
        4. Recommended gate adjustments

        Returns diagnosis report dict.
        """
        entries = self._load_log(performance_log_path)
        if len(entries) < 10:
            return {"status": "insufficient_data", "entries": len(entries)}

        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "entries_analyzed": len(entries),
            "backtest_holdout_correlation": self._analyze_holdout_correlation(entries),
            "walk_forward_bias": self._analyze_wf_bias(entries),
            "regime_gate_accuracy": self._analyze_regime_gates(entries),
            "gate_recommendations": {},
        }

        # Generate gate recommendations based on findings
        report["gate_recommendations"] = self._recommend_gates(report)

        # Save analysis
        self._bias_log_path.write_text(
            json.dumps(report, indent=2), encoding="utf-8",
        )

        return report

    # ── Holdout Correlation ───────────────────────────────────

    def _analyze_holdout_correlation(self, entries: list[dict]) -> dict:
        """Compare full-backtest profitability vs holdout profitability.

        If correlation is low, the backtest is over-fitting to training data
        and our gates aren't predicting real performance.
        """
        pairs = []
        for e in entries:
            fitness = e.get("fitness", {})
            ps = fitness.get("profitability_score", 0)
            holdout = fitness.get("holdout_profitability")
            wr = fitness.get("win_rate", 0)
            # Only include entries that have holdout data (added in Gap 7)
            if ps > 0 and wr > 0 and holdout is not None and holdout > 0:
                pairs.append({"profitability": ps, "holdout": holdout, "win_rate": wr})

        if len(pairs) < 5:
            return {"status": "insufficient_data", "pairs": len(pairs)}

        # Compute simple correlation metrics
        ps_values = [p["profitability"] for p in pairs]
        holdout_values = [p["holdout"] for p in pairs]

        # Mean absolute error between profitability and holdout
        mae = statistics.mean(abs(p - h) for p, h in zip(ps_values, holdout_values))

        # Systematic bias: does backtest consistently over-estimate?
        bias = statistics.mean(p - h for p, h in zip(ps_values, holdout_values))

        # How many agents that passed backtest gates also pass holdout?
        backtest_pass = [p for p in pairs if p["profitability"] >= 0.55]
        if backtest_pass:
            holdout_pass_rate = sum(
                1 for p in backtest_pass if p["holdout"] >= 0.50
            ) / len(backtest_pass)
        else:
            holdout_pass_rate = 0

        # WR-based analysis: agents with high backtest WR
        high_wr = [p for p in pairs if p["win_rate"] >= 0.58]
        if high_wr:
            high_wr_holdout_avg = statistics.mean(p["holdout"] for p in high_wr)
        else:
            high_wr_holdout_avg = 0

        return {
            "status": "analyzed",
            "sample_size": len(pairs),
            "mean_absolute_error": round(mae, 4),
            "systematic_bias": round(bias, 4),
            "bias_direction": "over_estimate" if bias > 0.02 else "under_estimate" if bias < -0.02 else "neutral",
            "holdout_pass_rate": round(holdout_pass_rate, 3),
            "high_wr_holdout_avg_ps": round(high_wr_holdout_avg, 4),
        }

    # ── Walk-Forward Bias ─────────────────────────────────────

    def _analyze_wf_bias(self, entries: list[dict]) -> dict:
        """Detect walk-forward segment bias.

        If early segments consistently perform better than late segments,
        the strategy may be over-fitting to older data patterns.
        """
        segment_scores: dict[str, list[float]] = defaultdict(list)

        for e in entries:
            wf_stats = e.get("fitness", {}).get("walk_forward_stats", [])
            for seg in wf_stats:
                seg_id = seg.get("segment_id", "")
                ps = seg.get("profitability_score")
                if seg_id and ps is not None:
                    try:
                        segment_scores[seg_id].append(float(ps))
                    except (ValueError, TypeError):
                        pass

        if len(segment_scores) < 2:
            return {"status": "insufficient_data"}

        segment_avgs = {}
        for seg_id in sorted(segment_scores.keys()):
            values = segment_scores[seg_id]
            if values:
                segment_avgs[seg_id] = round(statistics.mean(values), 4)

        # Check for temporal degradation (earlier segments better than later)
        avg_list = list(segment_avgs.values())
        if len(avg_list) >= 3:
            early_avg = statistics.mean(avg_list[:2])
            late_avg = statistics.mean(avg_list[-2:])
            temporal_bias = early_avg - late_avg
        else:
            temporal_bias = 0

        return {
            "status": "analyzed",
            "segment_averages": segment_avgs,
            "temporal_bias": round(temporal_bias, 4),
            "bias_type": (
                "early_overfit" if temporal_bias > 0.05
                else "late_degradation" if temporal_bias > 0.02
                else "stable"
            ),
        }

    # ── Regime-Specific Gate Accuracy ─────────────────────────

    def _analyze_regime_gates(self, entries: list[dict]) -> dict:
        """Check if viability/elite gates work equally well across regimes.

        Maybe WF>=1.0 is too strict for high_vol (fewer trades per fold)
        but appropriate for compression.
        """
        by_regime: dict[str, list[dict]] = defaultdict(list)

        for e in entries:
            mutations = e.get("mutations", {})
            regime = mutations.get("extend_regimes", "compression_only")
            fitness = e.get("fitness", {})
            if fitness.get("win_rate", 0) > 0:
                by_regime[regime].append({
                    "wr": fitness.get("win_rate", 0),
                    "wf": fitness.get("wealth_factor", 0),
                    "viable": fitness.get("viable", False),
                    "elite": fitness.get("elite", False),
                    "trade_count": fitness.get("trade_count", 0),
                    "holdout": fitness.get("holdout_profitability", 0),
                })

        regime_analysis = {}
        for regime, agents in by_regime.items():
            if len(agents) < 3:
                continue

            wrs = [a["wr"] for a in agents]
            wfs = [a["wf"] for a in agents]
            trades = [a["trade_count"] for a in agents]
            viable_count = sum(1 for a in agents if a["viable"])
            elite_count = sum(1 for a in agents if a["elite"])

            # Check if current gates are fair for this regime
            # High trade-count regimes should have more elite candidates
            avg_trades = statistics.mean(trades)
            viable_rate = viable_count / len(agents)
            elite_rate = elite_count / len(agents)

            regime_analysis[regime] = {
                "sample_size": len(agents),
                "avg_wr": round(statistics.mean(wrs), 4),
                "avg_wf": round(statistics.mean(wfs), 4),
                "avg_trades": round(avg_trades, 0),
                "viable_rate": round(viable_rate, 3),
                "elite_rate": round(elite_rate, 3),
                "gate_fairness": (
                    "too_strict" if viable_rate < 0.2 and statistics.mean(wrs) > 0.52
                    else "too_lenient" if elite_rate > 0.8
                    else "balanced"
                ),
            }

        return {
            "status": "analyzed" if regime_analysis else "insufficient_data",
            "regimes": regime_analysis,
        }

    # ── Gate Recommendations ──────────────────────────────────

    def _recommend_gates(self, report: dict) -> dict:
        """Generate specific gate adjustment recommendations."""
        recommendations = {}

        # Holdout-based recommendations
        holdout = report.get("backtest_holdout_correlation", {})
        if holdout.get("status") == "analyzed":
            if holdout["bias_direction"] == "over_estimate" and holdout["systematic_bias"] > 0.05:
                recommendations["tighten_profitability_gate"] = {
                    "reason": f"Backtest over-estimates by {holdout['systematic_bias']:.3f}",
                    "current_gate": 0.55,
                    "recommended_gate": round(0.55 + holdout["systematic_bias"] * 0.5, 3),
                }

            if holdout["holdout_pass_rate"] < 0.7:
                recommendations["holdout_gate"] = {
                    "reason": f"Only {holdout['holdout_pass_rate']:.0%} of backtest-passing agents pass holdout",
                    "recommendation": "Add holdout_profitability >= 0.50 as additional gate",
                }

        # Walk-forward bias recommendations
        wf = report.get("walk_forward_bias", {})
        if wf.get("bias_type") == "early_overfit":
            recommendations["recency_weight"] = {
                "reason": f"Early segments outperform late by {wf['temporal_bias']:.3f}",
                "recommendation": "Weight recent walk-forward segments more heavily in WF score",
            }

        # Regime-specific recommendations
        regime_data = report.get("regime_gate_accuracy", {}).get("regimes", {})
        for regime, stats in regime_data.items():
            if stats["gate_fairness"] == "too_strict":
                recommendations[f"loosen_gates_{regime}"] = {
                    "reason": f"Regime '{regime}' has {stats['viable_rate']:.0%} viable rate despite avg WR={stats['avg_wr']:.3f}",
                    "recommendation": f"Consider WF>=0.6 for '{regime}' (currently 0.8)",
                }

        return recommendations

    # ── Calibrated Gates ──────────────────────────────────────

    def get_calibrated_gates(self) -> dict[str, dict]:
        """Return calibrated gate thresholds.

        If calibration exists, return regime-specific gates.
        Otherwise return defaults.
        """
        if self._calibration_path.exists():
            return json.loads(self._calibration_path.read_text(encoding="utf-8"))

        return {
            "default": {
                "viable_wf": 0.8,
                "viable_wr": 0.52,
                "viable_trades": 30,
                "elite_wf": 1.0,
                "elite_wr": 0.58,
                "elite_trades": 50,
            }
        }

    def save_calibrated_gates(self, gates: dict) -> None:
        """Persist calibrated gates."""
        self._calibration_path.write_text(
            json.dumps(gates, indent=2), encoding="utf-8",
        )

    def auto_calibrate(self, performance_log_path: Path) -> dict:
        """Run diagnosis and auto-calibrate gates based on findings.

        Returns the new calibrated gates dict.
        """
        report = self.diagnose(performance_log_path)
        if report.get("status") == "insufficient_data":
            return self.get_calibrated_gates()

        gates = self.get_calibrated_gates()
        recommendations = report.get("gate_recommendations", {})

        # Apply tighter profitability gate if over-estimating
        if "tighten_profitability_gate" in recommendations:
            rec = recommendations["tighten_profitability_gate"]
            gates.setdefault("default", {})["profitability_gate"] = rec["recommended_gate"]

        # Apply regime-specific loosening
        for key, rec in recommendations.items():
            if key.startswith("loosen_gates_"):
                regime = key.replace("loosen_gates_", "")
                gates[regime] = {
                    **gates.get("default", {}),
                    "viable_wf": 0.6,
                    "note": rec["reason"],
                }

        self.save_calibrated_gates(gates)
        logger.info("Auto-calibrated gates: %d regime-specific adjustments", len(gates) - 1)
        return gates

    # ── Helpers ────────────────────────────────────────────────

    def _load_log(self, path: Path) -> list[dict]:
        """Load performance log entries."""
        if not path.exists():
            return []
        entries = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries
