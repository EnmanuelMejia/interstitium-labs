# iOS App Transport Security

After `npx cap add ios`, confirm `Info.plist`:

- Do **not** set `NSAllowsArbitraryLoads` to `true`
- Prefer default ATS (HTTPS only)
- Localhost for Capacitor live reload is handled by debug tooling; do not add broad exception domains

Universal Links (later): associated domains `applinks:interstitiumlabs.dev` only after `apple-app-site-association` is published.

Status bar: dark content on void `#070B16` via Capacitor StatusBar plugin.
