"""Reuse production instruments, never previous-edition findings or counts."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name):
    meta = json.loads((ROOT / 'src/lib/data/book/book.json').read_text())
    if meta['version'] != '0.11.0':
        raise RuntimeError('This wrapper requires canonical edition 0.11.0')
    path = ROOT / 'docs/v0.10.4' / (name + '.py')
    spec = importlib.util.spec_from_file_location('sts_v110_' + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.HERE = HERE
    if name == 'prove_epub_layout':
        module.OUT = HERE / 'epub-proof'
        module.PREVIOUS_CHECK = ROOT / 'docs/v0.10.4/epub-checks.json'
    return module
