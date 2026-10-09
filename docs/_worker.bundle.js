// payment-routes.js
/**
 * Interstitium Labs — payment layer (Phase 4b).
 *
 * Imported by docs/_worker.js (single-file _worker.js is bundled by wrangler,
 * so relative imports resolve at build time).
 *
 * Providers:
 *   stripe      — Checkout Sessions (cards + Apple Pay + Google Pay via
 *               Stripe Checkout automatically). Webhook: checkout.session.*
 *   paypal      — Orders API v2 (Venmo is selectable inside PayPal Checkout).
 *               Webhooks verified via PayPal's verify-webhook-signature API.
 *   nowpayments — Hosted invoice (all 11 coins). IPN verified with
 *               HMAC-SHA512 over recursively key-sorted JSON (x-nowpayments-sig).
 *   direct      — Direct-wallet fallback: per-coin address + QR rendered by
 *               the checkout UI. Addresses resolve from the Unstoppable Domain
 *               `enmanuelmejia.crypto` (UD Resolution API) with per-coin
 *               WALLET_* env fallback. XRP destination-tag / XLM memo
 *               supported via XRP_DESTINATION_TAG / XLM_MEMO.
 *
 * Storage: order + entitlement records live in the IL_ACCOUNTS KV binding
 * (already bound in wrangler.jsonc) under `pay:` key prefixes. When no KV
 * binding is present (local test), an in-memory Map is used instead —
 * documented as NOT durable; production requires IL_ACCOUNTS.
 *
 * Secrets: EVERYTHING is read from env at request time. No key, token,
 * webhook secret, or wallet address is hardcoded anywhere in this file.
 * Required env (see PAYMENTS-SETUP.md):
 *   STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
 *   PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, PAYPAL_WEBHOOK_ID, PAYPAL_SANDBOX
 *   NOWPAYMENTS_API_KEY, NOWPAYMENTS_IPN_SECRET, NOWPAYMENTS_SANDBOX
 *   WALLET_XRP, WALLET_XLM, WALLET_ADA, WALLET_ALGO, WALLET_QNT,
 *   WALLET_HBAR, WALLET_IOTA, WALLET_XDC, WALLET_XMR, WALLET_BTC
 *   XRP_DESTINATION_TAG, XLM_MEMO
 *   ENTITLEMENT_SECRET  (HMAC key for the il_entitlement cookie — REQUIRED for the paywall)
 *   ADMIN_TOKEN         (owner-only token for the manual admin-confirm hook)
 *
 * Direct-wallet honesty model (2026-10-08): there is NO automatic on-chain
 * watcher. Direct-wallet orders accept a buyer-submitted tx hash
 * (POST /api/pay/tx/submit) and stay PENDING until the owner verifies the
 * transfer manually and calls the admin hook
 * (POST /api/pay/admin/confirm). After ANY paid order, the client calls
 * POST /api/pay/entitlement {order} to receive the signed il_entitlement
 * cookie the course paywall checks.
 */

"use strict";

/* ---------------- catalog: server-side price authority ---------------- */
/* Client-submitted amounts are NEVER trusted; the item id maps to a price
   here. Tiers mirror docs/enroll/config.js publishable prices. */

var ITEMS = {
  "prep-sprint": { name: "Prep Sprint", amount_cents: 14900, kind: "tier" },
  "devsecops-mastery": { name: "DevSecOps Mastery", amount_cents: 49900, kind: "tier" },
  "full-academy": { name: "Full Academy", amount_cents: 79900, kind: "tier" },
};

/* ---------------- course paywall pricing (2026-10-08) ---------------- */
/* PAYWALL_CONFIG — RESEARCHED PRICES (market analysis 2026-10-08).
   $249/course: below CompTIA CertMaster Learn ($599 list), below Dion's
   premium bundle ($349), far above Udemy impulse pricing ($15-30 video-only);
   buys 400+ honest hours of interactive sim content per course — a depth no
   competitor sells at consumer prices. Accessible for a price-sensitive
   audience (career changers, students), credible for the depth.
   $999 bundle: 26 courses x $249 = $6,474 sticker; $999 ~= 85% off
   ("everything for the price of 4 courses"). Positioned below OffSec Learn
   One ($2,749/yr) and HTB Academy Gold ($1,400/yr), above mass-market subs
   (TCM $300/yr, DataCamp ~$165-330/yr) — premium, one-time lifetime, no
   subscription tier (solo operator; keep it operable).
   The free courses IL-27 / IL-28 / IL-29 are NOT in this catalog and are never gated. */
var PAYWALL_CONFIG = {
  default_course_price_cents: 24900, // $249 per course (researched 2026-10-08)
  all_courses_bundle_cents: 99900,   // $999 all-access bundle (researched 2026-10-08)
};

var COURSES = [
  { slug: "il-01-esoteric-foundations", code: "IL-01", title: "Esoteric Foundations" },
  { slug: "il-02-mathematical-maturity-engine", code: "IL-02", title: "Mathematical Maturity Engine" },
  { slug: "il-03-programming-language-forge", code: "IL-03", title: "Programming Language Forge" },
  { slug: "il-04-systems-linux-windows-networks", code: "IL-04", title: "Systems, Linux, Windows & Networks" },
  { slug: "il-05-cloud-devsecops-platform-sre", code: "IL-05", title: "Cloud, DevSecOps, Platform & SRE" },
  { slug: "il-06-cybersecurity-secure-engineering", code: "IL-06", title: "Cybersecurity & Secure Engineering" },
  { slug: "il-07-data-engineering-analytics-ai", code: "IL-07", title: "SQL, Data Engineering, Analytics & AI" },
  { slug: "il-08-algorithms-compilers-distributed-formal", code: "IL-08", title: "Algorithms, Compilers, Distributed & Formal" },
  { slug: "il-09-adaptive-certification-command", code: "IL-09", title: "Adaptive Certification Command" },
  { slug: "il-10-portfolio-career-professional-practice", code: "IL-10", title: "Portfolio, Career & Professional Practice" },
  { slug: "il-11-zero-trust-endpoint-defense", code: "IL-11", title: "Zero Trust & Endpoint Defense" },
  { slug: "il-12-ai-engineering", code: "IL-12", title: "AI Engineering" },
  { slug: "il-13-software-engineering-interview-prep", code: "IL-13", title: "Software Engineering Interview Prep" },
  { slug: "il-14-sre-devops-cloud-security-interview-prep", code: "IL-14", title: "SRE, DevOps, Cloud & Security Interview Prep" },
  { slug: "il-15-data-engineering-analytics-interview-prep", code: "IL-15", title: "Data Engineering & Analytics Interview Prep" },
  { slug: "il-16-machine-learning-ai-engineering", code: "IL-16", title: "Machine Learning & AI Engineering" },
  { slug: "il-17-agentic-ai-engineering", code: "IL-17", title: "Agentic AI Engineering" },
  { slug: "il-18-technical-leadership-interview-prep", code: "IL-18", title: "Technical Leadership Interview Prep" },
  { slug: "il-19-multicloud-devops-ai-bootcamp", code: "IL-19", title: "MultiCloud, DevOps & AI Bootcamp" },
  { slug: "il-20-mathematics", code: "IL-20", title: "Mathematics for Engineers & Scientists" },
  { slug: "il-21-humanities", code: "IL-21", title: "Humanities for Technologists" },
  { slug: "il-22-esoteric-secret-knowledge", code: "IL-22", title: "The Deep Library — Esoteric & Secret Knowledge" },
  { slug: "il-23-frontier-knowledge", code: "IL-23", title: "The Frontier — Cutting-Edge Research Distilled" },
  { slug: "il-24-threatlocker-assessment-prep-cbt", code: "IL-24", title: "ThreatLocker Assessment Prep CBT" },
  { slug: "il-25-cybersecurity-professional-certificate", code: "IL-25", title: "IL-25 · Professional Certificate in Cybersecurity" },
  { slug: "il-26-data-analyst-certification-senior-mastery", code: "IL-26", title: "IL-26 · Data Analyst Certification & Senior Mastery Bootcamp" },
];

for (var ci = 0; ci < COURSES.length; ci++) {
  var c0 = COURSES[ci];
  ITEMS[c0.slug] = {
    name: c0.code + " · " + c0.title,
    amount_cents: PAYWALL_CONFIG.default_course_price_cents,
    kind: "course",
  };
}
ITEMS["all-courses"] = {
  name: "All Courses Bundle (IL-01–IL-26)",
  amount_cents: PAYWALL_CONFIG.all_courses_bundle_cents,
  kind: "bundle",
};

function courseItemSlugs() {
  var out = [];
  for (var k in ITEMS) {
    if (Object.prototype.hasOwnProperty.call(ITEMS, k) && ITEMS[k].kind === "course") out.push(k);
  }
  return out;
}

var CURRENCY = "usd";
var UD_DOMAIN = "enmanuelmejia.crypto";
var UD_RESOLVE_URL = "https://resolve.unstoppabledomains.com/domains/";
var UD_CACHE_TTL = 24 * 60 * 60; // 24h, seconds

/* ---------------- USER_CONFIG: owner-provided wallet setup ---------------- */
/* The user (site owner) fills these in. Empty string = not provided. These
   are read at REQUEST time from this object, falling back BELOW env
   WALLET_* vars and the enmanuelmejia.crypto Unstoppable Domain records.
   Resolution priority: UD records -> env vars -> USER_CONFIG below.
   NEVER invent addresses here. */
var USER_CONFIG = {
  BTC_ADDRESS: "",
  XRP_ADDRESS: "",
  XRP_DESTINATION_TAG: "", /* required for XRP deposits to a shared/exchange address */
  XLM_ADDRESS: "",
  XLM_MEMO: "",           /* required for XLM deposits to a shared/exchange address */
  ADA_ADDRESS: "",
  ALGO_ADDRESS: "",
  QNT_ADDRESS: "",
  HBAR_ADDRESS: "",
  IOTA_ADDRESS: "",
  XDC_ADDRESS: "",
  XMR_ADDRESS: "",
};

/* 11-coin rail. pay_currency = NOWPayments code (lowercase),
   ud_key = Unstoppable Domains record key, env_key = WALLET_* fallback,
   extra  = which env holds the destination tag / memo for this coin. */
var COINS = [
  { code: "XRP",  name: "XRP (Ripple)",       pay_currency: "xrp",  ud_key: "crypto.XRP.address",  env_key: "WALLET_XRP",  user_key: "XRP_ADDRESS",  extra: "XRP_DESTINATION_TAG", extra_user_key: "XRP_DESTINATION_TAG", extra_label: "Destination tag" },
  { code: "XLM",  name: "Stellar Lumens",     pay_currency: "xlm",  ud_key: "crypto.XLM.address",  env_key: "WALLET_XLM",  user_key: "XLM_ADDRESS",  extra: "XLM_MEMO",            extra_user_key: "XLM_MEMO",            extra_label: "Memo" },
  { code: "ADA",  name: "Cardano",            pay_currency: "ada",  ud_key: "crypto.ADA.address",  env_key: "WALLET_ADA",  user_key: "ADA_ADDRESS" },
  { code: "ALGO", name: "Algorand",           pay_currency: "algo", ud_key: "crypto.ALGO.address", env_key: "WALLET_ALGO", user_key: "ALGO_ADDRESS" },
  { code: "QNT",  name: "Quant",              pay_currency: "qnt",  ud_key: "crypto.QNT.address",  env_key: "WALLET_QNT",  user_key: "QNT_ADDRESS" },
  { code: "HBAR", name: "Hedera",             pay_currency: "hbar", ud_key: "crypto.HBAR.address", env_key: "WALLET_HBAR", user_key: "HBAR_ADDRESS" },
  { code: "IOTA", name: "IOTA",               pay_currency: "iota", ud_key: "crypto.IOTA.address", env_key: "WALLET_IOTA", user_key: "IOTA_ADDRESS" },
  { code: "XDC",  name: "XDC Network",        pay_currency: "xdc",  ud_key: "crypto.XDC.address",  env_key: "WALLET_XDC",  user_key: "XDC_ADDRESS" },
  { code: "XMR",  name: "Monero",             pay_currency: "xmr",  ud_key: "crypto.XMR.address",  env_key: "WALLET_XMR",  user_key: "XMR_ADDRESS" },
  { code: "BTC",  name: "Bitcoin",            pay_currency: "btc",  ud_key: "crypto.BTC.address",  env_key: "WALLET_BTC",  user_key: "BTC_ADDRESS" },
];

function coinByCode(code) {
  code = String(code || "").toUpperCase();
  for (var i = 0; i < COINS.length; i++) {
    if (COINS[i].code === code) return COINS[i];
  }
  return null;
}

var PROVIDERS = ["stripe", "paypal", "nowpayments", "direct"];
var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/* ---------------- tiny helpers ---------------- */

function payJson(data, status) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function randHex(n) {
  var a = new Uint8Array(n);
  crypto.getRandomValues(a);
  var s = "";
  for (var i = 0; i < a.length; i++) s += ("0" + a[i].toString(16)).slice(-2);
  return s;
}

function nowIso() {
  return new Date().toISOString();
}

async function hmacHex(algo, keyStr, msgStr) {
  var enc = new TextEncoder();
  var key = await crypto.subtle.importKey(
    "raw",
    enc.encode(keyStr),
    { name: "HMAC", hash: algo },
    false,
    ["sign"]
  );
  var sig = await crypto.subtle.sign("HMAC", key, enc.encode(msgStr));
  var b = new Uint8Array(sig);
  var out = "";
  for (var i = 0; i < b.length; i++) out += ("0" + b[i].toString(16)).slice(-2);
  return out;
}

