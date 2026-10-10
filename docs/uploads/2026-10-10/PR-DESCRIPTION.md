Local book editions and associated work were spread across branches, worktrees and export folders. This archive records their provenance and preserves recovered files and current work snapshots.

- [October 8 book archive](https://github.com/ctavolazzi/survivingthesingularity/releases/tag/book-archive-2026-10-08): 149 book artifacts.
- [October 9 supplement](https://github.com/ctavolazzi/survivingthesingularity/releases/tag/book-work-archive-2026-10-09): 147 recovered production, artwork, research and project files.
- [October 10 coverage](https://github.com/ctavolazzi/survivingthesingularity/tree/archive/book-files-2026-10-08/docs/uploads/2026-10-10): remaining local work, including font and video-loading changes, landing-page copy and an ignored historical schema variant.
- [Standalone MVP history](https://github.com/ctavolazzi/survivingthesingularity/tree/archive/sts-mvp-2026-07-30): ten original commits and 38 current files.
- [Committed site fixes and audit tools](https://github.com/ctavolazzi/survivingthesingularity/tree/archive/site-fixes-2026-10-10): three additional commits.

Verification includes original/staged/decompressed archive hashes, GitHub part digests, remote commit IDs, and source-to-snapshot hashes. Secret scans pass for the recovered history and new files. A wrong-hash control is rejected. Full public sample-part downloads timed out during October 9 verification; all metadata downloads and first/final sample byte ranges passed. Receipts retain those limits.

Work-in-progress snapshots carry their source branch, base commit, capture time, file modes and checksums. They are preserved as found and do not claim production readiness. Dependencies, credentials, runtime data, generated test reports and raster proof screenshots are excluded.

This PR adds archive records and copies of work under docs/uploads, plus two narrow secret-scan exclusions for verified Git commit IDs. It does not apply the archived website snapshots to application source. Merging to main uses the existing deployment workflow; merging remains a separate action.
