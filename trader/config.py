"""Configuration loading.

API credentials are read ONLY from environment variables (or a local .env
file that is git-ignored). They must never be committed or shared in chat.
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
    # Platform: "binance" (crypto spot) or "oanda" (forex)
    platform: str = "binance"

    # Trading universe.
    #   binance: spot pairs like "BTCUSDT"
    #   oanda:   instruments like "EUR_USD"
    symbols: list = field(default_factory=lambda: ["BTCUSDT", "ETHUSDT"])
    quote_asset: str = "USDT"   # binance only

    # Mode: "paper"   - simulated fills on real market data
    #       "testnet" - real orders, fake funds (Binance testnet / OANDA practice)
    #       "live"    - real money. Only after validating on paper/testnet.
    mode: str = "paper"

    # Capital and risk
    paper_starting_balance: float = 1000.0
    max_position_fraction: float = 0.25      # max fraction of equity per position
    per_trade_risk_fraction: float = 0.01    # equity fraction risked per trade
    stop_loss_pct: float = 1.0               # % below entry to exit
    take_profit_pct: float = 1.5             # % above entry to exit
    max_open_positions: int = 2

    # Daily P&L management (all % of day-start equity, UTC day):
    #   daily_target_pct   - hard stop: quit for the day at this gain
    #   daily_min_lock_pct - once day P&L touches this, a profit floor activates
    #   daily_giveback_pct - the floor trails this far below the day's peak
    #                        (but never below daily_min_lock_pct)
    #   daily_max_loss_pct - hard stop on the downside
    daily_target_pct: float = 5.0
    daily_min_lock_pct: float = 2.0
    daily_giveback_pct: float = 1.0
    daily_max_loss_pct: float = 2.0

    # Trading costs, % of notional per side — applied in paper mode and
    # backtests so simulated results aren't flattered. (Binance spot taker
    # fee is 0.1%; OANDA's cost is the spread, modeled via slippage_pct.)
    fee_pct: float = 0.1
    slippage_pct: float = 0.05

    # Strategy: "scalp" (RSI/EMA on short candles) or
    #           "swing" (daily momentum + market regime filter — modeled on
    #           Sindbad.Tech's acceleration model + safeguard signal)
    strategy: str = "scalp"

    # Swing parameters (daily candles: set kline_interval to "1d")
    regime_symbol: str = "BTCUSDT"   # market proxy for the regime filter
    regime_ema_days: int = 50        # regime is UP when proxy closes above this EMA
    mom_fast_days: int = 7           # ~weekly momentum horizon
    mom_slow_days: int = 30

    # Scalp strategy parameters
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

    # Credentials (from environment only)
    api_key: str = ""
    api_secret: str = ""
    oanda_token: str = ""
    oanda_account_id: str = ""

    @classmethod
    def load(cls, path: str = "config.json") -> "Config":
        load_dotenv()
        cfg = cls()
        if os.path.exists(path):
            with open(path) as fh:
                data = json.load(fh)
            for key, value in data.items():
                if hasattr(cfg, key) and key not in (
                    "api_key", "api_secret", "oanda_token", "oanda_account_id"
                ):
                    setattr(cfg, key, value)
        cfg.api_key = os.environ.get("BINANCE_API_KEY", "")
        cfg.api_secret = os.environ.get("BINANCE_API_SECRET", "")
        cfg.oanda_token = os.environ.get("OANDA_API_TOKEN", "")
        cfg.oanda_account_id = os.environ.get("OANDA_ACCOUNT_ID", "")
        cfg.validate()
        return cfg

    def validate(self) -> None:
        if self.platform not in ("binance", "oanda"):
            raise ValueError(f"platform must be binance/oanda, got {self.platform!r}")
        if self.mode not in ("paper", "testnet", "live"):
            raise ValueError(f"mode must be paper/testnet/live, got {self.mode!r}")
        if self.platform == "binance" and self.mode in ("testnet", "live"):
            if not (self.api_key and self.api_secret):
                raise ValueError(
                    f"binance mode={self.mode!r} requires BINANCE_API_KEY and "
                    "BINANCE_API_SECRET environment variables (put them in .env)."
                )
        if self.platform == "oanda":
            # OANDA needs a token even for market data; practice tokens are free.
            if not (self.oanda_token and self.oanda_account_id):
                raise ValueError(
                    "oanda platform requires OANDA_API_TOKEN and OANDA_ACCOUNT_ID "
                    "environment variables (free practice account: "
                    "https://www.oanda.com -> demo account -> Manage API Access)."
                )
        if not self.symbols:
            raise ValueError("symbols list is empty")
        if self.stop_loss_pct <= 0 or self.take_profit_pct <= 0:
            raise ValueError("stop_loss_pct and take_profit_pct must be positive")
        if self.daily_max_loss_pct <= 0:
            raise ValueError("daily_max_loss_pct must be positive")
        if not (0 < self.daily_min_lock_pct <= self.daily_target_pct):
            raise ValueError(
                "daily_min_lock_pct must be positive and <= daily_target_pct"
            )
        if self.daily_giveback_pct <= 0:
            raise ValueError("daily_giveback_pct must be positive")
        if self.strategy not in ("scalp", "swing"):
            raise ValueError(f"strategy must be scalp/swing, got {self.strategy!r}")
        if self.strategy == "swing" and self.kline_interval not in ("4h", "1d"):
            raise ValueError(
                "swing strategy is designed for kline_interval '1d' (or '4h')"
            )
