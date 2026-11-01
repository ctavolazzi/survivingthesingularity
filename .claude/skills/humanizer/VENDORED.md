# Vendored: blader/humanizer

| Field | Value |
|---|---|
| Upstream | https://github.com/blader/humanizer |
| Commit | `0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0` (2026-10-28) |
| Skill version | 3.1.0 (SKILL.md frontmatter) |
| License | MIT, Copyright (c) 2025 Siqi Chen (`LICENSE` beside this file) |
| Vendored | 2026-11-01 |
| Files copied | `SKILL.md`, `LICENSE`, both unmodified |
| SKILL.md sha256 | `0612f1dfb1672b0ea9b97e139bf1f06cabe98d8b27424fe8ff01e1fb4cc99cad` |

Do not edit `SKILL.md` here. Book-specific rules live in `../humanize-book/SKILL.md`,
so an upstream update is a clean file replacement plus a re-read of the wrapper.

To update:

```bash
git clone --depth 1 https://github.com/blader/humanizer /tmp/humanizer
cp /tmp/humanizer/SKILL.md /tmp/humanizer/LICENSE .claude/skills/humanizer/
sha256sum .claude/skills/humanizer/SKILL.md   # record it above with the new commit
git diff .claude/skills/humanizer/SKILL.md    # read what changed before the next pass
python3 scripts/humanizer_scan.py --selftest  # the scanner's lists follow the pattern numbers
```

If upstream renumbers its patterns, update the numbers in `scripts/humanizer_scan.py` and
in `../humanize-book/SKILL.md` section 3.
