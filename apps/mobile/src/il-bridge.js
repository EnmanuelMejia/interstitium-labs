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


  function isCapacitor() {
    try {
      return !!(
        global.Capacitor ||
        (global.navigator && /capacitor/i.test(global.navigator.userAgent || ""))
      );
    } catch (_) {
      return false;
    }
  }

  /** Native default launch → Lab Muse companion (/coach/). Web PWA keeps site home.
   * The sync pipeline serves the coach entry directly at www/ root, so cold
   * start is a single page load; this redirect is a fallback for older
   * bundles, and never fires when the coach page is already rendered
   * (body.il-muse-page marker). */
  function openLabMuseHome() {
    if (!isCapacitor()) return;
    try {
      if (document.body && document.body.classList.contains("il-muse-page")) return;
      var path = (global.location && global.location.pathname) || "/";
      if (path === "/" || path === "/index.html" || path === "") {
        if (global.sessionStorage && global.sessionStorage.getItem("il-muse-home") === "1") return;
        if (global.sessionStorage) global.sessionStorage.setItem("il-muse-home", "1");
        global.location.replace("/coach/");
      }
    } catch (_) {}
  }

  async function applyVoidChrome() {
    try {
      var SB = global.Capacitor && global.Capacitor.Plugins && global.Capacitor.Plugins.StatusBar;
      if (SB) {
        // LIGHT = light status-bar content for the void background.
        await SB.setStyle({ style: "LIGHT" });
        // Android 15+ draws edge-to-edge; the status bar colour only applies on iOS.
        var platform = global.Capacitor.getPlatform ? global.Capacitor.getPlatform() : "";
        if (platform !== "android") await SB.setBackgroundColor({ color: "#070B16" });
      }
    } catch (_) {}
  }

  /** Deliberate splash behavior: hide exactly when the page is interactive.
   * capacitor.config.ts sets launchAutoHide: false, so the splash never hides
   * ambiguously; the 5s fallback covers a hung first paint. Defensive: every
   * plugin call is guarded, failures are silent. */
  var splashHidden = false;
  function hideSplash() {
    if (splashHidden) return;
    splashHidden = true;
    try {
      var SP = global.Capacitor && global.Capacitor.Plugins && global.Capacitor.Plugins.SplashScreen;
      if (SP && SP.hide) SP.hide();
    } catch (_) {}
  }

  global.ILNative = {
    FLAGS: FLAGS,
    shareProof: shareProof,
    initPushStub: initPushStub,
    initBiometricLockStub: initBiometricLockStub,
    applyVoidChrome: applyVoidChrome,
    openLabMuseHome: openLabMuseHome,
    hideSplash: hideSplash,
    isCapacitor: isCapacitor,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      applyVoidChrome();
      openLabMuseHome();
      hideSplash();
    });
  } else {
    applyVoidChrome();
    openLabMuseHome();
    hideSplash();
  }
  // Safety net: never leave the splash up longer than 5s even if DOMContentLoaded stalls.
  setTimeout(hideSplash, 5000);
})(typeof window !== "undefined" ? window : this);
