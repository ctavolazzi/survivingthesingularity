# Editorial Queue — Surviving the Singularity

**Source of truth:** `src/lib/data/book/` (unified in commit `5164f49`; serves both the
/book pages and the EPUB via `scripts/build-epub.sh`).
**Updated:** 2026-07-10 — Draft 5 ("Manual for the Cracks" lineage, recovered from Google
Drive via `manuscript/SOURCE-MANIFEST.md`) merged into the Part II–III stubs. See
`manuscript/StS-Complete-Draft-v0.0.3.md` Compilation Notes for the chapter mapping.
**Current total:** ~41,000 words in book source (was 24,018 this morning). **Target:** 45,000–50,000.
**Gap to close:** roughly 4,000–9,000 words. After the second fold (author source docs,
2026-07-10 afternoon: Research Synthesis, Empowerment Architecture, Executive Reference
Guide → new Appendix C), only Ch. 3 (872w) remains under 1,000 words.

---

## 1. Chapter thinness inventory

Rule of thumb for this genre: chapters land 1,500–3,000 words. Anything under
1,000 reads as a stub next to its neighbors.

| File | Chapter | Words | Status |
|---|---|---|---|
| 03-chapter1.md | 1. The Event Horizon | 2,075 | ✅ healthy |
| 04-chapter2.md | 2. The Era of AGI (Stages 1–5) | 2,153 | ✅ healthy |
| 05-chapter3.md | 3. The Leap to ASI & the Machine Exodus | 2,034 | ✅ filled — Elijah weave scene (2026-07-12); no chapter under 1,000 words remains |
| 06-chapter4.md | 4. Universal and Multiverse Apex | 814 | ✅ filled — gained Simulation Trilemma (Research Synthesis fold 2026-07-10) |
| 07-chapter5.md | 5. The Thermodynamics of Survival | 1,427 | ✅ healthy |
| 08-chapter6.md | 6. The Singularity Is a Done Deal | 979 | ✅ filled — gained Economic Paradox/FALC + Mathematical Dead End |
| 09-chapter7.md | 7. The Battle Lines | 1,323 | ✅ filled — gained Jahoda/Keynes/scarcity psychology + Waymo backlash data |
| 10-chapter8.md | 8. The Psychology of the Collapse | 4,867 | ✅ healthy — gained Cognitive Firewalls + Relational Autonomy (D5 merge 2026-07-10) |
| 11-chapter9.md | 9. Deglobalization & the Neighborhood Factory | 2,680 | ✅ healthy — gained Robot in the Soil (D5 merge) |
| 12-chapter10.md | 10. The "Create Over Consume" Protocol | 2,169 | ✅ healthy — gained Slop-ocalypse/Algorithmic Judo (D5 merge) |
| 13-chapter11.md | 11. Using the Tech to Your Advantage | 2,198 | ✅ healthy — gained The Crucible (D5 merge) |
| 14-chapter12.md | 12. The Land Strategy | 2,259 | ✅ healthy — gained Autonomy Horizon/CSA (D5 merge) |
| 15-chapter13.md | 13. The Shouse Protocol | 2,800 | ✅ healthy — gained Autonomous Shell build (D5 merge) |
| 16-chapter14.md | 14. The Collapse of the Long Tail | 1,424 | ✅ healthy |
| 17-chapter15.md | 15. The Power of Reclaiming Soil | 1,607 | ✅ healthy |
| 18-chapter16.md | 16. Digital Leverage and Media Autonomy | 1,470 | ✅ healthy |
| 19-chapter17.md | 17. Tools of the Trade | 1,708 | ✅ healthy |
| 20-chapter18.md | 18. The Roadmap and the Premortem Pivot | 1,201 | ✅ filled — gained New Social Contract + Empowerment Architecture |
| 21-conclusion.md | Conclusion: The 2027 Tipping Point | 313 | 🟡 improved — gained Moral Mandate crescendo; still short for a closer |

Front/back matter (preface 739, intro 544, appendices 1,318 + 1,460) is fine as-is.

**Priority order** (updated 2026-07-10 evening, after both folds; every former stub is
filled — remaining work is polish, not fill):
1. **Ch. 3 The Leap to ASI (872w)** — the only chapter still under 1,000 words.
2. **Egalitarian Pivot** section (Ch. 6/7 territory) — last outline gap with no prose.
3. **Conclusion (313w)** — improved but still short for a closer.
4. **Voice pass over all merged material** (Ch. 4, 6–13, 18) — the folds span the hot
   Manifesto register and the clinical research register; Part III should read like a
   field manual per the site's promise.
5. **Stage-2 evidence weave for Ch. 2** (June 2026 export-control shutdown / GLM-5.2).

## 2. Known gaps from the compilation notes (v0.0.1)

