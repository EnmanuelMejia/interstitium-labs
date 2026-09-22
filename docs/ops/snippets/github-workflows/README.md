# GitHub Actions templates

Copy these into `.github/workflows/` via the GitHub UI or a token with the `workflow` scope.

| File | Purpose |
| --- | --- |
| `security-audit.yml` | `npm ci` + `npm audit --audit-level=high` in `apps/mobile` (fail on high+) |
| `mobile-android-debug.yml` | Sync www + assembleDebug APK artifact |

Do **not** use `--force` to ignore audit findings.
