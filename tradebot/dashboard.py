"""Static HTML dashboard generator — blueprint / technical-drawing aesthetic.

Produces a fully self-contained docs/index.html (inline CSS/JS/SVG, no external
requests) so it can be served from GitHub Pages or opened locally."""

import html
import json

from .backtest import Stats
from .strategy import (BREAKOUT_UNCONFIRMED, BUY, EXIT, NEUTRAL, STATE_ORDER,
                       UPTREND, WATCH, Signal)

STATE_CLASS = {
    BUY: "buy", BREAKOUT_UNCONFIRMED: "warn", WATCH: "warn",
    UPTREND: "trend", NEUTRAL: "flat", EXIT: "exit",
}
STATE_ICON = {
    BUY: "▲", BREAKOUT_UNCONFIRMED: "◮", WATCH: "◈",
    UPTREND: "↗", NEUTRAL: "—", EXIT: "▼",
}

CSS = """
:root{
  --paper:#f4efe4; --card:#faf7ee; --ink:#17150f; --ink2:#5c574a; --muted:#8a8474;
  --line:#d9d2bf; --hair:#e4ddca; --accent:#b34a17; --accent-soft:#c65d2e;
  --buy:#2c6e31; --warn:#a05a00; --exit:#a63a2c; --chip:#eee8d8;
}
@media (prefers-color-scheme: dark){:root{
  --paper:#16140f; --card:#1d1a13; --ink:#eae4d3; --ink2:#a39d8c; --muted:#7d786a;
  --line:#37332a; --hair:#2a271f; --accent:#e07840; --accent-soft:#e07840;
  --buy:#7cc282; --warn:#dfa04a; --exit:#e07a6a; --chip:#26221a;
}}
:root[data-theme="light"]{
  --paper:#f4efe4; --card:#faf7ee; --ink:#17150f; --ink2:#5c574a; --muted:#8a8474;
  --line:#d9d2bf; --hair:#e4ddca; --accent:#b34a17; --accent-soft:#c65d2e;
  --buy:#2c6e31; --warn:#a05a00; --exit:#a63a2c; --chip:#eee8d8;
}
:root[data-theme="dark"]{
  --paper:#16140f; --card:#1d1a13; --ink:#eae4d3; --ink2:#a39d8c; --muted:#7d786a;
  --line:#37332a; --hair:#2a271f; --accent:#e07840; --accent-soft:#e07840;
  --buy:#7cc282; --warn:#dfa04a; --exit:#e07a6a; --chip:#26221a;
}
*{box-sizing:border-box}
body{background:var(--paper); color:var(--ink); margin:0;
  font:15px/1.55 "Iowan Old Style", Georgia, serif;}
.mono{font-family:"SF Mono", ui-monospace, "Cascadia Mono", Menlo, monospace;}
.wrap{max-width:1080px; margin:0 auto; padding:28px 20px 60px;}
header.blueprint{border:1px solid var(--line); padding:10px 16px; display:flex;
  justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap;
  font-family:ui-monospace, Menlo, monospace; font-size:11px; letter-spacing:.08em;
  text-transform:uppercase; color:var(--ink2);}
header.blueprint .rev{color:var(--accent);}
h1{font:800 clamp(30px,5.5vw,52px)/1.04 "Helvetica Neue", Arial, sans-serif;
  letter-spacing:-.01em; text-transform:uppercase; margin:34px 0 6px;}
p.sub{font-size:19px; color:var(--ink2); margin:0 0 26px; font-variant:small-caps;
  letter-spacing:.04em;}
.tiles{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:10px; margin:20px 0 30px;}
.tile{border:1px solid var(--line); background:var(--card); padding:12px 14px;}
.tile .lbl{font:11px/1.3 ui-monospace,Menlo,monospace; letter-spacing:.08em;
  text-transform:uppercase; color:var(--muted);}
.tile .val{font:600 26px/1.2 "Helvetica Neue", Arial, sans-serif; margin-top:2px;}
.tile .val.buy{color:var(--buy)} .tile .val.warn{color:var(--warn)}
.tile .val.exit{color:var(--exit)}
h2{font:700 13px/1 ui-monospace,Menlo,monospace; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent); margin:38px 0 14px;
  padding-top:14px; border-top:1px solid var(--line);}
.grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:14px;}
.card{border:1px solid var(--line); background:var(--card); padding:14px 16px;
  position:relative;}
.card .corner{position:absolute; top:-1px; right:-1px; border-top:2px solid var(--accent);
  border-right:2px solid var(--accent); width:14px; height:14px;}
.card h3{margin:0; font:700 18px/1.2 "Helvetica Neue", Arial, sans-serif;}
.card .nm{color:var(--muted); font-size:12px; font-family:ui-monospace,Menlo,monospace;
  text-transform:uppercase; letter-spacing:.08em;}
.badge{display:inline-flex; gap:6px; align-items:center; padding:3px 9px;
  font:700 11px/1.4 ui-monospace,Menlo,monospace; letter-spacing:.08em;
  border:1px solid currentColor; text-transform:uppercase;}
.badge.buy{color:var(--buy)} .badge.warn{color:var(--warn)}
.badge.exit{color:var(--exit)} .badge.trend{color:var(--ink2)}
.badge.flat{color:var(--muted)}
.head{display:flex; justify-content:space-between; align-items:start; gap:8px;}
.px{font:600 22px/1.1 "Helvetica Neue", Arial, sans-serif; margin:8px 0 0;}
.px .chg{font-size:13px; margin-left:8px; font-weight:600;}
.chg.up{color:var(--buy)} .chg.dn{color:var(--exit)}
.spark{margin:10px 0 4px; position:relative;}
.spark svg{display:block; width:100%; height:64px;}
.tip{position:absolute; pointer-events:none; background:var(--ink); color:var(--paper);
  font:11px/1.5 ui-monospace,Menlo,monospace; padding:3px 8px; white-space:nowrap;
  transform:translate(-50%,-130%); display:none; z-index:3;}
.lv{width:100%; border-collapse:collapse; font-family:ui-monospace,Menlo,monospace;
  font-size:12px; margin-top:8px;}
.lv td{padding:4px 0; border-top:1px solid var(--hair);
  font-variant-numeric:tabular-nums;}
.lv td:first-child{color:var(--muted); text-transform:uppercase;
  letter-spacing:.06em; font-size:10.5px;}
.lv td:last-child{text-align:right;}
.note{font-size:13px; color:var(--ink2); margin:8px 0 0; font-style:italic;}
table.bt{width:100%; border-collapse:collapse; font-family:ui-monospace,Menlo,monospace;
  font-size:12.5px; background:var(--card); border:1px solid var(--line);}
table.bt th{font-size:10.5px; letter-spacing:.08em; text-transform:uppercase;
  color:var(--muted); font-weight:600; text-align:right; padding:9px 12px;
  border-bottom:1px solid var(--line);}
table.bt th:first-child, table.bt td:first-child{text-align:left;}
table.bt td{padding:7px 12px; border-bottom:1px solid var(--hair); text-align:right;
  font-variant-numeric:tabular-nums;}
table.bt tr:last-child td{border-bottom:none}
.pos{color:var(--buy)} .neg{color:var(--exit)}
.review{border:1px dashed var(--ink2); margin:40px 0 0; padding:16px 20px;
  display:flex; gap:14px; align-items:center;}
.review .eye{font-size:22px; color:var(--accent);}
.review b{font-family:ui-monospace,Menlo,monospace; letter-spacing:.1em;
  text-transform:uppercase; display:block; font-size:12px;}
.review span{font-size:13px; color:var(--ink2);}
footer{margin-top:34px; font:10.5px/1.6 ui-monospace,Menlo,monospace;
  letter-spacing:.08em; text-transform:uppercase; color:var(--muted);
  display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;
  border-top:1px solid var(--line); padding-top:12px;}
.scroll{overflow-x:auto;}
"""

