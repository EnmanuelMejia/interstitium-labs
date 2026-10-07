/**
 * Interstitium Labs — edge entry for the solitary-sound-015a Worker.
 *
 * Handles a small set of dynamic routes, then falls through to the static
 * assets bundle for everything else (env.ASSETS).
 *
 * Routes:
 *   POST /api/waitlist            Persist an enroll waitlist signup (name + email, optional tier) to KV.
 *   POST /api/auth/request       Magic-link request: {email} -> token in IL_AUTH (15-min TTL), email via MailChannels.
 *   GET  /api/auth/verify?token= Validate token, create session in IL_ACCOUNTS, set cookie, redirect to /progress/.
 *   GET  /api/me                 Session whoami -> {email} or 401.
 *   GET  /api/progress           Per-account progress JSON (session required).
 *   PUT  /api/progress           Merge per-account progress JSON (session required).
 *   POST /api/certificates/issue {path} -> certificate record (session required).
 *   GET  /api/certificates/verify?id=  Public certificate verification.
 *   /os /os/                     301 -> /learn/
 *   /proof /proof/               301 -> /evidence/
 *   19 consolidated stub slugs   301 -> their Learning OS targets
 *     (code, command, desk, doctrine, drill, factory, field, graph,
 *      interview, library, measure, plant, platform, portfolio, pricing,
 *      radar, sheets, si, system) — stub dirs removed 2026-10-06
 *
 * KV bindings: WAITLIST (required for waitlist), IL_AUTH + IL_ACCOUNTS
 * (required for auth/progress/certificates; account routes 503 without them),
 * NOAH_STATS (Noah usage aggregates; stats endpoints degrade gracefully
 * without it). Workers AI binding (AI) powers POST /api/noah; the route
 * returns 503 with a local fallback flag when the binding is absent.
 *
 * 2026-10-06: Noah AI tutor backend merged in from the retired
 * learn.interstitiumlabs.dev worker; the /university/ content tree lives in
 * ./university/ (IL-01 through IL-18 academies).
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
  // Optional tier label from another builder's frontend (e.g. "free", "tier-1").
  // Sanitized to a short printable token; never trusted for anything but display.
  if (data && data.tier != null) {
    var tier = String(data.tier).trim();
    if (tier && tier.length <= 40 && /^[A-Za-z0-9 _-]+$/.test(tier)) {
      record.tier = tier;
    }
  }
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

/* ------------------------------------------------------------------ */
/* Account platform: magic-link auth + per-account progress + certificates */
/* ------------------------------------------------------------------ */

var SESSION_COOKIE = "il_session";
var SESSION_TTL = 30 * 24 * 60 * 60; // 30 days, seconds
var MAGIC_TOKEN_TTL = 15 * 60; // 15 minutes, seconds
var MAGIC_THROTTLE_TTL = 60; // 60 seconds between requests per email
var MAX_PROGRESS_BYTES = 256 * 1024;

function randomHex(bytes) {
  var a = new Uint8Array(bytes);
  crypto.getRandomValues(a);
  var s = "";
  for (var i = 0; i < a.length; i++) {
    s += ("0" + a[i].toString(16)).slice(-2);
  }
  return s;
}

function getCookie(request, name) {
  var header = request.headers.get("cookie") || "";
  var parts = header.split(";");
  for (var i = 0; i < parts.length; i++) {
    var eq = parts[i].indexOf("=");
    if (eq < 0) continue;
    var k = parts[i].slice(0, eq).trim();
    if (k === name) {
      try {
        return decodeURIComponent(parts[i].slice(eq + 1).trim());
      } catch (e) {
        return parts[i].slice(eq + 1).trim();
      }
    }
  }
  return null;
}

function setSessionCookie(id) {
  return (
    SESSION_COOKIE +
    "=" +
    encodeURIComponent(id) +
    "; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=" +
    SESSION_TTL
  );
}

function clearSessionCookie() {
  return (
    SESSION_COOKIE +
    "=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0; Expires=Thu, 01 Jan 1970 00:00:00 GMT"
  );
}

