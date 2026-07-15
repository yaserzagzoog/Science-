# Fable Rules — AI trading analysis system

Describe the idea → the rules are defined → the rules become code → the code
runs daily and pushes where the entry points are. Modeled on the
*Claude Fable × TradingView* system blueprint.

> **Human review required.** Everything here is research tooling on end-of-day
> data — not financial advice. Verify every level on your own chart before
> placing an order. Responsibility is yours.

## The strategy specification

| Rule | Definition |
|---|---|
| **Entry** | Price closes above the 20-day resistance with volume above its 20-day average |
| **Exit** | Close below the 20-day support, or opposite signal |
| **Stop loss** | Below breakout level / structure (the 10-day low) |
| **Position size** | Risk 1% of the account per trade |
| **Timeframe** | Daily |

## What's in here

```
tradebot/            The strategy engine (pure Python, no dependencies)
  config.py          Watchlist + parameters — edit this
  data.py            CSV cache + free Stooq refresh
  strategy.py        The Fable Rules -> daily Signal per symbol
  backtest.py        Indicative 12-month backtest of the rules
  report.py          Markdown daily report
  dashboard.py       Self-contained HTML dashboard (blueprint style)
  run.py             Entry point
data/                Cached OHLCV CSVs (committed so runs work offline)
reports/YYYY-MM-DD.md  Daily signal reports (pushed by the agent)
docs/index.html      The dashboard (enable GitHub Pages on /docs to host it)
pine/fable_rules.pine  The same rules as a TradingView Pine Script you can review
.github/workflows/daily-analysis.yml  The daily agent (GitHub Actions cron)
```

## Run it

```bash
python -m tradebot.run                # analyze cached data
python -m tradebot.run --refresh      # refresh data from Stooq first (free, no key)
python -m tradebot.run --account 25000 --risk 1
```

Outputs: `reports/<date>.md`, `docs/index.html`.

## The daily agent

`.github/workflows/daily-analysis.yml` runs every weekday at 22:15 UTC
(after the US close): refreshes data, recomputes signals, and pushes the new
report + dashboard to the repo. You can also trigger it manually from the
Actions tab. To see the dashboard on the web, enable **GitHub Pages** →
deploy from branch → `/docs`.

## Signal states

| State | Meaning |
|---|---|
| `BUY` | Fresh breakout today, volume-confirmed — the entry rule fired |
| `BREAKOUT (LOW VOL)` | Broke resistance without volume backing — wait |
| `WATCH` | Within 2% below the trigger — set an alert / buy-stop |
| `IN UPTREND` | Above the 50-day trend, no fresh trigger |
| `NEUTRAL` | No edge — do nothing |
| `EXIT` | Closed below 20-day support — the exit rule fired |
