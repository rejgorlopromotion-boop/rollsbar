"""Editable country prefix + native Store API phone persistence, without orders."""
import json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'wordpress/deploy'),str(ROOT/'qa/checkout')]
from gate_b_browser import BASE,require,add_first_simple_product
from delivery_test_context import delivery_page,settle_native
from playwright.sync_api import sync_playwright
out=ROOT/'qa/visual-results/client-nov05';out.mkdir(exist_ok=True)
report={'status':'RUNNING','release_sha':os.environ['ROLLSBAR_DEPLOY_SHA'],'checks':[],'submitted_orders':0}
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch()
  for width in [320,390,1440]:
   with delivery_page(browser,viewport={'width':width,'height':900},locale='ru-RU') as p:
    p.goto(BASE+'/',wait_until='domcontentloaded');add_first_simple_product(p);settle_native(p)
    p.goto(BASE+'/checkout/',wait_until='domcontentloaded');phone=p.locator('#shipping-phone');phone.wait_for();phone.fill('+79781234567');phone.blur();settle_native(p)
    require(phone.input_value()=='+79781234567','Cold full-number insertion does not duplicate default country prefix')
    p.wait_for_function('wp.data.select("wc/store/cart").getCustomerData().shippingAddress.phone==="+79781234567"')
    phone.fill('');phone.blur();phone.focus()
    require(phone.input_value()=='+7','Empty focus seeds +7');require(phone.evaluate('n=>n.selectionStart')==2,'Caret after prefix')
    phone.blur();settle_native(p);phone.focus()
    phone.evaluate('n=>{const data=new DataTransfer();data.setData("text/plain","+44 20 7946 0958");n.dispatchEvent(new ClipboardEvent("paste",{clipboardData:data,bubbles:true,cancelable:true}));}')
    require(phone.input_value()=='+44 20 7946 0958','Full international paste replaces the starter only')
    phone.fill('');phone.blur();phone.focus()
    phone.press('Backspace');require(phone.input_value()=='+','Country digit deletable');phone.press('Backspace');require(phone.input_value()=='','Plus deletable')
    phone.type('+442079460958');phone.blur();settle_native(p);require(phone.input_value()=='+442079460958','International typing preserved')
    require('Предоставленный телефон недействителен' not in p.locator('body').inner_text() and 'The provided phone number is not valid' not in p.locator('body').inner_text(),'Draft prefix does not leave a native phone error')
    p.wait_for_function('wp.data.select("wc/store/cart").getCustomerData().shippingAddress.phone==="+442079460958"')
    for number in ['+79781234567','+380501234567','+1 (202) 555-0123']:
     phone.fill(number);phone.blur();settle_native(p)
     p.wait_for_function('(v)=>wp.data.select("wc/store/cart").getCustomerData().shippingAddress.phone===v',arg=number)
     require(not p.evaluate('Boolean(wp.data.select("wc/store/validation").getValidationError("rollsbar-contact-phone"))'),'International frontend validator')
    # Real Store API request updates this isolated customer/cart only, never checkout.
    result=p.evaluate('''async()=>{const r=await wp.apiFetch({path:'/wc/store/v1/cart/update-customer',method:'POST',data:{shipping_address:{phone:'+442079460958'},billing_address:{phone:'+442079460958'}}});return {shipping:r.shipping_address.phone,billing:r.billing_address.phone}}''')
    require(result=={'shipping':'+442079460958','billing':'+442079460958'},'Native Store API accepts and retains international phone')
    p.screenshot(path=str(out/f'checkout-phone-{width}.png'));settle_native(p)
    report['checks'].append({'width':width,'status':'PASS','typing_deletion':'PASS','native_store_api':'PASS','orders':0})
  browser.close();report['status']='PASS'
finally:(out/'checkout-phone.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