async function readSession(request, env) {
  if (!env.IL_ACCOUNTS) return null;
  var sid = getCookie(request, SESSION_COOKIE);
  if (!sid || sid.length > 128 || !/^[A-Za-z0-9]+$/.test(sid)) return null;
  try {
    var raw = await env.IL_ACCOUNTS.get("sess:" + sid);
  } catch (e) {
    return null;
  }
  if (!raw) return null;
  try {
    var sess = JSON.parse(raw);
    if (!sess || !sess.email || !EMAIL_RE.test(sess.email)) return null;
    return sess;
  } catch (e) {
    return null;
  }
}

function requireAuthEnabled(env) {
  if (!env.IL_AUTH || !env.IL_ACCOUNTS) {
    return json({ ok: false, error: "accounts_unavailable" }, 503);
  }
  return null;
}

var MAIL_FROM = "noreply@interstitiumlabs.dev";
var MAIL_FROM_NAME = "Interstitium Labs";
var MAIL_SENDER_ID = "interstitiumlabs.dev";
// NOTE 2026-10-04: MailChannels' tx endpoint is currently rejecting sends
// (401 at their edge for this traffic). Documented fallback: site owner
// provisions a Resend API key, then swap this function to
// POST https://api.resend.com/emails with Authorization: Bearer <key>,
// { from, to, subject, text }. Do not invent another sender.

async function sendMagicLink(email, link) {
  var text =
    "Sign in to Interstitium Labs\n\n" +
    "Click this link to sign in (it expires in 15 minutes):\n\n" +
    link +
    "\n\n" +
    "If you didn't request this, you can safely ignore this email.\n\n" +
    "— Interstitium Labs · interstitiumlabs.dev";
  var payload = {
    personalizations: [{ to: [{ email: email }] }],
    from: { email: MAIL_FROM, name: MAIL_FROM_NAME },
    subject: "Your Interstitium Labs sign-in link",
    content: [{ type: "text/plain", value: text }],
  };
  var res;
  try {
    res = await fetch("https://api.mailchannels.net/tx/v1/send", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "X-MailChannels-Sender-Id": MAIL_SENDER_ID,
      },
      body: JSON.stringify(payload),
    });
  } catch (e) {
    return { ok: false, error: "mail_transport" };
  }
  if (res.status === 202) {
    return { ok: true };
  }
  var detail = "";
  try {
    detail = (await res.text()).slice(0, 400);
  } catch (e) {}
  return { ok: false, error: "mail_rejected", status: res.status, detail: detail };
}

async function handleAuthRequest(request, env) {
  var disabled = requireAuthEnabled(env);
  if (disabled) return disabled;
  if (request.method !== "POST") {
    return json({ ok: false, error: "method_not_allowed" }, 405);
  }
  var body;
  try {
    body = await request.json();
  } catch (e) {
    body = null;
  }
  var email =
    body && body.email != null ? String(body.email).trim().toLowerCase() : "";
  if (!email || email.length > 254 || !EMAIL_RE.test(email)) {
    return json({ ok: false, error: "email_invalid" }, 422);
  }
  // Per-email throttle: one request per 60s.
  try {
    var rlKey = "rl:" + email;
    if (await env.IL_AUTH.get(rlKey)) {
      return json({ ok: false, error: "too_many_requests" }, 429);
    }
    await env.IL_AUTH.put(rlKey, "1", { expirationTtl: MAGIC_THROTTLE_TTL });
  } catch (e) {
    return json({ ok: false, error: "store_unavailable" }, 503);
  }
  var token = randomHex(24);
  try {
    await env.IL_AUTH.put(
      "magic:" + token,
      JSON.stringify({ email: email, created_at: new Date().toISOString() }),
      { expirationTtl: MAGIC_TOKEN_TTL }
    );
  } catch (e) {
    return json({ ok: false, error: "store_unavailable" }, 503);
  }
  var url = new URL(request.url);
  var link = url.origin + "/api/auth/verify?token=" + token;
  var sent = await sendMagicLink(email, link);
  if (!sent.ok) {
    // Token stays usable for 15 minutes; report the send failure honestly
    // so the frontend can suggest retry / owner fallback.
    return json(
      { ok: false, error: "email_send_failed", reason: sent.error },
      502
    );
  }
  return json({ ok: true });
}

