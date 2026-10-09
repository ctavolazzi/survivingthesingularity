"""List every font embedded in a PDF, including inside form XObjects.

SVG figures are drawn as form XObjects, so a scan of page-level text runs
never sees their fonts. This walks every resource dictionary instead.

    python3 docs/v0.9.2/fonts_check.py book.pdf --allow BookSans BookSerif JetBrains-Mono
Exits 1 if any font family outside --allow is embedded.
"""
import argparse
from pypdf import PdfReader


def fonts(pdf):
    """Names of all embedded fonts. (WeasyPrint shares one font dictionary
    across pages, so a per-page count would say nothing.)"""
    found, seen = set(), set()

    def walk(resources):
        if resources is None:
            return
        resources = resources.get_object()
        for ref in (resources.get('/Font') or {}).values():
            found.add(str(ref.get_object().get('/BaseFont', '?')).lstrip('/').split('+')[-1])
        for ref in (resources.get('/XObject') or {}).values():
            xobj = ref.get_object()
            if id(xobj) not in seen:
                seen.add(id(xobj))
                if '/Resources' in xobj:
                    walk(xobj['/Resources'])

    for page in PdfReader(pdf).pages:
        walk(page.get('/Resources'))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('--allow', nargs='+', required=True, help='allowed family prefixes')
    args = ap.parse_args()
    found = fonts(args.pdf)
    bad = {name for name in found if not name.startswith(tuple(args.allow))}
    for name in sorted(found):
        print(('! ' if name in bad else '  ') + name)
    print(f'{len(bad)} font(s) outside the allowed families')
    raise SystemExit(1 if bad else 0)


if __name__ == '__main__':
    main()
