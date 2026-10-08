import { chromium } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
const base='http://127.0.0.1:5190';
const browser=await chromium.launch({channel:'chrome',headless:true});
const result={base,phase:'before',observations:{}};
async function unlock(page,path){await page.goto(base+path);await page.waitForLoadState('networkidle');await page.evaluate(async()=>{const{bookUnlocked}=await import('/src/lib/stores/bookAccess.js');bookUnlocked.set(true)});await page.locator('.gate-form').waitFor({state:'detached'});const consent=page.getByRole('button',{name:'I have read and agree to the Terms, Disclaimer, and Privacy',exact:true});if(await consent.isVisible())await consent.click();}
try{
const page=await browser.newPage({viewport:{width:1100,height:1000}});
await unlock(page,'/book/chapter9');
const figure=page.locator('[data-book-scene="food-delivery"]');
await figure.getByRole('button',{name:'Explore in 3D',exact:true}).focus();await page.keyboard.press('Enter');await figure.locator('canvas').waitFor();
result.observations.scene_open_focus=await page.evaluate(()=>({tag:document.activeElement.tagName,text:document.activeElement.textContent?.slice(0,70)}));
await figure.getByRole('button',{name:'Use still illustration',exact:true}).focus();await page.keyboard.press('Enter');await figure.locator('canvas').waitFor({state:'detached'});
result.observations.scene_close_focus=await page.evaluate(()=>({tag:document.activeElement.tagName,text:document.activeElement.textContent?.slice(0,70)}));
await figure.getByRole('button',{name:'Explore in 3D',exact:true}).focus();await page.keyboard.press('ArrowRight');await page.waitForTimeout(700);
result.observations.arrow_on_control_url=page.url();
await unlock(page,'/read');const trigger=page.getByRole('button',{name:'Chapters',exact:true}).first();await trigger.focus();await page.keyboard.press('Enter');
result.observations.drawer_open_focus=await page.evaluate(()=>({inside:!!document.activeElement.closest('#reader-toc'),tag:document.activeElement.tagName}));
await page.keyboard.press('Escape');
result.observations.escape_leaves_drawer_open=await trigger.getAttribute('aria-expanded');
await page.getByRole('button',{name:/Part II: How Humans React/}).click();await page.waitForTimeout(700);
const divider=page.locator('#s-part-2');
result.observations.divider_content=await divider.textContent();result.observations.divider_images=await divider.locator('img').count();
result.observations.chapter_jump_focus=await page.evaluate(()=>({tag:document.activeElement.tagName,hidden:!!document.activeElement.closest('[aria-hidden="true"]')}));
await page.screenshot({path:'docs/v0.10.2/reader-proof/before-divider.png'});
}finally{await browser.close();await writeFile('docs/v0.10.2/reader-proof/before.json',JSON.stringify(result,null,2)+'\n');}
console.log(JSON.stringify(result,null,2));
