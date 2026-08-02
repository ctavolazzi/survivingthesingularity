# Surviving the Singularity — Project Guide

## What This Is
A SvelteKit web platform for the **YouTube Shouse Blueprint** — a comprehensive strategy for material independence through digital leverage, local AI, open-source robotics, and minimalist infrastructure.

## Tech Stack
- **Framework**: SvelteKit v2 + Vite v5
- **Styling**: Tailwind CSS v3 + custom CSS (dark-only theme)
- **Auth/Database**: Supabase (SSR via `@supabase/ssr`)
- **Fonts**: Inter (primary), JetBrains Mono (accents/code)
- **Deployment**: adapter-auto (Vercel/Cloudflare/etc.)

## Design System
- **Background**: `#020617` (deep navy-black)
- **Primary accent**: `#f59e0b` (amber — builder energy)
- **Secondary accent**: `#3b82f6` (blue — contrast)
- **Text primary**: `#f1f5f9`
- **Text secondary**: `#94a3b8`
- **Surface**: `rgba(30, 41, 59, 0.5)`
- **All design tokens**: `src/lib/styles/theme.css`

## Routes
```
/                    → Landing page
/book                → Book preview (password-gated draft access)
/book/[sectionId]    → Individual book sections
/blog                → Blog listing
/blog/[slug]         → Individual blog posts
/checklist           → Free readiness checklist (EmailGate + email-to-inbox)
/signals             → Signals feed (arXiv sweep ticker)
/early-access        → Email capture + Stripe checkout ($5 preorder)
/early-access/success → Post-checkout fulfillment page
/about               → About page
/launch              → Launch page
/unsubscribe         → One-click unsubscribe
/policies /terms /disclaimer /accessibility → Legal pages
/api/*               → waitlist, checklist-email, stripe-checkout, timeline,
                       featured-posts, verify-book-password, unsubscribe,
                       fetch-title, discord-application
```
Accounts (added 2026-08-01):
```
/signup                   → create account / sign in (?mode=signin), form actions
/auth/oauth/[provider]    → GET, starts Google/GitHub OAuth (allowlisted)
/auth/callback            → GET, exchanges the code or token_hash for a session
/auth/signout             → POST only
```
(There are still no /blueprint, /login, or /profile routes — removed in a past
redesign; don't link to them. `/signup` is the sign-in surface, not `/login`.)

Auth is **server-side only**: no browser Supabase client, no key in the bundle,
session in httpOnly cookies. Read `src/lib/server/supabaseAuth.js` before
changing any of it. Verify with `node scripts/probe-auth-flow.mjs <url>` — and
run it against `npm run preview`, not `vite dev`, because SvelteKit disables its
CSRF origin check in dev (`if (!DEV)` in kit's respond.js), so the cross-origin
check is meaningless there. The probe detects this and says SKIP.

## Key Files
- `src/hooks.server.js`: resolves the session per request into `event.locals`, sets security headers.
- `src/lib/server/supabaseAdmin.js`: data client. Service role, server-only, bypasses RLS.
- `src/lib/server/supabaseAuth.js`: auth client. Request-scoped GoTrue, server-only. Read its header.
- `src/lib/data/blueprint.js` — All blueprint content (8 sections with prose, tables, callouts, directives)
- `src/routes/blog/+page.server.js` — Blog listing (hardcoded `posts` array; new posts must be added here)
- `src/lib/components/Navbar.svelte`: main nav. Its `user` prop is vestigial and unused.
- `src/lib/components/Footer.svelte` — Footer
- `src/lib/components/CookieConsent.svelte` — GDPR-style cookie banner

## Database Access
There is no browser-side Supabase client. Every query goes through
`src/lib/server/supabaseAdmin.js` on the service role, so the bundle ships no
publishable/anon key and the build needs no Supabase env set at all.

Set `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, and `SUPABASE_ANON_KEY` (server-only,
no `PUBLIC_` prefix, holds the publishable key that auth needs). Do NOT add
`PUBLIC_SUPABASE_*` or create a browser client: `src/lib/supabase.js` was deleted
in WO-08 (`docs/work-orders-2026-07-28.md`) for exactly that reason. Supabase's
own SvelteKit quickstart panel tells you to recreate it; ignore it. Anon holds no
grants on this project, so a browser client returns `42501` on every table anyway.

Full rules live in ONE place: the "Database access" section of `README.md`.

## Commands
```bash
npm run dev          # Start dev server
npm run build        # Production build
npm run preview      # Preview production build
```

(`npm run create-blog` scaffolds the LEGACY blog format and does not register the
post in the listing — do not use it for new posts; see Content Architecture.)

## Provenance and fact-checking

`sts.py factcheck` traces every mechanically detectable claim in the book back to
its evidence, and `scripts/build_factcheck_trace.py` renders that as the public
audit page at `/factcheck`. Full rules, the three git receipt states, what the
pass cannot see, and the verification discipline it was built under live in ONE
place: **`FACTCHECK.md`**. Read it before changing the harness or the trace page.
Do not restate it here.

The one thing worth repeating because it bites: **this worktree carries dirty
paths that belong to other sessions**, including `scripts/sts.py` and several
book chapters. Stage by name and check what else is in a file before committing
it. Never `git add -A`.

## Content Architecture

### The book: `src/lib/data/book/` (single source of truth)

Book text lives in `src/lib/data/book/`, one `.md` per section, with `book.json`
setting the running order. **Edit there and nowhere else.** The website, the EPUB,
the PDFs and the `manuscript/` snapshots are all generated from it and overwritten
on the next build. Never hand-edit an output to correct book text, and never hand
the user a list of stale outputs as if they were files to fix: fix the source, then
rebuild.

Full rules, including the `book.json` gate and the three ways people get this
wrong, live in ONE place: the **"Book content: the single source of truth"**
section of `README.md`. Read it before touching book content. Do not restate it
here; two copies of a rule is the problem it exists to prevent.

### Blueprint and blog

Blueprint content lives in `src/lib/data/blueprint.js` as a structured array of sections. Each section has:
- `slug`, `number`, `title`, `subtitle`
- `content[]` — array of blocks: `prose`, `heading`, `table`, `callout`, `directive`

Blog posts are per-route Svelte pages: `src/routes/blog/[slug]/+page.svelte` holds the
post, and the post must ALSO be added to the hardcoded `posts` array in
`src/routes/blog/+page.server.js` to appear in the listing (and to `static/sitemap.xml`).

Legacy note: `src/lib/data/blog-posts/[slug]/` (`content.md` + `index.js`) is the old
system. Three older routes (`whispers-of-the-future`, `claude-projects-weekend-project`,
`singularity-express`) still import their content from it, so don't delete it — but
never author new posts there.

## Conventions
- Dark mode only (forced via class)
- Component CSS > Tailwind for page-level styling
- JetBrains Mono for numbers, labels, code
- Amber (`#f59e0b`) for primary actions and accents
- All tables use the `data-table` pattern from blueprint sections
