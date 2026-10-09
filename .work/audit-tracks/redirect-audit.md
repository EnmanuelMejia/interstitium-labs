# Track 7 — Redirect Audit
**Date:** 2026-10-08 · **Scope:** audit only, no code changed
**Sites:** https://interstitiumlabs.dev · https://learn.interstitiumlabs.dev · https://enmanueldmejia.com
**Method:** `curl` hop-by-hop (no -L; each hop's status + Location recorded manually, max 6 hops, loop detection),
plus source review of `docs/_redirects` and `docs/_worker.js` and `flagship-deploy-config-20261008.json`.

## 1. Redirect rules found in source

### docs/_redirects (NOTE: INERT in the API deploy path — file header + AGENTS.md confirm;
### only the worker code-level 301s + run_worker_first entries take effect)
| Source | Target | Code |
|---|---|---|
| /os, /os/ | /learn/ | 301 |
| /proof, /proof/ | /evidence/ | 301 |
| /il26 | /university/course?course=il-26-data-analyst-certification-senior-mastery | 301 |
| /il27 | /university/course?course=il-27-it-infrastructure-specialist-threatlocker-mastery | 301 |
| /il28 | /university/course?course=il-28-devsecops-cloud-infrastructure-mastery | 301 |

### docs/_worker.js code-level redirects (movedPermanently → 301; trailing-slash variants handled)
| Source | Target | Code |
|---|---|---|
| /os, /os/ | /learn/ | 301 |
| /proof, /proof/ | /evidence/ | 301 |
| /il26, /il26/ | /university/course?course=il-26-data-analyst-certification-senior-mastery | 301 |
| /il27, /il27/ | /university/course?course=il-27-it-infrastructure-specialist-threatlocker-mastery | 301 |
| /il28, /il28/ | /university/course?course=il-28-devsecops-cloud-infrastructure-mastery | 301 |
| /il29, /il29/ | /university/course?course=il-29-threatlocker-ai-cybersecurity-mastery | 301 |
| 20 STUB_REDIRECTS: /code→/prep/programming/ · /command→/paths/ · /desk→/learn/ · /doctrine→/about/ · /drill→/prep/drills/ · /factory→/labs/ · /field→/learn/ · /graph→/learn/skills/ · /interview→/prep/drills/ · /library→/learn/ · /measure→/learn/ · /plant→/paths/ · /platform→/about/ · /portfolio→/labs/superlab/ · /devops-superlab→/labs/superlab/ · /pricing→/enroll/ · /radar→/trending/ · /sheets→/prep/ · /si→/learn/ · /system→/about/ | (each) | 301 |

### Other redirect-ish responses in _worker.js (API/form flows, not site URL rules)
- POST /api/waitlist (non-JSON client) → **303** → /enroll/success.html
- GET /api/auth/verify (success) → **303** → /progress/ (sets session cookie)
- Paywall: paid courses without entitlement → paywall HTML page (200) or 402 JSON — **no HTTP redirect**

### run_worker_first (flagship-deploy-config-20261008.json) — worker invoked ONLY for these paths
/os, /os/, /proof, /proof/, /il26, /il26/, /il27, /il27/, /il28, /il28/, /il29, /il29/,
/api/*, /university/course, /university/course.html, /university/data/courses/*.json, …
**NOT covered: any of the 20 stub slugs** (/code, /desk, …). The _worker.js STUB_REDIRECTS
block is therefore unreachable in production.

## 2. Redirect map — live hop chains
(Live results below; `→` = Location header followed.)

### 2a. Redirect-rule URLs (round 1)
@@ROUND1@@

### 2b. Inner-page sample (round 2)
@@ROUND2@@

## 3. Flagged findings
@@FLAGS@@

## 4. Summary
@@SUMMARY@@
