# Dead-link + blank-link audit — 2026-10-08 (final)

Sites: interstitiumlabs.dev · learn.interstitiumlabs.dev · enmanueldmejia.com
Authorized: user order 2026-10-08 ~09:09 EDT (+09:21 priority: /university/* inventory).
Scope honored: only href/src/action values changed in HTML; off-limits files untouched.
No deploy performed.

## Method
- Extracted every href/src/action (+ og:image/twitter:image/og:url meta content) from
  177 HTML pages (176 in ~/workspace/apex-audit/docs, 1 in ~/workspace/portfolio-site):
  10,081 URL occurrences → 989 unique checkable URLs.
- Each unique URL HTTP-checked live (curl -L, Chrome UA, 20s timeout, 1 retry;
  final status must be 2xx). 4xx/5xx/timeout = dead unless verified bot-blocked.
- Same-page anchors verified against repo id attributes; cross-page anchors against the
  target page's ids (index.html ↔ directory-URL normalized).
- learn.interstitiumlabs.dev serves BYTE-IDENTICAL content to interstitiumlabs.dev
  (verified: only diff is the Cloudflare challenge token) — a hostname alias, not a
  redirect to /university/. 40-URL spot-check on learn.: 39/39 matched flagship's 200
  (1 empty sample line). learn. links inherit flagship results.

## Counts
- Unique URLs checked: **989** → ok **904**, dead **83**, timeout **1**, bot-blocked **1**
  - interstitiumlabs.dev: 574 (63 non-ok — ALL deploy-caused or paywall-gated, see below)
  - enmanueldmejia.com: 12 — **0 dead**
  - external: 403 (github 81, kubernetes.io 33, learn.microsoft.com 21, …)
- Anchor-only links: 411 — verified, **2 broken found and fixed**
- mailto: links: 9 — valid, no action
- Blank/placeholder hrefs: 3 (`href="#"`) — all JS-populated at runtime (see Intentional)

## FIXED — genuinely wrong links (category b), each replacement verified 200 before writing
1. `docs/prep/devops/index.html` — TOC `href="#phase3"` had no matching id on the page
   → changed to `href="#main"` (exists; page top).
2. `docs/founders/index.html` — `href="/#bio"`; homepage has no `id="bio"`
   → changed to `href="/#founder-h"` (the founder bio section heading; verified present).
3. `docs/learn/sequences/crypto-protocols-2/index.html` — Mastering Bitcoin ch.1 link
   `…/blob/develop/ch01.asciidoc` 404 (repo restructured, now `ch01_intro.adoc`)
   → `https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch01_intro.adoc` (200 ✓).
4. `docs/learn/sequences/database-admin/index.html` ×8 — Oracle DBA guide landing
   `…/oracle-database/23/admin.html` 404 (Oracle restructured docs)
   → `https://docs.oracle.com/en/database/oracle/oracle-database/23/admin/` (200 ✓,
   "Oracle Database Database Administrator's Guide, 23ai").
5. `docs/prep/programming/index.html`, `docs/prep/index.html` — `https://www.bash.academy/`
   404 (site dead) → `https://www.gnu.org/software/bash/manual/` (200 ✓, official manual).
6. `docs/prep/index.html` — `learn.microsoft.com/…/training/paths/devsecops-mastery/`
   404 (MS retired the path; link text says "Azure Fundamentals")
   → `https://learn.microsoft.com/en-us/training/paths/azure-fundamentals/` (200 ✓).
7. `docs/prep/drills/instrument-desk/index.html` — Greenhouse Magic Leap posting #7589434
   302 → `…/magicleap?error=true` (posting removed; whole board 404s) → link wrapper
   removed, text "Greenhouse role #7589434" kept (no verified equivalent exists).

## "FIXED BY REDEPLOY" — category (a): correct links, broken live deploy
Every path below exists in ~/workspace/apex-audit/docs/ (file) or docs/_worker.js
(route) but 404s live. The deployed build lost a large part of the asset bundle +
worker routing (sibling LinkedIn audit independently confirmed ~13:10 EDT).
**Parent post-deploy verification must re-check every row.**

University subtree (the user's 404): `/university/`, `/university/course.html`,
`/university/course?course=<id>` (all 29 ids in docs/university/data/courses/*.json —
spot-checked il-04/il-05/il-19/il-26/il-28/il-29), `/university/courses.html`,
`/university/academy.html`, `/university/learn.html`, `/university/assess.html`,
`/university/path.html` (+ `?id=il03-generative-packing`), `/university/paths.html`,
`/university/tracks.html`, `/university/about.html`, `/university/enroll.html`,
`/university/honesty.html`, `/university/il-26-dossier.html`,
`/university/lab-generative-packing.html`, `/university/index.html`,
`/university/course-shell.css`, `/university/course-shell.js`, `/university/css/il.css`,
`/university/js/adaptive.js`, `/university/js/app.js`, `/university/js/hero.js`,
`/university/js/noah.js`, `/university/manifest.webmanifest`,
`/university/assets/apple-touch-icon.png`, `/university/assets/noah-avatar.png`,
`/university/assets/sigil-hero-static.png`, `/university/assets/sigil.svg`,
`/university/og/*.png` ×7 (il-26, il-27, il-28, il-29, devops-superlab, lps-enrollment,
sundance-ai — two edge-timed-out but same dead subtree).

Other deploy-missing files (exist in repo, 404 live):
`/assets/il-unified.css` (81 KB — referenced by **152 pages**),
`/assets/il-mobile390.css`, `/assets/il-seq.css`, `/assets/il-check.js`,
`/assets/il-seq.js`, `/learn/sequences/`, `/learn/sequences/ai-aided-cybersecurity/`,
`/learn/sequences/serving-stack-ops/`, `/learn/sequences/il-widgets.js`, `/start/`,
`/evidence/`, `/paths/adaptive-ops-math/`, `/certificates/`, `/progress/`,
`/search/`, `/search/search-app.js`, `/enroll/checkout.css`, `/enroll/checkout.html`,
`/enroll/checkout.js`, `/enroll/vendor/qrcode.js`, `/work/lps-enrollment-analysis/`,
`/work/sundance-ai-architecture/`, `/api/waitlist` (worker route),
`/il26` `/il27` `/il28` `/il29` (worker code-level 301s not firing — flagship IL-29
launch URL currently down).

## Paywall-gated by design (not dead links)
`/bootcamps/`, `/bootcamps/tl-interview/`, `/bootcamps/threatlocker-assessment-prep/`
(+ learn. alias) → **401 JSON, Vary: Cookie** for anonymous requests: the deployed
worker's entitlement gate. No repo files and no repo worker route, so the content is
served/allowed only with an `il_entitlement` cookie. **Parent: verify with an
entitlement cookie post-deploy** — anonymous 401 is expected IF the bootcamp is a
paid product; if it should be free, the gate is misconfigured.

## Bot-blocked / verified-OK (no fix)
- `linkedin.com/in/enmanuelmejia` → 999 (LinkedIn bot-wall; his real profile)
- `education.oracle.com/product/pexam_1Z0-829` → curl 403, page verified live via
  text fetch (Java SE 17 Developer exam page renders fully)
- `learnmeabitcoin.com/`, `labex.io/linuxjourney`, `linuxjourney.com`,
  `litecoin.com/`, `livesql.oracle.com/` → curl 403, all verified live via text fetch
- `freedesktop.org/…/systemd.{service,timer,unit}.html`, `journalctl.html` → curl 418
  (bot joke-status), pages verified live via text fetch
- `devops.com/`, `dash.cloudflare.com/` → curl 403 (login/bot wall; legitimate targets)
- `github.com/ggml-org/ggml/blob/master/docs/gguf.md` → 429 once, **200 on retry**
- `education.oracle.com/` root → curl timeout; the actually-linked product page above
  verified live

## Intentional (no change)
- 3× `href="#"`: `start-rec-path`, `start-rec-lesson` (docs/start/index.html),
  `cta-sitting` (docs/university/path.html) — set at runtime by inline page scripts
  (personalized CTAs); hard-coding would break them.
- `rel="preconnect"` to `fonts.googleapis.com` / `fonts.gstatic.com` — bare-domain 404
  is expected and harmless.
- `#/study`-style fragments in course.html — SPA route tokens, not DOM ids.
- `docs/assets/il-unified-nav.html` `#main` — include file; refers to host pages, all of
  which have `<main id="main">`.

## Unfixable / needs-user
None. Every dead link was either fixed (7), attributed to the broken deploy (list
above), paywall-gated (verify post-deploy), or bot-blocked-but-verified.

## Off-limits file findings (read-only; NOT edited)
- `docs/university/academy.html`: links are `/university/`, `course.html?course=<slug>`,
  `learn.html`, `assess.html`, `path.html?id=`, `paths.html`, `honesty.html`, internal
  assets — all exist in repo; all 404 live = deploy-caused. Nothing wrong in the file.
- `docs/university/course-shell.js`: builds links from course JSON (`dossierUrl`,
  `r.url`/`s.url`/`v.url`) + `assets/noah-avatar.png` — all resolve to repo/deploy
  paths; nothing wrong in the file.
- `docs/_worker.js`, `docs/payment-routes.js`, `docs/university/data/courses/*.json`:
  reviewed for route inventory only (`/university/course`, `/university/course.html`,
  `/il26`–`/il29` 301s, `/api/waitlist`); no edits.
- Note: `docs/university/index.html` line ~117/141/143 and `docs/index.html:430`
  reference the ThreatLocker bootcamp on learn. (401 = paywall gate, see above).

## learn.interstitiumlabs.dev findings
- NOT a redirect: returns 200 serving byte-identical flagship content (only diff is the
  CF challenge token). The "fold into /university/" did not remove the alias.
- `/university/*` 404s identically on learn. (deploy-caused, same fix).
- 40-URL spot-check: every URL 200 on flagship was also 200 on learn. — the alias is
  healthy wherever the deploy is healthy.

## enmanueldmejia.com findings
- Source repo `~/workspace/portfolio-site` matches live (only diff: CF challenge script).
- All 12 internal URLs 200. External profile links: github.com/EnmanuelMejia 200,
  linkedin.com/in/enmanuelmejia 999 (bot-wall, assumed OK).
- Portfolio links to `interstitiumlabs.dev/university/` and 3 course URLs — all
  deploy-caused 404s, fixed by redeploy. Portfolio `#about/#top/#work/#main/#contact/
  #stack` anchors all resolve (ids present).

## Scripts (re-runnable)
- `~/workspace/apex-audit/.work/extract-links.py` — HTML → URL occurrences + ids
- `~/workspace/apex-audit/.work/resolve-links.py` — resolve + dedupe + blanks/anchors
- `~/workspace/apex-audit/.work/check-links.py` — polite HTTP sweep (incremental,
  resumable: /tmp/check-results.jsonl)
- `~/workspace/apex-audit/.work/check-anchors.py` — anchor verification
- `~/workspace/apex-audit/.work/apply-fixes.py` + `/tmp/fix-map.json` — exact-match
  fix applier with count validation
