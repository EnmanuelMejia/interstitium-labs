/**
 * Interstitium Labs — edge entry for the solitary-sound-015a Worker.
 *
 * Handles a small set of dynamic routes, then falls through to the static
 * assets bundle for everything else (env.ASSETS).
 *
 * Routes:
 *   POST /api/waitlist   Persist an enroll waitlist signup (name + email) to KV.
 *   /os /os/             301 -> /learn/
 *   /proof /proof/       301 -> /evidence/
 *
 * KV binding required: WAITLIST (namespace id in deploy config).
 */

var NOINDEX_PREFIXES = ["/admin/", "/ops/", "/analytics/", "/measure/", "/brand/"];

function needsNoindex(path) {
  for (var i = 0; i < NOINDEX_PREFIXES.length; i++) {
    var pre = NOINDEX_PREFIXES[i];
    if (path === pre.slice(0, -1) || path.indexOf(pre) === 0) return true;
  }
  return false;
}

var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
var MAX_BODY = 8192;
var WAITLIST_SUCCESS_PATH = "/enroll/success.html";

function json(data, status) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function movedPermanently(request, path) {
  return Response.redirect(new URL(path, request.url).toString(), 301);
}

function wantsJson(request) {
  var accept = request.headers.get("accept") || "";
  return accept.indexOf("application/json") !== -1;
}

async function readSignup(request) {
  var ct = (request.headers.get("content-type") || "").toLowerCase();
  if (ct.indexOf("application/json") !== -1) {
    try {
      return await request.json();
    } catch (e) {
      return null;
    }
  }
  try {
    var form = await request.formData();
    var out = {};
    form.forEach(function (v, k) {
      out[k] = v;
    });
    return out;
  } catch (e) {
    return null;
  }
}

async function handleWaitlist(request, env) {
  if (request.method !== "POST") {
    return json({ ok: false, error: "method_not_allowed" }, 405);
  }
  var len = request.headers.get("content-length");
  if (len && parseInt(len, 10) > MAX_BODY) {
    return json({ ok: false, error: "payload_too_large" }, 413);
  }
  var data = await readSignup(request);
  var name = data && data.name != null ? String(data.name).trim() : "";
  var email = data && data.email != null ? String(data.email).trim().toLowerCase() : "";
  if (!name || name.length > 120) {
    return json({ ok: false, error: "name_required" }, 422);
  }
  if (!email || email.length > 254 || !EMAIL_RE.test(email)) {
    return json({ ok: false, error: "email_invalid" }, 422);
  }
  var record = {
    name: name,
    email: email,
    created_at: new Date().toISOString(),
    source: "enroll",
  };
  var key =
    "wl:" + Date.now() + ":" + Math.random().toString(36).slice(2, 10);
  try {
    await env.WAITLIST.put(key, JSON.stringify(record));
  } catch (e) {
    return json({ ok: false, error: "store_unavailable" }, 503);
  }
  // Non-JS form posts get a real redirect to the confirmation page;
  // fetch clients get JSON and navigate themselves.
  if (!wantsJson(request)) {
    return Response.redirect(
      new URL(WAITLIST_SUCCESS_PATH, request.url).toString(),
      303
    );
  }
  return json({ ok: true });
}

export default {
  async fetch(request, env) {
    var url = new URL(request.url);
    var path = url.pathname;

    if (path === "/os" || path === "/os/") {
      return movedPermanently(request, "/learn/");
    }
    if (path === "/proof" || path === "/proof/") {
      return movedPermanently(request, "/evidence/");
    }
    if (path === "/api/waitlist") {
      if (!env.WAITLIST) {
        return json({ ok: false, error: "store_unavailable" }, 503);
      }
      return handleWaitlist(request, env);
    }

    var res = await env.ASSETS.fetch(request);
    // _headers is not applied by this API deploy path, so gate operator
    // prefixes here (mirrors the _headers X-Robots-Tag intent).
    if (needsNoindex(path)) {
      var h = new Headers(res.headers);
      h.set("X-Robots-Tag", "noindex, nofollow");
      return new Response(res.body, {
        status: res.status,
        statusText: res.statusText,
        headers: h,
      });
    }
    return res;
  },
};
