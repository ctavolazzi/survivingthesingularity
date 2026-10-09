"""Reconstruct the editorial review checkpoint from exact recorded changes."""
from pathlib import Path
import hashlib
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def apply_unified(original,diff):
    source=original.splitlines(True);out=[];cursor=0
    lines=diff.splitlines(True);index=0
    while index<len(lines):
        match=re.match(r'@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@',lines[index])
        if not match:index+=1;continue
        start=int(match[1])-1
        assert start>=cursor
        out.extend(source[cursor:start]);cursor=start;index+=1
        while index<len(lines) and not lines[index].startswith('@@ '):
            line=lines[index];prefix=line[:1]
            if prefix in (' ','-'):
                assert source[cursor]==line[1:],(cursor,line)
                if prefix==' ':out.append(source[cursor])
                cursor+=1
            elif prefix=='+':out.append(line[1:])
            else:raise AssertionError('Unsupported diff line: '+line)
            index+=1
    out.extend(source[cursor:]);return ''.join(out)


def reconstruct():
    baseline=json.loads((HERE/'baseline.json').read_text())
    prior=Path(baseline['parent_worktree'])/'src/lib/data/book'
    checkpoint=json.loads((HERE/'reviewed-prose.json').read_text())['files']
    texts={name:(prior/name).read_text() for name in checkpoint}
    for section in json.loads((HERE/'opening-changes.json').read_text())['sections']:
        name=Path(section['file']).name
        if section.get('unified_diff'):texts[name]=apply_unified(texts[name],section['unified_diff'])
    for owner in ('middle','ending'):
        records=json.loads((HERE/f'{owner}-changes.json').read_text())
        if isinstance(records,dict):records=records['changes']
        for change in records:
            name=Path(change['file']).name
            assert texts[name].count(change['before'])==1,(owner,name)
            texts[name]=texts[name].replace(change['before'],change['after'],1)
    for name,text in texts.items():
        assert hashlib.sha256(text.encode()).hexdigest()==checkpoint[name],name
    return texts


if __name__=='__main__':print('Reconstructed',len(reconstruct()),'reviewed sections, all hashes match')
