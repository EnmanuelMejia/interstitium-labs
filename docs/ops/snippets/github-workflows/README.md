# GitHub Actions templates

Preferred location: `.github/workflows/` (committed in-repo when the push token has the `workflow` scope).

If a push rejects workflow files, copy from here via the GitHub UI (Actions → New workflow) or a PAT with `workflow` scope.

| File | Purpose |
| --- | --- |
| `security-audit.yml` | `scripts/security-check.sh` + `npm audit --audit-level=high` in `apps/mobile` (fail on high+) |
| `mobile-android-debug.yml` | Sync www + document Android debug path |

Do **not** use `--force` to ignore audit findings. Run locally: `bash scripts/security-check.sh`.
