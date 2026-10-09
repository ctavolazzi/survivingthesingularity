# R2 move plan for the book downloads

**Status: PLAN ONLY.** Nothing here is executed. Written 2026-08-04 against the
v0.7.5.1 open cycle; re-measure before acting on any number in it.

## Why move

Cloudflare Pages has a hard 25 MiB per-asset ceiling, enforced at deploy.
Measured today in `static/downloads/`:

| File | Size | Headroom |
|---|---|---|
| Surviving-the-Singularity-v0.7.5.pdf | 22.38 MiB | 2.62 MiB |
| Surviving-the-Singularity-v0.7.5.epub | 21.14 MiB | 3.86 MiB |
| Surviving-the-Singularity-v0.7.4.pdf | 22.34 MiB | carried for old links |
| Surviving-the-Singularity-v0.7.4.epub | 21.12 MiB | carried for old links |

`scripts/check-book-downloads.mjs` already warns at the near-ceiling threshold
and names the fix: an illustrated version will not fit under 25 MiB, and the
deploy simply fails on the day that happens. A second pressure is accumulation:
the branch deliberately carries prior versions so shared links keep working
(cce91d4), which adds roughly 45 MiB of Pages assets per kept version.

R2 has no per-object ceiling at these sizes and charges nothing for egress, so
the cost of serving the book from it is storage pennies.

## Target shape

- One R2 bucket (suggested name: `sts-downloads`) with a custom domain,
  suggested `dl.survivingthesingularity.com`, public read.
- Objects keep the exact filenames `bookManifest.js` derives
  (`Surviving-the-Singularity-vX.Y.Z.pdf` / `.epub`), so the one-filename-rule
  stays in `src/lib/bookManifest.js` and nowhere else.
- Stable aliases stay on the site as redirects: `/downloads/...` paths in
  `static/_redirects` can point at absolute URLs, so every link already in an
  inbox keeps resolving through the same door.
- The Municipal Autonomy Code PDF (50 KB) and covers stay on Pages; only the
  two book artifacts move. The preorder bundle zip lives in Supabase Storage
  and is explicitly OUT of this plan's scope.

## Repo changes, in dependency order

1. `scripts/publish-book-downloads.mjs`: after the local copy, add the upload
   step (`wrangler r2 object put sts-downloads/<name> --file book-build/<name>`),
   then fetch the object back through the public domain and compare sha256 to
   the local build. Publishing stays an explicit gesture at version close.
2. `scripts/check-book-downloads.mjs`: assert the remote objects exist and
   hash-match for the current version (HEAD + ranged GET is enough), instead of
   asserting the files sit in `static/downloads/`. Keep generating
   `static/_redirects`, now targeting `https://dl.../<versioned name>`.
3. `src/lib/bookManifest.js`: `downloadHref` returns the R2 URL. Every consumer
   (/book, /exclusive-friends-only, the preorder email) already derives from it,
   so this is the single flip.
4. Remove the four book files from `static/downloads/` only AFTER one full
   deploy has served the R2 hrefs and the redirects have been probed live.
   History keeps the blobs; nothing is lost.

## Rollout order, each step verified before the next

1. CT creates the bucket + custom domain (dashboard or `wrangler r2 bucket
   create`), and authorizes wrangler locally. The Cloudflare MCP connectors in
   this harness are unauthenticated, so this step is CT's.
2. Upload v0.7.5 pair and v0.7.4 pair beside the Pages copies. Verify by
   downloading both through the public domain and hash-comparing.
3. Land repo changes 1 to 3 on the branch; `npm run book:release` green.
4. Probe preview deploy: stable aliases 302 to R2, versioned paths resolve,
   old-version paths behave as decided in the open question below.
5. After the held merge ships and production serves R2 hrefs, remove the book
   files from `static/downloads/` (change 4) in its own commit.

## Open questions for CT

- Subdomain choice (`dl.` suggested), and bucket name.
- Do retired versions stay downloadable from R2 forever, or redirect to the
  current file the way `_redirects` does today? Keeping them costs ~45 MiB of
  storage per version and honors "the previous file is what past customers
  received"; redirecting matches current site behavior.
- Timing relative to the held merge to main: the flip (change 3) is
  buyer-facing, so it should ride the same merge discipline as everything else.

## What this plan deliberately does not do

- No compression pass on the book. The check's own comment says the fix is the
  move, not shrinking the artifact.
- No change to the Supabase bundle pipeline (`sts.py bundle ...`).
- No execution: no bucket exists, no object is uploaded, no href is flipped.
