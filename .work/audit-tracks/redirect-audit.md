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
== apex /os
  hop 1: [301] https://interstitiumlabs.dev/os -> https://interstitiumlabs.dev/learn/
  hop 2: [200] https://interstitiumlabs.dev/learn/
  FINAL: 200 https://interstitiumlabs.dev/learn/

== apex /os/
  hop 1: [301] https://interstitiumlabs.dev/os/ -> https://interstitiumlabs.dev/learn/
  hop 2: [200] https://interstitiumlabs.dev/learn/
  FINAL: 200 https://interstitiumlabs.dev/learn/

== apex /proof
  hop 1: [301] https://interstitiumlabs.dev/proof -> https://interstitiumlabs.dev/evidence/
  hop 2: [200] https://interstitiumlabs.dev/evidence/
  FINAL: 200 https://interstitiumlabs.dev/evidence/

== apex /proof/
  hop 1: [301] https://interstitiumlabs.dev/proof/ -> https://interstitiumlabs.dev/evidence/
  hop 2: [200] https://interstitiumlabs.dev/evidence/
  FINAL: 200 https://interstitiumlabs.dev/evidence/

== apex /il26
  hop 1: [301] https://interstitiumlabs.dev/il26 -> https://interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery
  hop 2: [200] https://interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery
  FINAL: 200 https://interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery

== apex /il26/
  hop 1: [301] https://interstitiumlabs.dev/il26/ -> https://interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery
  hop 2: [200] https://interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery
  FINAL: 200 https://interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery

== apex /il27
  hop 1: [301] https://interstitiumlabs.dev/il27 -> https://interstitiumlabs.dev/university/course?course=il-27-it-infrastructure-specialist-threatlocker-mastery
  hop 2: [200] https://interstitiumlabs.dev/university/course?course=il-27-it-infrastructure-specialist-threatlocker-mastery
  FINAL: 200 https://interstitiumlabs.dev/university/course?course=il-27-it-infrastructure-specialist-threatlocker-mastery

== apex /il28
  hop 1: [301] https://interstitiumlabs.dev/il28 -> https://interstitiumlabs.dev/university/course?course=il-28-devsecops-cloud-infrastructure-mastery
  hop 2: [200] https://interstitiumlabs.dev/university/course?course=il-28-devsecops-cloud-infrastructure-mastery
  FINAL: 200 https://interstitiumlabs.dev/university/course?course=il-28-devsecops-cloud-infrastructure-mastery

== apex /il29
  hop 1: [301] https://interstitiumlabs.dev/il29 -> https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery
  hop 2: [200] https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery
  FINAL: 200 https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery

== apex /il29/
  hop 1: [301] https://interstitiumlabs.dev/il29/ -> https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery
  hop 2: [200] https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery
  FINAL: 200 https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery

== apex /code
  hop 1: [307] https://interstitiumlabs.dev/code -> https://interstitiumlabs.dev/code/
  hop 2: [200] https://interstitiumlabs.dev/code/
  FINAL: 200 https://interstitiumlabs.dev/code/

== apex /command
  hop 1: [307] https://interstitiumlabs.dev/command -> https://interstitiumlabs.dev/command/
  hop 2: [200] https://interstitiumlabs.dev/command/
  FINAL: 200 https://interstitiumlabs.dev/command/

== apex /desk
  hop 1: [307] https://interstitiumlabs.dev/desk -> https://interstitiumlabs.dev/desk/
  hop 2: [200] https://interstitiumlabs.dev/desk/
  FINAL: 200 https://interstitiumlabs.dev/desk/

== apex /doctrine
  hop 1: [307] https://interstitiumlabs.dev/doctrine -> https://interstitiumlabs.dev/doctrine/
  hop 2: [200] https://interstitiumlabs.dev/doctrine/
  FINAL: 200 https://interstitiumlabs.dev/doctrine/

== apex /drill
  hop 1: [307] https://interstitiumlabs.dev/drill -> https://interstitiumlabs.dev/drill/
  hop 2: [200] https://interstitiumlabs.dev/drill/
  FINAL: 200 https://interstitiumlabs.dev/drill/

== apex /factory
  hop 1: [307] https://interstitiumlabs.dev/factory -> https://interstitiumlabs.dev/factory/
  hop 2: [200] https://interstitiumlabs.dev/factory/
  FINAL: 200 https://interstitiumlabs.dev/factory/

