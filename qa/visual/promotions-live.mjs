import {chromium,expect} from '@playwright/test';
import {mkdirSync,writeFileSync} from 'node:fs';
const base=process.env.ROLLSBAR_UX_BASE;
if(base!=='https://staging.rollsbar.ru')throw Error('Staging only');
const out='qa/visual-results/promotions';mkdirSync(out,{recursive:true});
const report={status:'RUNNING',release_sha:process.env.ROLLSBAR_DEPLOY_SHA,checks:[],submitted_orders:0};
const browser=await chromium.launch();
try{
 for(const width of [1440,701,700,390,320]){
  const context=await browser.newContext({viewport:{width,height:900},locale:'ru-RU',reducedMotion:'reduce'}),page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await context.route('**/wc/store/v1/checkout*',r=>r.request().method()==='POST'?r.abort():r.continue());
  await page.addInitScript(()=>localStorage.setItem('rollsbar_cookie_notice','1'));
  const response=await page.goto(base+'/aktsii/',{waitUntil:'domcontentloaded'});expect(response.status()).toBe(200);
  await expect(page.locator('h1')).toHaveText('Акции Rolls Bar');
  const offer=page.locator('.rb-offer');await expect(offer).toContainText('Скидка 10% именинникам');
  for(const text of ['В день рождения и ещё два дня после него.','На всё меню, кроме сетов.','17 февраля 2027','не применяется автоматически'])await expect(offer).toContainText(text);
  expect(await offer.innerText()).not.toContain('1000');
  await expect(offer.locator('a[href="tel:+79786882288"]')).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  for(const a of await offer.locator('a').all())expect((await a.boundingBox()).height).toBeGreaterThanOrEqual(44);
  await page.screenshot({path:out+`/page-${width}.png`,fullPage:true});
  await page.reload({waitUntil:'domcontentloaded'});await expect(page.locator('h1')).toHaveText('Акции Rolls Bar');
  await page.locator('[data-rollsbar-menu-open]').click();const menu=page.locator('#rollsbarSiteMenu');
  await expect(menu).toHaveAttribute('aria-hidden','false');await expect(menu.locator('a[href="'+base+'/aktsii/"]')).toHaveText('Акции');
  await page.keyboard.press('Escape');await expect(menu).toHaveAttribute('aria-hidden','true');
  await page.locator('.rb-offers__back').click();await page.waitForURL(base+'/');
  const promo=page.locator('.rollsbar-utility--promo');await expect(promo).toHaveAttribute('href',base+'/aktsii/');await expect(promo.locator('h3')).toHaveText('Акции');
  expect(await page.locator('.rollsbar-product-card').count()).toBe(126);
  if([1440,390].includes(width))await page.screenshot({path:out+`/home-${width}.png`});
  await promo.click();await page.waitForURL(base+'/aktsii/');await expect(page.locator('h1')).toHaveText('Акции Rolls Bar');
  await page.locator('.rb-offer__actions a').nth(1).click();await page.waitForURL(base+'/#rolls');
  await expect(page.locator('#rolls')).toBeVisible();expect(errors).toEqual([]);
  report.checks.push({width,status:'PASS',direct_entry:200,offer:'birthday only',navigation:'PASS',ordinary_reload:'PASS'});await context.close();
 }
 report.status='PASS';
}catch(e){report.status='FAIL';report.error=e.stack;throw e;}
finally{await browser.close();writeFileSync(out+'/evidence.json',JSON.stringify(report,null,2));}
