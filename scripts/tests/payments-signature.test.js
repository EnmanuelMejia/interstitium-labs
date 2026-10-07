/**
 * Payment layer unit tests — signature verification + pure helpers.
 *
 * Run: node --test scripts/tests/payments-signature.test.js
 * No secrets, no network, no Worker runtime required: WebCrypto is used
 * directly, exactly as the Worker module uses it.
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import { webcrypto } from "node:crypto";

import {
  sortKeysDeep,
  nowpaymentsSignature,
  verifyNowpaymentsIpn,
  parseStripeSigHeader,
  verifyStripeSignature,
  directQrPayload,
  centsToDecimal,
  validateCreate,
  providerConfigured,
  coinByCode,
  COINS,
  ITEMS,
  safeEqual,
} from "../../docs/payment-routes.js";

if (!globalThis.crypto) globalThis.crypto = webcrypto;
if (!globalThis.crypto.subtle && webcrypto.subtle) {
  globalThis.crypto = webcrypto;
}

/* ---------- Stripe ---------- */

test("stripe: valid signature verifies", async () => {
  const secret = "whsec_test_123";
  const ts = String(Math.floor(Date.now() / 1000));
  const body = '{"id":"evt_1","type":"checkout.session.completed"}';
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(ts + "." + body));
  const hex = [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
  const ok = await verifyStripeSignature(body, `t=${ts},v1=${hex}`, secret);
  assert.equal(ok, true);
});

test("stripe: tampered body fails", async () => {
  const secret = "whsec_test_123";
  const ts = String(Math.floor(Date.now() / 1000));
  const ok = await verifyStripeSignature(
    '{"id":"evt_2","tampered":true}',
    `t=${ts},v1=${"0".repeat(64)}`,
    secret
  );
  assert.equal(ok, false);
});

test("stripe: wrong secret fails", async () => {
  const ts = String(Math.floor(Date.now() / 1000));
  const body = '{"id":"evt_3"}';
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode("whsec_right"),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(ts + "." + body));
  const hex = [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
  const ok = await verifyStripeSignature(body, `t=${ts},v1=${hex}`, "whsec_wrong");
  assert.equal(ok, false);
});

test("stripe: stale timestamp (>5min) rejected as replay", async () => {
  const secret = "whsec_test_123";
  const ts = String(Math.floor(Date.now() / 1000) - 3600);
  const body = '{"id":"evt_4"}';
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(ts + "." + body));
  const hex = [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
  const ok = await verifyStripeSignature(body, `t=${ts},v1=${hex}`, secret);
  assert.equal(ok, false);
});

test("stripe: malformed header rejected", async () => {
  assert.equal(await verifyStripeSignature("{}", "", "whsec_x"), false);
  assert.equal(await verifyStripeSignature("{}", "t=abc", "whsec_x"), false);
  assert.equal(await verifyStripeSignature("", "t=1,v1=abc", "whsec_x"), false);
});

test("stripe: parseStripeSigHeader picks t and all v1s", () => {
  const p = parseStripeSigHeader("t=1492774577,v1=aaa,v0=bbb,v1=ccc");
  assert.equal(p.t, "1492774577");
  assert.deepEqual(p.v1, ["aaa", "ccc"]);
});

/* ---------- NOWPayments IPN ---------- */

test("nowpayments: signature is deterministic over key order", async () => {
  const secret = "ipn_secret_test";
  const a = { payment_id: "123", payment_status: "finished", order_id: "ord_1", nested: { b: 2, a: 1 } };
  const b = { nested: { a: 1, b: 2 }, order_id: "ord_1", payment_status: "finished", payment_id: "123" };
  const sa = await nowpaymentsSignature(a, secret);
  const sb = await nowpaymentsSignature(b, secret);
  assert.equal(sa, sb);
  assert.equal(sa.length, 128); // SHA-512 hex
});

test("nowpayments: valid IPN verifies", async () => {
  const secret = "ipn_secret_test";
  const payload = {
    payment_id: "5745459419",
    payment_status: "finished",
    pay_address: "rXRP...",
    price_amount: 149,
    price_currency: "usd",
    pay_currency: "xrp",
    order_id: "ord_abc",
  };
  const sig = await nowpaymentsSignature(payload, secret);
  assert.equal(await verifyNowpaymentsIpn(payload, sig, secret), true);
});

test("nowpayments: tampered payload fails", async () => {
  const secret = "ipn_secret_test";
  const payload = { payment_id: "1", payment_status: "finished", order_id: "ord_x" };
  const sig = await nowpaymentsSignature(payload, secret);
  const tampered = { ...payload, payment_status: "waiting" };
  assert.equal(await verifyNowpaymentsIpn(tampered, sig, secret), false);
});

