# Portfolio Link Audit — enmanueldmejia.com

**Date:** 2026-10-08 ~22:15 EDT
**Scope:** https://enmanueldmejia.com (single-page site, source: `~/workspace/portfolio-site/`)
**Method:** Extracted all `<a href>`, `<img src>`, `<script src>` from index.html; verified each with curl (status codes recorded).

## Summary

| Category | Checked | OK | Issues |
|---|---|---|---|
| Internal links | 10 | 10 | 0 |
| External links | 24 | 22 | 1 broken UX, 1 bot-blocked |
| Assets (img/js/css) | 7 | 7 | 0 |
| **Total** | **41** | **39** | **2** |

## Findings

### 1. BROKEN UX — "Explore the catalog" leads to 401 (HIGH)

- **Source page:** https://enmanueldmejia.com/ (Certification Bootcamp Catalog card)
- **Link text:** "Explore the catalog"
- **URL:** https://interstitiumlabs.dev/bootcamps/
- **Status:** **401** — returns `{"error":"sign-in-required"}`
- **Impact:** Users clicking "Explore the catalog" get a raw JSON error, not a catalog page. The bootcamp index is gated by the membership gateway.
- **Recommendation:** Either (a) link to a public catalog page, or (b) have the gateway return a friendly HTML page instead of JSON for browser visits.

### 2. LinkedIn returns 999 (EXPECTED, not broken)

- **URL:** https://www.linkedin.com/in/enmanuelmejia
- **Status:** 999 (LinkedIn bot-block)
- **Note:** LinkedIn blocks all automated curl/bot requests. The profile exists and is correct per user memory. Not a broken link.

### 3. Redirect chain (WORKING)

- **URL:** https://interstitiumlabs.dev/university/il-26-dossier.html
- **Chain:** 307 → https://interstitiumlabs.dev/university/il-26-dossier → **200**
- **Status:** Works correctly.

## Verified working

**Internal (all 200):**
- https://enmanueldmejia.com/
- /icon.webp, /manifest.webmanifest, /styles.css, /robots.txt, /sitemap.xml
- /app.js
- /assets/interstitium-sigil.e97584f2bc.webp
- /assets/enmanuel-d-mejia-portrait-720.b9eb5c2169.webp
- /assets/interstitium-labs-lockup.58aa83234a.webp
- /media/full-spectrum-og.png, /media/threatlocker-og.png

**External (all 200):**
- All 7 GitHub repos (EnmanuelMejia, ai-vision-deck-print-manufacturing, devops-superlab, interstitium-certification-bootcamps, interstitium-labs, lps-enrollment-analysis, threatlocker-assessment-prep-cbt)
- https://interstitiumlabs.dev, /about/, /founders/, /labs/, /noah/, /university/
- https://interstitiumlabs.dev/bootcamps/tl-interview/ (ThreatLocker card "Try it live")
- https://interstitiumlabs.dev/bootcamps/threatlocker-assessment-prep/
- https://interstitiumlabs.dev/evidence/withdrawn-note/
- All 3 course URLs (il-26, il-28, il-29)
- mailto:mejiaenmanueld@gmail.com (not testable via curl, format valid)

**Screenshot-specific links verified:**
- "Explore the catalog" → https://interstitiumlabs.dev/bootcamps/ → **401** (see Finding #1)
- "Source" (3 instances) → all 3 GitHub repos → **200**
- ThreatLocker Interview Test Bootcamp "Try it live" → https://interstitiumlabs.dev/bootcamps/tl-interview/ → **200**

## The user's 404 — traced

**Question:** Which portfolio link leads to "This path is not in the Learning OS"?

**Answer:** None. No link on enmanueldmejia.com returns 404.

The 404 the user encountered was `https://interstitiumlabs.dev/devops-superlab` — this URL is **not linked from the portfolio**. The parent agent identified and fixed it during this session (added to `run_worker_first`; now 301 → `/labs/superlab/`).

The portfolio's `/bootcamps/` link (Finding #1) returns 401, not the 404 page.

## Couldn't check

- mailto: link (format valid, not testable via HTTP)
- LinkedIn profile content (bot-blocked, but URL is correct per user records)
- JavaScript-rendered content (site is static HTML, no dynamic link injection found in app.js)