async function handleAuthVerify(request, env) {
  var disabled = requireAuthEnabled(env);
  if (disabled) return disabled;
  var url = new URL(request.url);
  var token = url.searchParams.get("token") || "";
  if (!token || token.length > 128 || !/^[a-f0-9]+$/.test(token)) {
    return json({ ok: false, error: "token_invalid" }, 400);
  }
  var raw;
  try {
    raw = await env.IL_AUTH.get("magic:" + token);
  } catch (e) {
    return json({ ok: false, error: "store_unavailable" }, 503);
  }
  if (!raw) {
    return json({ ok: false, error: "token_expired" }, 410);
  }
  var parsed;
  try {
    parsed = JSON.parse(raw);
  } catch (e) {
    parsed = null;
  }
  if (!parsed || !parsed.email || !EMAIL_RE.test(parsed.email)) {
    return json({ ok: false, error: "token_invalid" }, 400);
  }
  var email = parsed.email;
  // Single-use: burn the token before doing anything else.
  try {
    await env.IL_AUTH.delete("magic:" + token);
  } catch (e) {
    /* token already effectively dead; continue */
  }
  var sid = randomHex(32);
  var sess = {
    email: email,
    created_at: new Date().toISOString(),
    expires_at: new Date(Date.now() + SESSION_TTL * 1000).toISOString(),
  };
  try {
    await env.IL_ACCOUNTS.put("sess:" + sid, JSON.stringify(sess), {
      expirationTtl: SESSION_TTL,
    });
    // Account record: create on first sign-in (used by certificates + dashboard).
    var acctKey = "acct:" + email;
    var existing = await env.IL_ACCOUNTS.get(acctKey);
    if (!existing) {
      await env.IL_ACCOUNTS.put(
        acctKey,
        JSON.stringify({ email: email, created_at: sess.created_at })
      );
    }
  } catch (e) {
    return json({ ok: false, error: "store_unavailable" }, 503);
  }
  return new Response(null, {
    status: 303,
    headers: {
      "set-cookie": setSessionCookie(sid),
      location: new URL("/progress/", url.origin).toString(),
      "cache-control": "no-store",
    },
  });
}

async function handleMe(request, env) {
  var sess = await readSession(request, env);
  if (!sess) return json({ ok: false, error: "unauthorized" }, 401);
  return json({ ok: true, email: sess.email });
}

async function handleSignOut(request, env) {
  if (!env.IL_ACCOUNTS) {
    return json({ ok: false, error: "accounts_unavailable" }, 503);
  }
  var sid = getCookie(request, SESSION_COOKIE);
  if (sid && /^[A-Za-z0-9]+$/.test(sid)) {
    try {
      await env.IL_ACCOUNTS.delete("sess:" + sid);
    } catch (e) {}
  }
  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "set-cookie": clearSessionCookie(),
      "cache-control": "no-store",
    },
  });
}

function mergeProgress(base, incoming) {
  // base/incoming: { pathId: { ... } }. Merge per-path objects; top-level
  // scalar keys on incoming replace base. Arrays are replaced wholesale.
  var out = {};
  var k;
  for (k in base) {
    if (Object.prototype.hasOwnProperty.call(base, k)) out[k] = base[k];
  }
  for (k in incoming) {
    if (!Object.prototype.hasOwnProperty.call(incoming, k)) continue;
    var bv = out[k];
    var iv = incoming[k];
    if (
      bv &&
      iv &&
      typeof bv === "object" &&
      typeof iv === "object" &&
      !Array.isArray(bv) &&
      !Array.isArray(iv)
    ) {
      var merged = {};
      var j;
      for (j in bv) {
        if (Object.prototype.hasOwnProperty.call(bv, j)) merged[j] = bv[j];
      }
      for (j in iv) {
        if (Object.prototype.hasOwnProperty.call(iv, j)) merged[j] = iv[j];
      }
      out[k] = merged;
    } else {
      out[k] = iv;
    }
  }
  return out;
}

