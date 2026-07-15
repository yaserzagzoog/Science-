"""Watchlist and strategy parameters. Edit here — everything else follows."""

WATCHLIST = [
    # symbol, display name, asset class
    ("AAPL",   "Apple",          "stock"),
    ("MSFT",   "Microsoft",      "stock"),
    ("NVDA",   "NVIDIA",         "stock"),
    ("TSLA",   "Tesla",          "stock"),
    ("AMZN",   "Amazon",         "stock"),
    ("GOOGL",  "Alphabet",       "stock"),
    ("META",   "Meta",           "stock"),
    ("AMD",    "AMD",            "stock"),
    ("SPY",    "S&P 500 ETF",    "etf"),
    ("QQQ",    "Nasdaq 100 ETF", "etf"),
    ("BTCUSD", "Bitcoin",        "crypto"),
    ("ETHUSD", "Ethereum",       "crypto"),
]

PARAMS = {
    "breakout_len": 20,   # resistance = highest high of the prior N bars
    "exit_len": 20,       # support = lowest low of the prior N bars
    "stop_len": 10,       # initial stop = lowest low of the prior N bars
    "vol_len": 20,        # volume confirmation vs its N-bar SMA
    "trend_len": 50,      # trend filter SMA
    "near_trigger_pct": 2.0,  # within this % below resistance -> WATCH
    "risk_pct": 1.0,      # % of account risked per trade
    "account_size": 10_000.0,  # default account for position sizing
    "target_r": (2.0, 3.0),    # profit targets in R multiples
}

# Stooq symbol mapping used by the self-updating data fetcher (GitHub Actions).
STOOQ_SYMBOLS = {
    "AAPL": "aapl.us", "MSFT": "msft.us", "NVDA": "nvda.us", "TSLA": "tsla.us",
    "AMZN": "amzn.us", "GOOGL": "googl.us", "META": "meta.us", "AMD": "amd.us",
    "SPY": "spy.us", "QQQ": "qqq.us", "BTCUSD": "btcusd", "ETHUSD": "ethusd",
}
