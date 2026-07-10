"""Signal generation: RSI + EMA-crossover momentum on closing prices.

Entry (BUY):  RSI oversold recovery OR fast EMA crossing above slow EMA
              while RSI is not overbought.
Exit (SELL):  RSI overbought, or fast EMA crossing back below slow EMA.
Stop-loss / take-profit exits are handled by risk management, not here.
"""

from dataclasses import dataclass


def ema(values, period):
    if len(values) < period:
        return []
    k = 2 / (period + 1)
    out = [sum(values[:period]) / period]
    for value in values[period:]:
        out.append(value * k + out[-1] * (1 - k))
    return out


def rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    gains, losses = [], []
    for prev, cur in zip(closes[:-1], closes[1:]):
        change = cur - prev
        gains.append(max(change, 0.0))
        losses.append(max(-change, 0.0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for g, l in zip(gains[period:], losses[period:]):
        avg_gain = (avg_gain * (period - 1) + g) / period
        avg_loss = (avg_loss * (period - 1) + l) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)


@dataclass
class Signal:
    action: str   # "BUY", "SELL", or "HOLD"
    reason: str
    rsi: float


class Strategy:
    def __init__(self, cfg):
        self.cfg = cfg

    def evaluate(self, closes, holding: bool) -> Signal:
        cfg = self.cfg
        needed = max(cfg.ema_slow + 2, cfg.rsi_period + 2)
        if len(closes) < needed:
            return Signal("HOLD", "not enough data", 50.0)

        current_rsi = rsi(closes, cfg.rsi_period)
        prev_rsi = rsi(closes[:-1], cfg.rsi_period)
        fast = ema(closes, cfg.ema_fast)
        slow = ema(closes, cfg.ema_slow)
        cross_up = fast[-2] <= slow[-2] and fast[-1] > slow[-1]
        cross_down = fast[-2] >= slow[-2] and fast[-1] < slow[-1]

        if not holding:
            oversold_recovery = (
                prev_rsi is not None
                and prev_rsi < cfg.rsi_oversold
                and current_rsi >= cfg.rsi_oversold
            )
            if oversold_recovery:
                return Signal("BUY", f"RSI recovered from oversold ({current_rsi:.1f})", current_rsi)
            if cross_up and current_rsi < cfg.rsi_overbought:
                return Signal("BUY", "EMA fast crossed above slow", current_rsi)
            return Signal("HOLD", "no entry signal", current_rsi)

        if current_rsi > cfg.rsi_overbought:
            return Signal("SELL", f"RSI overbought ({current_rsi:.1f})", current_rsi)
        if cross_down:
            return Signal("SELL", "EMA fast crossed below slow", current_rsi)
        return Signal("HOLD", "holding", current_rsi)
