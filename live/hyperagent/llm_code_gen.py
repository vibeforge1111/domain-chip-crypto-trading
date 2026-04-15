"""LLM Code Generation — generate Python guard functions via LLM.

DGM-H Gap 1: Instead of just tweaking mutation dicts, the meta-agent can
generate entirely new guard logic as Python code. This is where the paper
saw its biggest wins — self-modifying code went from 14% to 34% solve rate.

Generated guards:
  - Live in generated_guards/ directory as Python files
  - Each exports a `guard(features, prediction) -> str` function
  - The evaluator dynamically loads and applies them during backtest
  - Guards that improve WR+WF survive; others are pruned

Cost control:
  - Uses staged evaluation to kill bad guards early
  - Caches LLM calls for identical prompts
  - Rate-limits to avoid excessive API costs
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)

EVOLUTION_ROOT = Path(__file__).resolve().parent.parent
GUARDS_DIR = EVOLUTION_ROOT / "generated_guards"
GUARDS_DIR.mkdir(parents=True, exist_ok=True)

# Feature keys available to guard functions (from backtest _feature_row)
AVAILABLE_FEATURES = [
    "upper_wick_ratio", "lower_wick_ratio", "body_ratio",
    "range_pct", "volume_ratio", "atr_ratio",
    "rsi_14", "ema_slope", "bb_width", "bb_position",
    "close_vs_open", "high_vs_close", "low_vs_close",
    "trend_strength", "volatility_regime", "momentum_score",
    # Expanded indicators
    "bb_pct_b", "vwap_deviation", "stoch_k", "stoch_d",
    "obv_slope", "macd_histogram", "rsi_2h",
]

# Guard template for LLM prompt
GUARD_TEMPLATE = '''def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like {feature_keys}
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    # YOUR LOGIC HERE
    return prediction
'''

SYSTEM_PROMPT = """You are a quantitative trading guard function generator.
You write Python guard functions that filter trading signals based on market features.

Rules:
1. Return "skip" to reject a trade, or return the original `prediction` to keep it
2. Only use features from the `features` dict — no external imports or side effects
3. Keep logic simple and interpretable (2-8 lines of logic)
4. Focus on filtering out BAD trades, not adding new signals
5. Use numeric thresholds based on the feature descriptions
6. Return ONLY the Python function, no explanation

