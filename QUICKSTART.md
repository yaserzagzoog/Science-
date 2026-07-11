# Quickstart — from zero to trading

Total time: ~10 minutes to paper trading, ~20 to testnet. Only Python 3.8+
is required — no packages to install.

## Step 1 — Get the code onto your machine (or a VPS)

```bash
git clone -b claude/binance-crypto-trader-0oyjcs https://github.com/yaserzagzoog/Science-.git trader-bot
cd trader-bot
```

A home PC works, but it must stay on — the bot only trades while running.
For 24/7 operation use a small VPS (Hetzner/DigitalOcean, ~$5/month).

## Step 2 — Start paper trading (no API keys needed)

```bash
python3 doctor.py       # preflight checks
python3 run_bot.py      # swing strategy, simulated money, live prices
```

That's it — it logs every decision. Also run the backtest to see how the
strategy would have done over the last year:

```bash
python3 backtest.py --days 365
```

## Step 3 — Connect your Binance API (testnet first)

**Never share API keys with anyone — not in chat, not by email, not with
AI assistants.** They live only in the `.env` file on your machine.

1. **Testnet keys (fake funds, real orders)**: log in at
   <https://testnet.binance.vision> with GitHub → *Generate HMAC-SHA256 Key*.
2. Create your local `.env`:
   ```bash
   cp .env.example .env
   nano .env          # paste the key + secret
   ```
3. Switch `"mode": "paper"` to `"mode": "testnet"` in `config.json`.
4. Verify and run:
   ```bash
   python3 doctor.py && python3 run_bot.py
   ```

## Step 4 — Going live (only after Steps 2–3 satisfy you)

1. Binance → Profile → **API Management** → Create API.
2. Permissions — this is the critical part:
   - ✅ Enable Reading
   - ✅ Enable Spot & Margin Trading
   - ❌ **Leave withdrawals OFF** (the bot never needs them)
   - 🔒 Restrict access to your machine's IP address
3. Put the live key/secret in `.env`, set `"mode": "live"`.
4. `python3 doctor.py` — it will verify the key **cannot withdraw**, can
   trade, and is IP-restricted, and will show your USDT balance.
5. Fund the account only with an amount you can afford to lose entirely.
   Start small (e.g. a few hundred dollars) even if tests looked great.
6. `python3 run_bot.py` — it prints a 10-second live-mode warning, then runs.

## Running 24/7 on a VPS

```bash
nohup python3 run_bot.py > bot.log 2>&1 &     # keeps running after logout
tail -f bot.log                               # watch it live
```

Or with systemd (survives reboots): create `/etc/systemd/system/trader.service`:

```ini
[Unit]
Description=Trading bot
After=network-online.target

[Service]
WorkingDirectory=/root/trader-bot
ExecStart=/usr/bin/python3 run_bot.py
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable --now trader.service
journalctl -u trader -f        # watch logs
```

## Controlling the bot

| Action | How |
|---|---|
| Stop instantly | `touch STOP` in the bot directory (or Ctrl-C) |
| Resume | delete the `STOP` file, restart the bot |
| See open positions / day P&L | `cat bot_state.json` |
| Change coins | edit `symbols` in `config.json`, restart |
| Second market (forex) | `python3 run_bot.py config.forex.json` |

State survives restarts: positions and the day's profit-lock/breaker status
are in `bot_state.json`, so restarting cannot bypass risk limits.

## Safety recap

- The bot can only trade inside your account; with withdrawals disabled and
  IP restriction on, a leaked key cannot move funds out.
- Daily rules: lock gains at +2% (trailing), stop at +5%, cut off at −3%
  (swing config). All persisted.
- If anything looks wrong: `touch STOP`, then investigate `bot.log`.
