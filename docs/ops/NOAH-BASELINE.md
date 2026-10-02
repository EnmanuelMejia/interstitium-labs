# Project Noah: verified production baseline

Observed on 2026-10-01 between 20:25 and 20:29 UTC (4:25–4:29 p.m. America/New_York), before Project Noah changes. This is a historical snapshot, not a claim about a later release. The audit used authenticated, read-only Cloudflare API calls, Workers Builds metadata/logs, public HTTPS requests, and repository inspection. No cloud resource, database row, secret, or deployment was changed. Machine-readable observations are in `noah-baseline.json`.

## Actual deployment boundary

| Public surface | Live service | Release observed | HTTP result |
| --- | --- | --- | --- |
| `interstitiumlabs.dev` | Worker `solitary-sound-015a`, static assets from `docs/` | Version `b9a4d6dc-1e87-43a7-af26-b768cb3b8bb3` (115), deployment `9cd28481-5c7e-4365-945c-1af71f67df56`, 100%, 2026-10-01 16:35:25 UTC | 200, title “Interstitium Labs — The Learning OS for unusually ambitious builders” |
| `app.interstitiumlabs.dev` | Worker `interstitium-labs` | Version `9b1a40d1-46df-4a0f-ac6e-f86092c2aa7f`, deployment `4fbdaf6d-9395-486b-bf5c-56479bf4b250`, 100%, 2026-09-20 00:09:50 UTC | 200, title “Interstitium Labs 3.0 — Knowledge Operating System” |
| `api.interstitiumlabs.dev` | Same Worker `interstitium-labs` | Same separate app/API release | `/api/health`: 200; `ok: true`, service `interstitium-labs-edge`, environment `production`, database `connected` |
| `learn.interstitiumlabs.dev/*` | Zone route to Worker `interstitium-labs-university` | Version `69dd82ba-2d6c-4812-94a5-d30728537940`, deployment `6f86d6d1-e24b-42a7-b155-bd69d6c67a03`, 100%, 2026-10-01 17:52:23 UTC | 200, title “Interstitium Labs — Knowledge Operating System” |

The apex site is **not** the Worker named `interstitium-labs`. Cloudflare reports no Pages projects in the connected account. The target DNS zone is active. App/API custom domains target `interstitium-labs`; the apex custom domain targets `solitary-sound-015a`; university uses a zone route rather than a custom-domain entry.

## Exact apex source and release

- Repository: `EnmanuelMejia/interstitium-labs`, GitHub.
- Production build branch: `main`; trigger includes `main` only, all paths, no path exclusions.
- Commit: `db3e74f99220deed6550a95bb3b6278a2b2629f9`.
- Successful build: `8b7f025c-db14-4923-9817-f8e971d39267`, started 16:32:50 UTC, stopped 16:35:28 UTC on 2026-10-01.
- Build root: `/`; build command empty; deployment command `npx wrangler deploy --assets docs`.
- Build logs explicitly report `Current Version ID: b9a4d6dc-1e87-43a7-af26-b768cb3b8bb3`, matching the active apex deployment. This establishes the commit-to-production link.
- Root `wrangler.jsonc` independently names `solitary-sound-015a`, compatibility date `2026-09-23`, static directory `./docs`, trailing-slash handling, and a 404-page fallback.

App/API and university have no Workers Builds entries in this account at inspection. Their exact source branches and commit linkage are unverified. Do not assume the apex commit is their source or publish them with the apex configuration.

## Bound resources and authentication

Only names and types are retained here; no environment values, credentials, account identifiers, personal records, or recovery bookmark values are published.

| Worker | Binding names and types |
| --- | --- |
| `solitary-sound-015a` | No named bindings returned |
| `interstitium-labs` | `AI_MODEL` / plain text; `API_LIMIT` / rate limit; `APP_ENV` / plain text; `APP_ORIGIN` / plain text; `ASSETS` / assets; `DB` / D1 |
| `interstitium-labs-university` | `AI` / Workers AI; `NOAH_STATS` / KV namespace (`noah-stats`) |

Secret-name inventories for all three Workers are empty. This does not establish that every possible upstream credential is absent. No secret values were requested. The app/API D1 database exists and its public health check reports connected. University has a live Workers AI binding; that binding does not itself verify any individual inference, model output, or task capability.

Cloudflare connector authentication works for these read operations. Write/deploy permission was not exercised. Local Wrangler was not found as a globally available command during this inspection; local CLI authentication was not verified. A working connector is not proof that a local CLI is signed in. Public health checks do not verify user sign-in, authorization, memory isolation, or provider OAuth flows.

## Runtime gaps in the primary repository

`apps/practice/` has application source and package metadata, but its referenced `scripts/` and `migrations/` directories are absent in the checked-out baseline. Consequently:

- `dev`, `build`, `build:dev`, and `preview` call missing `scripts/with-app-env.mjs`.
- `db:migrate` calls missing `scripts/migrate.mjs`; preview controls and `check:auth` also reference missing files.
- Vite imports missing `scripts/grok-pwa-plugin.mjs`, `scripts/app-env-plugin.mjs`, and `scripts/migration-plan.mjs`.
- Its test command references missing script tests; its database bootstrap expects migrations.
- Its Nitro build preset is `vercel`; there is no practice-local Worker configuration.

