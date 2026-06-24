"""Entry point for the Macro Synthesis Multi-Symbol Rotation Playbook.

Fetches kline data for all configured trading symbols, optionally fetches
FRED federal funds rate data for rate cycle awareness, assembles OHLCV
frames, and runs the Nautilus multi-instrument backtest.

Handles both historical backtest and live evaluation paths.
"""

import math
from typing import Any, Optional

from getagent import backtest, data, runtime

from . import live_trading, rate_regime

# Module-level global so strategy.py can read it.
RATE_REGIME: float = 0.5


def _sanitize(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _sanitize_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    return {key: _sanitize(val) for key, val in metrics.items()}


def _fetch_kline(symbol: str, interval: str = "4h", limit: int = 500) -> Any:
    """Fetch kline data, falling back gracefully on error."""
    try:
        return data.crypto.futures.kline(
            symbol=symbol,
            interval=interval,
            limit=limit,
        )
    except Exception:
        return None


def run_backtest() -> None:
    global RATE_REGIME

    cfg = runtime.manifest.get("strategy_config", {}) or {}
    symbols = cfg.get("trading_symbols") or ["NVDAUSDT"]

    # ------------------------------------------------------------------
    # 1. Fetch rate regime from FRED
    # ------------------------------------------------------------------
    RATE_REGIME = rate_regime.fetch_and_compute(data)
    # If FRED unavailable in this sandbox, default to neutral (0.5)

    # ------------------------------------------------------------------
    # 2. Fetch kline data for all symbols
    # ------------------------------------------------------------------
    ohlcv_data: dict[str, Any] = {}
    symbol_meta: list[dict[str, Any]] = []
    total_rows = 0

    for symbol in symbols:
        bars = _fetch_kline(symbol)
        if bars is None:
            symbol_meta.append({"symbol": symbol, "rows": 0, "error": "fetch_failed"})
            continue

        frame = backtest.prepare_frame(bars, datetime_index="date")
        if frame is None or frame.empty:
            symbol_meta.append({"symbol": symbol, "rows": 0, "error": "empty_frame"})
            continue

        instr_key = f"{symbol}.BINANCE"
        ohlcv_data[instr_key] = frame
        n_rows = len(frame)
        total_rows += n_rows
        symbol_meta.append({
            "symbol": symbol,
            "rows": n_rows,
            "first": str(frame.index[0]) if n_rows > 0 else None,
            "last": str(frame.index[-1]) if n_rows > 0 else None,
        })

    if not ohlcv_data:
        runtime.emit_signal(
            action="watch",
            symbol=symbols[0],
            confidence=0.0,
            metrics={"rows": 0, "rate_regime": RATE_REGIME},
            meta={"reason": "no historical bars for any symbol", "symbols": symbol_meta},
        )
        return

    # ------------------------------------------------------------------
    # 3. Inject rate_regime into strategy config via backtest spec
    # ------------------------------------------------------------------
    spec = runtime.backtest_spec
    if spec is not None and hasattr(spec, 'strategy') and hasattr(spec.strategy, 'config'):
        if isinstance(spec.strategy.config, dict):
            spec.strategy.config["rate_regime"] = RATE_REGIME

    # ------------------------------------------------------------------
    # 4. Run multi-instrument Nautilus backtest
    # ------------------------------------------------------------------
    result = backtest.run(ohlcv_data=ohlcv_data, spec=spec)

    # ------------------------------------------------------------------
    # 5. Generate chart & extract metrics
    # ------------------------------------------------------------------
    chart_path = backtest.generate_chart(result)
    summary = result.summary or {}
    net_pnl_raw = summary.get("net_pnl", 0)
    try:
        net_pnl = float(net_pnl_raw or 0)
    except (TypeError, ValueError):
        net_pnl = 0.0

    action = "long" if net_pnl > 0 else "watch"

    metrics = _sanitize_metrics({
        "total_return_pct": result.total_return_pct,
        "net_pnl": net_pnl,
        "starting_balance": summary.get("starting_balance"),
        "ending_balance": summary.get("ending_balance"),
        "sharpe_ratio": result.sharpe_ratio,
        "max_drawdown_pct": result.max_drawdown_pct,
        "win_rate": result.win_rate,
        "total_trades": result.total_trades,
        "profit_factor": result.profit_factor,
        "rows": total_rows,
        "symbols_loaded": len(ohlcv_data),
        "symbols": symbol_meta,
        "rate_regime": RATE_REGIME,
    })

    runtime.emit_signal(
        action=action,
        symbol=symbols[0],
        confidence=_sanitize(result.win_rate) or 0.0,
        metrics=metrics,
        meta={
            "chart_path": chart_path,
            "rate_regime": RATE_REGIME,
            "symbol_count": len(ohlcv_data),
        },
    )


def run_live() -> None:
    """Live trading path — fetch klines, compute regime, emit signal or auto-trade."""
    global RATE_REGIME
    RATE_REGIME = rate_regime.fetch_and_compute(data)

    cfg = runtime.manifest.get("strategy_config", {}) or {}
    symbols = cfg.get("trading_symbols") or ["NVDAUSDT"]
    interval = "4h"

    # --- Build live regime signals for all symbols ---
    signals: dict[str, float] = {}
    for symbol in symbols:
        try:
            bars = data.crypto.futures.kline(symbol=symbol, interval=interval, limit=100)
            if bars is None:
                continue
            frame = data.to_dataframe(bars)
            if frame is None or frame.empty:
                continue

            sig_gen = live_trading.LiveRegimeSignal(cfg)
            regime = None
            for _, row in frame.iterrows():
                regime = sig_gen.feed_bar(
                    float(row.get("close", 0)),
                    float(row.get("high", 0)),
                    float(row.get("low", 0)),
                )
            if regime is not None:
                signals[symbol] = regime
        except Exception:
            continue

    if not signals:
        runtime.emit_signal(
            action="watch", symbol=symbols[0], confidence=0.0,
            metrics={"rate_regime": RATE_REGIME, "signals": 0},
            meta={"reason": "no live regime signals computed"},
        )
        return

    # --- Select best symbol ---
    best_symbol, best_regime = max(signals.items(), key=lambda x: x[1])
    entry_th = cfg.get("regime_threshold_risk_on", 0.35)

    defense = cfg.get("defense_mode", 0.0)
    entry_th_adj = entry_th * (1.0 + defense * 0.2)

    action = "long" if best_regime > entry_th_adj else "watch"
    confidence = best_regime

    def _do_trade():
        return live_trading.execute_long(best_symbol, cfg)

    runtime.emit_signal_or_follow(
        action=action,
        symbol=best_symbol,
        confidence=confidence,
        metrics={
            "rate_regime": RATE_REGIME,
            "defense_mode": defense,
            "best_regime": best_regime,
            "entry_threshold": entry_th_adj,
            "all_signals": signals,
        },
        meta={"source": "live_cron"},
        execute_trade=_do_trade if action == "long" else None,
    )


def run() -> None:
    if runtime.is_historical():
        run_backtest()
    elif runtime.is_live():
        run_live()
    else:
        raise ValueError(f"unsupported evaluation_mode={runtime.evaluation_mode!r}")


if __name__ == "__main__":
    run()
