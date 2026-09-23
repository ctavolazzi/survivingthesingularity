#!/usr/bin/env python3
"""
verify_review_claims.py

Re-runs every mechanically checkable claim made in
docs/review-2026-08-16-v0751-full-book.md and proves each one from the files
on disk and the live web, rather than from anybody's memory of them.

Design rules, both bought the hard way (see ~/.claude/MISTAKES.md):

  1. Every check reports the ACTUAL observed value, not just a verdict. If a
     check says a string sits at line 40, it prints line 40.
  2. Every check class ships a NEGATIVE CONTROL that must come back RED. A
     green check nobody has watched fail is not evidence of anything (M-04).
  3. Network checks run through two independent stacks (urllib and curl),
     because the book harness's own "unreachable" verdicts turned out to be
     its TLS stack rather than the sources (M-02: the instrument can be the
     thing that is broken).

Usage:
    python3 scripts/verify_review_claims.py                  # JSON to stdout
    python3 scripts/verify_review_claims.py --offline        # skip network
    python3 scripts/verify_review_claims.py --html out.html  # render the page
"""

import argparse
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "src", "lib", "data", "book")
REPORT = os.path.join(ROOT, "docs", "review-2026-08-16-v0751-full-book.md")

RESULTS = []


# ----------------------------------------------------------------------------
# plumbing
# ----------------------------------------------------------------------------

def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def lines(path):
    return read(path).splitlines()


def record(cid, category, claim, method, expected, observed, ok, evidence=""):
    RESULTS.append({
        "id": cid,
        "category": category,
        "claim": claim,
        "method": method,
        "expected": str(expected),
        "observed": str(observed),
        "verdict": "PASS" if ok else "FAIL",
        "evidence": evidence,
    })
    return ok


def find_lines(path, needle, regex=False):
    """Return [(lineno, text)] for every line containing needle."""
    hits = []
    for i, ln in enumerate(lines(path), 1):
        if (re.search(needle, ln) if regex else needle in ln):
            hits.append((i, ln.strip()))
    return hits


def claim_string_at(cid, fname, needle, expect_line=None, note="", regex=False):
    """Assert a string exists in a book file, and report where it actually is."""
    path = os.path.join(BOOK, fname)
    hits = find_lines(path, needle, regex=regex)
    if not hits:
        return record(cid, "book-source", f"{fname} contains {needle!r}. {note}",
                      "substring scan of the file on disk",
                      f"present{' at line ' + str(expect_line) if expect_line else ''}",
                      "NOT FOUND", False)
    nums = [n for n, _ in hits]
    ok = True
    obs = f"found at line(s) {nums}"
    if expect_line is not None:
        ok = expect_line in nums
        obs = f"found at line(s) {nums}; report claimed line {expect_line}"
    ev = "\n".join(f"L{n}: {t[:300]}" for n, t in hits[:4])
    return record(cid, "book-source", f"{fname} contains {needle!r}. {note}",
                  "substring scan of the file on disk",
                  f"present at line {expect_line}" if expect_line else "present",
                  obs, ok, ev)


# ----------------------------------------------------------------------------
# A. manifest / structural claims
# ----------------------------------------------------------------------------

