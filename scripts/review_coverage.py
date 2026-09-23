#!/usr/bin/env python3
"""
review_coverage.py

Turns "comprehensive review" from an adjective into a measurement.

The problem this exists to solve: a review can CLAIM it read every line, and
there is no way to check that claim after the fact. This script makes the claim
falsifiable.

  Ground truth  : line counts computed here, from book.json and the files.
  Attestation   : each reviewer reports the line count it saw, plus a ledger
                  saying what it found in every 25-line block of the file.
  Verification  : an attested line count that disagrees with ground truth means
                  the reviewer did not open the whole file. A block ledger with
                  a hole means a range nobody looked at. Both are hard failures.

A section is only counted as REVIEWED when its attestation passes both tests.
Anything else is reported as NOT REVIEWED, by name, so partial work can never be
presented as finished work.

Usage:
    python3 scripts/review_coverage.py                 # coverage table
    python3 scripts/review_coverage.py --json          # machine readable
    python3 scripts/review_coverage.py --html out.html # render the page
"""

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "src", "lib", "data", "book")
ATTEST = os.path.join(ROOT, "docs", "review-attestations.json")
BLOCK = 25


def ground_truth():
    """Line and word counts for every section book.json actually ships."""
    meta = json.load(open(os.path.join(BOOK, "book.json"), encoding="utf-8"))
    order = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "file" and isinstance(v, str):
                    order.append((o.get("title", "?"), v))
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(meta)
    out = []
    for title, f in order:
        p = os.path.join(BOOK, f)
        if not os.path.exists(p):
            out.append({"file": f, "title": title, "lines": 0, "words": 0, "missing": True})
            continue
        txt = open(p, encoding="utf-8").read()
        out.append({
            "file": f, "title": title,
            "lines": len(txt.splitlines()),
            "words": len(txt.split()),
            "missing": False,
        })
    return out


def expected_blocks(n_lines):
    """The 25-line block labels a complete ledger must contain."""
    blocks = []
    start = 1
    while start <= n_lines:
        end = min(start + BLOCK - 1, n_lines)
        blocks.append(f"{start}-{end}")
        start += BLOCK
    return blocks


def load_attestations():
    if not os.path.exists(ATTEST):
        return {}
    return json.load(open(ATTEST, encoding="utf-8"))


def verify(gt, att):
    """Check one section's attestation against ground truth."""
    rec = att.get(gt["file"])
    if not rec:
        return {"status": "NOT REVIEWED", "problems": ["no attestation on record"],
                "findings": 0, "attested_lines": None, "blocks_ok": False}

    problems = []
    attested = rec.get("lines_total")
    if attested != gt["lines"]:
        problems.append(
            f"attested {attested} lines, file actually has {gt['lines']}: "
            f"reviewer did not read the whole file")

    want = expected_blocks(gt["lines"])
    got = list(rec.get("blocks", {}).keys())
    holes = [b for b in want if b not in got]
    extra = [b for b in got if b not in want]
    if holes:
        problems.append(f"{len(holes)} block(s) unaccounted for: {', '.join(holes[:6])}"
                        + (" ..." if len(holes) > 6 else ""))
    if extra:
        problems.append(f"ledger cites {len(extra)} block(s) outside the file: {', '.join(extra[:4])}")

    return {
        "status": "REVIEWED" if not problems else "INVALID",
        "problems": problems,
        "findings": len(rec.get("findings", [])),
        "attested_lines": attested,
        "blocks_ok": not holes and not extra,
        "reviewer": rec.get("reviewer", ""),
        "blocks_total": len(want),
        "blocks_clean": sum(1 for b, v in rec.get("blocks", {}).items()
                            if str(v).strip().upper() == "CLEAN"),
    }


