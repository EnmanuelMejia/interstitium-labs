/**
 * Interstitium Labs — service worker RETIRED (2026-10-01).
 * The offline worker poisoned mobile caches and broke rendering during
 * hiring-manager audits. This script now unregisters any service worker
 * and deletes every cache, then stays out of the way. The page always
 * loads fresh from the network. PWA re-introduction (if ever) will be
 * deliberate, versioned, and fail-open.
 */
(function (global) {
  "use strict";
  try {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker
        .getRegistrations()
        .then(function (regs) {
          regs.forEach(function (r) {
            try { r.unregister(); } catch (_) {}
          });
        })
        .catch(function () {});
    }
    if ("caches" in global) {
      caches
        .keys()
        .then(function (keys) {
          keys.forEach(function (k) {
            try { caches.delete(k); } catch (_) {}
          });
        })
        .catch(function () {});
    }
  } catch (_) {}
})(typeof window !== "undefined" ? window : this);
