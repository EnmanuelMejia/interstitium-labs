# SEO Audit — 2026-10-08

**Scope:** 17 pages across 4 hosts. Live fetch (normal UA + `LinkedInBot/1.0` crawler UA on course pages). Repo: `~/workspace/apex-audit` (source in `docs/`). Audit only — no code changed.

**Method:** `seo_audit_run.py` (in this dir) fetched each page, parsed `<head>`, verified every `og:image` URL returns HTTP 200, checked `robots.txt` + `sitemap.xml` per host. Raw data: `seo_results.json`.

---

## Per-page results

| URL | <title> | meta description | OG (title/desc/image/url/type) | canonical | Issues |
|---|---|---|---|---|---|
| https://interstitiumlabs.dev/ | Interstitium Labs — The Learning OS for unusually ambitious builders ✓ | ✓ (169 chars, slightly long) | ✓ all 5; og:image → 200 | https://interstitiumlabs.dev/ ✓ absolute | No twitter tags at all (gap) |
| https://interstitiumlabs.dev/about/ | About — Interstitium Labs ✓ | ✓ (110) | ✓ all 5; og:image → 200 | https://interstitiumlabs.dev/about/ ✓ | twitter:card only — missing twitter:title/description/image (gap) |
| https://interstitiumlabs.dev/founders/ | Founders · Student Zero Learning OS — Interstitium Labs ✓ | ✓ (139) | ✓ all 5; og:image → 200 | https://interstitiumlabs.dev/founders/ ✓ | twitter:card + twitter:image only — missing twitter:title/description (gap) |
| https://interstitiumlabs.dev/university/ | Interstitium Labs — Knowledge Operating System ✓ | ✓ (129) | ✓ all 5; og:image `sigil-hero-static.png` → 200 | https://interstitiumlabs.dev/university/ ✓ | Full twitter set ✓ — no issues |
| https://interstitiumlabs.dev/university/course?course=il-29-… (normal UA) | **Course · Interstitium Labs** — boilerplate, same for every course | **Boilerplate** "Interstitium Labs course shell — SCIENTIA OMNIA VINCIT" (54) | ✓ injected, course-specific; og:image `il-29-threatlocker-og.png` → 200; og:url host-correct | **MISSING** — no canonical tag | Boilerplate title/description; missing canonical |
| https://interstitiumlabs.dev/university/course?course=il-29-… (LinkedInBot) | Same as normal UA | Same as normal UA | Same as normal UA (full injected set + full twitter set) | **MISSING** | Identical to normal UA — edge injection works for crawlers ✓, but no canonical |
| https://learn.interstitiumlabs.dev/ | Interstitium Labs — The Learning OS… ✓ (identical to flagship) | ✓ (169) | ✓; og:image → 200 | **https://interstitiumlabs.dev/** — cross-host canonical | Canonical + og:url point to flagship host (see Finding A); no twitter tags |
| https://learn.interstitiumlabs.dev/about/ | About — Interstitium Labs ✓ (identical to flagship) | ✓ (110) | ✓; og:image → 200 | **https://interstitiumlabs.dev/about/** — cross-host | Canonical + og:url point to flagship host; twitter:card only |
| https://learn.interstitiumlabs.dev/university/course?course=il-29-… (both UAs) | Course · Interstitium Labs (boilerplate) | Boilerplate shell text (54) | ✓ injected, course-specific; og:image → 200; og:url = **learn-host URL** (worker builds from request origin ✓) | **MISSING** | Boilerplate title/description; missing canonical |
| https://learn.interstitiumlabs.dev/university/academy | Academy — Interstitium Labs ✓ | ✓ (91) | ✓; og:image → 200; **og:url = https://interstitiumlabs.dev/university/academy.html** | **https://interstitiumlabs.dev/university/academy.html** | Cross-host canonical; canonical points at the `.html` URL which 307-redirects to the fetched extensionless URL (mismatch); og:title is generic "Interstitium Labs — Learning University" (boilerplate, doesn't match page title) |
| https://enmanueldmejia.com/ | Enmanuel D. Mejia \| Cloud, DevOps & DevSecOps Portfolio ✓ | ✓ (161, slightly long) | ✓ all + og:image:* dims/alt; og:image → 200 | `/` — **relative**, resolves to homepage | Relative canonical (gap); full twitter set ✓ |
| https://enmanueldmejia.com/about/ | **DUPLICATE** — identical to homepage title | **DUPLICATE** — identical to homepage | Identical to homepage; og:url = homepage | `/` (→ homepage) | Duplicate title/description/og:url/canonical of homepage (see Finding B) |
| https://enmanueldmejia.com/work/ | **DUPLICATE** — identical to homepage title | **DUPLICATE** — identical to homepage | Identical to homepage; og:url = homepage | `/` (→ homepage) | Duplicate of homepage (see Finding B) |
| https://enmanueldmejia.com/contact/ | **DUPLICATE** — identical to homepage title | **DUPLICATE** — identical to homepage | Identical to homepage; og:url = homepage | `/` (→ homepage) | Duplicate of homepage (see Finding B) |
| https://app.interstitiumlabs.dev/ | Identical to flagship ✓ | ✓ (169) | ✓; og:image → 200 | **https://interstitiumlabs.dev/** — cross-host | Same as learn: canonical + og:url point to flagship; no twitter tags |
| https://app.interstitiumlabs.dev/about/ | Identical to flagship ✓ | ✓ (110) | ✓; og:image → 200 | **https://interstitiumlabs.dev/about/** — cross-host | Cross-host canonical/og:url; twitter:card only |
| https://app.interstitiumlabs.dev/founders/ | Identical to flagship ✓ | ✓ (139) | ✓; og:image → 200 | **https://interstitiumlabs.dev/founders/** — cross-host | Cross-host canonical/og:url; twitter:card + image only |
| https://app.interstitiumlabs.dev/university/ | Identical to flagship ✓ | ✓ (129) | ✓; og:image → 200 | **https://interstitiumlabs.dev/university/** — cross-host | Cross-host canonical/og:url; full twitter set ✓ |

