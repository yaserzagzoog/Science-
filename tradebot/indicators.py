"""Small stdlib-only indicator helpers. All return lists aligned to the input,
with None where the window is not yet full."""


def sma(values: list[float], length: int) -> list:
    out = [None] * len(values)
    total = 0.0
    for i, v in enumerate(values):
        total += v
        if i >= length:
            total -= values[i - length]
        if i >= length - 1:
            out[i] = total / length
    return out


def rolling_max(values: list[float], length: int) -> list:
    """Max of the PRIOR `length` bars (excludes the current bar) — the
    breakout resistance in `ta.crossover(close, ta.highest(high, 20))` terms."""
    out = [None] * len(values)
    for i in range(len(values)):
        if i >= length:
            out[i] = max(values[i - length:i])
    return out


def rolling_min(values: list[float], length: int) -> list:
    """Min of the PRIOR `length` bars (excludes the current bar)."""
    out = [None] * len(values)
    for i in range(len(values)):
        if i >= length:
            out[i] = min(values[i - length:i])
    return out


def rsi(closes: list[float], length: int = 14) -> list:
    out = [None] * len(closes)
    if len(closes) <= length:
        return out
    gains, losses = 0.0, 0.0
    for i in range(1, length + 1):
        d = closes[i] - closes[i - 1]
        gains += max(d, 0)
        losses += max(-d, 0)
    avg_gain, avg_loss = gains / length, losses / length
    out[length] = 100.0 if avg_loss == 0 else 100 - 100 / (1 + avg_gain / avg_loss)
    for i in range(length + 1, len(closes)):
        d = closes[i] - closes[i - 1]
        avg_gain = (avg_gain * (length - 1) + max(d, 0)) / length
        avg_loss = (avg_loss * (length - 1) + max(-d, 0)) / length
        out[i] = 100.0 if avg_loss == 0 else 100 - 100 / (1 + avg_gain / avg_loss)
    return out


def atr(highs: list[float], lows: list[float], closes: list[float], length: int = 14) -> list:
    n = len(closes)
    out = [None] * n
    if n < 2:
        return out
    trs = [highs[0] - lows[0]]
    for i in range(1, n):
        trs.append(max(highs[i] - lows[i],
                       abs(highs[i] - closes[i - 1]),
                       abs(lows[i] - closes[i - 1])))
    if n <= length:
        return out
    a = sum(trs[1:length + 1]) / length
    out[length] = a
    for i in range(length + 1, n):
        a = (a * (length - 1) + trs[i]) / length
        out[i] = a
    return out
