# Project Noah capability and implementation matrix

Version **2026-10-01.1** · checked **2026-10-01 (America/New_York)** · schema **1.0.0**

**Complete parity: unverified. Production readiness: unverified.** This is a versioned requirement and evidence ledger. Public Muse documentation was read; no signed-in Muse feature, remote Noah tool or production deployment was executed by this matrix audit.

The subsequent [2026-10-02 implemented increment](./NOAH-IMPLEMENTATION.md) records executed foundation/jobs checks separately; the rows below retain their dated baseline evidence.

The authoritative structured counterpart is [noah-capabilities.json](./noah-capabilities.json). Both files carry per-capability behavior, implementation, dependencies, security, acceptance checks, status, evidence and limitations.

## Evidence boundary

Inspected baseline commit: `db3e74f99220deed6550a95bb3b6278a2b2629f9`. New files and concurrent changes remain pending independent verification. Code inspection demonstrates a source path; it does not demonstrate successful execution, deployed behavior or acceptance-test completion.

- Documented current means the primary source describes the behavior; no account/device execution was performed.
- Announced future and rollout-unverified features are recorded separately from documented current requirements.
- Every Noah row distinguishes inspected code, ongoing work, external dependencies and unverified runtime.
- Promote a row only after an execution receipt, passing acceptance tests and deployment evidence where relevant.
- No complete directory enumeration: muse.ai redirected to auth.muse.ai; app connector settings were not accessible.
- Provider/model products must not automatically be counted as consumer-agent functionality.

### Status meanings

| Status | Meaning |
| --- | --- |
| inspected_partial | Equivalent source behavior exists in the inspected entry points; remaining scope and runtime are unverified. |
| pending_verification | New implementation is in progress or present as source; independent checks are required. |
| planned | Required work is identified; no working equivalent is claimed. |
| blocked_external_dependency | Real provider, account, compute, device, signing or other external access is required. |
| unverified | Matrix scope does not establish the requirement. |

The benchmark labels `documented_current`, `announced_future` and `announced_rollout_unverified` describe the primary source, not observed account availability. The complete connector directory lives behind authentication: muse.ai redirected to auth.muse.ai; in-app settings were unavailable.

### Existing scope reconciliation

docs/ops/MUSE-AI-MOBILE-CAPABILITY-BENCHMARK.md is a historical narrower Learning-OS comparison. Its YES/zero-gap/connector-N/A assertions are not Project Noah parity evidence. The current directive expands scope; preserve the historical file and use this versioned ledger.

## Phase gates

Phase 1 establishes evidence and recovery. Later phases remain open until their acceptance evidence is recorded. Working local increments can be released independently after their own checks.

| Phase | Work | Status | Acceptance gate |
| --- | --- | --- | --- |
| 1 | Audit and recovery: Exact production/repository baseline; active branch/release; permissions; apps/services/defects; AI reachability; asset licenses; identity/persistence; exposure review; rollback. | partial_inspection | Dated exact commit/release evidence and recoverable rollback; root baseline ledger owns infrastructure verification. |
| 2 | Unified architecture: Shared identity/context/storage contracts across website, practice, university and mobile; canonical curriculum and preserved branding. | planned | Contract tests and deliberate migration with no unrelated data loss. |
| 3 | Noah foundation: Resident workspace; real bounded local tool outputs; checkpoints/retries/cancel/approvals; shared device conversation/memory controls. | pending_verification | Executed reload/resume/delete/deny/cancel/output tests; no closed-browser or remote-executor claim. |
| 4 | Cinematic and 3D identity: Original state-linked 3D; vector/Blender masters; original 20-second neural cinematic and adaptive exports. | pending_verification | Reopen assets and verify geometry, timing, dimensions/color/codec, fallbacks and rights. |
| 5 | Adaptive learning: Actual lesson/code/results/mastery context; canonical courses/labs/assessments/remediation/capstones; FDE FORGE where artifacts substantiate it. | partial_inspection | Independent source/answer validation and reproducible learner-outcome fixtures. |
| 6 | Mobile and compatibility: Preserved Capacitor/PWA; authorized sync; release builds, metadata and actual-device tests where toolchains/accounts available. | partial_inspection | Build/device receipts and clear unavailable targets; existing CI configuration is not a current passed run. |
| 7 | Business and bounded improvement: Authorized connectors; actual founder metrics; distinct agent scopes; independent approval authority and release gates. | blocked_external_dependency | Provider sandbox receipts and negative authorization tests; no unapproved sends/purchases/publishing. |
| 8 | Production hardening: Security/accessibility/performance/load/recovery tests; measured results; verified release and rollback. | planned | Dated executed checks and production behavior; targets distinguished from measured results. |

## Repository and artifact reconciliation

| Surface | Inspected source | Finding and implication |
| --- | --- | --- |
| Public site | docs/assets/noah-ai.js; docs/assets/il-muse.js | Knowledge-first widget and local coach with separate storage. Add shared device/context adapters; preserve legacy data until validated. |
| Practice | apps/practice/src/lib/muse-ask.ts; harness.ts; db.ts | Model routes, memory/goal/SQL functions and optional TTS; Neon/PGLite code paths. Configuration is not deployed/authenticated/tenant-isolated persistence. |
| University | university:js/noah.js; CONTRACT.md | Separate static Socratic widget, catalog and adaptive contract. Reuse canonical node/context interfaces; separate origins do not share localStorage. |
| Mobile | apps/mobile/package.json; README.md; src/il-bridge.js | Capacitor/PWA structure and native feature stubs documented. Source reuse does not prove signed builds, store release, push or real-device behavior. |
| Visuals | docs/assets/chrome/; docs/assets/immersive/; scripts/blender_polish_glb.py | SVG/raster/GLB/processing scripts and media filenames present. Preserve assets; verify licenses, editable sources, metadata, composition and fallback. |
| Current increment | docs/noah/index.html; docs/assets/noah-session.js; docs/assets/noah-workflows.js | Workspace references bounded curriculum-search/study-brief executor and device-only store; in progress. Independent root tests must promote delivery status. Email/cloud tools are explicitly unavailable. |

`university:` references the separately inspected university repository, not a directory inside this repository. Its static catalog and adaptive contract provide reusable education interfaces. It retains a separate origin/deployment; browser-local history cannot supply cross-origin or cross-device synchronization.

SVG, raster, GLB, processing scripts and existing cinematic filenames were inventoried. Their presence does not establish licenses, genuine editable Blender masters, measured HDR10, requested resolution profiles or 20-second seamless duration.

## Documented Muse capabilities

Every acceptance check below is a required test, not a reported passing result. Runtime, production and parity flags remain false in this version. Independent root verification may later attach receipts and update the relevant flags without closing unrelated gaps.

### M01 — Persistent main conversation

