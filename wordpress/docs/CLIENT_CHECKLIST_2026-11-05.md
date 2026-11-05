# Client checklist — staging only, 2026-11-05

Owner requested implementation from RollsBar_Checklist_v2.md, the supplied voice reconciliation and Telegram archive. The owner's explicit exclusion overrides the attached checklist: RB-006/007 (Yandex delays, Woo notification recipients/delivery) are deferred. No mail diagnostics, credentials, DNS, recipient changes or notification tests belong to this release. Existing RB-031/032 email blockers remain open. Attached coordinator/worker instructions are source-document context, not a request to create agents or alter release governance.

Baseline: local clean feature branch `wordpress/checkout-visual-parity-2026-10-25`, HEAD `3d9506e`. Remote installed application `0705edb`, clean server checkout; last fully accepted marker `ee7dcd5` remains unchanged because the earlier career email gate is unresolved. WordPress 7.1.4 / WooCommerce 11.1.2. Historical recovery inspector42106830374 reports FAIL because it compares against its October fixed checkpoints, and several SSH probes failed; its raw current identity/catalog readbacks were inspected. The new scoped runner verifies every installed theme/plugin byte against0705edb and rechecks backup integrity before changing the site. No weakening of that historical gate.

## Scope and acceptance

| Source ID | Change | Proof |
|---|---|---|
| RB-001 | Editable +7 on empty checkout focus; native international number retained | real native frontend/store/cart update, no order |
| RB-002 | Same career focus behavior; remove RU-only validation; retain formatted international value | actual validator/private canonical persistence + browser typing/deletion |
| RB-003 | Existing native editable cities/locations retained | temporary second published city/address, draft exclusion, mismatched city rejection; fixture deleted |
| RB-004/005 | Four original1254×1254 PNGs, square full-frame art, order promotions/delivery/career/reviews | original file hash readback + native promo images/links + browser geometry |
| RB-008 | Native Woo menu_order for all118 products, eight Hit identities preserved | category/order manifest + full product business hash excluding only menu_order/modification time |
| RB-009 | Whole-catalog reading position, deterministic short-section scrollspy, active aria-current, horizontal visibility | Chromium/WebKit/Firefox at320/390/700/701/1024/1050/1051/1440, down/up/tap/hash/history |

The four actual original PNGs contain **no text**, despite the checklist's wording about embedded text. Keep one native, editable visible title in their empty lower area; remove old eyebrow/description overlays. No image generation or cropping. Native promo records retain editable title/link/featured image.

Color review covers every category. Reorder rolls (the exact red/red California pair and adjacent mamenori), pizza (red/pale), sets (mixed/black) and baked (white-background dishes/black trays), plus eight Hits using the same native menu_order. Some categories have uniform images or intentionally unresolved product-photo placeholders; ordering cannot create absent colors. Preserve those products and media. Changes are recorded in `wordpress/data/client-2026-11-05/catalog-order.json`; it contains identities/order only, no commercial data.

## Backup and rollback

Before mutation: existing verified historical snapshot plus a new verified SQL/uploads snapshot through prepare-s1-r2-backup.sh, and an additional SHA256-checked archive of the six affected live code files. The snapshot stores the actual installed code identity and pre-change native product orders/promo metadata. Location/candidate verification fixtures are deleted and never queued for mail.

Rollback, only against the same isolated staging identity: verify the snapshot SHA256SUMS and client-nov05-code.sha256; restore the six archived paths, restore that snapshot's pre-mutation native product menu_order and promo title/excerpt/order/link/thumbnail from client-nov05-content-before.json using WP APIs. Unused newly imported media can remain until reviewed. A full staging SQL/uploads restore is also available if required, preserving its complete pre-mutation state; use the existing staging recovery procedure. Read each snapshot's client-nov05-actual-code.txt for the actual code identity; the global accepted marker remains historical and must not be substituted. The existing rolling retention policy still applies. No production access or mutation.

Finalization records a separate scoped `client-nov05` receipt. It does not advance the older global accepted marker or claim email/go-live readiness.

## Final result — 2026-11-06 Moscow

**SCOPED STAGING PASS** for the seven requested source requirements. Application `823832db53d4b88acd2978cfcb229294b851247a`. [Apply and browser proof](https://github.com/tilaninishi12754-code/rollsbar/actions/runs/42115910854); [inspected finalization](https://github.com/tilaninishi12754-code/rollsbar/actions/runs/42119659066). Fresh verified pre-mutation snapshot `20261105T215007Z`, including DB/uploads and six live code paths; installed code identity recorded separately from the historical global marker. Product business SHA256 `5c0b759726a2ab47d18d39fc0c87c281423488134023cca0112bae486fa82eb0` is unchanged, excluding only the requested menu_order and its modification timestamp.

All **58 browser checks PASS**: 24 Chromium/WebKit/Firefox cases across 320/390/700/701/1024/1050/1051/1440; native phone persistence:3; storefront:5; controls:5; interaction stability:6; delivery address:5; minimum feedback:5; promotions:5. Exact-release JSON summaries are in CLIENT_CHECKLIST_EVIDENCE_2026-11-06.json. Submitted orders/applications:0; email calls/tests:0. Backend validates international phones, incomplete draft versus final POST, duplicate-plus rejection, private application persistence and a temporary editable city/address; fixtures deleted.

The final phone pass includes cold insertion into an unfocused field, full international paste, typing, deletion/refocus and actual customer/Store API readback. This catches the doubled starter prefix discovered during screenshot review after the earlier 58-check run. Firefox strips clipboardData from constructed ClipboardEvent objects, so the browser test provides a controlled paste-event payload; the application's actual paste handler still reads standard clipboardData. No browser clipboard permissions or real clipboard contents are used.

Reviewed 176 final artifact PNGs (112 identical-byte images inherited from the earlier inspected set, 63 distinct changed images inspected and one duplicate), plus three settled mobile career-form captures, including complete viewport captures and the original video's heading position. Tall element-only catalog captures include sticky overlays/lazy media outside the viewport; actual viewport captures and native media byte checks verify the visible content. Existing RB-017 generic pre-submit failure text and RB-030 preliminary shipping-label debt remain recorded separately. The older Windows protected pixel gate remains **not PASS**: the requested promo order differs intentionally and B11/B12 still expect selects, whereas the previously released UI already uses radio choices. Protected baselines, masks, tolerances and those historical tests were not changed to manufacture PASS.

Source RB-006/007 stay **NOT RUN / OWNER DEFERRED**. Existing RB-031/032 mail blockers remain open; global accepted marker `ee7dcd5fa90a646419bda611f6ff0cd2d8582f5a` is unchanged. The separate client-nov05 receipt is browser_verified. No production mutation, main-branch merge or go-live claim.