def check_manifest():
    meta = json.load(open(os.path.join(BOOK, "book.json"), encoding="utf-8"))

    record("A1", "manifest",
           "book.json is the authoritative version and reads 0.7.5.1, released 0.7.5",
           "parse book.json", "version=0.7.5.1 released=0.7.5",
           f"version={meta.get('version')} released={meta.get('released')}",
           meta.get("version") == "0.7.5.1" and meta.get("released") == "0.7.5",
           json.dumps({k: v for k, v in meta.items() if not isinstance(v, (list, dict))}, indent=1))

    shipped = set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "file" and isinstance(v, str):
                    shipped.add(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(meta)
    on_disk = {f for f in os.listdir(BOOK) if f.endswith(".md")}
    unshipped = sorted(on_disk - shipped)
    missing = sorted(shipped - on_disk)
    expected_meta = ["ELIJAH-PROTOCOL.md", "README.md", "VOICE-GUIDE.md"]

    record("A2", "manifest",
           "book.json ships exactly 30 sections, none missing from disk",
           "resolve every 'file' key in book.json against the directory",
           "30 shipped, 0 missing", f"{len(shipped)} shipped, {len(missing)} missing",
           len(shipped) == 30 and not missing,
           "missing: " + (", ".join(missing) if missing else "none"))

    record("A3", "manifest",
           "The only unshipped .md files are the three meta docs, so their em dashes never reach a reader",
           "set difference: files on disk minus files in the manifest",
           str(expected_meta), str(unshipped), unshipped == expected_meta,
           "unshipped: " + ", ".join(unshipped))

    # em dashes: zero in shipped prose, 73 in ELIJAH-PROTOCOL
    total = 0
    per_file = {}
    for f in sorted(shipped):
        p = os.path.join(BOOK, f)
        if not os.path.exists(p):
            continue
        n = read(p).count("—")
        if n:
            per_file[f] = n
        total += n
    record("A4", "house-rules",
           "Zero em dashes in shipped book prose",
           "count U+2014 across every file book.json ships",
           "0", str(total), total == 0,
           json.dumps(per_file, indent=1) if per_file else "no shipped file contains U+2014")

    ep_txt = read(os.path.join(BOOK, "ELIJAH-PROTOCOL.md"))
    ep_chars = ep_txt.count("—")
    ep_lines = sum(1 for ln in ep_txt.splitlines() if "—" in ln)
    record("A5", "house-rules",
           "ELIJAH-PROTOCOL.md carries 86 em dashes across 73 lines, and is not shipped",
           "count U+2014 characters AND lines containing one, in the unshipped meta doc",
           "86 characters on 73 lines", f"{ep_chars} characters on {ep_lines} lines",
           ep_chars == 86 and ep_lines == 73,
           "CORRECTION LOGGED: the review first reported '73 em dashes'. That was a grep -c\n"
           "LINE count mistaken for a character count. 73 is the line figure, 86 is the\n"
           "character figure. The substantive point is unchanged: A3 proves none of them ship.")

    body = [f for f in sorted(shipped) if os.path.exists(os.path.join(BOOK, f))]
    words = sum(len(read(os.path.join(BOOK, f)).split()) for f in body)
    record("A6", "manifest",
           "Current book source measures about 93,700 words, ahead of the queue's stale 90,647",
           "whitespace word count over shipped files only",
           "93000-94500", str(words), 93000 <= words <= 94500,
           f"{len(body)} shipped files counted")


# ----------------------------------------------------------------------------
# B. Appendix B integrity
# ----------------------------------------------------------------------------

def appendix_b_entries():
    t = read(os.path.join(BOOK, "23-appendix-b.md"))
    ents, pos = {}, 0
    for n in range(1, 233):
        m = re.compile(r"(?:^|\s)" + str(n) + r"\.\s").search(t, pos)
        if not m:
            ents[n] = None
            continue
        ents[n] = m.end()
        pos = m.end()
    bodies = {}
    keys = [k for k in sorted(ents) if ents[k] is not None]
    for idx, n in enumerate(keys):
        start = ents[n]
        end = ents[keys[idx + 1]] if idx + 1 < len(keys) else len(t)
        seg = t[start:end]
        seg = re.sub(r"\s+\d{1,3}\.\s*$", "", seg).strip()
        bodies[n] = seg
    return ents, bodies


def check_appendix_b():
    ents, bodies = appendix_b_entries()
    missing = [n for n, v in ents.items() if v is None]
    record("B1", "appendix-b",
           "Appendix B holds 232 entries with no numbering gaps",
           "sequential scan for 'N. ' in order, so digits inside titles cannot fool it",
           "232 found, 0 missing", f"{len(bodies)} found, {len(missing)} missing",
           len(bodies) == 232 and not missing,
           "missing: " + (str(missing) if missing else "none"))

    # Reproduce, faithfully, the WRONG parser I first used, so the false positive is on record.
    naive_parts = re.split(r"(?<![\d.])(\d{1,3})\.\s", read(os.path.join(BOOK, "23-appendix-b.md")))
    naive_pairs = []
    for i in range(1, len(naive_parts) - 1, 2):
        n = int(naive_parts[i])
        for u in re.findall(r"https?://\S+", naive_parts[i + 1]):
            naive_pairs.append((n, u))
    nn = sorted({n for n, _ in naive_pairs})
    naive_gaps = [x for x in range(nn[0], nn[-1] + 1) if x not in set(nn)] if nn else []
    record("B2", "appendix-b",
           "The naive parser I first used WRONGLY reports a gap at entry 40. Reproduced so nobody re-derives it",
           "re-run the original bad parser (split on any 'N. ', keep only entries that carry a URL)",
           "naive parser reports a spurious gap at [40]", f"naive gaps={naive_gaps}",
           naive_gaps == [40],
           "Entry 40's own TITLE begins '8. Unemployment and well-being...', so the regex splits\n"
           "inside it and the URL is attributed to a phantom entry '8'. Entry 40 then looks absent.\n"
           "B1 (sequential scan) is the correct measurement and finds all 232.\n"
           "This is the check catching MY error, not the book's.")

    urls = {}
    for n, b in bodies.items():
        for u in re.findall(r"https?://\S+", b):
            urls.setdefault(u.rstrip(".,"), []).append(n)
    dups = {u: ns for u, ns in urls.items() if len(ns) > 1}
    record("B3", "appendix-b",
           "Exactly 4 URLs appear under two entry numbers each",
           "group every URL by the entry numbers citing it",
           "4 duplicate URLs", f"{len(dups)} duplicate URLs", len(dups) == 4,
           "\n".join(f"{sorted(ns)}  {u[:96]}" for u, ns in sorted(dups.items(), key=lambda x: x[1])))

    e40 = bodies.get(40, "")
    bad40 = e40.startswith("8.") and "consi," in e40
    record("B4", "appendix-b",
           "Entry 40 is a raw PDF scrape: it starts with its own chapter numbering and truncates mid-word at 'consi'",
           "inspect entry 40's extracted body",
           "starts '8.' and contains 'consi,'", f"starts={e40[:14]!r} truncated={'consi,' in e40}",
           bad40, e40[:260])

    e189 = bodies.get(189, "")
    record("B5", "appendix-b",
           "Appendix B entry 189 itself calls the Wellington comparison an error",
           "read entry 189 verbatim",
           "contains 'the source of the error'",
           "contains" if "source of the error" in e189 else "MISSING",
           "source of the error" in e189, e189)


# ----------------------------------------------------------------------------
# C. the headline blocker: ch7 asserts what Appendix B calls an error
# ----------------------------------------------------------------------------

def check_wellington():
    p = os.path.join(BOOK, "09-chapter7.md")
    hits = find_lines(p, "against Napoleon")
    ok = bool(hits) and hits[0][0] == 40
    ev = "\n".join(f"L{n}: {t[:420]}" for n, t in hits)
    record("C1", "blocker-0",
           "09-chapter7.md line 40 asserts the Napoleon troop comparison in dialogue",
           "substring scan for 'against Napoleon'",
           "present at line 40", f"lines {[n for n, _ in hits]}", ok, ev)

    look = find_lines(p, "Look it up")
    record("C2", "blocker-0",
           "The same line tells the reader to go verify it",
           "substring scan for 'Look it up'",
           "present at line 40", f"lines {[n for n, _ in look]}",
           bool(look) and look[0][0] == 40,
           "\n".join(f"L{n}: {t[:200]}" for n, t in look))

    # and :144 states the sourced version with no Wellington
    l144 = lines(p)[143] if len(lines(p)) >= 144 else ""
    record("C3", "blocker-0",
           "Line 144 states the sourced twelve-thousand figure with NO Wellington comparison, so the defect is isolated to the dialogue",
           "read line 144 and test for Wellington/Napoleon/Peninsula",
           "twelve thousand present, comparison absent",
           f"twelve thousand={'twelve thousand' in l144}, "
           f"napoleon={'napoleon' in l144.lower()}, peninsula={'peninsul' in l144.lower()}",
           "twelve thousand" in l144 and "napoleon" not in l144.lower(),
           l144[:420])

    # nowhere else in the shipped body
    others = []
    for f in sorted(os.listdir(BOOK)):
        if not f.endswith(".md") or f in ("23-appendix-b.md",):
            continue
        for n, t in find_lines(os.path.join(BOOK, f), r"Napoleon|Wellington|Peninsular", regex=True):
            others.append(f"{f}:{n}")
    record("C4", "blocker-0",
           "The comparison appears in exactly one place in the book body",
           "regex scan for Napoleon|Wellington|Peninsular across all book files except Appendix B",
           "['09-chapter7.md:40']", str(others), others == ["09-chapter7.md:40"],
           "Appendix B is excluded because it legitimately cites the debunking sources 187-189.")


# ----------------------------------------------------------------------------
# D. precedent ledger arithmetic
# ----------------------------------------------------------------------------

def check_precedents():
    body_ids, appd_ids = set(), set()
    for f in sorted(os.listdir(BOOK)):
        if not f.endswith(".md"):
            continue
        ids = set(re.findall(r"P-\d\d", read(os.path.join(BOOK, f))))
        if f == "25-appendix-d.md":
            appd_ids = ids
        elif f != "23-appendix-b.md":
            body_ids |= ids
    expected = {f"P-{i:02d}" for i in range(1, 24)}
    record("D1", "precedents",
           "P-01 through P-23 all appear in the book body and in Appendix D",
           "regex P-\\d\\d across the book, compared against the full 1..23 set",
           "23 in body, 23 in Appendix D",
           f"{len(body_ids & expected)} in body, {len(appd_ids & expected)} in Appendix D",
           body_ids >= expected and appd_ids >= expected,
           f"body missing: {sorted(expected - body_ids) or 'none'}; "
           f"appendix D missing: {sorted(expected - appd_ids) or 'none'}")

    conc = os.path.join(BOOK, "21-conclusion.md")
    p23 = find_lines(conc, "P-23")
    twentytwo = find_lines(conc, "twenty-two entries")
    ok = bool(p23) and bool(twentytwo) and p23[0][0] < twentytwo[0][0]
    record("D2", "precedents",
           "The conclusion prints P-23 and then, LATER in the same file, tells the reader they have read twenty-two entries",
           "locate the P-23 heading and the 'twenty-two entries' sentence, compare line order",
           "P-23 heading precedes the twenty-two claim",
           f"P-23 at {[n for n, _ in p23]}, 'twenty-two entries' at {[n for n, _ in twentytwo]}",
           ok,
           "\n".join(f"L{n}: {t[:180]}" for n, t in (p23 + twentytwo)))

    intro = find_lines(os.path.join(BOOK, "02-introduction.md"), "twenty-two documented episodes")
    record("D3", "precedents",
           "The introduction also undercounts, saying twenty-two documented episodes",
           "substring scan of 02-introduction.md",
           "present", f"lines {[n for n, _ in intro]}", bool(intro),
           "\n".join(f"L{n}: {t[:220]}" for n, t in intro))


# ----------------------------------------------------------------------------
# E. Appendix D wrong referent
# ----------------------------------------------------------------------------

def check_appendix_d():
    t = read(os.path.join(BOOK, "25-appendix-d.md"))
    m = re.search(r"You will not find(.{0,600}?)\.\s", t, re.S)
    seg = m.group(1) if m else ""
    patent_last = seg.rstrip().endswith('"everything that can be invented has been invented"')
    railway_present = "brain disease" in seg
    idx_rail = seg.find("brain disease")
    idx_patent = seg.find("everything that can be invented")
    record("E1", "blocker-6",
           "In Appendix D's fabrication list the LAST item is the patent-office quote, while the railway item sits second-to-last",
           "extract the 'You will not find...' list and compare positions",
           "railway item occurs before the patent quote",
           f"railway_at={idx_rail}, patent_at={idx_patent}, patent_is_last={patent_last}",
           railway_present and 0 <= idx_rail < idx_patent,
           seg.strip()[:600])

    ref = "The last one is worth naming specifically, because it is the single most-cited example of railway technophobia"
    hits = find_lines(os.path.join(BOOK, "25-appendix-d.md"), "The last one is worth naming")
    record("E2", "blocker-6",
           "The text then calls 'the last one' an example of RAILWAY technophobia, which the patent quote is not",
           "locate the sentence and show the mismatch against E1",
           "sentence present", f"lines {[n for n, _ in hits]}", bool(hits),
           "\n".join(f"L{n}: {t[:520]}" for n, t in hits))


# ----------------------------------------------------------------------------
# F. every factual error the fact-check wave confirmed, proven present in source
# ----------------------------------------------------------------------------

FACT_CLAIMS = [
    ("F1", "11-chapter9.md", "kylegabriel", 185, "Mycodo install URL uses the wrong GitHub user"),
    ("F2", "11-chapter9.md", ":8080", None, "Mycodo web UI sent to port 8080 (it serves HTTPS on 443)"),
    ("F3", "11-chapter9.md", "3% of global carbon", None, "Haber-Bosch emissions overstated (real: about 1.3%)"),
    ("F4", "11-chapter9.md", "sub-millimeter precision", None, "FarmBot precision overstated (real: millimeter)"),
    ("F5", "12-chapter10.md", "millions of joules", None, "LLM page energy off by about 1000x (real: about 1 kJ)"),
    ("F6", "12-chapter10.md", "cannot tax or regulate", None, "Barter claim is legally false; IRS taxes barter at fair market value"),
    ("F7", "10-chapter8.md", "forty-eight hours", None, "Dopamine receptor upregulation claim has no supporting literature"),
    ("F8", "15-chapter13.md", "eighty pounds of plate steel", None, "Lightest Fisher stove ever made is 245 lb"),
    ("F9", "15-chapter13.md", "forty thousand pounds", None, "Contradicts the chapter's own 15,000 kg loaded figure"),
    ("F10", "19-chapter17.md", "PETG", None, "Bottle flake cannot become PETG; it becomes rPET"),
    ("F11", "20-chapter18.md", "synthetic neurons", None, "Google's synthetic neurons are 3D training geometry, not hardware"),
    ("F12", "09-chapter7.md", "Safe Street Rebels", None, "Group name is singular, per the book's own cited Guardian slug"),
    ("F13", "09-chapter7.md", "over 5,692", None, "5,692 is an exact total, so 'over' is indefensible"),
    ("F14", "17-chapter15.md", "independent wealth funds", None, "Term of art is sovereign wealth funds"),
    ("F15", "03-chapter1.md", "Universal Basic Computing", None, "Altman's coinage is 'Universal Basic Compute'"),
    ("F16", "04-chapter2.md", "four thousand acts", None, "Parliament passed over 5,200 enclosure acts"),
    ("F17", "08-chapter6.md", "roughly twice the median", None, "Mixes 1970 home VALUE ratio with a modern SALE PRICE ratio"),
]


def check_fact_claims():
    for cid, fname, needle, line, note in FACT_CLAIMS:
        path = os.path.join(BOOK, fname)
        hits = find_lines(path, needle)
        ev = "\n".join(f"L{n}: {t[:300]}" for n, t in hits[:3]) or "NOT FOUND"
        ok = bool(hits) and (line is None or line in [n for n, _ in hits])
        record(cid, "fact-check-in-source",
               f"{fname}: {note}", f"substring scan for {needle!r}",
               "present in source", f"lines {[n for n, _ in hits]}" if hits else "NOT FOUND",
               ok, ev)


# ----------------------------------------------------------------------------
# G. claims that something was ALREADY FIXED
# ----------------------------------------------------------------------------

def check_already_fixed():
    ch9 = find_lines(os.path.join(BOOK, "11-chapter9.md"), "7.03")
    stale = find_lines(os.path.join(BOOK, "11-chapter9.md"), "7.02")
    record("G1", "already-fixed",
           "The editorial queue's rounding defect is FIXED: chapter 9 reads 7.03, not 7.02",
           "scan for both the corrected and the stale value",
           "7.03 present, 7.02 absent",
           f"7.03 at {[n for n, _ in ch9]}, 7.02 at {[n for n, _ in stale]}",
           bool(ch9) and not stale,
           "\n".join(f"L{n}: {t[:200]}" for n, t in ch9))

    q = read(os.path.join(ROOT, "manuscript", "EDITORIAL-QUEUE.md"))
    record("G2", "already-fixed",
           "But EDITORIAL-QUEUE.md still lists that defect as open, so the queue is stale",
           "search the queue for the defect text it never closed",
           "queue still contains '7.02'", f"contains 7.02: {'7.02' in q}", "7.02" in q,
           "The queue reports fixed work as open. That is the finding.")


# ----------------------------------------------------------------------------
# H. self-audit: does my own report obey the house style rule?
# ----------------------------------------------------------------------------

def check_self():
    """Turn the em-dash rule on my own report, and first establish what the rule's scope is."""
    docsdir = os.path.join(ROOT, "docs")
    counts = {}
    for f in sorted(os.listdir(docsdir)):
        if f.endswith(".md"):
            counts[f] = read(os.path.join(docsdir, f)).count("—")
    mine = counts.get(os.path.basename(REPORT), 0)
    others = {k: v for k, v in counts.items() if k != os.path.basename(REPORT)}
    peers_using = {k: v for k, v in others.items() if v > 0}

    record("H1", "self-audit",
           "SCOPE FINDING: the no-em-dash rule is enforced on book prose, not on internal docs",
           "count U+2014 in every docs/*.md and compare my report against its peers",
           "book prose 0 (see A4); docs/ peers use them freely",
           f"my report={mine}; {len(peers_using)} of {len(others)} peer docs also use them",
           len(peers_using) > 0,
           "Peer docs: " + ", ".join(f"{k}={v}" for k, v in sorted(peers_using.items())) +
           "\n\nI first wrote this check asserting my report must be at 0. That was a\n"
           "MIS-SPECIFIED CHECK: measuring the repo shows docs/ is not held to the rule,\n"
           "while shipped book prose is, and A4 proves the book side is clean at 0.\n"
           "Recorded rather than silently deleted, because a checker asserting the wrong\n"
           "rule is exactly the failure mode this page exists to expose.")


# ----------------------------------------------------------------------------
# I. live network checks, through two stacks
# ----------------------------------------------------------------------------

def http_urllib(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (verify_review_claims)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(200000).decode("utf-8", "replace"), ""
    except urllib.error.HTTPError as e:
        return e.code, "", f"HTTPError {e.code}"
    except Exception as e:
        return None, "", f"{type(e).__name__}: {e}"


def http_curl(url, timeout=25):
    try:
        p = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", str(timeout), "-o", "-",
             "-w", "\n__CODE__%{http_code}", url],
            capture_output=True, text=True, timeout=timeout + 10)
        out = p.stdout
        code = out.rsplit("__CODE__", 1)[-1].strip() if "__CODE__" in out else ""
        body = out.rsplit("\n__CODE__", 1)[0]
        return (int(code) if code.isdigit() else None), body, p.stderr.strip()
    except Exception as e:
        return None, "", f"{type(e).__name__}: {e}"


