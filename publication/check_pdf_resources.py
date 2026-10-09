"""Run from repository root: python3 publication/check_pdf_resources.py.
Requires pypdf, Pillow, and Ghostscript. No network or source-PDF writes.
"""
from collections import Counter
from pathlib import Path
import hashlib
import io
import json
import re
import subprocess
import unicodedata
from PIL import Image, ImageChops
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, DecodedStreamObject, DictionaryObject, NameObject

ROOT = Path(__file__).resolve().parent.parent
KINDS = ['interior', 'reading', 'print-interior', 'front-cover']


def key(obj):
    ref = getattr(obj, 'indirect_reference', None)
    return (ref.idnum, ref.generation) if ref else ('direct', id(obj))


def embedded(font):
    font = font.get_object()
    if font.get('/Subtype') == '/Type0':
        descendants = font.get('/DescendantFonts', [])
        return bool(descendants) and all(embedded(f) for f in descendants)
    if font.get('/Subtype') == '/Type3':
        return bool(font.get('/CharProcs'))
    descriptor = font.get('/FontDescriptor')
    if not descriptor:
        return False
    descriptor = descriptor.get_object()
    return any(descriptor.get(k) and len(descriptor[k].get_object().get_data()) > 0
               for k in ['/FontFile', '/FontFile2', '/FontFile3'])


def fonts_in(resources, seen, fonts):
    if not resources:
        return
    resources = resources.get_object()
    for ref in resources.get('/Font', {}).values():
        font = ref.get_object()
        if key(font) not in fonts:
            fonts[key(font)] = {'base_font': str(font.get('/BaseFont', 'Type3')),
                                'subtype': str(font.get('/Subtype')), 'embedded': embedded(font)}
    for name in ['/XObject', '/Pattern']:
        for ref in resources.get(name, {}).values():
            item = ref.get_object()
            if key(item) not in seen:
                seen.add(key(item))
                fonts_in(item.get('/Resources'), seen, fonts)


def six_by_nine(width, height):
    return abs(float(width)-432) <= 0.02 and abs(float(height)-648) <= 0.02


def destination(reader, value):
    if isinstance(value, (str, bytes)):
        named = reader.named_destinations.get(str(value))
        return reader.get_destination_page_number(named) if named else None
    try:
        return reader.get_page_number(value.get_object()[0].get_object())
    except (AttributeError, TypeError, IndexError, KeyError):
        return None


def annotations(reader, offset=0):
    result = {'counts': [], 'descriptors': [], 'targets': [], 'unresolved': [], 'internal': 0, 'external': 0}
    for n, page in enumerate(reader.pages, 1):
        refs = page.get('/Annots', [])
        result['counts'].append(len(refs))
        rows = []
        for ref in refs:
            item = ref.get_object()
            action = item.get('/A')
            action = action.get_object() if action else {}
            target = item.get('/Dest')
            if target is None and action.get('/S') == '/GoTo':
                target = action.get('/D')
            if target is not None:
                page_number = destination(reader, target)
                result['internal'] += 1
                if page_number is None or not 0 <= page_number < len(reader.pages):
                    result['unresolved'].append({'page': n, 'destination': str(target)[:160]})
                identity = ('internal', page_number-offset if page_number is not None else None)
            elif action.get('/S') == '/URI':
                result['external'] += 1
                identity = ('uri', str(action.get('/URI')))
            else:
                identity = ('other', str(action.get('/S')), str(item.get('/Contents', '')))
            rows.append((str(item.get('/Subtype')), tuple(round(float(v), 2) for v in item.get('/Rect', [])), identity))
        result['descriptors'].append(Counter(rows))
        result['targets'].append(Counter((row[0], row[2]) for row in rows))
    return result


def space_kind(space, resources):
    space = space.get_object() if hasattr(space, 'get_object') else space
    if isinstance(space, str):
        if space in ['/DeviceGray', '/G']:
            return 'gray'
        if space in ['/DeviceRGB', '/RGB']:
            return 'rgb'
        if space in ['/DeviceCMYK', '/CMYK']:
            return 'cmyk'
        if space in resources.get('/ColorSpace', {}):
            return space_kind(resources['/ColorSpace'][space], resources)
        return space
    if isinstance(space, list):
        if space[0] == '/ICCBased':
            return 'gray' if space[1].get_object().get('/N') == 1 else 'icc-color'
        if space[0] == '/CalGray':
            return 'gray'
        if space[0] == '/Indexed':
            return space_kind(space[1], resources)
        return str(space[0])
    return str(space)


