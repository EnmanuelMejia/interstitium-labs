"""Batch 10: Security PDFs — auth/crypto, appsec, platform, detection, forensics, compliance (22 guides)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


# ---------------------------------------------------------------- 1. OIDC & SAML
def pdf_oidc_saml(path):
    c = new_canvas(path); pg = 1
    title_page(c, "OIDC & SAML\nVisual Guide",
               "Federated identity —\none login, many apps, no password sprawl.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "The Federation Triangle",
                       "One identity provider vouches for you to every app.")
    box(c, 72, y-100, 150, 90, BOX_BLUE, "You", "browser / device")
    box(c, 246, y-100, 150, 90, BOX_GREEN, "App (SP)", "relying party")
    box(c, 420, y-100, 120, 90, BOX_PURP, "IdP", "identity provider")
    arrow(c, 222, y-55, 246, y-55, color=ACCENT, width=2.2, label="log me in")
    arrow(c, 396, y-55, 420, y-55, color=GREEN, width=2.2, label="assertion")
    arrow(c, 246, y-120, 148, y-120, color=ORANGE, width=2.2, label="trusts the IdP")
    note(c, 72, y-190, 468, "The app never sees your password — it trusts a signed token from the IdP instead.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "SAML: Assertion Flow",
                       "The classic enterprise SSO handshake (XML-based).")
    box(c, 72, y-80, 120, 70, BOX_BLUE, "User", "clicks SSO login")
    box(c, 216, y-80, 130, 70, BOX_ORANGE, "App", "redirects w/ SAMLReq")
    box(c, 370, y-80, 170, 70, BOX_PURP, "IdP", "authenticates user")
    arrow(c, 192, y-45, 216, y-45, color=ACCENT, width=2.2)
    arrow(c, 346, y-45, 370, y-45, color=ACCENT, width=2.2)
    arrow(c, 370, y-120, 216, y-120, color=GREEN, width=2.5, label="signed SAML assertion (POST)")
    note(c, 72, y-200, 468, "Assertion = XML document: who you are + attributes + signature. Verify signature, check audience + expiry, then create the session.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "OIDC: Authorization Code + ID Token",
                       "Modern federation for web, mobile, APIs (JSON-based).")
    box(c, 72, y-70, 130, 64, BOX_BLUE, "App", "redirects to IdP")
    box(c, 240, y-70, 130, 64, BOX_PURP, "IdP", "user logs in")
    box(c, 408, y-70, 132, 64, BOX_GREEN, "Code", "short-lived")
    arrow(c, 202, y-38, 240, y-38, color=ACCENT, width=2.2)
    arrow(c, 370, y-38, 408, y-38, color=ACCENT, width=2.2)
    arrow(c, 450, y-90, 450, y-180, color=GREEN, width=2.5)
    box(c, 240, y-250, 200, 70, BOX_TEAL, "Token Endpoint", "code + client secret → tokens")
    note(c, 72, y-330, 468, "The code travels via the browser; tokens are exchanged server-to-server. PKCE replaces the client secret for public clients.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "The ID Token (a JWT)",
                       "Who the user is — signed, expiring, verifiable.")
    box(c, 72, y-70, 468, 60, BOX_BLUE, "Header", "alg + kid (which key signed it)")
    box(c, 72, y-150, 468, 60, BOX_GREEN, "Payload (claims)", "sub, iss, aud, exp, iat, nonce, email…")
    box(c, 72, y-230, 468, 60, BOX_RED, "Signature", "verifiable with the IdP's public key (JWKS)")
    note(c, 72, y-310, 468, "Always verify: signature, issuer (iss), audience (aud = YOUR app), expiry (exp). A valid-looking token that isn't verified is just a string.", BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "The SSO Session",
                       "Log in once — roam across every connected app.")
    box(c, 220, y-90, 172, 70, BOX_PURP, "IdP Session", "your single login")
    for i, (lbl, dx) in enumerate([("Email", -150), ("CRM", 0), ("VPN", 150)]):
        box(c, 72 + i*152, y-240, 140, 70, BOX_BLUE, lbl, "token minted silently")
        arrow(c, 306, y-92, 142 + i*152, y-168, color=GREEN, width=2)
    note(c, 72, y-330, 468, "Single logout ends the IdP session so tokens stop being minted. Session lifetime and re-auth policies live at the IdP, not in each app.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "SAML vs OIDC — Picking One",
                       "Both do SSO; the ecosystem decides.")
    box(c, 72, y-110, 224, 100, BOX_ORANGE, "SAML", "Enterprise legacy: XML assertions, mature IdP support, heavier.")
    box(c, 316, y-110, 224, 100, BOX_GREEN, "OIDC", "Modern default: JSON/JWT, built for mobile + APIs, lighter.")
    y = bullet_list(c, 72, y-250, [
        "Enterprise app that only speaks SAML → SAML.",
        "New web/mobile/API → OIDC (authorization code + PKCE).",
        "Never build your own protocol — delegate auth to the IdP."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "OIDC & SAML — Remember",
                 ["Federation: the app trusts a signed token from the IdP — passwords stay with the IdP.",
                  "SAML passes signed XML assertions; OIDC passes JWT ID tokens via the code flow.",
                  "Verify every token: signature, issuer, audience, expiry. Unverified = untrusted.",
                  "One IdP session powers SSO across apps; centralize session policy there.",
                  "New builds default to OIDC; keep SAML for legacy enterprise integrations."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 2. JWT
def pdf_jwt(path):
    c = new_canvas(path); pg = 1
    title_page(c, "JWT\nVisual Guide",
               "JSON Web Tokens —\ncompact, signed, self-contained credentials.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Anatomy: Three Segments",
                       "Header . Payload . Signature — base64url, dot-separated.")
    box(c, 72, y-80, 150, 80, BOX_BLUE, "Header", "alg: HS256, typ: JWT")
    box(c, 236, y-80, 150, 80, BOX_GREEN, "Payload", "claims about user")
    box(c, 400, y-80, 140, 80, BOX_RED, "Signature", "HMAC or RSA/ECDSA")
    arrow(c, 222, y-40, 236, y-40, color=MUTED, width=2)
    arrow(c, 386, y-40, 400, y-40, color=MUTED, width=2)
    note(c, 72, y-180, 468, "The payload is only base64url-ENCODED, not encrypted — anyone can read it. Never put secrets in claims.", BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Claims: What Tokens Say",
                       "Three claim flavors, one contract.")
    box(c, 72, y-80, 150, 90, BOX_PURP, "Registered", "iss, sub, aud, exp, iat, nbf, jti")
    box(c, 240, y-80, 150, 90, BOX_TEAL, "Public", "standard names, safe to share")
    box(c, 408, y-80, 132, 90, BOX_ORANGE, "Private", "app-specific (roles, tenant)")
    note(c, 72, y-200, 468, "Keep tokens small: a handful of claims. Everything you add rides on every request.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Validation: The Six Checks",
                       "Run all of them, every time, server-side.")
    checks = [("1. Signature", "recompute with the right key", BOX_BLUE),
              ("2. Issuer", "iss matches your IdP", BOX_GREEN),
              ("3. Audience", "aud is YOUR service", BOX_TEAL),
              ("4. Expiry", "exp in the future", BOX_ORANGE),
              ("5. Not-before", "nbf in the past", BOX_PURP),
              ("6. Replay", "jti not seen before (sensitive ops)", BOX_RED)]
    yy = y
    for i, (t, s, f) in enumerate(checks):
        box(c, 72 + (i % 2)*240, yy-58, 228, 62, f, t, s, font_size=10.5)
        if i % 2 == 1: yy -= 74
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Pitfalls That Burn People",
                       "Real attacks, still seen in the wild.")
    box(c, 72, y-100, 468, 80, BOX_RED, "alg=none", "Attacker strips the signature. Fix: whitelist allowed algorithms.")
    box(c, 72, y-200, 468, 80, BOX_RED, "Weak HS256 secret", "'secret123' brute-forced offline. Fix: 256-bit random key, or use RS256.")
    box(c, 72, y-300, 468, 80, BOX_ORANGE, "No expiry / giant lifetime", "Stolen token works forever. Fix: short exp + refresh tokens.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Key Rotation with JWKS",
                       "Keys change; tokens keep validating.")
    box(c, 72, y-80, 200, 70, BOX_PURP, "JWKS endpoint", "IdP publishes public keys")
    box(c, 330, y-80, 210, 70, BOX_BLUE, "kid in header", "picks the right key")
    arrow(c, 272, y-45, 330, y-45, color=ACCENT, width=2.5, label="fetch + cache")
    y = bullet_list(c, 72, y-190, [
        "Sign with RS256/ES256 (asymmetric) so verifiers only need public keys.",
        "Cache the JWKS; respect cache headers; handle key rollover gracefully.",
        "Rotate signing keys on a schedule and after any suspected compromise."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Tokens vs Sessions — When",
                       "Stateless is fast; stateful is revocable.")
    box(c, 72, y-110, 224, 100, BOX_GREEN, "JWT access tokens", "Stateless, short-lived (minutes). Great for APIs.")
    box(c, 316, y-110, 224, 100, BOX_BLUE, "Server sessions", "Instantly revocable. Great for web apps + admin.")
    note(c, 72, y-250, 468, "Classic pattern: short-lived JWT access token + rotating refresh token stored server-side. Best of both worlds.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "JWT — Remember",
                 ["JWT = header.payload.signature; payload is readable, not encrypted.",
                  "Validate six things: signature, issuer, audience, expiry, not-before, replay.",
                  "Kill alg confusion: whitelist algorithms, use strong random keys or RS256/ES256.",
                  "Rotate signing keys via JWKS; keep tokens short-lived with refresh tokens.",
                  "Short JWT for APIs, server sessions where instant revocation matters."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 3. MFA
def pdf_mfa(path):
    c = new_canvas(path); pg = 1
    title_page(c, "MFA\nVisual Guide",
               "Multi-Factor Authentication —\nmake a stolen password useless.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "TOTP Mechanics",
                       "Time-based one-time passwords: shared secret + clock.")
    box(c, 72, y-80, 180, 70, BOX_BLUE, "Shared secret", "set up once via QR")
    box(c, 292, y-80, 180, 70, BOX_GREEN, "Current time", "30-second windows")
    arrow(c, 252, y-45, 292, y-45, color=ACCENT, width=2.2)
    arrow(c, 362, y-82, 362, y-160, color=ACCENT, width=2.5)
    box(c, 242, y-240, 200, 70, BOX_ORANGE, "HMAC(secret, time)", "truncate → 6 digits")
    note(c, 72, y-330, 468, "Both sides compute the same code independently — no network needed. Clock drift beyond ~1 window = rejected.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "WebAuthn / Passkeys",
                       "Public-key login bound to the real site.")
    box(c, 72, y-80, 140, 70, BOX_BLUE, "Browser", "requests login")
    box(c, 252, y-80, 140, 70, BOX_PURP, "Authenticator", "phone / security key")
    box(c, 432, y-80, 108, 70, BOX_GREEN, "Server", "verifies")
    arrow(c, 212, y-45, 252, y-45, color=ACCENT, width=2.2, label="challenge")
    arrow(c, 392, y-45, 432, y-45, color=GREEN, width=2.2, label="signed response")
    note(c, 72, y-180, 468, "The signature covers the site's origin — a fake site's challenge won't verify. That origin-binding is what defeats phishing.", BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Push Approval & Number Matching",
                       "Convenient — but convenience gets attacked.")
    box(c, 72, y-80, 220, 70, BOX_BLUE, "Login attempt", "shows number: 42")
    box(c, 322, y-80, 218, 70, BOX_GREEN, "Phone push", "tap the matching number")
    arrow(c, 292, y-45, 322, y-45, color=ACCENT, width=2.5)
    note(c, 72, y-180, 468, "Number matching defeats 'MFA fatigue' spam-taps. Without it, attackers bombard the user until one tired tap approves.", BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Phishable vs Phishing-Resistant",
                       "Not all second factors are equal — rank them.")
    box(c, 72, y-80, 468, 60, BOX_RED, "SMS codes", "SIM-swap + interception — weakest, still better than nothing")
    box(c, 72, y-160, 468, 60, BOX_ORANGE, "TOTP / push", "Phishable via fake login pages — strong against password theft")
    box(c, 72, y-240, 468, 60, BOX_GREEN, "WebAuthn / passkeys", "Origin-bound cryptography — phishing-resistant")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Enrollment & Recovery",
                       "MFA is only as strong as its reset flow.")
    y = bullet_list(c, 72, y, [
        "Enroll MFA at account creation, not as an afterthought.",
        "Issue backup codes (single-use, stored offline) for lost devices.",
        "Recovery must re-verify identity as strongly as enrollment — no 'just email me a reset'.",
        "Log and alert on MFA changes: new device, disabled factor, recovery used."])
    note(c, 72, 180, 468, "Most MFA bypasses happen at the help-desk recovery flow, not the crypto. Harden that first.", BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Choosing Your MFA Policy",
                       "Match strength to risk.")
    box(c, 72, y-100, 150, 90, BOX_GREEN, "Everyone", "require MFA, allow TOTP+")
    box(c, 240, y-100, 150, 90, BOX_ORANGE, "Admins", "phishing-resistant only")
    box(c, 408, y-100, 132, 90, BOX_BLUE, "Execs / finance", "hardware keys")
    y = bullet_list(c, 72, y-230, [
        "Default: phishing-resistant for privileged accounts, TOTP minimum for all.",
        "Risk-based step-up: challenge again on new device, odd location, sensitive action."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "MFA — Remember",
                 ["A stolen password alone should never be enough — require a second factor.",
                  "TOTP = shared secret + time, no network needed; keep clocks in sync.",
                  "WebAuthn/passkeys bind the signature to the site's origin — phishing-resistant.",
                  "Use number matching on push; never rely on tired-tap approvals.",
                  "Harden enrollment and recovery — that's where bypasses actually happen.",
                  "Admins and finance get hardware keys; everyone else gets TOTP minimum."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 4. Password Hashing
def pdf_password_hashing(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Password Hashing\nVisual Guide",
               "Store passwords so a stolen database\nisn't a stolen password list.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Why Not Plaintext (or Plain SHA)",
                       "Databases leak. Hashes must survive the leak.")
    box(c, 72, y-80, 220, 70, BOX_RED, "Plaintext", "breach = every password")
    box(c, 322, y-80, 218, 70, BOX_ORANGE, "Unsalted SHA-256", "rainbow tables crack it in seconds")
    note(c, 72, y-180, 468, "Fast hashes are the enemy: GPUs compute billions of SHA-256 guesses per second. Password hashing must be deliberately SLOW.", BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Salting: Unique Hash per User",
                       "Same password, different stored hash.")
    box(c, 72, y-80, 200, 70, BOX_BLUE, "password123", "same input")
    box(c, 310, y-80, 230, 70, BOX_TEAL, "+ random salt", "16+ bytes, per user")
    arrow(c, 272, y-45, 310, y-45, color=ACCENT, width=2.2)
    arrow(c, 425, y-82, 425, y-160, color=ACCENT, width=2.5)
    box(c, 310, y-240, 230, 70, BOX_GREEN, "hash(salt + pw)", "attacker must crack each user separately")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "The Right Algorithms",
                       "Memory-hard + tunable cost. Pick one.")
    box(c, 72, y-100, 150, 90, BOX_GREEN, "Argon2id", "modern default — memory-hard, tunable")
    box(c, 240, y-100, 150, 90, BOX_BLUE, "bcrypt", "battle-tested, cost factor")
    box(c, 408, y-100, 132, 90, BOX_TEAL, "scrypt", "memory-hard, older tuning")
    note(c, 72, y-220, 468, "Never MD5 / SHA-1 / SHA-256 alone for passwords — they're built for speed, which is exactly what attackers want.", BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Work Factors: Tune the Cost",
                       "Slow enough to hurt attackers, fast enough for users.")
    box(c, 72, y-80, 220, 70, BOX_BLUE, "Target: ~0.5–1s", "per login on your hardware")
    box(c, 322, y-80, 218, 70, BOX_GREEN, "Attacker cost", "× millions of guesses = years")
    y = bullet_list(c, 72, y-190, [
        "Argon2id: tune memory (e.g. 64MB), iterations, parallelism together.",
        "bcrypt: cost 12+ as a starting point; raise as hardware improves.",
        "Re-tune annually — what was expensive in 2020 is cheap on 2026 GPUs."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Pepper: The Extra Layer",
                       "A secret salt the database never sees.")
    box(c, 72, y-80, 150, 70, BOX_PURP, "Salt", "stored with the hash")
    box(c, 252, y-80, 150, 70, BOX_ORANGE, "Pepper", "in app config / HSM")
    box(c, 432, y-80, 108, 70, BOX_GREEN, "Password", "user input")
    note(c, 72, y-180, 468, "Pepper lives outside the DB (config, env, HSM/KMS) — a pure database dump is then useless without it. Rotate carefully: you must re-hash.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Migrating Old Hashes",
                       "Upgrade without forcing a mass password reset.")
    y = bullet_list(c, 72, y, [
        "On each login: verify against the old hash, then immediately re-hash with Argon2id.",
        "Flag legacy-hash users; expire stragglers with a forced reset after a window.",
        "Never decrypt-then-rehash — you can't decrypt a hash; the login moment is your only chance.",
        "Monitor: track the % of users still on legacy hashes until it hits zero."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Password Hashing — Remember",
                 ["Never store plaintext; never use fast hashes (MD5/SHA) alone.",
                  "Salt every password with a unique random salt — kills rainbow tables.",
                  "Use Argon2id (or bcrypt/scrypt) with a tuned work factor (~0.5–1s).",
                  "Add a pepper stored outside the database for dump-resistance.",
                  "Migrate legacy hashes opportunistically at login; re-tune cost yearly."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 5. HMAC & Digital Signatures
def pdf_hmac(path):
    c = new_canvas(path); pg = 1
    title_page(c, "HMAC & Digital Signatures\nVisual Guide",
               "Prove a message is authentic —\nand prove who sent it.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "HMAC: Message Authentication",
                       "Shared secret + message → tamper-evident tag.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "Message", "API request")
    box(c, 252, y-80, 150, 70, BOX_PURP, "Secret key", "shared by both sides")
    arrow(c, 222, y-45, 252, y-45, color=ACCENT, width=2.2)
    arrow(c, 402, y-45, 430, y-45, color=ACCENT, width=2.2)
    box(c, 430, y-80, 110, 70, BOX_GREEN, "HMAC tag", "send alongside")
    note(c, 72, y-180, 468, "Receiver recomputes the tag with the same secret — match means authentic AND unmodified. Used in webhooks, API auth, cookie signing.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Digital Signatures: Sign & Verify",
                       "Private key signs, public key verifies — no shared secret.")
    box(c, 72, y-80, 200, 70, BOX_ORANGE, "Sign", "private key + hash(message)")
    box(c, 330, y-80, 210, 70, BOX_GREEN, "Verify", "public key + signature")
    arrow(c, 272, y-45, 330, y-45, color=ACCENT, width=2.5, label="signature")
    note(c, 72, y-180, 468, "Anyone can verify with the public key, but only the private-key holder could have signed. That's non-repudiation.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "RSA vs ECDSA",
                       "Two workhorses, different trade-offs.")
    box(c, 72, y-110, 224, 100, BOX_BLUE, "RSA", "2048-bit+ keys; widely supported; bigger signatures.")
    box(c, 316, y-110, 224, 100, BOX_GREEN, "ECDSA (P-256)", "Tiny keys + fast; same security, 1/8 the size.")
    note(c, 72, y-250, 468, "Always sign the HASH of the message, never the raw message. And use a modern padding/scheme — textbook RSA is broken.", BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Certificates Bind Keys to Identity",
                       "A public key is useless if you don't know whose it is.")
    box(c, 72, y-80, 150, 70, BOX_PURP, "End-entity", "your server's key")
    box(c, 252, y-80, 150, 70, BOX_BLUE, "Intermediate", "CA's signing key")
    box(c, 432, y-80, 108, 70, BOX_GREEN, "Root CA", "trusted anchor")
    arrow(c, 222, y-45, 252, y-45, color=ACCENT, width=2.2, label="signed by")
    arrow(c, 402, y-45, 432, y-45, color=ACCENT, width=2.2, label="signed by")
    note(c, 72, y-180, 468, "The chain lets a stranger's signature become trustworthy: each link vouches for the one below, anchored at a root you already trust.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "HMAC vs Signatures — When",
                       "Symmetric speed vs asymmetric trust.")
    box(c, 72, y-110, 224, 100, BOX_PURP, "HMAC", "Both sides share a secret. Fast. Use: webhooks, API keys, sessions.")
    box(c, 316, y-110, 224, 100, BOX_GREEN, "Signatures", "Public verification. Use: JWTs, code signing, certificates.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Key Handling Pitfalls",
                       "The math is solid; the handling is where it breaks.")
    y = bullet_list(c, 72, y, [
        "HMAC keys must be random 256-bit — 'secret' as a string is crackable.",
        "Compare tags in constant time — naive == leaks the tag byte-by-byte.",
        "Protect private keys in a KMS/HSM; never commit them to repos.",
        "Timestamp + nonce on signed messages to block replay attacks."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "HMAC & Signatures — Remember",
                 ["HMAC proves authenticity with a shared secret; signatures prove it with key pairs.",
                  "Sign the hash, not the message; use modern schemes and padding.",
                  "Certificates bind public keys to identities via a chain to a trusted root.",
                  "HMAC for webhooks/API auth; signatures for JWTs, code, and certificates.",
                  "Compare tags in constant time; keep private keys in KMS/HSM."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 6. Key Management (KMS/HSM)
def pdf_kms_hsm(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Key Management\nVisual Guide",
               "KMS, HSMs, envelope encryption —\nkeys are the crown jewels; treat them that way.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Envelope Encryption",
                       "Encrypt data with a data key; encrypt the data key with a master key.")
    box(c, 72, y-80, 200, 70, BOX_BLUE, "DEK", "data key — encrypts the data")
    box(c, 312, y-80, 228, 70, BOX_PURP, "KEK", "key-encrypting key — wraps the DEK")
    arrow(c, 272, y-45, 312, y-45, color=ACCENT, width=2.5, label="wraps")
    note(c, 72, y-180, 468, "Store the encrypted DEK next to the data; the KEK never leaves the KMS/HSM. Rotating the KEK re-wraps DEKs — no data re-encryption needed.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "KMS Architecture",
                       "Central key service with policy + audit on every use.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "App", "requests encrypt/")
    box(c, 252, y-80, 150, 70, BOX_PURP, "KMS", "policy check + audit log")
    box(c, 432, y-80, 108, 70, BOX_GREEN, "Keys", "never exported")
    arrow(c, 222, y-45, 252, y-45, color=ACCENT, width=2.2)
    arrow(c, 402, y-45, 432, y-45, color=ACCENT, width=2.2)
    note(c, 72, y-180, 468, "Apps get ciphertext and plaintext back — never the raw key. Every operation is logged: who used which key, when.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "HSM vs Cloud KMS",
                       "Hardware roots of trust vs managed service.")
    box(c, 72, y-110, 224, 100, BOX_ORANGE, "HSM", "Tamper-proof hardware; you control it. FIPS 140-2 Level 3. Highest assurance, most ops burden.")
    box(c, 316, y-110, 224, 100, BOX_GREEN, "Cloud KMS", "Managed keys on provider HSMs. Policy + audit built in. Easiest correct default.")
    note(c, 72, y-250, 468, "Rule of thumb: cloud KMS unless regulation or threat model demands your own HSMs.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Key Rotation, Done Right",
                       "Rotate on a schedule — and be able to rotate in an emergency.")
    box(c, 72, y-80, 140, 70, BOX_BLUE, "v1 key", "active Jan–Jun")
    box(c, 240, y-80, 140, 70, BOX_GREEN, "v2 key", "active Jul–Dec")
    box(c, 408, y-80, 132, 70, BOX_ORANGE, "Old keys", "kept for decrypt")
    arrow(c, 212, y-45, 240, y-45, color=ACCENT, width=2.5, label="rotate")
    note(c, 72, y-180, 468, "New data uses the new key; old keys stay available (decrypt-only) until all data is re-wrapped. Test emergency rotation before you need it.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Separation of Duties",
                       "No single person should own a key end-to-end.")
    y = bullet_list(c, 72, y, [
        "Key custodians create and back up keys; operators use them via policy — different people.",
        "Require multi-party approval (m-of-n) for destructive actions: delete key, export, disable.",
        "Break-glass procedures exist but every use pages security and leaves an audit trail.",
        "Developers get encrypt/decrypt rights; nobody gets raw key material."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Key Lifecycle Checklist",
                       "From birth to destruction.")
    y = bullet_list(c, 72, y, [
        "Generate in the KMS/HSM with a strong RNG — never on a laptop.",
        "Tag every key: owner, purpose, rotation schedule, data classification.",
        "Automate rotation; alert on rotation failures and stale keys.",
        "Destroy securely at end of life: crypto-shred by deleting the key (data becomes unreadable).",
        "Back up HSM master keys as split shares in separate safes — losing them loses everything."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Key Management — Remember",
                 ["Envelope encryption: DEKs encrypt data, KEKs wrap DEKs and never leave the KMS/HSM.",
                  "Apps see plaintext/ciphertext, never raw keys; every use is policy-checked and logged.",
                  "Cloud KMS is the sane default; own HSMs only when compliance demands it.",
                  "Rotate on schedule, keep old keys decrypt-only, and rehearse emergency rotation.",
                  "Separate duties: creators ≠ users; m-of-n approval for destructive actions."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 7. WAF
def pdf_waf(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Web Application Firewalls\nVisual Guide",
               "A shield in front of your app —\nfiltering attacks before they reach your code.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Where the WAF Sits",
                       "Every request passes inspection first.")
    box(c, 72, y-80, 120, 70, BOX_BLUE, "Client", "browser / bot")
    box(c, 222, y-80, 140, 70, BOX_ORANGE, "WAF", "inspect + decide")
    box(c, 392, y-80, 148, 70, BOX_GREEN, "App", "only clean traffic")
    arrow(c, 192, y-45, 222, y-45, color=ACCENT, width=2.5)
    arrow(c, 362, y-45, 392, y-45, color=GREEN, width=2.5, label="allow")
    note(c, 72, y-180, 468, "Deploy at the edge (CDN), as a reverse proxy, or as a host module. Edge placement also absorbs junk before it costs you origin bandwidth.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Negative vs Positive Security Models",
                       "Block known-bad vs allow known-good.")
    box(c, 72, y-110, 224, 100, BOX_RED, "Negative (blocklist)", "Signatures for known attacks. Easy start, misses novel payloads.")
    box(c, 316, y-110, 224, 100, BOX_GREEN, "Positive (allowlist)", "Learn normal traffic; block the rest. Stronger, needs tuning.")
    note(c, 72, y-250, 468, "Mature setups run both: blocklists for cheap wins, positive model for the crown-jewel endpoints.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "OWASP Core Rule Set (CRS)",
                       "The community rule pack most WAFs start from.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "Protocol", "malformed requests")
    box(c, 240, y-80, 150, 70, BOX_ORANGE, "Injection", "SQLi, XSS, RCE probes")
    box(c, 408, y-80, 132, 70, BOX_RED, "Anomaly", "scoring + thresholds")
    note(c, 72, y-180, 468, "CRS scores anomalies per request and blocks past a threshold (paranoia levels 1–4). Higher paranoia = more blocks AND more false positives.", BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Tuning: Killing False Positives",
                       "A WAF that blocks customers is a self-inflicted DDoS.")
    y = bullet_list(c, 72, y, [
        "Start in detection/log-only mode — observe what WOULD block for 1–2 weeks.",
        "Whitelist by rule ID for legitimate patterns (rich text editors trip XSS rules).",
        "Tune per endpoint: strict on /admin, lenient on the marketing blog.",
        "Re-tune after every app release — new features create new 'anomalies'."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Virtual Patching & Rate Limiting",
                       "Buy time when code can't ship today.")
    box(c, 72, y-110, 224, 100, BOX_PURP, "Virtual patch", "WAF rule blocks the exploit pattern while the real fix is coded.")
    box(c, 316, y-110, 224, 100, BOX_TEAL, "Rate limiting", "Throttle brute force, scraping, credential stuffing per IP/session.")
    note(c, 72, y-250, 468, "Virtual patches are band-aids with expiry dates — track them like tech debt and remove when the code fix ships.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "WAF Is One Layer",
                       "It reduces exposure; it doesn't replace secure code.")
    y = bullet_list(c, 72, y, [
        "WAFs can't see encrypted payloads they don't terminate, or logic flaws.",
        "Bypass techniques evolve — re-test your rules with each pentest.",
        "Pair with: secure coding, SAST/DAST, auth hardening, and monitoring.",
        "Measure: block rate, false-positive rate, time-to-tune after releases."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "WAF — Remember",
                 ["The WAF inspects traffic before it reaches your app — deploy at the edge when you can.",
                  "Negative model blocks known-bad; positive model allows known-good. Use both.",
                  "OWASP CRS is the standard starting rule set; tune paranoia levels carefully.",
                  "Always start in log-only mode and whitelist legitimate patterns per endpoint.",
                  "Virtual patching buys time for real fixes; rate limiting blunts brute force.",
                  "A WAF complements secure code — it never replaces it."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 8. DDoS Mitigation
def pdf_ddos(path):
    c = new_canvas(path); pg = 1
    title_page(c, "DDoS Mitigation\nVisual Guide",
               "When the internet itself attacks —\nlayers of defense that absorb the flood.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "The Three Attack Layers",
                       "Different floods need different defenses.")
    box(c, 72, y-110, 150, 100, BOX_RED, "Volumetric", "L3/L4: UDP floods, Gbps scale. Drown the pipe.")
    box(c, 240, y-110, 150, 100, BOX_ORANGE, "Protocol", "SYN floods, reflection. Exhaust state/tables.")
    box(c, 408, y-110, 132, 100, BOX_PURP, "Application", "L7: slow HTTP, bot floods. Exhaust the app.")
    note(c, 72, y-250, 468, "Modern attacks blend all three. Your defense must be layered too — no single box stops everything.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Scrubbing Centers",
                       "Dirty traffic in, clean traffic out.")
    box(c, 72, y-80, 130, 70, BOX_RED, "Attack", "flood + legit mixed")
    box(c, 240, y-80, 140, 70, BOX_ORANGE, "Scrubbing", "filter at scale")
    box(c, 418, y-80, 122, 70, BOX_GREEN, "Your app", "clean only")
    arrow(c, 202, y-45, 240, y-45, color=RED, width=3)
    arrow(c, 380, y-45, 418, y-45, color=GREEN, width=2.5, label="BGP reroute")
    note(c, 72, y-180, 468, "During an attack, BGP routes your prefixes to the scrubber; it drops the junk and tunnels clean traffic back. On-demand or always-on.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Anycast Absorption",
                       "Spread the flood across the planet.")
    box(c, 200, y-90, 212, 70, BOX_BLUE, "One anycast IP", "announced everywhere")
    for i, lbl in enumerate(["N. America", "Europe", "Asia"]):
        box(c, 72 + i*152, y-240, 140, 70, BOX_TEAL, lbl, "absorbs local share")
        arrow(c, 306, y-92, 142 + i*152, y-168, color=ACCENT, width=2)
    note(c, 72, y-330, 468, "Attackers in each region hit their nearest PoP — no single link takes the full blast. This is why edge networks matter.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Rate-Based & L7 Defense",
                       "Application-layer attacks need application-layer answers.")
    y = bullet_list(c, 72, y, [
        "Rate limit per IP, per session, per endpoint — login and search are favorite targets.",
        "Challenge suspicious clients: JS challenge, CAPTCHA, proof-of-work before expensive work.",
        "Cache aggressively — a cached response costs you nothing under flood.",
        "Bot management: distinguish good bots (search) from bad (scrapers, credential stuffers)."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Always-On vs On-Demand",
                       "Pick your posture before the attack.")
    box(c, 72, y-110, 224, 100, BOX_GREEN, "Always-on", "Traffic always scrubbed. Zero switchover delay; constant cost.")
    box(c, 316, y-110, 224, 100, BOX_ORANGE, "On-demand", "Scrubbing activates on detection. Cheaper idle; minutes of pain during spin-up.")
    note(c, 72, y-250, 468, "High-value targets choose always-on. Everyone else: on-demand WITH tested runbooks and pre-signed BGP authorization.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "DDoS Readiness Checklist",
                       "Do this on a quiet Tuesday, not during the flood.")
    y = bullet_list(c, 72, y, [
        "Know your baseline: normal pps, bandwidth, request mix per endpoint.",
        "Pre-authorize traffic rerouting with your provider; test the runbook quarterly.",
        "Origin protection: never expose origin IPs (DNS history leaks them — rotate after).",
        "Have a comms plan: status page, customer notice, who declares the incident."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "DDoS Mitigation — Remember",
                 ["Attacks hit three layers: volumetric, protocol, application — defend all three.",
                  "Scrubbing centers filter floods at scale via BGP rerouting.",
                  "Anycast spreads the blast across regions so no single link drowns.",
                  "L7 needs rate limits, challenges, caching, and bot management.",
                  "Choose always-on vs on-demand deliberately; rehearse the runbook.",
                  "Hide origin IPs and know your traffic baseline before you need it."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 9. SQL Injection Prevention
def pdf_sqli(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SQL Injection Prevention\nVisual Guide",
               "The oldest web attack still works —\nhere's how to kill it for good.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Injection Mechanics",
                       "User input becomes code when you concatenate strings.")
    box(c, 72, y-80, 230, 70, BOX_RED, "query = \"...\" + input", "attacker input: ' OR '1'='1")
    box(c, 340, y-80, 200, 70, BOX_ORANGE, "Database", "runs attacker's logic")
    arrow(c, 302, y-45, 340, y-45, color=RED, width=3)
    note(c, 72, y-180, 468, "The database can't tell your SQL apart from the attacker's — it's one string by the time it arrives. The fix: never build SQL by concatenation.", BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Parameterized Queries",
                       "Code and data travel separately — injection becomes impossible.")
    box(c, 72, y-80, 230, 70, BOX_BLUE, "SQL template", "WHERE user = ?")
    box(c, 340, y-80, 200, 70, BOX_GREEN, "Parameters", "bound separately, never parsed")
    arrow(c, 302, y-45, 340, y-45, color=GREEN, width=2.5, label="bound, not concatenated")
    note(c, 72, y-180, 468, "Placeholders (?, :name, $1) keep input as pure data. This single practice eliminates ~all classic SQLi.", BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "ORM Safety & Raw Queries",
                       "ORMs help — until you bypass them.")
    y = bullet_list(c, 72, y, [
        "ORM query builders parameterize automatically — prefer them over raw SQL.",
        "Danger zone: raw()/execute() with f-strings or % formatting — audit every use.",
        "Even with ORMs, validate sort/filter field names against an allowlist (no dynamic column names from input).",
        "Stored procedures help only if they also use parameters internally."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Least-Privilege DB Users",
                       "Assume injection happens — limit the blast radius.")
    box(c, 72, y-100, 150, 90, BOX_BLUE, "App user", "SELECT/INSERT/UPDATE only")
    box(c, 240, y-100, 150, 90, BOX_RED, "Never", "no DROP/ALTER, no DBA, no file read")
    box(c, 408, y-100, 132, 90, BOX_GREEN, "Migrations", "separate privileged user")
    note(c, 72, y-220, 468, "An injected query can only do what the DB user can do. A read-only reporting user can't drop tables.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Defense in Depth",
                       "Layers around the primary fix.")
    y = bullet_list(c, 72, y, [
        "WAF with SQLi rules: catches noisy probes, not a substitute for parameters.",
        "Input validation: type, length, format checks — defense, not the fix.",
        "Error handling: generic errors to users; detailed errors only in logs (no schema leaks).",
        "Monitoring: alert on SQL error spikes and suspicious query patterns."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Testing Checklist",
                       "Prove it's dead, don't assume.")
    y = bullet_list(c, 72, y, [
        "SAST rules flag string-concatenated SQL in CI — break the build.",
        "DAST/pentest with SQLi payloads against every input: forms, headers, APIs.",
        "Code review: grep for raw SQL execution; each hit needs a justification.",
        "Re-test after refactors — one 'quick' raw query reopens the hole."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SQL Injection — Remember",
                 ["Injection happens when input is concatenated into SQL strings.",
                  "Parameterized queries separate code from data — the definitive fix.",
                  "ORMs are safe until you drop to raw SQL; audit every raw() call.",
                  "Least-privilege DB users contain the damage if injection ever lands.",
                  "Add WAF, validation, and safe errors as layers — not substitutes.",
                  "Test continuously: SAST in CI, DAST payloads, and code review."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 10. XSS Prevention
def pdf_xss(path):
    c = new_canvas(path); pg = 1
    title_page(c, "XSS Prevention\nVisual Guide",
               "Cross-Site Scripting —\nstop attacker scripts running in your users' browsers.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "The Three XSS Types",
                       "Same payload, three delivery routes.")
    box(c, 72, y-110, 150, 100, BOX_RED, "Reflected", "Payload in URL → bounced back immediately. Phishing link.")
    box(c, 240, y-110, 150, 100, BOX_ORANGE, "Stored", "Payload saved in DB → served to every visitor. Worst blast.")
    box(c, 408, y-110, 132, 100, BOX_PURP, "DOM-based", "JS builds page from input client-side. No server round-trip.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Output Encoding by Context",
                       "Escape for WHERE the data lands, not just that it exists.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "HTML body", "escape < > & quotes")
    box(c, 240, y-80, 150, 70, BOX_TEAL, "Attribute", "quote-encode")
    box(c, 408, y-80, 132, 70, BOX_GREEN, "JavaScript", "\\u-encode")
    note(c, 72, y-180, 468, "HTML-encoding inside a script block does nothing — the browser still runs it. Context-aware encoding (or a framework that does it) is the fix.", BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Content-Security-Policy",
                       "A browser-enforced allowlist for what may execute.")
    box(c, 72, y-80, 468, 70, BOX_GREEN, "Content-Security-Policy: default-src 'self'; script-src 'self'", "header sent with every page")
    y = bullet_list(c, 72, y-190, [
        "Blocks inline scripts and unknown origins — kills most XSS payloads even if injected.",
        "Start with report-only mode; fix violations before enforcing.",
        "Add nonces/hashes for the few inline scripts you truly need."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Input Handling Done Right",
                       "Validate on the way in, encode on the way out.")
    box(c, 72, y-80, 220, 70, BOX_BLUE, "Input", "validate: type, length, allowlist")
    box(c, 330, y-80, 210, 70, BOX_GREEN, "Output", "context-aware encode")
    arrow(c, 292, y-45, 330, y-45, color=ACCENT, width=2.5)
    note(c, 72, y-180, 468, "Store raw input, encode at render time. Encoding at storage corrupts data and still misses contexts.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Cookie Defenses",
                       "Shrink what a successful XSS can steal.")
    y = bullet_list(c, 72, y, [
        "HttpOnly: cookies invisible to JavaScript — XSS can't read the session token.",
        "Secure: cookies only over HTTPS. SameSite=Lax/Strict: not sent on cross-site requests.",
        "Prefer short-lived tokens + refresh rotation over giant session cookies.",
        "These don't stop XSS — they limit it to actions, not full account theft."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Frameworks & Testing",
                       "Let the framework do the escaping — then verify.")
    y = bullet_list(c, 72, y, [
        "Modern frameworks auto-escape by default — danger only at raw-HTML APIs (innerHTML, dangerouslySetInnerHTML).",
        "Audit every raw-HTML escape hatch; sanitize with a proven library if user HTML is required.",
        "DAST scans and manual testing with polyglot payloads across all three XSS types.",
        "Monitor CSP violation reports — they're an early warning radar for injection attempts."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "XSS — Remember",
                 ["Three types: reflected (URL), stored (database), DOM-based (client JS).",
                  "Encode output for its context — HTML, attribute, and JS need different escaping.",
                  "Content-Security-Policy blocks injected scripts at the browser level.",
                  "Validate input, encode at render time; never encode at storage.",
                  "HttpOnly + Secure + SameSite cookies contain the damage.",
                  "Avoid raw-HTML APIs; test with DAST and watch CSP reports."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 11. CSRF & SSRF
def pdf_csrf_ssrf(path):
    c = new_canvas(path); pg = 1
    title_page(c, "CSRF & SSRF\nVisual Guide",
               "Cross-Site Request Forgery &\nServer-Side Request Forgery —\nwhen requests lie about their origin.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "CSRF Mechanics",
                       "Your browser, the attacker's request.")
    box(c, 72, y-80, 140, 70, BOX_RED, "Evil site", "hidden form")
    box(c, 252, y-80, 140, 70, BOX_BLUE, "Your browser", "sends cookies auto")
    box(c, 432, y-80, 108, 70, BOX_GREEN, "Your bank", "sees valid session")
    arrow(c, 212, y-45, 252, y-45, color=RED, width=2.5, label="visit")
    arrow(c, 392, y-45, 432, y-45, color=RED, width=2.5, label="forged POST")
    note(c, 72, y-180, 468, "Cookies go along automatically — the server can't tell your click from the attacker's. State-changing requests need proof of intent.", BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "CSRF Defenses",
                       "Tokens + SameSite cookies end it.")
    box(c, 72, y-110, 224, 100, BOX_GREEN, "CSRF tokens", "Unpredictable per-session token in every form/API call; server rejects mismatches.")
    box(c, 316, y-110, 224, 100, BOX_BLUE, "SameSite cookies", "Lax/Strict: browser won't send cookies on cross-site requests.")
    note(c, 72, y-250, 468, "SameSite is the seatbelt, tokens are the airbag — deploy both. GET requests must never change state.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "SSRF Mechanics",
                       "Trick YOUR server into attacking your network.")
    box(c, 72, y-80, 170, 70, BOX_RED, "Attacker", "url=http://169.254…")
    box(c, 282, y-80, 140, 70, BOX_ORANGE, "Your server", "fetches the URL")
    box(c, 462, y-80, 78, 70, BOX_PURP, "Metadata", "cloud creds leak")
    arrow(c, 242, y-45, 282, y-45, color=RED, width=2.5)
    arrow(c, 422, y-45, 462, y-45, color=RED, width=2.5)
    note(c, 72, y-180, 468, "Cloud metadata endpoints (169.254.169.254) hand out credentials to anything that asks — including your tricked server.", BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "SSRF Defenses",
                       "Never let user input choose server destinations freely.")
    y = bullet_list(c, 72, y, [
        "Allowlist egress: only fetch from approved hosts/schemes; deny by default.",
        "Block private ranges: 10/8, 172.16/12, 192.168/16, 169.254/16, localhost.",
        "Resolve-then-validate: DNS-rebinding defeats naive hostname checks — validate the IP too.",
        "Disable metadata endpoint access (IMDSv2 with hop limits) as a backstop."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "CSRF vs SSRF at a Glance",
                       "Mirror images: one abuses the browser, one abuses the server.")
    box(c, 72, y-110, 224, 100, BOX_BLUE, "CSRF", "Attacker → victim's browser → your app. Fix: tokens + SameSite.")
    box(c, 316, y-110, 224, 100, BOX_ORANGE, "SSRF", "Attacker → your server → internal targets. Fix: allowlist + IP validation.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Request-Forgery Checklist",
                       "Cover both sides of the mirror.")
    y = bullet_list(c, 72, y, [
        "Every state-changing endpoint requires a CSRF token; cookies are SameSite=Lax+.",
        "Server-side fetches use an allowlisted egress proxy — no raw user URLs.",
        "Private IP ranges blocked at the fetch layer AND the firewall.",
        "Test both with dedicated payloads in every pentest and DAST run."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "CSRF & SSRF — Remember",
                 ["CSRF rides your browser's automatic cookies — prove intent with tokens.",
                  "SameSite cookies + CSRF tokens together; GETs never change state.",
                  "SSRF tricks your server into fetching internal targets like metadata endpoints.",
                  "Allowlist egress destinations; block private IP ranges; validate resolved IPs.",
                  "Harden cloud metadata (IMDSv2) as a backstop against credential theft.",
                  "Test both forgery types in every security assessment."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 12. Vault (Secrets Management)
def pdf_vault(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Secrets Management\nwith Vault\nVisual Guide",
               "Dynamic secrets, leases, rotation —\nstop hardcoding credentials forever.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Dynamic Secrets",
                       "Credentials minted on demand, dead on arrival's schedule.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "App", "requests DB creds")
    box(c, 262, y-80, 140, 70, BOX_PURP, "Vault", "creates user/pass")
    box(c, 442, y-80, 98, 70, BOX_GREEN, "Database", "trusts Vault")
    arrow(c, 222, y-45, 262, y-45, color=ACCENT, width=2.5)
    arrow(c, 402, y-45, 442, y-45, color=ACCENT, width=2.5)
    note(c, 72, y-180, 468, "Each app instance gets UNIQUE, short-lived credentials. A leaked password is useless within minutes — and you know exactly which lease leaked.", BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Leases & Renewal",
                       "Every secret has a countdown.")
    box(c, 72, y-80, 130, 70, BOX_GREEN, "Issued", "TTL: 1h")
    box(c, 240, y-80, 130, 70, BOX_ORANGE, "Renewed", "TTL extended")
    box(c, 408, y-80, 132, 70, BOX_RED, "Revoked", "cred dies")
    arrow(c, 202, y-45, 240, y-45, color=ACCENT, width=2.5, label="renew")
    arrow(c, 370, y-45, 408, y-45, color=RED, width=2.5, label="expiry")
    note(c, 72, y-180, 468, "Apps renew leases while healthy; dead apps' secrets auto-expire. Revocation is instant and centralized — one call kills every copy.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Automatic Rotation",
                       "Secrets change themselves on a schedule.")
    y = bullet_list(c, 72, y, [
        "Static secrets (API keys, passwords) rotate on a timer — weekly, not yearly.",
        "Rotation writes the new value to BOTH Vault and the target system atomically.",
        "Apps always read the current value from Vault — never cache secrets in config.",
        "Break-glass: rotate immediately on any suspected exposure, then investigate."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Auth Methods",
                       "How callers prove they deserve secrets.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "Platform", "K8s / cloud IAM")
    box(c, 240, y-80, 150, 70, BOX_GREEN, "Human", "OIDC / SSO")
    box(c, 408, y-80, 132, 70, BOX_ORANGE, "Machine", "AppRole / TLS certs")
    note(c, 72, y-180, 468, "Machines authenticate with platform identity (service accounts), humans via SSO. Long-lived tokens are the last resort, tightly scoped.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Policies: Least Privilege for Secrets",
                       "Every identity sees only what it needs.")
    box(c, 72, y-80, 468, 70, BOX_PURP, 'path "secret/data/payments/*" { capabilities = ["read"] }', "policy snippet")
    y = bullet_list(c, 72, y-190, [
        "Bind policies to auth identity: the payments service reads payments secrets only.",
        "Deny by default; no wildcards in production policies.",
        "Audit every read — anomalous secret access is an early breach signal."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Seal, HA & Backup",
                       "Vault guards the guards — operate it carefully.")
    y = bullet_list(c, 72, y, [
        "Unseal requires multiple key shares (Shamir) — no single operator opens Vault alone.",
        "Run HA (Raft) across zones; back up encrypted snapshots offsite regularly.",
        "Monitor: seal status, lease counts, audit device health — Vault down means deploys stall.",
        "Disaster recovery: rehearse restore from snapshot before you need it."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Vault Secrets — Remember",
                 ["Dynamic secrets: unique, short-lived credentials per consumer — leaks self-heal.",
                  "Leases give every secret a TTL; renewal for the living, revocation for the dead.",
                  "Rotate static secrets automatically; apps always read live from Vault.",
                  "Authenticate machines with platform identity, humans with SSO.",
                  "Policies enforce least privilege; audit every secret read.",
                  "Shamir unseal, HA, and rehearsed backups keep Vault itself resilient."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 13. Container Security
def pdf_container(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Container Security\nVisual Guide",
               "From image to runtime —\nlock down every layer of the container stack.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Image Scanning in the Pipeline",
                       "Catch vulnerable layers before they deploy.")
    box(c, 72, y-80, 130, 70, BOX_BLUE, "Build", "Dockerfile")
    box(c, 240, y-80, 140, 70, BOX_ORANGE, "Scan", "CVE database")
    box(c, 418, y-80, 122, 70, BOX_GREEN, "Registry", "clean only")
    arrow(c, 202, y-45, 240, y-45, color=ACCENT, width=2.5)
    arrow(c, 380, y-45, 418, y-45, color=GREEN, width=2.5, label="gate")
    note(c, 72, y-180, 468, "Fail the build on critical CVEs with fixes available. Rescan on a schedule — new CVEs appear in old images daily.", BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Least-Privilege Users",
                       "Containers don't need to be root.")
    box(c, 72, y-80, 220, 70, BOX_RED, "USER root (default)", "escape = host root")
    box(c, 330, y-80, 210, 70, BOX_GREEN, "USER app (uid 1000)", "escape = unprivileged")
    note(c, 72, y-180, 468, "Add 'USER app' to every Dockerfile. A container escape as root owns the host; as an unprivileged user it's a contained nuisance.", BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Read-Only Filesystems",
                       "If it can't be written, it can't be backdoored.")
    y = bullet_list(c, 72, y, [
        "Run containers with read-only root filesystems — malware can't persist.",
        "Mount writable tmpfs only where the app genuinely needs scratch space.",
        "Drop /proc and /sys writes; mount secrets as read-only volumes, never env vars in images.",
        "Verify at deploy: admission policy rejects containers without readOnlyRootFilesystem."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "seccomp & AppArmor",
                       "Shrink the syscalls a container may invoke.")
    box(c, 72, y-110, 224, 100, BOX_PURP, "seccomp", "Allowlist of syscalls (default profile blocks ~44 dangerous ones).")
    box(c, 316, y-110, 224, 100, BOX_TEAL, "AppArmor", "Path-based mandatory access control per container.")
    note(c, 72, y-250, 468, "Exploits need syscalls — fewer available syscalls means fewer usable exploit primitives. Enable the defaults everywhere.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Never Privileged",
                       "The flags that delete your isolation.")
    y = bullet_list(c, 72, y, [
        "--privileged gives the container nearly all host capabilities — treat as root on the host.",
        "Drop ALL capabilities, then add back only the minimum (usually none).",
        "No hostPath mounts, no hostNetwork, no hostPID in multi-tenant clusters.",
        "Enforce with policy engines (admission controllers) — don't rely on convention."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Runtime Protection",
                       "Defense doesn't stop at deploy time.")
    y = bullet_list(c, 72, y, [
        "Runtime scanners watch for unexpected processes, network calls, file writes.",
        "Image signing + admission: only signed images from your registry may run.",
        "Network policies: default-deny between namespaces; allow only declared flows.",
        "Keep the host and runtime patched — container escapes target kernel bugs."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Container Security — Remember",
                 ["Scan images in CI and gate on critical CVEs; rescan continuously.",
                  "Run as non-root — 'USER app' in every Dockerfile.",
                  "Read-only filesystems with tmpfs scratch; secrets as volumes, not env.",
                  "Enable seccomp and AppArmor defaults to shrink the attack surface.",
                  "Never --privileged; drop all capabilities; enforce via admission policy.",
                  "Sign images, default-deny network, and monitor runtime behavior."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 14. Supply Chain Security
def pdf_supply_chain(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Supply Chain Security\nVisual Guide",
               "Your code is 90% someone else's —\nsecure the chain you build on.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "The Dependency Reality",
                       "Every deploy inherits every dependency's risk.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "Your code", "10%")
    box(c, 262, y-80, 140, 70, BOX_ORANGE, "Direct deps", "you chose them")
    box(c, 442, y-80, 98, 70, BOX_RED, "Transitive", "you didn't")
    arrow(c, 222, y-45, 262, y-45, color=ACCENT, width=2.2)
    arrow(c, 402, y-45, 442, y-45, color=RED, width=2.5)
    note(c, 72, y-180, 468, "Transitive dependencies are the blind spot — typosquats and compromised maintainers hide there. Visibility is step one.", BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "SBOM: Know Your Ingredients",
                       "A software bill of materials for every artifact.")
    box(c, 72, y-80, 468, 70, BOX_TEAL, "SBOM (CycloneDX / SPDX)", "every component + version + license, machine-readable")
    y = bullet_list(c, 72, y-190, [
        "Generate the SBOM at build time — it must match what actually shipped.",
        "When a CVE drops, query SBOMs to find exposure in minutes, not weeks.",
        "Share SBOMs with customers; demand them from vendors."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Artifact Signing with Sigstore",
                       "Prove the artifact is really yours, keylessly.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "Build", "CI identity (OIDC)")
    box(c, 262, y-80, 140, 70, BOX_GREEN, "Sigstore", "short-lived cert")
    box(c, 442, y-80, 98, 70, BOX_PURP, "Signed", "verifiable")
    arrow(c, 222, y-45, 262, y-45, color=ACCENT, width=2.5)
    arrow(c, 402, y-45, 442, y-45, color=GREEN, width=2.5)
    note(c, 72, y-180, 468, "Keyless signing ties the signature to the CI workload's identity — no long-lived keys to steal, and verifiers check a public transparency log.", BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Pinning & Lockfiles",
                       "Reproducible builds beat floating versions.")
    y = bullet_list(c, 72, y, [
        "Commit lockfiles — every build resolves the exact same dependency tree.",
        "Pin to hashes/digests for base images, not floating tags like 'latest'.",
        "Review dependency updates like code changes: diff, changelog, test.",
        "Automate updates (renovate/dependabot) but keep humans approving majors."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Provenance & SLSA",
                       "Attest HOW the artifact was built, not just what it is.")
    box(c, 72, y-110, 224, 100, BOX_PURP, "Provenance", "Signed record: source commit, builder, build steps, materials.")
    box(c, 316, y-110, 224, 100, BOX_BLUE, "SLSA levels", "L1: provenance exists → L4: hermetic, reproducible builds.")
    note(c, 72, y-250, 468, "A verifier can confirm: this binary came from this repo, built by this pipeline, from these inputs. Tampering anywhere breaks the chain.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Policy Gates",
                       "Make the pipeline enforce the rules.")
    y = bullet_list(c, 72, y, [
        "Admission: only signed artifacts with valid provenance may deploy.",
        "Block known-malicious packages and licenses via policy at pull time.",
        "Private registry proxy: vet once, serve internally — no direct public pulls in prod builds.",
        "Incident drill: practice the 'compromised dependency' response before it happens."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Supply Chain — Remember",
                 ["Your risk includes transitive dependencies you never chose — get visibility first.",
                  "Ship an SBOM with every artifact; use it for instant CVE exposure checks.",
                  "Sign artifacts keylessly (Sigstore) and record build provenance (SLSA).",
                  "Pin versions, commit lockfiles, review dependency updates like code.",
                  "Gate deploys on signatures + provenance; proxy public registries.",
                  "Rehearse the compromised-dependency response before you need it."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 15. SAST & DAST
def pdf_sast_dast(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SAST & DAST\nVisual Guide",
               "Static + Dynamic testing —\nfind bugs in code and in running apps.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "SAST: Reading the Code",
                       "Static analysis — no execution, just reasoning about source.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "IDE", "as you type")
    box(c, 262, y-80, 140, 70, BOX_PURP, "CI gate", "on every PR")
    box(c, 442, y-80, 98, 70, BOX_GREEN, "Fix", "cheapest here")
    arrow(c, 222, y-45, 262, y-45, color=ACCENT, width=2.5)
    arrow(c, 402, y-45, 442, y-45, color=GREEN, width=2.5)
    note(c, 72, y-180, 468, "SAST finds: injection flaws, hardcoded secrets, insecure crypto, taint-flow bugs. Fix cost rises 10x+ after merge — catch it in the IDE.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "DAST: Attacking the Running App",
                       "Dynamic analysis — real HTTP against a live deployment.")
    box(c, 72, y-80, 200, 70, BOX_ORANGE, "Scanner", "crawls + fuzzes")
    box(c, 312, y-80, 228, 70, BOX_GREEN, "Running app (staging)", "responds for real")
    arrow(c, 272, y-45, 312, y-45, color=ORANGE, width=3, label="attack traffic")
    note(c, 72, y-180, 468, "DAST finds: auth bypasses, session issues, server misconfig, XSS/SQLi that only manifest at runtime. Needs a faithful staging environment.", BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Shift-Left Timeline",
                       "When each technique pays off.")
    box(c, 72, y-80, 120, 70, BOX_BLUE, "IDE", "SAST instant")
    box(c, 212, y-80, 120, 70, BOX_PURP, "PR/CI", "SAST + SCA")
    box(c, 352, y-80, 120, 70, BOX_ORANGE, "Staging", "DAST")
    arrow(c, 192, y-45, 212, y-45, color=ACCENT, width=2.2)
    arrow(c, 332, y-45, 352, y-45, color=ACCENT, width=2.2)
    note(c, 72, y-180, 468, "Cost of a fix grows left→right. SAST everywhere, DAST on every staging deploy, pentest on major releases.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Don't Forget SCA",
                       "Software composition analysis — SAST for your dependencies.")
    y = bullet_list(c, 72, y, [
        "SCA scans lockfiles against CVE databases on every build.",
        "Prioritize reachable + exploitable vulns over raw CVE counts.",
        "Auto-PR safe upgrades; track the rest with SLAs by severity.",
        "SBOM out, CVE feed in — SCA closes the loop on supply chain."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Triage Without Drowning",
                       "Scanners are noisy — tune the signal.")
    y = bullet_list(c, 72, y, [
        "Break builds only on high-confidence, high-severity findings at first.",
        "Baseline existing issues; block only NEW findings to avoid big-bang cleanup.",
        "Dedupe across tools; route to the owning team with fix guidance attached.",
        "Track false-positive rates per rule — disable or tune chronic noisemakers."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "The Combined Pipeline",
                       "One flow, all three scanners.")
    box(c, 72, y-80, 468, 64, BOX_BLUE, "PR → SAST + SCA gate (block on new highs)", "developer feedback in minutes")
    box(c, 72, y-164, 468, 64, BOX_ORANGE, "Staging deploy → DAST scan (block on criticals)", "runtime truth before prod")
    box(c, 72, y-248, 468, 64, BOX_GREEN, "Release → pentest sample + continuous rescan", "humans where automation stops")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SAST & DAST — Remember",
                 ["SAST reads code (IDE/CI) — cheapest fixes; DAST attacks running apps (staging) — runtime truth.",
                  "Shift left: the earlier the find, the cheaper the fix.",
                  "Add SCA for dependencies — vulnerable libraries are the top finding source.",
                  "Baseline and block only new findings; tune noisy rules instead of ignoring them.",
                  "Pipeline: SAST+SCA on PRs, DAST on staging, pentest on releases.",
                  "No scanner replaces threat modeling and manual review for logic flaws."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 16. Pentest Methodology
def pdf_pentest(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Pentest Methodology\nVisual Guide",
               "Think like an attacker —\nwith permission, scope, and a report.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "The Five Phases",
                       "Every test follows the same arc.")
    phases = [("Recon", BOX_BLUE), ("Enum", BOX_TEAL), ("Exploit", BOX_ORANGE),
              ("Post-exploit", BOX_RED), ("Report", BOX_GREEN)]
    for i, (lbl, f) in enumerate(phases):
        box(c, 72 + i*94, y-80, 86, 70, f, lbl, f"{i+1}", font_size=10)
        if i < 4: arrow(c, 72 + i*94 + 86, y-45, 72 + (i+1)*94, y-45, color=ACCENT, width=2)
    note(c, 72, y-180, 468, "Time-box each phase — rabbit holes are the #1 pentest killer. Depth matters more than breadth on the target that counts.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Recon: Learn Without Touching",
                       "Passive first — the target shouldn't feel you yet.")
    y = bullet_list(c, 72, y, [
        "OSINT: domains, subdomains, certs, DNS history, employee tech footprints.",
        "Map the attack surface: every host, API, login page, forgotten staging box.",
        "Note technologies and versions — each one is a future search query.",
        "Stay passive: no scanning yet; respect scope like it's law (it is)."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Enumeration: Touch and Catalog",
                       "Active probing — build the target model.")
    y = bullet_list(c, 72, y, [
        "Port/service scanning, banner grabs, directory and API endpoint discovery.",
        "Identify versions precisely — 'Apache 2.4.x' isn't enough; get the patch level.",
        "Enumerate users, roles, and trust relationships where the scope allows.",
        "Document everything — enumeration notes become the exploit shortlist."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Exploitation: Prove Impact",
                       "Turn a finding into a demonstrated fact.")
    box(c, 72, y-80, 220, 70, BOX_ORANGE, "Attempt", "one vuln at a time")
    box(c, 330, y-80, 210, 70, BOX_RED, "Prove", "screenshot + data accessed")
    arrow(c, 292, y-45, 330, y-45, color=ORANGE, width=2.5)
    note(c, 72, y-180, 468, "Never exploit beyond scope, never destroy data, never pivot without permission. A proved finding beats ten theoretical ones.", BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Post-Exploitation & Reporting",
                       "What access buys — and how to fix it.")
    y = bullet_list(c, 72, y, [
        "Post-exploit: demonstrate lateral movement and data reach WITHIN scope — that sells the risk.",
        "Clean up: remove shells, accounts, and artifacts; confirm with the client.",
        "Report: executive summary (risk in business terms) + technical findings (repro steps, evidence).",
        "Rate by real impact × likelihood; every finding gets a concrete remediation."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Rules of Engagement",
                       "The contract that keeps testing legal and safe.")
    y = bullet_list(c, 72, y, [
        "Written authorization with exact scope: IPs, domains, accounts, time windows.",
        "No-go list: production data destruction, DoS, social engineering — unless explicitly approved.",
        "Emergency contacts and a kill-switch phrase; test the comms channel day one.",
        "Retest after fixes — a finding isn't closed until the retest passes."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Pentest Methodology — Remember",
                 ["Five phases: recon → enumeration → exploitation → post-exploitation → reporting.",
                  "Recon passive, enumeration active — document everything for the exploit shortlist.",
                  "Exploit to prove impact, never beyond scope; clean up afterwards.",
                  "Reports speak two languages: business risk for execs, repro steps for engineers.",
                  "Rules of engagement in writing: scope, no-gos, contacts, kill-switch.",
                  "Close the loop with retesting — fixes aren't done until verified."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 17. Threat Modeling
def pdf_threat_modeling(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Threat Modeling\nVisual Guide",
               "Design-time security —\nfind the flaws before the code exists.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Start with a Data-Flow Diagram",
                       "You can't threaten what you haven't drawn.")
    box(c, 72, y-80, 120, 70, BOX_BLUE, "User", "external entity")
    box(c, 232, y-80, 140, 70, BOX_GREEN, "Web app", "process")
    box(c, 412, y-80, 128, 70, BOX_ORANGE, "Database", "data store")
    arrow(c, 192, y-45, 232, y-45, color=ACCENT, width=2.2, label="login")
    arrow(c, 372, y-45, 412, y-45, color=ACCENT, width=2.2, label="queries")
    note(c, 72, y-180, 468, "Mark trust boundaries (browser→app, app→DB) — every crossing is where threats live. Keep the diagram honest and current.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "STRIDE: The Six Threat Buckets",
                       "Walk every DFD element through all six.")
    cats = [("Spoofing", "fake identity", BOX_RED), ("Tampering", "modify data", BOX_ORANGE),
            ("Repudiation", "deny actions", BOX_PURP), ("Info disclosure", "leak data", BOX_BLUE),
            ("DoS", "deny service", BOX_TEAL), ("Elevation", "gain privilege", BOX_GREEN)]
    yy = y
    for i, (t, s, f) in enumerate(cats):
        box(c, 72 + (i % 3)*156, yy-64, 148, 68, f, t, s, font_size=10)
        if i % 3 == 2: yy -= 80
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Attack Trees",
                       "One goal, many paths — drawn as a tree.")
    box(c, 216, y-80, 180, 64, BOX_RED, "Steal customer PII", "attacker goal")
    for i, lbl in enumerate(["SQLi", "Phish admin", "Backup theft"]):
        box(c, 72 + i*156, y-200, 148, 60, BOX_ORANGE, lbl, "path", font_size=10)
        arrow(c, 306, y-82, 146 + i*156, y-138, color=RED, width=1.8)
    note(c, 72, y-290, 468, "Prune any path your controls already kill. What remains is your real residual risk — and your fix list.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Prioritize: Risk = Impact × Likelihood",
                       "Not every threat deserves a sprint.")
    box(c, 72, y-110, 224, 100, BOX_RED, "High impact", "Fix now: PII theft, auth bypass, RCE on crown jewels.")
    box(c, 316, y-110, 224, 100, BOX_ORANGE, "Lower risk", "Backlog with owners: harden opportunistically.")
    note(c, 72, y-250, 468, "Score simply (1–3 × 1–3) and move on — precision theater wastes the workshop. Revisit when the design changes.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "When to Threat Model",
                       "At design time — and at every inflection point.")
    y = bullet_list(c, 72, y, [
        "New features and architectures: model before the first line of code.",
        "Major changes: new data flows, new trust boundaries, new third parties.",
        "Lightweight for small changes (30-min whiteboard), deep for crown jewels.",
        "Make it a gate: no design review sign-off without the threat model."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Outputs That Survive",
                       "A threat model is a living document, not a meeting.")
    y = bullet_list(c, 72, y, [
        "Threat list: each with STRIDE category, affected flow, risk score, owner.",
        "Mitigations as tickets — linked, scheduled, and verified when done.",
        "Assumptions recorded explicitly (they're the threats you chose to accept).",
        "Review trigger: architecture change or calendar date, whichever comes first."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Threat Modeling — Remember",
                 ["Draw the data-flow diagram first; threats live at trust boundaries.",
                  "Run every element through STRIDE: spoofing, tampering, repudiation, disclosure, DoS, elevation.",
                  "Attack trees turn one goal into prunable paths — fix what remains.",
                  "Prioritize by impact × likelihood; keep scoring simple and fast.",
                  "Model at design time and at every architecture inflection.",
                  "Output tickets with owners, record assumptions, and re-review on change."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 18. SIEM & SOC
def pdf_siem(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SIEM & SOC Operations\nVisual Guide",
               "Collect everything, correlate smartly —\nthe security operations center playbook.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Log Sources Feed the SIEM",
                       "Visibility first — you can't detect what you don't collect.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "Endpoints", "EDR telemetry")
    box(c, 240, y-80, 150, 70, BOX_TEAL, "Network", "firewall, DNS, proxy")
    box(c, 408, y-80, 132, 70, BOX_PURP, "Identity", "IdP, VPN, SaaS")
    arrow(c, 306, y-110, 306, y-170, color=ACCENT, width=2.5)
    box(c, 206, y-240, 200, 70, BOX_GREEN, "SIEM", "normalize + store")
    note(c, 72, y-330, 468, "Normalize to a common schema with synced clocks — correlation is impossible when timestamps and field names disagree.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Correlation Rules",
                       "Single events are noise; patterns are signal.")
    box(c, 72, y-80, 468, 70, BOX_ORANGE, "5 failed logins + 1 success + new country = 'possible account takeover'", "rule example")
    y = bullet_list(c, 72, y-190, [
        "Write rules from known attacker behavior (MITRE ATT&CK is the menu).",
        "Tune thresholds per environment — the same rule fires differently in dev vs prod.",
        "Version-control rules like code; peer-review changes."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Alert Triage Tiers",
                       "Not every alert deserves a human at 3 AM.")
    box(c, 72, y-80, 150, 90, BOX_GREEN, "Tier 1", "triage: true/false positive, enrich")
    box(c, 240, y-80, 150, 90, BOX_ORANGE, "Tier 2", "investigate: scope, contain")
    box(c, 408, y-80, 132, 90, BOX_RED, "Tier 3", "hunt + engineer: fix detection gaps")
    note(c, 72, y-200, 468, "Escalation criteria in writing — Tier 1 must know exactly what goes up and what closes. Ambiguity here burns analysts out.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Playbooks & SOAR",
                       "Repeatable response, automated where safe.")
    y = bullet_list(c, 72, y, [
        "Playbook per alert type: first 15 minutes scripted (isolate, snapshot, notify).",
        "Automate enrichment (threat intel, asset context) — never automate destructive containment without approval.",
        "SOAR orchestrates: SIEM alert → enrich → ticket → isolate → notify, in minutes.",
        "Drill playbooks quarterly; a playbook nobody has run is fiction."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Metrics That Matter",
                       "Measure the SOC like an engineering team.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "MTTD", "mean time to detect")
    box(c, 240, y-80, 150, 70, BOX_ORANGE, "MTTR", "mean time to respond")
    box(c, 408, y-80, 132, 70, BOX_GREEN, "Precision", "true-positive rate")
    note(c, 72, y-180, 468, "If MTTD is months and precision is 5%, you don't have a detection program — you have a log warehouse. Fix the rules, not the analysts.", BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "The Tuning Lifecycle",
                       "Detection is never 'done'.")
    y = bullet_list(c, 72, y, [
        "Review top-noisiest rules weekly — tune or disable chronic false positives.",
        "After every incident: did we detect it? If not, write the missing rule.",
        "Threat intel feeds new rules; purple-team exercises validate them.",
        "Retire rules for decommissioned systems — stale rules are pure noise."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SIEM & SOC — Remember",
                 ["Collect broadly (endpoint, network, identity) and normalize with synced clocks.",
                  "Correlation rules turn event noise into attack patterns — source them from ATT&CK.",
                  "Tier triage with written escalation criteria; protect Tier 1 from ambiguity.",
                  "Playbooks script the first 15 minutes; automate enrichment before containment.",
                  "Track MTTD, MTTR, and precision — tune rules, don't blame analysts.",
                  "Detection is a lifecycle: tune weekly, write rules from incidents, retire the stale."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 19. EDR
def pdf_edr(path):
    c = new_canvas(path); pg = 1
    title_page(c, "EDR\nVisual Guide",
               "Endpoint Detection & Response —\nsee everything, stop attacks in progress.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Endpoint Telemetry",
                       "The sensor sees what the OS sees.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "Processes", "parent/child trees")
    box(c, 240, y-80, 150, 70, BOX_TEAL, "Network", "connections, DNS")
    box(c, 408, y-80, 132, 70, BOX_ORANGE, "Files/registry", "writes, persistence")
    note(c, 72, y-180, 468, "Rich telemetry streams to the cloud console in near-real time — months of history per endpoint, queryable in seconds.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Behavioral Detection",
                       "Catch the technique, not just the file hash.")
    box(c, 72, y-110, 224, 100, BOX_RED, "Signatures", "Known-bad hashes. Fast, blind to novel malware.")
    box(c, 316, y-110, 224, 100, BOX_GREEN, "Behavioral", "Word spawning PowerShell → encoded command = malicious pattern, whatever the hash.")
    note(c, 72, y-250, 468, "Attackers recompile in seconds — behavior is the durable signal. Map detections to MITRE ATT&CK techniques.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Response Actions",
                       "Detect is half the job — respond from the console.")
    y = bullet_list(c, 72, y, [
        "Network isolation: cut the host off but keep the EDR channel alive.",
        "Kill process trees and quarantine files remotely — seconds, not tickets.",
        "Rollback: restore encrypted/altered files from protected snapshots (vs ransomware).",
        "Collect forensic artifacts (memory, disk) before remediation wipes evidence."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "EDR vs Traditional Antivirus",
                       "Prevention-only vs detect-and-respond.")
    box(c, 72, y-110, 224, 100, BOX_ORANGE, "Antivirus", "Signature blocking at execution. Quiet when it misses — which is often, silently.")
    box(c, 316, y-110, 224, 100, BOX_GREEN, "EDR", "Continuous telemetry + behavioral detection + remote response + threat hunting.")
    note(c, 72, y-250, 468, "AV asks 'is this file known-bad?'. EDR asks 'is this behavior malicious?' — and gives you the tools to answer what happened.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Deployment & Tuning",
                       "Coverage and signal quality decide everything.")
    y = bullet_list(c, 72, y, [
        "100% coverage: every endpoint including servers, Macs, Linux — attackers find the gap.",
        "Tamper protection on: malware's first move is killing the sensor.",
        "Tune in monitor mode first; aggressive auto-isolate without tuning causes self-DoS.",
        "Test with simulated attacks regularly — an untested EDR is a hope, not a control."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Investigating an Alert",
                       "The 10-minute triage flow.")
    box(c, 72, y-80, 468, 60, BOX_BLUE, "1. Process tree — what launched what?  2. Timeline — what happened before/after?", "scope")
    box(c, 72, y-160, 468, 60, BOX_ORANGE, "3. Prevalence — one host or fifty?  4. Intel — known-bad indicators?", "blast radius")
    box(c, 72, y-240, 468, 60, BOX_GREEN, "5. Contain → collect → remediate → document", "act")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "EDR — Remember",
                 ["EDR streams process, network, and file telemetry to a queryable console.",
                  "Behavioral detection catches techniques; signatures only catch known files.",
                  "Respond remotely: isolate, kill, quarantine, rollback — in seconds.",
                  "EDR ≠ antivirus: it's detection + investigation + response, not just blocking.",
                  "Demand 100% coverage with tamper protection; tune before auto-isolating.",
                  "Triage fast: process tree, timeline, prevalence, then contain and document."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 20. Incident Response Playbooks
def pdf_ir(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Incident Response\nPlaybooks\nVisual Guide",
               "Ransomware, breaches, takeovers —\nrehearsed step-flows for the worst days.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "The IR Lifecycle",
                       "Every incident rides the same six stages.")
    stages = ["Prepare", "Detect", "Contain", "Eradicate", "Recover", "Lessons"]
    for i, lbl in enumerate(stages):
        box(c, 72 + i*78, y-80, 72, 70, [BOX_BLUE, BOX_TEAL, BOX_ORANGE, BOX_RED, BOX_GREEN, BOX_PURP][i], lbl, f"{i+1}", font_size=9)
        if i < 5: arrow(c, 72 + i*78 + 72, y-45, 72 + (i+1)*78, y-45, color=ACCENT, width=1.8)
    note(c, 72, y-180, 468, "Preparation decides the outcome: contact lists, tooling access, and backups are built on quiet days — not during the fire.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Playbook: Ransomware",
                       "Speed of containment beats perfection of analysis.")
    y = bullet_list(c, 72, y, [
        "1. ISOLATE affected hosts immediately (network, not power — preserve memory forensics).",
        "2. Identify the variant and entry point; check backups are intact and OFFLINE.",
        "3. Engage leadership + legal; decide on ransom policy BEFORE pressure peaks (default: don't pay).",
        "4. Eradicate: rebuild from known-good images, rotate all credentials.",
        "5. Recover in priority order; validate clean with EDR sweeps before reconnecting."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Playbook: Data Breach",
                       "Scope the exposure, protect the people affected.")
    y = bullet_list(c, 72, y, [
        "1. CONTAIN the exfiltration path: revoke keys, block egress, preserve logs.",
        "2. Scope: what data, whose, how many records — forensics determines this, not guesses.",
        "3. Legal + privacy drive notifications: regulators and affected individuals on legal timelines.",
        "4. Eradicate root cause; rotate everything the attacker could have touched.",
        "5. Offer support to affected users; publish an honest post-mortem."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Playbook: Account Takeover",
                       "One compromised account can be a foothold — treat it that way.")
    y = bullet_list(c, 72, y, [
        "1. LOCK the account and revoke all sessions/tokens immediately.",
        "2. Timeline the attacker's actions: logins, password/MFA changes, data accessed.",
        "3. Check for persistence: new MFA devices, forwarding rules, OAuth grants.",
        "4. Reset credentials via a verified channel — never the possibly-compromised inbox.",
        "5. Harden: phishing-resistant MFA, alert on impossible-travel logins."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Roles & Communication",
                       "Chaos is the real adversary — organization beats it.")
    box(c, 72, y-80, 150, 70, BOX_RED, "Commander", "decisions")
    box(c, 240, y-80, 150, 70, BOX_BLUE, "Comms lead", "one voice")
    box(c, 408, y-80, 132, 70, BOX_GREEN, "Scribe", "timeline log")
    note(c, 72, y-180, 468, "War-room channel, 15-minute standups, single spokesperson. Log every decision with timestamps — memory lies, timelines don't.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "After-Action: Lessons Learned",
                       "The incident isn't over when systems are back.")
    y = bullet_list(c, 72, y, [
        "Blameless review within two weeks: timeline, what worked, what failed.",
        "Every gap becomes a ticket with an owner and a date — or it will recur.",
        "Update the playbooks with what you learned; the next incident inherits the wisdom.",
        "Share sanitized lessons org-wide; security culture is built from real stories."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "IR Playbooks — Remember",
                 ["All incidents follow: prepare → detect → contain → eradicate → recover → lessons.",
                  "Ransomware: isolate fast, verify offline backups, rebuild from known-good.",
                  "Breach: contain exfiltration, scope forensically, let legal drive notifications.",
                  "Takeover: revoke sessions, hunt persistence, reset via verified channels.",
                  "Assign commander, comms, scribe; run the war room on 15-minute cadence.",
                  "Close with blameless review — every gap becomes an owned ticket."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 21. Digital Forensics Basics
def pdf_forensics(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Digital Forensics Basics\nVisual Guide",
               "Collect evidence that holds up —\nchain of custody to timeline analysis.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Chain of Custody",
                       "Evidence is worthless if you can't prove its journey.")
    box(c, 72, y-80, 140, 70, BOX_BLUE, "Seize", "who, when, where")
    box(c, 242, y-80, 140, 70, BOX_TEAL, "Hash", "SHA-256 at capture")
    box(c, 412, y-80, 128, 70, BOX_GREEN, "Log", "every access signed")
    arrow(c, 212, y-45, 242, y-45, color=ACCENT, width=2.2)
    arrow(c, 382, y-45, 412, y-45, color=ACCENT, width=2.2)
    note(c, 72, y-180, 468, "Hash at the moment of capture; re-hash before analysis. Any gap in the log is reasonable doubt.", BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Disk Acquisition & Write Blockers",
                       "Copy everything, change nothing.")
    box(c, 72, y-80, 200, 70, BOX_ORANGE, "Write blocker", "hardware: blocks all writes")
    box(c, 312, y-80, 228, 70, BOX_GREEN, "Bit-for-bit image", "every sector incl. deleted")
    arrow(c, 272, y-45, 312, y-45, color=ACCENT, width=2.5)
    note(c, 72, y-180, 468, "Analyze the COPY, never the original. Booting a suspect drive alters timestamps — the evidence starts degrading the moment it powers on.", BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Memory Acquisition",
                       "RAM holds what disk never sees.")
    y = bullet_list(c, 72, y, [
        "Capture memory FIRST — it vanishes on shutdown (running processes, keys, connections).",
        "Memory reveals: injected code, decrypted payloads, active C2 sessions.",
        "Use trusted capture tools from external media; each tool leaves its own footprint — document it.",
        "Order of volatility: memory → network → disk. Collect in that order."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Timeline Analysis",
                       "Reconstruct the story from timestamps.")
    box(c, 72, y-80, 468, 64, BOX_PURP, "Super-timeline: filesystem + logs + registry + browser, merged and sorted", "one chronological view")
    y = bullet_list(c, 72, y-180, [
        "Anchor on known-good events, then walk outward to the suspicious.",
        "Correlate across sources: a file created at 02:14 matches the 02:14 firewall deny.",
        "Watch for timestomping — attackers forge timestamps; cross-check multiple sources."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Evidence Handling Rules",
                       "Discipline that survives cross-examination.")
    y = bullet_list(c, 72, y, [
        "Least privilege: only examiners touch originals; everyone else gets copies.",
        "Document every tool and command — reproducibility is credibility.",
        "Store originals sealed, hashed, and access-logged; encrypt in transit.",
        "Never work on live suspect systems longer than necessary to capture."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "From Findings to Report",
                       "Facts first, opinions labeled.")
    y = bullet_list(c, 72, y, [
        "Report states WHAT was found and HOW (method, hashes) — not who to blame.",
        "Separate observed facts from analyst inferences, clearly marked.",
        "Include limitations: what wasn't captured, what couldn't be recovered.",
        "Preserve everything — cases reopen, and spoliation destroys credibility."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Forensics — Remember",
                 ["Chain of custody: seize, hash at capture, log every access.",
                  "Write-block the original; analyze only bit-for-bit copies.",
                  "Capture memory first — order of volatility: RAM, network, disk.",
                  "Build super-timelines merging all sources; cross-check for timestomping.",
                  "Document every tool and command; reproducibility is credibility.",
                  "Report facts vs inferences separately; preserve everything."], pg)
    c.save(); print("wrote", path)


# ---------------------------------------------------------------- 22. SOC 2 & PCI-DSS
def pdf_compliance(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SOC 2 & PCI-DSS\nVisual Guide",
               "Trust criteria and card-data rules —\nturn audits from fire drills into routine.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "SOC 2: Trust Services Criteria",
                       "Five lenses auditors use to judge your controls.")
    cats = [("Security", "the baseline — required", BOX_RED), ("Availability", "uptime commitments", BOX_ORANGE),
            ("Processing Integrity", "correct processing", BOX_BLUE), ("Confidentiality", "protect secrets", BOX_PURP),
            ("Privacy", "personal info handling", BOX_TEAL)]
    yy = y
    for i, (t, s, f) in enumerate(cats):
        box(c, 72 + (i % 2)*240, yy-58, 228, 62, f, t, s, font_size=10.5)
        if i % 2 == 1: yy -= 74
    note(c, 72, yy-80, 468, "Type I = controls designed well at a point in time. Type II = operating effectively over 6–12 months. Customers want Type II.", BOX_BLUE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "PCI-DSS: Requirements Map",
                       "Twelve requirements in four groups — all about card data.")
    box(c, 72, y-80, 228, 70, BOX_BLUE, "1–2: Network", "firewalls, no defaults")
    box(c, 320, y-80, 220, 70, BOX_GREEN, "3–4: Protect data", "encrypt stored + transit")
    box(c, 72, y-170, 228, 70, BOX_ORANGE, "7–9: Access control", "least privilege, physical")
    box(c, 320, y-170, 220, 70, BOX_RED, "10–12: Monitor + policy", "logging, testing, program")
    note(c, 72, y-260, 468, "Scope rule: shrink the cardholder data environment (CDE) — network segmentation means fewer systems in audit scope.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Evidence Collection",
                       "Auditors believe artifacts, not assertions.")
    y = bullet_list(c, 72, y, [
        "Map each control to evidence: screenshots, configs, logs, tickets, attestations.",
        "Collect continuously — a control with 11 months of evidence and a gap in month 6 fails.",
        "Automate: pull configs and access reviews from APIs into your evidence locker.",
        "Name and date everything; an auditor should never ask 'what is this?'."])
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Audit Prep Timeline",
                       "Start months before the auditor arrives.")
    box(c, 72, y-80, 150, 70, BOX_BLUE, "T-6 months", "gap assessment")
    box(c, 240, y-80, 150, 70, BOX_ORANGE, "T-3 months", "remediate + collect")
    box(c, 408, y-80, 132, 70, BOX_GREEN, "T-1 month", "dry run")
    arrow(c, 222, y-45, 240, y-45, color=ACCENT, width=2.2)
    arrow(c, 390, y-45, 408, y-45, color=ACCENT, width=2.2)
    note(c, 72, y-180, 468, "Readiness assessments find the gaps cheaply. Walking into a Type II audit cold is how you buy a qualified opinion.", BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Shared Responsibility",
                       "Cloud doesn't outsource compliance.")
    box(c, 72, y-110, 224, 100, BOX_BLUE, "Provider", "physical, hypervisor, managed-service controls (their SOC 2 helps you).")
    box(c, 316, y-110, 224, 100, BOX_GREEN, "You", "data, access, configs, apps — always your responsibility.")
    note(c, 72, y-250, 468, "Collect your providers' attestations as YOUR evidence — but the auditor still holds you accountable for what's in your account.", BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Controls That Serve Two Masters",
                       "One control set, multiple audits.")
    y = bullet_list(c, 72, y, [
        "Map once: a single access-review process evidences SOC 2 CC6.1 AND PCI Req 7.",
        "Common control framework (CCM/ISO 27001) as the spine; each audit reads off it.",
        "Avoid audit-specific theater — real controls pass every framework.",
        "Continuous compliance: monitor controls year-round, not audit-season."])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SOC 2 & PCI-DSS — Remember",
                 ["SOC 2 judges five trust criteria; Type II (operating over time) is what customers want.",
                  "PCI-DSS's 12 requirements protect card data — shrink the CDE to shrink scope.",
                  "Evidence wins audits: collect continuously, automate pulls, label everything.",
                  "Prep timeline: gap assessment at T-6mo, remediate at T-3, dry run at T-1.",
                  "Cloud is shared responsibility — provider attestations are your evidence, not your excuse.",
                  "One control framework mapped to many audits beats per-audit theater."], pg)
    c.save(); print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    jobs = [
        (pdf_oidc_saml, "bbg-oidc-saml.pdf"),
        (pdf_jwt, "bbg-jwt.pdf"),
        (pdf_mfa, "bbg-mfa.pdf"),
        (pdf_password_hashing, "bbg-password-hashing.pdf"),
        (pdf_hmac, "bbg-hmac-signatures.pdf"),
        (pdf_kms_hsm, "bbg-kms-hsm.pdf"),
        (pdf_waf, "bbg-waf.pdf"),
        (pdf_ddos, "bbg-ddos.pdf"),
        (pdf_sqli, "bbg-sqli.pdf"),
        (pdf_xss, "bbg-xss.pdf"),
        (pdf_csrf_ssrf, "bbg-csrf-ssrf.pdf"),
        (pdf_vault, "bbg-vault.pdf"),
        (pdf_container, "bbg-container-security.pdf"),
        (pdf_supply_chain, "bbg-supply-chain.pdf"),
        (pdf_sast_dast, "bbg-sast-dast.pdf"),
        (pdf_pentest, "bbg-pentest.pdf"),
        (pdf_threat_modeling, "bbg-threat-modeling.pdf"),
        (pdf_siem, "bbg-siem.pdf"),
        (pdf_edr, "bbg-edr.pdf"),
        (pdf_ir, "bbg-ir-playbooks.pdf"),
        (pdf_forensics, "bbg-forensics.pdf"),
        (pdf_compliance, "bbg-compliance.pdf"),
    ]
    for fn, name in jobs:
        fn(os.path.join(out, name))
    print(f"DONE: {len(jobs)} PDFs")
