import {chromium,expect} from '@playwright/test';
import {mkdirSync,writeFileSync} from 'node:fs';
const base=process.env.ROLLSBAR_UX_BASE,out='qa/visual-results/careers';
if(base!=='https://staging.rollsbar.ru')throw Error('Staging only');mkdirSync(out,{recursive:true});
const report={status:'RUNNING',release_sha:process.env.ROLLSBAR_DEPLOY_SHA,checks:[],orders_submitted:0,applications_submitted:0};
const browser=await chromium.launch();
try{
 for(const width of [1440,701,700,390,320]){
  const context=await browser.newContext({viewport:{width,height:900},locale:'ru-RU',reducedMotion:'reduce'}),page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await context.route('**/wc/store/v1/checkout*',r=>r.request().method()==='POST'?r.abort():r.continue());
  await page.addInitScript(()=>localStorage.setItem('rollsbar_cookie_notice','1'));
  const response=await page.goto(base+'/rabota-v-rolls-bar/',{waitUntil:'domcontentloaded'});expect(response.status()).toBe(200);expect(response.headers()['cache-control']).toContain('no-store');
  const form=page.locator('[data-career-form]');await expect(form).toBeAttached();await page.locator('[data-career-apply]').click();await expect(form.locator('[name=city]')).toBeFocused();
  await expect(form.locator('[name=location]')).toHaveValue(/\d+/);await expect(form).toContainText('Адрес заведения');expect(await page.locator('body').innerText()).not.toContain('структура анкеты подготовлена');
  await form.locator('[type=submit]').click();await expect(form.locator('[name=position]')).toBeFocused();await expect(form.locator('[name=consent]')).toHaveAttribute('aria-invalid','true');
  await form.locator('[name=position]').selectOption('kitchen');await form.locator('[name=phone]').fill('89780000001');await expect(form.locator('[name=phone]')).toHaveValue('+79780000001');
  await form.locator('[name=name]').fill('ТЕСТ — НЕ ЗВОНИТЬ '+process.env.GITHUB_RUN_ID);
  await form.locator('[name=comment]').fill('ТЕСТ сайта: проверка анкеты. Не кандидат, не связываться. QA '+process.env.GITHUB_RUN_ID);
  await form.locator('[type=submit]').click();await expect(form.locator('[name=consent]')).toBeFocused();await expect(form.locator('.rb-career-consent .rb-career-error')).toContainText('Отметьте согласие');
  await page.screenshot({path:out+`/consent-${width}.png`});await form.locator('[name=consent]').check();await expect(form.locator('[name=consent]')).not.toHaveAttribute('aria-invalid');
  for(const name of ['surname','birthday','comment'])expect(await form.locator(`[name=${name}]`).evaluate(e=>e.required)).toBe(false);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  for(const button of await form.locator('input:not([type=hidden]):not([type=checkbox]):not([name=website]),select,button').all())expect((await button.boundingBox()).height).toBeGreaterThanOrEqual(44);
  await page.locator('#vacancy-form').screenshot({path:out+`/form-${width}.png`});
  await page.locator('.rollsbar-footer').scrollIntoViewIfNeeded();await expect(page.locator('.rollsbar-footer__logo img')).toHaveAttribute('src',/footer-logo\.svg$/);expect(await page.locator('.rollsbar-footer__logo img').evaluate(e=>e.complete&&e.naturalWidth===300)).toBe(true);
  await page.screenshot({path:out+`/footer-${width}.png`});
  if(width===1440){
   // Exactly one owner-requested application email; no order creation.
   await form.locator('[type=submit]').click();await page.waitForURL('**/?application=received#vacancy-form');await expect(page.locator('[data-career-status]')).toContainText('Анкета получена');report.applications_submitted++;
   await page.screenshot({path:out+'/received.png'});
  }
  expect(errors).toEqual([]);report.checks.push({width,status:'PASS',required_fields:'PASS',consent_marker:'PASS',phone_normalization:'PASS',footer:'PASS',overflow:'none'});await context.close();
 }
 report.status='PASS';
}catch(e){report.status='FAIL';report.error=e.stack;throw e;}
finally{await browser.close();writeFileSync(out+'/evidence.json',JSON.stringify(report,null,2));}