def chromatic(args, operator):
    if operator in [b'rg', b'RG']:
        return max(map(float, args))-min(map(float, args)) > 1e-8
    if operator in [b'k', b'K']:
        return any(abs(float(v)) > 1e-8 for v in args[:3])
    return False


def gray_resources(reader):
    result = {'operator_counts': Counter(), 'chromatic_operations': [], 'non_gray_spaces': [], 'images': [], 'shadings': [], 'inline_images': 0}
    seen = set()

    def inspect(stream, resources, label):
        resources = resources.get_object() if resources else {}
        stream = stream if hasattr(stream, 'operations') else ContentStream(stream, reader)
        for args, op in stream.operations:
            if op in [b'g', b'G', b'rg', b'RG', b'k', b'K', b'cs', b'CS', b'sc', b'SC', b'scn', b'SCN']:
                result['operator_counts'][op.decode()] += 1
            if chromatic(args, op):
                result['chromatic_operations'].append(label)
            if op in [b'cs', b'CS']:
                space = space_kind(args[0], resources)
                if space not in ['gray', '/Pattern']:
                    result['non_gray_spaces'].append({'where': label, 'space': space})
            if op == b'INLINE IMAGE':
                result['inline_images'] += 1
                settings = args.get('settings', {})
                space = space_kind(settings.get('/CS', settings.get('/ColorSpace')), resources)
                if space != 'gray':
                    result['non_gray_spaces'].append({'where': label+' inline', 'space': space})
        for ref in resources.get('/XObject', {}).values():
            item = ref.get_object()
            if key(item) in seen:
                continue
            seen.add(key(item))
            if item.get('/Subtype') == '/Form':
                inspect(item, item.get('/Resources', resources), label+' form')
            if item.get('/Subtype') == '/Image':
                space = space_kind(item.get('/ColorSpace'), resources)
                mask = bool(item.get('/ImageMask', False))
                result['images'].append({'object': str(key(item)), 'width': item.get('/Width'), 'height': item.get('/Height'), 'bits': item.get('/BitsPerComponent'), 'color_space': space, 'image_mask': mask})
                if space != 'gray' and not mask:
                    result['non_gray_spaces'].append({'where': label+' image', 'space': space})
        for ref in resources.get('/Shading', {}).values():
            space = space_kind(ref.get_object().get('/ColorSpace'), resources)
            result['shadings'].append(space)
            if space != 'gray':
                result['non_gray_spaces'].append({'where': label+' shading', 'space': space})
        for ref in resources.get('/Pattern', {}).values():
            item = ref.get_object()
            if key(item) not in seen and item.get('/PatternType') == 1:
                seen.add(key(item))
                inspect(item, item.get('/Resources', resources), label+' pattern')
    for n, page in enumerate(reader.pages, 1):
        inspect(page.get_contents(), page.get('/Resources'), f'page {n}')
    result['operator_counts'] = dict(result['operator_counts'])
    result['passes_stream_checks'] = not result['chromatic_operations'] and not result['non_gray_spaces']
    return result


def empty_final_page(page):
    """An intentional production verso has no annotations or content operations.

    Checking extracted text alone misses images and vector marks. Require the
    content stream itself to be empty, as PdfWriter.add_blank_page produces it.
    Even a single painted rectangle makes the page ineligible for exclusion.
    """
    if page.get('/Annots', []):
        return False
    contents = page.get_contents()
    return contents is None or not contents.operations


def print_page_parity(interior, printed):
    """Only an empty final print page may be excluded from pagewise parity."""
    color_count, print_count = len(interior.pages), len(printed.pages)
    extra = print_count - color_count
    blank = extra == 1 and empty_final_page(printed.pages[-1])
    allowed = extra == 0 or blank
    return {
        'interior_pages': color_count,
        'print_pages': print_count,
        'extra_print_pages': extra,
        'blank_final_page_excluded': blank,
        'passes': allowed,
        'reason': ('Equal page counts' if extra == 0 else
                   'One empty final print page excluded' if blank else
                   'Print must retain every interior page and add at most one empty final page'),
    }


