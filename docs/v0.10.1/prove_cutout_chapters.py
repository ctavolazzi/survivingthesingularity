"""Final alpha images in actual chapter and continuous reading routes."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent/'visual-proof'/'cutout-chapters';OUT.mkdir(exist_ok=True)
BASE='http://localhost:5189'
REGISTRY=json.loads((ROOT/'src/lib/data/book/visuals.json').read_text())['images']
CASES=[('introduction','atlas'),('chapter3','rocket'),('chapter5','sun'),('chapter9','printer'),('chapter11','spot'),('chapter17','tools')]
MEASURE=r'''img => {
 const figure=img.closest('figure'),root=img.closest('.chapter-article,.prose'),a=root.getBoundingClientRect(),f=figure.getBoundingClientRect(),i=img.getBoundingClientRect();
 const fs=getComputedStyle(figure),s=getComputedStyle(img),rs=getComputedStyle(root),caption=figure.querySelector('figcaption');
 const bounds={left:a.left+parseFloat(rs.paddingLeft),right:a.right-parseFloat(rs.paddingRight)};
 const collisions=[],walk=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
 while(walk.nextNode()) {
  const node=walk.currentNode;
  if(!node.textContent.trim()||node.parentElement.closest('figure'))continue;
  const range=document.createRange();range.selectNodeContents(node);
  for(const r of range.getClientRects())if(Math.min(r.right,f.right)-Math.max(r.left,f.left)>.6 && Math.min(r.bottom,f.bottom)-Math.max(r.top,f.top)>.6)collisions.push(node.textContent.trim().slice(0,100));
 }
 return {file:img.getAttribute('src').split('/').pop(),float:fs.cssFloat,width:i.width,height:i.height,natural:[img.naturalWidth,img.naturalHeight],
  inside:f.left>=bounds.left-.75 && f.right<=bounds.right+.75,collisions:[...new Set(collisions)],
  border:s.borderTopWidth,radius:s.borderTopLeftRadius,shadow:s.boxShadow,background:s.backgroundColor,
  caption:caption?.textContent,captionSize:caption?parseFloat(getComputedStyle(caption).fontSize):0,
  rootOverflow:root.scrollWidth>root.clientWidth+1,alt:img.getAttribute('alt')};
}'''
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome')
 page=browser.new_page(viewport={'width':1280,'height':1000},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def unlock(url):
  page.goto(url,wait_until='networkidle')
  page.evaluate("async () => (await import('/src/lib/stores/bookAccess.js')).bookUnlocked.set(true)")
 def inspect(route,chapter,slug,width):
  page.set_viewport_size({'width':width,'height':1000 if width>760 else 844})
  selector=f'img[src="/book-images/v101-cutout-{slug}.png"]'
  image=page.locator(selector);image.wait_for(state='attached')
  image.evaluate("img => {img.loading='eager';img.closest('figure').scrollIntoView({block:'center'});}")
  image.evaluate("img => img.decode()")
  page.evaluate('document.fonts.ready')
  image.evaluate("img => img.closest('figure').scrollIntoView({block:'center'})")
  page.evaluate("async () => await Promise.all(document.getAnimations().filter(a=>a.effect.getComputedTiming().iterations!==Infinity).map(a=>a.finished.catch(()=>{})))")
  measure=image.evaluate(MEASURE);measure.update({'route':route,'chapter':chapter,'viewport':width})
  expected=REGISTRY[measure['file']]['layout'].removeprefix('cutout-') if width>760 else 'none'
  assert measure['float']==expected and measure['inside'] and not measure['collisions'] and not measure['rootOverflow'],measure
  assert measure['natural']==REGISTRY[measure['file']]['pixels'],measure
  assert measure['border']=='0px' and measure['radius']=='0px' and measure['shadow']=='none' and measure['background']=='rgba(0, 0, 0, 0)',measure
  assert measure['caption'] and measure['captionSize']>=12 and measure['alt'],measure
  page.screenshot(path=str(OUT/f'{route}-{slug}-{width}.png'))
  results.append(measure)
 for chapter,slug in CASES:
  unlock(BASE+'/book/'+chapter)
  for width in [1280,390]:inspect('book',chapter,slug,width)
 # The continuous reader mounts chapters through its actual table-of-contents UI.
 page.set_viewport_size({'width':1280,'height':1000});unlock(BASE+'/read')
 page.locator('button[aria-controls="reader-toc"]').click()
 page.locator('.toc-item').filter(has_text='Chapter 17:').first.click()
 page.locator('img[src="/book-images/v101-cutout-tools.png"]').wait_for(state='attached')
 for chapter,slug in CASES:
  for width in [1280,390]:inspect('read',chapter,slug,width)
 # Prove real-DOM gutter detection using a reversible style mutation.
 image=page.locator('img[src="/book-images/v101-cutout-tools.png"]')
 image.evaluate("img=>img.closest('figure').style.transform='translateX(500px)'")
 assert not image.evaluate(MEASURE)['inside']
 image.evaluate("img=>img.closest('figure').style.transform=''")
 report={'checks':results,'count':len(results),'browser_errors':errors,'negative_control':'real figure translated into gutter, then restored','limits':'Actual local web readers at 1280px and390px; screenshots review digital layout/alpha appearance, not physical print.'}
 (OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'checks':len(results),'browser_errors':errors,'files':sorted({r['file'] for r in results})}))
 assert not errors,errors
 browser.close()
