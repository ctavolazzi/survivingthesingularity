# CLAUDE.md — Surviving the Singularity

## Project Overview

Educational web platform about AI and the technological Singularity. Built with SvelteKit, it provides blog content, book samples, AI timelines, and interactive features. The site has transitioned from a community platform to a curated educational resource — newsletter, Discord, and commercial community features have been removed.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | SvelteKit 2 + Svelte 4 |
| Build Tool | Vite 5 |
| Styling | Tailwind CSS 3 + Flowbite Svelte + Tailwind Typography |
| Content | MDSvex (Markdown in Svelte), marked, remark |
| Backend | Supabase (auth, database) |
| Payments | Stripe |
| Language | JavaScript (ES modules, JSConfig — not TypeScript) |
| Image Processing | Sharp + vite-imagetools (WebP conversion) |
| Other | Three.js, Chart.js, date-fns, PapaParse, PDF.js |

## Quick Start

```bash
npm install
cp .env.example .env   # Fill in Supabase + Stripe credentials
npm run dev             # Starts dev server at localhost:5173
```

## Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server |
| `npm run build` | Production build (runs prebuild image optimization first) |
| `npm run preview` | Preview production build locally |
| `npm run check` | Run svelte-check for type/lint diagnostics |
| `npm run check:watch` | Watch mode for svelte-check |
| `npm run create-blog "Title"` | Scaffold a new blog post |
| `npm run migrate-blog` | Migrate old-format blog posts to new structure |
| `npm run optimize-images` | Run image optimization manually |

## Project Structure

```
src/
├── routes/                    # SvelteKit file-based routing
│   ├── +layout.svelte         # Root layout (dark mode enforced)
│   ├── +page.svelte           # Home page
│   ├── +page.server.js        # Home page server-side data loading
│   ├── about/                 # About page
│   ├── blog/                  # Blog listing + individual post routes
│   ├── book/                  # Book content pages
│   ├── sample/                # Book sample pages
│   ├── start-here/            # Getting started guide
│   ├── policies/              # Privacy policy, terms
│   └── api/                   # API endpoints (see below)
├── lib/
│   ├── components/            # ~60 Svelte components
│   │   ├── ui/                # Reusable UI primitives (Button, Card, Input, etc.)
│   │   ├── ads/               # Ad-related components
│   │   └── *.svelte           # Feature components (Navbar, Footer, BlogPostTemplate, etc.)
│   ├── data/
│   │   ├── blog-posts/        # Blog content (see Blog System below)
│   │   └── timelineItems.json # Timeline event data
│   ├── stores/                # Svelte stores for global state
│   ├── utils/                 # Client-side utilities
│   │   ├── navigation.js      # gotoAndScrollTop helper
│   │   ├── supabaseClient.js  # Supabase client setup
│   │   ├── markdownParser.js  # Markdown processing
│   │   └── eventBus.js        # Event bus for cross-component communication
│   ├── server/                # Server-only code
│   │   └── supabaseAdmin.js   # Supabase admin client
│   ├── styles/
│   │   └── theme.css          # CSS custom properties (color tokens, layout vars)
│   └── assets/                # Importable static assets
├── app.css                    # Global styles and Tailwind directives
└── hooks.server.js            # Server hooks (navigation error handling)

static/                        # Public static assets (images, fonts)
docs/contributing/             # Contributing, style guide, security docs
work_efforts/                  # Task tracking (Johnny Decimal organized)
```

## API Endpoints

All under `src/routes/api/`:

| Endpoint | Purpose |
|----------|---------|
| `/api/featured-posts` | Featured blog posts (uses Cloudflare caching) |
| `/api/latest-post` | Most recent blog post |
| `/api/timeline` | Timeline events data |
| `/api/news-ticker` | News ticker content |
| `/api/fetch-title` | Fetch page title from URL |
| `/api/create-checkout-session` | Stripe checkout session |

## Blog System

Blog posts live in `src/lib/data/blog-posts/[post-slug]/` with this structure:

```
src/lib/data/blog-posts/
├── blogPosts.js              # loadBlogPosts() — imports and caches all posts
├── whispers-of-the-future/
│   ├── content.md            # Markdown content
│   └── index.js              # Metadata: title, date, author, excerpt, slug
├── singularity-express/
│   ├── content.md
│   └── index.js
└── ...
```

To create a new post: `npm run create-blog "Post Title"`

Blog routes use `+page.server.js` load functions for server-side data fetching. The `blogPosts.js` module dynamically imports all posts and caches them.

## Architecture & Patterns

### Component Conventions
- Component files use **PascalCase**: `BlogPostTemplate.svelte`
- Non-component files use **kebab-case**: `timeline-items.json`
- Functions use **camelCase**: `handleSubmit`, `loadBlogPosts`
- Component structure order: `<script>` → markup → `<style>`
- Props declared with `export let propName`
- Reactive declarations with `$:` syntax

