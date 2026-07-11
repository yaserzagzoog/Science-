#!/usr/bin/env python3
"""Backtest the EXACT live strategy + risk logic over historical candles.

    python3 backtest.py [config.json] [--days 90]
    python3 backtest.py config.forex.json --days 60

Uses the same Strategy and RiskManager code the live bot runs, plus
fees/slippage from the config, so results are as honest as a candle-level
simulation can be. Remaining optimism to keep in mind: intrabar fills are
approximated (stop-loss assumed to fill at the stop price; in violent moves
real fills are worse) and 5m candles hide intra-candle sequencing.
"""

import statistics
import sys
import time
from datetime import datetime, timezone

from trader.bot import make_client
from trader.config import Config
from trader.risk import RiskManager
from trader.strategy import Strategy

INTERVAL_MS = {
    "1m": 60_000, "5m": 300_000, "15m": 900_000, "30m": 1_800_000,
    "1h": 3_600_000, "4h": 14_400_000, "1d": 86_400_000,
}


def fetch_history(client, symbol, interval, days):
    """Paginate klines_full from `days` ago to now."""
    step = INTERVAL_MS[interval]
    start = int(time.time() * 1000) - days * 86_400_000
    out = []
    while True:
        batch = client.klines_full(symbol, interval, start_ms=start)
        if not batch:
            break
        # guard against overlap/stall
        if out and batch[-1]["t"] <= out[-1]["t"]:
            break
        out.extend(c for c in batch if not out or c["t"] > out[-1]["t"])
        start = out[-1]["t"] + step
        if start > int(time.time() * 1000) - step:
            break
        time.sleep(0.2)   # be polite to the API
    return out


