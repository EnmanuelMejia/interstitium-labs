var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// ../brand-logo-paths.mjs
var CANONICAL_LOGO = "/assets/chrome/interstitium-logo.png";
var RETIRED_LOGO_PATHS = /* @__PURE__ */ new Set([
  "/assets/chrome/canonical-lockup-2x.webp",
  "/assets/chrome/canonical-lockup-3x.webp",
  "/assets/chrome/canonical-lockup.png",
  "/assets/chrome/canonical-lockup.webp",
  "/assets/chrome/sigil-decor.webp",
  "/assets/chrome/sigil-glyph.svg",
  "/assets/chrome/sigil-hero-400.png",
  "/assets/chrome/sigil-hero-720.webp",
  "/assets/chrome/sigil-hero.webp",
  "/assets/chrome/apple-touch.png",
  "/assets/chrome/icon-192.png",
  "/assets/chrome/icon-512.png",
  "/assets/chrome/icon-maskable-512.png",
  "/assets/chrome/lab-muse-dee.svg",
  "/assets/il-muse-avatar-sigil.svg",
  "/assets/il-logo.js",
  "/favicon.svg",
  "/favicon.png",
  "/og-sigil.jpg",
  "/og.jpg"
]);
function isRetiredLogo(path) {
  return typeof path === "string" && RETIRED_LOGO_PATHS.has(path);
}
__name(isRetiredLogo, "isRetiredLogo");

