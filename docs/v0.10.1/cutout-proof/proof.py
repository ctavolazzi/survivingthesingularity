"""Read-only PNG alpha inspection and browser contact sheets.

This script never writes source images. Canvas reads pixels for measurements;
all proof PNGs are screenshots of ordinary browser image elements.
"""
from pathlib import Path
import argparse
import base64
from datetime import date
from html import escape
import hashlib
import json
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
IMAGES = ROOT / 'static/book-images'
PAIRS = {
    'atlas': 'ch01-atlas.jpg',
    'printer': 'ch09-3d-printer.jpg',
    'sun': 'ch05-sdo-sun.jpg',
    'tools': 'ch17-workbench.jpg',
    'spot': 'ch11-spot.jpg',
    'rocket': 'ch03-falcon-heavy.jpg',
}

ANALYZE = r'''({data,width,height}) => {
 let zero=0,partial=0,opaque=0,border=0,nearOpaque=0,maxAlpha=0;
 let x0=width,y0=height,x1=-1,y1=-1;
 for(let y=0;y<height;y++)for(let x=0;x<width;x++){
  const a=data[(y*width+x)*4+3];
  maxAlpha=Math.max(maxAlpha,a);if(a>=250)nearOpaque++;
  if(a===0)zero++;else if(a===255)opaque++;else partial++;
  if(a>=16){
   x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x);y1=Math.max(y1,y);
   if(x===0||y===0||x===width-1||y===height-1)border++;
  }
 }
 const n=width*height;
 return {width,height,fully_transparent_fraction:zero/n,partial_alpha_fraction:partial/n,
  opaque_fraction:opaque/n,alpha_250_or_higher_fraction:nearOpaque/n,max_alpha:maxAlpha,alpha_16_bbox:[x0,y0,x1,y1],
  alpha_16_margins:{left:x0,top:y0,right:width-x1-1,bottom:height-y1-1},
  alpha_16_border_pixels:border,has_visible_and_transparent_pixels:zero>0&&zero<n};
}'''


def uri(path):
    mime = 'image/png' if path.suffix == '.png' else 'image/jpeg'
    return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()


def page_html(body, background='#f1f5f9'):
    return '''<!doctype html><meta charset="utf-8"><style>
    *{box-sizing:border-box}body{margin:0;padding:24px;font:16px/1.4 Arial,sans-serif;background:'''+background+''';color:#0f172a}
    h1{font-size:25px;margin:0 0 8px}p{margin:0 0 20px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
    figure{margin:0;padding:18px;border:1px solid #64748b}figcaption{font-size:18px;font-weight:700;margin-bottom:12px}
    .white{background:#fff;color:#0f172a}.dark{background:#020617;color:#f1f5f9}
    .stage{height:430px;display:flex;align-items:center;justify-content:center}.stage img{display:block;max-width:100%;max-height:100%;object-fit:contain}
    .compare .stage{height:590px}.compare figure{padding:12px}.compare{gap:12px}
    </style><body>'''+body+'</body>'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--allow-pending',action='store_true')
    args=parser.parse_args()
    pending=[name for name in PAIRS if not (IMAGES/f'v101-cutout-{name}.png').exists()]
    assert args.allow_pending or not pending, 'Missing assets: '+', '.join(pending)
    names=[name for name in PAIRS if name not in pending]
    files=[IMAGES/PAIRS[name] for name in names]+[IMAGES/f'v101-cutout-{name}.png' for name in names]
    hashes={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
    records={}
    with sync_playwright() as pw:
        browser=pw.chromium.launch(channel='chrome')
        page=browser.new_page(viewport={'width':1200,'height':800},device_scale_factor=2)
        page.goto('about:blank')
        page.evaluate('() => {window.analyzePixels = '+ANALYZE+';}')
        opaque=page.evaluate('() => window.analyzePixels({data:new Uint8ClampedArray([1,2,3,255,1,2,3,255]),width:2,height:1})')
        assert not opaque['has_visible_and_transparent_pixels'], 'Opaque negative control stayed green'
        clipped=page.evaluate('() => window.analyzePixels({data:new Uint8ClampedArray([1,2,3,255,0,0,0,0]),width:2,height:1})')
        assert clipped['alpha_16_border_pixels']==1, 'Border negative control stayed green'
        for name in names:
            output=IMAGES/f'v101-cutout-{name}.png'
            pixels=page.evaluate('''async (src) => {
             const img=new Image();img.src=src;await img.decode();
             const canvas=document.createElement('canvas');canvas.width=img.naturalWidth;canvas.height=img.naturalHeight;
             const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(img,0,0);
             return window.analyzePixels({data:ctx.getImageData(0,0,canvas.width,canvas.height).data,width:canvas.width,height:canvas.height});
            }''',uri(output))
            assert pixels['has_visible_and_transparent_pixels'], name+' lacks usable alpha'
            records[name]={'source':PAIRS[name],'output':output.name,'measurements':pixels,
                           'png_ihdr_color_type':output.read_bytes()[25]}
        for surface in ['white','dark']:
            body='<h1>Cutout alpha proof: '+surface+' surface</h1><p>Unmodified PNG assets displayed over '+('#ffffff' if surface=='white' else '#020617')+'. Generated editorial adaptations; compare with originals.</p><main class="grid">'
            for name in names:
                body+='<figure class="'+surface+'"><figcaption>'+escape(name)+'</figcaption><div class="stage"><img alt="'+name+' cutout" src="'+uri(IMAGES/f'v101-cutout-{name}.png')+'"></div></figure>'
            body+='</main>'
            page.set_content(page_html(body))
            page.evaluate('() => Promise.all([...document.images].map(i=>i.decode()))')
            page.screenshot(path=str(HERE/f'contact-{surface}.png'),full_page=True)
        for name in names:
            source=uri(IMAGES/PAIRS[name]);cutout=uri(IMAGES/f'v101-cutout-{name}.png')
            body='<h1>'+escape(name)+': source and generated adaptation</h1><p>Original file at left; identical cutout PNG on white and dark surfaces. Images fit without cropping.</p><main class="grid compare">'
            for label,surface,src in [('Source original','white',source),('Cutout / white','white',cutout),('Cutout / dark','dark',cutout)]:
                body+='<figure class="'+surface+'"><figcaption>'+label+'</figcaption><div class="stage"><img alt="'+label+'" src="'+src+'"></div></figure>'
            body+='</main>'
            page.set_content(page_html(body))
            page.evaluate('() => Promise.all([...document.images].map(i=>i.decode()))')
            page.screenshot(path=str(HERE/f'compare-{name}.png'),full_page=True)
        browser.close()
    assert all(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest for path,digest in hashes.items()), 'Proof altered an input'
    result={'review_date':date.today().isoformat(),'pending':pending,'complete':not pending,'files':hashes,
            'negative_controls':{'opaque_background_rejected':True,'border_contact_detected':True},
            'figures':records,'limits':'Browser alpha measurements and contact sheets. Numeric bounds cannot determine whether a machine detail is authentic, a corona is scientifically preserved, or a soft edge is visually suitable. No source image is changed.'}
    (HERE/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({name:row['measurements'] for name,row in records.items()},indent=2))
    print('Pending:',pending)


if __name__=='__main__':
    main()
