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
/                    → Landing page (hero + thesis + 3 pillars + stack table + chapter preview)
/blueprint           → Blueprint table of contents (8 chapters)
/blueprint/[section] → Individual blueprint sections (data from src/lib/data/blueprint.js)
/book                → Book preview (existing content preserved)
/blog                → Blog listing (existing posts preserved)
/blog/[slug]         → Individual blog posts
/about               → About page
/login               → Auth (login/signup/forgot password)
/profile             → User profile (protected route)
/auth/callback       → OAuth/email callback handler
/policies            → Legal policies
```

## Key Files
- `src/hooks.server.js` — Supabase session management (gracefully degrades without credentials)
- `src/lib/supabase.js` — SSR-compatible Supabase client factory
- `src/lib/data/blueprint.js` — All blueprint content (8 sections with prose, tables, callouts, directives)
- `src/lib/data/blog-posts/blogPosts.js` — Blog post loader
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
npm run create-blog  # Create new blog post
```

## Content Architecture
Blueprint content lives in `src/lib/data/blueprint.js` as a structured array of sections. Each section has:
- `slug`, `number`, `title`, `subtitle`
- `content[]` — array of blocks: `prose`, `heading`, `table`, `callout`, `directive`

Blog posts live in `src/lib/data/blog-posts/[slug]/` with `content.md` + `index.js`.

## Conventions
- Dark mode only (forced via class)
- Component CSS > Tailwind for page-level styling
- JetBrains Mono for numbers, labels, code
- Amber (`#f59e0b`) for primary actions and accents
- All tables use the `data-table` pattern from blueprint sections
