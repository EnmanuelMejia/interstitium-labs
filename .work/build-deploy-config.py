#!/usr/bin/env python3
"""Build the flagship deploy config for solitary-sound-015a.

Reconstructs the 2026-10-07 deploy (sibling config not on disk) from the
live worker's settings + the worker source's route surface. run_worker_first
uses EXACT paths only (proven supported) covering every path the worker's
fetch() handles: redirects, APIs, course pages, gated course/story JSONs.
"""
import json, os

DOCS = "/home/hatch/workspace/apex-audit/docs"

paths = [
    # code-level 301 redirects
    "/os", "/os/", "/proof", "/proof/", "/il26", "/il26/",
    "/il27", "/il27/", "/il28", "/il28/", "/il29", "/il29/",
    # APIs (waitlist, auth, progress, certificates, payments, noah)
    "/api/waitlist",
    "/api/auth/request", "/api/auth/verify", "/api/me", "/api/auth/signout",
    "/api/progress",
    "/api/certificates/issue", "/api/certificates", "/api/certificates/verify",
    "/api/pay/create", "/api/pay/status", "/api/pay/ud",
    "/api/pay/tx/submit", "/api/pay/admin/confirm", "/api/pay/entitlement",
    "/api/pay/webhook/stripe", "/api/pay/webhook/paypal",
    "/api/pay/ipn/nowpayments",
    "/api/pay/paypal/return", "/api/pay/paypal/cancel",
    "/api/pay/stripe/return",
    "/api/noah-stats", "/api/noah",
    # course player (OG injection + paywall)
    "/university/course", "/university/course.html",
]

# course JSONs (gated ones need the worker for 402; non-gated passthrough =
# asset served). Exact per-file paths exceed the 100-char rule limit, so use
# wildcard patterns — the worker's courseGate only acts on matching slugs and
# passes everything else through to the asset.
paths.append("/university/data/courses/*.json")
paths.append("/university/data/courses/stories/*.json")

config = {
    "_notes": [
        "Flagship interstitiumlabs.dev (knowledge OS). Reconstructed 2026-10-08 "
        "from live worker settings + _worker.js route surface. run_worker_first "
        "uses exact paths only; covers every path fetch() handles."
    ],
    "worker": "solitary-sound-015a",
    "assets_dir": DOCS + "/",
    "compatibility_date": "2026-09-23",
    "main_module": "_worker.bundle.js",
    "bindings": [
        # NOTE: secret_text bindings (ENTITLEMENT_SECRET, SESSION_SECRET) are
        # intentionally OMITTED — the API rejects them without a value, and
        # omitting preserves the live secrets server-side untouched.
        {"name": "AI", "type": "ai", "project": "<catalog>"},
        {"name": "ASSETS", "type": "assets"},
        {"name": "IL_ACCOUNTS", "type": "kv_namespace",
         "namespace_id": "1dbec2d5ffa1400989e3363ba5d5e1ec"},
        {"name": "IL_AUTH", "type": "kv_namespace",
         "namespace_id": "739945c3eed841288cf167d88c8d39b1"},
        {"name": "NOAH_STATS", "type": "kv_namespace",
         "namespace_id": "6c7b016f095d439b83d8231ee2ad4af5"},
        {"name": "WAITLIST", "type": "kv_namespace",
         "namespace_id": "a26c514c707d4baa9263610c5ac8c4ac"},
    ],
    "assets_config": {
        "html_handling": "auto-trailing-slash",
        "not_found_handling": "404-page",
        "run_worker_first": paths,
    },
}

out = "/home/hatch/workspace/apex-audit/.work/flagship-deploy-config-20261008.json"
with open(out, "w") as f:
    json.dump(config, f, indent=2)
print("wrote", out, "with", len(paths), "run_worker_first paths")
