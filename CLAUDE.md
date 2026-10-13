# Surviving the Singularity — project guide

## Product and stack

SvelteKit 2 / Svelte 4 / Vite 5 site for the book **Surviving the Singularity**.
The v0.11 release combines the book, a free public sample and checklist, a blog,
and the $5 digital preorder. `src/lib/offer.js` owns purchase promises. Keep
consumer copy consistent with that module; print is a separate product.

## Source and generated files

Read README.md's **Book content: the single source of truth** before changing
book prose. `src/lib/data/book/book.json` sets the order of canonical Markdown
in that directory. PDFs, EPUBs, snapshots, and bonus archives are generated.
Do not hand-edit those outputs. `publication/README.md` describes the current
artifact pipeline and provenance checks.

Read `FACTCHECK.md` before editing the claim harness or trace page. The current
public trace is a historical mechanical snapshot, not semantic certification
of the current book. Do not describe URL/image resolution as factual support.

## Routes and data

- `/sample`: open introduction and reading guide from canonical book source.
- `/book`, `/book/[sectionId]`, `/read`: draft readers with a shared access-code
  gate. This is intentional client-side friction, not authentication.
- `/early-access` and `/early-access/success`: purchase and verified receipt access.
- `/checklist`, `/blog`, `/about`, `/factcheck`, `/signals`: public site content.
- `/api/*`: server handlers. Customer data uses only the server service-role
  client in `src/lib/server/supabaseAdmin.js`; never add a public Supabase client.

Blog posts are per-route Svelte pages registered in
`src/routes/blog/+page.server.js` and `static/sitemap.xml`. The legacy
`create-blog` scaffolder does not register a post; do not use it for new posts.
The static sitemap is authoritative; exclude gated and transient routes.

## Paid delivery and release

`docs/payment-reliability-rollout.md` is the rollout/runbook. Migration 017 must
precede the new payment code. Missing DB, email, or reviewed bundle configuration
is a retryable/unavailable condition, never a successful paid delivery.
The bundle path, book version, and SHA256 in deployment configuration must match
the generated bundle manifest after a remote-byte verification. Never default to
an old bundle. Production synthetic sessions cannot grant access.

`npm run check`, `npm run test:release`, `npm run build`, and
`npm run test:launch-browser` are release checks. The browser suite requires a
built site and installed Playwright browsers, intercepts writes, and does not
prove a live payment or inbox delivery. The disposable Postgres integration
suite is documented alongside the payment tests.

## Working conventions

Dark theme, Inter UI, JetBrains Mono labels, amber actions. Reuse existing styles
and accessible modal behavior. Keep third-party videos click-to-load.
Stage explicit paths and review the diff; other sessions may own dirty files.
Never commit secrets or customer records. Keep production migrations, storage
upload verification and test-mode purchase evidence separate from mocked tests.
Merging the release to main deploys production; do not treat a local build as
proof that hosting secrets, database changes or private storage are configured.