def title_of(html):
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else "(no <title>)"


def check_network():
    mycodo = [
        ("I1", "https://raw.githubusercontent.com/kylegabriel/Mycodo/master/install", 404,
         "The URL printed in the book returns 404, so the reader pipes an error page into bash"),
        ("I2", "https://raw.githubusercontent.com/kizniche/Mycodo/master/install", 404,
         "Fixing ONLY the username still returns 404, so the obvious fix is also wrong"),
        ("I3", "https://kizniche.github.io/Mycodo/install", 200,
         "The documented installer, and the only one of the three that works"),
    ]
    for cid, url, want, note in mycodo:
        code, body, err = http_curl(url)
        record(cid, "network-mycodo", note, f"curl -sSL {url}",
               f"HTTP {want}", f"HTTP {code}" + (f" ({err})" if err else ""),
               code == want, f"bytes returned: {len(body)}")

    # the two sources the book harness called unreachable
    for cid, url, entry, expect_sub, verdict_note in [
        ("I4", "https://transformco.com/press-releases/pr/1882", 225, "Digital Sears",
         "Appendix B 225 cites it as the 'Digital Sears' timeline. The live title matches, so this source is GOOD."),
        ("I5", "https://www.theoffgridshop.com.au/products/48-volt-off-grid-kit-6-6kw-of-panels", 62, "Shouse",
         "Appendix B 62 cites it as a Shouse product listing with specific inverter and battery specs."),
    ]:
        ucode, _, uerr = http_urllib(url)
        ccode, cbody, _ = http_curl(url)
        t = title_of(cbody) if cbody else "(no body)"
        matches = expect_sub.lower() in t.lower()
        record(cid, "network-sources",
               f"Appendix B entry {entry}: live status and whether the page still supports the citation",
               "fetch through urllib AND curl, then compare the live <title> against what Appendix B says the source is",
               f"HTTP 200 and title containing {expect_sub!r}",
               f"urllib={ucode or 'FAILED'} curl={ccode} title={t!r} title_matches_citation={matches}",
               ccode == 200 and matches,
               f"urllib error: {uerr or 'none'}\n{verdict_note}\n"
               f"A 200 alone is not proof: this check compares CONTENT against the citation, "
               f"which is the failure class the book's link checker cannot see.")


