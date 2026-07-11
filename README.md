# Crypto + Forex Trading Bot (Binance / OANDA)

A trading bot with strict risk management that runs on two platforms:

- **Binance** — crypto spot pairs (e.g. `BTCUSDT`, `ETHUSDT`)
- **OANDA** — forex pairs (e.g. `EUR_USD`, `GBP_USD`)

The architecture is platform-agnostic (one strategy/risk core, thin API
clients), so more markets — Saudi Tadawul, US stocks — can be phased in
later as additional clients.

## Two strategies

**`swing` (default, `config.json`)** — modeled on the design of
[Sindbad.Tech](https://sindbad.tech) (a CMA-permitted Saudi trading-bot
company), translated to crypto:

- *Momentum/acceleration model*: daily candles; enters when ~weekly (7d) and
  monthly (30d) momentum are both positive **and** momentum is accelerating —
  their "non-linear model predicting behavior a week ahead" analog.
- *Safeguard signal*: a market regime filter — long only while BTC (the
  market proxy) closes above its 50-day EMA; goes to cash in down-markets.
  This is the capital-protection idea behind their "Safeguard Signal".
- Wide per-position stop (−8%) / take-profit (+25%), few trades → minimal
  fee drag. For context, Sindbad.Tech's own paid tier advertises
  "Average Profit Up to 15% Yearly" — that is the realistic scale licensed
  firms claim.

**`scalp` (`config.scalp.json`)** — RSI + EMA crossover on 5-minute candles
with tight stops. Trades often; fees matter a lot (backtest it!).

## Daily P&L management (both strategies)

Each day's P&L is managed with a **minimum profit lock of +2%** and a
**stretch target of +5%**:

| Day P&L reaches | What happens |
|---|---|
| **+2%** | Profit floor activates — this gain will not be given back |
| above +2% | Floor trails 1% below the day's peak (peak +4% → floor +3%) |
| falls back to floor | Bot sells everything, locks the gain, done for the day |
| **+5%** | Hard stop — quit while ahead |
| **−2%** | Hard stop on the downside |

All rules persist in a state file, so restarting the bot cannot bypass them.
Zero third-party dependencies — Python 3.8+ standard library only.

## ⚠️ Read this first — honest expectations

**Consistent daily gains of 2–5% are not a realistic long-run average.**
Compounded, even 2%/day is over +137,000% per year; professional firms
consider 5% per *month* excellent. The percentages above are **circuit
breakers that shape good days and cap bad ones** — not a promise of profit.
Some days end at the −2% stop. **Never trade money you cannot afford to
lose.** Forex specifics: markets close on weekends, and real accounts use
leverage — this bot deliberately sizes positions unleveraged (max 25% of
equity per position). Nothing here is financial advice.

## Risk controls

- **Position sizing**: each trade risks a fixed fraction of equity via its
  stop distance, capped per position (swing: 30%, max 3 positions).
- **Kill switch**: create a file named `STOP` in the bot directory and all
  instances halt immediately.

## Backtesting — measure before you trade

Replay months of real market history through the exact live strategy and
risk logic, with fees and slippage included:

```bash
python3 backtest.py --days 365                    # swing strategy (config.json)
python3 backtest.py config.scalp.json --days 90   # scalp strategy
python3 backtest.py config.forex.json --days 60   # forex (needs OANDA token)
```

The report shows total/monthly return, buy-and-hold comparison, win rate,
max drawdown, the daily P&L distribution, and how often each daily breaker
fired. **Judge the strategy by these numbers — not by targets or by the
30–40% claims of commercial "AI trading bots", which are unverified
marketing.** If a backtest or paper run doesn't convince you, don't fund it.

## Three modes — use them in this order

| Mode      | Orders                                    | Money at risk |
|-----------|-------------------------------------------|---------------|
| `paper`   | Simulated fills on real market data       | none          |
| `testnet` | Real orders — Binance testnet / OANDA practice account | none (fake funds) |
| `live`    | Real orders, real funds                   | **YES**       |

Run `paper` for 1–2 weeks, then `testnet`, and only go `live` if the results
actually satisfy you.

## Setup

```bash
git clone <this repo> && cd <repo>
python3 run_bot.py                    # crypto swing instance (config.json)
python3 run_bot.py config.forex.json  # forex instance (run in a second terminal)
```

Crypto paper mode works immediately with no keys. Forex needs a free OANDA
practice token even for paper mode (their market data requires login).

### Choosing your instruments

- Crypto: edit `symbols` in `config.json` — any Binance spot pair, e.g.
  `["BTCUSDT", "ETHUSDT", "SOLUSDT"]`
- Forex: edit `symbols` in `config.forex.json` — OANDA instruments, e.g.
  `["EUR_USD", "GBP_USD", "USD_JPY"]`

All risk parameters are per-config-file, documented in `trader/config.py`.

### Connecting your accounts

**Never share API keys/tokens with anyone — including in chat with an AI
assistant.** The bot reads them only from a local `.env` file (git-ignored).

```bash
cp .env.example .env    # then edit .env
```

**Binance:** create a key under API Management.
✅ Enable Reading, ✅ Enable Spot & Margin Trading,
❌ **never enable withdrawals**, 🔒 restrict to your machine's IP.
Testnet keys: <https://testnet.binance.vision>.

**OANDA:** open a free demo (practice) account at <https://www.oanda.com>,
then *Manage API Access* → generate token. Put the token and your account ID
(like `101-004-1234567-001`) in `.env`. `mode: "testnet"` trades the practice
account; `mode: "live"` requires a funded live account and a live token.

## Files

```
run_bot.py            entry point (optional arg: config file)
backtest.py           historical simulation of the exact live logic
config.json           crypto swing strategy (default)
config.scalp.json     crypto scalp strategy
config.forex.json     forex instance settings
.env                  your credentials (from .env.example, never commit)
trader/
  config.py           config loading + validation
  exchange.py         Binance REST client (live + testnet, signed requests)
  oanda.py            OANDA v20 REST client (practice + live)
  strategy.py         scalp (RSI/EMA) + swing (momentum/regime) strategies
  risk.py             sizing, stops, daily profit lock + circuit breakers
  bot.py              main loop, paper/live brokers
bot_state*.json       runtime state per instance — auto-created
STOP                  create this file to kill the bot instantly
```

## Disclaimer

This software is provided for educational purposes, as-is, without warranty of
any kind. You are solely responsible for any trades placed with your accounts
and for compliance with your local regulations. Use at your own risk.
