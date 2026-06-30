# Hardening & Architecture Handoff

> **You are a fresh AI picking up the pre-launch hardening of this site.** This doc is
> your starting point. It captures what's done, what's verified, what remains (prioritized),
> and the working method. Read `docs/ARCHITECTURE.md` first (the site + API map), then this.
>
> **Last updated:** 2026-06-30 (session 2) · **Active branch:** `homepage-redux-jun2026`

---

## How to work (the method that's been paying off)

1. **Verify every audit claim against the code before acting.** This effort used three
   parallel audit agents; verification caught real errors in their output (see
   "Corrections" below). Never delete or "fix" on an agent's say-so — open the file.
2. **`npm run build` must stay green after every change group.** Commit per coherent group
   with a descriptive message (end messages with the `Co-Authored-By` trailer).
3. **Update `docs/ARCHITECTURE.md` in the same change** whenever you add/remove a route or
   API endpoint, flip a render mode (prerender ↔ SSR), or touch the data model.
4. **Prefer additive/reversible.** Don't delete without confirming a backup (e.g. the game
   was *preserved on a branch*, not deleted — see below). Ask before destructive ops.
5. **Verify behavior, not just compilation.** The engine/sim code is DOM-free and can be
   driven headlessly in Node (see the auto-sim verification that proved the game loop). Use
   `curl` against the dev server for routes/headers; reserve a real browser for client render.

---

## What's done in session 2 (staged, not yet committed)

- **P1.5** `vite.config.js` `sourcemap: false` — no `.map` files ship to CDN
- **P1.6** `src/routes/api/fetch-title/+server.js` — `rateLimit('fetch-title:'+ip, 10, 60_000)` added
- **P1.3** `src/routes/api/checklist-email/+server.js` — origin check + content-type guard match `waitlist/+server.js`
- **P1.4** `src/lib/components/Navbar.svelte` — removed invalid `role="listitem"` from `<a>` and `role="list"` from container div; no more A11y build warning
- **P1.2** `src/routes/blog/+page.server.js` — added 3 missing posts (darpa, neuralink, synthetic-biological-computers); removed unused `loadBlogPosts` import; blog index now covers all 12 real posts (example-template-post intentionally excluded)
- **P1.1** `sql/005_preorders_copy_lock.sql` — new migration: `UNIQUE (edition_type, copy_number)` + `pg_advisory_xact_lock(hashtext('authors_copy'))` in trigger; endpoint already handles 23505/SOLD_OUT correctly

All changes build green (`npm run build` ✓ 22.75s, ~65 prerendered routes, no A11y role warnings, zero .map files in client output). Awaiting commit.

---

## What's already done (committed)

- **Launch premortem fixes** — commit `f325373` on `homepage-redux-jun2026`:
  - Static routes **prerendered** (homepage, blog+posts, book+sections, legal, signals) via
    `prerender = true` on the root `+layout.server.js`; dynamic routes opt out; `/book/[sectionId]`
    has explicit `entries()`. Only `/early-access`, `/early-access/success`, `/unsubscribe` stay SSR.
  - Welcome email is **fire-and-forget** (`waitUntil`) in `src/routes/api/waitlist/+server.js`.
  - **Lead-capture fallback** on `/early-access` (buffers to localStorage + retries on outage).
  - `static/_headers` restores CSP/HSTS on prerendered pages that bypass `hooks.server.js`.
- **Shouse game split off** — commit `f3ed56a`: the orphaned 3D game (24 files) was removed
  from this branch and **preserved on branch `StS-Game`** (pushed to origin). `StS-Game` also has
  an **ambient auto-sim** mode (`cff8baf`, local) — runs all build stages, holds, loops. Do not
  reintroduce game code here; work on it from `StS-Game`.
- **`docs/ARCHITECTURE.md`** — the living site + API map (C4 + arc42 style). Keep it current.

