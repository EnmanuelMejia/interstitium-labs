# TRACK 6 — PAYWALL AUDIT (2026-10-08 ~21:22–21:45 EDT)

Method: anonymous `curl` (no cookies, no credentials). No code changed, no bypass attempted.
Repo: ~/workspace/apex-audit. Worker gate logic referenced read-only from `docs/_worker.js`
(`GATED_COURSE_SLUGS`, `slugFromCourseJsonPath`) and `docs/payment-routes.js`.

## 1. Course JSON paywall — all 29 courses

Base: `https://interstitiumlabs.dev/university/data/courses/` — filenames discovered from repo.

| Course | File | Anon status | Expected |
|---|---|---|---|
| IL-01 | il-01-esoteric-foundations.json | 402 | 402 ✓ |
| IL-02 | il-02-mathematical-maturity-engine.json | 402 | 402 ✓ |
| IL-03 | il-03-programming-language-forge.json | 402 | 402 ✓ |
| IL-04 | il-04-systems-linux-windows-networks.json | 402 | 402 ✓ |
| IL-05 | il-05-cloud-devsecops-platform-sre.json | 402 | 402 ✓ |
| IL-06 | il-06-cybersecurity-secure-engineering.json | 402 | 402 ✓ |
| IL-07 | il-07-data-engineering-analytics-ai.json | 402 | 402 ✓ |
| IL-08 | il-08-algorithms-compilers-distributed-formal.json | 402 | 402 ✓ |
| IL-09 | il-09-adaptive-certification-command.json | 402 | 402 ✓ |
| IL-10 | il-10-portfolio-career-professional-practice.json | 402 | 402 ✓ |
| IL-11 | il-11-zero-trust-endpoint-defense.json | 402 | 402 ✓ |
| IL-12 | il-12-ai-engineering.json | 402 | 402 ✓ |
| IL-13 | il-13-software-engineering-interview-prep.json | 402 | 402 ✓ |
| IL-14 | il-14-sre-devops-cloud-security-interview-prep.json | 402 | 402 ✓ |
| IL-15 | il-15-data-engineering-analytics-interview-prep.json | 402 | 402 ✓ |
| IL-16 | il-16-machine-learning-ai-engineering.json | 402 | 402 ✓ |
| IL-17 | il-17-agentic-ai-engineering.json | 402 | 402 ✓ |
| IL-18 | il-18-technical-leadership-interview-prep.json | 402 | 402 ✓ |
| IL-19 | il-19-multicloud-devops-ai-bootcamp.json | 402 | 402 ✓ |
| IL-20 | il-20-mathematics.json | 402 | 402 ✓ |
| IL-21 | il-21-humanities.json | 402 | 402 ✓ |
| IL-22 | il-22-esoteric-secret-knowledge.json | 402 | 402 ✓ |
| IL-23 | il-23-frontier-knowledge.json | 402 | 402 ✓ |
| IL-24 | il-24-threatlocker-assessment-prep-cbt.json | 402 | 402 ✓ |
| IL-25 | il-25-cybersecurity-professional-certificate.json | 402 | 402 ✓ |
| IL-26 | il-26-data-analyst-certification-senior-mastery.json | 402 | 402 ✓ |
| IL-27 | il-27-it-infrastructure-specialist-threatlocker-mastery.json | 200 | 200 ✓ |
| IL-28 | il-28-devsecops-cloud-infrastructure-mastery.json | 200 | 200 ✓ |
| IL-29 | il-29-threatlocker-ai-cybersecurity-mastery.json | 200 | 200 ✓ |

Result: **29/29 match expected** (26 paid → 402, 3 free → 200). Gate list `GATED_COURSE_SLUGS`
in `docs/_worker.js:299` contains exactly IL-01..IL-26 slugs.

## 2. Story JSON paywall (3 paid + 1 free)

Base: `https://interstitiumlabs.dev/university/data/courses/stories/`

| Story file | Anon status | Expected |
|---|---|---|
| il-01-esoteric-foundations-stories.json | 402 | 402 ✓ |
| il-12-ai-engineering-stories.json | 402 | 402 ✓ |
| il-26-data-analyst-certification-senior-mastery-stories.json | 402 | 402 ✓ |
| il-27-it-infrastructure-specialist-threatlocker-mastery-stories.json | 200 | 200 ✓ |

Result: **4/4 match** — gated story JSONs 402, free-course story JSON 200.

## 3. Checkout page

