# Android security overlays

After `npx cap add android` / `npx cap sync android`:

1. Copy `res/xml/network_security_config.xml` → `android/app/src/main/res/xml/`
2. Set `android:usesCleartextTraffic="false"` and `android:networkSecurityConfig="@xml/network_security_config"` on `<application>`
3. Add HTTPS intent-filter for `interstitiumlabs.dev` only (see snippets)
4. Never commit `*.jks`, `google-services.json`

See `docs/ops/MOBILE-SECURITY.md`.
