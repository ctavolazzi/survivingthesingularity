"""Build and prove a readable cast plate from unchanged existing PNG sprites.

Run from any directory with Python, Pillow, Playwright, and Chrome installed.
The SVG viewports exclude transparent margins only. Embedded PNG bytes and
fonts are copied exactly; labels remain editable SVG text. No raster is edited.
"""
from pathlib import Path
import base64
import hashlib
import json
from html import escape
import xml.etree.ElementTree as ET

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
IMAGES = ROOT / 'static/book-images'
PROOF = Path(__file__).parent / 'cast-proof'
WIDTH, HEIGHT = 480, 588
DISPLAY_WIDTH = 4.56 * 96
FONT = 'JetBrains Mono'
CAST = [
    ('elijah', 'ELIJAH', ['Former tech worker', 'Learning to build']),
    ('marta', 'MARTA', ['Fabricator', 'Runs the co-op shop']),
    ('priya', 'PRIYA', ['Soil scientist']),
    ('denny', 'DENNY', ['Former logistics worker', 'Co-op media operator']),
]
PALETTES = {
    'screen': dict(bg='#020617', ink='#f1f5f9', muted='#94a3b8', edge='#334155', accent='#f59e0b'),
    'print': dict(bg='#ffffff', ink='#0f172a', muted='#334155', edge='#cbd5e1', accent='#b45309'),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def data_uri(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def font_css():
    return ''.join(
        f"@font-face{{font-family:'{FONT}';font-weight:{weight};src:url({data_uri(ROOT / f'publication/assets/fonts/JetBrainsMono-{face}.ttf', 'font/ttf')});}}"
        for face, weight in [('Regular', 400), ('SemiBold', 600)]
    )


def label(x, y, value, color, size=13.5, anchor='middle', weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(value)}</text>\n'


def render(mode):
    colors = PALETTES[mode]
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="{FONT},monospace" role="img" aria-labelledby="cast-title cast-desc">\n'
    svg += '<title id="cast-title">The co-op: Elijah, Marta, Priya, and Denny</title>\n'
    svg += '<desc id="cast-desc">Four fictional characters. Elijah is a former tech worker learning to build. Marta is the fabricator running the co-op shop. Priya is a soil scientist. Denny is a former logistics worker and co-op media operator.</desc>\n'
    svg += '<defs><style>' + font_css() + '</style></defs>\n'
    svg += f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{colors["bg"]}"/>\n'
    svg += label(24, 34, 'THE CO-OP', colors['ink'], 19, 'start', 600)
    svg += f'<path d="M24 48H456" stroke="{colors["accent"]}" stroke-width="1.5"/>\n'
    svg += label(24, 70, 'Four people in the story', colors['muted'], anchor='start')
    svg += f'<path d="M240 88V566M24 324H456" stroke="{colors["edge"]}" fill="none"/>\n'
    for index, (slug, name, roles) in enumerate(CAST):
        path = IMAGES / f'sprites/sts-char-{slug}.png'
        with Image.open(path) as picture:
            image_width, image_height = picture.size
            left, top, right, bottom = picture.getchannel('A').getbbox()
        # Padding surrounds every nontransparent pixel; the PNG is unchanged.
        viewport = f'{left-10} {top-10} {right-left+20} {bottom-top+20}'
        center = 128 if index % 2 == 0 else 352
        y = 82 if index < 2 else 332
        svg += f'<svg x="{center-86}" y="{y}" width="172" height="166" viewBox="{viewport}" preserveAspectRatio="xMidYMid meet">\n'
        svg += f'<image id="sprite-{slug}" width="{image_width}" height="{image_height}" href="{data_uri(path, "image/png")}"/>\n</svg>\n'
        svg += label(center, y+192, name, colors['accent'], 18, weight=600)
        svg += ''.join(label(center, y+213+20*i, role, colors['muted']) for i, role in enumerate(roles))
    return svg + '</svg>\n'


METRICS = r'''() => {
    const root=document.querySelector('svg'), rect=root.getBoundingClientRect();
    const texts=[...root.querySelectorAll('text')];
    const boxes=texts.map(t=>{const b=t.getBoundingClientRect();return {text:t.textContent,x:b.x,y:b.y,w:b.width,h:b.height,pt:parseFloat(getComputedStyle(t).fontSize)*rect.width/root.viewBox.baseVal.width*72/96};});
    const overlaps=[];
    for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){
      const a=boxes[i],b=boxes[j];
      if(a.x<b.x+b.w-0.1 && b.x<a.x+a.w-0.1 && a.y<b.y+b.h-0.1 && b.y<a.y+a.h-0.1)overlaps.push([a.text,b.text]);
    }
    const outside=boxes.filter(b=>b.x<rect.x || b.y<rect.y || b.x+b.w>rect.right || b.y+b.h>rect.bottom).map(b=>b.text);
    return {width_in:rect.width/96,height_in:rect.height/96,min_pt:Math.min(...boxes.map(b=>b.pt)),labels:boxes.length,overlaps,outside,sizes:boxes.map(({text,pt})=>({text,pt}))};
}'''


def main():
    PROOF.mkdir(parents=True, exist_ok=True)
    records = {}
    outputs = {'screen': IMAGES / 'coop-cast.svg', 'print': IMAGES / 'print/coop-cast.svg'}
    for mode, destination in outputs.items():
        destination.write_text(render(mode))
        parsed = ET.fromstring(destination.read_text())
        images = parsed.findall('.//{http://www.w3.org/2000/svg}image')
        assert len(images) == 4
        originals = {}
        for image in images:
            slug = image.attrib['id'].removeprefix('sprite-')
            path = IMAGES / f'sprites/sts-char-{slug}.png'
            embedded = base64.b64decode(image.attrib['href'].partition(',')[2])
            assert embedded == path.read_bytes(), slug
            originals[slug] = {'path': str(path.relative_to(ROOT)), 'sha256': sha(embedded)}
        records[mode] = {'path': str(destination.relative_to(ROOT)), 'sha256': sha(destination.read_bytes()), 'unchanged_sprites': originals}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='chrome')
        page = browser.new_page(viewport={'width': 500, 'height': 650}, device_scale_factor=2)
        def load(mode):
            content = outputs[mode].read_text().replace('<svg ', f'<svg width="{DISPLAY_WIDTH}" ', 1)
            page.set_content('<!doctype html><body style="margin:0;background:white">' + content)
            page.evaluate('() => document.fonts.ready')
        load('print')
        page.evaluate("() => {const t=document.querySelector('svg text'); t.parentNode.appendChild(t.cloneNode(true));}")
        assert page.evaluate(METRICS)['overlaps'], 'Overlap negative control stayed green'
        load('print')
        page.evaluate("() => document.querySelector('svg text').setAttribute('font-size','1')")
        assert page.evaluate(METRICS)['min_pt'] < 8, 'Size negative control stayed green'
        for mode in outputs:
            load(mode)
            metrics = page.evaluate(METRICS)
            assert not metrics['overlaps'] and not metrics['outside'], (mode, metrics)
            assert metrics['min_pt'] >= 8 and metrics['height_in'] <= 7, (mode, metrics)
            page.locator('body > svg').screenshot(path=str(PROOF / f'coop-cast-{mode}.png'))
            records[mode]['geometry'] = metrics
        browser.close()
    report = {'negative_controls': {'overlap_detected': True, 'undersize_detected': True}, 'outputs': records,
              'limits': 'Browser geometry at 4.56 inches, not a physical printer proof or external rights clearance. PNG bytes are unchanged. Only transparent outer margins are excluded by SVG viewports.'}
    (PROOF / 'checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({mode: value['geometry'] for mode, value in records.items()}, indent=2))


if __name__ == '__main__':
    main()
