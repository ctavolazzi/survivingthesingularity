---
title: "Surviving the Singularity — Project Status"
author: Christopher Tavolazzi
date: June 12, 2026
---

# Surviving the Singularity — Project Status

**Date:** June 12, 2026  
**Author:** Christopher Tavolazzi (Coffee Jesus)  
**Live site:** survivingthesingularity.com  

---

## What This Is

*Surviving the Singularity* is a book-in-progress and companion website. The premise: a practical, satirical field manual for people who want to stay agentic as AI rewrites work, money, medicine, and meaning. Tone is conversational and darkly funny — think Kurzweil meets Anthony Bourdain.

The site is open draft. Everything is free to read. No login. No paywall. The book ships when it ships.

---

## Platform Status

The SvelteKit site is live and functional with the following routes:

| Route | Status |
|-------|--------|
| `/` | Live — landing page, thesis, calculator, chapter index |
| `/why` | Live — AGI timeline, expert voices, benchmarks |
| `/book` | Live — open draft, chapter previews |
| `/blueprint` | Live — 8-chapter shouse/independence blueprint |
| `/blog` | Live — dispatches |
| `/about` | Live |
| `/checklist` | Live — email-gated content |
| `/agi` | Live — redirects |
| `/shouse` | Live — 3D Shouse Builder strategy game |
| `/preorder` | **Not built** — planned (Phase 2) |

The tech stack is solid: SvelteKit v2, Tailwind CSS, Supabase for email capture, Cloudflare Pages deployment. A free sample PDF (`StS-free-sample.pdf`) exists in static assets.

**Recent site work (2026):** Interactive diagrams added to landing, mobile layout overhaul, email capture + checklist gate, buy CTA wired to `PURCHASE_URL` env var (renders when set), launch script ready.

---

## Book Content Status

The manuscript exists in two states inside the repo:

### book-draft-v2 — Original Draft

Full manuscript, ~41,900 words across 19 files. All 12 chapters exist plus front matter (acknowledgements, introduction, TOC) and back matter (epilogue, glossary, further reading, index).

| Chapter | Title | Words |
|---------|-------|-------|
| Intro | Welcome to the Weirdness | ~1,800 |
| Ch. 1 | What the Hell is Going On? | 2,144 |
| Ch. 2 | Show Me the Money | 2,437 |
| Ch. 3 | Your AI BFF | 3,056 |
| Ch. 4 | Dr. AI Will See You Now | 2,467 |
| Ch. 5 | School of the Future | 4,088 |
| Ch. 6 | When Robots Get Creative | 5,492 |
| Ch. 7 | Love in the Time of Algorithms | **6,857** |
| Ch. 8 | Lights, Camera, Algorithm! | 926 |
| Ch. 9 | AI for President | 3,370 |
| Ch. 10 | Money Never Sleeps | 943 |
| Ch. 11 | The Singularity: When AI Gets Smarter | 785 |
| Ch. 12 | So Long, and Thanks for All the Data | 827 |

**Observation:** Chapters 8, 10, 11, and 12 are significantly underdeveloped (785–943 words each vs. 3,000–7,000 for the stronger chapters). These are the back half of the book and need the most work.

### book-editing — Revised Draft

A second pass exists in `book-editing/`, ~31,700 words total. Chapters have been tightened, edited for voice consistency, and some content rearranged. Notable: Chapter 8 in this draft runs 5,945 words (vs. 926 in v2 — substantially rewritten).

| Chapter | book-draft-v2 | book-editing | Delta |
|---------|--------------|--------------|-------|
| Ch. 1 | 2,144 | 2,074 | -70 |
| Ch. 2 | 2,437 | 1,140 | -1,297 |
| Ch. 3 | 3,056 | 1,226 | -1,830 |
| Ch. 4 | 2,467 | 941 | -1,526 |
| Ch. 5 | 4,088 | 992 | -3,096 |
| Ch. 6 | 5,492 | 974 | -4,518 |
| Ch. 7 | 6,857 | 1,057 | -5,800 |
| Ch. 8 | 926 | **5,945** | +5,019 |
| Ch. 9 | 3,370 | 2,441 | -929 |
| Ch. 10 | 943 | 1,070 | +127 |
| Ch. 11 | 785 | 2,604 | +1,819 |
| Ch. 12 | 827 | 2,298 | +1,471 |

The editing draft shows major cuts to middle chapters (Ch. 3–7) and major expansions to the back half (Ch. 8, 11, 12). This is the right direction: the back half is where the book pays off.

---

## EPUB Status

**No EPUB file exists yet.**

All content is in Markdown and is ready for EPUB assembly. The pipeline would be:

1. Decide which draft is canonical (book-editing is more current but some chapters are skeletal)
2. Reconcile the two drafts into a single clean manuscript
3. Write/finalize the underdeveloped chapters (8, 10, 11, 12 in v2 terms)
4. Assemble via pandoc with metadata (cover, title, author, ISBN if applicable)
5. Validate the EPUB output
6. Upload to Gumroad/distribution as the purchase artifact (site already has buy CTA waiting for `PURCHASE_URL`)

**pandoc is installed** (`3.6.4`) — ready to go.

---

## Revenue / Distribution Status

| Item | Status |
|------|--------|
| Email waitlist | Live (Supabase) |
| Free sample PDF | Exists (`StS-free-sample.pdf`) |
| Gumroad account | Unknown — not confirmed |
| Stripe pre-order | Planned, not built |
| EPUB/PDF for sale | Not assembled yet |
| Launch URL (`PURCHASE_URL`) | Not set — env var placeholder |

The site's buy CTA is wired and waiting. Setting `PURCHASE_URL` in `.env` is all that's needed to activate it.

---

## What Needs to Happen Next

### Immediate (before EPUB can ship)

1. **Reconcile the two drafts.** Decide: is `book-editing` the working canonical? Or merge best-of-both? The v2 has stronger long-form content in Ch. 3–7; the editing draft has better back-half content.
2. **Fill the gaps.** Ch. 8, 10, 11 (in v2) are stub-length. They need full passes before the book is complete.
3. **Assemble the EPUB.** Once content is settled, pandoc can compile in minutes.

### After EPUB

4. Set up Gumroad product (or Stripe pre-order per the roadmap in `docs/PREORDER-ROADMAP.md`).
5. Set `PURCHASE_URL` in `.env` and redeploy — buy button goes live.
6. Email the waitlist.

---

## File Map (Key Paths)

```
src/lib/data/
  book-draft-v2/      Original full draft (~42k words)
  book-editing/       Revised draft (~32k words)
  blueprint.js        8-chapter shouse blueprint (site content)

static/
  StS-free-sample.pdf Free sample (already distributed)

docs/
  PREORDER-ROADMAP.md Stripe/payment plan
  EMAIL-FUNNEL.md     Email capture notes
```

---

## Summary

The book has a complete structure, a strong voice, a live website, an email list, and a sample PDF. The manuscript is roughly 70% camera-ready — the front half is polished, the back half needs work. The EPUB is one focused writing sprint + one pandoc command away from existing. The site is already wired to sell it; it just needs the URL.

The bottleneck is content, not infrastructure.
