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

Before mutation: existing verified historical snapshot plus a new verified SQL/uploads snapshot through prepare-s1-r2-backup.sh, and an additional SHA256-checked archive of the five affected live code files. The snapshot stores the actual installed code identity and pre-change native product orders/promo metadata. Location/candidate verification fixtures are deleted and never queued for mail.

Rollback, only against the same isolated staging identity: verify the snapshot SHA256SUMS and client-nov05-code.sha256; restore the five archived paths, restore the original native product menu_order and promo title/link/thumbnail from client-nov05-content-before.json using WP APIs. Unused newly imported media can remain until reviewed. A full staging SQL/uploads restore is also available if required, preserving its complete pre-change state; use the existing staging recovery procedure. Do not substitute an accepted marker for the actual0705edb code identity. No production access or mutation.

Finalization records a separate scoped `client-nov05` receipt. It does not advance the older global accepted marker or claim email/go-live readiness.
