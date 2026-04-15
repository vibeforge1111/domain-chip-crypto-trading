"""Self-Referential Modification — the meta-agent rewrites its own strategies.

DGM-H Gap 4: The modification procedure itself is editable. The meta-agent
can read its own strategy code, analyze performance, and generate improved
versions — or entirely new strategies.

This is the "metacognitive self-modification" that distinguishes DGM-H from
standard evolutionary search. The system doesn't just find better solutions;
it finds better ways to find solutions.

Implementation:
  - Each meta-strategy is stored as a separate Python file in strategies/active/
  - The meta-agent reads its own code + performance stats
  - It decides whether to: fine-tune params, rewrite logic, or invent new strategies
  - All generated code runs in a sandboxed evaluator
  - Failed strategies are logged as dead ends and pruned
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)

EVOLUTION_ROOT = Path(__file__).resolve().parent.parent
ACTIVE_STRATEGIES_DIR = EVOLUTION_ROOT / "strategies" / "active"
ACTIVE_STRATEGIES_DIR.mkdir(parents=True, exist_ok=True)

STRATEGY_TEMPLATE = '''"""Auto-generated meta-strategy: {name}

Generated at generation {generation}.
"""


def generate(population, params, dead_ends):
    """Generate new mutation dicts using this strategy.

    Args:
        population: List of Agent objects (the current population)
        params: MetaStrategyParams (evolvable parameters)
        dead_ends: Set of known dead-end mutation patterns

    Returns:
        dict: A new mutation dict for evaluation
    """
    import copy
    import random

    # Select a parent agent
    if not population:
        return None

    parent = max(population, key=lambda a: a.win_rate)
    mutations = copy.deepcopy(parent.mutations)

    # YOUR STRATEGY LOGIC HERE

    return mutations
'''

SYSTEM_PROMPT = """You are a meta-strategy generator for an evolutionary trading system.
You write Python functions that generate new trading mutation dicts.

The system evolves trading strategies by generating mutation dicts like:
{
    "doctrine_id": "compression_mean_reversion",
    "strategy_id": "compression_range_bounce",
    "asset_universe": "BTC",
    "session_quality_filter": "skip_compression_toxic",
    "cr_wick_guard": "reject_high",
    "extend_regimes": "trend,event_driven,range"
}

Available mutation keys:
- doctrine_id: compression_mean_reversion, trend_regime_following, event_driven_fade, etc.
- strategy_id: compression_range_bounce, ema_pullback_long, event_fade, etc.
- asset_universe: BTC, ETH, SOL, BTC,ETH, BTC,SOL, BTC,ETH,SOL
- Guards: cr_wick_guard, cr_down_in_downtrend, drawdown_guard, volume_guard, cr_loose_setup
- extend_regimes: trend, event_driven, range, trend,event_driven,range, etc.

