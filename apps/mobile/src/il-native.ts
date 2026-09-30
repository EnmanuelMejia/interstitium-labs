/**
 * Native capability stubs for equal Learning OS surface.
 * Feature flags default OFF for push + biometric until auth exists.
 * See docs/ops/MOBILE-SECURITY.md.
 */

export const IL_FEATURES = {
  /** Share sheet for proof-wall items — safe, on by default */
  SHARE: true,
  /** Push: stub only — no FCM/APNs keys in repo */
  PUSH: false,
  /** Biometric lock: wired behind flag OFF until auth + Keychain/Keystore */
  BIOMETRIC_LOCK: false,
} as const;

export type SharePayload = {
  title?: string;
  text?: string;
  url?: string;
  dialogTitle?: string;
};

/** Capacitor Share — proof wall items (no secrets). */
export async function shareProof(payload: SharePayload): Promise<boolean> {
  if (!IL_FEATURES.SHARE) return false;
  try {
    const { Share } = await import("@capacitor/share");
    await Share.share({
      title: payload.title ?? "Interstitium Labs",
      text: payload.text,
      url: payload.url,
      dialogTitle: payload.dialogTitle ?? "Share proof",
    });
    return true;
  } catch {
    if (typeof navigator !== "undefined" && navigator.share) {
      await navigator.share({
        title: payload.title,
        text: payload.text,
        url: payload.url,
      });
      return true;
    }
    return false;
  }
}

/**
 * Push stub — does not register with FCM/APNs.
 * Security: never embed google-services / AuthKey material here.
 */
export async function initPushStub(): Promise<{ enabled: false; reason: string }> {
  if (!IL_FEATURES.PUSH) {
    return {
      enabled: false,
      reason: "IL_FEATURE_PUSH is false — no push credentials shipped (MOBILE-SECURITY.md §3.8)",
    };
  }
  return {
    enabled: false,
    reason: "Push implementation not configured — refuse fake FCM keys",
  };
}

/**
 * Biometric lock stub — OFF until session auth exists.
 * Future: Keychain (iOS) / Keystore + BiometricPrompt (Android).
 * Do not store auth tokens in plain SharedPreferences / Preferences.
 */
export async function initBiometricLockStub(): Promise<{ enabled: false; reason: string }> {
  if (!IL_FEATURES.BIOMETRIC_LOCK) {
    return {
      enabled: false,
      reason: "IL_FEATURE_BIOMETRIC_LOCK is false until auth ships",
    };
  }
  return {
    enabled: false,
    reason: "Biometric plugin not activated — Keychain/Keystore required",
  };
}

/** Status bar / safe-area theming — void #070B16 */
export async function applyVoidChrome(): Promise<void> {
  try {
    const { Capacitor } = await import("@capacitor/core");
    const { StatusBar, Style } = await import("@capacitor/status-bar");
    await StatusBar.setStyle({ style: Style.Dark });
    // Android 15+ draws edge-to-edge; the status bar colour only applies on iOS.
    if (Capacitor.getPlatform() !== "android") {
      await StatusBar.setBackgroundColor({ color: "#070B16" });
    }
  } catch {
    /* web / unsupported */
  }
}
