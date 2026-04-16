# PRO System — Premium Intelligence Packs

## What Is This?

The domain chip has two tiers:

| Tier | What You Get | How Intelligence Arrives |
|------|-------------|------------------------|
| **Free** | Full engine: tri-loop autoloop, backtester, live paper trader, dashboard, researcher | Discovers everything from zero. Your system learns by running cycles. |
| **Pro** | Engine + pre-trained intelligence packs (`.cpak` files) | Inject 2,478 generations of proven evolution intelligence. Skip months of discovery. |

**Free users get the complete engine.** Every feature works. The autoloop discovers doctrine, backtests candidates, promotes to paper trading, and evolves — all from scratch.

**Pro users get a head start.** Premium packs contain battle-tested agents (72.8% peak WR), 2,587 proven guard modules, 11,000+ synthesized insights, regime calibration data, and a dead-end blacklist that tells the autoloop which strategies to stop wasting time on.

The engine is identical. Pro packs are compressed search time.

---

## What's In Each Pack?

### 1. Agents Pack (`pro-agents-v1.cpak`)
- **99 live-ready agents** extracted from 9,200+ tested agents across 2,478 evolution generations
- Each agent has proven fitness: win rate, wealth factor, trade count, regime tags
- Top agent: 72.8% WR on walk-forward validated backtest data
- Agents merge into the live paper trader automatically — they begin trading alongside any agents the free engine discovers

### 2. Guards Pack (`pro-guards-v1.cpak`)
- **2,587 guard modules** — Python functions that filter bad trades
- Each guard has an effectiveness ranking (e.g., `volume_guard` adds +6.2% WR delta)
- Guards are the #1 driver of win rate in the evolution system
- The autoloop's LLM code generator can reference these guards when building new strategies

### 3. Insights Pack (`pro-insights-v1.cpak`)
- **11,167 synthesized insights** from the evolution system's meta-improvement engine
- Includes: regime-specific patterns, guard effectiveness rankings, strategy family analysis
- **Dead-end blacklist**: Strategies with <5% improvement rate across hundreds of tests — tells the autoloop "don't bother with these"
- **Strategy effectiveness index**: Which strategy families actually produce elite agents, and which are noise

### 4. Calibration Pack (`pro-calibration-v1.cpak`)
- **Gate calibration data**: Optimal thresholds for walk-forward validation, trade count minimums
- **Bias analysis**: Known systematic biases in the backtester (e.g., regime over-representation)
- **Meta-agent state**: The evolution engine's accumulated learning about what mutations work

### 5. Doctrine Pack (`pro-doctrine-v1.cpak`)
- **Battle-tested doctrine cards** validated 3+ times across evolution cycles
- Each card has mechanism descriptions, priority rankings, failure modes
- Cards merge with the `pro__` prefix — never overwrite user-discovered doctrine

---

## How Installation Works

### For Subscribers

You receive a `.cpak` file and a license key. That's it.

```bash
# Install a pack
crypto-autoloop pack install pro-agents-v1.cpak --key YOUR_LICENSE_KEY

# See what's installed
crypto-autoloop pack list

# Verify checksums (integrity check)
crypto-autoloop pack verify

# See free vs pro asset counts
crypto-autoloop pack status

# Uninstall a pack
crypto-autoloop pack remove pro-agents-v1
```

### What Happens During Install

1. The `.cpak` file is decrypted using your license key (Fernet symmetric encryption)
2. A ZIP archive is extracted containing the manifest, checksums, and asset files
3. SHA-256 checksums are verified for every file (tamper detection)
4. Guard `.py` files are scanned for dangerous patterns (`import os`, `subprocess`, `eval`, `exec`) — blocked if found
5. Assets are merged into the live system with a `pro__` namespace prefix:
   - Agents → `live/archive/generations/pro__gen_premium.json`
   - Guards → `live/generated_guards/pro__guard_*.py`
   - Insights → `packs/pro-insights-v1/` (read by dashboard)
   - Calibration → `packs/pro-calibration-v1/` (optional overlay)
6. A registry entry is written to `packs/registry.json`

### Non-Destructive Merge

Premium assets **never overwrite** user-discovered content:

