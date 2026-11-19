// Print the HTML made by make_pdf.py to a PDF with page numbers. Usage: node make_pdf.cjs in.html out.pdf
const { chromium } = require('playwright');
(async () => {
  const [, , input, output] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + require('path').resolve(input), { waitUntil: 'load' });
  await p.pdf({
    path: output, width: '6in', height: '9in', printBackground: false, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;text-align:center;font-family:serif;font-size:8pt;color:#444;"><span class="pageNumber"></span></div>',
    margin: { top: '0.8in', bottom: '0.85in', left: '0.7in', right: '0.7in' },
  });
  await b.close();
})();
