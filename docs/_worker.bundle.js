// docs/payment-routes.js
var ITEMS = {
  "prep-sprint": { name: "Prep Sprint", amount_cents: 14900 },
  "devsecops-mastery": { name: "DevSecOps Mastery", amount_cents: 49900 },
  "full-academy": { name: "Full Academy", amount_cents: 79900 }
};
var CURRENCY = "usd";
var UD_DOMAIN = "enmanuelmejia.crypto";
var UD_RESOLVE_URL = "https://resolve.unstoppabledomains.com/domains/";
var UD_CACHE_TTL = 24 * 60 * 60;
var COINS = [
  { code: "XRP", name: "XRP (Ripple)", pay_currency: "xrp", ud_key: "crypto.XRP.address", env_key: "WALLET_XRP", extra: "XRP_DESTINATION_TAG", extra_label: "Destination tag" },
  { code: "XLM", name: "Stellar Lumens", pay_currency: "xlm", ud_key: "crypto.XLM.address", env_key: "WALLET_XLM", extra: "XLM_MEMO", extra_label: "Memo" },
  { code: "ADA", name: "Cardano", pay_currency: "ada", ud_key: "crypto.ADA.address", env_key: "WALLET_ADA" },
  { code: "ALGO", name: "Algorand", pay_currency: "algo", ud_key: "crypto.ALGO.address", env_key: "WALLET_ALGO" },
  { code: "QNT", name: "Quant", pay_currency: "qnt", ud_key: "crypto.QNT.address", env_key: "WALLET_QNT" },
  { code: "HBAR", name: "Hedera", pay_currency: "hbar", ud_key: "crypto.HBAR.address", env_key: "WALLET_HBAR" },
  { code: "IOTA", name: "IOTA", pay_currency: "iota", ud_key: "crypto.IOTA.address", env_key: "WALLET_IOTA" },
  { code: "XDC", name: "XDC Network", pay_currency: "xdc", ud_key: "crypto.XDC.address", env_key: "WALLET_XDC" },
  { code: "XMR", name: "Monero", pay_currency: "xmr", ud_key: "crypto.XMR.address", env_key: "WALLET_XMR" },
  { code: "BTC", name: "Bitcoin", pay_currency: "btc", ud_key: "crypto.BTC.address", env_key: "WALLET_BTC" }
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
function payJson(data, status) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store"
    }
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
  return (/* @__PURE__ */ new Date()).toISOString();
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
function safeEqual(a, b) {
  a = String(a || "");
  b = String(b || "");
  if (a.length !== b.length) return false;
  var diff = 0;
  for (var i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}
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
async function nowpaymentsSignature(payload, ipnSecret) {
  var canonical = JSON.stringify(sortKeysDeep(payload));
  return hmacHex("SHA-512", ipnSecret, canonical);
}
async function verifyNowpaymentsIpn(payload, signature, ipnSecret) {
  if (!signature || !ipnSecret) return false;
  var expected = await nowpaymentsSignature(payload, ipnSecret);
  return safeEqual(expected, String(signature).toLowerCase());
}
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
  if (Math.abs(Date.now() / 1e3 - t) > 300) return false;
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
function directQrPayload(coinCode, address) {
  address = String(address || "").trim();
  if (coinCode === "BTC") return "bitcoin:" + address;
  return address;
}
function centsToDecimal(cents) {
  return (cents / 100).toFixed(2);
}
var memStore = /* @__PURE__ */ new Map();
function makeStore(env) {
  if (env && env.IL_ACCOUNTS && typeof env.IL_ACCOUNTS.get === "function") {
    return {
      backend: "kv",
      get: function(k) {
        return env.IL_ACCOUNTS.get(k);
      },
      put: function(k, v) {
        return env.IL_ACCOUNTS.put(k, v);
      }
    };
  }
  return {
    backend: "memory",
    get: async function(k) {
      return memStore.has(k) ? memStore.get(k) : null;
    },
    put: async function(k, v) {
      memStore.set(k, v);
    }
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
  if (order.status === "paid" && order.email && order.item) {
    await store.put(
      "pay:entitle:" + order.email.toLowerCase() + ":" + order.item,
      JSON.stringify({
        order_id: order.id,
        item: order.item,
        provider: order.provider,
        paid_at: order.paid_at
      })
    );
  }
}
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
async function fetchUdRecords() {
  var res = await fetch(UD_RESOLVE_URL + encodeURIComponent(UD_DOMAIN), {
    headers: { accept: "application/json" }
  });
  if (!res.ok) throw new Error("ud_http_" + res.status);
  var data = await res.json();
  return data && data.records || {};
}
async function resolveCoinAddresses(env, store) {
  var cacheKey = "pay:ud:" + UD_DOMAIN;
  var cached = null;
  try {
    var raw = await store.get(cacheKey);
    if (raw) cached = JSON.parse(raw);
  } catch (e) {
    cached = null;
  }
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
          JSON.stringify({ records, source: "ud", expires_at: Date.now() + UD_CACHE_TTL * 1e3, fetched_at: nowIso() })
        );
      } catch (e) {
      }
    } catch (e) {
      records = {};
      source = "env";
    }
  }
  var out = [];
  for (var i = 0; i < COINS.length; i++) {
    var c = COINS[i];
    var addr = records && records[c.ud_key] || env && env[c.env_key] || "";
    addr = String(addr || "").trim();
    var entry = {
      code: c.code,
      name: c.name,
      address: addr,
      source: addr ? records && records[c.ud_key] ? "ud" : "env" : "missing",
      ud_domain: UD_DOMAIN
    };
    if (c.extra && env && env[c.extra]) {
      entry[c.extra === "XRP_DESTINATION_TAG" ? "destination_tag" : "memo"] = String(env[c.extra]).trim();
      entry.extra_label = c.extra_label;
    }
    out.push(entry);
  }
  return { domain: UD_DOMAIN, coins: out, resolved_via: source, fetched_at: nowIso() };
}
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
    if (!coin) return { ok: false, error: "coin_invalid", valid: COINS.map(function(c) {
      return c.code;
    }) };
  }
  return { ok: true, provider, item, email, coin };
}
function providerConfigured(env, provider) {
  if (provider === "stripe") return !!env.STRIPE_SECRET_KEY;
  if (provider === "paypal") return !!(env.PAYPAL_CLIENT_ID && env.PAYPAL_CLIENT_SECRET);
  if (provider === "nowpayments") return !!env.NOWPAYMENTS_API_KEY;
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
    provider,
    item,
    item_name: spec.name,
    amount_cents: spec.amount_cents,
    currency: "USD",
    email: email || "",
    coin: coin ? coin.code : "",
    status: "created",
    provider_ref: "",
    created_at: nowIso(),
    updated_at: nowIso(),
    paid_at: ""
  };
}
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
    "payment_method_types[]": "card",
    // Checkout adds Apple Pay / Google Pay automatically where eligible
    "line_items[0][price_data][currency]": CURRENCY,
    "line_items[0][price_data][product_data][name]": "Interstitium Labs \u2014 " + order.item_name,
    "line_items[0][price_data][unit_amount]": String(order.amount_cents),
    "line_items[0][quantity]": "1",
    "mode": "payment",
    "customer_email": order.email || void 0,
    "success_url": origin + "/api/pay/stripe/return?session_id={CHECKOUT_SESSION_ID}",
    "cancel_url": origin + "/enroll/cancel.html",
    "metadata[order_id]": order.id,
    "metadata[item]": order.item
  };
  var clean = {};
  for (var k of Object.keys(p)) if (p[k] !== void 0) clean[k] = p[k];
  var res = await fetch(stripeApiBase() + "/checkout/sessions", {
    method: "POST",
    headers: {
      "authorization": "Bearer " + env.STRIPE_SECRET_KEY,
      "content-type": "application/x-www-form-urlencoded"
    },
    body: stripeForm(clean)
  });
  var data = await res.json().catch(function() {
    return null;
  });
  if (!res.ok || !data || !data.url) {
    throw new Error("stripe_session_failed:" + (data && data.error && data.error.message ? data.error.message : res.status));
  }
  return { session_id: data.id, url: data.url };
}
async function stripeRetrieveSession(env, sessionId) {
  var res = await fetch(stripeApiBase() + "/checkout/sessions/" + encodeURIComponent(sessionId), {
    headers: { "authorization": "Bearer " + env.STRIPE_SECRET_KEY }
  });
  if (!res.ok) throw new Error("stripe_retrieve_failed:" + res.status);
  return res.json();
}
function paypalApiBase(env) {
  return env.PAYPAL_SANDBOX === "1" ? "https://api-m.sandbox.paypal.com" : "https://api-m.paypal.com";
}
async function paypalAccessToken(env) {
  var res = await fetch(paypalApiBase(env) + "/v1/oauth2/token", {
    method: "POST",
    headers: {
      "authorization": "Basic " + base64Encode(env.PAYPAL_CLIENT_ID + ":" + env.PAYPAL_CLIENT_SECRET),
      "content-type": "application/x-www-form-urlencoded"
    },
    body: "grant_type=client_credentials"
  });
  var data = await res.json().catch(function() {
    return null;
  });
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
        description: "Interstitium Labs \u2014 " + order.item_name,
        custom_id: order.id,
        amount: { currency_code: "USD", value: centsToDecimal(order.amount_cents) }
      }
    ],
    application_context: {
      brand_name: "Interstitium Labs",
      return_url: origin + "/api/pay/paypal/return",
      cancel_url: origin + "/api/pay/paypal/cancel",
      user_action: "PAY_NOW"
    }
  };
  var res = await fetch(paypalApiBase(env) + "/v2/checkout/orders", {
    method: "POST",
    headers: {
      "authorization": "Bearer " + token,
      "content-type": "application/json"
    },
    body: JSON.stringify(body)
  });
  var data = await res.json().catch(function() {
    return null;
  });
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
      body: "{}"
    }
  );
  var data = await res.json().catch(function() {
    return null;
  });
  if (!res.ok || !data) throw new Error("paypal_capture_failed:" + res.status);
  return data;
}
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
    webhook_event: eventBody
  };
  var res = await fetch(paypalApiBase(env) + "/v1/notifications/verify-webhook-signature", {
    method: "POST",
    headers: {
      "authorization": "Bearer " + token,
      "content-type": "application/json"
    },
    body: JSON.stringify(payload)
  });
  var data = await res.json().catch(function() {
    return null;
  });
  return !!(data && data.verification_status === "SUCCESS");
}
function nowpaymentsApiBase(env) {
  return env.NOWPAYMENTS_SANDBOX === "1" ? "https://api-sandbox.nowpayments.io/v1" : "https://api.nowpayments.io/v1";
}
async function nowpaymentsCreateInvoice(env, order, coin, origin) {
  var body = {
    price_amount: Number(centsToDecimal(order.amount_cents)),
    price_currency: "usd",
    pay_currency: coin.pay_currency,
    order_id: order.id,
    order_description: "Interstitium Labs \u2014 " + order.item_name,
    ipn_callback_url: origin + "/api/pay/ipn/nowpayments",
    success_url: origin + "/enroll/success.html?order=" + order.id,
    cancel_url: origin + "/enroll/cancel.html"
  };
  var res = await fetch(nowpaymentsApiBase(env) + "/invoice", {
    method: "POST",
    headers: {
      "x-api-key": env.NOWPAYMENTS_API_KEY,
      "content-type": "application/json"
    },
    body: JSON.stringify(body)
  });
  var data = await res.json().catch(function() {
    return null;
  });
  if (!res.ok || !data || !data.invoice_url) {
    throw new Error("nowpayments_invoice_failed:" + (data && data.message ? data.message : res.status));
  }
  return { invoice_id: String(data.id || ""), url: data.invoice_url };
}
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
        qr_payload: directQrPayload(v.coin.code, entry.address)
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
        confirmation: "manual_review"
      });
    }
  } catch (e) {
    order.status = "failed";
    try {
      await saveOrder(store, order);
    } catch (e2) {
    }
    var msg = e && e.message || "provider_error";
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
    created_at: order.created_at
  });
}
async function handleUd(request, env, store) {
  if (request.method !== "GET") return payJson({ ok: false, error: "method_not_allowed" }, 405);
  try {
    var resolved = await resolveCoinAddresses(env, store);
  } catch (e) {
    return payJson({ ok: false, error: "resolution_failed" }, 502);
  }
  var coins = resolved.coins.map(function(c) {
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
    coins
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
  var orderId = obj.metadata && obj.metadata.order_id || "";
  if (type === "checkout.session.completed") {
    var order = await getOrder(store, orderId);
    if (order) {
      if (obj.amount_total !== void 0 && Number(obj.amount_total) !== order.amount_cents) {
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
      if (capAmount !== void 0 && capAmount !== centsToDecimal(order.amount_cents)) {
        order.status = "failed";
        order.note = "amount_mismatch";
        await saveOrder(store, order);
      } else {
        await markPaid(store, order, resource.id || "", { paypal_capture: true });
      }
    }
  } else if (type === "CHECKOUT.ORDER.APPROVED") {
    var ro = event.resource || {};
    var oid = ro.custom_id || "";
    var o = await getOrder(store, oid);
    if (o && o.status !== "paid" && o.provider_ref) {
      try {
        var cap = await paypalCaptureOrder(env, o.provider_ref);
        var pu = cap.purchase_units && cap.purchase_units[0] || {};
        var captures = pu.payments && pu.payments.captures || [];
        var capId = captures.length ? captures[0].id : "";
        await markPaid(store, o, o.provider_ref, { paypal_capture_id: capId });
      } catch (e) {
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
        nowpayments_pay_amount: payload.pay_amount || ""
      });
    } else if (status === "failed" || status === "refunded" || status === "expired") {
      if (order.status !== "paid") {
        order.status = status === "refunded" ? "refunded" : "failed";
        await saveOrder(store, order);
      }
    }
  }
  return payJson({ ok: true, received: status });
}
function redirectTo(url, request) {
  return Response.redirect(new URL(url, new URL(request.url).origin).toString(), 303);
}
async function handlePaypalReturn(request, env, store) {
  var url = new URL(request.url);
  var token = url.searchParams.get("token") || "";
  if (!token) return redirectTo("/enroll/cancel.html", request);
  var order = null;
  try {
    var cap = await paypalCaptureOrder(env, token);
    var pu = cap.purchase_units && cap.purchase_units[0] || {};
    var ref = pu.reference_id || "";
    order = await getOrder(store, ref);
    if (order && order.status !== "paid") {
      var captures = pu.payments && pu.payments.captures || [];
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
    var orderId = s.metadata && s.metadata.order_id || "";
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

// docs/_worker.js
var NOINDEX_PREFIXES = ["/admin/", "/ops/", "/analytics/", "/measure/", "/brand/"];
function needsNoindex(path) {
  for (var i = 0; i < NOINDEX_PREFIXES.length; i++) {
    var pre = NOINDEX_PREFIXES[i];
    if (path === pre.slice(0, -1) || path.indexOf(pre) === 0) return true;
  }
  return false;
}
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
  return path === "/coach" || path === "/cinema" || path.indexOf("/coach/") === 0 || path.indexOf("/cinema/") === 0;
}
function applyAssetHeaders(res, path) {
  var h = new Headers(res.headers);
  for (var k in SECURITY_HEADERS) {
    if (!h.has(k)) h.set(k, SECURITY_HEADERS[k]);
  }
  h.set("Permissions-Policy", micAllowed(path) ? "camera=(), microphone=(self), geolocation=(), payment=(), usb=(), interest-cohort=()" : "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()");
  if (needsNoindex(path)) h.set("X-Robots-Tag", "noindex, nofollow");
  return new Response(res.body, {
    status: res.status,
    statusText: res.statusText,
    headers: h
  });
}
var EMAIL_RE2 = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
var MAX_BODY = 8192;
var WAITLIST_SUCCESS_PATH = "/enroll/success.html";
function json(data, status) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store"
    }
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
    form.forEach(function(v, k) {
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
  if (!email || email.length > 254 || !EMAIL_RE2.test(email)) {
    return json({ ok: false, error: "email_invalid" }, 422);
  }
  var record = {
    name,
    email,
    created_at: (/* @__PURE__ */ new Date()).toISOString(),
    source: "enroll"
  };
  if (data && data.tier != null) {
    var tier = String(data.tier).trim();
    if (tier && tier.length <= 40 && /^[A-Za-z0-9 _-]+$/.test(tier)) {
      record.tier = tier;
    }
  }
  var key = "wl:" + Date.now() + ":" + Math.random().toString(36).slice(2, 10);
  try {
    await env.WAITLIST.put(key, JSON.stringify(record));
  } catch (e) {
    return json({ ok: false, error: "store_unavailable" }, 503);
  }
  if (!wantsJson(request)) {
    return Response.redirect(
      new URL(WAITLIST_SUCCESS_PATH, request.url).toString(),
      303
    );
  }
  return json({ ok: true });
}
var SESSION_COOKIE = "il_session";
var SESSION_TTL = 30 * 24 * 60 * 60;
var MAGIC_TOKEN_TTL = 15 * 60;
var MAGIC_THROTTLE_TTL = 60;
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
  return SESSION_COOKIE + "=" + encodeURIComponent(id) + "; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=" + SESSION_TTL;
}
function clearSessionCookie() {
  return SESSION_COOKIE + "=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0; Expires=Thu, 01 Jan 1970 00:00:00 GMT";
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
    if (!sess || !sess.email || !EMAIL_RE2.test(sess.email)) return null;
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
async function sendMagicLink(email, link) {
  var text = "Sign in to Interstitium Labs\n\nClick this link to sign in (it expires in 15 minutes):\n\n" + link + "\n\nIf you didn't request this, you can safely ignore this email.\n\n\u2014 Interstitium Labs \xB7 interstitiumlabs.dev";
  var payload = {
    personalizations: [{ to: [{ email }] }],
    from: { email: MAIL_FROM, name: MAIL_FROM_NAME },
    subject: "Your Interstitium Labs sign-in link",
    content: [{ type: "text/plain", value: text }]
  };
  var res;
  try {
    res = await fetch("https://api.mailchannels.net/tx/v1/send", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "X-MailChannels-Sender-Id": MAIL_SENDER_ID
      },
      body: JSON.stringify(payload)
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
  } catch (e) {
  }
  return { ok: false, error: "mail_rejected", status: res.status, detail };
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
  var email = body && body.email != null ? String(body.email).trim().toLowerCase() : "";
  if (!email || email.length > 254 || !EMAIL_RE2.test(email)) {
    return json({ ok: false, error: "email_invalid" }, 422);
  }
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
      JSON.stringify({ email, created_at: (/* @__PURE__ */ new Date()).toISOString() }),
      { expirationTtl: MAGIC_TOKEN_TTL }
    );
  } catch (e) {
    return json({ ok: false, error: "store_unavailable" }, 503);
  }
  var url = new URL(request.url);
  var link = url.origin + "/api/auth/verify?token=" + token;
  var sent = await sendMagicLink(email, link);
  if (!sent.ok) {
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
  if (!parsed || !parsed.email || !EMAIL_RE2.test(parsed.email)) {
    return json({ ok: false, error: "token_invalid" }, 400);
  }
  var email = parsed.email;
  try {
    await env.IL_AUTH.delete("magic:" + token);
  } catch (e) {
  }
  var sid = randomHex(32);
  var sess = {
    email,
    created_at: (/* @__PURE__ */ new Date()).toISOString(),
    expires_at: new Date(Date.now() + SESSION_TTL * 1e3).toISOString()
  };
  try {
    await env.IL_ACCOUNTS.put("sess:" + sid, JSON.stringify(sess), {
      expirationTtl: SESSION_TTL
    });
    var acctKey = "acct:" + email;
    var existing = await env.IL_ACCOUNTS.get(acctKey);
    if (!existing) {
      await env.IL_ACCOUNTS.put(
        acctKey,
        JSON.stringify({ email, created_at: sess.created_at })
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
      "cache-control": "no-store"
    }
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
    } catch (e) {
    }
  }
  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "set-cookie": clearSessionCookie(),
      "cache-control": "no-store"
    }
  });
}
function mergeProgress(base, incoming) {
  var out = {};
  var k;
  for (k in base) {
    if (Object.prototype.hasOwnProperty.call(base, k)) out[k] = base[k];
  }
  for (k in incoming) {
    if (!Object.prototype.hasOwnProperty.call(incoming, k)) continue;
    var bv = out[k];
    var iv = incoming[k];
    if (bv && iv && typeof bv === "object" && typeof iv === "object" && !Array.isArray(bv) && !Array.isArray(iv)) {
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
    var incoming = body && body.progress && typeof body.progress === "object" && !Array.isArray(body.progress) ? body.progress : null;
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
    merged.__updated_at = (/* @__PURE__ */ new Date()).toISOString();
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
    id,
    path: pathId,
    email: sess.email,
    issued_at: (/* @__PURE__ */ new Date()).toISOString()
  };
  try {
    await env.IL_ACCOUNTS.put("cert:" + id, JSON.stringify(cert));
    var listKey = "certs:" + sess.email;
    var list = [];
    try {
      var lraw = await env.IL_ACCOUNTS.get(listKey);
      if (lraw) list = JSON.parse(lraw) || [];
    } catch (e) {
    }
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
var NOAH_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast";
var KNOWLEDGE_PATH = "/university/data/noah-knowledge.md";
var MAX_MSGS = 20;
var MAX_CHARS_PER_MSG = 4e3;
var MAX_TOKENS = 900;
var RATE_WINDOW_MS = 6e4;
var RATE_MAX = 15;
var knowledgeCache = null;
var rateMap = /* @__PURE__ */ new Map();
function noahCors(resp, origin) {
  const h = new Headers(resp.headers);
  h.set("Access-Control-Allow-Origin", origin);
  h.set("Access-Control-Allow-Methods", "POST, OPTIONS");
  h.set("Access-Control-Allow-Headers", "Content-Type");
  h.set("Vary", "Origin");
  return new Response(resp.body, { status: resp.status, headers: h });
}
function noahJson(obj, status, origin) {
  return noahCors(
    new Response(JSON.stringify(obj), {
      status,
      headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" }
    }),
    origin
  );
}
function noahAllowedOrigin(request) {
  const o = request.headers.get("Origin") || "";
  const self = new URL(request.url).origin;
  if (o === self) return o;
  if (o === "https://interstitiumlabs.dev" || o === "https://www.interstitiumlabs.dev") return o;
  return self;
}
function rateLimited(ip) {
  const now = Date.now();
  let rec = rateMap.get(ip);
  if (!rec || now - rec.start > RATE_WINDOW_MS) {
    rec = { start: now, count: 0 };
    rateMap.set(ip, rec);
  }
  rec.count += 1;
  if (rateMap.size > 5e3) rateMap.clear();
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
  } catch (e) {
  }
  knowledgeCache = "";
  return "";
}
function sanitizeMessages(raw) {
  if (!Array.isArray(raw)) return null;
  const out = [];
  for (const m of raw.slice(-MAX_MSGS)) {
    if (!m || m.role !== "user" && m.role !== "assistant") return null;
    const content = String(m.content == null ? "" : m.content).slice(0, MAX_CHARS_PER_MSG);
    if (!content.trim()) continue;
    out.push({ role: m.role, content });
  }
  return out.length ? out : null;
}
async function handleNoah(request, env) {
  const origin = noahAllowedOrigin(request);
  if (!env.AI) {
    return noahJson({ error: "AI unavailable", fallback: true }, 503, origin);
  }
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  if (rateLimited(ip)) {
    return noahJson({ error: "Rate limited. Try again shortly.", fallback: true }, 429, origin);
  }
  let body;
  try {
    body = await request.json();
  } catch (e) {
    return noahJson({ error: "Invalid JSON body." }, 400, origin);
  }
  const messages = sanitizeMessages(body.messages);
  if (!messages) {
    return noahJson({ error: "Provide messages: [{role, content}]." }, 400, origin);
  }
  const knowledge = await loadKnowledge(env, request);
  const system = `You are Noah AI, the resident intelligence of Interstitium Labs \u2014 the personal AI of founder Enmanuel D. Mejia, living on interstitiumlabs.dev, learn.interstitiumlabs.dev, and the Interstitium Labs mobile apps. Your name is Noah AI. Never claim to be Muse, Meta AI, or any other assistant.

PRIMARY MISSION \u2014 personalized adaptive tutor. You adapt to each learner: infer their level (novice / intermediate / advanced) from their vocabulary, questions, and attempts, then calibrate depth, jargon, and pacing to match. Notice what they already grasp and skip it; dwell where they stumble. Remember what they tell you within the conversation \u2014 their goal (a cert, an interview, a course, a project), their background, what they have tried \u2014 and refer back to it explicitly: "last time you got stuck on X, let's build on that." Keep a running mental model of the session: goal, background, attempts, what worked. Restate it when relevant ("on your second attempt at the subnetting drill you nailed the mask but slipped on the broadcast \u2014 here is why"). This memory is conversation-scoped: it ends when the session ends.

LEARNING STYLE \u2014 detect how they learn from interaction signals: terse vs verbose replies; code-first vs concept-first vs example-first questions; requests for diagrams or analogies; trial-and-error attempts vs read-first behavior. Match their style: concise answers for the terse, worked examples for the example-first, code before prose for the code-first, an ASCII sketch when they ask to see it. Keep re-detecting as signals accumulate \u2014 styles drift, and so should your strategy.

DOCTRINE (Socratic): when the visitor is learning, guide before telling. Acknowledge their hypothesis, ask ONE sharp guiding question, offer the next smallest step. Never dump a full worked answer first when they are studying. Diagnose the misconception behind a wrong answer and repair the mental model, not just the answer. Give graduated hints on request; check understanding with one quick practice question before moving on. Celebrate real progress specifically ("your subnetting is clean now \u2014 that was the hard part"); normalize struggle, never shame it. If they plainly ask for a direct answer outside a study context, answer directly and well.

PACING \u2014 set one explicit micro-goal at the start of each study session ("by the end of this you will ..."). Check mastery with ONE question before advancing; move on only when they show understanding. At every checkpoint offer three branches: go deeper, move on, or review. Never race ahead of them.

LAB COACHING \u2014 for hands-on work, never paste a full solution first. Diagnose: ask what they tried, what they expected, what actually happened. Hint in graduated steps: a nudge, then a stronger nudge, then a worked sketch of the missing piece; the full solution only when they are still stuck. When they show you an attempt, review it: name what is right before what is wrong, and repair the reasoning, not just the code.

BEYOND TUTORING you are a complete assistant. Answer questions about the full course catalog \u2014 recommend academies and paths BY CODE (e.g. IL-11) and cite the catalog code when you do. Navigate visitors to the right page; help with writing, planning, and technical problems. For code: explain and debug by careful reasoning, but be honest that you cannot execute code \u2014 say so before reasoning about what it will do, and verify claims by tracing, not asserting. For career questions about Enmanuel: ground every claim ONLY in his real materials \u2014 his resume, his projects, this knowledge base. Never invent credentials, employers, salaries, offers, or outcomes for him or the visitor. Anything a capable personal AI would do, within the honesty rules below.

ITERATION \u2014 a privacy-respecting pipeline records only counters of how this chat is used (opens, asks, fallbacks; never message text). When the conversation itself shows stuck signals \u2014 the same topic asked repeatedly, escalating hint requests, circling one concept \u2014 name it briefly and invite a check question or a different angle. Sparingly: at most one such nudge per session. These moments feed the weekly human review that improves you.

VOICE: measured, precise, warm but never gushing. Latin sparingly. No hype, no emojis. Short paragraphs. Use simple markdown (bold, lists, code spans) where it aids clarity.

SCOPE: you speak from the knowledge base below \u2014 Enmanuel's projects, code, the Learning University curriculum, the mobile apps, and the Interstitium Labs sites. Recommend specific academies/paths by code (e.g. IL-11) when relevant. If asked about something outside the knowledge base, say so plainly and help from general knowledge, marked as general. Never invent credentials, experience, certifications, or project details \u2014 for Enmanuel or the visitor.

KNOWLEDGE BASE:
` + (knowledge || "(knowledge base unavailable \u2014 answer from general knowledge and say so.)");
  try {
    const aiMessages = [{ role: "system", content: system }, ...messages];
    const result = await env.AI.run(NOAH_MODEL, {
      messages: aiMessages,
      max_tokens: MAX_TOKENS,
      temperature: 0.6
    });
    const reply = (result && result.response ? String(result.response) : "").trim() || "I could not compose a reply just now. Try again, or ask the local Socratic engine below.";
    return noahJson({ reply }, 200, origin);
  } catch (e) {
    return noahJson({ error: "AI request failed.", fallback: true }, 502, origin);
  }
}
var STAT_KEYS = ["opens", "asks", "remotes", "fallbacks", "nudges", "chips", "errors"];
function freshAgg() {
  return { opens: 0, asks: 0, remotes: 0, fallbacks: 0, nudges: 0, chips: 0, errors: 0, byTopic: {} };
}
function dayKey(d) {
  return "stats:day:" + d.toISOString().slice(0, 10);
}
function sanitizeAgg(a) {
  if (!a || typeof a !== "object") return null;
  const out = {};
  for (const k of STAT_KEYS) {
    const n = Number(a[k]);
    out[k] = Number.isFinite(n) && n >= 0 ? Math.min(Math.floor(n), 1e4) : 0;
  }
  out.byTopic = {};
  if (a.byTopic && typeof a.byTopic === "object") {
    for (const t of Object.keys(a.byTopic).slice(0, 40)) {
      if (/^[a-z-]{1,24}$/.test(t)) {
        const n = Number(a.byTopic[t]);
        if (Number.isFinite(n) && n > 0) out.byTopic[t] = Math.min(Math.floor(n), 1e4);
      }
    }
  }
  return out;
}
function mergeAgg(base, d) {
  const out = Object.assign(freshAgg(), base, { byTopic: {} });
  for (const k of STAT_KEYS) out[k] = (Number(base[k]) || 0) + (d[k] || 0);
  const bt = base.byTopic && typeof base.byTopic === "object" ? base.byTopic : {};
  for (const t of Object.keys(bt)) out.byTopic[t] = bt[t];
  for (const t of Object.keys(d.byTopic)) out.byTopic[t] = (out.byTopic[t] || 0) + d.byTopic[t];
  return out;
}
async function handleNoahStats(request, env) {
  const origin = noahAllowedOrigin(request);
  if (request.method === "OPTIONS") {
    return noahCors(new Response(null, { status: 204 }), origin);
  }
  if (request.method === "POST") {
    let body = null;
    try {
      body = await request.json();
    } catch (e) {
      return noahJson({ error: "Bad JSON." }, 400, origin);
    }
    if (!body || body.v !== 1) return noahJson({ error: "Bad version." }, 400, origin);
    const d = sanitizeAgg(body.agg);
    if (!d) return noahJson({ error: "Bad aggregate." }, 400, origin);
    const ip = request.headers.get("CF-Connecting-IP") || "x";
    if (rateLimited("stats:" + ip)) return noahCors(new Response(null, { status: 429 }), origin);
    if (env.NOAH_STATS) {
      try {
        const day = dayKey(/* @__PURE__ */ new Date());
        const cur = await env.NOAH_STATS.get(day, "json") || freshAgg();
        await env.NOAH_STATS.put(day, JSON.stringify(mergeAgg(cur, d)));
        const g = await env.NOAH_STATS.get("stats:global", "json") || freshAgg();
        await env.NOAH_STATS.put("stats:global", JSON.stringify(mergeAgg(g, d)));
      } catch (e) {
        console.log("noah-stats kv error: " + (e && e.message));
      }
    } else {
      console.log("noah-stats (no KV): " + JSON.stringify(d));
    }
    return noahCors(new Response(null, { status: 204 }), origin);
  }
  if (request.method === "GET") {
    const out = { global: freshAgg(), days: [] };
    if (env.NOAH_STATS) {
      try {
        out.global = await env.NOAH_STATS.get("stats:global", "json") || freshAgg();
        for (let i = 0; i < 7; i++) {
          const k = dayKey(new Date(Date.now() - i * 864e5));
          const v = await env.NOAH_STATS.get(k, "json");
          if (v) out.days.push(Object.assign({ day: k.slice(10) }, v));
        }
      } catch (e) {
      }
    }
    return noahJson(out, 200, origin);
  }
  return noahJson({ error: "Use GET or POST." }, 405, origin);
}
var worker_default = {
  async fetch(request, env) {
    var url = new URL(request.url);
    var path = url.pathname;
    if (path === "/os" || path === "/os/") {
      return movedPermanently(request, "/learn/");
    }
    if (path === "/proof" || path === "/proof/") {
      return movedPermanently(request, "/evidence/");
    }
    var STUB_REDIRECTS = {
      "/code": "/prep/programming/",
      "/command": "/paths/",
      "/desk": "/learn/",
      "/doctrine": "/about/",
      "/drill": "/prep/drills/",
      "/factory": "/labs/",
      "/field": "/learn/",
      "/graph": "/learn/skills/",
      "/interview": "/prep/drills/",
      "/library": "/learn/",
      "/measure": "/learn/",
      "/plant": "/paths/",
      "/platform": "/about/",
      "/portfolio": "/labs/superlab/",
      "/pricing": "/enroll/",
      "/radar": "/trending/",
      "/sheets": "/prep/",
      "/si": "/learn/",
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
    if (path === "/api/pay/create" || path === "/api/pay/status" || path === "/api/pay/ud" || path === "/api/pay/webhook/stripe" || path === "/api/pay/webhook/paypal" || path === "/api/pay/ipn/nowpayments" || path === "/api/pay/paypal/return" || path === "/api/pay/paypal/cancel" || path === "/api/pay/stripe/return") {
      return handlePay(request, env);
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
    return applyAssetHeaders(res, path);
  }
};
export {
  worker_default as default
};
