# Packaged publication fonts

Packaged 2026-09-22. Font files are unmodified static OpenType assets. This directory is self-contained for the selected book typography; it does not depend on a font being installed on the reader's computer.

## Selection and rights

Body text uses **Source Serif 4**, version 4.005, downloaded from [Adobe's official Source Serif repository](https://github.com/adobe-fonts/source-serif) at commit `80d3f8894c09c937bebfa9011247d2e1c79fd6f4`. Three faces are provided: regular, italic, and semibold.

Labels, captions, tables, and navigation use **Source Sans Pro**, version 3.006. Four faces are provided: regular, italic, semibold, and semibold italic. These were copied unchanged from the locally installed TeX Live 2025 `sourcesanspro` package, together with that package's original font license. The font binaries identify Adobe as copyright holder and explicitly state SIL Open Font License 1.1. Adobe's [official version 3.006 release](https://github.com/adobe-fonts/source-sans/releases/tag/3.006R) documents that version. The [CTAN package record](https://www.ctan.org/pkg/sourcesans) identifies the package lineage and its font license; its current version is newer than this installed package. The local files have not been claimed as fresh downloads or byte-compared against the upstream 3.006 release.

Source Sans 3 was the initial preference. Requests to the pinned official repository, its release branch, its contents API, and a byte-range endpoint repeatedly stalled or timed out. The complete licensed local Source Sans Pro set was selected to avoid an undocumented system-font fallback. No incomplete Source Sans 3 files have been included.

Both families are supplied under **SIL Open Font License 1.1**. That license permits embedding and redistribution under its conditions; distributing a document created with the font does not put the document under OFL. Keep the original copyright and license files with any redistributed font package. These rights are grounded in the supplied font licenses and the [official OFL text](https://openfontlicense.org/open-font-license-official-text/), not merely in a font's availability online.

- [Source Serif 4 original license](SourceSerif4-LICENSE.md), copied from the exact pinned repository version.
- [Source Sans Pro original package license](SourceSansPro-LICENSE.txt), copied from the installed distribution.
- [Copyright notices extracted from the supplied fonts](FONT-COPYRIGHTS.txt). This preserves the binaries' more recent notices in addition to the unmodified package license.
- [Machine-readable provenance and SHA-256 manifest](font-provenance.json).

## Static-face verification

FontTools successfully parsed every supplied font. All seven fonts lack an `fvar` table, confirming these are static faces. All have `OS/2.fsType = 0`. Regular and italic weights are 400; semibold weights are 600. These metadata checks establish file identity and embedding-bit status. The accompanying OFL documents establish the license basis.

| File | Family | Style | Weight |
| --- | --- | --- | --- |
| [SourceSansPro-Regular.otf](SourceSansPro-Regular.otf) | Source Sans Pro | Regular | 400 |
| [SourceSansPro-RegularIt.otf](SourceSansPro-RegularIt.otf) | Source Sans Pro | Italic | 400 |
| [SourceSansPro-Semibold.otf](SourceSansPro-Semibold.otf) | Source Sans Pro | Semibold | 600 |
| [SourceSansPro-SemiboldIt.otf](SourceSansPro-SemiboldIt.otf) | Source Sans Pro | Semibold Italic | 600 |
| [SourceSerif4-It.otf](SourceSerif4-It.otf) | Source Serif 4 | Italic | 400 |
| [SourceSerif4-Regular.otf](SourceSerif4-Regular.otf) | Source Serif 4 | Regular | 400 |
| [SourceSerif4-Semibold.otf](SourceSerif4-Semibold.otf) | Source Serif 4 | Semibold | 600 |

Use the exact paths and weights in the publication stylesheet. The Source Sans Pro italic filename is `SourceSansPro-RegularIt.otf`, not `SourceSans3-It.otf`. Source Serif 4 semibold italic is not packaged; an unavailable face should not silently be described as an embedded genuine face. Final PDF font-resource inspection remains necessary to detect font substitution or synthesis in the actual typeset artifact.

## Exact sources and checksums

The source locations below describe where the packaged bytes came from. Local paths are included for reproducibility on this machine. SHA-256 values let future work verify that the packaged files have not changed.

### SourceSansPro-Regular.otf

Local source: `/usr/local/texlive/2025/texmf-dist/fonts/opentype/adobe/sourcesanspro/SourceSansPro-Regular.otf`.

Upstream context: [Adobe Source Sans 3.006 release](https://github.com/adobe-fonts/source-sans/releases/tag/3.006R).

SHA-256: `7134d229b15cdd0827376d8a24f6f531f616eb1b3fecd16e1cf8a86d0bf6bc51`

### SourceSansPro-RegularIt.otf

Local source: `/usr/local/texlive/2025/texmf-dist/fonts/opentype/adobe/sourcesanspro/SourceSansPro-RegularIt.otf`.

Upstream context: [Adobe Source Sans 3.006 release](https://github.com/adobe-fonts/source-sans/releases/tag/3.006R).

SHA-256: `d38e0d70cd4f4aa072457c5ae647b987f10c3cea34bff581ee358a7c2a526053`

### SourceSansPro-Semibold.otf

Local source: `/usr/local/texlive/2025/texmf-dist/fonts/opentype/adobe/sourcesanspro/SourceSansPro-Semibold.otf`.

Upstream context: [Adobe Source Sans 3.006 release](https://github.com/adobe-fonts/source-sans/releases/tag/3.006R).

SHA-256: `aa53ed4fc17334a0c2ee8412c1e4e728bfb732a96b119164f7354343dad8f2f2`

### SourceSansPro-SemiboldIt.otf

Local source: `/usr/local/texlive/2025/texmf-dist/fonts/opentype/adobe/sourcesanspro/SourceSansPro-SemiboldIt.otf`.

Upstream context: [Adobe Source Sans 3.006 release](https://github.com/adobe-fonts/source-sans/releases/tag/3.006R).

SHA-256: `cdeddc767fdb11770451c5fac8f98b7d343b7fc9604f9db5034f50f7f437047a`

### SourceSerif4-It.otf

Source: [pinned Adobe repository file](https://raw.githubusercontent.com/adobe-fonts/source-serif/80d3f8894c09c937bebfa9011247d2e1c79fd6f4/OTF/SourceSerif4-It.otf).

SHA-256: `f8062257f4693e438a8e317c9fe2b4393f0d4eed84d897edcbfd733c30a1c1a1`

### SourceSerif4-Regular.otf

Source: [pinned Adobe repository file](https://raw.githubusercontent.com/adobe-fonts/source-serif/80d3f8894c09c937bebfa9011247d2e1c79fd6f4/OTF/SourceSerif4-Regular.otf).

SHA-256: `edf160d0d584deee8a3bb2c3371b2a7624ca63580fbe02c57c1f4c91e84d8787`

### SourceSerif4-Semibold.otf

Source: [pinned Adobe repository file](https://raw.githubusercontent.com/adobe-fonts/source-serif/80d3f8894c09c937bebfa9011247d2e1c79fd6f4/OTF/SourceSerif4-Semibold.otf).

SHA-256: `25e034392847d9965c92f98971b3646436b7ab919ece9118b0c0e5ec94c02efc`

### SourceSerif4-LICENSE.md

Source: [pinned Adobe repository license](https://raw.githubusercontent.com/adobe-fonts/source-serif/80d3f8894c09c937bebfa9011247d2e1c79fd6f4/LICENSE.md).

SHA-256: `c21d7293d87b6d7ab1d0229a2f55b77f33a7613a6a4e66f6693d68d7d8d09464`

### SourceSansPro-LICENSE.txt

Local source: `/usr/local/texlive/2025/texmf-dist/doc/latex/sourcesanspro/LICENSE.txt`.

SHA-256: `4a4a4179a96b5ef6786186d199f0d049b151352f460b8d2f3c00083792f37dd9`

