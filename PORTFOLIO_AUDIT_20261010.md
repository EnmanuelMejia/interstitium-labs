# Portfolio Audit — 2026-10-10

**Site:** https://enmanueldmejia.com/
**Date:** 2026-10-10 ~12:40 EDT
**Method:** Fetched live HTML, extracted 48 unique URLs (href/src/data-src/poster), checked each with curl (follow redirects, 15s timeout).

## Summary

| Category | Checked | Working (200) | Broken | Unverifiable |
|---|---|---|---|---|
| Total URLs | 48 | 46 | 1 | 1 |
| Videos (MP4) | 11 | 11 | 0 | 0 |
| Posters (PNG) | 11 | 11 | 0 | 0 |
| Page links (interstitiumlabs.dev) | 19 | 18 | 1 | 0 |
| GitHub links | 7 | 7 | 0 | 0 |
| LinkedIn | 1 | 0 | 0 | 1 (bot-blocked) |

## Broken URLs

| URL | Status | Used by | Expected behavior | Fix |
|---|---|---|---|---|
| https://interstitiumlabs.dev/labs/ | 404 | "Visual Library — Byte-Sized Animated Guides" card ("Try it live" link) | Per CONSOLIDATION_PLAN.md, `/labs/` should 301-redirect to `/prep/drills/` | Add worker redirect: `/labs` and `/labs/` → `/prep/drills/` (same as the other retired paths like `/cinema/`, `/cards/`, `/trending/`, `/library/`). Verify `/prep/drills/` returns 200 (confirmed). |

## Unverifiable

| URL | Status | Note |
|---|---|---|
| https://www.linkedin.com/in/enmanuelmejia | 999 | LinkedIn blocks automated checks. Manually verified pattern — profile URL is correct format. |

## Video inventory (all healthy)

| Video | Status | Size | Content-Type |
|---|---|---|---|
| hq-ai-vision_16x9.mp4 | 200 | 6,085,303 B (5.8 MB) | video/mp4 |
| hq-catalog_16x9.mp4 | 200 | 4,792,774 B (4.6 MB) | video/mp4 |
| hq-il19_16x9.mp4 | 200 | 5,101,919 B (4.9 MB) | video/mp4 |
| hq-il26_16x9.mp4 | 200 | 4,701,008 B (4.5 MB) | video/mp4 |
| hq-il28_16x9.mp4 | 200 | 4,359,122 B (4.2 MB) | video/mp4 |
| hq-il29_16x9.mp4 | 200 | 6,163,525 B (5.9 MB) | video/mp4 |
| hq-lps_16x9.mp4 | 200 | 4,903,880 B (4.7 MB) | video/mp4 |
| hq-rhel_16x9.mp4 | 200 | 5,772,802 B (5.5 MB) | video/mp4 |
| hq-superlab_16x9.mp4 | 200 | 5,648,899 B (5.4 MB) | video/mp4 |
| hq-tl-assessment_16x9.mp4 | 200 | 8,159,126 B (7.8 MB) | video/mp4 |
| hq-tl-interview_16x9.mp4 | 200 | 8,788,175 B (8.4 MB) | video/mp4 |

All 11 poster PNGs also return 200 with `image/png` content-type and non-zero sizes (1.2–1.8 MB each).

## "Try it live" link verification

| Card | Link | Status |
|---|---|---|
| Interstitium Labs | https://interstitiumlabs.dev/ | 200 |
| IL-26 | /university/course?course=il-26-... | 200 |
| IL-28 | /university/course?course=il-28-... | 200 |
| IL-29 | /university/course?course=il-29-... | 200 |
| IL-19 | /university/course?course=il-19-... | 200 |
| DevOps SuperLab | (GitHub link) | 200 |
| RHEL AI & Systems Fabric | /rhel-fabric/ | 200 |
| Certification Bootcamp Catalog | /bootcamp-catalog/ | 200 |
| ThreatLocker Interview Test Bootcamp | /bootcamps/tl-interview/ | 200 (restored) |
| ThreatLocker Assessment Prep CBT | /bootcamps/threatlocker-assessment-prep/ | 200 |
| AI Vision Deck | (GitHub link) | 200 |
| LPS Enrollment Analysis | (GitHub link) | 200 |
| Visual Library | /labs/ | **404 BROKEN** |

## Notes

- The tl-interview card video and link (restored 2026-10-10 per user order) are fully functional.
- No wrong content-types detected (no video URL returning HTML, no image URL returning wrong type).
- No unexpected redirects detected (only expected: `/university/il-26-dossier.html` → `/university/il-26-dossier` 301, which resolves to 200).
- The `/labs/` 404 is the only broken item. It affects the "Visual Library" card. The consolidation plan (Phase 2, 2026-10-09) intended `/labs/` → `/prep/drills/` as a 301, but the redirect was never added to the worker (unlike `/cinema/`, `/cards/`, `/trending/`, `/library/` which were done).

## Recommended fix

Add to `_worker.js` alongside the other consolidation redirects:
```js
if (path === "/labs" || path === "/labs/") {
  return movedPermanently(request, "/prep/drills/");
}
```
Then rebuild bundle, redeploy, and verify with curl.
