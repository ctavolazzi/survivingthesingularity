#!/usr/bin/env python3
"""Render the factcheck JSON inventory into one self-contained HTML trace.

Consumes what `sts.py factcheck --out` produces and emits a single file that
opens from file:// with no network of any kind: no CDN, no font fetch, no
XHR. Inline everything or do not ship it.

Why this is not a verb on sts.py: sts.py is the project API and is stdlib
only, single file, measurement oriented. A thousand lines of HTML template
is a rendering concern and does not belong in the measurement tool. sts.py
owns the numbers; this owns the page.

The page never hardcodes a count. Every number it displays is computed in
the browser from the embedded records, so the page cannot drift from its
own data.

Usage:
    python3 scripts/build_factcheck_trace.py docs/factcheck-2026-07-30.json \
            docs/factcheck-trace-2026-07-30.html
"""

import json
import sys
from pathlib import Path

# The long dash, written as a code point so this file can enforce the no-long-dash
# house rule without containing the character it bans.
LONG_DASH = chr(8212)


def trim(report):
    """Only the fields the page actually renders. Keeps the inline payload
    small enough to stay a single portable file."""
    out = []
    for c in report["claims"]:
        g = c["git"]
        rec = {
            "i": c["seq"],
            "q": c["claim"][:600],
            "t": c["type"],
            "s": c["section"],
            "st": c["section_title"],
            "f": c["file"],
            "ln": c["line"],
            "b": c["block_id"],
            "bt": c["block_type"],
            "bl": c["block_lines"],
            "bh": c.get("block_hash"),
            "v": c["verdict"],
            "n": c["note"],
            "rs": g["receipt_state"],
            "rr": g["reason"],
            "sha": g["short"],
            "au": g["author"],
            "dt": g["date"],
            # Commit subjects are historical strings and some carry an em dash,
            # which the house style bars from generated output. Normalise the
            # punctuation only, never the words, and say so on the page. The SHA
            # stays authoritative: anyone can read the true subject from it.
            "sm": (g["summary"] or "").replace(LONG_DASH, "-") or None,
            "pl": g["permalink"],
            "ls": g["link_state"],
        }
        for k in ("url", "host", "in_works_cited", "bare_wikipedia",
                  "xref_kind", "target", "resolved", "image", "art_id",
                  "on_disk", "in_catalog", "comparison_claim",
                  "has_citation_nearby", "years", "source_state"):
            if k in c:
                rec[k] = c[k]
        out.append(rec)
    return out


def build(report):
    payload = {
        "generated": report["generated"],
        "repo": report["repo"],
        "repo_public": report["repo_public"],
        "book_version": report["book_version"],
        "network": report["network"],
        "totals": report["totals"],
        "targets": report["targets"],
        "not_covered": report["not_covered"],
        "git": report["git"],
        "claims": trim(report),
    }
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return HTML.replace("__DATA__", data)


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Surviving the Singularity: chain of custody</title>
<style>
:root{
  --bg:#020617; --panel:#0b1327; --panel2:#111c36; --line:#1e2b4d;
  --ink:#f1f5f9; --mut:#94a3b8; --dim:#64748b;
  --amber:#f59e0b; --blue:#3b82f6; --green:#34d399; --red:#f87171;
  --violet:#a78bfa; --slate:#64748b;
  --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:"Inter",system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:var(--sans)}
body{line-height:1.6;overflow-x:hidden}
a{color:var(--blue)}
.wrap{max-width:1200px;margin:0 auto;padding:0 20px}

/* header */
header{border-bottom:1px solid var(--line);padding:44px 0 30px;background:
  radial-gradient(1000px 340px at 12% -60px,rgba(245,158,11,.13),transparent 62%),
  radial-gradient(800px 300px at 88% -40px,rgba(59,130,246,.10),transparent 62%)}
.kick{font-family:var(--mono);font-size:11px;letter-spacing:.20em;text-transform:uppercase;color:var(--amber)}
h1{font-size:clamp(28px,4.6vw,50px);line-height:1.08;margin:12px 0 10px;letter-spacing:-.02em;font-weight:800}
.sub{color:var(--mut);max-width:70ch;font-size:16px;margin:0}
.asof{font-family:var(--mono);font-size:12px;color:var(--dim);margin-top:14px}

.banner{margin-top:22px;border:1px solid rgba(245,158,11,.42);background:rgba(245,158,11,.07);
  border-radius:12px;padding:14px 16px;display:flex;gap:12px;align-items:flex-start}
.banner .dot{width:9px;height:9px;border-radius:50%;background:var(--amber);margin-top:7px;flex:none;
  box-shadow:0 0 0 0 rgba(245,158,11,.55);animation:pulse 2.4s infinite}
