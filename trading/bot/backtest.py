"""Event-driven backtester (long/flat) with fees, slippage, ATR stops, and metrics.

Usage:
    python -m bot.backtest --strategy combo --capital 1000 --limit 2000
    python -m bot.backtest --all            # compare all strategies vs buy & hold

Writes trading/dashboard/data.json for the dashboard when --export is passed.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from dataclasses import dataclass, field

from .data import Candle, load
from .indicators import atr
from .risk import RiskConfig, RiskManager
from .strategy import STRATEGIES


@dataclass
class Trade:
    entry_ts: int
    entry_price: float
    units: float
    exit_ts: int = 0
    exit_price: float = 0.0
    pnl: float = 0.0
    reason: str = ""


@dataclass
class Result:
    strategy: str
    source: str
    initial_capital: float
    equity_curve: list[float] = field(default_factory=list)
    timestamps: list[int] = field(default_factory=list)
    trades: list[Trade] = field(default_factory=list)
    halted: bool = False

    @property
    def final_equity(self) -> float:
        return self.equity_curve[-1] if self.equity_curve else self.initial_capital

    def metrics(self) -> dict:
        eq = self.equity_curve
        total_return = self.final_equity / self.initial_capital - 1
        peak, max_dd = 0.0, 0.0
        for v in eq:
            peak = max(peak, v)
            max_dd = max(max_dd, 1 - v / peak)
        rets = [eq[i] / eq[i - 1] - 1 for i in range(1, len(eq))]
        mean = sum(rets) / len(rets) if rets else 0.0
        var = sum((r - mean) ** 2 for r in rets) / len(rets) if rets else 0.0
        # hourly bars -> annualize with sqrt(24*365)
        sharpe = (mean / math.sqrt(var)) * math.sqrt(24 * 365) if var > 0 else 0.0
        closed = [t for t in self.trades if t.exit_ts]
        wins = [t for t in closed if t.pnl > 0]
        losses = [t for t in closed if t.pnl <= 0]
        gross_win = sum(t.pnl for t in wins)
        gross_loss = -sum(t.pnl for t in losses)
        return {
            "total_return_pct": round(100 * total_return, 2),
            "final_equity": round(self.final_equity, 2),
            "max_drawdown_pct": round(100 * max_dd, 2),
            "sharpe": round(sharpe, 2),
            "trades": len(closed),
            "win_rate_pct": round(100 * len(wins) / len(closed), 1) if closed else 0.0,
            "profit_factor": round(gross_win / gross_loss, 2) if gross_loss > 0 else float("inf"),
            "halted_by_kill_switch": self.halted,
        }


def run_backtest(candles: list[Candle], strategy_name: str, source: str,
                 capital: float = 1000.0, risk: RiskConfig | None = None) -> Result:
    risk = risk or RiskConfig()
    signals = STRATEGIES[strategy_name](candles)
    atrs = atr([c.high for c in candles], [c.low for c in candles],
               [c.close for c in candles], 14)
    rm = RiskManager(risk)
    res = Result(strategy=strategy_name, source=source, initial_capital=capital)

    cash, units = capital, 0.0
    open_trade: Trade | None = None
    stop = 0.0

    for i, c in enumerate(candles[:-1]):
        # signals[i] is acted on at the NEXT bar's open: no look-ahead bias.
        nxt = candles[i + 1]
        equity = cash + units * c.close
        rm.update_equity(equity)

        want_long = signals[i] == 1 and not rm.halted
        stopped = units > 0 and nxt.low <= stop

        if units > 0 and (stopped or not want_long):
            fill = stop if stopped else nxt.open
            fill *= (1 - risk.slippage)
            proceeds = units * fill * (1 - risk.fee_rate)
            assert open_trade is not None
            open_trade.exit_ts = nxt.ts
            open_trade.exit_price = fill
            open_trade.pnl = proceeds - open_trade.units * open_trade.entry_price
            open_trade.reason = "stop" if stopped else "signal"
            res.trades.append(open_trade)
            cash += proceeds
            units, open_trade = 0.0, None
        elif units == 0 and want_long and atrs[i]:
            size = rm.position_size(equity, nxt.open, atrs[i])
            fill = nxt.open * (1 + risk.slippage)
            cost = size * fill * (1 + risk.fee_rate)
            if size > 0 and cost <= cash:
                cash -= cost
                units = size
                stop = rm.stop_price(fill, atrs[i])
                open_trade = Trade(entry_ts=nxt.ts, entry_price=fill, units=size)

        res.equity_curve.append(cash + units * nxt.close)
        res.timestamps.append(nxt.ts)

    res.halted = rm.halted
    return res


def buy_and_hold(candles: list[Candle], source: str, capital: float = 1000.0) -> Result:
    res = Result(strategy="buy_and_hold", source=source, initial_capital=capital)
    units = capital / candles[0].open
    for c in candles[1:]:
        res.equity_curve.append(units * c.close)
        res.timestamps.append(c.ts)
    return res


def export_dashboard(result: Result, candles: list[Candle], path: str) -> None:
    payload = {
        "meta": {"strategy": result.strategy, "source": result.source,
                 "simulated": True, "metrics": result.metrics()},
        "candles": [[c.ts, c.open, c.high, c.low, c.close, round(c.volume, 2)]
                    for c in candles],
        "equity": [[t, round(e, 2)] for t, e in
                   zip(result.timestamps, result.equity_curve)],
        "trades": [{"entry_ts": t.entry_ts, "entry": round(t.entry_price, 2),
                    "exit_ts": t.exit_ts, "exit": round(t.exit_price, 2),
                    "units": round(t.units, 6), "pnl": round(t.pnl, 2),
                    "reason": t.reason} for t in result.trades],
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(payload, f)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--strategy", default="combo", choices=list(STRATEGIES))
    p.add_argument("--all", action="store_true", help="compare all strategies")
    p.add_argument("--capital", type=float, default=1000.0)
    p.add_argument("--symbol", default="BTCUSDT")
    p.add_argument("--interval", default="1h")
    p.add_argument("--limit", type=int, default=2000)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--export", action="store_true",
                   help="write dashboard/data.json for the dashboard")
    args = p.parse_args()

    candles, source = load(args.symbol, args.interval, args.limit, seed=args.seed)
    print(f"Data: {len(candles)} candles from {source}\n")

    names = list(STRATEGIES) if args.all else [args.strategy]
    header = f"{'strategy':<16}{'return%':>9}{'maxDD%':>8}{'sharpe':>8}{'trades':>8}{'win%':>7}{'PF':>7}"
    print(header)
    print("-" * len(header))
    best: Result | None = None
    for name in names:
        r = run_backtest(candles, name, source, capital=args.capital)
        m = r.metrics()
        print(f"{name:<16}{m['total_return_pct']:>9}{m['max_drawdown_pct']:>8}"
              f"{m['sharpe']:>8}{m['trades']:>8}{m['win_rate_pct']:>7}{m['profit_factor']:>7}")
        if best is None or r.final_equity > best.final_equity:
            best = r
    bh = buy_and_hold(candles, source, capital=args.capital)
    mb = bh.metrics()
    print(f"{'buy_and_hold':<16}{mb['total_return_pct']:>9}{mb['max_drawdown_pct']:>8}"
          f"{mb['sharpe']:>8}{'-':>8}{'-':>7}{'-':>7}")

    if args.export and best is not None:
        out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "dashboard", "data.json")
        export_dashboard(best, candles, out)
        print(f"\nExported best run ({best.strategy}) -> {out}")


if __name__ == "__main__":
    main()
