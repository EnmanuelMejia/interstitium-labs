# Media Audit — 2026-10-09

## Summary
- **Total files checked:** 88 (75 videos + 13 images)
- **Broken:** 0
- **Fixed:** 1 root cause (already deployed by parent)

## Videos (75 total)

| Location | Count | Status |
|----------|-------|--------|
| `/assets/cards/hq/*.mp4` | 22 | All OK |
| `/assets/topics/*.mp4` | 24 | All OK |
| `/assets/cinematic/**/*.mp4` | 29 | All OK |

Every video verified:
- ✅ Exists locally in `~/workspace/apex-audit/docs/assets/`
- ✅ Returns HTTP 200
- ✅ Content-Type: `video/mp4`
- ✅ ffprobe validates (not corrupted)
- ✅ `Cross-Origin-Resource-Policy: cross-origin`
- ✅ `Access-Control-Allow-Origin: *`

## Images (13 total)

All 12 poster PNGs (`*_poster.png`) + `hq-il19_linkedin.png`:
- ✅ Exist locally, valid PNG format
- ✅ Return HTTP 200 with `image/png`
- ✅ Correct CORS headers

## Root Cause of Portfolio Breakage

The portfolio videos were blocked by `Cross-Origin-Resource-Policy: same-origin` — a security header that told browsers to refuse cross-origin embedding. The portfolio (enmanueldmejia.com) loads videos from interstitiumlabs.dev, so the browser blocked them.

**Fix deployed:** `/assets/*` now serves `Cross-Origin-Resource-Policy: cross-origin` + `Access-Control-Allow-Origin: *`. Range requests also pass through unwrapped for video seeking.

## False Alarm: 403s During Audit

Rapid sequential requests triggered Cloudflare rate limiting (403). Retrying with delays returned 200. Not a real failure.

## Portfolio Local Media

`~/workspace/portfolio-site/media/videos/` contains local .mp4 files but `index.html` doesn't reference them — it uses interstitiumlabs.dev URLs. Unused locals, no action needed.

## Remaining

None. All media serves correctly with proper headers. If videos still don't play on the portfolio, hard-refresh to clear browser cache.
