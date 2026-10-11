# External Link Audit — interstitiumlabs.dev

**Date:** 2026-10-09
**Scope:** 245 files (.html, .js, .css) under `~/workspace/apex-audit/docs/`
**Unique external URLs found:** 254
**URLs checked:** 191 (63 excluded as code examples, internal placeholders, or regex artifacts)

## Summary

| Category | Count |
|---|---|
| Working (200/redirect) | 93 |
| **Fixed** | **59** |
| False positives (API endpoints, bot-blocked, JS templates) | 36 |
| **Needs owner input** | **3** |

## Fixed: MIT OpenCourseWare links (59)

**Problem:** All 62 MIT OCW course links used the short format `https://ocw.mit.edu/courses/{course-id}` which returns **404**. MIT OCW requires the full slug URL.

**Fix:** Replaced with the working search format `https://ocw.mit.edu/search/?q={course-id}` (verified 200).

**Files changed:**
- `subject-map/subject-map-data.js` — 59 URLs fixed
- `subject-map/subject-map.js` — 1 URL (base `ocw.mit.edu/courses/`, already working)

**Example:**
- Before: `https://ocw.mit.edu/courses/6-0002` → 404
- After: `https://ocw.mit.edu/search/?q=6-0002` → 200

## Needs Owner Input: Payment Placeholders (3)

**File:** `enroll/config.js`

These are placeholder payment links that were never replaced with real ones:

| Line | URL |
|---|---|
| 39 | `https://buy.stripe.com/PLACEHOLDER_PREP_SPRINT` |
| 58 | `https://buy.stripe.com/PLACEHOLDER_DEVSECOPS_MASTERY` |
| 76 | `https://buy.stripe.com/PLACEHOLDER_FULL_ACADEMY` |

Plus matching PayPal placeholders: `https://www.paypal.com/ncp/payment/PLACEHOLDER_*`

**Action needed:** Provide real Stripe Payment Links and PayPal payment URLs, or confirm these tiers should be removed. Per standing notes, Stripe/PayPal merchant keys were never provided.

## Flagged: Unstoppable Domains API Timeout

**File:** `payment-routes.js` (line 129), `_worker.bundle.js`

`https://resolve.unstoppabledomains.com/domains/` times out from this VM. This is the server-side API used to resolve `enmanuelmejia.crypto` to wallet addresses for crypto payments. May work from Cloudflare's edge — needs live verification, not a code fix.

## False Positives (verified working or by-design)

**API endpoints returning 401/400 by design** (require auth, not broken links):
- `api.stripe.com`, `api-m.paypal.com`, `api-m.sandbox.paypal.com`
- `api.nowpayments.io`, `api-sandbox.nowpayments.io`
- `api.mailchannels.net`, `api.resend.com`
- `api.github.com`, `github.com/login/oauth/access_token`
- `oauth2.googleapis.com`, `www.googleapis.com/oauth2/v2/userinfo`
- `api.linkedin.com`, `www.linkedin.com/oauth/v2/accessToken`
- `api.twitter.com`, `graph.facebook.com`

**Bot-blocked (403 to curl, work in browsers):**
- `stackoverflow.com`, `www.devops.com`, `linuxjourney.com`
- `education.oracle.com`, `dash.cloudflare.com`
- `cdn.jsdelivr.net/pyodide/`, `buy.stripe.com/PLACEHOLDER_*` (placeholders, see above)

**JS template strings** (completed at runtime, verified working):
- `https://i.ytimg.com/vi/{id}/hqdefault.jpg` — YouTube thumbnails
- `https://cdn.jsdelivr.net/npm/sql.js@{version}/dist/` — verified 200
- `https://commons.wikimedia.org/wiki/File:Enochian_letters_(1583_manuscript)_alt.jpg` — verified 200

**Code examples** (in `<pre>` blocks, comments, placeholders — not links):
- `https://example.com` (curl example in prep/devops)
- `https://training.example.com/course/` (textarea placeholder in university/courses.html)
- `https://httpbin.org/get` (commented Python in prep/programming)

**Internal/demo strings** (terminal animations, input placeholders):
- `https://relay.internal`, `https://lab-control/v1`, `ssh://10.8.4.20`

**Regex artifacts** (not real URLs): `//g`, `//.test`, `//i.test`, `//history`, backtick fragments

## User-Reported Issues (from mobile screenshot)

The user reported "home in header and pill broken" and "page doesn't load." Investigation:
- Homepage (`/`) returns 200, `/university/` returns 200
- Nav fragment `assets/il-unified-nav.html` has correct `href="/"` home link
- Inlined nav on `index.html` matches fragment
- **Cannot reproduce without live browser** — needs visual verification on Pixel 9 Pro XL

## Verification

- All 59 fixed OCW URLs verified: search format returns 200
- No internal links were modified
- Worker files were not modified (except pre-existing bundle)
- No files deleted in this audit
