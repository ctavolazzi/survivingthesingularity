"""Verify preserved reference edition and accounted-for final source changes."""
from pathlib import Path
import difflib
import hashlib
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'src/lib/data/book'
sha=lambda data:hashlib.sha256(data).hexdigest()


def require_hash(data,expected):
    assert sha(data)==expected,'Source receipt mismatch'


def undo_art(text,name,changes):
    for change in reversed(changes):
        if change['file']!=name:continue
        assert text.count(change['after'])==1,(name,change['asset'])
        text=text.replace(change['after'],change['before'],1)
    return text


def main():
    before=json.loads((HERE/'baseline.json').read_text())
    reviewed=json.loads((HERE/'reviewed-prose.json').read_text())
    art=json.loads((HERE/'art-integration.json').read_text())
    parent=Path(before['parent_worktree']);old=parent/'src/lib/data/book'
    # A changed reference or unrecorded final sentence must be rejected.
    name=next(iter(reviewed['files']));sample=(SOURCE/name).read_text()
    restored=undo_art(sample,name,art['caption_changes'])
    controls=[]
    for label,data,digest in [('changed reference', (old/'book.json').read_bytes()+b'\n',before['files']['book.json']),
                              ('unrecorded sentence', (restored+'\nUnrecorded sentence.\n').encode(),reviewed['files'][name])]:
        try:require_hash(data,digest)
        except AssertionError:controls.append(label)
        else:raise AssertionError('Negative control stayed green: '+label)
    for name,digest in before['files'].items():require_hash((old/name).read_bytes(),digest)
    for record in before['deliveries']:require_hash((parent/record['path']).read_bytes(),record['sha256'])
    meta=json.loads((SOURCE/'book.json').read_text());prior=json.loads((old/'book.json').read_text())
    assert meta['version']=='0.10.2' and meta['sections']==prior['sections']
    assert set(reviewed['files'])=={s['file'] for s in meta['sections']}
    records=[];diff=[]
    for section in meta['sections']:
        name=section['file'];current=(SOURCE/name).read_text();previous=(old/name).read_text()
        require_hash(undo_art(current,name,art['caption_changes']).encode(),reviewed['files'][name])
        refs=lambda t:re.findall(r'\]\(/book-images/([^\s)]+)\)',t)
        assert refs(current)==refs(previous),(name,'image references changed')
        records.append({'file':name,'before_sha256':sha(previous.encode()),'after_sha256':sha(current.encode()),'changed':current!=previous,'image_references':len(refs(current))})
        diff.extend(difflib.unified_diff(previous.splitlines(True),current.splitlines(True),fromfile='v0.10.1/'+name,tofile='v0.10.2/'+name))
    registry=json.loads((SOURCE/'visuals.json').read_text())
    assert registry['edition']=='0.10.2' and set(registry['images'])==set(art['expected_registered'])
    report={'edition':'0.10.2','sections':records,'changed_sections':sum(x['changed'] for x in records),'preserved_reference_files':len(before['files']),
            'preserved_deliveries':len(before['deliveries']),'image_references':sum(x['image_references'] for x in records),'registered_figures':len(registry['images']),
            'negative_controls':controls,'limits':'Checks reference preservation and review receipts, not the truth of source claims or rendered output.'}
    (HERE/'source-review.json').write_text(json.dumps(report,indent=2)+'\n')
    (HERE/'source-changes.diff').write_text(''.join(diff))
    print(json.dumps({k:v for k,v in report.items() if k!='sections'}))


if __name__=='__main__':main()
