"""Validate EPUB resources, navigation, metadata and canonical text coverage."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import posixpath
import re
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'src/lib/data/book'
META=json.loads((SOURCE/'book.json').read_text())
EPUB=ROOT/'book-build'/f'Surviving-the-Singularity-v{META["version"]}.epub'

def norm(text):
    return re.sub(r'\s+','',unicodedata.normalize('NFKC',text)).replace('\u00ad','')

def check_resources(files):
    errors=[]
    parsed={name:BeautifulSoup(data,'xml') for name,data in files.items() if name.endswith(('.xhtml','.html','.opf'))}
    for name,doc in parsed.items():
        for node in doc.select('[href], [src]'):
            ref=node.get('href') or node.get('src')
            url=urlsplit(ref)
            if url.scheme or url.netloc:continue
            target=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(url.path))) if url.path else name
            if target not in files: errors.append(f'{name}: missing {ref}')
            elif url.fragment and target in parsed and not parsed[target].find(id=unquote(url.fragment)):
                errors.append(f'{name}: missing anchor {ref}')
    return errors

with zipfile.ZipFile(EPUB) as z:
    assert z.testzip() is None
    files={name:z.read(name) for name in z.namelist()}
assert files['mimetype']==b'application/epub+zip'
container=BeautifulSoup(files['META-INF/container.xml'],'xml')
opf=container.find('rootfile')['full-path'];package=BeautifulSoup(files[opf],'xml')
assert META['version'] in str(package), 'EPUB metadata has no current version'
assert package.find('dc:title').get_text()==META['title']
manifest={x['id']:posixpath.normpath(posixpath.join(posixpath.dirname(opf),x['href'])) for x in package.find_all('item')}
spine=[manifest[x['idref']] for x in package.find_all('itemref')]
text=''.join(BeautifulSoup(files[x],'xml').get_text() for x in spine)
normalized=norm(text)
reference=BeautifulSoup((ROOT/'publication/output/source-rendered.html').read_text(),'html.parser')
# Pandoc generates alt-text captions that aren't part of narrative prose.
for caption in reference.select('figure figcaption'):caption.decompose()
blocks=[x.get_text('',strip=False) for x in reference.select('p, li, th, td, h1, h2, h3, h4')]
blocks=[x for x in blocks if len(norm(x))>=15]
missing=[x for x in blocks if norm(x) not in normalized]
errors=check_resources(files)
mutant=dict(files);mutant['EPUB/text/probe.xhtml']=b'<html xmlns="http://www.w3.org/1999/xhtml"><body><img src="missing.png"/></body></html>'
assert check_resources(mutant), 'Missing-resource control failed'
assert norm('Intentionally missing EPUB proof paragraph.') not in normalized
report={'version':META['version'],'spine_documents':len(spine),'source_sections':len(META['sections']),
        'epub_sha256':hashlib.sha256(EPUB.read_bytes()).hexdigest(),
        'source_sha256':json.loads((ROOT/'docs/publication/baseline.json').read_text()),
        'source_blocks_checked':len(blocks),'missing_blocks':missing,'resource_errors':errors,
        'metadata_checked':True,'zip_integrity':True,'negative_controls':['absent image','absent text'],
        'limits':'Structural and text proof; not EPUBCheck certification or a physical-device test.'}
(ROOT/'docs/v0.10.0/epub-checks.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({**report,'missing_blocks':missing[:3]},indent=2))
assert not errors, errors
assert not missing, f'{len(missing)} missing EPUB source blocks'
