# Workboard: who is doing what on the novel, right now

Several Claude sessions work on this book at once: Claude Code on CT's desktop, Claude Duet on his
phone, and cloud sessions. Two of them started the same job on 22 November without knowing. This
page stops that.

**Before you start a task on the manuscript or its notes, read this page and claim the task. When
you finish or stop, say so here.** Times are Pacific.

If your chat cannot write to GitHub, use the block "Who is working on what" at the top of the Google
Doc "v4 scaffold" instead. It holds the same claims, and every session reads it. Whoever can write
here copies the claims across.

Where the files are: [`BRIDGE.md`](BRIDGE.md), or the Drive page "sts-bridge: read this first".

## Working now

Nobody, as of 12:55 on Nov 22. CT is reading the v4 scaffold, step by step.

## Next, when CT says go (in this order)

1. **CT reads the v4 scaffold.** Its top says how: Decided so far, Characters, Open questions, Fixes, the chapters, then Checks.
2. **CT settles the suggestions still open in Revised Manuscript v3**: Sparrow (Ch 7, Ch 19, Author's Note), Nadzieja Czekaj (Ch 3, Appendix), Bidwell's watcher (Meanwhiles 2 and 3), the machine's speech (Ch 38), and Duet's.
3. **Rulings CT still has to make**:
   - Chapter 9: is Nadzieja a ghost Elijah never meets?
   - The 800 miles between Ma and the co-op cannot fit in Northern California. Which place moves? v3 says "three hours" in Ch 15, 16, 22, 23, 29 and the Appendix.
   - Frank's profile cites "When I was his age we put a man on the moon" (Ch 25). It is not in v3. Add the line or drop the citation.
4. **Small edits into v3, once ruled**: Elijah's middle name Gaelen (v3 says Galen, twice); the "Fixes for the final version" list in the scaffold.
5. **The port.** Copy v3 in Drive to make "StS Final Draft v4" (a copy keeps the text, italics, 19 pictures and any open suggestions exactly). Rename the empty "StS Final Draft v4" placeholder to OLD. Compare the copy to v3 paragraph by paragraph. Make v3 read-only, and tell Duet to work in v4. Copy the Characters folder the same way. Then update `src/lib/data/novel/instances.json`, export `BRIDGE.md`, and remake the Drive bridge page.
6. **Amazon (KDP)**: a Kindle ebook needs no ISBN. A first book cannot be a pre-order with Thanksgiving as release day (the final file is due 5 days before), so publish directly; review takes up to 72 hours. Build the Kindle file from v4 once it holds the settled text, text only, and check it against the Doc.
7. **The website**: every Cloudflare deploy of `main` has failed since at least Nov 9. The likely cause is the hosted deployment gate (`scripts/check-hosted-deployment.mjs`), which stops the build until payment prerequisites are verified (see `docs/launch-readiness-2026-10-13/README.md`). Not confirmed: the Cloudflare log needs CT's login. The live site still serves an old version.

## Done today (Nov 22)

- **v4 scaffold**: created by Claude Code; "Decided so far" by Claude Code and Duet; "Open for v4" notes by Claude Code; every chapter, a profile for every character, open questions and fixes filled by Duet (about 12:00 to 12:45); checked by Claude Code (Checks section, 3 passes). Duet also fixed its own heading styles.
- **The bridge**: `BRIDGE.md`, `scripts/sts-bridge.mjs` (status, check, where, edit, suggestions, verify, export), the Drive page, and this workboard. Merged to main.
- **v3**: many edits by Duet (Crop Dust, the Fishman amp, Linda Madrone and Joan Hollis, Devendra stays in San Jose, March 2025, Lou and Bidwell are cousins); suggestions by Claude Code (Sparrow, Nadzieja, Bidwell's watcher, the machine's speech).
- **Notes in Drive**: the Ma dossier (800 miles), the Architect's dossier (her name, CT's direction), the machine's dossier (a full bio).
- **Draft compendium** in the private reader at `/novel/<key>/compendium`: six sample entries, now out of date (it still says Second Crop and the Fisher).

## How to claim

Add a row under "Working now" before you start: the task, who you are, the time, "In progress". Name
the exact chapters or files. If a row already covers what you want to do, do something else or ask CT.
When you stop, move the row to "Done" with one line on what you finished and what you left.
