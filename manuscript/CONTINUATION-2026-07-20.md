# Continuation Prompt — Surviving the Singularity (book) — 2026-07-20

Paste this into a fresh session to resume. Read `AUDITOR-BRIEF.md` (repo root) first
for canonical facts, tools, and the versioning ritual. Then this.

## Where we are

- Repo: `~/Code/active/survivingthesingularity`, branch `weave-and-mobile-polish`.
- Book is at **v0.7.0** (book.json). Live prod is at **v0.6.2** (deployed 2026-07-19).
- **v0.7.0 is committed + pushed on the branch but NOT deployed.** It adds the pixel-art
  illustration layer (see below). It is 1 commit ahead of main.
- Spin-up: `python3 scripts/sts.py status`, `git log --oneline -8`, `tail -40 devlog.md`.
- Deploy ritual = "update the website and swap the PDF" (both), then merge to main only
  with CT's explicit yes (prod runs LIVE Stripe; the author owns that call).

## Art system (new at v0.7.0)

- Machine-readable catalog: **`src/lib/data/book/art-catalog.json`** (schema `sts-art-catalog/v1`,
  20 assets, stable IDs `sts.<kind>.<slug>`). Human index: `manuscript/ART-CATALOG.md`.
- Raw reusable sprites (transparent PNG): `static/book-images/sprites/`.
- Made with PixelLab (Tier 1; ~1370 generations left) + Python/Pillow compositing on the
  navy/amber palette; 2 diagrams hand-authored as house-style SVG.
- 7 figures placed: intro (ox), ch9 (supply lines), ch17 (field kit + photobioreactor +
  algae loop), Appendix E (cyberdeck), Part II divider (co-op cast).

## TODO — the rest of the book

### 0. Immediate decision (blocking)
- [ ] **Ship v0.7.0 or iterate.** CT to approve the illustrated version. If yes: merge
      `weave-and-mobile-polish` → main, update website, swap public PDF to v0.7.0. If iterate:
      collect the change list (swap sprite frames, re-place figures, re-caption) first.

### 1. Art cataloguing → coursework (CT's stated goal)
- [ ] **Extend `art-catalog.json` to every book figure**: the 33 pre-existing `ch*-*.svg`
      diagrams, the photo headers (`ch*.jpg/.webp` with their credits from `credits.json`),
      and the 3 `part*-divider.png` banners. Add `concepts[]` tags to each so figures are
      queryable by topic.
- [ ] **Design the coursework schema** (`coursework.json` or generator): one module per
      chapter, each pulling figures by catalog ID, with learning objectives, the chapter's
      Precedent (P-01..P-22), the "practice" actions already in Appendix D, and a check-for-
      understanding. The catalog's `concepts[]` + `placement.chapter` are the join keys.
- [ ] **Build the generator** that reads `art-catalog.json` + book sections + Appendix D
      practices and emits per-chapter coursework. Keep it data-driven so new art auto-enrolls.
- [ ] Optional richer media: character sprites have all 8 directions + 40+ PixelLab template
      animations available by `character_id` — usable for interactive/animated coursework.

### 2. More art (optional, if CT wants breadth)
- [ ] Remaining cast: Reuben, Frank, Gary, Devendra (minor but named). Per-chapter pixel
      headers. Animate key sprites (e.g., the photobioreactor bubbling, the plasma table cutting).

### 3. Editorial (from AUDITOR-BRIEF roadmap)
- [ ] **Voice-unification pass (roadmap C)** — the largest open editorial job. Foundations
      sections swing rant↔academic; target the field-manual register for Part III.
- [ ] **Fact-check P-07..P-22 (roadmap B)** — only P-01..P-06 verified; log new sources to
      Appendix B (next number 183; 179-182 are the SECTOR 07 / EasyGrow / Kyle Gabriel / SANANBIO videos).
- [ ] **Cyberdeck source URLs 166-178** still unverified (roadmap H).
- [ ] **Appendix C** is 344 words — decide intentionally thin vs expand.
- [ ] **EPUB device spot-read** never performed.

### 4. Settled (do not reopen)
- No em dashes. Never the word "manifesto". Hyper-local over decentralized (see ch9 anchor).
- /book download button removed on purpose; view-in-browser button stays.
- Versions start at 0.0.1-style increments; bump on every content change.

## Reminders
- Parallel sessions edit this repo: `git status` before editing; commit per coherent wave, `book:` prefix.
- Update `AUDITOR-BRIEF.md` in the same commit whenever tooling/conventions/versions change.
- Vault banners live at `~/Documents/Personal-Remote-Vault/2026-07-1*_StS_*.md`; update via
  SimpleAgentOS `atomic_io`, never raw writes.