Decisions already made by the owner: **keep `adapter-auto`** (don't pin); **rate limiter stays
in-memory for launch**, durable upgrade is a post-launch follow-up.

---

## Remaining work — prioritized (all findings verified against code)

### P1 — correctness & security (do first; small, high-value)

1. **Author's Edition copy-number race** — `sql/003_preorders.sql:28-37`. A `BEFORE INSERT`
   trigger does `select coalesce(max(copy_number),0)+1` with **no unique constraint on
   `copy_number`** → concurrent author's-edition preorders can both claim the same number /
   oversell past 100. Fix: new migration adding `unique (edition_type, copy_number)` (fail-safe)
   + `pg_advisory_xact_lock(hashtext('authors_copy'))` in the trigger; handle 23505 retry in
   `src/routes/api/preorder/+server.js`.
2. **Blog content drift** — `src/routes/blog/+page.server.js` hardcodes a **9-post** array but
   there are **13** post directories → ~4 published posts never show on `/blog`. Fix: drive the
   index from `loadBlogPosts()` (`src/lib/data/blog-posts/blogPosts.js`). Confirm which dirs are
   intentionally excluded (e.g. `example-template-post`).
3. **`checklist-email` missing guards** — `src/routes/api/checklist-email/+server.js:41` has
   rate-limit + honeypot but **no origin check / content-type guard** (email-bomb vector). Copy
   the guards from `waitlist/+server.js:17-35`.
4. **Navbar invalid ARIA** — `src/lib/components/Navbar.svelte` `<a role="listitem">` (build
   emits the A11y warning). Put `role="listitem"` on the `<li>` or use a real `<ul><li>`.
5. **Production sourcemaps** — `vite.config.js:22` `sourcemap: true` ships source to the CDN.
   Set `false` (or gate on `NODE_ENV`).
6. **`fetch-title` unthrottled** — `src/routes/api/fetch-title/+server.js` is SSRF-guarded
   (https-only, `ALLOWED_HOSTS`, private-IP block) but has **no rate limit**. Add
   `rateLimit('fetch-title:'+ip, 10, 60_000)`.

### P2 — hardening & cleanup

7. **Consent version skew** — `StickyCaptureBar.svelte` and `DisclaimerBanner.svelte` hardcode
   the consent version separately. Extract `CONSENT_KEY`/`CONSENT_VERSION` to `src/lib/consent.js`.
8. **Dead code (deletion gated on owner OK)** — 20 verified-orphan components (zero refs):
   `BlueprintTOC, WindowSim, DivergenceDiagram, IndependenceCountdown, AGICountdown,
   StackConfigurator, LiveDashboard, BookStatusBanner, SignalsTicker, YouTubeEmbed,
   LaunchPlanCard, PillarsLoopDiagram, CopyPageText, ReadingPreferences, AudienceSwitcher,
   SavingsCalculator, PlaceholderImage, InteractiveStackTable, FloatingNav, ChapterPreviewCard`.
   They still carry dead `/blueprint` links. (The game cluster — also dead — is already split to
   `StS-Game`.) Re-verify zero refs at delete time; they live in git history.
9. **Unused book drafts** — `src/lib/data/book-draft`, `book-draft-v2`, `book-editing` (804K).
   **NOT bundled** (`bookContent.js` globs only `book/*.md`) — disk/repo cleanup only.
10. **`.AI-Setup/` clutter** — 896 tracked files. `git rm -r --cached` (keep local) or remove.
11. **CSP `'unsafe-inline'`** — `src/hooks.server.js:38-39` + `static/_headers`. Proper fix is
    SvelteKit's `kit.csp` config (its own hash/nonce), not a hand-rolled nonce. Keep both in sync.
12. **API guard gaps** — add rate limits to `unsubscribe` (+honeypot), `stripe-checkout`
    (+content-type), and read GETs (`preorder-count, featured-posts, latest-post, timeline`);
    clamp pagination in `src/routes/api/timeline/+server.js:10-11`. Reuse `rateLimit.js`.
13. **Images** — recompress `static/book-images/*` (multi-MB) to width-capped WebP; add
    `width`/`height`/`decoding="async"` site-wide (layout shift, esp. now-prerendered); consider
    self-hosting the ~12 hotlinked external image hosts in the CSP `img-src`. The
    `work_efforts/.../image_build_hook.js` emits `optimized/manifest.json` nothing consumes —
    wire it up or drop it.
14. **SEO** — per-route meta description + `og:image` on `/book/[sectionId]` and `/early-access`;
    Article/Book JSON-LD; prerender `/sitemap.xml`; optional `Disallow: /api/` in `robots.txt`.

### P3 — polish
15. **Email HTML escaping** — `src/lib/server/email.js` interpolates `name` unescaped into
    preorder/admin email HTML; add an escape/clip helper (checklist email already escapes).

### Standing follow-ups
- **Durable rate limiter** — in-memory limiter (`src/lib/server/rateLimit.js`) is per-isolate on
  serverless. Recommended durable store: a Supabase counter (host-portable, matches `adapter-auto`).
- **Resend custom domain** — `email.js` sends from the `resend.dev` sandbox; verify a real domain
  and set `EMAIL_FROM` before the marketing push (deliverability).

---

## Corrections to watch for (where the audits were wrong)

- Book drafts are **disk weight, not bundle bloat** — the glob is scoped to `book/*.md`.
- Crawl does **not** auto-prerender discovered pages in this setup — only routes that inherit
  `prerender = true` (set at the root layout) get baked; that's why the root-layout approach was used.
- `SignalsTicker` / `ReadingPreferences` are **dead code**, so any audit findings on them are moot.
- `fetch-title` is **already SSRF-guarded**; it only needs a rate limit, not an allowlist rebuild.
- `fulfilled_sessions` idempotency (success page) is **correct** (PK on `session_id`).

---

## Verification playbook
- `npm run build` → green; confirm the prerender set is unchanged (~65 routes) and no A11y/role warnings.
- Routes/headers: `curl -I` the dev server; prerendered page should show CSP/HSTS via `_headers`.
- Engine/sim logic: import the DOM-free module in a Node `.mjs` and drive it (see how the game
  auto-sim was proven: two runs each reached all 6 stages headlessly).
- Funnel: POST `/api/waitlist` (and cross-origin/burst variants → expect 403/429); confirm a row lands.
- DB race (#1): reason through the new unique constraint + advisory lock, or simulate concurrent inserts.

## Key files
- Render/build: `src/routes/+layout.server.js`, `svelte.config.js`, `vite.config.js`, `static/_headers`
- API/data: `src/routes/api/*/+server.js`, `src/lib/server/{email,rateLimit,supabaseAdmin}.js`, `sql/*.sql`
- Content: `src/routes/blog/+page.server.js`, `src/lib/data/blog-posts/blogPosts.js`, `src/lib/bookContent.js`
- Security: `src/hooks.server.js`
- Map to keep current: `docs/ARCHITECTURE.md`