- User doctrine cards: `docs/doctrine-cards/card_*.yaml`
- Pro doctrine cards: `docs/doctrine-cards/pro__card_*.yaml`
- User guards: `live/generated_guards/guard_*.py`
- Pro guards: `live/generated_guards/pro__guard_*.py`
- User agents: `live/archive/generations/gen_*.json`
- Pro agents: `live/archive/generations/pro__gen_premium.json`

If you uninstall a pack, only `pro__` files are removed. Your own work is untouched.

---

## How Premium Content Integrates at Runtime

### Agent Loading
The `PopulationArchive.load_latest()` method scans both standard (`gen_*.json`) and premium (`pro__gen_*.json`) files. Premium agents are tagged with `_source: "premium"` so the dashboard can distinguish them.

### Guard Loading
The `load_guard()` function first looks for `guard_{id}.py`, then falls back to `pro__guard_{id}.py`. Premium guards work identically to user-generated guards.

### Dashboard
- **PRO badge**: Shows number of installed packs in the top stats bar
- **Source column**: Agent and guard tables show whether each item is "user" or "pro"
- **Insights panel**: Displays guard effectiveness rankings and dead-end blacklist from the insights pack
- **API endpoints**: `/api/pack-status` and `/api/premium-insights` serve pack data

### Autoloop Integration
The autoloop continues discovering on its own. Pro packs give it a better starting population (agents), better guard library (guards), and knowledge of what NOT to try (dead-end blacklist). The autoloop can still discover novel strategies that outperform the pro pack contents.

---

## Key Distribution Model

### Architecture

```
Publisher (you)                    Subscriber
─────────────────                  ─────────────────
Evolution system                   Domain chip (free engine)
  │                                  │
  ├─ export_premium_pack.py          │
  │  (reads evolution data,          │
  │   builds ZIP, encrypts           │
  │   with Fernet key)               │
  │                                  │
  ▼                                  │
.cpak file ──── delivery ────────►  .cpak file
                channel               │
                                      ├─ crypto-autoloop pack install
Fernet key ──── separate ────────►    │   --key LICENSE_KEY
                channel               │
                                      ▼
                                   Decrypted assets in live system
```

### How Keys Work

- **Encryption**: Fernet (AES-128-CBC + HMAC-SHA256) via Python's `cryptography` library
- **Key = License**: The Fernet key IS the license key. No server, no activation, no phone-home
- **Offline**: Everything works fully offline. No internet required after download
- **One key per pack version**: Each `.cpak` file is encrypted with one key. Different packs can use the same or different keys

### Key Generation

```bash
# Generate a new license key (publisher-side)
python scripts/export_premium_pack.py generate-key
# Output: kUOGqXVS7dn8rqxExo_fU-LT_WC15sypCHdQ3yxuCJw=
```

### Distribution Options

| Method | How | Pros | Cons |
|--------|-----|------|------|
| **Direct delivery** | Email .cpak + key separately | Simple, no infra | Manual, no revocation |
| **Download link + key email** | Host .cpak on S3/GCS, email key | Scalable download | Still manual key mgmt |
| **Gumroad / Paddle** | Sell .cpak as digital product, key in receipt | Payment + delivery handled | No key rotation |
| **License server** (future) | API validates key, returns download URL | Revocation, analytics, trials | Requires server infra |

**Current recommendation**: Start with **direct delivery** (email .cpak + key). Move to Gumroad when you have 10+ subscribers. Build a license server when you need revocation or trials.

### Key Rotation

To rotate keys (e.g., for a new version):
1. Generate a new Fernet key
2. Re-export packs with the new key
3. Distribute new `.cpak` files + new key to active subscribers
4. Old `.cpak` files remain usable with old keys (no revocation in current model)

### What Subscribers Cannot Do

- **Extract the export pipeline**: `export_premium_pack.py` is excluded from the public repo (`.gitignore`)
- **Reverse-engineer pack creation**: They get encrypted `.cpak` blobs. Without the source evolution system data, they can't recreate packs
- **Share meaningfully**: A leaked key + `.cpak` lets someone install the pack, but the pack's value depreciates as the free engine catches up over time. The real value is getting NEW packs with fresh evolution data

