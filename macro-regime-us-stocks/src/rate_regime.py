"""Rate cycle detection from FRED federal funds rate data.

Provides `compute_rate_regime()` which returns a float between 0 and 1:
  - > 0.5: dovish (rates falling / being cut)
  - < 0.5: hawkish (rates rising / being hiked)
  - 0.5: neutral / no data

Used by the strategy to adjust risk budget — dovish regime loosens
thresholds and increases position sizing; hawkish tightens them.
"""

import math
from typing import Optional


# Known FRED series ID for effective federal funds rate
FED_FUNDS_RATE_SERIES = "FEDFUNDS"


def compute_rate_regime(rate_data: Optional[list[dict]] = None) -> float:
    """Return a rate regime score from FRED-like data.

    Args:
        rate_data: Optional list of dicts with 'value' and optional 'date'/'time'.
                   If None or empty, returns 0.5 (neutral / unknown).

    Returns:
        float in [0.0, 1.0] where higher = more dovish (cutting).
    """
    if not rate_data:
        return 0.5

    values = []
    for row in rate_data:
        v = None
        if isinstance(row, dict):
            v = row.get("value")
        if v is None:
            continue
        try:
            values.append(float(v))
        except (ValueError, TypeError):
            continue

    if len(values) < 3:
        return 0.5

    # Use last 3 data points to determine direction
    recent = values[-3:]
    if len(recent) < 3:
        return 0.5

    # Rate level: higher rates → more hawkish
    current = recent[-1]
    # Normalize: ~2.5% = neutral, ~5.5% = very hawkish, ~0% = very dovish
    level_score = 1.0 - max(0.0, min(1.0, current / 5.5))

    # Rate direction: falling → dovish
    oldest, newest = recent[0], recent[-1]
    if oldest > 0:
        change = (newest - oldest) / oldest
        # -5% change → dovish=1.0, +5% → dovish=0.0
        direction_score = 0.5 - change * 10.0
        direction_score = max(0.0, min(1.0, direction_score))
    else:
        direction_score = 0.5

    # Blend: 40% level, 60% direction (trend matters more than absolute level)
    raw = 0.4 * level_score + 0.6 * direction_score
    return max(0.0, min(1.0, raw))


def fetch_and_compute(data_module=None) -> float:
    """Fetch FRED data and compute rate regime.

    In the Playbook sandbox, use `data.economy.fred_series()`.
    Outside the sandbox, pass None and return neutral (0.5).

    Args:
        data_module: The `getagent.data` module, if available.

    Returns:
        float rate regime score.
    """
    if data_module is None:
        return 0.5

    try:
        rates = data_module.economy.fred_series(
            series_id=FED_FUNDS_RATE_SERIES,
            limit=12,
        )
        if rates is not None and hasattr(rates, 'results'):
            rate_list = rates.results if isinstance(rates.results, list) else []
            return compute_rate_regime(rate_list)
        elif isinstance(rates, list):
            return compute_rate_regime(rates)
    except Exception:
        pass

    return 0.5
