"""Minimal event-driven backtest of the Fable Rules on one symbol.

Mirrors the Pine Script semantics: a signal on bar N fills at bar N+1's open;
the stop is checked intrabar. Indicative only — no fees, slippage, or dividends."""

from dataclasses import dataclass

from .config import PARAMS
from .data import Bar
from .indicators import rolling_max, rolling_min, sma


@dataclass
class Stats:
    trades: int
    wins: int
    win_rate: float
    total_return_pct: float   # compounded, fully-invested-per-trade
    avg_r: float
    max_drawdown_pct: float
    profit_factor: float
    in_position: bool
    last_entry: float | None


def run(bars: list[Bar], params: dict | None = None) -> Stats | None:
    p = dict(PARAMS)
    if params:
        p.update(params)
    n = len(bars)
    warmup = max(p["breakout_len"], p["exit_len"], p["vol_len"]) + 1
    if n < warmup + 10:
        return None

    closes = [b.close for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    vols = [b.volume for b in bars]
    res = rolling_max(highs, p["breakout_len"])
    sup = rolling_min(lows, p["exit_len"])
    stop_line = rolling_min(lows, p["stop_len"])
    vol_sma = sma(vols, p["vol_len"])

    equity, peak, max_dd = 1.0, 1.0, 0.0
    trades, wins, rs = 0, 0, []
    gross_win, gross_loss = 0.0, 0.0
    pos_entry, pos_stop = None, None
    pending_entry = False   # signal fired yesterday -> fill at today's open
    pending_exit = False

    for i in range(warmup, n):
        o, h, l, c = bars[i].open, highs[i], lows[i], closes[i]

        if pos_entry is None and pending_entry:
            pos_entry, pos_stop = o, stop_line[i - 1]
            trades += 1
        pending_entry = False

        if pos_entry is not None:
            exit_px = None
            if pending_exit:
                exit_px = o
            elif pos_stop is not None and l <= pos_stop:
                exit_px = min(pos_stop, o)  # gap through the stop fills at open
            pending_exit = False
            if exit_px is not None:
                ret = exit_px / pos_entry - 1.0
                risk = (pos_entry - pos_stop) / pos_entry if pos_stop else 0.0
                rs.append(ret / risk if risk > 0 else 0.0)
                if ret > 0:
                    wins += 1
                    gross_win += ret
                else:
                    gross_loss += -ret
                equity *= 1.0 + ret
                peak = max(peak, equity)
                max_dd = max(max_dd, 1.0 - equity / peak)
                pos_entry, pos_stop = None, None

        crossed_up = c > res[i] and closes[i - 1] <= res[i - 1]
        vol_ok = vol_sma[i] and vols[i] > vol_sma[i]
        crossed_down = c < sup[i] and closes[i - 1] >= sup[i - 1]
        if pos_entry is None:
            if crossed_up and vol_ok:
                pending_entry = True
        else:
            if crossed_down:
                pending_exit = True
            # mark-to-market drawdown while holding
            eq_now = equity * (c / pos_entry)
            peak = max(peak, eq_now)
            max_dd = max(max_dd, 1.0 - eq_now / peak)

    closed = len(rs)
    return Stats(
        trades=trades,
        wins=wins,
        win_rate=(wins / closed * 100.0) if closed else 0.0,
        total_return_pct=(equity - 1.0) * 100.0,
        avg_r=(sum(rs) / closed) if closed else 0.0,
        max_drawdown_pct=max_dd * 100.0,
        profit_factor=(gross_win / gross_loss) if gross_loss > 0 else (999.0 if gross_win > 0 else 0.0),
        in_position=pos_entry is not None,
        last_entry=pos_entry,
    )
