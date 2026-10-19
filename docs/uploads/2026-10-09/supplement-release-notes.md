This supplement preserves **147 files** found during the October 9 coverage audit: print-production and diagnostic PDFs, bonus research packages, original text exports, artwork and composition sources, supporting research drafts, and the pixel-video and production-tracker projects.

It adds to the [October 8 book archive](https://github.com/ctavolazzi/survivingthesingularity/releases/tag/book-archive-2026-10-08), which preserves 149 book artifacts. These additional files include production intermediates and project work, so the file count does not represent new numbered editions.

The supplement is **123,741,800 bytes compressed**, containing **380,405,614 bytes** across 147 paths. All original, staged and decompressed files were checked by size and SHA256. [supplement-inventory.json](https://github.com/ctavolazzi/survivingthesingularity/releases/download/book-work-archive-2026-10-09/supplement-inventory.json) records every file, original location and classification.

Download [download-supplement.py](https://github.com/ctavolazzi/survivingthesingularity/releases/download/book-work-archive-2026-10-09/download-supplement.py) and [supplement-transport.json](https://github.com/ctavolazzi/survivingthesingularity/releases/download/book-work-archive-2026-10-09/supplement-transport.json) into the same folder. Python 3.9 or later downloads and verifies all 30 parts, resumes valid saved parts, then checks the combined archive:

```sh
python3 download-supplement.py --manifest supplement-transport.json
```

Use the file path printed after `Verified archive:` when extracting. If an existing file did not match, the downloader preserves it and may choose a different filename for the verified archive. Extraction requires zstd with its 512 MiB window enabled:

```sh
mkdir -p extracted
zstd --long=29 -dc sts-book-work-supplement-2026-10-09/Surviving-the-Singularity-supplement-2026-10-09.tar.zst | tar -xf - -C extracted
cd extracted
sha256sum -c SHA256SUMS
```

On macOS, use `shasum -a 256 -c SHA256SUMS` for the last command. Parts must be combined in the manifest's order and exact filenames; the downloader handles this automatically.

Combined archive SHA256:

```text
db1da47195f82bec1f7fd3ca1ceb5d7db17568fe4f38cf99a49480c50dd6ccaa
```

The standalone projects retain their selected directory structure under `projects/`. Other recovered files retain their original relative paths under `files/`. The archive also contains `manifest.json` and `SHA256SUMS`.

Dependencies, session databases, caches and individually generated video frames are excluded; project source and final video exports are preserved. Research drafts retain their recorded status and do not become fact-checked book content through archival inclusion.

[October 9 coverage records and recent-work snapshots](https://github.com/ctavolazzi/survivingthesingularity/tree/archive/book-files-2026-10-08/docs/uploads/2026-10-09) document the audit, current source coverage, research clarification and captured website work. The historical [August 2 snapshot](https://github.com/ctavolazzi/survivingthesingularity/tree/snapshot/2026-08-02-spinup) is also preserved on GitHub.
