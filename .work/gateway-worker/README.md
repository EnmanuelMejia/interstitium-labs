# interstitium-course-gateway worker source

- Worker: `interstitium-course-gateway` (Cloudflare account bb1baf6bc6c34d30fadc402b420fa3c2)
- File `interstitium-course-gateway-20261008-free-bootcamp.js`: downloaded bundle as deployed
  2026-10-08 ~10:15 EDT (deployment b1c0f873802b4f9cb3c99354f4fd524d),
  with the anonymous bypass for `/bootcamps/threatlocker-assessment-prep/`
  (the free bootcamp). All other gateway routes still require sign-in.
- No local build source exists; this file is the de-facto source. To change:
  edit this file, `node --check` it, and redeploy via PUT
  /accounts/<id>/workers/scripts/interstitium-course-gateway with multipart
  metadata (main_module index.js, compatibility_date 2026-10-07) including
  ALL bindings: CERT_BOOTCAMPS, FULL_SPECTRUM, MEMBERSHIP, THREATLOCKER_ASSESSMENT,
  THREATLOCKER_BOOTCAMP (service bindings) + COURSE_GATEWAY_ENABLED="true".
  See /tmp/deploy-gateway.py pattern (ephemeral) if needed again.
- Routes (Cloudflare worker routes, all three domains): /bootcamps/*, /bootcamp/*, /assessments/*,
  plus /bootcamps/threatlocker-assessment-prep/*.