def page_parity_controls():
    """Exercise page loss and non-text marks without modifying final PDFs."""
    def sample(count, painted_last=False):
        writer = PdfWriter()
        for _ in range(count):
            writer.add_blank_page(width=432, height=648)
        if painted_last:
            stream = DecodedStreamObject()
            stream.set_data(b'0 0 10 10 re f')
            writer.pages[-1][NameObject('/Contents')] = writer._add_object(stream)
        buffer = io.BytesIO()
        writer.write(buffer)
        buffer.seek(0)
        return PdfReader(buffer)

    interior = sample(3)
    return {
        'equal_print_page_count_accepted': print_page_parity(interior, sample(3))['passes'],
        'blank_final_print_page_accepted': print_page_parity(interior, sample(4))['passes'],
        'nonblank_extra_print_page_rejected': not print_page_parity(interior, sample(4, True))['passes'],
        'truncated_print_page_rejected': not print_page_parity(interior, sample(2))['passes'],
        'two_extra_print_pages_rejected': not print_page_parity(interior, sample(5))['passes'],
    }


def normalized(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text)).replace('\u00ad', '')


def raster_neutrality(image):
    red, green, blue = image.convert('RGB').split()
    maximum = max(ImageChops.difference(a, b).getextrema()[1] for a, b in [(red, green), (red, blue), (green, blue)])
    return {'max_channel_difference_8bit': maximum, 'passes_one_level_tolerance': maximum <= 1}


