"""Four revised resource diagrams. Geometry is shared by screen and print."""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'docs/v0.10.1'))
from vignettes import Art, PALETTES


def arrow(a, x, y, x2, y2, color='blue'):
    import math
    a.line(x, y, x2, y2, color, 2)
    angle = math.atan2(y2-y, x2-x)
    for offset in (-.55, .55):
        a.line(x2, y2, x2-8*math.cos(angle+offset), y2-8*math.sin(angle+offset), color, 2)


def network(mode):
    a=Art(mode, 560, 'A NETWORK THAT MUST DELIVER',
          'A proposed growing and tool network coordinated by people. Food and support reach households through paid work, transport and backup. Each resource has its own supply and demand budget.')
    a.text(20,77,'Proposed service, not a measured yield')
    for x,title,lines in [(20,'Growing site',['Water · power','Crops · tending']), (260,'Shared workshop',['Tools · parts','Repairs · upkeep'])]:
        a.path(f'M{x} 99H{x+200}V190H{x}Z','ink',1.5)
        a.text(x+12,124,title,17,'ink')
        for i,line in enumerate(lines):a.text(x+12,150+i*21,line)
    arrow(a,120,194,120,235);arrow(a,360,194,360,235)
    a.line(120,235,360,235,'blue',2);arrow(a,240,235,240,257)
    a.text(240,286,'People coordinate the service',17,'ink',anchor='middle')
    a.text(240,311,'Requests · stock · routes · backup',anchor='middle')
    arrow(a,240,329,240,366,'amber')
    a.path('M145 408L240 374L335 408V450H145Z','ink',2)
    a.text(240,422,'Households',18,'ink',anchor='middle')
    a.text(240,443,'Food and support',anchor='middle')
    a.footer(488,['Budget food, energy, water and work separately.','A surplus in one cannot cancel a shortage','in another. Delivery still needs people.'])
    return a


def shockwave(mode):
    a=Art(mode,552,'WHEN REPLENISHMENT BREAKS',
          'An illustrative chain from disruption to delayed deliveries and pressure on local stock, with rerouting and replenishment as possible responses. No fixed countdown or inevitable collapse is implied.')
    a.text(20,77,'Illustrative sequence, not a four-day clock')
    stages=[('Upstream disruption','A port, supplier or ordering system fails.'),
            ('Deliveries delayed','Stock arrives late or takes another route.'),
            ('Local buffer under pressure','Demand and remaining stock set the pace.'),
            ('Service response','Reroute, replenish and prioritize needs.')]
    for y in (133,221,309):a.line(42,y,42,y+58,'blue',2)
    for i,(title,detail) in enumerate(stages):
        y=124+i*88
        a.circle(42,y-6,15,'amber',2,fill='paper');a.text(42,y,str(i+1),16,'ink',anchor='middle')
        a.text(72,y,title,17,'ink');a.text(72,y+26,detail,14)
    a.footer(473,['There is no universal time to empty shelves.','Buffers, alternative routes, replenishment','and demand change the outcome.'])
    return a


def soil(mode):
    a=Art(mode,598,'SOIL CYCLES, HARVEST LEAVES',
          'Plants exchange carbon with a soil food web. Decomposition and grazing cycle nutrients; harvest removes nutrients and losses also occur. Soil care includes measurement and appropriate replenishment.')
    a.text(20,77,'A nutrient cycle is not a sealed container')
    # Growing plant and root zone, with a harvest leaving the field.
    a.path('M100 228V126M100 157Q63 119 66 156Q83 174 100 166M100 142Q133 108 135 142Q120 159 100 153','amber',2)
    a.path('M100 224L79 255M100 231L117 262M95 237L96 273M80 255L59 265M117 262L137 270','ink',2)
    a.line(20,223,460,223,'rule',2)
    a.text(20,108,'Light + water',color='ink')
    arrow(a,149,160,260,160,'amber');a.text(283,155,'Harvest',17,'ink');a.text(283,181,'Nutrients leave')
    a.text(168,244,'Roots supply carbon',color='ink')
    a.text(168,268,'to the soil food web.')
    arrow(a,99,286,99,322)
    a.text(20,349,'Bacteria + fungi',17,'ink');a.text(20,375,'Decomposition')
    a.text(267,349,'Microbial grazers',17,'ink');a.text(267,375,'Nutrient cycling')
    arrow(a,193,345,248,345)
    a.path('M355 393V428H8V245H63','blue',2);a.path('M55 238L63 245L55 252','blue',2)
    a.text(240,456,'Nutrients can return to plant uptake.',anchor='middle')
    a.footer(513,['Harvest and losses draw down the budget.','Test the soil, keep it covered, and replenish','what the crop and site actually require.'])
    return a


def algae(mode):
    a=Art(mode,618,'WATER LOOP, FEED BRANCH',
          'Aquaponic water recirculates from a fish tank through solids handling and biofiltration to grow beds and back. Algae cultivation is a separate branch whose harvested output may supply a validated share of feed. Feed, nutrients, water, power and labor remain inputs.')
    a.text(20,77,'Conceptual flows, not a construction plan')
    a.text(20,112,'1  AQUAPONIC WATER',17,'ink')
    a.path('M20 135H180V204H20Z','blue',2)
    a.text(100,165,'Fish tank',17,'ink',anchor='middle');a.text(100,189,'Feed enters',anchor='middle')
    arrow(a,182,169,259,169)
    a.text(274,149,'Solids handling',color='ink');a.text(274,172,'+ biofiltration',color='ink')
    arrow(a,351,189,351,224)
    a.path('M267 229H457V298H267Z','blue',2)
    a.text(362,257,'Grow beds',17,'ink',anchor='middle');a.text(362,282,'Plants take nutrients',14,anchor='middle')
    a.path('M264 270H100V209','blue',2);a.path('M93 217L100 209L107 217','blue',2)
    a.text(20,315,'Return water',color='ink');a.text(264,323,'Plant harvest leaves')
    a.line(20,345,460,345)
    a.text(20,378,'2  POSSIBLE ALGAE FEED',17,'ink')
    a.text(20,410,'Cultivation',17,'ink');a.text(20,434,'Light, nutrients');a.text(20,456,'and water')
    arrow(a,157,409,230,409,'amber')
    a.text(250,408,'Harvest + prepare',17,'ink');a.text(250,434,'Check species, diet');a.text(250,456,'and feed contribution')
    a.text(20,490,'Validated feed contribution → fish tank',color='ink')
    a.footer(541,['Algae is not automatically a complete feed.','Feed, nutrients, water, power and human work','remain part of the operating budget.'])
    return a


BUILDERS={'ch12-csa-network.svg':network,'ch14-logistic-shockwave.svg':shockwave,
          'ch15-soil-food-web.svg':soil,'ch17-algae-loop.svg':algae}


def main():
    records=[]
    for name,builder in BUILDERS.items():
        record={'file':name,'generator':'docs/v0.10.2/figures_core.py','kind':'conceptual','pixels':[480,builder('print').height],
                'provenance':'Original native SVG revision; semantics aligned with the reviewed canonical chapter and its bibliography. No new numerical dataset.'}
        for mode in PALETTES:
            p=ROOT/'static/book-images'/('print' if mode=='print' else '')/name
            content=builder(mode).finish();p.write_text(content);assert p.read_text()==content
            record[mode+'_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
        records.append(record)
    path=HERE/'art-core-changes.json';path.write_text(json.dumps(records,indent=2)+'\n')
    assert json.loads(path.read_text())==records


if __name__=='__main__':main()
