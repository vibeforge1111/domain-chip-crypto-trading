"""Export premium packs from the evolution system into encrypted .cpak files.

Usage:
    python scripts/export_premium_pack.py doctrine    --evo-root <path> --key <key> --output pro-doctrine-v1.cpak
    python scripts/export_premium_pack.py agents      --evo-root <path> --key <key> --output pro-agents-v1.cpak
    python scripts/export_premium_pack.py guards      --evo-root <path> --key <key> --output pro-guards-v1.cpak
    python scripts/export_premium_pack.py insights    --evo-root <path> --key <key> --output pro-insights-v1.cpak
    python scripts/export_premium_pack.py calibration --evo-root <path> --key <key> --output pro-calibration-v1.cpak
    python scripts/export_premium_pack.py all         --evo-root <path> --key <key> --output-dir ./packs/
    python scripts/export_premium_pack.py generate-key
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _build_zip(files: dict[str, bytes], manifest: dict, checksums: dict[str, str]) -> bytes:
    """Build a ZIP archive in memory from file dict + manifest + checksums."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest.json", json.dumps(manifest, indent=2))
        zf.writestr("checksums.json", json.dumps(checksums, indent=2))
        for path, data in files.items():
            zf.writestr(path, data)
    return buf.getvalue()


def _encrypt_zip(zip_data: bytes, key: str) -> bytes:
    from cryptography.fernet import Fernet
    fernet = Fernet(key.encode() if isinstance(key, str) else key)
    return fernet.encrypt(zip_data)


def _write_cpak(zip_data: bytes, key: str, output: Path) -> None:
    encrypted = _encrypt_zip(zip_data, key)
    output.write_bytes(encrypted)
    print(f"  Written: {output} ({len(encrypted):,} bytes)")


# ── Exporters ─────────────────────────────────────────────


