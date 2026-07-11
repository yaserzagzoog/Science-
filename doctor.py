#!/usr/bin/env python3
"""Preflight checks — run this BEFORE starting the bot.

    python3 doctor.py                    # checks config.json
    python3 doctor.py config.forex.json

Verifies config, credentials, connectivity, clock sync, symbols, account
access, and (live Binance) that the API key CANNOT withdraw funds.
Exits 0 when everything needed for the configured mode passes.
"""

import sys
import time

from trader.bot import make_client
from trader.config import Config

OK, BAD, WARN = "  [ OK ]", "  [FAIL]", "  [WARN]"
failures = 0
warnings = 0


def fail(msg):
    global failures
    failures += 1
    print(BAD, msg)


def warn(msg):
    global warnings
    warnings += 1
    print(WARN, msg)


def ok(msg):
    print(OK, msg)


def main():
    global failures
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    print(f"== Preflight: {config_path} ==\n")

    # 1. config + credentials
    try:
        cfg = Config.load(config_path)
        ok(f"config valid: platform={cfg.platform} mode={cfg.mode} "
           f"strategy={cfg.strategy} symbols={','.join(cfg.symbols)}")
    except (ValueError, OSError) as exc:
        fail(f"config: {exc}")
        print("\nFix the config or .env first, then re-run.")
        return 1

    if cfg.mode == "live":
        warn("mode=live — REAL MONEY. Make sure paper/testnet results "
             "convinced you first.")

    client = make_client(cfg)

    # 2. connectivity + clock sync
    try:
        t0 = time.time()
        price = client.ticker_price(cfg.symbols[0])
        ok(f"API reachable ({cfg.symbols[0]} = {price})")
    except Exception as exc:
        fail(f"cannot reach {cfg.platform} API: {exc}")
        print("\nCheck your network/firewall. If you are on a VPS, confirm "
              "outbound HTTPS is allowed.")
        return 1

    if cfg.platform == "binance":
        try:
            drift_ms = abs(client.server_time_ms() - int(time.time() * 1000))
            if drift_ms > 1000:
                warn(f"clock drift {drift_ms}ms vs exchange — signed requests "
                     "may fail. Enable NTP time sync on this machine.")
            else:
                ok(f"clock in sync (drift {drift_ms}ms)")
        except Exception as exc:
            warn(f"could not check server time: {exc}")

    # 3. every configured symbol resolves
    for symbol in cfg.symbols[1:]:
        try:
            client.ticker_price(symbol)
            ok(f"symbol {symbol} tradeable")
        except Exception as exc:
            fail(f"symbol {symbol}: {exc}")
    if cfg.strategy == "swing":
        try:
            n = len(client.klines(cfg.regime_symbol, cfg.kline_interval, limit=60))
            ok(f"regime data {cfg.regime_symbol}: {n} candles")
        except Exception as exc:
            fail(f"regime symbol {cfg.regime_symbol}: {exc}")

    # 4. account access (signed) for testnet/live
    if cfg.mode == "paper":
        ok("paper mode: no account access needed")
    else:
        try:
            if cfg.platform == "binance":
                balances = client.account_balances()
                quote = balances.get(cfg.quote_asset, 0.0)
                ok(f"account access works — {cfg.quote_asset} balance: {quote}")
                if quote <= 0:
                    warn(f"no free {cfg.quote_asset} in the account; the bot "
                         "will have nothing to trade with.")
            else:
                nav = client.equity()
                ok(f"OANDA account access works — NAV: {nav}")
        except Exception as exc:
            fail(f"account access: {exc}")
            print("\nCheck the key/secret in .env and the key's permissions "
                  "and IP restriction.")
            return 1

    # 5. live Binance: verify the key is locked down
    if cfg.platform == "binance" and cfg.mode == "live":
        try:
            r = client.api_restrictions()
            if r.get("enableWithdrawals"):
                fail("API key has WITHDRAWALS ENABLED. Disable withdrawals on "
                     "this key in Binance API Management before going live — "
                     "the bot never needs them, and a leaked key with "
                     "withdrawals can drain your account.")
            else:
                ok("withdrawals disabled on this key")
            if not r.get("enableSpotAndMarginTrading"):
                fail("API key cannot trade spot. Enable 'Spot & Margin "
                     "Trading' on the key.")
            else:
                ok("spot trading enabled on this key")
            if not r.get("ipRestrict"):
                warn("key is not IP-restricted. Strongly consider restricting "
                     "it to this machine's IP in Binance API Management.")
            else:
                ok("key is IP-restricted")
        except Exception as exc:
            warn(f"could not read key restrictions: {exc}")

    print()
    if failures:
        print(f"RESULT: {failures} failure(s), {warnings} warning(s) — fix "
              "the failures before running the bot.")
        return 1
    print(f"RESULT: all checks passed ({warnings} warning(s)).")
    print(f"Start the bot with:  python3 run_bot.py {config_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
