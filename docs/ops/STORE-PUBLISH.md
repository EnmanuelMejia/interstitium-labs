# Store publish path — Interstitium Labs

**Bundle ID (all platforms):** `dev.interstitiumlabs.app`  
**App name:** Interstitium Labs  
**Primary surface:** Learning OS via Capacitor → `docs/`  
**Default native shell:** **Lab Muse** (`/coach/`) — Muse-class companion shell (Interstitium brand: cyan/gold/void + lockup + Dee monas avatar; not Meta)  

Scaffold and CI notes live in-repo. **Enmanuel must complete Apple Developer + Google Play Console account steps** — agents cannot finish store submission without those accounts.

---

## What is already scaffolded

| Item | Location |
| --- | --- |
| Capacitor 6+ project | `apps/mobile/` |
| Sync `docs/` → `www/` | `scripts/sync-mobile-web.sh` |
| Security threat model | [MOBILE-SECURITY.md](./MOBILE-SECURITY.md) |
| Android network security sample | `apps/mobile/android-security/` |
| Optional Android debug APK CI | `.github/workflows/mobile-android-debug.yml` |
| PWA (installable web) | `docs/manifest.webmanifest`, `docs/sw.js` |
| Lab Muse mobile shell | `docs/assets/il-muse-mobile.css`, Dee avatar, Capacitor home → `/coach/` |

**Not completable without Enmanuel:** paid Apple Developer Program, Google Play Console developer registration, store listing privacy forms, production signing secrets, final binary upload.

---

## Bundle identifiers

| Platform | ID |
| --- | --- |
| iOS / Android / future desktop | `dev.interstitiumlabs.app` |
| URL / App Links host | `interstitiumlabs.dev` |
| Optional custom scheme (later) | `interstitiumlabs://` — disabled until verified |

---

## A. Apple App Store (Enmanuel)

1. Enroll in [Apple Developer Program](https://developer.apple.com/programs/) ($99/yr) under the account that will own Interstitium Labs.
2. In App Store Connect → **My Apps** → New App:
   - Platform: iOS
   - Name: Interstitium Labs
   - Bundle ID: register `dev.interstitiumlabs.app`
   - SKU: e.g. `il-learning-os-ios`
3. **Certificates & Profiles** (Xcode or Certificates portal):
   - Apple Distribution certificate
   - App Store provisioning profile for `dev.interstitiumlabs.app`
4. Privacy / App Privacy (“nutrition labels”):
   - Disclose first-party analytics if enabled
   - Do **not** claim push or account data until those features ship
   - Payments: Stripe/PayPal hosted checkout — describe as linking out / purchase off-app if applicable
5. Build on **macOS** with Xcode:
   ```bash
   ./scripts/sync-mobile-web.sh
   cd apps/mobile && npm ci && npx cap sync ios
   npx cap open ios
   ```
   Archive → Distribute → App Store Connect.
6. Screenshots (required device sizes — check current ASC matrix):
   - Lab Muse companion (full-bleed chat, Dee avatar, bottom nav) — Muse-class shell
   - Home / hero with Interstitium lockup + sigil
   - Founders Learning OS
   - Learn / Prep / Play
   - Dark void `#070B16` chrome with cyan/gold accents (not Meta purple)
7. Submit for review. iOS **cannot** be archived on this Linux CI box — document only.

### App Transport Security reminder

Keep ATS strict (`NSAllowsArbitraryLoads` = false). See MOBILE-SECURITY.md.

---

## B. Google Play Console (Enmanuel)

1. Register [Google Play Console](https://play.google.com/console/) (one-time developer fee).
2. Create app: **Interstitium Labs**, package `dev.interstitiumlabs.app`.
3. **Data safety** form:
   - Local progress / XP in WebView storage — disclose as app activity / app info if collected
   - No third-party ad trackers by default
   - No push until `IL_FEATURE_PUSH` is enabled with real FCM
4. **Signing:**
   - Generate upload keystore **locally** (never commit):
     ```bash
     keytool -genkey -v -keystore il-upload.jks -keyalg RSA -keysize 2048 -validity 10000 -alias il-upload
     ```
   - Opt in to Play App Signing
   - Store passwords in a password manager; CI secret if automating release
5. Build AAB (preferred) or APK:
   ```bash
   ./scripts/sync-mobile-web.sh
   cd apps/mobile && npm ci && npx cap sync android
   cd android && ./gradlew bundleRelease   # after signing config
   ```
6. Store listing: short/full description, feature graphic, screenshots (phone + 7" / 10" tablet as required).
7. Content rating questionnaire; target audience (learning / education — not children’s app unless COPPA reviewed).
8. Roll out internal testing → closed → production.

### Cleartext / Network Security

Confirm release manifest has cleartext disabled and merges `android-security/network_security_config.xml`.

---

## C. Screenshots checklist (both stores)

- [ ] Void background `#070B16`, cyan `#5eead4`, gold accents — matches brand
- [ ] Sigil splash or hero visible
- [ ] Founders OS (skills / weekly / proof wall)
- [ ] Learn hub
- [ ] Prep or Paths
- [ ] Play / gamification HUD if shipping
- [ ] No placeholder “Grok App” branding
- [ ] No secrets or admin-only URLs in frames

---

## D. Desktop / PWA (equal capability path)

| Channel | Status | Notes |
| --- | --- | --- |
| **PWA** | Ship with site | `manifest.webmanifest` + `sw.js` — installable from browser |
| **Capacitor desktop** | Later | Same `apps/mobile` webDir; evaluate Capacitor for Electron-like targets when needed |
| **Electron / Tauri** | Documented option | Prefer Tauri for smaller rust shell **or** Electron if team prefers JS — wrap same `docs/` sync; apply same HTTPS / no-secrets rules |

Equal capability means **same Learning OS**, not three different products.

---

## E. CI reality

| Job | Feasible here |
| --- | --- |
| Sync www + `npm ci` | Yes |
| Android **debug** APK artifact | Often yes (Linux + Android SDK in Actions) |
| Android **release** signed AAB | Needs Enmanuel’s keystore secrets |
| iOS Archive | Needs macOS runner + Apple creds — **out of scope for Linux agents** |

See `.github/workflows/mobile-android-debug.yml`.

---

## F. Pre-submit security gate

Before any store binary:

1. Read [MOBILE-SECURITY.md](./MOBILE-SECURITY.md)
2. `cd apps/mobile && npm audit`
3. Confirm no keystores / `google-services.json` / `.p8` in git status
4. Confirm `IL_FEATURE_PUSH` and `IL_FEATURE_BIOMETRIC_LOCK` remain false unless auth+privacy ready
5. Smoke-test allowNavigation: only `interstitiumlabs.dev` (+ localhost debug)

---

## Muse-class companion shell

Native and PWA coach experience mirrors public Muse *interaction* patterns (chat-first, thumb mic/speak, drawers) under **Interstitium** brand only:

- Product name: **Lab Muse** / Interstitium Labs
- Tokens: void `#070B16`, cyan `#5EEAD4`, gold `#D4A853`
- Lockup: canonical Interstitium (56–80px industry scale) — not Meta logo
- Avatar: original Dee / Monas Hieroglyphica–inspired SVG (`assets/il-muse-avatar-dee.svg`) with status glows

## Operator contacts

- Domain / Pages: Cloudflare Workers Assets → `interstitiumlabs.dev`
- Repo: https://github.com/EnmanuelMejia/interstitium-labs
- Owner steps above: **Enmanuel D. Mejia**
