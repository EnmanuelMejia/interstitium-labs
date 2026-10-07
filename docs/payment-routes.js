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
 */

"use strict";

/* ---------------- catalog: server-side price authority ---------------- */
/* Client-submitted amounts are NEVER trusted; the item id maps to a price
   here. Tiers mirror docs/enroll/config.js publishable prices. */

var ITEMS = {
  "prep-sprint": { name: "Prep Sprint", amount_cents: 14900 },
  "devsecops-mastery": { name: "DevSecOps Mastery", amount_cents: 49900 },
  "full-academy": { name: "Full Academy", amount_cents: 79900 },
};

var CURRENCY = "usd";
var UD_DOMAIN = "enmanuelmejia.crypto";
var UD_RESOLVE_URL = "https://resolve.unstoppabledomains.com/domains/";
var UD_CACHE_TTL = 24 * 60 * 60; // 24h, seconds

/* 11-coin rail. pay_currency = NOWPayments code (lowercase),
   ud_key = Unstoppable Domains record key, env_key = WALLET_* fallback,
   extra  = which env holds the destination tag / memo for this coin. */
var COINS = [
  { code: "XRP",  name: "XRP (Ripple)",       pay_currency: "xrp",  ud_key: "crypto.XRP.address",  env_key: "WALLET_XRP",  extra: "XRP_DESTINATION_TAG", extra_label: "Destination tag" },
  { code: "XLM",  name: "Stellar Lumens",     pay_currency: "xlm",  ud_key: "crypto.XLM.address",  env_key: "WALLET_XLM",  extra: "XLM_MEMO",            extra_label: "Memo" },
  { code: "ADA",  name: "Cardano",            pay_currency: "ada",  ud_key: "crypto.ADA.address",  env_key: "WALLET_ADA" },
  { code: "ALGO", name: "Algorand",           pay_currency: "algo", ud_key: "crypto.ALGO.address", env_key: "WALLET_ALGO" },
  { code: "QNT",  name: "Quant",              pay_currency: "qnt",  ud_key: "crypto.QNT.address",  env_key: "WALLET_QNT" },
  { code: "HBAR", name: "Hedera",             pay_currency: "hbar", ud_key: "crypto.HBAR.address", env_key: "WALLET_HBAR" },
  { code: "IOTA", name: "IOTA",               pay_currency: "iota", ud_key: "crypto.IOTA.address", env_key: "WALLET_IOTA" },
  { code: "XDC",  name: "XDC Network",        pay_currency: "xdc",  ud_key: "crypto.XDC.address",  env_key: "WALLET_XDC" },
  { code: "XMR",  name: "Monero",             pay_currency: "xmr",  ud_key: "crypto.XMR.address",  env_key: "WALLET_XMR" },
  { code: "BTC",  name: "Bitcoin",            pay_currency: "btc",  ud_key: "crypto.BTC.address",  env_key: "WALLET_BTC" },
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
    var addr = (records && records[c.ud_key]) || (env && env[c.env_key]) || "";
    addr = String(addr || "").trim();
    var entry = {
      code: c.code,
      name: c.name,
      address: addr,
      source: addr ? ((records && records[c.ud_key]) ? "ud" : "env") : "missing",
      ud_domain: UD_DOMAIN,
    };
    if (c.extra && env && env[c.extra]) {
      entry[c.extra === "XRP_DESTINATION_TAG" ? "destination_tag" : "memo"] = String(env[c.extra]).trim();
      entry.extra_label = c.extra_label;
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
  UD_DOMAIN,
  sortKeysDeep,
  nowpaymentsSignature,
  verifyNowpaymentsIpn,
  parseStripeSigHeader,
  verifyStripeSignature,
  directQrPayload,
  centsToDecimal,
  safeEqual,
};
