"""Capture representative figures from the exact packaged EPUB at both widths.

This supplements prove_epub_layout.py without replacing any source or registry.
The saved report identifies EPUB and embedded-resource hashes for visual review.
"""
from pathlib import Path
import hashlib
import json
import mimetypes
from posixpath import dirname, join, normpath
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import zipfile

from playwright.sync_api import sync_playwright
from prove_epub_layout import METRICS, defects

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
OUT=HERE/'epub-proof/manual-samples'
EPUB=ROOT/'book-build/Surviving-the-Singularity-v0.10.2.epub'
SAMPLES={
    'intro-nine-stages.svg', 'ch05-horses-tractors.svg',
    'ch09-greenhouse-bus.svg', 'ch11-cooling-loop.svg',
    'ch12-csa-network.svg', 'ch17-algae-loop.svg',
    'ch19-conversion-ladder.svg', 'appd-precedent-timeline.svg',
    'v101-scene-living-soil.svg', 'v101-cutout-atlas.png',
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    check=json.loads((HERE/'epub-checks.json').read_text())
    layout=json.loads((HERE/'epub-proof/checks.json').read_text())
    epub_hash=digest(EPUB.read_bytes())
    assert epub_hash==check['epub_sha256']==layout['epub_sha256']
    assert not layout['layout_errors'] and not layout['missing_requests']
    with zipfile.ZipFile(EPUB) as z:
        files={name:z.read(name) for name in z.namelist()}
    named={record['embedded'][0]:record['file'] for record in check['artwork'] if record['registered']}
    chapters=list(dict.fromkeys(record['chapter'] for record in check['artwork'] if record['file'] in SAMPLES))
    OUT.mkdir(exist_ok=True)
    records=[]
    missing=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='chrome',headless=True)
        context=browser.new_context(java_script_enabled=False)
        def route(request):
            path=unquote(urlsplit(request.request.url).path).lstrip('/')
            if path not in files:
                missing.append(path)
                request.abort()
                return
            request.fulfill(status=200,body=files[path],content_type=mimetypes.guess_type(path)[0] or 'application/octet-stream')
        context.route('**/*',route)
        page=context.new_page()
        for width in [390,768]:
            page.set_viewport_size({'width':width,'height':1000})
            for chapter in chapters:
                page.goto('http://epub.local/'+chapter,wait_until='networkidle')
                measured=page.evaluate(METRICS)
                assert not defects(measured)
                for index,metric in enumerate(measured):
                    embedded=normpath(join(dirname(chapter),metric['src']))
                    name=named[embedded]
                    if name not in SAMPLES:
                        continue
                    shot=OUT/f'{Path(name).stem}-{width}.png'
                    page.locator('figure.book-figure').nth(index).screenshot(path=str(shot))
                    record={'file':name,'width':width,'chapter':chapter,'embedded':embedded,
                            'embedded_sha256':digest(files[embedded]),'screenshot':str(shot.relative_to(ROOT)),
                            'screenshot_sha256':digest(shot.read_bytes()),'metrics':metric}
                    if name.endswith('.svg'):
                        svg=ET.fromstring(files[embedded])
                        viewbox=list(map(float,svg.attrib['viewBox'].split()))
                        fonts=[float(el.attrib['font-size']) for el in svg.iter() if el.tag.endswith('text') and 'font-size' in el.attrib]
                        record['svg_viewBox']=viewbox
                        record['minimum_explicit_svg_font']=min(fonts) if fonts else None
                        record['minimum_label_css_px_estimate']=min(fonts)*metric['image']['width']/viewbox[2] if fonts else None
                    records.append(record)
        browser.close()
    assert not missing,missing
    assert len(records)==2*len(SAMPLES),(len(records),len(SAMPLES))
    report={'epub_sha256':epub_hash,'viewports':[390,768],'samples':records,
            'missing_requests':missing,
            'limits':'Exact packaged XHTML/CSS/image bytes in Chrome. Font estimates use image width and SVG geometry, not physical-device measurement. Images do not reflow their internal labels when body-text size changes.'}
    target=OUT/'samples.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    assert json.loads(target.read_text())==report
    print(json.dumps({'captured':len(records),'assets':len(SAMPLES),'epub_sha256':epub_hash,
                      'label_css_px_range':{str(width):[round(min(r['minimum_label_css_px_estimate'] for r in records if r['width']==width and r.get('minimum_label_css_px_estimate')),2),round(max(r['minimum_label_css_px_estimate'] for r in records if r['width']==width and r.get('minimum_label_css_px_estimate')),2)] for width in [390,768]}}))


if __name__=='__main__':
    main()
