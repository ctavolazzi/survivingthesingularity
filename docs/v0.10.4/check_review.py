"""Replay reviewed edits and verify preserved source, artwork and prior deliveries."""
from collections import Counter
from pathlib import Path
import difflib
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'src/lib/data/book'
read = lambda path: json.loads(path.read_text())
sha = lambda data: hashlib.sha256(data).hexdigest()


def replay(text, edits):
    for edit in edits:
        assert edit['before'] != edit['after'], 'Empty editorial change'
        assert text.count(edit['before']) == 1, 'Ambiguous or stale edit'
        text = text.replace(edit['before'], edit['after'], 1)
    return text


def same(expected, actual):
    assert expected == actual, 'Unreviewed content or altered reference'


def main():
    baseline = read(HERE / 'baseline.json')
    parent = Path(baseline['parent_worktree'])
    previous = parent / 'src/lib/data/book'
    reviews = [read(HERE / (name + '-review.json')) for name in ('opening', 'middle', 'ending')]
    edits = [edit for review in reviews for edit in review['edits']]
    coverage = [dict(entry, file=Path(entry['file']).name) for review in reviews for entry in review['files_read']]
    edits = [dict(edit, file=Path(edit['file']).name) for edit in edits]
    meta = read(SOURCE / 'book.json')
    prior_meta = read(previous / 'book.json')
    same('0.10.4', meta['version'])
    same(prior_meta['sections'], meta['sections'])
    same(prior_meta['released'], meta['released'])
    expected_names = [section['file'] for section in meta['sections']]
    coverage = [entry for entry in coverage if entry['file'] in expected_names]
    same(Counter(expected_names), Counter(entry['file'] for entry in coverage))
    controls = []
    for name, operation in [
        ('unrecorded prose', lambda: same('Reviewed paragraph.', 'Reviewed paragraph. Extra sentence.')),
        ('changed reference hash', lambda: same(sha(b'original'), sha(b'altered'))),
        ('missing or ambiguous edit', lambda: replay('Missing anchor.', [{'before': 'Original.', 'after': 'Revised.'}]))]:
        try:
            operation()
        except AssertionError:
            controls.append(name)
        else:
            raise AssertionError('Negative control stayed green: ' + name)
    for name, expected in baseline['files'].items():
        same(expected, sha((previous / name).read_bytes()))
    for record in baseline['deliveries']:
        same(record['sha256'], sha((parent / record['path']).read_bytes()))
    for name, expected in baseline['images'].items():
        same(expected, sha((parent / name).read_bytes()))
        same(expected, sha((ROOT / name).read_bytes()))
    records, diff = [], []
    for entry in coverage:
        name = entry['file']
        before, after = (previous / name).read_text(), (SOURCE / name).read_text()
        selected = [edit for edit in edits if edit['file'] == name]
        same(entry['before_sha256'], sha(before.encode()))
        same(entry['after_sha256'], sha(after.encode()))
        same(replay(before, selected), after)
        refs = lambda text: re.findall(r'!\[[^\]]*\]\(/book-images/[^)]+\)', text)
        same(refs(before), refs(after))
        links = lambda text: re.findall(r'\]\((https?://[^)]+)\)', text)
        same(links(before), links(after))
        records.append({'file': name, 'edits': len(selected), 'before_sha256': sha(before.encode()),
                        'after_sha256': sha(after.encode()), 'image_references': len(refs(after))})
        diff.extend(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                    fromfile='v0.10.3/' + name, tofile='v0.10.4/' + name))
    report = {'version': meta['version'], 'sections': records, 'reviewed_sections': len(records),
              'edits': len(edits), 'changed_sections': sum(record['edits'] > 0 for record in records),
              'image_references': sum(record['image_references'] for record in records),
              'preserved_art_files': len(baseline['images']), 'preserved_deliveries': len(baseline['deliveries']),
              'current_source_sha256': {name: sha((SOURCE / name).read_bytes()) for name in baseline['files']},
              'negative_controls': controls, 'errors': [],
              'limits': 'Exact editorial replay and preservation checks. Literary judgment is in the reviews; this does not recertify inherited external claims.'}
    (HERE / 'source-checks.json').write_text(json.dumps(report, indent=2) + '\n')
    (HERE / 'source-changes.diff').write_text(''.join(diff))
    assert read(HERE / 'source-checks.json') == report
    print(json.dumps({key: value for key, value in report.items() if key not in ('sections', 'current_source_sha256')}))


if __name__ == '__main__':
    main()
