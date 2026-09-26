import type { CapacitorConfig } from "@capacitor/cli";

/**
 * Interstitium Labs — Capacitor 8 config (security-first).
 * appId must match store Bundle ID / applicationId.
 * allowNavigation: first-party + localhost only (see docs/ops/MOBILE-SECURITY.md).
 *
 * Android 16 (targetSdk 36) enforces edge-to-edge: the web view draws behind
 * the system bars, and StatusBar backgroundColor / overlaysWebView no longer
 * apply there. The site already sets viewport-fit=cover and pads with
 * env(safe-area-inset-*); SystemBars keeps those insets correct on Android.
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
      launchAutoHide: true,
      showSpinner: false,
    },
    StatusBar: {
      style: "DARK",
      // iOS only from Android 16 on; see the note above.
      backgroundColor: "#070B16",
    },
    SystemBars: {
      // Inject --safe-area-inset-* as well as env() values on Android.
      insetsHandling: "css",
      // Every page declares viewport-fit=cover; saying so up front avoids a layout jump.
      initialViewportFitValueHint: "cover",
      // Light system bar icons on the void background.
      style: "DARK",
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
