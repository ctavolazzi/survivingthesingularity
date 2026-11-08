#!/usr/bin/env python3
"""Turn a hyperlinked manuscript into print-friendly sourcing.

  Body citation   "Claim. [CDFA, Food Recovery](https://...)"
      print    -> "Claim. (Source: CDFA, Food Recovery)"     the word "Source:" stops at --label-until
      later    -> "Claim. (CDFA, Food Recovery)"
      ebook    -> "Claim. (Source: [CDFA, Food Recovery](https://...))"   links kept, same wording
  Back-to-back citations are merged:  (Source: A; B)
  Image credits, in-sentence links, and reading-list "Free at ..." links keep their words and lose the
      link in print (their URLs go to the back list).
  Appendix B (Works Cited): titles stay; the full URL is printed at the end of the entry.
  Any URL cited in the body but missing from Appendix B is appended there, so no address is lost.

usage: print_sourcing.py IN.md OUT.md [--mode print|ebook] [--label-until "Chapter 2"] [--report R.md]
exit 1 if any self-check fails.
"""
import argparse
import re
import sys
from collections import OrderedDict

LINK_RE = r'(?<!!)\[(?:[^\[\]]|\[[^\]]*\])+\]\((?:[^()\s]|\([^)]*\))+(?:\s+"[^"]*")?\)'
LINK = re.compile(r'(?<!!)\[((?:[^\[\]]|\[[^\]]*\])+)\]\(((?:[^()\s]|\([^)]*\))+)(?:\s+"[^"]*")?\)')
RUN = re.compile(LINK_RE + r'(?:[\s;,]*' + LINK_RE + r')*')
GENERIC = re.compile(r'^(here|link|source|sources|read more|more|click here|this|free\b.*|digitized issue|.*\btranscribed|.*\bonline)$', re.I)
M1, M2 = "\x02", "\x03"          # debug markers around every edit (used by the self-check)


def norm_url(u):
    u = u.strip().split("#")[0].rstrip("/")
    return re.sub(r"^https?://(www\.)?", "", u, flags=re.I).lower()


def fix_label(t):
    new = re.sub(r"\s*\((\d{4})\)\s*$", r", \1", t.strip())     # "IEA (2026)" -> "IEA, 2026": no nested brackets
    return new, new != t.strip()


def convert(lines, mode="print", label_until="Chapter 2", mark=False):
    out, stats, ledger = [], OrderedDict((k, 0) for k in (
        "links_in", "body_citations_labelled", "body_citations_bare", "grouped_runs", "in_sentence_stripped",
        "caption_credits_stripped", "generic_anchor_stripped", "works_cited_links", "nested_year_fixed")), OrderedDict()
    flags = {"generic": [], "year": [], "in_sentence": []}
    labelled, section, in_wc, wc_end, prev_nonblank, in_code = True, "", False, None, "", False
    wc_urls = set()
    sec = ""                                                   # pass 1: what Appendix B already lists
    for ln in lines:
        if ln.startswith("# "): sec = ln[2:]
        if sec.lower().startswith("appendix b"): wc_urls.update(norm_url(m.group(2)) for m in LINK.finditer(ln))
    def wrap(s): return f"{M1}{s}{M2}" if mark else s
    for ln in lines:
        if ln.startswith("```"): in_code = not in_code
        if ln.startswith("# "):
            section = ln[2:].strip()
            in_wc = section.lower().startswith("appendix b")
            if label_until and section.lower().startswith(label_until.lower()): labelled = False
            if wc_end is None and not in_wc and any(o.startswith("# Appendix B") for o in out) and "wc_closed" not in flags:
                flags["wc_closed"] = len(out)                   # first H1 after Appendix B
        if in_code or ln.startswith("!["):
            out.append(ln); prev_nonblank = ln if ln.strip() else prev_nonblank; continue
        runs = list(RUN.finditer(ln))
        stats["links_in"] += len(LINK.findall(ln))
        if not runs:
            out.append(ln); prev_nonblank = ln if ln.strip() else prev_nonblank; continue
        is_caption = bool(re.match(r"^\*[^*].*\*\s*$", ln.strip())) and prev_nonblank.startswith("![")
        new, pos, urls_for_end = [], 0, []
        for r in runs:
            links = [(m.group(1), m.group(2)) for m in LINK.finditer(r.group(0))]
            seps = re.split(LINK_RE, r.group(0))                # separators between the links of this run
            for t, u in links: ledger.setdefault(norm_url(u), [t, u, section, is_caption])
            wm = re.search(r"\((?:Source:\s*)?$", ln[:r.start()])          # already hand-converted: "(Source: [X](url))"
            wrapped = bool(wm) and ln[r.end():r.end() + 1] == ")" and not in_wc and not is_caption
            s0, e0 = (wm.start(), r.end() + 1) if wrapped else (r.start(), r.end())
            before = re.sub(r"[*_`]", "", ln[:r.start()]).rstrip()
            after = ln[r.end():].lstrip(" ")
            sentence_before = before == "" or bool(re.search(r"[.!?:;][\"”’')\]]*$", before)) or bool(re.fullmatch(r"[-*>\d.\s]*", before))
            sentence_after = after == "" or not re.match(r"[a-z]", re.sub(r"^[*_\"'“‘(]+", "", after))
            generic = any(GENERIC.match(t.strip()) or t.startswith("http") for t, _ in links)
            if in_wc:                                           # bibliography: titles stay, URL goes to the end
                stats["works_cited_links"] += len(links)
                if mode == "print":
                    rep = "".join(t + (seps[i + 1] if i + 1 < len(seps) else "") for i, (t, _) in enumerate(links))
                    urls_for_end += [u for _, u in links]
                    new.append((r.start(), r.end(), wrap(rep)))
                continue
            if is_caption:
                stats["caption_credits_stripped"] += len(links)
                if mode == "print":
                    rep = "".join(t + (seps[i + 1] if i + 1 < len(seps) else "") for i, (t, _) in enumerate(links))
                    new.append((r.start(), r.end(), wrap(rep)))
                continue
            if wrapped or (sentence_before and sentence_after and not generic):      # a citation (new or already wrapped)
                labs = []
                for t, u in links:
                    lab, changed = fix_label(t)
                    if changed: stats["nested_year_fixed"] += 1; flags["year"].append((t, lab))
                    labs.append(lab if mode == "print" else f"[{lab}]({u})")
                prefix = "Source: " if labelled else ""
                stats["body_citations_labelled" if labelled else "body_citations_bare"] += len(links)
                if len(links) > 1: stats["grouped_runs"] += 1
                new.append((s0, e0, wrap(f"({prefix}{'; '.join(labs)})")))
            else:                                                       # in-sentence / generic: words stay, link goes
                key = "generic_anchor_stripped" if generic else "in_sentence_stripped"
                stats[key] += len(links)
                flags["generic" if generic else "in_sentence"] += [(t, u) for t, u in links]
                if mode == "print":
                    rep = "".join(t + (seps[i + 1] if i + 1 < len(seps) else "") for i, (t, _) in enumerate(links))
                    new.append((r.start(), r.end(), wrap(rep)))
        res, pos = [], 0
        for s, e, rep in new:
            res.append(ln[pos:s]); res.append(rep); pos = e
        res.append(ln[pos:])
        line_out = "".join(res)
        if urls_for_end and mode == "print":
            line_out = line_out.rstrip() + " " + (f"\x05{' '.join(urls_for_end)}\x06" if mark else " ".join(urls_for_end))
        out.append(line_out); prev_nonblank = ln if ln.strip() else prev_nonblank
    missing = [(v[0], v[1]) for k, v in ledger.items() if k not in wc_urls and not v[2].lower().startswith("appendix b") and not v[3]]
    credits = [(v[0], v[1]) for k, v in ledger.items() if v[3] and k not in wc_urls]
    if mode == "print" and (missing or credits):
        block = ["\x04"]
        if missing: block += ["\x04## Additional sources cited in the text", "\x04"] + [f"\x04- {t}. {u}" for t, u in missing] + ["\x04"]
        if credits: block += ["\x04## Image credits", "\x04"] + [f"\x04- {t}. {u}" for t, u in credits] + ["\x04"]
        at = flags.get("wc_closed")
        if at is None: at = len(out)
        out[at:at] = block
    return out, stats, ledger, flags, missing


