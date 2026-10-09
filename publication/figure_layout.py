"""Capture and audit registered book figures from actual WeasyPrint boxes.

No dimensions are inferred from HTML/CSS. The build captures live layout;
preflight checks the durable capture against the final HTML and registry.
"""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

SCHEMA='sts-figure-layout/v1'


def rect(box):
    return [box.content_box_x(),box.content_box_y(),box.width,box.height]


def contained(inner,outer,tolerance=.75):
    x,y,w,h=inner;X,Y,W,H=outer
    return x>=X-tolerance and y>=Y-tolerance and x+w<=X+W+tolerance and y+h<=Y+H+tolerance


def intersects(a,b,tolerance=.5):
    x,y,w,h=a;X,Y,W,H=b
    return min(x+w,X+W)-max(x,X)>tolerance and min(y+h,Y+H)-max(y,Y)>tolerance


def normalize(text):
    return re.sub(r'\s+','',text).replace('\u00ad','')


def capture(document,html_path,registry_path):
    pages=[]
    for page_number,page in enumerate(document.pages,1):
        figures={};other_text=[]
        def walk(box,current=None,in_caption=False):
            element=box.element
            marker=element.get('data-book-visual') if element is not None else None
            if marker and marker!=current:
                current=marker
                figures.setdefault(marker,{'file':marker,'fragments':[],'images':[],'caption_boxes':[]})['fragments'].append(rect(box))
            in_caption=in_caption or (element is not None and element.tag=='figcaption')
            if type(box).__name__=='TextBox' and box.text.strip():
                item={'text':box.text,'rect':rect(box)}
                if current and in_caption:figures[current]['caption_boxes'].append(item)
                elif not current:other_text.append(item)
            if 'ReplacedBox' in type(box).__name__ and current and element is not None:
                figures[current]['images'].append({'file':Path(element.get('src','')).name,'rect':rect(box),'alt':element.get('alt','')})
            for child in getattr(box,'children',[]):walk(child,current,in_caption)
        walk(page._page_box)
        if figures:
            pages.append({'page':page_number,'content_rect':rect(page._page_box),'figures':list(figures.values()),'other_text':other_text})
    return {'schema':SCHEMA,'html_sha256':hashlib.sha256(Path(html_path).read_bytes()).hexdigest(),
            'registry_sha256':hashlib.sha256(Path(registry_path).read_bytes()).hexdigest(),'pages':pages}


def specifications(html_document,registry):
    result=[]
    for figure in html_document.select('figure[data-book-visual]'):
        name=figure['data-book-visual'];image=figure.find('img');caption=figure.find('figcaption')
        result.append({'file':name,'layout':registry.get(name,{}).get('layout'),
                       'caption':caption.get_text(' ',strip=True) if caption else '',
                       'alt':image.get('alt','') if image else '',
                       'image_file':Path(image.get('src','')).name if image else ''})
    return result


