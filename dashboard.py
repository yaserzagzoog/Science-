#!/usr/bin/env python3
"""Local web dashboard — run it next to the bot on the same machine:

    python3 dashboard.py                     # http://localhost:8777
    python3 dashboard.py config.forex.json 8778

Shows live equity, day P&L vs the profit-lock/target/stop levels, open
positions, halt status, and the log tail. Buttons: STOP (creates the
kill-switch file the bot honors) and RESUME (removes it).

Binds to 127.0.0.1 only — it is private to the machine. To view it from
your phone/laptop when the bot runs on a VPS, use an SSH tunnel:

    ssh -L 8777:localhost:8777 user@your-vps
"""

import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from trader.config import Config

CFG_PATH = "config.json"
LOG_FILE = "bot.log"

PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trading Bot</title>
<style>
:root{--bg:#0f1420;--card:#1a2233;--text:#e6ecf5;--dim:#8fa0b8;
--green:#38c172;--red:#e3564f;--amber:#e0a83b;--line:#2a3550}
*{box-sizing:border-box;margin:0}
body{background:var(--bg);color:var(--text);
font:15px/1.5 system-ui,-apple-system,sans-serif;padding:16px;max-width:760px;margin:0 auto}
h1{font-size:18px;margin:4px 0 14px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
.lbl{color:var(--dim);font-size:12px;text-transform:uppercase;letter-spacing:.04em}
.val{font-size:22px;font-weight:600;margin-top:2px;font-variant-numeric:tabular-nums}
.pos .val{font-size:15px;font-weight:400}
.up{color:var(--green)}.down{color:var(--red)}.warn{color:var(--amber)}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}
td,th{padding:6px 8px;text-align:right;border-bottom:1px solid var(--line);font-size:14px}
td:first-child,th:first-child{text-align:left}
th{color:var(--dim);font-weight:500;font-size:12px}
#log{background:#0a0e17;border:1px solid var(--line);border-radius:10px;padding:10px;
font:12px/1.6 ui-monospace,monospace;white-space:pre-wrap;max-height:280px;
overflow-y:auto;color:#a9b7cc;overflow-x:auto}
.btns{display:flex;gap:10px;margin:14px 0}
button{flex:1;padding:12px;border-radius:10px;border:0;font-size:15px;font-weight:600;cursor:pointer}
#stop{background:var(--red);color:#fff}#resume{background:var(--card);color:var(--text);
border:1px solid var(--line)}
.banner{border-radius:10px;padding:10px 12px;margin-bottom:12px;display:none;font-weight:500}
.banner.show{display:block}
.banner.halted{background:#3a2426;color:#f0b7b3;border:1px solid #5c3234}
.banner.stale{background:#3a3224;color:#ecd9a8;border:1px solid #5c5234}
section{margin-top:16px}
</style></head><body>
<h1>Trading Bot <span id="meta" class="lbl"></span></h1>
<div id="stopped" class="banner halted"></div>
<div id="stale" class="banner stale"></div>
<div class="grid">
<div class="card"><div class="lbl">Equity</div><div class="val" id="equity">–</div></div>
<div class="card"><div class="lbl">Day P&amp;L</div><div class="val" id="daypnl">–</div></div>
<div class="card"><div class="lbl">Day peak</div><div class="val" id="peak">–</div></div>
<div class="card"><div class="lbl">Profit floor</div><div class="val" id="floor">–</div></div>
</div>
<div class="btns">
<button id="stop" onclick="act('stop')">STOP BOT</button>
<button id="resume" onclick="act('resume')">RESUME</button>
</div>
<section class="card pos"><div class="lbl">Open positions</div>
<table id="positions"><tbody></tbody></table></section>
<section><div class="lbl" style="margin-bottom:6px">Log</div><div id="log">waiting…</div></section>
<script>
const $=id=>document.getElementById(id);
const fmt=(v,d=2)=>v==null?'–':Number(v).toFixed(d);
const cls=v=>v>0?'up':(v<0?'down':'');
async function act(a){await fetch('/api/'+a,{method:'POST'});refresh()}
async function refresh(){
 try{
  const r=await fetch('/api/state');const s=await r.json();
  $('meta').textContent=s.platform+' · '+s.mode+' · '+s.strategy;
  $('equity').textContent=fmt(s.equity);
  $('daypnl').textContent=(s.day_pct>0?'+':'')+fmt(s.day_pct)+'%';
  $('daypnl').className='val '+cls(s.day_pct);
  $('peak').textContent=(s.peak>0?'+':'')+fmt(s.peak)+'%';
  $('floor').textContent=s.floor==null?'not active':'+'+fmt(s.floor)+'%';
  $('floor').className='val '+(s.floor==null?'':'up');
  const halted=s.kill_switch?'Kill switch file present — bot stopped.':(s.halted?('Halted: '+s.halt_reason):null);
  $('stopped').textContent=halted||'';$('stopped').className='banner halted'+(halted?' show':'');
  $('stale').textContent='No update from bot for '+s.age+'s — is it running?';
  $('stale').className='banner stale'+(s.age!=null&&s.age>180?' show':'');
  let rows='<tr><th>Symbol</th><th>Qty</th><th>Entry</th><th>Now</th><th>P&L %</th></tr>';
  const ps=Object.entries(s.positions||{});
  if(!ps.length)rows+='<tr><td colspan=5 style="color:var(--dim)">none — in cash</td></tr>';
  for(const[sym,p]of ps){
   const now=(s.prices||{})[sym];
   const pct=now?((now/p.entry_price-1)*100):null;
   rows+=`<tr><td>${sym}</td><td>${p.qty}</td><td>${fmt(p.entry_price,4)}</td>
   <td>${fmt(now,4)}</td><td class="${cls(pct)}">${pct==null?'–':(pct>0?'+':'')+fmt(pct)+'%'}</td></tr>`;
  }
  $('positions').innerHTML=rows;
  $('log').textContent=s.log||'(no log file found — start the bot with: python3 run_bot.py > bot.log 2>&1)';
 }catch(e){$('stale').textContent='Dashboard cannot reach its server.';$('stale').className='banner stale show'}
}
refresh();setInterval(refresh,5000);
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    cfg = None

    def log_message(self, *args):   # silence request spam
        pass

    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            return self._send(200, PAGE, "text/html; charset=utf-8")
        if self.path == "/api/state":
            return self._send(200, json.dumps(self.state()))
        self._send(404, "{}")

    def do_POST(self):
        cfg = self.cfg
        if self.path == "/api/stop":
            with open(cfg.kill_switch_file, "w") as fh:
                fh.write("stopped from dashboard\n")
            return self._send(200, '{"ok":true}')
        if self.path == "/api/resume":
            if os.path.exists(cfg.kill_switch_file):
                os.remove(cfg.kill_switch_file)
            return self._send(200, '{"ok":true}')
        self._send(404, "{}")

    def state(self):
        cfg = self.cfg
        st = {}
        if os.path.exists(cfg.state_file):
            try:
                with open(cfg.state_file) as fh:
                    st = json.load(fh)
            except (json.JSONDecodeError, OSError):
                pass
        equity = st.get("last_equity")
        start = st.get("day_start_equity")
        day_pct = (equity - start) / start * 100 if equity and start else 0.0
        peak = st.get("day_peak_pct", 0.0)
        floor = None
        if peak >= cfg.daily_min_lock_pct:
            floor = max(cfg.daily_min_lock_pct, peak - cfg.daily_giveback_pct)
        last = st.get("last_update")
        log_tail = ""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "rb") as fh:
                fh.seek(0, 2)
                fh.seek(max(0, fh.tell() - 8000))
                log_tail = fh.read().decode(errors="replace")
                log_tail = "\n".join(log_tail.splitlines()[-60:])
        return {
            "platform": cfg.platform, "mode": cfg.mode, "strategy": cfg.strategy,
            "equity": equity, "day_pct": round(day_pct, 3), "peak": peak,
            "floor": floor, "positions": st.get("positions", {}),
            "prices": st.get("last_prices", {}),
            "halted": st.get("halted", False),
            "halt_reason": st.get("halt_reason", ""),
            "kill_switch": os.path.exists(cfg.kill_switch_file),
            "age": (int(time.time()) - last) if last else None,
            "log": log_tail,
        }


def main():
    args = sys.argv[1:]
    cfg_path = args[0] if args and not args[0].isdigit() else CFG_PATH
    port = int(args[-1]) if args and args[-1].isdigit() else 8777
    Handler.cfg = Config.load(cfg_path)
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"dashboard for {cfg_path} at http://localhost:{port}  (Ctrl-C to quit)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
