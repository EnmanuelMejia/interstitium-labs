/**
 * Injected into bundled www for Capacitor runtime.
 * Exposes window.ILNative stubs; real Capacitor plugins load when available.
 */
(function (global) {
  "use strict";
  var FLAGS = {
    SHARE: true,
    PUSH: false,
    BIOMETRIC_LOCK: false,
  };

  async function shareProof(payload) {
    if (!FLAGS.SHARE) return false;
    try {
      if (global.Capacitor && global.Capacitor.Plugins && global.Capacitor.Plugins.Share) {
        await global.Capacitor.Plugins.Share.share({
          title: (payload && payload.title) || "Interstitium Labs",
          text: payload && payload.text,
          url: payload && payload.url,
          dialogTitle: (payload && payload.dialogTitle) || "Share proof",
        });
        return true;
      }
      if (navigator.share) {
        await navigator.share(payload || {});
        return true;
      }
    } catch (_) {}
    return false;
  }

  function initPushStub() {
    return Promise.resolve({
      enabled: false,
      reason: "IL_FEATURE_PUSH off — no FCM keys (security-first)",
    });
  }

  function initBiometricLockStub() {
    return Promise.resolve({
      enabled: false,
      reason: "IL_FEATURE_BIOMETRIC_LOCK off until auth + Keychain/Keystore",
    });
  }

  async function applyVoidChrome() {
    try {
      var SB = global.Capacitor && global.Capacitor.Plugins && global.Capacitor.Plugins.StatusBar;
      if (SB) {
        await SB.setStyle({ style: "DARK" });
        await SB.setBackgroundColor({ color: "#070B16" });
      }
    } catch (_) {}
  }

  global.ILNative = {
    FLAGS: FLAGS,
    shareProof: shareProof,
    initPushStub: initPushStub,
    initBiometricLockStub: initBiometricLockStub,
    applyVoidChrome: applyVoidChrome,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      applyVoidChrome();
    });
  } else {
    applyVoidChrome();
  }
})(typeof window !== "undefined" ? window : this);
