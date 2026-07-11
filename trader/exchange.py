"""Binance Spot REST client using only the standard library.

Supports public market data plus HMAC-SHA256 signed endpoints for
account/order operations. Live and testnet base URLs.
"""

import hashlib
import hmac
import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request

LIVE_URL = "https://api.binance.com"
TESTNET_URL = "https://testnet.binance.vision"


class BinanceError(Exception):
    pass


class BinanceClient:
    def __init__(self, api_key: str = "", api_secret: str = "", testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = TESTNET_URL if testnet else LIVE_URL
        self._filters_cache = {}

    # ------------------------------------------------------------------ http

    def _request(self, method: str, path: str, params: dict = None, signed: bool = False):
        params = dict(params or {})
        headers = {"User-Agent": "binance-trader-bot/0.1"}
        if self.api_key:
            headers["X-MBX-APIKEY"] = self.api_key
        if signed:
            if not self.api_secret:
                raise BinanceError("signed request requires an API secret")
            params["timestamp"] = int(time.time() * 1000)
            params["recvWindow"] = 5000
            query = urllib.parse.urlencode(params)
            signature = hmac.new(
                self.api_secret.encode(), query.encode(), hashlib.sha256
            ).hexdigest()
            query = f"{query}&signature={signature}"
        else:
            query = urllib.parse.urlencode(params)

        url = f"{self.base_url}{path}"
        data = None
        if method in ("POST", "PUT", "DELETE") and signed:
            data = query.encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        elif query:
            url = f"{url}?{query}"

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    return json.loads(resp.read().decode())
            except urllib.error.HTTPError as exc:
                body = exc.read().decode(errors="replace")
                # 4xx errors are not retryable (bad request / auth / filters)
                if 400 <= exc.code < 500:
                    raise BinanceError(f"HTTP {exc.code}: {body}") from exc
                if attempt == 2:
                    raise BinanceError(f"HTTP {exc.code}: {body}") from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt == 2:
                    raise BinanceError(f"network error: {exc}") from exc
            time.sleep(2 ** attempt)

    # ---------------------------------------------------------- market data

    def klines(self, symbol: str, interval: str, limit: int = 100):
        """Return list of closes (floats) for recent candles, oldest first."""
        raw = self._request(
            "GET", "/api/v3/klines",
            {"symbol": symbol, "interval": interval, "limit": limit},
        )
        return [float(candle[4]) for candle in raw]

    def klines_full(self, symbol: str, interval: str, limit: int = 1000,
                    start_ms: int = None):
        """Return OHLC candles as dicts {t, o, h, l, c}, oldest first.
        t is the open time in ms. Used by the backtester."""
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        if start_ms is not None:
            params["startTime"] = start_ms
        raw = self._request("GET", "/api/v3/klines", params)
        return [
            {"t": c[0], "o": float(c[1]), "h": float(c[2]),
             "l": float(c[3]), "c": float(c[4])}
            for c in raw
        ]

    def ticker_price(self, symbol: str) -> float:
        data = self._request("GET", "/api/v3/ticker/price", {"symbol": symbol})
        return float(data["price"])

    def symbol_filters(self, symbol: str) -> dict:
        """Return {step_size, min_qty, min_notional, tick_size} for a symbol."""
        if symbol in self._filters_cache:
            return self._filters_cache[symbol]
        info = self._request("GET", "/api/v3/exchangeInfo", {"symbol": symbol})
        result = {"step_size": 0.0, "min_qty": 0.0, "min_notional": 0.0, "tick_size": 0.0}
        for f in info["symbols"][0]["filters"]:
            if f["filterType"] == "LOT_SIZE":
                result["step_size"] = float(f["stepSize"])
                result["min_qty"] = float(f["minQty"])
            elif f["filterType"] in ("NOTIONAL", "MIN_NOTIONAL"):
                result["min_notional"] = float(f.get("minNotional", 0))
            elif f["filterType"] == "PRICE_FILTER":
                result["tick_size"] = float(f["tickSize"])
        self._filters_cache[symbol] = result
        return result

    def round_qty(self, symbol: str, qty: float) -> float:
        step = self.symbol_filters(symbol)["step_size"]
        if step <= 0:
            return qty
        decimals = max(0, -int(round(math.log10(step))))
        return round(math.floor(qty / step) * step, decimals)

    # -------------------------------------------------------------- account

    def account_balances(self) -> dict:
        data = self._request("GET", "/api/v3/account", signed=True)
        return {
            b["asset"]: float(b["free"])
            for b in data["balances"]
            if float(b["free"]) > 0
        }

    def market_order(self, symbol: str, side: str, quantity: float) -> dict:
        return self._request(
            "POST", "/api/v3/order",
            {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": f"{quantity:.8f}".rstrip("0").rstrip("."),
            },
            signed=True,
        )
