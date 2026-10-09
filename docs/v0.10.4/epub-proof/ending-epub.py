"""Check and capture revised ending passages from the actual packaged EPUB."""
from pathlib import Path
import hashlib
import json
import mimetypes
import subprocess
from urllib.parse import unquote, urlsplit
import zipfile

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
HERE = OUT.parent
META = json.loads((ROOT / 'src/lib/data/book/book.json').read_text())
EPUB = ROOT / 'book-build' / f'Surviving-the-Singularity-v{META["version"]}.epub'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    check = json.loads((HERE / 'epub-checks.json').read_text())
    assert check['epub_sha256'] == digest(EPUB)
    assert check['version'] == META['version']
    assert not any(check[key] for key in ('missing_blocks', 'resource_errors', 'art_errors'))
    for name, expected in check['source_sha256'].items():
        assert digest(ROOT / 'src/lib/data/book' / name) == expected
    review = json.loads((HERE / 'ending-review.json').read_text())
    chapter_for = {item['section']: item['chapter'] for item in check['artwork']}
    with zipfile.ZipFile(EPUB) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}
    report = {'version': META['version'], 'epub_sha256': digest(EPUB),
              'structural_report_sha256': digest(HERE / 'epub-checks.json'),
              'viewports': [390, 768], 'measurements': [], 'captures': [],
              'missing_requests': [], 'negative_controls': [],
              'scope': 'All six changed ending passages from packaged EPUB XHTML and CSS, with JavaScript disabled. Text and horizontal bounds checked; screenshots support separate visual inspection.'}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel='chrome', headless=True)
        report['browser'] = browser.version
        context = browser.new_context(java_script_enabled=False)

        def route(request):
            path = unquote(urlsplit(request.request.url).path).lstrip('/')
            if path not in files:
                report['missing_requests'].append(path)
                request.abort()
                return
            request.fulfill(status=200, body=files[path], content_type=mimetypes.guess_type(path)[0] or 'application/octet-stream')

        context.route('**/*', route)
        page = context.new_page()

        def find(expected):
            index = page.locator('p,li,h2').evaluate_all('''(nodes, expected) => {
                const norm = value => value.normalize('NFKC').replace(/\\s+/g, ' ').trim();
                return nodes.findIndex(node => norm(node.textContent) === norm(expected));
            }''', expected)
            assert index >= 0, ('Missing revised text', expected)
            return page.locator('p,li,h2').nth(index)

        for width in report['viewports']:
            page.set_viewport_size({'width': width, 'height': 1000})
            for index, edit in enumerate(review['edits'], 1):
                name = Path(edit['file']).name
                chapter = chapter_for[name]
                html = subprocess.run(['pandoc', '--from=markdown', '--to=html5'], input=edit['after'], capture_output=True, text=True, check=True).stdout
                expected = BeautifulSoup(html, 'html.parser').find(['li', 'p', 'h2']).get_text()
                page.goto('http://epub.local/' + chapter, wait_until='networkidle')
                node = find(expected)
                node.scroll_into_view_if_needed()
                measurement = node.evaluate('''element => {
                    const box = element.getBoundingClientRect();
                    return {text: element.textContent, bounds: box.toJSON(), viewport: innerWidth,
                            horizontal_overflow: box.left < -.5 || box.right > innerWidth + .5,
                            visible: getComputedStyle(element).visibility !== 'hidden' && box.width > 0 && box.height > 0};
                }''')
                assert measurement['visible'] and not measurement['horizontal_overflow']
                if width == 390 and index == 1:
                    original = node.inner_html()
                    node.evaluate("element => {element.textContent = 'Deliberately missing expected passage';}")
                    caught = False
                    try:
                        find(expected)
                    except AssertionError:
                        caught = True
                    assert caught, 'Changed-text negative control stayed green'
                    node.evaluate('(element, html) => {element.innerHTML = html;}', original)
                    find(expected)
                    report['negative_controls'].append({'control': 'actual packaged passage replaced in browser', 'rejected': True, 'restored': True})
                capture = OUT / f'ending-epub-{index}-{width}.png'
                node.screenshot(path=str(capture))
                report['captures'].append({'file': str(capture.relative_to(ROOT)), 'sha256': digest(capture), 'edit': index, 'width': width})
                report['measurements'].append({'edit': index, 'source': name, 'chapter': chapter, 'width': width, **measurement})
        browser.close()
    assert not report['missing_requests']
    assert digest(EPUB) == report['epub_sha256']
    report['status'] = 'pass'
    (OUT / 'ending-epub.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'status': report['status'], 'measurements': len(report['measurements']), 'captures': len(report['captures']), 'negative_controls': len(report['negative_controls'])}))


if __name__ == '__main__':
    main()
