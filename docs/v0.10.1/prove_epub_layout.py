"""Render actual EPUB XHTML/resources in Chrome at two reflow widths.

No source artwork or publication output is substituted. This is browser evidence,
not a claim about a dedicated e-reader or physical device.
"""
from collections import Counter
from io import BytesIO
import hashlib
import json
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit
import zipfile

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = HERE / 'epub-proof'
EPUB = ROOT / 'book-build/Surviving-the-Singularity-v0.10.1.epub'
METRICS = '''() => [...document.querySelectorAll('figure.book-figure')].map(figure => {
 const image = figure.querySelector('img'), caption = figure.querySelector('figcaption');
 const r=figure.getBoundingClientRect(), i=image.getBoundingClientRect(), c=caption.getBoundingClientRect();
 const bounds = rect => ({x:rect.x,y:rect.y,width:rect.width,height:rect.height,right:rect.right});
 return {src:image.getAttribute('src'), alt:image.alt, figure:bounds(r), image:bounds(i), caption:bounds(c),
         float:getComputedStyle(figure).float, complete:image.complete, naturalWidth:image.naturalWidth,
         viewport:innerWidth, captionText:caption.textContent.trim()};
})'''


def defects(records):
    errors = []
    for record in records:
        if not record['complete'] or not record['naturalWidth']:
            errors.append('unloaded image')
        if record['float'] != 'none':
            errors.append('figure floats')
        for kind in ('figure', 'image', 'caption'):
            bounds = record[kind]
            if bounds['width'] <= 0 or bounds['height'] <= 0 or bounds['x'] < -0.5 or bounds['right'] > record['viewport'] + 0.5:
                errors.append(f'{kind} outside viewport or empty')
        if record['caption']['y'] < record['image']['y'] + record['image']['height'] - 0.5:
            errors.append('caption overlaps image')
    return errors


def main():
    OUT.mkdir(exist_ok=True)
    check = json.loads((HERE / 'epub-checks.json').read_text())
    digest = hashlib.sha256(EPUB.read_bytes()).hexdigest()
    assert check['epub_sha256'] == digest, 'Run the structural check on this EPUB first'
    with zipfile.ZipFile(EPUB) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}
    registered = [record for record in check['artwork'] if record['registered']]
    named = {record['embedded'][0]: record['file'] for record in registered}
    alpha = []
    for record in registered:
        if 'cutout' not in record['file']:
            continue
        picture = Image.open(BytesIO(files[record['embedded'][0]]))
        assert picture.mode == 'RGBA', record['file']
        histogram = picture.getchannel('A').histogram()
        pixels = picture.width * picture.height
        # Generated cutouts can peak at 254; visible pixels need not be fully opaque.
        assert histogram[0] > 0 and sum(histogram[250:]) > 0, record['file']
        alpha.append({'file': record['file'], 'dimensions': list(picture.size),
                      'transparent_fraction': histogram[0] / pixels,
                      'partial_alpha_fraction': sum(histogram[1:255]) / pixels,
                      'near_opaque_fraction': sum(histogram[250:]) / pixels,
                      'max_alpha': picture.getchannel('A').getextrema()[1]})
    records = []
    failures = []
    requested_missing = []
    screenshots = []
    representatives = {
        'v101-cutout-atlas.png', 'v101-cutout-printer.png', 'v101-cutout-spot.png',
        'v101-chart-data-centre-demand.svg', 'v101-chart-waste-pathways.svg',
        'v101-chart-weights-memory.svg', 'v101-scene-food-delivery.svg',
        'v101-scene-living-soil.svg', 'v101-scene-shared-workshop.svg',
    }
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel='chrome', headless=True)
        version = browser.version
        context = browser.new_context(java_script_enabled=False)
        def route(request):
            path = unquote(urlsplit(request.request.url).path).lstrip('/')
            if path not in files:
                requested_missing.append(path)
                request.abort()
                return
            mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
            request.fulfill(status=200, body=files[path], content_type=mime)
        context.route('**/*', route)
        page = context.new_page()
        chapters = list(dict.fromkeys(record['chapter'] for record in registered))
        for width in (390, 768):
            page.set_viewport_size({'width': width, 'height': 1000})
            count = 0
            for chapter in chapters:
                page.goto('http://epub.local/' + chapter, wait_until='networkidle')
                measurements = page.evaluate(METRICS)
                count += len(measurements)
                failures.extend({'chapter': chapter, 'width': width, 'error': error} for error in defects(measurements))
                for index, measurement in enumerate(measurements):
                    # Browser resolves EPUB-relative references exactly as the reader would.
                    from posixpath import normpath, join, dirname
                    asset = named[normpath(join(dirname(chapter), measurement['src']))]
                    records.append({'chapter': chapter, 'width': width, 'file': asset, **measurement})
                    if width == 768 and asset in representatives:
                        output = OUT / f'{Path(asset).stem}-{width}.png'
                        page.locator('figure.book-figure').nth(index).screenshot(path=str(output))
                        screenshots.append(str(output.relative_to(ROOT)))
            assert count == 23, (width, count)
        # Defect uses the same EPUB DOM and measurement path as the positive proof.
        # add_style_tag waits for a page event that does not fire with page JS off.
        # DevTools evaluation can set inline properties synchronously instead.
        page.evaluate('''() => document.querySelectorAll('figure.book-figure').forEach(figure => {
          figure.style.setProperty('width', '150vw', 'important');
          figure.style.setProperty('max-width', 'none', 'important');
          figure.style.setProperty('float', 'left', 'important');
        })''')
        assert defects(page.evaluate(METRICS)), 'Overflow/float negative control stayed green'
        browser.close()
    report = {'epub_sha256': digest, 'browser': f'Chrome {version}', 'javascript_disabled': True,
              'viewports': [390, 768], 'registered_figures_per_viewport': 23,
              'measurements': records, 'layout_errors': failures, 'missing_requests': requested_missing,
              'cutout_alpha': alpha, 'screenshots': screenshots,
              'negative_controls': ['actual EPUB figure given 150vw width and left float'],
              'limits': 'Chrome reflow of packaged XHTML/CSS; not dedicated EPUB-reader pagination or physical-device acceptance.'}
    (OUT / 'checks.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'measurements'}, indent=2))
    assert not failures, failures
    assert not requested_missing, requested_missing


if __name__ == '__main__':
    main()
