"""Risk management: position sizing, stop-loss/take-profit, daily circuit breakers.

The bot halts for the rest of the UTC day when either the daily target
gain or the daily maximum loss is reached. State survives restarts via a
JSON file so the breakers cannot be bypassed by rebooting the bot.
"""

import json
import os
from datetime import datetime, timezone


def utc_today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


class RiskManager:
    def __init__(self, cfg):
        self.cfg = cfg
        self.state = {
            "day": utc_today(),
            "day_start_equity": None,
            "realized_pnl": 0.0,
            "halted": False,
            "halt_reason": "",
            "positions": {},   # symbol -> {qty, entry_price}
        }
        self._load()

    # ------------------------------------------------------------- persistence

    def _load(self):
        if os.path.exists(self.cfg.state_file):
            try:
                with open(self.cfg.state_file) as fh:
                    saved = json.load(fh)
                if saved.get("day") == utc_today():
                    self.state.update(saved)
                else:
                    # new UTC day: keep positions, reset counters
                    self.state["positions"] = saved.get("positions", {})
            except (json.JSONDecodeError, OSError):
                pass

    def save(self):
        with open(self.cfg.state_file, "w") as fh:
            json.dump(self.state, fh, indent=2)

    # ---------------------------------------------------------------- breakers

    def roll_day_if_needed(self, equity: float):
        if self.state["day"] != utc_today():
            self.state.update(
                day=utc_today(),
                day_start_equity=equity,
                realized_pnl=0.0,
                halted=False,
                halt_reason="",
            )
            self.save()
        elif self.state["day_start_equity"] is None:
            self.state["day_start_equity"] = equity
            self.save()

    def check_breakers(self, equity: float) -> str:
        """Return halt reason ('' if trading is allowed)."""
        if os.path.exists(self.cfg.kill_switch_file):
            return f"kill switch file {self.cfg.kill_switch_file!r} present"
        if self.state["halted"]:
            return self.state["halt_reason"]
        start = self.state["day_start_equity"]
        if not start:
            return ""
        change_pct = (equity - start) / start * 100
        if change_pct >= self.cfg.daily_target_pct:
            self._halt(f"daily target reached: {change_pct:+.2f}%")
        elif change_pct <= -self.cfg.daily_max_loss_pct:
            self._halt(f"daily max loss reached: {change_pct:+.2f}%")
        return self.state["halt_reason"]

    def _halt(self, reason: str):
        self.state["halted"] = True
        self.state["halt_reason"] = reason
        self.save()

    # ---------------------------------------------------------------- sizing

    def position_size(self, equity: float, price: float) -> float:
        """Quantity sized so the stop-loss risks per_trade_risk_fraction of equity,
        capped at max_position_fraction of equity."""
        risk_amount = equity * self.cfg.per_trade_risk_fraction
        stop_distance = price * self.cfg.stop_loss_pct / 100
        qty_by_risk = risk_amount / stop_distance if stop_distance > 0 else 0
        qty_by_cap = equity * self.cfg.max_position_fraction / price
        return max(0.0, min(qty_by_risk, qty_by_cap))

    # -------------------------------------------------------------- positions

    def can_open(self) -> bool:
        return len(self.state["positions"]) < self.cfg.max_open_positions

    def open_position(self, symbol: str, qty: float, price: float):
        self.state["positions"][symbol] = {"qty": qty, "entry_price": price}
        self.save()

    def close_position(self, symbol: str, exit_price: float) -> float:
        pos = self.state["positions"].pop(symbol, None)
        if not pos:
            return 0.0
        pnl = (exit_price - pos["entry_price"]) * pos["qty"]
        self.state["realized_pnl"] += pnl
        self.save()
        return pnl

    def get_position(self, symbol: str):
        return self.state["positions"].get(symbol)

    def stop_or_target_hit(self, symbol: str, price: float) -> str:
        """Return exit reason if stop-loss or take-profit is hit, else ''."""
        pos = self.get_position(symbol)
        if not pos:
            return ""
        entry = pos["entry_price"]
        change_pct = (price - entry) / entry * 100
        if change_pct <= -self.cfg.stop_loss_pct:
            return f"stop-loss hit ({change_pct:+.2f}%)"
        if change_pct >= self.cfg.take_profit_pct:
            return f"take-profit hit ({change_pct:+.2f}%)"
        return ""
