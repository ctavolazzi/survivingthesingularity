# Stable manuscript ID review, v0.10.2

Completed 2026-09-28. Reviewed every one of the 183 inherited IDs carried by position, the 19 provisionally new blocks, and the two initially tombstoned blocks against preserved v0.10.1 source and index. Repaired 19 block assignments in five sections. Fourteen of the 183 positional assignments had transferred inherited IDs to unrelated material; five provisionally new IDs also sat on revised old material. No canonical manuscript text changed.

## Cause and evidence

`scripts/sts.py::_reconcile` first matches exact content, then pairs every residual block of the same type in order across the section. It has no edit-boundary awareness. A deletion or an insertion before a revision can therefore shift otherwise stable IDs. The warning was substantive here. All 2,083 content-matched blocks retained their IDs and metadata.

Evidence included complete before/after text recovered from index line spans, the canonical Markdown diffs, `opening-changes.json` findings O17/O18, `middle-changes.json` Chapter 7 replacements, `ending-changes.json` E11/E12/E17/E18 and Appendix B replacements, and the recorded figure alt/caption revisions. Similarity was used only to flag pairs for inspection, not to determine identity.

## Exact repairs

IDs below are full stable IDs. Line spans refer to v0.10.2 at review time. Swapped provisional IDs were never part of the preserved v0.10.1 release.

| Section and line | Before this repair | Corrected ID | Block identity |
| --- | --- | --- | --- |
| chapter5:82 | `sts.chapter5.b0171` | `sts.chapter5.b0176` | New conversion-boundaries paragraph |
| chapter5:92 | `sts.chapter5.b0176` | `sts.chapter5.b0171` | Revised data-centre demand and price paragraph |
| chapter7:111 | `sts.chapter7.b0124` | `sts.chapter7.b0129` | Payroll incentive |
| chapter7:133 | `sts.chapter7.b0129` | `sts.chapter7.b0135` | Scarcity study |
| chapter7:152 | `sts.chapter7.b0135` | `sts.chapter7.b0181` | Waymo sources |
| chapter7:173 | `sts.chapter7.b0181` | `sts.chapter7.b0104` | Missing opposition campaigns |
| chapter7:183 | `sts.chapter7.b0104` | `sts.chapter7.b0165` | Local trust |
| chapter7:185 | `sts.chapter7.b0165` | `sts.chapter7.b0106` | Cooperative buffer and scarcity |
| chapter7:263 | `sts.chapter7.b0106` | `sts.chapter7.b0199` | Musicians union mechanism |
| chapter16:87 | `sts.chapter16.b0097` | `sts.chapter16.b0115` | Revised Kiwix archive instructions |
| chapter17:89 | `sts.chapter17.b0120` | `sts.chapter17.b0185` | New feed qualification and FAO source |
| appendix-b:59 | `sts.appendix-b.b0118` | `sts.appendix-b.b0205` | Inserted 1878 and 1896 statutes |
| appendix-b:224 | `sts.appendix-b.b0205` | `sts.appendix-b.b0118` | Revised additional-source introduction |
| appendix-b:238 | `sts.appendix-b.b0187` | `sts.appendix-b.b0214` | Inserted Stanford AI Index source |
| appendix-b:308 | `sts.appendix-b.b0214` | `sts.appendix-b.b0187` | Revised USDA and food-recovery source list |
| appendix-b:246 | `sts.appendix-b.b0193` | `sts.appendix-b.b0220` | Inserted NASA Hubble source |
| appendix-b:342 | `sts.appendix-b.b0220` | `sts.appendix-b.b0193` | Revised food, eviction, and basic-services source list |
| appendix-b:255 | `sts.appendix-b.b0200` | `sts.appendix-b.b0221` | Inserted Raspberry Pi and E Ink sources |
| appendix-b:387 | `sts.appendix-b.b0221` | `sts.appendix-b.b0200` | Revised reference-stack source list including DOE insulation |

