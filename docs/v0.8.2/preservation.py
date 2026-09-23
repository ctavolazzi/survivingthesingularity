"""Compare the author-approved baseline with the additive historical revision."""
from pathlib import Path
import copy
import difflib
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
DOCS = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/lib/data/book'
BASELINE = DOCS / 'baseline-v0.8.1'
META = json.loads((SOURCE / 'book.json').read_text())
EXCEPTIONS = json.loads((DOCS / 'preservation-exceptions.json').read_text())
RECORD = json.loads((DOCS / 'baseline.json').read_text())


def lines(text):
    return [line for line in text.splitlines() if line.strip()]


def omissions(current):
    failures = []
    for section in META['sections']:
        name = section['file']
        approved = {entry['old_line'] for entry in EXCEPTIONS.get(name, [])}
        before = [line for line in lines((BASELINE / name).read_text()) if line not in approved]
        after = iter(lines(current[name]))
        for line in before:
            if not any(candidate == line for candidate in after):
                failures.append({'file': name, 'missing_or_moved_line': line[:180]})
                break
        for entry in EXCEPTIONS.get(name, []):
            if entry['new_line'] not in current[name]:
                failures.append({'file': name, 'missing_approved_correction': entry['new_line'][:180]})
    return failures


def source_urls(text):
    return set(re.findall(r'\]\((https?://[^)]+)\)', text))


current = {s['file']: (SOURCE / s['file']).read_text() for s in META['sections']}
probe = copy.deepcopy(current)
name = '01-preface.md'
line = next(line for line in lines((BASELINE / name).read_text()) if line.startswith("This is an optimist's field manual."))
probe[name] = probe[name].replace(line, '')
assert omissions(probe), 'Preservation detector failed its deliberate omission control'
assert not omissions(current), omissions(current)

parent = Path(RECORD['source_directory']) / 'src/lib/data/book'
for name, digest in RECORD['source_sha256'].items():
    assert hashlib.sha256((parent / name).read_bytes()).hexdigest() == digest, ('parent changed', name)
    assert hashlib.sha256((BASELINE / name).read_bytes()).hexdigest() == digest, ('snapshot changed', name)

bibliography = source_urls(current['23-appendix-b.md'])
new_urls = set()
for section in META['sections']:
    if section['id'].startswith(('appendix', 'part')):
        continue
    name = section['file']
    new_urls |= source_urls(current[name]) - source_urls((BASELINE / name).read_text())
assert new_urls <= bibliography, sorted(new_urls - bibliography)
assert all('\u2014' not in text for text in current.values()), 'Em dash found in manuscript'

old_sections = json.loads((BASELINE / 'book.json').read_text())['sections']
assert META['sections'] == old_sections, 'Section order or chapter titles changed'
chapters = [s for s in META['sections'] if re.fullmatch(r'chapter\d+', s['id'])]
assert len(chapters) == 19
assert all(len(current[s['file']]) > len((BASELINE / s['file']).read_text()) for s in chapters)

diff = ''.join(''.join(difflib.unified_diff(
    (BASELINE / s['file']).read_text().splitlines(True),
    current[s['file']].splitlines(True),
    fromfile='v0.8.1/' + s['file'], tofile='v0.8.2/' + s['file'])) for s in META['sections'])
(DOCS / 'CHANGES-FROM-v0.8.1.diff').write_text(diff)
report = {
    'sections_compared': len(META['sections']),
    'numbered_chapters_expanded': len(chapters),
    'approved_line_replacements': sum(len(items) for items in EXCEPTIONS.values()),
    'all_other_nonblank_lines_preserved_in_order': True,
    'all_approved_corrections_present': True,
    'new_in_text_source_urls_present_in_bibliography': len(new_urls),
    'parent_and_snapshot_hashes_unchanged': True,
    'deliberate_missing_paragraph_detected': True,
    'chapter_order_and_titles_unchanged': True,
    'scope': 'Structural preservation, source locators, and baseline integrity; historical interpretation reviewed separately.'
}
(DOCS / 'preservation-checks.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