def day_of(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


class Backtester:
    def __init__(self, cfg: Config, history: dict):
        """history: symbol -> list of {t, o, h, l, c} candles."""
        cfg.state_file = ""            # in-memory risk state
        self.cfg = cfg
        self.history = history
        self.sim_day = ""
        self.risk = RiskManager(cfg, today_fn=lambda: self.sim_day)
        self.strategy = Strategy(cfg)
        self.cash = cfg.paper_starting_balance
        self.cost_frac = (cfg.fee_pct + cfg.slippage_pct) / 100
        self.trades = []               # closed trades
        self.daily = {}                # day -> {start, end, halt}
        self.equity_curve = []

    # ------------------------------------------------------------- accounting

    def _buy(self, symbol, qty, price, ts):
        self.cash -= qty * price * (1 + self.cost_frac)
        self.risk.open_position(symbol, qty, price)
        self.risk.state["positions"][symbol]["entry_t"] = ts

    def _sell(self, symbol, price, ts, reason):
        pos = self.risk.get_position(symbol)
        if not pos:
            return
        self.cash += pos["qty"] * price * (1 - self.cost_frac)
        entry_cost = pos["entry_price"] * (1 + self.cost_frac)
        exit_net = price * (1 - self.cost_frac)
        pnl = (exit_net - entry_cost) * pos["qty"]
        self.trades.append({
            "symbol": symbol, "entry_t": pos.get("entry_t"), "exit_t": ts,
            "entry": pos["entry_price"], "exit": price,
            "qty": pos["qty"], "pnl": pnl, "reason": reason,
        })
        self.risk.close_position(symbol, price)

    def equity(self, prices):
        total = self.cash
        for symbol, pos in self.risk.state["positions"].items():
            total += pos["qty"] * prices.get(symbol, pos["entry_price"])
        return total

    # ------------------------------------------------------------- simulation

    def run(self):
        cfg = self.cfg
        # merged timeline of all candle open times
        timeline = sorted({c["t"] for candles in self.history.values() for c in candles})
        by_ts = {
            symbol: {c["t"]: c for c in candles}
            for symbol, candles in self.history.items()
        }
        closes = {symbol: [] for symbol in self.history}

        for ts in timeline:
            self.sim_day = day_of(ts)
            candles_now = {
                s: by_ts[s][ts] for s in self.history if ts in by_ts[s]
            }
            prices = {s: c["c"] for s, c in candles_now.items()}
            for s, c in candles_now.items():
                closes[s].append(c["c"])

            # 1. intrabar stop-loss / take-profit (stop assumed first: worst case)
            for s, c in candles_now.items():
                pos = self.risk.get_position(s)
                if not pos:
                    continue
                stop_px = pos["entry_price"] * (1 - cfg.stop_loss_pct / 100)
                tp_px = pos["entry_price"] * (1 + cfg.take_profit_pct / 100)
                if c["l"] <= stop_px:
                    self._sell(s, stop_px, ts, "stop-loss")
                elif c["h"] >= tp_px:
                    self._sell(s, tp_px, ts, "take-profit")

            # 2. daily accounting + circuit breakers
            eq = self.equity(prices)
            self.risk.roll_day_if_needed(eq)
            day = self.daily.setdefault(
                self.sim_day,
                {"start": self.risk.state["day_start_equity"] or eq, "end": eq, "halt": ""},
            )
            halt = self.risk.check_breakers(eq)
            if halt:
                for s in list(self.risk.state["positions"]):
                    if s in prices:
                        self._sell(s, prices[s], ts, "daily halt")
                day["halt"] = halt
                day["end"] = self.equity(prices)
                self.equity_curve.append((ts, day["end"]))
                continue

            # 3. strategy signals at candle close
            for s, c in candles_now.items():
                holding = self.risk.get_position(s) is not None
                signal = self.strategy.evaluate(closes[s], holding)
                if signal.action == "BUY" and not holding and self.risk.can_open():
                    qty = self.risk.position_size(eq, c["c"])
                    if qty * c["c"] >= 10:     # skip dust
                        self._buy(s, qty, c["c"], ts)
                elif signal.action == "SELL" and holding:
                    self._sell(s, c["c"], ts, signal.reason)

            day["end"] = self.equity(prices)
            self.equity_curve.append((ts, day["end"]))

        # liquidate leftovers at final close for a clean final number
        last_prices = {s: candles[-1]["c"] for s, candles in self.history.items()}
        for s in list(self.risk.state["positions"]):
            self._sell(s, last_prices[s], timeline[-1], "end of backtest")
        if self.daily:
            self.daily[max(self.daily)]["end"] = self.equity(last_prices)

    # ------------------------------------------------------------------ report

    def report(self):
        cfg = self.cfg
        start_bal = cfg.paper_starting_balance
        final = self.equity_curve[-1][1] if self.equity_curve else start_bal
        days = [
            (d, (v["end"] - v["start"]) / v["start"] * 100, v["halt"])
            for d, v in sorted(self.daily.items())
        ]
        day_pcts = [p for _, p, _ in days]
        n_days = len(days)
        total_pct = (final / start_bal - 1) * 100

        wins = [t for t in self.trades if t["pnl"] > 0]
        losses = [t for t in self.trades if t["pnl"] <= 0]

        peak, max_dd = -1e18, 0.0
        for _, eq in self.equity_curve:
            peak = max(peak, eq)
            max_dd = max(max_dd, (peak - eq) / peak * 100)

        print("=" * 64)
        print(f"BACKTEST  platform={cfg.platform}  symbols={','.join(cfg.symbols)}")
        print(f"period: {days[0][0]} .. {days[-1][0]}  ({n_days} trading days)")
        print(f"costs modeled: {cfg.fee_pct}% fee + {cfg.slippage_pct}% slippage per side")
        print("=" * 64)
        print(f"final equity:      {final:.2f} (started {start_bal:.2f})")
        print(f"total return:      {total_pct:+.2f}%")
        if n_days >= 2:
            monthly = ((final / start_bal) ** (30 / n_days) - 1) * 100
            print(f"compounded ~30d:   {monthly:+.2f}%")
        for s, candles in self.history.items():
            bh = (candles[-1]["c"] / candles[0]["c"] - 1) * 100
            print(f"buy&hold {s}: {bh:+.2f}%")
        print(f"max drawdown:      {max_dd:.2f}%")
        print("-" * 64)
        print(f"trades: {len(self.trades)}  |  win rate: "
              f"{len(wins) / len(self.trades) * 100 if self.trades else 0:.1f}%")
        if wins:
            print(f"avg win:  {statistics.mean(t['pnl'] for t in wins):+.2f}")
        if losses:
            print(f"avg loss: {statistics.mean(t['pnl'] for t in losses):+.2f}")
        if day_pcts:
            print("-" * 64)
            print(f"daily P&L: mean {statistics.mean(day_pcts):+.2f}%  "
                  f"median {statistics.median(day_pcts):+.2f}%  "
                  f"best {max(day_pcts):+.2f}%  worst {min(day_pcts):+.2f}%")
            print(f"positive days: {sum(1 for p in day_pcts if p > 0)}/{n_days}")
            locks = sum(1 for _, _, h in days if "locked" in h)
            targets = sum(1 for _, _, h in days if "target" in h)
            stops = sum(1 for _, _, h in days if "max loss" in h)
            print(f"days halted: +{cfg.daily_target_pct}% target x{targets}, "
                  f"profit-lock x{locks}, -{cfg.daily_max_loss_pct}% stop x{stops}")
        print("=" * 64)


def main():
    args = [a for a in sys.argv[1:]]
    days = 90
    if "--days" in args:
        i = args.index("--days")
        days = int(args[i + 1])
        del args[i:i + 2]
    config_path = args[0] if args else "config.json"

    cfg = Config.load(config_path)
    client = make_client(cfg)
    history = {}
    for symbol in cfg.symbols:
        print(f"fetching {days}d of {cfg.kline_interval} candles for {symbol}...")
        history[symbol] = fetch_history(client, symbol, cfg.kline_interval, days)
        print(f"  {len(history[symbol])} candles")

    bt = Backtester(cfg, history)
    bt.run()
    bt.report()


if __name__ == "__main__":
    main()
