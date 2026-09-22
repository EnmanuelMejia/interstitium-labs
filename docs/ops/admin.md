# Administer the site

Interstitium Labs is a **static** site under `docs/`, served as **Cloudflare Workers Assets** (domain: [interstitiumlabs.dev](https://interstitiumlabs.dev)). There is no application server and no secret Stripe keys in the repo.

## Edit content

1. Open [github.com/EnmanuelMejia/interstitium-labs](https://github.com/EnmanuelMejia/interstitium-labs).
2. Browse `docs/` and use GitHub’s web editor or a local clone.
3. Prefer inspectable HTML under `docs/about/`, `docs/prep/`, `docs/paths/`, `docs/enroll/`, etc.
4. Commit to `main` and push — Cloudflare picks up the asset publish from `docs/`.

Operator overview UI: [/admin/](https://interstitiumlabs.dev/admin/).

## Cloudflare Workers deploy

**Canonical edge:** Worker / Workers Assets project **`solitary-sound-015a`** → custom domain `interstitiumlabs.dev`.

GitHub Pages (`main` / `docs/`) may build in parallel for backup, but **production traffic is Cloudflare**. If `curl` shows 404 for files that exist in `docs/` on `main`, the Worker Assets publish is stale — re-upload / re-trigger Assets from the dashboard (or connected Git integration). Do not assume a GitHub Pages green check means the CF edge is current.

1. Sign in to the [Cloudflare dashboard](https://dash.cloudflare.com/).
2. Open Workers & Pages → project bound to `interstitiumlabs.dev` (name historically `solitary-sound-015a`).
3. Confirm the asset root is `docs/` on branch `main` (or upload the `docs/` folder as static assets).
4. Trigger **Deploy** / **Retry deployment** after each go-live push.
5. Verify with `curl -sI https://interstitiumlabs.dev/labs/superlab/` (expect 200) and security headers per [`_worker_security_headers.md`](./_worker_security_headers.md).
6. Hard-refresh / purge CDN cache if an old HIT persists.

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