JS = """
document.querySelectorAll('.spark').forEach(function(box){
  var svg = box.querySelector('svg');
  var tip = box.querySelector('.tip');
  var dot = svg.querySelector('.hoverdot');
  var data = JSON.parse(box.dataset.series);
  var pad = 6, W = 320, H = 64;
  var min = Math.min.apply(null, data.c), max = Math.max.apply(null, data.c);
  if (max === min) { max = min + 1; }
  function x(i){ return pad + (W - 2*pad) * i / (data.c.length - 1); }
  function y(v){ return H - pad - (H - 2*pad) * (v - min) / (max - min); }
  svg.addEventListener('mousemove', function(ev){
    var r = svg.getBoundingClientRect();
    var px = (ev.clientX - r.left) / r.width * W;
    var i = Math.round((px - pad) / (W - 2*pad) * (data.c.length - 1));
    i = Math.max(0, Math.min(data.c.length - 1, i));
    dot.setAttribute('cx', x(i)); dot.setAttribute('cy', y(data.c[i]));
    dot.style.display = 'block';
    tip.style.display = 'block';
    tip.style.left = (x(i) / W * 100) + '%';
    tip.style.top = (y(data.c[i]) / H * 100) + '%';
    tip.textContent = data.d[i] + ' \\u00b7 ' + data.c[i].toLocaleString(
      undefined, {maximumFractionDigits: 2});
  });
  svg.addEventListener('mouseleave', function(){
    tip.style.display = 'none'; dot.style.display = 'none';
  });
});
"""


