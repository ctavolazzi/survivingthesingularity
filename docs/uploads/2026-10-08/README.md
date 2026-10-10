# Book archive: 2026-10-08

**Status: complete.** All 91 remote parts and required source branches have been verified.

[Archive release](https://github.com/ctavolazzi/survivingthesingularity/releases/tag/book-archive-2026-10-08) preserves **149 distinct files** recovered from 505 local copies: **34 numbered edition labels, eight legacy draft labels and four dated manuscript snapshots**. The complete download is **379 MB compressed** (379,175,616 bytes), containing **3.04 GB of book files** (3,041,969,876 bytes). Identical bytes are stored once; different builds remain separate.

## Download and extract

The archive is transported as **91 parts**, each **4 MiB** except the final part. Use [download-archive.py](https://github.com/ctavolazzi/survivingthesingularity/releases/download/book-archive-2026-10-08/download-archive.py) with [archive-transport.json](https://github.com/ctavolazzi/survivingthesingularity/releases/download/book-archive-2026-10-08/archive-transport.json). Python 3.9 or later downloads the exact filenames in manifest order, checks every part, resumes valid saved parts, then verifies the combined archive. Installing zstd is required for extraction.

Save the downloader and manifest in the same folder, then run:

```sh
python3 download-archive.py --manifest archive-transport.json
```

This creates `sts-book-archive-2026-10-08/Surviving-the-Singularity-all-editions-2026-10-08.tar.zst`. Rerun the command after an interrupted download. Valid completed parts are reused. Files whose bytes do not match are preserved, and verified replacements receive a different filename. If the path printed after `Verified archive:` differs from the default below, use that printed path in the extraction command.

The downloader combines parts in the manifest's listed order. Retry uploads can have different names, so wildcard concatenation is unsuitable.

After the downloader reports a verified archive, extract and check the recovered files:

```sh
mkdir -p extracted
zstd --long=29 -dc sts-book-archive-2026-10-08/Surviving-the-Singularity-all-editions-2026-10-08.tar.zst | tar -xf - -C extracted
cd extracted
sha256sum -c SHA256SUMS
```

On macOS, use `shasum -a 256 -c SHA256SUMS` for the final command. The archive requires zstd's `--long=29` decoder option, which allows its 512 MiB window. Extraction includes the portable `manifest.json` and `SHA256SUMS` alongside the edition folders.

Combined archive SHA256:

```text
8812195af8cdfde5c776222bd0869cd61a8dd486bdd403d6eb8b594ecc1977ce
```

[book-catalog.json](https://github.com/ctavolazzi/survivingthesingularity/releases/download/book-archive-2026-10-08/book-catalog.json) records each file's archive path, original locations, byte count and SHA256. The catalog below lists files inside the archive. Earlier release attachments named `individual-upload-plan.md`, `individual-upload-plan.json` and `SHA256SUMS.txt` describe the original individual-file upload plan. Use `ARCHIVE-INDEX.md`, the transport manifest and `book-catalog.json` for the complete archive download.

## Source and recent work

Newest edition is v0.11.0. Its PDF, EPUB, print interior, cover, Markdown and editable package match the finalized delivery manifest. All 36 finalized delivery records for v0.10.0 through v0.11.0 match the recovered files. Older files are preserved as recovered without applying current production review claims to them.

[Source provenance](https://github.com/ctavolazzi/survivingthesingularity/releases/download/book-archive-2026-10-08/SOURCE-PROVENANCE.md) identifies known commits, reissued early drafts and unresolved version metadata. The archive tag anchors this inventory; each edition's source has its own history. `book-v0.9.3` carries the v0.9.2 commit and manifest, and no separate v0.9.3 artifact was recovered.

Recent manuscript, artwork, landing-page, editorial-note and proof work is preserved on [book-v0.10.0](https://github.com/ctavolazzi/survivingthesingularity/tree/book-v0.10.0) through [book-v0.11.0](https://github.com/ctavolazzi/survivingthesingularity/tree/book-v0.11.0). [Recent-work provenance](https://github.com/ctavolazzi/survivingthesingularity/releases/download/book-archive-2026-10-08/recent-work.json) and [game preview patch](https://github.com/ctavolazzi/survivingthesingularity/releases/download/book-archive-2026-10-08/game-preview-work.patch) record the separate game-preview snapshot and its limits.

This archival prerelease retains v0.7.5 as the existing latest release. Website publication and main remain separate from this archive.

## File catalog

Paths below are relative to the extraction folder. The folders distinguish edition labels and snapshots; variant names preserve proof renders, converted interiors and alternative builds.

### 0.0.1: 1 file

| Extracted file | Bytes |
|---|---:|
| `book-v0.0.1/StS-Complete-Draft-v0.0.1.md` | 164,807 |

### 0.0.3: 1 file

| Extracted file | Bytes |
|---|---:|
| `book-v0.0.3/StS-Complete-Draft-v0.0.3.md` | 290,157 |

### 0.0.5: 1 file

| Extracted file | Bytes |
|---|---:|
| `book-v0.0.5/StS-Complete-Draft-v0.0.5.md` | 309,847 |

### 0.0.6: 1 file

| Extracted file | Bytes |
|---|---:|
| `book-v0.0.6/StS-Complete-Draft-v0.0.6.md` | 316,304 |

### 0.0.7: 1 file

| Extracted file | Bytes |
|---|---:|
| `book-v0.0.7/StS-Complete-Draft-v0.0.7.md` | 492,838 |

### 0.0.8: 1 file

| Extracted file | Bytes |
|---|---:|
| `book-v0.0.8/StS-Complete-Draft-v0.0.8.md` | 521,344 |

### 0.0.9: 1 file

| Extracted file | Bytes |
|---|---:|
| `book-v0.0.9/StS-Complete-Draft-v0.0.9.md` | 530,602 |

### 0.2: 1 file

| Extracted file | Bytes |
|---|---:|
| `book-v0.2/Surviving-the-Singularity-Book-Draft-v0.2.pdf` | 250,724 |

### 0.3.0: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.3.0/Surviving-the-Singularity-v0.3.0.epub` | 16,483,456 |
| `book-v0.3.0/Surviving-the-Singularity-v0.3.0.pdf` | 16,845,507 |

### 0.3.1: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.3.1/Surviving-the-Singularity-v0.3.1.epub` | 16,483,533 |
| `book-v0.3.1/Surviving-the-Singularity-v0.3.1.pdf` | 16,845,482 |

### 0.5.0: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.5.0/Surviving-the-Singularity-v0.5.0.epub` | 16,537,578 |
| `book-v0.5.0/Surviving-the-Singularity-v0.5.0.pdf` | 17,212,205 |

### 0.5.1: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.5.1/Surviving-the-Singularity-v0.5.1.epub` | 16,538,268 |
| `book-v0.5.1/Surviving-the-Singularity-v0.5.1.pdf` | 17,259,480 |

### 0.5.2: 4 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.5.2/Surviving-the-Singularity-v0.5.2.epub` | 16,538,279 |
| `book-v0.5.2/Surviving-the-Singularity-v0.5.2-DELUXE.pdf` | 17,403,840 |
| `book-v0.5.2/Surviving-the-Singularity-v0.5.2.pdf` | 17,259,628 |
| `book-v0.5.2/Surviving-the-Singularity-v0.5.2-PLAIN.pdf` | 2,101,979 |

### 0.6.0: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.6.0/Surviving-the-Singularity-v0.6.0.epub` | 16,540,721 |
| `book-v0.6.0/Surviving-the-Singularity-v0.6.0.pdf` | 17,264,860 |

### 0.6.1: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.6.1/Surviving-the-Singularity-v0.6.1.epub` | 16,541,527 |
| `book-v0.6.1/Surviving-the-Singularity-v0.6.1.pdf` | 17,266,588 |

### 0.6.2: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.6.2/Surviving-the-Singularity-v0.6.2.epub` | 16,541,523 |
| `book-v0.6.2/Surviving-the-Singularity-v0.6.2.pdf` | 17,266,581 |

### 0.7.0: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.7.0/Surviving-the-Singularity-v0.7.0.epub` | 16,738,744 |
| `book-v0.7.0/Surviving-the-Singularity-v0.7.0.pdf` | 17,503,684 |

### 0.7.1: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.7.1/Surviving-the-Singularity-v0.7.1.epub` | 20,664,297 |
| `book-v0.7.1/Surviving-the-Singularity-v0.7.1.pdf` | 21,921,376 |

### 0.7.2: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.7.2/Surviving-the-Singularity-v0.7.2.epub` | 20,664,299 |
| `book-v0.7.2/Surviving-the-Singularity-v0.7.2.pdf` | 21,921,406 |

### 0.7.3: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.7.3/Surviving-the-Singularity-v0.7.3.epub` | 20,670,710 |
| `book-v0.7.3/Surviving-the-Singularity-v0.7.3.pdf` | 21,936,863 |

### 0.7.4: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.7.4/Surviving-the-Singularity-v0.7.4.epub` | 22,142,881 |
| `book-v0.7.4/Surviving-the-Singularity-v0.7.4.pdf` | 23,428,861 |

### 0.7.5: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.7.5/Surviving-the-Singularity-v0.7.5.epub` | 22,170,885 |
| `book-v0.7.5/Surviving-the-Singularity-v0.7.5.pdf` | 23,463,333 |

### 0.8.0: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.8.0/Surviving-the-Singularity-v0.8.0-render-input-markdown.md` | 268,091 |
| `book-v0.8.0/Surviving-the-Singularity-v0.8.0.pdf` | 19,520,687 |

### 0.8.1: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.8.1/Surviving-the-Singularity-v0.8.1-render-input-markdown.md` | 312,215 |
| `book-v0.8.1/Surviving-the-Singularity-v0.8.1.pdf` | 19,473,938 |

### 0.8.2: 16 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-editable-package-editable_package.zip` | 48,288,286 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-proof-01-front-cover.pdf` | 253,611 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-proof-02-front-cover.pdf` | 312,390 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-publication-render-front-cover.pdf` | 312,390 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-proof-01-interior.pdf` | 13,622,666 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-proof-02-interior.pdf` | 13,748,923 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-proof-04-interior.pdf` | 13,167,164 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-proof-final-interior.pdf` | 13,157,801 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-publication-render-interior.pdf` | 13,157,810 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-render-input-markdown.md` | 371,694 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-print-converted-print-interior.pdf` | 7,572,104 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-publication-render-print-interior.pdf` | 7,718,646 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2.pdf` | 19,534,748 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-proof-01-reading.pdf` | 13,624,380 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-proof-02-reading.pdf` | 14,294,870 |
| `book-v0.8.2/Surviving-the-Singularity-v0.8.2-publication-render-reading.pdf` | 13,696,456 |

### 0.9.0: 2 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.9.0/Surviving-the-Singularity-v0.9.0-render-input-markdown.md` | 520,333 |
| `book-v0.9.0/Surviving-the-Singularity-v0.9.0.pdf` | 23,181,879 |

### 0.9.1: 7 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.9.1/Surviving-the-Singularity-v0.9.1-publication-render-front-cover.pdf` | 4,060,296 |
| `book-v0.9.1/Surviving-the-Singularity-v0.9.1-publication-render-interior.pdf` | 17,245,139 |
| `book-v0.9.1/Surviving-the-Singularity-v0.9.1-render-input-markdown.md` | 526,786 |
| `book-v0.9.1/Surviving-the-Singularity-v0.9.1-print-converted-print-interior.pdf` | 182,465,932 |
| `book-v0.9.1/Surviving-the-Singularity-v0.9.1-publication-render-print-interior.pdf` | 189,751,386 |
| `book-v0.9.1/Surviving-the-Singularity-v0.9.1.pdf` | 21,805,199 |
| `book-v0.9.1/Surviving-the-Singularity-v0.9.1-publication-render-reading.pdf` | 21,713,709 |

### 0.9.2: 9 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.9.2/Surviving-the-Singularity-v0.9.2.epub` | 22,174,451 |
| `book-v0.9.2/Surviving-the-Singularity-v0.9.2-publication-render-front-cover.pdf` | 4,060,296 |
| `book-v0.9.2/Surviving-the-Singularity-v0.9.2-publication-render-interior.pdf` | 16,000,914 |
| `book-v0.9.2/Surviving-the-Singularity-v0.9.2-render-input-markdown.md` | 598,116 |
| `book-v0.9.2/Surviving-the-Singularity-v0.9.2-print-converted-print-interior.pdf` | 9,978,633 |
| `book-v0.9.2/Surviving-the-Singularity-v0.9.2-publication-render-print-interior.pdf` | 10,241,756 |
| `book-v0.9.2/Surviving-the-Singularity-v0.9.2.pdf` | 21,954,266 |
| `book-v0.9.2/Surviving-the-Singularity-v0.9.2-epub-review.pdf` | 21,983,027 |
| `book-v0.9.2/Surviving-the-Singularity-v0.9.2-publication-render-reading.pdf` | 20,495,169 |

### 0.10.0: 10 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.10.0/Surviving-the-Singularity-v0.10.0-final-delivery-editable_package.zip` | 70,553,120 |
| `book-v0.10.0/Surviving-the-Singularity-v0.10.0.epub` | 19,205,713 |
| `book-v0.10.0/Surviving-the-Singularity-v0.10.0-front-cover.pdf` | 4,060,296 |
| `book-v0.10.0/Surviving-the-Singularity-v0.10.0-publication-render-interior.pdf` | 16,063,228 |
| `book-v0.10.0/Surviving-the-Singularity-v0.10.0.md` | 606,253 |
| `book-v0.10.0/Surviving-the-Singularity-v0.10.0-render-input-markdown.md` | 608,834 |
| `book-v0.10.0/Surviving-the-Singularity-v0.10.0-print-interior.pdf` | 10,296,924 |
| `book-v0.10.0/Surviving-the-Singularity-v0.10.0-print-converted-print-interior.pdf` | 10,019,985 |
| `book-v0.10.0/Surviving-the-Singularity-v0.10.0-before-visual-corrections.pdf` | 20,589,237 |
| `book-v0.10.0/Surviving-the-Singularity-v0.10.0.pdf` | 20,575,004 |

### 0.10.1: 9 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.10.1/Surviving-the-Singularity-v0.10.1-final-delivery-editable_package.zip` | 105,099,274 |
| `book-v0.10.1/Surviving-the-Singularity-v0.10.1.epub` | 30,215,141 |
| `book-v0.10.1/Surviving-the-Singularity-v0.10.1-front-cover.pdf` | 4,060,298 |
| `book-v0.10.1/Surviving-the-Singularity-v0.10.1-publication-render-interior.pdf` | 27,185,491 |
| `book-v0.10.1/Surviving-the-Singularity-v0.10.1.md` | 619,073 |
| `book-v0.10.1/Surviving-the-Singularity-v0.10.1-render-input-markdown.md` | 623,243 |
| `book-v0.10.1/Surviving-the-Singularity-v0.10.1-print-interior.pdf` | 11,808,561 |
| `book-v0.10.1/Surviving-the-Singularity-v0.10.1-print-converted-print-interior.pdf` | 11,506,851 |
| `book-v0.10.1/Surviving-the-Singularity-v0.10.1.pdf` | 31,792,078 |

### 0.10.2: 9 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.10.2/Surviving-the-Singularity-v0.10.2-final-delivery-editable_package.zip` | 104,956,555 |
| `book-v0.10.2/Surviving-the-Singularity-v0.10.2.epub` | 30,220,678 |
| `book-v0.10.2/Surviving-the-Singularity-v0.10.2-front-cover.pdf` | 4,060,297 |
| `book-v0.10.2/Surviving-the-Singularity-v0.10.2-publication-render-interior.pdf` | 27,065,790 |
| `book-v0.10.2/Surviving-the-Singularity-v0.10.2.md` | 637,063 |
| `book-v0.10.2/Surviving-the-Singularity-v0.10.2-render-input-markdown.md` | 641,233 |
| `book-v0.10.2/Surviving-the-Singularity-v0.10.2-print-interior.pdf` | 11,723,058 |
| `book-v0.10.2/Surviving-the-Singularity-v0.10.2-print-converted-print-interior.pdf` | 11,414,416 |
| `book-v0.10.2/Surviving-the-Singularity-v0.10.2.pdf` | 31,637,921 |

### 0.10.3: 9 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.10.3/Surviving-the-Singularity-v0.10.3-final-delivery-editable_package.zip` | 139,030,172 |
| `book-v0.10.3/Surviving-the-Singularity-v0.10.3.epub` | 41,851,429 |
| `book-v0.10.3/Surviving-the-Singularity-v0.10.3-front-cover.pdf` | 4,060,299 |
| `book-v0.10.3/Surviving-the-Singularity-v0.10.3-publication-render-interior.pdf` | 37,940,249 |
| `book-v0.10.3/Surviving-the-Singularity-v0.10.3.md` | 639,481 |
| `book-v0.10.3/Surviving-the-Singularity-v0.10.3-render-input-markdown.md` | 644,115 |
| `book-v0.10.3/Surviving-the-Singularity-v0.10.3-print-interior.pdf` | 12,407,539 |
| `book-v0.10.3/Surviving-the-Singularity-v0.10.3-print-converted-print-interior.pdf` | 12,098,835 |
| `book-v0.10.3/Surviving-the-Singularity-v0.10.3.pdf` | 42,514,070 |

### 0.10.4: 9 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.10.4/Surviving-the-Singularity-v0.10.4-final-delivery-editable_package.zip` | 139,033,750 |
| `book-v0.10.4/Surviving-the-Singularity-v0.10.4.epub` | 41,851,412 |
| `book-v0.10.4/Surviving-the-Singularity-v0.10.4-front-cover.pdf` | 4,060,297 |
| `book-v0.10.4/Surviving-the-Singularity-v0.10.4-publication-render-interior.pdf` | 37,940,997 |
| `book-v0.10.4/Surviving-the-Singularity-v0.10.4.md` | 639,376 |
| `book-v0.10.4/Surviving-the-Singularity-v0.10.4-render-input-markdown.md` | 644,010 |
| `book-v0.10.4/Surviving-the-Singularity-v0.10.4-print-interior.pdf` | 12,409,143 |
| `book-v0.10.4/Surviving-the-Singularity-v0.10.4-print-converted-print-interior.pdf` | 12,100,204 |
| `book-v0.10.4/Surviving-the-Singularity-v0.10.4.pdf` | 42,515,518 |

### 0.11.0: 9 files

| Extracted file | Bytes |
|---|---:|
| `book-v0.11.0/Surviving-the-Singularity-v0.11.0-final-delivery-editable_package.zip` | 139,095,688 |
| `book-v0.11.0/Surviving-the-Singularity-v0.11.0.epub` | 41,855,461 |
| `book-v0.11.0/Surviving-the-Singularity-v0.11.0-front-cover.pdf` | 4,060,296 |
| `book-v0.11.0/Surviving-the-Singularity-v0.11.0-publication-render-interior.pdf` | 37,956,936 |
| `book-v0.11.0/Surviving-the-Singularity-v0.11.0.md` | 649,044 |
| `book-v0.11.0/Surviving-the-Singularity-v0.11.0-render-input-markdown.md` | 653,678 |
| `book-v0.11.0/Surviving-the-Singularity-v0.11.0-print-interior.pdf` | 12,432,892 |
| `book-v0.11.0/Surviving-the-Singularity-v0.11.0-print-converted-print-interior.pdf` | 12,118,062 |
| `book-v0.11.0/Surviving-the-Singularity-v0.11.0.pdf` | 42,538,010 |

### legacy-5.4: 2 files

| Extracted file | Bytes |
|---|---:|
| `legacy-5.4/Surviving-the-Singularity-5.4.epub` | 16,394,293 |
| `legacy-5.4/Surviving-the-Singularity-5.4.pdf` | 16,639,100 |

### legacy-5.5: 2 files

| Extracted file | Bytes |
|---|---:|
| `legacy-5.5/Surviving-the-Singularity-5.5.epub` | 16,402,829 |
| `legacy-5.5/Surviving-the-Singularity-5.5.pdf` | 16,658,207 |

### legacy-DRAFT: 2 files

| Extracted file | Bytes |
|---|---:|
| `legacy-DRAFT/Surviving-the-Singularity-DRAFT.epub` | 16,483,529 |
| `legacy-DRAFT/Surviving-the-Singularity-DRAFT.pdf` | 16,845,482 |

### legacy-DRAFT_5.2: 2 files

| Extracted file | Bytes |
|---|---:|
| `legacy-DRAFT_5.2/Surviving-the-Singularity-DRAFT_5.2.epub` | 16,385,871 |
| `legacy-DRAFT_5.2/Surviving-the-Singularity-DRAFT_5.2.pdf` | 16,619,878 |

### legacy-DRAFT_5.3: 2 files

| Extracted file | Bytes |
|---|---:|
| `legacy-DRAFT_5.3/Surviving-the-Singularity-DRAFT_5.3.epub` | 16,388,633 |
| `legacy-DRAFT_5.3/Surviving-the-Singularity-DRAFT_5.3.pdf` | 16,626,245 |

### legacy-DRAFT_7: 2 files

| Extracted file | Bytes |
|---|---:|
| `legacy-DRAFT_7/Surviving-the-Singularity-DRAFT_7.epub` | 7,625,490 |
| `legacy-DRAFT_7/Surviving-the-Singularity-DRAFT_7.pdf` | 8,650,170 |

### legacy-Draft5: 1 file

| Extracted file | Bytes |
|---|---:|
| `legacy-Draft5/STS-Draft5-google-doc.md` | 181,014 |

### legacy-Draft5.1: 1 file

| Extracted file | Bytes |
|---|---:|
| `legacy-Draft5.1/StS-Draft-5.1-google-doc.md` | 98,282 |

### snapshot-2026-07-19: 1 file

| Extracted file | Bytes |
|---|---:|
| `snapshot-2026-07-19/StS-Complete-Draft-compiled-2026-07-19.md` | 531,209 |

### snapshot-2026-07-20: 1 file

| Extracted file | Bytes |
|---|---:|
| `snapshot-2026-07-20/StS-Complete-Draft-compiled-2026-07-20.md` | 533,286 |

### snapshot-2026-07-21: 1 file

| Extracted file | Bytes |
|---|---:|
| `snapshot-2026-07-21/StS-Complete-Draft-compiled-2026-07-21.md` | 541,052 |

### snapshot-2026-08-02: 1 file

| Extracted file | Bytes |
|---|---:|
| `snapshot-2026-08-02/StS-Complete-Draft-compiled-2026-08-02.md` | 577,574 |
