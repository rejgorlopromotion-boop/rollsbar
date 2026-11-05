import {chromium,webkit,firefox,expect} from '@playwright/test';
import {mkdirSync,readFileSync,writeFileSync} from 'node:fs';
const base='https://staging.rollsbar.ru',out='qa/visual-results/client-nov05';mkdirSync(out,{recursive:true});
const plan=JSON.parse(readFileSync('wordpress/data/client-2026-11-05/catalog-order.json','utf8'));
const report={status:'RUNNING',release_sha:process.env.ROLLSBAR_DEPLOY_SHA,checks:[],submitted_orders:0,submitted_applications:0};
async function run(engine,name){
 const browser=await engine.launch();
 try{for(const width of [320,390,700,701,1024,1050,1051,1440]){
  const context=await browser.newContext({viewport:{width,height:900},locale:'ru-RU',hasTouch:name!=='firefox'&&width<=700,reducedMotion:'reduce'}),page=await context.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await context.route('**/wc/store/**/checkout*',r=>{const q=r.request(),method=q.headers()['x-http-method-override']||q.method();return method.toUpperCase()==='POST'?r.abort():r.continue();});
  await context.route('**/wp-admin/admin-post.php*',r=>r.abort());
  if(process.env.ROLLSBAR_CLIENT_SHADOW==='1')await context.route('**/rollsbar-theme/assets/js/app.js*',r=>r.fulfill({status:200,contentType:'application/javascript',body:readFileSync('wordpress/wp-content/themes/rollsbar-theme/assets/js/app.js','utf8')}));
  await page.addInitScript(()=>localStorage.setItem('rollsbar_cookie_notice','1'));
  await page.goto(base+'/?client-nov05='+report.release_sha,{waitUntil:'domcontentloaded'});
  await expect(page.locator('.rollsbar-product-card')).toHaveCount(126);
  const identities=JSON.parse(await page.locator('#rollsbarProductDetailsData').textContent());expect(Object.keys(identities)).toHaveLength(118);
  for(const [id,order] of Object.entries(plan.categories))expect(await page.locator('#'+id+' .rollsbar-product-card').evaluateAll(ns=>ns.map(n=>n.dataset.rollsbarSourceId)),id).toEqual(order);
  const cards=page.locator('.rollsbar-utility');expect(await cards.locator('h3').allTextContents()).toEqual(['Акции','Доставка','Работа в Rolls Bar','Отзывы']);
  const urls=['/aktsii/','/#delivery','/rabota-v-rolls-bar/','/otzyvy/'];
  for(let i=0;i<4;i++){
   const card=cards.nth(i),img=card.locator('img.rollsbar-utility__artwork');await expect(img).toBeAttached();
   expect(new URL(await card.getAttribute('href')).pathname+new URL(await card.getAttribute('href')).hash).toBe(urls[i]);
   await img.evaluate(n=>n.decode());expect(await img.evaluate(n=>n.naturalWidth)).toBeGreaterThanOrEqual(178);
   const rect=await card.boundingBox();expect(Math.abs(rect.width-rect.height)).toBeLessThan(1.1);
   await expect(card.locator('.rollsbar-utility__eyebrow')).toBeHidden();await expect(card.locator('.rollsbar-utility__text')).toBeHidden();
  }
  if(width===1440){for(const url of urls.filter(u=>!u.includes('#')))expect((await context.request.get(base+url)).status()).toBe(200);}
  await page.screenshot({path:`${out}/${name}-${width}-home.png`});
  const combo=page.locator('.rollsbar-category-nav__scroll a[href="#combo"]'),sets=page.locator('.rollsbar-category-nav__scroll a[href="#sets"]');
  await combo.click();await expect(combo).toHaveAttribute('aria-current','location');
  await sets.click();await expect(sets).toHaveAttribute('aria-current','location');
  await combo.click();await expect(combo).toHaveClass('active');
  // Original video at6s: Sets heading is roughly27px below the sticky bar.
  await page.locator('#sets h2').evaluate(n=>{const nav=document.querySelector('.rollsbar-category-nav');window.scrollTo({top:scrollY+n.getBoundingClientRect().top-(parseFloat(getComputedStyle(nav).top)+nav.offsetHeight+27),behavior:'instant'});});
  await expect(sets).toHaveAttribute('aria-current','location');
  await page.locator('#sets img').evaluateAll(imgs=>Promise.all(imgs.slice(0,4).map(img=>{img.loading='eager';return img.decode().catch(()=>{});})));await page.mouse.move(width-5,895);
  await page.screenshot({path:`${out}/${name}-${width}-video-replay.png`});
  await combo.click();await expect(combo).toHaveClass('active');
  // Replay the reported down/up transition using wheel movement, then pause in each category.
  await page.mouse.move(width/2,500);
  const distance=await page.locator('#sets h2').evaluate(n=>n.getBoundingClientRect().top)-200;
  await page.mouse.wheel(0,Math.max(0,distance));await page.waitForTimeout(150);
  await page.mouse.wheel(0,260);await expect(sets).toHaveAttribute('aria-current','location');
  await page.waitForTimeout(150);await expect(sets).toHaveClass('active');
  await page.locator('#sets img').evaluateAll(imgs=>Promise.all(imgs.slice(0,4).map(img=>{img.loading='eager';return img.decode().catch(()=>{});})));await page.mouse.move(width-5,895);
  await page.screenshot({path:`${out}/${name}-${width}-sets.png`});
  await page.locator('#combo h2').evaluate(n=>window.scrollTo({top:scrollY+n.getBoundingClientRect().top-80,behavior:'instant'}));
  await expect(combo).toHaveAttribute('aria-current','location');
  await page.mouse.wheel(0,-80);await expect(combo).toHaveClass('active');
  await sets.click();await combo.click();await page.goBack({waitUntil:'domcontentloaded'});await expect(sets).toHaveAttribute('aria-current','location');
  await page.goto(base+'/#sets',{waitUntil:'domcontentloaded'});await expect(sets).toHaveAttribute('aria-current','location');
  const activeRect=await sets.boundingBox(),navRect=await page.locator('.rollsbar-category-nav__scroll').boundingBox();
  expect(activeRect.x).toBeGreaterThanOrEqual(navRect.x-1);expect(activeRect.x+activeRect.width).toBeLessThanOrEqual(navRect.x+navRect.width+1);
  if(width===390||width===320||width===1440){
   await page.locator('#rolls').screenshot({path:`${out}/${name}-${width}-rolls.png`});
   await page.goto(base+'/rabota-v-rolls-bar/',{waitUntil:'domcontentloaded'});
   const phone=page.locator('[data-career-phone]');await phone.fill('+79781234567');await expect(phone).toHaveValue('+79781234567');await phone.fill('');await phone.blur();await phone.focus();await expect(phone).toHaveValue('+7');
   // Firefox intentionally strips clipboardData from an untrusted ClipboardEvent.
   // Supply the fixture payload explicitly; the real input/paste handler is unchanged.
   await phone.evaluate(n=>{const data=new DataTransfer();data.setData('text/plain','+44 20 7946 0958');const event=new Event('paste',{bubbles:true,cancelable:true});Object.defineProperty(event,'clipboardData',{value:data});n.dispatchEvent(event);});await expect(phone).toHaveValue('+44 20 7946 0958');
   await phone.fill('');await phone.blur();await phone.focus();await expect(phone).toHaveValue('+7');
   expect(await phone.evaluate(n=>n.selectionStart)).toBe(2);await phone.press('Backspace');await expect(phone).toHaveValue('+');await phone.press('Backspace');await expect(phone).toHaveValue('');
   await phone.pressSequentially('+442079460958');await expect(phone).toHaveValue('+442079460958');expect(await phone.evaluate(n=>n.checkValidity())).toBe(true);
   await phone.fill('+380501234567');await phone.blur();await phone.focus();await expect(phone).toHaveValue('+380501234567');expect(await phone.evaluate(n=>n.checkValidity())).toBe(true);
   await phone.fill('');await phone.blur();await phone.focus();await expect(phone).toHaveValue('+7');await phone.pressSequentially('9781234567');expect(await phone.evaluate(n=>n.checkValidity())).toBe(true);
   await page.screenshot({path:`${out}/${name}-${width}-career.png`});
  }
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);expect(errors).toEqual([]);
  report.checks.push({engine:name,width,status:'PASS',catalog:118,hits:8,promo:'PASS',scroll_down_up_tap_hash_history:'PASS',phone:width===390||width===320||width===1440?'PASS':'covered at 320/390/1440'});
  writeFileSync(out+'/browser.json',JSON.stringify(report,null,2));console.log(name,width,'client checklist PASS');await context.close();
 }}finally{await browser.close();}
}
try{await run(chromium,'chromium');await run(webkit,'webkit');await run(firefox,'firefox');report.status='PASS';}
catch(e){report.status='FAIL';report.error=e.stack;throw e;}
finally{writeFileSync(out+'/browser.json',JSON.stringify(report,null,2));}