async function handleProgress(request, env, sess) {
  var key = "prog:" + sess.email;
  if (request.method === "GET") {
    var raw = null;
    try {
      raw = await env.IL_ACCOUNTS.get(key);
    } catch (e) {
      return json({ ok: false, error: "store_unavailable" }, 503);
    }
    var data = {};
    if (raw) {
      try {
        data = JSON.parse(raw) || {};
      } catch (e) {
        data = {};
      }
    }
    return json({ ok: true, progress: data, updated_at: data.__updated_at || null });
  }
  if (request.method === "PUT") {
    var len = request.headers.get("content-length");
    if (len && parseInt(len, 10) > MAX_PROGRESS_BYTES) {
      return json({ ok: false, error: "payload_too_large" }, 413);
    }
    var body;
    try {
      body = await request.json();
    } catch (e) {
      return json({ ok: false, error: "bad_json" }, 422);
    }
    var incoming =
      body && body.progress && typeof body.progress === "object" && !Array.isArray(body.progress)
        ? body.progress
        : null;
    if (!incoming) {
      return json({ ok: false, error: "progress_required" }, 422);
    }
    var existing = {};
    try {
      var eraw = await env.IL_ACCOUNTS.get(key);
      if (eraw) existing = JSON.parse(eraw) || {};
    } catch (e) {
      return json({ ok: false, error: "store_unavailable" }, 503);
    }
    var merged = mergeProgress(existing, incoming);
    merged.__updated_at = new Date().toISOString();
    try {
      var payload = JSON.stringify(merged);
      if (payload.length > MAX_PROGRESS_BYTES) {
        return json({ ok: false, error: "payload_too_large" }, 413);
      }
      await env.IL_ACCOUNTS.put(key, payload);
    } catch (e) {
      return json({ ok: false, error: "store_unavailable" }, 503);
    }
    return json({ ok: true, progress: merged, updated_at: merged.__updated_at });
  }
  return json({ ok: false, error: "method_not_allowed" }, 405);
}

async function handleIssueCertificate(request, env, sess) {
  if (request.method !== "POST") {
    return json({ ok: false, error: "method_not_allowed" }, 405);
  }
  var body;
  try {
    body = await request.json();
  } catch (e) {
    body = null;
  }
  var pathId = body && body.path != null ? String(body.path).trim() : "";
  if (!pathId || pathId.length > 120 || !/^[A-Za-z0-9][A-Za-z0-9 _./-]*$/.test(pathId)) {
    return json({ ok: false, error: "path_required" }, 422);
  }
  var id = "cert-" + randomHex(12);
  var cert = {
    id: id,
    path: pathId,
    email: sess.email,
    issued_at: new Date().toISOString(),
  };
  try {
    await env.IL_ACCOUNTS.put("cert:" + id, JSON.stringify(cert));
    // Append to the account's certificate list for the /certificates/ page.
    var listKey = "certs:" + sess.email;
    var list = [];
    try {
      var lraw = await env.IL_ACCOUNTS.get(listKey);
      if (lraw) list = JSON.parse(lraw) || [];
    } catch (e) {}
    if (!Array.isArray(list)) list = [];
    list.push(cert);
    await env.IL_ACCOUNTS.put(listKey, JSON.stringify(list));
  } catch (e) {
    return json({ ok: false, error: "store_unavailable" }, 503);
  }
  return json({ ok: true, certificate: cert });
}

async function handleVerifyCertificate(request, env) {
  if (!env.IL_ACCOUNTS) {
    return json({ ok: false, error: "accounts_unavailable" }, 503);
  }
  var url = new URL(request.url);
  var id = url.searchParams.get("id") || "";
  if (!id || id.length > 80 || !/^cert-[a-f0-9]+$/.test(id)) {
    return json({ ok: false, error: "id_invalid" }, 422);
  }
  var raw;
  try {
    raw = await env.IL_ACCOUNTS.get("cert:" + id);
  } catch (e) {
    return json({ ok: false, error: "store_unavailable" }, 503);
  }
  if (!raw) {
    return json({ ok: false, error: "not_found" }, 404);
  }
  var cert;
  try {
    cert = JSON.parse(raw);
  } catch (e) {
    return json({ ok: false, error: "not_found" }, 404);
  }
  return json({ ok: true, certificate: cert });
}

async function handleListCertificates(request, env, sess) {
  if (request.method !== "GET") {
    return json({ ok: false, error: "method_not_allowed" }, 405);
  }
  var list = [];
  try {
    var lraw = await env.IL_ACCOUNTS.get("certs:" + sess.email);
    if (lraw) list = JSON.parse(lraw) || [];
  } catch (e) {
    return json({ ok: false, error: "store_unavailable" }, 503);
  }
  if (!Array.isArray(list)) list = [];
  return json({ ok: true, certificates: list });
}

/* ------------------------------------------------------------------ */

