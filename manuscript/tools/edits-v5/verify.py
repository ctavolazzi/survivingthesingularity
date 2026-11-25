#!/usr/bin/env python3
"""Check every edit in the v5 edit list against a fresh read of the v5 Doc.

    python3 manuscript/tools/edits-v5/verify.py READ.json [--table FILE] [--require accepted|present]

READ.json is the Docs connector's read_doc output for "StS v5 draft (Nov 23)". The checks for each edit are in
checks.py next to this file: words that must be in the book once the edit is made, and words that must be gone.
In a check, "[break]" stands for a scene break (an empty paragraph in the Doc).

Each edit gets one status:
  accepted        the change is in the text itself
  suggested       the change is in the Doc as a suggestion, not accepted yet
  not in the Doc  nothing of it is there yet
  PARTIAL         some of it is there and some is not: look at it by hand

--table FILE      also writes the status table as Markdown (EDITS-v5-status.md)
--require accepted  exit 1 unless every edit is accepted (used before a rebuild)
--require present   exit 1 unless every edit is at least suggested
Without --require it exits 1 only if an edit is PARTIAL.
"""
import argparse, datetime, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from checks import C

def views(path):
    d = json.load(open(path))
    d = d.get("content", d)
    acc, orig, ids = [], [], set()
    for el in d["tabs"][0]["documentTab"]["body"]["content"]:
        p = el.get("paragraph")
        if not p:
            continue
        for e in p["elements"]:
            tr = e.get("textRun")
            if not tr:
                continue
            si, sd = tr.get("suggestedInsertionIds"), tr.get("suggestedDeletionIds")
            ids.update(si or []); ids.update(sd or [])
            if not sd:
                acc.append(tr["content"])
            if not si:
                orig.append(tr["content"])
    return d.get("revisionId", ""), "".join(acc), "".join(orig), len(ids)

def flat(s):
    s = s.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"').replace("\xa0", " ")
    s = re.sub(r"\n[ \t\xa0]*\n", " [break] ", s)  # an empty paragraph is a scene break
    return re.sub(r"\s+", " ", s)

def status(A, O, have, gone):
    in_a = all(flat(h) in A for h in have) and not any(flat(g) in A for g in gone)
    in_o = all(flat(h) in O for h in have) and not any(flat(g) in O for g in gone)
    none_a = not any(flat(h) in A for h in have) and (not gone or all(flat(g) in A for g in gone))
    if in_o:
        return "accepted"
    if in_a:
        return "suggested"
    if none_a:
        return "not in the Doc"
    return "PARTIAL"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("read")
    ap.add_argument("--table")
    ap.add_argument("--require", choices=["accepted", "present"])
    a = ap.parse_args()
    rev, acc, orig, nsug = views(a.read)
    A, O = flat(acc), flat(orig)
    rows = []
    for n, where, have, gone in sorted(C, key=lambda r: r[0]):
        rows.append((n, where, status(A, O, have, gone), have[0] if have else "gone: " + gone[0]))
    counts = {}
    for r in rows:
        counts[r[2]] = counts.get(r[2], 0) + 1
    print(f"revision {rev[:24]}  pending suggestions in the Doc: {nsug}")
    for n, where, st, _ in rows:
        print(f"{n:>3}  {where:<18} {st}")
    print("totals:", ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    if a.table:
        today = datetime.date.today().isoformat()
        out = [f"# v5 edits: status of every edit", "",
               f"Written by `manuscript/tools/edits-v5/verify.py` on {today} from a read of the Doc \"StS v5 draft",
               f"(Nov 23)\", revision `{rev}`. {nsug} suggestions were waiting in the Doc at that read.",
               "", "Totals: " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())) + ".", "",
               "The edits themselves, with CT's words, are in `EDITS-v5-pending.md`. Row 90 in `checks.py` is the",
               "follow-ups of 25 November (bill, rate hike, San Jose, notary); it is listed here as \"follow-ups\".",
               "Edit 57 was never used. Edit 132 was cut by CT.", "",
               "| Edit | Where | Status | Checked for |", "|---|---|---|---|"]
        for n, where, st, key in rows:
            label = "follow-ups" if where == "follow-ups" else str(n)
            key = key.replace("\n", " / ").replace("|", "/")
            key = key if len(key) <= 70 else key[:67] + "..."
            out.append(f"| {label} | {where} | {st} | {key} |")
        Path(a.table).write_text("\n".join(out) + "\n", encoding="utf-8")
    bad = [r for r in rows if r[2] == "PARTIAL"]
    if a.require == "accepted":
        bad = [r for r in rows if r[2] != "accepted"]
    elif a.require == "present":
        bad = [r for r in rows if r[2] not in ("accepted", "suggested")]
    if bad:
        print("NOT READY:", ", ".join(f"{r[0]} ({r[2]})" for r in bad))
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