def export_doctrine(evo_root: Path, key: str, output: Path) -> None:
    """Export doctrine cards + packets from evolution system."""
    print("Exporting doctrine pack...")
    files: dict[str, bytes] = {}
    checksums: dict[str, str] = {}

    # Cards
    cards_dir = evo_root / "docs" / "doctrine-cards"
    if not cards_dir.exists():
        # Try alternative location
        cards_dir = evo_root / "archive" / "doctrine_cards"

    card_count = 0
    if cards_dir.exists():
        for f in sorted(cards_dir.glob("*.json")):
            data = f.read_bytes()
            path = f"doctrine-cards/{f.name}"
            files[path] = data
            checksums[path] = _sha256(data)
            card_count += 1

    # Packets
    packets_dir = evo_root / "docs" / "doctrine-packets"
    if packets_dir.exists():
        for f in sorted(packets_dir.glob("*.json")):
            data = f.read_bytes()
            path = f"doctrine-packets/{f.name}"
            files[path] = data
            checksums[path] = _sha256(data)

    manifest = {
        "pack_id": "pro-doctrine-v1",
        "pack_name": "Pro Doctrine Pack",
        "pack_type": "doctrine",
        "version": "1.0.0",
        "asset_count": card_count,
        "source_generation": _latest_gen(evo_root),
        "merge_strategy": "namespace",
        "namespace_prefix": "pro__",
        "description": f"{card_count} battle-tested doctrine cards from evolutionary search",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    zip_data = _build_zip(files, manifest, checksums)
    _write_cpak(zip_data, key, output)
    print(f"  Doctrine cards: {card_count}")


def export_agents(evo_root: Path, key: str, output: Path) -> None:
    """Export live-ready agents from evolution archive."""
    print("Exporting agent pack...")
    files: dict[str, bytes] = {}
    checksums: dict[str, str] = {}

    # Primary source: live_ready_agents.json
    agents_file = evo_root / "archive" / "live_ready_agents.json"
    if not agents_file.exists():
        print(f"  Warning: {agents_file} not found, checking alternatives...")
        # Try paper_trade_results.json
        agents_file = evo_root / "archive" / "paper_trade_results.json"

    if not agents_file.exists():
        print("  Error: No agent data found in evolution archive.")
        return

    agents_data = json.loads(agents_file.read_text(encoding="utf-8"))
    if isinstance(agents_data, list):
        agent_list = agents_data
    else:
        agent_list = agents_data.get("agents", [agents_data])

    # Filter to live-ready only
    live_ready = [
        a for a in agent_list
        if a.get("status") == "live_ready"
        or a.get("fitness", {}).get("elite", False)
        or a.get("pt_score", 0) >= 0.85
    ]
    if not live_ready:
        # Fall back to top agents by pt_wr or win_rate
        live_ready = sorted(
            agent_list,
            key=lambda a: a.get("pt_wr", a.get("pt_wr_avg", a.get("fitness", {}).get("win_rate", 0))),
            reverse=True,
        )[:30]

    # Normalize agent format for consumption by current system
    normalized = []
    for agent in live_ready:
        # Handle both evolution formats (flat aid/mutations vs nested)
        norm = {
            "agent_id": agent.get("aid", agent.get("agent_id", "")),
            "mutations": agent.get("mutations", {}),
            "meta_strategy": agent.get("meta", agent.get("meta_strategy", "premium")),
            "parent_id": agent.get("parent_id"),
            "generation": agent.get("generation", 0),
            "fitness": agent.get("fitness", {}),
            "created_at": agent.get("created_at", ""),
            "children_count": agent.get("children_count", 0),
            "_source": "premium",
            "_pt_wr": agent.get("pt_wr", agent.get("pt_wr_avg", 0)),
            "_pt_trades": agent.get("pt_trades", agent.get("pt_trades_total", 0)),
            "_pt_score": agent.get("pt_score", 0),
            "_status": agent.get("status", ""),
        }
        # If fitness is empty but we have top-level metrics, populate it
        if not norm["fitness"] and agent.get("bt_wr"):
            norm["fitness"] = {
                "win_rate": agent.get("bt_wr", 0),
                "wealth_factor": 1.0,
                "viable": True,
                "elite": True,
            }
        normalized.append(norm)

    data = json.dumps(normalized, indent=2).encode("utf-8")
    files["live_ready_agents.json"] = data
    checksums["live_ready_agents.json"] = _sha256(data)

    # Also include referenced guard files
    guards_dir = evo_root / "generated_guards"
    if not guards_dir.exists():
        guards_dir = evo_root / "hyperagent" / "generated_guards"
    guard_ids_needed = set()
    for agent in normalized:
        gid = agent.get("mutations", {}).get("llm_guard_id", "")
        if gid:
            guard_ids_needed.add(gid)

    if guards_dir.exists():
        for gid in guard_ids_needed:
            for suffix in [".py", ".meta.json"]:
                gfile = guards_dir / f"guard_{gid}{suffix}"
                if gfile.exists():
                    gdata = gfile.read_bytes()
                    path = f"guards/guard_{gid}{suffix}"
                    files[path] = gdata
                    checksums[path] = _sha256(gdata)

    manifest = {
        "pack_id": "pro-agents-v1",
        "pack_name": "Pro Agent Pack",
        "pack_type": "agents",
        "version": "1.0.0",
        "asset_count": len(normalized),
        "source_generation": _latest_gen(evo_root),
        "merge_strategy": "namespace",
        "namespace_prefix": "pro__",
        "description": f"{len(normalized)} live-ready agents from evolutionary search",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    zip_data = _build_zip(files, manifest, checksums)
    _write_cpak(zip_data, key, output)
    print(f"  Live-ready agents: {len(normalized)}")
    print(f"  Guard files included: {len(guard_ids_needed)}")


def export_guards(evo_root: Path, key: str, output: Path) -> None:
    """Export top-performing guard modules + effectiveness index."""
    print("Exporting guard pack...")
    files: dict[str, bytes] = {}
    checksums: dict[str, str] = {}

    guards_dir = evo_root / "generated_guards"
    if not guards_dir.exists():
        guards_dir = evo_root / "hyperagent" / "generated_guards"
    if not guards_dir.exists():
        print("  Error: No guards directory found.")
        return

    guard_count = 0
    for f in sorted(guards_dir.iterdir()):
        if f.suffix in (".py", ".json"):
            data = f.read_bytes()
            path = f"guards/{f.name}"
            files[path] = data
            checksums[path] = _sha256(data)
            if f.suffix == ".py":
                guard_count += 1

    # Include effectiveness index if available
    eff_file = evo_root / "archive" / "meta_improvements" / "synthesized_insights.json"
    if eff_file.exists():
        # Extract guard-specific insights as effectiveness index
        insights = json.loads(eff_file.read_text(encoding="utf-8"))
        guard_insights = [
            i for i in insights
            if i.get("type") == "guard_effectiveness"
        ]
        if guard_insights:
            data = json.dumps(guard_insights, indent=2).encode("utf-8")
            files["guard_effectiveness.json"] = data
            checksums["guard_effectiveness.json"] = _sha256(data)

    manifest = {
        "pack_id": "pro-guards-v1",
        "pack_name": "Pro Guard Pack",
        "pack_type": "guards",
        "version": "1.0.0",
        "asset_count": guard_count,
        "source_generation": _latest_gen(evo_root),
        "merge_strategy": "namespace",
        "namespace_prefix": "pro__",
        "description": f"{guard_count} LLM-generated guard modules with effectiveness index",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    zip_data = _build_zip(files, manifest, checksums)
    _write_cpak(zip_data, key, output)
    print(f"  Guard modules: {guard_count}")


def export_insights(evo_root: Path, key: str, output: Path) -> None:
    """Export synthesized insights, dead-end blacklist, strategy effectiveness."""
    print("Exporting insights pack...")
    files: dict[str, bytes] = {}
    checksums: dict[str, str] = {}
    asset_count = 0

    meta_dir = evo_root / "archive" / "meta_improvements"

    # Synthesized insights
    insights_file = meta_dir / "synthesized_insights.json"
    if insights_file.exists():
        data = insights_file.read_bytes()
        files["synthesized_insights.json"] = data
        checksums["synthesized_insights.json"] = _sha256(data)
        asset_count += len(json.loads(data))

    # Strategy effectiveness
    strat_file = meta_dir / "strategy_effectiveness.json"
    if strat_file.exists():
        data = strat_file.read_bytes()
        files["strategy_effectiveness.json"] = data
        checksums["strategy_effectiveness.json"] = _sha256(data)
        asset_count += 1

    # Build dead-end blacklist from strategy effectiveness
    if strat_file.exists():
        strat_data = json.loads(strat_file.read_text(encoding="utf-8"))
        dead_ends = {}
        for name, stats in strat_data.items():
            rate = stats.get("improvement_rate", 1.0)
            if rate < 0.05 and stats.get("attempts", 0) >= 100:
                dead_ends[name] = {
                    "improvement_rate": rate,
                    "attempts": stats.get("attempts", 0),
                    "avg_wr": stats.get("avg_wr", 0),
                    "recommendation": "avoid",
                }
        if dead_ends:
            data = json.dumps(dead_ends, indent=2).encode("utf-8")
            files["dead_end_blacklist.json"] = data
            checksums["dead_end_blacklist.json"] = _sha256(data)
            asset_count += len(dead_ends)

    # Performance log summary (not full 900K lines — just key stats)
    perf_file = meta_dir / "performance_log.jsonl"
    if perf_file.exists():
        # Read last 1000 lines for summary stats
        lines = perf_file.read_text(encoding="utf-8").strip().split("\n")
        total = len(lines)
        summary = {
            "total_evaluations": total,
            "source": "performance_log.jsonl",
            "note": "Full log available in evolution system archive",
        }
        data = json.dumps(summary, indent=2).encode("utf-8")
        files["performance_summary.json"] = data
        checksums["performance_summary.json"] = _sha256(data)

    manifest = {
        "pack_id": "pro-insights-v1",
        "pack_name": "Pro Insights Pack",
        "pack_type": "insights",
        "version": "1.0.0",
        "asset_count": asset_count,
        "source_generation": _latest_gen(evo_root),
        "merge_strategy": "namespace",
        "namespace_prefix": "pro__",
        "description": "Synthesized insights, dead-end blacklist, and strategy effectiveness from evolutionary search",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    zip_data = _build_zip(files, manifest, checksums)
    _write_cpak(zip_data, key, output)
    print(f"  Insights + dead-ends: {asset_count}")


def export_calibration(evo_root: Path, key: str, output: Path) -> None:
    """Export gate calibration, bias analysis, meta-agent state."""
    print("Exporting calibration pack...")
    files: dict[str, bytes] = {}
    checksums: dict[str, str] = {}
    asset_count = 0

    diag_dir = evo_root / "archive" / "self_diagnosis"

    for name in ["gate_calibration.json", "bias_analysis.json"]:
        f = diag_dir / name
        if f.exists():
            data = f.read_bytes()
            files[name] = data
            checksums[name] = _sha256(data)
            asset_count += 1

    meta_state = evo_root / "archive" / "meta_agent_state.json"
    if meta_state.exists():
        data = meta_state.read_bytes()
        files["meta_agent_state.json"] = data
        checksums["meta_agent_state.json"] = _sha256(data)
        asset_count += 1

    manifest = {
        "pack_id": "pro-calibration-v1",
        "pack_name": "Pro Calibration Pack",
        "pack_type": "calibration",
        "version": "1.0.0",
        "asset_count": asset_count,
        "source_generation": _latest_gen(evo_root),
        "merge_strategy": "namespace",
        "namespace_prefix": "pro__",
        "description": "Gate calibration, bias analysis, and meta-agent hyperparameters from evolutionary search",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    zip_data = _build_zip(files, manifest, checksums)
    _write_cpak(zip_data, key, output)
    print(f"  Calibration files: {asset_count}")


# ── Helpers ───────────────────────────────────────────────


def _latest_gen(evo_root: Path) -> int:
    """Find the latest generation number in evolution archive."""
    gen_dir = evo_root / "archive" / "generations"
    if not gen_dir.exists():
        return 0
    gen_files = sorted(gen_dir.glob("gen_*.json"))
    if not gen_files:
        return 0
    try:
        return int(gen_files[-1].stem.split("_")[1])
    except (IndexError, ValueError):
        return 0


# ── CLI ───────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export premium packs from evolution system.",
    )
    parser.add_argument(
        "pack_type",
        choices=["doctrine", "agents", "guards", "insights", "calibration", "all", "generate-key"],
        help="Pack type to export, 'all' for everything, or 'generate-key' to create a new license key.",
    )
    parser.add_argument("--evo-root", type=Path, help="Path to the evolution system root.")
    parser.add_argument("--key", help="Fernet key for encryption.")
    parser.add_argument("--output", type=Path, help="Output .cpak file path.")
    parser.add_argument("--output-dir", type=Path, help="Output directory (for 'all' mode).")

    args = parser.parse_args()

    if args.pack_type == "generate-key":
        from cryptography.fernet import Fernet
        key = Fernet.generate_key().decode()
        print(f"License key: {key}")
        print("Store this securely. Share with subscribers for pack decryption.")
        return 0

    if not args.evo_root:
        parser.error("--evo-root is required for export.")
    if not args.key:
        parser.error("--key is required for export.")
    if not args.evo_root.exists():
        parser.error(f"Evolution root not found: {args.evo_root}")

    exporters = {
        "doctrine": export_doctrine,
        "agents": export_agents,
        "guards": export_guards,
        "insights": export_insights,
        "calibration": export_calibration,
    }

    if args.pack_type == "all":
        out_dir = args.output_dir or Path(".")
        out_dir.mkdir(parents=True, exist_ok=True)
        for ptype, exporter in exporters.items():
            out = out_dir / f"pro-{ptype}-v1.cpak"
            exporter(args.evo_root, args.key, out)
        print(f"\nAll packs exported to {out_dir}")
        return 0

    exporter = exporters[args.pack_type]
    output = args.output or Path(f"pro-{args.pack_type}-v1.cpak")
    exporter(args.evo_root, args.key, output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