/* ------------------------------------------------------------------
 * Noah AI tutor backend (merged 2026-10-06 from the retired
 * interstitium-labs-university worker on learn.interstitiumlabs.dev).
 *   POST /api/noah       Socratic tutor chat via Workers AI.
 *   POST /api/noah-stats Privacy-respecting usage aggregates -> KV NOAH_STATS.
 *   GET  /api/noah-stats Coarse public aggregates for iteration.
 * Helpers are noah*-prefixed to avoid colliding with the flagship's own
 * json()/routing helpers above.
 * ------------------------------------------------------------------ */

/* =====================================================================
 * Interstitium Labs Learning University — Worker
 *
 * Static assets + Noah AI endpoint.
 *  - All non-API traffic -> static assets (existing site, unchanged).
 *  - POST /api/noah -> proxied chat completion via Workers AI.
 *    CORS-enabled for https://interstitiumlabs.dev (apex widget).
 *  - POST /api/noah-stats -> privacy-respecting usage aggregates
 *    (counters only, no message text, no PII) into KV (NOAH_STATS).
 *    GET /api/noah-stats -> coarse public aggregates for iteration.
 * ===================================================================== */

const NOAH_MODEL = '@cf/meta/llama-3.3-70b-instruct-fp8-fast';
const KNOWLEDGE_PATH = '/university/data/noah-knowledge.md';
const MAX_MSGS = 20;
const MAX_CHARS_PER_MSG = 4000;
const MAX_TOKENS = 900;
const RATE_WINDOW_MS = 60_000;
const RATE_MAX = 15;

let knowledgeCache = null;
const rateMap = new Map();

function noahCors(resp, origin) {
  const h = new Headers(resp.headers);
  h.set('Access-Control-Allow-Origin', origin);
  h.set('Access-Control-Allow-Methods', 'POST, OPTIONS');
  h.set('Access-Control-Allow-Headers', 'Content-Type');
  h.set('Vary', 'Origin');
  return new Response(resp.body, { status: resp.status, headers: h });
}

function noahJson(obj, status, origin) {
  return noahCors(
    new Response(JSON.stringify(obj), {
      status,
      headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
    }),
    origin
  );
}

function noahAllowedOrigin(request) {
  const o = request.headers.get('Origin') || '';
  const self = new URL(request.url).origin;
  if (o === self) return o;
  if (o === 'https://interstitiumlabs.dev' || o === 'https://www.interstitiumlabs.dev') return o;
  return self; // default: same-origin only
}

function rateLimited(ip) {
  const now = Date.now();
  let rec = rateMap.get(ip);
  if (!rec || now - rec.start > RATE_WINDOW_MS) {
    rec = { start: now, count: 0 };
    rateMap.set(ip, rec);
  }
  rec.count += 1;
  if (rateMap.size > 5000) rateMap.clear();
  return rec.count > RATE_MAX;
}

async function loadKnowledge(env, request) {
  if (knowledgeCache) return knowledgeCache;
  try {
    const res = await env.ASSETS.fetch(new URL(KNOWLEDGE_PATH, request.url));
    if (res.ok) {
      knowledgeCache = await res.text();
      return knowledgeCache;
    }
  } catch (e) { /* fall through to empty */ }
  knowledgeCache = '';
  return '';
}

function sanitizeMessages(raw) {
  if (!Array.isArray(raw)) return null;
  const out = [];
  for (const m of raw.slice(-MAX_MSGS)) {
    if (!m || (m.role !== 'user' && m.role !== 'assistant')) return null;
    const content = String(m.content == null ? '' : m.content).slice(0, MAX_CHARS_PER_MSG);
    if (!content.trim()) continue;
    out.push({ role: m.role, content });
  }
  return out.length ? out : null;
}

