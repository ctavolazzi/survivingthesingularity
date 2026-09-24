import json,re,os,sys
root=sys.argv[1]
bj=json.load(open(f'{root}/src/lib/data/book/book.json'))
files=[s['file'] for s in bj['sections']]
text={f:open(f'{root}/src/lib/data/book/{f}').read() for f in files}
fails=[]
def hit(name,pat,flags=0,allow=None):
    for f,t in text.items():
        for m in re.finditer(pat,t,flags):
            line=t[max(0,m.start()-60):m.end()+60].replace('\n',' ')
            if allow and re.search(allow,line): continue
            fails.append((name,f,line))
hit('em dash','—')
hit('manifesto',r'manifesto',re.I,allow=r'Bastani|Fully Automated Luxury Communism: A Manifesto')
hit('uncontracted Let us',r'\bLet us\b')
# error catalogue (v0.8.1 evidence review + 2026-08-16 review)
cat={
 'Napoleon superlative':r'Napoleon',
 'four thousand acts':r'four thousand acts',
 'free to everyone (commons)':r'Free to everyone, so it',
 'Universal Basic Computing':r'Universal Basic Computing',
 'sub-millimeter FarmBot':r'sub-millimeter',
 'millions of joules':r'millions of joules',
 '48-hour dopamine':r'forty-eight hours your dopamine|48 hours.{0,40}dopamine',
 'forty thousand pounds':r'forty thousand pounds',
 'eighty pounds Fisher':r'eighty pounds',
 'horse peak 1915':r'1915',
 'lead-acid decades':r'lights on for decades',
 'PETG from bottles':r'bottles.{0,80}\(PETG\)',
 'Google synthetic neurons':r'Google producing synthetic neurons',
 'Safe Street Rebels plural':r'Safe Street Rebels',
 '365-degree':r'365-degree',
 'twenty-two entries/episodes':r'twenty-two (entries|documented episodes)',
 'Hitchcock quote':r'Hitchcock',
 'bad Mycodo URL':r'raw\.githubusercontent\.com/kylegabriel',
 'Mycodo port 8080':r'pi-ip>:8080',
 'Krugman fax':r'fax machine\'s',
 'Daily Mail fad':r'Daily Mail',
 'barter cannot tax':r'cannot tax or regulate',
 'machine God':r'machine [Gg]od',
 'Wake the fuck up':r'Wake the fuck up',
 'capitalist goblins':r'capitalist goblins',
 'orbs':r'"orbs"',
 'compost tea recipe':r'[Mm]olasses',
 'independent wealth funds':r'independent wealth funds',
 'Starving the Beast':r'Starving the Beast',
 'religious tax shield':r'Religious or Educational Trust',
 'terminator seeds':r'sterile offspring',
 'Denny whose chapter':r'whose chapter this properly is',
 'Devendra seam':r'first visit he had managed with the children',
 'next day (directive)':r'switched both models off worldwide the next day',
 'seventy-nine pages':r'[Ss]eventy-[Nn]ine [Pp]ages',
 'decentralized as goal':r'[Dd]ecentralization, [Nn]ot',
 'supermarkets 72h':r'seventy-two hours',
 'Kelvin marvel quote':r'greatest marvel',
 'Western Union passed':r'Western Union, offered',
 'no-updates policy':r'[Ff]reeze the stack',
 'Faraday impenetrable':r'impenetrable',
 # v0.9.2 corrections
 'open weights recall claim':r"open weights can't be recalled",
 'one order one day':r'One order\. One day\.',
 'Kropotkin false ellipsis':r'over the country … so as to',
}
for k,v in cat.items(): hit(k,v)
# images resolve
for f,t in text.items():
    for m in re.finditer(r'!\[[^\]]*\]\((/book-images/[^)]+)\)',t):
        if not os.path.exists(f'{root}/static{m.group(1)}'): fails.append(('missing image',f,m.group(1)))
# cross-references: "Chapter N" must be 0..18
for f,t in text.items():
    for m in re.finditer(r'Chapter (\d+)',t):
        near=t[max(0,m.start()-200):m.end()+120]
        if int(m.group(1))>19 and 'Northanger' not in near and 'gutenberg.org/files/121' not in near:
            fails.append(('bad chapter ref',f,m.group(0)))
# precedent ids present once each in body, and in Appendix D
body=''.join(text[f] for f in files)
for i in range(1,25):
    pid=f'P-{i:02d}'
    n=len(re.findall(rf'^## Precedent {pid}:',body,re.M))
    if n!=1: fails.append(('precedent count',pid,str(n)))
    if pid not in text['25-appendix-d.md']: fails.append(('ledger missing',pid,''))
# h1 matches book.json title (case-insensitive)
for s in bj['sections']:
    h1=text[s['file']].split('\n')[0].lstrip('# ').strip()
    if h1.lower()!=s['title'].lower(): fails.append(('title mismatch',s['file'],h1+' | '+s['title']))
for x in fails: print('FAIL',x[0],'|',x[1],'|',x[2][:150])
print('TOTAL FAILS',len(fails))
