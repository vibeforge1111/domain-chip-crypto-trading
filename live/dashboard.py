"""
DGM-H Evolution Dashboard - Real-Time Trading Strategy Evolution Monitor
=========================================================================
Live dashboard showing the self-improving trading strategy evolution system.

Run: python -m streamlit run dashboard.py
"""

import streamlit as st
import json
import os
import glob
import time
from datetime import datetime, timezone
from pathlib import Path

# --- Config ---
ARCHIVE_DIR = Path(__file__).parent / "archive"
GENERATIONS_DIR = ARCHIVE_DIR / "generations"
META_DIR = ARCHIVE_DIR / "meta_improvements"
DIAG_DIR = ARCHIVE_DIR / "self_diagnosis"

REFRESH_INTERVAL = 10  # seconds

st.set_page_config(
    page_title="DGM-H Evolution Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS ---
st.markdown("""
<style>
    .stMetric {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #0f3460;
    }
    .stMetric label {
        color: #a8b2d1 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #64ffda !important;
        font-size: 2rem !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0.5rem;
    }
    .elite-badge {
        background: linear-gradient(135deg, #00b4d8, #0077b6);
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .viable-badge {
        background: linear-gradient(135deg, #2ec4b6, #168a7a);
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8em;
    }
    .weak-badge {
        background: #333;
        color: #888;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8em;
    }
    h1 {
        background: linear-gradient(90deg, #64ffda, #00b4d8, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
    }
    .live-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #00ff88;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; box-shadow: 0 0 5px #00ff88; }
        50% { opacity: 0.5; box-shadow: 0 0 15px #00ff88; }
        100% { opacity: 1; box-shadow: 0 0 5px #00ff88; }
    }
</style>
""", unsafe_allow_html=True)


# --- Data Loading ---
@st.cache_data(ttl=REFRESH_INTERVAL)
def load_json(path):
    """Load a JSON file, return empty dict/list on failure."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}


@st.cache_data(ttl=REFRESH_INTERVAL)
def load_jsonl_tail(path, n=50):
    """Load last N lines of a JSONL file."""
    try:
        lines = []
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
        tail = lines[-n:] if len(lines) > n else lines
        return [json.loads(l) for l in tail]
    except Exception:
        return []


@st.cache_data(ttl=REFRESH_INTERVAL)
def get_latest_report():
    """Find and load the latest generation report."""
    try:
        reports = sorted(glob.glob(str(GENERATIONS_DIR / "report_*.json")))
        if not reports:
            return {}
        return load_json(reports[-1])
    except Exception:
        return {}


@st.cache_data(ttl=REFRESH_INTERVAL)
def get_recent_reports(n=50):
    """Load the last N generation reports for trend data."""
    try:
        reports = sorted(glob.glob(str(GENERATIONS_DIR / "report_*.json")))
        recent = reports[-n:] if len(reports) > n else reports
        results = []
        for rpath in recent:
            try:
                with open(rpath, "r") as f:
                    results.append(json.load(f))
            except Exception:
                pass
        return results
    except Exception:
        return []


@st.cache_data(ttl=REFRESH_INTERVAL)
def get_recent_elites(n=20):
    """Get the most recent elite agents from performance log."""
    entries = load_jsonl_tail(META_DIR / "performance_log.jsonl", 500)
    elites = []
    for e in reversed(entries):
        fitness = e.get("fitness", {})
        if fitness.get("elite"):
            elites.append(e)
            if len(elites) >= n:
                break
    return elites


@st.cache_data(ttl=REFRESH_INTERVAL)
def get_champion_history():
    """Extract champion progression from performance log."""
    entries = load_jsonl_tail(META_DIR / "performance_log.jsonl", 5000)
    best_wr = 0
    champions = []
    for e in entries:
        fitness = e.get("fitness", {})
        wr = fitness.get("win_rate", 0)
        wf = fitness.get("wealth_factor", 0)
        if wr and wr > best_wr and wf and wf >= 1.0 and fitness.get("elite"):
            best_wr = wr
            champions.append({
                "generation": e.get("generation", 0),
                "agent_id": e.get("agent_id", "?")[:8],
                "win_rate": wr,
                "strategy": e.get("meta_strategy", "?"),
                "trades": fitness.get("trade_count", 0),
            })
    return champions


# --- Load all data ---
latest_report = get_latest_report()
pop = latest_report.get("population_summary", {})
strat_eff = latest_report.get("strategy_effectiveness", {})
paper_trade = load_json(ARCHIVE_DIR / "paper_trade_results.json")
bias = load_json(DIAG_DIR / "bias_analysis.json")
insights_raw = load_json(META_DIR / "synthesized_insights.json")
insights = insights_raw if isinstance(insights_raw, list) else []
recent_reports = get_recent_reports(100)
recent_elites = get_recent_elites(20)

current_gen = latest_report.get("generation", 0)
best_wr = pop.get("best_wr", 0)
avg_wr = pop.get("avg_wr", 0)
elite_count = pop.get("elite", 0)
viable_count = pop.get("viable", 0)
total_pop = pop.get("size", 0)

# --- Header ---
col_title, col_live = st.columns([4, 1])
with col_title:
    st.markdown("# DGM-H Evolution Dashboard")
    st.markdown("Self-improving trading strategy discovery powered by evolutionary search + LLM guards")
with col_live:
    st.markdown(f"""
    <div style="text-align: right; padding-top: 20px;">
        <span class="live-dot"></span>
        <span style="color: #00ff88; font-weight: bold; font-size: 1.1em;">LIVE</span>
        <br/>
        <span style="color: #666; font-size: 0.8em;">Refreshes every {REFRESH_INTERVAL}s</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- Top Metrics Row ---
m1, m2, m3, m4, m5, m6 = st.columns(6)

# Calculate deltas from recent reports
prev_elite = recent_reports[-2].get("population_summary", {}).get("elite", elite_count) if len(recent_reports) >= 2 else elite_count
elite_delta = elite_count - prev_elite

with m1:
    st.metric("Generation", f"{current_gen:,}", delta=None)
with m2:
    st.metric("Best Win Rate", f"{best_wr*100:.1f}%", delta=None)
with m3:
    st.metric("Avg Win Rate", f"{avg_wr*100:.1f}%", delta=None)
with m4:
    st.metric("Elite Agents", f"{elite_count:,}", delta=f"+{elite_delta}" if elite_delta > 0 else None)
with m5:
    st.metric("Viable Agents", f"{viable_count:,}", delta=None)
with m6:
    st.metric("Total Population", f"{total_pop:,}", delta=None)

st.divider()

# --- Main Content: Two columns ---
left_col, right_col = st.columns([3, 2])

with left_col:
    # --- Recent Elite Agents (Live Feed) ---
    st.markdown("### Recent Elite Agents")

    if recent_elites:
        for agent in recent_elites[:10]:
            fitness = agent.get("fitness", {})
            wr = fitness.get("win_rate", 0)
            wf = fitness.get("wealth_factor", 0)
            trades = fitness.get("trade_count", 0)
            gen = agent.get("generation", 0)
            aid = agent.get("agent_id", "?")[:8]
            strategy = agent.get("meta_strategy", "?")
            ts = agent.get("timestamp", "")
            try:
                t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                time_str = t.strftime("%H:%M:%S")
            except Exception:
                time_str = "?"

            # Color code by win rate
            if wr >= 0.65:
                wr_color = "#ffd700"  # gold
                icon = "🏆"
            elif wr >= 0.60:
                wr_color = "#64ffda"  # teal
                icon = "⭐"
            else:
                wr_color = "#a8b2d1"  # silver
                icon = "🧬"

            st.markdown(f"""
            <div style="background: #1a1a2e; padding: 8px 15px; border-radius: 8px; margin-bottom: 6px;
                        border-left: 3px solid {wr_color};">
                <span style="color: #666; font-size: 0.8em;">Gen {gen} | {time_str}</span>
                <span style="float: right; color: #666; font-size: 0.8em;">{strategy}</span>
                <br/>
                {icon} <span style="color: {wr_color}; font-weight: bold; font-size: 1.1em;">{wr*100:.1f}%</span>
                <span style="color: #888; margin-left: 10px;">Agent {aid}</span>
                <span style="color: #666; margin-left: 10px;">{trades} trades | WF={wf:.1f}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Waiting for elite agents...")

    st.markdown("")

    # --- Population Growth Chart ---
    st.markdown("### Population Growth")
    if recent_reports:
        chart_data = []
        for r in recent_reports:
            ps = r.get("population_summary", {})
            chart_data.append({
                "Generation": r.get("generation", 0),
                "Elite": ps.get("elite", 0),
                "Viable": ps.get("viable", 0),
                "Total": ps.get("size", 0),
            })
        if chart_data:
            import pandas as pd
            df = pd.DataFrame(chart_data)
            if len(df) > 0:
                st.line_chart(df.set_index("Generation")[["Elite", "Viable", "Total"]], use_container_width=True)

    # --- Win Rate Distribution (recent agents) ---
    st.markdown("### Elite Production Per Generation")
    if recent_reports:
        elite_prod = []
        for r in recent_reports:
            elite_prod.append({
                "Generation": r.get("generation", 0),
                "New Elite": r.get("new_elite", 0),
                "New Viable": r.get("new_viable", 0),
            })
        if elite_prod:
            import pandas as pd
            df_prod = pd.DataFrame(elite_prod)
            if len(df_prod) > 0:
                st.bar_chart(df_prod.set_index("Generation"), use_container_width=True)


with right_col:
    # --- Meta-Strategy Effectiveness ---
    st.markdown("### Evolution Methods")

    if strat_eff:
        # Sort by improvement rate
        sorted_strats = sorted(strat_eff.items(), key=lambda x: x[1].get("improvement_rate", 0), reverse=True)
        for name, data in sorted_strats:
            rate = data.get("improvement_rate", 0) * 100
            attempts = data.get("attempts", 0)
            improvements = data.get("improvements", 0)
            avg = data.get("avg_wr", 0) * 100
            best = data.get("best_wr", 0) * 100

            # Color by rate
            if rate >= 50:
                bar_color = "#64ffda"
            elif rate >= 20:
                bar_color = "#00b4d8"
            elif rate >= 10:
                bar_color = "#fca311"
            else:
                bar_color = "#e63946"

            display_name = name.replace("_", " ").title()
            st.markdown(f"""
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <span style="color: #ccd6f6; font-weight: bold;">{display_name}</span>
                    <span style="color: {bar_color}; font-weight: bold;">{rate:.0f}%</span>
                </div>
                <div style="background: #1a1a2e; border-radius: 4px; height: 8px; margin: 4px 0;">
                    <div style="background: {bar_color}; width: {min(rate, 100):.0f}%; height: 100%;
                                border-radius: 4px;"></div>
                </div>
                <div style="color: #666; font-size: 0.75em;">
                    {improvements:,}/{attempts:,} improvements | Avg WR: {avg:.1f}% | Best: {best:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # --- Paper Trade Validation ---
    st.markdown("### Paper Trade Validation")

    if isinstance(paper_trade, list) and paper_trade:
        for pt in paper_trade[:3]:
            aid = pt.get("agent_id", "?")[:8]
            bt_wr = pt.get("backtest_wr", 0)
            pt_wr = pt.get("paper_trade_wr", 0)
            delta = pt.get("delta", 0)
            trades = pt.get("paper_trade_trades", 0)
            validation = pt.get("validation", "?")

            delta_color = "#64ffda" if delta >= 0 else "#e63946"
            val_icon = "✅" if validation == "PASS" else "⚠️"

            st.markdown(f"""
            <div style="background: #1a1a2e; padding: 10px 15px; border-radius: 8px; margin-bottom: 8px;">
                <span style="color: #ccd6f6; font-weight: bold;">Agent {aid}</span>
                <span style="float: right;">{val_icon} {validation}</span>
                <br/>
                <span style="color: #888;">Backtest: <strong style="color: #a8b2d1;">{bt_wr*100:.1f}%</strong></span>
                <span style="color: #888; margin-left: 15px;">Paper: <strong style="color: #64ffda;">{pt_wr*100:.1f}%</strong></span>
                <span style="color: {delta_color}; margin-left: 15px; font-weight: bold;">
                    {'+' if delta >= 0 else ''}{delta*100:.1f}%
                </span>
                <span style="color: #666; margin-left: 10px;">({trades} trades)</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No paper trade results yet")

    st.divider()

    # --- System Health ---
    st.markdown("### System Health")

    if bias:
        holdout = bias.get("backtest_holdout_correlation", {})
        wf_bias = bias.get("walk_forward_bias", {})

        mae = holdout.get("mean_absolute_error", 0) * 100
        sys_bias = holdout.get("systematic_bias", 0) * 100
        bias_dir = holdout.get("bias_direction", "?")
        pass_rate = holdout.get("holdout_pass_rate", 0) * 100
        temporal = wf_bias.get("temporal_bias", 0) * 100
        bias_type = wf_bias.get("bias_type", "?")

        h1, h2 = st.columns(2)
        with h1:
            st.metric("Prediction Error", f"{mae:.1f}%")
            st.metric("Pass Rate", f"{pass_rate:.0f}%")
        with h2:
            st.metric("Systematic Bias", f"{sys_bias:.1f}%", delta=f"{bias_dir}")
            st.metric("Temporal Bias", f"{temporal:.1f}%", delta=f"{bias_type}")

    st.divider()

    # --- Top Guard Insights ---
    st.markdown("### Top Guard Discoveries")

    if insights:
        # Filter for guard effectiveness insights and sort by validation count
        guard_insights = [i for i in insights if "guard" in i.get("type", "").lower()
                         or "guard" in i.get("insight", "").lower()]
        guard_insights.sort(key=lambda x: x.get("times_validated", 0), reverse=True)

        for gi in guard_insights[:5]:
            insight_text = gi.get("insight", "")
            times = gi.get("times_validated", 0)
            confidence = gi.get("confidence", 0)
            evidence = gi.get("evidence", {})
            delta = evidence.get("delta", 0)

            conf_color = "#64ffda" if confidence >= 0.8 else "#fca311" if confidence >= 0.5 else "#e63946"

            st.markdown(f"""
            <div style="background: #1a1a2e; padding: 8px 12px; border-radius: 6px; margin-bottom: 6px;
                        font-size: 0.85em;">
                <span style="color: #ccd6f6;">{insight_text[:80]}{'...' if len(insight_text) > 80 else ''}</span>
                <br/>
                <span style="color: #666;">Validated: <strong style="color: {conf_color};">{times}x</strong></span>
                {f'<span style="color: #666; margin-left: 10px;">WR impact: <strong style="color: #64ffda;">+{delta*100:.1f}%</strong></span>' if delta else ''}
            </div>
            """, unsafe_allow_html=True)

st.divider()

# --- Champion Progression (Full Width) ---
st.markdown("### Champion Progression")

# Hardcoded champion history (from EVOLUTION_LOG.md) + any new from data
champions = [
    {"generation": 52, "agent_id": "14feebbc", "win_rate": 0.627, "strategy": "breeding", "trades": 0},
    {"generation": 120, "agent_id": "30763000", "win_rate": 0.640, "strategy": "breeding", "trades": 0},
    {"generation": 197, "agent_id": "e91f9934", "win_rate": 0.667, "strategy": "breeding", "trades": 0},
    {"generation": 238, "agent_id": "b3b3bb5e", "win_rate": 0.674, "strategy": "breeding", "trades": 92},
    {"generation": 405, "agent_id": "04556dd7", "win_rate": 0.689, "strategy": "tweaking", "trades": 135},
    {"generation": 1271, "agent_id": "1391a4f1", "win_rate": 0.722, "strategy": "breeding", "trades": 0},
    {"generation": 1366, "agent_id": "fc7ea9fa", "win_rate": 0.728, "strategy": "breeding", "trades": 81},
    {"generation": 1381, "agent_id": "8e326766", "win_rate": 0.735, "strategy": "breeding", "trades": 34},
]

import pandas as pd

# Add current gen to show plateau
champions_with_now = champions + [
    {"generation": current_gen, "agent_id": "current", "win_rate": best_wr, "strategy": "plateau", "trades": 0}
]

df_champ = pd.DataFrame(champions_with_now)
if len(df_champ) > 0:
    c1, c2 = st.columns([3, 2])
    with c1:
        st.line_chart(df_champ.set_index("generation")["win_rate"], use_container_width=True)
    with c2:
        st.markdown("**Champion Timeline**")
        for ch in reversed(champions):
            wr_pct = ch["win_rate"] * 100
            st.markdown(f"""
            <div style="padding: 4px 0; border-bottom: 1px solid #1a1a2e; font-size: 0.85em;">
                <span style="color: #888;">Gen {ch['generation']}</span>
                <span style="color: #64ffda; font-weight: bold; margin-left: 10px;">{wr_pct:.1f}%</span>
                <span style="color: #666; margin-left: 10px;">{ch['agent_id'][:8]}</span>
                <span style="color: #444; margin-left: 10px;">via {ch['strategy']}</span>
            </div>
            """, unsafe_allow_html=True)

# --- Footer ---
st.divider()
footer_left, footer_right = st.columns([3, 1])
with footer_left:
    st.markdown("""
    <div style="color: #444; font-size: 0.8em;">
        <strong>DGM-H</strong> (Darwin Godel Machine - Hyperagents) |
        Self-improving trading strategy discovery |
        Powered by evolutionary search + LLM-generated guards |
        Built with <a href="https://github.com/anthropics/claude-code" style="color: #7c3aed;">Claude Code</a>
    </div>
    """, unsafe_allow_html=True)
with footer_right:
    st.markdown(f"""
    <div style="color: #444; font-size: 0.8em; text-align: right;">
        Last refresh: {datetime.now().strftime("%H:%M:%S")}
    </div>
    """, unsafe_allow_html=True)

# --- Auto-refresh ---
time.sleep(REFRESH_INTERVAL)
st.rerun()
