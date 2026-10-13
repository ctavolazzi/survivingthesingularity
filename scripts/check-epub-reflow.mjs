#!/usr/bin/env node
/** Render the delivered EPUB's chapters at phone/tablet widths and enlarged text. */
import { chromium, firefox, webkit } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtempSync, readFileSync, readdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const meta = JSON.parse(readFileSync(join(root, 'src/lib/data/book/book.json')));
const epub = resolve(process.argv[2] || join(root, `static/downloads/Surviving-the-Singularity-v${meta.version}.epub`));
const engine = process.env.EPUB_REFLOW_BROWSER || 'chromium';
const browserType = { chromium, firefox, webkit }[engine];
if (!browserType) throw new Error('EPUB_REFLOW_BROWSER must be chromium, firefox or webkit');
const temporary = mkdtempSync(join(tmpdir(), 'sts-epub-reflow-'));
let browser;
try {
  // Read a local publication artifact only. Reject escaping archive members
  // before extraction, even when checking a candidate supplied as an argument.
  execFileSync('python3', ['-c', `
import pathlib, sys, zipfile
root = pathlib.Path(sys.argv[2]).resolve()
with zipfile.ZipFile(sys.argv[1]) as archive:
    assert archive.testzip() is None, 'Corrupt EPUB'
    for member in archive.namelist():
        assert (root / member).resolve().is_relative_to(root), 'Archive path escapes the reading directory'
    archive.extractall(root)
`, epub, temporary]);
  const directory = join(temporary, 'EPUB/text');
  const chapters = readdirSync(directory).filter(name => /^ch\d+\.xhtml$/.test(name));
  if (chapters.length !== meta.sections.length) throw new Error('EPUB chapter count differs from canonical source');
  browser = await browserType.launch({ headless: true });
  const results = [];
  for (const width of [320, 768]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    // EPUB content should work offline; a mistaken external resource must not
    // become a successful render merely because this test has a network.
    await page.route(/^https?:/, route => route.abort());
    for (const chapter of chapters) {
      await page.goto(pathToFileURL(join(directory, chapter)).href);
      for (const fontSize of [18, 28]) {
        const style = await page.addStyleTag({ content: `html { font-size: ${fontSize}px } body { font-size: 1rem }` });
        const result = await page.evaluate(async () => {
          await document.fonts.ready;
          await Promise.all([...document.images].map(image => image.decode().catch(() => {})));
          const wideTables = [...document.querySelectorAll('table')]
            .filter(table => table.scrollWidth > table.clientWidth + 1);
          const unscrollableTables = wideTables.filter(table => {
            table.scrollLeft = table.scrollWidth;
            const canPan = table.scrollLeft > 0 && getComputedStyle(table).overflowX === 'auto';
            table.scrollLeft = 0;
            return !canPan;
          }).length;
          return {
            viewport: innerWidth,
            documentWidth: document.documentElement.scrollWidth,
            missingImages: [...document.images].filter(image => !image.complete || !image.naturalWidth).length,
            wideTables: wideTables.length,
            unscrollableTables
          };
        });
        results.push({ chapter, fontSize, ...result });
        await style.evaluate(element => element.remove());
      }
    }
    await page.close();
  }
  const failures = results.filter(result => result.documentWidth > result.viewport + 1 || result.missingImages || result.unscrollableTables);
  console.log(JSON.stringify({
    epub: epub.replace(root + '/', ''),
    browser: engine,
    sha256: createHash('sha256').update(readFileSync(epub)).digest('hex'),
    chapterCount: chapters.length,
    checks: results.length,
    containedTablePanChecks: results.reduce((total, result) => total + result.wideTables, 0),
    failures,
    limits: 'Browser reflow checks; not dedicated e-reader pagination or assistive-technology certification.'
  }, null, 2));
  if (failures.length) process.exitCode = 1;
} finally {
  await browser?.close();
  rmSync(temporary, { recursive: true, force: true });
}
