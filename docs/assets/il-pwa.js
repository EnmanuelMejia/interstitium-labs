/**
 * Interstitium Labs — PWA register + install hints.
 * Registers /sw.js on HTTPS or localhost. No third-party trackers.
 */
(function (global) {
  "use strict";
  if (!("serviceWorker" in navigator)) return;

  var host = global.location.hostname;
  var ok =
    global.location.protocol === "https:" ||
    host === "localhost" ||
    host === "127.0.0.1";
  if (!ok) return;

  global.addEventListener("load", function () {
    navigator.serviceWorker
      .register("/sw.js", { scope: "/" })
      .catch(function () {
        /* offline or blocked — fail closed silently */
      });
  });
})(typeof window !== "undefined" ? window : this);
