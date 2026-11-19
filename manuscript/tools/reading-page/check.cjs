// Measure the built page at phone width and take screenshots of the two maps.
// Usage: node check.cjs <built.html> <output-folder> [light|dark]
// Needs Playwright with Chromium. It prints: page overflow, script errors, and any map text
// that runs past the right edge of its box. All three should be 0 or empty.
const { chromium } = require('playwright');
(async () => {
  const [, , file, outDir, scheme = 'light'] = process.argv;
  const b = await chromium.launch();
  const body = require('fs').readFileSync(file, 'utf8');
  const doc = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + body + '</body></html>';
  const p = await b.newPage({ viewport: { width: 400, height: 900 }, colorScheme: scheme, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.setContent(doc, { waitUntil: 'networkidle' });
  await p.evaluate(() => { location.hash = '#map'; });
  await p.waitForTimeout(300);
  console.log('overflow px:', await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth), 'script errors:', errs.length, errs[0] || '');
  for (const id of ['map-all', 'map-elijah']) {
    const info = await p.evaluate((id) => {
      const s = document.getElementById(id); if (!s) return null;
      const vb = s.viewBox.baseVal; const past = [];
      s.querySelectorAll('text').forEach(t => {
        if (t.getAttribute('text-anchor') === 'end') return;
        const bx = t.getBBox();
        if (bx.x + bx.width > vb.width - 12) past.push(t.textContent.slice(0, 50) + ' -> ' + Math.round(bx.x + bx.width));
      });
      return { height: vb.height, textPastEdge: past };
    }, id);
    console.log(id, JSON.stringify(info));
    const el = p.locator('#' + id);
    if (await el.count()) await el.screenshot({ path: outDir + '/' + id + '-' + scheme + '.png' });
  }
  await b.close();
})();
