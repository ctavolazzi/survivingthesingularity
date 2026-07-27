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
(There are no /blueprint, /login, /profile, or /auth routes — removed in a past
redesign; don't link to them.)

## Key Files
- `src/hooks.server.js` — Supabase session management (gracefully degrades without credentials)
- `src/lib/supabase.js` — SSR-compatible Supabase client factory
- `src/lib/data/blueprint.js` — All blueprint content (8 sections with prose, tables, callouts, directives)
- `src/routes/blog/+page.server.js` — Blog listing (hardcoded `posts` array; new posts must be added here)
- `src/lib/components/Navbar.svelte` — Main nav with auth state
- `src/lib/components/Footer.svelte` — Footer
- `src/lib/components/CookieConsent.svelte` — GDPR-style cookie banner

## Auth Setup
Auth requires a real Supabase project. Without credentials, the site runs fine but auth features are disabled.
1. Create a Supabase project at https://supabase.com
2. Copy URL + anon key to `.env` (replace placeholders)
3. Enable Email auth + any OAuth providers (GitHub, Google) in Supabase dashboard
4. Set redirect URL to `https://yourdomain.com/auth/callback`

## Commands
```bash
npm run dev          # Start dev server
npm run build        # Production build
npm run preview      # Preview production build
```

(`npm run create-blog` scaffolds the LEGACY blog format and does not register the
post in the listing — do not use it for new posts; see Content Architecture.)

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
