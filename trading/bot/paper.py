"""Paper-trading loop: runs a strategy against live (or simulated) prices with
virtual money and prints an execution log like the dashboard's.

Usage:
    python -m bot.paper --strategy combo --capital 1000 --steps 50

With no live connectivity it steps through simulated data one bar at a time.
No real orders are ever sent anywhere — there is no exchange API key handling
in this codebase on purpose.
"""

from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone

from .data import load
from .indicators import atr
from .risk import RiskConfig, RiskManager
from .strategy import STRATEGIES


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--strategy", default="combo", choices=list(STRATEGIES))
    p.add_argument("--capital", type=float, default=1000.0)
    p.add_argument("--symbol", default="BTCUSDT")
    p.add_argument("--interval", default="1h")
    p.add_argument("--steps", type=int, default=50, help="bars to step through")
    p.add_argument("--delay", type=float, default=0.2, help="seconds between bars")
    args = p.parse_args()

    warmup = 200
    candles, source = load(args.symbol, args.interval, warmup + args.steps)
    log(f"PAPER TRADING ({source}) | {args.symbol} {args.interval} | strategy={args.strategy}")
    log("All fills are virtual. This is a simulation.")

    risk = RiskConfig()
    rm = RiskManager(risk)
    cash, units, stop = args.capital, 0.0, 0.0
    entry_price = 0.0

    for i in range(warmup, warmup + args.steps):
        window = candles[: i + 1]
        c = window[-1]
        sig = STRATEGIES[args.strategy](window)[-1]
        a = atr([x.high for x in window], [x.low for x in window],
                [x.close for x in window], 14)[-1] or 0.0
        equity = cash + units * c.close
        rm.update_equity(equity)

        if units > 0 and c.low <= stop:
            fill = stop * (1 - risk.slippage)
            cash += units * fill * (1 - risk.fee_rate)
            log(f"STOP  sell {units:.6f} @ {fill:,.2f} | pnl {units*(fill-entry_price):+,.2f}")
            units = 0.0
        elif units > 0 and sig != 1:
            fill = c.close * (1 - risk.slippage)
            cash += units * fill * (1 - risk.fee_rate)
            log(f"EXIT  sell {units:.6f} @ {fill:,.2f} | pnl {units*(fill-entry_price):+,.2f}")
            units = 0.0
        elif units == 0 and sig == 1 and not rm.halted:
            size = rm.position_size(equity, c.close, a)
            fill = c.close * (1 + risk.slippage)
            cost = size * fill * (1 + risk.fee_rate)
            if size > 0 and cost <= cash:
                cash -= cost
                units, entry_price = size, fill
                stop = rm.stop_price(fill, a)
                log(f"ENTRY buy  {units:.6f} @ {fill:,.2f} | stop {stop:,.2f}")

        if rm.halted:
            log("KILL SWITCH: max drawdown hit, trading halted.")
            break
        if (i - warmup) % 10 == 0:
            log(f"tick  px {c.close:,.2f} | equity {equity:,.2f} | pos {units:.6f}")
        time.sleep(args.delay)

    equity = cash + units * candles[warmup + args.steps - 1].close
    ret = 100 * (equity / args.capital - 1)
    log(f"DONE  equity {equity:,.2f} ({ret:+.2f}%) over {args.steps} bars")


if __name__ == "__main__":
    main()