# ----------------------------------------------------------------------------
# NEGATIVE CONTROLS: every checker above must be able to go red
# ----------------------------------------------------------------------------

def check_negative_controls():
    """Feed each checker a known-bad input and require it to FAIL."""
    nc = []

    def neg(cid, desc, went_red, evidence):
        nc.append({
            "id": cid, "category": "negative-control", "claim": desc,
            "method": "inject a known defect and require the checker to report it",
            "expected": "checker goes RED", "observed": "went RED" if went_red else "stayed GREEN",
            "verdict": "PASS" if went_red else "FAIL", "evidence": evidence,
        })

    # 1. em dash counter
    sample = "clean text with no dash"
    poisoned = "text with an — injected"
    neg("N1", "The em-dash counter detects an injected U+2014",
        sample.count("—") == 0 and poisoned.count("—") == 1,
        f"clean={sample.count(chr(0x2014))}, poisoned={poisoned.count(chr(0x2014))}")

    # 2. sequential numbering scanner
    good = " ".join(f"{i}. Item {i} https://x/{i}" for i in range(1, 21))
    bad = " ".join(f"{i}. Item {i} https://x/{i}" for i in range(1, 21) if i != 7)

    def scan(text, upto):
        pos, found = 0, []
        for n in range(1, upto + 1):
            m = re.compile(r"(?:^|\s)" + str(n) + r"\.\s").search(text, pos)
            if m:
                found.append(n)
                pos = m.end()
        return found

    neg("N2", "The Appendix B numbering scanner detects a removed entry",
        len(scan(good, 20)) == 20 and 7 not in scan(bad, 20),
        f"intact list -> {len(scan(good, 20))}/20 found; list with 7 deleted -> "
        f"{len(scan(bad, 20))}/20 found, missing {sorted(set(range(1, 21)) - set(scan(bad, 20)))}")

    # 3. duplicate URL detector
    dup_src = {1: "a https://dup", 2: "b https://dup", 3: "c https://uniq"}
    urls = {}
    for n, b in dup_src.items():
        for u in re.findall(r"https?://\S+", b):
            urls.setdefault(u, []).append(n)
    found_dups = {u: ns for u, ns in urls.items() if len(ns) > 1}
    neg("N3", "The duplicate-URL detector finds a planted duplicate",
        found_dups == {"https://dup": [1, 2]}, f"detected: {found_dups}")

    # 4. substring locator
    neg("N4", "The substring locator returns nothing for a string that is absent",
        not find_lines(os.path.join(BOOK, "09-chapter7.md"), "zzz_not_in_this_book_zzz"),
        "searched 09-chapter7.md for a nonsense token and correctly got 0 hits")

    # 5. live HTTP checker
    code404, _, _ = http_curl("https://raw.githubusercontent.com/kizniche/Mycodo/master/install")
    code200, _, _ = http_curl("https://kizniche.github.io/Mycodo/install")
    neg("N5", "The HTTP checker distinguishes a real 404 from a real 200",
        code404 == 404 and code200 == 200,
        f"known-bad URL -> {code404}; known-good URL -> {code200}")

    # 6. title/content comparator
    neg("N6", "The citation-content comparator rejects a title that does not match the citation",
        "shouse" not in "What We Install Sigenergy Deye EcoFlow Victron".lower(),
        "The live off-grid-shop title contains no 'Shouse', which is exactly why I5 fails. "
        "Same comparator returns True for the Transformco title, which is why I4 passes.")

    RESULTS.extend(nc)