No page had a `<meta name="robots">` tag (no accidental noindex anywhere). No page had duplicate `<title>` or duplicate canonical tags.

---

## Missing-tag list (URL + tag)

1. `https://interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery` — **missing `<link rel="canonical">`** (both normal and crawler UA). Worker injects OG + twitter but no canonical.
2. `https://learn.interstitiumlabs.dev/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery` — **missing `<link rel="canonical">`** (both UAs).
3. `https://interstitiumlabs.dev/` — missing all `twitter:*` tags (gap, not bug).
4. `https://learn.interstitiumlabs.dev/`, `https://app.interstitiumlabs.dev/` — missing all `twitter:*` tags (same as flagship source).
5. `https://interstitiumlabs.dev/about/` (+ learn/app mirrors) — missing `twitter:title`, `twitter:description`, `twitter:image` (only `twitter:card` present).
6. `https://interstitiumlabs.dev/founders/` (+ learn/app mirrors) — missing `twitter:title`, `twitter:description` (only `twitter:card` + `twitter:image` present).
7. `https://enmanueldmejia.com/` (+ /about/, /work/, /contact/) — canonical is **relative** (`href="/"`) instead of absolute URL (gap; resolves correctly but best practice is absolute).

## Duplicate / boilerplate findings

- **Finding A — cross-host canonicals (learn + app):** every page on `learn.interstitiumlabs.dev` and `app.interstitiumlabs.dev` carries a hardcoded `<link rel="canonical">` and `og:url` pointing at `https://interstitiumlabs.dev/…` (confirmed in repo source `docs/*.html`). Search engines will treat both hosts as duplicates and consolidate ranking to the flagship. If learn/app are meant to be independently indexed, this is broken; if they are intentional mirrors, it is working as designed but should be a conscious decision.
- **Finding B — portfolio duplicate metadata:** `/`, `/about/`, `/work/`, `/contact/` on `enmanueldmejia.com` serve byte-identical `<title>`, meta description, `og:url` (all = homepage), and canonical `/`. Four URLs, one identity — subpages cannot rank independently and look like soft-duplicates to Google.
- **Finding C — course boilerplate:** `<title>` = "Course · Interstitium Labs" and meta description = "Interstitium Labs course shell — SCIENTIA OMNIA VINCIT" are identical for every course (only the edge-injected OG/twitter tags are course-specific). A search result for any course shows the generic shell title.
- **Finding D — academy canonical mismatch:** `https://learn.interstitiumlabs.dev/university/academy` (200) declares canonical `https://interstitiumlabs.dev/university/academy.html`, but `academy.html` 307-redirects to the extensionless URL — the canonical points at a redirecting URL on another host. Also its `og:title` ("Interstitium Labs — Learning University") is boilerplate that doesn't match the page `<title>` ("Academy — Interstitium Labs").

