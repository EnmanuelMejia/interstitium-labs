# Zero-Trust Security Hardening Report
**Date:** 2026-10-09 ~06:36 EDT
**Order:** "Harden all GitHub and Cloudflare security, advanced settings, configs to zero trust and Palantir enterprise grade flawless standards"
**Scope:** github.com/EnmanuelMejia (19 repos) + Cloudflare zones interstitiumlabs.dev & enmanueldmejia.com

---

## GITHUB HARDENING — 18/18 repos ✅

All repos except `threatlocker-interview-test-bootcamp` (empty, no branch, being deleted by sibling task).

### Applied to every repo (verified persisted via API re-check)

| Control | Setting | Status |
|---------|---------|--------|
| Branch protection (main) | Require 1 PR approver, dismiss stale reviews | ✅ Applied |
| Branch protection (main) | Enforce on administrators | ✅ Applied |
| Branch protection (main) | Block force pushes | ✅ Applied |
| Branch protection (main) | Block branch deletion | ✅ Applied |
| Branch protection (main) | Require conversation resolution | ✅ Applied |
| Required signed commits | `required_signatures` on main | ✅ Applied |
| Secret scanning | `enabled` | ✅ Applied |
| Push protection | `enabled` | ✅ Applied |
| Dependabot alerts | `vulnerability-alerts` enabled | ✅ Applied |
| Dependabot security updates | `automated-security-fixes` enabled | ✅ Applied |
| Private vulnerability reporting | `enabled` | ✅ Applied |
| SECURITY.md | Disclosure policy committed to main | ✅ Added (18 repos) |

### Implementation notes
- First pass had a payload bug (`dismissal_restrictions: {}` caused 422 on the branch protection PUT; error was masked by a faulty success check). Root-caused via manual API test, rewrote with fixed error detection, re-applied cleanly — **18/18 repos, 0 failures** on second pass.
- Verified live on `interstitium-labs`: protection object returns correct values, secret scanning + push protection show `enabled`, private vuln reporting shows `enabled: true`, SECURITY.md present (673 bytes).

### Account-level (cannot enforce via API — MANUAL ACTION NEEDED)
- **2FA status:** API returned `null` (indeterminate). **User must verify 2FA is enabled** at github.com/settings/security.
- **SSH keys:** Cannot list — `gh` token lacks `admin:public_key` scope. **User should audit** at github.com/settings/keys and remove stale keys.
- **GPG keys:** Cannot list — `gh` token lacks `admin:gpg_key` scope. **User should audit** at github.com/settings/keys. Note: signed commits are now *required* on all repos, so a GPG/SSH signing key must be configured or pushes will fail.

### ⚠️ OPERATIONAL IMPACT
**Signed commits are now REQUIRED on all 18 repos.** Any push of unsigned commits to `main` will be rejected. The user must configure commit signing (GPG or SSH) in their git client before the next push, or use GitHub's web UI (which signs automatically).

---

## CLOUDFLARE HARDENING — both zones ✅

### interstitiumlabs.dev (`3f705489afbb4d6ed20b777e2d027047`)

| Control | Before | After | Verified |
|---------|--------|-------|----------|
| SSL mode | strict | strict (no change needed) | ✅ |
| Min TLS | 1.2 | 1.2 (no change needed) | ✅ |
| Security level | medium | medium (no change needed) | ✅ |
| Always HTTPS | on | on (no change needed) | ✅ |
| Security headers (Transform Rules) | Ruleset existed, **0 rules** | 6 headers added | ✅ Live (curl verified) |
| Rate limiting | none | 1 rule: 20 req/10s per IP on `/api/*` | ✅ Active |
| Managed WAF | 31 block rules | 31 block rules (no change) | ✅ Active |
| DDoS L7 | present | present (no change) | ✅ |
| Bot Fight Mode | off | **FAILED** — 405, token scope insufficient | ❌ Manual |

### enmanueldmejia.com (`c17e24dfb06602421aefb6d8e88e60c2`)

| Control | Before | After | Verified |
|---------|--------|-------|----------|
| SSL mode | strict (fixed in prior audit) | strict | ✅ |
| Min TLS | 1.2 (fixed in prior audit) | 1.2 | ✅ |
| Security level | medium | medium | ✅ |
| Always HTTPS | on | on | ✅ |
| Security headers (Transform Rules) | **no ruleset** | New "Security Headers" ruleset, 6 headers | ✅ Live (curl verified) |
| Rate limiting | none | 1 rule: 20 req/10s per IP on `/api/*` | ✅ Active |
| Managed WAF | 31 block rules | 31 block rules (no change) | ✅ Active |
| DDoS L7 | present | present (no change) | ✅ |
| Bot Fight Mode | off | **FAILED** — 405, token scope insufficient | ❌ Manual |

### Security headers now served (verified via curl on both domains)
- `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), geolocation=(), microphone=(self)` (mic allowed for Noah voice chat)
- `Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; style-src 'self' 'unsafe-inline' https:; img-src 'self' data: https: blob:; font-src 'self' data: https:; connect-src 'self' https: wss:; media-src 'self' https: blob:; object-src 'none'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'`

CSP is intentionally permissive on `script-src` (`unsafe-inline`/`unsafe-eval` + https:) because the site architecture is inline-heavy; the meaningful restrictions are `frame-ancestors 'none'` (clickjacking), `object-src 'none'`, `base-uri`/`form-action` scoping. Both sites return HTTP 200 with the new headers — no breakage.

### Free-plan constraints discovered (documented, not failures)
- **Rate limiting:** free plan allows max 1 rule per zone, period=10s only, mitigation_timeout=10s only. Applied: single `/api/*` rule at 20 req/10s per IP+colo.
- **Bot Fight Mode:** cannot enable via account API token (405 "Method not allowed for this authentication scheme"; legacy setting endpoint returns 400 "Unrecognized zone setting name"). **Requires dashboard access.**
- **WAF custom rules:** not available on free plan; the Cloudflare Managed Free Ruleset (31 block rules incl. Log4j, Shellshock, SQLi, XSS patterns) is active and is the WAF coverage.
- **Zero Trust / Cloudflare Access:** not configured; no admin paths identified that need Access policies (Workers serve public content; no admin dashboard on the zones).

### Manual actions needed (Cloudflare)
1. **Enable Bot Fight Mode** in dashboard: Security → Bots → Configure Bot Fight Mode → On (both zones).
2. Optional: Cloudflare Access policies if any admin-only paths are added later.

---

## SUMMARY

| Platform | Controls applied | Verified | Manual actions |
|----------|----------------|----------|----------------|
| GitHub (18 repos) | 12 controls × 18 repos = 216 settings | ✅ API re-check | 2FA verify, SSH/GPG key audit, configure commit signing |
| Cloudflare (2 zones) | Security headers, rate limiting | ✅ curl + API re-check | Bot Fight Mode (dashboard) |

**No shortcuts taken.** Every change was applied via API and verified persisted via independent re-check (not inferred from HTTP 200 on the apply call).
