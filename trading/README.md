# Gravia-Style Trading Bot — an honest reconstruction

This project was inspired by a viral post claiming a 19-year-old in Japan built a
"Claude Code trading bot" that turned **$68 into $750,000**. Before using anything
here, read the analysis below — it matters more than the code.

## The trading analysis: why that claim is not real

1. **The dashboard in the viral video literally says `SIMULATED`** — it is visible
   in the order-book panel. It is a demo UI running on virtual money, exactly like
   the dashboard in this repo.
2. **Even the post spreading it admits there is "no strong independent evidence"**
   for the profit number or the trading results. No exchange statements, no
   on-chain proof, no audited track record.
3. **The math doesn't work.** $68 → $750,000 is an ~11,000× return. The claimed
   edge was "price mismatches across 50 markets" (arbitrage). Real cross-exchange
   arbitrage spreads are typically 0.05–0.3%, while taker fees alone are ~0.1%
   *per side*, plus slippage, plus minutes-to-hours of transfer latency during
   which the spread closes. With $68 of capital, minimum order sizes and fees eat
   the entire edge. Firms that actually do this run co-located servers, market-maker
   fee tiers, and millions in inventory pre-positioned on every venue — and they
   compete the spread down to nearly nothing.
4. **Survivorship + fabrication drive viral finance content.** If a claim like
   this were real and repeatable, publishing it would destroy the edge. The story
   exists to farm engagement.

**Realistic expectations:** good retail systematic strategies fight for
10–30% *annual* returns with real drawdowns, and most backtested strategies fail
live due to overfitting, fees, and regime change. Anyone promising more than that
without audited evidence is selling something.

## What this repo gives you instead (the "better" part)

A complete, transparent research stack — the thing the viral video pretends to be:

```
trading/
├── bot/
│   ├── data.py        # Binance public API fetch + regime-switching synthetic fallback
│   ├── indicators.py  # SMA, EMA, RSI, ATR (pure Python, no dependencies)
│   ├── strategy.py    # EMA cross, RSI mean-reversion, Donchian breakout, trend combo
│   ├── risk.py        # ATR position sizing, stops, max-drawdown kill switch
│   ├── backtest.py    # event-driven backtester: fees, slippage, no look-ahead bias
│   └── paper.py       # paper-trading loop with an execution log (virtual fills only)
└── dashboard/
    └── index.html     # Gravia-style live dashboard (candles, equity, trade log)
```

Things it does that the viral dashboards don't show you:

- **Fees and slippage on every fill** (0.1% + 5 bps by default) — the silent killers.
- **No look-ahead bias**: signals computed on bar *i* execute at bar *i+1*'s open.
- **Risk management**: each trade risks 1% of equity, ATR-based stops, and a hard
  kill switch that halts trading at 25% drawdown.
- **A buy-and-hold benchmark** printed next to every run — if your strategy doesn't
  beat holding, the strategy is the problem.

## Usage

Requires only Python 3.10+ (standard library only).

```bash
cd trading

# Compare all strategies against buy & hold, export dashboard data
python -m bot.backtest --all --capital 1000 --limit 3000 --export

# Single strategy
python -m bot.backtest --strategy breakout --capital 1000

# Paper-trade bar by bar with a live execution log (virtual money)
python -m bot.paper --strategy combo --steps 100

# View the dashboard
python -m http.server 8000 --directory dashboard   # then open http://localhost:8000
```

With internet access the data layer pulls real BTCUSDT candles from Binance's
public API; offline it falls back to a regime-switching synthetic market
(trends, chop, and crashes) so strategies can't win by accident on easy data.

## Sample output

```
strategy          return%  maxDD%  sharpe  trades   win%     PF
---------------------------------------------------------------
ema_cross           25.88   10.72    3.06      40   25.0   1.96
rsi_reversion       -1.54    3.12   -0.98      18   61.1   0.79
breakout            31.53    8.13     3.7      21   38.1   3.34
combo                14.3    7.99    2.53      68   35.3   1.62
buy_and_hold       139.69   32.49    3.06       -      -      -
```

Note the honest lesson in that table: **buy-and-hold beat every strategy on this
run.** That's the norm. A dashboard that never shows you the benchmark is hiding it.

## If you want to go further (in order)

1. Walk-forward validation (train/test splits over rolling windows) to detect overfitting.
2. Parameter-sensitivity analysis — a strategy that only works at `fast=12, slow=48` is noise.
3. Multiple assets and regime detection.
4. Only after months of consistent paper results, tiny live size you can afford to lose entirely.

## Disclaimer

This is research and educational software. Nothing here is financial advice, no
strategy here is claimed to be profitable, and the code deliberately contains no
exchange API-key handling — it cannot place real orders. Trading cryptocurrencies
can lose all of your capital.
