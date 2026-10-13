"""Run actual PDF prose/geometry proof and bind its receipt to current bytes."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'publication/output'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = json.loads((HERE / 'source-preservation.json').read_text())
    assert source['version'] == '0.11.0' and not source['errors']
    for name, expected in source['current_source_sha256'].items():
        assert digest(ROOT / 'src/lib/data/book' / name) == expected, 'Stale source receipt: ' + name
    build = json.loads((OUT / 'build.json').read_text())
    assert build['source_sha256'] == source['current_source_sha256'], 'Build covers different canonical source'
    outputs = {kind: {'path': record['path'], 'sha256': record['sha256']}
               for kind, record in build['outputs'].items()}
    for record in outputs.values():
        path = Path(record['path'])
        assert digest(path if path.is_absolute() else OUT / path) == record['sha256']
    subprocess.run([sys.executable, 'publication/proof.py'], cwd=ROOT, check=True)
    proof = json.loads((OUT / 'proof/checks.json').read_text())
    report = {'version': source['version'], 'checked_utc': datetime.now(timezone.utc).isoformat(),
              'source_sha256': source['current_source_sha256'], 'outputs': outputs,
              'source_rendered_sha256': digest(OUT / 'source-rendered.html'),
              'geometry_sha256': digest(OUT / 'interior-layout.json'),
              'proof_sha256': digest(OUT / 'proof/checks.json'),
              'source_text_blocks_checked': proof['source_text_blocks_checked'],
              'status': 'pass', 'limits': proof['limits']}
    target = HERE / 'pdf-checks.json'
    target.write_text(json.dumps(report, indent=2) + '\n')
    assert json.loads(target.read_text()) == report
    print(json.dumps({'version': report['version'], 'status': report['status'],
                      'source_text_blocks_checked': report['source_text_blocks_checked']}))


if __name__ == '__main__':
    main()