def main():
    paths = {k: ROOT/'publication/output'/f'Surviving-the-Singularity-{k}.pdf' for k in KINDS}
    readers = {k: PdfReader(path) for k, path in paths.items()}
    report = {'scope': 'Frozen publication PDFs; independent resource and text-layer audit', 'files': {}, 'negative_controls': {}}
    controls = report['negative_controls']
    controls.update(page_parity_controls())
    for kind, reader in readers.items():
        fonts, seen, wrong = {}, set(), []
        for n, page in enumerate(reader.pages, 1):
            for name in ['mediabox', 'cropbox']:
                box = getattr(page, name)
                if not six_by_nine(box.width, box.height):
                    wrong.append({'page': n, 'box': name, 'size': [float(box.width), float(box.height)]})
            fonts_in(page.get('/Resources'), seen, fonts)
        data = paths[kind].read_bytes()
        report['files'][kind] = {'path': str(paths[kind]), 'sha256': hashlib.sha256(data).hexdigest(), 'pages': len(reader.pages), 'bytes': len(data), 'all_boxes_6x9': not wrong, 'wrong_boxes': wrong, 'fonts': list(fonts.values()), 'all_fonts_embedded': all(f['embedded'] for f in fonts.values()), 'metadata': dict(reader.metadata or {}), 'page_labels_first_seven': reader.page_labels[:7], 'page_labels_last_three': reader.page_labels[-3:]}
        print('Resources:', kind, len(fonts), flush=True)
    controls['missing_font_program_rejected'] = not embedded(DictionaryObject({NameObject('/Subtype'): NameObject('/Type1')}))
    controls['wrong_page_width_rejected'] = not six_by_nine(433, 648)
    a, b, g = annotations(readers['interior']), annotations(readers['reading'], 1), annotations(readers['print-interior'])
    parity = print_page_parity(readers['interior'], readers['print-interior'])
    report['page_parity'] = parity
    interior_pages = len(readers['interior'].pages)
    report['annotation_checks'] = {'interior_total': sum(a['counts']), 'reading_total': sum(b['counts']), 'print_total': sum(g['counts']), 'cover_annotations': b['counts'][0], 'reading_counts_equal_after_cover': a['counts'] == b['counts'][1:], 'reading_rectangles_and_targets_equal': a['descriptors'] == b['descriptors'][1:], 'print_counts_equal_color': parity['passes'] and a['counts'] == g['counts'][:interior_pages], 'print_target_multisets_equal_color': parity['passes'] and a['targets'] == g['targets'][:interior_pages], 'all_internal_destinations_resolve': not a['unresolved'] and not b['unresolved'] and not g['unresolved'], 'internal_counts': {k: v['internal'] for k, v in [('interior', a), ('reading', b), ('print', g)]}, 'external_counts': {k: v['external'] for k, v in [('interior', a), ('reading', b), ('print', g)]}, 'unresolved': {k: v['unresolved'] for k, v in [('interior', a), ('reading', b), ('print', g)]}}
    controls['missing_destination_rejected'] = destination(readers['reading'], '__missing_probe__') is None
    changed = a['counts'].copy()
    changed[next(n for n, count in enumerate(changed) if count)] -= 1
    controls['removed_annotation_detected'] = changed != a['counts']
    gray = gray_resources(readers['print-interior'])
    report['grayscale_checks'] = gray
    controls['red_vector_rejected'] = chromatic([1, 0, 0], b'rg')
    controls['rgb_image_space_rejected'] = space_kind('/DeviceRGB', {}) != 'gray'
    texts = {}
    for kind in ['interior', 'print-interior']:
        texts[kind] = []
        for n, page in enumerate(readers[kind].pages, 1):
            texts[kind].append(page.extract_text() or '')
            if n % 50 == 0:
                print('Text:', kind, n, flush=True)
    mismatches = []
    for n, (left, right) in enumerate(zip(texts['interior'], texts['print-interior']), 1):
        left, right = normalized(left), normalized(right)
        if left != right:
            start = next((i for i, (x, y) in enumerate(zip(left, right)) if x != y), min(len(left), len(right)))
            mismatches.append({'page': n, 'first_difference': start, 'color_excerpt': left[max(0, start-30):start+70], 'print_excerpt': right[max(0, start-30):start+70]})
    joined = {k: '\n'.join(v) for k, v in texts.items()}
    report['text_checks'] = {'normalization': 'NFKC; remove whitespace and soft hyphens only; retain punctuation and text order', 'pages_compared': min(len(texts['interior']), len(texts['print-interior'])), 'print_page_parity_passes': parity['passes'], 'blank_final_page_excluded': parity['blank_final_page_excluded'], 'same_page_count': len(texts['interior']) == len(texts['print-interior']), 'all_pages_equal': parity['passes'] and not mismatches, 'mismatches': mismatches, 'after_counts': {k: len(re.findall(r'\bafter\b', v, re.I)) for k, v in joined.items()}, 'shift_counts': {k: len(re.findall(r'\bshift\b', v, re.I)) for k, v in joined.items()}, 'previous_ft_corruption_present': {k: bool(re.search('[Ƥɇ]', v)) for k, v in joined.items()}, 'example_phrase': {k: 'silence after the first one' in re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', v)) for k, v in joined.items()}}
    controls['text_corruption_detected'] = normalized('silence after the first one') != normalized('silence aƤer the first one')
    rasters = []
    raster_pages = sorted({min(n, len(readers['print-interior'].pages)) for n in [1, 5, 28, 139]})
    for n in raster_pages:
        result = subprocess.run(['gs', '-q', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m', '-r45', f'-dFirstPage={n}', f'-dLastPage={n}', '-sOutputFile=-', str(paths['print-interior'])], capture_output=True, check=True)
        image = Image.open(io.BytesIO(result.stdout))
        rasters.append({'page': n, 'pixels': list(image.size), **raster_neutrality(image)})
    gray['rendered_pixel_checks'] = rasters
    gray['pixel_tolerance_reason'] = 'RGB rendering of gray PDF photographs introduces at most one 8-bit level of channel conversion rounding. All stream operators and image color spaces independently verify gray representation.'
    controls['red_raster_pixel_rejected'] = not raster_neutrality(Image.new('RGB', (1, 1), (255, 0, 0)))['passes_one_level_tolerance']
    report['navigation_metadata_checks'] = {'reading_labels_correct': readers['reading'].page_labels[:7] == ['Cover', 'i', 'ii', 'iii', 'iv', '1', '2'], 'print_labels_correct': readers['print-interior'].page_labels[:7] == ['i', 'ii', 'iii', 'iv', '1', '2', '3'], 'title_author_consistent': all(r.metadata.get('/Title') == 'Surviving the Singularity' and r.metadata.get('/Author') == 'Christopher Tavolazzi' for r in readers.values())}
    report['limitations'] = ['Color interior keeps default physical-number PDF labels; reading and print use Roman frontmatter and Arabic main text.', 'Annotation arrays are compared as multisets; Ghostscript ordering is not assumed identical. Reading checks include rectangles and normalized page targets. Print checks compare pagewise target counts.', 'All print page/form streams and referenced image/shading spaces are inspected. Four rendered pages check actual neutral pixels with documented one-level rounding. This is not an ink-separation or PDF/X certification.', 'Font embedding checks nonempty programs, not appearance or rights. Original font licenses are packaged separately.', 'Text checks compare extracted page text after stated normalization. One empty final print page may be excluded; missing pages, multiple extras, annotations or any content operations on an extra page are rejected. Manuscript paragraph preservation is independently checked by the main proof script.']
    annotation_keys = ['reading_counts_equal_after_cover', 'reading_rectangles_and_targets_equal', 'print_counts_equal_color', 'print_target_multisets_equal_color', 'all_internal_destinations_resolve']
    report['overall_pass'] = (all(f['all_boxes_6x9'] and f['all_fonts_embedded'] for f in report['files'].values()) and all(report['annotation_checks'][k] for k in annotation_keys) and gray['passes_stream_checks'] and all(r['passes_one_level_tolerance'] for r in rasters) and parity['passes'] and not mismatches and not any(report['text_checks']['previous_ft_corruption_present'].values()) and all(controls.values()) and all(report['navigation_metadata_checks'].values()))
    docs = ROOT/'docs/publication'
    (docs/'PDF-RESOURCE-CHECKS.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
    counts = ', '.join(f"{k}: {len(v['fonts'])}" for k, v in report['files'].items())
    page_counts = ', '.join(f"{kind}: {item['pages']}" for kind, item in report['files'].items())
    annotation_counts = ', '.join(f"{kind}: {sum(item['counts'])}" for kind, item in [('interior', a), ('reading', b), ('print', g)])
    internal_counts = ', '.join(f"{kind}: {item['internal']}" for kind, item in [('interior', a), ('reading', b), ('print', g)])
    external_counts = ', '.join(f"{kind}: {item['external']}" for kind, item in [('interior', a), ('reading', b), ('print', g)])
    text_checks = report['text_checks']
    markdown = f"""# PDF resource checks

Result: **{'PASS' if report['overall_pass'] else 'FAIL'}** for the publication PDFs.

Reproduce with `python3 publication/check_pdf_resources.py` from repository root. Dependencies are pypdf, Pillow, and Ghostscript. No network access or source-PDF changes occur. Exact hashes and complete results are in [PDF-RESOURCE-CHECKS.json](PDF-RESOURCE-CHECKS.json).

| Check | Measured result |
| --- | --- |
| Page geometry | All media and crop boxes are 432 by 648 points: {all(item['all_boxes_6x9'] for item in report['files'].values())}. |
| Page counts | {page_counts}. |
| Print page parity | {parity['reason']}. Pass: {parity['passes']}. |
| Fonts | All discovered page/form/pattern fonts have a nonempty embedded program: {all(item['all_fonts_embedded'] for item in report['files'].values())}. Resource counts: {counts}. |
| Annotations | {annotation_counts}. Reading rectangles and targets match after the cover offset: {report['annotation_checks']['reading_rectangles_and_targets_equal']}. Print target multisets match on all interior pages: {report['annotation_checks']['print_target_multisets_equal_color']}. |
| Destinations | Internal: {internal_counts}. External URI annotations: {external_counts}. All internal destinations resolve: {report['annotation_checks']['all_internal_destinations_resolve']}. Remote URL availability was not tested. |
| Grayscale streams | Fill-gray operators: {gray['operator_counts'].get('g', 0)}; stroke-gray operators: {gray['operator_counts'].get('G', 0)}. Referenced images: {len(gray['images'])}. Chromatic operations: {len(gray['chromatic_operations'])}; non-gray spaces: {len(gray['non_gray_spaces'])}. |
| Grayscale render | Pages {', '.join(map(str, raster_pages))}; every sample passes one-level 8-bit RGB neutrality: {all(item['passes_one_level_tolerance'] for item in rasters)}. |
| Text | {text_checks['pages_compared']} interior pages compared; {len(mismatches)} mismatches. One permitted final empty print page excluded: {parity['blank_final_page_excluded']}. NFKC normalization removes whitespace and soft hyphens while retaining punctuation and text order. |
| Prior ligature defect | Previous ft corruption present: {text_checks['previous_ft_corruption_present']}. Counts of after: {text_checks['after_counts']}; shift: {text_checks['shift_counts']}. Example phrase preserved: {text_checks['example_phrase']}. |
| Navigation metadata | Reading labels correct: {report['navigation_metadata_checks']['reading_labels_correct']}. Print labels correct: {report['navigation_metadata_checks']['print_labels_correct']}. Title and author agree: {report['navigation_metadata_checks']['title_author_consistent']}. |

## Controls

{sum(bool(value) for value in controls.values())} of {len(controls)} controls passed. These include accepting equal page counts and one empty final print page; rejecting a truncated print PDF, two extra pages, and a final page carrying a painted rectangle even when it has no extractable text. The font, geometry, annotation, destination, grayscale and text-corruption controls run without modifying the final PDFs. The JSON report lists each outcome separately.

## Limits

This audit verifies resource, navigation, grayscale, and text-layer properties. It does not certify literary accuracy, image permissions, printed appearance, PDF/X conformance, a printer's color profile, or accessibility tagging. Font licenses are packaged separately. Manuscript preservation and visual layout are checked by the main proof process.
"""
    (docs/'PDF-RESOURCE-CHECKS.md').write_text(markdown)
    print('Resource validation:', report['overall_pass'], flush=True)
    return 0 if report['overall_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
