/* Interstitium Labs — service worker KILL SWITCH.
 *
 * The offline worker is retired. This file exists so a device still controlled
 * by the September precache can update once, drop every cache, reload open
 * windows from the network, and unregister. Fetch never reads or writes a cache.
 *
 * A second activate must not navigate again: reloaded URLs carry il_heal=1, and
 * /enroll/ is left alone so an in-progress form is not wiped.
 */
self.addEventListener("install", function (event) {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    (async function () {
      try {
        var names = await caches.keys();
        await Promise.all(
          names.map(function (n) {
            return caches.delete(n).catch(function () {});
          })
        );
      } catch (e) {}

      var wins = [];
      try {
        await self.clients.claim();
        wins = await self.clients.matchAll({
          type: "window",
          includeUncontrolled: true,
        });
      } catch (e2) {}

      await Promise.all(
        wins.map(function (c) {
          var url;
          try {
            url = new URL(c.url);
          } catch (e3) {
            return Promise.resolve();
          }
          if (url.origin !== self.location.origin) return Promise.resolve();
          if (url.pathname.indexOf("/enroll/") === 0) return Promise.resolve();
          if (url.searchParams.get("il_heal") === "1") return Promise.resolve();
          url.searchParams.set("il_heal", "1");
          try {
            return Promise.resolve(c.navigate(url.href)).catch(function () {});
          } catch (e4) {
            return Promise.resolve();
          }
        })
      );

      try {
        await self.registration.unregister();
      } catch (e5) {}
    })()
  );
});

self.addEventListener("fetch", function (event) {
  event.respondWith(
    fetch(event.request).catch(function () {
      return Response.error();
    })
  );
});
