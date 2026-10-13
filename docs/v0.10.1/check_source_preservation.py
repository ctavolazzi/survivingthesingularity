"""Compare this edition with the SHA-verified v0.10.0 source, without changing it."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/lib/data/book'
BASELINE = HERE / 'baseline.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source_blocks(text):
    # Includes headings, tables, image/caption blocks and citations as well as
    # prose. Blank paragraph separators are not compared; each block is exact.
    return [block for block in re.split(r'\n\s*\n', text) if block.strip()]


def image_refs(text):
    return re.findall(r'\]\(/book-images/([^\s)]+)\)', text)


def missing_in_order(before, after):
    position = 0
    missing = []
    for index, block in enumerate(source_blocks(before), 1):
        found = after.find(block, position)
        if found < 0:
            missing.append({'block': index, 'sha256': sha(block.encode()), 'excerpt': block[:160]})
        else:
            position = found + len(block)
    return missing


def verify_hash(data, expected, name):
    actual = sha(data)
    if actual != expected:
        raise AssertionError(f'Before-source hash mismatch: {name}')
    return actual


def ordered_subsequence(old, new):
    stream = iter(new)
    return all(any(item == expected for item in stream) for expected in old)


def main():
    baseline = json.loads(BASELINE.read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', type=Path, default=Path(baseline['parent_worktree']))
    args = parser.parse_args()
    before_root = args.before.resolve()
    before_source = before_root / 'src/lib/data/book'
    final_record = before_root / 'docs/v0.10.0/final-source.json'
    final = json.loads(final_record.read_text())
    assert baseline['version'] == final['version'] == '0.10.0'
    assert baseline['files'] == final['files'], 'v0.10.1 baseline differs from v0.10.0 final-source ledger'
    verified_before = {}
    for name, expected in baseline['files'].items():
        data = (before_source / name).read_bytes()
        verify_hash(data, expected, name)
        verified_before[name] = data
    before_meta = json.loads(verified_before['book.json'])
    after_meta = json.loads((SOURCE / 'book.json').read_bytes())
    assert before_meta['sections'] == after_meta['sections'], 'Section manifest or order changed'
    assert before_meta['version'] == '0.10.0' and after_meta['version'] == '0.10.1'
    sections = []
    before_images, after_images = [], []
    errors = []
    for section in before_meta['sections']:
        name = section['file']
        before = verified_before[name].decode()
        current_bytes = (SOURCE / name).read_bytes()
        current = current_bytes.decode()
        old_images, new_images = image_refs(before), image_refs(current)
        missing = missing_in_order(before, current)
        removed = list((Counter(old_images) - Counter(new_images)).elements())
        image_order = ordered_subsequence(old_images, new_images)
        record = {
            'id': section['id'], 'file': name,
            'before_sha256': baseline['files'][name], 'before_hash_verified': True,
            'after_sha256': sha(current_bytes),
            'before_source_blocks': len(source_blocks(before)),
            'after_source_blocks': len(source_blocks(current)),
            'before_blocks_preserved_in_order': len(source_blocks(before)) - len(missing),
            'missing_or_reordered_before_blocks': missing,
            'before_image_references': len(old_images), 'after_image_references': len(new_images),
            'removed_image_occurrences': removed, 'before_image_order_preserved': image_order,
            'added_image_references': list((Counter(new_images) - Counter(old_images)).elements()),
        }
        sections.append(record)
        if missing or removed or not image_order:
            errors.append(name)
        before_images.extend(old_images)
        after_images.extend(new_images)
    added = list((Counter(after_images) - Counter(before_images)).elements())
    registry = json.loads((SOURCE / 'visuals.json').read_text())['images']
    assert len(added) == len(set(added)) == len(registry) == 23
    assert set(added) == set(registry), 'Added figures differ from presentation registry'
    # Controls live in memory, never in either edition's source files.
    controls = []
    try:
        verify_hash(verified_before['book.json'] + b'\n', baseline['files']['book.json'], 'deliberate mutation')
    except AssertionError:
        controls.append('Changed reference bytes rejected by baseline SHA-256 gate.')
    else:
        raise AssertionError('Hash gate accepted a changed reference')
    sample = before_meta['sections'][0]['file']
    original = verified_before[sample].decode()
    actual = (SOURCE / sample).read_text()
    unique = next(block for block in source_blocks(original) if len(block) > 150 and actual.count(block) == 1)
    assert missing_in_order(original, actual.replace(unique, '', 1))
    controls.append('Deletion of one real unique source block rejected by ordered comparison.')
    assert missing_in_order('first\n\nsecond\n\nfirst', 'first\n\nsecond')
    controls.append('Loss of a repeated block rejected; one surviving copy cannot satisfy two original occurrences.')
    assert not ordered_subsequence(['a.svg', 'b.svg'], ['b.svg', 'a.svg'])
    controls.append('Reordered image references rejected.')
    report = {
        'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'before_edition': before_meta['version'], 'after_edition': after_meta['version'],
        'before_worktree': str(before_root), 'after_worktree': str(ROOT),
        'baseline': {'path': str(BASELINE.relative_to(ROOT)), 'sha256': sha(BASELINE.read_bytes()),
                     'v0_10_0_final_source_record': str(final_record), 'final_record_sha256': sha(final_record.read_bytes()),
                     'ledgers_match_exactly': True, 'verified_files': len(verified_before)},
        'manifest': {'before_sha256': baseline['files']['book.json'], 'after_sha256': sha((SOURCE / 'book.json').read_bytes()),
                     'sections_and_order_unchanged': True,
                     'metadata_changes': {key: {'before': before_meta.get(key), 'after': after_meta.get(key)} for key in sorted(set(before_meta) | set(after_meta)) if key != 'sections' and before_meta.get(key) != after_meta.get(key)}},
        'totals': {'sections': len(sections),
                   'before_source_blocks': sum(s['before_source_blocks'] for s in sections),
                   'after_source_blocks': sum(s['after_source_blocks'] for s in sections),
                   'before_blocks_preserved_in_order': sum(s['before_blocks_preserved_in_order'] for s in sections),
                   'before_image_references': len(before_images), 'after_image_references': len(after_images),
                   'before_unique_images': len(set(before_images)), 'after_unique_images': len(set(after_images)),
                   'added_image_references': len(added)},
        'added_images': added, 'sections': sections, 'errors': errors, 'negative_controls': controls,
        'limits': 'Compares exact paragraph-delimited source blocks in order, including headings, tables, images and citations. Blank paragraph separators are not compared. Verifies source preservation, not factual accuracy, visual quality, generated PDF/EPUB coverage, or external rights.'
    }
    (HERE / 'source-preservation.json').write_text(json.dumps(report, indent=2) + '\n')
    t = report['totals']
    rows = '\n'.join(f"| {s['file']} | {s['before_source_blocks']} | {s['after_source_blocks']} | {s['before_blocks_preserved_in_order']} | {s['before_image_references']} / {s['after_image_references']} |" for s in sections)
    markdown = f'''# v0.10.1 source preservation

Checked against the preserved v0.10.0 source. Before reading that source as
reference material, the check verified all {len(verified_before)} files against
`docs/v0.10.1/baseline.json`. Its file map also exactly matches the preserved
v0.10.0 `final-source.json`. The old worktree was read only.

- Sections and manifest order: {t['sections']}, unchanged.
- Paragraph-delimited source blocks: {t['before_source_blocks']} before, {t['after_source_blocks']} after.
- Original blocks preserved verbatim and in order: {t['before_blocks_preserved_in_order']} of {t['before_source_blocks']}.
- Image references: {t['before_image_references']} before, {t['after_image_references']} after.
- Unique referenced images: {t['before_unique_images']} before, {t['after_unique_images']} after.
- Added image references: {t['added_image_references']}, each present once and matching the presentation registry.
- Missing or reordered source blocks and removed image occurrences: {len(errors)} affected sections.

[Machine report](source-preservation.json) records exact before/after file
SHA-256 values, both baseline-ledger hashes, metadata changes, per-section
counts, and the added image list. Rerun after any canonical source change:

```sh
python3 docs/v0.10.1/check_source_preservation.py
```

For a relocated reference worktree, pass `--before /path/to/sts-v0.10.0`.
That override changes only where the reference is read; all expected hashes
must still match.

The blocks are separated by blank lines and include headings, tables,
images, captions, citations, and prose. Each original block must occur in
order in the new source, and repeated blocks need distinct occurrences.
This does not claim byte-identical source files: additions are expected,
and blank paragraph separators are not part of the block comparison.

Intentional in-memory controls rejected changed reference bytes, deletion
of a real source block, loss of a repeated block, and reordered image
references. The report verifies source preservation only. Final PDF/EPUB
coverage and visual checks remain separate.

| Source file | Blocks before | Blocks after | Original blocks preserved | Image refs before / after |
| --- | ---: | ---: | ---: | ---: |
{rows}
'''
    (HERE / 'SOURCE-PRESERVATION.md').write_text(markdown)
    print(json.dumps({'totals': t, 'errors': errors, 'negative_controls': controls}, indent=2))
    assert not errors, errors


if __name__ == '__main__':
    main()