### Styling
- **Tailwind CSS** for layout and utilities
- **Component `<style>` blocks** for animations and component-specific styles
- **Dark mode is always on** — enforced in root layout, class-based (`darkMode: 'class'` in Tailwind config)
- CSS custom properties defined in `src/lib/styles/theme.css`:
  - Primary: `#3b82f6` (blue)
  - Accent: `#ff7708` (orange, used for headings and links in prose)
  - Heading font: `Orbitron` (secondary/display font)
  - Body font: system font stack
- Responsive breakpoints: 768px (tablet), 480px (mobile), 350px (extra small)
- Use `:global()` selector for overriding child component styles

### State Management
- **Svelte stores** in `src/lib/stores/` — no external state management library
- `darkMode.js` — readable store, always returns `true`
- `tacticLibrary.js` — tactics/strategies data
- `downloadStats.js` — download tracking
- `bookPage.js` — book reading progress
- `userStore.js` — user state
- `researchLinksStore.js` — research links

### Data Fetching
- Server-side: `+page.server.js` load functions (preferred)
- Client-side: `onMount` fetch calls when needed
- API responses use Cloudflare Cache API headers where applicable

### Navigation
- Use `gotoAndScrollTop()` from `$lib/utils/navigation` instead of raw `goto()`
- Server hooks redirect malformed URLs (e.g., `[object Object]` in path) to home

### Image Handling
- `vite-imagetools` converts images to WebP at quality 80 during build
- `ResponsiveImage.svelte` and `SafeResponsiveImage.svelte` for optimized rendering
- `prebuild` script copies blog post assets and runs `image_build_hook.js`

## Environment Variables

Required in `.env` (see `.env.example`):

```
SUPABASE_URL=             # Server-side Supabase URL
SUPABASE_SERVICE_KEY=     # Server-side Supabase service key
PUBLIC_SUPABASE_URL=      # Client-side Supabase URL
PUBLIC_SUPABASE_ANON_KEY= # Client-side Supabase anon key
STRIPE_SECRET_KEY=        # Stripe secret key
STRIPE_PRICE_ID=          # Stripe price ID
PUBLIC_BASE_URL=          # Base URL (http://localhost:5173 for dev)
```

Server-side env vars: `$env/static/private`
Client-side env vars: `$env/static/public` (must be prefixed with `PUBLIC_`)

## Security Rules

- Never expose API keys or secrets in client-side code
- Sensitive values go in `.env` (gitignored)
- All data mutations must go through server endpoints
- Validate user input on both client and server
- `scripts/` and `supabase/` directories are gitignored for security
- See `docs/contributing/SUPABASE_SECURITY.md` for database security guidelines

## Configuration Files

| File | Purpose |
|------|---------|
| `svelte.config.js` | SvelteKit config: adapter-auto, mdsvex preprocessing, `.md`/`.svx` extensions |
| `vite.config.js` | Vite config: imagetools plugin, sourcemaps, markdown asset handling |
| `tailwind.config.js` | Tailwind: Flowbite plugin, typography plugin, custom colors, dark mode class |
| `postcss.config.js` | PostCSS: Tailwind + Autoprefixer |
| `jsconfig.json` | JavaScript project config (path aliases via `$lib`) |
| `.npmrc` | `engine-strict=true` |

## SvelteKit-Specific Notes

- **Adapter**: `adapter-auto` — auto-detects deployment platform (Vercel, Netlify, Cloudflare, etc.)
- **File extensions**: `.svelte`, `.md`, `.svx` are all valid page/component extensions
- **Prerender errors**: 404s on `/newsletter` and `/blog` paths are ignored during build; other HTTP errors fail the build
- **Missing IDs**: `handleMissingId: 'ignore'` in prerender config
- **Path alias**: `$lib` maps to `src/lib/`

## Testing & Linting

- **No test framework** is configured (no Jest, Vitest, Cypress, etc.)
- **No ESLint or Prettier** config — code quality relies on `svelte-check`
- Run `npm run check` to validate Svelte component types and catch errors
- **No CI/CD pipelines** — no `.github/workflows/` present

## Things to Avoid

- Do not re-add removed community features (newsletter signup, Discord integration, Treasure Tavern)
- Do not commit `.env` files, SQL files, or anything in `scripts/`, `cursor/`, `supabase/`
- Do not change dark mode to be toggleable — it is intentionally always on
- Do not add TypeScript — the project uses plain JavaScript with JSConfig
- Do not use `goto()` directly — use `gotoAndScrollTop()` from `$lib/utils/navigation`