Do not call that application runnable or deployed merely because its source and README exist. Restore the intended runtime contracts and migration provenance before running any database migration or mapping that source onto the live D1-backed Worker. The apex can be changed independently through its existing static-assets release path.

## Header and voice findings

The apex HTTPS response includes HSTS, CSP, `nosniff`, frame denial, referrer restrictions, and origin isolation headers. Its global Permissions Policy disables microphone access. `_headers` attempts to allow microphone access under `/coach/*` and `/cinema/*`, but live requests to both paths return the global disabled policy **and** the route-specific policy. Voice enablement is therefore unverified and the configuration needs correction before a voice feature is claimed to work.

Cloudflare documents that repeated header values are combined. A route override can detach the inherited header with `! Permissions-Policy`, then attach the intended route policy. Verify the resulting single live header and actual browser behavior after release. Worker-generated responses require their own headers; static `_headers` does not cover them. See [Cloudflare static asset headers](https://developers.cloudflare.com/workers/static-assets/headers/).

## Recovery procedure

Code release and user-data recovery are separate operations. Before any release, record the active deployment/version for the **specific** target Worker and verify that no unexpected release has occurred since this snapshot. Keep branch changes off `main` until release gates pass: pushing `main` starts the observed apex build trigger.

For apex code rollback, the immediately preceding observed version is `784a6aac-0890-42c0-8736-4c59aed4d900` (deployment `cdd79d8d-1712-4a5d-b1c9-41fe4c97f94b`). In Cloudflare Dashboard, select **Workers & Pages → solitary-sound-015a → Deployments**, inspect the intended version, and select **Rollback**. Alternatively, after confirming authentication/account/target, use `wrangler rollback 784a6aac-0890-42c0-8736-4c59aed4d900 --name solitary-sound-015a`. Rollback is an immediate production mutation; it was not performed here. Recheck public pages, script assets, health endpoints, headers, and the active version afterward. [Cloudflare rollback documentation](https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/).

University's immediately preceding observed version is `b1adb047-db62-4cd2-a88e-3afe437bd8aa` (2026-10-01 16:36:51 UTC). The app/API Worker has only one observed deployment, so this snapshot provides no earlier app/API rollback candidate. Inspect its own release history before changing it. At inspection the apex had 115 deployment records and university had 21; Cloudflare rollback limits and binding compatibility still apply.

A read-only D1 Time Travel bookmark request succeeded for the app/API database. Its exact bookmark was intentionally omitted from public files. Before any authorized data change, retrieve and securely retain a fresh bookmark and verify the applicable retention window. For a required data recovery, stop conflicting writes, select a confirmed timestamp/bookmark, obtain approval for the destructive restore, use D1's restore workflow, then validate schema, application health, and relevant data without exposing records. Code rollback does not roll back D1 or KV content. KV recovery needs a separately authorized backup/restore process; no KV content was read or backup created in this audit. Do not alter bindings, resources, or stored data to simplify a code rollback.

## Assets and local production dependencies

Existing asset rights/provenance were not established by this infrastructure audit. Build messages describing generated cinematic media do not establish licenses, ownership, HDR mastering, genuine 3D source, or permission to use film footage. Retain edit sources and provider/license evidence per asset. Requested film footage must remain excluded unless authorized rights are verified.

Targeted local checks found FFmpeg 9.0.2 and Android SDK ADB 37.0.1, emulator binaries, build-tools 36.0.0, and Android Studio's bundled Java executable. Blender was not found on PATH, in the standard Program Files locations, or in exact-name uninstall entries; this is a bounded discovery result, not proof it is absent everywhere. Android command-line tools were not found in the usual SDK directory. No tool was installed, emulator started, device contacted, 3D scene rendered, or mobile build performed in this audit.

Supplemental read-only dependency research on 2026-10-01 established a viable portable Blender option: the [official Blender 5.2.2 Windows download portal](https://www.blender.org/download/release/Blender5.2/blender-5.2.2-windows-x64.zip/) links the [Windows x64 ZIP](https://mirror.blender.org/release/Blender5.2/blender-5.2.2-windows-x64.zip). A HEAD request returned 200, `application/zip`, and 404,453,484 bytes. The [official SHA-256 manifest](https://mirror.blender.org/release/Blender5.2/blender-5.2.2.sha256) returned 200 and lists ZIP checksum `3849d17a682cba006075aaa3f3597ecb5c9c30ec31035b2e092c53e40679b535`. The package was not downloaded or executed for this audit. A separately authorized, verified portable runtime can create a real `.blend` without changing a system installation; local discovery alone is not a blocker.

The portfolio Worker `enmanuel-mejia`, its domains, mail/DNS records outside the target, and private/family services are outside this change. Do not publish `private/` or move an unrelated domain to another Worker.

## Reverification

Run `node scripts/verify-noah-baseline.mjs` for read-only public status checks. It can confirm public availability and report the known voice-header issue; it cannot establish release IDs, account access, user-data isolation, license rights, or product capability parity. Requery authenticated Cloudflare release metadata for any future production baseline.
