/* Interstitium Labs service worker — self-healing shell (2026-10-01, heal2)
 *
 * This worker exists to REPAIR poisoned offline state, then stay healthy.
 * - On activate it deletes EVERY cache it can see (including all older
 *   il-sw-* shell/page caches), so stale or half-written entries from
 *   previous workers can never be served again.
 * - After the purge it reloads every open tab (except form/stateful pages),
 *   so a device stuck on a poisoned render heals visibly without the user
 *   having to clear site data.
 * - HTML navigations are network-first: visitors always get the newest page.
 * - Static assets are stale-while-revalidate: instant render from cache when
 *   present, but every entry is revalidated in the background on each visit,
 *   so a bad cached copy heals itself within a single page load.
 * - Error responses (4xx/5xx) and opaque failures are NEVER written to cache.
 * - Sensitive/volatile paths are network-only.
 * - Same-origin only; third-party (fonts, CDNs) is never intercepted.
 */
const SW_VERSION = "il-sw-2026-10-01-heal2";
const SHELL_CACHE = SW_VERSION + "-shell";
const PAGE_CACHE = SW_VERSION + "-pages";

/* Minimal precache: only long-lived brand chrome. Versioned CSS/JS is NOT
 * precached — it is cached on first use via stale-while-revalidate, so
 * filename drift between deploys can never poison the shell. */
const SHELL_URLS = [
  "/manifest.webmanifest",
  "/favicon.png",
  "/favicon.svg",
  "/assets/chrome/icon-192.png",
  "/assets/chrome/icon-512.png",
  "/assets/chrome/apple-touch.png",
  "/assets/chrome/icon-maskable-512.png",
];

/** Paths that must never be cached. */
function isSensitiveOrVolatile(url) {
  const p = url.pathname;
  if (p === "/enroll/config.js" || p.startsWith("/enroll/config")) return true;
  if (p.startsWith("/admin")) return true;
  if (p.includes("google-services") || p.endsWith(".jks") || p.endsWith(".p8")) return true;
  return false;
}

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(SHELL_CACHE)
      .then((cache) => cache.addAll(SHELL_URLS.map((u) => new Request(u, { cache: "reload" }))))
      .then(() => self.skipWaiting())
      .catch(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      // Nuclear purge: remove every cache, including all older il-sw-* shells.
      // The fresh caches for this version are (re)created lazily below.
      .then((keys) => Promise.all(keys.map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
      // Make the heal visible: reload open tabs so a poisoned render is
      // replaced by a fully fresh one. Skip form/stateful pages so in-progress
      // input is never yanked out from under the visitor.
      .then(() => self.clients.matchAll({ type: "window", includeUncontrolled: true }))
      .then((clients) =>
        Promise.all(
          clients.map((client) => {
            try {
              const u = new URL(client.url);
              if (u.origin !== self.location.origin) return Promise.resolve();
              if (u.pathname.startsWith("/enroll/") || u.search) return Promise.resolve();
              return client.navigate(client.url).catch(() => {});
            } catch (_) {
              return Promise.resolve();
            }
          })
        )
      )
      .catch(() => {})
  );
});

/** Revalidate a request in the background and refresh the cache entry. */
function revalidate(cacheName, req) {
  fetch(req)
    .then((res) => {
      if (res && res.ok) {
        const copy = res.clone();
        caches.open(cacheName).then((c) => c.put(req, copy)).catch(() => {});
      }
    })
    .catch(() => {});
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  let url;
  try {
    url = new URL(req.url);
  } catch (_) {
    return;
  }

  // Same-origin only — do not intercept third-party (fonts, etc.)
  if (url.origin !== self.location.origin) return;

  if (isSensitiveOrVolatile(url)) {
    // Network-only: never cache, never serve stale.
    event.respondWith(fetch(req));
    return;
  }

  const acceptsHTML =
    req.mode === "navigate" ||
    (req.headers.get("accept") || "").includes("text/html");

  if (acceptsHTML) {
    // Network-first for documents so updates land immediately.
    event.respondWith(
      fetch(req)
        .then((res) => {
          if (res && res.ok) {
            const copy = res.clone();
            caches.open(PAGE_CACHE).then((c) => c.put(req, copy)).catch(() => {});
          }
          return res;
        })
        .catch(() =>
          caches.match(req).then((hit) => hit || caches.match("/"))
        )
    );
    return;
  }

  // Stale-while-revalidate for everything else (CSS/JS/images/JSON).
  // Serves instantly when cached, but ALWAYS revalidates in the background,
  // so poisoned entries heal on the next visit without any user action.
  event.respondWith(
    caches.match(req).then((hit) => {
      if (hit) {
        revalidate(SHELL_CACHE, req);
        return hit;
      }
      return fetch(req).then((res) => {
        if (res && res.ok) {
          const copy = res.clone();
          caches.open(SHELL_CACHE).then((c) => c.put(req, copy)).catch(() => {});
        }
        return res;
      });
    })
  );
});