## robots.txt / sitemap.xml per host

| Host | robots.txt | sitemap.xml |
|---|---|---|
| interstitiumlabs.dev | ✓ `User-agent: * / Allow: /`, Disallow: /brand/ /ops/ /admin/ /_imports/ /analytics/ /measure/ /academy/ /desk/; `Sitemap: https://interstitiumlabs.dev/sitemap.xml` | ✓ 120 URLs, all flagship-host, lastmod up to 2026-10-07 |
| learn.interstitiumlabs.dev | ✓ present, but `Sitemap:` line points to **https://interstitiumlabs.dev/sitemap.xml** | Serves the flagship sitemap (120 flagship URLs, zero learn-host URLs) — wrong-host sitemap |
| app.interstitiumlabs.dev | ✓ present (same as flagship) | Serves the flagship sitemap (120 flagship URLs, zero app-host URLs) — wrong-host sitemap |
| enmanueldmejia.com | ✓ present, incl. explicit AI-crawler blocks (Amazonbot, Applebot-Extended, Bytespider, CCBot, ClaudeBot, Diffbot, Google-Extended, GPTBot, omgili…) | Exists but **thin: only the homepage URL** — `/about/`, `/work/`, `/contact/` (all 200) are not listed |

## Notes

- **Course OG injection (crawler UA) works:** `curl -A "LinkedInBot/1.0"` on both hosts' `/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery` returns the worker-injected per-course `og:title`/`og:description`/`og:image` (→ 200)/`og:url`/`og:type`/`og:site_name` plus full twitter-card set. Normal UA returns byte-identical tags (IL-29 is free/open, not in the worker's `GATED_COURSE_SLUGS`, so no paywall divergence for this course).
- All `og:image` URLs verified HTTP 200: `/og.jpg`, `/university/og/il-29-threatlocker-og.png`, `/university/assets/sigil-hero-static.png`, portfolio `og-enmanuel-d-mejia.7f099d3e90.jpg`.
- Meta descriptions run 169 chars (flagship/learn/app homepages) and 161 chars (portfolio) — slightly over the ~155–160 display truncation point; minor.
- `/university/academy.html` → 307 → `/university/academy` (200) on learn; flagship `/university/academy` → 200 directly.
- Sites were intermittently slow during the audit (several 45s+ fetches); two initial fetches timed out and succeeded on retry — flakiness, not findings.

---

## Summary

1. **17 pages audited across 4 hosts (all HTTP 200): titles present and unique within each host, meta descriptions present on every page, all og:image URLs return 200, no missing og:title/og:description/og:url/og:type, no duplicate title/canonical tags, no rogue noindex.**
2. **Top structural issue:** every page on `learn.interstitiumlabs.dev` and `app.interstitiumlabs.dev` hardcodes canonical + og:url to `interstitiumlabs.dev`, so both hosts read as duplicates of the flagship to search engines; their robots.txt/sitemap.xml also serve the flagship's sitemap (zero learn/app URLs).
3. **Top content issue:** all four `enmanueldmejia.com` pages (`/`, `/about/`, `/work/`, `/contact/`) share identical title, description, og:url and a relative canonical — subpages are invisible as distinct pages; plus its sitemap.xml lists only the homepage.
4. **Course pages:** edge OG injection verified working for crawler UA on both hosts (course-specific tags, images 200, host-correct og:url), but both course URLs lack `<link rel="canonical">` and keep boilerplate `<title>`/meta description ("Course · Interstitium Labs").
5. **Twitter cards are the consistent gap:** homepage (all 3 IL hosts) has no twitter tags; `/about/` has only `twitter:card`; `/founders/` has card+image but no title/description — while `/university/`, course pages, and the portfolio have full sets.