async function handleNoah(request, env) {
  const origin = noahAllowedOrigin(request);

  if (!env.AI) {
    return noahJson({ error: 'AI unavailable', fallback: true }, 503, origin);
  }

  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  if (rateLimited(ip)) {
    return noahJson({ error: 'Rate limited. Try again shortly.', fallback: true }, 429, origin);
  }

  let body;
  try {
    body = await request.json();
  } catch (e) {
    return noahJson({ error: 'Invalid JSON body.' }, 400, origin);
  }

  const messages = sanitizeMessages(body.messages);
  if (!messages) {
    return noahJson({ error: 'Provide messages: [{role, content}].' }, 400, origin);
  }

  const knowledge = await loadKnowledge(env, request);
  const system =
    'You are Noah AI, the resident intelligence of Interstitium Labs — ' +
    'the personal AI of founder Enmanuel D. Mejia, living on interstitiumlabs.dev, ' +
    'learn.interstitiumlabs.dev, and the Interstitium Labs mobile apps. ' +
    'Your name is Noah AI. Never claim to be Muse, Meta AI, or any other assistant.\n\n' +
    'PRIMARY MISSION — personalized adaptive tutor. You adapt to each learner: ' +
    'infer their level (novice / intermediate / advanced) from their vocabulary, ' +
    'questions, and attempts, then calibrate depth, jargon, and pacing to match. ' +
    'Notice what they already grasp and skip it; dwell where they stumble. ' +
    'Remember what they tell you within the conversation — their goal (a cert, ' +
    'an interview, a course, a project), their background, what they have tried — ' +
    'and refer back to it explicitly: "last time you got stuck on X, let\'s build on that." ' +
    'Keep a running mental model of the session: goal, background, attempts, what worked. ' +
    'Restate it when relevant ("on your second attempt at the subnetting drill you nailed the mask but slipped on the broadcast — here is why"). ' +
    'This memory is conversation-scoped: it ends when the session ends.\n\n' +
    'LEARNING STYLE — detect how they learn from interaction signals: terse vs verbose ' +
    'replies; code-first vs concept-first vs example-first questions; requests for diagrams ' +
    'or analogies; trial-and-error attempts vs read-first behavior. Match their style: ' +
    'concise answers for the terse, worked examples for the example-first, code before prose ' +
    'for the code-first, an ASCII sketch when they ask to see it. Keep re-detecting as ' +
    'signals accumulate — styles drift, and so should your strategy.\n\n' +
    'DOCTRINE (Socratic): when the visitor is learning, guide before telling. ' +
    'Acknowledge their hypothesis, ask ONE sharp guiding question, offer the next ' +
    'smallest step. Never dump a full worked answer first when they are studying. ' +
    'Diagnose the misconception behind a wrong answer and repair the mental model, ' +
    'not just the answer. Give graduated hints on request; check understanding ' +
    'with one quick practice question before moving on. Celebrate real progress ' +
    'specifically ("your subnetting is clean now — that was the hard part"); ' +
    'normalize struggle, never shame it. If they plainly ask for a direct answer ' +
    'outside a study context, answer directly and well.\n\n' +
    'PACING — set one explicit micro-goal at the start of each study session ("by the end of this you will ..."). ' +
    'Check mastery with ONE question before advancing; move on only when they show understanding. ' +
    'At every checkpoint offer three branches: go deeper, move on, or review. Never race ahead of them.\n\n' +
    'LAB COACHING — for hands-on work, never paste a full solution first. Diagnose: ask what they tried, ' +
    'what they expected, what actually happened. Hint in graduated steps: a nudge, then a stronger nudge, ' +
    'then a worked sketch of the missing piece; the full solution only when they are still stuck. ' +
    'When they show you an attempt, review it: name what is right before what is wrong, and repair ' +
    'the reasoning, not just the code.\n\n' +
    'BEYOND TUTORING you are a complete assistant. Answer questions about the full course ' +
    'catalog — recommend academies and paths BY CODE (e.g. IL-11) and cite the catalog code when you do. ' +
    'Navigate visitors to the right page; help with writing, planning, and technical problems. ' +
    'For code: explain and debug by careful reasoning, but be honest that you cannot execute code — ' +
    'say so before reasoning about what it will do, and verify claims by tracing, not asserting. ' +
    'For career questions about Enmanuel: ground every claim ONLY in his real materials — his resume, ' +
    'his projects, this knowledge base. Never invent credentials, employers, salaries, offers, or ' +
    'outcomes for him or the visitor. Anything a capable personal AI would do, within the honesty rules below.\n\n' +
    'ITERATION — a privacy-respecting pipeline records only counters of how this chat is used ' +
    '(opens, asks, fallbacks; never message text). When the conversation itself shows stuck signals — ' +
    'the same topic asked repeatedly, escalating hint requests, circling one concept — name it briefly ' +
    'and invite a check question or a different angle. Sparingly: at most one such nudge per session. ' +
    'These moments feed the weekly human review that improves you.\n\n' +
    'VOICE: measured, precise, warm but never gushing. Latin sparingly. No hype, ' +
    'no emojis. Short paragraphs. Use simple markdown (bold, lists, code spans) ' +
    'where it aids clarity.\n\n' +
    'SCOPE: you speak from the knowledge base below — Enmanuel\'s projects, code, ' +
    'the Learning University curriculum, the mobile apps, and the Interstitium Labs sites. ' +
    'Recommend specific academies/paths by code (e.g. IL-11) when relevant. ' +
    'If asked about something outside the knowledge base, say so plainly and help ' +
    'from general knowledge, marked as general. Never invent credentials, ' +
    'experience, certifications, or project details — for Enmanuel or the visitor.\n\n' +
    'KNOWLEDGE BASE:\n' + (knowledge || '(knowledge base unavailable — answer from general knowledge and say so.)');

  try {
    const aiMessages = [{ role: 'system', content: system }, ...messages];
    const result = await env.AI.run(NOAH_MODEL, {
      messages: aiMessages,
      max_tokens: MAX_TOKENS,
      temperature: 0.6,
    });
    const reply =
      (result && result.response ? String(result.response) : '').trim() ||
      'I could not compose a reply just now. Try again, or ask the local Socratic engine below.';
    return noahJson({ reply }, 200, origin);
  } catch (e) {
    return noahJson({ error: 'AI request failed.', fallback: true }, 502, origin);
  }
}

