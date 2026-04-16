"""Premium Pack Manager — encrypted asset packs for Pro tier subscribers.

Pack types:
  - doctrine:    Battle-tested doctrine cards + packets
  - agents:      Live-ready agents with walk-forward validation
  - guards:      LLM-generated guard modules + effectiveness index
  - insights:    Synthesized insights, dead-end blacklist, strategy effectiveness
  - calibration: Gate calibration, bias analysis, meta-agent state

Usage:
    crypto-autoloop pack install pro-agents-v1.cpak --key <fernet-key>
    crypto-autoloop pack list
    crypto-autoloop pack verify
    crypto-autoloop pack remove pro-agents-v1
    crypto-autoloop pack status
"""

from __future__ import annotations

import ast
import hashlib
import io
import json
import shutil
import zipfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKS_DIR = REPO_ROOT / "packs"
REGISTRY_PATH = PACKS_DIR / "registry.json"

NAMESPACE_PREFIX = "pro__"

VALID_PACK_TYPES = {"doctrine", "agents", "guards", "insights", "calibration"}

# Forbidden patterns in guard .py files (security)
GUARD_FORBIDDEN = [
    "import os", "import sys", "import subprocess",
    "open(", "exec(", "eval(", "__import__",
    "os.system", "os.popen", "shutil.",
    "requests.", "urllib.", "socket.",
]


