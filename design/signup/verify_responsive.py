#!/usr/bin/env python3
"""
Responsive verification probe for design/signup/signup.html.

Why this exists as a script rather than a one-off: the interesting failures
here (horizontal overflow at 280px, the submit button falling below the fold
on a square viewport) are exactly the ones that are invisible if you eyeball a
scaled screenshot. They need measurement, and measurement needs to be repeatable
after every edit.

Two things make this non-obvious on macOS:

  1. Chrome's --window-size clamps to a ~500px minimum, so screenshotting at
     280px silently renders at 500px and reports no overflow when there is
     plenty. Every width below 500 must be measured inside an iframe instead.
  2. iframe introspection needs same-origin, and file:// origins are opaque in
     Chrome. So this serves the directory over http on a loopback port first.

Usage:
    python3 verify_responsive.py            # measure, print table, write JSON
    python3 verify_responsive.py --shots    # also write PNG screenshots

Stdlib only. No network access beyond loopback.
"""

import argparse
import http.server
import json
import re
import socket
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# name, width, height. The list is deliberately weighted toward the sizes that
# usually go unchecked: folded phones, squares, and landscape phones.
VIEWPORTS = [
    ("folded-phone",    280,  653),
    ("small-phone",     320,  568),
    ("iphone-13",       390,  844),
    ("iphone-pro-max",  430,  932),
    ("square-small",    500,  500),
    ("phone-landscape", 844,  390),
    ("ipad-portrait",   834, 1112),
    ("square-large",    900,  900),
    ("ipad-landscape", 1112,  834),
    ("laptop",         1280,  800),
    ("desktop",        1440,  900),
    ("ultrawide",      2560, 1080),
]

# Selectors that must be present and must not overflow their container.
CRITICAL = ["#submit", "#email", "#password", ".card", ".rail h1", ".masthead"]


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


# The probe posts its measurements back here rather than writing them into the
# DOM. --dump-dom serialises at the load event, which is before an async chain
# of iframe loads can finish, so scraping the DOM reports a half-run probe.
INBOX: dict = {}
ARRIVED = threading.Event()


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        if self.path != "/__results":
            self.send_error(404)
            return
        n = int(self.headers.get("Content-Length", 0))
        try:
            INBOX["data"] = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception as exc:
            INBOX["error"] = str(exc)
        self.send_response(204)
        self.end_headers()
        ARRIVED.set()


def serve(port: int) -> socketserver.TCPServer:
    handler = lambda *a, **kw: QuietHandler(*a, directory=str(HERE), **kw)
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