The Chapter 16 transition at line 75 deliberately retains `sts.chapter16.b0096`. E11 records a single two-paragraph-to-one replacement in that location. Its replacement text begins “The next section handles the files. Permission comes first”. Retaining the first block ID records that in-place rewrite; the removed second block, `sts.chapter16.b0097`, is tombstoned. The separate archive revision E12 regains its own `sts.chapter16.b0115`.

Chapter 17 receives the sole additional allocation made by this repair: `sts.chapter17.b0185` for the new feed qualification. `next_ordinal` advances from 185 to 186. The duplicate deleted inventory exercise is not the new fish-feed paragraph.

## Tombstones and allocation

Compared with preserved v0.10.1, the only newly deleted block IDs are:

- `sts.chapter16.b0097`: second paragraph of the E11 two-to-one transition rewrite.
- `sts.chapter17.b0120`: duplicate tool-inventory exercise, E18.
- `sts.chapter7.b0124`: removed scene moral, documented in middle review.

The repaired index contains 20 new IDs relative to v0.10.1: one in Chapter 5, one in Chapter 17, and eighteen in Appendix B. No historical tombstone was resurrected. The two IDs mistakenly tombstoned during the initial v0.10.2 build, `sts.chapter7.b0199` and `sts.chapter16.b0115`, are restored to their revised original passages. Appendix B has no deletions; its four shifted old blocks recover their old IDs and all added sources retain new IDs.

## Review coverage

| Section | Positional inherited IDs reviewed | Incorrect inherited assignments repaired |
| --- | ---: | ---: |
| introduction | 8 | 0 |
| chapter1 | 8 | 0 |
| chapter2 | 3 | 0 |
| chapter3 | 2 | 0 |
| chapter4 | 2 | 0 |
| chapter5 | 8 | 1 |
| chapter6 | 3 | 0 |
| chapter7 | 7 | 7 |
| chapter8 | 12 | 0 |
| chapter9 | 10 | 0 |
| chapter10 | 10 | 0 |
| chapter11 | 6 | 0 |
| chapter12 | 9 | 0 |
| chapter13 | 12 | 0 |
| chapter14 | 9 | 0 |
| chapter15 | 12 | 0 |
| chapter16 | 6 | 1 |
| chapter17 | 10 | 1 |
| chapter18 | 6 | 0 |
| chapter19 | 9 | 0 |
| conclusion | 1 | 0 |
| appendix-b | 6 | 4 |
| appendix-c | 1 | 0 |
| appendix-d | 4 | 0 |
| appendix-e | 8 | 0 |
| appendix-f | 6 | 0 |
| appendix-g | 3 | 0 |
| appendix-h | 2 | 0 |

All other inherited assignments represent in-place prose, list, table, figure-description, or caption revisions. The seven sections without positional changes were checked through the complete content-match preservation assertion and new/deleted-block inventory.

## Verification

- The semantic identity probe was run on the actual pre-repair index first: it failed on all 19 documented wrong assignments. The same probe passed on the repaired index read back from disk.
- Every one of the 2,083 exactly matched blocks retains its previous ID and complete metadata.
- Direct verification of the persisted index passed ID uniqueness, syntax, source span coverage, content hashes, and art links. Live IDs and tombstones are disjoint; every next ordinal exceeds all active and tombstoned IDs.
- A non-writing rebuild from the repaired index returns identical persistent state, 2,285 content matches and zero positional matches.
- SHA-256 checks confirm all 35 canonical Markdown files were unchanged during this repair.
- `python3 scripts/sts.py id verify` passed all seven checks: 2,285 blocks, 35 sections, 103,209 words, and 102 valid art links.

This is a repair of this edition’s known transition. It does not alter the reconciler algorithm or claim that structural `id verify` can detect semantic identity shifts. Future mixed insert/delete/rewrite edits still require review of positional warnings.

## Index fingerprints

- Preserved v0.10.1: `0abf3cdb5f683ff77cd2abee5d72eb77a634ebb6d36ab82a1acd58c762fb26ac`
- Before this repair: `178616d1cf841ac0b318ef1812e887b3c447d987f7f106b3193572b4a9ceb2c9`
- Repaired v0.10.2: `a02c3d4b216578d11cc592c58dfaf7cfd2bdf7b14a4ff3e025688f125b1e45c1`