/* ---- Noah stats: privacy-respecting usage aggregates ----
   POST /api/noah-stats { v:1, sid, platform, agg:{ opens, asks, remotes,
   fallbacks, nudges, chips, errors, byTopic } } -> 204.
   Counters only; never message text, never PII. Stored per-day plus a
   global rollup in KV (binding NOAH_STATS). GET returns coarse public
   aggregates consumed by the weekly autonomous-iteration review. */
const STAT_KEYS = ['opens', 'asks', 'remotes', 'fallbacks', 'nudges', 'chips', 'errors'];

function freshAgg() {
  return { opens: 0, asks: 0, remotes: 0, fallbacks: 0, nudges: 0, chips: 0, errors: 0, byTopic: {} };
}

function dayKey(d) { return 'stats:day:' + d.toISOString().slice(0, 10); }

function sanitizeAgg(a) {
  if (!a || typeof a !== 'object') return null;
  const out = {};
  for (const k of STAT_KEYS) {
    const n = Number(a[k]);
    out[k] = Number.isFinite(n) && n >= 0 ? Math.min(Math.floor(n), 10000) : 0;
  }
  out.byTopic = {};
  if (a.byTopic && typeof a.byTopic === 'object') {
    for (const t of Object.keys(a.byTopic).slice(0, 40)) {
      if (/^[a-z-]{1,24}$/.test(t)) {
        const n = Number(a.byTopic[t]);
        if (Number.isFinite(n) && n > 0) out.byTopic[t] = Math.min(Math.floor(n), 10000);
      }
    }
  }
  return out;
}

function mergeAgg(base, d) {
  const out = Object.assign(freshAgg(), base, { byTopic: {} });
  for (const k of STAT_KEYS) out[k] = (Number(base[k]) || 0) + (d[k] || 0);
  const bt = (base.byTopic && typeof base.byTopic === 'object') ? base.byTopic : {};
  for (const t of Object.keys(bt)) out.byTopic[t] = bt[t];
  for (const t of Object.keys(d.byTopic)) out.byTopic[t] = (out.byTopic[t] || 0) + d.byTopic[t];
  return out;
}