@keyframes pulse{70%{box-shadow:0 0 0 12px rgba(245,158,11,0)}100%{box-shadow:0 0 0 0 rgba(245,158,11,0)}}
.banner b{color:var(--amber)}
.banner p{margin:0;font-size:14px;color:var(--mut)}

/* tiles */
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));gap:12px;margin:26px 0 0}
.tile{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:15px 16px}
.tile .num{font-family:var(--mono);font-size:27px;font-weight:700;letter-spacing:-.02em}
.tile .lab{font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.10em;margin-top:3px}
.tile.ok .num{color:var(--green)} .tile.warn .num{color:var(--amber)}
.tile.bad .num{color:var(--red)} .tile.info .num{color:var(--blue)}
.tile.neutral .num{color:var(--ink)} .tile.violet .num{color:var(--violet)}

section{padding:44px 0;border-bottom:1px solid var(--line)}
h2{font-size:23px;margin:0 0 6px;letter-spacing:-.01em}
.lede{color:var(--mut);margin:0 0 22px;max-width:78ch;font-size:15px}

/* coverage */
.cov{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:12px}
.cov .card{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--red);
  border-radius:10px;padding:14px 16px}
.cov .card h4{margin:0 0 6px;font-size:14px;color:var(--red);font-family:var(--mono);
  text-transform:uppercase;letter-spacing:.07em}
.cov .card p{margin:0;font-size:13.5px;color:var(--mut)}

.bars{display:flex;flex-direction:column;gap:9px;margin-top:6px}
.bar{display:grid;grid-template-columns:168px 1fr 74px;gap:12px;align-items:center;font-size:13px}
.bar .nm{font-family:var(--mono);color:var(--mut);font-size:12px}
.bar .tr{height:9px;background:var(--panel2);border-radius:6px;overflow:hidden}
.bar .fl{height:100%;width:0;border-radius:6px;transition:width 1.1s cubic-bezier(.22,1,.36,1)}
.bar .vl{font-family:var(--mono);text-align:right;color:var(--mut);font-size:12px}

/* controls */
.controls{position:sticky;top:0;z-index:40;background:rgba(2,6,23,.94);
  backdrop-filter:blur(9px);border-bottom:1px solid var(--line);padding:12px 0}
.crow{display:flex;gap:9px;flex-wrap:wrap;align-items:center}
input[type=search],select{background:var(--panel);border:1px solid var(--line);color:var(--ink);
  border-radius:9px;padding:8px 11px;font-size:13px;font-family:var(--sans);min-width:0}
input[type=search]{flex:1 1 240px}
select{font-family:var(--mono);font-size:12px}
input[type=search]:focus,select:focus{outline:2px solid rgba(59,130,246,.55);outline-offset:1px}
.count{font-family:var(--mono);font-size:12px;color:var(--mut);margin-left:auto;white-space:nowrap}
.btn{background:var(--panel);border:1px solid var(--line);color:var(--mut);border-radius:9px;
  padding:8px 12px;font-size:12px;font-family:var(--mono);cursor:pointer}
.btn:hover{border-color:var(--blue);color:var(--ink)}

/* claim rows */
.rows{display:flex;flex-direction:column;gap:7px;margin-top:16px}
.row{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:11px 13px;
  cursor:pointer;display:grid;grid-template-columns:88px 1fr auto;gap:12px;align-items:center;
  transition:border-color .16s,transform .16s}
.row:hover{border-color:var(--blue);transform:translateX(2px)}
.row:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.row .ty{font-family:var(--mono);font-size:10px;text-transform:uppercase;letter-spacing:.06em;
  color:var(--dim);border:1px solid var(--line);border-radius:5px;padding:3px 5px;text-align:center}