### What Subscribers CAN Do

- **Inspect installed assets**: After decryption, guard `.py` files and agent JSON are plaintext on disk. This is by design — they need to be readable for the engine to use them
- **Copy installed files**: Yes. This is the DRM tradeoff. The encryption protects distribution, not post-install copying. Acceptable for a subscription model where value comes from ongoing updates

---

## Security Audit Checklist

### What's Protected

| Item | Status | How |
|------|--------|-----|
| `.cpak` files | Not tracked in git | `.gitignore`: `*.cpak` |
| Decrypted pack contents (`packs/*/`) | Not tracked in git | `.gitignore`: `packs/*/`, `packs/registry.json` |
| Merged `pro__*` files | Not tracked in git | `.gitignore`: `live/generated_guards/pro__*`, `live/archive/generations/pro__*` |
| Export pipeline | Not tracked in git | `.gitignore`: `scripts/export_premium_pack.py` |
| Fernet keys | Never in source code | Passed via `--key` CLI arg only |
| Guard code injection | Blocked at install | AST parse + pattern scan for `import os`, `subprocess`, `eval`, `exec` |

### What's Public (Intentionally)

| Item | Why |
|------|-----|
| `pack_manager.py` | Subscribers need the install/verify/remove logic |
| `autoloop.py` pack subcommands | CLI interface for pack management |
| `population.py` pro__ loading | Engine must know how to load premium agents |
| `llm_code_gen.py` pro__ fallback | Engine must know how to find premium guards |
| `dashboard_app.py` premium indicators | Dashboard must render pro badge and insights |

The mechanism is public. The content is private. This is the standard model (like a media player being open-source while the content requires a subscription).

---

## File Locations

### Publisher-Side (Your Machine Only)

| File | Purpose |
|------|---------|
| `scripts/export_premium_pack.py` | Builds `.cpak` from evolution system |
| Generated `.cpak` files | Encrypted archives for distribution |
| Fernet keys | License keys for subscribers |

### Subscriber-Side (In the Public Repo)

| File | Purpose |
|------|---------|
| `src/.../pack_manager.py` | Pack install/verify/remove logic |
| `src/.../autoloop.py` | CLI `pack` subcommand group |
| `live/hyperagent/population.py` | Loads `pro__gen_*.json` agents |
| `live/hyperagent/llm_code_gen.py` | Loads `pro__guard_*.py` guards |
| `live/dashboard_app.py` | Renders pro badge + insights panel |

### Runtime (Created by `pack install`, Gitignored)

| Path | Contents |
|------|----------|
| `packs/*.cpak` | Encrypted pack archives |
| `packs/<pack-id>/` | Decrypted pack contents |
| `packs/registry.json` | Installed pack registry |
| `live/archive/generations/pro__gen_premium.json` | Premium agents |
| `live/generated_guards/pro__guard_*.py` | Premium guard modules |
| `live/generated_guards/pro__effectiveness_index.json` | Guard rankings |

---

## Export Pipeline (Publisher Reference)

```bash
# Generate a license key
python scripts/export_premium_pack.py generate-key

# Export individual packs
python scripts/export_premium_pack.py agents   --evo-root <path-to-evolution> --key <KEY> --output pro-agents-v1.cpak
python scripts/export_premium_pack.py guards   --evo-root <path-to-evolution> --key <KEY> --output pro-guards-v1.cpak
python scripts/export_premium_pack.py insights --evo-root <path-to-evolution> --key <KEY> --output pro-insights-v1.cpak
python scripts/export_premium_pack.py calibration --evo-root <path-to-evolution> --key <KEY> --output pro-calibration-v1.cpak

# Export all packs at once
python scripts/export_premium_pack.py all --evo-root <path-to-evolution> --key <KEY> --output-dir ./packs/
```

### Pack Versioning

Version packs by changing the output filename:
- `pro-agents-v1.cpak` → `pro-agents-v2.cpak`
- Each version is a standalone snapshot. Users install the latest, old versions still work.
- The `pack_id` in the manifest determines identity — installing `pro-agents-v2` replaces `pro-agents-v1` automatically.
