# Surviving the Singularity

> A field manual for staying agentic as AI rewrites work, money, medicine, and meaning.

**Live site:** [survivingthesingularity.com](https://survivingthesingularity.com)
**Status:** Open draft. Book ships when it ships. Site updates as the world does.

---

**Editing the book?** The single source of truth is
[`src/lib/data/book/`](src/lib/data/book/) plus
[`book.json`](src/lib/data/book/book.json). Everything else that contains book
text is generated output. Full rules: [Book content: the single source of
truth](#book-content-the-single-source-of-truth).

---

## 📖 The book reader just got a real upgrade (2026-07-15)

The `/book` reading experience went from "a page with chapters on it" to an actual reader, in one long session:

- **Reader Mode.** A real, engineered distraction-free mode (browsers don't expose an API to trigger their native reader mode from the page, so we built our own): one tap strips the chrome - our own nav, the site's floating navbar, all of it - and bumps the type size up for comfortable reading. Toggle lives bottom-right, always reachable, remembers your preference.
- **The chapter nav gets out of your way.** Scroll down to read, the TOC/Chapters pill slides out of sight. Scroll up, it slides back. Less UI fighting the text for space.
- **It remembers your page, but re-locks on refresh.** Reload the tab, close it, open a new one - the password gate comes back, on purpose. But your reading position survives all of that, so re-entering the password drops you right back where you left off.
- **Continue Reading, fixed for real.** It used to freeze on whatever chapter you first opened, because SvelteKit reuses the page component across chapter navigation and the old code only checked on first mount. Now it tracks properly across every chapter you visit.
- **Word counts instead of "X min read."** Time estimates read like a chore. A number doesn't.
- **All 287 em dashes gone** from the actual book text - replaced with whatever punctuation the sentence actually wanted (comma, ellipsis for interrupted dialogue, colon in two titles), not a blind find-and-replace.
- **Keyboard nav.** Left/right arrows move between chapters.
- **A real "thank you."** The quiet footer line on every page now opens an actual note - short, direct, no fluff, because the people who read this far into a book about the Singularity deserve better than a decorative emoji.

Four PRs, all tested against production with real browser automation before being called done, not just "looks right in the diff."

---

## What this is

A SvelteKit site built around one question:

> What does it look like to build a life that doesn't depend on the things AI is about to dissolve?

It is not a sales page. It is not a course. It is a working draft of a book, a long blueprint of practical answers, and a blog of dispatches from the curve. Free to read. No login. No paywall. No email required.

## Who this is for

- People who have read Kurzweil, Hinton, Aschenbrenner, Amodei and want to take the timeline seriously.
- People who can feel the economic ground shifting under their feet and want a practical move, not another think piece.
- Makers, builders, parents, teachers, anyone who would rather stay agentic than be passive cargo.

If you came here because someone you trust sent you the link, start at [**Why**](https://survivingthesingularity.com/why). It is the shortest case for why any of this matters.

## What is on the site

| Route | What it is |
|-------|-----------|
| [`/`](https://survivingthesingularity.com/) | Landing page. Thesis, four steps, the stack, a savings calculator, the chapter index. |
| [`/why`](https://survivingthesingularity.com/why) | The case. AGI timeline, expert voices, benchmarks. Start here if you are new. |
| [`/book`](https://survivingthesingularity.com/book) | Open draft of *Surviving the Singularity*. Free to read. Chapter previews. |
| [`/blueprint`](https://survivingthesingularity.com/blueprint) | Eight chapter blueprint. Shouse construction, collective ownership, semi-autonomous CSA, local AI, offline healthcare AI, and more. |
| [`/blog`](https://survivingthesingularity.com/blog) | Dispatches. Some philosophical, some profane. |
| [`/about`](https://survivingthesingularity.com/about) | What this project is and is not. |

## Stay in touch

There is one channel: [thecoffeejesus.substack.com](https://thecoffeejesus.substack.com). Subscribe if you want chapter drops and launch alerts. Otherwise the site is here, always, and you can read it whenever.

---

## For developers

This project is open source. If you want to fork it, remix it, or contribute fixes, here is what you need to know.

### Stack

- **Framework:** SvelteKit v2 + Vite v5
- **Styling:** Tailwind CSS v3 + scoped component CSS, dark-only theme
- **Auth/Database:** Supabase (newsletter signup fallback only, gracefully degrades without credentials)
- **Fonts:** Inter (UI) + JetBrains Mono (numbers, code)
- **Deployment:** adapter-auto (Cloudflare Pages target)

### Design tokens

- Background: `#020617` (deep navy-black)
- Primary accent: `#f59e0b` (amber)
- Secondary accent: `#3b82f6` (blue)
- Tokens: [`src/lib/styles/theme.css`](src/lib/styles/theme.css)

### Local development

```bash
git clone https://github.com/ctavolazzi/survivingthesingularity.git
cd survivingthesingularity
npm install
npm run dev -- --open
```

Without Supabase credentials in `.env`, newsletter signup falls back to localStorage. Everything else works.

### Building

```bash
npm run build
npm run preview
```

### Project layout

```text
src/
  routes/                Pages and API endpoints
    +page.svelte         Landing
    book/                The book, one route per section
      [sectionId]/       Dynamic section pages
    read/                Continuous reader (whole book, one scroll)
    blog/                Posts
    about/               Project framing
  lib/
    bookContent.js       Loads the book from book.json + the .md files
    components/          Reusable Svelte components (41+)
    data/
      book/              THE BOOK. Source of truth. See below.
      blog-posts/        Legacy per-slug blog content (do not add new posts here)
      blueprint.js       Orphaned: no route renders this any more
    styles/theme.css     Design tokens
static/
  book-images/           Every figure the book references (106 files)
```

### Book content: the single source of truth

**The book is the 30 Markdown files in [`src/lib/data/book/`](src/lib/data/book/), and [`book.json`](src/lib/data/book/book.json) decides which files are the book and in what order.**

Both halves are required:

- **`*.md`** holds the prose, one file per section.
- **`book.json`** is the manifest: which files, what order, what titles, plus the version, title and subtitle that become EPUB and PDF metadata.

Neither is the book on its own. **A `.md` file in that folder that is not listed in `book.json` is not in the book.** That is how `VOICE-GUIDE.md`, `ELIJAH-PROTOCOL.md` and `README.md` live in the directory without leaking into the manuscript. It is a real gate, not a convention: `scripts/build-epub.sh` reads the file list with `jq -r '.sections[].file'`, and the website reads the same manifest in `src/lib/bookContent.js`.

Everything else is **output, derived from those two inputs**:

| Artifact | Made by | What it is |
| --- | --- | --- |
| The `/book` reader and `/read` | `src/lib/bookContent.js` | rebuilt from source every deploy |
| Shipping EPUB and review PDF | `scripts/build-epub.sh` | regenerated by the build |
| PLAIN and DELUXE PDFs | `scripts/build-pdf-variants.sh` | regenerated by the build |
| `manuscript/StS-Complete-Draft-*.md` | `sts.py compile` | export snapshots, nothing reads them back |
| `src/lib/data/book/manuscript-index.json` | `sts.py id build` | a generated cache |

Five consumers, no editable copies. Hand-editing any of them is lost work: the next build overwrites it.

Three ways people get this wrong:

1. **Editing a compiled draft.** The files in `manuscript/` look like the manuscript. They are exports. Edits there are a dead end.
2. **Trusting the index.** `manuscript-index.json` is a cache over the truth. `sts.py id verify` re-parses the live source and checks that against itself, so it *cannot* tell you the index file on disk has gone stale. A clean `id verify` is not evidence the index is current.
3. **Editing an orphan that looks like the source.** `src/lib/data/book-v1-archive/` is an older draft with near-identical filenames, and `src/lib/data/sample.md` is stale promo copy. Nothing imports either one, verified by grep, so neither can reach the site or any build. If your edit changes nothing, check which directory you are in.

For version and word count, the only authorities are `book.json` and `scripts/sts.py` run live. Any document asserting a number is making a claim, not a measurement.

### Blueprint content

[`src/lib/data/blueprint.js`](src/lib/data/blueprint.js) still exists but **no route renders it** - the `/blueprint` route was removed in a past redesign. Treat it as orphaned rather than as a content source, and do not link to `/blueprint`.

### Blog posts

```bash
npm run create-blog "Your Post Title"
```

Creates a new directory in `src/lib/data/blog-posts/` with `content.md` and `index.js`.

### Conventions

- Dark mode only (class-forced)
- Component-scoped CSS preferred over Tailwind for page-level styling
- JetBrains Mono for numbers, labels, and code
- Amber (`#f59e0b`) for primary actions
- Tables follow the `data-table` pattern used in blueprint sections
- No em-dashes anywhere in copy. Hyphens, commas, periods, or parentheticals only.

### Contributing

PRs welcome for bug fixes, accessibility improvements, and performance. Content edits live in `src/lib/data/`. See [docs/contributing/CONTRIBUTING.md](docs/contributing/CONTRIBUTING.md) for details.

## License

Code: open source. Book content: all rights reserved, free to read on the live site.

## Author

Christopher Tavolazzi. Writes as [Coffee Jesus](https://thecoffeejesus.substack.com).
