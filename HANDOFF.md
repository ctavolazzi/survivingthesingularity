# Handoff: recent work and open tasks

**Start here if you are picking up this repo, human or agent.** This file answers two questions: what was done recently, and what still needs doing. It is short on purpose. Detail lives in the PRs and files linked below.

**Keep it current.** When you finish a piece of work, add a line to *Recent work* (newest first) and update *Open tasks*. When a task is done, move it to *Recent work*, don't just delete it. Trim *Recent work* to roughly the last 20 entries; git history keeps the rest.

*Last updated: 2026-09-26*

---

## Open pull requests

| PR | Branch | What it is | State |
| --- | --- | --- | --- |
| [#21](https://github.com/ctavolazzi/survivingthesingularity/pull/21) | `claude/cost-per-labor-unit-l1w2y4` | Cost per Labor-Hour Equivalent (CLHE), Jevons Paradox and textiles, and the 1519 analogy, added to Ch 1 and Ch 6 and fact-checked, plus a blog teaser. Also adds this file. | Ready for review, awaiting CT's merge |
| [#20](https://github.com/ctavolazzi/survivingthesingularity/pull/20) | `claude/se-repos-evaluation-88j1bx` | Launch plan, 21 video scripts, book precedent fixes, free `/ledger` page | Draft |
| [#19](https://github.com/ctavolazzi/survivingthesingularity/pull/19) | `claude/manuscript-update-clm8pq` | Retitle Chapter 11, intake the v0.7.4 revision package | Draft |

All three touch `src/lib/data/book/`. Whoever merges second or third should expect conflicts in the chapter files and in `manuscript-index.json`. Regenerate the index with `python3 scripts/sts.py id build`; never hand-merge it.

---

## Recent work (newest first)

- **2026-09-26, PR #21.** Added this handoff file, linked from `README.md` and `CLAUDE.md`.
- **2026-09-26, PR #21.** Fact-check pass on the labor-hour material. The PR description lists each figure as confirmed or corrected, with sources. Corrections: apparel spending was 14.0% of the household budget in 1901 and 2.5% in 2024; the origin of the 1545 and 1576 *cocoliztli* epidemics is disputed; Philip II's defaults are dated 1557, 1560, 1575 and 1596. Additions: AT&T operator automation (NBER w28061), robotic sewing, and the Meiji caveat.
- **2026-09-26, PR #21.** Book integration.
  - Ch 1 gets a new subsection, *The Price of a Labor-Hour*.
  - Ch 6 gets three new sections: *Jevons and the Blue Jeans*, *The Gold of the New World*, and *Three Paths, and a Fourth*.
  - Appendix C gets a CLHE entry. Appendix B Works Cited gets entries 207 to 227.
  - No new precedent IDs.
- **2026-09-25, PR #21.** Blog post `/blog/the-price-of-a-labor-hour`, added to the blog listing and the sitemap.
- **2026-09-23, PR #20.** Launch plan, video scripts, precedent fixes, `/ledger` page. See that PR.
- **2026-09-21, PR #19.** Chapter 11 retitle and v0.7.4 revision intake. See that PR.
- **2026-09 (ongoing, on `main`).** Daily `chore: daily signals sweep` commits feed `/signals`. They are automated and need no action.
- **2026-08-01, on `main`.** Stripe guard fixes, customer email plain-text part, downloads now ship the book the site links to, claims brought current, and the fact-check trace republished. See `git log origin/main`.

---

## Open tasks

### Book

- [ ] **Merge or close PRs #19, #20 and #21.** Merging is CT's call. Mind the conflict note above.
- [ ] **Voice read of the new Ch 6 sections** (PR #21). They add about 80 lines. Check them against `src/lib/data/book/VOICE-GUIDE.md` and trim if needed.
- [ ] **Run `python3 scripts/sts.py verify --links`** somewhere with open internet access. It has not been run on Works Cited entries 207 to 227, because the agent environment blocks outbound network. Each URL was confirmed by web search instead.
- [ ] **Version close for the next release.** Bump `version` and `lastUpdated` in `src/lib/data/book/book.json`, rebuild the EPUB (`scripts/build-epub.sh`) and the PDFs (`scripts/build-pdf-variants.sh`), and swap `static/downloads/`. The procedure is in `AUDITOR-BRIEF.md` and `src/lib/data/book/README.md`.

### Site and infrastructure

These are carried over from [`docs/work-orders-2026-07-28.md`](docs/work-orders-2026-07-28.md). Its last recorded status is **2026-07-29**, and some items may have moved since, especially the Stripe work on 2026-08-01. **Verify each one before acting on it.**

- [ ] **WO-03.** The failing download URL still needs to be supplied (needs CT).
- [ ] **WO-09.** Run `sql/011` (`email_deliveries`) in Supabase (needs CT).
- [ ] **WO-10.** Blocked by WO-09.
- [ ] **WO-12.** Stripe was still on test keys as of 2026-07-29 (needs CT).
- [ ] **WO-13.** Awaiting go-ahead.
- [ ] **Rate limiter is per-isolate** (`rateLimit.js`), so it doesn't actually stop a distributed attacker. It needs a decision: Cloudflare WAF rate limiting, Turnstile, or KV/Durable Object counters.
- [ ] **CSP still allows `*.supabase.co`** in `static/_headers`. It can probably be dropped once someone confirms at runtime that nothing in the browser still connects to Supabase.

---

## Where the deeper records live

| For | Read |
| --- | --- |
| Repo orientation for agents | [`CLAUDE.md`](CLAUDE.md) |
| Book source-of-truth rules | [`README.md`](README.md#book-content-the-single-source-of-truth), [`src/lib/data/book/README.md`](src/lib/data/book/README.md) |
| Book voice | [`src/lib/data/book/VOICE-GUIDE.md`](src/lib/data/book/VOICE-GUIDE.md) |
| Fact-check harness | [`FACTCHECK.md`](FACTCHECK.md) |
| Book version history | [`RELEASES.md`](RELEASES.md), [`manuscript/EDITORIAL-QUEUE.md`](manuscript/EDITORIAL-QUEUE.md) |
| Security and infrastructure work orders | [`docs/work-orders-2026-07-28.md`](docs/work-orders-2026-07-28.md) |

`PROJECT-STATUS.md`, `docs/PROJECT-STATUS.md` and `devlog.md` are older snapshots (June 2026 and earlier). Don't treat them as current.
