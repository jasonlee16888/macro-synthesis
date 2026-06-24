"""Live trading module for Macro Synthesis — auto-execution path.

Handles real-time signal generation and trade execution via
getagent.trade for Bitget RWA USDT perpetual contracts.

Used by the live path in main.py when execution_mode is follow_trade.
"""

import math
from typing import Any, Optional

from getagent import data, runtime, trade


# ------------------------------------------------------------------
# Signal generation (live, no backtest engine)
# ------------------------------------------------------------------

class LiveRegimeSignal:
    """Compute regime score from live kline data for a single symbol."""

    def __init__(self, config: dict):
        self.cfg = config
        self.closes: list[float] = []
        self.highs: list[float] = []
        self.lows: list[float] = []
        self.fast_ema: Optional[float] = None
        self.slow_ema: Optional[float] = None
        self.atr: Optional[float] = None
        self._warmed: bool = False

    def feed_bar(self, close: float, high: float, low: float) -> Optional[float]:
        """Feed one OHLCV bar, return regime score once warm."""
        self.closes.append(close)
        self.highs.append(high)
        self.lows.append(low)

        slow = self.cfg.get("trend_slow", 26)
        vol_lb = self.cfg.get("volatility_lookback", 20)
        warmup = max(slow, vol_lb) + 1

        fast_p = self.cfg.get("trend_fast", 12)
        slow_p = self.cfg.get("trend_slow", 26)

        if len(self.closes) < warmup:
            self.fast_ema = _ema(self.fast_ema, close, fast_p)
            self.slow_ema = _ema(self.slow_ema, close, slow_p)
            self.atr = _atr(self.atr, high, low, close, vol_lb)
            return None

        self._warmed = True
        self.fast_ema = _ema(self.fast_ema, close, fast_p)
        self.slow_ema = _ema(self.slow_ema, close, slow_p)
        self.atr = _atr(self.atr, high, low, close, vol_lb)

        vol_score = _vol_score(self.atr, self.closes)
        trend_score = _trend_score(self.fast_ema, self.slow_ema)
        mom_score = _mom_score(self.closes, self.cfg.get("momentum_period", 10))

        vw = self.cfg.get("volatility_weight", 0.25)
        tw = self.cfg.get("trend_weight", 0.45)
        mw = self.cfg.get("momentum_weight", 0.30)

        return max(0.0, min(1.0, vw * vol_score + tw * trend_score + mw * mom_score))


# ------------------------------------------------------------------
# Trade execution
# ------------------------------------------------------------------

def execute_long(symbol: str, config: dict) -> dict:
    """Open a long position on a Bitget RWA USDT perpetual."""
    margin = config.get("margin_budget", "5000")
    lev = config.get("leverage", 10)

    qty_plan = trade.helpers.compute_qty(
        symbol=symbol,
        market="contract",
        budget_amount=str(margin),
        leverage=lev,
    )

    tpsl_plan = trade.helpers.resolve_contract_tpsl(
        symbol=symbol,
        side="long",
        leverage=lev,
    )

    result = trade.contract.open_long_market(
        symbol=symbol,
        qty=qty_plan.qty,
        tp_trigger_price=tpsl_plan.tp_trigger_price,
        sl_trigger_price=tpsl_plan.sl_trigger_price,
    )

    return {
        "action": "long",
        "symbol": symbol,
        "qty": str(qty_plan.qty) if qty_plan else "0",
        "leverage": lev,
        "success": trade.is_success(result),
        "order_id": getattr(result, "order_id", "") if result else "",
    }


def execute_close(symbol: str) -> dict:
    """Close all open positions for a symbol."""
    result = trade.contract.close_position_market(symbol=symbol)
    return {
        "action": "close",
        "symbol": symbol,
        "success": trade.is_success(result),
        "order_id": getattr(result, "order_id", "") if result else "",
    }


# ------------------------------------------------------------------
# Helpers (mirror strategy.py logic for live use)
# ------------------------------------------------------------------

def _ema(prev: Optional[float], value: float, period: int) -> float:
    if prev is None:
        return value
    alpha = 2.0 / (period + 1)
    return alpha * value + (1.0 - alpha) * prev


def _atr(prev: Optional[float], high: float, low: float, close: float, period: int) -> float:
    tr = max(high - low, abs(high - close), abs(low - close))
    if prev is None:
        return tr
    return (1.0 / period) * tr + (1.0 - 1.0 / period) * prev


def _vol_score(atr: Optional[float], closes: list[float]) -> float:
    if atr is None or atr <= 0 or len(closes) < 2:
        return 0.5
    price = closes[-1]
    if price <= 0:
        return 0.5
    return max(0.0, min(1.0, 1.0 - (atr / price) / 0.05))


def _trend_score(fast_ema: Optional[float], slow_ema: Optional[float]) -> float:
    if fast_ema is None or slow_ema is None or slow_ema <= 0:
        return 0.5
    return max(0.0, min(1.0, (fast_ema / slow_ema - 0.95) / 0.10))


def _mom_score(closes: list[float], period: int) -> float:
    if len(closes) < period + 1:
        return 0.5
    wins = sum(1 for i in range(len(closes) - period, len(closes))
               if i > 0 and closes[i] > closes[i - 1])
    return wins / period if period > 0 else 0.5
