# work_efforts/ — RETIRED 2026-08-02

This directory is a **retired tracker**. Nothing in it is active. Do not open a
new work effort here.

It ran from roughly 2024-12 to 2025-07 under a Johnny Decimal scheme. The project
was rebuilt out from under it: by 2026-08 the site, the component tree, the
checkout flow and the content architecture had all been replaced, and the tracker
was left describing a codebase that no longer existed. Six items still read
"In Progress" or "Not Started" while naming files that had been deleted months
earlier.

It is kept in place, not deleted, because the closeout notes record why each line
of work stopped. That is worth more than a clean directory listing.

## Where the work actually lives now

| Concern | Current home |
| --- | --- |
| Release planning | `V0.7.4-SCOPE.md`, `V0.7.5-SCOPE.md`, `RELEASES.md` |
| Project state | `sts.py status`, `sts.py audit` |
| Build gates | `.github/workflows/build-guard.yml`, the three `check:*` npm scripts |
| Test coverage | `tests/e2e/` (14 specs), 4 GitHub workflows |
| Book content | `src/lib/data/book/`, single source of truth, see `README.md` |
| Provenance | `sts.py factcheck`, `/factcheck`, see `FACTCHECK.md` |
| Payments | `STRIPE-GO-LIVE.md` |

## Closeout status of every work effort

Verified against the tree on 2026-08-02, not against the previous session's
claims.

| Work effort | Prior status | Closed as |
| --- | --- | --- |
| `00.02_finish_line_roadmap` | In Progress | Overtaken by events |
| `00.03_comprehensive_site_review` | In Progress | **Completed** |
| `20.01_content_audit_migration` | Not Started | Superseded |
| `40.02_build_pipeline_verification` | Not Started | Superseded |
| `50.01_svelte_warnings_cleanup_migration` | In Progress (80%) | Obsolete |
| `50.02_work_efforts_migration` | In Progress | Abandoned |
| `00.01`, `00.04`, `00.05`, `20.05`, `16`, `17` | Completed | unchanged |

Only one item had real work left in it. `00.03` asked for three deletions on
privacy grounds; two had already happened, and the third,
`src/lib/utils/hookEm.js`, was deleted during this closeout. It had decayed to a
3 line `console.log` stub with zero importers, so the original privacy concern
had no live surface by then.

"Superseded" and "Obsolete" are not "Completed". Nothing here was marked done
that was not verifiably done.

## WARNING: this directory contains production code

`12_image_optimization_enhancements/` is **not a work effort**. It holds no
document at all. It holds `image_build_hook.js`, which `package.json` calls from
both `prebuild` and `optimize-images`.

**Deleting or moving this directory will break every build.**

It is the one thing here that is not safe to treat as an archive.

## Open follow-ups that outlive this tracker

These are live repo issues surfaced by the closeout. They are recorded here
because they have no other home yet, not because they belong to a retired
tracker.

1. **Relocate `image_build_hook.js` to `scripts/`.** Production code should not
   live in a retired tracker. Requires updating the two `package.json` script
   paths in the same change. Deferred on 2026-08-02 because a parallel session
   had 153 uncommitted lines in that file (a content-hash build cache) and moving
   it would have collided with live work. Do this once that lands.

2. **`npm run check` is broken and has never run.** The script is
   `svelte-kit sync && svelte-check --tsconfig ./jsconfig.json`, but
   `svelte-check` is absent from `devDependencies` and absent from
   `node_modules`. It fails with `sh: svelte-check: command not found`. This was
   `50.01`'s acceptance gate, which is the likely reason that work effort stalled
   at "80%" for over a year. Either add the dependency or drop the script, but do
   not leave a success criterion that cannot be executed.

3. **`[[../SITEMAP]]` resolves to the wrong depth** in all 10 category index
   files. `SITEMAP.md` is at the repo root, so from `work_efforts/XX_category/`
   the correct link is `[[../../SITEMAP]]`. Cosmetic, affects Obsidian browsing
   only. Left unfixed as out of proportion to the value.

4. **`BookCoverModal.svelte` has zero importers.** Flagged during the `00.03`
   review, deliberately not deleted, since it may be held on purpose. Confirm
   intent before removing.

## Dangling links, on purpose

`50.02` still contains wikilinks to five work efforts that were never created
(`00.01`, `10.01`, `20.03`, `20.04`, `40.01`). They are left intact as the record
of an abandoned migration plan, and its closeout note says plainly that none of
the targets exist. Elsewhere those references were demoted to plain text so they
stop reading as live links.
