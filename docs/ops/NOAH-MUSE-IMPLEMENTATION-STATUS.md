# Noah AI / Muse-equivalent delivery status

Updated: 2026-10-02. This is a delivery ledger, not a feature-parity claim.

## Existing as-built behavior

- The public /noah/ workspace uses a browser-scoped conversation and memory module.
- The local workflow runner supports **only two approved tools**: site-curriculum search and local study-brief creation. A human must approve the artifact-writing step.
- The client has a procedural neural visualization and linked original asset files.
- The new reusable-skills module provides built-in research and study-brief templates; visitors can save, launch and delete their own templates *on this device*. This change is in a review branch until merged and deployed.
- External email connectors and a cloud computer are disabled rather than simulated.

## What remains to claim complete functional parity

1. Identity-backed, user-isolated server persistence and cross-device sync.
2. Authenticated background execution and durable scheduling when the browser is closed.
3. Isolated remote browser/computer with strict allowlists and bounded execution.
4. Permissioned connector framework, consent and approval receipts, including email and calendar.
5. General tool creation and invocation backed by reviewed policies (local templates are **not** equivalent).
6. Full file and document workflows, multimedia generation and editing with licensed model/service providers.
7. Full mobile capabilities, push delivery, device-specific permission handling and representative real-device QA.
8. Multi-agent delegation, operational observability, failure recovery and cost controls.
9. Independent, per-feature tests against the documented product behavior and production execution receipts.

## Release gates

- Review and pass node unit tests, source checks and Playwright browser tests on the skill PR.
- Merge after review, deploy to the authorized Cloudflare environment and verify the live /noah/ experience before marking any production row as verified.
- Establish an authenticated server runtime, a real job store and a bounded queue before enabling tools with external authority.
- Never advertise parity based on a mockup, a front-end UI, a code commit, or a list of planned features.

Canonical full inventory: [noah-capabilities.json](noah-capabilities.json).
