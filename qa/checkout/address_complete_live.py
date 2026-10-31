"""Owner override: street+house required, manual fallback and operator notice. No orders."""
import json,os,sys
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'wordpress/deploy'),str(ROOT/'qa/checkout')]
from gate_b_browser import BASE,require,add_first_simple_product
from delivery_test_context import delivery_page,settle_native
from playwright.sync_api import sync_playwright
shadow='--shadow' in sys.argv
out=ROOT/'qa/visual-results'/('address-complete-shadow' if shadow else 'address-complete');out.mkdir(parents=True,exist_ok=True)
report={'status':'RUNNING','mode':'shadow' if shadow else 'live','release_sha':os.environ['ROLLSBAR_DEPLOY_SHA'],'checks':[],'submitted_orders':0}
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch()
  for width in [1440,701,700,390,320]:
   with delivery_page(browser,viewport={'width':width,'height':900},locale='ru-RU') as p:
    if shadow:
     for tail in ['assets/js/checkout.js','assets/css/checkout.css']:
      path=ROOT/'wordpress/wp-content/plugins/rollsbar-core'/tail
      p.route('**/rollsbar-core/'+tail+'*',lambda r,request,path=path:r.fulfill(status=200,body=path.read_text(encoding='utf8'),content_type='application/javascript' if path.suffix=='.js' else 'text/css'))
    p.goto(BASE+'/',wait_until='domcontentloaded');add_first_simple_product(p);settle_native(p)
    p.goto(BASE+'/checkout/',wait_until='domcontentloaded');address=p.locator('#shipping-address_1');address.wait_for()
    p.locator('#shipping-phone').fill('+79781234567');p.locator('#order-rollsbar-privacy-consent').check()
    query='Симферополь Киевская'
    with p.expect_response(lambda r:'/address-suggestions' in r.url and parse_qs(urlsplit(r.url).query).get('query')==[query]) as suggested:address.fill(query)
    suggestions=suggested.value.json()['suggestions'];require(bool(suggestions),'real street suggestions available')
    p.wait_for_function('(v)=>document.querySelector(".rollsbar-address-suggestions__item")?.textContent===v',arg=suggestions[0]['display'])
    with p.expect_response(lambda r:'/address-resolve' in r.url and r.request.method=='POST') as resolved:p.locator('.rollsbar-address-suggestions__item').first.click()
    require(not resolved.value.json().get('house'),'provider street selection has no house')
    settle_native(p)
    p.evaluate('''()=>{window.__rbAddressPayload=null;window.__rbAddressPosts=0;wp.apiFetch.use((o,next)=>{if((o.path||o.url||'').includes('/wc/store/v1/checkout')&&(o.method||'GET').toUpperCase()==='POST'){window.__rbAddressPosts++;window.__rbAddressPayload=JSON.parse(JSON.stringify(o.data));return Promise.reject({code:'qa_stop',message:'QA stopped before HTTP',data:{status:400}});}return next(o);});}''')
    button=p.locator('.wc-block-components-checkout-place-order-button');button.click()
    p.wait_for_function('document.activeElement?.id==="shipping-address_1"&&wp.data.select("wc/store/checkout").isIdle()')
    require(p.evaluate('window.__rbAddressPosts')==0,'street-only blocks native POST assembly')
    require(address.get_attribute('aria-invalid')=='true','address is marked invalid')
    holder=p.locator('.rollsbar-address-incomplete');require(holder.count()==1 and 'Укажите полный адрес' in holder.inner_text(),'visible local explanation')
    require(holder.evaluate('e=>{let r=e.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight}'),'focused field and explanation are visible')
    p.screenshot(path=str(out/f'incomplete-{width}.png'))
    manual='Симферополь, ул Неизвестная, д 99Б';address.fill(manual);address.blur();settle_native(p)
    p.wait_for_function('!wp.data.select("wc/store/validation").getValidationError("rollsbar-delivery-address")')
    require(not p.locator('.rollsbar-address-incomplete').count(),'marker clears after manual completion')
    require(not p.evaluate('wp.data.select("wc/store/validation").getValidationError("rollsbar-delivery-minimum")'),'unknown manual house does not gain guessed strict minimum')
    button.scroll_into_view_if_needed();operator=p.locator('.rollsbar-operator-confirmation')
    require(operator.is_visible() and 'Окончательную стоимость заказа и условия доставки подтверждает оператор' in operator.inner_text(),'operator confirmation beside native submit')
    p.screenshot(path=str(out/f'operator-{width}.png'))
    button.click();p.wait_for_function('window.__rbAddressPayload!==null&&wp.data.select("wc/store/checkout").isIdle()')
    payload=p.evaluate('window.__rbAddressPayload');require(payload['shipping_address']['address_1']==manual and payload['payment_method']=='cod','manual address uses native Woo payload/COD')
    require(payload['additional_fields'].get('rollsbar/privacy-consent') is True,'explicit consent remains in native request')
    require(not payload.get('extensions',{}).get('rollsbar-delivery',{}).get('address_proof'),'manual text does not forge geocode proof')
    p.locator('.wc-block-checkout__shipping-method [role=radio]').nth(1).click();settle_native(p)
    require(not p.evaluate('wp.data.select("wc/store/validation").getValidationError("rollsbar-delivery-address")'),'pickup clears delivery requirement')
    require(not address.is_visible(),'pickup hides client address')
    p.locator('[data-rollsbar-modal="1"]').evaluate('e=>e.scrollTop=0');p.screenshot(path=str(out/f'pickup-{width}.png'))
    require(p.evaluate('document.documentElement.scrollWidth<=innerWidth'),'no overflow')
    report['checks'].append({'width':width,'status':'PASS','street_only_posts':0,'manual_native_payload':True,'pickup_exempt':True,'operator_notice':True})
  browser.close()
 report['status']='PASS'
finally:(out/'evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
