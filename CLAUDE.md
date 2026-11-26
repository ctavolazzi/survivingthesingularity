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

## The novel in progress

The next version of the book is a novel. It is not the text in `src/lib/data/book/`.
**Start with the bridge: read `manuscript/novel/BRIDGE.md`.** It says which copy is the book right
now, lists every other copy, and gives the one way to change the manuscript. In short:

- The manuscript is a Google Doc, and it moves between Docs. Do not assume which one from memory
  or from an older note. `node scripts/sts-bridge.mjs status` marks exactly one copy CURRENT.
- To change the manuscript: read the current Doc fresh with the Docs connector, then
  `node scripts/sts-bridge.mjs edit READ.json --find "old words" --replace "new words"`. It checks
  that the passage appears exactly once and prints the request to send. Changes go in as
  suggestions the author accepts or rejects. A direct edit needs his say-so each time.
- `node scripts/sts-bridge.mjs suggestions READ.json` lists what is waiting on him.
- When a copy is made or the current one changes, update `src/lib/data/novel/instances.json`,
  run `node scripts/sts-bridge.mjs export md > manuscript/novel/BRIDGE.md`, and remake the bridge
  page in Google Drive ("sts-bridge: read this first"), which chats without code read.
- `manuscript/novel/README.md` and `manuscript/tools/book.py` describe the method of 19 November,
  when the manuscript was "FINAL StS Manuscript". The repository copy made then is behind.
- Each character has a folder in `manuscript/novel/characters/` and a notes file in Drive.
- Pushing to `main` redeploys the live site. Merge the book into `main` only when he says.

### Finishing the novel (from 26 November)

Three files run the endgame: `manuscript/novel/REFERENCE.md` (how: reading order, policies, procedures, tools),
`manuscript/novel/GOALS.md` (what done is) and `manuscript/novel/TODO.md` (what is next, with the next edit number).
Start a session at `REFERENCE.md`, section 1.

### Writing a line for the novel (the author's corrections, 26 November)

**Before writing any line for the book, read `manuscript/novel/WRITING-INSTRUCTIONS.md`, all of it.** It is the full
set of the author's writing rules, his own voice with examples, each character's speech, and a checklist to run
before a chapter is logged. Chapters 20 to 36 are being rewritten to `manuscript/novel/PLAN-CHAPTERS-20-TO-36.md`.
The history of each correction is in "Writing a beat for CT" in `manuscript/novel/EDIT-LOGGING-PROCEDURE.md`. In short:

- Search the current text for the key word and its cousins first, so the new line doesn't repeat a phrase the
  book already has.
- Show the thing in two or three small steps. One flat statement reads dry; a pile of detail is too much.
- One beat. Don't explain why it matters.
- Write the action plainly and leave the sentence that names the feeling to the author.
- Offer one version, sized in the middle. If he says it's dry, add one step, not five.
- No mirrored contrast lines: "It's not X. It's Y.", "They can. They just won't.", "He's on this side of the fence.
  His friends aren't." CT called the shape AI-sounding (edits 119 and 174) and, 26 Nov: "We've already established that
  we can do better than this." People talk in their own trade and habits, half-finished, concrete, sometimes wrong; a
  line that sounds built to be quoted is the wrong line.
- No beat-counting: "He read it twice. Then he wrote back." (CT: "Don't do the pattern.") Go straight to the action.
- The middle path: quips, a dry closing line or an inversion are welcome where they add levity or read literary, never
  where they cheapen a heavy moment, and never as a trick to vary openings (CT: "Find the middle path").
- Unpack a clever line into the plain thing it means. Written messages are italic. Flag every fact you invent.
- When he corrects a line, add what was learned to `WRITING-INSTRUCTIONS.md` in the same turn.

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

`npm run check`, `npm run test:release`, `npm run build`, `npm run test:cloudflare`,
and `npm run test:launch-browser` are release checks. The browser suite requires a
built site and installed Playwright browsers, intercepts writes, and does not
prove a live payment or inbox delivery. The disposable Postgres integration
suite is documented alongside the payment tests.

Cloudflare uses the pinned adapter and dashboard-managed production settings.
Do not add an automatically discovered root Wrangler configuration without
importing the existing dashboard settings: it takes over environment variables.
`tests/fixtures/cloudflare-runtime.json` is only for isolated local emulation.
`_headers` and the generated `_redirects` belong at the repository root. The local Worker guard
isolates credentials, verifies all canonical chapter loads and checks static
routing; it does not deploy. Markdown sanitization must work without a DOM.

## Working conventions

Dark theme, Inter UI, JetBrains Mono labels, amber actions. Reuse existing styles
and accessible modal behavior. Keep third-party videos click-to-load.
Stage explicit paths and review the diff; other sessions may own dirty files.
Never commit secrets or customer records. Keep production migrations, storage
upload verification and test-mode purchase evidence separate from mocked tests.
Merging the release to main deploys production; do not treat a local build as
proof that hosting secrets, database changes or private storage are configured.
