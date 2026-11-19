// Print the HTML made by make_pdf.py to a PDF with page numbers. Usage: node make_pdf.cjs in.html out.pdf [cover.png]
const { chromium } = require('playwright');
(async () => {
  const [, , input, output, cover] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + require('path').resolve(input), { waitUntil: 'load' });
  await p.pdf({
    path: output, width: '6in', height: '9in', printBackground: false, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;text-align:center;font-family:serif;font-size:8pt;color:#444;"><span class="pageNumber"></span></div>',
    margin: { top: '0.8in', bottom: '0.85in', left: '0.7in', right: '0.7in' },
  });
  if (cover) {
    // the cover is its own page, the same width as the book and as tall as the art, with no margins
    const sizeOf = require('child_process').execFileSync('python3', ['-c', 'from PIL import Image;import sys;im=Image.open(sys.argv[1]);print(im.width, im.height)', cover]).toString().trim().split(' ').map(Number);
    const h = (6 * sizeOf[1] / sizeOf[0]).toFixed(3) + 'in';
    const data = require('fs').readFileSync(cover).toString('base64');
    const c = await b.newPage();
    await c.setContent('<html><body style="margin:0"><img alt="Cover: Surviving the Singularity" src="data:image/png;base64,' + data + '" style="display:block;width:6in;height:' + h + '"></body></html>');
    await c.pdf({ path: output + '.cover.pdf', width: '6in', height: h, printBackground: true, margin: { top: '0', bottom: '0', left: '0', right: '0' } });
    require('fs').renameSync(output, output + '.body.pdf');
    require('child_process').execFileSync('pdfunite', [output + '.cover.pdf', output + '.body.pdf', output]);
    require('fs').unlinkSync(output + '.cover.pdf');
    require('fs').unlinkSync(output + '.body.pdf');
  }
  await b.close();
})();