Available features in the `features` dict:
- upper_wick_ratio: float (0-1) — how much of the candle is upper wick
- lower_wick_ratio: float (0-1) — how much of the candle is lower wick
- body_ratio: float (0-1) — how much of the candle is body
- range_pct: float — candle range as percentage of price
- volume_ratio: float — current volume / average volume
- atr_ratio: float — current ATR / average ATR
- rsi_14: float (0-100) — relative strength index
- ema_slope: float — slope of the EMA (positive=uptrend)
- bb_width: float — Bollinger Band width
- bb_position: float (0-1) — position within Bollinger Bands
- trend_strength: float — strength of the current trend
- volatility_regime: float — current volatility level
- momentum_score: float — momentum indicator score
- bb_pct_b: float (0-1) — position within Bollinger Bands (0=lower, 1=upper)
- vwap_deviation: float — distance from VWAP as fraction of price (negative=below)
- stoch_k: float (0-100) — Stochastic %K oscillator
- stoch_d: float (0-100) — Stochastic %D (smoothed %K)
- obv_slope: float — On-Balance Volume slope (positive=accumulation)
- macd_histogram: float — MACD histogram normalized by price
- rsi_2h: float (0-100) — RSI from 2-hour wider context
"""


class LLMCodeGenerator:
    """Generate Python guard functions using an LLM."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        max_guards_per_generation: int = 3,
        cache_dir: Path | None = None,
    ):
        self.api_key = api_key or os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = base_url or os.environ.get("LLM_BASE_URL") or None
        self.model = model or os.environ.get("LLM_MODEL", "gpt-4o-mini")
        self.max_guards_per_generation = max_guards_per_generation
        self.cache_dir = cache_dir or (GUARDS_DIR / ".cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._last_call_time = 0.0
        self._min_interval = 2.0  # seconds between API calls

    @property
    def available(self) -> bool:
        """Check if LLM generation is available (API key set)."""
        return bool(self.api_key)

    def generate_guard(
        self,
        insights: list[dict] | None = None,
        elite_guards: list[dict] | None = None,
        generation: int = 0,
        synergy_mode: bool = False,
        champion_guards: dict | None = None,
    ) -> dict[str, Any] | None:
        """Generate a new guard function using the LLM.

        Args:
            insights: Actionable insights from InsightSynthesizer
            elite_guards: Existing elite guard patterns for context
            generation: Current generation number
            synergy_mode: If True, generate a guard complementary to champion's stack
            champion_guards: Champion's guard config dict (used in synergy mode)

        Returns:
            Dict with guard_id, code, file_path, or None if generation fails.
        """
        if not self.available:
            logger.debug("LLM code gen unavailable (no API key)")
            return None

        if synergy_mode and champion_guards:
            prompt = self._build_synergy_prompt(champion_guards, insights, generation)
        else:
            prompt = self._build_prompt(insights, elite_guards, generation=generation)
        code = self._call_llm(prompt)
        if not code:
            return None

        # Validate the generated code
        if not self._validate_guard(code):
            logger.warning("Generated guard failed validation")
            return None

        # Save guard to file
        guard_id = self._guard_id(code)
        file_path = GUARDS_DIR / f"guard_{guard_id}.py"
        file_path.write_text(code, encoding="utf-8")

        # Save metadata
        meta = {
            "guard_id": guard_id,
            "generation": generation,
            "model": self.model,
            "prompt_hash": hashlib.md5(prompt.encode()).hexdigest()[:8],
            "code": code,
            "file_path": str(file_path),
            "synergy_mode": synergy_mode,
        }
        meta_path = GUARDS_DIR / f"guard_{guard_id}.meta.json"
        meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

        logger.info("Generated guard %s (%d chars, synergy=%s)", guard_id, len(code), synergy_mode)
        return meta

    def _build_prompt(
        self,
        insights: list[dict] | None,
        elite_guards: list[dict] | None,
        generation: int = 0,
    ) -> str:
        """Build the LLM prompt with context from insights and elite guards."""
        import random as _rng

        # Pick a random focus area to force diversity across generations
        focus_areas = [
            "Use bb_pct_b and stoch_k together to detect overbought/oversold extremes",
            "Use vwap_deviation to filter trades that are too close to fair value",
            "Use obv_slope to detect volume flow direction and skip trades against it",
            "Use macd_histogram to detect momentum deceleration before entry",
            "Use rsi_2h (2-hour RSI) to align entries with the broader trend",
            "Combine atr_ratio with bb_width to detect true vs false compression",
            "Use stoch_k vs stoch_d crossover to time entries precisely",
            "Filter based on vwap_deviation AND momentum_score disagreement",
            "Create a multi-indicator confirmation requiring 2+ signals to agree",
            "Use bb_pct_b extremes (<0.05 or >0.95) as high-confidence entry zones",
        ]
        focus = _rng.choice(focus_areas)

        parts = [
            f"Generate a Python guard function that filters bad trading signals. (Generation {generation}, variant {_rng.randint(1000,9999)})",
            f"\nTemplate:\n```python\n{GUARD_TEMPLATE.format(feature_keys=', '.join(AVAILABLE_FEATURES[:8]))}\n```",
        ]

        parts.append(f"\nFOCUS AREA for this guard: {focus}")

        if insights:
            parts.append("\nKnown insights from previous generations:")
            for ins in insights[:5]:
                parts.append(f"- {ins['insight']}")

        if elite_guards:
            parts.append("\nPatterns from elite (high-performing) guards:")
            for g in elite_guards[:3]:
                parts.append(f"- {g.get('description', str(g))}")

        parts.append(
            "\nGenerate a DIFFERENT guard that explores the focus area above. "
            "Use the NEW features (bb_pct_b, vwap_deviation, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h). "
            "Return ONLY the Python function definition, nothing else."
        )

        return "\n".join(parts)

    def _build_synergy_prompt(
        self,
        champion_guards: dict,
        insights: list[dict] | None,
        generation: int = 0,
    ) -> str:
        """Build a prompt that generates a guard complementary to the champion's stack."""
        import random as _rng

        # Describe champion's existing guard config
        guard_desc_lines = []
        for key, val in sorted(champion_guards.items()):
            if key.startswith("cr_") or key.endswith("_guard") or key.endswith("_filter"):
                guard_desc_lines.append(f"  - {key} = {val}")

        guard_desc = "\n".join(guard_desc_lines) if guard_desc_lines else "  (no explicit guards)"

        synergy_angles = [
            "Find trades the champion's guards miss: look for patterns where the existing guards pass a trade but it still loses. Target the GAP in their coverage.",
            "Add a volatility-regime filter: the champion guards focus on candle structure. Add a guard that considers broader volatility context (atr_ratio, bb_width, volatility_regime).",
            "Add a momentum confirmation layer: verify that momentum indicators (momentum_score, macd_histogram, obv_slope) agree with the prediction direction before entry.",
            "Add a mean-reversion timing guard: since crypto 15-min is mean-reverting, use RSI extremes (rsi_14, rsi_2h, stoch_k) to time entries at reversal points.",
            "Add a volume quality filter: use volume_ratio and obv_slope to skip trades where volume doesn't confirm the setup.",
        ]
        angle = _rng.choice(synergy_angles)

        parts = [
            f"SYNERGY MODE: Generate a guard that COMPLEMENTS the champion's existing guard stack. (Gen {generation}, variant {_rng.randint(1000,9999)})",
            f"\nThe champion agent (best in population) uses these guards:\n{guard_desc}",
            f"\nYour guard will run IN ADDITION to these. Don't duplicate what they already filter.",
            f"\nSYNERGY ANGLE: {angle}",
            f"\nTemplate:\n```python\n{GUARD_TEMPLATE.format(feature_keys=', '.join(AVAILABLE_FEATURES[:8]))}\n```",
        ]

        if insights:
            parts.append("\nKnown insights from evolution:")
            for ins in insights[:3]:
                parts.append(f"- {ins['insight']}")

        parts.append(
            "\nGenerate a guard that fills a GAP in the champion's defenses. "
            "Return ONLY the Python function definition."
        )

        return "\n".join(parts)

    def _call_llm(self, prompt: str) -> str | None:
        """Call the LLM API with rate limiting and caching."""
        # Check cache
        cache_key = hashlib.md5(prompt.encode()).hexdigest()
        cache_path = self.cache_dir / f"{cache_key}.txt"
        if cache_path.exists():
            return cache_path.read_text(encoding="utf-8")

        # Rate limit
        elapsed = time.time() - self._last_call_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)

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
                temperature=0.8,
                max_tokens=2000,
            )
            self._last_call_time = time.time()

            code = response.choices[0].message.content.strip()

            # Strip reasoning/think tags (MiniMax, DeepSeek, etc.)
            import re
            code = re.sub(r"<think>.*?</think>", "", code, flags=re.DOTALL).strip()

            # Strip markdown code fences if present
            if code.startswith("```python"):
                code = code[len("```python"):].strip()
            if code.startswith("```"):
                code = code[3:].strip()
            if code.endswith("```"):
                code = code[:-3].strip()

            # Cache the result
            cache_path.write_text(code, encoding="utf-8")
            return code

        except ImportError:
            logger.warning("openai package not installed, skipping LLM code gen")
            return None
        except Exception as e:
            logger.error("LLM API call failed: %s", e)
            return None

    def _validate_guard(self, code: str) -> bool:
        """Validate generated guard code is safe and well-formed."""
        # Must contain the guard function definition
        if "def guard(" not in code:
            return False

        # Must not contain dangerous operations
        forbidden = [
            "import os", "import sys", "import subprocess",
            "open(", "exec(", "eval(", "__import__",
            "os.system", "os.popen", "shutil",
            "requests.", "urllib.", "socket.",
        ]
        for f in forbidden:
            if f in code:
                logger.warning("Guard contains forbidden pattern: %s", f)
                return False

        # Must compile without errors
        try:
            compile(code, "<guard>", "exec")
        except SyntaxError as e:
            logger.warning("Guard has syntax error: %s", e)
            return False

        # Must return correct type when executed
        try:
            namespace: dict[str, Any] = {}
            exec(code, namespace)
            guard_fn = namespace.get("guard")
            if not callable(guard_fn):
                return False

            # Test with dummy features
            dummy_features = {k: 0.5 for k in AVAILABLE_FEATURES}
            result = guard_fn(dummy_features, "long")
            if result not in ("long", "short", "skip"):
                logger.warning("Guard returned invalid value: %s", result)
                return False

        except Exception as e:
            logger.warning("Guard execution test failed: %s", e)
            return False

        return True

    def _guard_id(self, code: str) -> str:
        """Generate a short unique ID for a guard from its code."""
        return hashlib.md5(code.encode()).hexdigest()[:10]

    # ── Guard Loading & Management ────────────────────────────

    def load_guard(self, guard_id: str) -> Callable | None:
        """Dynamically load a guard function from its file."""
        file_path = GUARDS_DIR / f"guard_{guard_id}.py"
        if not file_path.exists():
            return None

        try:
            spec = importlib.util.spec_from_file_location(
                f"guard_{guard_id}", file_path,
            )
            if spec is None or spec.loader is None:
                return None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return getattr(module, "guard", None)
        except Exception as e:
            logger.error("Failed to load guard %s: %s", guard_id, e)
            return None

    def list_guards(self) -> list[dict]:
        """List all generated guards with metadata."""
        guards = []
        for meta_path in sorted(GUARDS_DIR.glob("guard_*.meta.json")):
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                guards.append(meta)
            except Exception:
                pass
        return guards

    def prune_guards(
        self,
        guard_results: dict[str, dict],
        min_improvement: float = 0.0,
    ) -> list[str]:
        """Remove guards that don't improve performance.

        Args:
            guard_results: Dict mapping guard_id to fitness results
            min_improvement: Minimum WR improvement over no-guard baseline

        Returns:
            List of pruned guard IDs
        """
        pruned = []
        for guard_id, result in guard_results.items():
            if result.get("win_rate", 0) < 0.52 or not result.get("viable", False):
                # Remove underperforming guard
                guard_path = GUARDS_DIR / f"guard_{guard_id}.py"
                meta_path = GUARDS_DIR / f"guard_{guard_id}.meta.json"
                if guard_path.exists():
                    guard_path.unlink()
                if meta_path.exists():
                    meta_path.unlink()
                pruned.append(guard_id)
                logger.info("Pruned guard %s (WR=%.3f)", guard_id, result.get("win_rate", 0))

        return pruned
