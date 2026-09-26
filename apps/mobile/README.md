# Interstitium Labs — Capacitor mobile shell

**Equal capability:** iOS, Android, and (later) desktop wrap the same Learning OS as `docs/` / https://interstitiumlabs.dev  
**Default native launch:** **Lab Muse** (`/coach/`) — Muse-class companion shell (chat-first, Interstitium cyan/gold/void + Dee monas avatar). Not Meta Muse; no Meta trademarks/assets.  
**Security:** [docs/ops/ENTERPRISE-SECURITY.md](../../docs/ops/ENTERPRISE-SECURITY.md) · [MOBILE-SECURITY.md](../../docs/ops/MOBILE-SECURITY.md)  
**Stores:** [STORE-PUBLISH.md](../../docs/ops/STORE-PUBLISH.md)

| | |
| --- | --- |
| appId | `dev.interstitiumlabs.app` |
| appName | Interstitium Labs |
| webDir | `www/` (synced from `docs/`) |

## Toolchain (Capacitor 8)

| | Minimum |
| --- | --- |
| Node | 22 |
| Android | Android Studio Otter 2025.2.1, JDK 21; app targets API 36, runs on API 24+ |
| iOS | Xcode 26; app runs on iOS 15+, CocoaPods project, UIScene lifecycle |

Android 16 (API 36) draws apps edge-to-edge: the web view sits behind the status and navigation bars, and StatusBar `backgroundColor` no longer applies there. The site already pads with `env(safe-area-inset-*)` under `viewport-fit=cover`, and `SystemBars` in `capacitor.config.ts` keeps those insets correct.

CI: `.github/workflows/mobile-build.yml` builds Android (debug + release, unit tests, lint) and an unsigned iOS simulator app on every change under `apps/mobile/`.

## Commands

```bash
# From repo root
./scripts/sync-mobile-web.sh
cd apps/mobile
npm ci
npm run audit          # or: npm audit --omit=dev --audit-level=high
npx cap add android    # once — requires Android SDK
npx cap add ios        # once — requires macOS + Xcode
npx cap sync
npx cap open android   # / ios
```

Copy Android security overlay after first `cap add android`:

```bash
mkdir -p android/app/src/main/res/xml android/app/src/debug/res/xml
cp android-security/res/xml/network_security_config.xml android/app/src/main/res/xml/
cp android-security/debug/res/xml/network_security_config.xml android/app/src/debug/res/xml/
# Set usesCleartextTraffic=false + networkSecurityConfig (see android-security/README.md)
```

## Native equal-capability APIs

| Capability | Status |
| --- | --- |
| Full Learning OS | Bundled `www/` from `docs/` |
| Lab Muse companion shell | Default native home `/coach/` · `il-muse-mobile.css` · Dee avatar |
| Status bar / void theme `#070B16` | StatusBar plugin + `il-bridge.js` |
| Splash / sigil | SplashScreen + brand assets |
| Share (proof wall) | `@capacitor/share` — ON |
| Push | Stub — `IL_FEATURE_PUSH=false`, no FCM keys |
| Biometric lock | Stub — OFF until auth + Keychain/Keystore |

## Desktop later

Same `www/` sync: Capacitor desktop targets, **or** Tauri/Electron wrapping synced assets — apply the same HTTPS / no-secrets / CSP policy from ENTERPRISE-SECURITY.md. PWA already installable via `docs/manifest.webmanifest` + `sw.js`.


## Open on a phone

### PWA (any phone browser)

1. Open https://interstitiumlabs.dev/coach/ (or install the site PWA from https://interstitiumlabs.dev).
2. Share → **Add to Home Screen** (iOS Safari) / **Install app** (Android Chrome).
3. Standalone display uses void `#070B16`, safe-area insets, and the Lab Muse bottom nav (Muse · Paths · Labs · OS).

### Capacitor native

```bash
./scripts/sync-mobile-web.sh
cd apps/mobile
npm ci
npx cap sync
npx cap run android   # device/emulator + Android SDK
npx cap run ios       # macOS + Xcode + device/sim
```

`il-bridge.js` deep-links Capacitor cold start from `/` → `/coach/` (Lab Muse). Brand lockup stays Interstitium (56–80px industry scale); avatar is the original Dee/Monas SVG (`docs/assets/il-muse-avatar-dee.svg (mirrored at assets/chrome/lab-muse-dee.svg)`).

## Never commit

`*.jks`, `AuthKey_*.p8`, `google-services.json`, `GoogleService-Info.plist` — see root `.gitignore`.
