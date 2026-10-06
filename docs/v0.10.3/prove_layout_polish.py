"""Bounded before/after pagination proofs using the preceding edition's HTML.

No complete book build and no writes to prior editions. Run again after a full
build to supplement these isolated reproductions with the final PDF review.
"""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

from bs4 import BeautifulSoup
from weasyprint import HTML

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / 'layout-proof'
BASE = Path(json.loads((HERE / 'baseline.json').read_text())['parent_worktree'])
OLD_HTML = BASE / 'publication/output/interior.html'
OLD_CSS = BASE / 'publication/book.css'
NEW_CSS = ROOT / 'publication/book.css'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def body_words(page):
    return ' '.join(b.text for b in page._page_box.descendants()
                    if type(b).__name__ == 'TextBox' and 55 < b.position_y < 796)


def render(fragment, css):
    text = f'<html lang="en-US"><head><link rel="stylesheet" href="{css.as_uri()}"></head><body><main>{fragment}</main></body></html>'
    return HTML(string=text, base_url=BASE.as_uri()).render()


def relocate(soup, filename, before):
    figure = soup.find('img', src=lambda value: value and value.endswith(filename)).find_parent('figure')
    target = next(node for node in soup.find_all(['h2', 'p'])
                  if ' '.join(node.get_text().split()).startswith(before))
    target.insert_before(figure.extract())


def preserve(before, after):
    assert Counter(before.stripped_strings) == Counter(after.stripped_strings)
    assert Counter(i['src'] for i in before.find_all('img')) == Counter(i['src'] for i in after.find_all('img'))


def run():
    OUT.mkdir(exist_ok=True)
    source = BeautifulSoup(OLD_HTML.read_text(), 'html.parser')
    result = {'scope': 'Isolated prior-edition HTML fragments, not final new-edition pagination',
              'prior_html_sha256': digest(OLD_HTML), 'prior_css_sha256': digest(OLD_CSS),
              'new_css_sha256': digest(NEW_CSS), 'cases': {}}
    cases = [
        ('chapter19', ['sec-chapter18', 'sec-chapter19'], 'ch19-conversion-ladder.svg', 'Rung 1:'),
        ('greenhouse', ['sec-chapter9'], 'ch09-greenhouse-bus.svg', 'A worked example: one delivery'),
        ('ledger', ['sec-appendix-d'], 'appd-precedent-timeline.svg', 'The rules, in one breath each'),
    ]
    for name, ids, filename, anchor in cases:
        original = BeautifulSoup(''.join(str(source.find(id=sid)) for sid in ids), 'html.parser')
        revised = copy.deepcopy(original)
        relocate(revised, filename, anchor)
        preserve(original, revised)
        before = render(str(original), OLD_CSS)
        after = render(str(revised), NEW_CSS)
        before_text = [body_words(p) for p in before.pages]
        after_text = [body_words(p) for p in after.pages]
        item = {'before_pages': len(before.pages), 'after_pages': len(after.pages),
                'same_text_and_images': True,
                'before_body_words': [len(t.split()) for t in before_text],
                'after_body_words': [len(t.split()) for t in after_text]}
        if name == 'chapter19':
            # The prior layout is the failing control, observed before repair.
            assert '' in before_text and '' not in after_text
            assert any(t.startswith('CHAPTER 19') and len(t.split()) < 15 for t in before_text)
            opening = next(i for i,t in enumerate(after_text) if t.startswith('CHAPTER 19'))
            assert 'The county chambers' in after_text[opening]
            item['negative_control_blank_and_title_only_observed'] = True
            item['after_opening_includes_story'] = True
            after.copy([after.pages[opening]]).write_pdf(OUT / 'after-fragment-chapter19-opening.pdf')
        elif name == 'greenhouse':
            heading = 'The greenhouse brain'
            before_open = next(t for t in before_text if heading in t)
            after_open = next(t for t in after_text if heading in t)
            assert len(before_open.split()) < 50
            assert 'Sensors:' in after_open and 'Actuators:' in after_open
            assert len(after_open.split()) > 200 and 'PID' in after_open and 'manual valve' in after_open
            item['negative_control_orphaned_heading_observed'] = True
            item['after_heading_includes_component_explanation'] = True
            index = next(i for i,t in enumerate(after_text) if heading in t)
            after.copy([after.pages[index]]).write_pdf(OUT / 'after-fragment-greenhouse.pdf')
        else:
            assert 'How to run the Ledger' not in before_text[0]
            assert 'How to run the Ledger' in after_text[0]
            item['negative_control_opening_only_observed'] = True
            item['after_opening_includes_procedure'] = True
            after.copy([after.pages[0]]).write_pdf(OUT / 'after-fragment-ledger-opening.pdf')
        result['cases'][name] = item
        print(name, item['before_pages'], '->', item['after_pages'], flush=True)
    # Exercise the actual builder's heading block without importing its build.
    build = (ROOT / 'publication/build.py').read_text()
    block = build[build.index('    original_h1 ='):build.index('    for fig in soup.find_all')]
    import textwrap
    def make(tag, attrs=None, text=None):
        node = BeautifulSoup('', 'html.parser').new_tag(tag, attrs=attrs or {})
        if text is not None:
            node.string = text
        return node
    for title, label in [('How to Use This Book', None), ('Chapter 19: The Ladder', 'Chapter 19')]:
        soup = BeautifulSoup(f'<h1>{title}</h1>', 'html.parser')
        exec(textwrap.dedent(block), {'soup': soup, 'section': {'title': title}, 'make': make})
        eyebrow = soup.select_one('.chapter-label')
        assert (eyebrow.get_text() if eyebrow else None) == label
        assert len(soup.find_all('h1')) == 1
    result['cases']['heading'] = {'unnumbered_title_once': True, 'numbered_label_retained': True}
    # Test the credits change with the same prior entries, isolating spacing.
    credits = copy.deepcopy(source.find(id='image-credits'))
    before = render(str(credits), OLD_CSS)
    paras = credits.find_all('p', recursive=False)
    wrapper = BeautifulSoup('', 'html.parser').new_tag('div', attrs={'class': 'credits-closing'})
    paras[-2].insert_before(wrapper)
    wrapper.append(paras[-2].extract())
    wrapper.append(paras[-1].extract())
    after = render(str(credits), NEW_CSS)
    result['cases']['credits'] = {'before_pages': len(before.pages), 'after_pages': len(after.pages),
                                  'before_last_page_words': len(body_words(before.pages[-1]).split()),
                                  'after_last_page_words': len(body_words(after.pages[-1]).split()),
                                  'final_provenance_grouped': True}
    assert len(after.pages) < len(before.pages)
    after.copy([after.pages[-1]]).write_pdf(OUT / 'after-fragment-credits-final.pdf')
    (OUT / 'fragment-checks.json').write_text(json.dumps(result, indent=2) + '\n')
    assert json.loads((OUT / 'fragment-checks.json').read_text()) == result
    print('All bounded layout checks passed. Final assembled PDF still requires review.')


if __name__ == '__main__':
    run()
