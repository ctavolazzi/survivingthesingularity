# October 10 remaining-work backup

This closes gaps found after the October 8 and October 9 archives.

- [Standalone MVP](https://github.com/ctavolazzi/survivingthesingularity/tree/archive/sts-mvp-2026-07-30): all ten original commits, 38 current files, and 50 historical file versions. The historical demo and plan remain as written.
- [Committed website fixes](https://github.com/ctavolazzi/survivingthesingularity/tree/archive/site-fixes-2026-10-10): three commits preserving ten site-source changes and seven audit files.
- `snapshots/sts-site-fixes/`: 23 files covering self-hosted fonts, their licenses and fetcher, font integration and network auditing.
- `snapshots/sts-plain-claims/`: two files containing the current landing-page and offer-copy work.
- `historical-sql/`: an ignored historical Discord-application migration variant. Its provenance records the original location and hash; it has not been applied or substituted for the current migration.

`working-tree-snapshots.json` records each source branch, base commit, capture time, original file path, mode, size and SHA256. To restore a snapshot, make a separate checkout of its base commit, then copy that snapshot's files to their recorded original paths. The snapshots preserve work in progress and do not establish production readiness.

`coverage.json` records history and file coverage, verification and deliberate exclusions. Dependencies, credentials, runtime data, generated test reports and raster proof images are outside this source-and-deliverable backup. Original book editions and supporting artifacts remain in the [book archive](https://github.com/ctavolazzi/survivingthesingularity/releases/tag/book-archive-2026-10-08) and [supplement](https://github.com/ctavolazzi/survivingthesingularity/releases/tag/book-work-archive-2026-10-09).
