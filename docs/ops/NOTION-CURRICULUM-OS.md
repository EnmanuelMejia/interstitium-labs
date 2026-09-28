# Notion ↔ Curriculum OS

_Last updated: 2026-09-28 ~09:20 EDT (America/New_York)._  
_Live parent:_ [Interstitium Curriculum OS](https://www.notion.so/3e38c2a0d36181678bd6f90d8b78414b)

## Product law

**Notion = Curriculum OS SoT.**  
**Runtime = Interstitium** `/learn` `/labs` `/prep` `/paths` with **`immersive: 3d-first`**.

3D stays **Unreal / Blender / Godot / glTF + Lab Muse stage**.  
**Do not** treat Notion embeds as the 3D runtime.

## Live databases (shipped this pass)

| DB | Notion URL | Data source |
|----|------------|-------------|
| Tracks | https://www.notion.so/959f61a948154ee89731c17227d655d8 | `59526a3e-bb94-4f35-922d-272dba3b7790` |
| Lectures | https://www.notion.so/116e10860ffa47d4807b734f36f1fbdd | `748aa46f-e459-4b7d-996b-014648d670f4` |
| Labs | https://www.notion.so/e625a98ff9c34d2ebfb1f57ef4b1fbd1 | `4963e02e-ebd7-4291-8852-6ae187c36131` |
| Certs | https://www.notion.so/5d2b3980fa994150a6f5fd90ccb05f05 | `c5f740f2-06eb-402d-a2f8-414de346683d` |
| Assets3D | https://www.notion.so/bd2a2ae85e6c4c30a58349a0a00b9ac8 | `41c8653d-36fa-42b5-97f2-9ea032d27ba7` |

IDs also live in `docs/curriculum-os/notion-ids.json`.

## Shared enums

| Field | Values |
|-------|--------|
| PublishStatus | `draft` · `review` · `published` · `archived` |
| Lang | `EN` · `ES` |
| ImmersiveMode | `3d-first` (only) |
| ImmersiveEngine | `three` · `godot` · `unreal` · `webgpu` |

## Connect steps (MCP / agents)

1. Cursor MCP server **`user-Notion-xai`** must show `serverStatus: ready` (`notion-get-tool-access`).
2. If `needsAuth`: authenticate Notion in Cursor desktop IDE, then retry.
3. Prefer **query / fetch** against data-source IDs above; write via `notion-create-pages` / `notion-update-page`.
4. After Notion edits: refresh local mirror under `docs/curriculum-os/` (or run agent sync) so `il-curriculum-sync.js` stamps surfaces.
5. Never point a student page at a Notion embed for the 3D stage — stamp `data-il-immersive` + `data-il-scene` / `data-gltf` instead.

## Local mirror (always ship)

| Path | Role |
|------|------|
| `docs/curriculum-os/mirror.json` | Full SoT for browser sync |
| `docs/curriculum-os/schema.json` | Contract |
| `docs/assets/il-curriculum-sync.js` | Reads mirror (optional Notion later); stamps 3d-first hooks |

Offline / auth-fail path: file mirror alone is enough to ship; reconnect Notion later without schema drift.

## Surface stamp targets

| Surface | Default scene | Player |
|---------|---------------|--------|
| `/learn/` | `k8s` / lecture glTF | `il-immersive-3d` + sync |
| `/labs/` | `k8s` / cert shell | same + `data-kind=cert` |
| `/prep/` | `rack` | same |
| `/paths/` | track immersive asset | same |

Companion: `IMMERSIVE-3D-CURRICULUM.md` · `LAB-MUSE-3D.md` · `ANTI-MEDIOCRITY-ELON-GATE.md`