.row .qq{font-size:13.5px;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.row .qq small{color:var(--dim);font-family:var(--mono);font-size:11px;margin-left:8px}
.vd{font-family:var(--mono);font-size:10px;padding:3px 7px;border-radius:5px;letter-spacing:.05em;white-space:nowrap}
.vd.SUPPORTED{background:rgba(52,211,153,.13);color:var(--green);border:1px solid rgba(52,211,153,.34)}
.vd.PARTIAL{background:rgba(245,158,11,.13);color:var(--amber);border:1px solid rgba(245,158,11,.34)}
.vd.UNCHECKED{background:rgba(148,163,184,.11);color:var(--mut);border:1px solid rgba(148,163,184,.28)}
.vd.UNCHECKABLE{background:rgba(167,139,250,.13);color:var(--violet);border:1px solid rgba(167,139,250,.34)}
.vd.CONTRADICTED{background:rgba(248,113,113,.14);color:var(--red);border:1px solid rgba(248,113,113,.36)}
.vd.UNSUPPORTED{background:rgba(248,113,113,.10);color:var(--red);border:1px solid rgba(248,113,113,.28)}
.more{text-align:center;margin-top:16px}
.trunc{font-family:var(--mono);font-size:12px;color:var(--amber);text-align:center;margin-top:12px}

/* drawer */
.scrim{position:fixed;inset:0;background:rgba(2,6,23,.72);opacity:0;pointer-events:none;
  transition:opacity .24s;z-index:60}
.scrim.on{opacity:1;pointer-events:auto}
.drawer{position:fixed;top:0;right:0;bottom:0;width:min(680px,100%);background:var(--bg);
  border-left:1px solid var(--line);transform:translateX(100%);transition:transform .32s cubic-bezier(.22,1,.36,1);
  z-index:61;overflow-y:auto;overscroll-behavior:contain}
.drawer.on{transform:translateX(0)}
.dhead{position:sticky;top:0;background:rgba(2,6,23,.96);backdrop-filter:blur(9px);
  border-bottom:1px solid var(--line);padding:16px 20px;display:flex;gap:12px;align-items:flex-start}
.dhead h3{margin:0;font-size:15px;font-weight:700;flex:1}
.dhead .x{background:none;border:1px solid var(--line);color:var(--mut);border-radius:8px;
  width:30px;height:30px;cursor:pointer;font-size:16px;line-height:1;flex:none}
.dhead .x:hover{border-color:var(--red);color:var(--red)}
.dbody{padding:20px}
.replay{margin:0 0 18px}

/* the chain */
.chain{position:relative;padding-left:34px}
.hop{position:relative;margin-bottom:14px;opacity:0;transform:translateY(9px);
  transition:opacity .34s ease,transform .34s ease}
.hop.in{opacity:1;transform:none}
.hop .pip{position:absolute;left:-34px;top:5px;width:15px;height:15px;border-radius:50%;
  background:var(--bg);border:2px solid var(--slate);z-index:2}
.hop.ok .pip{border-color:var(--green);box-shadow:0 0 0 4px rgba(52,211,153,.13)}
.hop.broken .pip{border-color:var(--red);box-shadow:0 0 0 4px rgba(248,113,113,.13)}
.hop.na .pip{border-color:var(--slate);border-style:dashed}
/* the connector that draws itself between hops */
.hop .link{position:absolute;left:-27px;top:20px;width:2px;height:0;background:var(--slate);
  z-index:1;transition:height .34s ease}
.hop.in .link{height:calc(100% + 14px)}
.hop.ok .link{background:linear-gradient(180deg,var(--green),rgba(52,211,153,.34))}
.hop.na .link{background:repeating-linear-gradient(180deg,var(--slate) 0 3px,transparent 3px 7px)}
/* a broken hop terminates: the connector runs the height of the card and then
   stops dead in the gap below it, capped and labelled. The label sits in that
   gap rather than over the card, so it never collides with the hop value. */
.hop.broken .link{background:linear-gradient(180deg,var(--red),rgba(248,113,113,.55));height:0}
.hop.broken.in .link{height:calc(100% + 8px)}
.hop.broken .cap{position:absolute;left:-33px;bottom:-31px;color:var(--red);font-family:var(--mono);
  font-size:15px;font-weight:700;opacity:0;transition:opacity .3s ease .2s;z-index:3;line-height:1}
.hop.broken.in .cap{opacity:1}
.hop.broken .term{position:absolute;left:-12px;bottom:-29px;font-family:var(--mono);font-size:10px;
  color:var(--red);letter-spacing:.09em;opacity:0;transition:opacity .3s ease .28s;white-space:nowrap}
.hop.broken.in .term{opacity:1}
.hop.broken{margin-bottom:48px}

.hop .card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:11px 13px}
.hop.ok .card{border-left:3px solid var(--green)}
.hop.broken .card{border-left:3px solid var(--red)}
.hop.na .card{border-left:3px solid var(--slate);opacity:.82}
.hop .hn{font-family:var(--mono);font-size:10px;letter-spacing:.10em;text-transform:uppercase;
  color:var(--dim);display:flex;gap:8px;align-items:center;margin-bottom:5px}
.hop .hn i{font-style:normal;color:var(--slate)}
.hop .val{font-size:13.5px;word-break:break-word}
.hop .val.q{font-size:14px;line-height:1.55;color:var(--ink);border-left:2px solid var(--line);
  padding-left:10px;font-style:italic}
.hop .why{font-size:12.5px;color:var(--mut);margin-top:6px}
.mono{font-family:var(--mono);font-size:12px;color:var(--mut)}
.hop a{word-break:break-all;font-size:12.5px;font-family:var(--mono)}

