"""Technical indicators computed over full series (index-aligned, None until warm)."""

from __future__ import annotations


def sma(values: list[float], period: int) -> list[float | None]:
    out: list[float | None] = [None] * len(values)
    s = 0.0
    for i, v in enumerate(values):
        s += v
        if i >= period:
            s -= values[i - period]
        if i >= period - 1:
            out[i] = s / period
    return out


def ema(values: list[float], period: int) -> list[float | None]:
    out: list[float | None] = [None] * len(values)
    k = 2.0 / (period + 1)
    prev: float | None = None
    for i, v in enumerate(values):
        if i == period - 1:
            prev = sum(values[:period]) / period
        elif prev is not None:
            prev = v * k + prev * (1 - k)
        out[i] = prev
    return out


def rsi(values: list[float], period: int = 14) -> list[float | None]:
    out: list[float | None] = [None] * len(values)
    avg_gain = avg_loss = 0.0
    for i in range(1, len(values)):
        change = values[i] - values[i - 1]
        gain, loss = max(change, 0.0), max(-change, 0.0)
        if i <= period:
            avg_gain += gain / period
            avg_loss += loss / period
            if i == period:
                out[i] = 100.0 if avg_loss == 0 else 100 - 100 / (1 + avg_gain / avg_loss)
        else:
            avg_gain = (avg_gain * (period - 1) + gain) / period
            avg_loss = (avg_loss * (period - 1) + loss) / period
            out[i] = 100.0 if avg_loss == 0 else 100 - 100 / (1 + avg_gain / avg_loss)
    return out


def atr(highs: list[float], lows: list[float], closes: list[float],
        period: int = 14) -> list[float | None]:
    out: list[float | None] = [None] * len(closes)
    prev: float | None = None
    trs: list[float] = []
    for i in range(len(closes)):
        if i == 0:
            tr = highs[i] - lows[i]
        else:
            tr = max(highs[i] - lows[i],
                     abs(highs[i] - closes[i - 1]),
                     abs(lows[i] - closes[i - 1]))
        trs.append(tr)
        if i == period - 1:
            prev = sum(trs) / period
        elif prev is not None:
            prev = (prev * (period - 1) + tr) / period
        out[i] = prev
    return out
