/**
 * Interstitium Labs — service worker retired.
 * Unregister any worker, delete every cache, and strip the one-shot il_heal
 * query the kill switch adds when it reloads a stuck tab. Pages load from
 * the network. A future worker has to be versioned and fail-open on purpose.
 */
(function (global) {
  "use strict";
  try {
    try {
      var here = new URL(global.location.href);
      if (here.searchParams.get("il_heal") === "1") {
        here.searchParams.delete("il_heal");
        var next = here.pathname + here.search + here.hash;
        global.history.replaceState(global.history.state, "", next);
      }
    } catch (eUrl) {}
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
