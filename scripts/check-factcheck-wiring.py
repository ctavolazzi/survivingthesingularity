#!/usr/bin/env python3
"""check-factcheck-wiring.py - guard on the seam between the two factcheck halves.

WHY THIS EXISTS

`sts factcheck` used to hardcode `network: False` and stamp all 227 URL claims
UNCHECKED, while scripts/factcheck_network.py wrote 220 real verdicts into
.factcheck-cache/ that nothing ever read. Wiring them together moved 167 claims
from UNCHECKED to SUPPORTED, which is exactly the kind of change that is easy to
get quietly wrong in the generous direction.

Three failure modes are worth more than the feature:

  1. Over-promotion. Anything other than LIVE_CONFIRMED reading as verified. A
     403 from researchgate is a fact about researchgate, and if it ever renders
     as SUPPORTED the audit is lying on a public page.
  2. A dead branch. DEAD and SOFT_404 map to UNSUPPORTED, and with zero dead
     links in the corpus that path never executes in production. An untested
     branch is worth what it costs to write, so it is exercised here against a
     synthetic cache.
  3. Silent network claims. An absent cache must fall back to the old offline
     behaviour and say so, never assert a network run that did not happen.

Run:  python3 scripts/check-factcheck-wiring.py
Exit: 0 all assertions hold, 1 otherwise.
"""

import argparse
import contextlib
import importlib.util
import io
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

spec = importlib.util.spec_from_file_location("sts_under_test", HERE / "sts.py")
sts = importlib.util.module_from_spec(spec)
sys.modules["sts_under_test"] = sts
spec.loader.exec_module(sts)

FAILURES: list[str] = []
CHECKS = 0


def check(label: str, got, want) -> None:
    global CHECKS
    CHECKS += 1
    if got != want:
        FAILURES.append(f"{label}\n      wanted: {want}\n      got:    {got}")


# ------------------------------------------------------- 1. the mapping itself

M = sts.FC_NET_TO_VERDICT

check("LIVE_CONFIRMED is the ONLY state that promotes to SUPPORTED",
      sorted(k for k, v in M.items() if v == sts.FC_SUPPORTED), ["LIVE_CONFIRMED"])

for state in ("BLOCKED", "WALLED", "LIVE_UNVERIFIED", "LIVE_UNCONFIRMED",
              "SERVER_ERROR", "UNREACHABLE", "OTHER"):
    check(f"{state} stays UNCHECKED, a refusal is not a failed citation",
          M[state], sts.FC_UNCHECKED)

for state in ("DEAD", "SOFT_404"):
    check(f"{state} is UNSUPPORTED", M[state], sts.FC_UNSUPPORTED)


# ------------------------------------------------------- 2. the cache loader

check("absent cache dir loads as empty, not as a crash",
      sts._fc_network_cache.__call__() is not None, True)

TMP = ROOT / ".factcheck-cache-selftest"


def write_cache(records: list[dict]) -> None:
    shutil.rmtree(TMP, ignore_errors=True)
    TMP.mkdir(parents=True)
    for i, r in enumerate(records):
        (TMP / f"{i}.json").write_text(json.dumps(r), encoding="utf-8")


def with_cache(rel: str):
    """Run cmd_factcheck against a chosen cache dir, return (report, summary).

    Run TWICE on purpose. `--json` returns before the human summary is printed,
    so a single json=True run captures a report and an empty summary, and an
    assertion against that summary can never fail. This file caught exactly that
    bug in itself, which is the only reason to trust the assertions below it.
    """
    old = sts.FC_NET_CACHE_REL
    sts.FC_NET_CACHE_REL = rel
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sts.cmd_factcheck(argparse.Namespace(json=True, out=None))
        report = json.loads(buf.getvalue())

        buf2 = io.StringIO()
        with contextlib.redirect_stdout(buf2):
            sts.cmd_factcheck(argparse.Namespace(json=False, out=None))
        return report, buf2.getvalue()
    finally:
        sts.FC_NET_CACHE_REL = old


