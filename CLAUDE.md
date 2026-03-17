# Surviving the Singularity

## Project Overview

**Surviving the Singularity** is a book + website by Christopher Tavolazzi about understanding, preparing for, and thriving through the most transformative period in human history — the technological singularity.

The site serves as the book's home base: marketing, blog, book reader, and community hub.

## Tech Stack

- **Framework:** SvelteKit 2.0 + Vite 5
- **Styling:** Tailwind CSS 3.4 + custom CSS (dark-first design)
- **UI Library:** Flowbite Svelte
- **Markdown:** mdsvex for `.md`/`.svx` files
- **Backend:** Supabase (auth, storage)
- **Payments:** Stripe
- **Images:** Sharp + vite-imagetools (auto WebP)
- **Deployment:** adapter-auto

## Key Commands

```bash
npm run dev          # Start dev server
npm run build        # Production build
npm run preview      # Preview production build
npm run optimize-images  # Optimize images
npm run create-blog  # Scaffold a new blog post
```

## Project Structure

```
src/
├── routes/              # SvelteKit pages
│   ├── +page.svelte     # Homepage (hero, countdown, timeline, features, FAQ)
│   ├── +layout.svelte   # Root layout (banner, navbar, footer)
│   ├── blog/            # Blog listing + individual posts
│   ├── book/[sectionId] # Book reader with pagination & progress
│   ├── about/           # Mission / about page
│   ├── sample/          # Book sample / preview
│   ├── start-here/      # Onboarding page
│   └── api/             # API endpoints
├── lib/
│   ├── components/      # 64+ Svelte components
│   ├── data/
│   │   ├── book-draft-v2/   # Full book content (19 markdown files, 12 chapters)
│   │   ├── blog-posts/      # Blog posts (content.md + index.js each)
│   │   ├── quotes.json      # Featured quotes
│   │   ├── timelineItems.json
│   │   └── technologies.json
│   ├── stores/          # Svelte stores (darkMode, bookPage, etc.)
│   ├── utils/           # Helpers (navigation, etc.)
│   └── styles/          # Global styles
static/
├── images/              # Static assets, book cover, blog images
work_efforts/            # Johnny Decimal project management system (see below)
docs/contributing/       # CONTRIBUTING.md, STYLE_GUIDE.md, SECURITY.md
.AI-Setup/               # AI session context docs (autoseeded to Claude)
```

## Book Content

The book has 12 chapters + intro, epilogue, glossary, and further reading:

1. AI & the Singularity overview
2. AI's impact on jobs and economy
3. AI in everyday life
4. AI in healthcare
5. AI in education
6. AI in art, creativity, entertainment
7. AI in relationships
8. AI in politics
9. AI in finance
10. Surviving the age of AI
11. Thriving in the age of AI
12. Looking forward

**Writing voice:** Conversational, witty, direct address ("you"), pop culture references, satirical commentary balanced with genuine optimism. NOT doom-and-gloom — practical and empowering.

## Design System

- **Theme:** Dark-first (forced dark mode via `document.documentElement.classList.add('dark')`)
- **Primary accent:** Blue gradient (#63b3ed / #3b82f6 / #8b5cf6)
- **Background:** Deep navy (#020617 / #0f172a)
- **Text:** Light slate (#e2e8f0 primary, #94a3b8 secondary)
- **Fonts:** Inter (body), JetBrains Mono (code/accents), Orbitron (special headings)
- **Feel:** Futuristic, clean, editorial — like a tech magazine from 2030

## Current Status: Book Revival Phase

The site was rebuilt with a fresh v2 design (new hero, navbar, footer, theme). We are now entering the **book revival phase** — shifting from "under construction" to actively promoting and hyping the book.

### Revival Goals
- Transform the site from "coming soon" energy to "the book is HERE" energy
- Drive readers to explore the book content
- Build excitement and shareability
- Position the book as essential reading for the AI age
- Encourage word-of-mouth sharing

### Key Pages for Book Promotion
- `/sample` — Book sample/preview (primary conversion page)
- `/book/[sectionId]` — Full book reader
- `/start-here` — Onboarding funnel
- `/blog` — Supporting content that builds authority

## Environment Variables

```
SUPABASE_URL, SUPABASE_SERVICE_KEY
PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY
STRIPE_SECRET_KEY, STRIPE_PRICE_ID
PUBLIC_BASE_URL
```

## Blog System

Blog posts live in `src/lib/data/blog-posts/<slug>/`:
- `content.md` — Post body in markdown
- `index.js` — Metadata (title, date, author, excerpt, featured image, slug)

Use `npm run create-blog` to scaffold new posts.

## Work Efforts (Johnny Decimal System)

Tasks and project history live in `work_efforts/` using a Johnny Decimal numbering scheme:

| Folder | Domain |
|--------|--------|
| `00_project_management/` | Roadmaps, indices, meta |
| `10_development/` | Features, bug fixes, refactors |
| `12_image_optimization_enhancements/` | Image pipeline work |
| `20_content/` | Blog posts, book content, copy |
| `30_design_ui/` | Visual design, UI changes |
| `40_infrastructure/` | Hosting, CI, env config |
| `50_maintenance/` | Deps, security, cleanup |
| `60_testing/` | QA, test suites |
| `70_documentation/` | Docs, guides, changelogs |
| `80_deployment/` | Release, deploy tasks |
| `90_archive/` | Completed / abandoned work |

Each work effort is a markdown file named `<id>_<slug>.md` with frontmatter: `title`, `status`, `priority`, `assignee`, `created`, `last_updated`, `due_date`, `tags`.

Active project log: `work_efforts/devlog.md`

## AI Session Docs (Autoseed)

The `.AI-Setup/` directory contains context documents that are automatically available to AI assistants:

- `INSTRUCTIONS.md` — Quick reference and command overview
- `AI-setup-instructions.md` — How the ai-setup tooling works
- `AI-work-effort-system.md` — Work effort format and conventions
- `AI-setup-validation-instructions.md` — Validation checklist

These docs supplement `CLAUDE.md`. `CLAUDE.md` is the authoritative project context; `.AI-Setup/` docs cover tooling conventions.

## Contributing & Style

See `docs/contributing/` for:
- `CONTRIBUTING.md` — PR workflow, branching, commit style
- `STYLE_GUIDE.md` — Component structure, naming, CSS conventions
- `SECURITY.md` — Security policy
- `SUPABASE_SECURITY.md` — Database/auth security rules

## Important Notes

- The site uses Svelte 4 reactive syntax (`$:`, `export let`, etc.) — not Svelte 5 runes
- Dark mode is force-enabled globally; no light mode toggle needed
- Image optimization runs at build time; use `/images/` path for static assets
- The construction banner in `+layout.svelte` should reflect current project phase
- Book cover image: `/images/Surviving-the-Singularity-Cover.png` (+ `.webp` variant)
- Supabase and Stripe integrations are currently **disabled** (both return stubs); env vars are defined but not active
