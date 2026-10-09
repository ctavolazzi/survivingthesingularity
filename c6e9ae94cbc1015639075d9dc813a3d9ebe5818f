"""Prove an additive edition against git book-v0.10.4 and stable block IDs.

The sole permitted original-text replacement changes the closing imperative.
All other original blocks, images, captions, scene markers and citations must
remain in order. Controls modify in-memory copies, never source or artifacts.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'src/lib/data/book'
BASE_REF = 'book-v0.10.4'
CHANGED = {'02-introduction.md', '08-chapter6.md', '27-chapter19.md',
           '21-conclusion.md', '23-appendix-b.md'}
ENDING_BEFORE = "Stop arguing. Stop waiting. Start building. And when you've found your footing, turn around and help everyone you can reach find theirs."
ENDING_AFTER = "Stop waiting. Show up. Start building. And when you've found your footing, turn around and help everyone you can reach find theirs."
IMAGE = re.compile(r'!\[[^\n]*?\]\(/book-images/[^\s)]+\)')
SCENE = re.compile(r'<!--\s*(?:book-scene|interactive:).*?-->|\[\[interactive:.*?\]\]', re.S)
LINK = re.compile(r'\]\((?:https?://|sts:)[^)]+\)')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, check=True).stdout


def baseline(name):
    return git('show', BASE_REF + ':src/lib/data/book/' + name)


def blocks(text):
    return [part for part in re.split(r'\n[ \t]*\n', text.strip('\n')) if part.strip()]


def subsequence(before, after):
    position, missing = 0, []
    for index, block in enumerate(before):
        try:
            found = after.index(block, position)
        except ValueError:
            missing.append({'block': index + 1, 'sha256': sha(block.encode()), 'excerpt': block[:120]})
        else:
            position = found + 1
    return missing


def section_check(name, before, after):
    errors = []
    expected = before
    if name == '21-conclusion.md':
        if before.count(ENDING_BEFORE) != 1 or after.count(ENDING_AFTER) != 1 or ENDING_BEFORE in after:
            errors.append({'kind': 'closing_line', 'file': name})
        expected = before.replace(ENDING_BEFORE, ENDING_AFTER, 1)
    if name not in CHANGED and before != after:
        errors.append({'kind': 'unexpected_changed_section', 'file': name})
    missing = subsequence(blocks(expected), blocks(after))
    if missing:
        errors.append({'kind': 'original_blocks_missing_or_reordered', 'file': name, 'blocks': missing})
    for label, expression in [('images', IMAGE), ('scene_markers', SCENE)]:
        if expression.findall(before) != expression.findall(after):
            errors.append({'kind': label + '_changed', 'file': name})
    if subsequence(LINK.findall(before), LINK.findall(after)):
        errors.append({'kind': 'existing_citation_changed', 'file': name})
    # Exact caption blocks cannot be silently edited, even in changed sections.
    caption = lambda value: [part for part in blocks(value) if part.startswith('*') and part.endswith('*')]
    if subsequence(caption(before), caption(after)):
        errors.append({'kind': 'existing_caption_changed', 'file': name})
    remaining = Counter(blocks(after)) - Counter(blocks(expected))
    return errors, {'file': name, 'before_sha256': sha(before.encode()), 'after_sha256': sha(after.encode()),
                    'before_blocks': len(blocks(before)), 'after_blocks': len(blocks(after)),
                    'image_references': len(IMAGE.findall(after)), 'scene_markers': len(SCENE.findall(after)),
                    'retained_blocks': len(blocks(expected)) - len(missing),
                    'added_blocks': list(remaining.elements())}


def index_check(before, after, previous_source, current_source):
    errors, unchanged, replaced = [], 0, []
    old_sections = {section['id']: section for section in before['sections']}
    new_sections = {section['id']: section for section in after['sections']}
    if list(old_sections) != list(new_sections):
        errors.append({'kind': 'sidecar_section_order'})
    ids = [block['id'] for section in after['sections'] for block in section['blocks']]
    if len(ids) != len(set(ids)):
        errors.append({'kind': 'duplicate_block_id'})
    for sid, old_section in old_sections.items():
        new_section = new_sections.get(sid)
        if not new_section:
            continue
        name = old_section['file']
        current = {block['id']: block for block in new_section['blocks']}
        old_lines, new_lines = previous_source[name].splitlines(), current_source[name].splitlines()
        for old in old_section['blocks']:
            new = current.get(old['id'])
            if not new:
                errors.append({'kind': 'lost_inherited_id', 'id': old['id']})
                continue
            extract = lambda lines, item: '\n'.join(lines[item['lines'][0] - 1:item['lines'][1]])
            old_text, new_text = extract(old_lines, old), extract(new_lines, new)
            if old_text == new_text and old['type'] == new['type'] and old['hash'] == new['hash']:
                unchanged += 1
            elif name == '21-conclusion.md' and old_text == ENDING_BEFORE and new_text == ENDING_AFTER:
                replaced.append(old['id'])
            else:
                errors.append({'kind': 'changed_inherited_id_content', 'id': old['id'], 'file': name})
        inherited = {block['id'] for block in old_section['blocks']} | set(old_section.get('tombstones', []))
        for new in new_section['blocks']:
            if new['id'] in set(old_section.get('tombstones', [])):
                errors.append({'kind': 'reused_tombstone_id', 'id': new['id']})
            if new['id'] not in inherited:
                ordinal = int(new['id'].rsplit('.b', 1)[1])
                if ordinal < old_section['next_ordinal']:
                    errors.append({'kind': 'new_id_below_old_frontier', 'id': new['id']})
    return errors, {'unchanged_inherited_ids': unchanged, 'reviewed_replacement_ids': replaced,
                    'inherited_blocks': sum(len(section['blocks']) for section in before['sections']),
                    'current_blocks': len(ids), 'new_ids': len(ids) - unchanged - len(replaced)}


def blob_digest(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def asset_matches(data, expected):
    return blob_digest(data) == expected


def negative_controls(previous, old_index):
    controls = []
    name = '08-chapter6.md'
    original = previous[name]
    paragraphs = blocks(original)
    unique = next(part for part in paragraphs if len(part) > 120 and original.count(part) == 1 and not part.startswith(('#', '*', '>')))
    good = original + '\n\nA deliberate additive control paragraph.\n'
    assert not section_check(name, original, good)[0]
    mutant = good.replace(unique, '', 1)
    assert any(error['kind'] == 'original_blocks_missing_or_reordered' for error in section_check(name, original, mutant)[0])
    controls.append('removed real inherited paragraph inside a changed chapter')
    image = IMAGE.search(original).group()
    assert any(error['kind'] == 'images_changed' for error in section_check(name, original, good.replace(image, '', 1))[0])
    controls.append('removed real image markup')
    ending = previous['21-conclusion.md']
    intended = ending.replace(ENDING_BEFORE, ENDING_AFTER, 1)
    assert not section_check('21-conclusion.md', ending, intended)[0]
    assert any(error['kind'] == 'closing_line' for error in section_check('21-conclusion.md', ending, intended.replace(ENDING_AFTER, '', 1))[0])
    controls.append('removed approved closing imperative')
    assert subsequence(['repeated', 'middle', 'repeated'], ['repeated', 'middle'])
    controls.append('removed repeated source block occurrence')
    copied = copy.deepcopy(old_index)
    sample = copied['sections'][0]['blocks']
    sample[0]['id'], sample[1]['id'] = sample[1]['id'], sample[0]['id']
    errors, _ = index_check(old_index, copied, previous, previous)
    assert any(error['kind'] == 'changed_inherited_id_content' for error in errors)
    controls.append('swapped real inherited block IDs')
    path = 'static/book-images/intro-nine-stages.svg'
    asset = git('show', BASE_REF + ':' + path)
    expected = git('rev-parse', BASE_REF + ':' + path).decode().strip()
    assert asset_matches(asset, expected)
    assert not asset_matches(asset + b'\nDeliberate in-memory corruption.', expected)
    controls.append('changed real retained diagram rejected by asset hash gate')
    return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    old_meta = json.loads(baseline('book.json'))
    previous = {section['file']: baseline(section['file']).decode() for section in old_meta['sections']}
    old_index = json.loads(baseline('manuscript-index.json'))
    controls = negative_controls(previous, old_index)
    if args.self_test:
        print(json.dumps({'negative_controls': controls, 'source_or_output_writes': False}, indent=2))
        return
    meta = json.loads((SOURCE / 'book.json').read_text())
    errors = []
    if meta['version'] != '0.11.0' or meta['lastUpdated'] != '2026-10-07':
        errors.append({'kind': 'edition_metadata'})
    for key in set(old_meta) | set(meta):
        if key not in {'version', 'lastUpdated'} and meta.get(key) != old_meta.get(key):
            errors.append({'kind': 'unexpected_metadata_change', 'key': key})
    current = {name: (SOURCE / name).read_text() for name in previous}
    sections = []
    for name, before in previous.items():
        findings, record = section_check(name, before, current[name])
        errors.extend(findings)
        sections.append(record)
    required = {
        '08-chapter6.md': ['## Whose robots?', 'Wiener', 'Ostrom', 'oligarch'],
        '27-chapter19.md': ['## Get involved', 'Tucson', 'Douglass'],
        '21-conclusion.md': ['solarpunk', 'Le Guin', ENDING_AFTER],
        '23-appendix-b.md': ['Wiener', 'Ostrom', 'Le Guin', 'Douglass'],
    }
    for name, phrases in required.items():
        for phrase in phrases:
            if phrase not in current[name]:
                errors.append({'kind': 'missing_new_content', 'file': name, 'phrase': phrase})
    if not any(record['added_blocks'] for record in sections if record['file'] == '02-introduction.md'):
        errors.append({'kind': 'missing_introduction_qualification'})
    source_names = git('ls-tree', '-r', '--name-only', BASE_REF, '--', 'src/lib/data/book').decode().splitlines()
    for path in source_names:
        name = Path(path).name
        if name in previous or name in {'book.json', 'manuscript-index.json'}:
            continue
        if (ROOT / path).read_bytes() != git('show', BASE_REF + ':' + path):
            errors.append({'kind': 'unexpected_source_auxiliary_change', 'file': path})
    new_index = json.loads((SOURCE / 'manuscript-index.json').read_text())
    if new_index['book_version'] != meta['version']:
        errors.append({'kind': 'stale_sidecar_version'})
    index_errors, continuity = index_check(old_index, new_index, previous, current)
    errors.extend(index_errors)
    paths = ('static/book-images', 'scripts/book-cover.png', 'publication/assets')
    asset_tree = git('ls-tree', '-r', '--format=%(objectname) %(path)', BASE_REF, '--', *paths).decode().splitlines()
    assets = []
    for row in asset_tree:
        expected, path = row.split(' ', 1)
        target = ROOT / path
        valid = target.is_file() and asset_matches(target.read_bytes(), expected)
        assets.append({'file': path, 'git_blob': expected, 'unchanged': valid})
        if not valid:
            errors.append({'kind': 'asset_changed_or_missing', 'file': path})
    report = {'version': meta['version'], 'checked_utc': datetime.now(timezone.utc).isoformat(),
              'baseline_ref': BASE_REF, 'baseline_commit': git('rev-parse', BASE_REF).decode().strip(),
              'allowed_changed_sections': sorted(CHANGED), 'sections': sections, 'stable_ids': continuity,
              'index_sha256': sha((SOURCE / 'manuscript-index.json').read_bytes()),
              'asset_files_checked': len(assets), 'assets': assets, 'negative_controls': controls,
              'current_source_sha256': {name: sha((SOURCE / name).read_bytes()) for name in ['book.json', *previous]},
              'errors': errors,
              'limits': 'Proves original text and artwork preservation plus known additions; does not validate new claims, literary quality or artifact rendering. EPUB content and PDF text require separate fresh-source proofs.'}
    target = HERE / 'source-preservation.json'
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    assert json.loads(target.read_text()) == report
    print(json.dumps({'version': meta['version'], 'sections': len(sections), 'stable_ids': continuity,
                      'assets': len(assets), 'negative_controls': controls, 'errors': errors}, indent=2))
    if errors:
        raise AssertionError(f'{len(errors)} source preservation failures')


if __name__ == '__main__':
    main()