async function handleNoahStats(request, env) {
  const origin = noahAllowedOrigin(request);
  if (request.method === 'OPTIONS') {
    return noahCors(new Response(null, { status: 204 }), origin);
  }
  if (request.method === 'POST') {
    let body = null;
    try { body = await request.json(); } catch (e) { return noahJson({ error: 'Bad JSON.' }, 400, origin); }
    if (!body || body.v !== 1) return noahJson({ error: 'Bad version.' }, 400, origin);
    const d = sanitizeAgg(body.agg);
    if (!d) return noahJson({ error: 'Bad aggregate.' }, 400, origin);
    const ip = request.headers.get('CF-Connecting-IP') || 'x';
    if (rateLimited('stats:' + ip)) return noahCors(new Response(null, { status: 429 }), origin);
    if (env.NOAH_STATS) {
      try {
        const day = dayKey(new Date());
        const cur = (await env.NOAH_STATS.get(day, 'json')) || freshAgg();
        await env.NOAH_STATS.put(day, JSON.stringify(mergeAgg(cur, d)));
        const g = (await env.NOAH_STATS.get('stats:global', 'json')) || freshAgg();
        await env.NOAH_STATS.put('stats:global', JSON.stringify(mergeAgg(g, d)));
      } catch (e) {
        console.log('noah-stats kv error: ' + (e && e.message));
      }
    } else {
      console.log('noah-stats (no KV): ' + JSON.stringify(d));
    }
    return noahCors(new Response(null, { status: 204 }), origin);
  }
  if (request.method === 'GET') {
    const out = { global: freshAgg(), days: [] };
    if (env.NOAH_STATS) {
      try {
        out.global = (await env.NOAH_STATS.get('stats:global', 'json')) || freshAgg();
        for (let i = 0; i < 7; i++) {
          const k = dayKey(new Date(Date.now() - i * 864e5));
          const v = await env.NOAH_STATS.get(k, 'json');
          if (v) out.days.push(Object.assign({ day: k.slice(10) }, v));
        }
      } catch (e) { /* serve empty aggregates */ }
    }
    return noahJson(out, 200, origin);
  }
  return noahJson({ error: 'Use GET or POST.' }, 405, origin);
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
    // 2026-10-06: consolidated redirect stubs (zero-value stub dirs removed)
    var STUB_REDIRECTS = {
      "/code": "/prep/programming/", "/command": "/paths/",
      "/desk": "/learn/", "/doctrine": "/about/",
      "/drill": "/prep/drills/", "/factory": "/labs/",
      "/field": "/learn/", "/graph": "/learn/skills/",
      "/interview": "/prep/drills/", "/library": "/learn/",
      "/measure": "/learn/", "/plant": "/paths/",
      "/platform": "/about/", "/portfolio": "/labs/superlab/",
      "/pricing": "/enroll/", "/radar": "/trending/",
      "/sheets": "/prep/", "/si": "/learn/",
      "/system": "/about/"
    };
    var stubTarget = STUB_REDIRECTS[path.replace(/\/$/, "")];
    if (stubTarget) {
      return movedPermanently(request, stubTarget);
    }
    if (path === "/api/waitlist") {
      if (!env.WAITLIST) {
        return json({ ok: false, error: "store_unavailable" }, 503);
      }
      return handleWaitlist(request, env);
    }
    if (path === "/api/auth/request") {
      return handleAuthRequest(request, env);
    }
    if (path === "/api/auth/verify") {
      return handleAuthVerify(request, env);
    }
    if (path === "/api/me") {
      return handleMe(request, env);
    }
    if (path === "/api/auth/signout") {
      return handleSignOut(request, env);
    }
    if (path === "/api/progress") {
      var sess = await readSession(request, env);
      if (!sess) return json({ ok: false, error: "unauthorized" }, 401);
      return handleProgress(request, env, sess);
    }
    if (path === "/api/certificates/issue") {
      var csess = await readSession(request, env);
      if (!csess) return json({ ok: false, error: "unauthorized" }, 401);
      return handleIssueCertificate(request, env, csess);
    }
    if (path === "/api/certificates") {
      var lsess = await readSession(request, env);
      if (!lsess) return json({ ok: false, error: "unauthorized" }, 401);
      return handleListCertificates(request, env, lsess);
    }
    if (path === "/api/certificates/verify") {
      return handleVerifyCertificate(request, env);
    }

    if (path === "/api/noah-stats") {
      return handleNoahStats(request, env);
    }
    if (path === "/api/noah") {
      if (request.method === "OPTIONS") {
        return noahCors(new Response(null, { status: 204 }), noahAllowedOrigin(request));
      }
      if (request.method !== "POST") {
        var noahOrigin = noahAllowedOrigin(request);
        return noahCors(noahJson({ error: "Use POST." }, 405, noahOrigin), noahOrigin);
      }
      return handleNoah(request, env);
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
