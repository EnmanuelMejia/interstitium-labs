import type { CapacitorConfig } from "@capacitor/cli";

/**
 * Interstitium Labs — Capacitor 6 config (security-first).
 * appId must match store Bundle ID / applicationId.
 * allowNavigation: first-party + localhost only (see docs/ops/MOBILE-SECURITY.md).
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
