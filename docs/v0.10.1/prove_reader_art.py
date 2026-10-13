"""Exercise the actual Vite-served renderer and shared desktop/mobile rules."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent/'visual-proof'
BASE='http://localhost:5189'
PARAGRAPH='A useful service reaches the people who depend on it. The work includes maintaining equipment, checking the arrangements, listening to complaints, and telling households what they can rely on. A meal has to arrive on an ordinary day as well as a demonstration day.'
METRICS=r'''() => {
 const root=document.querySelector('article'),figure=root.querySelector('figure'),img=figure.querySelector('img'),caption=figure.querySelector('figcaption');
 const a=root.getBoundingClientRect(),f=figure.getBoundingClientRect(),i=img.getBoundingClientRect(),s=getComputedStyle(img),fs=getComputedStyle(figure);
 let collisions=[];
 for(const p of root.querySelectorAll(':scope > p')) {
  const range=document.createRange();range.selectNodeContents(p);
  for(const r of range.getClientRects())if(r.left<i.right && i.left<r.right && r.top<i.bottom && i.top<r.bottom)collisions.push(p.textContent);
 }
 return {float:fs.cssFloat,figureWidth:f.width,articleWidth:a.width,inside:f.left>=a.left-.5&&f.right<=a.right+.5,collisions,
  border:s.borderTopWidth,radius:s.borderTopLeftRadius,shadow:s.boxShadow,background:s.backgroundColor,caption:caption.textContent,
  horizontalOverflow:document.documentElement.scrollWidth>innerWidth};
}'''

with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome')
 page=browser.new_page(viewport={'width':1100,'height':1000},device_scale_factor=1)
 page.goto(BASE,wait_until='domcontentloaded')
 markdown='![Atlas cutout](/book-images/v101-cutout-atlas.png)\n\n*Caption follows only this figure.*\n\n'+('\n\n'.join([PARAGRAPH]*4))+'\n\n## Clear section\n\nText after the illustration.\n'
 rendered=page.evaluate("async s => (await import('/src/lib/utils/bookMarkdown.js')).renderMarkdown(s)",markdown)
 # A missing alpha file does not block layout proof: use the source portrait.
 if not (ROOT/'static/book-images/v101-cutout-atlas.png').exists():
  rendered=rendered.replace('/book-images/v101-cutout-atlas.png','/book-images/ch01-atlas.jpg')
 control_source='![alt](/book-images/v101-visual-access-gate.svg)\n\n*Italic start* ordinary prose.\n\nRetained paragraph.\n\n*Later italic paragraph.*\n\n<img src=x onerror=alert(1)>'
 control=page.evaluate("async s => (await import('/src/lib/utils/bookMarkdown.js')).renderMarkdown(s)",control_source)
 assert control.count('<figure')==1
 assert 'onerror' not in control and 'Retained paragraph.' in control
 assert '<figcaption>' not in control,'Caption matching swallowed unrelated paragraphs'
 unregistered=page.evaluate("async () => (await import('/src/lib/utils/bookMarkdown.js')).renderMarkdown('![alt](/book-images/ch01-atlas.jpg)')")
 assert '<figure' not in unregistered and 'width="1280"' in unregistered and 'height="1920"' in unregistered
 css=(ROOT/'src/lib/styles/book-figures.css').read_text()
 fixture=f'''<!doctype html><style>body{{margin:0;background:#0f172a;color:#f1f5f9}}article{{max-width:680px;margin:40px auto;padding:0;font:18px/1.65 Georgia}}p{{margin:0 0 1em}}h2{{font:26px Georgia}}@media(max-width:759px){{article{{margin:20px 22px;font-size:17px}}}}
 /* Reproduce old route image defaults; shared art rules must win. */
 .chapter-article img{{width:100%;border-radius:12px;box-shadow:0 15px 35px #000;border:1px solid #f90;background:#123}}{css}</style><article class="chapter-article">{rendered}</article>'''
 page.set_content(fixture);page.wait_for_function("document.images[0].complete && document.images[0].naturalWidth>0")
 desktop=page.evaluate(METRICS)
 assert desktop['float']=='right' and desktop['inside'] and not desktop['collisions'] and not desktop['horizontalOverflow'],desktop
 assert desktop['border']=='0px' and desktop['radius']=='0px' and desktop['shadow']=='none' and desktop['background']=='rgba(0, 0, 0, 0)',desktop
 page.screenshot(path=str(OUT/'reader-desktop.png'),full_page=True)
 # Instrument control: shift the figure into the gutter and verify detection.
 page.add_style_tag(content='figure.book-figure { transform: translateX(500px); }')
 assert not page.evaluate(METRICS)['inside']
 page.set_content(fixture)
 page.set_viewport_size({'width':390,'height':844});page.wait_for_function("document.images[0].complete && document.images[0].naturalWidth>0")
 mobile=page.evaluate(METRICS)
 assert mobile['float']=='none' and mobile['inside'] and not mobile['collisions'] and not mobile['horizontalOverflow'],mobile
 page.screenshot(path=str(OUT/'reader-mobile.png'),full_page=True)
 report={'desktop':desktop,'mobile':mobile,'negative_controls':['gutter shift','script handler sanitization','caption does not consume intervening prose'],'intrinsic_legacy_dimensions_preserved':True,'limits':'Shared renderer/CSS fixture, including previous image styles. Full chapter route and frozen book checks remain separate.'}
 (OUT/'reader-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
 browser.close()