// ../brand.js
var STYLESHEET = "/assets/il-brand.css";
var MASTHEAD = '<a class="skip il-site-skip" href="#il-site-content">Skip to page content</a><header class="il-site-masthead il-brand-masthead" aria-label="Interstitium Labs"><a class="il-site-brand il-brand-home" href="/" aria-label="Interstitium Labs home"><img class="il-site-logo il-brand-logo" src="' + CANONICAL_LOGO + '" width="44" height="44" alt=""><span class="il-site-copy il-brand-copy"><strong class="il-site-name il-brand-name">Interstitium Labs</strong><small class="il-site-motto il-brand-motto" lang="la">Scientia omnia vincit</small></span></a><nav class="il-site-nav il-brand-nav" aria-label="Interstitium Labs"><a href="/member-courses/">Courses</a><a href="/noah/">Noah</a><a href="/login/">Member sign-in</a><a href="/enroll/">Membership</a></nav></header><span id="il-site-content" class="il-site-content" tabindex="-1"></span>';
var SITE_HOSTS = /* @__PURE__ */ new Set(["interstitiumlabs.dev", "www.interstitiumlabs.dev", "learn.interstitiumlabs.dev", "app.interstitiumlabs.dev", "api.interstitiumlabs.dev", "enmanueldmejia.com", "www.enmanueldmejia.com"]);
function retiredReference(value, request) {
  if (typeof value !== "string") return false;
  try {
    const pagePath = request ? new URL(request.url).pathname : "/";
    const url = new URL(value, "https://interstitiumlabs.dev" + pagePath);
    return SITE_HOSTS.has(url.hostname) && isRetiredLogo(decodeURIComponent(url.pathname));
  } catch {
    return false;
  }
}
__name(retiredReference, "retiredReference");
function replaceSrcset(value, request) {
  if (typeof value !== "string") return value;
  return value.replace(/(^|,)(\s*)([^\s,]+)(?=\s|,|$)/g, (match, separator, space, url) => retiredReference(url, request) ? separator + space + CANONICAL_LOGO : match);
}
__name(replaceSrcset, "replaceSrcset");
function brandDocument(response, request) {
  if (request && request.method !== "GET" || response.status !== 200 || !response.body || response.headers.get("Content-Type")?.split(";")[0].trim().toLowerCase() !== "text/html") return response;
  if (typeof HTMLRewriter !== "function") return response;
  const headers = new Headers(response.headers);
  for (const name of ["Content-Length", "ETag", "Content-MD5", "Digest", "Content-Digest", "Repr-Digest"]) headers.delete(name);
  return new HTMLRewriter().on("html", { element(element) {
    const classes = new Set((element.getAttribute("class") || "").split(/\s+/).filter(Boolean));
    classes.add("il-site-theme");
    element.setAttribute("class", [...classes].join(" "));
  } }).on("head", { element(element) {
    element.append('<meta name="theme-color" content="#0a0f1d"><link rel="icon" type="image/png" sizes="192x192" href="' + CANONICAL_LOGO + '"><link rel="stylesheet" href="' + STYLESHEET + '">', { html: true });
  } }).on('meta[name="theme-color"], link[rel="stylesheet"][href="/assets/il-brand.css"]', { element(element) {
    element.remove();
  } }).on(".il-site-masthead, .il-site-skip, #il-site-content", { element(element) {
    element.remove();
  } }).on("link[rel]", { element(element) {
    const rel = (element.getAttribute("rel") || "").toLowerCase().split(/\s+/), href = element.getAttribute("href");
    if (rel.some((value) => ["icon", "apple-touch-icon", "apple-touch-icon-precomposed", "mask-icon"].includes(value))) element.remove();
    else if (retiredReference(href, request)) {
      if (/\.js(?:[?#]|$)/i.test(href)) element.remove();
      else element.setAttribute("href", CANONICAL_LOGO);
    }
  } }).on("img, source", { element(element) {
    const prior = element.getAttribute("src");
    if (retiredReference(prior, request)) {
      element.setAttribute("src", CANONICAL_LOGO);
      if (element.tagName === "img") {
        element.setAttribute("width", "192");
        element.setAttribute("height", "192");
        if (element.getAttribute("alt")) element.setAttribute("alt", "Interstitium Labs");
      }
    }
    const srcset = element.getAttribute("srcset");
    if (srcset) {
      const next = replaceSrcset(srcset, request);
      if (next !== srcset) element.setAttribute("srcset", next);
    }
  } }).on("meta[content]", { element(element) {
    if (retiredReference(element.getAttribute("content"), request)) element.setAttribute("content", CANONICAL_LOGO);
  } }).on("script[src]", { element(element) {
    if (retiredReference(element.getAttribute("src"), request)) element.remove();
  } }).on('header a.brand[href="/"], header a.il-brand[href="/"]', { element(element) {
    element.remove();
  } }).on("body", { element(element) {
    element.prepend(MASTHEAD, { html: true });
  } }).transform(new Response(response.body, { status: response.status, statusText: response.statusText, headers }));
}
__name(brandDocument, "brandDocument");

// index.mjs
var ORIGIN = "https://interstitiumlabs.dev";
var ALIASES = /* @__PURE__ */ new Set(["learn.interstitiumlabs.dev", "www.interstitiumlabs.dev", "enmanueldmejia.com", "www.enmanueldmejia.com"]);
var SESSION = "__Host-labs_session";
var ROUTES = [
  ["/bootcamps/threatlocker-assessment-prep/", "THREATLOCKER_ASSESSMENT"],
  ["/bootcamps/", "CERT_BOOTCAMPS"],
  ["/assessments/", "FULL_SPECTRUM"],
  ["/bootcamp/", "THREATLOCKER_BOOTCAMP"]
];
var HEADERS = { "Cache-Control": "private, no-store", "Vary": "Cookie", "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer", "X-Frame-Options": "DENY", "Cross-Origin-Resource-Policy": "same-origin", "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()" };
function reply(error, status) {
  return new Response(JSON.stringify({ error }), { status, headers: { ...HEADERS, "Content-Type": "application/json; charset=utf-8" } });
}
__name(reply, "reply");
function normalizedPath(url) {
  try {
    const path = decodeURIComponent(url.pathname);
    return /[\\%\u0000-\u001f\u007f]|\/\/|(?:^|\/)\.{1,2}(?:\/|$)/.test(path) ? null : path;
  } catch {
    return null;
  }
}
__name(normalizedPath, "normalizedPath");
function selectCourseService(path) {
  return ROUTES.find(([prefix]) => path.startsWith(prefix))?.[1] || null;
}
__name(selectCourseService, "selectCourseService");
function sessionCookie(request) {
  const matches = (request.headers.get("Cookie") || "").split(";").map((x) => x.trim()).filter((x) => x.startsWith(SESSION + "="));
  if (matches.length !== 1) return null;
  const value = matches[0].slice(SESSION.length + 1);
  return /^[A-Za-z0-9_-]{43}$/.test(value) ? SESSION + "=" + value : null;
}
__name(sessionCookie, "sessionCookie");
function cancelBody(body) {
  try {
    body?.cancel().catch(() => {
    });
  } catch {
  }
}
__name(cancelBody, "cancelBody");
async function verify(binding, cookie) {
  const controller = new AbortController();
  let reader;
  let rejectDeadline;
  const deadline = new Promise((_, reject) => {
    rejectDeadline = reject;
  });
  const timeout = setTimeout(() => {
    controller.abort();
    cancelBody(reader);
    rejectDeadline(Error("timeout"));
  }, 5e3);
  try {
    const response = await Promise.race([deadline, binding.fetch(new Request(ORIGIN + "/api/membership?view=learning", { headers: { Cookie: cookie, Accept: "application/json" }, redirect: "manual", signal: controller.signal }))]);
    if (!response.ok || response.headers.get("Content-Type")?.split(";")[0].trim().toLowerCase() !== "application/json") {
      cancelBody(response.body);
      return null;
    }
    reader = response.body?.getReader();
    if (!reader) return null;
    let size = 0;
    const chunks = [];
    try {
      while (true) {
        const { done, value } = await Promise.race([deadline, reader.read()]);
        if (controller.signal.aborted) throw Error("timeout");
        if (done) break;
        size += value.byteLength;
        if (size > 16384) {
          cancelBody(reader);
          return null;
        }
        chunks.push(value);
      }
    } finally {
      reader.releaseLock();
    }
    const bytes = new Uint8Array(size);
    let offset = 0;
    for (const chunk of chunks) {
      bytes.set(chunk, offset);
      offset += chunk.length;
    }
    return JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes));
  } catch {
    return null;
  } finally {
    clearTimeout(timeout);
  }
}
__name(verify, "verify");
async function fetchOriginal(binding, request, headers) {
  const controller = new AbortController();
  let timeout;
  const deadline = new Promise((_, reject) => {
    timeout = setTimeout(() => {
      controller.abort();
      reject(Error("timeout"));
    }, 5e3);
  });
  try {
    const pending = binding.fetch(new Request(request, { headers, redirect: "manual", signal: controller.signal }));
    Promise.resolve(pending).then((response) => {
      if (controller.signal.aborted) cancelBody(response.body);
    }, () => {
    });
    return await Promise.race([deadline, pending]);
  } finally {
    clearTimeout(timeout);
  }
}
__name(fetchOriginal, "fetchOriginal");
var index_default = {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = normalizedPath(url);
    if (path === null) return reply("invalid-path", 400);
    if (isRetiredLogo(path)) return reply("not-found", 404);
    const service = selectCourseService(path);
    if (!service) return reply("not-found", 404);
    if (ALIASES.has(url.hostname)) {
      if (!["GET", "HEAD"].includes(request.method)) return reply("use-canonical-host", 409);
      return new Response(null, { status: 308, headers: { ...HEADERS, Location: ORIGIN + path } });
    }
    if (url.origin !== ORIGIN) return reply("unavailable-host", 421);
    if (env.COURSE_GATEWAY_ENABLED !== "true" || !env.MEMBERSHIP?.fetch || !env[service]?.fetch) return reply("temporarily-unavailable", 503);
    if (!["GET", "HEAD"].includes(request.method)) return reply("legacy-account-migration-required", 503);
    const freeBootcamp = path.startsWith("/bootcamps/threatlocker-assessment-prep/") ||
      path.startsWith("/bootcamps/tl-interview/");
    if (!freeBootcamp) {
      const cookie = sessionCookie(request);
      if (!cookie) return denied(request, false);
      const member = await verify(env.MEMBERSHIP, cookie);
      if (!member || member.available !== true) return reply("temporarily-unavailable", 503);
      if (member.authenticated !== true || member.active !== true) return denied(request, member.authenticated === true);
    }
    try {
      const headers = new Headers(request.headers);
      headers.delete("Cookie");
      headers.delete("Authorization");
      for (const key of [...headers.keys()]) if (/^x-(?:user|paid|member|membership|learner|forwarded)/i.test(key)) headers.delete(key);
      const response = await fetchOriginal(env[service], request, headers);
      const output = new Headers(response.headers);
      for (const name of ["CDN-Cache-Control", "Cloudflare-CDN-Cache-Control", "Surrogate-Control"]) output.delete(name);
      for (const [key, value] of Object.entries(HEADERS)) if (key !== "Vary") output.set(key, value);
      const vary = new Set((output.get("Vary") || "").split(",").map((x) => x.trim()).filter(Boolean));
      vary.add("Cookie");
      output.set("Vary", [...vary].join(", "));
      output.delete("Set-Cookie");
      if (request.method === "HEAD") cancelBody(response.body);
      return brandDocument(new Response(request.method === "HEAD" ? null : response.body, { status: response.status, statusText: response.statusText, headers: output }), request);
    } catch {
      return reply("temporarily-unavailable", 503);
    }
  }
};
function denied(request, authenticated) {
  const document = request.headers.get("Sec-Fetch-Dest") === "document" || request.headers.get("Accept")?.includes("text/html");
  if (document) return new Response(null, { status: 303, headers: { ...HEADERS, Location: ORIGIN + "/login/" } });
  return reply(authenticated ? "subscription-required" : "sign-in-required", authenticated ? 403 : 401);
}
__name(denied, "denied");
export {
  index_default as default,
  selectCourseService
};
//# sourceMappingURL=index.js.map