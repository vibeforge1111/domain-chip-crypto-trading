"""Risk Manager -- position sizing, circuit breakers, and stop-loss logic.

Production-grade risk management for live trading deployment.
Uses half-Kelly criterion for conservative position sizing,
ATR-based stop-losses, and daily drawdown circuit breakers.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class TradeRecord:
    """A single trade for risk tracking."""

    agent_id: str
    asset: str
    direction: str  # "long" or "short"
    entry_price: float
    entry_time: datetime
    size_usd: float
    stop_loss: float = 0.0
    exit_price: float | None = None
    exit_time: datetime | None = None
    pnl_usd: float = 0.0
    closed: bool = False


class RiskManager:
    """Production risk management for live trading.

    Parameters:
        max_risk_per_trade: Max fraction of account risked per trade (default 2%)
        max_daily_drawdown: Halt trading if daily loss exceeds this fraction (default 5%)
        max_open_positions: Max concurrent open positions per asset (default 3)
        stop_loss_atr_mult: ATR multiplier for stop-loss distance (default 2.0)
        kelly_fraction: Fraction of full Kelly to use (default 0.5 = half-Kelly)
    """

    def __init__(
        self,
        max_risk_per_trade: float = 0.02,
        max_daily_drawdown: float = 0.05,
        max_open_positions: int = 3,
        stop_loss_atr_mult: float = 2.0,
        kelly_fraction: float = 0.5,
    ):
        self.max_risk_per_trade = max_risk_per_trade
        self.max_daily_drawdown = max_daily_drawdown
        self.max_open_positions = max_open_positions
        self.stop_loss_atr_mult = stop_loss_atr_mult
        self.kelly_fraction = kelly_fraction

        # State
        self._open_trades: list[TradeRecord] = []
        self._closed_trades: list[TradeRecord] = []
        self._daily_pnl: float = 0.0
        self._daily_start_balance: float = 0.0
        self._current_day: str = ""
        self._halted: bool = False
        self._halt_reason: str = ""

    # ── Position Sizing ───────────────────────────────────────

    def size_position(
        self,
        account_balance: float,
        win_rate: float,
        avg_win: float,
        avg_loss: float,
    ) -> float:
        """Calculate position size using half-Kelly criterion.

        Args:
            account_balance: Current account balance in USD
            win_rate: Historical win rate (0-1)
            avg_win: Average winning trade profit in USD
            avg_loss: Average losing trade loss in USD (positive number)

        Returns:
            Position size in USD.
        """
        if account_balance <= 0 or win_rate <= 0 or avg_win <= 0 or avg_loss <= 0:
            return 0.0

        # Kelly criterion: f* = (p * b - q) / b
        # where p = win_rate, q = 1 - p, b = avg_win / avg_loss
        p = min(win_rate, 0.99)  # cap to avoid division issues
        q = 1.0 - p
        b = avg_win / avg_loss

        kelly_full = (p * b - q) / b if b > 0 else 0.0

        # Half-Kelly for safety
        kelly = max(0.0, kelly_full * self.kelly_fraction)

        # Cap at max risk per trade
        kelly = min(kelly, self.max_risk_per_trade)

        position_size = account_balance * kelly

        # Floor at $0, ceiling at 20% of account (hard cap)
        position_size = max(0.0, min(position_size, account_balance * 0.20))

        return round(position_size, 2)

    # ── Trade Gating ──────────────────────────────────────────

    def check_trade_allowed(
        self,
        asset: str | None = None,
        account_balance: float = 0.0,
    ) -> tuple[bool, str]:
        """Check if a new trade is allowed given current risk state.

        Returns:
            (allowed, reason) tuple.
        """
        # Circuit breaker check
        if self._halted:
            return False, f"HALTED: {self._halt_reason}"

        # Daily drawdown check
        if self._daily_start_balance > 0:
            drawdown = -self._daily_pnl / self._daily_start_balance
            if drawdown >= self.max_daily_drawdown:
                self._halted = True
                self._halt_reason = (
                    f"Daily drawdown limit hit: {drawdown:.1%} >= {self.max_daily_drawdown:.1%}"
                )
                return False, self._halt_reason

        # Open position count check
        if asset:
            asset_positions = sum(
                1 for t in self._open_trades if t.asset == asset and not t.closed
            )
            if asset_positions >= self.max_open_positions:
                return False, (
                    f"Max positions for {asset}: {asset_positions}/{self.max_open_positions}"
                )

        total_open = sum(1 for t in self._open_trades if not t.closed)
        if total_open >= self.max_open_positions * 3:  # global cap
            return False, f"Global position limit: {total_open}"

        return True, "OK"

    # ── Stop-Loss ─────────────────────────────────────────────

    def calculate_stop_loss(
        self,
        entry_price: float,
        direction: str,
        atr: float,
    ) -> float:
        """Calculate ATR-based stop-loss price.

        Args:
            entry_price: Trade entry price
            direction: "long" or "short"
            atr: Current Average True Range value

        Returns:
            Stop-loss price.
        """
        distance = atr * self.stop_loss_atr_mult

        if direction == "long":
            return round(entry_price - distance, 8)
        else:  # short
            return round(entry_price + distance, 8)

    def check_stop_loss(self, trade: TradeRecord, current_price: float) -> bool:
        """Check if a trade's stop-loss has been hit.

        Returns True if stop-loss triggered.
        """
        if trade.stop_loss <= 0:
            return False

        if trade.direction == "long":
            return current_price <= trade.stop_loss
        else:
            return current_price >= trade.stop_loss

    # ── Trade Lifecycle ───────────────────────────────────────

    def open_trade(
        self,
        agent_id: str,
        asset: str,
        direction: str,
        entry_price: float,
        size_usd: float,
        atr: float = 0.0,
    ) -> TradeRecord | None:
        """Open a new trade with risk checks.

        Returns TradeRecord if allowed, None if blocked.
        """
        allowed, reason = self.check_trade_allowed(asset=asset)
        if not allowed:
            logger.warning("Trade blocked: %s", reason)
            return None

        stop_loss = self.calculate_stop_loss(entry_price, direction, atr) if atr > 0 else 0.0

        trade = TradeRecord(
            agent_id=agent_id,
            asset=asset,
            direction=direction,
            entry_price=entry_price,
            entry_time=datetime.now(timezone.utc),
            size_usd=size_usd,
            stop_loss=stop_loss,
        )
        self._open_trades.append(trade)
        logger.info(
            "Opened %s %s %.2f USD @ %.2f (SL=%.2f)",
            direction, asset, size_usd, entry_price, stop_loss,
        )
        return trade

    def close_trade(
        self,
        trade: TradeRecord,
        exit_price: float,
    ) -> float:
        """Close a trade and calculate PnL.

        Returns PnL in USD.
        """
        if trade.closed:
            return trade.pnl_usd

        trade.exit_price = exit_price
        trade.exit_time = datetime.now(timezone.utc)
        trade.closed = True

        # Calculate PnL
        if trade.direction == "long":
            pnl_pct = (exit_price - trade.entry_price) / trade.entry_price
        else:
            pnl_pct = (trade.entry_price - exit_price) / trade.entry_price

        trade.pnl_usd = round(trade.size_usd * pnl_pct, 2)

        # Update daily PnL
        self._daily_pnl += trade.pnl_usd

        # Move to closed list
        self._open_trades = [t for t in self._open_trades if not t.closed]
        self._closed_trades.append(trade)

        logger.info(
            "Closed %s %s @ %.2f -> %.2f (PnL: %+.2f USD)",
            trade.direction, trade.asset, trade.entry_price, exit_price, trade.pnl_usd,
        )
        return trade.pnl_usd

    # ── Daily Reset ───────────────────────────────────────────

    def start_new_day(self, account_balance: float) -> None:
        """Reset daily tracking for a new trading day."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if today != self._current_day:
            self._current_day = today
            self._daily_pnl = 0.0
            self._daily_start_balance = account_balance
            self._halted = False
            self._halt_reason = ""
            logger.info("New trading day: %s (balance: %.2f)", today, account_balance)

    # ── Reporting ─────────────────────────────────────────────

    def daily_report(self) -> dict[str, Any]:
        """Generate daily risk report."""
        open_count = sum(1 for t in self._open_trades if not t.closed)
        open_exposure = sum(t.size_usd for t in self._open_trades if not t.closed)
        closed_today = [
            t for t in self._closed_trades
            if t.exit_time and t.exit_time.strftime("%Y-%m-%d") == self._current_day
        ]
        wins = sum(1 for t in closed_today if t.pnl_usd > 0)
        losses = sum(1 for t in closed_today if t.pnl_usd <= 0)

        drawdown_pct = (
            -self._daily_pnl / self._daily_start_balance
            if self._daily_start_balance > 0
            else 0.0
        )

        return {
            "date": self._current_day,
            "daily_pnl": round(self._daily_pnl, 2),
            "daily_drawdown_pct": round(drawdown_pct, 4),
            "open_positions": open_count,
            "open_exposure_usd": round(open_exposure, 2),
            "trades_today": len(closed_today),
            "wins": wins,
            "losses": losses,
            "win_rate": round(wins / len(closed_today), 3) if closed_today else 0.0,
            "halted": self._halted,
            "halt_reason": self._halt_reason,
            "max_risk_per_trade": self.max_risk_per_trade,
            "max_daily_drawdown": self.max_daily_drawdown,
            "max_open_positions": self.max_open_positions,
        }
