---
title: "Surviving the Singularity: Project Status"
author: Christopher Tavolazzi
date: June 12, 2026
---

**Live site:** survivingthesingularity.com | **Written as:** Coffee Jesus

---

## What This Is

*Surviving the Singularity* is a book-in-progress with a companion website. The premise: a practical, satirical field manual for people who want to stay agentic as AI rewrites work, money, medicine, and meaning. The voice is conversational, darkly funny, and direct, with a 60/30/10 balance of information, humor, and reflection.

The site is an open draft. Everything is free to read. No login, no paywall. The book ships when it ships.

---

## Platform Status: Live and Launch-Ready

The SvelteKit site is deployed on Cloudflare Pages and fully functional.

| Route | Status |
| ----- | ------ |
| `/` | Live. Landing page with thesis, interactive diagrams, chapter index |
| `/book` | Live. Open draft with chapter previews. Buy CTA wired to `PURCHASE_URL` (renders when Gumroad URL is set via `LAUNCH.sh`) |
| `/blog` | Live. Dispatches |
| `/checklist` | Live. Email-gated readiness checklist |
| `/signals` | Live. Automated arXiv research feed with daily updates and RSS |
| `/early-access` | Live. Email capture waitlist; $5 price locks in at launch (Stripe deferred to Phase 2) |
| `/launch` | Live. Author's Edition preorder + launch messaging |
| `/about` | Live |
| `/policies`, `/terms`, `/disclaimer`, `/accessibility` | Live. Legal/compliance pages |
| `/unsubscribe` | Live. Email opt-out |
| `/blueprint`, `/why`, `/agi`, `/shouse`, `/timeline`, `/evidence` | Retired (June 2026). Content folded into `/book` |
| `/preorder` | Not built. Planned as Phase 2 (Stripe) |

**Recent platform work (homepage-redux-jun2026 branch, 13+ commits):**

- Homepage reframe: selfish framing, 3-part book structure, updated stats
- `/early-access` converted from mock Stripe to real email capture (Supabase waitlist)
- `PURCHASE_URL` constant added to `/book` page — LAUNCH.sh sets this when Gumroad is ready
- `/signals` route added: live arXiv AI research feed with daily auto-update
- `/about` rewritten as author-forward first-person page
- Navbar simplified to 2 links + CTA; command palette updated to live routes
- Retired routes removed: `/blueprint`, `/why`, `/agi`, `/shouse`, `/timeline`, `/evidence`
- Dead-link cleanup: email templates, sitemap, layout components updated
- Homepage og:image and Twitter card added
- Blog copy update: "Information You Can Use Today" framing

**Translation: the storefront is built. It is waiting on the product.**

---

## Manuscript Status: Two Drafts, No Canonical Version Yet

The book content lives in two parallel directories, and this is the central open question of the project.

### Draft A: `book-draft-v2` (~39,500 words)

The fuller draft. Twelve chapters plus introduction, epilogue, glossary (two versions), further reading, and index.

| Chapter | Words | | Chapter | Words |
| ------- | ----- | - | ------- | ----- |
| 1. What the Hell is Going On? | 2,144 | | 7. Love in the Time of Algorithms | 6,857 |
| 2. Show Me the Money | 2,437 | | 8. Lights, Camera, Algorithm! | 926 |
| 3. Your AI BFF | 3,056 | | 9. AI for President | 3,370 |
| 4. Dr. AI Will See You Now | 2,467 | | 10. Money Never Sleeps | 943 |
| 5. School of the Future | 4,088 | | 11. The Singularity | 785 |
| 6. When Robots Get Creative | 5,492 | | 12. So Long, and Thanks for All the Data | 827 |

**Problem:** wildly uneven. Chapter 7 is 6,857 words; chapters 8, 10, 11, and 12 are under 1,000. Chapter 11 (the literal title chapter) is the second-shortest in the book.

### Draft B: `book-editing` (~29,300 words)

