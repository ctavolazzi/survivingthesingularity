"""Register v0.10.1 artwork, source adaptations, print variants, and credits."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / 'src/lib/data/book'
ART = ROOT / 'static/book-images'
def read(path): return json.loads(path.read_text())
def write(path, value): path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    registry = read(BOOK / 'visuals.json')['images']
    prompts = {p['output']: p for p in read(ROOT / 'docs/v0.10.1/image-prompts.json')['items']}
    spec = importlib.util.spec_from_file_location('sts', ROOT / 'scripts/sts.py')
    sys.path.insert(0, str(ROOT / 'scripts'))
    sts = importlib.util.module_from_spec(spec)
    sys.modules['sts'] = sts
    spec.loader.exec_module(sts)
    index = sts._build_index(BOOK, read(BOOK / 'manuscript-index.json'))
    figures = sts._figure_records(BOOK, index)
    by_name = {Path(f['image']).name: f for f in figures}
    rights_path = ROOT / 'docs/publication/asset-rights.json'
    rights = read(rights_path)
    assets = {a['file']: a for a in rights['assets']}
    credits = read(ART / 'credits.json')
    credit_by_name = {c['file']: c for c in credits}
    catalog = read(BOOK / 'art-catalog.json')
    catalog_by_id = {a['id']: a for a in catalog['assets']}
    summary = []
    for name, visual in registry.items():
        f = by_name[name]
        entry = {
            'file': name, 'path': 'static/book-images/' + name,
            'section': f['file'], 'caption': f['caption'], 'sha256': sha(ART / name),
            'audited_for': 'v0.10.1', 'status': 'retain', 'size': visual['pixels'],
            'catalog_id': f['art_id'], 'kind': visual['kind'],
        }
        provenance = {'edition': '0.10.1', 'kind': visual['kind']}
        if name in prompts:
            p = prompts[name]
            source = assets[p['source']]
            assert source['status'] == 'retain'
            entry.update({k: source[k] for k in ('artist','license','license_url','source_url','title')})
            entry['kind'] = 'photo_adaptation'
            entry['format'] = 'PNG'
            entry['title'] = 'Photo-derived editorial illustration: ' + source['title'].removeprefix('File:')
            entry['source_file'] = p['source']
            entry['source_sha256'] = source['sha256']
            entry['modification_note'] = 'AI-adapted using built-in image_gen. Background removed; subject details regenerated. Tools and launch plume recomposed where applicable. Actual alpha transparency; resized for layout and converted to grayscale in print. This illustration is not an unchanged documentary photograph.'
            entry['generation_record'] = 'docs/v0.10.1/image-prompts.json'
            entry['basis'] = 'Adapted from the retained source named here; the source attribution and license remain attached to the adaptation. Prior source verification is recorded on the original asset, not asserted for these generated pixels.'
            entry['required_credit'] = ' | '.join([entry[k] for k in ('title','artist','license','source_url','license_url','modification_note')])
            if 'BY-SA' in entry['license']:
                entry['derivative_license_note'] = 'This image adaptation remains available under CC BY-SA 4.0. This does not relicense the independent book text.'
            credit_by_name[name] = {'file': name, 'source_title': entry['title'], 'page': entry['source_url'], 'artist': entry['artist'], 'license': entry['license']}
            provenance.update({'tool': 'built-in image_gen', 'source': p['source'], 'source_sha256': source['sha256'], 'license': entry['license'], 'prompt_record': entry['generation_record'], 'adaptation': True})
        else:
            entry['kind'] = 'original_svg'
            entry['format'] = 'SVG'
            entry['basis'] = 'Original code-authored illustration for this edition. Charts distinguish source estimates, forecasts, derived arithmetic, and illustrative worksheets. Scene stills use the same Three.js geometry as the interactive reader.'
            entry['creation_record'] = ('docs/v0.10.1/chart-data.json' if visual['kind']=='chart' else 'docs/v0.10.1/scenes/render-manifest.json' if visual['kind']=='scene' else 'docs/v0.10.1/vignettes.py')
            entry['print_variant'] = copy.deepcopy(visual['print'])
            provenance.update({'tool': 'Three.js 0.168.0 and SVGRenderer' if visual['kind']=='scene' else 'Python-authored SVG', 'record': entry['creation_record']})
        assets[name] = entry
        c = catalog_by_id[f['art_id']]
        c.update({'alt':f['alt'], 'caption':f['caption'], 'label':name.removeprefix('v101-').rsplit('.',1)[0].replace('-',' ').title(), 'provenance':provenance})
        if not c.get('concepts'):
            c['concepts'] = [name.removeprefix('v101-chart-').removeprefix('v101-visual-').rsplit('.',1)[0]]
        summary.append({'file':name,'kind':entry['kind'],'sha256':entry['sha256'],'catalog_id':f['art_id']})
    # Refresh captions for existing records without discarding their provenance.
    for f in figures:
        if f['art_id'] in catalog_by_id:
            catalog_by_id[f['art_id']].update({'alt':f['alt'],'caption':f['caption']})
    rights.update({'edition':'0.10.1','checked_at':'2026-09-28','scope':'Inherited v0.10.0 audit plus 23 visual additions: six credited photo-derived AI adaptations and seventeen original SVGs with verified print variants. Prior cover and quotation limits remain unchanged.'})
    rights['assets'] = list(assets.values())
    write(rights_path, rights)
    write(ART / 'credits.json', list(credit_by_name.values()))
    catalog['provenance']['v0.10.1'] = 'Six photo-derived alpha illustrations edited with built-in image_gen; eight charts, six conceptual SVGs, and three Three.js scenes. Per-asset records name sources and licenses; historical PixelLab provenance remains on earlier assets.'
    write(BOOK / 'art-catalog.json', catalog)
    write(ROOT / 'docs/v0.10.1/art-registration.json', {'version':'0.10.1','figures':len(figures),'additions':summary})
    assert read(rights_path)['edition']=='0.10.1'
    assert len(summary)==23 and len(figures)==102
    print('Registered 23 additions; 102 manuscript figures.')
if __name__ == '__main__': main()
