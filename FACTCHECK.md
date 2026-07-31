# `sts factcheck`: the chain of custody

**Status: BUILT and running.** Written 2026-07-31 against `sts.py` at `ad98b87`.
Everything below was measured, not estimated. Re-run the commands and check.

The question this answers is one sentence long:

> For any single claim in the book, what makes it true, and where exactly does
> that stop being knowable?

`verify math` recomputes the arithmetic, `verify precedents` checks ledger
integrity, `verify links` pings Works Cited over the network, and `art list`
ties figures to the catalog. None of them answers the question above, because
none of them follows a single claim from the sentence on the page all the way
back to its evidence and reports where the trail dies.

---

## What it produces

```bash
python3 scripts/sts.py factcheck                          # summary to stdout
python3 scripts/sts.py factcheck --out docs/factcheck.json # the inventory
python3 scripts/build_factcheck_trace.py docs/factcheck.json docs/trace.html
```

`sts.py` owns the measurement. `build_factcheck_trace.py` owns the page. That
split is deliberate: sts.py is stdlib only and single file, and a thousand
lines of HTML template is a rendering concern that does not belong in a
measurement tool.

The page is self-contained, opens from `file://`, and computes every number it
displays in the browser from its own embedded records. It cannot drift from its
own data because there is no second copy of the data to drift from.

---

## The ten hops

Every claim gets all ten. A hop that cannot be resolved is recorded BROKEN with
a reason. **Nothing is ever inferred.** A hop that is merely plausible is still
BROKEN.

| # | Hop | Resolvable locally |
|---|---|---|
| 1 | claim, quoted verbatim | yes |
| 2 | type | yes |
| 3 | location, file and line | yes |
| 4 | block id | yes, this is the anchor |
| 5 | git receipt, SHA plus author plus date | yes |
| 6 | github permalink pinned to a SHA | yes |
| 7 | source | only for internal refs and figures |
| 8 | source state | **no, needs network** |
| 9 | archive.org snapshot | **no, needs network** |
| 10 | verdict | yes |

Hop 4 is the anchor, not hop 3. Line numbers rot on the next edit above them.
Block ids from `sts id` survive it.

---

## The receipt states, which are the load-bearing idea

A permalink is only worth anything if it resolves for somebody who is not you.
So the receipt is resolved against **blob identity with origin**, in three
states:

| State | Meaning | Permalink |
|---|---|---|
| `origin_exact` | the working file is byte identical to the file at `origin/main` | **minted.** Current line numbers are valid at that SHA |
| `local_only` | committed here, but the file differs from origin | **not minted** |
| `uncommitted` | dirty in the working tree | **not minted** |

The temptation is to pin every receipt to `git blame`'s SHA and call it done.
That produces links that 404 for every reader but the machine that made them,
which is worse than no link, because a broken receipt that looks authoritative
is how a citation problem hides.

`origin_exact` is checked by comparing `git hash-object <file>` against
`git rev-parse origin/main:<path>`. Blob equality is the only thing that
guarantees the line numbers in the permalink point at the text being cited.
The blame SHA, author and date are still recorded as provenance even when no
permalink can be minted, because they are true and useful; they are just not a
link.

**As of 2026-07-30 this gap is large and it is the most actionable finding in
the whole pass.** 151 of 1,242 claims have no resolvable receipt, every one of
them in the four chapter files dirty in the working tree. That text has never
been committed, so no SHA describes it. Committing those four files closes 151
broken receipts in one move.

---

## What it measured, 2026-07-30

Against book version 0.7.4, 30 sections, 2,065 blocks, 91,950 words.

| | |
|---|---:|
| claims traced | **1,242** |
| receipts resolvable | 1,091 |
| receipts broken | **151** |
| SUPPORTED | 273 |
| UNCHECKED (no network run) | 776 |
| UNCHECKABLE (needs a human) | 190 |
| PARTIAL | 3 |
| CONTRADICTED | **0** |

By type: attribution 283, url 227, dated event 223, internal cross reference
191, causal claim 190, image 85, statistic 43.

The internal reference graph, which **nothing checked before this**: 101
chapter references, 82 precedent references, 5 appendix, 3 table. All resolve.
85 figures, all present on disk and all enrolled in `art-catalog.json`.

Citation posture: 227 URLs, of which **38 are Wikipedia** and 4 do not appear
in the Appendix B Works Cited list. **36 claims use comparison language**
("more than X", "the first Y"), which is the exact shape of the P-09 error this
project already caught and cut. That list is the highest-value triage queue in
the book and it is one filter click away on the trace page.

### Reconciliation against the 2026-07-26 REFS-DESIGN survey

Every divergence has a cause. None of them is a defect.

- **98,737 words** was `wc -w` over all 33 `.md` files in the book directory.
  Three of those are not manuscript: `README.md`, `VOICE-GUIDE.md`,
  `ELIJAH-PROTOCOL.md`. The book is the 30 files in `book.json`.
- **107 "Chapter N" hits** was the same over-count. 101 are in the manuscript,
  6 are in the three non-manuscript files.
- **22 precedents is stale.** There are **23**; P-23 landed in the conclusion.
  `LEDGER_SIZE` in `sts.py` already tracks this.
- The word count has three legitimate answers depending on instrument:
  `sts book` says 90,623 (markdown stripped), raw `wc -w` over the 30 files
  says 91,566, the block index says 91,950. Quote the instrument with the
  number.