Rules:
1. The function must accept (population, params, dead_ends) and return a mutation dict
2. Use `import copy` and `import random` — no other imports
3. You can access agent.mutations, agent.win_rate, agent.wealth_factor, agent.fitness
4. Filter out dead_end patterns from the result
5. Be creative — try combining mutation patterns that haven't been tried
6. Return ONLY the Python function, no explanation
"""


class SelfReferentialEngine:
    """Enable the meta-agent to read and rewrite its own strategy code."""

    def __init__(
        self,
        archive_root: Path | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ):
        self.archive_root = archive_root or (EVOLUTION_ROOT / "archive")
        self.api_key = api_key or os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = base_url or os.environ.get("LLM_BASE_URL") or None
        self.model = model or os.environ.get("LLM_MODEL", "gpt-4o-mini")
        self._strategy_log_path = self.archive_root / "strategy_evolution_log.jsonl"
        self._last_call_time = 0.0

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    # ── Strategy Introspection ────────────────────────────────

    def read_current_strategies(self) -> dict[str, str]:
        """Read all active strategy source code for self-inspection."""
        strategies = {}

        # Read built-in strategies from meta_agent.py
        meta_agent_path = Path(__file__).parent / "meta_agent.py"
        if meta_agent_path.exists():
            strategies["meta_agent.py"] = meta_agent_path.read_text(encoding="utf-8")

        # Read any active custom strategies
        for py_file in ACTIVE_STRATEGIES_DIR.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            strategies[py_file.name] = py_file.read_text(encoding="utf-8")

        return strategies

    def analyze_strategy_performance(
        self,
        effectiveness: dict[str, dict],
    ) -> dict[str, str]:
        """Categorize strategies by their performance for self-modification.

        Returns dict mapping strategy name to recommended action:
        - "keep": performing well, don't change
        - "refine": moderate performance, try small improvements
        - "rewrite": poor performance, needs new logic
        - "replace": consistently failing, generate replacement
        """
        actions = {}
        for name, stats in effectiveness.items():
            attempts = stats.get("attempts", 0)
            rate = stats.get("improvement_rate", 0)

            if attempts < 5:
                actions[name] = "keep"  # Not enough data
            elif rate >= 0.5:
                actions[name] = "keep"
            elif rate >= 0.2:
                actions[name] = "refine"
            elif rate >= 0.05:
                actions[name] = "rewrite"
            else:
                actions[name] = "replace"

        return actions

    # ── Strategy Generation ───────────────────────────────────

    def generate_new_strategy(
        self,
        effectiveness: dict[str, dict],
        insights: list[dict] | None = None,
        generation: int = 0,
    ) -> dict[str, Any] | None:
        """Use LLM to generate a new meta-strategy.

        The LLM sees:
        1. Current strategy performance stats
        2. Insights from the performance analyzer
        3. Which strategies need replacement

        Returns metadata dict with strategy_id, code, file_path.
        """
        if not self.available:
            return None

        prompt = self._build_strategy_prompt(effectiveness, insights)
        code = self._call_llm(prompt)
        if not code:
            return None

        if not self._validate_strategy(code):
            logger.warning("Generated strategy failed validation")
            return None

        strategy_id = f"evolved_gen{generation}_{hashlib.md5(code.encode()).hexdigest()[:6]}"
        file_path = ACTIVE_STRATEGIES_DIR / f"{strategy_id}.py"
        file_path.write_text(code, encoding="utf-8")

        meta = {
            "strategy_id": strategy_id,
            "generation": generation,
            "model": self.model,
            "code": code,
            "file_path": str(file_path),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Log the strategy evolution event
        with open(self._strategy_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(meta) + "\n")

        logger.info("Generated new strategy: %s", strategy_id)
        return meta

    def _build_strategy_prompt(
        self,
        effectiveness: dict[str, dict],
        insights: list[dict] | None,
    ) -> str:
        parts = [
            "Generate a new meta-strategy function for an evolutionary trading system.",
            "\nCurrent strategy performance:",
        ]

        for name, stats in sorted(
            effectiveness.items(),
            key=lambda x: x[1].get("improvement_rate", 0),
        ):
            parts.append(
                f"  - {name}: {stats.get('improvement_rate', 0):.0%} improvement "
                f"({stats.get('attempts', 0)} attempts, avg WR={stats.get('avg_wr', 0):.3f})"
            )

        if insights:
            parts.append("\nDiscovered insights:")
            for ins in insights[:5]:
                parts.append(f"  - {ins['insight']}")

        parts.append(
            "\nGenerate a strategy that combines the best patterns from high-performing "
            "strategies while avoiding the patterns of failing ones. "
            "The function signature must be: def generate(population, params, dead_ends) -> dict"
            "\nReturn ONLY the Python function."
        )

        return "\n".join(parts)

    def _call_llm(self, prompt: str) -> str | None:
        """Call LLM API for strategy generation."""
        elapsed = time.time() - self._last_call_time
        if elapsed < 3.0:
            time.sleep(3.0 - elapsed)

        try:
            import openai

            client_kwargs = {"api_key": self.api_key}
            if self.base_url:
                client_kwargs["base_url"] = self.base_url
            client = openai.OpenAI(**client_kwargs)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.9,
                max_tokens=2000,
            )
            self._last_call_time = time.time()

            code = response.choices[0].message.content.strip()

            # Strip reasoning/think tags (MiniMax, DeepSeek, etc.)
            import re
            code = re.sub(r"<think>.*?</think>", "", code, flags=re.DOTALL).strip()

            if code.startswith("```python"):
                code = code[len("```python"):].strip()
            if code.startswith("```"):
                code = code[3:].strip()
            if code.endswith("```"):
                code = code[:-3].strip()

            return code

        except ImportError:
            logger.warning("openai package not installed")
            return None
        except Exception as e:
            logger.error("LLM strategy generation failed: %s", e)
            return None

    def _validate_strategy(self, code: str) -> bool:
        """Validate a generated strategy is safe and functional."""
        if "def generate(" not in code:
            return False

        forbidden = [
            "import os", "import sys", "import subprocess",
            "open(", "exec(", "eval(", "__import__",
            "os.system", "requests.", "urllib.", "socket.",
        ]
        for f in forbidden:
            if f in code:
                logger.warning("Strategy contains forbidden pattern: %s", f)
                return False

        try:
            compile(code, "<strategy>", "exec")
        except SyntaxError as e:
            logger.warning("Strategy syntax error: %s", e)
            return False

        return True

    # ── Strategy Loading ──────────────────────────────────────

    def load_strategy(self, strategy_id: str) -> Callable | None:
        """Dynamically load a generated strategy function."""
        file_path = ACTIVE_STRATEGIES_DIR / f"{strategy_id}.py"
        if not file_path.exists():
            return None

        try:
            spec = importlib.util.spec_from_file_location(strategy_id, file_path)
            if spec is None or spec.loader is None:
                return None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return getattr(module, "generate", None)
        except Exception as e:
            logger.error("Failed to load strategy %s: %s", strategy_id, e)
            return None

    def list_active_strategies(self) -> list[str]:
        """List all active custom strategy IDs."""
        return [
            p.stem for p in ACTIVE_STRATEGIES_DIR.glob("*.py")
            if not p.name.startswith("__")
        ]

    def prune_strategy(self, strategy_id: str) -> bool:
        """Remove a failed strategy."""
        file_path = ACTIVE_STRATEGIES_DIR / f"{strategy_id}.py"
        if file_path.exists():
            file_path.unlink()
            logger.info("Pruned strategy: %s", strategy_id)
            return True
        return False
