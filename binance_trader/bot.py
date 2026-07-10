"""Main trading loop.

Modes:
  paper   - live market data, simulated fills, no API keys needed
  testnet - real orders against Binance Spot testnet (fake funds)
  live    - real money. Only use after validating on paper/testnet.
"""

import logging
import time

from .config import Config
from .exchange import BinanceClient, BinanceError
from .risk import RiskManager
from .strategy import Strategy

log = logging.getLogger("bot")


class PaperBroker:
    """Simulates fills at the current market price."""

    def __init__(self, cfg, client):
        self.cfg = cfg
        self.client = client
        self.quote_balance = cfg.paper_starting_balance

    def buy(self, symbol, qty, price):
        cost = qty * price
        if cost > self.quote_balance:
            raise BinanceError("insufficient paper balance")
        self.quote_balance -= cost
        log.info("[PAPER] BUY %s qty=%.8f @ %.4f (cost %.2f)", symbol, qty, price, cost)

    def sell(self, symbol, qty, price):
        proceeds = qty * price
        self.quote_balance += proceeds
        log.info("[PAPER] SELL %s qty=%.8f @ %.4f (proceeds %.2f)", symbol, qty, price, proceeds)


class LiveBroker:
    def __init__(self, cfg, client):
        self.cfg = cfg
        self.client = client

    def buy(self, symbol, qty, price):
        order = self.client.market_order(symbol, "BUY", qty)
        log.info("BUY %s -> orderId=%s status=%s", symbol, order.get("orderId"), order.get("status"))

    def sell(self, symbol, qty, price):
        order = self.client.market_order(symbol, "SELL", qty)
        log.info("SELL %s -> orderId=%s status=%s", symbol, order.get("orderId"), order.get("status"))


class TradingBot:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        # Paper mode uses LIVE market data (public endpoints, no keys) but fake fills.
        self.client = BinanceClient(cfg.api_key, cfg.api_secret, testnet=(cfg.mode == "testnet"))
        self.risk = RiskManager(cfg)
        self.strategy = Strategy(cfg)
        self.broker = (
            PaperBroker(cfg, self.client) if cfg.mode == "paper" else LiveBroker(cfg, self.client)
        )

    # ------------------------------------------------------------------ equity

    def equity(self, prices: dict) -> float:
        """Quote-asset balance plus mark-to-market value of open positions."""
        if self.cfg.mode == "paper":
            quote = self.broker.quote_balance
        else:
            balances = self.client.account_balances()
            quote = balances.get(self.cfg.quote_asset, 0.0)
        total = quote
        for symbol, pos in self.risk.state["positions"].items():
            price = prices.get(symbol) or pos["entry_price"]
            total += pos["qty"] * price
        return total

    # ------------------------------------------------------------------- loop

    def run_once(self) -> bool:
        """One evaluation pass. Returns False when trading is halted for the day."""
        prices = {}
        for symbol in self.cfg.symbols:
            try:
                prices[symbol] = self.client.ticker_price(symbol)
            except BinanceError as exc:
                log.warning("price fetch failed for %s: %s", symbol, exc)

        if not prices:
            return True

        equity = self.equity(prices)
        self.risk.roll_day_if_needed(equity)
        halt = self.risk.check_breakers(equity)

        start = self.risk.state["day_start_equity"] or equity
        day_pct = (equity - start) / start * 100 if start else 0.0
        log.info("equity=%.2f %s | day P&L %+.2f%% | positions=%d",
                 equity, self.cfg.quote_asset, day_pct,
                 len(self.risk.state["positions"]))

        if halt:
            log.warning("TRADING HALTED: %s", halt)
            self._close_all(prices)
            return False

        for symbol in self.cfg.symbols:
            if symbol in prices:
                self._process_symbol(symbol, prices[symbol], equity)
        return True

    def _process_symbol(self, symbol: str, price: float, equity: float):
        # 1. Hard exits first: stop-loss / take-profit
        exit_reason = self.risk.stop_or_target_hit(symbol, price)
        if exit_reason:
            self._close(symbol, price, exit_reason)
            return

        # 2. Strategy signal
        try:
            closes = self.client.klines(symbol, self.cfg.kline_interval,
                                        limit=self.cfg.ema_slow * 4)
        except BinanceError as exc:
            log.warning("klines failed for %s: %s", symbol, exc)
            return

        holding = self.risk.get_position(symbol) is not None
        signal = self.strategy.evaluate(closes, holding)
        log.debug("%s price=%.4f rsi=%.1f -> %s (%s)",
                  symbol, price, signal.rsi, signal.action, signal.reason)

        if signal.action == "BUY" and not holding and self.risk.can_open():
            qty = self.risk.position_size(equity, price)
            qty = self.client.round_qty(symbol, qty)
            filters = self.client.symbol_filters(symbol)
            if qty < filters["min_qty"] or qty * price < filters["min_notional"]:
                log.info("%s BUY skipped: size %.8f below exchange minimums", symbol, qty)
                return
            try:
                self.broker.buy(symbol, qty, price)
                self.risk.open_position(symbol, qty, price)
                log.info("OPENED %s qty=%.8f @ %.4f (%s)", symbol, qty, price, signal.reason)
            except BinanceError as exc:
                log.error("BUY %s failed: %s", symbol, exc)
        elif signal.action == "SELL" and holding:
            self._close(symbol, price, signal.reason)

    def _close(self, symbol: str, price: float, reason: str):
        pos = self.risk.get_position(symbol)
        if not pos:
            return
        try:
            self.broker.sell(symbol, pos["qty"], price)
        except BinanceError as exc:
            log.error("SELL %s failed: %s", symbol, exc)
            return
        pnl = self.risk.close_position(symbol, price)
        log.info("CLOSED %s @ %.4f pnl=%+.2f (%s)", symbol, price, pnl, reason)

    def _close_all(self, prices: dict):
        for symbol in list(self.risk.state["positions"]):
            price = prices.get(symbol)
            if price:
                self._close(symbol, price, "daily halt - flattening")

    def run(self):
        log.info("starting bot: mode=%s symbols=%s target=+%.1f%%/day max_loss=-%.1f%%/day",
                 self.cfg.mode, ",".join(self.cfg.symbols),
                 self.cfg.daily_target_pct, self.cfg.daily_max_loss_pct)
        if self.cfg.mode == "live":
            log.warning("LIVE MODE: real orders will be placed. Ctrl-C to abort (10s)...")
            time.sleep(10)
        try:
            while True:
                active = self.run_once()
                # When halted, keep polling slowly so the day rollover resumes trading
                time.sleep(self.cfg.poll_seconds if active else 300)
        except KeyboardInterrupt:
            log.info("stopped by user; open positions are preserved in %s",
                     self.cfg.state_file)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )
    TradingBot(Config.load()).run()


if __name__ == "__main__":
    main()
