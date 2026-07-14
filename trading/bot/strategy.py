"""Trading strategies. Each returns an index-aligned signal series:
+1 = want long, 0 = flat, -1 = want short (backtester is long/flat by default).
"""

from __future__ import annotations

from .data import Candle
from .indicators import atr, ema, rsi, sma


def ema_crossover(candles: list[Candle], fast: int = 12, slow: int = 48) -> list[int]:
    closes = [c.close for c in candles]
    f, s = ema(closes, fast), ema(closes, slow)
    return [0 if f[i] is None or s[i] is None else (1 if f[i] > s[i] else -1)
            for i in range(len(closes))]


def rsi_mean_reversion(candles: list[Candle], period: int = 14,
                       oversold: float = 30, overbought: float = 70) -> list[int]:
    closes = [c.close for c in candles]
    r = rsi(closes, period)
    sig, state = [], 0
    for v in r:
        if v is not None:
            if v < oversold:
                state = 1
            elif v > overbought:
                state = -1
            elif 45 < v < 55:  # exit near neutral
                state = 0
        sig.append(state)
    return sig


def momentum_breakout(candles: list[Candle], lookback: int = 55,
                      exit_lookback: int = 20) -> list[int]:
    """Donchian-style breakout: long above N-bar high, exit below M-bar low."""
    sig, state = [], 0
    for i, c in enumerate(candles):
        if i >= lookback:
            hi = max(x.high for x in candles[i - lookback:i])
            lo = min(x.low for x in candles[i - exit_lookback:i])
            if c.close > hi:
                state = 1
            elif c.close < lo:
                state = 0
        sig.append(state)
    return sig


def trend_filter_combo(candles: list[Candle]) -> list[int]:
    """EMA cross gated by a long SMA trend filter, with RSI overheat exit."""
    closes = [c.close for c in candles]
    cross = ema_crossover(candles, 12, 48)
    trend = sma(closes, 120)
    r = rsi(closes, 14)
    out = []
    for i in range(len(candles)):
        if trend[i] is None or r[i] is None:
            out.append(0)
        elif cross[i] == 1 and closes[i] > trend[i] and r[i] < 78:
            out.append(1)
        else:
            out.append(0)
    return out


STRATEGIES = {
    "ema_cross": ema_crossover,
    "rsi_reversion": rsi_mean_reversion,
    "breakout": momentum_breakout,
    "combo": trend_filter_combo,
}
