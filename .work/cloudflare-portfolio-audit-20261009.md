# Cloudflare Portfolio Audit — enmanueldmejia.com
Date: 2026-10-09 ~06:30 EDT
Zone ID: c17e24dfb06602421aefb6d8e88e60c2 (active)
Worker: enmanuel-mejia (modified 2026-10-09T07:35:13Z)

## Baseline comparison: interstitiumlabs.dev
- ssl: strict (Full Strict) | min_tls: 1.2 | security_level: medium
- (Note: interstitiumlabs.dev minify also reports all-off via API — Auto Minify is deprecated by Cloudflare; not actionable)

## Findings & Fixes

### 1. DNS — OK
- AAAA enmanueldmejia.com -> 100:: (proxied)
- AAAA www.enmanueldmejia.com -> 100:: (proxied)
- 100:: is Cloudflare's placeholder for proxied records. IPv6-only origin behind proxy is fine.

### 2. Worker attachment — OK (custom domains, no root route needed)
- enmanuel-mejia attached via custom domains: enmanueldmejia.com + www.enmanueldmejia.com
- Zone routes only cover gateway paths (/assessments/*, /bootcamps/*, /bootcamp/*, threatlocker-assessment-prep/*) -> interstitium-course-gateway — correct, no conflict with root.
- Worker settings: compatibility_date 2026-09-25, standard usage model, no bindings (correct for static portfolio).

### 3. SSL/TLS — FIXED
- ssl was `full` -> set to `strict` (Full Strict). Verified persisted.
- min_tls_version was `1.0` -> set to `1.2`. Verified persisted.
- always_use_https: on. automatic_https_rewrites: on.

### 4. Cache — OK
- cache_level: aggressive. No page rules (0). Static portfolio behind aggressive caching is correct.

### 5. Security — OK
- security_level: medium (matches flagship).
- bot_management: fight_mode False, enable_js True (free-plan defaults).
- WAF: Cloudflare Managed Free Ruleset, Normalization, DDoS L7, rate-limit ruleset all present.

### 6. Performance — OK
- brotli: on. early_hints: on. http2: on. http3: on.
- minify: all off via API — same as flagship zone; Cloudflare deprecated Auto Minify, not actionable.

### 7. Live verification
- https://enmanueldmejia.com/ -> 200
- https://www.enmanueldmejia.com/ -> 200

## Open / not changed
- No WAF custom rules (free plan; static portfolio, low risk).
- Worker version current as of this morning's deploy; no redeploy needed.
