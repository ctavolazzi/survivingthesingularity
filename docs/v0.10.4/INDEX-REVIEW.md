# Stable manuscript ID review, v0.10.4

All 2,301 inherited IDs are retained. The rebuild matched 2,284 blocks by content and carried 17 by position. Every positional assignment was checked against the 18 exact approved replacements in the opening, middle and ending reviews; all were correct. No repair or new tombstone was needed.

Two documented splits add two IDs, bringing the index to 2,303 blocks across 35 sections:

| Retained ID | Retained fragment | New ID | New fragment |
| --- | --- | --- | --- |
| `sts.introduction.b0142` | Paragraph beginning “Because almost everything” | `sts.introduction.b0162` | Paragraph beginning “Between 2000 and 2018” |
| `sts.chapter3.b0060` | Original four briefing bullets | `sts.chapter3.b0098` | Separate “Reading route” paragraph |

Appendix E's revised heading retains `sts.appendix-e.b0059`. All other changes are in-place revisions. The [machine receipt](index-review.json) records every positional assignment, exact before/after block text, source spans, approved-edit references and fingerprints.

Verification used the persisted index read back from disk. ID count, uniqueness, syntax, spans, hashes, exact source coverage and artwork links pass. Each structural check first rejected a deliberate in-memory defect. All 2,284 unchanged blocks retain their IDs and non-span metadata. Live IDs and historical tombstones are disjoint, no tombstone was added, and every next ordinal exceeds allocated IDs.

A separate semantic control swapped the two Introduction fragment IDs in memory. Structural checks still passed, as expected, but the identity probe rejected both assignments. The restored persisted index passes that probe. A rebuild then returns 2,303 content matches, zero positional matches and identical persistent state; a second write is a byte-preserving no-op. All 36 frozen canonical source hashes and the preserved v0.10.3 index remain unchanged.

This verifies the documented edition transition. It does not change the reconciler or make positional matching safe for future mixed edits.