def build():
    gts = ground_truth()
    att = load_attestations()
    rows = []
    for gt in gts:
        v = verify(gt, att)
        rows.append({**gt, **v})
    tot_lines = sum(r["lines"] for r in rows)
    done_lines = sum(r["lines"] for r in rows if r["status"] == "REVIEWED")
    return {
        "sections_total": len(rows),
        "sections_reviewed": sum(1 for r in rows if r["status"] == "REVIEWED"),
        "sections_invalid": sum(1 for r in rows if r["status"] == "INVALID"),
        "sections_unreviewed": sum(1 for r in rows if r["status"] == "NOT REVIEWED"),
        "lines_total": tot_lines,
        "lines_reviewed": done_lines,
        "pct_lines": round(100.0 * done_lines / tot_lines, 1) if tot_lines else 0.0,
        "words_total": sum(r["words"] for r in rows),
        "words_reviewed": sum(r["words"] for r in rows if r["status"] == "REVIEWED"),
        "findings_total": sum(r["findings"] for r in rows),
        "rows": rows,
    }


def render_text(d):
    out = []
    out.append(f"{'section':<24} {'lines':>6} {'blocks':>7} {'find':>5}  status")
    out.append("-" * 74)
    for r in d["rows"]:
        blocks = f"{r['blocks_total']}" if r["status"] != "NOT REVIEWED" else "-"
        out.append(f"{r['file']:<24} {r['lines']:>6} {blocks:>7} "
                   f"{r['findings'] if r['status'] != 'NOT REVIEWED' else '-':>5}  {r['status']}")
        for p in r["problems"]:
            out.append(f"{'':>24} !! {p}")
    out.append("-" * 74)
    out.append(f"REVIEWED {d['sections_reviewed']}/{d['sections_total']} sections, "
               f"{d['lines_reviewed']}/{d['lines_total']} lines ({d['pct_lines']}%), "
               f"{d['findings_total']} findings")
    if d["sections_unreviewed"] or d["sections_invalid"]:
        out.append("")
        out.append("THIS REVIEW IS NOT COMPLETE. Unreviewed or invalid sections:")
        for r in d["rows"]:
            if r["status"] != "REVIEWED":
                out.append(f"  - {r['file']} ({r['lines']} lines): {r['status']}")
    return "\n".join(out)


def render_html(d, path):
    def esc(s):
        return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

    rows = []
    for r in d["rows"]:
        cls = {"REVIEWED": "ok", "INVALID": "bad", "NOT REVIEWED": "none"}[r["status"]]
        probs = ("<div class='probs'>" +
                 "".join(f"<div>{esc(p)}</div>" for p in r["problems"]) + "</div>") if r["problems"] else ""
        bar = 0 if r["status"] == "NOT REVIEWED" else 100
        rows.append(f"""
      <tr class="{cls}">
        <td><code>{esc(r['file'])}</code><div class="ttl">{esc(r['title'])}</div>{probs}</td>
        <td class="num">{r['lines']}</td>
        <td class="num">{r['words']}</td>
        <td class="num">{r['blocks_total'] if r['status'] != 'NOT REVIEWED' else '-'}</td>
        <td class="num">{r['findings'] if r['status'] != 'NOT REVIEWED' else '-'}</td>
        <td><span class="pill {cls}">{esc(r['status'])}</span>
            <div class="bar"><i style="width:{bar}%"></i></div></td>
      </tr>""")

    complete = d["sections_reviewed"] == d["sections_total"]
    banner = ("<div class='banner ok'>Every shipped section has a verified attestation. "
              "Coverage is complete.</div>" if complete else
              f"<div class='banner bad'><b>THIS REVIEW IS NOT COMPLETE.</b> "
              f"{d['sections_reviewed']} of {d['sections_total']} sections have a verified "
              f"attestation, covering {d['pct_lines']}% of the book's lines. "
              f"Sections listed below as NOT REVIEWED or INVALID have not been read to a "
              f"provable standard, and nothing about them should be treated as checked.</div>")

    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>STS review coverage</title>
