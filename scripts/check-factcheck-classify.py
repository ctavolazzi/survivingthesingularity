#!/usr/bin/env python3
"""check-factcheck-classify.py - assert-based guard on the factcheck verdict logic.

WHY THIS EXISTS

Two verdicts in the 2026-08-01 network pass were wrong, and both were the
instrument failing rather than the source:

  UNREACHABLE  https://d-nb.info/1308833946/34
      A live PDF. The host answers `Content-Type: application/pdf;charset=base64`,
      so get_content_charset() returns 'base64', and bytes.decode('base64')
      raises LookupError. A working source was reported dead by a decode crash.

  SOFT_404     https://en.wikipedia.org/wiki/Kit_house
      A live article. The marker scan read the whole page and hit a footnote
      21,000 characters in: "the katrina cottage plans are no longer available
      at lowe's". The cited work was on the page the entire time.

The second one is the dangerous shape. Relaxing a check to clear a false
positive can silently turn the check off, and a check that cannot fail is worse
than no check because it launders an unverified bibliography into a
verified-looking one. So every relaxation here is paired with a NEGATIVE
CONTROL: a synthetic input that must still be condemned. If the controls stop
failing, this file starts failing.

Run:  python3 scripts/check-factcheck-classify.py
Exit: 0 all assertions hold, 1 otherwise.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from factcheck_network import classify, visible_text  # noqa: E402

FAILURES: list[str] = []
CHECKS = 0


def check(label: str, got, want) -> None:
    global CHECKS
    CHECKS += 1
    if got != want:
        FAILURES.append(f"{label}\n      wanted: {want}\n      got:    {got}")


def resp(body: str, ctype: str = "text/html; charset=utf-8", status: int = 200) -> dict:
    return {"status": status, "final_url": "https://example.test/x",
            "content_type": ctype, "body": body, "reason": ""}


def cite(title: str, url: str = "https://example.test/x") -> dict:
    return {"n": 1, "title": title, "url": url}


# ------------------------------------------------------------------ regressions

# 1. The Kit_house shape. Marker present, but buried far from the top AND the
#    cited title is plainly on the page. Must NOT be condemned.
kit_body = (
    "<h1>Kit house</h1><p>A kit house is a house sold in pieces.</p>"
    + "<p>filler about prefabricated housing.</p>" * 400
    + "<ol><li>\"The Katrina Cottage plans are no longer available at Lowe's,\""
      " lowes.com, accessed 6 July 2011</li></ol>"
)
check("kit_house is not a soft 404",
      classify(cite("Kit house"), resp(kit_body))["state"], "LIVE_CONFIRMED")

# 2. NEGATIVE CONTROL for the above. Same marker, but the cited work is absent.
#    This MUST still be SOFT_404 or the relaxation above disabled the check.
check("NEGATIVE CONTROL: genuine soft 404 is still caught",
      classify(cite("Some Vanished Monograph On Rotifers"),
               resp("<h1>Page not found</h1><p>This content is no longer available.</p>")
               )["state"],
      "SOFT_404")

# 3. NEGATIVE CONTROL: a parked domain with no relation to the citation.
check("NEGATIVE CONTROL: parked domain is still caught",
      classify(cite("Distributed Ledger Governance In Practice"),
               resp("<h1>buy this domain</h1><p>domain is for sale</p>"))["state"],
      "SOFT_404")

# ------------------------------------------------------------------ unchanged behaviour

# 4. A wall with the work absent is still WALLED, and is reported before the
#    unconfirmed fallback.
check("wall with cited work absent is still WALLED",
      classify(cite("Entirely Unrelated Title Words Here"),
               resp("<p>Please enable cookies to continue</p>"))["state"],
      "WALLED")

# 5. A wall with the work PRESENT is not a wall. Real articles carry banners.
check("wall with cited work present is confirmed",
      classify(cite("Rotifer Population Dynamics"),
               resp("<p>please enable cookies</p><h1>Rotifer Population Dynamics</h1>"
                    "<p>full text of the article on rotifer population dynamics</p>")
               )["state"],
      "LIVE_CONFIRMED")

# 6. Non-HTML is live but never confirmed, whatever the declared charset says.
check("PDF is LIVE_UNVERIFIED, not confirmed",
      classify(cite("Anything At All"),
               resp("%PDF-1.6 binary", ctype="application/pdf;charset=base64"))["state"],
      "LIVE_UNVERIFIED")

# 7. A refusal is never called dead.
for code in (401, 403, 429):
    check(f"HTTP {code} is BLOCKED, not DEAD",
          classify(cite("X"), resp("", status=code))["state"], "BLOCKED")

# 8. A real 404 still is dead.
for code in (404, 410):
    check(f"HTTP {code} is DEAD", classify(cite("X"), resp("", status=code))["state"], "DEAD")

# ------------------------------------------------------------------ decode guard

# 9. The exact crash that produced the UNREACHABLE verdict. Proving the premise
#    is real, so this file fails loudly if Python ever makes it stop raising.
try:
    b"%PDF-1.6".decode("base64")
    FAILURES.append("premise broken: decode('base64') no longer raises, revisit fetch()")
except LookupError:
    pass
CHECKS += 1

# 10. The fallback the fetch() fix relies on.
check("utf-8 fallback decodes PDF bytes without raising",
      b"%PDF-1.6".decode("utf-8", errors="replace")[:5], "%PDF-")

# 11. visible_text strips markup so markers match what a reader sees.
check("visible_text strips script bodies",
      "alert" in visible_text("<script>alert('page not found')</script><p>hello</p>"), False)


print(f"factcheck classify guard  {CHECKS} checks")
if FAILURES:
    print(f"\n  {len(FAILURES)} FAILED\n")
    for f in FAILURES:
        print(f"    {f}\n")
    sys.exit(1)
print("  all pass")
sys.exit(0)
