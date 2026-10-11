# Noah Connectors — Architecture & Backend Contract

## Overview

`noah-connectors.js` is the frontend framework. Connectors are pluggable
modules: each declares actions, natural-language patterns, and reversibility.
Noah routes user requests to connectors, executes via backend, renders
results conversationally, and chains actions with confirmation gates.

## Frontend (`/assets/noah-connectors.js`)

- `NoahConnectors.register(def)` — add a connector
- `NoahConnectors.handle(text, hostEl)` — route + execute; returns bool
- `NoahConnectors.list()` — registered connector summaries
- `NoahConnectors.chain(steps, hostEl)` — autonomous multi-step execution
- Irreversible actions (`reversible:false`) show a Confirm/Cancel gate.
- Chains show progress + a Cancel button.

## Backend contract (to implement in `_worker.js`)

```
POST /api/noah/connectors/:id
Content-Type: application/json
{ "action": "<action-id>", "params": { ... }, "confirm_token": "<optional>" }

-> 200 { "ok": true, "summary": "<conversational HTML-safe summary>",
         "data": { ... }, "chain": [ {connector, action, params} ]? }
-> 200 { "ok": true, "needs_confirm": true, "confirm_token": "<token>",
         "summary": "About to <action>…" }
-> 200 { "ok": false, "error": "<message>", "setup_url": "<oauth-url>"? }
```

Security rules:
- Never expose tokens/keys in responses.
- `confirm_token`: single-use, short TTL, bound to the exact action+params.
- Log every irreversible action server-side.
- OAuth: Google (Gmail + Calendar) via one consent screen; GitHub via
  GitHub App or PAT stored in Secrets (never in code).

## Connector: gmail

| action  | params         | reversible | notes                          |
|---------|----------------|------------|--------------------------------|
| search  | query          | yes        | Gmail API messages.list        |
| read    | query          | yes        | first matching thread, snippet |
| draft   | to, subject    | yes        | returns draft id               |
| send    | to, subject    | **no**     | requires confirm gate          |

NL: "search my mail for …", "find the email about …", "draft an email to …",
"send an email to …".

## Connector: gcal

| action   | params       | reversible | notes                        |
|----------|--------------|------------|------------------------------|
| freebusy | when         | yes        | parse natural dates          |
| schedule | title, when  | **no**     | requires confirm gate        |
| list     | —            | yes        | next 7 days                  |

NL: "am I free …", "check my calendar", "schedule … on …", "what's next".

## Connector: github

| action  | params           | reversible | notes                      |
|---------|------------------|------------|----------------------------|
| status  | repo             | yes        | default branch, open PRs   |
| prs     | repo?            | yes        | open PRs                   |
| issues  | repo?            | yes        | open issues                |
| trigger | workflow, repo   | **no**     | workflow_dispatch, confirm |

NL: "status of …", "list PRs", "list issues", "trigger workflow …".

## Adding a connector

1. Frontend: `NoahConnectors.register({...})` in `noah-connectors.js`
   (or a separate file loaded after it).
2. Backend: add the `:id` case to the `/api/noah/connectors/` route.
3. Document the action table above.

## Suggested next connectors

LinkedIn (read-only insights), Cloudflare (deploy status via API token),
job boards (search via existing tracker), X/Instagram/Threads (post +
analytics), Spotify (playback), weather/news (info), Drive (files).