.legend{display:flex;gap:16px;flex-wrap:wrap;margin-top:14px;font-size:12px;color:var(--mut)}
.legend span{display:flex;gap:6px;align-items:center;font-family:var(--mono);font-size:11px}
.sw{width:11px;height:11px;border-radius:50%;border:2px solid}
.sw.g{border-color:var(--green)} .sw.r{border-color:var(--red)} .sw.s{border-color:var(--slate);border-style:dashed}

footer{padding:34px 0 60px;color:var(--dim);font-size:12.5px}
footer code{font-family:var(--mono);color:var(--mut)}
.empty{text-align:center;color:var(--mut);padding:40px;font-family:var(--mono);font-size:13px}
@media (max-width:640px){
  .row{grid-template-columns:1fr;gap:7px}
  .row .ty{justify-self:start}
  .bar{grid-template-columns:106px 1fr 54px}
}
@media (prefers-reduced-motion:reduce){
  *{animation-duration:.001ms;transition-duration:.001ms}
  .hop{opacity:1;transform:none}
}
</style>
</head>
<body>

<header>
  <div class="wrap">
    <div class="kick">Surviving the Singularity</div>
    <h1>Chain of custody</h1>
    <p class="sub">Every mechanically detectable claim in the manuscript, traced from the
      sentence on the page back to the thing that makes it true. Pick any claim and watch
      the provenance resolve hop by hop, including the hops that break.</p>
    <div class="asof" id="asof"></div>
    <div class="banner">
      <div class="dot"></div>
      <p><b>This was a local-only pass. No URL was fetched.</b> Nothing on this page tells you
        whether a source is live, dead, paywalled or archived, because no network request was
        made. Every external source hop is recorded broken with a reason rather than guessed at.
        A claim marked <span class="vd UNCHECKED">UNCHECKED</span> is not a claim that failed.
        It is a claim nobody has checked yet.</p>
    </div>
    <div class="tiles" id="tiles"></div>
  </div>
</header>

<section>
  <div class="wrap">
    <h2>What this does not cover</h2>
    <p class="lede">Listed first and in full, because a trace that quietly omits the hard
      claims is worse than no trace. Each of these is a real gap, not a rounding error.</p>
    <div class="cov" id="cov"></div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>The shape of the evidence</h2>
    <p class="lede">Computed from the records on this page, never typed in.</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:32px">
      <div><h4 class="mono" style="margin:0 0 10px;color:var(--mut)">BY CLAIM TYPE</h4>
        <div class="bars" id="byType"></div></div>
      <div><h4 class="mono" style="margin:0 0 10px;color:var(--mut)">BY VERDICT</h4>
        <div class="bars" id="byVerdict"></div></div>
      <div><h4 class="mono" style="margin:0 0 10px;color:var(--mut)">GIT RECEIPT STATE</h4>
        <div class="bars" id="byReceipt"></div></div>
      <div><h4 class="mono" style="margin:0 0 10px;color:var(--mut)">TOP CITED HOSTS</h4>
        <div class="bars" id="byHost"></div></div>
    </div>
  </div>
</section>

<section style="padding-bottom:0">
  <div class="wrap">
    <h2>Walk the claims</h2>
    <p class="lede">Click any row to open its chain. The trace draws itself one hop at a
      time, and stops dead where the custody breaks.</p>
    <div class="legend">
      <span><i class="sw g"></i> hop resolved</span>
      <span><i class="sw r"></i> hop broken, chain terminates</span>
      <span><i class="sw s"></i> not applicable to this claim type</span>
    </div>
  </div>
</section>

<div class="controls">
  <div class="wrap crow">
    <input type="search" id="q" placeholder="Search claim text, block id, source, host, note...">
    <select id="fSec"></select>
    <select id="fType"></select>
    <select id="fVerdict"></select>
    <select id="fReceipt"></select>
    <button class="btn" id="reset">reset</button>
    <span class="count" id="count"></span>
  </div>
</div>

<section style="border-bottom:none">
  <div class="wrap">
    <div class="rows" id="rows"></div>
    <div class="trunc" id="trunc"></div>
    <div class="more"><button class="btn" id="more">show more</button></div>
  </div>
</section>

<footer>
  <div class="wrap" id="foot"></div>
</footer>

<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" aria-label="Claim chain of custody">
  <div class="dhead">
    <h3 id="dtitle">Chain of custody</h3>
    <button class="x" id="dclose" aria-label="Close">&times;</button>
  </div>
  <div class="dbody">
    <div class="replay"><button class="btn" id="replay">replay the trace</button></div>
    <div class="chain" id="chain"></div>
  </div>
</aside>

