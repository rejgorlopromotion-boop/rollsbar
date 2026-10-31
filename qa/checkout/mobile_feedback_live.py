"""Mobile row alignment and visible delivery shortfall at top and submit; no orders."""
import os,sys,json,re
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'wordpress/deploy'),str(ROOT/'qa/checkout')]
from gate_b_browser import BASE,add_first_simple_product,require
from delivery_test_context import delivery_page,settle_native
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf8',line_buffering=True)
shadow='--shadow' in sys.argv
out=ROOT/'qa/visual-results'/('mobile-feedback-shadow' if shadow else 'mobile-feedback');out.mkdir(exist_ok=True)
report={'status':'RUNNING','mode':'shadow' if shadow else 'live','release_sha':os.environ.get('ROLLSBAR_DEPLOY_SHA'),'checks':[],'submitted_orders':0}
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch()
  for width in [1440,701,700,390,320]:
   with delivery_page(b,viewport={'width':width,'height':900},locale='ru-RU') as p:
    if shadow:
     for tail,path in [('rollsbar-theme/assets/css/app.css','wordpress/wp-content/themes/rollsbar-theme/assets/css/app.css'),('rollsbar-core/assets/css/checkout.css','wordpress/wp-content/plugins/rollsbar-core/assets/css/checkout.css'),('rollsbar-core/assets/js/checkout.js','wordpress/wp-content/plugins/rollsbar-core/assets/js/checkout.js')]:
      p.route('**/'+tail+'*',lambda r,request,path=path:r.fulfill(status=200,body=(ROOT/path).read_text(encoding='utf8'),content_type='application/javascript' if path.endswith('.js') else 'text/css'))
    p.goto(BASE+'/',wait_until='domcontentloaded')
    p.wait_for_function('Array.from(document.querySelectorAll(".rollsbar-product-card")).every(e=>e.getAttribute("aria-busy")!=="true")')
    rows=p.evaluate('''()=>Array.from(document.querySelectorAll('.rollsbar-product-grid')).flatMap(grid=>{const rows=new Map();for(const card of grid.children){const r=card.getBoundingClientRect(),f=card.querySelector('.rollsbar-product-card__footer').getBoundingClientRect(),price=card.querySelector('.rollsbar-price').getBoundingClientRect(),key=Math.round(r.top);if(!rows.has(key))rows.set(key,[]);rows.get(key).push({id:card.dataset.rollsbarSourceId,bottom:f.bottom,price:price.top});}return [...rows.values()].filter(r=>r.length>1).map(row=>({footerDelta:Math.max(...row.map(x=>x.bottom))-Math.min(...row.map(x=>x.bottom)),priceDelta:Math.max(...row.map(x=>x.price))-Math.min(...row.map(x=>x.price))}));})''')
    if width<=700:require(all(r['footerDelta']<=1 and r['priceDelta']<=1 for r in rows),'all mobile row footer/price baselines aligned, including accent cards')
    require(p.evaluate('document.documentElement.scrollWidth<=innerWidth'),'no catalog overflow')
    card=p.locator('#rolls [data-rollsbar-source-id="rolls-filadelfiya-s-krevetkoy"]');card.scroll_into_view_if_needed();p.screenshot(path=str(out/f'cards-{width}.png'))
    add_first_simple_product(p);settle_native(p);p.goto(BASE+'/checkout/',wait_until='domcontentloaded')
    address=p.locator('#shipping-address_1');address.wait_for()
    with p.expect_response(lambda r:'/address-suggestions' in r.url and parse_qs(urlsplit(r.url).query).get('query')==['Гагарина 1']) as suggested:address.fill('Гагарина 1')
    display=suggested.value.json()['suggestions'][0]['display'];p.wait_for_function('(v)=>document.querySelector(".rollsbar-address-suggestions__item")?.textContent===v',arg=display)
    with p.expect_response(lambda r:'/address-resolve' in r.url and r.request.method=='POST') as resolved:p.locator('.rollsbar-address-suggestions__item').first.click()
    require(resolved.value.json()['delivery']['minimum']==1200,'real verified delivery minimum1200')
    p.locator('#shipping-phone').fill('89781234567');p.locator('#order-rollsbar-privacy-consent').check();settle_native(p)
    p.wait_for_function('!!wp.data.select("wc/store/validation").getValidationError("rollsbar-delivery-minimum")')
    p.evaluate('''()=>{window.__rbMinPosts=0;wp.apiFetch.use((o,next)=>{if((o.path||o.url||'').includes('/wc/store/v1/checkout')&&(o.method||'GET').toUpperCase()==='POST'){window.__rbMinPosts++;return Promise.reject({code:'qa_stop',message:'QA stopped before HTTP',data:{status:400}});}return next(o);});}''')
    button=p.locator('.wc-block-components-checkout-place-order-button');button.click()
    notice=p.locator('.rollsbar-minimum-notice');notice.wait_for(state='visible');p.wait_for_function('wp.data.select("wc/store/checkout").isIdle()')
    flat=re.sub(r'\s','',notice.inner_text());require('1200' in flat and '780' in flat,'top warning states actual minimum and780 shortfall for420 cart')
    require(p.evaluate('window.__rbMinPosts')==0,'known below-minimum cart blocked before native POST assembly')
    require(notice.evaluate('e=>{const r=e.getBoundingClientRect(),d=e.closest("[data-rollsbar-modal]").getBoundingClientRect();return r.top>=d.top&&r.bottom<=d.bottom}'),'post-click focus lands on visible explanation')
    p.locator('[data-rollsbar-modal="1"]').evaluate('e=>e.scrollTop=0')
    require(notice.evaluate('e=>{let r=e.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight}'),'warning visible even when Woo scrolls to modal top')
    p.screenshot(path=str(out/f'minimum-top-{width}.png'))
    button.scroll_into_view_if_needed();feedback=p.locator('.rollsbar-submit-feedback')
    require(re.sub(r'\s','',feedback.inner_text())==flat,'same exact shortfall remains beside submit')
    p.screenshot(path=str(out/f'minimum-button-{width}.png'))
    p.locator('.wc-block-checkout__shipping-method [role="radio"]').nth(1).click();p.wait_for_function('wp.data.select("wc/store/checkout").prefersCollection()===true');settle_native(p)
    require(not notice.is_visible(),'pickup clears top delivery warning')
    p.locator('.wc-block-checkout__shipping-method [role="radio"]').first.click();p.wait_for_function('wp.data.select("wc/store/checkout").prefersCollection()===false');settle_native(p)
    p.wait_for_function('!!wp.data.select("wc/store/validation").getValidationError("rollsbar-delivery-minimum")')
    p.evaluate('async()=>{const s=wp.data.select("wc/store/cart");await wp.data.dispatch("wc/store/cart").changeCartItemQuantity(s.getCartData().items[0].key,3)}');settle_native(p)
    p.wait_for_function('!wp.data.select("wc/store/validation").getValidationError("rollsbar-delivery-minimum")')
    require(not notice.is_visible() and not notice.inner_text(),'1260 qualifying total clears stale minimum warning')
    report['checks'].append({'width':width,'status':'PASS','mobile_rows':rows if width<=700 else 'desktop unchanged','minimum':1200,'cart':420,'shortfall':780,'qualified_cart':1260,'checkout_posts':p.evaluate('window.__rbMinPosts')})
  b.close()
 report['status']='PASS'
finally:(out/'evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
