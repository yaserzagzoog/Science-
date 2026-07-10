# Binance Crypto Trading Bot

A spot trading bot for Binance with strict risk management. It trades the
coins you specify, targets a **+5% daily gain**, and shuts itself off for the
rest of the day when it hits either the daily target or the daily loss limit.

Zero third-party dependencies — Python 3.8+ standard library only.

## ⚠️ Read this first — honest expectations

**A consistent 5% daily gain is not a realistic expectation.** Compounded,
5%/day is roughly +5,000,000% per year; no strategy, human or bot, sustains
that. Professional trading firms consider 5% per *month* excellent. This bot
uses "5% daily" as a **stop-trading target** (a circuit breaker that locks in
good days), not a promise. On most days it will make less, and on some days it
will lose money — that's why the daily max-loss breaker (default −2%) exists.

**Never trade money you cannot afford to lose.** Crypto is extremely volatile
and past performance of any strategy does not predict future results. Nothing
here is financial advice.

## How it works

- **Strategy**: RSI(14) oversold-recovery entries plus EMA 9/21 crossover
  momentum on 5-minute candles. Exits on RSI overbought, EMA cross-down,
  or hard stop-loss (−1%) / take-profit (+1.5%) per position.
- **Position sizing**: each trade risks 1% of equity (via the stop distance)
  and is capped at 25% of equity, max 2 concurrent positions.
- **Daily circuit breakers**: when day P&L reaches **+5%** (your goal) or
  **−2%**, the bot flattens all positions and stops trading until the next
  UTC day. State persists in `bot_state.json`, so restarting the bot does not
  bypass the breakers.
- **Kill switch**: create a file named `STOP` in the bot directory and it
  halts immediately.

## Three modes — use them in this order

| Mode      | Orders                        | Keys needed | Money at risk |
|-----------|-------------------------------|-------------|---------------|
| `paper`   | Simulated, on live prices     | none        | none          |
| `testnet` | Real orders on Binance testnet| testnet keys| none (fake funds) |
| `live`    | Real orders, real funds       | live keys   | **YES**       |

Run in `paper` mode for at least 1–2 weeks, then `testnet`, and only go
`live` if the results actually satisfy you.

## Setup

```bash
git clone <this repo> && cd <repo>
python3 run_bot.py          # starts immediately in paper mode, no keys needed
```

### Choosing your coins

Edit `symbols` in `config.json` — any Binance spot pair quoted in USDT:

```json
"symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
```

All other parameters (stop-loss, daily target, candle interval, etc.) are in
`config.json` with comments in `binance_trader/config.py`.

### Connecting your Binance account (testnet / live)

**Never share your API keys with anyone — including in chat with an AI
assistant.** The bot reads them only from a local `.env` file.

1. Create an API key:
   - Testnet: <https://testnet.binance.vision> (log in with GitHub, free fake funds)
   - Live: Binance → Profile → API Management
2. **Key permissions (critical):**
   - ✅ Enable Reading
   - ✅ Enable Spot & Margin Trading
   - ❌ **Never enable withdrawals** — the bot doesn't need them, and this
     limits damage if the key ever leaks.
   - 🔒 Restrict access to your machine's IP address.
3. Configure the bot:
   ```bash
   cp .env.example .env      # then edit .env with your key + secret
   ```
4. Set `"mode": "testnet"` (or later `"live"`) in `config.json` and run:
   ```bash
   python3 run_bot.py
   ```

`.env` and `bot_state.json` are git-ignored — keep it that way.

## Files

```
run_bot.py                  entry point
config.json                 your trading settings (coins, risk, daily target)
.env                        your API keys (create from .env.example, never commit)
binance_trader/
  config.py                 config loading + validation
  exchange.py               Binance REST client (live + testnet, signed requests)
  strategy.py               RSI + EMA signal generation
  risk.py                   sizing, stops, daily circuit breakers
  bot.py                    main loop, paper/live brokers
bot_state.json              runtime state (positions, day P&L) — auto-created
STOP                        create this file to kill the bot instantly
```

## Disclaimer

This software is provided for educational purposes, as-is, without warranty of
any kind. You are solely responsible for any trades placed with your account
and for compliance with your local regulations. Use at your own risk.