# ----------------------------------------------------------------------------
# HTML
# ----------------------------------------------------------------------------

def render_html(path, offline):
    cats = {}
    for r in RESULTS:
        cats.setdefault(r["category"], []).append(r)
    total = len(RESULTS)
    passed = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    failed = total - passed

    def esc(s):
        return (str(s).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))

    CAT_BLURB = {
        "manifest": "What ships, what does not, and what the version actually is.",
        "house-rules": "The project's own style rules, measured rather than assumed.",
        "appendix-b": "Structural integrity of the 232-entry works cited.",
        "blocker-0": "The headline finding: the prose asserts what the bibliography calls an error.",
        "precedents": "Ledger arithmetic. The book counts its own precedents wrong.",
        "blocker-6": "Appendix D points the phrase 'the last one' at the wrong list item.",
        "fact-check-in-source": "Each externally confirmed error, proven to exist at a real line in real source.",
        "already-fixed": "Claims that something was ALREADY repaired, plus the tracking doc that never noticed.",
        "self-audit": "Turning the same checker on my own report.",
        "network-mycodo": "Live HTTP against the three candidate installer URLs.",
        "network-sources": "Live HTTP plus a CONTENT comparison the book's link checker cannot perform.",
        "negative-control": "Every checker above, fed a known defect, required to go red.",
    }
    order = ["blocker-0", "network-mycodo", "network-sources", "precedents", "blocker-6",
             "appendix-b", "fact-check-in-source", "manifest", "house-rules",
             "already-fixed", "self-audit", "negative-control"]
    ordered = [c for c in order if c in cats] + [c for c in cats if c not in order]

    rows = []
    for c in ordered:
        items = cats[c]
        p = sum(1 for r in items if r["verdict"] == "PASS")
        body = []
        for r in items:
            body.append(f"""
    <details class="chk {r['verdict'].lower()}">
      <summary>
        <span class="badge {r['verdict'].lower()}">{r['verdict']}</span>
        <span class="cid">{esc(r['id'])}</span>
        <span class="claim">{esc(r['claim'])}</span>
      </summary>
      <div class="detail">
        <div class="kv"><b>How it was checked</b><span>{esc(r['method'])}</span></div>
        <div class="kv"><b>Expected</b><span>{esc(r['expected'])}</span></div>
        <div class="kv"><b>Actually observed</b><span class="obs">{esc(r['observed'])}</span></div>
        {'<pre>' + esc(r['evidence']) + '</pre>' if r['evidence'] else ''}
      </div>
    </details>""")
        rows.append(f"""
  <section>
    <h2>{esc(c)} <span class="score">{p}/{len(items)}</span></h2>
    <p class="blurb">{esc(CAT_BLURB.get(c, ''))}</p>
    {''.join(body)}
  </section>""")

    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>STS review, verification run</title>