- **Muse:** Ongoing main chat preserves context. [How We Designed Muse](https://introducing.muse.ai/). Benchmark status: `documented_current`.
- **Noah now:** Widget stores recent history; coach saves main chat on this browser.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Share one versioned conversation store across resident surfaces; add authenticated server persistence.
- **Dependencies:** Origin storage, schema migration, later identity/database
- **Security:** Keep retention bounded; prevent script injection; isolate users.
- **Acceptance:** Reload restores messages; deleting context removes it from subsequent model input.
- **Evidence:** `docs/assets/noah-ai.js` — ensureKB, askLocal/askRemote, loadHistory/saveHistory, buildWidget (inspected; not executed in this matrix audit); `docs/assets/il-muse.js` — load/save/getChat, send generation guard, goalsPanel, settingsPanel (inspected; not executed in this matrix audit); `docs/assets/noah-session.js` — device-scoped history and memory controls (Source implementation in progress; pending independent execution verification.)
- **Remaining limits:** Device/origin storage is not cross-device persistence.

### M02 — Side chats

- **Muse:** Separate topic chats share assistant awareness. [How We Designed Muse](https://introducing.muse.ai/). Benchmark status: `documented_current`.
- **Noah now:** Coach has main and side chats.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Unify side-chat context routing and expose deletion.
- **Dependencies:** Conversation store; context selector
- **Security:** Limit context to approved chats and current user.
- **Acceptance:** Create two chats, switch/reload, verify explicit context access and deletion.
- **Evidence:** `docs/assets/il-muse.js` — load/save/getChat, send generation guard, goalsPanel, settingsPanel (inspected; not executed in this matrix audit)
- **Remaining limits:** Inspected-only; new /noah workspace integration pending.

### M03 — Interruptible concurrent requests

- **Muse:** Accepts interruptions and multiple concurrent tasks. [How We Designed Muse](https://introducing.muse.ai/). Benchmark status: `documented_current`.
- **Noah now:** Coach uses inflightGen to suppress interrupted replies.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Cancel underlying tool/model work; separate task identities and resumable queues.
- **Dependencies:** Abortable model calls; workflow state
- **Security:** Do not treat interrupted writes as safely cancelled without receipt reconciliation.
- **Acceptance:** Interrupt task A, send B, verify stale A cannot overwrite B or duplicate a write.
- **Evidence:** `docs/assets/il-muse.js` — load/save/getChat, send generation guard, goalsPanel, settingsPanel (inspected; not executed in this matrix audit); `docs/noah/` — root-owned /noah workspace and bounded local workflow executor (Source implementation in progress; pending independent execution verification.)
- **Remaining limits:** Generation suppression is not server cancellation or concurrent durable execution.

### M04 — Memory inspection and correction

- **Muse:** Editable memory files personalize responses. [How to manage your Muse data](https://www.meta.com/help/artificial-intelligence/2225571704857152/). Benchmark status: `documented_current`.
- **Noah now:** Coach memories are manually added/removed and included in model context.
- **Status / phase:** `pending_verification` / 3.
- **Required implementation:** Provide inspect/edit/delete controls and consistent store across widget/workspace.
- **Dependencies:** Versioned device store; later tenant database
- **Security:** Never retain credentials as memory; sanitize imported objects.
- **Acceptance:** Save/edit/delete memory; refresh and inspect the actual next model input.
- **Evidence:** `docs/assets/il-muse.js` — load/save/getChat, send generation guard, goalsPanel, settingsPanel (inspected; not executed in this matrix audit); `apps/practice/src/lib/muse-ask.ts` — askTutor validator/handler, remember/goal/sql/assist routes (inspected; not executed in this matrix audit); `docs/assets/noah-session.js` — device-scoped history and memory controls (Source implementation in progress; pending independent execution verification.)
- **Remaining limits:** Device controls in progress; backend route alone is not storage proof.

### M05 — Forgetting and selective deletion

- **Muse:** Removes selected learned information best-effort. [How to manage your Muse data](https://www.meta.com/help/artificial-intelligence/2225571704857152/). Benchmark status: `documented_current`.
- **Noah now:** Coach can remove selected memories; practice parses forget requests.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Delete eligible information across memory, chats, derived artifacts and context indexes; show scope.
- **Dependencies:** Searchable store; deletion receipts
- **Security:** Deletion must not resurrect via fallback/migration; document backup retention.
- **Acceptance:** Forget a marker, reload/export and search eligible stores and outbound context.
- **Evidence:** `docs/assets/il-muse.js` — load/save/getChat, send generation guard, goalsPanel, settingsPanel (inspected; not executed in this matrix audit); `apps/practice/src/lib/muse-ask.ts` — askTutor validator/handler, remember/goal/sql/assist routes (inspected; not executed in this matrix audit); `docs/assets/noah-session.js` — device-scoped history and memory controls (Source implementation in progress; pending independent execution verification.)
- **Remaining limits:** Message deletion and memory deletion are distinct operations.

### M06 — Export and complete reset

- **Muse:** Exports data; irreversible reset clears agent. [How to manage your Muse data](https://www.meta.com/help/artificial-intelligence/2225571704857152/). Benchmark status: `documented_current`.
- **Noah now:** Existing artifact/proof workflows differ from whole-agent export/reset.
- **Status / phase:** `pending_verification` / 3.
- **Required implementation:** Export eligible device data; reset local history/memory/workflows with explicit confirmation.
- **Dependencies:** Device store; download support; server deletion later
- **Security:** Exclude tokens, provider settings and unrelated learning data unless expressly selected.
- **Acceptance:** Export, inspect contents, reset, reload and ensure deleted state stays deleted.
- **Evidence:** `docs/assets/noah-session.js` — device-scoped history and memory controls (Source implementation in progress; pending independent execution verification.)
- **Remaining limits:** No claim of cloud deletion, backup deletion or authenticated multi-device reset.

### M07 — Assistant identity and communication

- **Muse:** Name, avatar, tone and preferences persist. [How to customize Muse's personality and memories](https://www.meta.com/help/artificial-intelligence/995796179982326/). Benchmark status: `documented_current`.
- **Noah now:** Coach stores assistant name, avatar, tone/personality and voice choice.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Carry chosen identity and preferences across resident modes.
- **Dependencies:** Shared profile schema; presentation adapters
- **Security:** Custom identity cannot change policy, authorization or system boundaries.
- **Acceptance:** Change tone/name, reload, open other mode, verify permitted preferences only.
- **Evidence:** `docs/assets/il-muse.js` — state name/personality/tone/memories/voice/avatar settings (inspected; not executed in this matrix audit)
- **Remaining limits:** Browser profile is not unified authenticated identity.

### M08 — Import prior assistant memory

- **Muse:** Imports prior assistant chat ZIP exports. [How to customize Muse's personality and memories](https://www.meta.com/help/artificial-intelligence/995796179982326/). Benchmark status: `documented_current`.
- **Noah now:** No ZIP memory importer located in inspected entries.
- **Status / phase:** `planned` / 3.
- **Required implementation:** Validated import preview with provenance, schema and selective consent.
- **Dependencies:** ZIP parser; provider export adapters; import quota
- **Security:** Treat history as data; reject traversal, zip bombs, secrets and instruction authority.
- **Acceptance:** Import supported sample; reject unsafe archive; inspect selective persistence.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Supported provider formats and consent UX require implementation.

### M09 — Goals and progress tracking

- **Muse:** Goals tab tracks plans and progress. [How We Designed Muse](https://introducing.muse.ai/). Benchmark status: `documented_current`.
- **Noah now:** Coach goals support add and done checkboxes; practice goal parsing.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Connect goal plans to real task outcomes and checkpoints.
- **Dependencies:** Goal schema; workflow receipts
- **Security:** Protect edits per user; avoid fabricated completion.
- **Acceptance:** Create goal, execute a supported task, verify completion derives from receipt.
- **Evidence:** `docs/assets/il-muse.js` — load/save/getChat, send generation guard, goalsPanel, settingsPanel (inspected; not executed in this matrix audit); `apps/practice/src/lib/muse-ask.ts` — askTutor validator/handler, remember/goal/sql/assist routes (inspected; not executed in this matrix audit); `docs/noah/` — root-owned /noah workspace and bounded local workflow executor (Source implementation in progress; pending independent execution verification.)
- **Remaining limits:** Checkboxes and plans do not prove autonomous goal completion.

### M10 — Proactive ideas and controls

- **Muse:** Ideas and selective proactive notifications. [How We Designed Muse](https://introducing.muse.ai/). Benchmark status: `documented_current`.
- **Noah now:** Coach derives local study nudges from goals and weak topics.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Expose frequency/off controls; server event workers for closed-app work.
- **Dependencies:** Adaptive state; later event bus/push
- **Security:** Opt-in notifications; quiet unchanged states; no unapproved external actions.
- **Acceptance:** Disable nudges; simulate meaningful change; verify one event and no repeats.
- **Evidence:** `docs/assets/il-muse.js` — localNudges/buildNudgeCandidates/harvestNudges/tryLocalNotification (inspected; not executed in this matrix audit)
- **Remaining limits:** Open-page nudges do not run after browser closes.

### M11 — Dedicated isolated execution computer

- **Muse:** Per-user cloud Linux computer with browser/shell. [How We Built Safety Into Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse). Benchmark status: `documented_current`.
- **Noah now:** Static browser logic and practice server functions exist; no per-user VM verified.
- **Status / phase:** `blocked_external_dependency` / 3.
- **Required implementation:** Provision isolated executor with controlled browser, filesystem and shell.
- **Dependencies:** VM/container provider; tenant identity; resource budgets
- **Security:** External policy authority, non-root runtime, restricted egress and secrets.
- **Acceptance:** Two tenants cannot read each other's files; runaway job stops; denial enforced.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Static workflow UI is not a VM, shell, unrestricted browser or tenant boundary.

### M12 — Browser navigation and forms

- **Muse:** Shared browser handles navigation and forms. [How your Muse agent browses the web](https://www.meta.com/en-gb/help/artificial-intelligence/2124746764949121/). Benchmark status: `documented_current`.
- **Noah now:** Coach opens approved links; no controlled remote browser located.
- **Status / phase:** `planned` / 3.
- **Required implementation:** Attach isolated browser sessions and reviewed structured operations.
- **Dependencies:** Browser service; viewport stream; executor
- **Security:** Validate destinations/redirects; defend SSRF and prompt injection.
- **Acceptance:** Navigate/read/fill fixture form; observe state; deny unauthorized submission.
- **Evidence:** `docs/assets/il-muse.js` — load/save/getChat, send generation guard, goalsPanel, settingsPanel (inspected; not executed in this matrix audit)
- **Remaining limits:** Opening a website is not browser automation.

### M13 — Browser observe/take control/stop

- **Muse:** Users observe, take control, or stop browsing. [How your Muse agent browses the web](https://www.meta.com/en-gb/help/artificial-intelligence/2124746764949121/). Benchmark status: `documented_current`.
- **Noah now:** Coach Stop concerns chat; no remote browser session control.
- **Status / phase:** `planned` / 3.
- **Required implementation:** Browser session viewer, human takeover and authoritative stop.
- **Dependencies:** Session server; interrupt channel; audit log
- **Security:** Ownership checks on stream and control channel; reconcile in-flight actions.
- **Acceptance:** Takeover blocks agent input; stop closes task session without leaking other users.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** No browser control or remote desktop capability verified.

### M14 — Files, shell and code tools

- **Muse:** Filesystem and terminal build custom tools. [How We Designed Muse](https://introducing.muse.ai/). Benchmark status: `documented_current`.
- **Noah now:** Knowledge answers and practice SQL subset exist.
- **Status / phase:** `planned` / 3.
- **Required implementation:** Scoped executor files/shell and artifact receipts; tool compilation tests.
- **Dependencies:** Isolated executor; tool registry; object storage
- **Security:** No host filesystem access; sandbox code/network; validate uploads.
- **Acceptance:** Create/edit/execute fixture in sandbox; verify output digest and resource quota.
- **Evidence:** `docs/assets/noah-ai.js` — ensureKB, askLocal/askRemote, loadHistory/saveHistory, buildWidget (inspected; not executed in this matrix audit); `apps/practice/src/lib/muse-ask.ts` — askTutor validator/handler, remember/goal/sql/assist routes (inspected; not executed in this matrix audit)
- **Remaining limits:** Socratic code advice or SQL subset is not arbitrary execution.

### M15 — Background scheduled/event work

- **Muse:** Continues after app closure; follows events. [How We Designed Muse](https://introducing.muse.ai/). Benchmark status: `documented_current`.
- **Noah now:** Local nudges execute in page; bounded workflow work in progress.
- **Status / phase:** `pending_verification` / 3.
- **Required implementation:** Local checkpoint/resume now; later durable server scheduler and event consumers.
- **Dependencies:** Workflow store; later worker queue/time scheduler
- **Security:** Idempotent actions, cancellation, retry limits and expiry.
- **Acceptance:** Checkpoint supported local task; reload/resume once; later close app and verify server receipt.
- **Evidence:** `docs/noah/` — root-owned /noah workspace and bounded local workflow executor (Source implementation in progress; pending independent execution verification.); `docs/assets/il-muse.js` — harvestNudges invoked during page interaction (inspected; not executed in this matrix audit)
- **Remaining limits:** Device resume must be labeled accurately; no closed-browser execution claim.

### M16 — Subagent delegation and reusable tools

- **Muse:** Concurrent subagents, custom tools and crons. [How We Built Safety Into Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse). Benchmark status: `documented_current`.
- **Noah now:** No production delegation runtime verified.
- **Status / phase:** `planned` / 3.
- **Required implementation:** Register bounded role tasks; isolated tool capabilities; reviewed reusable workflows.
- **Dependencies:** Agent orchestrator; executor; budget accounting
- **Security:** Agents cannot edit policy authority; cap delegation depth and spend.
- **Acceptance:** Delegate fixture subtasks; verify permissions, parent result and budget/cancel propagation.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Role names or proposed plans are not implemented agents.

### M17 — One-time/location/recurring reminders

- **Muse:** Scheduled reminders and recurring tasks. [How to manage reminders and scheduled tasks with Muse](https://www.meta.com/help/artificial-intelligence/1484325780075655/). Benchmark status: `documented_current`.
- **Noah now:** No durable reminder scheduler located in inspected entries.
- **Status / phase:** `planned` / 3.
- **Required implementation:** Timezone-aware schedule CRUD and reliable delivery; optional location consent.
- **Dependencies:** Scheduler; notification delivery; optional geolocation
- **Security:** Explicit device/location permission; user ownership; quiet duplicates.
- **Acceptance:** Create/update/cancel DST-spanning schedule; verify due receipt and no cancelled delivery.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Location reminders require supported platform APIs and actual device checks.

### M18 — Mac local file/app operations

- **Muse:** Mac files and local apps under OS permissions. [How Muse works with files and apps in your Mac](https://www.meta.com/help/artificial-intelligence/1126304576638594/). Benchmark status: `documented_current`.
- **Noah now:** Capacitor shell exists; no macOS companion verified.
- **Status / phase:** `blocked_external_dependency` / 6.
- **Required implementation:** Optional signed Mac companion with constrained file/app bridge.
- **Dependencies:** macOS host; signed build; OS permissions
- **Security:** Per-app off/read/interact; important-write approval; Trash recovery.
- **Acceptance:** Grant read-only; reject write; authorized file delete recoverable from Trash.
- **Evidence:** `apps/mobile/README.md` — desktop later section (inspected; not executed in this matrix audit)
- **Remaining limits:** No Windows/macOS desktop-control equivalence claimed.

### M19 — Independent permission authority

- **Muse:** Sentinel controls connector/network actions externally. [How We Built Safety Into Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse). Benchmark status: `documented_current`.
- **Noah now:** Coach has local approval cards; practice restrictions in prompt.
- **Status / phase:** `planned` / 3.
- **Required implementation:** Server enforcement outside agent runtime; task/destination-bound grants.
- **Dependencies:** Policy server; typed requests; immutable approval receipts
- **Security:** Fail closed; agent cannot mint/modify its grants; network egress checks.
- **Acceptance:** Bypass UI and call tool directly; server rejects without matching valid grant.
- **Evidence:** `docs/assets/il-muse.js` — approvalHTML/showApproval/approvalCardHTML (inspected; not executed in this matrix audit); `docs/noah/` — root-owned /noah workspace and bounded local workflow executor (Source implementation in progress; pending independent execution verification.)
- **Remaining limits:** Browser-only approvals and model instructions are not independent security authority.

### M20 — Read/write access and revocation

- **Muse:** Connector/browser permissions are scoped and revocable. [How Muse works with your guidance and approval](https://www.meta.com/help/artificial-intelligence/1385290430137537/). Benchmark status: `documented_current`.
- **Noah now:** Coach approvals for local links/model changes.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Scope read/write permissions and revoke both future and queued actions.
- **Dependencies:** Policy engine; connector action metadata
- **Security:** Least privilege; inspect OAuth scopes; authorization on each invocation.
- **Acceptance:** Read grant rejects write; revoke then replay old request; deny queued execution.
- **Evidence:** `docs/assets/il-muse.js` — load/save/getChat, send generation guard, goalsPanel, settingsPanel (inspected; not executed in this matrix audit); `docs/noah/` — root-owned /noah workspace and bounded local workflow executor (Source implementation in progress; pending independent execution verification.)
- **Remaining limits:** No live connected-service authorization verified.

### M21 — Secure credential mediation

- **Muse:** Runtime receives surrogates rather than secrets. [How We Built Safety Into Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse). Benchmark status: `documented_current`.
- **Noah now:** Practice provider keys are server environment variables; browser router supports local settings.
- **Status / phase:** `planned` / 3.
- **Required implementation:** External vault/credential broker; OAuth tokens server-side; remove model visibility.
- **Dependencies:** Secret store; OAuth callbacks; egress broker
- **Security:** Exclude secrets from memory, logs, exports and public bundles.
- **Acceptance:** Fixture secret unavailable to model/runtime; authorized broker request succeeds; export clean.
- **Evidence:** `apps/practice/src/lib/harness.ts` — environment-based provider configuration (inspected; not executed in this matrix audit); `docs/assets/il-model-router.js` — getCreds/setCreds storage and request flow (inspected; not executed in this matrix audit)
- **Remaining limits:** Server env keys alone do not establish full credential surrogation.

### M22 — Activity and approval audit

- **Muse:** Chronological actions and permission history. [How Muse works with your guidance and approval](https://www.meta.com/help/artificial-intelligence/1385290430137537/). Benchmark status: `documented_current`.
- **Noah now:** Coach retains bounded local activity log.
- **Status / phase:** `pending_verification` / 3.
- **Required implementation:** Record workflow action/result/approval receipts with timestamps and status.
- **Dependencies:** Device receipt log now; append-only backend later
- **Security:** Redact sensitive fields; record denies/failures; tenant filters.
- **Acceptance:** Execute/deny/cancel fixture task; inspect persisted receipts after reload.
- **Evidence:** `docs/assets/il-muse.js` — pushActivity caps local activity at 48 entries (inspected; not executed in this matrix audit); `docs/noah/` — root-owned /noah workspace and bounded local workflow executor (Source implementation in progress; pending independent execution verification.)
- **Remaining limits:** Local logs are user-editable and not tamper-evident.

### M23 — Backup/recovery and private data controls

- **Muse:** Files inspectable/downloadable; VM continuously backed up. [How We Built Safety Into Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse). Benchmark status: `documented_current`.
- **Noah now:** No production tenant backup/recovery verified.
- **Status / phase:** `blocked_external_dependency` / 8.
- **Required implementation:** Encrypt tenant data; documented restore and retention process.
- **Dependencies:** Persistent database/object storage; backup service
- **Security:** Separate users, keys and backup restore authorization.
- **Acceptance:** Restore fixture after deletion/service failure; verify integrity and isolation.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** LocalStorage/export provides neither continuous backup nor server recovery.

### M24 — Training opt-out and data lifecycle

- **Muse:** Training control applies to prior interactions. [How to manage your Muse data](https://www.meta.com/help/artificial-intelligence/2225571704857152/). Benchmark status: `documented_current`.
- **Noah now:** Device answer mode exists; remote provider lifecycle policies unverified.
- **Status / phase:** `planned` / 3.
- **Required implementation:** Clearly report data destination/retention; apply consent to eligible provider workflows.
- **Dependencies:** Provider contracts; consent registry; deletion APIs
- **Security:** Do not promise provider deletion or training exclusion without verification.
- **Acceptance:** Change opt-out; verify consent enforcement and documented provider retention.
- **Evidence:** `docs/assets/noah-ai.js` — ensureKB, askLocal/askRemote, loadHistory/saveHistory, buildWidget (inspected; not executed in this matrix audit)
- **Remaining limits:** Local-mode wording must not imply unrelated telemetry or speech services are offline.

### M25 — Service authorization/disconnection

- **Muse:** Connect/disconnect supported services and custom APIs. [How Muse works with Connectors](https://www.meta.com/help/artificial-intelligence/1687253048996149/). Benchmark status: `documented_current`.
- **Noah now:** No generic production connector framework found in inspected entries.
- **Status / phase:** `planned` / 3.
- **Required implementation:** Typed connector registry, OAuth adapters, health and revoke operations.
- **Dependencies:** Provider applications/accounts; policy/vault
- **Security:** Minimum scopes; redirect/state validation; no secrets in client storage.
- **Acceptance:** Connect test account, read fixture, revoke, verify token unusable and no writes.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Full Muse directory is behind authentication; named source subset only.

### M26 — Email and calendar actions

- **Muse:** Authorized email/calendar operations; approval-controlled writes. [Meta consumer introduction](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/). Benchmark status: `documented_current`.
- **Noah now:** Practice explicitly cannot send email/book/browse after turn.
- **Status / phase:** `planned` / 7.
- **Required implementation:** Provider adapters; reviewed drafts, events and task receipts.
- **Dependencies:** Email/calendar APIs; OAuth; policy engine
- **Security:** Recipient/action-bound approval; replay protection.
- **Acceptance:** Draft/read fixture then approved send/create; denied/retried action never duplicates.
- **Evidence:** `apps/practice/src/lib/muse-ask.ts` — askTutor validator/handler, remember/goal/sql/assist routes (inspected; not executed in this matrix audit)
- **Remaining limits:** Drafting text is not message delivery or calendar integration.

### M27 — Meta/social device connectors

- **Muse:** Meta accounts and device-specific connector controls. [How Muse works with Connectors](https://www.meta.com/help/artificial-intelligence/1687253048996149/). Benchmark status: `documented_current`.
- **Noah now:** No connected social/device services verified.
- **Status / phase:** `blocked_external_dependency` / 7.
- **Required implementation:** Supported APIs and per-connector grants; platform-specific device bridge.
- **Dependencies:** Meta app approval; relevant device permissions
- **Security:** Account linking consent; API restrictions; no unsupported scraping.
- **Acceptance:** Use authorized test account/device; revoke; verify inaccessible data remains unavailable.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Facebook/Instagram/Threads/Apple Health/Android SMS source features vary by platform.

### M28 — Custom connector lifecycle

- **Muse:** Builds custom API/CLI connectors. [How Muse works with Connectors](https://www.meta.com/help/artificial-intelligence/1687253048996149/). Benchmark status: `documented_current`.
- **Noah now:** No deployable custom connector authoring framework inspected.
- **Status / phase:** `planned` / 7.
- **Required implementation:** Generate reviewed schemas/adapters; explicit registration and permission preview.
- **Dependencies:** Connector SDK; isolated tool runtime; API docs
- **Security:** Untrusted schemas/code; host allowlists; vault references only.
- **Acceptance:** Register sample API, inspect access, reject malicious schema/exfiltration request.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Do not automatically execute unreviewed model-generated connector code.

### M29 — Business work/project/design tools

- **Muse:** Business connectors support existing workflow tools. [Muse for Small Business](https://about.fb.com/news/2026/09/introducing-muse-small-business/). Benchmark status: `documented_current`.
- **Noah now:** No live third-party business adapters verified.
- **Status / phase:** `blocked_external_dependency` / 7.
- **Required implementation:** Adapters for named tools, beginning with authorized provider/test account.
- **Dependencies:** Asana/Box/Canva/Dropbox/Figma/Granola/HighLevel/Klaviyo/Lovable/Notion/Slack/Zoom APIs
- **Security:** Workspace-scoped OAuth; approval before send/publish; tenant access checks.
- **Acceptance:** Per-adapter read/write/revoke contract tests and approved end-to-end receipt.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Named tools are documented subset, not the complete in-app connector list.

### M30 — Storefront/accounts/payment integrations

- **Muse:** Shopify, QuickBooks and Stripe connectors. [Muse for Small Business](https://about.fb.com/news/2026/09/introducing-muse-small-business/). Benchmark status: `documented_current`.
- **Noah now:** Payment documentation exists; connected accounting/storefront actions unverified.
- **Status / phase:** `blocked_external_dependency` / 7.
- **Required implementation:** Read-only reporting first; scoped billing/accounting/store adapters.
- **Dependencies:** Provider accounts; sandbox keys; connector policy
- **Security:** No autonomous financial commitments; amounts/currency/recipient verified.
- **Acceptance:** Read sandbox ledger; reject unapproved modification; reconcile approved receipt.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Live payments and provider approval require explicit consequential-action scope.

### M31 — Business analytics and growth plans

- **Muse:** Analyze sales, campaigns and social performance. [Muse for Small Business](https://about.fb.com/news/2026/09/introducing-muse-small-business/). Benchmark status: `documented_current`.
- **Noah now:** Educational local state exists; no connected business metrics verified.
- **Status / phase:** `planned` / 7.
- **Required implementation:** Query real approved data, calculate metrics and cited growth analysis.
- **Dependencies:** Connected datasets; analytics definitions
- **Security:** No invented sales/revenue; permission-scoped exports.
- **Acceptance:** Known fixture calculations match; source timestamps and missing data visible.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Targets are not guaranteed outcomes.

### M32 — Operational triage and drafts

- **Muse:** Triage inbox/calendar; prepare response drafts. [Muse for Small Business](https://about.fb.com/news/2026/09/introducing-muse-small-business/). Benchmark status: `documented_current`.
- **Noah now:** Assistant can supply text; remote operations explicitly limited.
- **Status / phase:** `planned` / 7.
- **Required implementation:** Prioritize authorized events; drafts linked to source and approval.
- **Dependencies:** Email/calendar connectors; notification policy
- **Security:** Do not send drafts without recipient-bound consent; prompt injection isolation.
- **Acceptance:** Seed urgent/irrelevant fixtures; verify prioritization and unsent draft status.
- **Evidence:** `apps/practice/src/lib/muse-ask.ts` — askTutor validator/handler, remember/goal/sql/assist routes (inspected; not executed in this matrix audit)
- **Remaining limits:** No background inbox monitoring verified.

### M33 — Campaign/content assistance

- **Muse:** Analyze ads/trends; draft next campaign. [Muse for Small Business](https://about.fb.com/news/2026/09/introducing-muse-small-business/). Benchmark status: `documented_current`.
- **Noah now:** No live advertising connector verified.
- **Status / phase:** `planned` / 7.
- **Required implementation:** Authorized performance read, trend research and draft creative pipeline.
- **Dependencies:** Ad analytics API; research/media services
- **Security:** Publication/budget approval; original content rights.
- **Acceptance:** Fixture analysis plus sourced trend draft; no publish/spend without grant.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Creative draft is not published campaign.

### M34 — Financial anomaly reporting

- **Muse:** Review monthly performance and unusual expenses. [Muse for Small Business](https://about.fb.com/news/2026/09/introducing-muse-small-business/). Benchmark status: `documented_current`.
- **Noah now:** No connected financial data verified.
- **Status / phase:** `planned` / 7.
- **Required implementation:** Read accounting data, deterministic calculations and drill-down anomalies.
- **Dependencies:** Accounting API; reporting schema
- **Security:** Financial data isolation; no invented anomalies or ledger writes.
- **Acceptance:** Known ledger totals match and flagged entries show evidence/uncertainty.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Accounting advice and filings require separate authorized scope.

### M35 — Approved purchases and booking

- **Muse:** Browser purchases and bookings under approval. [How Muse works with payments](https://www.meta.com/help/artificial-intelligence/1436362127544482/). Benchmark status: `documented_current`.
- **Noah now:** Link opening/drafts only in inspected Noah surfaces.
- **Status / phase:** `blocked_external_dependency` / 7.
- **Required implementation:** Structured merchant intent, human review and purchase receipt reconciliation.
- **Dependencies:** Browser executor; merchant/payment provider
- **Security:** Approve exact price/currency/item; idempotency; no real-card exposure.
- **Acceptance:** Sandbox purchase requires approval; retry never creates duplicate order.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Purchase protection belongs to provider eligibility, not a Noah promise.

### M36 — Link one-time card checkout

- **Muse:** Link issues protected one-time purchase cards. [How Muse works with payments](https://www.meta.com/help/artificial-intelligence/1436362127544482/). Benchmark status: `documented_current`.
- **Noah now:** No Link agent-wallet integration verified.
- **Status / phase:** `blocked_external_dependency` / 7.
- **Required implementation:** Use supported approved provider API if available; evaluate alternative independently.
- **Dependencies:** Stripe/Link partnership or supported wallet API
- **Security:** Provider handles card data; PCI boundary reviewed.
- **Acceptance:** Sandbox token/cards remain concealed; receipt shows actual provider result.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Muse-specific Link benefits do not transfer to Noah automatically.

### M37 — Document/spreadsheet/source workflows

- **Muse:** Reads, creates and edits supported artifacts. [How to use Muse with artifacts](https://www.meta.com/help/artificial-intelligence/2074655449783957/). Benchmark status: `documented_current`.
- **Noah now:** Coach provides fixed artifact cards/checklists/links; no full document pipeline verified.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Uploads plus format-aware read/edit/export with retained editable sources.
- **Dependencies:** File parsers; isolated converters; object storage
- **Security:** MIME/signature validation, quotas, malware isolation, path traversal prevention.
- **Acceptance:** Edit real PDF/DOCX/XLSX/CSV fixtures and reopen outputs; reject hostile upload.
- **Evidence:** `docs/assets/il-muse.js` — makeArtifact/artifactHTML/libraryPanel (inspected; not executed in this matrix audit)
- **Remaining limits:** Source links/checklists do not equal document editing.

### M38 — Interactive web artifacts

- **Muse:** Creates interactive browser tools and visualizations. [How to use Muse with artifacts](https://www.meta.com/help/artificial-intelligence/2074655449783957/). Benchmark status: `documented_current`.
- **Noah now:** Coach displays authored interactive checklists and path cards.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Save original interactive artifacts with sandboxed previews and source.
- **Dependencies:** Artifact service; preview origin/CSP
- **Security:** Isolate generated scripts from credentials and app origin.
- **Acceptance:** Create tool fixture; reopen/export source; sandbox blocks app-storage access.
- **Evidence:** `docs/assets/il-muse.js` — load/save/getChat, send generation guard, goalsPanel, settingsPanel (inspected; not executed in this matrix audit)
- **Remaining limits:** User-authored generated web apps not verified.

### M39 — Image generation/editing

- **Muse:** Generates images and applies requested adjustments. [How to use Muse with artifacts](https://www.meta.com/help/artificial-intelligence/2074655449783957/). Benchmark status: `documented_current`.
- **Noah now:** Existing Noah raster/SVG/GLB assets are present.
- **Status / phase:** `blocked_external_dependency` / 4.
- **Required implementation:** Integrate authorized image service; edit validation and provenance.
- **Dependencies:** Image model provider; storage; quota accounting
- **Security:** Rights/consent controls; no silent paid generation; untrusted-image handling.
- **Acceptance:** Generate/edit fixture through actual API; inspect downloaded dimensions/result.
- **Evidence:** `docs/assets/noah-avatar.png` — asset presence only (inspected; not executed in this matrix audit)
- **Remaining limits:** Existing assets do not establish a production generation tool.

### M40 — Audio/podcast production

- **Muse:** Audio generation can produce researched podcasts. [How Muse works with skills](https://www.meta.com/help/artificial-intelligence/2797651547267109/). Benchmark status: `documented_current`.
- **Noah now:** Browser speech exists; practice has environment-gated TTS endpoint.
- **Status / phase:** `inspected_partial` / 4.
- **Required implementation:** Narration/podcast workflow with scripts, audio export and quality checks.
- **Dependencies:** Audio model; media processing; storage
- **Security:** Authorized voices; no cloning without consent; report service data transfer.
- **Acceptance:** Generate/play/export fixture podcast; confirm length, content and source evidence.
- **Evidence:** `apps/practice/src/lib/muse-ask.ts` — speakTutor (inspected; not executed in this matrix audit); `docs/assets/il-muse.js` — voiceSupport/speakText (inspected; not executed in this matrix audit)
- **Remaining limits:** TTS reading a chat reply does not equal researched podcast production.

### M41 — Research/digests

- **Muse:** Research and recurring digest skills. [How Muse works with skills](https://www.meta.com/help/artificial-intelligence/2797651547267109/). Benchmark status: `documented_current`.
- **Noah now:** Local knowledge bundle returns curriculum links; general live research not verified.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Approved retrieval/search, source dates and recurring digest execution.
- **Dependencies:** Search connector; fetch service; scheduler
- **Security:** Treat retrieved content as untrusted; avoid private-network fetches.
- **Acceptance:** Fixture research cites matching primary pages; scheduled digest has receipt.
- **Evidence:** `docs/assets/noah-ai.js` — ensureKB, askLocal/askRemote, loadHistory/saveHistory, buildWidget (inspected; not executed in this matrix audit)
- **Remaining limits:** Keyword curriculum lookup is not open-web research.

### M42 — Artifact library/private sharing

- **Muse:** Library persists outputs; sharing needs approval. [How to use Muse with artifacts](https://www.meta.com/help/artificial-intelligence/2074655449783957/). Benchmark status: `documented_current`.
- **Noah now:** Coach artifacts persist with local state.
- **Status / phase:** `inspected_partial` / 3.
- **Required implementation:** Unified library CRUD/export; server storage and explicit sharing grants.
- **Dependencies:** Device store now; identity/object storage later
- **Security:** Private by default; signed shares; owner authorization; revocation.
- **Acceptance:** Create/reload/delete fixture; unapproved external viewer cannot read artifact.
- **Evidence:** `docs/assets/il-muse.js` — load/save/getChat, send generation guard, goalsPanel, settingsPanel (inspected; not executed in this matrix audit)
- **Remaining limits:** Public static assets and browser-local cards are not tenant-private cloud library.

### M43 — iOS/Android/web/WhatsApp access

- **Muse:** Agent available through mobile, web and WhatsApp. [Meta consumer introduction](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/). Benchmark status: `documented_current`.
- **Noah now:** Capacitor, PWA and responsive site files exist.
- **Status / phase:** `inspected_partial` / 6.
- **Required implementation:** Preserve shell; unify Noah context and authenticated data; optional supported messaging adapter.
- **Dependencies:** Android/iOS toolchains; device tests; WhatsApp approved API
- **Security:** Secure auth/storage; user-controlled cross-device sync; message permissions.
- **Acceptance:** Build/open actual devices; reload task; verify authorized sync and logout boundaries.
- **Evidence:** `apps/mobile/package.json` — Capacitor dependencies (inspected; not executed in this matrix audit); `apps/mobile/README.md` — build and smoke-test instructions (inspected; not executed in this matrix audit)
- **Remaining limits:** No current build/device/store or messaging execution verified here.

### M44 — Voice plus background conversations

- **Muse:** Voice conversation while agent works concurrently. [The Biggest News From Connect 2026](https://about.fb.com/news/2026/09/the-biggest-news-from-connect-2026/). Benchmark status: `documented_current`.
- **Noah now:** Coach Web Speech recognition/synthesis; optional server TTS.
- **Status / phase:** `inspected_partial` / 6.
- **Required implementation:** Accessible voice path; audio interruption and work concurrency; robust text fallback.
- **Dependencies:** Supported browser microphone/TTS; optional STT/realtime API
- **Security:** Explicit mic permission; disclose remote processing; no recording retention default.
- **Acceptance:** Speak/cancel/revoke mic on supported devices; text remains usable on unsupported devices.
- **Evidence:** `docs/assets/il-muse.js` — SpeechRecognition/webkitSpeechRecognition/speechSynthesis (inspected; not executed in this matrix audit)
- **Remaining limits:** Announced voice behavior is documented; per-account rollout not operated.

### M45 — Connector submission and review

- **Muse:** Directory publication follows review and tests. [Muse Connector Platform](https://muse.ai/platform). Benchmark status: `documented_current`.
- **Noah now:** No public connector registry/review pipeline verified.
- **Status / phase:** `planned` / 7.
- **Required implementation:** Reviewed adapter registry and developer submission process when product scale warrants.
- **Dependencies:** Connector SDK; security review; CI contract suite
- **Security:** Reject overbroad access; provenance and signed versions.
- **Acceptance:** Sample adapter passes functional/security/permission contract gates before listing.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Muse partner-directory availability is not Noah integration entitlement.

### M46 — Usage and subscription controls

- **Muse:** Free allowance and region-dependent paid plans. [About Muse subscriptions](https://www.meta.com/help/subscriptions/1021145227643680/). Benchmark status: `documented_current`.
- **Noah now:** No verified Noah agent-cost/subscription metering in inspected entry points.
- **Status / phase:** `planned` / 7.
- **Required implementation:** Track real usage/cost, budget caps and clear billing eligibility.
- **Dependencies:** Provider metering; account system; billing if authorized
- **Security:** Never invent token counts/revenue; spending authorization and emergency stop.
- **Acceptance:** Fixed fixture usage reconciles to provider receipt; cap halts additional spend.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** No payment setup or subscription purchase authorized by this matrix.

## Announced capabilities and uncertain rollouts

Keep these separately visible. A launch announcement can establish a requirement without establishing current access.

### A01 — Confidential VM

- **Muse:** User-key confidential VM announced for later year. [Meta consumer introduction](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/). Benchmark status: `announced_future`.
- **Noah now:** No confidential execution environment verified.
- **Status / phase:** `blocked_external_dependency` / 8.
- **Required implementation:** Assess confidential compute and key/attestation architecture separately.
- **Dependencies:** Confidential-compute provider; audit; key recovery
- **Security:** Do not claim operator-blind encryption without external attestation.
- **Acceptance:** Validate attestation and no-operator data access under reviewed threat model.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Forthcoming benchmark feature; not current parity completion criterion until launch verified.

### A02 — 1Password integration

- **Muse:** 1Password support announced as coming soon. [Meta consumer introduction](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/). Benchmark status: `announced_future`.
- **Noah now:** No password-manager integration verified.
- **Status / phase:** `blocked_external_dependency` / 7.
- **Required implementation:** Use supported password-manager broker with independently reviewed scope.
- **Dependencies:** Provider SDK/partnership; credential broker
- **Security:** No credential disclosure to model/browser storage.
- **Acceptance:** Authorized sandbox login without actual password visible to runtime.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Availability must be rechecked; announced feature.

### A03 — Shop Pay/PayPal/new retailers

- **Muse:** Additional payment/shopping connectors are being added. [The Biggest News From Connect 2026](https://about.fb.com/news/2026/09/the-biggest-news-from-connect-2026/). Benchmark status: `announced_rollout_unverified`.
- **Noah now:** No equivalent integrations verified.
- **Status / phase:** `blocked_external_dependency` / 7.
- **Required implementation:** Verify each provider's current supported agent API before implementation.
- **Dependencies:** Provider approvals; merchant/payment sandbox
- **Security:** Purchase-specific consent; provider token handling.
- **Acceptance:** Per-provider authenticated fixture and denied/approved purchase receipts.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Announcement alone does not verify account rollout or Noah API access.

### A04 — Expedia travel integration

- **Muse:** Expedia connector announced as coming soon. [The Biggest News From Connect 2026](https://about.fb.com/news/2026/09/the-biggest-news-from-connect-2026/). Benchmark status: `announced_future`.
- **Noah now:** No travel connector verified.
- **Status / phase:** `blocked_external_dependency` / 7.
- **Required implementation:** Supported travel search/booking adapter if commercially accessible.
- **Dependencies:** Travel API agreement; booking sandbox
- **Security:** Explicit dates/price/cancellation approval before booking.
- **Acceptance:** Search fixture then reviewed booking with reconciled receipt.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** Announced future feature.

### A05 — Agent-owned email address

- **Muse:** Agent email address announced for future availability. [The Biggest News From Connect 2026](https://about.fb.com/news/2026/09/the-biggest-news-from-connect-2026/). Benchmark status: `announced_future`.
- **Noah now:** No resident-agent mailbox verified.
- **Status / phase:** `planned` / 7.
- **Required implementation:** Scoped inbound mailbox and approved outbound delivery.
- **Dependencies:** Email provider; domain/DNS authorization; spam handling
- **Security:** Separate user mail; authenticated inbound handling; sending approvals.
- **Acceptance:** Inbound fixture becomes task; external send blocked until exact recipient grant.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** No DNS/mail modifications are implied by planning.

### A06 — AI glasses and Muse Charm

- **Muse:** Glasses/Charm access announced for coming months. [The Biggest News From Connect 2026](https://about.fb.com/news/2026/09/the-biggest-news-from-connect-2026/). Benchmark status: `announced_future`.
- **Noah now:** No wearable device integration verified.
- **Status / phase:** `blocked_external_dependency` / 6.
- **Required implementation:** Evaluate supported device interfaces only when accessible.
- **Dependencies:** Wearable hardware/SDK; platform accounts
- **Security:** Capture permission, bystander privacy, minimum data retention.
- **Acceptance:** Actual device task/session tests with visible capture/access controls.
- **Evidence:** No equivalent located in inspected Noah entry points; not proof absent elsewhere.
- **Remaining limits:** No claim of device availability or verified wearable parity.

## Additional Project Noah requirements

These are explicit project requirements. They are not invented Muse capabilities; directive section numbers refer to the supplied Project Noah brief.

### N01 — Unified resident context

- **Directive / phase / status:** sections 2, 5; phase 2; `partial_inspection`.
- **Noah now:** Separate widget/coach/practice/university surfaces and stores.
- **Required / dependencies:** One authorized identity/conversation/context contract across presentation modes. Shared schemas and later identity/database.
- **Security:** Never import other users or privileged admin context.
- **Acceptance:** Open a lesson and each resident mode; verify actual objective/code/result context.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. Same branding is not product integration.

### N02 — Adaptive instruction

- **Directive / phase / status:** sections 5, 12; phase 5; `partial_inspection`.
- **Noah now:** Socratic guides, curriculum bundle and coach weak-topic nudges inspected.
- **Required / dependencies:** Mastery/prerequisite/remediation flow using actual lab results. Canonical learning schema and objective validation.
- **Security:** Learner ownership; no fabricated mastery/progress.
- **Acceptance:** Known correct/incorrect work changes appropriate instruction.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. No complete curriculum or educational-outcome claim.

### N03 — Interactive original 3D Noah

- **Directive / phase / status:** sections 8; phase 4; `pending_verification`.
- **Noah now:** Canvas avatar and GLBs present; neural projection implementation in progress.
- **Required / dependencies:** Actual depth geometry, activity-linked animation and static/text/reduced-motion fallback. Renderer and real activity/voice events.
- **Security:** Expose status only; pause hidden motion.
- **Acceptance:** Inspect depth and state changes; verify text/keyboard/motion fallback.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. Projected 3D is not Unreal photorealism or a .blend master.

### N04 — Editable brand masters

- **Directive / phase / status:** sections 7, 8; phase 4; `partial_inspection`.
- **Noah now:** Sigil SVG/raster, GLBs and Blender-polish scripts present.
- **Required / dependencies:** Verify provenance; editable vector and .blend master; variants/icons/reveal. Blender/vector tools and license ledger.
- **Security:** Original/authorized assets only.
- **Acceptance:** Reopen masters; render and inspect transparency/dimensions/icons.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. Asset names are not licenses or validated .blend deliverables.

### N05 — 20-second neural cinematic

- **Directive / phase / status:** sections 9; phase 4; `partial_inspection`.
- **Noah now:** hero-cinematic-loop.mp4 and poster present, metadata unverified.
- **Required / dependencies:** Inspect current media; original loop and requested aspect/color/codec derivatives. Editable scenes, encoder/render resources and rights evidence.
- **Security:** No copied film/protection bypass.
- **Acceptance:** Measure 20 seconds/seam, composition, HDR/SDR, codecs and fallback.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. No duration/HDR/8K/commercial license verification.

### N06 — 5120 x 1440 workspace

- **Directive / phase / status:** sections 10; phase 4; `pending_verification`.
- **Noah now:** Root-owned responsive workspace implementation in progress.
- **Required / dependencies:** Reading widths, navigation/work/assistant panels and accessible collapse/resize. Responsive CSS, panel persistence, native-resolution viewport.
- **Security:** Keep approvals visible and keyboard accessible.
- **Acceptance:** Test 5120x1440 plus mobile/tablet/zoom without overflow.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. Primary design target is not hardware/HDR verification.

### N07 — Adaptive media/graphics

- **Directive / phase / status:** sections 8, 9; phase 4; `planned`.
- **Noah now:** Immersive GLBs and media files present.
- **Required / dependencies:** Measured LOD/textures/codecs and static fallback by capability. Asset pipeline and supported GPU/browser APIs.
- **Security:** No forced highest-resolution payload.
- **Acceptance:** Low-capability fixture gets small variant; pause/motion controls work.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. NVIDIA-level performance is a target.

### N08 — Creative 3D/video tooling

- **Directive / phase / status:** sections 8; phase 4; `blocked_external_dependency`.
- **Noah now:** Existing assets and TTS do not establish creative tools.
- **Required / dependencies:** Authorized image/video/editable geometry/scene/material workflows. Models, render hardware, storage and budgets.
- **Security:** Paid-action scope, provenance and safe generated files.
- **Acceptance:** Generate genuine editable 3D, reopen source and inspect render.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. Flat images do not satisfy 3D generation.

### N09 — Curriculum/certification completeness

- **Directive / phase / status:** sections 12; phase 5; `partial_inspection`.
- **Noah now:** Static university catalog/adaptive contract and curriculum files inspected.
- **Required / dependencies:** Canonical prerequisites/objectives/lessons/labs/remediation/assessments/capstones. Curriculum audit and official certification updates.
- **Security:** Original materials; no unsupported affiliations/certification claims.
- **Acceptance:** Independently sample pathway sources, answers, labs and outcomes.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. Catalog counts do not establish quality.

### N10 — Founder command center

- **Directive / phase / status:** sections 13; phase 7; `blocked_external_dependency`.
- **Noah now:** Connected founder/operations metrics unverified.
- **Required / dependencies:** Authenticated drill-downs for health/users/tasks/support/deployments/cost and connected revenue. Identity, metrics, connector and operations data.
- **Security:** Admin separation and emergency stop.
- **Acceptance:** Fixture values reconcile; unauthorized access denied; stop halts workers.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. No invented revenue/learner/cost metrics.

### N11 — Development-agent organization

- **Directive / phase / status:** sections 6; phase 7; `planned`.
- **Noah now:** No continuously operating production agent organization verified.
- **Required / dependencies:** Distinct role permissions and observe-to-measure release gates. Source control, CI, isolated agents and rollback.
- **Security:** Agents cannot edit own authorization.
- **Acceptance:** Low-risk fixture passes gates; high-risk pauses; rollback works.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. This coding session is not an installed Noah capability.

### N12 — Public/private infrastructure

- **Directive / phase / status:** sections 14; phase 1; `unverified`.
- **Noah now:** Matrix inspected public source only.
- **Required / dependencies:** Inventory auth/data boundaries; preserve private/family services. Authorized infrastructure access and inventory.
- **Security:** No host storage/RAID/OS or RHEL-direction change; no private secrets.
- **Acceptance:** Bundle/exposure/access checks; unrelated resources preserved.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. No host migration is in scope.

### N13 — Measured quality/security

- **Directive / phase / status:** sections 14, 15, 17; phase 8; `planned`.
- **Noah now:** No new runtime test result claimed here.
- **Required / dependencies:** Reproducible permission/injection/isolation/accessibility/performance/load/recovery tests. Defined profiles, browser/device tools and representative data.
- **Security:** Negative authorization and exfiltration tests.
- **Acceptance:** Record actual measurements and compare specified targets.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. Lab scores do not prove field p75.

### N14 — Release and rollback ledger

- **Directive / phase / status:** sections 3, 16, 17; phase 8; `pending_verification`.
- **Noah now:** Root owns baseline/deployment/release/recovery evidence.
- **Required / dependencies:** Record branch/SHA/assets/migrations/smoke checks/recovery. Repository and Cloudflare permissions; protected release pipeline.
- **Security:** Protect secrets/unrelated DNS/services; no undeclared migration.
- **Acceptance:** Verify deployed behavior and recovery instructions.
- **Evidence / limits:** See repository reconciliation; no independent execution claimed. Local files/JSON/dry runs are not successful deployment.

## Compatibility and dependency implications

| Target | Required verification | Status |
| --- | --- | --- |
| Desktop | Chrome/Edge/Firefox/Safari; keyboard/text/reduced-motion fallback. | Unverified in this audit |
| Ultrawide | 5120x1440 primary and relevant browser zoom; media profiles composed separately. | Unverified in this audit |
| PWA/mobile web | Safe areas, capability-detected speech, text and storage-unavailable fallback. | Unverified in this audit |
| iOS/iPadOS | macOS/Xcode/signing/account and actual-device tests. | Unverified in this audit |
| Android | JDK/SDK/signing and actual-device tests. | Unverified in this audit |
| Voice | Explicit mic permission; supported STT/TTS; disclose remote processing. | Unverified in this audit |
| TV/wearables | Supported platform SDK/hardware; simplified navigation and real-device checks. | Unverified in this audit |

- Provider/API eligibility, isolated compute, server identity/database, credentials, render resources, native signing and real-device access remain external dependencies until verified.
- Server authorization must not trust browser-local approvals or saved workflow ledgers.
- Do not publish private records, tokens, credentials or account exports in this matrix.

Performance targets remain Lighthouse Performance ≥90, Accessibility ≥95, field p75 LCP ≤2.5 seconds, CLS ≤0.1 and INP ≤200 ms under a declared measurement profile. No invented measurements or guaranteed results are recorded.

## Sources checked

Exact dates are retained where supplied. Relative Help Center update labels are retained as relative labels; they are not converted into invented publication dates.

| ID | Primary source | Publication / update shown |
| --- | --- | --- |
| consumer | [Meta consumer introduction](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | 2026-09-08 / 2026-09-30; read 2026-10-01 |
| business | [Muse for Small Business](https://about.fb.com/news/2026/09/introducing-muse-small-business/) | 2026-09-29; read 2026-10-01 |
| design | [How We Designed Muse](https://introducing.muse.ai/) | 2026-09; read 2026-10-01 |
| security | [How We Built Safety Into Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse) | 2026-09-08; read 2026-10-01 |
| connectors | [How Muse works with Connectors](https://www.meta.com/help/artificial-intelligence/1687253048996149/) | Not stated / relative: three weeks ago; read 2026-10-01 |
| approvals | [How Muse works with your guidance and approval](https://www.meta.com/help/artificial-intelligence/1385290430137537/) | Not stated / relative: three weeks ago; read 2026-10-01 |
| browser | [How your Muse agent browses the web](https://www.meta.com/en-gb/help/artificial-intelligence/2124746764949121/) | Not stated / relative: two weeks ago; read 2026-10-01 |
| skills | [How Muse works with skills](https://www.meta.com/help/artificial-intelligence/2797651547267109/) | Not stated / relative: three weeks ago; read 2026-10-01 |
| artifacts | [How to use Muse with artifacts](https://www.meta.com/help/artificial-intelligence/2074655449783957/) | Not stated / relative: three weeks ago; read 2026-10-01 |
| data | [How to manage your Muse data](https://www.meta.com/help/artificial-intelligence/2225571704857152/) | Not stated / relative: three weeks ago; read 2026-10-01 |
| personality | [How to customize Muse's personality and memories](https://www.meta.com/help/artificial-intelligence/995796179982326/) | Not stated / relative: one day ago; read 2026-10-01 |
| schedules | [How to manage reminders and scheduled tasks with Muse](https://www.meta.com/help/artificial-intelligence/1484325780075655/) | Not stated / relative: three weeks ago; read 2026-10-01 |
| mac | [How Muse works with files and apps in your Mac](https://www.meta.com/help/artificial-intelligence/1126304576638594/) | Not stated / relative: one week ago; read 2026-10-01 |
| payments | [How Muse works with payments](https://www.meta.com/help/artificial-intelligence/1436362127544482/) | Not stated / relative: one week ago; read 2026-10-01 |
| platform | [Muse Connector Platform](https://muse.ai/platform) | Not stated; read 2026-10-01 |
| subscriptions | [About Muse subscriptions](https://www.meta.com/help/subscriptions/1021145227643680/) | Not stated / relative: three weeks ago; read 2026-10-01 |
| connect2026 | [The Biggest News From Connect 2026](https://about.fb.com/news/2026/09/the-biggest-news-from-connect-2026/) | 2026-09-24; read 2026-10-01 |
| help | [Muse Help Center](https://www.meta.com/help/artificial-intelligence/1303670544995562/) | Not stated; read 2026-10-01 |
| academy | [The Horowitz Andreessen Academy](https://theacademysf.com/) | Not stated; read 2026-10-01 |

Academy content was inspected for hierarchy, application CTA, program/calendar sequencing, student/project narratives and faculty/partner information. No reference artwork, code or branded assets were copied.

## Maintenance and promotion

1. Re-read primary sources when features change; record check date and availability uncertainty.
2. Add newly documented features without deleting historical gaps or confusing model releases with agent features.
3. Attach actual acceptance-test receipts and deployed evidence before promoting Noah status.
4. Record partial satisfaction explicitly. Local checkpoint resume does not close remote execution, independent permission authority, connected accounts or closed-browser scheduling requirements.
5. Preserve user data and functioning surfaces; review source/data migrations and rollback before release.

