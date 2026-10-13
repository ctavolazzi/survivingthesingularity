"""Integrate reviewed SVG pairs, canonical descriptions and edition metadata.

Run once after the four figure generators and their proofs. Subsequent builds
use the recorded hashes; they do not run historical artwork generators.
"""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from reconstruct_reviewed import reconstruct

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BOOK=ROOT/'src/lib/data/book'
IMAGES=ROOT/'static/book-images'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def save(path,value):
    text=json.dumps(value,indent=2,ensure_ascii=False)+'\n'
    path.write_text(text);assert path.read_text()==text


def main():
    assert not (HERE/'art-integration.json').exists(), 'Integration already recorded; inspect before rerunning'
    meta=json.loads((BOOK/'book.json').read_text())
    prior=Path(json.loads((HERE/'baseline.json').read_text())['parent_worktree'])
    registry=json.loads((prior/'src/lib/data/book/visuals.json').read_text())
    inherited=list(registry['images'])
    changes=[]
    for owner in ['opening','middle','ending','core']:
        records=json.loads((HERE/f'art-{owner}-changes.json').read_text())
        if owner=='opening':
            records=[dict(record,file=name,generator=records['generator'],
                kind='chart' if name in ('intro-food-insecurity.svg','ch05-horses-tractors.svg') else 'conceptual',
                pixels=record['dimensions'],screen_sha256=record['after']['source_sha256'],print_sha256=record['after']['print_sha256'])
                for name,record in records['figures'].items()]
        elif owner=='ending':
            records=[dict(record,generator=record['source'],pixels=record['dimensions'],
                provenance=' '.join(record['provenance']),kind='chart' if record['kind']=='historical_timeline' else record['kind'],
                screen_sha256=record['screen']['sha256'],print_sha256=record['print']['sha256']) for record in records['figures']]
        changes.extend(records)
    assert len(changes)==len({c['file'] for c in changes})==31
    texts=reconstruct()
    prose=[]
    for change in changes:
        name=change['file'];source=IMAGES/name;light=IMAGES/'print'/name
        assert sha(source)==change['screen_sha256'],name
        assert sha(light)==change['print_sha256'],name
        assert (ROOT/change['generator']).exists()
        registry['images'][name]={'layout':'diagram','kind':change['kind'],'pixels':change['pixels'],
            'print':{'file':'print/'+name,'source_sha256':sha(source),'sha256':sha(light)}}
        pattern=re.compile(r'!\[([^\]]*)\]\(/book-images/'+re.escape(name)+r'\)\n\n\*([^\n]+)\*')
        matches=[(filename,m) for filename,text in texts.items() for m in pattern.finditer(text)]
        assert len(matches)==1,(name,len(matches))
        filename,m=matches[0]
        default_alt=ET.fromstring(source.read_text()).find('{http://www.w3.org/2000/svg}desc')
        alt=change.get('recommended_alt',default_alt.text if default_alt is not None else m[1])
        caption=change.get('recommended_caption',m[2])
        caption=caption.replace('\\u2019',"'")
        if name=='ch15-soil-food-web.svg':
            caption='The soil food web cycles nutrients. Harvest and other losses remove them, so a productive bed still needs measurement and appropriate replenishment.'
        after=f'![{alt}](/book-images/{name})\n\n*{caption}*'
        assert '\u2014' not in after and '\n' not in alt
        if after!=m[0]:
            prose.append({'file':filename,'asset':name,'before':m[0],'after':after})
            texts[filename]=texts[filename].replace(m[0],after,1)
    registry['edition']='0.10.2'
    # All catalog descriptions are copies of canonical captions, never another source.
    catalog=json.loads((BOOK/'art-catalog.json').read_text())
    by_name={Path(x['figure']).name:x for x in catalog['assets'] if x.get('figure')}
    rights_path=ROOT/'docs/publication/asset-rights.json'
    rights=json.loads(rights_path.read_text());rights_by_name={x['file']:x for x in rights['assets']}
    revised={c['file']:c for c in changes}
    refs=[]
    for section,text in texts.items():
        for m in re.finditer(r'!\[([^\]]*)\]\(/book-images/([^\s)]+)\)\n\n\*([^\n]+)\*',text):
            alt,name,caption=m.groups();refs.append(name)
            assert name in by_name,(name,'catalog missing')
            entry=by_name[name];entry['alt']=alt;entry['caption']=caption
            record=rights_by_name[name];record['caption']=caption;record['section']=section
            record['line']=text[:m.start()].count('\n')+1
            if name in revised:
                c=revised[name]
                entry['label']=ET.parse(IMAGES/name).getroot().find('{http://www.w3.org/2000/svg}title').text
                entry['provenance']={'edition':'0.10.2','kind':c['kind'],'tool':'Python-authored native SVG','record':c['generator'],'review':'docs/v0.10.2/ART-AUDIT.md'}
                record.update({'sha256':sha(IMAGES/name),'audited_for':'v0.10.2','kind':'original_svg','size':c['pixels'],
                    'format':'SVG','basis':c['provenance'],'creation_record':c['generator'],'print_variant':registry['images'][name]['print']})
    assert len(refs)==99,len(refs) # Three part dividers intentionally have no captions.
    all_refs=[name for text in texts.values() for name in re.findall(r'!\[[^\]]*\]\(/book-images/([^\s)]+)\)',text)]
    assert len(all_refs)==102,len(all_refs)
    catalog['generated']='2026-09-28'
    catalog['provenance']['v0.10.2']='31 existing native SVGs revised for legible print labels and agreement with reviewed prose. Per-asset generators and before/after records are in docs/v0.10.2. Earlier image-generation provenance remains unchanged.'
    for name,text in texts.items():
        path=BOOK/name;path.write_text(text);assert path.read_text()==text
    save(BOOK/'visuals.json',registry)
    save(BOOK/'art-catalog.json',catalog)
    rights.update({'edition':'0.10.2','checked_at':'2026-09-28','scope':'Inherited rights audit with hashes and descriptions synchronized for 31 original SVG revisions and all canonical captions. No new third-party images. Prior cover and quotation limits remain unchanged.'})
    save(rights_path,rights)
    save(HERE/'art-integration.json',{'edition':'0.10.2','inherited_registered':inherited,'revised':[c['file'] for c in changes],
         'expected_registered':list(registry['images']),'caption_changes':prose,'canonical_image_references':len(all_refs),
         'limits':'Records asset and text synchronization. Geometry, content and final-page proofs are separate.'})
    print('Integrated',len(changes),'revised SVGs;',len(registry['images']),'registered figures;',len(prose),'alt/caption changes')


if __name__=='__main__':main()