- `https://interstitiumlabs.dev/enroll/checkout.html` → 307 → `https://interstitiumlabs.dev/enroll/checkout` → **200** anonymous.
- `https://interstitiumlabs.dev/university/enroll.html` → 307 → `/university/enroll` (existence confirmed; content not needed for this check).
- `https://interstitiumlabs.dev/pricing/` → **200**, page titled "Pricing moved into the Learning OS" (no prices in static HTML).
- Static HTML of the live checkout page contains **no dollar prices** — prices are injected
  client-side from `checkout.js`. Live `https://interstitiumlabs.dev/enroll/checkout.js`
  (200 anonymous) matches repo `docs/enroll/checkout.js`: **$249/course for all 26 paid
  courses (IL-01..IL-26), $999 all-access bundle**. Legacy tiers also still present in the
  live JS: Prep Sprint $149, DevSecOps Mastery $499, Full Academy $799.
- Note: actual rendered prices on screen were not verified (needs a live browser; curl can't run JS). Server-side price authority is `payment-routes.js PAYWALL_CONFIG` (not tested — would require payment attempt, out of scope).

## 4. Leak check — deep content paths under /university/data/

| URL | Anon status | Content? | Verdict |
|---|---|---|---|
| /university/data/courses/_index.json | 404 | — | OK (no such file) |
| **/university/data/courses/_il26-build/part1_modules.json** | **200** | **24,611 bytes — real paid content** (IL26-M41 "DuckDB for Analytics" module w/ summary) | **LEAK** |
| **/university/data/courses/_il26-build/module-flesh.json** | **200** | **466,558 bytes — real paid content** (IL26-M26 module patch w/ objectives) | **LEAK** |
| /university/data/courses/_il27-build/modules.json | 200 | free course (IL-27) build artifacts | OK (free lane) |
| /university/data/courses/_il29-build/_module-template.json | 200 | free course (IL-29) template | OK (free lane) |
| /university/data/courses/.resbak-20261008/ | 404 | — | OK |
| /university/data/courses/il-01-esoteric-foundations.json.bak | 404 | — | OK |

**Root cause (repo, read-only):** `slugFromCourseJsonPath` in `docs/_worker.js:376`
anchors two regexes — `^/university/data/courses/([A-Za-z0-9-]+)\.json$` and
`^/university/data/courses/stories/([A-Za-z0-9-]+)-stories\.json$`. Any nested
subdirectory (`_il26-build/`, `_il27-build/`, `_il28-build/`, `_il27-remediation/`,
`_il29-build/`) falls through the gate and serves 200 anonymously. The
`_il26-build/` directory holds real IL-26 module content (paid) — confirmed
200 anonymous with full module text, not stub data.

## 5. Academy page badges

- `https://interstitiumlabs.dev/university/academy.html` → 307 → `https://interstitiumlabs.dev/university/academy` → **200** anonymous.
- Badge logic present in the served page: `FREE_COURSE_CODES = { 'IL-27': 1, 'IL-28': 1, 'IL-29': 1 }`.
- Ternary in the course-detail CTA (`#acad-course-cta`):
  - IL-27/28/29 → `<span class="il-badge il-badge-free">FREE · open access</span>` (green).
  - all others → `<span class="il-badge il-badge-paid">` + inline lock SVG icon (gold).
- Result: **lock/free badges render per the paywall split** — free badge on IL-27/28/29,
  lock badge on paid courses IL-01..IL-26 (code-verified in served HTML; per-course
  visual render not checked — needs a live browser).

## Summary

1. Course JSONs: 29/29 correct — IL-01..IL-26 return 402 anonymous, IL-27/28/29 return 200.
2. Story JSONs: 4/4 correct — paid (IL-01, IL-12, IL-26) 402; free (IL-27) 200.
3. Checkout loads 200 anonymous at /enroll/checkout; prices are JS-injected from live checkout.js: $249/course, $999 bundle (legacy $149/$499/$799 tiers still in code).
4. **LEAK FOUND: paid IL-26 module content serves 200 anonymous** via `_il26-build/` subdir (`part1_modules.json` 24.6KB, `module-flesh.json` 466.6KB — verified real module text). Worker's paywall regex only gates top-level course/story JSONs; nested subdirs are ungated. `.bak`/`.resbak` files correctly 404.
5. Academy page badges verified in served HTML: FREE badge on IL-27/28/29, lock badge on IL-01..IL-26 — matches the paywall split.
