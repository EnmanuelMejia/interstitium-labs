# Mobile security — Interstitium Labs

**Audience:** operators shipping Capacitor shells (`apps/mobile`) and the PWA under `docs/`  
**Domain:** `interstitiumlabs.dev`  
**Alignment:** OWASP MASVS (Mobile Application Security Verification Standard) — L1 baseline + selected L2 controls where they apply to a hybrid WebView shell.

This document is the **threat model and control catalog**. Implement controls in native config before store submission. Never weaken them for convenience.

---

## 1. Assets & trust boundaries

| Asset | Sensitivity | Where it lives |
| --- | --- | --- |
| Learning OS static content | Public | `docs/` → bundled `www/` + HTTPS origin |
| Local XP / progress (`il.game.v1`) | Low (integrity preferred) | WebView `localStorage` / Preferences |
| Enroll Payment Link URLs | Public placeholders only | `docs/enroll/config.js` |
| Stripe / PayPal **secret** keys | Critical — **must not exist in client** | Cloudflare secrets / operator vault only |
| Future auth tokens / session | High | Keychain (iOS) / Keystore (Android) — never plain SharedPreferences |
| Push credentials (FCM/APNs) | High | Not present until stub is replaced; never fake keys in repo |
| Signing keystores / `.p8` / `google-services.json` | Critical | Operator machine / CI secrets — gitignored |

**Trust boundary:** Native shell (Capacitor) → WebView → first-party origin `https://interstitiumlabs.dev` (+ `http://localhost` for debug only). Anything outside that origin is untrusted.

---

## 2. Adversaries & threats (STRIDE-minded)

| Threat | Example | Control |
| --- | --- | --- |
| **Spoofing** | Deep link opens phishing HTML | Intent / universal-link allowlist; `allowNavigation` host allowlist |
| **Tampering** | Modified APK / injected JS bridge | Play App Signing; minimize plugins; no arbitrary `eval` bridges |
| **Repudiation** | Fake “enrolled” client state | Payments stay on Stripe/PayPal hosted pages; client never holds secrets |
| **Information disclosure** | Secrets in APK / repo | No secrets in client; `npm audit`; gitignore keystores |
| **Denial of service** | Offline cache poisoning | SW never caches enroll config as authoritative secrets; network-first HTML |
| **Elevation** | `file://` WebView abuse | Block `file://` navigation; HTTPS-only; cleartext disabled |

---

## 3. Control map (security-first order)

### 3.1 No secrets in repo / client (MASVS-STORAGE / MASVS-CODE)

- Stripe **Payment Links** only in `docs/enroll/config.js` (placeholders until live).
- Never commit `sk_live_`, `sk_test_`, webhook secrets, FCM server keys, APNs `.p8`, keystores, or `google-services.json` with production keys.
- See `.gitignore` entries for `*.jks`, `*.keystore`, `AuthKey_*.p8`, `google-services.json`, `GoogleService-Info.plist`.

### 3.1b Android backup

- `android:allowBackup="false"` on `<application>` (enterprise default).

### 3.2 Transport security (MASVS-NETWORK)

- **HTTPS-only** for production loads of Learning OS.
- **Android:** `android:usesCleartextTraffic="false"` + Network Security Config denying cleartext; allow `localhost` only in debug builds if needed.
- **iOS:** App Transport Security — `NSAllowsArbitraryLoads` must remain **false**. No exception domains except documented localhost for debug.
- Remote update fetches (if used) must pin or at least use TLS + integrity notes (SRI / hash check in release notes). Prefer bundling offline shell; treat remote as enhancement.

### 3.3 CSP-friendly asset loading

- Prefer same-origin assets under `/assets/`, `/assets/chrome/`.
- Third-party fonts (Google Fonts) are a known CSP friction — document any `style-src` / `font-src` exceptions; do not add trackers.
- Capacitor `server.allowNavigation` / `allowNavigation` equivalent: **only** `interstitiumlabs.dev` and localhost for development.

### 3.4 Secure storage (MASVS-STORAGE)

| Data | Allowed today | Guidance |
| --- | --- | --- |
| XP / quest HUD | `localStorage` via `il-game.js` | Non-auth; integrity not guaranteed; do not treat as proof of purchase |
| UI prefs | Capacitor Preferences OK for non-secrets | Do **not** store auth tokens in Preferences without encryption |
| Future auth | Keychain / EncryptedSharedPreferences / Keystore | Feature-flagged biometric lock stays **OFF** until auth exists |
| Analytics | First-party only (`il-analytics` / operator-controlled) | No third-party tracker SDKs in the native shell by default |

**Never** put XP or tokens in plain Android `SharedPreferences` without documenting encryption (EncryptedSharedPreferences) when sensitivity rises.

### 3.5 WebView hardening (MASVS-PLATFORM)

- `allowNavigation`: `https://interstitiumlabs.dev`, `http://localhost`, `http://127.0.0.1` (dev).
- Block `file://` and unexpected custom schemes except documented deep links.
- Minimize Capacitor plugins / JS bridge surface; each plugin is attack surface.
- Disable `setAllowFileAccess` / universal file access patterns on Android WebView where Capacitor defaults allow tightening.
- Do not enable remote debugging in release builds.

### 3.6 Deep links & intent filters

Allowlist only:

- `https://interstitiumlabs.dev/*` (App Links / Universal Links — verify `assetlinks.json` / `apple-app-site-association` before enabling `autoVerify`)
- Custom scheme (optional later): `interstitiumlabs://` — not enabled until associated domains are ready

Reject open redirects into the WebView from untrusted intents.

### 3.7 Dependencies (MASVS-CODE)

- Pin Capacitor and plugin versions in `apps/mobile/package.json`.
- Run `npm audit` in CI / before release (see `apps/mobile` scripts).
- Prefer official `@capacitor/*` packages; review new plugins for network and storage permissions.

### 3.8 Privacy & analytics (MASVS-PRIVACY)

- First-party analytics only by default.
- No Adjust / Firebase Analytics / Facebook SDK / etc. in the native shell unless explicitly approved and disclosed in store privacy forms.
- Push notifications: **stub only** until real credentials and privacy labels exist — no fake FCM keys.

### 3.9 Release signing checklist

1. Generate upload keystore **off-repo**; store password in password manager / CI secret.
2. Enable Google Play App Signing.
3. Apple: distribution cert + App Store provisioning via Enmanuel’s Apple Developer account.
4. Confirm `.gitignore` excludes keystores and cloud messaging config files.
5. Verify release build has cleartext disabled and debug bridges off.

---

## 4. Feature flags (native stubs)

| Flag | Default | Notes |
| --- | --- | --- |
| `IL_FEATURE_PUSH` | `false` | Stub API only; no FCM/APNs keys |
| `IL_FEATURE_BIOMETRIC_LOCK` | `false` | Wire plugin only behind flag; requires future auth |
| `IL_FEATURE_SHARE` | `true` | Capacitor Share for proof-wall items (no secrets) |

---

## 5. Residual risks (accepted for v1 hybrid shell)

- Client-side XP can be edited by a motivated user — acceptable for gamification, not for entitlement.
- Bundled `www/` can drift from live site — mitigate with sync script + release checklist.
- Google Fonts CDN dependency — offline / CSP tradeoff; consider self-hosting fonts in a later hardening pass.

---

## 6. Related docs

- [STORE-PUBLISH.md](./STORE-PUBLISH.md) — App Store / Play Console steps for Enmanuel
- [payments.md](./payments.md) — no secret keys in static enroll
- `apps/mobile/README.md` — Capacitor commands and platform notes
