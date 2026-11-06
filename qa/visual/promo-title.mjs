import {chromium, webkit, firefox, expect} from '@playwright/test';
import {mkdirSync, writeFileSync} from 'node:fs';
const out='qa/visual-results/promo-title';mkdirSync(out,{recursive:true});
const report={release_sha:process.env.ROLLSBAR_DEPLOY_SHA,status:'RUNNING',checks:[]};
try {
 for(const [name,engine] of Object.entries({chromium,webkit,firefox})) {
  const browser=await engine.launch();
  try { for(const width of [320,390,700,701,1051,1440,2048]) {
   const page=await browser.newPage({viewport:{width,height:1000},locale:'ru-RU',reducedMotion:'reduce'});
   await page.addInitScript(()=>localStorage.setItem('rollsbar_cookie_notice','1'));
   await page.goto('https://staging.rollsbar.ru/?promo-title='+report.release_sha,{waitUntil:'domcontentloaded'});
   await page.evaluate(()=>document.fonts.ready);
   const cards=page.locator('.rollsbar-utility');
   expect(await cards.locator('h3').allTextContents()).toEqual(['Акции','Доставка','Работа в Rolls Bar','Отзывы']);
   const card=page.locator('.rollsbar-utility--work'),title=card.locator('h3');
   await card.scrollIntoViewIfNeeded();
   await card.locator('img').evaluate(n=>n.decode());
   await expect(title).toHaveCSS('background-color','rgb(255, 255, 255)');
   await expect(title).toHaveCSS('color','rgb(37, 37, 37)');
   const a=await card.boundingBox(),b=await title.boundingBox();
   expect(b.x).toBeGreaterThan(a.x);expect(b.x+b.width).toBeLessThan(a.x+a.width);
   expect(b.y).toBeGreaterThan(a.y);expect(b.y+b.height).toBeLessThan(a.y+a.height);
   expect(await title.evaluate(n=>n.scrollWidth<=n.clientWidth)).toBe(true);
   expect(new URL(await card.getAttribute('href')).pathname).toBe('/rabota-v-rolls-bar/');
   await card.screenshot({path:`${out}/${name}-${width}-work.png`});
   if(width===390||width===1440||width===2048)await page.screenshot({path:`${out}/${name}-${width}-home.png`});
   report.checks.push({engine:name,width,status:'PASS'});await page.close();
  }} finally {await browser.close();}
 }
 report.status='PASS';
}catch(e){report.status='FAIL';report.error=e.stack;throw e;}
finally{writeFileSync(out+'/browser.json',JSON.stringify(report,null,2));}