<script>
const D = __DATA__;
const C = D.claims;
const $ = s => document.querySelector(s);
const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g,
  m => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
const nf = n => n.toLocaleString("en-US");

/* ---------- every number below is derived from C, never written by hand ---------- */
const tally = (arr, fn) => arr.reduce((m, x) => {
  const k = fn(x); if (k == null) return m; m[k] = (m[k] || 0) + 1; return m; }, {});
const sortT = o => Object.entries(o).sort((a, b) => b[1] - a[1]);

const byType    = tally(C, c => c.t);
const byVerdict = tally(C, c => c.v);
const byReceipt = tally(C, c => c.rs);
const byHost    = tally(C.filter(c => c.t === "url"), c => c.host);
const bySection = tally(C, c => c.st);

const nResolvable  = C.filter(c => c.ls === "resolvable").length;
const nBroken      = C.length - nResolvable;
const nContra      = (byVerdict.CONTRADICTED || 0);
const nUrls        = (byType.url || 0);
const nWiki        = C.filter(c => c.bare_wikipedia).length;
const nCompare     = C.filter(c => c.comparison_claim).length;
const nNotCited    = C.filter(c => c.t === "url" && c.in_works_cited === false).length;
const nUncommitted = Object.values(D.git).filter(g => g.receipt_state === "uncommitted").length;

$("#asof").textContent =
  "As of " + D.generated + " . book version " + D.book_version +
  " . " + nf(D.totals.words) + " words . " + nf(D.totals.blocks) + " blocks . " +
  D.totals.sections + " sections . generated at build time, not live";

const tiles = [
  ["neutral", nf(C.length), "claims traced"],
  ["ok",      nf(byVerdict.SUPPORTED || 0), "supported"],
  [nContra ? "bad" : "ok", nf(nContra), "contradicted"],
  ["warn",    nf(byVerdict.UNCHECKED || 0), "unchecked"],
  ["violet",  nf(byVerdict.UNCHECKABLE || 0), "uncheckable"],
  ["info",    nf(nResolvable), "receipts resolvable"],
  [nBroken ? "bad" : "ok", nf(nBroken), "receipts broken"],
  ["warn",    nf(nUrls), "external urls"],
];
$("#tiles").innerHTML = tiles.map(([k, n, l]) =>
  `<div class="tile ${k}"><div class="num">${n}</div><div class="lab">${esc(l)}</div></div>`).join("");

$("#cov").innerHTML = D.not_covered.map(x =>
  `<div class="card"><h4>${esc(x.kind)}</h4><p>${esc(x.why)}</p></div>`).join("");

const COLOR = {
  SUPPORTED:"var(--green)", PARTIAL:"var(--amber)", UNCHECKED:"var(--slate)",
  UNCHECKABLE:"var(--violet)", CONTRADICTED:"var(--red)", UNSUPPORTED:"var(--red)",
  origin_exact:"var(--green)", local_only:"var(--amber)", uncommitted:"var(--red)",
};
function bars(el, entries, total, colorFn) {
  el.innerHTML = entries.map(([k, v]) =>
    `<div class="bar"><div class="nm">${esc(k)}</div>
     <div class="tr"><div class="fl" data-w="${(v / total * 100).toFixed(1)}"
       style="background:${colorFn ? colorFn(k) : "var(--blue)"}"></div></div>
     <div class="vl">${nf(v)}</div></div>`).join("");
}
bars($("#byType"), sortT(byType), C.length, () => "var(--blue)");
bars($("#byVerdict"), sortT(byVerdict), C.length, k => COLOR[k] || "var(--blue)");
bars($("#byReceipt"), sortT(byReceipt), C.length, k => COLOR[k] || "var(--blue)");
bars($("#byHost"), sortT(byHost).slice(0, 12), Math.max(1, nUrls), () => "var(--amber)");

// fill the bars once they scroll into view so the proportions animate in
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.style.width = e.target.dataset.w + "%"; io.unobserve(e.target); }
}), { threshold: .1 });
document.querySelectorAll(".fl").forEach(el => io.observe(el));

/* ---------- filters ---------- */
function fill(sel, label, keys) {
  sel.innerHTML = `<option value="">${label} (all)</option>` +
    keys.map(k => `<option value="${esc(k)}">${esc(k)}</option>`).join("");
}
fill($("#fSec"), "section", Object.keys(bySection));
fill($("#fType"), "type", sortT(byType).map(e => e[0]));
fill($("#fVerdict"), "verdict", sortT(byVerdict).map(e => e[0]));
fill($("#fReceipt"), "receipt", sortT(byReceipt).map(e => e[0]));

const PAGE = 200;
let shown = PAGE, filtered = C;

