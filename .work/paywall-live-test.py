#!/usr/bin/env python3
"""Set ENTITLEMENT_SECRET on solitary-sound-015a and live-test the paywall gate.

1. Generates a cryptographically random 32-byte secret (base64url).
2. PUTs it as a worker secret via the Cloudflare API (never printed/logged).
3. Mints test entitlement tokens with the exact signEntitlement construction:
     b64u(JSON({course, iat, exp})) + "." + b64u(HMAC-SHA256(secret, body))
4. Live-tests: valid token -> gated JSON 200; tampered sig -> 402;
   wrong scope -> 402; no cookie -> 402; free course JSON -> 200.
Prints only PASS/FAIL, never the secret value.
"""
import base64
import hashlib
import hmac
import json
import subprocess
import sys
import time
import urllib.request

ACCOUNT = "bb1baf6bc6c34d30fadc402b420fa3c2"
SCRIPT = "solitary-sound-015a"
GATED_SLUG = "il-26-data-analyst-certification-senior-mastery"
FREE_SLUG = "il-29-threatlocker-ai-cybersecurity-mastery"
BASE = "https://interstitiumlabs.dev"
ENTITLEMENT_TTL = 86400 * 365  # must match payment-routes.js ENTITLEMENT_TTL


def b64u(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


def sign(secret_b64: str, course: str) -> str:
    secret = secret_b64.encode()
    now = int(time.time())
    payload = json.dumps({"course": course, "iat": now, "exp": now + ENTITLEMENT_TTL},
                         separators=(",", ":")).encode()
    body = b64u(payload)
    sig = b64u(hmac.new(secret, body.encode(), hashlib.sha256).digest())
    return body + "." + sig


def put_secret(secret: str) -> bool:
    """PUT worker secret via cf-api helper. Returns True on success."""
    body = json.dumps({"name": "ENTITLEMENT_SECRET", "text": secret, "type": "secret_text"})
    p = subprocess.run(
        ["/home/hatch/workspace/skills/cloudflare/bin/cf-api", "PUT",
         f"/accounts/{ACCOUNT}/workers/scripts/{SCRIPT}/secrets"],
        input=body, capture_output=True, text=True, timeout=90,
    )
    try:
        data = json.loads(p.stdout)
    except Exception:
        print("secret PUT: FAIL (unparseable response)")
        return False
    ok = bool(data.get("success"))
    print("secret PUT:", "PASS" if ok else f"FAIL ({str(data)[:200]})")
    return ok


def get(path: str, cookie: str | None = None):
    req = urllib.request.Request(BASE + path)
    # Cloudflare bot management 403s the default Python-urllib UA; use a browser UA.
    req.add_header("User-Agent",
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
    if cookie:
        req.add_header("Cookie", cookie)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()[:120]
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:120]
    finally:
        time.sleep(3)  # avoid edge rate-limiting on test bursts


def main() -> int:
    import urllib.error
    secret = b64u(__import__("secrets").token_bytes(32))
    if not put_secret(secret):
        return 1
    # Allow a few seconds for the secret to propagate to the edge.
    time.sleep(8)

    results = []
    gated_json = f"/university/data/courses/{GATED_SLUG}.json"
    free_json = f"/university/data/courses/{FREE_SLUG}.json"

    valid = sign(secret, GATED_SLUG)
    code, body = get(gated_json, f"il_entitlement={valid}")
    ok = code == 200 and body[:1] == b"{"
    results.append(("valid token -> gated JSON 200", ok, code))

    tampered = valid[:-2] + ("AA" if not valid.endswith("AA") else "BB")
    code, _ = get(gated_json, f"il_entitlement={tampered}")
    results.append(("tampered token -> 402", code == 402, code))

    wrong_scope = sign(secret, "il-01-esoteric-foundations")
    code, _ = get(gated_json, f"il_entitlement={wrong_scope}")
    results.append(("wrong-scope token -> 402", code == 402, code))

    code, _ = get(gated_json)
    results.append(("no cookie -> 402", code == 402, code))

    code, _ = get(free_json)
    results.append(("free course JSON no cookie -> 200", code == 200, code))

    code, _ = get(f"/university/course?course={GATED_SLUG}", f"il_entitlement={valid}")
    results.append(("valid token -> gated course page 200", code == 200, code))

    allok = True
    for name, ok, code in results:
        print(("PASS" if ok else "FAIL"), f"[http {code}]", name)
        allok = allok and ok
    print("ALL PASS" if allok else "SOME FAILED")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