A separate editing pass with its own structure, including a `book.json` manifest and a back-cover blurb that Draft A lacks.

| Chapter | Words | | Chapter | Words |
| ------- | ----- | - | ------- | ----- |
| 1 | 2,074 | | 7 | 1,057 |
| 2 | 1,140 | | 8 | 5,945 |
| 3 | 1,226 | | 9 | 2,441 |
| 4 | 941 | | 10 | 1,070 |
| 5 | 992 | | 11 | 2,604 |
| 6 | 974 | | 12 | 2,298 |

**Notable:** the two drafts are nearly mirror images. Where Draft A is long, Draft B is short, and vice versa. Draft B has a real Chapter 11 and 12 (2,604 and 2,298 words) where Draft A has stubs. Draft A has rich middle chapters where Draft B is thin.

**The opportunity:** a merged best-of-both manuscript would land around 45,000 to 50,000 words, which is solid territory for this genre of trade nonfiction.

### Supporting Editorial Assets (already written)

- `EDITING_STRATEGY.md`: global edit plan plus chapter-by-chapter notes
- `WRITING_CHECKLIST.md`: voice and structure quality gates
- Style guide: full documentation of the "Dynamic Satirical Commentary" voice
- Glossary with definitions, further reading, index, acknowledgements, back cover

---

## EPUB Status: Not Started

This is the next milestone. No `.epub` file exists anywhere in the project yet.

**What we have going for us:**

- All content is already clean Markdown with a numbered file order
- `book.json` manifest exists in the `book-editing` draft for structure
- Pandoc 3.6.4 is installed locally, which converts ordered Markdown directly to EPUB with metadata, cover, and CSS
- Front and back matter (acknowledgements, glossary, further reading, back cover) already exist as files

**What the EPUB needs before it can be built:**

1. **Pick the canonical draft.** Merge Draft A and Draft B, or anoint one and pull the best chapters from the other. This is the single decision blocking everything downstream.
2. **Fill the thin chapters.** Whichever draft wins, four-plus chapters need real content.
3. **Cover image.** No cover asset exists yet.
4. **Metadata file.** Title, author, ISBN (if desired), publisher, rights. Trivial once decided.
5. **EPUB CSS.** A small stylesheet for chapter headings, callouts, and the interactive-element boxes (Reality Check, Future Forecast, Survival Strategy, Your Turn).
6. **Build script.** A repeatable `make epub` style command so every manuscript edit can regenerate the book in seconds. Roughly an afternoon of work once items 1 and 4 exist.

---

## Distribution and Monetization

| Channel | Status |
| ------- | ------ |
| Email waitlist | Live (Supabase, with localStorage fallback) |
| Free sample PDF | Live on `/book` |
| Gumroad | Pending. `LAUNCH.sh` is written and waiting on the product URL |
| Stripe pre-orders | Planned (Phase 2 roadmap documented in `docs/PREORDER-ROADMAP.md`) |
| Substack | Live channel for chapter drops and launch alerts |

---

## The Critical Path

Everything funnels to one sequence:

1. **Decide the canonical manuscript** (merge strategy for the two drafts)
2. **Write/expand the thin chapters** to bring every chapter to fighting weight
3. **Build the EPUB pipeline** (pandoc + metadata + CSS + cover)
4. **Create the Gumroad product** with the EPUB as the deliverable
5. **Run `LAUNCH.sh`** and announce on Substack

The website, the funnel, the sample, and the buy button are all done. The remaining work is the book itself and the EPUB that packages it.

---

## Bottom Line

This project is in the classic 80/20 endgame. The platform is launch-ready and has been polished extensively through 2026. The manuscript has roughly 50,000 words of material written across two drafts but needs one consolidation pass to become a single coherent book. The EPUB is unbuilt but cheap to build once the manuscript is canonical, since the entire toolchain (Markdown source, pandoc, file ordering, front and back matter) is already in place.

**Shortest path to revenue: consolidate the drafts, build the EPUB, ship on Gumroad.**
