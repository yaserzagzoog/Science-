"""Daily runner: refresh data (best effort), analyze, backtest, write outputs.

Usage:
    python -m tradebot.run                 # analyze from cached CSVs
    python -m tradebot.run --refresh       # try to update CSVs from Stooq first
    python -m tradebot.run --account 25000 --risk 1.0
"""

import argparse
import os
import sys

from . import backtest, dashboard, data, report
from .config import PARAMS, WATCHLIST
from .strategy import analyze

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FULL_DOC = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
{body}
</html>
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Fable Rules daily analysis")
    ap.add_argument("--refresh", action="store_true", help="refresh CSVs from Stooq first")
    ap.add_argument("--account", type=float, default=PARAMS["account_size"])
    ap.add_argument("--risk", type=float, default=PARAMS["risk_pct"])
    args = ap.parse_args(argv)

    overrides = {"account_size": args.account, "risk_pct": args.risk}
    signals, stats = [], {}
    for symbol, name, klass in WATCHLIST:
        if args.refresh:
            bars, status = data.refresh(symbol)
            print(f"  {symbol}: {status}", file=sys.stderr)
        else:
            bars = data.load(symbol)
        if not bars:
            print(f"  {symbol}: no data — skipped", file=sys.stderr)
            continue
        sig = analyze(symbol, name, klass, bars, overrides)
        if sig is None:
            print(f"  {symbol}: insufficient history — skipped", file=sys.stderr)
            continue
        signals.append(sig)
        st = backtest.run(bars)
        if st:
            stats[symbol] = st

    if not signals:
        print("No signals produced (no data). Run with --refresh or populate data/.",
              file=sys.stderr)
        return 1

    run_date = max(s.date for s in signals)

    md = report.build(signals, stats, run_date, args.account, args.risk)
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    report_path = os.path.join(ROOT, "reports", f"{run_date}.md")
    with open(report_path, "w") as f:
        f.write(md)

    body = dashboard.build(signals, stats, run_date, args.account, args.risk)
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    dash_path = os.path.join(ROOT, "docs", "index.html")
    with open(dash_path, "w") as f:
        f.write(FULL_DOC.format(body=f"</head>\n<body>\n{body}\n</body>"))
    # body-only copy, convenient for Claude artifact publishing
    with open(os.path.join(ROOT, "docs", "dashboard-body.html"), "w") as f:
        f.write(body)

    print(f"Wrote {report_path}")
    print(f"Wrote {dash_path}")
    actionable = [s for s in signals if s.state in
                  ("BUY", "BREAKOUT (LOW VOL)", "WATCH", "EXIT")]
    print(f"{len(signals)} symbols analyzed on {run_date}; "
          f"{len(actionable)} actionable: "
          + (", ".join(f"{s.symbol} [{s.state}]" for s in actionable) or "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
