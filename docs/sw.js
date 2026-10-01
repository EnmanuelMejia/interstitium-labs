/* Interstitium Labs — service worker KILL SWITCH (2026-10-01).
 *
 * The service worker is RETIRED. This script exists for exactly one reason:
 * to find any device still controlled by the old worker (which precached `/`
 * and served stale builds for days), and force-heal it with zero user action:
 *
 *   install  -> skipWaiting(), take over immediately
 *   activate -> delete EVERY CacheStorage cache, claim clients,
 *               force-reload every open window to the fresh network HTML,
 *               then unregister self so no worker ever controls the site again
 *   fetch    -> fail-open: always network, never cache
 *
 * Runs once per device, then removes itself. Safe to keep deployed forever.
 */
self.addEventListener("install", function (event) {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    (async function () {
      // 1. Nuke every cache — this is what served the stale September builds.
      try {
        var names = await caches.keys();
        await Promise.all(
          names.map(function (n) {
            return caches.delete(n).catch(function () {});
          })
        );
      } catch (e) {}

      // 2. Take control of every open tab/window right now.
      var wins = [];
      try {
        await self.clients.claim();
        wins = await self.clients.matchAll({
          type: "window",
          includeUncontrolled: true,
        });
      } catch (e) {}

      // 3. Force each window to reload from network (fresh HTML carries the
      //    inline cache-killer too, as belt-and-suspenders).
      await Promise.all(
        wins.map(function (c) {
          try {
            return c.navigate(c.url);
          } catch (e) {
            return Promise.resolve();
          }
        })
      );

      // 4. Unregister self — no service worker, ever again, until a
      //    deliberately versioned, fail-open PWA strategy ships.
      try {
        await self.registration.unregister();
      } catch (e) {}
    })()
  );
});

self.addEventListener("fetch", function (event) {
  // Fail-open: never serve from cache. If the network fails, the browser
  // shows its own offline page — never a stale build.
  event.respondWith(fetch(event.request));
});