- [x] **"Relational Autonomy"** — DONE 2026-07-10: Draft 5 Ch. 9 (Philosophy of the Commons)
  merged into Ch. 8 as the "Relational Autonomy" section, terminology-audited.
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
- [ ] Total lands 45k–50k **(see §6 — the narrative weave changes this target)**

## 6. Narrative weave rollout (Elijah Integration Protocol)

**Protocol:** `src/lib/data/book/ELIJAH-PROTOCOL.md` (character, world, three-zone
architecture, scene ledger). Each chapter gets Zone 1 briefing bullets + a Zone 2
Elijah scene (800–1,200 words) + the existing manifesto content under a Zone 3
`## The Foundations` label. Ch. 0 is the book-scale cold open (exempt).

**Word-count consequence:** a full 18-chapter weave adds ~15k–18k words of new
fiction. That pushes the total from ~42k toward ~60k — **above the old
45k–50k target.** This is an accepted result of the dual-format pivot, not drift.
**CONFIRMED by author 2026-07-12:** single narrative edition, target **~55k–60k**.
No separate workbook edition for now.

**Naming note (2026-07-12):** the OpenAI stand-in was renamed **PorusAI**
(formerly ProneAI) — updated in Ch. 0, the protocol proper-noun table, the
references doc, and the frozen manuscript snapshots.

**History infusion (2026-07-12, author-directed):** verified historical casebook
at `manuscript/HISTORY-CASEBOOK.md` (11 cases, sources, apocrypha blacklist).
Landed so far: Ch. 2 Stage 2 (Red Flag Act 1865), Ch. 5 (new "Cyberdeck" section:
230-year moral-panic lineage + full cyberdeck anatomy/culture + the Tiffany
doctrine — author-mandated early-chapter placement), Ch. 14 ("Graveyard of the
Unconvinced": Kodak/Sears/Blockbuster/Borders + Fujifilm/Swatch counter-cases).
Appendix B sources 105–132 added. Still staged in casebook: Trithemius (Ch. 10/16),
full Sousa treatment (optional, Ch. 16). Editorial dossier (ruthless pass) at
`manuscript/EDITORIAL-DOSSIER-2026-07-12.md` — awaiting author chapter-by-chapter
review + rulings on S9/S3/S4.

| Chapter | Zone 1 bullets | Zone 2 scene | Zone 3 label | Status |
|---|---|---|---|---|
| 0. The Demonstration | n/a (cold open) | ✅ (whole chapter) | n/a | ✅ done — backstory retrofit 2026-07-11 |
| 1. The Event Horizon | ✅ | ✅ (the week after the toast) | ✅ | ✅ **pilot done** 2026-07-11 |
| 2. The Era of AGI | ✅ | ✅ (Companion all-hands; enclosure of the commons) | ✅ | ✅ done 2026-07-12 — 1,062w scene |
| 3. The Leap to ASI | ✅ | ✅ (RSI vertigo; failed call to his mother) | ✅ | ✅ done 2026-07-12 — 1,020w scene; chapter no longer thin (2,034w) |
| 4. Universal / Multiverse Apex | ✅ | ✅ (LADDER.xlsx overreach; map ≠ territory) | ✅ | ✅ done 2026-07-16 — 969w scene |
| 5. Thermodynamics of Survival | ✅ | ✅ (the $211 power bill; grandmother's woodstove) | ✅ | ✅ done 2026-07-16 — 879w scene |
| 6. The Singularity Is a Done Deal | ✅ | ✅ (quits Claypot; Marta shuts the pitch down; the broom) | ✅ | ✅ done 2026-07-16 — 954w scene |
| 7. Battle Lines | — | — | — | ⬜ pending (Denny) |
| 8. Psychology of the Collapse | — | — | — | ⬜ pending (Marta) |
| 9. Deglobalization / Neighborhood Factory | — | — | — | ⬜ pending (Marta, Reuben) |
| 10. Create Over Consume | — | — | — | ⬜ pending (Denny) |
| 11. Using the Tech to Your Advantage | — | — | — | ⬜ pending (deploy-leak friction) |
| 12. The Land Strategy | — | — | — | ⬜ pending (Reuben) |
| 13. The Shouse Protocol | — | — | — | ⬜ pending (Marta) |
| 14. Collapse of the Long Tail | — | — | — | ⬜ pending (Denny) |
| 15. Reclaiming Soil | — | — | — | ⬜ pending (Priya) |
| 16. Digital Leverage / Media Autonomy | — | — | — | ⬜ pending |
| 17. Tools of the Trade | — | — | — | ⬜ pending (Marta, Priya) |
| 18. Roadmap / Premortem Pivot | — | — | — | ⬜ pending (full co-op) |
| Conclusion: 2027 Tipping Point | — | — | — | ⬜ pending (loop close to Bear Flag) |
