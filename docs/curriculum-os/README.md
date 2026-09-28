<!-- refreshed 2026-09-28 -->
# Curriculum OS — local mirror (Notion-shaped SoT)

_Last updated: 2026-09-22 ~00:46 EDT (America/New_York)._

**Notion** is the curriculum OS source of truth. This folder is the **file-based mirror** that ships with the static site so `/learn` `/labs` `/prep` `/paths` stay 3d-first even when Notion MCP is offline.

## Law

| Role | System |
|------|--------|
| SoT / authoring | Notion Curriculum OS databases |
| Runtime delivery | Interstitium immersive player (WebGL / WebGPU / glTF / Unreal PS) |
| Coach familiar | Lab Muse (`il-muse-3d`) — **not** a Notion embed |

**Never** use Notion embeds as the 3D runtime.

## Databases (concepts)

| DB | Purpose |
|----|---------|
| Tracks | Outcome spines → surfaces |
| Lectures | 3d-first lecture stages (glTF preferred) |
| Labs | cert / sim / non-cert / challenge |
| Certs | Vendor exams + **3D lab shell** |
| Assets3D | Blender/Godot/Unreal/procedural registry |

Shared: `PublishStatus` (`draft|review|published|archived`), `Lang` (`EN|ES`), `immersive.mode=3d-first`.

## Files

| File | Role |
|------|------|
| `mirror.json` | Full SoT dump for `il-curriculum-sync.js` |
| `schema.json` | Shape contract |
| `notion-ids.json` | Live Notion page/database/data-source IDs |
| `tracks.json` … `assets3d.json` | Per-collection slices |

## Sync

```js
// stamped by docs/assets/il-curriculum-sync.js
data-immersive='{"mode":"3d-first","engine":"three|webgpu","asset":"procedural:*|/assets/immersive/*.glb","webgpu":true}'
```

Ops: [`../ops/NOTION-CURRICULUM-OS.md`](../ops/NOTION-CURRICULUM-OS.md) · Gate: [`../ops/ANTI-MEDIOCRITY-ELON-GATE.md`](../ops/ANTI-MEDIOCRITY-ELON-GATE.md)
