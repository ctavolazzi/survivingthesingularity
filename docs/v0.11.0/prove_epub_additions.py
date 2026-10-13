"""Measure every addition's actual EPUB prose at phone and tablet widths."""
from pathlib import Path
import hashlib
import json
import mimetypes
import posixpath
from urllib.parse import unquote, urlsplit
import zipfile

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from _additions import additions

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / 'epub-proof'
EPUB = ROOT / 'book-build/Surviving-the-Singularity-v0.11.0.epub'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source, changes = additions()
    check = json.loads((HERE / 'epub-checks.json').read_text())
    assert check['version'] == source['version'] == '0.11.0'
    assert check['epub_sha256'] == digest(EPUB)
    assert check['source_sha256'] == source['current_source_sha256']
    assert not any(check[key] for key in ('missing_blocks', 'resource_errors', 'art_errors'))
    with zipfile.ZipFile(EPUB) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}
    # TOC covers every canonical section, including text-only Appendix B.
    container = BeautifulSoup(files['META-INF/container.xml'], 'xml')
    opf = container.find('rootfile')['full-path']
    package = BeautifulSoup(files[opf], 'xml')
    nav_item = next(item for item in package.find_all('item') if 'nav' in item.get('properties', '').split())
    nav_path = posixpath.normpath(posixpath.join(posixpath.dirname(opf), unquote(urlsplit(nav_item['href']).path)))
    toc = BeautifulSoup(files[nav_path], 'xml').find('nav', {'epub:type': 'toc'})
    chapters = [posixpath.normpath(posixpath.join(posixpath.dirname(nav_path), unquote(urlsplit(link['href']).path)))
                for link in toc.find_all('a')]
    meta = json.loads((ROOT / 'src/lib/data/book/book.json').read_text())
    assert len(chapters) == len(meta['sections'])
    chapter_for = {section['file']: chapter for section, chapter in zip(meta['sections'], chapters)}
    OUT.mkdir(exist_ok=True)
    report = {'version': source['version'], 'epub_sha256': digest(EPUB), 'viewports': [390, 768],
              'measurements': [], 'captures': [], 'missing_requests': [], 'negative_controls': [],
              'limits': 'Packaged XHTML/CSS in Chrome with JavaScript disabled. Every addition is checked for actual text and bounds; dedicated-reader pagination and physical devices remain untested.'}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel='chrome', headless=True)
        report['browser'] = browser.version
        context = browser.new_context(java_script_enabled=False)

        def route(request):
            name = unquote(urlsplit(request.request.url).path).lstrip('/')
            if name not in files:
                report['missing_requests'].append(name)
                request.abort()
            else:
                request.fulfill(status=200, body=files[name],
                                content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream')

        context.route('**/*', route)
        page = context.new_page()

        def find(expected):
            position = page.locator('p,li,th,td,h1,h2,h3,h4').evaluate_all(r'''(nodes, expected) => {
                const norm = value => value.normalize('NFKC').replace(/\s+/g, ' ').trim();
                return nodes.findIndex(node => norm(node.textContent) === norm(expected));
            }''', expected)
            assert position >= 0, ('Missing new EPUB prose', expected)
            return page.locator('p,li,th,td,h1,h2,h3,h4').nth(position)

        for width in report['viewports']:
            page.set_viewport_size({'width': width, 'height': 1000})
            captured, current_chapter = set(), None
            for change in changes:
                chapter = chapter_for[change['file']]
                if chapter != current_chapter:
                    page.goto('http://epub.local/' + chapter, wait_until='networkidle')
                    current_chapter = chapter
                for expected in change['nodes']:
                    node = find(expected['text'])
                    node.scroll_into_view_if_needed()
                    measurement = node.evaluate('''element => {
                        const box = element.getBoundingClientRect();
                        return {text: element.textContent, bounds: box.toJSON(), viewport: innerWidth,
                                horizontal_overflow: box.left < -.5 || box.right > innerWidth + .5,
                                visible: getComputedStyle(element).visibility !== 'hidden' && box.width > 0 && box.height > 0};
                    }''')
                    assert measurement['visible'] and not measurement['horizontal_overflow'], (change, measurement)
                    report['measurements'].append({'file': change['file'], 'block': change['block'],
                                                   'tag': expected['tag'], 'width': width, **measurement})
                    # Exercise real paragraph text, not only a section heading.
                    if width == 390 and not report['negative_controls'] and expected['tag'] in {'p', 'li'} and len(expected['text']) > 100:
                        original = node.inner_html()
                        node.evaluate("element => {element.textContent = 'Deliberately removed addition';}")
                        try:
                            find(expected['text'])
                        except AssertionError:
                            report['negative_controls'].append('real new EPUB paragraph replaced, rejected, then restored')
                        else:
                            raise AssertionError('New paragraph omission control stayed green')
                        node.evaluate('(element, html) => {element.innerHTML = html;}', original)
                        find(expected['text'])
                    if change['file'] not in captured and expected['tag'] in {'p', 'li'}:
                        target = OUT / (Path(change['file']).stem + f'-additions-{width}.png')
                        page.screenshot(path=str(target))
                        report['captures'].append({'path': str(target.relative_to(ROOT)), 'sha256': digest(target)})
                        captured.add(change['file'])
        browser.close()
    assert report['negative_controls'] and not report['missing_requests']
    assert digest(EPUB) == report['epub_sha256']
    report['status'] = 'pass'
    target = OUT / 'additions.json'
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    assert json.loads(target.read_text()) == report
    print(json.dumps({'version': report['version'], 'status': report['status'],
                      'new_nodes_checked': len(report['measurements']), 'captures': len(report['captures']),
                      'negative_controls': report['negative_controls']}))


if __name__ == '__main__':
    main()
