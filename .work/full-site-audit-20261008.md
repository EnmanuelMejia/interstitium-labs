# Full Site Audit — 2026-10-08

**Scope:** https://interstitiumlabs.dev · https://learn.interstitiumlabs.dev · https://enmanueldmejia.com · https://app.interstitiumlabs.dev · bootcamp gateway pages
**Method:** 8 parallel audit tracks (subagents), curl + repo inspection. Audit only — no code changed.
**Track reports:** `.work/audit-tracks/` (link, asset, render, consistency, seo, paywall, redirect, bootcamp-gateway)

## Executive summary

| Track | Checked | Broken/Failed | Verdict |
|---|---|---|---|
| Links | 799 (739 internal + 60 external sample) | 0 verified broken | CLEAN |
| Assets | 102 across 9 pages | 0 broken (100× 200) | CLEAN |
| Render | 8 pages, 82 JS files | 3 issues (1 high) | 1 HIGH |
| Consistency | 12 pages, 4 hosts | 5 deviation classes | NEEDS WORK |
| SEO | 17 pages, 4 hosts | 0 missing titles; structural issues | NEEDS WORK |
| Paywall | 29 course JSONs + 4 story + 7 deep probes | **1 LEAK** | **CRITICAL** |
| Redirects | 59 URLs traced | 1 dead, 20 inert | 1 HIGH |
| Bootcamp gateway | 20 URLs | 0 broken; 1 caution | CLEAN* |

## Prioritized findings (by user impact)

### P0 — CRITICAL
1. **Paywall leak: paid IL-26 module content serves 200 anonymous.** `https://interstitiumlabs.dev/university/data/courses/_il26-build/part1_modules.json` (24.6 KB, real IL26-M41 module text) and `module-flesh.json` (466.6 KB, IL26-M26 patch) return 200 with no auth. Root cause: worker paywall regex (`slugFromCourseJsonPath` in `docs/_worker.js`) only gates top-level `courses/<slug>.json` and `stories/<slug>-stories.json`; nested subdirectories fall through ungated. `.bak` files and `.resbak-20261008/` correctly 404. **Remediation:** gate the `_il26-build/` subdirectory (and audit for any other paid-content subdirs) in the worker.

### P1 — HIGH
2. **`/devops-superlab` → 404 (dead redirect).** Worker maps it 301 → `/labs/superlab/`, but the worker never fires for that path (not in `run_worker_first`) and no stub asset dir exists. Previously fixed, now dead again. **Remediation:** add to `run_worker_first` or ship a meta-refresh stub dir like the other 19.
3. **`docs/assets/il-proof.js:65` — SyntaxError** (`Unexpected identifier 's'`, unescaped apostrophe in `Noah's` inside a single-quoted string). Loaded by `docs/evidence/index.html:58`; the whole script dies at parse, so the `[data-il-proof]` widget (Download .md / Copy / Print) never mounts — JS visitors see an empty section. **Remediation:** escape as `Noah\'s`. (81 other JS files `node --check` clean.)

### P2 — MEDIUM
4. **Retired logo paths served live on every flagship page.** `/assets/chrome/sigil-glyph.svg` (nav brand + footer logo — `docs/index.html:45,461`, `course.html:29,174`, `academy.html:385`, `jobs/index.html:19,166`, `noah/index.html:21,173`), `sigil-decor.webp`, `favicon.svg`/`favicon.png`, `og.jpg` — all on the retired list in the gateway worker's `brand-logo-paths.mjs`, but the flagship worker does no edge rewriting (only the `/bootcamps/*` worker rewrites retired refs), so they reach browsers live. **Remediation:** swap to canonical `/assets/chrome/interstitium-logo.png` in flagship source (or add edge rewriting to the flagship worker).
5. **`learn.` and `app.` serve the flagship homepage byte-for-byte** (diff-identical to `/`). Needs owner confirmation of intent — if intentional, fine; if not, route properly.
6. **20 stub 301s are inert in production.** Bare slugs (`/code`, `/pricing`, …) return `307 → /slug/` then 200 + meta-refresh page — `_worker.js` STUB_REDIRECTS is dead code (no stub path in `run_worker_first`). Visitors land correctly; crawlers/API clients see no 301. **Remediation:** add stub paths to `run_worker_first` or accept meta-refresh behavior.
7. **SEO duplicate-content signals.** Every page on learn/app hardcodes canonical + og:url to `interstitiumlabs.dev` (both hosts read as flagship duplicates; their sitemaps serve zero learn/app URLs). All four portfolio pages share identical title/description/og:url/canonical — subpages invisible as distinct pages; portfolio sitemap lists only homepage. Course pages lack `<link rel="canonical">` and keep boilerplate title/description ("Course · Interstitium Labs"). Academy canonical points to a URL that 307-redirects (canonical→redirect mismatch, cross-host).
8. **Nav deviations.** jobs/ and noah/ use a different `masthead` header with 3–4 link plain nav (no pill nav). academy.html's pill nav is JS-injected only (absent for no-JS/static fetches). Homepage pillnav mislabels `/prep/drills/` as "Practice & Exams" while every other surface says "Practice".