try:
    # A truncated entry is a miss, not a crash.
    write_cache([{"url": "https://example.test/a", "state": "LIVE_CONFIRMED"}])
    (TMP / "broken.json").write_text("{not json", encoding="utf-8")
    old = sts.FC_NET_CACHE_REL
    sts.FC_NET_CACHE_REL = TMP.name
    loaded = sts._fc_network_cache()
    sts.FC_NET_CACHE_REL = old
    check("truncated cache entry is skipped, the rest still load", len(loaded), 1)

    # --------------------------------------------- 3. the dead branch, end to end

    # Take a URL the book really cites and declare it dead, then confirm the
    # claim is actually condemned rather than quietly staying UNCHECKED.
    real, _ = with_cache(".factcheck-cache")
    real_urls = [c["url"] for c in real["claims"] if c["type"] == "url"]
    if not real_urls:
        FAILURES.append("no url claims found, the rest of this file proves nothing")
        victim = "https://example.test/none"
    else:
        victim = real_urls[0]

    write_cache([{"url": victim, "state": "DEAD", "status": 404,
                  "detail": "HTTP 404", "final_url": victim}])
    dead_report, _ = with_cache(TMP.name)
    victim_claims = [c for c in dead_report["claims"]
                     if c["type"] == "url" and c["url"] == victim]
    check("a DEAD citation produces at least one claim", bool(victim_claims), True)
    check("a DEAD citation is condemned UNSUPPORTED, not left UNCHECKED",
          sorted({c["verdict"] for c in victim_claims}), [sts.FC_UNSUPPORTED])
    check("a DEAD citation records its real source_state",
          sorted({c["source_state"] for c in victim_claims}), ["DEAD"])

    # NEGATIVE CONTROL for the above: the same URL marked BLOCKED must NOT be
    # condemned. If this ever flips, a host refusing robots reads as a bad source.
    write_cache([{"url": victim, "state": "BLOCKED", "status": 403,
                  "detail": "HTTP 403, host refused an automated request.",
                  "final_url": victim}])
    blocked_report, _ = with_cache(TMP.name)
    blocked_claims = [c for c in blocked_report["claims"]
                      if c["type"] == "url" and c["url"] == victim]
    check("NEGATIVE CONTROL: a BLOCKED citation is NOT condemned",
          sorted({c["verdict"] for c in blocked_claims}), [sts.FC_UNCHECKED])

    # --------------------------------------------- 4. no silent network claims

    offline, offline_out = with_cache(".factcheck-cache-DOES-NOT-EXIST")
    check("absent cache reports network False", offline["network"], False)
    check("absent cache says so in the printed summary",
          "network: OFF" in offline_out, True)
    check("absent cache lists external liveness as not covered",
          any("no network record exists" in nc["why"].lower()
              for nc in offline["not_covered"]), True)

    # And the live one must carry a real receipt rather than a bare true.
    check("present cache reports a receipt, not a bare boolean",
          isinstance(real["network"], dict), True)
    check("the receipt counts resolved claims",
          real["network"]["url_claims_resolved"] > 0, True)
    check("resolved plus unresolved equals every url claim",
          real["network"]["url_claims_resolved"]
          + real["network"]["url_claims_unresolved"],
          real["network"]["url_claims"])

    # The headline promise: nothing but LIVE_CONFIRMED became SUPPORTED.
    promoted = {c["source_state"] for c in real["claims"]
                if c["type"] == "url" and c["verdict"] == sts.FC_SUPPORTED}
    check("in the real corpus, only LIVE_CONFIRMED claims are SUPPORTED",
          sorted(promoted), ["LIVE_CONFIRMED"])

finally:
    shutil.rmtree(TMP, ignore_errors=True)

print(f"factcheck wiring guard  {CHECKS} checks")
if FAILURES:
    print(f"\n  {len(FAILURES)} FAILED\n")
    for f in FAILURES:
        print(f"    {f}\n")
    sys.exit(1)
print("  all pass")
sys.exit(0)
