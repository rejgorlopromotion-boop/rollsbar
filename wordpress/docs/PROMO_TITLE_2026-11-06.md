# Career promo title readability — staging

The longer native title “Работа в Rolls Bar” overlapped the illustration's red area. A compact opaque white backing now follows the title, with rounded corners and safe wrapping. Only the career artwork card is affected. The original images, editable title/link, card order and all other application files are preserved.

Application: `cab31f46ba19904bbe98df4541c9c186fb3fce02`.
Verified fresh DB/uploads backup: `20261106T013129Z`, outside webroot, plus `promo-title-before.css` and its verified SHA256 for direct CSS rollback. All tracked theme/plugin bytes checked before/after; product business hash unchanged. Global accepted marker and previous scoped receipts remain historical.

Local live verification: 21/21 checks PASS — Chromium, WebKit and Firefox at 320, 390, 700, 701, 1051, 1440 and 2048px. Confirms opaque white background, dark text, title within the card, no title overflow, unchanged four titles and career destination. Reviewed all 30 local PNGs in five contact sheets plus desktop/mobile captures individually. Product images outside this focused card may still be loading in the full-page captures; no claim of a full storefront regression in this narrow CSS fix.

[Backed-up application run](https://github.com/tilaninishi12754-code/rollsbar/actions/runs/42144269353) applied successfully; its browser step stopped before starting because the diagnostic wrapper required a missing staging-base environment variable. [Verification-only rerun](https://github.com/tilaninishi12754-code/rollsbar/actions/runs/42144535471) supplies that variable and targets the already deployed application, without another mutation.

No order/application submissions, email tests or configuration changes. Yandex delay and Woo notification work remain owner-deferred. No production mutation.

Verification-only run completed SUCCESS; all 21 browser cases passed. The installed application stays at `cab31f4`; subsequent commits contain verification tooling/documentation only.
