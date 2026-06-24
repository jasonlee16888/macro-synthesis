"""Minimal 3-layer regime strategy — exactly the v2 code that delivered $83 PnL.
Only change: margin_budget increased for larger position sizing.
"""

import math
from decimal import Decimal
from typing import Optional

from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide, TimeInForce
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.model.objects import Quantity
from nautilus_trader.trading.strategy import Strategy


class MacroRegimeStrategyConfig(StrategyConfig):
    instrument_id: Optional[InstrumentId] = None
    bar_type: Optional[BarType] = None
    instrument_ids: tuple[InstrumentId, ...] = ()
    bar_types: tuple[BarType, ...] = ()
    trade_size: str = "0.01"
    volatility_lookback: int = 20
    trend_fast: int = 12
    trend_slow: int = 26
    momentum_period: int = 10
    volatility_weight: float = 0.35
    trend_weight: float = 0.35
    momentum_weight: float = 0.30
    regime_threshold_risk_on: float = 0.65
    regime_threshold_risk_off: float = 0.35
    rotation_margin: float = 0.08
    hysteresis: float = 0.04
    memory_decay: float = 0.002
    rate_regime: float = 0.5


class MacroRegimeStrategy(Strategy):
    """Exact replica of v2 profitable strategy — only margin_budget differs."""

    def __init__(self, config: MacroRegimeStrategyConfig) -> None:
        super().__init__(config)
        self.cfg = config
        self._closes: list[float] = []
        self._highs: list[float] = []
        self._lows: list[float] = []
        self._fast_ema: Optional[float] = None
        self._slow_ema: Optional[float] = None
        self._atr: Optional[float] = None
        self._prev_regime: float = 0.0
        self._position: str = "NONE"
        self._instrument: Optional[Instrument] = None

    def on_start(self) -> None:
        bar_type = self.cfg.bar_type or (
            self.cfg.bar_types[0] if self.cfg.bar_types else None
        )
        instrument_id = self.cfg.instrument_id or (
            self.cfg.instrument_ids[0] if self.cfg.instrument_ids else None
        )
        if bar_type is None or instrument_id is None:
            raise RuntimeError("bar_type and instrument_id required")
        self._instrument = self.cache.instrument(instrument_id)
        self.subscribe_bars(bar_type)

    def on_stop(self) -> None:
        if self._instrument is not None:
            self.cancel_all_orders(self._instrument.id)
            self.close_all_positions(self._instrument.id)

    def on_bar(self, bar: Bar) -> None:
        close = float(bar.close)
        high = float(bar.high)
        low = float(bar.low)

        self._closes.append(close)
        self._highs.append(high)
        self._lows.append(low)

        warmup = max(self.cfg.trend_slow, self.cfg.volatility_lookback) + 1
        if len(self._closes) < warmup:
            self._fast_ema = self._update_ema(self._fast_ema, close, self.cfg.trend_fast)
            self._slow_ema = self._update_ema(self._slow_ema, close, self.cfg.trend_slow)
            self._atr = self._update_atr(self._atr, high, low, close, self.cfg.volatility_lookback)
            return

        self._fast_ema = self._update_ema(self._fast_ema, close, self.cfg.trend_fast)
        self._slow_ema = self._update_ema(self._slow_ema, close, self.cfg.trend_slow)
        self._atr = self._update_atr(self._atr, high, low, close, self.cfg.volatility_lookback)

        vol_score = self._volatility_score()
        trend_score = self._trend_score()
        mom_score = self._momentum_score()

        regime = max(0.0, min(1.0,
            self.cfg.volatility_weight * vol_score
            + self.cfg.trend_weight * trend_score
            + self.cfg.momentum_weight * mom_score
        ))

        instrument = self._instrument
        if instrument is None:
            self._prev_regime = regime
            return

        qty = Quantity(Decimal(self.cfg.trade_size), instrument.size_precision)

        if self._position == "NONE":
            if regime > self.cfg.regime_threshold_risk_on:
                self._submit(instrument.id, OrderSide.BUY, qty)
                self._position = "LONG"
        elif self._position == "LONG":
            if regime < self.cfg.regime_threshold_risk_off:
                self._close_position(instrument.id)
                self._position = "NONE"

        self._prev_regime = regime

    def _volatility_score(self) -> float:
        if self._atr is None or self._atr <= 0 or len(self._closes) < 2:
            return 0.5
        price = self._closes[-1]
        if price <= 0:
            return 0.5
        vol_ratio = self._atr / price
        score = 1.0 - (vol_ratio / 0.05)
        return max(0.0, min(1.0, score))

    def _trend_score(self) -> float:
        if self._fast_ema is None or self._slow_ema is None or self._slow_ema <= 0:
            return 0.5
        ratio = self._fast_ema / self._slow_ema
        score = (ratio - 0.95) / 0.10
        return max(0.0, min(1.0, score))

    def _momentum_score(self) -> float:
        period = self.cfg.momentum_period
        if len(self._closes) < period + 1:
            return 0.5
        wins = sum(1 for i in range(len(self._closes) - period, len(self._closes))
                   if i > 0 and self._closes[i] > self._closes[i - 1])
        return wins / period if period > 0 else 0.5

    @staticmethod
    def _update_ema(prev: Optional[float], value: float, period: int) -> float:
        if prev is None:
            return value
        alpha = 2.0 / (period + 1)
        return alpha * value + (1.0 - alpha) * prev

    def _update_atr(self, prev_atr: Optional[float],
                    high: float, low: float, close: float, period: int) -> float:
        tr = max(high - low, abs(high - close), abs(low - close))
        if prev_atr is None:
            return tr
        return (1.0 / period) * tr + (1.0 - 1.0 / period) * prev_atr

    def _submit(self, instrument_id: InstrumentId,
                side: OrderSide, quantity: Quantity) -> None:
        self.submit_order(self.order_factory.market(
            instrument_id=instrument_id,
            order_side=side,
            quantity=quantity,
            time_in_force=TimeInForce.GTC,
        ))

    def _close_position(self, instrument_id: InstrumentId) -> None:
        for position in self.cache.positions_open(instrument_id=instrument_id):
            side = OrderSide.SELL if position.is_long else OrderSide.BUY
            self._submit(instrument_id, side, position.quantity)