function apply() {
  const q = $("#q").value.trim().toLowerCase();
  const s = $("#fSec").value, t = $("#fType").value;
  const v = $("#fVerdict").value, r = $("#fReceipt").value;
  filtered = C.filter(c => {
    if (s && c.st !== s) return false;
    if (t && c.t !== t) return false;
    if (v && c.v !== v) return false;
    if (r && c.rs !== r) return false;
    if (!q) return true;
    return (c.q + " " + c.b + " " + (c.url || "") + " " + (c.host || "") + " " +
            (c.target || "") + " " + c.n + " " + c.f).toLowerCase().includes(q);
  });
  shown = PAGE;
  render();
}
function render() {
  const slice = filtered.slice(0, shown);
  $("#count").textContent = nf(filtered.length) + " of " + nf(C.length) + " claims";
  $("#rows").innerHTML = slice.length ? slice.map(c =>
    `<div class="row" tabindex="0" data-i="${c.i}">
       <div class="ty">${esc(c.t.replace("_", " "))}</div>
       <div class="qq">${esc(c.q.slice(0, 190))}<small>${esc(c.b)}</small></div>
       <div class="vd ${esc(c.v)}">${esc(c.v)}</div>
     </div>`).join("")
    : `<div class="empty">No claim matches these filters.</div>`;
  const hidden = filtered.length - slice.length;
  $("#trunc").textContent = hidden > 0
    ? nf(hidden) + " more match these filters and are not rendered yet. Nothing was dropped."
    : "";
  $("#more").style.display = hidden > 0 ? "" : "none";
}
["#q", "#fSec", "#fType", "#fVerdict", "#fReceipt"].forEach(s =>
  $(s).addEventListener("input", apply));
$("#reset").addEventListener("click", () => {
  $("#q").value = ""; ["#fSec", "#fType", "#fVerdict", "#fReceipt"].forEach(s => $(s).value = "");
  apply();
});
$("#more").addEventListener("click", () => { shown += PAGE; render(); });