test("nowpayments: missing secret/signature fails closed", async () => {
  const payload = { payment_id: "1" };
  assert.equal(await verifyNowpaymentsIpn(payload, "abc", ""), false);
  assert.equal(await verifyNowpaymentsIpn(payload, "", "secret"), false);
});

test("sortKeysDeep sorts nested keys and preserves arrays", () => {
  const out = sortKeysDeep({ z: 1, a: { d: 4, b: 2 }, arr: [{ y: 1, x: 2 }] });
  assert.deepEqual(Object.keys(out), ["a", "arr", "z"]);
  assert.deepEqual(Object.keys(out.a), ["b", "d"]);
  assert.deepEqual(Object.keys(out.arr[0]), ["x", "y"]);
});

/* ---------- pure helpers ---------- */

test("directQrPayload: BTC uses BIP-21, others raw address", () => {
  assert.equal(directQrPayload("BTC", "bc1qxyz"), "bitcoin:bc1qxyz");
  assert.equal(directQrPayload("XRP", "rXYZ"), "rXYZ");
  assert.equal(directQrPayload("XMR", "4ABC"), "4ABC");
});

test("centsToDecimal formats for PayPal/Stripe display", () => {
  assert.equal(centsToDecimal(14900), "149.00");
  assert.equal(centsToDecimal(49900), "499.00");
  assert.equal(centsToDecimal(79900), "799.00");
});

test("validateCreate accepts all providers, rejects bad input", () => {
  assert.equal(validateCreate({ provider: "stripe", item: "prep-sprint", email: "a@b.co" }).ok, true);
  assert.equal(validateCreate({ provider: "direct", item: "full-academy", coin: "xrp" }).ok, true);
  assert.equal(validateCreate({ provider: "direct", item: "full-academy", coin: "doge" }).ok, false);
  assert.equal(validateCreate({ provider: "nowpayments", item: "prep-sprint" }).ok, false); // coin required
  assert.equal(validateCreate({ provider: "bogus", item: "prep-sprint" }).ok, false);
  assert.equal(validateCreate({ provider: "stripe", item: "nope" }).ok, false);
  assert.equal(validateCreate({ provider: "stripe", item: "prep-sprint", email: "not-an-email" }).ok, false);
  // client-supplied amount is ignored entirely (no amount field read)
  const v = validateCreate({ provider: "stripe", item: "prep-sprint", amount_cents: 1 });
  assert.equal(v.ok, true);
  assert.equal(ITEMS[v.item].amount_cents, 14900);
});

test("providerConfigured checks env presence only", () => {
  assert.equal(providerConfigured({ STRIPE_SECRET_KEY: "sk_x" }, "stripe"), true);
  assert.equal(providerConfigured({}, "stripe"), false);
  assert.equal(providerConfigured({ PAYPAL_CLIENT_ID: "a", PAYPAL_CLIENT_SECRET: "b" }, "paypal"), true);
  assert.equal(providerConfigured({ PAYPAL_CLIENT_ID: "a" }, "paypal"), false);
  assert.equal(providerConfigured({ NOWPAYMENTS_API_KEY: "k" }, "nowpayments"), true);
  assert.equal(providerConfigured({ WALLET_BTC: "bc1..." }, "direct"), true);
  assert.equal(providerConfigured({}, "direct"), false);
});

test("coin catalog: 10 enumerated coins, each with UD key + NOWPayments code", () => {
  assert.equal(COINS.length, 10);
  for (const c of COINS) {
    assert.ok(c.code && c.pay_currency && c.ud_key && c.env_key, c.code);
    assert.equal(coinByCode(c.code.toLowerCase()).code, c.code);
  }
  const codes = COINS.map((c) => c.code);
  for (const want of ["XRP", "XLM", "ADA", "ALGO", "QNT", "HBAR", "IOTA", "XDC", "XMR", "BTC"]) {
    assert.ok(codes.includes(want), want);
  }
});

test("XRP/XLM carry destination-tag/memo config slots", () => {
  const xrp = coinByCode("XRP");
  const xlm = coinByCode("XLM");
  assert.equal(xrp.extra, "XRP_DESTINATION_TAG");
  assert.equal(xrp.extra_label, "Destination tag");
  assert.equal(xlm.extra, "XLM_MEMO");
  assert.equal(xlm.extra_label, "Memo");
});

test("safeEqual is length-strict and value-strict", () => {
  assert.equal(safeEqual("abc", "abc"), true);
  assert.equal(safeEqual("abc", "abd"), false);
  assert.equal(safeEqual("abc", "ab"), false);
  assert.equal(safeEqual("", ""), true);
});
