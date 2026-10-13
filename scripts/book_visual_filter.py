#!/usr/bin/env python3
"""Pandoc JSON filter: registered book art, accessible stills, manual captions."""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
VISUALS = json.loads((ROOT/'src/lib/data/book/visuals.json').read_text())['images']


def images(node):
    if isinstance(node, dict):
        if node.get('t') == 'Image':
            yield node
        for value in node.values():
            yield from images(value)
    elif isinstance(node, list):
        for value in node:
            yield from images(value)


def transform(blocks):
    result = []
    index = 0
    while index < len(blocks):
        block = blocks[index]
        if block.get('t') == 'RawBlock' and block['c'][0] == 'html' and re.fullmatch(r'\s*<!--[\s\S]*?-->\s*', block['c'][1]):
            index += 1
            continue
        if block.get('t') == 'Figure':
            pictures = list(images(block))
            if len(pictures) == 1:
                name = Path(unquote(urlsplit(pictures[0]['c'][2][0]).path)).name
                entry = VISUALS.get(name)
                if entry:
                    block['c'][0][1] += ['book-figure', 'figure-' + entry['layout']]
                    if index+1 < len(blocks):
                        following = blocks[index+1]
                        if following.get('t') == 'Para' and len(following['c']) == 1 and following['c'][0].get('t') == 'Emph':
                            block['c'][1] = [None, [{'t':'Plain','c':following['c'][0]['c']}]]
                            index += 1
        result.append(block)
        index += 1
    return result


def main():
    document = json.load(sys.stdin)
    document['blocks'] = transform(document['blocks'])
    json.dump(document, sys.stdout)


if __name__ == '__main__':
    main()