/* ---------- the chain of custody ---------- */
function hops(c) {
  const H = [];
  const ok = (n, label, val, why) => H.push({ n, label, val, why, st: "ok" });
  const bad = (n, label, val, why) => H.push({ n, label, val, why, st: "broken" });
  const na = (n, label, val, why) => H.push({ n, label, val, why, st: "na" });

  H.push({ n: 1, label: "claim", val: c.q, why: "Quoted verbatim from the manuscript source.",
           st: "ok", quote: true });
  ok(2, "type", c.t.replace("_", " ") +
      (c.xref_kind ? " (" + c.xref_kind + ")" : "") +
      (c.comparison_claim ? "  ::  comparison claim" : ""),
      c.comparison_claim
        ? "Contains comparison language. The P-09 post mortem found the book's failure mode is inherited comparison claims, not invented facts, so these carry extra risk."
        : "Classified by pattern from the block source.");
  ok(3, "location", c.f + ":" + c.ln + "  (block lines " + c.bl[0] + " to " + c.bl[1] + ")",
      "Section: " + c.st + ". Line numbers are valid for the working tree at build time and rot on the next edit, which is why they are not the anchor.");
  ok(4, "block id", c.b + "   [" + c.bt + "]" + (c.bh ? "   hash " + c.bh : ""),
      "The stable anchor from `sts id`. Survives edits above it, unlike the line number.");

  if (c.rs === "origin_exact") {
    ok(5, "git receipt", (c.sha || "unknown") + (c.au ? "  by " + c.au : "") + (c.dt ? "  on " + c.dt : "") +
        (c.sm ? "\n" + c.sm : ""),
        "Commit that last touched this line, via git blame. The subject line is reproduced with its punctuation normalised to house style; the SHA is the authoritative record and carries the original wording.");
  } else {
    bad(5, "git receipt", "BROKEN", c.rr || "No immutable receipt exists for this text.");
  }

  if (c.ls === "resolvable" && c.pl) {
    H.push({ n: 6, label: "github link", val: c.pl, why:
      "Pinned to a commit SHA, not a branch name. The file is byte identical to origin/main, so these line numbers are valid at that SHA and the link resolves for any reader. The repository is public.",
      st: "ok", link: c.pl });
  } else {
    bad(6, "github link", "BROKEN",
      c.rs === "uncommitted"
        ? "There is no SHA to link to. This text exists only in the working tree, so no permalink can be minted. Pinning to a local-only commit would 404 for every reader but this machine."
        : "This file differs from origin/main, so no commit a reader can fetch contains these lines at these numbers.");
  }

  if (c.t === "url") {
    H.push({ n: 7, label: "source", val: c.url, st: "ok", link: c.url, why:
      "Cited URL, extracted from the block source. " +
      (c.in_works_cited ? "Also present in the Appendix B Works Cited list."
                        : "NOT present in the Appendix B Works Cited list.") +
      (c.bare_wikipedia ? " Host is Wikipedia, which the P-09 post mortem treats as unverified by default when it is a claim's only citation." : "") });
    bad(8, "source state", "BROKEN",
      "No network request was made in this run, so liveness is unknown. A 200 would not have been enough anyway: soft 404s, parked domains, consent walls and paywalls all return 200, so the content has to be read, not just the status code.");
    bad(9, "archive", "BROKEN", "No web.archive.org snapshot was resolved. Requires network.");
  } else if (c.t === "image") {
    H.push({ n: 7, label: "source", val: c.image + (c.art_id ? "\nart_id " + c.art_id : ""),
      st: c.on_disk ? "ok" : "broken",
      why: c.on_disk ? "Asset resolved on disk under static/." : "No such file exists under static/." });
    H.push({ n: 8, label: "source state", val: c.on_disk ? "present on disk" : "MISSING",
      st: c.on_disk ? "ok" : "broken",
      why: c.in_catalog ? "Enrolled in art-catalog.json, so its provenance and licence are tracked."
                        : "Not enrolled in art-catalog.json, so nothing tracks its provenance or licence." });
    na(9, "archive", "not applicable", "Local asset. Nothing to archive.");
  } else if (c.t === "internal_xref") {
    H.push({ n: 7, label: "source", val: c.target, st: c.resolved ? "ok" : "broken",
      why: c.resolved ? "Target exists inside the book itself. This is the one claim class fully decidable without network."
                      : "Target does not exist in the book. Dangling internal reference." });
    H.push({ n: 8, label: "source state", val: c.resolved ? "resolved in-book" : "DANGLING",
      st: c.resolved ? "ok" : "broken", why: c.n });
    na(9, "archive", "not applicable", "Internal reference. Nothing to archive.");
  } else {
    bad(7, "source", "BROKEN",
      "No external source is attached to this claim in the manuscript source. " +
      (c.has_citation_nearby ? "The enclosing block does carry a URL, so a source may be intended but is not bound to this sentence."
                             : "The enclosing block carries no URL at all, so even a network run would have nothing to resolve."));
    bad(8, "source state", "BROKEN", "No source to check. Local-only run, no network request made.");
    bad(9, "archive", "BROKEN", "No source to archive.");
  }

  H.push({ n: 10, label: "verdict", val: c.v, st:
    (c.v === "SUPPORTED" ? "ok" : (c.v === "CONTRADICTED" || c.v === "UNSUPPORTED") ? "broken" : "na"),
    why: c.n, verdict: c.v });
  return H;
}

let timers = [];
function drawChain(c) {
  timers.forEach(clearTimeout); timers = [];
  const H = hops(c);
  $("#chain").innerHTML = H.map(h => `
    <div class="hop ${h.st}">
      <div class="pip"></div><div class="link"></div>
      ${h.st === "broken" ? '<div class="cap">&#10007;</div><div class="term">CUSTODY BREAKS HERE</div>' : ""}
      <div class="card">
        <div class="hn"><i>${String(h.n).padStart(2, "0")}</i> ${esc(h.label)}</div>
        ${h.verdict ? `<div class="val"><span class="vd ${esc(h.verdict)}">${esc(h.verdict)}</span></div>`
          : h.link ? `<div class="val"><a href="${esc(h.link)}" target="_blank" rel="noopener">${esc(h.val)}</a></div>`
          : `<div class="val${h.quote ? " q" : ""}" style="white-space:pre-wrap">${esc(h.val)}</div>`}
        ${h.why ? `<div class="why">${esc(h.why)}</div>` : ""}
      </div>
    </div>`).join("");
  const els = $("#chain").querySelectorAll(".hop");
  els.forEach((el, i) => timers.push(setTimeout(() => el.classList.add("in"), 90 + i * 190)));
}

let current = null;
function open(i) {
  const c = C.find(x => x.i === i); if (!c) return;
  current = c;
  $("#dtitle").textContent = c.t.replace("_", " ").toUpperCase() + "  .  " + c.b;
  $("#drawer").classList.add("on"); $("#scrim").classList.add("on");
  $("#drawer").scrollTop = 0;
  drawChain(c);
}
function close() {
  $("#drawer").classList.remove("on"); $("#scrim").classList.remove("on");
  timers.forEach(clearTimeout); timers = [];
}
$("#rows").addEventListener("click", e => {
  const r = e.target.closest(".row"); if (r) open(+r.dataset.i); });
