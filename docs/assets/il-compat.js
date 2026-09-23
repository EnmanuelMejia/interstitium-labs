/**
 * Interstitium Labs — lightweight compatibility helpers
 * - --il-vh fallback for older Safari / WebViews without dvh
 * - Detect PWA standalone + Capacitor for safe-area CSS hooks
 * Safe to load with defer; idempotent.
 */
(function (w, d) {
  "use strict";
  if (w.__IL_COMPAT__) return;
  w.__IL_COMPAT__ = true;

  if (!d.getElementById("il-logo")) {
    var logo = d.createElement("script");
    logo.id = "il-logo";
    logo.src = "/assets/il-logo.js";
    logo.defer = true;
    d.head.appendChild(logo);
  }

  if (!d.getElementById("il-practice-language")) {
    var link = d.createElement("link");
    link.id = "il-practice-language";
    link.rel = "stylesheet";
    link.href = "/assets/il-practice-language.css";
    d.head.appendChild(link);
  }

  var root = d.documentElement;

  function setVh() {
    var h = w.innerHeight || (d.documentElement && d.documentElement.clientHeight) || 0;
    if (!h) return;
    root.style.setProperty("--il-vh", h / 100 + "px");
  }

  function detectShell() {
    var standalone = false;
    try {
      standalone =
        (w.matchMedia && w.matchMedia("(display-mode: standalone)").matches) ||
        (w.navigator && w.navigator.standalone === true);
    } catch (_) {}
    if (standalone) root.classList.add("il-standalone");

    var cap = false;
    try {
      cap = !!(
        w.Capacitor ||
        (w.navigator && /capacitor/i.test(w.navigator.userAgent || "")) ||
        (w.navigator && /InterstitiumLabs/i.test(w.navigator.userAgent || ""))
      );
    } catch (_) {}
    if (cap) root.classList.add("il-capacitor");
  }

  setVh();
  detectShell();

  var resizeTimer = null;
  function onResize() {
    if (resizeTimer) w.clearTimeout(resizeTimer);
    resizeTimer = w.setTimeout(setVh, 100);
  }

  w.addEventListener("resize", onResize, { passive: true });
  w.addEventListener("orientationchange", function () {
    w.setTimeout(setVh, 200);
  }, { passive: true });

  // VisualViewport accounts for iOS URL bar show/hide
  if (w.visualViewport) {
    w.visualViewport.addEventListener("resize", onResize, { passive: true });
  }

  if (d.readyState === "loading") {
    d.addEventListener("DOMContentLoaded", setVh, { once: true });
  }
})(window, document);
