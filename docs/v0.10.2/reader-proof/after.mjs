import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { writeFile, readFile } from 'node:fs/promises';
const base='http://127.0.0.1:5190';
const browser=await chromium.launch({channel:'chrome',headless:true});
const result={base,phase:'after',checks:{},errors:[]};
async function unlock(page,path){await page.goto(base+path);await page.waitForLoadState('networkidle');await page.evaluate(async()=>{const{bookUnlocked}=await import('/src/lib/stores/bookAccess.js');bookUnlocked.set(true)});await page.locator('.gate-form').waitFor({state:'detached'});const consent=page.getByRole('button',{name:'I have read and agree to the Terms, Disclaimer, and Privacy',exact:true});if(await consent.isVisible())await consent.click();}
try{
const page=await browser.newPage({viewport:{width:1100,height:1000},reducedMotion:'reduce'});page.on('pageerror',e=>result.errors.push(e.message));
await unlock(page,'/book/chapter9');
const figure=page.locator('[data-book-scene="food-delivery"]');
const toggle=figure.locator('.primary');
await toggle.focus();await page.keyboard.press('Enter');await figure.locator('canvas').waitFor();
assert.equal(await toggle.evaluate(e=>document.activeElement===e),true,'Opening must keep focus on the same toggle');result.checks.scene_open_focus=true;
await page.keyboard.press('Enter');await figure.locator('canvas').waitFor({state:'detached'});
assert.equal(await toggle.evaluate(e=>document.activeElement===e),true,'Closing must keep focus on the same toggle');result.checks.scene_close_focus=true;
await page.keyboard.press('ArrowRight');await page.waitForTimeout(200);assert.equal(new URL(page.url()).pathname,'/book/chapter9');result.checks.control_arrow_does_not_navigate=true;
await page.keyboard.press('Enter');await figure.locator('canvas').waitFor();await figure.getByRole('button',{name:'Rotate view right',exact:true}).focus();
await figure.locator('canvas').evaluate(c=>c.getContext('webgl2').getExtension('WEBGL_lose_context').loseContext());await figure.locator('[data-scene-state="fallback"]').waitFor();
assert.equal(await toggle.evaluate(e=>document.activeElement===e),true,'Context loss must restore focus when it removes the focused camera control');result.checks.context_loss_focus_restored=true;
await figure.locator('summary').focus();await page.keyboard.press('ArrowRight');await page.waitForTimeout(100);assert.equal(new URL(page.url()).pathname,'/book/chapter9');
await page.getByRole('button',{name:'Chapters',exact:true}).focus();await page.keyboard.press('Enter');await page.locator('.chapter-nav-item').first().focus();await page.keyboard.press('Escape');
assert.equal(await page.getByRole('button',{name:'Chapters',exact:true}).getAttribute('aria-expanded'),'false');assert.equal(await page.getByRole('button',{name:'Chapters',exact:true}).evaluate(e=>document.activeElement===e),true);result.checks.chapter_dropdown_escape_restores_focus=true;
await unlock(page,'/read');const trigger=page.getByRole('button',{name:'Chapters',exact:true}).first();await trigger.focus();await page.keyboard.press('Enter');
assert.equal(await page.evaluate(()=>!!document.activeElement.closest('#reader-toc')),true);assert.equal(await page.locator('#reader-toc').evaluate(e=>e.matches(':modal')),true);
assert.equal(await trigger.evaluate(e=>{e.focus();return document.activeElement!==e}),true,'The modal must prevent focusing background controls');
await page.locator('.toc-foot-link').focus();await page.keyboard.press('Tab');
assert.equal(await page.evaluate(()=>document.activeElement===document.body||!!document.activeElement.closest('#reader-toc')),true,'Tab may reach browser chrome, but not background controls');
await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>!!document.activeElement.closest('#reader-toc')),true,'Tab returns to the modal after browser chrome');
await page.keyboard.press('Escape');assert.equal(await trigger.getAttribute('aria-expanded'),'false');assert.equal(await trigger.evaluate(e=>document.activeElement===e),true);result.checks.drawer_focus_modal_escape_restore=true;
await trigger.click();await page.getByRole('button',{name:/Part II: How Humans React/}).click();await page.waitForTimeout(200);
const divider=page.locator('#s-part-2');assert.equal(await divider.locator('img').count(),2);assert.match(await divider.textContent(),/nineteen households are trying something else/);assert.equal(await divider.locator('h1').evaluate(e=>document.activeElement===e),true);result.checks.part2_prose_images_and_jump_focus=true;
await page.screenshot({path:'docs/v0.10.2/reader-proof/after-divider.png'});
await trigger.click();await page.getByRole('button',{name:/Part III: How to Survive/}).click();assert.match(await page.locator('#s-part-3').textContent(),/You can also be the person receiving help/);assert.equal(await page.locator('#s-part-3 img').count(),1);result.checks.part3_prose_images=true;
// Test the actual current registry, including legacy diagrams added in this release.
const visuals=JSON.parse(await readFile('src/lib/data/book/visuals.json','utf8'));
let verified=0;
for(const[file,v]of Object.entries(visuals.images)){
const s=`![Alt for ${file}](/book-images/${file})\n\n*Caption with a [source](https://example.com/evidence) for ${file}.*`;
const r=await page.evaluate(async s=>(await import('/src/lib/utils/bookMarkdown.js')).renderMarkdown(s),s);
assert.match(r,/<figure/);assert.match(r,/<figcaption>/);assert.match(r,/href="https:\/\/example.com\/evidence"/);assert.ok(r.includes(`alt="Alt for ${file}"`));verified++;
}
result.checks.registry_figures_with_alt_caption_and_source=verified;
const control=await page.evaluate(async()=>{const{renderMarkdown}=await import('/src/lib/utils/bookMarkdown.js');return renderMarkdown('![alt](/book-images/v101-visual-access-gate.svg)\n\n*Italic start* ordinary prose.\n\nRetained paragraph.\n\n*Later italic paragraph.*\n\n<img src=x onerror=alert(1)>')});
assert.doesNotMatch(control,/<figcaption>|onerror/);assert.match(control,/Retained paragraph/);result.checks.renderer_sanitization_and_caption_boundary=true;
assert.deepEqual(result.errors,[]);
}finally{await browser.close();await writeFile('docs/v0.10.2/reader-proof/after.json',JSON.stringify(result,null,2)+'\n');}
console.log(JSON.stringify(result,null,2));
