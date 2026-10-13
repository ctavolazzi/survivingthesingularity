"""Six deterministic editorial SVG vignettes; source and print geometry match.

These are conceptual illustrations, not measured quantities, technical plans,
or depictions of a working service. Run with --proof for browser geometry and
actual-width screenshots. Prepared variants register both hashes atomically
within this generator's six entries, preserving other artists' entries.
"""
from pathlib import Path
from html import escape
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
IMAGES = ROOT/'static/book-images'
REGISTRY = ROOT/'src/lib/data/book/visuals.json'
WIDTH = 480
PALETTES = {
 'screen':dict(ink='#f1f5f9',muted='#94a3b8',amber='#f59e0b',blue='#60a5fa',paper='#0f172a',rule='#475569'),
 'print':dict(ink='#17251f',muted='#4b5b52',amber='#9a4f13',blue='#315f78',paper='#ffffff',rule='#a2afa6'),
}


class Art:
 def __init__(self, mode, height, title, desc):
  self.p=PALETTES[mode];self.height=height
  self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 {height}" role="img" aria-labelledby="title desc" font-family="JetBrains Mono, monospace">',f'<title id="title">{escape(title)}</title>',f'<desc id="desc">{escape(desc)}</desc>']
  if mode=='print':self.parts.append(f'<rect width="480" height="{height}" fill="#ffffff"/>')
  self.text(20,31,title,20,'ink',weight=600)
  self.line(20,46,460,46,'amber',2)
 def text(self,x,y,s,size=14,color='muted',anchor='start',weight=400):
  self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{self.p[color]}" text-anchor="{anchor}" font-weight="{weight}">{escape(s)}</text>')
 def line(self,x,y,x2,y2,color='rule',width=1,dash=None):
  self.parts.append(f'<path d="M{x} {y}L{x2} {y2}" fill="none" stroke="{self.p[color]}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def path(self,d,color='ink',width=2,fill='none',dash=None):
  self.parts.append(f'<path d="{d}" fill="{self.p.get(fill,fill)}" stroke="{self.p[color]}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def circle(self,x,y,r,color='ink',width=2,fill='none'):
  self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{self.p.get(fill,fill)}" stroke="{self.p[color]}" stroke-width="{width}"/>')
 def hatch(self,x,y,w,h,step=10,color='rule'):
  for a in range(0,w+1,step):self.line(x+a,y,x+a,y+h,color,.7)
 def footer(self,y,lines):
  self.line(20,y-20,460,y-20)
  for i,s in enumerate(lines):self.text(20,y+i*21,s)
 def finish(self):return '\n'.join(self.parts)+'\n</svg>\n'


def gate(mode):
 a=Art(mode,338,'THE GATE AFTER THE MACHINE','A productive machine, a gate and a plate. Access depends on terms, price, eligibility and delivery, not capability alone.')
 a.text(26,78,'Capability',color='ink');a.text(454,78,'Access',color='ink',anchor='end')
 # Gear and a seed: production is the beginning of this journey.
 import math
 for n in range(16):
  t=n*math.pi/8
  a.line(100+43*math.cos(t),159+43*math.sin(t),100+53*math.cos(t),159+53*math.sin(t),'amber',5)
 a.circle(100,159,43,'amber',3);a.circle(100,159,18,'amber',2)
 a.path('M100 178V128M100 143Q76 120 81 148Q93 158 100 153M100 140Q123 113 120 140Q114 151 100 150','ink',2)
 a.line(156,159,208,159,'ink',2);a.path('M200 153L208 159L200 165')
 # Open frame, door angled away, threshold repeated as engraved marks.
 a.path('M226 229V97H290V229M220 229H310','ink',3)
 a.path('M234 104L269 121V222L234 213Z','blue',2,fill='paper');a.circle(260,170,2,'blue',1,fill='blue')
 for y in range(128,211,9):a.line(240,y,249,y+4,'rule',.7)
 a.line(302,159,345,159,'ink',2);a.path('M337 153L345 159L337 165')
 a.circle(398,159,39,'ink',2);a.circle(398,159,30,'rule',1)
 a.path('M384 163Q398 143 412 163Q400 179 384 163Z','amber',2)
 a.text(260,258,'Terms · price · eligibility · delivery',anchor='middle')
 a.footer(300,['A working tool still needs a way through.'])
 return a


def ribbon(mode):
 a=Art(mode,352,'THE DAY, CUT INTO PIECES','Fragmented ribbon contrasted with an intact ribbon. A visual metaphor for interruptions and time devoted to a chosen task, without measured scale.')
 a.text(20,78,'Pulled away',color='ink')
 fragments=[(28,113,60,133),(101,108,144,146),(165,121,209,144),(235,104,281,128),(309,119,350,147),(381,108,446,131)]
 for i,(x,y,x2,y2) in enumerate(fragments):
  a.path(f'M{x} {y}L{x2} {y+5}L{x2-4} {y2}L{x+3} {y2-4}Z','amber',1.4,fill='paper')
  for k in range(6,int(x2-x)-4,8):a.line(x+k,y+8,x+k-2,y2-7,'rule',.8)
  if i<5:a.line(x2+3,122,x2+14,112,'muted',1)
 a.text(20,191,'A chosen task',color='ink')
 a.path('M28 223C120 198 172 256 240 232S366 203 449 226L449 252C366 230 302 279 240 258S120 225 28 249Z','blue',2,fill='paper')
 a.path('M31 235C120 210 172 269 240 245S366 216 446 239','rule',.7)
 a.footer(306,['Illustration of interruptions, not a clock.','No fixed recovery time is implied.'])
 return a


def stack(mode):
 a=Art(mode,397,'THE FILE IS ONE LAYER','Model weights shown as a loose paper beside an exploded operating stack. A usable local system also requires software, compute, power and people who can maintain it.')
 a.text(20,79,'Open weights',color='ink');a.text(252,79,'Operating stack',color='ink')
 a.path('M33 101L155 109L148 231L26 222Z','amber',2,fill='paper')
 a.path('M44 127L135 133M42 139L133 145M41 151L119 157M39 163L130 169M38 175L102 181M36 187L123 193','rule',1)
 a.path('M46 210L70 212M78 213L103 215M111 216L133 218','amber',2)
 a.text(20,261,'License sets',color='ink');a.text(20,282,'the terms.')
 # Exploded, staggered physical layers. Labels are beside, never on a seam.
 for y,color,label in [(114,'amber','Software'),(166,'blue','Compute'),(218,'ink','Power')]:
  a.path(f'M239 {y}L286 {y-15}L327 {y}L280 {y+15}Z',color,2,fill='paper')
  a.path(f'M239 {y}V{y+8}L280 {y+23}L327 {y+8}V{y}',color,1.3)
  a.line(333,y+2,349,y+2,'rule',1)
  a.text(355,y+7,label,14,'ink')
 a.path('M215 273Q270 248 332 273M215 281Q270 256 332 281','muted',1.5)
 a.text(270,309,'Maintenance',14,'ink',anchor='middle')
 a.footer(357,['A downloadable model is not a whole service.'])
 return a


def copies(mode):
 a=Art(mode,374,'KEEP A COPY YOU CAN OPEN','A distant server and a local folder separated by a broken network link. A local copy can preserve information access, but still requires power, compatible software and an up-to-date version.')
 a.text(20,80,'Remote service',color='ink');a.text(459,80,'Local copy',color='ink',anchor='end')
 for y in [103,126,149]:
  a.path(f'M40 {y}H147V{y+17}H40Z','blue',1.5,fill='paper')
  a.circle(50,y+8,2,'blue',1,fill='blue');a.line(112,y+8,136,y+8,'rule',1)
 a.line(93,169,93,195,'ink',1.5)
 a.path('M50 195H137','ink',2)
 a.line(161,139,220,139,'muted',1.5,'4 5');a.line(262,139,319,139,'muted',1.5,'4 5')
 a.path('M233 129L225 139L237 145L231 155M247 125L241 136L253 142L247 153','amber',2)
 a.path('M335 107H373L385 118H446V203H335Z','amber',2,fill='paper')
 a.path('M344 126H437L426 209H324Z','ink',1.5,fill='paper')
 a.path('M355 146H416M352 157H413M349 168H397','rule',1)
 a.text(241,239,'The link can fail.',anchor='middle')
 a.footer(286,['Keep the files, an app that opens them,','and a version you have checked.','Copies do not provide electrical power.'])
 return a


def land(mode):
 a=Art(mode,399,'LAND HAS PEOPLE ON IT','Cultivated land rests above an open agreement with distinct spaces for an owner, users and neighbors. Shared use requires consent, terms and a way to challenge decisions.')
 # A field in perspective, with furrows and irregular plants.
 a.path('M55 153L209 88L427 150L270 219Z','ink',2,fill='paper')
 for i in range(1,11):
  t=i/12;x=55+154*t;y=153-65*t
  a.line(x,y,x+210,y+62,'rule',1)
 for x,y in [(122,148),(183,129),(263,156),(334,155),(233,189)]:
  a.path(f'M{x} {y}V{y-20}M{x} {y-9}Q{x-14} {y-25} {x-8} {y-8}M{x} {y-12}Q{x+14} {y-30} {x+9} {y-12}','amber',1.5)
 # Open sheet, folds meet but signatures remain separate.
 a.path('M49 240L184 225L299 245L431 230V309L299 324L184 304L49 319Z','blue',1.5,fill='paper')
 a.line(184,231,184,296,'rule',1);a.line(299,252,299,315,'rule',1)
 a.text(114,272,'Owner',14,'ink',anchor='middle');a.text(241,279,'Users',14,'ink',anchor='middle');a.text(365,275,'Neighbors',14,'ink',anchor='middle')
 a.path('M70 298Q91 282 104 297T154 292M206 299Q222 289 238 302T277 299M322 303Q336 283 350 299T407 291','muted',1.2)
 a.footer(364,['Consent · terms · decisions people can contest'])
 return a


def calendar(mode):
 a=Art(mode,384,'INK FOR WHAT IS FUNDED','Two calendar sheets distinguish funding secured through June from a proposed continuation. Delivery also depends on paid work, backup cover and clear communication with households. No year or invented schedule is shown.')
 # Two loose calendar sheets, one solid, one pencil-like outline.
 a.path('M28 103H222V243H28Z','ink',2,fill='paper');a.path('M252 103H446V243H252Z','muted',1.4,fill='paper',dash='5 4')
 for x in [66,184,290,408]:a.path(f'M{x} 111V91','ink',3)
 a.text(125,147,'THROUGH JUNE',17,'ink',anchor='middle');a.text(349,147,'CONTINUATION',17,'muted',anchor='middle')
 a.line(45,161,205,161,'rule');a.line(269,161,429,161,'rule',1,'3 4')
 a.path('M82 202L106 220L165 180','amber',4)
 a.text(349,204,'proposed',17,'muted',anchor='middle')
 a.text(125,274,'Secured',14,'ink',anchor='middle');a.text(349,274,'Not yet promised',14,'ink',anchor='middle')
 a.footer(322,['Name the cover. Pay for the work.','Tell households what is actually secured.'])
 return a


BUILDERS={'access-gate':gate,'attention-ribbon':ribbon,'operating-stack':stack,'local-copies':copies,'shared-land':land,'continuity-calendar':calendar}


def main():
 registry=json.loads(REGISTRY.read_text())
 for key,builder in BUILDERS.items():
  name='v101-visual-'+key+'.svg';height=builder('screen').height
  for mode in PALETTES:
   path=IMAGES/('print' if mode=='print' else '')/name
   content=builder(mode).finish();path.write_text(content);assert path.read_text()==content
  registry['images'][name]={'layout':'diagram','kind':'conceptual','pixels':[WIDTH,height],
    'print':{'file':'print/'+name,'source_sha256':hashlib.sha256((IMAGES/name).read_bytes()).hexdigest(),'sha256':hashlib.sha256((IMAGES/'print'/name).read_bytes()).hexdigest()}}
 REGISTRY.write_text(json.dumps(registry,indent=2)+'\n')
 if '--proof' in sys.argv:
  from prove_vignettes import proof
  proof()


if __name__=='__main__':main()
