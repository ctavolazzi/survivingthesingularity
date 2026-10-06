"""Produce the grayscale print interior, retaining the color master and reading PDF."""
from pathlib import Path
import hashlib
import json
import subprocess
import time
from prune_pdf_resources import prepare
from pypdf import PdfReader, PdfWriter
from pypdf.constants import PageLabelStyle

HERE=Path(__file__).resolve().parent
OUT=HERE/'output'
ROOT_BOOKJSON=HERE.parent/'src/lib/data/book/book.json'
source=OUT/'Surviving-the-Singularity-interior.pdf'
prepared=OUT/'print-prepared.pdf'
converted=OUT/'print-converted.pdf'
target=OUT/'Surviving-the-Singularity-print-interior.pdf'
preparation=prepare(source,prepared)
print('Print resource preparation:',json.dumps(preparation),flush=True)
conversion_start=time.monotonic()
subprocess.run(['gs','-q','-dBATCH','-dNOPAUSE','-dPDFSTOPONERROR','-sDEVICE=pdfwrite','-dCompatibilityLevel=1.7','-sColorConversionStrategy=Gray','-dProcessColorModel=/DeviceGray','-dEmbedAllFonts=true','-dSubsetFonts=false','-dDownsampleColorImages=false','-dDownsampleGrayImages=false','-dDownsampleMonoImages=false',f'-sOutputFile={converted}',str(prepared)],check=True)
conversion_seconds=round(time.monotonic()-conversion_start,2)
if len(PdfReader(converted).pages)!=preparation['pages']:
    raise RuntimeError('Ghostscript conversion lost pages')
writer=PdfWriter(clone_from=converted)
added_blank=False
if len(writer.pages)%2:
    writer.add_blank_page(width=432,height=648)
    added_blank=True
writer.set_page_label(0,3,style=PageLabelStyle.LOWERCASE_ROMAN,start=1)
writer.set_page_label(4,len(writer.pages)-1,style=PageLabelStyle.DECIMAL,start=1)
writer.add_metadata({'/Title':'Surviving the Singularity','/Author':'Christopher Tavolazzi','/Subject':'6 x 9 inch grayscale print interior, manuscript v' + json.loads(open(ROOT_BOOKJSON).read())['version']})
writer.write(target)
record=json.loads((OUT/'build.json').read_text())
record['outputs']['print-interior']={'path':str(target),'pages':len(writer.pages),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'grayscale':True,'blank_final_verso_added':added_blank,'resource_pruning':preparation,'conversion_seconds':conversion_seconds}
(OUT/'build.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record['outputs']['print-interior'],indent=2))
