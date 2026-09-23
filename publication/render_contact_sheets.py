"""Render every PDF page into inspectable contact sheets, retaining thumbnails."""
from pathlib import Path
import subprocess
import hashlib
import shutil
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader

HERE=Path(__file__).resolve().parent
PDF=HERE/'output/Surviving-the-Singularity-interior.pdf'
OUT=HERE/'output/proof/contact'
OUT.mkdir(parents=True,exist_ok=True)
digest=hashlib.sha256(PDF.read_bytes()).hexdigest()[:12]
snapshot=OUT/f'interior-{digest}.pdf'
shutil.copy2(PDF,snapshot)
PDF=snapshot
subprocess.run(['gs','-q','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r40',f'-sOutputFile={OUT}/page-%03d.png',str(PDF)],check=True)
count=len(PdfReader(PDF).pages)
for start in range(1,count+1,24):
    sheet=Image.new('RGB',(6*260,4*395),(226,227,221));draw=ImageDraw.Draw(sheet)
    for n in range(start,min(start+24,count+1)):
        index=n-start;x=(index%6)*260;y=(index//6)*395
        with Image.open(OUT/f'page-{n:03d}.png') as page: sheet.paste(page,(x+10,y+25))
        draw.text((x+12,y+8),f'PDF page {n}',fill=(30,40,32))
    sheet.save(OUT/f'sheet-{start:03d}-{min(start+23,count):03d}.jpg',quality=90)
    print(f'Contact sheet {start}-{min(start+23,count)}',flush=True)
