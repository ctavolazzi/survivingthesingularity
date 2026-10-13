"""Prove v0.10.3 adds artwork while retaining v0.10.2 prose and deliveries.

The only source exceptions are eight new image/caption pairs and the three
recorded relocations of existing image/caption pairs. Paragraph contents and
their remaining order must match exactly. Blank paragraph separators may vary.
Negative controls change in-memory strings and bytes, never the old checkout.
Use --self-test before final integration; the default requires the full release.
"""
from collections import Counter
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'src/lib/data/book'
EXPECTED_ADDITIONS = 8
EXPECTED_OLD_REFS = 102
EXPECTED_REGISTRY = 62
MOVE_FILES = {
    '11-chapter9.md': 'ch09-greenhouse-bus.svg',
    '27-chapter19.md': 'ch19-conversion-ladder.svg',
    '25-appendix-d.md': 'appd-precedent-timeline.svg',
}
REF = re.compile(r'\]\(/book-images/([^\s)]+)\)')
IMAGE = re.compile(r'!\[(?P<alt>[^\n]*)\]\(/book-images/(?P<file>[^\s)]+)\)')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def blocks(text):
    return re.split(r'\n[ \t]*\n', text.strip('\n')) if text.strip('\n') else []


def caption(block):
    return len(block) > 2 and block.startswith('*') and not block.startswith('**') and block.endswith('*')


def hash_errors(expected, actual):
    return [name for name, digest in expected.items()
            if name not in actual or sha(actual[name]) != digest]


def remove_blocks(values, removed):
    result = list(values)
    for block in removed:
        assert result.count(block) == 1, 'Relocated content must occur exactly once'
        result.remove(block)
    return result


def compare_sections(previous, current, moves, expected_additions=EXPECTED_ADDITIONS):
    """Pure content instrument shared by the real check and negative controls."""
    errors, records, additions = [], [], []
    old_refs = Counter(name for text in previous.values() for name in REF.findall(text))
    new_refs = Counter(name for text in current.values() for name in REF.findall(text))
    missing_refs = old_refs - new_refs
    extra_old = Counter({name: new_refs[name] - count for name, count in old_refs.items()
                         if new_refs[name] > count})
    if missing_refs:
        errors.append({'kind': 'missing_old_image_references', 'references': dict(missing_refs)})
    if extra_old:
        errors.append({'kind': 'duplicated_old_image_references', 'references': dict(extra_old)})
    new_names = set(new_refs) - set(old_refs)
    if sum(new_refs[name] for name in new_names) != expected_additions or len(new_names) != expected_additions:
        errors.append({'kind': 'new_image_count', 'expected': expected_additions,
                       'unique': len(new_names), 'occurrences': sum(new_refs[name] for name in new_names)})
    for name in previous:
        if name not in current:
            errors.append({'kind': 'missing_section', 'file': name})
            continue
        before, after = blocks(previous[name]), blocks(current[name])
        reduced, index = [], 0
        section_additions = []
        while index < len(after):
            image = IMAGE.fullmatch(after[index])
            if image and image['file'] in new_names:
                if not image['alt'].strip():
                    errors.append({'kind': 'empty_new_alt', 'file': name, 'image': image['file']})
                if index + 1 >= len(after) or not caption(after[index + 1]):
                    errors.append({'kind': 'missing_new_caption', 'file': name, 'image': image['file']})
                    reduced.append(after[index])
                    index += 1
                    continue
                record = {'section': name, 'file': image['file'], 'alt': image['alt'],
                          'image_block': after[index], 'caption_block': after[index + 1]}
                additions.append(record)
                section_additions.append(image['file'])
                index += 2
                continue
            reduced.append(after[index])
            index += 1
        move = moves.get(name)
        if move:
            move_parts = blocks(move['moved_block'])
            try:
                assert len(move_parts) == 2 and IMAGE.fullmatch(move_parts[0]) and caption(move_parts[1])
                assert IMAGE.fullmatch(move_parts[0])['file'] == MOVE_FILES[name]
                assert previous[name].count(move['moved_block']) == 1
                assert current[name].count(move['moved_block']) == 1
                assert current[name].count(move['moved_block'] + move['before_anchor']) == 1
                before = remove_blocks(before, move_parts)
                reduced = remove_blocks(reduced, move_parts)
            except (AssertionError, ValueError):
                errors.append({'kind': 'invalid_recorded_move', 'file': name})
        if before != reduced:
            errors.append({'kind': 'prose_or_old_art_changed', 'file': name,
                           'missing_blocks': list((Counter(before) - Counter(reduced)).elements())[:5],
                           'unexpected_blocks': list((Counter(reduced) - Counter(before)).elements())[:5],
                           'order_changed': Counter(before) == Counter(reduced)})
        records.append({'file': name, 'before_sha256': sha(previous[name].encode()),
                        'after_sha256': sha(current[name].encode()), 'old_blocks_checked': len(before),
                        'old_image_references': len(REF.findall(previous[name])),
                        'current_image_references': len(REF.findall(current[name])),
                        'added_artwork': section_additions, 'recorded_move': bool(move),
                        'exact_remaining_block_sequence': before == reduced})
    if set(current) != set(previous):
        errors.append({'kind': 'section_membership_changed'})
    if len(additions) != expected_additions:
        errors.append({'kind': 'image_caption_pair_count', 'expected': expected_additions, 'actual': len(additions)})
    return {'errors': errors, 'sections': records, 'additions': additions,
            'old_image_references': sum(old_refs.values()), 'image_references': sum(new_refs.values()),
            'retained_old_references': sum((old_refs & new_refs).values()),
            'old_prose_block_contents_and_order_preserved': not any(
                error['kind'] in ('prose_or_old_art_changed', 'invalid_recorded_move', 'missing_section', 'section_membership_changed')
                for error in errors)}