---

## The discipline this was built under

This section is the point. The harness is replaceable; the practice is not.

**1. Re-measure the handoff. Every time.** The continuation prompt for this
work carried a dozen numbers. Most were right, three were over-counts, and one
("22 precedents") had gone stale in four days. A summary of state is a claim,
not a measurement, and that includes summaries written by the previous session
and it includes this document.

**2. Break the check on purpose before believing it.** `factcheck` reported
**0 CONTRADICTED** across 98,000 words. A fact-check that finds nothing wrong
has usually not run. So a bad chapter reference, appendix, table, precedent and
figure were injected into a clean file: CONTRADICTED moved 0 to exactly 5, then
the file was restored and the restore was proven by comparing its blob hash
against origin. Only then was the zero worth reporting. **Ten false passes have
been caught in this project family, four of them in verification code.** A green
check you have never seen go red is not evidence.

**3. Ask whether the instrument can observe the thing at all.** Before writing
CONTRADICTED, ask what class of defect this tool is even capable of seeing.
Local-only means external sources are UNCHECKED, never UNSUPPORTED. Absence of
a network pass is not evidence of a dead link, and conflating those two would
manufacture findings.

**4. A 200 is not a live source, and a rendered file is not a working page.**
The animated trace was verified in real Chrome through Playwright
(`channel: 'chrome'`), never `--dump-dom`, because `--virtual-time-budget`
advances timers but not the frame clock and captures any animation mid-flight.
That exact trap produced a fabricated bug report in this project once, which was
committed and then retracted. The proof the page animates is empirical: 1 hop
drawn at 260ms, 10 at 2860ms.

**5. Read the screenshot. Do not trust your own assertions.** Every Playwright
assertion passed on the first run. Reading the actual PNG showed the
"CUSTODY BREAKS HERE" terminator rendering on top of the hop value. Assertions
check what you thought to ask; the image shows what shipped.

**6. Never sweep work that is not yours.** `scripts/sts.py` carried a prior
session's uncommitted checkout-hardening changes. The factcheck verb was
committed by building a staging blob from `HEAD` plus only the new functions and
staging it with `git update-index --cacheinfo`, leaving the working tree
untouched. `git add scripts/sts.py` would have committed someone else's
half-finished work under this commit message. **In this worktree, stage by name
and check what else is in the file first.**

**7. Document an exception, never bypass it silently.** Two house rules could
not be satisfied literally. Long dashes appear in historical git commit
subjects; the banned word appears in Aaron Bastani's real book subtitle in
Appendix B and in the subject of the very commit that banned it. Rewriting a
bibliographic title or a historical commit subject inside a provenance tool
would be a worse error than the lint hit. So the punctuation is normalised, the
wording is not, the page says so, and the SHA carries the original. Both
exceptions are written down here and in the commit message. A silent bypass is
indistinguishable from a bug six months later.

---

## What this cannot see

Stated here and reproduced on the trace page above the statistics, because a
trace that quietly omits the hard claims is worse than no trace. The list lives
in `FC_NOT_COVERED` in `sts.py` so the code and this document cannot disagree.

- **Named entities.** No entity extraction. Recognising "Frank Darvall" as a
  person and checking he said the thing needs a gazetteer or a model, and
  guessing from capitalisation would produce confident nonsense.
- **External source liveness.** No URL has been fetched. Nothing here says
  whether a source is live, dead, paywalled or archived.
- **Archive.org snapshots.** Every archive hop is BROKEN.
- **Causal claims.** Detected by connective language, never adjudicated. A
  connective word is not a causal claim.
- **Quotation wording.** Attributions are located; whether the quoted words
  match the source is not checked.
- **Table numbering.** Table numbers live in prose, not markup. Nothing binds
  "Table 2" to a specific table block, so these resolve only to a plausible
  range. This is why the 3 table references are PARTIAL and not SUPPORTED.

---

## Build order for what is next

1. **Commit the four dirty chapter files.** Closes 151 broken receipts and
   costs nothing else. Highest value per unit of effort in this document.
2. **The network pass.** Fetch each of the 227 URLs, cache every response to
   disk, and make the run resumable, because archive.org rate-limits hard and a
   pass that cannot resume will never finish. **Verify the cited content is on
   the page, not the status code**: soft 404s, parked domains, consent walls and
   paywalls all return 200. This is the single easiest place to ship a hollow
   check.
3. **Triage the 36 comparison claims** against primary sources. P-09 established
   that this book's failure mode is inherited comparison claims, not invented
   facts. Treat any precedent whose only citation is a bare Wikipedia link as
   unverified by default; 38 of 227 citations are Wikipedia.
4. **The 4 URLs absent from Appendix B.** Either cite them properly or cut them.

Stop after 1 and 2 if the value is not obvious. Step 1 is free. Step 2 is the
September risk: unverified citations are what gets a manuscript declined by an
acquisitions editor.

---

## Not doing

**Verdict adjudication by model.** `factcheck` never asks a language model
whether a claim is true. Every verdict it writes is mechanical and reproducible:
does the target resolve, does the file exist, does the blob match. An LLM's
recall is not a source. If it was not fetched this session, it is not verified,
and the tool says UNCHECKED rather than guessing.
