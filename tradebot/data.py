"""OHLCV loading and refresh. CSV cache in data/ is the source of truth;
`refresh()` tries to extend it from Stooq (free, no API key) and silently
keeps the cache when the network is unavailable."""

import csv
import io
import os
import urllib.request
from dataclasses import dataclass

from .config import STOOQ_SYMBOLS

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


@dataclass
class Bar:
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float


def csv_path(symbol: str) -> str:
    return os.path.join(DATA_DIR, f"{symbol}.csv")


def load(symbol: str) -> list[Bar]:
    """Load cached bars for a symbol, oldest first."""
    path = csv_path(symbol)
    if not os.path.exists(path):
        return []
    bars = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            try:
                bars.append(Bar(
                    date=row["date"],
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"] or 0),
                ))
            except (ValueError, KeyError):
                continue
    bars.sort(key=lambda b: b.date)
    return bars


def save(symbol: str, bars: list[Bar]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(csv_path(symbol), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "open", "high", "low", "close", "volume"])
        for b in sorted(bars, key=lambda x: x.date):
            w.writerow([b.date, b.open, b.high, b.low, b.close, int(b.volume)])


def _fetch_stooq(symbol: str) -> list[Bar]:
    stooq = STOOQ_SYMBOLS.get(symbol)
    if not stooq:
        return []
    url = f"https://stooq.com/q/d/l/?s={stooq}&i=d"
    req = urllib.request.Request(url, headers={"User-Agent": "fable-rules/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    bars = []
    for row in csv.DictReader(io.StringIO(text)):
        try:
            bars.append(Bar(
                date=row["Date"],
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=float(row.get("Volume") or 0),
            ))
        except (ValueError, KeyError):
            continue
    return bars


def refresh(symbol: str, keep_days: int = 500) -> tuple[list[Bar], str]:
    """Merge fresh Stooq data into the cache. Returns (bars, status)."""
    cached = load(symbol)
    try:
        fresh = _fetch_stooq(symbol)
    except Exception as e:  # offline / blocked — cache still works
        return cached, f"cache only ({type(e).__name__})"
    if not fresh:
        return cached, "cache only (no data returned)"
    merged = {b.date: b for b in cached}
    merged.update({b.date: b for b in fresh})
    bars = sorted(merged.values(), key=lambda b: b.date)[-keep_days:]
    save(symbol, bars)
    return bars, f"refreshed through {bars[-1].date}" if bars else "empty"
