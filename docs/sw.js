/* Interstitium Labs service worker — Learning OS offline shell
 * Security: NEVER cache enroll config as authoritative secrets (there are none client-side;
 * still exclude /enroll/config.js from long-lived shell cache). First-party only.
 */
const SW_VERSION = "il-sw-v1-2026-09-21";
const SHELL_CACHE = SW_VERSION + "-shell";
const PAGE_CACHE = SW_VERSION + "-pages";

const SHELL_URLS = [
  "/",
  "/manifest.webmanifest",
  "/favicon.png",
  "/favicon.svg",
  "/assets/chrome/icon-192.png",
  "/assets/chrome/icon-512.png",
  "/assets/chrome/apple-touch.png",
  "/assets/chrome/icon-maskable-512.png",
  "/assets/chrome/canonical-lockup.png",
  "/assets/il-game.js",
  "/assets/il-motion.js",
  "/assets/il-motion.css",
  "/assets/il-pwa.js",
  "/founders/",
  "/learn/",
  "/play/",
  "/prep/",
  "/paths/",
];

/** Paths that must not be put in the durable shell cache */
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
      .then((keys) =>
        Promise.all(
          keys
            .filter((k) => k.startsWith("il-sw-") && k !== SHELL_CACHE && k !== PAGE_CACHE)
            .map((k) => caches.delete(k))
        )
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  let url;
  try {
    url = new URL(req.url);
  } catch (_) {
    return;
  }

  // Same-origin only — do not intercept third-party (fonts, Stripe hosted pages)
  if (url.origin !== self.location.origin) return;

  if (isSensitiveOrVolatile(url)) {
    event.respondWith(fetch(req).catch(() => caches.match(req)));
    return;
  }

  const acceptsHTML =
    req.mode === "navigate" ||
    (req.headers.get("accept") || "").includes("text/html");

  if (acceptsHTML) {
    // Network-first for HTML so Learning OS updates land; fall back to cache offline
    event.respondWith(
      fetch(req)
        .then((res) => {
          if (res && res.ok) {
            const copy = res.clone();
            caches.open(PAGE_CACHE).then((c) => c.put(req, copy));
          }
          return res;
        })
        .catch(() =>
          caches.match(req).then((hit) => hit || caches.match("/") || caches.match("/founders/"))
        )
    );
    return;
  }

  // Cache-first for shell static assets
  event.respondWith(
    caches.match(req).then((hit) => {
      if (hit) return hit;
      return fetch(req).then((res) => {
        if (res && res.ok && (url.pathname.startsWith("/assets/") || url.pathname.startsWith("/assets/chrome/"))) {
          const copy = res.clone();
          caches.open(SHELL_CACHE).then((c) => c.put(req, copy));
        }
        return res;
      });
    })
  );
});