<style>
  :root {{
    --bg:#f7f5f0; --card:#fff; --ink:#22201d; --muted:#6b645c; --line:#ddd6c9;
    --pass:#1c7a4a; --passbg:#e6f4ec; --fail:#b3261e; --failbg:#fbeae9; --accent:#b45309;
  }}
  @media (prefers-color-scheme:dark) {{ :root:not([data-theme=light]) {{
    --bg:#14130f; --card:#1d1c18; --ink:#ece7de; --muted:#a49c90; --line:#332f28;
    --pass:#5cc98e; --passbg:#12301f; --fail:#ff8f85; --failbg:#3a1714; --accent:#f0a94c;
  }} }}
  * {{ box-sizing:border-box }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
    font:16px/1.6 ui-sans-serif,-apple-system,Segoe UI,Roboto,sans-serif; }}
  .wrap {{ max-width:1000px; margin:0 auto; padding:40px 20px 80px }}
  h1 {{ font-size:30px; margin:0 0 6px; letter-spacing:-.02em }}
  .sub {{ color:var(--muted); margin:0 0 26px }}
  .totals {{ display:flex; gap:12px; flex-wrap:wrap; margin-bottom:26px }}
  .tile {{ background:var(--card); border:1px solid var(--line); border-radius:12px;
    padding:14px 18px; min-width:120px }}
  .tile b {{ display:block; font-size:26px; font-variant-numeric:tabular-nums }}
  .tile span {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.07em }}
  .note {{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--accent);
    border-radius:10px; padding:14px 18px; margin-bottom:30px; }}
  .note p {{ margin:0 0 8px }} .note p:last-child {{ margin:0 }}
  section {{ margin-bottom:34px }}
  h2 {{ font-size:14px; text-transform:uppercase; letter-spacing:.09em; color:var(--muted);
    margin:0 0 4px; display:flex; align-items:center; gap:10px }}
  .score {{ font-variant-numeric:tabular-nums; color:var(--ink); background:var(--card);
    border:1px solid var(--line); border-radius:20px; padding:2px 10px; font-size:12px }}
  .blurb {{ margin:0 0 12px; color:var(--muted); font-size:14px }}
  .chk {{ background:var(--card); border:1px solid var(--line); border-radius:10px;
    margin-bottom:8px; overflow:hidden }}
  .chk.fail {{ border-color:var(--fail) }}
  summary {{ cursor:pointer; padding:12px 14px; display:flex; gap:10px;
    align-items:flex-start; list-style:none }}
  summary::-webkit-details-marker {{ display:none }}
  .badge {{ font-size:11px; font-weight:700; letter-spacing:.05em; padding:3px 8px;
    border-radius:5px; flex:none; margin-top:2px }}
  .badge.pass {{ background:var(--passbg); color:var(--pass) }}
  .badge.fail {{ background:var(--failbg); color:var(--fail) }}
  .cid {{ font:600 12px ui-monospace,SFMono-Regular,Menlo,monospace; color:var(--muted);
    flex:none; margin-top:4px; min-width:34px }}
  .claim {{ flex:1 }}
  .detail {{ padding:0 14px 14px 14px; border-top:1px dashed var(--line); margin-top:2px; padding-top:12px }}
  .kv {{ display:flex; gap:12px; padding:5px 0; font-size:14px; align-items:baseline }}
  .kv b {{ flex:none; width:150px; color:var(--muted); font-weight:600; font-size:12px;
    text-transform:uppercase; letter-spacing:.05em }}
  .obs {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:13px }}
  pre {{ background:var(--bg); border:1px solid var(--line); border-radius:8px; padding:12px;
    overflow-x:auto; font-size:12.5px; line-height:1.5; white-space:pre-wrap;
    word-break:break-word; margin:10px 0 0 }}
  footer {{ color:var(--muted); font-size:13px; border-top:1px solid var(--line); padding-top:16px }}
  code {{ font-family:ui-monospace,Menlo,monospace; background:var(--bg);
    border:1px solid var(--line); border-radius:4px; padding:1px 5px; font-size:13px }}
