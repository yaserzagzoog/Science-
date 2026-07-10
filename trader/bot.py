"""Main trading loop, platform-agnostic (Binance crypto / OANDA forex).

Modes:
  paper   - real market data, simulated fills
  testnet - real orders, fake funds (Binance Spot testnet / OANDA practice)
  live    - real money. Only use after validating on paper/testnet.
"""

import logging
import sys
import time

from .config import Config
from .exchange import BinanceClient, BinanceError
from .oanda import OandaClient, OandaError
from .risk import RiskManager
from .strategy import Strategy

log = logging.getLogger("bot")

TradeError = (BinanceError, OandaError)


class PaperBroker:
    """Simulates fills at the current market price."""

    def __init__(self, cfg):
        self.cfg = cfg
        self.quote_balance = cfg.paper_starting_balance

    def buy(self, symbol, qty, price):
        cost = qty * price
        if cost > self.quote_balance:
            raise BinanceError("insufficient paper balance")
        self.quote_balance -= cost
        log.info("[PAPER] BUY %s qty=%.8f @ %.5f (cost %.2f)", symbol, qty, price, cost)

    def sell(self, symbol, qty, price):
        proceeds = qty * price
        self.quote_balance += proceeds
        log.info("[PAPER] SELL %s qty=%.8f @ %.5f (proceeds %.2f)", symbol, qty, price, proceeds)


class LiveBroker:
    def __init__(self, cfg, client):
        self.cfg = cfg
        self.client = client

    def buy(self, symbol, qty, price):
        order = self.client.market_order(symbol, "BUY", qty)
        log.info("BUY %s submitted: %s", symbol, _order_summary(order))

    def sell(self, symbol, qty, price):
        order = self.client.market_order(symbol, "SELL", qty)
        log.info("SELL %s submitted: %s", symbol, _order_summary(order))


def _order_summary(order: dict) -> str:
    if "orderId" in order:   # binance
        return f"orderId={order.get('orderId')} status={order.get('status')}"
    fill = order.get("orderFillTransaction", {})   # oanda
    return f"id={fill.get('id')} price={fill.get('price')}"


def make_client(cfg: Config):
    if cfg.platform == "oanda":
        return OandaClient(cfg.oanda_token, cfg.oanda_account_id,
                           practice=(cfg.mode != "live"))
    return BinanceClient(cfg.api_key, cfg.api_secret,
                         testnet=(cfg.mode == "testnet"))


class TradingBot:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.client = make_client(cfg)
        self.risk = RiskManager(cfg)
        self.strategy = Strategy(cfg)
        self.broker = PaperBroker(cfg) if cfg.mode == "paper" else LiveBroker(cfg, self.client)

    # ------------------------------------------------------------------ equity

    def equity(self, prices: dict) -> float:
        """Cash/NAV plus mark-to-market value of bot-tracked open positions."""
        if self.cfg.mode == "paper":
            quote = self.broker.quote_balance
        elif self.cfg.platform == "oanda":
            # OANDA NAV already includes unrealized P&L of open trades.
            return self.client.equity()
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
            except TradeError as exc:
                log.warning("price fetch failed for %s: %s", symbol, exc)

        if not prices:
            return True

        try:
            equity = self.equity(prices)
        except TradeError as exc:
            log.warning("equity fetch failed: %s", exc)
            return True
        self.risk.roll_day_if_needed(equity)
        halt = self.risk.check_breakers(equity)

        start = self.risk.state["day_start_equity"] or equity
        day_pct = (equity - start) / start * 100 if start else 0.0
        floor = self.risk.profit_floor()
        log.info("equity=%.2f | day P&L %+.2f%% (peak %+.2f%%%s) | positions=%d",
                 equity, day_pct, self.risk.state["day_peak_pct"],
                 f", floor {floor:+.2f}%" if floor is not None else "",
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
        except TradeError as exc:
            log.warning("klines failed for %s: %s", symbol, exc)
            return

        holding = self.risk.get_position(symbol) is not None
        signal = self.strategy.evaluate(closes, holding)
        log.debug("%s price=%.5f rsi=%.1f -> %s (%s)",
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
                log.info("OPENED %s qty=%.8f @ %.5f (%s)", symbol, qty, price, signal.reason)
            except TradeError as exc:
                log.error("BUY %s failed: %s", symbol, exc)
        elif signal.action == "SELL" and holding:
            self._close(symbol, price, signal.reason)

    def _close(self, symbol: str, price: float, reason: str):
        pos = self.risk.get_position(symbol)
        if not pos:
            return
        try:
            self.broker.sell(symbol, pos["qty"], price)
        except TradeError as exc:
            log.error("SELL %s failed: %s", symbol, exc)
            return
        pnl = self.risk.close_position(symbol, price)
        log.info("CLOSED %s @ %.5f pnl=%+.2f (%s)", symbol, price, pnl, reason)

    def _close_all(self, prices: dict):
        for symbol in list(self.risk.state["positions"]):
            price = prices.get(symbol)
            if price:
                self._close(symbol, price, "daily halt - flattening")

    def run(self):
        log.info("starting bot: platform=%s mode=%s symbols=%s | "
                 "day rules: lock at +%.1f%%, trail %.1f%%, stop at +%.1f%% or -%.1f%%",
                 self.cfg.platform, self.cfg.mode, ",".join(self.cfg.symbols),
                 self.cfg.daily_min_lock_pct, self.cfg.daily_giveback_pct,
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
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    TradingBot(Config.load(config_path)).run()


if __name__ == "__main__":
    main()
