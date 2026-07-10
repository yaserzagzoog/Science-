#!/usr/bin/env python3
"""Entry point.

    python3 run_bot.py                     # uses config.json (crypto/Binance)
    python3 run_bot.py config.forex.json   # forex/OANDA instance
"""

from trader.bot import main

if __name__ == "__main__":
    main()
