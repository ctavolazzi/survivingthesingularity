import assert from 'node:assert/strict';
import {writeFile} from 'node:fs/promises';
import {chromium} from '@playwright/test';
const browser=await chromium.launch({channel:'chrome',headless:true});
try {
 const page=await browser.newPage({viewport:{width:1280,height:1100}});
 await page.goto('http://127.0.0.1:5190/book/chapter9');await page.waitForLoadState('networkidle');
 await page.evaluate(async()=>{const{bookUnlocked}=await import('/src/lib/stores/bookAccess.js');bookUnlocked.set(true)});
 await page.locator('[data-book-scene="food-delivery"]').getByRole('button',{name:'Explore in 3D'}).click();
 await page.locator('[data-three-canvas="food-delivery"]').waitFor();
 await page.evaluate(()=>{window.__oldSceneCanvas=document.querySelector('[data-three-canvas="food-delivery"]')});
 await page.evaluate(async()=>{const{safeGoto}=await import('/src/lib/utils/navigation.js');await safeGoto('/book/chapter15')});
 const next=page.locator('[data-book-scene="living-soil"]');await next.waitFor();
 assert.equal(await next.locator('canvas').count(),0,'A new chapter must start on its own still, not reuse the prior active model');
 assert.equal(await page.evaluate(()=>window.__oldSceneCanvas.getContext('webgl2').isContextLost()),true,'Previous chapter releases its WebGL context');
 await next.getByRole('button',{name:'Explore in 3D'}).click();await next.locator('[data-three-canvas="living-soil"]').waitFor();
 await writeFile('docs/v0.10.2/reader-proof/navigation-proof.json',JSON.stringify({spa_navigation:'chapter9 to chapter15',previous_context_disposed:true,new_chapter_starts_on_still:true,new_model_matches_chapter:true},null,2)+'\n');
 console.log('Client-side chapter navigation disposes the old scene and starts the new chapter on its own still.');
} finally {await browser.close()}