### P3 — LOW
9. **Motto case inconsistent three ways:** uppercase `SCIENTIA OMNIA VINCIT` (flagship nav/footer), Title Case in homepage meta description, lowercase `Scientia omnia vincit` (bootcamp masthead), Title Case (portfolio).
10. **Course page (`course.html`) has no favicon link** — every other key page has one.
11. **Twitter cards spotty:** homepage (all 3 IL hosts) has no twitter tags; `/about/` has only `twitter:card`; `/founders/` has card+image but no title/description.
12. **No www→apex redirect** on interstitiumlabs.dev or enmanueldmejia.com (both serve 200 directly). http→https 301 clean on all hosts.
13. **Bootcamp engine-path fragility (caution):** `/bootcamps/threatlocker-assessment-prep/engine/style.css` (per-bootcamp path, not the shared `/bootcamps/_engine/*`) timed out on 3 of 4 probes; later probes of the known-good shared path also timed out from the audit environment, so this may be egress flakiness — re-verify from another vantage. The two free pages resolve engine assets differently (shared vs per-bootcamp) — worth normalizing.

## What's clean (verified)
- **Links:** 739 internal links, zero verified broken; 58/60 external sample OK (2 bot-blocked, couldn't-check); all 9 course URLs + both bootcamp pages 200; all 4 sitemaps healthy.
- **Assets:** 100/102 return 200 (2 are Google Fonts preconnect origins, 404 by design). All 4 of the 2026-10-08 bootcamp/brand fixes verified held anonymous: `/bootcamps/_engine/style.css` 200 (was 401), `/bootcamps/_engine/bootcamp.js` 200 (was 401), `/assets/il-brand.css` 200 (was 404), `/assets/chrome/interstitium-logo.png` 200 (was 404).
- **Paywall (beyond the leak):** 29/29 course JSONs gate correctly (IL-01..26 → 402, IL-27/28/29 → 200); 4/4 story JSONs correct; checkout loads 200 ($249/course, $999 bundle in code); academy FREE/lock badges correct.
- **Bootcamp gateway:** free pages + all 7 engine JS + CSS 200 anonymous; `/bootcamps/` index + paid paths still 401-gated (no over-opening); gateway masthead styled (not unstyled); learn host 308→200.
- **Redirects:** 0 loops, 0 timeouts, 0 external-domain redirects; `/os`, `/proof`, `/il26`–`/il29` single-hop 301→200.
- **Theme:** dark default everywhere, no light-mode defaults or `prefers-color-scheme: light` overrides. Footer byte-identical canonical across `/`, academy, jobs, noah.
- **SEO basics:** every page has non-empty unique title + meta description; all og:image URLs 200; no duplicate title/canonical tags; no rogue noindex; robots.txt on all hosts.

## Couldn't-check (needs live browser — no browser available in this audit)
- JS-rendered content: runtime-loaded JSON (`cert-index.json`, course data on academy), quiz/checkout rendered prices ($249/$999 seen in code, not rendered).
- The 8-item browser check list from the render track: `/evidence/` console error + widget; IL-29 at 390px (nav collapse, no overflow); learn/app homepage intent; course favicon; both bootcamp pages at 390px; portfolio at 390px; course page with JS disabled; screen-reader/axe on decorative alt="" images.
- Logged-in content behind `/account/` and `/admin/`; 2 bot-gated external links.

## Remediation checklist (suggested order)
1. [ ] Gate `_il26-build/` (and scan for other paid-content subdirs) in worker paywall regex — P0
2. [ ] Fix `/devops-superlab` 404 (run_worker_first or stub dir) — P1
3. [ ] Fix `il-proof.js:65` unescaped apostrophe — P1
4. [ ] Replace retired logo paths in flagship source — P2
5. [ ] Decide learn/app homepage intent — P2
6. [ ] Activate stub 301s (run_worker_first) — P2
7. [ ] SEO: learn/app canonicals, portfolio subpage tags, course canonicals — P2
8. [ ] Nav/motto/favicon/Twitter polish items — P3