def check(report,specs,registry):
    errors=[];occurrences={};measured=[]
    if report.get('schema')!=SCHEMA:return [{'issue':'missing or unsupported figure-layout schema'}],[]
    counts=Counter(x['file'] for x in specs)
    for name in registry:
        if counts[name]!=1:errors.append({'issue':'expected exactly one registered figure marker','file':name,'count':counts[name]})
    for name in counts:
        if name not in registry:errors.append({'issue':'unknown figure marker','file':name})
    expected={x['file']:x for x in specs}
    for page in report['pages']:
        for fig in page['figures']:
            name=fig['file'];occurrences.setdefault(name,[]).append((page,fig))
            for fragment in fig['fragments']:
                if not contained(fragment,page['content_rect']):errors.append({'issue':'figure outside content area','file':name,'page':page['page'],'rect':fragment})
                for text in page['other_text']:
                    if intersects(fragment,text['rect']):errors.append({'issue':'prose intersects figure','file':name,'page':page['page'],'text':text['text']})
            for item in fig['images']+fig['caption_boxes']:
                if not any(contained(item['rect'],f) for f in fig['fragments']):errors.append({'issue':'image or caption outside figure','file':name,'page':page['page'],'rect':item['rect']})
    for name,spec in expected.items():
        seen=occurrences.get(name,[])
        if len(seen)!=1:
            errors.append({'issue':'figure absent or split across pages','file':name,'pages':[p['page'] for p,f in seen]})
            continue
        page,fig=seen[0];images=fig['images'];caption=normalize(''.join(b['text'] for b in fig['caption_boxes']))
        if len(images)!=1 or images[0]['file']!=name:errors.append({'issue':'missing or mismatched figure image','file':name,'page':page['page']})
        if not spec['caption'] or caption!=normalize(spec['caption']):errors.append({'issue':'caption absent, incomplete, or on another page','file':name,'page':page['page']})
        if not spec['alt'] or (images and images[0]['alt']!=spec['alt']):errors.append({'issue':'missing accessible description','file':name})
        if images:
            width=images[0]['rect'][2]/96;height=images[0]['rect'][3]/96
            layout=spec['layout'];target=4.56 if layout=='diagram' else 1.42 if layout in ('cutout-left','cutout-right') else None
            if target is not None and abs(width-target)>.015:errors.append({'issue':'unexpected figure width','file':name,'actual_inches':width,'expected_inches':target})
            measured.append({'file':name,'page':page['page'],'layout':layout,'display_inches':[width,height],'caption_same_page':bool(caption)})
    return errors,measured


def negative_controls():
    """Mutate recorded layout, including the classes this checker must observe."""
    registry={'probe.png':{'layout':'cutout-left'}}
    specs=[{'file':'probe.png','layout':'cutout-left','caption':'A complete caption.','alt':'Description','image_file':'probe.png'}]
    valid={'schema':SCHEMA,'pages':[{'page':1,'content_rect':[70,60,437.76,700],
       'figures':[{'file':'probe.png','fragments':[[70,100,136.32,220]],
       'images':[{'file':'probe.png','rect':[70,100,136.32,170],'alt':'Description'}],
       'caption_boxes':[{'text':'A complete caption.','rect':[70,285,130,20]}]}],
       'other_text':[{'text':'Adjacent prose.','rect':[225,100,250,20]}]}]}
    assert not check(valid,specs,registry)[0]
    def reject(label,mutate,issue):
        mutant=deepcopy(valid);mutate(mutant)
        found=check(mutant,specs,registry)[0]
        assert any(x['issue']==issue for x in found),f'{label} negative control stayed green: {found}'
        return label
    controls=[]
    controls.append(reject('figure shifted into gutter',lambda m:m['pages'][0]['figures'][0]['fragments'][0].__setitem__(0,-10),'figure outside content area'))
    controls.append(reject('prose moved into figure',lambda m:m['pages'][0]['other_text'][0].__setitem__('rect',[90,120,100,20]),'prose intersects figure'))
    controls.append(reject('caption clipped by figure',lambda m:m['pages'][0]['figures'][0]['caption_boxes'][0].__setitem__('rect',[70,310,130,40]),'image or caption outside figure'))
    controls.append(reject('missing caption text',lambda m:m['pages'][0]['figures'][0]['caption_boxes'].clear(),'caption absent, incomplete, or on another page'))
    controls.append(reject('missing rendered figure',lambda m:m['pages'].clear(),'figure absent or split across pages'))
    controls.append(reject('diagram/cutout shrunk',lambda m:m['pages'][0]['figures'][0]['images'][0]['rect'].__setitem__(2,70),'unexpected figure width'))
    mutant=deepcopy(valid);second=deepcopy(mutant['pages'][0]);second['page']=2;second['figures'][0]['images']=[];second['other_text']=[]
    mutant['pages'][0]['figures'][0]['caption_boxes']=[];mutant['pages'].append(second)
    assert any(x['issue']=='figure absent or split across pages' for x in check(mutant,specs,registry)[0]);controls.append('caption moved to a second page')
    assert check(valid,[],registry)[0];controls.append('missing HTML figure marker')
    return controls


if __name__=='__main__':
    print(json.dumps({'negative_controls':negative_controls()},indent=2))
