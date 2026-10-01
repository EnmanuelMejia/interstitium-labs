import type { CapacitorConfig } from "@capacitor/cli";

/**
 * Interstitium Labs — Capacitor 8 config (security-first).
 * appId must match store Bundle ID / applicationId.
 * allowNavigation: first-party + localhost only (see docs/ops/MOBILE-SECURITY.md).
 *
 * Android 16 (targetSdk 36) enforces edge-to-edge: the web view draws behind
 * the system bars, and StatusBar backgroundColor / overlaysWebView no longer
 * apply there. The launch pages set viewport-fit=cover and pad with
 * env(safe-area-inset-*) themselves; there is no official
 * `@capacitor/system-bars` package, so no such plugin is configured here —
 * the site's own safe-area CSS is the source of truth.
 */
const config: CapacitorConfig = {
  appId: "dev.interstitiumlabs.app",
  appName: "Interstitium Labs",
  webDir: "www",
  server: {
    // Production loads bundled www/. For live remote debugging only, set url temporarily —
    // never ship a release pointing at an untrusted host.
    androidScheme: "https",
    iosScheme: "https",
    hostname: "interstitiumlabs.dev",
    allowNavigation: [
      "interstitiumlabs.dev",
      "*.interstitiumlabs.dev",
      "localhost",
      "127.0.0.1",
    ],
  },
  plugins: {
    SplashScreen: {
      backgroundColor: "#070B16",
      // Primary path: explicit SplashScreen.hide() from il-bridge.js once the
      // page is interactive (plus a 5s in-bridge safety timeout). Native
      // backstop: launchAutoHide stays ON with a long duration, so if the
      // bridge file ever fails to load or parse, the native plugin still
      // dismisses the splash at 8s — users can never be stranded on it.
      launchAutoHide: true,
      launchShowDuration: 8000,
      showSpinner: false,
    },
    StatusBar: {
      // LIGHT = light status-bar content (clock/battery) for the void
      // background. "DARK" would render dark content — invisible on #070B16.
      style: "LIGHT",
      // Ignored on Android 16+ (edge-to-edge); applies on iOS.
      backgroundColor: "#070B16",
    },
  },
  android: {
    allowMixedContent: false,
    backgroundColor: "#070B16",
  },
  ios: {
    backgroundColor: "#070B16",
    contentInset: "automatic",
    preferredContentMode: "mobile",
  },
};

export default config;
