"""Check inherited editorial rules and new regressions, with in-memory faults."""
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch
import builtins
import io
import json
import re
import runpy
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'src/lib/data/book'


def inherited(inject=False):
    original_open = builtins.open
    def reader(path, *args, **kwargs):
        if inject and str(path).endswith('/02-introduction.md'):
            return io.StringIO((SOURCE / '02-introduction.md').read_text() + '\nInjected \u2014 defect.\n')
        return original_open(path, *args, **kwargs)
    captured = io.StringIO()
    with patch.object(sys, 'argv', ['gates.py', str(ROOT)]), patch('builtins.open', reader), redirect_stdout(captured):
        result = runpy.run_path(str(ROOT / 'docs/v0.9.2/gates.py'))
    return result['fails'], captured.getvalue()


def new_checks(meta, texts):
    errors = []
    if meta['version'] != '0.10.2':
        errors.append('Wrong final edition version')
    for filename, text in texts.items():
        if re.search(r'\b(?:TODO|FIXME|TBD|lorem ipsum)\b', text, re.I):
            errors.append('Unfinished marker: ' + filename)
        for image in re.findall(r'!\[[^\]]*\]\((/book-images/[^)]+)\)', text):
            if not (ROOT / 'static' / image.lstrip('/')).is_file():
                errors.append('Missing image: ' + image)
    glossary = texts['28-appendix-f.md']
    for stale in ["Once released, they can't be recalled", 'every node connects to several',
                  'process every word in relation to every other at once']:
        if stale in glossary:
            errors.append('Glossary overclaim: ' + stale)
    if 'Here they are in an order you can live' in texts['29-appendix-g.md']:
        errors.append('Year plan falsely claims complete practice coverage')
    return errors


def main():
    faults, _ = inherited(inject=True)
    assert any(f[0] == 'em dash' for f in faults), 'Inherited gate missed injected defect'
    meta = json.loads((SOURCE / 'book.json').read_text())
    texts = {s['file']: (SOURCE / s['file']).read_text() for s in meta['sections']}
    bad = dict(texts)
    bad['28-appendix-f.md'] += "\nOnce released, they can't be recalled\n"
    bad['29-appendix-g.md'] += '\nHere they are in an order you can live\n'
    bad['22-appendix-a.md'] += '\nTODO\n![probe](/book-images/__absent_v0102.svg)\n'
    assert len(new_checks(meta, bad)) == 4, 'New gates missed injected defects'
    faults, output = inherited()
    errors = new_checks(meta, texts)
    print(output, end='')
    for error in errors:
        print('FAIL', error)
    report = {'version': meta['version'], 'sections': len(texts),
              'inherited_errors': faults, 'new_errors': errors,
              'negative_controls': ['em dash', 'glossary overclaim', 'practice coverage', 'unfinished marker', 'missing image'],
              'limits': 'Known editorial regressions and source structure only; not a factual or literary certification.'}
    (Path(__file__).parent / 'gate-results.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Negative controls: 5 detected. Final errors:', len(faults) + len(errors))
    return bool(faults or errors)


if __name__ == '__main__':
    raise SystemExit(main())
