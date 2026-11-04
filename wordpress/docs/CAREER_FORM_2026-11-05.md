# Career form and dark-footer logo

Owner requested port of the existing GitHub career questionnaire to native WordPress, editable establishment addresses, applications emailed to `stroy_business24@mail.ru`, and a readable footer logo. Scope is staging only; no Woo order creation.

Implementation: existing `/rabota-v-rolls-bar/` template, native `admin-post.php` submission with nonce, private canonical candidate record, native Action Scheduler / `wp_mail` using the existing SMTP configuration. No external form processor or second candidate store. City and published establishment are validated together on the server. Administrators / shop managers can manage addresses under **Rolls Bar → Адреса заведений** and inspect **Анкеты кандидатов**. The real primary address is seeded once from existing company settings; future unpublished addresses are excluded.

Fields: city, establishment address, direction, phone, first name and explicit employment-contact consent required; surname, date of birth and comment optional. Existing generic directions are preserved; no active vacancy or invented branch is published. Phone accepts 8 / 7 and stores +7. Errors appear beside the fields, including consent. Duplicate form tokens prevent repeated submissions. Private applications remain available if email fails; email retries are bounded at three. Successful redirect means the application was saved, not a claim of inbox delivery. Form responses are no-store so shared page caches cannot retain nonces / duplicate tokens.

Footer SVG embeds the original logo bitmap and changes dark letter pixels to white without replacing the drawing; header logo stays original. ImageGen was tried and rejected because it redrew outlines. GitHub static footer references the same self-contained SVG.

Local validation fixture: valid canonical application and 11 invalid cases PASS; PHP/JavaScript/Python syntax PASS. Staging integration will verify private access, live editable address lookup, retries and sent-message idempotency with intercepted email, then one clearly marked test application will exercise the actual requested recipient. Existing checkout and storefront regression gates remain unchanged.

Release status: pending staging deploy and verification. Final evidence will be added after actual screenshot inspection.