def negative_controls():
    old = {'sample.md': '# A chapter\n\nAn existing paragraph must remain byte for byte.\n\n'
                       '![Original image](/book-images/old.svg)\n\n*Original caption.*\n'}
    good = {'sample.md': old['sample.md'] + '\n![Added image](/book-images/new.svg)\n\n*Added caption.*\n'}
    assert not compare_sections(old, good, {}, 1)['errors'], 'Unmodified content fixture failed'
    cases = [
        ('missing_prose', good['sample.md'].replace('An existing paragraph must remain byte for byte.\n\n', ''), 'prose_or_old_art_changed'),
        ('missing_old_image_reference', good['sample.md'].replace('![Original image](/book-images/old.svg)\n\n', ''), 'missing_old_image_references'),
        ('changed_old_caption', good['sample.md'].replace('*Original caption.*', '*Changed old caption.*'), 'prose_or_old_art_changed'),
        ('unexpected_new_prose', good['sample.md'] + '\nAn unauthorized new paragraph.\n', 'prose_or_old_art_changed'),
    ]
    controls = {}
    for label, text, expected in cases:
        result = compare_sections(old, {'sample.md': text}, {}, 1)
        assert any(error['kind'] == expected for error in result['errors']), ('Control missed its intended defect', label)
        controls[label] = {'rejected': True, 'expected_failure': expected}
    frozen = {name: sha(text.encode()) for name, text in old.items()}
    unchanged = {name: text.encode() for name, text in old.items()}
    assert not hash_errors(frozen, unchanged)
    mutated = {**unchanged, 'sample.md': unchanged['sample.md'] + b'\nChanged reference baseline.\n'}
    assert hash_errors(frozen, mutated) == ['sample.md']
    controls['mutated_old_baseline'] = {'rejected': True, 'expected_failure': 'reference source hash mismatch'}
    return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true', help='Run only in-memory instrument controls')
    args = parser.parse_args()
    controls = negative_controls()
    if args.self_test:
        print(json.dumps({'negative_controls': controls, 'production_check_run': False}, indent=2))
        return
    baseline_path = HERE / 'baseline.json'
    baseline = json.loads(baseline_path.read_text())
    assert baseline['version'] == '0.10.2'
    parent = Path(baseline['parent_worktree']).resolve()
    assert parent == ROOT.parent / 'sts-v0.10.2', 'Unexpected reference checkout'
    old_source = parent / 'src/lib/data/book'
    old_bytes = {name: (old_source / name).read_bytes() for name in baseline['files']}
    assert not hash_errors(baseline['files'], old_bytes), 'Reference edition source changed'
    deliveries = []
    for record in baseline['deliveries']:
        path = parent / record['path']
        assert path.stat().st_size == record['bytes'] and file_sha(path) == record['sha256'], ('Reference delivery changed', record['path'])
        deliveries.append({'path': record['path'], 'sha256': record['sha256'], 'unchanged': True})
    prior = json.loads(old_bytes['book.json'])
    meta = json.loads((SOURCE / 'book.json').read_text())
    assert meta['version'] == HERE.name.removeprefix('v') == '0.10.3'
    assert meta['sections'] == prior['sections'], 'Manifest order or membership changed'
    ignored = {'version', 'lastUpdated'}
    assert {k: v for k, v in meta.items() if k not in ignored} == {k: v for k, v in prior.items() if k not in ignored}, 'Unexpected manifest changes'
    names = [section['file'] for section in meta['sections']]
    assert set(baseline['files']) == {'book.json', *names}, 'Baseline lacks manifest coverage'
    journal = json.loads((HERE / 'layout-source-moves.json').read_text())
    moves = {Path(row['file']).name: row for row in journal}
    assert len(journal) == len(moves) and set(moves) == set(MOVE_FILES), 'Unexpected relocation exceptions'
    for name, row in moves.items():
        assert row['file'] == f'src/lib/data/book/{name}' and row['image'] == MOVE_FILES[name]
        assert row['before_sha256'] == baseline['files'][name], 'Move receipt refers to another baseline'
    previous = {name: old_bytes[name].decode() for name in names}
    current = {name: (SOURCE / name).read_text() for name in names}
    report = compare_sections(previous, current, moves)
    assert not report['errors'], report['errors']
    assert report['old_image_references'] == report['retained_old_references'] == EXPECTED_OLD_REFS
    assert report['image_references'] == EXPECTED_OLD_REFS + EXPECTED_ADDITIONS
    old_registry = json.loads((old_source / 'visuals.json').read_text())['images']
    registry = json.loads((SOURCE / 'visuals.json').read_text())
    added = {entry['file'] for entry in report['additions']}
    assert registry['edition'] == meta['version']
    assert set(registry['images']) == set(old_registry) | added, 'Registry must retain old figures and register exactly the additions'
    assert len(registry['images']) == EXPECTED_REGISTRY
    extensions = Counter(Path(name).suffix for name in added)
    assert extensions['.svg'] == 4 and sum(extensions[ext] for ext in ('.png', '.jpg', '.jpeg', '.webp')) == 4, extensions
    asset_records = []
    for name in sorted(set(REF.findall('\n'.join(previous.values())))):
        old_asset, asset = parent / 'static/book-images' / name, ROOT / 'static/book-images' / name
        assert file_sha(old_asset) == file_sha(asset), ('Retained artwork changed', name)
        asset_records.append({'file': name, 'sha256': file_sha(asset), 'unchanged': True})
    for name in added:
        assert (ROOT / 'static/book-images' / name).is_file(), ('New artwork absent', name)
    report.update({'edition': meta['version'], 'baseline_sha256': file_sha(baseline_path),
                   'preserved_reference_source_files': len(old_bytes), 'preserved_deliveries': deliveries,
                   'retained_artwork': asset_records, 'registered_figures': len(registry['images']),
                   'expected_registered': sorted(registry['images']), 'addition_formats': dict(extensions),
                   'current_source_sha256': {'book.json': file_sha(SOURCE / 'book.json'), **{name: sha(text.encode()) for name, text in current.items()}},
                   'negative_controls': controls,
                   'limits': 'Exact paragraph content/order and recorded art moves, reference-source/delivery hashes, and retained image bytes. Blank paragraph separators are ignored. Does not establish factual truth, visual quality or rendered completeness.'})
    target = HERE / 'source-checks.json'
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    assert json.loads(target.read_text()) == report
    diff = ''.join(line for name in names for line in difflib.unified_diff(
        previous[name].splitlines(True), current[name].splitlines(True), fromfile='v0.10.2/' + name, tofile='v0.10.3/' + name))
    (HERE / 'source-changes.diff').write_text(diff)
    print(json.dumps({key: report[key] for key in ('edition', 'old_image_references', 'retained_old_references', 'image_references', 'registered_figures', 'addition_formats', 'negative_controls')}, indent=2))


if __name__ == '__main__':
    main()
