"""Market data: live fetch from Binance public API with an offline synthetic fallback.

The synthetic generator produces regime-switching geometric Brownian motion with
volatility clustering, so strategies face trends, chop, and crashes — not a
straight line a bad strategy could accidentally "win" on.
"""

from __future__ import annotations

import json
import math
import random
import urllib.request
from dataclasses import dataclass


@dataclass
class Candle:
    ts: int  # open time, ms since epoch
    open: float
    high: float
    low: float
    close: float
    volume: float


def fetch_binance(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 1000,
                  timeout: float = 10.0) -> list[Candle]:
    """Fetch OHLCV candles from Binance's public (keyless) REST API."""
    url = (f"https://api.binance.com/api/v3/klines?symbol={symbol}"
           f"&interval={interval}&limit={limit}")
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        raw = json.loads(resp.read())
    return [Candle(ts=r[0], open=float(r[1]), high=float(r[2]),
                   low=float(r[3]), close=float(r[4]), volume=float(r[5]))
            for r in raw]


def synthetic(n: int = 2000, start_price: float = 78000.0, seed: int = 7,
              step_ms: int = 3_600_000, start_ts: int = 1_700_000_000_000) -> list[Candle]:
    """Regime-switching GBM with volatility clustering (GARCH-ish)."""
    rng = random.Random(seed)
    # regimes: (annualized drift, base hourly vol)
    regimes = [(0.8, 0.006), (-0.6, 0.011), (0.05, 0.004), (0.0, 0.016)]
    regime = 0
    price = start_price
    vol = regimes[regime][1]
    candles: list[Candle] = []
    for i in range(n):
        if rng.random() < 0.01:  # ~1% chance per bar to switch regime
            regime = rng.randrange(len(regimes))
        drift, base_vol = regimes[regime]
        # volatility clustering: mean-revert vol toward the regime base
        vol = max(0.001, 0.9 * vol + 0.1 * base_vol + 0.15 * vol * abs(rng.gauss(0, 1)) * 0.1)
        r = drift / (365 * 24) + vol * rng.gauss(0, 1)
        o = price
        c = price * math.exp(r)
        wick = abs(rng.gauss(0, vol * 0.7))
        h = max(o, c) * (1 + wick)
        low = min(o, c) * (1 - abs(rng.gauss(0, vol * 0.7)))
        v = abs(rng.gauss(400, 150)) * (1 + 30 * vol)
        candles.append(Candle(ts=start_ts + i * step_ms, open=o, high=h,
                              low=low, close=c, volume=v))
        price = c
    return candles


def load(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 1000,
         seed: int = 7) -> tuple[list[Candle], str]:
    """Try live data, fall back to synthetic. Returns (candles, source)."""
    try:
        return fetch_binance(symbol, interval, limit), "binance-live"
    except Exception:
        return synthetic(n=limit, seed=seed), "synthetic"