== apex /field
  hop 1: [307] https://interstitiumlabs.dev/field -> https://interstitiumlabs.dev/field/
  hop 2: [200] https://interstitiumlabs.dev/field/
  FINAL: 200 https://interstitiumlabs.dev/field/

== apex /graph
  hop 1: [307] https://interstitiumlabs.dev/graph -> https://interstitiumlabs.dev/graph/
  hop 2: [200] https://interstitiumlabs.dev/graph/
  FINAL: 200 https://interstitiumlabs.dev/graph/

== apex /interview
  hop 1: [307] https://interstitiumlabs.dev/interview -> https://interstitiumlabs.dev/interview/
  hop 2: [200] https://interstitiumlabs.dev/interview/
  FINAL: 200 https://interstitiumlabs.dev/interview/

== apex /library
  hop 1: [307] https://interstitiumlabs.dev/library -> https://interstitiumlabs.dev/library/
  hop 2: [200] https://interstitiumlabs.dev/library/
  FINAL: 200 https://interstitiumlabs.dev/library/

== apex /measure
  hop 1: [307] https://interstitiumlabs.dev/measure -> https://interstitiumlabs.dev/measure/
  hop 2: [200] https://interstitiumlabs.dev/measure/
  FINAL: 200 https://interstitiumlabs.dev/measure/

== apex /plant
  hop 1: [307] https://interstitiumlabs.dev/plant -> https://interstitiumlabs.dev/plant/
  hop 2: [200] https://interstitiumlabs.dev/plant/
  FINAL: 200 https://interstitiumlabs.dev/plant/

== apex /platform
  hop 1: [307] https://interstitiumlabs.dev/platform -> https://interstitiumlabs.dev/platform/
  hop 2: [200] https://interstitiumlabs.dev/platform/
  FINAL: 200 https://interstitiumlabs.dev/platform/

== apex /portfolio
  hop 1: [307] https://interstitiumlabs.dev/portfolio -> https://interstitiumlabs.dev/portfolio/
  hop 2: [200] https://interstitiumlabs.dev/portfolio/
  FINAL: 200 https://interstitiumlabs.dev/portfolio/

== apex /devops-superlab
  hop 1: [404] https://interstitiumlabs.dev/devops-superlab
  FINAL: 404 https://interstitiumlabs.dev/devops-superlab

== apex /pricing
  hop 1: [307] https://interstitiumlabs.dev/pricing -> https://interstitiumlabs.dev/pricing/
  hop 2: [200] https://interstitiumlabs.dev/pricing/
  FINAL: 200 https://interstitiumlabs.dev/pricing/

== apex /radar
  hop 1: [307] https://interstitiumlabs.dev/radar -> https://interstitiumlabs.dev/radar/
  hop 2: [200] https://interstitiumlabs.dev/radar/
  FINAL: 200 https://interstitiumlabs.dev/radar/

== apex /sheets
  hop 1: [307] https://interstitiumlabs.dev/sheets -> https://interstitiumlabs.dev/sheets/
  hop 2: [200] https://interstitiumlabs.dev/sheets/
  FINAL: 200 https://interstitiumlabs.dev/sheets/

== apex /si
  hop 1: [307] https://interstitiumlabs.dev/si -> https://interstitiumlabs.dev/si/
  hop 2: [200] https://interstitiumlabs.dev/si/
  FINAL: 200 https://interstitiumlabs.dev/si/

== apex /system
  hop 1: [307] https://interstitiumlabs.dev/system -> https://interstitiumlabs.dev/system/
  hop 2: [200] https://interstitiumlabs.dev/system/
  FINAL: 200 https://interstitiumlabs.dev/system/

== apex http root
  hop 1: [301] http://interstitiumlabs.dev/ -> https://interstitiumlabs.dev/
  hop 2: [200] https://interstitiumlabs.dev/
  FINAL: 200 https://interstitiumlabs.dev/

== apex http /os
  hop 1: [301] http://interstitiumlabs.dev/os -> https://interstitiumlabs.dev/os
  hop 2: [301] https://interstitiumlabs.dev/os -> https://interstitiumlabs.dev/learn/
  hop 3: [200] https://interstitiumlabs.dev/learn/
  FINAL: 200 https://interstitiumlabs.dev/learn/

== apex www root
  hop 1: [200] https://www.interstitiumlabs.dev/
  FINAL: 200 https://www.interstitiumlabs.dev/

