"""Fable Rules — rule-based breakout trading analysis toolkit.

Strategy specification (the "Fable Rules" system):
  ENTRY      price closes above 20-day resistance with volume above its 20-day average
  EXIT       close below 20-day support, or opposite signal
  STOP LOSS  below breakout level / structure (10-day low)
  SIZE       risk 1% of account per trade
  TIMEFRAME  daily

Code is generated. Human review required. Responsibility is yours.
This is analysis tooling, not financial advice.
"""

__version__ = "1.0.0"
