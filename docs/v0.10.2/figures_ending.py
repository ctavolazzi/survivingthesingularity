"""Recompose ten ending diagrams with matched screen and white-print geometry.

Only owned SVGs, art-ending-changes.json and proof artifacts are written.
No registry, canonical text, rights catalogue or full-book build is changed.
Run: python3 docs/v0.10.2/figures_ending.py --proof
"""
from pathlib import Path
from html import escape
import importlib.util
import json
import hashlib
import sys
import base64
import math

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
IMAGES = ROOT / 'static/book-images'
BASELINE = ROOT.parent / 'sts-v0.10.1' / 'static/book-images'
spec = importlib.util.spec_from_file_location('v101_art', ROOT/'docs/v0.10.1/vignettes.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Art = module.Art


def rect(a,x,y,w,h,color='ink',fill='none',width=1.5,dash=None):
 a.path(f'M{x} {y}H{x+w}V{y+h}H{x}Z',color,width,fill,dash)


def arrow(a,x,y,x2,y2,color='ink',width=1.6):
 a.line(x,y,x2,y2,color,width)
 theta=math.atan2(y2-y,x2-x)
 for d in [-.5,.5]:
  a.line(x2,y2,x2-8*math.cos(theta+d),y2-8*math.sin(theta+d),color,width)


def shell(mode):
 a=Art(mode,450,'A double-wide shell','Conceptual plan of two nominal forty-by-eight-foot containers. Their combined exterior footprint is640 square feet, not usable interior area. Foundations, openings, connections and reinforcement require project-specific design.')
 a.text(20,77,'Conceptual plan; no connection recipe.')
 a.line(75,111,405,111);a.line(75,105,75,119);a.line(405,105,405,119)
 a.text(240,101,'40 ft nominal',14,'ink',anchor='middle')
 rect(a,75,141,330,132,'ink','paper',2)
 a.line(75,207,405,207,'amber',2,'5 5')
 for x in [75,405]:
  for y in [141,207,273]:rect(a,x-3,y-3,6,6,'amber','amber',1)
 a.text(240,174,'Workshop',17,'ink',anchor='middle')
 a.text(240,246,'Home',17,'ink',anchor='middle')
 a.line(50,141,50,273);a.line(44,141,56,141);a.line(44,273,56,273)
 a.text(33,186,'8',14,'ink',anchor='middle');a.text(33,205,'ft',14,'ink',anchor='middle')
 a.text(33,249,'8',14,'ink',anchor='middle');a.text(33,268,'ft',14,'ink',anchor='middle')
 a.text(240,308,'40 ft × 16 ft = 640 sq ft',17,'ink',anchor='middle')
 a.text(240,333,'Nominal outside footprint, not floor area.',14,anchor='middle')
 a.footer(383,['Openings, foundations, joints and reinforcement','need a site-specific engineered design.','The chapter’s budget belongs to its fiction.'])
 return a


def thermal(mode):
 a=Art(mode,500,'A wall is an assembly','Conceptual wall section with steel, insulation and air control, and an interior layer. Insulation reduces conduction without eliminating it. Moisture, ventilation and required fire protection belong in the complete design.')
 a.text(20,78,'Conceptual section, not a thickness schedule.')
 a.text(20,113,'Example heat flow',14,'ink')
 rect(a,149,147,20,130,'ink','paper',2)
 rect(a,181,147,109,130,'amber','paper',2)
 for i in range(0,100,12):a.line(187+i,157,187+i,267,'rule',.8)
 a.line(178,147,178,277,'blue',3)
 rect(a,303,147,22,130,'ink','paper',2)
 arrow(a,22,212,133,212,'amber',1.6)
 arrow(a,340,212,450,212,'amber',1.6)
 for x,n in [(159,'1'),(235,'2'),(314,'3')]:
  a.circle(x,301,12,'ink',1.3,'paper');a.text(x,306,n,14,'ink',anchor='middle')
 a.text(20,342,'1  Steel skin')
 a.text(20,364,'2  Insulation + continuous air control')
 a.text(20,386,'3  Interior finish + required fire protection')
 a.footer(431,['Idealized layer: heat flow = k × A × ΔT / d','Design moisture control and ventilation too.','Heat flow depends on the whole assembly.'])
 return a


def mesh(mode):
 a=Art(mode,540,'A second route must exist','A single-uplink network loses its connection when the tower fails. A four-node mesh routes around a failed link only because another powered and tested path remains.')
 a.text(20,80,'ONE UPLINK IN THIS EXAMPLE',14,'ink',weight=600)
 a.path('M226 162L240 111L254 162M232 139H248','blue',2)
 a.circle(240,105,4,'blue',1,'blue')
 for x in [90,240,390]:
  a.line(240,168,x,213,'rule',1.3,'4 5');a.circle(x,220,9,'ink',1.5,'paper')
  a.text(x,248,'Home',14,'ink',anchor='middle')
 a.path('M271 130L288 148M288 130L271 148','amber',3)
 a.text(20,280,'Tower fails: this route is lost.')
 a.line(20,302,460,302)
 a.text(20,334,'MESH WITH AN ALTERNATE ROUTE',14,'ink',weight=600)
 a.line(110,373,220,373,'rule',1.5,'4 5');a.line(260,373,370,373,'rule',1.5,'4 5')
 a.path('M232 365L248 381M248 365L232 381','amber',2.5)
 a.path('M110 373V449H370V373','blue',2.5)
 for x,y in [(110,373),(370,373),(110,449),(370,449)]:a.circle(x,y,9,'ink',1.5,'paper')
 a.text(240,414,'usable route below',14,anchor='middle')
 a.footer(505,['Test coverage, power and a missing relay.'])
 return a


def clt(mode):
 a=Art(mode,500,'Land and homes, separate','A typical community land trust homeownership arrangement. A household owns the home; the trust holds the land under a long renewable ground lease with resale restrictions. Taxes, debt and stewardship duties remain.')
 a.text(20,77,'A common housing model; terms vary.')
 # House sits above its ground, visibly distinct from its lease document.
 a.path('M49 240L199 193L430 249L280 296Z','amber',2,'paper')
 a.path('M161 154L233 101L307 154Z','ink',2,'paper')
 rect(a,175,155,119,85,'ink','paper',2)
 rect(a,194,179,23,29,'blue','paper',1.5);rect(a,245,190,29,50,'ink','paper',1.5)
 a.text(280,276,'Trust’s land',14,'ink',anchor='middle')
 # A small agreement, separate from the physical building.
 rect(a,337,122,90,84,'blue','paper',1.3)
 for y in [142,152,162]:a.line(349,y,413,y,'rule',1)
 a.path('M349 188Q364 174 378 187T415 182','blue',1.4)
 a.text(382,227,'Lease',14,'ink',anchor='middle')
 a.text(20,336,'Household: owns the home',16,'ink')
 a.text(20,361,'Trust: holds and stewards the land',16,'ink')
 a.footer(412,['Often a 99-year renewable ground lease.','Resale terms aim to retain affordability.','Taxes, debt and governance duties remain.'])
 return a


def sneakernet(mode):
 a=Art(mode,424,'A library walks across town','A checked file moves between two computers on hand-carried storage. No live network link is required. Private material may be encrypted, but loss, copying, incompatible software and unsafe endpoints remain possible.')
 a.text(92,82,'Prepare',16,'ink',anchor='middle');a.text(387,82,'Receive',16,'ink',anchor='middle')
 for x in [28,323]:
  rect(a,x,118,130,86,'blue','paper',1.8)
  for yy in [140,155,170]:a.line(x+16,yy,x+100,yy,'rule',1)
  a.path(f'M{x+65} 205V222M{x+37} 223H{x+93}','blue',1.7)
 # Cut corner identifies storage without asserting a particular capacity.
 a.path('M215 126H248L265 143V200H215Z','amber',2,'paper')
 for x in [222,232,242,252]:a.line(x,177,x,192,'amber',2)
 arrow(a,169,161,205,161,'ink');arrow(a,277,161,312,161,'ink')
 a.text(92,251,'Check files',14,anchor='middle');a.text(387,251,'Open + verify',14,anchor='middle')
 a.text(240,286,'Carry a copy. No live link required.',14,'ink',anchor='middle')
 a.footer(336,['Trusted handling and compatible software.','Encrypt private material; keep a backup.','Loss, copying and unsafe endpoints remain.'])
 return a


def dc(mode):
 a=Art(mode,585,'Two routes to a DC load','Solar charging and storage feed two conceptual paths to an already-DC device. The inverter path converts DC to AC and an adapter converts it back. The DC route still needs voltage regulation and protection. Both have charging, wiring and operating losses; compare at the intended load.')
 a.text(20,78,'Same device. Compare the complete systems.')
 # Shared upstream chain: a panel, control plate and battery.
 rect(a,31,111,91,48,'blue','paper',1.5)
 for x in [52,76,100]:a.line(x,112,x,158,'rule',.8)
 a.line(32,135,121,135,'rule',.8)
 rect(a,191,111,98,48,'ink','paper',1.5)
 for x in [208,222,236,250,264]:a.line(x,122,x,146,'rule',1)
 rect(a,357,115,76,42,'amber','paper',1.6);rect(a,382,107,25,8,'amber','paper',1.5)
 arrow(a,133,135,181,135);arrow(a,300,135,347,135)
 a.text(77,184,'Solar',14,'ink',anchor='middle');a.text(240,184,'Charge control',14,'ink',anchor='middle');a.text(395,184,'Battery',14,'ink',anchor='middle')
 a.line(395,200,395,213,'rule');a.line(123,213,360,213,'rule');a.line(395,213,360,213,'rule')
 a.text(123,249,'INVERTER PATH',14,'ink',anchor='middle');a.text(360,249,'DC PATH',14,'ink',anchor='middle')
 arrow(a,123,264,123,280);arrow(a,360,264,360,306)
 a.text(123,305,'Inverter',16,'ink',anchor='middle');a.text(123,326,'DC → AC',14,anchor='middle')
 arrow(a,123,340,123,356)
 a.text(123,381,'Adapter',16,'ink',anchor='middle');a.text(123,402,'AC → DC',14,anchor='middle')
 a.text(360,332,'Regulation +',14,'ink',anchor='middle');a.text(360,354,'fused distribution',14,'ink',anchor='middle')
 a.text(360,383,'matched voltage',14,anchor='middle')
 arrow(a,123,418,123,447);arrow(a,360,401,360,447)
 for x in [123,360]:
  rect(a,x-44,456,88,32,'ink','paper',1.5);a.text(x,478,'DC load',14,'ink',anchor='middle')
 a.footer(530,['Charging, wires and regulation still lose energy.','Both need protection and voltage matching.','Conceptual energy paths, not a wiring plan.'])
 return a


def fab(mode):
 a=Art(mode,562,'A neighborhood fab lab','A printer, a metalworking station and a shared walk-behind tractor are tools for selected jobs. Suitable materials, trained people, maintenance and checking remain necessary. Commercial tractor forms are not labelled open source, and parts are not guaranteed fit for every application.')
 a.text(20,78,'Suitable stock + usable salvage',16,'ink')
 a.text(20,102,'Materials, designs and spares come from outside.')
 # Printer frame and moving bed.
 rect(a,30,149,114,121,'blue','none',2)
 a.line(40,168,134,168,'blue',2);rect(a,74,163,20,20,'blue','paper',1.5)
 a.path('M84 184V201M46 245H130M64 244V213H103V244','ink',2)
 # Metalwork table, plate and torch.
 a.path('M183 232H294M190 232V271M285 232V271M196 224H278','ink',2)
 a.path('M253 151L253 196L244 206','amber',2.5)
 for x,y in [(237,210),(251,213),(244,222)]:a.line(244,207,x,y,'amber',1.5)
 # Walk-behind tractor: wheels, engine and handle.
 a.circle(359,247,21,'ink',2);a.circle(359,247,8,'ink',1.5);a.circle(411,247,16,'ink',2)
 rect(a,358,203,50,29,'amber','paper',1.7)
 a.path('M380 203L422 159L444 159M365 232H414','ink',2)
 a.text(87,304,'Printer',14,'ink',anchor='middle');a.text(240,304,'Metalwork',14,'ink',anchor='middle')
 a.text(391,304,'Shared',14,'ink',anchor='middle');a.text(391,324,'tractor',14,'ink',anchor='middle')
 a.line(20,344,460,344)
 a.text(240,376,'Trained people · power · maintenance',14,'ink',anchor='middle')
 arrow(a,240,395,240,422,'amber',2)
 # A bracket is a specific modest output, not an unspecified safety-critical part.
 a.path('M188 467V432H210V450H285V467Z','ink',2,'paper')
 a.circle(200,443,3,'ink',1);a.circle(270,458,3,'ink',1)
 a.text(240,496,'Suitable, checked parts and field work',14,'ink',anchor='middle')
 a.footer(541,['Open designs do not make every tool open source.'])
 return a


def social(mode):
 a=Art(mode,535,'A floor people can rely on','A current vulnerability ties essentials to continuing earnings. A proposed arrangement funds supplies, remaining paid work, tools and backup capacity so people can receive essentials without a job. Adequate provision is a commitment to verify, not an achieved effect of robots or a closed loop.')
 a.text(120,80,'CURRENT VULNERABILITY',14,'ink',anchor='middle')
 a.text(359,80,'PROPOSED ARRANGEMENT',14,'ink',anchor='middle')
 a.line(240,105,240,438,'rule',1)
 # Earnings: envelope, then wage, then the price of essentials.
 a.path('M73 119H166V176H73ZM73 119L120 151L166 119','blue',1.7,'paper')
 a.text(120,205,'Paid work',16,'ink',anchor='middle');arrow(a,120,217,120,245)
 a.text(120,273,'Wage',16,'ink',anchor='middle');arrow(a,120,285,120,315)
 a.text(120,343,'Buy essentials',16,'ink',anchor='middle')
 a.text(120,395,'Income can fail;',14,anchor='middle');a.text(120,417,'needs continue.',14,anchor='middle')
 # Public ledger with a deliberately unfinished final check.
 rect(a,309,115,104,68,'amber','paper',1.6,'5 5')
 for y in [133,148,163]:a.line(325,y,398,y,'rule',1)
 a.text(359,212,'Funded provision',15,'ink',anchor='middle')
 a.text(359,244,'Supplies + paid work',14,anchor='middle')
 a.text(359,267,'Tools + backup',14,anchor='middle')
 arrow(a,359,281,359,315,'amber')
 a.text(359,343,'Deliver essentials',15,'ink',anchor='middle')
 a.text(359,395,'Access without a job;',14,anchor='middle');a.text(359,417,'check who receives it.',14,anchor='middle')
 a.footer(477,['Fund the promise. Keep people able to challenge it.','Adequacy is measured at the recipient’s end.'])
 return a


RUNGS=[
 (9,'Keep the market above the floor','Money stays; survival is the floor.'),
 (8,'Make the service accountable','Publish access, cost and unmet need.'),
 (7,'Widen the floor','NHS (1948); proposed basic services.'),
 (6,'Protect access to essentials','NYC eviction counsel (2017).'),
 (5,'Own the machines together','Rural electric co-ops (from 1936).'),
 (4,'Take land out of speculation','Land trusts; long-term ground leases.'),
 (3,'Make meals a public service','California school meals (2022–23).'),
 (2,'Feed people who ask','France (2016): surplus recovery rules.'),
 (1,'Count waste and food insecurity','California SB 1383 recovery records.')]


def ladder(mode):
 a=Art(mode,646,'Nine rungs, one public floor','Nine proposed steps, read from bottom to top. The first seven draw on bounded precedents, not a completed universal guarantee. Dashed rungs eight and nine describe accountability and keeping markets above the floor. France’s precedent concerns surplus recovery rules; land trusts use long-term leases.')
 a.text(20,74,'Start below. Build upward.')
 a.line(33,99,33,509,'blue',2);a.line(75,99,75,509,'blue',2)
 for i,(n,title,sub) in enumerate(RUNGS):
  y=111+i*46
  a.line(33,y+2,75,y+2,'amber',3,'5 5' if n>=8 else None)
  a.text(54,y-8,str(n),14,'ink',anchor='middle')
  a.text(96,y,title,14,'ink',weight=600);a.text(96,y+20,sub,14)
 a.line(25,547,67,547,'amber',3);a.text(83,551,'Draws on a precedent')
 a.line(25,571,67,571,'amber',3,'5 5');a.text(83,575,'Proposed guardrail')
 a.footer(614,['Precedents support parts of this proposal.','None establishes the complete guarantee.'])
 return a


# Exact spans use source endpoints; broad period labels are explicitly approximate.
# Compact names are lookup labels, not replacements for Appendix D’s full titles.
TIMELINE=[
 ('P-01 Reading rage',1770,1830,True),('P-20 Paine’s pamphlet',1776,1776,False),
 ('P-07 Horse + ledger',1786,1949,True),('P-09 Frame-breakers',1811,1816,False),
 ('P-15 Homesteading',1862,1862,False),('P-04 Red Flag',1865,1865,False),
 ('P-02 Bell at the fair',1876,1876,False),('P-03 Flight forecast',1903,1903,False),
 ('P-16 Mail-order homes',1908,1940,True),('P-11 Torches',1929,1929,False),
 ('P-10 Recorded music',1929,1948,False),('P-23 NHS',1942,1948,False),
 ('P-19 Victory gardens',1943,1944,False),('P-14 Quartz watches',1962,1983,False),
 ('P-21 Access to tools',1968,1968,False),('P-17 Kodak',1975,2013,False),
 ('P-24 Web forecasts',1993,1995,False),('P-22 Y2K',1999,2004,False),
 ('P-18 Fujifilm',2000,2009,True)]
DEEP=[('P-08 Grain trap','c. 9500–6000 BC'),('P-12 Bronze networks','14th–12th c. BC'),
 ('P-05 Ming voyages','1405–1433'),('P-13 Abbot + press','1492–1494'),('P-06 Copernicus','1543')]


def timeline(mode):
 a=Art(mode,650,'Twenty-four precedents','Compact index of all twenty-four precedents. Nineteen appear against an axis from1700 to2025; five earlier cases have written dates. Dots identify one date, solid bars dated spans, and visibly dashed square-ended bars approximate periods. Full titles and dates remain in Appendix D.')
 x0,x1=248,457
 def x(year):return x0+(year-1700)/(2025-1700)*(x1-x0)
 for year in [1700,1800,1900,2025]:
  a.line(x(year),88,x(year),450,'rule',.7)
  a.text(x(year),76,str(year),14,anchor='end' if year==2025 else 'middle')
 for i,(label,start,end,approx) in enumerate(TIMELINE):
  y=105+i*19
  a.text(20,y,label,14,'ink')
  if start==end:a.circle(x(start),y-5,2.8,'amber',1,'amber')
  else:a.line(x(start),y-5,x(end),y-5,'amber',3,'3 4' if approx else None)
 a.text(20,475,'Dots: one date. Dashed: approximate period.')
 a.text(20,501,'EARLIER CASES',14,'ink',weight=600)
 for i,(label,dates) in enumerate(DEEP):
  y=526+i*20
  a.text(20,y,label,14,'ink');a.text(248,y,dates,14,'amber')
 a.text(20,637,'Full names and dates: Appendix D.')
 return a


BUILDERS={
 'ch13-shell-architecture':shell,'ch13-thermal-seal':thermal,'ch14-mesh-comms':mesh,
 'ch15-clt-firewall':clt,'ch16-sneakernet':sneakernet,'ch17-dc-native':dc,
 'ch17-fab-lab':fab,'ch18-social-contract':social,'ch19-conversion-ladder':ladder,
 'appd-precedent-timeline':timeline}
CAPTIONS={
 'ch13-shell-architecture':'Two nominal forty-foot containers give a 640-square-foot exterior footprint. Usable space and structural details depend on the finished design; the chapter’s budget is fictional.',
 'ch13-thermal-seal':'Insulation is one layer in a wall. Air control, moisture, ventilation and fire protection have to work with it.',
 'ch14-mesh-comms':'A mesh can route around a break only where another powered, usable path remains. Test the missing relay.',
 'ch15-clt-firewall':'A common land-trust housing arrangement separates ownership of land and home. Resale terms need continuing stewardship; taxes and debt remain.',
 'ch16-sneakernet':'A hand-carried copy needs no live network link. It still needs trusted handling, a compatible reader and a recoverable backup.',
 'ch17-dc-native':'For a load that already uses DC, compare the whole path. Avoiding an inverter pair does not remove charging, wiring or regulation losses.',
 'ch17-fab-lab':'A neighborhood fab lab combines suitable tools with trained people, supported materials and checks for the actual job.',
 'ch18-social-contract':'The proposal makes essentials a funded floor, available without a job. Tools help; remaining work, supplies and reliable delivery still need provision.',
 'ch19-conversion-ladder':'Read from the bottom up. The first seven rungs draw on bounded precedents; the final two describe how the proposal would be maintained.',
 'appd-precedent-timeline':'All twenty-four precedents. Square-ended dashed bars mark approximate periods; exact dates and complete titles are in Appendix D.'}
SOURCES={
 'ch13-shell-architecture':['Chapter13 corrected canonical prose; ART-AUDIT A07. Geometry is a nominal exterior-footprint illustration, not a construction drawing.'],
 'ch13-thermal-seal':['Chapter13 corrected canonical prose; DOE Insulation Guide cited in AppendixB. No material thickness is prescribed.'],
 'ch14-mesh-comms':['Chapter14 canonical prose; Meshtastic mesh documentation cited in AppendixB. Graph is illustrative, not a tested installation.'],
 'ch15-clt-firewall':['Chapter15 corrected canonical prose; Grounded Solutions Network typical homeownership model.'],
 'ch16-sneakernet':['Chapter16 corrected canonical prose; ART-AUDIT A08. Physical transport removes the need for a live link, not endpoint/media risks.'],
 'ch17-dc-native':['Chapter17 canonical prose; DOE DC Microgrid Scoping Study cited in AppendixB. Configuration-dependent energy paths, no efficiency percentages.'],
 'ch17-fab-lab':['Chapter17 corrected canonical prose; ART-AUDIT A12. A shared commercial tractor is distinct from a licensed open machine design.'],
 'ch18-social-contract':['Chapter18 corrected canonical prose; ART-AUDIT A09. A proposed funded service, not achieved local abundance.'],
 'ch19-conversion-ladder':['Chapter19 corrected canonical prose and AppendixB sources for each precedent; ART-AUDIT A10. Legal examples are bounded as in prose.'],
 'appd-precedent-timeline':['AppendixD current precedent index; ART-AUDIT A13. Approximate spans retain the prior diagram’s illustrative endpoints (1770–1830, 1786–1949, 1908–1940, 2000–2009); Appendix D supplies their broader period descriptions. The axis begins at 1700; no new historical dates are asserted.']}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
 records=[]
 for key,builder in BUILDERS.items():
  item={'file':key+'.svg','width':480,'height':builder('screen').height,'source':'docs/v0.10.2/figures_ending.py','provenance':SOURCES[key],'recommended_caption':CAPTIONS[key],'kind':'conceptual' if key!='appd-precedent-timeline' else 'historical_timeline'}
  for mode in ['screen','print']:
   art=builder(mode);text=art.finish().replace('footprint is640','footprint is 640').replace('from1700 to2025','from 1700 to 2025')
   path=IMAGES/('print' if mode=='print' else '')/(key+'.svg')
   path.write_text(text);assert path.read_text()==text
   baseline=BASELINE/('print' if mode=='print' else '')/(key+'.svg')
   item[mode]={'file':str(path.relative_to(IMAGES)),'sha256':sha(path),'baseline_sha256':sha(baseline)}
   if mode=='screen':
    import xml.etree.ElementTree as ET
    doc=ET.fromstring(text)
    item['recommended_alt']=doc.find('{http://www.w3.org/2000/svg}desc').text
    item['meaning']=item['recommended_alt']
  import xml.etree.ElementTree as ET
  def geometry_fingerprint(path):
   svg=ET.fromstring(path.read_text())
   for child in list(svg):
    if child.tag.endswith('}rect') and child.attrib.get('width')=='480' and child.attrib.get('height')==str(item['height']) and child.attrib.get('fill')=='#ffffff':svg.remove(child)
   for node in svg.iter():
    for attr in ['fill','stroke']:node.attrib.pop(attr,None)
   return ET.tostring(svg)
  assert geometry_fingerprint(IMAGES/item['screen']['file'])==geometry_fingerprint(IMAGES/item['print']['file']),key
  item['geometry_pair_verified']=True
  item['dimensions']=[480,item['height']]
  item['print']['source_sha256']=item['screen']['sha256']
  records.append(item)
 report={'edition':'0.10.2','figures':records,'registry_integration':'Root-owned; this generator never writes shared registries or canonical prose.','geometry':'480 units wide; all labels at least 14 units; screen and print geometry is identical except print background.'}
 report_path=HERE/'art-ending-changes.json';report_path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');assert json.loads(report_path.read_text())==report
 if '--proof' in sys.argv:proof()
 print(json.dumps({'generated':len(records),'assets':len(records)*2,'maximum_height':max(x['height'] for x in records)}))


METRICS=r'''() => {
 const svg=document.querySelector('svg'),frame=svg.getBoundingClientRect(), ts=[...svg.querySelectorAll('text')];
 const boxes=ts.map(t=>({text:t.textContent,...t.getBoundingClientRect().toJSON()}));const overlaps=[];
 for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const a=boxes[i],b=boxes[j];if(a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom)overlaps.push([a.text,b.text]);}
 return {labels:ts.length,min_user_units:Math.min(...ts.map(t=>parseFloat(getComputedStyle(t).fontSize))),min_pt:Math.min(...ts.map(t=>parseFloat(getComputedStyle(t).fontSize)*frame.width/svg.viewBox.baseVal.width*.75)),width_in:frame.width/96,height_in:frame.height/96,overlaps,outside:boxes.filter(b=>b.left<frame.left||b.right>frame.right||b.top<frame.top||b.bottom>frame.bottom).map(b=>b.text)};
}'''


def proof():
 from playwright.sync_api import sync_playwright
 spec=importlib.util.spec_from_file_location('legacy_geometry',ROOT/'docs/v0.9.2/print_figures.py')
 geometry=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry)
 out=HERE/'art-ending-proof';out.mkdir(exist_ok=True)
 font=base64.b64encode((ROOT/'publication/assets/fonts/JetBrainsMono-Regular.ttf').read_bytes()).decode()
 style=f"@font-face{{font-family:'JetBrains Mono';src:url(data:font/ttf;base64,{font})}}body{{margin:0}}svg{{display:block;width:4.56in;height:auto}}"
 checks={};controls={}
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='chrome');page=browser.new_page(viewport={'width':600,'height':800},device_scale_factor=1)
  def load(text,mode='print'):
   page.set_content(f'<style>{style}body{{background:{"#020617" if mode=="screen" else "#fff"}}}</style>'+text);page.evaluate('document.fonts.ready')
  sample=shell('print').finish();load(sample)
  page.evaluate("document.querySelector('text').setAttribute('font-size','4')")
  assert page.evaluate(METRICS)['min_pt']<8;controls['undersized_label_detected']=True
  load(sample);page.evaluate("const t=document.querySelectorAll('text');t[1].setAttribute('x',t[0].getAttribute('x'));t[1].setAttribute('y',t[0].getAttribute('y'))")
  assert page.evaluate(METRICS)['overlaps'];controls['overlapping_labels_detected']=True
  load(sample);page.evaluate("document.querySelector('text').setAttribute('x','470')")
  assert page.evaluate(METRICS)['outside'];controls['out_of_frame_label_detected']=True
  load(sample);page.evaluate("const t=document.querySelector('text'),b=t.getBBox(),l=document.createElementNS('http://www.w3.org/2000/svg','path');l.setAttribute('d',`M${b.x} ${b.y+b.height/2}h${b.width}`);l.setAttribute('stroke','red');t.parentNode.append(l)")
  assert any('crosses' in x for x in page.evaluate(geometry.AUDIT_JS));controls['path_through_label_detected']=True
  for key in BUILDERS:
   checks[key]={}
   for mode in ['screen','print']:
    path=IMAGES/('print' if mode=='print' else '')/(key+'.svg');load(path.read_text(),mode)
    measured=page.evaluate(METRICS);measured['path_errors']=page.evaluate(geometry.AUDIT_JS)
    checks[key][mode]=measured
    page.locator('svg').screenshot(path=str(out/f'{key}-{mode}.png'))
  browser.close()
 report={'figures':checks,'negative_controls':controls,'limits':'Actual 4.56-inch browser rendering with embedded JetBrains Mono, label bounds/overlap and sampled path intersections. Does not certify physical print contrast, other-reader font substitution or full-book pagination.'}
 (out/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
 errors={k:{m:r for m,r in v.items() if r['min_user_units']<14 or r['min_pt']<8 or r['overlaps'] or r['outside'] or r['path_errors']} for k,v in checks.items()}
 errors={k:v for k,v in errors.items() if v}
 if errors:raise AssertionError(json.dumps(errors,indent=2))
 print(json.dumps({'proof_figures':len(checks),'min_pt':min(v['print']['min_pt'] for v in checks.values()),'negative_controls':controls}))


if __name__=='__main__':main()