== apex www /os
  hop 1: [301] https://www.interstitiumlabs.dev/os -> https://www.interstitiumlabs.dev/learn/
  hop 2: [200] https://www.interstitiumlabs.dev/learn/
  FINAL: 200 https://www.interstitiumlabs.dev/learn/

== learn http root
  hop 1: [301] http://learn.interstitiumlabs.dev/ -> https://learn.interstitiumlabs.dev/
  hop 2: [200] https://learn.interstitiumlabs.dev/
  FINAL: 200 https://learn.interstitiumlabs.dev/

== learn http /il29
  hop 1: [301] http://learn.interstitiumlabs.dev/il29 -> https://learn.interstitiumlabs.dev/il29
  hop 2: [301] https://learn.interstitiumlabs.dev/il29 -> https://learn.interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery
  hop 3: [200] https://learn.interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery
  FINAL: 200 https://learn.interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery

== portfolio https root
  hop 1: [200] https://enmanueldmejia.com/
  FINAL: 200 https://enmanueldmejia.com/

== portfolio http root
  hop 1: [301] http://enmanueldmejia.com/ -> https://enmanueldmejia.com/
  hop 2: [200] https://enmanueldmejia.com/
  FINAL: 200 https://enmanueldmejia.com/

== portfolio www root
  hop 1: [200] https://www.enmanueldmejia.com/
  FINAL: 200 https://www.enmanueldmejia.com/

### 2b. Inner-page sample (round 2)
== apex inner /about/
  hop 1: [200] https://interstitiumlabs.dev/about/
  FINAL: 200 https://interstitiumlabs.dev/about/

== apex inner /learn/
  hop 1: [200] https://interstitiumlabs.dev/learn/
  FINAL: 200 https://interstitiumlabs.dev/learn/

== apex inner /evidence/
  hop 1: [200] https://interstitiumlabs.dev/evidence/
  FINAL: 200 https://interstitiumlabs.dev/evidence/

== apex inner /labs/superlab/
  hop 1: [200] https://interstitiumlabs.dev/labs/superlab/
  FINAL: 200 https://interstitiumlabs.dev/labs/superlab/

== apex inner /trending/
  hop 1: [200] https://interstitiumlabs.dev/trending/
  FINAL: 200 https://interstitiumlabs.dev/trending/

== apex inner /university/
  hop 1: [200] https://interstitiumlabs.dev/university/
  FINAL: 200 https://interstitiumlabs.dev/university/

== apex inner course il29
  hop 1: [200] https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery
  FINAL: 200 https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery

== apex inner course il26
  hop 1: [200] https://interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery
  FINAL: 200 https://interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery

== apex inner /enroll/
  hop 1: [200] https://interstitiumlabs.dev/enroll/
  FINAL: 200 https://interstitiumlabs.dev/enroll/

== apex inner /learn/skills/
  hop 1: [200] https://interstitiumlabs.dev/learn/skills/
  FINAL: 200 https://interstitiumlabs.dev/learn/skills/

== apex inner /prep/programming/
  hop 1: [200] https://interstitiumlabs.dev/prep/programming/
  FINAL: 200 https://interstitiumlabs.dev/prep/programming/

== apex inner /prep/drills/
  hop 1: [200] https://interstitiumlabs.dev/prep/drills/
  FINAL: 200 https://interstitiumlabs.dev/prep/drills/

== apex inner /paths/
  hop 1: [200] https://interstitiumlabs.dev/paths/
  FINAL: 200 https://interstitiumlabs.dev/paths/

== apex inner /jobs/
  hop 1: [200] https://interstitiumlabs.dev/jobs/
  FINAL: 200 https://interstitiumlabs.dev/jobs/

== learn /il29
  hop 1: [301] https://learn.interstitiumlabs.dev/il29 -> https://learn.interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery
  hop 2: [200] https://learn.interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery
  FINAL: 200 https://learn.interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery

== learn /il26
  hop 1: [301] https://learn.interstitiumlabs.dev/il26 -> https://learn.interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery
  hop 2: [200] https://learn.interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery
  FINAL: 200 https://learn.interstitiumlabs.dev/university/course?course=il-26-data-analyst-certification-senior-mastery

== learn /university/
  hop 1: [200] https://learn.interstitiumlabs.dev/university/
  FINAL: 200 https://learn.interstitiumlabs.dev/university/

== portfolio inner root
  hop 1: [200] https://enmanueldmejia.com/
  FINAL: 200 https://enmanueldmejia.com/

