# Administer the site

Interstitium Labs is a **static** site under `docs/`, served as **Cloudflare Workers Assets** (domain: [interstitiumlabs.dev](https://interstitiumlabs.dev)). There is no application server and no secret Stripe keys in the repo.

## Edit content

1. Open [github.com/EnmanuelMejia/interstitium-labs](https://github.com/EnmanuelMejia/interstitium-labs).
2. Browse `docs/` and use GitHub’s web editor or a local clone.
3. Prefer inspectable HTML under `docs/about/`, `docs/prep/`, `docs/paths/`, `docs/enroll/`, etc.
4. Commit to `main` and push — Cloudflare picks up the asset publish from `docs/`.

Operator overview UI: [/admin/](https://interstitiumlabs.dev/admin/).

## Cloudflare Workers deploy

1. Sign in to the [Cloudflare dashboard](https://dash.cloudflare.com/).
2. Open the Workers / Pages (Assets) project bound to `interstitiumlabs.dev`.
3. Confirm the publish root is `docs/` on branch `main`.
4. After each push, wait for the deployment to succeed; hard-refresh the live URL if CDN cache lags.

Local preview:

```bash
cd docs && python3 -m http.server 8080
```

## Enrollment commerce config

Public checkout URLs live in [`docs/enroll/config.js`](https://github.com/EnmanuelMejia/interstitium-labs/blob/main/docs/enroll/config.js). See [payments.md](./payments.md). Never commit Stripe **secret** keys (`sk_live_…`, `sk_test_…`, webhook signing secrets).

## Future: Decap CMS + Cloudflare Access

Planned (not built):

- **Decap CMS** (or similar) for non-git operators to edit markdown/HTML via a `/admin` Git Gateway.
- **Cloudflare Access** in front of any write UI so the public cannot open an editor.

Until then, GitHub + this static `/admin/` console are the administration surface.

## Related

- [payments.md](./payments.md) — Stripe / PayPal go-live
- [AUDIT.md](./AUDIT.md) — URL map and commerce status
- [PENDING-IMPORTS.md](./PENDING-IMPORTS.md) — ChatGPT shares awaiting extract