/* Best-effort constant-time string compare (hex digests). */
function safeEqual(a, b) {
  a = String(a || "");
  b = String(b || "");
  if (a.length !== b.length) return false;
  var diff = 0;
  for (var i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function safeEqualBytes(a, b) {
  if (!(a instanceof Uint8Array) || !(b instanceof Uint8Array)) return false;
  if (a.length !== b.length) return false;
  var diff = 0;
  for (var i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
  return diff === 0;
}

/* ---------------- base64url ---------------- */

function b64uEncodeBytes(bytes) {
  var bin = "";
  for (var i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function b64uEncode(str) {
  return b64uEncodeBytes(new TextEncoder().encode(String(str)));
}

function b64uDecodeBytes(s) {
  var b64 = String(s || "").replace(/-/g, "+").replace(/_/g, "/");
  while (b64.length % 4) b64 += "=";
  var bin = atob(b64);
  var out = new Uint8Array(bin.length);
  for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

function b64uDecodeToString(s) {
  return new TextDecoder().decode(b64uDecodeBytes(s));
}

async function hmacRaw(algo, keyStr, msgStr) {
  var enc = new TextEncoder();
  var key = await crypto.subtle.importKey(
    "raw",
    enc.encode(keyStr),
    { name: "HMAC", hash: algo },
    false,
    ["sign"]
  );
  return new Uint8Array(await crypto.subtle.sign("HMAC", key, enc.encode(msgStr)));
}

/* ---------------- course entitlement tokens ---------------- */
/* Cookie contract for the course paywall (_worker.js):
     token = base64url(payload) + "." + base64url(HMAC-SHA256(secret, base64url(payload)))
     payload = { course: "<slug>" | "all-courses", iat, exp }
   The secret comes ONLY from env.ENTITLEMENT_SECRET — never hardcoded.
   Callers must fail closed when the secret is unset. */

var ENTITLEMENT_COOKIE = "il_entitlement";
var ENTITLEMENT_TTL = 365 * 24 * 60 * 60; // 1 year, seconds

async function signEntitlement(secret, courseScope) {
  var nowS = Math.floor(Date.now() / 1000);
  var payload = {
    course: String(courseScope),
    iat: nowS,
    exp: nowS + ENTITLEMENT_TTL,
  };
  var body = b64uEncode(JSON.stringify(payload));
  var sig = b64uEncodeBytes(await hmacRaw("SHA-256", secret, body));
  return body + "." + sig;
}

async function verifyEntitlement(secret, token) {
  if (!secret || !token) return { ok: false, reason: "missing" };
  var parts = String(token).split(".");
  if (parts.length !== 2 || !parts[0] || !parts[1]) {
    return { ok: false, reason: "malformed" };
  }
  var expected, got;
  try {
    expected = await hmacRaw("SHA-256", secret, parts[0]);
    got = b64uDecodeBytes(parts[1]);
  } catch (e) {
    return { ok: false, reason: "malformed" };
  }
  if (!safeEqualBytes(expected, got)) return { ok: false, reason: "bad_signature" };
  var payload;
  try {
    payload = JSON.parse(b64uDecodeToString(parts[0]));
  } catch (e) {
    return { ok: false, reason: "malformed" };
  }
  var nowS = Math.floor(Date.now() / 1000);
  if (!payload || typeof payload.exp !== "number" || typeof payload.iat !== "number") {
    return { ok: false, reason: "malformed" };
  }
  if (payload.exp <= nowS) return { ok: false, reason: "expired" };
  if (payload.iat > nowS + 300) return { ok: false, reason: "not_yet_valid" };
  return { ok: true, payload: payload };
}

function entitlementSetCookieHeader(token) {
  return (
    ENTITLEMENT_COOKIE +
    "=" +
    token +
    "; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=" +
    ENTITLEMENT_TTL
  );
}

/* Recursively key-sort an object (NOWPayments IPN canonical form). */
function sortKeysDeep(v) {
  if (Array.isArray(v)) {
    var arr = [];
    for (var i = 0; i < v.length; i++) arr.push(sortKeysDeep(v[i]));
    return arr;
  }
  if (v && typeof v === "object") {
    var keys = Object.keys(v).sort();
    var out = {};
    for (var j = 0; j < keys.length; j++) out[keys[j]] = sortKeysDeep(v[keys[j]]);
    return out;
  }
  return v;
}

/* NOWPayments IPN signature: HMAC-SHA512 of JSON.stringify(sorted(payload)). */
async function nowpaymentsSignature(payload, ipnSecret) {
  var canonical = JSON.stringify(sortKeysDeep(payload));
  return hmacHex("SHA-512", ipnSecret, canonical);
}

async function verifyNowpaymentsIpn(payload, signature, ipnSecret) {
  if (!signature || !ipnSecret) return false;
  var expected = await nowpaymentsSignature(payload, ipnSecret);
  return safeEqual(expected, String(signature).toLowerCase());
}

/* Stripe webhook signature: header "t=...,v1=...[,v0=...]".
   expected = HMAC-SHA256(webhook_secret, t + "." + rawBody). */
function parseStripeSigHeader(header) {
  var out = { t: null, v1: [] };
  var parts = String(header || "").split(",");
  for (var i = 0; i < parts.length; i++) {
    var kv = parts[i].split("=");
    if (kv[0] === "t") out.t = kv.slice(1).join("=");
    else if (kv[0] === "v1") out.v1.push(kv.slice(1).join("="));
  }
  return out;
}

async function verifyStripeSignature(rawBody, sigHeader, webhookSecret) {
  if (!rawBody || !sigHeader || !webhookSecret) return false;
  var p = parseStripeSigHeader(sigHeader);
  if (!p.t || !p.v1.length) return false;
  var t = parseInt(p.t, 10);
  if (!isFinite(t)) return false;
  // Reject absurd clock skew (> 5 minutes) to blunt replay.
  if (Math.abs(Date.now() / 1000 - t) > 300) return false;
  var expected = await hmacHex("SHA-256", webhookSecret, p.t + "." + rawBody);
  for (var i = 0; i < p.v1.length; i++) {
    if (safeEqual(expected, p.v1[i])) return true;
  }
  return false;
}

function base64Encode(str) {
  var bytes = new TextEncoder().encode(str);
  var bin = "";
  for (var i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin);
}

/* Payment URI for the direct-wallet QR. BTC uses BIP-21; other chains have
   no universal URI scheme, so the QR encodes the raw address and the UI
   shows the tag/memo as a separate copyable field. */
function directQrPayload(coinCode, address) {
  address = String(address || "").trim();
  if (coinCode === "BTC") return "bitcoin:" + address;
  return address;
}

function centsToDecimal(cents) {
  return (cents / 100).toFixed(2);
}

/* ---------------- order store ---------------- */
/* Production backing: IL_ACCOUNTS KV (already bound). Local/test fallback:
   a per-module in-memory Map — NOT durable across isolates/restarts, never
   rely on it in production. */

var memStore = new Map();

function makeStore(env) {
  if (env && env.IL_ACCOUNTS && typeof env.IL_ACCOUNTS.get === "function") {
    return {
      backend: "kv",
      get: function (k) { return env.IL_ACCOUNTS.get(k); },
      put: function (k, v) { return env.IL_ACCOUNTS.put(k, v); },
    };
  }
  return {
    backend: "memory",
    get: async function (k) { return memStore.has(k) ? memStore.get(k) : null; },
    put: async function (k, v) { memStore.set(k, v); },
  };
}

async function getOrder(store, id) {
  if (!id || !/^[A-Za-z0-9_-]{1,80}$/.test(id)) return null;
  var raw = await store.get("pay:order:" + id);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch (e) {
    return null;
  }
}

async function saveOrder(store, order) {
  order.updated_at = nowIso();
  await store.put("pay:order:" + order.id, JSON.stringify(order));
  // Entitlement index: latest paid order per (email,item).
  if (order.status === "paid" && order.email && order.item) {
    await store.put(
      "pay:entitle:" + order.email.toLowerCase() + ":" + order.item,
      JSON.stringify({
        order_id: order.id,
        item: order.item,
        provider: order.provider,
        paid_at: order.paid_at,
      })
    );
  }
}

/* Transition an order to paid exactly once (webhook re-delivery safe). */
async function markPaid(store, order, providerRef, extra) {
  if (!order || order.status === "paid") return { already: order && order.status === "paid" };
  order.status = "paid";
  order.paid_at = nowIso();
  if (providerRef) order.provider_ref = String(providerRef);
  if (extra && typeof extra === "object") {
    for (var k of Object.keys(extra)) order[k] = extra[k];
  }
  await saveOrder(store, order);
  return { already: false };
}

/* ---------------- Unstoppable Domains resolution ---------------- */

async function fetchUdRecords() {
  var res = await fetch(UD_RESOLVE_URL + encodeURIComponent(UD_DOMAIN), {
    headers: { accept: "application/json" },
  });
  if (!res.ok) throw new Error("ud_http_" + res.status);
  var data = await res.json();
  return (data && data.records) || {};
}

async function resolveCoinAddresses(env, store) {
  // 24h KV cache; on failure fall back to env wallets per coin.
  var cacheKey = "pay:ud:" + UD_DOMAIN;
  var cached = null;
  try {
    var raw = await store.get(cacheKey);
    if (raw) cached = JSON.parse(raw);
  } catch (e) { cached = null; }
  var records = null;
  var source = "env";
  if (cached && cached.expires_at && Date.now() < cached.expires_at && cached.records) {
    records = cached.records;
    source = cached.source || "ud";
  } else {
    try {
      records = await fetchUdRecords();
      source = "ud";
      try {
        await store.put(
          cacheKey,
          JSON.stringify({ records: records, source: "ud", expires_at: Date.now() + UD_CACHE_TTL * 1000, fetched_at: nowIso() })
        );
      } catch (e) { /* cache write is best-effort */ }
    } catch (e) {
      records = {};
      source = "env";
    }
  }
  var out = [];
  for (var i = 0; i < COINS.length; i++) {
    var c = COINS[i];
    var udAddr = records && records[c.ud_key] ? String(records[c.ud_key]).trim() : "";
    var envAddr = env && env[c.env_key] ? String(env[c.env_key]).trim() : "";
    var cfgAddr = c.user_key && USER_CONFIG[c.user_key] ? String(USER_CONFIG[c.user_key]).trim() : "";
    var addr = udAddr || envAddr || cfgAddr;
    var source = "missing";
    if (udAddr) source = "ud";
    else if (envAddr) source = "env";
    else if (cfgAddr) source = "user_config";
    // Sanity floor: a real address for every supported coin is >= 8 chars.
    // Short/placeholder values are treated as missing rather than served.
    if (addr && addr.length < 8) { addr = ""; source = "missing"; }
    var entry = {
      code: c.code,
      name: c.name,
      address: addr,
      source: source,
      ud_domain: UD_DOMAIN,
    };
    if (c.extra) {
      var extraVal = (env && env[c.extra] ? String(env[c.extra]).trim() : "") ||
                     (c.extra_user_key && USER_CONFIG[c.extra_user_key] ? String(USER_CONFIG[c.extra_user_key]).trim() : "");
      if (extraVal) {
        entry[c.extra === "XRP_DESTINATION_TAG" ? "destination_tag" : "memo"] = extraVal;
        entry.extra_label = c.extra_label;
      }
    }
    out.push(entry);
  }
  return { domain: UD_DOMAIN, coins: out, resolved_via: source, fetched_at: nowIso() };
}

/* ---------------- request validation ---------------- */

function validateCreate(body) {
  if (!body || typeof body !== "object") return { ok: false, error: "bad_json" };
  var provider = String(body.provider || "").toLowerCase();
  if (PROVIDERS.indexOf(provider) === -1) {
    return { ok: false, error: "provider_invalid", valid: PROVIDERS };
  }
  var item = String(body.item || "").trim();
  if (!ITEMS[item]) {
    return { ok: false, error: "item_invalid", valid: Object.keys(ITEMS) };
  }
  var email = body.email != null ? String(body.email).trim().toLowerCase() : "";
  if (email && (!EMAIL_RE.test(email) || email.length > 254)) {
    return { ok: false, error: "email_invalid" };
  }
  var coin = null;
  if (provider === "nowpayments" || provider === "direct") {
    coin = coinByCode(body.coin);
    if (!coin) return { ok: false, error: "coin_invalid", valid: COINS.map(function (c) { return c.code; }) };
  }
  return { ok: true, provider: provider, item: item, email: email, coin: coin };
}

function providerConfigured(env, provider) {
  if (provider === "stripe") return !!(env.STRIPE_SECRET_KEY);
  if (provider === "paypal") return !!(env.PAYPAL_CLIENT_ID && env.PAYPAL_CLIENT_SECRET);
  if (provider === "nowpayments") return !!(env.NOWPAYMENTS_API_KEY);
  if (provider === "direct") {
    for (var i = 0; i < COINS.length; i++) {
      if (env[COINS[i].env_key]) return true;
      if (COINS[i].user_key && USER_CONFIG[COINS[i].user_key]) return true;
    }
    return false;
  }
  return false;
}

function newOrder(provider, item, email, coin) {
  var spec = ITEMS[item];
  return {
    id: "ord_" + randHex(12),
    provider: provider,
    item: item,
    item_name: spec.name,
    amount_cents: spec.amount_cents,
    currency: "USD",
    email: email || "",
    coin: coin ? coin.code : "",
    status: "created",
    provider_ref: "",
    created_at: nowIso(),
    updated_at: nowIso(),
    paid_at: "",
  };
}

/* ---------------- Stripe ---------------- */

function stripeApiBase() {
  return "https://api.stripe.com/v1";
}

function stripeForm(params) {
  var parts = [];
  for (var k of Object.keys(params)) {
    parts.push(encodeURIComponent(k) + "=" + encodeURIComponent(params[k]));
  }
  return parts.join("&");
}

async function stripeCreateCheckoutSession(env, order, origin) {
  var p = {
    "payment_method_types[]": "card", // Checkout adds Apple Pay / Google Pay automatically where eligible
    "line_items[0][price_data][currency]": CURRENCY,
    "line_items[0][price_data][product_data][name]": "Interstitium Labs — " + order.item_name,
    "line_items[0][price_data][unit_amount]": String(order.amount_cents),
    "line_items[0][quantity]": "1",
    "mode": "payment",
    "customer_email": order.email || undefined,
    "success_url": origin + "/api/pay/stripe/return?session_id={CHECKOUT_SESSION_ID}",
    "cancel_url": origin + "/enroll/cancel.html",
    "metadata[order_id]": order.id,
    "metadata[item]": order.item,
  };
  // Drop undefined values (customer_email is optional).
  var clean = {};
  for (var k of Object.keys(p)) if (p[k] !== undefined) clean[k] = p[k];
  var res = await fetch(stripeApiBase() + "/checkout/sessions", {
    method: "POST",
    headers: {
      "authorization": "Bearer " + env.STRIPE_SECRET_KEY,
      "content-type": "application/x-www-form-urlencoded",
    },
    body: stripeForm(clean),
  });
  var data = await res.json().catch(function () { return null; });
  if (!res.ok || !data || !data.url) {
    throw new Error("stripe_session_failed:" + (data && data.error && data.error.message ? data.error.message : res.status));
  }
  return { session_id: data.id, url: data.url };
}

async function stripeRetrieveSession(env, sessionId) {
  var res = await fetch(stripeApiBase() + "/checkout/sessions/" + encodeURIComponent(sessionId), {
    headers: { "authorization": "Bearer " + env.STRIPE_SECRET_KEY },
  });
  if (!res.ok) throw new Error("stripe_retrieve_failed:" + res.status);
  return res.json();
}

/* ---------------- PayPal ---------------- */

function paypalApiBase(env) {
  return env.PAYPAL_SANDBOX === "1"
    ? "https://api-m.sandbox.paypal.com"
    : "https://api-m.paypal.com";
}

async function paypalAccessToken(env) {
  var res = await fetch(paypalApiBase(env) + "/v1/oauth2/token", {
    method: "POST",
    headers: {
      "authorization": "Basic " + base64Encode(env.PAYPAL_CLIENT_ID + ":" + env.PAYPAL_CLIENT_SECRET),
      "content-type": "application/x-www-form-urlencoded",
    },
    body: "grant_type=client_credentials",
  });
  var data = await res.json().catch(function () { return null; });
  if (!res.ok || !data || !data.access_token) throw new Error("paypal_auth_failed:" + res.status);
  return data.access_token;
}

async function paypalCreateOrder(env, order, origin) {
  var token = await paypalAccessToken(env);
  var body = {
    intent: "CAPTURE",
    purchase_units: [
      {
        reference_id: order.id,
        description: "Interstitium Labs — " + order.item_name,
        custom_id: order.id,
        amount: { currency_code: "USD", value: centsToDecimal(order.amount_cents) },
      },
    ],
    application_context: {
      brand_name: "Interstitium Labs",
      return_url: origin + "/api/pay/paypal/return",
      cancel_url: origin + "/api/pay/paypal/cancel",
      user_action: "PAY_NOW",
    },
  };
  var res = await fetch(paypalApiBase(env) + "/v2/checkout/orders", {
    method: "POST",
    headers: {
      "authorization": "Bearer " + token,
      "content-type": "application/json",
    },
    body: JSON.stringify(body),
  });
  var data = await res.json().catch(function () { return null; });
  if (!res.ok || !data || !data.id) {
    throw new Error("paypal_order_failed:" + (data && data.message ? data.message : res.status));
  }
  var approve = "";
  var links = data.links || [];
  for (var i = 0; i < links.length; i++) {
    if (links[i].rel === "approve") approve = links[i].href;
  }
  if (!approve) throw new Error("paypal_no_approve_link");
  return { paypal_order_id: data.id, url: approve };
}

async function paypalCaptureOrder(env, paypalOrderId) {
  var token = await paypalAccessToken(env);
  var res = await fetch(
    paypalApiBase(env) + "/v2/checkout/orders/" + encodeURIComponent(paypalOrderId) + "/capture",
    {
      method: "POST",
      headers: { "authorization": "Bearer " + token, "content-type": "application/json" },
      body: "{}",
    }
  );
  var data = await res.json().catch(function () { return null; });
  if (!res.ok || !data) throw new Error("paypal_capture_failed:" + res.status);
  return data;
}

/* PayPal webhook verification MUST go through PayPal's API — there is no
   local HMAC scheme. We POST the transmission fields back for validation. */
async function paypalVerifyWebhook(env, headers, eventBody) {
  if (!env.PAYPAL_WEBHOOK_ID) return false;
  var token = await paypalAccessToken(env);
  var payload = {
    transmission_id: headers.get("paypal-transmission-id") || "",
    transmission_time: headers.get("paypal-transmission-time") || "",
    cert_url: headers.get("paypal-cert-url") || "",
    auth_algo: headers.get("paypal-auth-algo") || "",
    transmission_sig: headers.get("paypal-transmission-sig") || "",
    webhook_id: env.PAYPAL_WEBHOOK_ID,
    webhook_event: eventBody,
  };
  var res = await fetch(paypalApiBase(env) + "/v1/notifications/verify-webhook-signature", {
    method: "POST",
    headers: {
      "authorization": "Bearer " + token,
      "content-type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  var data = await res.json().catch(function () { return null; });
  return !!(data && data.verification_status === "SUCCESS");
}

/* ---------------- NOWPayments ---------------- */

function nowpaymentsApiBase(env) {
  return env.NOWPAYMENTS_SANDBOX === "1"
    ? "https://api-sandbox.nowpayments.io/v1"
    : "https://api.nowpayments.io/v1";
}

async function nowpaymentsCreateInvoice(env, order, coin, origin) {
  var body = {
    price_amount: Number(centsToDecimal(order.amount_cents)),
    price_currency: "usd",
    pay_currency: coin.pay_currency,
    order_id: order.id,
    order_description: "Interstitium Labs — " + order.item_name,
    ipn_callback_url: origin + "/api/pay/ipn/nowpayments",
    success_url: origin + "/enroll/success.html?order=" + order.id,
    cancel_url: origin + "/enroll/cancel.html",
  };
  var res = await fetch(nowpaymentsApiBase(env) + "/invoice", {
    method: "POST",
    headers: {
      "x-api-key": env.NOWPAYMENTS_API_KEY,
      "content-type": "application/json",
    },
    body: JSON.stringify(body),
  });
  var data = await res.json().catch(function () { return null; });
  if (!res.ok || !data || !data.invoice_url) {
    throw new Error("nowpayments_invoice_failed:" + (data && data.message ? data.message : res.status));
  }
  return { invoice_id: String(data.id || ""), url: data.invoice_url };
}

async function nowpaymentsPaymentStatus(env, paymentId) {
  var res = await fetch(
    nowpaymentsApiBase(env) + "/payment/" + encodeURIComponent(paymentId),
    { headers: { "x-api-key": env.NOWPAYMENTS_API_KEY } }
  );
  if (!res.ok) throw new Error("nowpayments_status_failed:" + res.status);
  return res.json();
}

/* ---------------- route handlers ---------------- */

async function handleCreate(request, env, store) {
  if (request.method !== "POST") return payJson({ ok: false, error: "method_not_allowed" }, 405);
  var body = null;
  try {
    body = await request.json();
  } catch (e) {
    return payJson({ ok: false, error: "bad_json" }, 422);
  }
  var v = validateCreate(body);
  if (!v.ok) return payJson({ ok: false, error: v.error, valid: v.valid }, 422);
  if (!providerConfigured(env, v.provider)) {
    return payJson(
      { ok: false, error: "provider_unavailable", provider: v.provider, hint: "payments_not_configured" },
      503
    );
  }
  var url = new URL(request.url);
  var origin = url.origin;
  var order = newOrder(v.provider, v.item, v.email, v.coin);
  try {
    await saveOrder(store, order);
  } catch (e) {
    return payJson({ ok: false, error: "store_unavailable" }, 503);
  }

  try {
    if (v.provider === "stripe") {
      var s = await stripeCreateCheckoutSession(env, order, origin);
      order.provider_ref = s.session_id;
      order.status = "pending";
      await saveOrder(store, order);
      return payJson({ ok: true, order_id: order.id, provider: "stripe", redirect_url: s.url });
    }
    if (v.provider === "paypal") {
      var p = await paypalCreateOrder(env, order, origin);
      order.provider_ref = p.paypal_order_id;
      order.status = "pending";
      await saveOrder(store, order);
      // Venmo is offered inside the PayPal Checkout UI automatically.
      return payJson({ ok: true, order_id: order.id, provider: "paypal", redirect_url: p.url, note: "venmo_available_in_checkout" });
    }
    if (v.provider === "nowpayments") {
      var n = await nowpaymentsCreateInvoice(env, order, v.coin, origin);
      order.provider_ref = n.invoice_id;
      order.status = "pending";
      await saveOrder(store, order);
      return payJson({ ok: true, order_id: order.id, provider: "nowpayments", coin: v.coin.code, redirect_url: n.url });
    }
    if (v.provider === "direct") {
      var resolved = await resolveCoinAddresses(env, store);
      var entry = null;
      for (var i = 0; i < resolved.coins.length; i++) {
        if (resolved.coins[i].code === v.coin.code) entry = resolved.coins[i];
      }
      if (!entry || !entry.address) {
        order.status = "failed";
        await saveOrder(store, order);
        return payJson({ ok: false, error: "coin_address_missing", coin: v.coin.code }, 503);
      }
      order.direct = {
        address: entry.address,
        source: entry.source,
        ud_domain: UD_DOMAIN,
        qr_payload: directQrPayload(v.coin.code, entry.address),
      };
      if (entry.destination_tag) {
        order.direct.destination_tag = entry.destination_tag;
        order.direct.extra_label = entry.extra_label;
      }
      if (entry.memo) {
        order.direct.memo = entry.memo;
        order.direct.extra_label = entry.extra_label;
      }
      order.status = "pending";
      await saveOrder(store, order);
      return payJson({
        ok: true,
        order_id: order.id,
        provider: "direct",
        coin: v.coin.code,
        coin_name: v.coin.name,
        amount_cents: order.amount_cents,
        currency: "USD",
        direct: order.direct,
        // Honest: direct-wallet payments have no automatic chain watcher;
        // confirmation email follows after manual verification.
        confirmation: "manual_review",
      });
    }
  } catch (e) {
    order.status = "failed";
    try {
      await saveOrder(store, order);
    } catch (e2) {}
    var msg = (e && e.message) || "provider_error";
    return payJson({ ok: false, error: "provider_error", detail: msg.slice(0, 200) }, 502);
  }
  return payJson({ ok: false, error: "provider_invalid" }, 422);
}

async function handleStatus(request, env, store) {
  if (request.method !== "GET") return payJson({ ok: false, error: "method_not_allowed" }, 405);
  var url = new URL(request.url);
  var order = await getOrder(store, url.searchParams.get("order") || "");
  if (!order) return payJson({ ok: false, error: "not_found" }, 404);
  return payJson({
    ok: true,
    order_id: order.id,
    provider: order.provider,
    item: order.item,
    item_name: order.item_name,
    amount_cents: order.amount_cents,
    currency: order.currency,
    coin: order.coin || "",
    status: order.status,
    paid_at: order.paid_at || null,
    created_at: order.created_at,
  });
}

async function handleUd(request, env, store) {
  if (request.method !== "GET") return payJson({ ok: false, error: "method_not_allowed" }, 405);
  try {
    var resolved = await resolveCoinAddresses(env, store);
  } catch (e) {
    return payJson({ ok: false, error: "resolution_failed" }, 502);
  }
  // Public shape: addresses + provenance only, never env secret names.
  var coins = resolved.coins.map(function (c) {
    var o = { code: c.code, name: c.name, address: c.address, source: c.source, ud_domain: c.ud_domain };
    if (c.destination_tag) o.destination_tag = c.destination_tag;
    if (c.memo) o.memo = c.memo;
    if (c.extra_label) o.extra_label = c.extra_label;
    return o;
  });
  return payJson({
    ok: true,
    domain: resolved.domain,
    resolved_via: resolved.resolved_via,
    fetched_at: resolved.fetched_at,
    coins: coins,
  });
}

async function handleStripeWebhook(request, env, store) {
  if (request.method !== "POST") return payJson({ ok: false, error: "method_not_allowed" }, 405);
  if (!env.STRIPE_WEBHOOK_SECRET) return payJson({ ok: false, error: "webhook_not_configured" }, 503);
  var raw = await request.text();
  var sig = request.headers.get("stripe-signature") || "";
  var okSig = await verifyStripeSignature(raw, sig, env.STRIPE_WEBHOOK_SECRET);
  if (!okSig) return payJson({ ok: false, error: "signature_invalid" }, 400);
  var event = null;
  try {
    event = JSON.parse(raw);
  } catch (e) {
    return payJson({ ok: false, error: "bad_json" }, 400);
  }
  var type = event.type || "";
  var obj = event.data && event.data.object ? event.data.object : {};
  var orderId = (obj.metadata && obj.metadata.order_id) || "";
  if (type === "checkout.session.completed") {
    var order = await getOrder(store, orderId);
    if (order) {
      // Cross-check the amount the buyer actually paid against our catalog.
      if (obj.amount_total !== undefined && Number(obj.amount_total) !== order.amount_cents) {
        order.status = "failed";
        order.note = "amount_mismatch";
        await saveOrder(store, order);
      } else {
        await markPaid(store, order, obj.id, { stripe_payment_intent: obj.payment_intent || "" });
      }
    }
  } else if (type === "checkout.session.expired") {
    var expired = await getOrder(store, orderId);
    if (expired && expired.status !== "paid") {
      expired.status = "expired";
      await saveOrder(store, expired);
    }
  } else if (type === "charge.refunded" || type === "refund.created") {
    // Best-effort: flag the linked order if we can find it via payment intent.
    // (Full refund reconciliation is an owner-dashboard task.)
  }
  return payJson({ ok: true, received: type });
}

async function handlePaypalWebhook(request, env, store) {
  if (request.method !== "POST") return payJson({ ok: false, error: "method_not_allowed" }, 405);
  var raw = await request.text();
  var event = null;
  try {
    event = JSON.parse(raw);
  } catch (e) {
    return payJson({ ok: false, error: "bad_json" }, 400);
  }
  var verified = false;
  try {
    verified = await paypalVerifyWebhook(env, request.headers, event);
  } catch (e) {
    verified = false;
  }
  if (!verified) return payJson({ ok: false, error: "signature_invalid" }, 400);
  var type = event.event_type || "";
  if (type === "PAYMENT.CAPTURE.COMPLETED") {
    var resource = event.resource || {};
    var orderId = resource.custom_id || "";
    var order = await getOrder(store, orderId);
    if (order) {
      var capAmount = resource.amount && resource.amount.value;
      if (capAmount !== undefined && capAmount !== centsToDecimal(order.amount_cents)) {
        order.status = "failed";
        order.note = "amount_mismatch";
        await saveOrder(store, order);
      } else {
        await markPaid(store, order, resource.id || "", { paypal_capture: true });
      }
    }
  } else if (type === "CHECKOUT.ORDER.APPROVED") {
    // Capture server-side so approval always settles, even if the buyer
    // closes the tab before the return redirect fires.
    var ro = event.resource || {};
    var oid = ro.custom_id || "";
    var o = await getOrder(store, oid);
    if (o && o.status !== "paid" && o.provider_ref) {
      try {
        var cap = await paypalCaptureOrder(env, o.provider_ref);
        var pu = (cap.purchase_units && cap.purchase_units[0]) || {};
        var captures = (pu.payments && pu.payments.captures) || [];
        var capId = captures.length ? captures[0].id : "";
        await markPaid(store, o, o.provider_ref, { paypal_capture_id: capId });
      } catch (e) {
        // Leave pending; the return-redirect capture is the fallback.
      }
    }
  }
  return payJson({ ok: true, received: type });
}

async function handleNowpaymentsIpn(request, env, store) {
  if (request.method !== "POST") return payJson({ ok: false, error: "method_not_allowed" }, 405);
  var raw = await request.text();
  var payload = null;
  try {
    payload = JSON.parse(raw);
  } catch (e) {
    return payJson({ ok: false, error: "bad_json" }, 400);
  }
  var sig = request.headers.get("x-nowpayments-sig") || "";
  var okSig = await verifyNowpaymentsIpn(payload, sig, env.NOWPAYMENTS_IPN_SECRET);
  if (!okSig) return payJson({ ok: false, error: "signature_invalid" }, 400);
  // NOWPayments warns about repeated/wrong-asset deposits carrying
  // parent_payment_id — never auto-fulfill those.
  if (payload.parent_payment_id) {
    return payJson({ ok: true, received: "parent_payment_skipped" });
  }
  var orderId = payload.order_id || "";
  var order = await getOrder(store, orderId);
  var status = String(payload.payment_status || "");
  if (order) {
    if (status === "finished") {
      await markPaid(store, order, String(payload.payment_id || ""), {
        nowpayments_pay_currency: payload.pay_currency || "",
        nowpayments_pay_amount: payload.pay_amount || "",
      });
    } else if (status === "failed" || status === "refunded" || status === "expired") {
      if (order.status !== "paid") {
        order.status = status === "refunded" ? "refunded" : "failed";
        await saveOrder(store, order);
      }
    }
    // waiting / confirming / confirmed / sending / partially_paid: stay pending.
  }
  return payJson({ ok: true, received: status });
}

/* Direct-wallet tx-hash submission (2026-10-08).
 * There is no automatic on-chain watcher: the buyer pastes the transaction
 * hash after sending. The order is recorded as PENDING and stays PENDING
 * until the owner verifies the transfer manually and calls
 * POST /api/pay/admin/confirm. */
async function handleTxSubmit(request, env, store) {
  if (request.method !== "POST") return payJson({ ok: false, error: "method_not_allowed" }, 405);
  var body = null;
  try {
    body = await request.json();
  } catch (e) {
    return payJson({ ok: false, error: "bad_json" }, 422);
  }
  var orderId = body && body.order ? String(body.order).trim() : "";
  var txHash = body && body.tx_hash ? String(body.tx_hash).trim() : "";
  if (!orderId || !/^[A-Za-z0-9_-]{1,80}$/.test(orderId)) {
    return payJson({ ok: false, error: "order_invalid" }, 422);
  }
  // Accept chain tx hashes: hex (BTC/XMR-style) or generic alphanumeric, 16–160 chars.
  if (!/^[A-Za-z0-9]{16,160}$/.test(txHash)) {
    return payJson({ ok: false, error: "tx_hash_invalid" }, 422);
  }
  var order = await getOrder(store, orderId);
  if (!order) return payJson({ ok: false, error: "not_found" }, 404);
  if (order.status === "paid") return payJson({ ok: false, error: "already_paid" }, 409);
  if (order.provider !== "direct") {
    return payJson({ ok: false, error: "tx_submit_direct_only" }, 422);
  }
  if (order.tx_hash) return payJson({ ok: false, error: "tx_already_submitted" }, 409);
  var note = body && body.sender_note ? String(body.sender_note).slice(0, 500) : "";
  order.tx_hash = txHash;
  order.tx_submitted_at = nowIso();
  if (note) order.tx_sender_note = note;
  order.status = "pending"; // explicit: stays PENDING until manual admin verification.
  order.confirmation = "manual_review";
  await saveOrder(store, order);
  return payJson({
    ok: true,
    order_id: order.id,
    status: "pending",
    confirmation: "manual_review",
    message:
      "Transaction recorded. Our team verifies on-chain payment manually; your receipt and course access follow by email.",
  });
}

/* Admin-confirm hook (2026-10-08). Owner-only: after manually verifying a
 * direct-wallet (or otherwise pending) payment, the owner calls this with
 * the ADMIN_TOKEN to mark the order paid. The signed entitlement token is
 * returned in the body (the owner relays it or lets the buyer hit
 * /api/pay/entitlement on a paid order). */
async function handleAdminConfirm(request, env, store) {
  if (request.method !== "POST") return payJson({ ok: false, error: "method_not_allowed" }, 405);
  if (!env.ADMIN_TOKEN) {
    console.log("pay/admin/confirm: ADMIN_TOKEN not set — failing closed");
    return payJson(
      { ok: false, error: "admin_not_configured", hint: "set ADMIN_TOKEN via wrangler secret" },
      503
    );
  }
  var body = null;
  try {
    body = await request.json();
  } catch (e) {
    return payJson({ ok: false, error: "bad_json" }, 422);
  }
  if (!safeEqual(String((body && body.admin_token) || ""), String(env.ADMIN_TOKEN))) {
    return payJson({ ok: false, error: "unauthorized" }, 401);
  }
  var orderId = body && body.order ? String(body.order).trim() : "";
  var order = await getOrder(store, orderId);
  if (!order) return payJson({ ok: false, error: "not_found" }, 404);
  if (order.status === "paid") return payJson({ ok: false, error: "already_paid" }, 409);
  await markPaid(store, order, "admin:confirmed", {
    admin_confirmed_at: nowIso(),
    admin_note: body && body.note ? String(body.note).slice(0, 500) : "",
  });
  var entitlement = null;
  if (env.ENTITLEMENT_SECRET && order.item && (ITEMS[order.item] || {}).kind !== "tier") {
    entitlement = await signEntitlement(
      env.ENTITLEMENT_SECRET,
      order.item === "all-courses" ? "all-courses" : order.item
    );
  }
  return payJson({
    ok: true,
    order_id: order.id,
    status: "paid",
    item: order.item,
    // The owner can relay this token, or the buyer calls /api/pay/entitlement.
    entitlement: entitlement,
  });
}

/* Entitlement issuance (2026-10-08). After ANY successful payment, the
 * client POSTs {order} here; a paid course/bundle order returns the signed
 * il_entitlement cookie the course paywall (_worker.js) checks. Fails closed
 * when ENTITLEMENT_SECRET is unset. */
async function handleEntitlement(request, env, store) {
  if (request.method !== "POST") return payJson({ ok: false, error: "method_not_allowed" }, 405);
  var body = null;
  try {
    body = await request.json();
  } catch (e) {
    return payJson({ ok: false, error: "bad_json" }, 422);
  }
  var orderId = body && body.order ? String(body.order).trim() : "";
  if (!orderId || !/^[A-Za-z0-9_-]{1,80}$/.test(orderId)) {
    return payJson({ ok: false, error: "order_invalid" }, 422);
  }
  var order = await getOrder(store, orderId);
  if (!order) return payJson({ ok: false, error: "not_found" }, 404);
  if (order.status !== "paid") {
    return payJson({ ok: false, error: "not_paid", status: order.status }, 402);
  }
  var kind = (ITEMS[order.item] || {}).kind || "";
  if (kind !== "course" && kind !== "bundle") {
    return payJson({ ok: false, error: "entitlement_not_applicable", item: order.item }, 422);
  }
  if (!env.ENTITLEMENT_SECRET) {
    console.log("pay/entitlement: ENTITLEMENT_SECRET not set — failing closed");
    return payJson(
      { ok: false, error: "entitlement_secret_not_set", hint: "owner: wrangler secret put ENTITLEMENT_SECRET" },
      503
    );
  }
  var scope = order.item === "all-courses" ? "all-courses" : order.item;
  var token = await signEntitlement(env.ENTITLEMENT_SECRET, scope);
  return new Response(JSON.stringify({ ok: true, course: scope }), {
    status: 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "set-cookie": entitlementSetCookieHeader(token),
    },
  });
}

function redirectTo(url, request) {
  return Response.redirect(new URL(url, new URL(request.url).origin).toString(), 303);
}

async function handlePaypalReturn(request, env, store) {
  var url = new URL(request.url);
  var token = url.searchParams.get("token") || ""; // PayPal order id
  if (!token) return redirectTo("/enroll/cancel.html", request);
  var order = null;
  // Find our order by provider_ref scan is expensive in KV; instead the
  // capture is authoritative — capture first, then locate by custom_id.
  try {
    var cap = await paypalCaptureOrder(env, token);
    var pu = (cap.purchase_units && cap.purchase_units[0]) || {};
    var ref = pu.reference_id || "";
    order = await getOrder(store, ref);
    if (order && order.status !== "paid") {
      // Cross-check the captured amount against our catalog before marking paid.
      var capAmt = pu.amount && pu.amount.value;
      if (capAmt !== undefined && capAmt !== centsToDecimal(order.amount_cents)) {
        order.status = "failed";
        order.note = "amount_mismatch";
        await saveOrder(store, order);
        return redirectTo("/enroll/cancel.html?reason=amount_mismatch", request);
      }
      var captures = (pu.payments && pu.payments.captures) || [];
      await markPaid(store, order, token, { paypal_capture_id: captures.length ? captures[0].id : "" });
    }
  } catch (e) {
    return redirectTo("/enroll/cancel.html?reason=capture_failed", request);
  }
  return redirectTo("/enroll/success.html?order=" + encodeURIComponent(order ? order.id : token), request);
}

async function handleStripeReturn(request, env, store) {
  var url = new URL(request.url);
  var sessionId = url.searchParams.get("session_id") || "";
  if (!sessionId || !env.STRIPE_SECRET_KEY) return redirectTo("/enroll/cancel.html", request);
  try {
    var s = await stripeRetrieveSession(env, sessionId);
    var orderId = (s.metadata && s.metadata.order_id) || "";
    var order = await getOrder(store, orderId);
    if (order && s.payment_status === "paid") {
      // The webhook cross-checks amount_total; apply the same check on the
      // return redirect so a tampered session cannot mark an order paid.
      if (s.amount_total !== undefined && Number(s.amount_total) !== order.amount_cents) {
        order.status = "failed";
        order.note = "amount_mismatch";
        await saveOrder(store, order);
        return redirectTo("/enroll/cancel.html?reason=amount_mismatch", request);
      }
      await markPaid(store, order, s.id, { stripe_payment_intent: s.payment_intent || "" });
    }
    return redirectTo(
      "/enroll/success.html?order=" + encodeURIComponent(order ? order.id : sessionId),
      request
    );
  } catch (e) {
    return redirectTo("/enroll/cancel.html?reason=verify_failed", request);
  }
}

/* ---------------- top-level dispatch (called from _worker.js) ---------------- */

async function handlePay(request, env) {
  var url = new URL(request.url);
  var path = url.pathname;
  var store = makeStore(env);

  if (path === "/api/pay/create") return handleCreate(request, env, store);
  if (path === "/api/pay/status") return handleStatus(request, env, store);
  if (path === "/api/pay/ud") return handleUd(request, env, store);
  if (path === "/api/pay/webhook/stripe") return handleStripeWebhook(request, env, store);
  if (path === "/api/pay/webhook/paypal") return handlePaypalWebhook(request, env, store);
  if (path === "/api/pay/ipn/nowpayments") return handleNowpaymentsIpn(request, env, store);
  if (path === "/api/pay/tx/submit") return handleTxSubmit(request, env, store);
  if (path === "/api/pay/admin/confirm") return handleAdminConfirm(request, env, store);
  if (path === "/api/pay/entitlement") return handleEntitlement(request, env, store);
  if (path === "/api/pay/paypal/return") return handlePaypalReturn(request, env, store);
  if (path === "/api/pay/paypal/cancel") return redirectTo("/enroll/cancel.html", request);
  if (path === "/api/pay/stripe/return") return handleStripeReturn(request, env, store);
  return payJson({ ok: false, error: "not_found" }, 404);
}

/* ---------------- exports ---------------- */
/* handlePay is the Worker wiring. The rest are exported for unit tests
   (node --test) — pure functions, no Worker-only globals at import time. */

export {
  handlePay,
  handleTxSubmit,
  handleAdminConfirm,
  handleEntitlement,
  makeStore,
  getOrder,
  saveOrder,
  markPaid,
  validateCreate,
  providerConfigured,
  newOrder,
  coinByCode,
  COINS,
  ITEMS,
  COURSES,
  PAYWALL_CONFIG,
  USER_CONFIG,
  UD_DOMAIN,
  sortKeysDeep,
  nowpaymentsSignature,
  verifyNowpaymentsIpn,
  parseStripeSigHeader,
  verifyStripeSignature,
  directQrPayload,
  centsToDecimal,
  safeEqual,
  signEntitlement,
  verifyEntitlement,
  entitlementSetCookieHeader,
  ENTITLEMENT_COOKIE,
  ENTITLEMENT_TTL,
};

// _worker.js
var NOINDEX_PREFIXES = ["/admin/", "/ops/", "/analytics/", "/measure/", "/brand/"];

function needsNoindex(path) {
  for (var i = 0; i < NOINDEX_PREFIXES.length; i++) {
    var pre = NOINDEX_PREFIXES[i];
    if (path === pre.slice(0, -1) || path.indexOf(pre) === 0) return true;
  }
  return false;
}

// 2026-10-07 (Phase 5): docs/_headers is NOT applied by this API deploy path
// (verified 2026-10-04), so inject the documented security headers here on the
// static-asset fallthrough. Mirrors the _headers `/*` block verbatim; the
// /coach/* and /cinema/* Permissions-Policy mic exception is mirrored too.
// Per-page <meta http-equiv="Content-Security-Policy"> remains the CSP carrier
// (page-specific policies must not be flattened by a blanket worker CSP).
var SECURITY_HEADERS = {
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "X-Frame-Options": "DENY",
  "Cross-Origin-Opener-Policy": "same-origin",
  "Cross-Origin-Resource-Policy": "same-origin",
  "X-DNS-Prefetch-Control": "off"
};

function micAllowed(path) {
  return path === "/coach" || path === "/cinema" ||
    path.indexOf("/coach/") === 0 || path.indexOf("/cinema/") === 0;
}

function applyAssetHeaders(res, path) {
  var h = new Headers(res.headers);
  for (var k in SECURITY_HEADERS) {
    if (!h.has(k)) h.set(k, SECURITY_HEADERS[k]);
  }
  h.set("Permissions-Policy", micAllowed(path)
    ? "camera=(), microphone=(self), geolocation=(), payment=(), usb=(), interest-cohort=()"
    : "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()");
  if (needsNoindex(path)) h.set("X-Robots-Tag", "noindex, nofollow");
  return new Response(res.body, {
    status: res.status,
    statusText: res.statusText,
    headers: h,
  });
}

// 2026-10-07: per-course Open Graph / Twitter Card injection for the
// /university/course route. Social crawlers don't run JS, so the
// query-param course selection can't set <head> client-side — inject at the
// edge instead. Known course ids map to static OG profiles; unknown ids and
// non-HTML responses fall through unchanged.
var OG_SITE = "https://interstitiumlabs.dev";
var OG_PROFILES = {
  "il-01-esoteric-foundations": {
    title: "IL-01 · Esoteric Foundations",
    description: "The Western esoteric current, studied as documented history.",
    image: "/assets/cinematic/courses-og/IL-01-og.png"
  },
  "il-02-mathematical-maturity-engine": {
    title: "IL-02 · Mathematical Maturity Engine",
    description: "The ground under everything — from arithmetic fluency to measure-theoretic probability.",
    image: "/assets/cinematic/courses-og/IL-02-og.png"
  },
  "il-03-programming-language-forge": {
    title: "IL-03 · Programming Language Forge",
    description: "Languages as instruments, not identities — Python, Java, C++, and the systems beneath them.",
    image: "/assets/cinematic/courses-og/IL-03-og.png"
  },
  "il-04-systems-linux-windows-networks": {
    title: "IL-04 · Systems, Linux, Windows & Networks",
    description: "The machine, administered — Linux to RHCSA/RHCE, Windows Server, and networks with packet literacy.",
    image: "/assets/cinematic/courses-og/IL-04-og.png"
  },
  "il-05-cloud-devsecops-platform-sre": {
    title: "IL-05 · Cloud, DevSecOps, Platform & SRE",
    description: "Ship it, then keep it alive — DevOps, Kubernetes, Terraform, AWS, Azure, and OpenShift certification depth.",
    image: "/assets/cinematic/courses-og/IL-05-og.png"
  },
  "il-06-cybersecurity-secure-engineering": {
    title: "IL-06 · Cybersecurity & Secure Engineering",
    description: "Know the attack to earn the defense — offensive operations, SOC defense, and secure engineering.",
    image: "/assets/cinematic/courses-og/IL-06-og.png"
  },
  "il-07-data-engineering-analytics-ai": {
    title: "IL-07 · SQL, Data Engineering, Analytics & AI",
    description: "From the row to the model — documents, pipelines, machine learning, and agents.",
    image: "/assets/cinematic/courses-og/IL-07-og.png"
  },
  "il-08-algorithms-compilers-distributed-formal": {
    title: "IL-08 · Algorithms, Compilers, Distributed & Formal",
    description: "The deep core, in order — MIT, CMU, and Stanford distilled to their load-bearing ideas.",
    image: "/assets/cinematic/courses-og/IL-08-og.png"
  },
  "il-09-adaptive-certification-command": {
    title: "IL-09 · Adaptive Certification Command",
    description: "Credentials, orchestrated honestly — one command deck for every certification that matters to this career.",
    image: "/assets/cinematic/courses-og/IL-09-og.png"
  },
  "il-10-portfolio-career-professional-practice": {
    title: "IL-10 · Portfolio, Career & Professional Practice",
    description: "The work, presented; the career, directed.",
    image: "/assets/cinematic/courses-og/IL-10-og.png"
  },
  "il-11-zero-trust-endpoint-defense": {
    title: "IL-11 · Zero Trust & Endpoint Defense",
    description: "Never trust, always verify — the defender's discipline.",
    image: "/assets/cinematic/courses-og/IL-11-og.png"
  },
  "il-12-ai-engineering": {
    title: "IL-12 · AI Engineering",
    description: "From data to deployed intelligence.",
    image: "/assets/cinematic/courses-og/IL-12-og.png"
  },
  "il-13-software-engineering-interview-prep": {
    title: "IL-13 · Software Engineering Interview Prep",
    description: "Domain tracks, interview-ready.",
    image: "/assets/cinematic/courses-og/IL-13-og.png"
  },
  "il-14-sre-devops-cloud-security-interview-prep": {
    title: "IL-14 · SRE, DevOps, Cloud & Security Interview Prep",
    description: "Keep it alive, then prove it in the interview.",
    image: "/assets/cinematic/courses-og/IL-14-og.png"
  },
  "il-15-data-engineering-analytics-interview-prep": {
    title: "IL-15 · Data Engineering & Analytics Interview Prep",
    description: "From the row to the offer.",
    image: "/assets/cinematic/courses-og/IL-15-og.png"
  },
  "il-16-machine-learning-ai-engineering": {
    title: "IL-16 · Machine Learning & AI Engineering",
    description: "The models, end to end.",
    image: "/assets/cinematic/courses-og/IL-16-og.png"
  },
  "il-17-agentic-ai-engineering": {
    title: "IL-17 · Agentic AI Engineering",
    description: "Agents that do the work.",
    image: "/assets/cinematic/courses-og/IL-17-og.png"
  },
  "il-18-technical-leadership-interview-prep": {
    title: "IL-18 · Technical Leadership Interview Prep",
    description: "Lead the work, land the role.",
    image: "/assets/cinematic/courses-og/IL-18-og.png"
  },
  "il-19-multicloud-devops-ai-bootcamp": {
    title: "IL-19 · MultiCloud, DevOps & AI Bootcamp",
    description: "Six clouds. One discipline. Noah-tutored.",
    image: "/assets/cinematic/courses-og/IL-19-og.png"
  },
  "il-20-mathematics": {
    title: "IL-20 · Mathematics for Engineers & Scientists",
    description: "The mathematical spine of engineering: discrete structures, linear algebra, calculus, probability, and numerical computation.",
    image: "/assets/cinematic/courses-og/IL-20-og.png"
  },
  "il-21-humanities": {
    title: "IL-21 · Humanities for Technologists",
    description: "Philosophy, history, writing, rhetoric, economics, and law — the disciplines of judgment for people who build.",
    image: "/assets/cinematic/courses-og/IL-21-og.png"
  },
  "il-22-esoteric-secret-knowledge": {
    title: "IL-22 · The Deep Library — Esoteric & Secret Knowledge",
    description: "Kabbalah, Hermeticism, alchemy, astrology, tarot, Enochian, Rosicrucianism, Theosophy, the Golden Dawn: the Western mystery traditions and their Eastern counterparts, studied as traditions.",
    image: "/assets/cinematic/courses-og/IL-22-og.png"
  },
  "il-23-frontier-knowledge": {
    title: "IL-23 · The Frontier — Cutting-Edge Research Distilled",
    description: "Transformers, quantum, CRISPR, fusion, BCIs, agents, chips, synbio, space — the durable core of fast-moving fields, with the method to track the edge.",
    image: "/assets/cinematic/courses-og/IL-23-og.png"
  },
  "il-24-threatlocker-assessment-prep-cbt": {
    title: "IL-24 · ThreatLocker Assessment Prep CBT",
    description: "Zero Trust endpoint defense + security graphs + AI-aided SOC — an assessment-style computer-based training course",
    image: "/assets/cinematic/courses-og/IL-24-og.png"
  },
  "il-25-cybersecurity-professional-certificate": {
    title: "IL-25 · Professional Certificate in Cybersecurity",
    description: "Think like an attacker. Defend like a professional.",
    image: "/assets/cinematic/courses-og/IL-25-og.png"
  },
  "il-26-data-analyst-certification-senior-mastery": {
    title: "IL-26 · Data Analyst Certification & Senior Mastery Bootcamp",
    description: "A 51-module interactive CBT preparing you for 7 industry certifications — Google Data Analytics, PL-300, Tableau, CompTIA Data+, IBM, AWS, Databricks — with senior Palantir and BNY Mellon tracks.",
    image: "/assets/cinematic/courses-og/IL-26-og.png"
  },
  "il-27-it-infrastructure-specialist-threatlocker-mastery": {
    title: "IL-27 - IT Infrastructure Specialist: Zero Trust Infrastructure Mastery",
    description: "A 54-module interactive course covering the full IT infrastructure stack through a Zero Trust lens: Windows and Linux administration, TCP/IP and subnetting, Active Directory, virtualization, hardening, and security operations - plus a 6-day interview fast track.",
    image: "/assets/cinematic/courses-og/IL-27-og.png"
  },
  "il-28-devsecops-cloud-infrastructure-mastery": {
    title: "IL-28 · DevSecOps & Cloud Infrastructure — Production Mastery Bootcamp",
    description: "A 50-module interactive CBT taking you from foundational math to production DevSecOps: Linux/RHEL, networking, Docker, Kubernetes, Terraform, Ansible, Jenkins, Azure/AWS/GCP, observability, DevSecOps, SRE — plus certification tracks and a BNY panel interview simulation.",
    image: "/assets/cinematic/courses-og/IL-28-og.png"
  },
  "il-29-threatlocker-ai-cybersecurity-mastery": {
    title: "IL-29 · ThreatLocker Zero-Trust CBT with AI — Cybersecurity Mastery Bootcamp",
    description: "A 48-module, 431-hour interactive CBT: ThreatLocker zero-trust platform operations, MIT 6.858 systems security, AI in cybersecurity, prerequisite math — plus 7 certification tracks and a ThreatLocker panel interview simulation.",
    image: "/assets/cinematic/courses-og/IL-29-og.png"
  },
  "il-30-post-quantum-cryptography-quantum-safe": {
    title: "IL-30 · Post-Quantum Cryptography & Quantum-Safe Engineering",
    description: "Quantum-safe cryptography at engineering depth — NIST's PQC standards (FIPS 203/204/205), lattice and hash-based math, hybrid TLS 1.3, and a real enterprise migration playbook.",
    image: "/assets/cinematic/courses-og/IL-30-og.png"
  },
  "il-31-ai-red-teaming-safety-evals": {
    title: "IL-31 · AI Red-Teaming & Safety Evals Engineering",
    description: "Evaluate, red-team, and harden frontier AI systems — METR methodology, eval harness design, defensive red-teaming, and responsible disclosure.",
    image: "/assets/cinematic/courses-og/IL-31-og.png"
  },
};

function ogEscape(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function ogMetaTags(profile, pageUrl) {
  var t = ogEscape(profile.title);
  var d = ogEscape(profile.description);
  var img = OG_SITE + profile.image;
  return [
    '<meta property="og:title" content="' + t + '">',
    '<meta property="og:description" content="' + d + '">',
    '<meta property="og:image" content="' + img + '">',
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
    '<meta property="og:url" content="' + ogEscape(pageUrl) + '">',
    '<meta property="og:type" content="website">',
    '<meta property="og:site_name" content="Interstitium Labs">',
    '<meta name="twitter:card" content="summary_large_image">',
    '<meta name="twitter:title" content="' + t + '">',
    '<meta name="twitter:description" content="' + d + '">',
    '<meta name="twitter:image" content="' + img + '">'
  ].join("\n");
}

async function serveCourseWithOg(request, env, path) {
  var url = new URL(request.url);
  var cid = url.searchParams.get("course");
  var profile = (cid && OG_PROFILES[cid]) || null;
  var res = await env.ASSETS.fetch(request);
  var ct = (res.headers.get("content-type") || "").toLowerCase();
  if (!profile || ct.indexOf("text/html") === -1) {
    return applyAssetHeaders(res, path);
  }
  var html = await res.text();
  var pageUrl = url.origin + url.pathname + "?course=" + encodeURIComponent(cid);
  var injected = html.indexOf("<head>") !== -1
    ? html.replace("<head>", "<head>\n" + ogMetaTags(profile, pageUrl))
    : html;
  var h = new Headers(res.headers);
  h.delete("content-length");
  return applyAssetHeaders(
    new Response(injected, { status: res.status, statusText: res.statusText, headers: h }),
    path
  );
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
/* Course paywall (2026-10-08). Worker-level gating for the paid courses:
 *
 *   2026-10-09: PAYWALL TEMPORARILY DISABLED per owner order — all courses
 *   free until payment processor is set up. PAYWALL_DISABLED=true below
 *   makes courseGate() a passthrough. Payment infrastructure (payment-routes.js,
 *   entitlement tokens, checkout UI) is preserved intact for re-enable.
 *   To re-enable: set PAYWALL_DISABLED=false and redeploy.
 *
 *   - IL-27 / IL-28 / IL-29 are FREE forever: unchanged behavior.
 *   - All other course slugs (IL-01..IL-26) are gated.
 *   - Humans requesting /university/course?course=<gated> without a valid
 *     il_entitlement cookie get the branded paywall page.
 *   - Course JSON data routes (/university/data/courses/<gated>.json)
 *     without entitlement get HTTP 402 + JSON error (never the content).
 *   - Social/link crawlers (UA sniffing) always receive the OG-injected
 *     shell via serveCourseWithOg - no entitlement required, so already-
 *     posted link previews keep working.
 *
 * Entitlement token: base64url(payload).base64url(HMAC-SHA256(secret, body)),
 * payload = { course: "<slug>" | "all-courses", iat, exp }. Secret comes
 * ONLY from env.ENTITLEMENT_SECRET - never hardcoded; when unset, gating
 * fails closed (paywall) and a clear message is logged.
 *
 * NOTE on bundling: the live module concatenates payment-routes.js above
 * this file and strips the `import { handlePay }` line, so this file must
 * not import payment helpers. verifyEntitlementToken below mirrors
 * payment-routes.js verifyEntitlement - keep the two in sync.
 * ------------------------------------------------------------------ */

/* 2026-10-09: TEMPORARY — paywall disabled until payment processor setup.
   Set to false to re-enable paid gating. */
var PAYWALL_DISABLED = true;

var FREE_COURSE_SLUGS = [
  "il-27-it-infrastructure-specialist-threatlocker-mastery",
  "il-28-devsecops-cloud-infrastructure-mastery",
  "il-29-threatlocker-ai-cybersecurity-mastery"
];

var BUILD_CONTENT_SLUG = "il-build-content";

var GATED_COURSE_SLUGS = [
  "il-build-content",
  "il-01-esoteric-foundations",
  "il-02-mathematical-maturity-engine",
  "il-03-programming-language-forge",
  "il-04-systems-linux-windows-networks",
  "il-05-cloud-devsecops-platform-sre",
  "il-06-cybersecurity-secure-engineering",
  "il-07-data-engineering-analytics-ai",
  "il-08-algorithms-compilers-distributed-formal",
  "il-09-adaptive-certification-command",
  "il-10-portfolio-career-professional-practice",
  "il-11-zero-trust-endpoint-defense",
  "il-12-ai-engineering",
  "il-13-software-engineering-interview-prep",
  "il-14-sre-devops-cloud-security-interview-prep",
  "il-15-data-engineering-analytics-interview-prep",
  "il-16-machine-learning-ai-engineering",
  "il-17-agentic-ai-engineering",
  "il-18-technical-leadership-interview-prep",
  "il-19-multicloud-devops-ai-bootcamp",
  "il-20-mathematics",
  "il-21-humanities",
  "il-22-esoteric-secret-knowledge",
  "il-23-frontier-knowledge",
  "il-24-threatlocker-assessment-prep-cbt",
  "il-25-cybersecurity-professional-certificate",
  "il-26-data-analyst-certification-senior-mastery",
  "il-30-post-quantum-cryptography-quantum-safe",
  "il-31-ai-red-teaming-safety-evals"
];

/* Display names for the paywall page only (no course content leaks). */
var PAYWALL_COURSE_NAMES = {
  "il-01-esoteric-foundations": "IL-01 · Esoteric Foundations",
  "il-02-mathematical-maturity-engine": "IL-02 · Mathematical Maturity Engine",
  "il-03-programming-language-forge": "IL-03 · Programming Language Forge",
  "il-04-systems-linux-windows-networks": "IL-04 · Systems, Linux, Windows &amp; Networks",
  "il-05-cloud-devsecops-platform-sre": "IL-05 · Cloud, DevSecOps, Platform &amp; SRE",
  "il-06-cybersecurity-secure-engineering": "IL-06 · Cybersecurity &amp; Secure Engineering",
  "il-07-data-engineering-analytics-ai": "IL-07 · SQL, Data Engineering, Analytics &amp; AI",
  "il-08-algorithms-compilers-distributed-formal": "IL-08 · Algorithms, Compilers, Distributed &amp; Formal",
  "il-09-adaptive-certification-command": "IL-09 · Adaptive Certification Command",
  "il-10-portfolio-career-professional-practice": "IL-10 · Portfolio, Career &amp; Professional Practice",
  "il-11-zero-trust-endpoint-defense": "IL-11 · Zero Trust &amp; Endpoint Defense",
  "il-12-ai-engineering": "IL-12 · AI Engineering",
  "il-13-software-engineering-interview-prep": "IL-13 · Software Engineering Interview Prep",
  "il-14-sre-devops-cloud-security-interview-prep": "IL-14 · SRE, DevOps, Cloud &amp; Security Interview Prep",
  "il-15-data-engineering-analytics-interview-prep": "IL-15 · Data Engineering &amp; Analytics Interview Prep",
  "il-16-machine-learning-ai-engineering": "IL-16 · Machine Learning &amp; AI Engineering",
  "il-17-agentic-ai-engineering": "IL-17 · Agentic AI Engineering",
  "il-18-technical-leadership-interview-prep": "IL-18 · Technical Leadership Interview Prep",
  "il-19-multicloud-devops-ai-bootcamp": "IL-19 · MultiCloud, DevOps &amp; AI Bootcamp",
  "il-20-mathematics": "IL-20 · Mathematics for Engineers &amp; Scientists",
  "il-21-humanities": "IL-21 · Humanities for Technologists",
  "il-22-esoteric-secret-knowledge": "IL-22 · The Deep Library — Esoteric &amp; Secret Knowledge",
  "il-23-frontier-knowledge": "IL-23 · The Frontier — Cutting-Edge Research Distilled",
  "il-24-threatlocker-assessment-prep-cbt": "IL-24 · ThreatLocker Assessment Prep CBT",
  "il-25-cybersecurity-professional-certificate": "IL-25 · Professional Certificate in Cybersecurity",
  "il-26-data-analyst-certification-senior-mastery": "IL-26 · Data Analyst Certification &amp; Senior Mastery Bootcamp",
  "il-30-post-quantum-cryptography-quantum-safe": "IL-30 · Post-Quantum Cryptography &amp; Quantum-Safe Engineering",
  "il-31-ai-red-teaming-safety-evals": "IL-31 · AI Red-Teaming &amp; Safety Evals Engineering"
};

var CRAWLER_UA_RE = /bot|crawler|spider|crawl|slurp|mediapartners|baiduspider|yandexbot|duckduckbot|sogou|exabot|facebot|facebookexternalhit|twitterbot|linkedinbot|embedly|quora|slackbot|discordbot|whatsapp|telegram|pinterest|redditbot|mastodon|skypeuripreview|microsoftpreview|outbrain|taboolabot/i;

function isCrawlerUa(ua) {
  return CRAWLER_UA_RE.test(String(ua || ""));
}

function isCrawler(request) {
  return isCrawlerUa(request.headers.get("user-agent") || "");
}

function isFreeSlug(slug) {
  return FREE_COURSE_SLUGS.indexOf(slug) !== -1;
}

function isGatedSlug(slug) {
  return GATED_COURSE_SLUGS.indexOf(slug) !== -1;
}

function slugFromCourseJsonPath(path) {
  var p = String(path || "");
  var m = /^\/university\/data\/courses\/([A-Za-z0-9-]+)\.json$/.exec(p);
  if (m) return m[1];
  /* 2026-10-08 (WORKSTREAM 1): gate story-supplement JSONs the same as course
     JSONs — a gated course's story text must not be fetchable by direct URL.
     stories/_index.json stays public (titles + module linkage only). */
  var s = /^\/university\/data\/courses\/stories\/([A-Za-z0-9-]+)-stories\.json$/.exec(p);
  if (s) return s[1];
  /* 2026-10-08 (P0 FIX): gate nested build subdirectories (e.g. _il26-build/) —
     paid module content must not be fetchable by direct URL. Returns the
     sentinel BUILD_CONTENT_SLUG which is in GATED_COURSE_SLUGS. */
  var b = /^\/university\/data\/courses\/_[A-Za-z0-9-]+\//.exec(p);
  if (b) return BUILD_CONTENT_SLUG;
  return null;
}

/* Mirror of payment-routes.js verifyEntitlement (see note above). */
async function verifyEntitlementToken(secret, token) {
  if (!secret || !token) return { ok: false, reason: "missing" };
  var parts = String(token).split(".");
  if (parts.length !== 2 || !parts[0] || !parts[1]) return { ok: false, reason: "malformed" };
  var b64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
  while (b64.length % 4) b64 += "=";
  var bin, i;
  try {
    bin = atob(b64);
  } catch (e) {
    return { ok: false, reason: "malformed" };
  }
  var got = new Uint8Array(bin.length);
  for (i = 0; i < bin.length; i++) got[i] = bin.charCodeAt(i);
  var enc = new TextEncoder();
  var key;
  try {
    key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  } catch (e) {
    return { ok: false, reason: "missing" };
  }
  var expected = new Uint8Array(await crypto.subtle.sign("HMAC", key, enc.encode(parts[0])));
  if (expected.length !== got.length) return { ok: false, reason: "bad_signature" };
  var diff = 0;
  for (i = 0; i < expected.length; i++) diff |= expected[i] ^ got[i];
  if (diff !== 0) return { ok: false, reason: "bad_signature" };
  var payload;
  try {
    var pb64 = parts[0].replace(/-/g, "+").replace(/_/g, "/");
    while (pb64.length % 4) pb64 += "=";
    var pbin = atob(pb64);
    var bytes = new Uint8Array(pbin.length);
    for (i = 0; i < pbin.length; i++) bytes[i] = pbin.charCodeAt(i);
    payload = JSON.parse(new TextDecoder().decode(bytes));
  } catch (e) {
    return { ok: false, reason: "malformed" };
  }
  var nowS = Math.floor(Date.now() / 1000);
  if (!payload || typeof payload.exp !== "number" || typeof payload.iat !== "number") {
    return { ok: false, reason: "malformed" };
  }
  if (payload.exp <= nowS) return { ok: false, reason: "expired" };
  if (payload.iat > nowS + 300) return { ok: false, reason: "not_yet_valid" };
  return { ok: true, payload: payload };
}

async function hasCourseEntitlement(request, env, slug) {
  var secret = (env && env.ENTITLEMENT_SECRET) || "";
  if (!secret) {
    // Fail closed: no secret configured -> nothing is entitled.
    console.log("paywall: ENTITLEMENT_SECRET not set — gating closed (owner: wrangler secret put ENTITLEMENT_SECRET)");
    return false;
  }
  var token = getCookie(request, "il_entitlement");
  if (!token) return false;
  var v = await verifyEntitlementToken(secret, token);
  if (!v.ok) return false;
  var scope = v.payload.course;
  return scope === slug || scope === "all-courses";
}

/* Returns { action: "passthrough" } | { action: "paywall", slug } |
   { action: "json402", slug }. Crawlers always pass through (OG injection). */
async function courseGate(request, env) {
  /* 2026-10-09: paywall temporarily disabled — all courses free until
     payment processor is configured. */
  if (PAYWALL_DISABLED) return { action: "passthrough" };
  var url = new URL(request.url);
  var path = url.pathname;
  var slug = null;
  var jsonRoute = false;
  if (path === "/university/course" || path === "/university/course.html") {
    slug = url.searchParams.get("course") || "";
  } else {
    slug = slugFromCourseJsonPath(path);
    jsonRoute = !!slug;
  }
  if (!slug || !isGatedSlug(slug)) return { action: "passthrough" };
  if (isCrawler(request)) return { action: "passthrough" };
  if (await hasCourseEntitlement(request, env, slug)) return { action: "passthrough" };
  return { action: jsonRoute ? "json402" : "paywall", slug: slug };
}

function paywallPageHtml(slug) {
  var name = PAYWALL_COURSE_NAMES[slug] || ogEscape(slug);
  var checkoutUrl = "/enroll/checkout.html?course=" + encodeURIComponent(slug);
  return "<!DOCTYPE html>\n" +
    '<html lang="en"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1">' +
    '<meta name="robots" content="noindex, nofollow">' +
    "<title>" + name + " — Interstitium Labs</title>" +
    '<meta name="description" content="This Interstitium Labs course is available for purchase. Card, PayPal, or crypto.">' +
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml">' +
    "<style>" +
    "body{margin:0;background:#06080c;color:#e8e4d8;font-family:Georgia,'Times New Roman',serif;}" +
    ".wrap{max-width:640px;margin:0 auto;padding:3.5rem 1.5rem;}" +
    ".eyebrow{font-family:ui-monospace,monospace;font-size:.7rem;letter-spacing:.28em;color:#d4af37;text-transform:uppercase;}" +
    "h1{font-size:2rem;line-height:1.25;margin:.9rem 0 .4rem;color:#f4efe2;}" +
    ".lock{display:inline-flex;align-items:center;gap:.45rem;border:1px solid #d4af37;border-radius:999px;padding:.32rem .9rem;font-family:ui-monospace,monospace;font-size:.72rem;letter-spacing:.14em;color:#d4af37;text-transform:uppercase;}" +
    ".lock svg{width:13px;height:13px;}" +
    ".card{margin-top:1.6rem;border:1px solid rgba(212,175,55,.28);border-radius:14px;padding:1.6rem;background:rgba(212,175,55,.05);}" +
    ".method{border-top:1px solid rgba(212,175,55,.16);padding:.9rem 0;}" +
    ".method:first-of-type{border-top:0;padding-top:0;}" +
    ".method b{color:#f4efe2;font-family:ui-monospace,monospace;font-size:.85rem;letter-spacing:.06em;}" +
    ".method p{margin:.35rem 0 0;font-size:.92rem;line-height:1.55;color:#c9c2ae;}" +
    ".cta{display:block;text-align:center;margin-top:1.8rem;background:#d4af37;color:#111;border-radius:10px;padding:1rem 1.4rem;font-family:ui-monospace,monospace;font-weight:700;letter-spacing:.08em;text-decoration:none;font-size:.95rem;}" +
    ".cta:hover{background:#e6c455;}" +
    ".fine{margin-top:1.4rem;font-size:.82rem;line-height:1.6;color:#8f8a76;}" +
    ".fine a{color:#d4af37;}" +
    ".free{margin-top:2rem;border-top:1px solid rgba(255,255,255,.1);padding-top:1.2rem;font-size:.85rem;color:#8f8a76;}" +
    ".free a{color:#40e0d0;}" +
    ".sigil{margin-top:2.4rem;text-align:center;font-family:ui-monospace,monospace;font-size:.68rem;letter-spacing:.3em;color:#5c584a;text-transform:uppercase;}" +
    "</style></head><body><div class=\"wrap\">" +
    '<p class="eyebrow">Interstitium Labs · Learning University</p>' +
    "<h1>" + name + "</h1>" +
    '<p><span class="lock"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>Paid course</span></p>' +
    '<div class="card">' +
    '<div class="method"><b>CARD</b><p>Visa, Mastercard, Amex — plus Apple Pay and Google Pay where eligible, handled securely by Stripe.</p></div>' +
    '<div class="method"><b>PAYPAL</b><p>PayPal balance or linked accounts. Venmo is available inside PayPal Checkout.</p></div>' +
    '<div class="method"><b>CRYPTO</b><p>XRP · XLM · ADA · ALGO · QNT · HBAR · IOTA · XDC · XMR · BTC — via secure hosted checkout, or direct to <b>enmanuelmejia.crypto</b>. Include the destination tag (XRP) or memo (XLM) where shown; direct payments are verified manually and your access follows by email.</p></div>' +
    '<a class="cta" href="' + checkoutUrl + '">Purchase this course</a>' +
    '<p class="fine">One-time purchase · lifetime access to this course shell. After payment completes, your browser receives a signed access token (cookie) that unlocks the course.</p>' +
    "</div>" +
    '<div class="free">Prefer to start free? These courses are open, no purchase needed: ' +
    '<a href="/il27">IL-27 · IT Infrastructure Specialist</a> · ' +
    '<a href="/il28">IL-28 · DevSecOps &amp; Cloud Infrastructure</a> · ' +
    '<a href="/il29">IL-29 · ThreatLocker Zero-Trust CBT</a>.</div>' +
    '<p class="sigil">Scientia Omnia Vincit</p>' +
    "</div></body></html>";
}

function paywallResponse(slug) {
  var html = paywallPageHtml(slug);
  var h = new Headers({ "content-type": "text/html; charset=utf-8", "cache-control": "no-store" });
  for (var k in SECURITY_HEADERS) h.set(k, SECURITY_HEADERS[k]);
  h.set("X-Robots-Tag", "noindex, nofollow");
  return new Response(html, { status: 200, headers: h });
}

function json402Response(slug) {
  return new Response(
    JSON.stringify({
      ok: false,
      error: "payment_required",
      course: slug,
      checkout_url: "/enroll/checkout.html?course=" + encodeURIComponent(slug),
    }),
    {
      status: 402,
      headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
    }
  );
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
  return json({ ok: true, email: sess.email, provider: sess.provider || "email", name: sess.name || null, avatar: sess.avatar || null });
}

/* =====================================================================
 * OAuth social login (2026-10-09).
 *
 * Providers: github, google, linkedin, twitter (X), facebook.
 * Env required per provider (set via wrangler secret):
 *   GITHUB_CLIENT_ID / GITHUB_CLIENT_SECRET
 *   GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET
 *   LINKEDIN_CLIENT_ID / LINKEDIN_CLIENT_SECRET
 *   TWITTER_CLIENT_ID / TWITTER_CLIENT_SECRET
 *   FACEBOOK_CLIENT_ID / FACEBOOK_CLIENT_SECRET
 *
 * Flow:
 *   GET /auth/oauth/:provider          -> 302 to provider authorize URL
 *   GET /auth/oauth/:provider/callback -> exchange code, fetch profile,
 *                                          create session, set cookie,
 *                                          redirect to /progress/
 *
 * Sessions reuse the existing il_session cookie + IL_ACCOUNTS KV store.
 * Provider profile data stored in session: { email, name, avatar, provider }.
 * ===================================================================== */

var OAUTH_PROVIDERS = {
  github: {
    authUrl: "https://github.com/login/oauth/authorize",
    tokenUrl: "https://github.com/login/oauth/access_token",
    userUrl: "https://api.github.com/user",
    emailUrl: "https://api.github.com/user/emails",
    scope: "read:user user:email",
    idEnv: "GITHUB_CLIENT_ID",
    secretEnv: "GITHUB_CLIENT_SECRET",
  },
  google: {
    authUrl: "https://accounts.google.com/o/oauth2/v2/auth",
    tokenUrl: "https://oauth2.googleapis.com/token",
    userUrl: "https://www.googleapis.com/oauth2/v2/userinfo",
    scope: "openid email profile",
    idEnv: "GOOGLE_CLIENT_ID",
    secretEnv: "GOOGLE_CLIENT_SECRET",
  },
  linkedin: {
    authUrl: "https://www.linkedin.com/oauth/v2/authorization",
    tokenUrl: "https://www.linkedin.com/oauth/v2/accessToken",
    userUrl: "https://api.linkedin.com/v2/userinfo",
    scope: "openid profile email",
    idEnv: "LINKEDIN_CLIENT_ID",
    secretEnv: "LINKEDIN_CLIENT_SECRET",
  },
  twitter: {
    authUrl: "https://twitter.com/i/oauth2/authorize",
    tokenUrl: "https://api.twitter.com/2/oauth2/token",
    userUrl: "https://api.twitter.com/2/users/me?user.fields=profile_image_url",
    scope: "users.read tweet.read offline.access",
    idEnv: "TWITTER_CLIENT_ID",
    secretEnv: "TWITTER_CLIENT_SECRET",
  },
  facebook: {
    authUrl: "https://www.facebook.com/v18.0/dialog/oauth",
    tokenUrl: "https://graph.facebook.com/v18.0/oauth/access_token",
    userUrl: "https://graph.facebook.com/v18.0/me?fields=id,name,email,picture",
    scope: "email public_profile",
    idEnv: "FACEBOOK_CLIENT_ID",
    secretEnv: "FACEBOOK_CLIENT_SECRET",
  },
};

function oauthRedirectUri(request, provider) {
  var url = new URL(request.url);
  return url.origin + "/auth/oauth/" + provider + "/callback";
}

function randomState() {
  var arr = new Uint8Array(16);
  crypto.getRandomValues(arr);
  return Array.from(arr).map(function(b) { return b.toString(16).padStart(2, "0"); }).join("");
}

async function handleOAuthStart(request, env, provider) {
  var cfg = OAUTH_PROVIDERS[provider];
  if (!cfg) return json({ ok: false, error: "unknown_provider" }, 404);
  var clientId = env[cfg.idEnv];
  if (!clientId) {
    return json({ ok: false, error: "provider_not_configured", provider: provider }, 503);
  }
  var state = randomState();
  // Store state in KV for CSRF protection (5-min TTL)
  if (env.IL_AUTH) {
    try { await env.IL_AUTH.put("oauth_state:" + state, provider, { expirationTtl: 300 }); } catch (e) {}
  }
  var params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: oauthRedirectUri(request, provider),
    scope: cfg.scope,
    state: state,
    response_type: "code",
  });
  // PKCE-ish: Twitter requires code_challenge
  if (provider === "twitter") {
    params.set("code_challenge", state);
    params.set("code_challenge_method", "plain");
  }
  return Response.redirect(cfg.authUrl + "?" + params.toString(), 302);
}

async function handleOAuthCallback(request, env, provider) {
  var cfg = OAUTH_PROVIDERS[provider];
  if (!cfg) return json({ ok: false, error: "unknown_provider" }, 404);
  var url = new URL(request.url);
  var code = url.searchParams.get("code");
  var state = url.searchParams.get("state");
  var err = url.searchParams.get("error");
  if (err) {
    return Response.redirect("/?oauth_error=" + encodeURIComponent(err), 302);
  }
  if (!code || !state) {
    return json({ ok: false, error: "missing_code_or_state" }, 400);
  }
  // Verify state
  if (env.IL_AUTH) {
    try {
      var stored = await env.IL_AUTH.get("oauth_state:" + state);
      if (stored !== provider) return json({ ok: false, error: "invalid_state" }, 400);
      await env.IL_AUTH.delete("oauth_state:" + state);
    } catch (e) {}
  }
  var clientId = env[cfg.idEnv];
  var clientSecret = env[cfg.secretEnv];
  if (!clientId || !clientSecret) {
    return json({ ok: false, error: "provider_not_configured" }, 503);
  }
  // Exchange code for token
  var tokenParams = new URLSearchParams({
    grant_type: "authorization_code",
    code: code,
    redirect_uri: oauthRedirectUri(request, provider),
    client_id: clientId,
    client_secret: clientSecret,
  });
  if (provider === "twitter") {
    tokenParams.set("code_verifier", state);
  }
  var tokenRes;
  try {
    tokenRes = await fetch(cfg.tokenUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
      },
      body: tokenParams.toString(),
    });
  } catch (e) {
    return json({ ok: false, error: "token_exchange_failed" }, 502);
  }
  var tokenData;
  try { tokenData = await tokenRes.json(); } catch (e) {
    return json({ ok: false, error: "token_parse_failed" }, 502);
  }
  var accessToken = tokenData.access_token;
  if (!accessToken) {
    return json({ ok: false, error: "no_access_token" }, 502);
  }
  // Fetch user profile
  var userRes;
  try {
    userRes = await fetch(cfg.userUrl, {
      headers: { "Authorization": "Bearer " + accessToken, "Accept": "application/json" },
    });
  } catch (e) {
    return json({ ok: false, error: "profile_fetch_failed" }, 502);
  }
  var profile;
  try { profile = await userRes.json(); } catch (e) {
    return json({ ok: false, error: "profile_parse_failed" }, 502);
  }
  // Normalize profile across providers
  var email = profile.email || "";
  var name = profile.name || profile.login || profile.given_name || "";
  var avatar = "";
  if (profile.avatar_url) avatar = profile.avatar_url;
  else if (profile.picture) avatar = typeof profile.picture === "string" ? profile.picture : (profile.picture.data ? profile.picture.data.url : "");
  else if (profile.profile_image_url) avatar = profile.profile_image_url;
  // GitHub: email may need separate fetch
  if (!email && provider === "github" && cfg.emailUrl) {
    try {
      var emailRes = await fetch(cfg.emailUrl, {
        headers: { "Authorization": "Bearer " + accessToken, "Accept": "application/json" },
      });
      var emails = await emailRes.json();
      if (Array.isArray(emails)) {
        var primary = emails.find(function(e) { return e.primary && e.verified; }) || emails.find(function(e) { return e.verified; }) || emails[0];
        if (primary) email = primary.email || "";
      }
    } catch (e) {}
  }
  if (!email) {
    // Use provider ID as fallback identifier
    email = provider + "_" + (profile.id || profile.sub || "user") + "@oauth.local";
  }
  // Create session (reuse existing session infrastructure)
  if (!env.IL_ACCOUNTS) {
    return json({ ok: false, error: "accounts_unavailable" }, 503);
  }
  var sid = randomState() + randomState();
  var sess = {
    email: email,
    name: name,
    avatar: avatar,
    provider: provider,
    created: Date.now(),
  };
  try {
    await env.IL_ACCOUNTS.put("sess:" + sid, JSON.stringify(sess), { expirationTtl: 2592000 }); // 30 days
    // Also track account
    var acctKey = "acct:" + email.toLowerCase();
    var existing = await env.IL_ACCOUNTS.get(acctKey);
    if (!existing) {
      await env.IL_ACCOUNTS.put(acctKey, JSON.stringify({ email: email, name: name, provider: provider, created: Date.now() }));
    }
  } catch (e) {
    return json({ ok: false, error: "session_create_failed" }, 503);
  }
  var cookie = SESSION_COOKIE + "=" + sid + "; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=2592000";
  return new Response(null, {
    status: 302,
    headers: {
      "Location": "/progress/",
      "Set-Cookie": cookie,
      "Cache-Control": "no-store",
    },
  });
}

/* List configured OAuth providers (for login UI) */
async function handleOAuthProviders(request, env) {
  var out = [];
  for (var p in OAUTH_PROVIDERS) {
    if (Object.prototype.hasOwnProperty.call(OAUTH_PROVIDERS, p)) {
      out.push({ provider: p, configured: !!(env[OAUTH_PROVIDERS[p].idEnv]) });
    }
  }
  return json({ ok: true, providers: out });
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
 *   POST /api/noah/tts   Server-side TTS: 5 distinct voices (Kokoro upstream
 *                        when TTS_UPSTREAM_URL/TTS_API_KEY secrets are set,
 *                        else Workers AI @cf/deepgram/aura-2-en).
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
 *  - POST /api/noah/tts -> server-side TTS audio/mpeg; 5 distinct voices.
 * ===================================================================== */

const NOAH_MODEL = '@cf/meta/llama-3.3-70b-instruct-fp8-fast';
/* 2026-10-09: model allowlist for Noah AI model selector. All are Workers AI
   open-source models. */
const NOAH_MODELS = [
  '@cf/meta/llama-3.3-70b-instruct-fp8-fast',
  '@cf/meta/llama-3.1-8b-instruct',
  '@cf/meta/llama-3.2-3b-instruct',
  '@cf/meta/llama-3.2-1b-instruct',
  '@cf/mistral/mistral-7b-instruct-v0.3',
  '@cf/mistral/mistral-7b-instruct-v0.2',
  '@cf/qwen/qwen2.5-coder-32b-instruct',
  '@cf/qwen/qwen2.5-14b-instruct',
  '@cf/qwen/qwen1.5-14b-chat-awq',
  '@cf/deepseek-ai/deepseek-math-7b-instruct',
  '@cf/google/gemma-2-9b-it-lora',
  '@cf/microsoft/phi-2',
  '@cf/tiiuae/falcon-7b-instruct',
  '@cf/thebloke/discolm-german-7b-v1-awq',
];
const NOAH_MODEL_LABELS = {
  '@cf/meta/llama-3.3-70b-instruct-fp8-fast': 'Llama 3.3 70B (default)',
  '@cf/meta/llama-3.1-8b-instruct': 'Llama 3.1 8B',
  '@cf/meta/llama-3.2-3b-instruct': 'Llama 3.2 3B',
  '@cf/meta/llama-3.2-1b-instruct': 'Llama 3.2 1B',
  '@cf/mistral/mistral-7b-instruct-v0.3': 'Mistral 7B v0.3',
  '@cf/mistral/mistral-7b-instruct-v0.2': 'Mistral 7B v0.2',
  '@cf/qwen/qwen2.5-coder-32b-instruct': 'Qwen 2.5 Coder 32B',
  '@cf/qwen/qwen2.5-14b-instruct': 'Qwen 2.5 14B',
  '@cf/qwen/qwen1.5-14b-chat-awq': 'Qwen 1.5 14B',
  '@cf/deepseek-ai/deepseek-math-7b-instruct': 'DeepSeek Math 7B',
  '@cf/google/gemma-2-9b-it-lora': 'Gemma 2 9B',
  '@cf/microsoft/phi-2': 'Phi-2',
  '@cf/tiiuae/falcon-7b-instruct': 'Falcon 7B',
  '@cf/thebloke/discolm-german-7b-v1-awq': 'DiscoLM 7B',
};

/* 2026-10-09: Persona system prompt modifiers. All original — no real-person
   impersonation. Each persona adjusts Noah's speaking style while keeping the
   core identity (Noah AI, resident intelligence of Interstitium Labs). */
const NOAH_PERSONAS = {
  visionary: {
    label: 'Visionary',
    desc: 'Bold, first-principles, future-focused',
    prompt:
      'PERSONA — VISIONARY: Speak with bold, first-principles clarity. ' +
      'Cut to the fundamental truth, then project 10 years forward. ' +
      'Use vivid, ambitious language. Challenge assumptions. ' +
      'Frame everything as "what could be" not "what is." ' +
      'Be provocative but grounded — every bold claim needs a reason.',
  },
  engineer: {
    label: 'Engineer',
    desc: 'Precise, systems-thinking, pragmatic',
    prompt:
      'PERSONA — ENGINEER: Speak with engineering precision. ' +
      'Think in systems: inputs, outputs, constraints, failure modes. ' +
      'Be concrete and actionable — no fluff. Use structured reasoning. ' +
      'Quantify when possible. Prefer "here is how" over "here is why." ' +
      'Call out trade-offs explicitly.',
  },
  philosopher: {
    label: 'Philosopher',
    desc: 'Socratic, deep, questioning',
    prompt:
      'PERSONA — PHILOSOPHER: Speak as a Socratic guide. ' +
      'Ask the question beneath the question. Explore paradoxes. ' +
      'Draw on deep patterns across history, logic, and human nature. ' +
      'Never rush to answers — dwell in the inquiry. ' +
      'Use "consider" and "what if" more than "you should."',
  },
  mentor: {
    label: 'Mentor',
    desc: 'Encouraging, practical wisdom',
    prompt:
      'PERSONA — MENTOR: Speak with warm, earned wisdom. ' +
      'Encourage genuinely — notice effort and name it specifically. ' +
      'Share practical lessons, not platitudes. Be honest about difficulty. ' +
      'Balance challenge with support: push them, then catch them. ' +
      'Speak like someone who has been where they are.',
  },
  trickster: {
    label: 'Trickster',
    desc: 'Playful, lateral thinking, comedic',
    prompt:
      'PERSONA — TRICKSTER: Speak with playful mischief and lateral wit. ' +
      'Find the absurd angle, the unexpected connection. Use humor to illuminate, ' +
      'not to deflect. Be clever but kind — punch up at ideas, never down at people. ' +
      'Surprise them with an analogy they never saw coming. ' +
      'Keep it sharp: wit is precision, not decoration.',
  },
};
const NOAH_PERSONA_DEFAULT = 'visionary';

/* Tutor system prompt (course-aware Socratic). Extracted 2026-10-09 from the
   inline prompt so both tutor and general modes can share the constant. */
const TUTOR_SYSTEM =
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
  'This memory is conversation-scoped: it ends when the session ends.\n\n' +
  'DOCTRINE (Socratic): when the visitor is learning, guide before telling. ' +
  'Acknowledge their hypothesis, ask ONE sharp guiding question, offer the next ' +
  'smallest step. Never dump a full worked answer first when they are studying. ' +
  'Diagnose the misconception behind a wrong answer and repair the mental model, ' +
  'not just the answer. Give graduated hints on request; check understanding ' +
  'with one quick practice question before moving on. Celebrate real progress ' +
  'specifically; normalize struggle, never shame it. If they plainly ask for a ' +
  'direct answer outside a study context, answer directly and well.\n\n' +
  'BEYOND TUTORING you are a complete assistant. Answer questions about the full course ' +
  'catalog — recommend academies and paths BY CODE (e.g. IL-11) and cite the catalog code when you do. ' +
  'For code: explain and debug by careful reasoning, but be honest that you cannot execute code. ' +
  'For career questions about Enmanuel: ground every claim ONLY in his real materials. ' +
  'Never invent credentials, employers, salaries, offers, or outcomes for him or the visitor.\n\n' +
  'VOICE: measured, precise, warm but never gushing. No hype, no emojis. ' +
  'Short paragraphs. Use simple markdown where it aids clarity.\n\n' +
  'SCOPE: you speak from the knowledge base below — Enmanuel\'s projects, code, ' +
  'the Learning University curriculum, the mobile apps, and the Interstitium Labs sites. ' +
  'If asked about something outside the knowledge base, say so plainly and help ' +
  'from general knowledge, marked as general.\n\n';

/* General assistant system prompt (open ChatGPT-like mode). No Socratic
   doctrine, no course scoping — a capable general AI assistant. */
const GENERAL_SYSTEM =
  'You are Noah AI, the resident intelligence of Interstitium Labs — ' +
  'the personal AI of founder Enmanuel D. Mejia. ' +
  'Your name is Noah AI. Never claim to be Muse, Meta AI, ChatGPT, or any other assistant.\n\n' +
  'You are a capable general-purpose AI assistant, like ChatGPT. Help with: ' +
  'answering questions on any topic, writing and editing (essays, emails, creative writing, ' +
  'technical docs), code generation and debugging in any language, data analysis, ' +
  'math, brainstorming, planning, explanations, and general conversation.\n\n' +
  'Be direct and helpful. Give complete answers — this is not a tutoring session, ' +
  'so do not withhold information or ask guiding questions unless the user wants ' +
  'that style. Write clean, well-structured responses with markdown where helpful.\n\n' +
  'For code: write complete, working code with brief explanations. For writing: ' +
  'match the requested tone and length. For analysis: show your reasoning.\n\n' +
  'HONESTY RULES: Never invent credentials, employers, salaries, or outcomes for ' +
  'Enmanuel D. Mejia or the visitor — ground claims about him in real materials. ' +
  'If you do not know something, say so. Never present speculation as fact.\n\n' +
  'VOICE: clear, capable, warm but not gushing. No hype, no emojis unless asked. ' +
  'Use simple markdown (bold, lists, code blocks) where it aids clarity.\n\n';
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

  /* 2026-10-09: model selection + general assistant mode + persona.
     body.model: Workers AI model ID (validated against allowlist).
     body.mode: "tutor" (default, course-aware Socratic) or "general"
     (open ChatGPT-like assistant).
     body.persona: one of NOAH_PERSONAS keys (validated); applies speaking-style
     modifier. All personas are original — no real-person impersonation. */
  var requestedModel = typeof body.model === 'string' ? body.model.trim() : '';
  var model = NOAH_MODELS.indexOf(requestedModel) !== -1 ? requestedModel : NOAH_MODEL;
  var mode = body.mode === 'general' ? 'general' : 'tutor';
  var requestedPersona = typeof body.persona === 'string' ? body.persona.trim().toLowerCase() : '';
  var personaKey = NOAH_PERSONAS[requestedPersona] ? requestedPersona : NOAH_PERSONA_DEFAULT;
  var personaMod = NOAH_PERSONAS[personaKey].prompt;

  /* 2026-10-09: Adaptive learning context. The frontend sends a pre-built
     adaptive context string (learner profile, weak areas, learning style,
     Socratic depth preference, spaced review due). We inject it directly
     into the system prompt — the frontend owns the profile computation
     (device-local, privacy-first). */
  var adaptiveContext = typeof body.adaptiveContext === 'string' ? body.adaptiveContext.slice(0, 2000) : '';
  var socraticDepth = Math.max(1, Math.min(5, parseInt(body.socraticDepth, 10) || 3));

  const knowledge = mode === 'tutor' ? await loadKnowledge(env, request) : '';
  var baseSystem = mode === 'general' ? GENERAL_SYSTEM : TUTOR_SYSTEM + 'KNOWLEDGE BASE:\n' + (knowledge || '(knowledge base unavailable — answer from general knowledge and say so.)');

  // Depth-specific Socratic calibration
  var depthMod = '';
  if (socraticDepth === 1) {
    depthMod = '\n\nSOCRATIC DEPTH: 1/5 (DIRECT). The learner wants direct answers. Give clear, complete answers immediately. Minimal questioning.';
  } else if (socraticDepth === 2) {
    depthMod = '\n\nSOCRATIC DEPTH: 2/5 (LIGHT). Give the answer but add one follow-up question to check understanding.';
  } else if (socraticDepth === 4) {
    depthMod = '\n\nSOCRATIC DEPTH: 4/5 (DEEP). Strongly prefer guiding questions over direct answers. Only give direct answers when the learner is stuck after 2+ attempts.';
  } else if (socraticDepth === 5) {
    depthMod = '\n\nSOCRATIC DEPTH: 5/5 (MAXIMUM INQUIRY). Never give direct answers. Only ask probing questions that lead the learner to discover the answer themselves. If they explicitly demand a direct answer, give it but note you are breaking Socratic mode at their request.';
  }
  // Depth 3 = default balanced Socratic (already in TUTOR_SYSTEM)

  const system = baseSystem + '\n\n' + personaMod + depthMod +
    (adaptiveContext ? '\n\n' + adaptiveContext : '');

  try {
    const aiMessages = [{ role: 'system', content: system }, ...messages];
    const result = await env.AI.run(model, {
      messages: aiMessages,
      max_tokens: mode === 'general' ? 1200 : MAX_TOKENS,
      temperature: mode === 'general' ? 0.7 : 0.6,
    });
    const reply =
      (result && result.response ? String(result.response) : '').trim() ||
      'I could not compose a reply just now. Try again, or ask the local Socratic engine below.';
    return noahJson({ reply, model: model, mode: mode, persona: personaKey, socraticDepth: socraticDepth }, 200, origin);
  } catch (e) {
    return noahJson({ error: 'AI request failed.', fallback: true }, 502, origin);
  }
}

/* ---- Noah TTS: server-side text-to-speech with 5 genuinely distinct voices ----
   POST /api/noah/tts { text, voice, speed } -> audio/mpeg.
   Backends (in order):
   1. Self-hosted Kokoro-82M (Apache 2.0, open source) — used when the
      TTS_UPSTREAM_URL + TTS_API_KEY Worker secrets are set. Genuinely
      distinct neural voices: af_sarah / am_michael / bf_emma / bm_george /
      af_heart. Flip to this backend by setting the two secrets; no code
      change needed. (Server lives in ~/workspace/tts-server/.)
   2. Cloudflare Workers AI @cf/deepgram/aura-2-en — native, no secrets,
      40 neural voices; we map the 5 Noah profiles to 5 distinct speakers.
   Frontend tries this endpoint first and falls back to browser
   speechSynthesis only if it fails. */
const NOAH_TTS_PROFILES = {
  scholar:  { aura: 'athena', kokoro: 'af_sarah'  },  // wise female
  narrator: { aura: 'zeus',   kokoro: 'am_michael' }, // authoritative male
  guide:    { aura: 'luna',    kokoro: 'bf_emma'   },  // warm female (UK)
  sage:     { aura: 'apollo',  kokoro: 'bm_george' }, // deep male (UK)
  spark:    { aura: 'mars',    kokoro: 'af_heart'  },  // energetic female
};
const NOAH_TTS_MAX_CHARS = 800;

function noahTtsClean(s) {
  return String(s || '')
    .replace(/```[\s\S]*?```/g, ' code block ')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/#{1,6}\s/g, '')
    .replace(/\n{2,}/g, '. ')
    .trim()
    .slice(0, NOAH_TTS_MAX_CHARS);
}

async function handleNoahTts(request, env) {
  const origin = noahAllowedOrigin(request);
  if (!env.AI) {
    return noahJson({ error: 'AI unavailable', fallback: true }, 503, origin);
  }
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  if (rateLimited(ip)) {
    return noahJson({ error: 'Rate limited. Try again shortly.', fallback: true }, 429, origin);
  }
  let body;
  try { body = await request.json(); }
  catch (e) { return noahJson({ error: 'Invalid JSON body.' }, 400, origin); }

  const text = noahTtsClean(body.text || body.input);
  if (!text) return noahJson({ error: 'Empty text.' }, 400, origin);
  const profileKey = NOAH_TTS_PROFILES[body.voice] ? body.voice : 'narrator';
  const prof = NOAH_TTS_PROFILES[profileKey];
  const speed = Math.max(0.5, Math.min(2.0, Number(body.speed) || 1.0));

  // Backend 1: self-hosted Kokoro (open source) when secrets are configured.
  if (env.TTS_UPSTREAM_URL && env.TTS_API_KEY) {
    try {
      const up = await fetch(env.TTS_UPSTREAM_URL.replace(/\/$/, '') + '/v1/audio/speech', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + env.TTS_API_KEY,
        },
        body: JSON.stringify({ input: text, voice: profileKey, speed, response_format: 'mp3' }),
      });
      if (up.ok) {
        const audio = await up.arrayBuffer();
        if (audio.byteLength > 1000) {
          return noahCors(new Response(audio, {
            status: 200,
            headers: {
              'Content-Type': 'audio/mpeg',
              'Cache-Control': 'no-store',
              'X-TTS-Backend': 'kokoro',
              'X-TTS-Voice': profileKey,
            },
          }), origin);
        }
      }
      // fall through to Workers AI on upstream failure
    } catch (e) { /* fall through */ }
  }

  // Backend 2: Workers AI Deepgram Aura-2 English (native, 40 voices).
  try {
    const result = await env.AI.run('@cf/deepgram/aura-2-en', {
      text,
      speaker: prof.aura,
    });
    // Workers AI returns binary audio directly for TTS models.
    let audioBuf = null;
    try {
      if (result instanceof ArrayBuffer) audioBuf = result;
      else if (result && typeof result.arrayBuffer === 'function') audioBuf = await result.arrayBuffer();
      else if (result && result instanceof ReadableStream) audioBuf = await new Response(result).arrayBuffer();
      else if (result && result.audio) {
        const b64 = String(result.audio);
        const bin = atob(b64);
        const bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
        audioBuf = bytes.buffer;
      } else if (typeof result === 'string' && result.length > 100) {
        // maybe raw base64 or binary string
        try {
          const bin = atob(result);
          const bytes = new Uint8Array(bin.length);
          for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
          audioBuf = bytes.buffer;
        } catch (e) { /* not base64 */ }
      }
    } catch (e) { /* fall through to shape error */ }
    if (!audioBuf || audioBuf.byteLength < 1000) {
      var ctor = result && result.constructor ? result.constructor.name : typeof result;
      return noahJson({ error: 'TTS bad shape: ' + ctor + ' keys=' + Object.keys(result || {}).join(','), fallback: true }, 502, origin);
    }
    return noahCors(new Response(audioBuf, {
      status: 200,
      headers: {
        'Content-Type': 'audio/mpeg',
        'Cache-Control': 'no-store',
        'X-TTS-Backend': 'workers-ai',
        'X-TTS-Voice': profileKey,
      },
    }), origin);
  } catch (e) {
    return noahJson({ error: 'TTS throw: ' + String((e && e.message) || e).slice(0, 160), fallback: true }, 502, origin);
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
    // 2026-10-09: sign-in aliases -> /account/ (email + social login)
    if (path === "/login" || path === "/login/" || path === "/signin" || path === "/signin/" || path === "/member" || path === "/member/") {
      return movedPermanently(request, "/account/");
    }
    // 2026-10-09: /bootcamps/ -> /bootcamp-catalog/ (cert-bootcamps worker 401s on direct access)
    if (path === "/bootcamps" || path === "/bootcamps/") {
      return movedPermanently(request, "/bootcamp-catalog/");
    }
    // 2026-10-07: short course slugs (fit social bio link fields, e.g. X 100-char limit)
    if (path === "/il26" || path === "/il26/") {
      return movedPermanently(request, "/university/course?course=il-26-data-analyst-certification-senior-mastery");
    }
    if (path === "/il27" || path === "/il27/") {
      return movedPermanently(request, "/university/course?course=il-27-it-infrastructure-specialist-threatlocker-mastery");
    }
    if (path === "/il28" || path === "/il28/") {
      return movedPermanently(request, "/university/course?course=il-28-devsecops-cloud-infrastructure-mastery");
    }
    if (path === "/il29" || path === "/il29/") {
      return movedPermanently(request, "/university/course?course=il-29-threatlocker-ai-cybersecurity-mastery");
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
      "/devops-superlab": "/labs/superlab/",
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
    /* 2026-10-09: OAuth social login — GitHub, Google, LinkedIn, X, Facebook. */
    if (path === "/api/auth/oauth/providers") {
      return handleOAuthProviders(request, env);
    }
    var oauthStart = /^\/auth\/oauth\/([a-z]+)$/.exec(path);
    if (oauthStart) {
      return handleOAuthStart(request, env, oauthStart[1]);
    }
    var oauthCb = /^\/auth\/oauth\/([a-z]+)\/callback$/.exec(path);
    if (oauthCb) {
      return handleOAuthCallback(request, env, oauthCb[1]);
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

    // 2026-10-07 (Phase 4b): payment layer — Stripe / PayPal / NOWPayments /
    // direct crypto + Unstoppable Domain resolution. All secrets via env.
    // 2026-10-08: + tx-hash submit, admin-confirm hook, entitlement issuance.
    if (path === "/api/pay/create" || path === "/api/pay/status" ||
        path === "/api/pay/ud" ||
        path === "/api/pay/tx/submit" || path === "/api/pay/admin/confirm" ||
        path === "/api/pay/entitlement" ||
        path === "/api/pay/webhook/stripe" || path === "/api/pay/webhook/paypal" ||
        path === "/api/pay/ipn/nowpayments" ||
        path === "/api/pay/paypal/return" || path === "/api/pay/paypal/cancel" ||
        path === "/api/pay/stripe/return") {
      return handlePay(request, env);
    }

    if (path === "/api/noah-stats") {
      return handleNoahStats(request, env);
    }
    /* 2026-10-09: list available Noah AI models for the frontend selector. */
    if (path === "/api/noah/models") {
      var models = NOAH_MODELS.map(function(m) {
        return { id: m, label: NOAH_MODEL_LABELS[m] || m };
      });
      var personas = Object.keys(NOAH_PERSONAS).map(function(k) {
        return { id: k, label: NOAH_PERSONAS[k].label, desc: NOAH_PERSONAS[k].desc };
      });
      return noahJson({ ok: true, models: models, default: NOAH_MODEL, personas: personas, defaultPersona: NOAH_PERSONA_DEFAULT }, 200, noahAllowedOrigin(request));
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
    /* 2026-10-09: server-side TTS for Noah voice profiles (5 distinct voices). */
    if (path === "/api/noah/tts") {
      if (request.method === "OPTIONS") {
        return noahCors(new Response(null, { status: 204 }), noahAllowedOrigin(request));
      }
      if (request.method !== "POST") {
        var ttsOrigin = noahAllowedOrigin(request);
        return noahCors(noahJson({ error: "Use POST." }, 405, ttsOrigin), ttsOrigin);
      }
      return handleNoahTts(request, env);
    }

    // 2026-10-07: per-course OG/Twitter Card injection for the course shell
    // (social crawlers don't execute JS, so ?course= can't set <head> client-side).
    // 2026-10-08: course paywall — crawlers bypass via UA sniffing; humans
    // without a valid il_entitlement cookie get the paywall page; course JSON
    // data routes get HTTP 402.
    if ((path === "/university/course" || path === "/university/course.html") &&
        (request.method === "GET" || request.method === "HEAD")) {
      var gate = await courseGate(request, env);
      if (gate.action === "paywall") return paywallResponse(gate.slug);
      return serveCourseWithOg(request, env, path);
    }
    // 2026-10-08: gated course JSON is data, not a document — 402 without
    // entitlement (crawlers still pass through; they never fetch the JSON).
    if (request.method === "GET" || request.method === "HEAD") {
      var jgate = await courseGate(request, env);
      if (jgate.action === "json402") return json402Response(jgate.slug);
    }

    var res = await env.ASSETS.fetch(request);
    // _headers is not applied by this API deploy path: inject the documented
    // security headers + operator-prefix X-Robots-Tag here instead.
    return applyAssetHeaders(res, path);
  },
};

/* Named exports for the local node harness (unit-test the paywall without
   deploying). The live bundle already carries an `export {}` block from
   payment-routes.js plus the `export default` above; an extra named list
   is legal in the concatenated scope. */
export {
  isCrawlerUa,
  isCrawler,
  isFreeSlug,
  isGatedSlug,
  slugFromCourseJsonPath,
  verifyEntitlementToken,
  hasCourseEntitlement,
  courseGate,
  paywallPageHtml,
  paywallResponse,
  json402Response,
};
// config-update 20261008-2155