<style>
 :root{{--bg:#f7f5f0;--card:#fff;--ink:#22201d;--muted:#6b645c;--line:#ddd6c9;
   --ok:#1c7a4a;--okbg:#e6f4ec;--bad:#b3261e;--badbg:#fbeae9;--none:#8a8279;--nonebg:#efece6;}}
 @media(prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#14130f;--card:#1d1c18;
   --ink:#ece7de;--muted:#a49c90;--line:#332f28;--ok:#5cc98e;--okbg:#12301f;--bad:#ff8f85;
   --badbg:#3a1714;--none:#8a8279;--nonebg:#26241f;}}}}
 *{{box-sizing:border-box}}
 body{{margin:0;background:var(--bg);color:var(--ink);
   font:16px/1.6 ui-sans-serif,-apple-system,Segoe UI,Roboto,sans-serif}}
 .wrap{{max-width:1060px;margin:0 auto;padding:40px 20px 80px}}
 h1{{font-size:30px;margin:0 0 6px;letter-spacing:-.02em}}
 .sub{{color:var(--muted);margin:0 0 22px}}
 .banner{{border-radius:12px;padding:16px 20px;margin-bottom:24px;border:1px solid var(--line)}}
 .banner.ok{{background:var(--okbg);border-color:var(--ok)}}
 .banner.bad{{background:var(--badbg);border-color:var(--bad)}}
 .totals{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px}}
 .tile{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;min-width:130px}}
 .tile b{{display:block;font-size:26px;font-variant-numeric:tabular-nums}}
 .tile span{{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.07em}}
 .scroll{{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--card)}}
 table{{border-collapse:collapse;width:100%;min-width:720px}}
 th{{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);
   padding:12px 14px;border-bottom:1px solid var(--line);font-weight:600}}
 td{{padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:top}}
 tr:last-child td{{border-bottom:none}}
 .num{{font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}}
 code{{font-family:ui-monospace,Menlo,monospace;font-size:13px}}
 .ttl{{color:var(--muted);font-size:12px;margin-top:2px}}
 .probs{{margin-top:8px;font-size:12.5px;color:var(--bad);background:var(--badbg);
   border-radius:6px;padding:8px 10px}}
 .pill{{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.05em;
   padding:3px 8px;border-radius:5px;white-space:nowrap}}
 .pill.ok{{background:var(--okbg);color:var(--ok)}}
 .pill.bad{{background:var(--badbg);color:var(--bad)}}
 .pill.none{{background:var(--nonebg);color:var(--none)}}
 .bar{{height:4px;background:var(--nonebg);border-radius:3px;margin-top:7px;overflow:hidden;min-width:80px}}
 .bar i{{display:block;height:100%;background:var(--ok)}}
 tr.bad .bar i,tr.none .bar i{{background:var(--bad)}}
 .note{{background:var(--card);border:1px solid var(--line);border-radius:10px;
   padding:14px 18px;margin-top:24px;font-size:14px;color:var(--muted)}}
</style></head><body><div class="wrap">
<h1>Review coverage</h1>
<p class="sub">Every section book.json ships, and whether a reviewer has provably read it.
Generated by <code>scripts/review_coverage.py</code>.</p>
{banner}
<div class="totals">
 <div class="tile"><b>{d['sections_reviewed']}/{d['sections_total']}</b><span>sections verified</span></div>
 <div class="tile"><b>{d['pct_lines']}%</b><span>of lines</span></div>
 <div class="tile"><b>{d['words_reviewed']:,}</b><span>of {d['words_total']:,} words</span></div>
 <div class="tile"><b>{d['findings_total']}</b><span>findings</span></div>
</div>
<div class="scroll"><table>
 <thead><tr><th>Section</th><th class="num">Lines</th><th class="num">Words</th>
 <th class="num">Blocks</th><th class="num">Findings</th><th>Status</th></tr></thead>
 <tbody>{''.join(rows)}</tbody></table></div>
<div class="note"><b>How a section earns REVIEWED.</b> The reviewer must report the file's exact
line count, which is compared against a count taken independently here, and must account for every
25-line block of the file as either carrying findings or being explicitly clean. A wrong line count
means the whole file was never opened. A missing block means a range nobody looked at. Either one
marks the section INVALID rather than reviewed, because a review that cannot prove its coverage is
indistinguishable from a review that skimmed.</div>
</div></body></html>"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--html")
    a = ap.parse_args()
    d = build()
    if a.html:
        render_html(d, a.html)
    print(json.dumps(d, indent=1) if a.json else render_text(d))
    return 0 if d["sections_reviewed"] == d["sections_total"] else 1


if __name__ == "__main__":
    sys.exit(main())
