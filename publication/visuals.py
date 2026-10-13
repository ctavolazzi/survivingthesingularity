"""Shared, fail-closed presentation and prepared-print registry."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / 'static/book-images'
REGISTRY = ROOT / 'src/lib/data/book/visuals.json'
LAYOUTS = {'diagram', 'cutout-left', 'cutout-right', 'inset'}


def entries():
    data = json.loads(REGISTRY.read_text())
    assert data['schema'] == 'sts-visuals/v1'
    for name, entry in data['images'].items():
        assert Path(name).name == name, ('Invalid visual filename', name)
        assert entry['layout'] in LAYOUTS, ('Invalid visual layout', name)
    return data['images']


def prepared_variant(name):
    """None means legacy artwork. Registered print artwork must match both hashes."""
    entry = entries().get(name)
    if not entry or not entry.get('print'):
        assert not name.startswith('v101-') or not name.endswith('.svg'), ('Unregistered prepared SVG', name)
        return None
    record = entry['print']
    target = (IMAGES / record['file']).resolve()
    assert target.is_relative_to((IMAGES / 'print').resolve()), ('Print path escapes print directory', name)
    assert target.name == name, ('Print filename differs', name)
    for path, digest in ((IMAGES / name, record['source_sha256']), (target, record['sha256'])):
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == digest, f'Prepared artwork is stale: {path.relative_to(ROOT)}; rerun its edition generator and register hashes'
    return target


def apply_figure_class(figure, filename):
    entry = entries().get(filename)
    if entry:
        figure['class'] = ['book-figure', 'figure-' + entry['layout']]
        figure['data-book-visual'] = filename
    return entry
