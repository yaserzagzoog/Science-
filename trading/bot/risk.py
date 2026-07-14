"""Risk management: position sizing, stops, and a drawdown kill switch.

This is the part every viral "turned $68 into $750k" post skips, and the part
that decides whether an account survives.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskConfig:
    risk_per_trade: float = 0.01      # fraction of equity risked per trade
    atr_stop_mult: float = 2.5        # stop distance in ATRs
    max_position_frac: float = 0.5    # never put more than this fraction of equity in one position
    max_drawdown: float = 0.25        # kill switch: stop trading past this peak-to-trough loss
    fee_rate: float = 0.001           # taker fee per side (0.1%, Binance default)
    slippage: float = 0.0005          # 5 bps assumed slippage per fill


class RiskManager:
    def __init__(self, cfg: RiskConfig):
        self.cfg = cfg
        self.peak_equity = 0.0
        self.halted = False

    def update_equity(self, equity: float) -> None:
        self.peak_equity = max(self.peak_equity, equity)
        if self.peak_equity > 0:
            dd = 1 - equity / self.peak_equity
            if dd >= self.cfg.max_drawdown:
                self.halted = True

    def position_size(self, equity: float, price: float, atr_value: float) -> float:
        """Units to buy so that a stop-out loses ~risk_per_trade of equity."""
        if self.halted or atr_value <= 0 or price <= 0:
            return 0.0
        stop_dist = self.cfg.atr_stop_mult * atr_value
        units = (equity * self.cfg.risk_per_trade) / stop_dist
        max_units = (equity * self.cfg.max_position_frac) / price
        return min(units, max_units)

    def stop_price(self, entry: float, atr_value: float) -> float:
        return entry - self.cfg.atr_stop_mult * atr_value
