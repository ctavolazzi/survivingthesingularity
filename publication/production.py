"""Produce the grayscale print interior, retaining the color master and reading PDF."""
from pathlib import Path
import hashlib
import json
import subprocess
from pypdf import PdfReader, PdfWriter
from pypdf.constants import PageLabelStyle

HERE=Path(__file__).resolve().parent
OUT=HERE/'output'
source=OUT/'Surviving-the-Singularity-interior.pdf'
converted=OUT/'print-converted.pdf'
target=OUT/'Surviving-the-Singularity-print-interior.pdf'
subprocess.run(['gs','-q','-dBATCH','-dNOPAUSE','-sDEVICE=pdfwrite','-dCompatibilityLevel=1.7','-sColorConversionStrategy=Gray','-dProcessColorModel=/DeviceGray','-dEmbedAllFonts=true','-dSubsetFonts=false','-dDownsampleColorImages=false','-dDownsampleGrayImages=false','-dDownsampleMonoImages=false',f'-sOutputFile={converted}',str(source)],check=True)
writer=PdfWriter(clone_from=converted)
added_blank=False
if len(writer.pages)%2:
    writer.add_blank_page(width=432,height=648)
    added_blank=True
writer.set_page_label(0,3,style=PageLabelStyle.LOWERCASE_ROMAN,start=1)
writer.set_page_label(4,len(writer.pages)-1,style=PageLabelStyle.DECIMAL,start=1)
writer.add_metadata({'/Title':'Surviving the Singularity','/Author':'Christopher Tavolazzi','/Subject':'6 x 9 inch grayscale print interior, manuscript v0.8.2'})
writer.write(target)
record=json.loads((OUT/'build.json').read_text())
record['outputs']['print-interior']={'path':str(target),'pages':len(writer.pages),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'grayscale':True,'blank_final_verso_added':added_blank}
(OUT/'build.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record['outputs']['print-interior'],indent=2))
