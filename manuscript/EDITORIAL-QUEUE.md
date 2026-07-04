# Editorial Queue — Surviving the Singularity

**Source of truth:** `src/lib/data/book/` (unified in commit `5164f49`; serves both the
/book pages and the EPUB via `scripts/build-epub.sh`).
**Compiled:** 2026-07-04. Word counts via `wc -w` on the chapter files.
**Current total:** 24,018 words (incl. front/back matter). **Target:** 45,000–50,000.
**Gap to close:** roughly 21,000–26,000 words, concentrated in Parts II–III below.

---

## 1. Chapter thinness inventory

Rule of thumb for this genre: chapters land 1,500–3,000 words. Anything under
1,000 reads as a stub next to its neighbors.

| File | Chapter | Words | Status |
|---|---|---|---|
| 03-chapter1.md | 1. The Event Horizon | 2,075 | ✅ healthy |
| 04-chapter2.md | 2. The Era of AGI (Stages 1–5) | 2,153 | ✅ healthy |
| 05-chapter3.md | 3. The Leap to ASI & the Machine Exodus | 872 | 🟡 thin |
| 06-chapter4.md | 4. Universal and Multiverse Apex | 367 | 🔴 stub |
| 07-chapter5.md | 5. The Thermodynamics of Survival | 1,427 | ✅ healthy |
| 08-chapter6.md | 6. The Singularity Is a Done Deal | 434 | 🔴 stub |
| 09-chapter7.md | 7. The Battle Lines | 326 | 🔴 stub |
| 10-chapter8.md | 8. The Psychology of the Collapse | 1,599 | ✅ healthy |
| 11-chapter9.md | 9. Deglobalization & the Neighborhood Factory | 407 | 🔴 stub |
| 12-chapter10.md | 10. The "Create Over Consume" Protocol | 445 | 🔴 stub |
| 13-chapter11.md | 11. Using the Tech to Your Advantage | 179 | 🔴 stub |
| 14-chapter12.md | 12. The Land Strategy | 125 | 🔴 stub (thinnest) |
| 15-chapter13.md | 13. The Shouse Protocol | 264 | 🔴 stub |
| 16-chapter14.md | 14. The Collapse of the Long Tail | 1,424 | ✅ healthy |
| 17-chapter15.md | 15. The Power of Reclaiming Soil | 1,607 | ✅ healthy |
| 18-chapter16.md | 16. Digital Leverage and Media Autonomy | 1,470 | ✅ healthy |
| 19-chapter17.md | 17. Tools of the Trade | 1,708 | ✅ healthy |
| 20-chapter18.md | 18. The Roadmap and the Premortem Pivot | 760 | 🟡 thin |
| 21-conclusion.md | Conclusion: The 2027 Tipping Point | 240 | 🟡 thin for a closer |

Front/back matter (preface 739, intro 544, appendices 1,318 + 1,460) is fine as-is.

**Priority order** (impact on reader experience per word written):
1. **Ch. 12 The Land Strategy (125w)** — a named pillar of the sales pitch; currently the
   thinnest file in the book.
2. **Ch. 11 Using the Tech to Your Advantage (179w)** and **Ch. 13 The Shouse
   Protocol (264w)** — Part III is what the site sells hardest ("actionable mechanics");
   these are its backbone.
3. **Ch. 7 The Battle Lines (326w)** and **Ch. 6 Done Deal (434w)** — Part II opener pair;
   this is also where the two missing outline sections land (see §2).
4. **Ch. 4 Apex (367w)** and **Ch. 9 Neighborhood Factory (407w)**, **Ch. 10 Create Over
   Consume (445w)**.
5. **Ch. 3 (872w), Ch. 18 (760w), Conclusion (240w)** — polish last; Ch. 18 reads dense
   already, the Conclusion needs a proper crescendo.

## 2. Known gaps from the compilation notes (v0.0.1)

- [ ] **"Relational Autonomy"** — outline section, no drafted prose. Natural home: Part II,
  inside or after Ch. 8 (Psychology of the Collapse). → AI first draft queued:
  `manuscript/drafts/draft-relational-autonomy.md`
- [ ] **"Egalitarian Pivot"** — outline section, no drafted prose. Natural home: Part II,
  Ch. 6/7 territory (the homepage now explicitly promises "the egalitarian pivot").
  → AI first draft queued: `manuscript/drafts/draft-egalitarian-pivot.md`
- [ ] **Stage-2 real-world evidence weave for Ch. 2** (June 2026 export-control shutdown /
  GLM-5.2 events). → AI first draft queued: `manuscript/drafts/draft-ch2-stage2-evidence.md`
- [ ] **"Local Biological Hub" / "Abundance Quotient"** — referenced concepts without
  standalone chapters; Ch. 18 carries them for now. Optional: give each a section inside
  Ch. 9/Ch. 15 rather than new chapters.

## 3. Voice-register map (for the unification pass)

Two registers per the compilation notes; mark each chapter as you edit.

| Register | Chapters (current) |
|---|---|
| **Manifesto** (hot, declarative) | Intro, Ch. 1–4 (Stages prose), Ch. 18, Conclusion |
| **Manual** (calm, instructional) | Preface, Ch. 5, Ch. 14–17, Appendix A |
| **Mixed / TBD** | Ch. 6–13 (mostly stubs — write them straight into the target register) |

Suggested rule from the site's own copy: Parts I–II may run hot; Part III should read
like a field manual (the homepage promises "actionable mechanics, not abstract advice").

## 4. Reference index cross-check (StS-References-and-Proper-Nouns.md)

- Terminology audit: **clean** — `grep -ri sovereign src/lib/data/book/` returns nothing;
  the distributed v0.2 PDF verified clean end-to-end (local = Drive = Supabase bundle,
  md5 `d60b418e…`).
- The references doc §6 records the audit as done — still accurate.
- Chapter-location pointers in the references doc refer to v0.0.1 numbering, which matches
  the current book.json order (18 chapters, 3 parts). No drift detected.

## 5. Definition of done (pre-launch)

- [ ] No chapter under 1,000 words (or consciously merged into a neighbor)
- [ ] Two outline gaps drafted, edited, and placed
- [ ] One voice pass over Part II–III stubs
- [ ] `scripts/build-epub.sh vX` run; EPUB spot-read on a phone + e-reader
- [ ] Total lands 45k–50k
