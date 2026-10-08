"""Render independently identified edition additions with production refs."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

from bs4 import BeautifulSoup
from check_source_preservation import ENDING_AFTER

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def additions():
    report = json.loads((HERE / 'source-preservation.json').read_text())
    assert not report['errors'] and report['version'] == '0.11.0'
    for name, digest in report['current_source_sha256'].items():
        assert hashlib.sha256((ROOT / 'src/lib/data/book' / name).read_bytes()).hexdigest() == digest, 'Stale source preservation report: ' + name
    assert hashlib.sha256((ROOT / 'src/lib/data/book/manuscript-index.json').read_bytes()).hexdigest() == report['index_sha256'], 'Stable-ID sidecar changed since source preservation proof'
    sys.path.insert(0, str(ROOT / 'scripts'))
    spec = importlib.util.spec_from_file_location('sts_additions_refs', ROOT / 'scripts/sts.py')
    resolver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resolver)
    targets = resolver._ref_targets(resolver._live_index())
    records = []
    for section in report['sections']:
        selected = list(section['added_blocks'])
        if section['file'] == '21-conclusion.md':
            selected.append(ENDING_AFTER)
        for index, block in enumerate(selected, 1):
            expanded = resolver._expand_refs(block, targets, section['file'])
            html = subprocess.run(['pandoc', '--from=markdown', '--to=html5'], input=expanded,
                                  text=True, capture_output=True, check=True).stdout
            doc = BeautifulSoup(html, 'html.parser')
            nodes = [{'tag': node.name, 'text': node.get_text('', strip=False)}
                     for node in doc.select('p, li, th, td, h1, h2, h3, h4')]
            if nodes:
                records.append({'file': section['file'], 'block': index, 'nodes': nodes})
    return report, records
