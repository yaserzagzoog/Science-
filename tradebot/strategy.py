"""The Fable Rules strategy: breakout above 20-day resistance confirmed by
rising volume, structure stop at the 10-day low, exit on close below the
20-day support. Produces one Signal per symbol per day."""

from dataclasses import dataclass, field

from .config import PARAMS
from .data import Bar
from .indicators import atr, rolling_max, rolling_min, rsi, sma

# Signal states, most actionable first.
BUY = "BUY"                    # fresh breakout today, volume confirmed
BREAKOUT_UNCONFIRMED = "BREAKOUT (LOW VOL)"  # broke out without volume backing
WATCH = "WATCH"                # within striking distance of the trigger
UPTREND = "IN UPTREND"         # above trend filter, no fresh trigger
EXIT = "EXIT"                  # closed below 20-day support today
NEUTRAL = "NEUTRAL"            # nothing to do

STATE_ORDER = [BUY, BREAKOUT_UNCONFIRMED, WATCH, UPTREND, NEUTRAL, EXIT]


@dataclass
class Signal:
    symbol: str
    name: str
    asset_class: str
    date: str
    state: str
    close: float
    change_1d: float
    change_5d: float
    change_20d: float
    resistance: float          # 20-day high = entry trigger
    support: float             # 20-day low = exit line
    stop: float                # 10-day low = initial stop
    dist_to_trigger_pct: float  # negative = below trigger
    volume_ratio: float        # today's volume / 20-day average
    rsi14: float
    sma50: float
    above_trend: bool
    entry: float               # suggested entry (the trigger level)
    risk_per_share: float
    shares: int                # for account_size at risk_pct
    risk_dollars: float
    targets: list = field(default_factory=list)  # [(label, price), ...]
    note: str = ""
    closes: list = field(default_factory=list)   # trailing closes for sparkline
    dates: list = field(default_factory=list)


def analyze(symbol: str, name: str, asset_class: str, bars: list[Bar],
            params: dict | None = None) -> Signal | None:
    p = dict(PARAMS)
    if params:
        p.update(params)
    n = len(bars)
    need = max(p["breakout_len"], p["exit_len"], p["trend_len"]) + 2
    if n < need:
        return None

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    vols = [b.volume for b in bars]

    res = rolling_max(highs, p["breakout_len"])
    sup = rolling_min(lows, p["exit_len"])
    stop_line = rolling_min(lows, p["stop_len"])
    vol_sma = sma(vols, p["vol_len"])
    trend = sma(closes, p["trend_len"])
    rsi14 = rsi(closes, 14)

    i = n - 1
    c, c1 = closes[i], closes[i - 1]
    resistance, support, stop = res[i], sup[i], stop_line[i]
    v_avg = vol_sma[i] or 0.0
    vol_ratio = (vols[i] / v_avg) if v_avg else 0.0

    crossed_up = c > resistance and c1 <= res[i - 1]
    crossed_down = c < support and c1 >= sup[i - 1]
    vol_ok = vol_ratio > 1.0
    dist = (c / resistance - 1.0) * 100.0

    if crossed_down:
        state, note = EXIT, "Closed below 20-day support — exit / stand aside."
    elif crossed_up and vol_ok:
        state, note = BUY, (f"Fresh breakout above {resistance:.2f} on "
                            f"{vol_ratio:.1f}x average volume.")
    elif crossed_up:
        state, note = BREAKOUT_UNCONFIRMED, (
            "Broke resistance but volume is below average — wait for confirmation.")
    elif -p["near_trigger_pct"] <= dist < 0:
        state, note = WATCH, (f"Within {abs(dist):.1f}% of the {resistance:.2f} "
                              f"trigger — set an alert / buy-stop above it.")
    elif trend[i] is not None and c > trend[i]:
        state, note = UPTREND, "Above the 50-day trend line; no fresh trigger yet."
    else:
        state, note = NEUTRAL, "Below trend and away from the trigger — no edge here."

    # Position sizing at the trigger (worst-case fill = trigger price).
    entry = resistance if state in (WATCH, UPTREND, NEUTRAL) else c
    risk_ps = max(entry - stop, 0.0)
    if risk_ps > 0:
        risk_dollars = p["account_size"] * p["risk_pct"] / 100.0
        shares = int(risk_dollars / risk_ps)
    else:
        risk_dollars, shares = 0.0, 0
    targets = [(f"{r:g}R", entry + r * risk_ps) for r in p["target_r"]] if risk_ps else []

    def chg(k):
        return (c / closes[i - k] - 1.0) * 100.0 if i >= k else 0.0

    tail = min(60, n)
    return Signal(
        symbol=symbol, name=name, asset_class=asset_class, date=bars[i].date,
        state=state, close=c, change_1d=chg(1), change_5d=chg(5), change_20d=chg(20),
        resistance=resistance, support=support, stop=stop,
        dist_to_trigger_pct=dist, volume_ratio=vol_ratio,
        rsi14=rsi14[i] or 0.0, sma50=trend[i] or 0.0,
        above_trend=bool(trend[i] and c > trend[i]),
        entry=entry, risk_per_share=risk_ps, shares=shares, risk_dollars=risk_dollars,
        targets=targets, note=note,
        closes=closes[-tail:], dates=[b.date for b in bars[-tail:]],
    )