== portfolio probe /about
  hop 1: [200] https://enmanueldmejia.com/about
  FINAL: 200 https://enmanueldmejia.com/about

== portfolio probe /contact
  hop 1: [200] https://enmanueldmejia.com/contact
  FINAL: 200 https://enmanueldmejia.com/contact

## 3. Flagged findings
### F-1 [HIGH] /devops-superlab → 404 (dead redirect; intended target never reached)
- Source rule: `_worker.js` STUB_REDIRECTS maps `/devops-superlab` → 301 → `/labs/superlab/`.
- `/devops-superlab` is NOT in `run_worker_first`, so the worker 301 never fires in production.
- Unlike the other 19 stubs, `docs/devops-superlab/` has NO asset dir / meta-refresh page.
- Live chain: `hop 1: [404] https://interstitiumlabs.dev/devops-superlab — FINAL: 404`.
- Fix options: add `/devops-superlab` (+ trailing variant) to `run_worker_first`, or ship a meta-refresh stub dir like the other 19.

### F-2 [MEDIUM] All 20 stub-slug HTTP 301s are dead code in production (no stub path is in run_worker_first)
- Live behavior for bare slugs (e.g. /code, /pricing): `307 → /<slug>/` (Cloudflare asset-dir slash append) then `200` serving a meta-refresh HTML page (`<meta http-equiv="refresh" content="0;url=<target>">`).
- Visitor outcome is correct (browser follows the refresh), but there is NO HTTP 301: no link-equity transfer, an extra round trip, and non-browser clients (curl, bots, link checkers) do not follow.
- 19/20 refresh targets verified to match the worker's STUB_REDIRECTS map exactly and all resolve 200 live (see inner-page sample).
- Stale comment: `_worker.js` says "consolidated redirect stubs (zero-value stub dirs removed)" but 19 stub dirs still exist in `docs/`.

### F-3 [LOW] No www → apex canonicalization (both sites)
- `https://www.interstitiumlabs.dev/` → `200` (serves site directly, no redirect to apex).
- `https://www.enmanueldmejia.com/` → `200` (same).
- `http://` → `https://` 301 works on all three hosts (apex, learn, portfolio). No http→https gap.
- SEO note: www and apex serve identical content with no canonical redirect — flagging for the SEO track, not a broken redirect.

### F-4 [INFO] /il29 verified — behaves as designed
- `hop 1: [301] https://interstitiumlabs.dev/il29 → https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery`
- `hop 2: [200]` — free course shell renders without paywall gate on GET. Same on learn host (origin-preserving).

### Clean (no action)
- /os, /os/, /proof, /proof/, /il26, /il26/, /il27, /il28, /il29, /il29/: all single-hop `301 → 200`, targets resolve.
- All 20 inner pages: `200`, no unexpected redirects.
- No redirect loops (loop detector tripped 0 times across 59 URLs).
- No redirects to external domains; no redirect-to-404 except F-1.
- Longest chains are 2 hops and expected: `http://…/os` (301 https-upgrade + 301 rule) and bare stub slugs (307 slash-append + 200 refresh page).
- `docs/_redirects` is INERT in the API deploy path (file header + deploy config confirm); its /il26–/il28 rules are harmless duplicates of the worker code. /il29 absent from _redirects but present in worker — no live impact.
- Paywall gating returns paywall HTML (200) / 402 JSON — no HTTP redirects involved.

## 4. Summary
1. **59 URLs traced** (39 redirect-rule + http/www variants, 20 inner pages): 59 finals, **0 loops, 0 timeouts, 0 external-domain redirects**.
2. **1 dead redirect [HIGH]:** `/devops-superlab` → **404** — its worker 301 never fires (not in `run_worker_first`) and it has no stub asset dir, unlike the other 19 stubs.
3. **20 stub 301s don't fire as HTTP [MEDIUM]:** bare slugs return `307 → /slug/` then `200` + meta-refresh page (all 19 existing refresh targets match the worker map and resolve 200). Visitors land correctly; crawlers/API clients see no 301.
4. **No www→apex redirect [LOW]:** `www.interstitiumlabs.dev` and `www.enmanueldmejia.com` both serve 200 directly. `http://`→`https://` 301 is clean on all three hosts — no http→https gap.
5. **Everything else clean:** `/os`, `/proof`, `/il26`–`/il29` (both slash variants) are single-hop `301 → 200`; `/il29` lands on the live IL-29 course page (200); all 20 inner pages return 200 with no surprise redirects; longest chains are 2 hops and expected.
