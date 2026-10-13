"""Verify release receipts, create versioned delivery copies and their manifest."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import zipfile
from pypdf import PdfReader

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'publication/output'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())


def main():
    source=read(HERE/'final-source.json')
    assert source['version']=='0.10.2'
    for name,digest in source['files'].items():assert sha(ROOT/'src/lib/data/book'/name)==digest,name
    proof=read(OUT/'proof/checks.json')
    for key in ['missing_text_blocks','text_outside_page','broken_internal_links','missing_assets','figure_layout_errors']:
        assert not proof[key],key
    assert proof['source_sections_unchanged']==35 and proof['manifest_unchanged']
    assert all(proof['fonts_embedded'].values())
    assert len(proof['registered_figures'])==54
    resources=read(ROOT/'docs/publication/PDF-RESOURCE-CHECKS.json')
    assert resources['overall_pass'] and all(resources['negative_controls'].values())
    epub=ROOT/'book-build/Surviving-the-Singularity-v0.10.2.epub'
    epub_check=read(HERE/'epub-checks.json');layout=read(HERE/'epub-proof/checks.json')
    assert sha(epub)==epub_check['epub_sha256']==layout['epub_sha256']
    assert not epub_check['missing_blocks'] and not epub_check['resource_errors'] and not epub_check['art_errors']
    assert not layout['layout_errors'] and not layout['missing_requests']
    for report in ['pdf-proof/FINAL-PDF-REVIEW.md','EPUB-REVIEW.md','READER-REVIEW.md','INDEX-REVIEW.md']:
        assert (HERE/report).is_file(),report
    package=OUT/'Surviving-the-Singularity-v0.10.2-editable-publication.zip'
    with zipfile.ZipFile(package) as archive:assert archive.testzip() is None
    build=read(OUT/'build.json');deliveries=[]
    for kind,suffix in [('reading',''),('print-interior','-print-interior'),('front-cover','-front-cover')]:
        src=OUT/f'Surviving-the-Singularity-{kind}.pdf'
        assert sha(src)==build['outputs'][kind]['sha256']
        target=ROOT/f'book-build/Surviving-the-Singularity-v0.10.2{suffix}.pdf'
        if target.exists():assert sha(target)==sha(src),'Refusing to replace changed delivery: '+str(target)
        else:shutil.copyfile(src,target)
        assert sha(target)==sha(src)
        deliveries.append({'kind':kind,'path':str(target.relative_to(ROOT)),'bytes':target.stat().st_size,'sha256':sha(target),'pages':len(PdfReader(target).pages)})
    for kind,path in [('epub',epub),('markdown',ROOT/'manuscript/Surviving-the-Singularity-v0.10.2.md'),('editable_package',package)]:
        deliveries.append({'kind':kind,'path':str(path.relative_to(ROOT)),'bytes':path.stat().st_size,'sha256':sha(path)})
    receipts=['source-review.json','art-integration.json','art-release-checks.json','gate-results.json','epub-checks.json','epub-proof/checks.json','reader-proof/after.json','reader-proof/mobile-reader.json','package-negative-controls.json','pdf-proof/final-samples.json']
    report={'version':'0.10.2','finalized_utc':datetime.now(timezone.utc).isoformat(),'baseline_version':'0.10.1',
        'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source_uncommitted':True,
        'status':'Final local digital edition; no commit or external publication','source_files_sha256':source['files'],
        'sections':35,'images':102,'revised_svg_figures':31,'registered_figures':54,
        'outputs':deliveries,'proof_receipts':{name:sha(HERE/name) for name in receipts},
        'publication_pdf_proof_sha256':sha(OUT/'proof/checks.json'),'publication_resource_proof_sha256':sha(ROOT/'docs/publication/PDF-RESOURCE-CHECKS.json'),
        'limits':'Targeted source review and local digital proofs; inherited external cover/quotation decisions, physical printing and dedicated e-reader pagination remain separate.'}
    path=HERE/'deliverables.json';path.write_text(json.dumps(report,indent=2)+'\n');assert read(path)==report
    print(json.dumps({'version':report['version'],'deliveries':deliveries},indent=2))


if __name__=='__main__':main()
