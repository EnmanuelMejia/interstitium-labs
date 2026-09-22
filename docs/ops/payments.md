# Payments runbook (Stripe + PayPal)

**Honest status:** Student checkout on [/enroll/](https://interstitiumlabs.dev/enroll/) is **inactive** until Enmanuel pastes live Payment Link / PayPal URLs into `docs/enroll/config.js`, sets enabled flags + `paymentsLive: true`, and redeploys.

This is an **operator guide**, not legal, tax, or PCI advice. Confirm your own business/tax setup with qualified professionals.

## Phase 1 — Payment Links (no secrets in repo)

Static sites should use hosted checkout, not embedded secret-key charges.

### Stripe

1. Create / activate a [Stripe](https://dashboard.stripe.com/) account; complete identity and payouts for **live** mode when ready.
2. Products → create three products matching tiers (Prep Sprint, DevSecOps Mastery, Full Academy) with one-time prices (or your chosen amounts).
3. **Payment Links** → create one link per product.
   - Enable card payments; Stripe Link and Apple Pay / Google Pay appear where Stripe supports them for your account/region.
   - After payment → Success URL: `https://interstitiumlabs.dev/enroll/success.html`
   - If canceled → Cancel URL: `https://interstitiumlabs.dev/enroll/cancel.html`
4. Copy each Payment Link URL (`https://buy.stripe.com/…`).
5. Paste into `docs/enroll/config.js`:
   - `tiers[].stripePaymentLink`
   - `tiers[].stripeEnabled: true`
   - When at least one live link is ready: `paymentsLive: true`
6. Commit, push `main`, wait for Cloudflare Workers Assets deploy.
7. Open `/enroll/` and click through **one** live link in a private window (use Stripe test mode links first if still validating).

**Do not** put `sk_live_`, `sk_test_`, or webhook secrets in git. Publishable keys are optional for Payment Links and are not required for this static wiring.

### Optional PayPal

1. In PayPal business tools, create no-code / payment buttons or payment links for the same three offers.
2. Paste URLs into `tiers[].paypalLink` and set `paypalEnabled: true`.
3. Redeploy as above.

## Operator fulfillment (until webhooks)

Phase 1 has **no automatic entitlements**. When a payment email/receipt arrives:

1. Confirm amount and product name.
2. Email the student kickoff (prep map, calendar link, expectations).
3. Log the sale offline (spreadsheet is fine).

## Phase 2 — Webhooks (later)

When you want automatic access grants:

- Add a small Worker or backend that verifies Stripe/PayPal webhooks with secrets stored in Cloudflare secrets (never in `docs/`).
- Update CRM / mailing list / invite codes from the event.
- Keep Payment Links as the public CTA; webhooks only confirm.

## Related

- [admin.md](./admin.md)
- Config file: `docs/enroll/config.js`
- Console: [/admin/](https://interstitiumlabs.dev/admin/)
