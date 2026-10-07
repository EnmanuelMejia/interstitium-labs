# Payments Setup — Interstitium Labs Checkout (Phase 4b)

> **⛔ NO LIVE TRANSACTIONS until every item below is complete and you have run
> one sandbox test purchase per provider.** The checkout page
> (`/enroll/checkout.html`) is built and wired, but every provider returns
> `provider_unavailable` until its secrets are set. The page then shows a
> "checkout isn't live yet" state with a waitlist call-to-action — that is the
> safe default, not a bug.

**What was built (2026-10-07, not deployed):**

- `docs/payment-routes.js` — Worker module: Stripe Checkout Sessions, PayPal
  Orders v2 (Venmo inside PayPal Checkout), NOWPayments hosted invoices for
  crypto, direct-wallet fallback with Unstoppable Domain resolution, and all
  webhook/IPN signature verification. Wired into `docs/_worker.js`.
- `docs/enroll/checkout.html` + `checkout.css` + `checkout.js` — branded
  checkout (motto *SCIENTIA OMNIA VINCIT*, "Created by Interstitium Labs"),
  provider/coin picker, QR rendering for direct crypto, fail-safe error states,
  mobile-first (390px).
- `docs/enroll/vendor/qrcode.js` — vendored MIT QR encoder (Kazuhiko Arase);
  QR codes render locally, no third-party QR service ever sees addresses.
- Order/entitlement records live in the existing `IL_ACCOUNTS` KV namespace
  (`pay:order:<id>`, `pay:entitle:<email>:<item>`). No new KV namespace needed.

**Endpoints (all same-origin; secrets never touch the browser):**

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/pay/create` | `{provider, item, coin?, email?}` → order + `redirect_url`, or direct-wallet details |
| GET | `/api/pay/status?order=` | Order status / entitlement check |
| GET | `/api/pay/ud` | Resolved addresses for `enmanuelmejia.crypto` (cached 24h) |
| POST | `/api/pay/webhook/stripe` | Stripe webhook (HMAC-SHA256 verified) |
| POST | `/api/pay/webhook/paypal` | PayPal webhook (verified via PayPal API) |
| POST | `/api/pay/ipn/nowpayments` | NOWPayments IPN (HMAC-SHA512 verified) |
| GET | `/api/pay/paypal/return` | PayPal return → server-side capture → success page |
| GET | `/api/pay/stripe/return` | Stripe return → session verify → success page |
| GET | `/api/pay/paypal/cancel` | → `/enroll/cancel.html` |

Prices are server-side only (`prep-sprint` $149, `devsecops-mastery` $499,
`full-academy` $799); the browser never sends an amount.

---

## 1. Stripe

1. Create/confirm your **Stripe account** (business details + bank payout).
2. Register the webhook endpoint in **Stripe Dashboard → Developers → Webhooks**:
   - URL: `https://interstitiumlabs.dev/api/pay/webhook/stripe`
   - Events: `checkout.session.completed`, `checkout.session.expired`
   - Copy the **signing secret** (`whsec_…`).
3. Copy your **secret key** (`sk_live_…`; use `sk_test_…` first for sandbox).
4. Set the secrets (from `~/workspace/apex-audit/`):
   ```bash
   npx wrangler secret put STRIPE_SECRET_KEY        # paste sk_live_… (or sk_test_… first)
   npx wrangler secret put STRIPE_WEBHOOK_SECRET    # paste whsec_…
   ```
5. Cards, Apple Pay, and Google Pay are all handled by Stripe Checkout
   automatically — no extra configuration.

## 2. PayPal (Venmo included)

Venmo is selectable by the buyer *inside* PayPal Checkout — no separate
integration needed. (Your PayPal Business account must have Venmo enabled as a
payment method; check **Account Settings → Payment methods**.)

1. **PayPal Developer Dashboard** (developer.paypal.com) → create a **Live**
   app (and a **Sandbox** app for testing) → copy **Client ID** + **Secret**.
2. In the app settings, add the webhook:
   - URL: `https://interstitiumlabs.dev/api/pay/webhook/paypal`
   - Events: `PAYMENT.CAPTURE.COMPLETED`, `CHECKOUT.ORDER.APPROVED`
   - Copy the **Webhook ID** (shown after you save the webhook).
3. Set the secrets:
   ```bash
   npx wrangler secret put PAYPAL_CLIENT_ID
   npx wrangler secret put PAYPAL_CLIENT_SECRET
   npx wrangler secret put PAYPAL_WEBHOOK_ID        # the webhook ID from step 2
   ```
4. Sandbox testing only — set a plain (non-secret) var in `wrangler.jsonc`:
   `"vars": { "PAYPAL_SANDBOX": "1" }`, then remove it before going live.
   (Vars change = config edit, no deploy needed beyond your normal deploy.)

## 3. NOWPayments (crypto rail)

1. Create your **NOWPayments account** (nowpayments.io) → **Dashboard →
   API keys** → generate a production key (and a sandbox key for testing).
2. **Dashboard → Settings → IPN**: set an **IPN secret key**, and set the
   **IPN callback URL** to `https://interstitiumlabs.dev/api/pay/ipn/nowpayments`.
3. Enable payouts/coins: make sure all 10 coins are enabled for your account:
   **XRP, XLM, ADA, ALGO, QNT, HBAR, IOTA, XDC, XMR, BTC**.
4. Set the secrets:
   ```bash
   npx wrangler secret put NOWPAYMENTS_API_KEY
   npx wrangler secret put NOWPAYMENTS_IPN_SECRET
   ```