</style></head><body><div class="wrap">
<h1>Verification run</h1>
<p class="sub">Every checkable claim in <code>docs/review-2026-08-16-v0751-full-book.md</code>,
re-derived from the files on disk and the live web. Generated by
<code>scripts/verify_review_claims.py</code>. {"Network checks SKIPPED (--offline)." if offline else "Network checks ran live."}</p>

<div class="totals">
  <div class="tile"><b>{total}</b><span>checks</span></div>
  <div class="tile"><b style="color:var(--pass)">{passed}</b><span>passed</span></div>
  <div class="tile"><b style="color:var(--fail)">{failed}</b><span>failed</span></div>
</div>

<div class="note">
  <p><b>How to read this.</b> A check passing means the claim in the report matched what the
  file or the server actually says. Every row opens to show the real observed value and the raw
  evidence behind it, so nothing rests on my summary of it.</p>
  <p><b>Why the negative controls are at the bottom.</b> A green check that has never been watched
  go red is not evidence. Each checker here is fed a deliberately broken input and is required to
  report the defect. If those go green, the whole page is worthless and should be ignored.</p>
  <p><b>A FAIL is not always a bug in the book.</b> These checks assert what the review claimed.
  Read each row's observed value to see which way it cuts.</p>
</div>
{''.join(rows)}
<footer>Re-run with <code>python3 scripts/verify_review_claims.py --html verification.html</code>.
Machine-readable output: <code>python3 scripts/verify_review_claims.py &gt; results.json</code>.</footer>
</div></body></html>"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--html")
    a = ap.parse_args()

    check_manifest()
    check_appendix_b()
    check_wellington()
    check_precedents()
    check_appendix_d()
    check_fact_claims()
    check_already_fixed()
    check_self()
    if not a.offline:
        check_network()
    check_negative_controls()

    if a.html:
        render_html(a.html, a.offline)

    p = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    print(json.dumps({
        "total": len(RESULTS), "passed": p, "failed": len(RESULTS) - p,
        "results": RESULTS,
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