def _fmt(x: float, nd: int = 2) -> str:
    return f"{x:,.{nd}f}"


def _spark(s: Signal) -> str:
    W, H, pad = 320, 64, 6
    cs = s.closes
    lo, hi = min(cs), max(cs)
    if hi == lo:
        hi = lo + 1

    def x(i):
        return pad + (W - 2 * pad) * i / (len(cs) - 1)

    def y(v):
        return H - pad - (H - 2 * pad) * (v - lo) / (hi - lo)

    pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(cs))
    area = f"M{pad},{H - pad} L{pts.replace(' ', ' L')} L{W - pad},{H - pad} Z"
    trig_line = ""
    if lo <= s.resistance <= hi:
        ty = y(s.resistance)
        trig_line = (f'<line x1="{pad}" y1="{ty:.1f}" x2="{W - pad}" y2="{ty:.1f}" '
                     f'stroke="var(--accent)" stroke-width="1" opacity="0.65"/>')
    series = json.dumps({"c": [round(v, 2) for v in cs], "d": s.dates},
                        separators=(",", ":"))
    return f'''<div class="spark" data-series='{series}'>
  <svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" role="img"
       aria-label="{s.symbol} 60-day closing price line">
    <path d="{area}" fill="var(--accent-soft)" opacity="0.10"/>
    {trig_line}
    <polyline points="{pts}" fill="none" stroke="var(--ink)" stroke-width="2"
      stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>
    <circle cx="{x(len(cs) - 1):.1f}" cy="{y(cs[-1]):.1f}" r="4"
      fill="var(--accent)" stroke="var(--card)" stroke-width="2"/>
    <circle class="hoverdot" r="4" fill="var(--accent)" stroke="var(--card)"
      stroke-width="2" style="display:none"/>
  </svg>
  <div class="tip"></div>
</div>'''


def _card(s: Signal) -> str:
    cls = STATE_CLASS[s.state]
    chg_cls = "up" if s.change_1d >= 0 else "dn"
    targets = " · ".join(f"{lbl} {_fmt(px)}" for lbl, px in s.targets) or "n/a"
    rows = [
        ("Entry trigger", _fmt(s.resistance)),
        ("Stop loss", _fmt(s.stop)),
        ("Support 20d", _fmt(s.support)),
        ("Targets", targets),
        ("Dist to trigger", f"{s.dist_to_trigger_pct:+.1f}%"),
        ("Volume vs 20d", f"{s.volume_ratio:.1f}x"),
        ("RSI 14", f"{s.rsi14:.0f}"),
        ("Size @ 1% risk", f"{s.size_label} ≈ ${s.shares * s.entry:,.0f}"),
    ]
    trs = "\n".join(f"<tr><td>{html.escape(k)}</td><td>{html.escape(v)}</td></tr>"
                    for k, v in rows)
    return f'''<div class="card">
  <div class="corner"></div>
  <div class="head">
    <div><h3>{s.symbol}</h3><div class="nm">{html.escape(s.name)} · {s.asset_class}</div></div>
    <span class="badge {cls}">{STATE_ICON[s.state]} {html.escape(s.state)}</span>
  </div>
  <p class="px">{_fmt(s.close)}<span class="chg {chg_cls}">{s.change_1d:+.2f}% 1d</span></p>
  {_spark(s)}
  <table class="lv">{trs}</table>
  <p class="note">{html.escape(s.note)}</p>
</div>'''