$("#rows").addEventListener("keydown", e => {
  if (e.key === "Enter" || e.key === " ") {
    const r = e.target.closest(".row"); if (r) { e.preventDefault(); open(+r.dataset.i); } } });
$("#dclose").addEventListener("click", close);
$("#scrim").addEventListener("click", close);
$("#replay").addEventListener("click", () => current && drawChain(current));
document.addEventListener("keydown", e => { if (e.key === "Escape") close(); });

/* ---------- footer, also computed ---------- */
const uncommittedFiles = Object.values(D.git)
  .filter(g => g.receipt_state === "uncommitted").map(g => g.file);
$("#foot").innerHTML = `
  <p><b>How to read a broken receipt.</b> ${nf(nBroken)} of ${nf(C.length)} claims
  (${(nBroken / C.length * 100).toFixed(1)}%) have no receipt a reader can resolve. Every one of
  them sits in ${nUncommitted} manuscript file(s) that are dirty in the working tree:
  <code>${uncommittedFiles.map(esc).join("</code>, <code>")}</code>. That text has never been
  committed, so there is no SHA to link to. This is not a bug in the trace. It is the single
  most actionable thing on this page.</p>
  <p><b>Citation posture.</b> ${nf(nUrls)} external URLs, of which ${nf(nWiki)} are Wikipedia
  (${(nWiki / Math.max(1, nUrls) * 100).toFixed(0)}% of the citation base) and ${nf(nNotCited)}
  do not appear in the Appendix B Works Cited list. ${nf(nCompare)} claims use comparison
  language, which is the exact shape of the one error this project has already caught and cut.</p>
  <p><b>Provenance of this page.</b> Generated by <code>sts.py factcheck</code> and
  <code>scripts/build_factcheck_trace.py</code> on ${esc(D.generated)} against book version
  ${esc(D.book_version)}. Network was off. Every count above is computed in the browser from the
  embedded records, so this page cannot disagree with its own data. Repository:
  <a href="${esc(D.repo)}" target="_blank" rel="noopener">${esc(D.repo)}</a> (public).</p>`;

apply();
</script>
</body>
</html>
"""


def summarise(report):
    """The headline numbers, for the site route to import.

    The /factcheck page must not hardcode a single count either, so it reads
    this file instead. One generator, one set of numbers, no third copy to
    drift."""
    claims = report["claims"]
    def count(pred):
        return sum(1 for c in claims if pred(c))
    urls = [c for c in claims if c["type"] == "url"]
    return {
        "generated": report["generated"],
        "book_version": report["book_version"],
        "repo": report["repo"],
        "network": report["network"],
        "words": report["totals"]["words"],
        "sections": report["totals"]["sections"],
        "blocks": report["totals"]["blocks"],
        "claims": len(claims),
        "resolvable": count(lambda c: c["git"]["link_state"] == "resolvable"),
        "broken": count(lambda c: c["git"]["link_state"] != "resolvable"),
        "by_verdict": report["by_verdict"],
        "by_type": report["by_type"],
        "urls": len(urls),
        "wikipedia": sum(1 for c in urls if c.get("bare_wikipedia")),
        "not_in_works_cited": sum(1 for c in urls if c.get("in_works_cited") is False),
        "comparison_claims": count(lambda c: c.get("comparison_claim")),
        "figures": count(lambda c: c["type"] == "image"),
        "internal_refs": count(lambda c: c["type"] == "internal_xref"),
        "uncommitted_files": sorted(
            g["file"] for g in report["git"].values()
            if g["receipt_state"] == "uncommitted"),
        "not_covered": report["not_covered"],
    }


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit("usage: build_factcheck_trace.py <in.json> <out.html> "
                 "[--summary <path.json>] [--static <path.html>]")
    src, dst = Path(args[0]), Path(args[1])
    summary_path = static_path = None
    i = 2
    while i < len(args):
        if args[i] == "--summary":
            summary_path = Path(args[i + 1]); i += 2
        elif args[i] == "--static":
            static_path = Path(args[i + 1]); i += 2
        else:
            sys.exit(f"unknown argument: {args[i]}")

    report = json.loads(src.read_text(encoding="utf-8"))
    html = build(report)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(html, encoding="utf-8")
    kb = len(html.encode("utf-8")) / 1024
    print(f"wrote {dst}  ({kb:,.0f} KB, {len(report['claims']):,} claims)")

    if static_path:
        static_path.parent.mkdir(parents=True, exist_ok=True)
        static_path.write_text(html, encoding="utf-8")
        print(f"wrote {static_path}  (served by the site)")

    if summary_path:
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(
            json.dumps(summarise(report), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        print(f"wrote {summary_path}  (headline numbers for the /factcheck route)")


if __name__ == "__main__":
    main()
