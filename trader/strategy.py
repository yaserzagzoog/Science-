"""Signal generation. Two strategies share one interface:

Strategy ("scalp") — RSI + EMA-crossover on short candles.
  Entry:  RSI oversold recovery OR fast EMA crossing above slow EMA.
  Exit:   RSI overbought, or EMA crossing back down.

SwingStrategy ("swing") — weekly-horizon momentum on daily candles, gated
by a market regime filter (modeled on Sindbad.Tech's "acceleration model"
+ "safeguard signal" design):
  Regime: long only while the regime symbol (e.g. BTCUSDT as the market
          proxy) closes above its long EMA; go/stay in cash otherwise.
  Entry:  fast and slow momentum both positive AND momentum accelerating.
  Exit:   regime turns down, or fast momentum turns negative.
  Far fewer trades than scalp -> far less fee drag.

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

    @property
    def required_bars(self) -> int:
        return max(self.cfg.ema_slow * 4, self.cfg.rsi_period + 2)

    def evaluate(self, closes, holding: bool, regime_closes=None) -> Signal:
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


def roc(closes, days):
    """Rate of change over `days` bars, as a fraction."""
    if len(closes) < days + 1:
        return None
    return closes[-1] / closes[-1 - days] - 1


class SwingStrategy:
    """Daily-candle momentum with a market regime gate. See module docstring."""

    def __init__(self, cfg):
        self.cfg = cfg

    @property
    def required_bars(self) -> int:
        cfg = self.cfg
        return max(cfg.regime_ema_days, cfg.mom_slow_days + cfg.mom_fast_days) + 5

    def regime_up(self, regime_closes) -> bool:
        if not regime_closes or len(regime_closes) < self.cfg.regime_ema_days:
            return False   # unknown regime -> stay defensive
        trend = ema(regime_closes, self.cfg.regime_ema_days)
        return regime_closes[-1] > trend[-1]

    def evaluate(self, closes, holding: bool, regime_closes=None) -> Signal:
        cfg = self.cfg
        up = self.regime_up(regime_closes)
        fast = roc(closes, cfg.mom_fast_days)
        slow = roc(closes, cfg.mom_slow_days)
        fast_prev = roc(closes[:-cfg.mom_fast_days], cfg.mom_fast_days) if \
            len(closes) >= 2 * cfg.mom_fast_days + 1 else None

        if fast is None or slow is None:
            return Signal("HOLD", "not enough data", 50.0)

        if holding:
            if not up:
                return Signal("SELL", "regime turned down (safeguard)", 50.0)
            if fast < 0:
                return Signal("SELL", f"momentum turned negative ({fast:+.1%})", 50.0)
            return Signal("HOLD", "riding trend", 50.0)

        if not up:
            return Signal("HOLD", "regime down - staying in cash", 50.0)
        accelerating = fast_prev is not None and fast > fast_prev
        if fast > 0 and slow > 0 and accelerating:
            return Signal(
                "BUY",
                f"momentum up ({cfg.mom_fast_days}d {fast:+.1%}, "
                f"{cfg.mom_slow_days}d {slow:+.1%}) and accelerating",
                50.0,
            )
        return Signal("HOLD", "no momentum entry", 50.0)


def make_strategy(cfg):
    return SwingStrategy(cfg) if cfg.strategy == "swing" else Strategy(cfg)
