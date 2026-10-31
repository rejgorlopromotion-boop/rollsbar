import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source=readFileSync('wordpress/wp-content/plugins/rollsbar-core/assets/js/checkout.js','utf8');
const code=source.match(/function hasCompleteAddress\(address\)\{[\s\S]*?\n\t\}/)[0];
const check=vm.runInNewContext('('+code+')');
const cases=JSON.parse(readFileSync('qa/checkout/address-completeness.json','utf8'));
for(const [address,expected] of cases)assert.equal(check(address),expected,address);
console.log('ADDRESS_COMPLETENESS_JS_PASS',cases.length);