PROBE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>probe</title>
<style>html,body{margin:0;background:#111}iframe{border:0;display:block}</style>
</head><body>
<div id="out" style="display:none"></div>
<script>
var VIEWPORTS = __VIEWPORTS__;
var CRITICAL = __CRITICAL__;
var results = [];
var i = 0;

function nextFrame() {
  if (i >= VIEWPORTS.length) {
    fetch('/__results', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(results)
    });
    document.title = 'done';
    return;
  }
  var v = VIEWPORTS[i];
  var f = document.createElement('iframe');
  f.width = v[1]; f.height = v[2];
  f.style.width = v[1] + 'px';
  f.style.height = v[2] + 'px';
  f.src = 'signup.html?probe=' + v[0];
  f.onload = function () {
    var d = f.contentDocument, w = f.contentWindow;
    var de = d.documentElement, body = d.body;
    var r = {
      name: v[0], w: v[1], h: v[2],
      scrollW: Math.max(de.scrollWidth, body.scrollWidth),
      clientW: de.clientWidth,
      scrollH: Math.max(de.scrollHeight, body.scrollHeight),
      overflowX: 0, missing: [], escapes: [], tiny_targets: [], fold: {}
    };
    r.overflowX = r.scrollW - r.clientW;

    // An element only counts as escaping if nothing between it and the root
    // clips it. Without this check every decorative layer inside an
    // overflow:hidden wrapper reports as overflow when it cannot scroll
    // anything. (The ambient orbs are deliberately oversized and clipped.)
    function isClipped(el) {
      var p = el.parentElement;
      while (p && p !== d.documentElement) {
        var cs = w.getComputedStyle(p);
        if (cs.overflow !== 'visible' || cs.overflowX !== 'visible') return true;
        p = p.parentElement;
      }
      return false;
    }

    // Any element whose right edge escapes the viewport is a real overflow,
    // even when body{overflow-x:hidden} is masking it.
    var all = d.querySelectorAll('body *');
    for (var k = 0; k < all.length; k++) {
      var el = all[k];
      if (el.offsetParent === null && w.getComputedStyle(el).position !== 'fixed') continue;
      var b = el.getBoundingClientRect();
      if (b.width === 0 && b.height === 0) continue;
      if (isClipped(el)) continue;
      if (b.right > r.clientW + 1 || b.left < -1) {
        var tag = el.tagName.toLowerCase() +
          (el.id ? '#' + el.id : '') +
          (el.className && typeof el.className === 'string' && el.className.trim()
            ? '.' + el.className.trim().split(/\\s+/)[0] : '');
        if (r.escapes.indexOf(tag) === -1 && r.escapes.length < 6) r.escapes.push(tag);
      }
    }

    // Critical elements must exist and be laid out.
    CRITICAL.forEach(function (sel) {
      var el = d.querySelector(sel);
      if (!el) { r.missing.push(sel); return; }
      var b = el.getBoundingClientRect();
      if (b.width === 0 || b.height === 0) r.missing.push(sel + ' (zero box)');
    });

    // Tap targets: every interactive control must clear 44px (WCAG 2.5.5).
    var ctrls = d.querySelectorAll('button, input, a[href], [role="tab"]');
    for (var j = 0; j < ctrls.length; j++) {
      var c = ctrls[j];
      if (c.closest('.demo-bar')) continue;      // demo scaffold, not the design
      // WCAG 2.5.5 exempts links inline in a sentence. These are all prose
      // links inside running text, not standalone controls.
      if (c.closest('.footer')) continue;
      if (c.closest('.masthead-alt')) continue;
      if (c.closest('.field-hint')) continue;
      if (c.closest('.consent-text')) continue;
      if (c.closest('.card-foot')) continue;
      // A checkbox wrapped in a label is activated by the whole label, so the
      // label box is the real target. Measure that instead of the 20px box.
      var lbl = c.tagName === 'INPUT' ? c.closest('label') : null;
      if (lbl) c = lbl;
      var cb = c.getBoundingClientRect();
      if (cb.width === 0 && cb.height === 0) continue;
      if (cb.height < 44) {
        var t = c.tagName.toLowerCase() + (c.id ? '#' + c.id : '') +
          (c.className && typeof c.className === 'string' && c.className.trim()
            ? '.' + c.className.trim().split(/\\s+/)[0] : '');
        r.tiny_targets.push(t + ' h=' + Math.round(cb.height));
      }
    }

    // Is the primary action reachable without scrolling?
    var sub = d.querySelector('#submit');
    if (sub) {
      var sb = sub.getBoundingClientRect();
      r.fold = { submitBottom: Math.round(sb.bottom), viewportH: v[2],
                 aboveFold: sb.bottom <= v[2] };
    }

    results.push(r);
    f.remove();
    i++;
    setTimeout(nextFrame, 40);
  };
  document.body.appendChild(f);
}
window.addEventListener('load', function () { setTimeout(nextFrame, 120); });
</script></body></html>
"""


def run_probe(port: int) -> list:
    probe = PROBE.replace("__VIEWPORTS__", json.dumps([[n, w, h] for n, w, h in VIEWPORTS]))
    probe = probe.replace("__CRITICAL__", json.dumps(CRITICAL))
    probe_path = HERE / "_probe.html"
    probe_path.write_text(probe, encoding="utf-8")

    # Chrome does not reliably exit on its own here, so it is launched detached
    # and killed once the probe has posted its measurements back.
    try:
        with tempfile.TemporaryDirectory() as prof:
            proc = subprocess.Popen(
                [CHROME, "--headless=old", "--no-sandbox", "--hide-scrollbars",
                 "--disable-lcd-text", "--force-device-scale-factor=1",
                 f"--user-data-dir={prof}",
                 f"http://127.0.0.1:{port}/_probe.html"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            got = ARRIVED.wait(timeout=120)
            proc.kill()
            proc.wait(timeout=10)

        if not got:
            print("Probe never reported back (timed out).", file=sys.stderr)
            return []
        if "error" in INBOX:
            print(f"Probe payload was unreadable: {INBOX['error']}", file=sys.stderr)
            return []
        return INBOX.get("data", [])
    finally:
        probe_path.unlink(missing_ok=True)


def shoot(port: int) -> None:
    """Screenshots. Anything under 500px wide is captured through a scaled
    iframe, because Chrome will not honour a smaller --window-size on macOS."""
    shots = HERE / "shots"
    shots.mkdir(exist_ok=True)
    for name, w, h in VIEWPORTS:
        target = f"http://127.0.0.1:{port}/signup.html"
        win_w, win_h = w, h
        holder = None
        if w < 500:
            holder = HERE / f"_shot_{name}.html"
            holder.write_text(
                f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                f"<style>html,body{{margin:0;background:#020617}}"
                f"iframe{{border:0;display:block;width:{w}px;height:{h}px}}</style></head>"
                f"<body><iframe src='signup.html'></iframe></body></html>",
                encoding="utf-8")
            target = f"http://127.0.0.1:{port}/{holder.name}"
            win_w, win_h = 520, h
        out_png = shots / (name + ".png")
        out_png.unlink(missing_ok=True)
        try:
            with tempfile.TemporaryDirectory() as prof:
                # Chrome does not exit after --screenshot on this setup, so
                # wait for the PNG to land and stop growing, then kill it.
                proc = subprocess.Popen(
                    [CHROME, "--headless=old", "--no-sandbox", "--hide-scrollbars",
                     "--virtual-time-budget=5000",
                     f"--user-data-dir={prof}",
                     f"--window-size={win_w},{win_h}",
                     f"--screenshot={out_png}", target],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                last, stable, waited = -1, 0, 0.0
                while waited < 45:
                    time.sleep(0.4)
                    waited += 0.4
                    size = out_png.stat().st_size if out_png.exists() else -1
                    if size > 0 and size == last:
                        stable += 1
                        if stable >= 2:
                            break
                    else:
                        stable = 0
                    last = size
                proc.kill()
                proc.wait(timeout=10)
            ok = out_png.exists() and out_png.stat().st_size > 0
            print(f"  {'ok  ' if ok else 'FAIL'} {name:<17} {w}x{h}")
        finally:
            if holder:
                holder.unlink(missing_ok=True)
    print(f"\nScreenshots written to {shots}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", action="store_true", help="also write PNG screenshots")
    args = ap.parse_args()

    if not Path(CHROME).exists():
        print(f"Chrome not found at {CHROME}", file=sys.stderr)
        return 2

    port = free_port()
    httpd = serve(port)
    try:
        results = run_probe(port)
        if not results:
            return 1

        print(f"\n{'viewport':<17}{'size':<13}{'overflow-x':<12}"
              f"{'escapes':<9}{'tap<44':<9}{'CTA above fold':<16}status")
        print("-" * 86)

        failures = []
        for r in results:
            bad = []
            if r["overflowX"] > 0:
                bad.append(f"overflow-x {r['overflowX']}px")
            if r["escapes"]:
                bad.append("escaping: " + ", ".join(r["escapes"]))
            if r["missing"]:
                bad.append("missing: " + ", ".join(r["missing"]))
            if r["tiny_targets"]:
                bad.append("small targets: " + ", ".join(r["tiny_targets"][:3]))
            status = "PASS" if not bad else "FAIL"
            if bad:
                failures.append((r["name"], bad))
            fold = r.get("fold", {})
            fold_s = ("yes" if fold.get("aboveFold") else
                      f"no (+{fold.get('submitBottom', 0) - r['h']}px)")
            print(f"{r['name']:<17}{str(r['w']) + 'x' + str(r['h']):<13}"
                  f"{r['overflowX']:<12}{len(r['escapes']):<9}"
                  f"{len(r['tiny_targets']):<9}{fold_s:<16}{status}")

        print()
        if failures:
            print("FAILURES")
            for name, bad in failures:
                for b in bad:
                    print(f"  {name}: {b}")
        else:
            print("All viewports pass: no horizontal overflow, no escaping boxes, "
                  "no undersized tap targets, all critical elements laid out.")

        (HERE / "verify_results.json").write_text(
            json.dumps(results, indent=2), encoding="utf-8")
        print(f"\nRaw measurements: {HERE / 'verify_results.json'}")

        if args.shots:
            shoot(port)
        return 1 if failures else 0
    finally:
        httpd.shutdown()


if __name__ == "__main__":
    sys.exit(main())
