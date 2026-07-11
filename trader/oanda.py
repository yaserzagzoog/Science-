"""OANDA v20 REST client for forex, standard library only.

Presents the same interface as BinanceClient (ticker_price, klines,
symbol_filters, round_qty, market_order, equity) so the bot core is
platform-agnostic. Instruments use OANDA naming, e.g. "EUR_USD".

Practice (demo) and live endpoints. A free practice account provides an
API token: https://www.oanda.com -> demo account -> Manage API Access.
"""

import json
import time
import urllib.error
import urllib.parse
import urllib.request

LIVE_URL = "https://api-fxtrade.oanda.com"
PRACTICE_URL = "https://api-fxpractice.oanda.com"

# bot interval -> OANDA granularity
GRANULARITY = {
    "1m": "M1", "5m": "M5", "15m": "M15", "30m": "M30",
    "1h": "H1", "4h": "H4", "1d": "D",
}


class OandaError(Exception):
    pass


class OandaClient:
    def __init__(self, token: str, account_id: str, practice: bool = True):
        self.token = token
        self.account_id = account_id
        self.base_url = PRACTICE_URL if practice else LIVE_URL

    # ------------------------------------------------------------------ http

    def _request(self, method: str, path: str, params: dict = None, body: dict = None):
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept-Datetime-Format": "UNIX",
            "User-Agent": "trader-bot/0.1",
        }
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    return json.loads(resp.read().decode())
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode(errors="replace")
                if 400 <= exc.code < 500:
                    raise OandaError(f"HTTP {exc.code}: {detail}") from exc
                if attempt == 2:
                    raise OandaError(f"HTTP {exc.code}: {detail}") from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt == 2:
                    raise OandaError(f"network error: {exc}") from exc
            time.sleep(2 ** attempt)

    # ---------------------------------------------------------- market data

    def ticker_price(self, symbol: str) -> float:
        data = self._request(
            "GET", f"/v3/accounts/{self.account_id}/pricing",
            {"instruments": symbol},
        )
        prices = data.get("prices", [])
        if not prices:
            raise OandaError(f"no pricing for {symbol}")
        p = prices[0]
        if p.get("tradeable") is False:
            raise OandaError(f"{symbol} not tradeable now (market closed?)")
        bid = float(p["bids"][0]["price"])
        ask = float(p["asks"][0]["price"])
        return (bid + ask) / 2

    def klines(self, symbol: str, interval: str, limit: int = 100):
        """Return list of mid closes for completed candles, oldest first."""
        granularity = GRANULARITY.get(interval)
        if granularity is None:
            raise OandaError(f"unsupported interval {interval!r}")
        data = self._request(
            "GET", f"/v3/instruments/{symbol}/candles",
            {"granularity": granularity, "count": min(limit, 500), "price": "M"},
        )
        return [
            float(c["mid"]["c"]) for c in data.get("candles", []) if c.get("complete")
        ]

    def klines_full(self, symbol: str, interval: str, limit: int = 500,
                    start_ms: int = None):
        """Return OHLC candles as dicts {t, o, h, l, c}, oldest first.
        t is the open time in ms. Used by the backtester."""
        granularity = GRANULARITY.get(interval)
        if granularity is None:
            raise OandaError(f"unsupported interval {interval!r}")
        params = {"granularity": granularity, "count": min(limit, 500), "price": "M"}
        if start_ms is not None:
            params["from"] = f"{start_ms / 1000:.3f}"
        data = self._request(
            "GET", f"/v3/instruments/{symbol}/candles", params)
        out = []
        for c in data.get("candles", []):
            if not c.get("complete"):
                continue
            mid = c["mid"]
            out.append({
                "t": int(float(c["time"]) * 1000),
                "o": float(mid["o"]), "h": float(mid["h"]),
                "l": float(mid["l"]), "c": float(mid["c"]),
            })
        return out

    def symbol_filters(self, symbol: str) -> dict:
        # OANDA trades whole units of the base currency; 1 unit minimum.
        return {"step_size": 1.0, "min_qty": 1.0, "min_notional": 0.0, "tick_size": 0.0}

    def round_qty(self, symbol: str, qty: float) -> float:
        return float(int(qty))

    # -------------------------------------------------------------- account

    def equity(self) -> float:
        data = self._request("GET", f"/v3/accounts/{self.account_id}/summary")
        return float(data["account"]["NAV"])

    def market_order(self, symbol: str, side: str, quantity: float) -> dict:
        units = int(quantity) if side == "BUY" else -int(quantity)
        result = self._request(
            "POST", f"/v3/accounts/{self.account_id}/orders",
            body={"order": {
                "type": "MARKET",
                "instrument": symbol,
                "units": str(units),
                "timeInForce": "FOK",
                "positionFill": "DEFAULT",
            }},
        )
        if "orderCancelTransaction" in result:
            reason = result["orderCancelTransaction"].get("reason", "unknown")
            raise OandaError(f"order cancelled: {reason}")
        return result
