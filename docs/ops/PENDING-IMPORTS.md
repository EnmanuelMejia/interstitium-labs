# Pending imports

Tracked ChatGPT shares that have not yet landed under `docs/_imports/`. ComputerUse extraction may still be in flight. When a matching file appears, fold **unique** content into the site and remove or strike the row below.

| Share ID | Expected import path | Title hint | Destination (when available) | Status |
|----------|----------------------|------------|------------------------------|--------|
| `6ab1eabe-1f24-83ea-8f55-212e35a45529` | `docs/_imports/chatgpt-6ab1eabe*.md` (+ meta) | Create FDE Training Webapp | Unique bits → `docs/paths/fde-training/` (do **not** clone BNY Prep, DevSecOps Mastery, NVIDIA AI, Magic Leap, or DS certs) | **Pending** — share fetch timed out; no import file as of 2026-09-21 ~22:43 EDT |
| `6ab1eb2c-8158-83ea-baed-16b51daa823b` | `docs/_imports/chatgpt-6ab1eb2c-8158-83ea-baed-16b51daa823b.md` (+ meta) | (second ChatGPT share; extract title from import) | Dedupe against prep/paths/NVIDIA/BNY/Magic Leap; place only unique residual under `docs/paths/fde-training/` or a short ops note | **Pending** — no import file as of 2026-09-21 ~22:43 EDT |

## Operator checklist when an import appears

1. Confirm file name matches the expected pattern under `docs/_imports/`.
2. Skim for overlap with `/prep/`, `/paths/devsecops-mastery/`, `/paths/nvidia-ai/`, `/prep/drills/*`.
3. Copy only non-duplicative outlines, UI IA, or FDE-specific modules into `docs/paths/fde-training/`.
4. Update this table to **Imported** and link the commit.
5. Redeploy Cloudflare Workers Assets if HTML changed.

## Public share URLs

- https://chatgpt.com/share/6ab1eabe-1f24-83ea-8f55-212e35a45529
- https://chatgpt.com/share/6ab1eb2c-8158-83ea-baed-16b51daa823b
