"""Narrow page XObject dictionaries without changing nested resources or content.

WeasyPrint shares the entire book's image/form dictionary across all pages.
Ghostscript repeatedly prepares those unused objects. This preparation step
keeps only names invoked by each page's Do operators, preserving indirect
references. It rejects forms, tiling patterns or Type3 fonts that depend on an
inherited resource scope. The color master is never rewritten.
"""
from pathlib import Path
import hashlib
import time

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject, DecodedStreamObject, DictionaryObject, IndirectObject, NameObject,
    NumberObject,
)

try:
    from .check_pdf_resources import annotations
except ImportError:
    from check_pdf_resources import annotations


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def nested_scopes(writer):
    """Return immutable fingerprints; fail on unknown or inherited scopes."""
    scopes = []
    for obj in writer._objects:
        if not isinstance(obj, DictionaryObject):
            continue
        nested = (obj.get('/Subtype') in ['/Form', '/Type3']
                  or obj.get('/PatternType') == 1)
        if nested:
            if '/Resources' not in obj:
                raise ValueError('Resource pruning refuses a form, pattern or Type3 font with inherited resources')
            resources = obj['/Resources']
            if not isinstance(resources, DictionaryObject):
                raise ValueError('Unknown nested resource representation')
            scopes.append((id(obj), repr(resources)))
        if obj.get('/Type') == '/XObject' and obj.get('/Subtype') not in ['/Form', '/Image']:
            raise ValueError(f"Unknown XObject subtype: {obj.get('/Subtype')}")
    return scopes


def called_xobjects(page):
    content = page.get_contents()
    return {args[0] for args, op in content.operations if op == b'Do'} if content is not None else set()


def retained_references(original, selected, used):
    for name in used:
        if name not in original or name not in selected:
            raise ValueError(f'Referenced XObject missing: {name}')
        old, new = original.raw_get(name), selected.raw_get(name)
        if not isinstance(old, IndirectObject) or not isinstance(new, IndirectObject):
            raise ValueError(f'XObject must remain an indirect reference: {name}')
        if old != new:
            raise ValueError(f'Referenced XObject changed: {name}')


def prune_page(page):
    resources = page['/Resources']
    original = resources.get('/XObject', DictionaryObject()).get_object()
    used = called_xobjects(page)
    # Dictionary indexing dereferences streams. Iterating items preserves the
    # original indirect objects and avoids invalid direct streams in Resources.
    selected = DictionaryObject({name: ref for name, ref in original.items() if name in used})
    retained_references(original, selected, used)
    replacement = DictionaryObject(resources)
    replacement[NameObject('/XObject')] = selected
    page[NameObject('/Resources')] = replacement
    return len(original), len(selected)


def controls():
    writer = PdfWriter()
    page = writer.add_blank_page(width=432, height=648)
    form = DecodedStreamObject()
    form.set_data(b'0 0 10 10 re f')
    form[NameObject('/Type')] = NameObject('/XObject')
    form[NameObject('/Subtype')] = NameObject('/Form')
    form[NameObject('/BBox')] = ArrayObject([NumberObject(n) for n in [0, 0, 10, 10]])
    form[NameObject('/Resources')] = DictionaryObject()
    ref = writer._add_object(form)
    original = DictionaryObject({NameObject('/Used'): ref, NameObject('/Unused'): ref})
    page[NameObject('/Resources')] = DictionaryObject({NameObject('/XObject'): original})
    content = DecodedStreamObject()
    content.set_data(b'/Used Do')
    page[NameObject('/Contents')] = writer._add_object(content)
    before, after = prune_page(page)
    selected = page['/Resources']['/XObject']
    result = {'referenced_object_retained': '/Used' in selected and before == 2 and after == 1}
    for label, bad in [
        ('removed_reference_rejected', DictionaryObject()),
        ('direct_stream_rejected', DictionaryObject({NameObject('/Used'): form})),
    ]:
        try:
            retained_references(original, bad, called_xobjects(page))
        except ValueError:
            result[label] = True
        else:
            result[label] = False
    del form[NameObject('/Resources')]
    try:
        nested_scopes(writer)
    except ValueError:
        result['inherited_scope_rejected'] = True
    else:
        result['inherited_scope_rejected'] = False
    if not all(result.values()):
        raise AssertionError(f'Resource pruning controls failed: {result}')
    return result


def prepare(source, target):
    start = time.monotonic()
    source, target = Path(source), Path(target)
    if source.resolve() == target.resolve():
        raise ValueError('Prepared PDF must not overwrite the color master')
    source_hash = digest(source)
    source_reader = PdfReader(source)
    writer = PdfWriter(clone_from=source)
    scopes_before = nested_scopes(writer)
    totals = [0, 0]
    for page in writer.pages:
        before, after = prune_page(page)
        totals[0] += before
        totals[1] += after
    if scopes_before != nested_scopes(writer):
        raise ValueError('A nested resource scope changed during page pruning')
    writer.write(target)
    prepared = PdfReader(target)
    if len(source_reader.pages) != len(prepared.pages):
        raise ValueError('Prepared PDF lost pages')
    for n, (original, output) in enumerate(zip(source_reader.pages, prepared.pages), 1):
        original_content, output_content = original.get_contents(), output.get_contents()
        left = original_content.get_data() if original_content is not None else b''
        right = output_content.get_data() if output_content is not None else b''
        if left != right:
            raise ValueError(f'Page {n}: content stream changed')
        missing = called_xobjects(output) - set(output['/Resources']['/XObject'])
        if missing:
            raise ValueError(f'Page {n}: referenced XObjects missing after write: {missing}')
        for ref in output['/Resources']['/XObject'].values():
            if not isinstance(ref, IndirectObject):
                raise ValueError(f'Page {n}: direct XObject after write')
    if annotations(source_reader)['descriptors'] != annotations(prepared)['descriptors']:
        raise ValueError('Prepared PDF annotations changed')
    if digest(source) != source_hash:
        raise ValueError('Color master changed during resource preparation')
    return {
        'input_sha256': source_hash,
        'prepared_path': str(target),
        'prepared_sha256': digest(target),
        'pages': len(prepared.pages),
        'page_xobject_references_before': totals[0],
        'page_xobject_references_after': totals[1],
        'removed_unused_page_references': totals[0]-totals[1],
        'nested_scopes_unchanged': len(scopes_before),
        'page_streams_unchanged': True,
        'annotation_descriptors_unchanged': True,
        'controls': controls(),
        'seconds': round(time.monotonic()-start, 2),
    }