5. Sandbox testing: `"vars": { "NOWPAYMENTS_SANDBOX": "1" }` in
   `wrangler.jsonc`, remove before going live.

## 4. Wallet addresses (direct-wallet fallback) — 10 coins

> **Count note:** the brief says "11 coins" but enumerates 10 (8 ISO 20022 +
> XMR + BTC). Slots below cover exactly the enumerated 10. If you want an
> 11th coin, name it and a slot gets added.

Provide **one receiving address per coin** — these are used ONLY as a fallback
when the Unstoppable Domain record for that coin is missing (UD records win
when present). Set each with:

```bash
npx wrangler secret put WALLET_XRP
npx wrangler secret put WALLET_XLM
npx wrangler secret put WALLET_ADA
npx wrangler secret put WALLET_ALGO
npx wrangler secret put WALLET_QNT
npx wrangler secret put WALLET_HBAR
npx wrangler secret put WALLET_IOTA
npx wrangler secret put WALLET_XDC
npx wrangler secret put WALLET_XMR
npx wrangler secret put WALLET_BTC
```

**XRP destination tag / XLM memo — required if your receiving address is a
shared/exchange address:**

- If your XRP address needs a destination tag, also set it or payments **will
  not be credited**:
  ```bash
  npx wrangler secret put XRP_DESTINATION_TAG
  ```
- If your XLM address needs a memo, set:
  ```bash
  npx wrangler secret put XLM_MEMO
  ```
- The checkout UI shows the tag/memo as a **required, copyable field** next to
  the QR code whenever it is configured.

## 5. Unstoppable Domain — `enmanuelmejia.crypto`

The checkout displays **"Pay to enmanuelmejia.crypto"** for the direct rail
and resolves each coin's address at runtime via the UD Resolution API
(cached 24h in KV; falls back to the `WALLET_*` secrets above per coin).

In your Unstoppable Domains dashboard (ud.me) → `enmanuelmejia.crypto` →
**Records → Crypto**, set these records:

| Record key | Value |
|---|---|
| `crypto.XRP.address` | your XRP address |
| `crypto.XLM.address` | your XLM address |
| `crypto.ADA.address` | your ADA address |
| `crypto.ALGO.address` | your ALGO address |
| `crypto.QNT.address` | your QNT address |
| `crypto.HBAR.address` | your HBAR address |
| `crypto.IOTA.address` | your IOTA address |
| `crypto.XDC.address` | your XDC address |
| `crypto.XMR.address` | your XMR address |
| `crypto.BTC.address` | your BTC address |

Verify any time: `GET https://interstitiumlabs.dev/api/pay/ud` returns each
coin's address and whether it came from `ud` or `env`.

---

## 6. Full secret list (copy/paste checklist)

```
STRIPE_SECRET_KEY          wrangler secret put STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET      wrangler secret put STRIPE_WEBHOOK_SECRET
PAYPAL_CLIENT_ID           wrangler secret put PAYPAL_CLIENT_ID
PAYPAL_CLIENT_SECRET       wrangler secret put PAYPAL_CLIENT_SECRET
PAYPAL_WEBHOOK_ID          wrangler secret put PAYPAL_WEBHOOK_ID
NOWPAYMENTS_API_KEY        wrangler secret put NOWPAYMENTS_API_KEY
NOWPAYMENTS_IPN_SECRET     wrangler secret put NOWPAYMENTS_IPN_SECRET
WALLET_XRP / WALLET_XLM / WALLET_ADA / WALLET_ALGO / WALLET_QNT /
WALLET_HBAR / WALLET_IOTA / WALLET_XDC / WALLET_XMR / WALLET_BTC
XRP_DESTINATION_TAG        (only if your XRP address needs one)
XLM_MEMO                   (only if your XLM address needs one)
```

Run `npx wrangler secret list` to confirm all are present. **Never put any of
these in the repo, in `enroll/config.js`, or in chat.**

## 7. Go-live test plan (sandbox first)

1. Set **test/sandbox** keys + `*_SANDBOX=1` vars first.
2. One test purchase per provider on `/enroll/checkout.html?tier=prep-sprint`:
   Stripe test card → PayPal sandbox → NOWPayments sandbox invoice →
   direct-wallet (send a dust amount, confirm `/api/pay/status?order=…`
   flips to `paid` — note: direct orders flip to `paid` only via webhook/IPN
   or manual verification; dust test confirms the address/QR render).
3. Refund/void every test purchase.
4. Swap to live keys, remove `*_SANDBOX` vars, re-run one **live $1-style**
   check per provider if the provider supports it, refund immediately.
5. Flip `paymentsLive` in `docs/enroll/config.js` only after the above —
   note: `config.js` still documents the old Payment-Links approach; the new
   Worker API (`/api/pay/*`) supersedes it for `checkout.html`.

## 8. Notes & limits (honest)

- **Direct-wallet payments have no automatic chain watcher.** NOWPayments and
  Stripe/PayPal confirm via webhook/IPN automatically; direct transfers are
  marked `paid` after manual verification (the UI says exactly this).
- PayPal webhooks are verified by calling PayPal's API (there is no local
  HMAC scheme) — `PAYPAL_WEBHOOK_ID` must match the registered webhook.
- NOWPayments IPN re-deliveries are idempotent; `parent_payment_id`
  callbacks (repeated/wrong-asset deposits) are never auto-fulfilled.
- Order data lives in `IL_ACCOUNTS` KV. The in-memory fallback in
  `payment-routes.js` is for local tests only and is **not durable**.
- Nothing here is deployed — `wrangler deploy` (needs your Cloudflare login)
  is still the release gate, same as the rest of Phase 4.