def build(signals: list[Signal], stats: dict[str, Stats], run_date: str,
          account_size: float, risk_pct: float) -> str:
    signals = sorted(signals, key=lambda s: STATE_ORDER.index(s.state))
    n_buy = sum(1 for s in signals if s.state == BUY)
    n_watch = sum(1 for s in signals if s.state in (WATCH, BREAKOUT_UNCONFIRMED))
    n_exit = sum(1 for s in signals if s.state == EXIT)
    n_up = sum(1 for s in signals if s.above_trend)

    cards = "\n".join(_card(s) for s in signals)

    bt_rows = []
    for s in signals:
        st = stats.get(s.symbol)
        if not st:
            continue
        pf = "∞" if st.profit_factor >= 999 else f"{st.profit_factor:.2f}"
        ret_cls = "pos" if st.total_return_pct >= 0 else "neg"
        bt_rows.append(
            f"<tr><td>{s.symbol}</td><td>{st.trades}</td><td>{st.win_rate:.0f}%</td>"
            f"<td>{st.avg_r:+.2f}</td><td class='{ret_cls}'>{st.total_return_pct:+.1f}%</td>"
            f"<td>{st.max_drawdown_pct:.1f}%</td><td>{pf}</td></tr>")

    return f'''<title>Fable Rules — Daily Signals</title>
<style>{CSS}</style>
<div class="wrap">
  <header class="blueprint">
    <span>✳ Fable Rules × TradingView</span>
    <span>Doc: AI-Trading-Integration · Type: Daily Signals</span>
    <span class="rev">Run {run_date}</span>
  </header>

  <h1>Where the rules<br>say to act.</h1>
  <p class="sub">Breakout entries, stops and targets — recomputed daily. Human review required.</p>

  <div class="tiles">
    <div class="tile"><div class="lbl">Buy signals today</div>
      <div class="val {'buy' if n_buy else ''}">{n_buy}</div></div>
    <div class="tile"><div class="lbl">Setups on watch</div>
      <div class="val {'warn' if n_watch else ''}">{n_watch}</div></div>
    <div class="tile"><div class="lbl">Exit signals</div>
      <div class="val {'exit' if n_exit else ''}">{n_exit}</div></div>
    <div class="tile"><div class="lbl">Above 50-day trend</div>
      <div class="val">{n_up}/{len(signals)}</div></div>
    <div class="tile"><div class="lbl">Risk per trade</div>
      <div class="val">{risk_pct:g}% · ${account_size * risk_pct / 100:,.0f}</div></div>
  </div>

  <h2>01 · Signal board</h2>
  <div class="grid">
{cards}
  </div>

  <h2>02 · Rule backtest — last ~12 months (indicative, no fees/slippage)</h2>
  <div class="scroll">
  <table class="bt">
    <thead><tr><th>Symbol</th><th>Trades</th><th>Win rate</th><th>Avg R</th>
      <th>Total return</th><th>Max DD</th><th>Profit factor</th></tr></thead>
    <tbody>{"".join(bt_rows)}</tbody>
  </table>
  </div>

  <div class="review">
    <span class="eye">◉</span>
    <div><b>Human review required</b>
    <span>Signals are generated by fixed rules on end-of-day data. This is research
    output, not financial advice. Verify levels on your own chart before placing
    any order. Responsibility is yours.</span></div>
  </div>

  <footer>
    <span>Grid: 8pt · Baseline: 4pt · Origin: (0,0)</span>
    <span>Account basis ${account_size:,.0f} · Rules in tradebot/ · Pine mirror in pine/</span>
  </footer>
</div>
<script>{JS}</script>
'''
