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
import posixpath
from urllib.parse import unquote, urlsplit
import zipfile

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = HERE / 'epub-proof'
SOURCE = ROOT / 'src/lib/data/book'
META = json.loads((SOURCE / 'book.json').read_text())
EPUB = ROOT / 'book-build' / f'Surviving-the-Singularity-v{META["version"]}.epub'
PREVIOUS_CHECK = ROOT / 'docs/v0.10.3/epub-checks.json'
METRICS = '''() => [...document.querySelectorAll('figure.book-figure')].map(figure => {
 const image = figure.querySelector('img'), caption = figure.querySelector('figcaption');
 const bounds = element => {
   if (!element) return null;
   const rect=element.getBoundingClientRect();
   return {x:rect.x,y:rect.y,width:rect.width,height:rect.height,right:rect.right};
 };
 return {src:image?.getAttribute('src') || '', alt:image?.alt || '',
         figure:bounds(figure), image:bounds(image), caption:bounds(caption),
         float:getComputedStyle(figure).float, complete:image?.complete || false,
         naturalWidth:image?.naturalWidth || 0, viewport:innerWidth,
         captionText:caption?.textContent.trim() || ''};
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
            if bounds is None:
                if kind != 'caption' or record['caption_required']:
                    errors.append(f'missing {kind}')
                continue
            if bounds['width'] <= 0 or bounds['height'] <= 0 or bounds['x'] < -0.5 or bounds['right'] > record['viewport'] + 0.5:
                errors.append(f'{kind} outside viewport or empty')
        if record['caption_required'] and not record['captionText']:
            errors.append('empty required caption')
        if record['caption'] and record['image'] and record['caption']['y'] < record['image']['y'] + record['image']['height'] - 0.5:
            errors.append('caption overlaps image')
    return errors


def main():
    OUT.mkdir(exist_ok=True)
    check = json.loads((HERE / 'epub-checks.json').read_text())
    digest = hashlib.sha256(EPUB.read_bytes()).hexdigest()
    assert check['epub_sha256'] == digest, 'Run the structural check on this EPUB first'
    assert check['version'] == META['version'], 'Structural report covers a different edition'
    assert not any(check[key] for key in ('missing_blocks', 'resource_errors', 'art_errors')), 'Structural check has unresolved errors'
    current_hashes = {name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
                      for name in check['source_sha256']}
    frozen = json.loads((ROOT / 'docs/publication/baseline.json').read_text())
    assert current_hashes == check['source_sha256'] == frozen, 'Source or freeze changed since structural check'
    registry_bytes = (SOURCE / 'visuals.json').read_bytes()
    assert hashlib.sha256(registry_bytes).hexdigest() == check['registry_sha256'], 'Registry changed since structural check'
    visuals = json.loads(registry_bytes)['images']
    with zipfile.ZipFile(EPUB) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}
    registered = [record for record in check['artwork'] if record['registered']]
    assert {record['file'] for record in registered} == set(visuals), 'Structural report does not cover current registry'
    by_chapter = {}
    for record in registered:
        assert record['embedded'], ('Registered artwork is not embedded', record['file'])
        by_chapter.setdefault(record['chapter'], []).append(record)
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
    photographed = set()
    previous = json.loads(PREVIOUS_CHECK.read_text())
    previous_registered = {record['file'] for record in previous['artwork'] if record['registered']}
    added_assets = set(visuals) - previous_registered
    representatives = {
        'v103-reading-routes.svg', 'v103-first-year-index.svg',
        'ch12-csa-network.svg', 'ch14-logistic-shockwave.svg', 'ch15-soil-food-web.svg', 'ch17-algae-loop.svg', 'ch13-shell-architecture.svg', 'intro-nine-stages.svg', 'appd-precedent-timeline.svg', 'v101-cutout-atlas.png', 'v101-cutout-printer.png', 'v101-cutout-spot.png',
        'v101-chart-data-centre-demand.svg', 'v101-chart-waste-pathways.svg',
        'v101-chart-weights-memory.svg', 'v101-scene-food-delivery.svg',
        'v101-scene-living-soil.svg', 'v101-scene-shared-workshop.svg',
    } | added_assets
    assert representatives <= set(visuals), ('Unregistered screenshot representatives', sorted(representatives - set(visuals)))
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
        def measurements_for(chapter):
            expected = {embedded: record for record in by_chapter[chapter] for embedded in record['embedded']}
            measurements = page.evaluate(METRICS)
            for measurement in measurements:
                embedded = posixpath.normpath(posixpath.join(posixpath.dirname(chapter), unquote(urlsplit(measurement['src']).path)))
                assert embedded in expected, ('Unexpected registered figure resource', chapter, measurement['src'])
                source = expected[embedded]
                measurement.update({'file': source['file'], 'caption_required': source['caption_required']})
            assert Counter(item['file'] for item in measurements) == Counter(item['file'] for item in by_chapter[chapter]), ('Registered figure placements differ', chapter)
            return measurements
        chapters = list(by_chapter)
        for width in (390, 768):
            page.set_viewport_size({'width': width, 'height': 1000})
            count = 0
            for chapter in chapters:
                page.goto('http://epub.local/' + chapter, wait_until='networkidle')
                measurements = measurements_for(chapter)
                count += len(measurements)
                failures.extend({'chapter': chapter, 'width': width, 'error': error} for error in defects(measurements))
                for index, measurement in enumerate(measurements):
                    asset = measurement['file']
                    records.append({'chapter': chapter, 'width': width, **measurement})
                    if (width == 768 and asset in representatives) or asset in added_assets:
                        output = OUT / f'{Path(asset).stem}-{width}.png'
                        page.locator('figure.book-figure').nth(index).screenshot(path=str(output))
                        screenshots.append(str(output.relative_to(ROOT)))
                        photographed.add(asset)
            assert count == len(registered), (width, count)
        # Defect uses the same EPUB DOM and measurement path as the positive proof.
        # add_style_tag waits for a page event that does not fire with page JS off.
        # DevTools evaluation can set inline properties synchronously instead.
        page.evaluate('''() => document.querySelectorAll('figure.book-figure').forEach(figure => {
          figure.style.setProperty('width', '150vw', 'important');
          figure.style.setProperty('max-width', 'none', 'important');
          figure.style.setProperty('float', 'left', 'important');
        })''')
        assert defects(measurements_for(chapter)), 'Overflow/float negative control stayed green'
        browser.close()
    assert photographed == representatives, ('Missing representative screenshots', sorted(representatives - photographed))
    report = {'version': META['version'], 'epub_sha256': digest, 'browser': f'Chrome {version}', 'javascript_disabled': True,
              'viewports': [390, 768], 'registered_figures_per_viewport': len(registered),
              'registry_entries': len(visuals),
              'caption_required_figures_per_viewport': sum(record['caption_required'] for record in registered),
              'uncaptioned_source_figures_per_viewport': sum(not record['caption_required'] for record in registered),
              'measurements': records, 'layout_errors': failures, 'missing_requests': requested_missing,
              'cutout_alpha': alpha, 'screenshots': screenshots,
              'screenshot_representatives': sorted(representatives),
              'new_art_screenshot_widths': [390, 768],
              'added_registry_assets': sorted(added_assets), 'comparison_edition': previous['version'],
              'negative_controls': ['actual EPUB figure given 150vw width and left float'],
              'limits': 'Chrome reflow of packaged XHTML/CSS; not dedicated EPUB-reader pagination or physical-device acceptance.'}
    (OUT / 'checks.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'measurements'}, indent=2))
    assert not failures, failures
    assert not requested_missing, requested_missing


if __name__ == '__main__':
    main()
