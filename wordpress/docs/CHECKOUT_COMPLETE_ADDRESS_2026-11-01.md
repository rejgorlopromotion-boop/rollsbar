# Full delivery address and operator confirmation

Status: local verification PASS; staging acceptance pending. Production forbidden, no submitted orders authorized.

Owner override 2026-11-01: delivery requires a street/local address name and a house, including manual entry when no matching suggestion exists. A street-only, town-only or empty address must block native checkout, focus/scroll to the address and explain what to complete. Pickup retains phone + explicit consent with client address hidden. Name remains optional. This supersedes the former delivery phone-only allowance; it does not require a verified geocoder house or turn imprecise coordinates into precise coordinates.

Add a permanent note beside the native place-order action, in both modes: final order cost and delivery conditions are confirmed by the operator, who calls after the request. Existing native COD remains the only payment path. No online payment, fee or automatic birthday discount is added.

Implementation: PHP pre-order Store API guard checks completeness before the existing signed delivery-minimum check. Equivalent client grammar uses the existing Woo validation store, native click path, focus and local red marker. No second form, submission endpoint, cart state or address storage. Numeric street names alone (8 Марта, 60 лет Октября, 2-я улица Коллективных садов) cannot supply a house. Manual completion permits native callback assembly without signed zone proof. Existing known-minimum blocks, consent/phone priority, pickup exemption and DaData precision safety remain.

Local proof: shared 26 address examples pass both actual PHP helper and extracted browser helper; native-policy fixtures retain known minimum, saved proof, low-precision/manual callback, consent and note cleanup behavior. Five-width shadow browser checks at1440/701/700/390/320 PASS: actual provider street-only selection, zero native POST assembly on incomplete address, visible field focus/error, manual complete native payload without HTTP submission, operator note, pickup exemption. Preview-only critical screenshots reviewed; final live artifact/vision review is required before PASS.

Earlier tests accepting blank delivery address were updated only for the explicit owner override. Blank pickup address and manually complete unknown delivery remain accepted. No baseline/masks/geometry tolerance relaxed.