def selfcheck(src, mode, label_until):
    """Re-run in marker mode; every byte outside an edit must equal the input, line by line."""
    marked, *_ = convert(src, mode, label_until, mark=True)
    marked = [l for l in marked if not l.startswith("\x04")]
    bad = []
    for i, (a, b) in enumerate(zip(src, marked)):
        sk_in = re.sub(r"\((?:Source:\s*)?(?:" + LINK_RE + r"(?:[\s;,]*" + LINK_RE + r")*)\)", "\x00", a) if not a.startswith("![") else a
        sk_in = RUN.sub("\x00", sk_in)
        sk_out = re.sub(r" ?\x05.*?\x06", "", b)               # URLs appended to Works Cited entries
        sk_out = re.sub(f"{M1}.*?{M2}", "\x00", sk_out)
        if mode == "print" and sk_in.rstrip() != sk_out.rstrip():
            bad.append(i + 1)
    return bad, len(src), len(marked)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--mode", default="print", choices=["print", "ebook"])
    ap.add_argument("--label-until", default="Chapter 2")
    ap.add_argument("--report")
    a = ap.parse_args()
    src = open(a.inp, encoding="utf-8").read().split("\n")
    out, st, ledger, flags, missing = convert(src, a.mode, a.label_until)
    out = [l[1:] if l.startswith("\x04") else l for l in out]
    open(a.out, "w", encoding="utf-8").write("\n".join(out))
    accounted = (st["body_citations_labelled"] + st["body_citations_bare"] + st["in_sentence_stripped"] + st["caption_credits_stripped"]
                 + st["generic_anchor_stripped"] + st["works_cited_links"])
    left = len(LINK.findall("\n".join(out)))
    bad, n_in, n_out = selfcheck(src, a.mode, a.label_until)
    rep = [f"# print_sourcing report ({a.mode}, label stops at '{a.label_until}')", ""]
    rep += [f"- {k}: {v}" for k, v in st.items()]
    rep += [f"- links accounted for: {accounted} of {st['links_in']}", f"- links still in output: {left} ({'expected 0' if a.mode == 'print' else 'expected all kept'})",
            f"- unique URLs: {len(ledger)}; cited in body but not in Appendix B (added to the back list): {len(missing)}",
            f"- self-check: lines compared {n_in}, lines where text outside an edit changed: {len(bad)} {bad[:8]}"]
    if flags["generic"]: rep += ["", "## generic anchors (words kept, link dropped; check wording)"] + [f"- {t}  <- {u[:70]}" for t, u in flags["generic"]]
    if flags["year"]: rep += ["", "## '(YYYY)' turned into ', YYYY' inside parentheses"] + [f"- {t}  ->  {n}" for t, n in flags["year"]]
    if a.report: open(a.report, "w", encoding="utf-8").write("\n".join(rep))
    print("\n".join(rep[:16]))
    ok = accounted == st["links_in"] and not bad and (left == 0 if a.mode == "print" else left == st["links_in"])
    print("\nRESULT:", "ALL SELF-CHECKS PASS" if ok else "SELF-CHECK FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
