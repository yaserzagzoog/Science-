# Crypto + Forex Trading Bot (Binance / OANDA)

A trading bot with strict risk management that runs on two platforms:

- **Binance** — crypto spot pairs (e.g. `BTCUSDT`, `ETHUSDT`)
- **OANDA** — forex pairs (e.g. `EUR_USD`, `GBP_USD`)

It trades the instruments you specify and manages each day's P&L with a
**minimum profit lock of +2%** and a **stretch target of +5%**:

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

## How it works

- **Strategy** (same for both platforms): RSI(14) oversold-recovery entries
  plus EMA 9/21 crossover momentum on 5-minute candles. Exits on RSI
  overbought, EMA cross-down, or per-position stop-loss / take-profit
  (crypto: −1% / +1.5%; forex: −0.3% / +0.45% — forex moves are smaller).
- **Position sizing**: each trade risks 1% of equity via its stop distance,
  capped at 25% of equity, max 2 concurrent positions.
- **Kill switch**: create a file named `STOP` in the bot directory and both
  instances halt immediately.

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
python3 run_bot.py                    # crypto instance (config.json)
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
config.json           crypto instance settings
config.forex.json     forex instance settings
.env                  your credentials (from .env.example, never commit)
trader/
  config.py           config loading + validation
  exchange.py         Binance REST client (live + testnet, signed requests)
  oanda.py            OANDA v20 REST client (practice + live)
  strategy.py         RSI + EMA signal generation
  risk.py             sizing, stops, daily profit lock + circuit breakers
  bot.py              main loop, paper/live brokers
bot_state*.json       runtime state per instance — auto-created
STOP                  create this file to kill the bot instantly
```

## Disclaimer

This software is provided for educational purposes, as-is, without warranty of
any kind. You are solely responsible for any trades placed with your accounts
and for compliance with your local regulations. Use at your own risk.
