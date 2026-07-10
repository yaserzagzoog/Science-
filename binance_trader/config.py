"""Configuration loading.

API keys are read ONLY from environment variables (or a local .env file that
is git-ignored). They must never be committed or shared in chat.
"""

import json
import os
from dataclasses import dataclass, field


def load_dotenv(path: str = ".env") -> None:
    """Minimal .env loader (no third-party dependency)."""
    if not os.path.exists(path):
        return
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip().strip("'\"")
            os.environ.setdefault(key, value)


@dataclass
class Config:
    # Trading universe — quote asset is derived per symbol (e.g. BTCUSDT -> USDT)
    symbols: list = field(default_factory=lambda: ["BTCUSDT", "ETHUSDT"])
    quote_asset: str = "USDT"

    # Mode: "paper" (no keys, simulated fills on live prices),
    #       "testnet" (Binance Spot testnet, fake funds),
    #       "live" (real money — only after you have validated the bot)
    mode: str = "paper"

    # Capital and risk
    paper_starting_balance: float = 1000.0   # quote units for paper mode
    max_position_fraction: float = 0.25      # max fraction of equity per position
    per_trade_risk_fraction: float = 0.01    # equity fraction risked per trade
    stop_loss_pct: float = 1.0               # % below entry to exit
    take_profit_pct: float = 1.5             # % above entry to exit
    max_open_positions: int = 2

    # Daily circuit breakers (bot halts for the rest of the UTC day)
    daily_target_pct: float = 5.0            # stop trading after this gain
    daily_max_loss_pct: float = 2.0          # stop trading after this loss

    # Strategy parameters
    kline_interval: str = "5m"
    rsi_period: int = 14
    rsi_oversold: float = 30.0
    rsi_overbought: float = 70.0
    ema_fast: int = 9
    ema_slow: int = 21

    # Loop timing
    poll_seconds: int = 30

    # State/kill-switch files
    state_file: str = "bot_state.json"
    kill_switch_file: str = "STOP"

    api_key: str = ""
    api_secret: str = ""

    @classmethod
    def load(cls, path: str = "config.json") -> "Config":
        load_dotenv()
        cfg = cls()
        if os.path.exists(path):
            with open(path) as fh:
                data = json.load(fh)
            for key, value in data.items():
                if hasattr(cfg, key) and key not in ("api_key", "api_secret"):
                    setattr(cfg, key, value)
        cfg.api_key = os.environ.get("BINANCE_API_KEY", "")
        cfg.api_secret = os.environ.get("BINANCE_API_SECRET", "")
        cfg.validate()
        return cfg

    def validate(self) -> None:
        if self.mode not in ("paper", "testnet", "live"):
            raise ValueError(f"mode must be paper/testnet/live, got {self.mode!r}")
        if self.mode in ("testnet", "live") and not (self.api_key and self.api_secret):
            raise ValueError(
                f"mode={self.mode!r} requires BINANCE_API_KEY and BINANCE_API_SECRET "
                "environment variables (put them in a local .env file)."
            )
        if not self.symbols:
            raise ValueError("symbols list is empty")
        if self.stop_loss_pct <= 0 or self.take_profit_pct <= 0:
            raise ValueError("stop_loss_pct and take_profit_pct must be positive")
        if self.daily_max_loss_pct <= 0:
            raise ValueError("daily_max_loss_pct must be positive")
