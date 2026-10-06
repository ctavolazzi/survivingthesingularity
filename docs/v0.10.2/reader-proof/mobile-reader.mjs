import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});
const result={base:'http://127.0.0.1:5190',viewport:[390,844],reduced_motion:true};
try{
await page.goto(result.base+'/read');await page.waitForLoadState('networkidle');await page.evaluate(async()=>{const{bookUnlocked}=await import('/src/lib/stores/bookAccess.js');bookUnlocked.set(true)});await page.locator('.gate-form').waitFor({state:'detached'});
const consent=page.getByRole('button',{name:'I have read and agree to the Terms, Disclaimer, and Privacy',exact:true});if(await consent.isVisible())await consent.click();
const trigger=page.getByRole('button',{name:'Chapters',exact:true});await trigger.click();await page.locator('dialog[open]').waitFor();await page.screenshot({path:'docs/v0.10.2/reader-proof/mobile-chapters.png'});
assert.equal(await page.evaluate(()=>!!document.activeElement.closest('dialog')),true);
await page.evaluate(()=>{const proto=Element.prototype;const old=proto.scrollTo;window.__readerScrolls=[];proto.scrollTo=function(...args){window.__readerScrolls.push(args[0]);return old.apply(this,args)}});
await page.getByRole('button',{name:/Part I: What is/}).click();await page.waitForTimeout(150);
result.scroll_calls=await page.evaluate(()=>window.__readerScrolls);assert.ok(result.scroll_calls.some(s=>s.behavior==='auto'));assert.ok(result.scroll_calls.every(s=>s.behavior!=='smooth'));
result.divider=await page.locator('#s-part-1').evaluate(el=>({images:el.querySelectorAll('img').length,text:el.textContent,overflow:el.scrollWidth>el.clientWidth}));assert.equal(result.divider.overflow,false);assert.ok(result.divider.images>0);assert.ok(result.divider.text.length>100);
await page.screenshot({path:'docs/v0.10.2/reader-proof/mobile-divider.png'});
await trigger.click();await page.getByRole('button',{name:'Close chapter list',exact:true}).click();assert.equal(await trigger.evaluate(e=>document.activeElement===e),true);result.close_restores_trigger=true;
}finally{await browser.close();await writeFile('docs/v0.10.2/reader-proof/mobile-reader.json',JSON.stringify(result,null,2)+'\n');}
console.log('Mobile drawer name, focus, divider parity, overflow, and reduced-motion scroll passed.');