@dataclass
class PackManifest:
    """Metadata for an installed premium pack."""

    pack_id: str
    pack_name: str
    pack_type: str
    version: str
    asset_count: int
    source_generation: int = 0
    merge_strategy: str = "namespace"
    namespace_prefix: str = NAMESPACE_PREFIX
    description: str = ""
    created_at: str = ""
    installed_at: str = ""
    files: list[dict] = field(default_factory=list)
    merged_paths: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> PackManifest:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class PackManager:
    """Manages premium pack installation, verification, and removal."""

    def __init__(self, repo_root: Path | None = None):
        self.repo_root = repo_root or REPO_ROOT
        self.packs_dir = self.repo_root / "packs"
        self.packs_dir.mkdir(parents=True, exist_ok=True)
        self.registry_path = self.packs_dir / "registry.json"

    # ── Registry ──────────────────────────────────────────────

    def _load_registry(self) -> dict[str, dict]:
        if self.registry_path.exists():
            return json.loads(self.registry_path.read_text(encoding="utf-8"))
        return {}

    def _save_registry(self, registry: dict[str, dict]) -> None:
        self.registry_path.write_text(
            json.dumps(registry, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    # ── Install ───────────────────────────────────────────────

    def install(self, cpak_path: Path, key: str) -> PackManifest:
        """Decrypt a .cpak archive, validate checksums, and merge assets.

        Args:
            cpak_path: Path to the encrypted .cpak file.
            key: Fernet key (base64-encoded) for decryption.

        Returns:
            PackManifest of the installed pack.

        Raises:
            ValueError: Invalid pack, checksum mismatch, or security issue.
            RuntimeError: Decryption failure.
        """
        from cryptography.fernet import Fernet, InvalidToken

        cpak_path = Path(cpak_path)
        if not cpak_path.exists():
            raise FileNotFoundError(f"Pack file not found: {cpak_path}")

        # Decrypt
        try:
            fernet = Fernet(key.encode() if isinstance(key, str) else key)
        except Exception as exc:
            raise ValueError(f"Invalid license key format: {exc}") from exc

        encrypted_data = cpak_path.read_bytes()
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
        except InvalidToken:
            raise RuntimeError("Decryption failed — invalid license key or corrupted pack file.")

        # Unzip in memory
        zip_buf = io.BytesIO(decrypted_data)
        if not zipfile.is_zipfile(zip_buf):
            raise ValueError("Decrypted data is not a valid ZIP archive.")
        zip_buf.seek(0)

        with zipfile.ZipFile(zip_buf, "r") as zf:
            # Read manifest
            if "manifest.json" not in zf.namelist():
                raise ValueError("Pack missing manifest.json")
            manifest_data = json.loads(zf.read("manifest.json"))
            manifest = PackManifest.from_dict(manifest_data)

            if manifest.pack_type not in VALID_PACK_TYPES:
                raise ValueError(f"Unknown pack type: {manifest.pack_type}")

            # Check if already installed — remove old version first
            registry = self._load_registry()
            if manifest.pack_id in registry:
                self._remove_merged_files(registry[manifest.pack_id])

            # Validate checksums
            if "checksums.json" in zf.namelist():
                checksums = json.loads(zf.read("checksums.json"))
                self._validate_checksums(zf, checksums)

            # Security check for guard packs
            if manifest.pack_type == "guards":
                self._security_check_guards(zf)

            # Extract pack to packs/<pack-id>/
            pack_dir = self.packs_dir / manifest.pack_id
            if pack_dir.exists():
                shutil.rmtree(pack_dir)
            pack_dir.mkdir(parents=True)

            for name in zf.namelist():
                target = pack_dir / name
                target.parent.mkdir(parents=True, exist_ok=True)
                if not name.endswith("/"):
                    target.write_bytes(zf.read(name))

        # Merge into system directories
        merged_paths = self._merge(manifest, pack_dir)
        manifest.merged_paths = [str(p) for p in merged_paths]
        manifest.installed_at = datetime.now(timezone.utc).isoformat()

        # Update registry
        registry[manifest.pack_id] = manifest.to_dict()
        self._save_registry(registry)

        return manifest

    def _validate_checksums(self, zf: zipfile.ZipFile, checksums: dict[str, str]) -> None:
        for filepath, expected_hash in checksums.items():
            if filepath not in zf.namelist():
                raise ValueError(f"Checksum references missing file: {filepath}")
            actual = hashlib.sha256(zf.read(filepath)).hexdigest()
            if actual != expected_hash:
                raise ValueError(
                    f"Checksum mismatch for {filepath}: expected {expected_hash[:12]}..., got {actual[:12]}..."
                )

    def _security_check_guards(self, zf: zipfile.ZipFile) -> None:
        for name in zf.namelist():
            if name.endswith(".py"):
                code = zf.read(name).decode("utf-8", errors="replace")
                for forbidden in GUARD_FORBIDDEN:
                    if forbidden in code:
                        raise ValueError(
                            f"Security: guard {name} contains forbidden pattern '{forbidden}'"
                        )
                # AST parse check
                try:
                    ast.parse(code)
                except SyntaxError as exc:
                    raise ValueError(f"Guard {name} has invalid Python syntax: {exc}") from exc

    # ── Merge Logic ───────────────────────────────────────────

    def _merge(self, manifest: PackManifest, pack_dir: Path) -> list[Path]:
        """Merge pack contents into the system's working directories."""
        merge_map = {
            "doctrine": self._merge_doctrine,
            "agents": self._merge_agents,
            "guards": self._merge_guards,
            "insights": self._merge_insights,
            "calibration": self._merge_calibration,
        }
        handler = merge_map.get(manifest.pack_type)
        if handler is None:
            return []
        return handler(pack_dir)

    def _merge_doctrine(self, pack_dir: Path) -> list[Path]:
        merged = []
        cards_src = pack_dir / "doctrine-cards"
        packets_src = pack_dir / "doctrine-packets"
        cards_dst = self.repo_root / "docs" / "doctrine-cards"
        packets_dst = self.repo_root / "docs" / "doctrine-packets"
        cards_dst.mkdir(parents=True, exist_ok=True)
        packets_dst.mkdir(parents=True, exist_ok=True)

        if cards_src.exists():
            for src in cards_src.glob("*.json"):
                card = json.loads(src.read_text(encoding="utf-8"))
                card["card_id"] = f"{NAMESPACE_PREFIX}{card.get('card_id', src.stem)}"
                card["_source"] = "premium_pack"
                dest = cards_dst / f"{NAMESPACE_PREFIX}{src.name}"
                dest.write_text(json.dumps(card, indent=2), encoding="utf-8")
                merged.append(dest)

        if packets_src.exists():
            for src in packets_src.glob("*.json"):
                packet = json.loads(src.read_text(encoding="utf-8"))
                pid = packet.get("packet_id", packet.get("source_packet_id", src.stem))
                packet["packet_id"] = f"{NAMESPACE_PREFIX}{pid}"
                packet["_source"] = "premium_pack"
                dest = packets_dst / f"{NAMESPACE_PREFIX}{src.name}"
                dest.write_text(json.dumps(packet, indent=2), encoding="utf-8")
                merged.append(dest)

        return merged

    def _merge_agents(self, pack_dir: Path) -> list[Path]:
        merged = []
        gen_dst = self.repo_root / "live" / "archive" / "generations"
        gen_dst.mkdir(parents=True, exist_ok=True)

        # Look for any generation files or live_ready_agents.json in pack
        agents_file = pack_dir / "live_ready_agents.json"
        if agents_file.exists():
            agents_data = json.loads(agents_file.read_text(encoding="utf-8"))
            # Wrap in generation format with _source tag
            if isinstance(agents_data, list):
                agent_list = agents_data
            else:
                agent_list = agents_data.get("agents", [agents_data])

            for agent in agent_list:
                agent["_source"] = "premium"

            gen_wrapper = {
                "generation": 99999,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "population_size": len(agent_list),
                "elite_count": sum(
                    1 for a in agent_list
                    if a.get("fitness", {}).get("elite", False)
                ),
                "viable_count": sum(
                    1 for a in agent_list
                    if a.get("fitness", {}).get("viable", False)
                ),
                "best_wr": max(
                    (a.get("fitness", {}).get("win_rate", 0) for a in agent_list),
                    default=0,
                ),
                "agents": agent_list,
                "_source": "premium_pack",
            }
            dest = gen_dst / f"{NAMESPACE_PREFIX}gen_premium.json"
            dest.write_text(json.dumps(gen_wrapper, indent=2), encoding="utf-8")
            merged.append(dest)

        # Also copy any gen_*.json files from pack
        for src in pack_dir.glob("generations/gen_*.json"):
            dest = gen_dst / f"{NAMESPACE_PREFIX}{src.name}"
            data = json.loads(src.read_text(encoding="utf-8"))
            data["_source"] = "premium_pack"
            for agent in data.get("agents", []):
                agent["_source"] = "premium"
            dest.write_text(json.dumps(data, indent=2), encoding="utf-8")
            merged.append(dest)

        return merged

    def _merge_guards(self, pack_dir: Path) -> list[Path]:
        merged = []
        guards_src = pack_dir / "guards"
        guards_dst = self.repo_root / "live" / "generated_guards"
        guards_dst.mkdir(parents=True, exist_ok=True)

        if not guards_src.exists():
            return merged

        for src in guards_src.iterdir():
            dest = guards_dst / f"{NAMESPACE_PREFIX}{src.name}"
            shutil.copy2(src, dest)
            merged.append(dest)

        # Copy effectiveness index if present
        eff_src = pack_dir / "guard_effectiveness.json"
        if eff_src.exists():
            dest = guards_dst / f"{NAMESPACE_PREFIX}effectiveness_index.json"
            shutil.copy2(eff_src, dest)
            merged.append(dest)

        return merged

    def _merge_insights(self, pack_dir: Path) -> list[Path]:
        # Insights stay in packs/ dir — dashboard reads directly
        return [pack_dir / f for f in pack_dir.iterdir() if f.suffix == ".json"]

    def _merge_calibration(self, pack_dir: Path) -> list[Path]:
        # Calibration stays in packs/ dir — optional overlay
        return [pack_dir / f for f in pack_dir.iterdir() if f.suffix == ".json"]

    # ── Remove ────────────────────────────────────────────────

    def remove(self, pack_id: str) -> bool:
        """Uninstall a pack and clean up merged files."""
        registry = self._load_registry()
        if pack_id not in registry:
            return False

        self._remove_merged_files(registry[pack_id])

        # Remove pack directory
        pack_dir = self.packs_dir / pack_id
        if pack_dir.exists():
            shutil.rmtree(pack_dir)

        del registry[pack_id]
        self._save_registry(registry)
        return True

    def _remove_merged_files(self, pack_data: dict) -> None:
        for path_str in pack_data.get("merged_paths", []):
            p = Path(path_str)
            if p.exists() and NAMESPACE_PREFIX in p.name:
                p.unlink(missing_ok=True)

    # ── List / Verify / Status ────────────────────────────────

    def list_installed(self) -> list[PackManifest]:
        registry = self._load_registry()
        return [PackManifest.from_dict(v) for v in registry.values()]

    def verify(self, pack_id: str | None = None) -> dict[str, dict[str, Any]]:
        """Verify checksums of installed pack(s)."""
        registry = self._load_registry()
        ids = [pack_id] if pack_id else list(registry.keys())
        results: dict[str, dict[str, Any]] = {}

        for pid in ids:
            if pid not in registry:
                results[pid] = {"status": "not_found"}
                continue

            pack_dir = self.packs_dir / pid
            checksums_path = pack_dir / "checksums.json"
            if not checksums_path.exists():
                results[pid] = {"status": "no_checksums"}
                continue

            checksums = json.loads(checksums_path.read_text(encoding="utf-8"))
            failures = []
            for filepath, expected in checksums.items():
                full_path = pack_dir / filepath
                if not full_path.exists():
                    failures.append({"file": filepath, "error": "missing"})
                    continue
                actual = hashlib.sha256(full_path.read_bytes()).hexdigest()
                if actual != expected:
                    failures.append({"file": filepath, "error": "mismatch"})

            results[pid] = {
                "status": "ok" if not failures else "failed",
                "files_checked": len(checksums),
                "failures": failures,
            }

        return results

    def status(self) -> dict[str, Any]:
        """Return free vs pro asset counts by category."""
        registry = self._load_registry()
        installed = list(registry.values())

        # Count user assets
        user_cards = len(list(
            (self.repo_root / "docs" / "doctrine-cards").glob("*.json")
        )) if (self.repo_root / "docs" / "doctrine-cards").exists() else 0
        pro_cards = len(list(
            (self.repo_root / "docs" / "doctrine-cards").glob(f"{NAMESPACE_PREFIX}*.json")
        )) if (self.repo_root / "docs" / "doctrine-cards").exists() else 0

        gen_dir = self.repo_root / "live" / "archive" / "generations"
        user_gens = len(list(gen_dir.glob("gen_*.json"))) if gen_dir.exists() else 0
        pro_gens = len(list(gen_dir.glob(f"{NAMESPACE_PREFIX}gen_*.json"))) if gen_dir.exists() else 0

        guards_dir = self.repo_root / "live" / "generated_guards"
        user_guards = len(list(guards_dir.glob("guard_*.py"))) if guards_dir.exists() else 0
        pro_guards = len(list(guards_dir.glob(f"{NAMESPACE_PREFIX}guard_*.py"))) if guards_dir.exists() else 0

        return {
            "packs_installed": len(installed),
            "packs": [
                {"id": p["pack_id"], "type": p["pack_type"], "version": p["version"],
                 "assets": p.get("asset_count", 0)}
                for p in installed
            ],
            "assets": {
                "doctrine_cards": {"user": user_cards - pro_cards, "pro": pro_cards},
                "generations": {"user": user_gens, "pro": pro_gens},
                "guards": {"user": user_guards, "pro": pro_guards},
                "insights": any(p["pack_type"] == "insights" for p in installed),
                "calibration": any(p["pack_type"] == "calibration" for p in installed),
            },
        }
