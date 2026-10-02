# Noah foundation and career workspace

Delivery increment: **2026-10-02**. The [capability matrix](./NOAH-CAPABILITY-MATRIX.md) records the broader Project Noah requirements at the inspected baseline. This increment supplies working browser features; it does not establish complete Muse parity or completion of every project phase.

## Implemented behavior

- `/jobs/` adds public Remotive listings, combined filters, imported postings, saved roles, comparisons, and a manual Preparing/Applied/Interview/Closed tracker. Jobright opens in its own service; a visitor can bring a selected posting here. Private Jobright recommendations, profiles, and credentials are not synchronized. Employer applications and contact remain external actions.
- A Noah job review displays the exact bounded prompt and requires fresh consent. Only that prompt is sent, even if the visitor previously enabled other memory/context sharing. Evidence checks distinguish stated experience, project learning, missing evidence, and unresolved location/seniority requirements. They do not calculate an invented eligibility percentage.
- `/noah/` supplies a resident workspace with a shared, device-scoped conversation, editable notes and learning goals, export/forget controls, visible answer provenance, and public-page context sharing that requires a separate opt-in. This store is shared with the existing floating Noah widget on the same origin. Coach and university still have separate legacy presentation/storage contracts.
- The workflow runner performs a real search of the 66-entry public curriculum index. It checkpoints completed steps and requires approval to create a downloadable reading brief. It has bounded retries, cancellation, and explicit unavailable external tools. Work executes while the page is open; a user resumes saved work after an interruption. It does not execute code or operate a remote computer.
- Noah's original procedural neural geometry renders in WebGL and changes with actual activity events. Motion respects reduced-motion preferences, page visibility, offscreen state, and the pause control. Editable GLB/Blender sources and a native 5120×1440 SDR render are supplied. [Graphics provenance and verification](./NOAH-GRAPHICS.md) records the separate video gate.
- Homepage navigation and career content connect both workspaces. Responsive layouts cover narrow screens through a 5120-pixel ultrawide viewport. Existing unrelated deployments, mail/DNS, private files, and backend data remain outside this increment.

## Data and authorization boundaries

Browser-local storage is bounded and user-controlled, but it is neither encrypted account storage nor cross-device synchronization. Shared browser profiles share these records. Common credential patterns are redacted; this is not a guarantee that arbitrary sensitive text can be recognized. Export and forget operate on each workspace's own keys. A remote request already processed cannot be retracted by clearing device history.

Public job snapshots carry retrieval time, source links, a 24-hour provider delay, and a stale-data notice. Visitors load the shared same-origin snapshot; they do not each query Remotive. `scripts/refresh-noah-jobs.mjs` refreshes with a six-hour minimum interval and preserves the previous valid snapshot on failure. No automatic refresh schedule is installed.

AI-generated replies and imported postings remain untrusted text. Reply formatting uses DOM/text nodes and validated links rather than interpreting HTML. The browser cannot grant authority to an email, payment, shell, cloud-computer, or arbitrary model-selected tool. Local workflow records are not server authorization credentials.

## Executed verification

The disposable Edge browser regression run on 2026-10-02 passed **29 checks**: real public snapshot loading; import canonicalization; saving and manual tracking; comparison; exact-prompt sharing and privacy overrides; memory CRUD/export/forget; checkpoint resume/approval/artifact downloads; safe reply links; WebGL; and responsive navigation/layout. Tested widths were 360, 768, 1920, and 5120 pixels, plus a 200% zoom equivalent. New-workspace page/console errors were absent in that run.

Automated axe checks found zero violations in the tested Noah and jobs views. Some color-contrast checks were unresolved; this is not a full WCAG conformance claim. Browser viewports are emulated; physical devices and other browsers are not established by this receipt. Browser remote-response tests use a controlled mock to inspect exact request content.

A separate live request to `https://learn.interstitiumlabs.dev/api/noah` returned HTTP 200, a non-fallback career preparation reply, and the allowed apex CORS origin. It used a generic public test scenario, not a private candidate profile. This establishes endpoint inference availability for that request, not accuracy across all jobs.

Root source checks and all **40 Node regression tests** pass. The pinned dependency audit reports zero vulnerabilities, and the Wrangler static-assets dry run passes. The release review additionally tests persistence deletion failure and stale-tab workflow behavior. The exact final results and deployment receipt are retained with the release.

## Release and recovery

Work is on `codex/project-noah`, based on `db3e74f99220deed6550a95bb3b6278a2b2629f9`. The existing apex Worker is **solitary-sound-015a**, with `docs/` as its asset source; merging to `main` starts its existing Workers Builds release. The app/API and university Workers retain their own deployments and bindings.

The immediately pre-increment apex version is `b9a4d6dc-1e87-43a7-af26-b768cb3b8bb3`, refreshed on 2026-10-02. Recheck the target and latest version before any recovery. If this increment requires code rollback, select that pre-increment version for the apex Worker, then verify its public pages and headers. Code rollback does not restore D1/KV data. No database migration or data restore is part of this increment. [Baseline and recovery evidence](./NOAH-BASELINE.md).

The GitHub check workflow uses pinned actions, exact dependency locks, read-only repository permissions, source/Node/dependency checks, and disposable Chromium browser tests. Local CLI credentials are unavailable; the authenticated GitHub connector provides the repository publication path. Production is verified after the Cloudflare build, not inferred from a dry run or branch upload.

## Remaining Project Noah scope

Authenticated user identity and tenant-isolated server memory; cross-origin/cross-device synchronization; durable closed-browser execution; provider-authorized connectors; sandboxed remote computer/code tools; multimodal generation services; validated mastery/curriculum expansion; business metrics and approval authority; native release signing/store access and physical-device testing; measured HDR10/4K/8K media delivery; full load/recovery tests; and complete benchmark parity remain open requirements. The practice application still has the missing build/migration contracts documented in the baseline. The current site features do not resolve those dependencies.
