"""Batch 4: Security PDFs — Zero Trust, PKI/Encryption, OAuth 2.0."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


def pdf_zero_trust(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Zero Trust\nArchitecture",
               "Never trust, always verify.\nSecurity for a world without perimeters.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "The Old Model: Castle and Moat",
                       "Hard shell, soft center — once inside, attackers roam free.")
    # castle diagram
    c.setFillColor(BOX_RED); c.roundRect(216, 380, 180, 120, 10, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 12)
    c.drawCentredString(306, 470, "Corporate Network")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 450, "flat • implicit trust")
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(306, 420, "attacker inside → game over")
    box(c, 72, 380, 110, 60, BOX_BLUE, "Firewall", "the moat")
    arrow(c, 182, 410, 214, 410, color=ACCENT)
    note(c, 72, 280, 468, "VPNs extend the moat to homes and cafes — but the inside is still implicitly trusted. Lateral movement is trivial.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "The Zero Trust Principle",
                       "No implicit trust — not for users, devices, networks, or workloads.")
    principles = [("Verify explicitly", "Authenticate + authorize every request: identity, device health, context.", BOX_BLUE),
                  ("Least privilege", "Just-in-time, just-enough access. No standing admin.", BOX_GREEN),
                  ("Assume breach", "Segment so a compromise stays contained; monitor everything.", BOX_RED)]
    yy = y
    for name, desc, fill in principles:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=12)
        yy -= 76
    c.setFillColor(INK); c.setFont(TITLE_FONT, 12)
    c.drawCentredString(306, yy - 20, '"The network is always hostile — even your own."')
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Identity Becomes the Perimeter",
                       "Every request carries proof of who/what is asking.")
    box(c, 72, 440, 140, 60, BOX_BLUE, "User identity", "MFA'd human")
    box(c, 246, 440, 140, 60, BOX_GREEN, "Device identity", "cert + posture")
    box(c, 420, 440, 92, 60, BOX_ORANGE, "Workload", "SPIFFE id")
    box(c, 216, 320, 180, 70, BOX_PURP, "Policy Engine", "allow / deny / step-up")
    for bx in [142, 316, 466]:
        arrow(c, bx, 438, 306, 392, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 270, "Signals: who, what device, where, when, risk score → decision per request.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Micro-Segmentation",
                       "Shrink the blast radius: tiny zones, explicit allow-rules between them.")
    zones = [("Web tier", BOX_BLUE, 72), ("App tier", BOX_GREEN, 216), ("Data tier", BOX_ORANGE, 360)]
    for name, fill, bx in zones:
        box(c, bx, 420, 120, 70, fill, name, "")
    arrow(c, 192, 455, 214, 455, color=GREEN, label="✓ allow")
    arrow(c, 336, 455, 358, 455, color=GREEN, label="✓ allow")
    c.setStrokeColor(RED); c.setLineWidth(2); c.setDash(5, 4)
    c.line(132, 418, 420, 418); c.setDash()
    c.setFillColor(RED); c.setFont(BODY_FONT, 10)
    c.drawCentredString(276, 396, "✗ default deny — no lateral movement")
    note(c, 72, 280, 468, "East-west traffic (server to server) gets the same scrutiny as north-south. Compromising web doesn't reach data.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "The Pillars of Zero Trust",
                       "Six areas to harden — maturity is a journey.")
    pillars = [("Identities", "Phishing-resistant MFA, passwordless where possible", BOX_BLUE),
               ("Devices", "Managed, patched, encrypted, attested health", BOX_GREEN),
               ("Networks", "Encrypted, segmented, no implicit trust zones", BOX_TEAL),
               ("Applications", "Secure SDLC, runtime protection", BOX_ORANGE),
               ("Data", "Classify, encrypt, DLP, minimal retention", BOX_PURP),
               ("Visibility", "Centralized logs, UEBA, automated response", BOX_RED)]
    yy = y
    for name, desc, fill in pillars:
        box(c, 72, yy - 44, 468, 48, fill, name, desc, font_size=11)
        yy -= 60
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Putting It Together: A Request's Journey",
                       "One API call, verified five ways.")
    steps = ["1. User + device authenticate (MFA, cert)", "2. Policy engine evaluates risk signals",
             "3. Micro-segment allows web→app only", "4. Service identity (mTLS) app→data",
             "5. Everything logged to SIEM"]
    yy = y
    for s in steps:
        box(c, 72, yy - 36, 468, 40, LIGHT_BG, "", "")
        c.setFillColor(ACCENT); c.circle(96, yy - 16, 10, fill=1, stroke=0)
        c.setFillColor(white); c.setFont(TITLE_FONT, 10)
        c.drawCentredString(96, yy - 12, s[0])
        c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
        c.drawString(116, yy - 12, s[3:])
        yy -= 52
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Zero Trust — Remember",
                 ["Verify explicitly, least privilege, assume breach — the three tenets.",
                  "Identity (user + device + workload) replaces the network perimeter.",
                  "Micro-segmentation with default-deny contains lateral movement.",
                  "Harden all six pillars: identities, devices, networks, apps, data, visibility.",
                  "Every request is authenticated, authorized, encrypted, and logged."],
                 pg)
    c.save(); print("wrote", path)


def pdf_pki(path):
    c = new_canvas(path); pg = 1
    title_page(c, "PKI & Encryption\nVisual Guide",
               "Public keys, private keys, and the math\nthat keeps secrets secret.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "Symmetric vs Asymmetric",
                       "One key or two? Speed vs key distribution.")
    box(c, 72, y - 70, 225, 130, BOX_GREEN, "Symmetric", "AES-256", font_size=13)
    box(c, 315, y - 70, 225, 130, BOX_BLUE, "Asymmetric", "RSA / ECC", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    sy = ["One shared secret key", "Very fast (GB/s)", "Key distribution problem", "Use: bulk data encryption"]
    ay = ["Public + private key pair", "Slow (~1000x slower)", "Share public freely", "Use: key exchange, signatures"]
    yy = y - 100
    for t in sy: c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 100
    for t in ay: c.drawString(331, yy, "• " + t); yy -= 18
    note(c, 72, 200, 468, "Hybrid reality: use asymmetric crypto to agree on a symmetric key, then encrypt bulk data symmetrically. Best of both.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Public-Key Encryption: The Mailbox Analogy",
                       "Anyone can drop a letter in; only the owner opens it.")
    box(c, 72, 420, 150, 70, BOX_BLUE, "Public key", "shared openly 🔓")
    box(c, 390, 420, 150, 70, BOX_RED, "Private key", "never leaves owner 🔒")
    arrow(c, 222, 455, 388, 455, color=ACCENT, label="encrypt")
    c.setFillColor(INK); c.setFont(MONO_FONT, 11)
    c.drawCentredString(306, 380, '"attack at dawn"  →  9f2a…c41d')
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 358, "ciphertext: meaningless without the private key")
    arrow(c, 465, 418, 540, 350, color=GREEN)
    c.setFillColor(GREEN); c.setFont(BODY_FONT, 10)
    c.drawString(420, 320, "decrypt → plaintext")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Digital Signatures: Prove It Was You",
                       "Encryption's mirror image — authenticity instead of secrecy.")
    yy = bullet_list(c, 72, y,
        ["1. Hash the message (SHA-256) → fixed-size digest.",
         "2. Encrypt the digest with the sender's PRIVATE key → signature.",
         "3. Receiver decrypts the signature with the sender's PUBLIC key.",
         "4. Receiver hashes the message itself and compares — match = authentic + untampered.",
         "Non-repudiation: only the private-key holder could have made that signature."],
        font_size=11, gap=24)
    box(c, 72, 170, 468, 56, BOX_ORANGE, "Sign with private → verify with public",
        "the exact reverse of encryption", font_size=11)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Certificates Bind Keys to Identities",
                       "A public key alone says nothing about WHO owns it.")
    box(c, 72, 440, 468, 70, BOX_TEAL, "X.509 Certificate",
        "subject (example.com) • public key • issuer • validity • signature", font_size=10.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 390, "A Certificate Authority (CA) verifies identity, then SIGNS the certificate.")
    c.drawString(72, 372, "Your browser trusts ~150 root CAs — their signatures vouch for everyone else.")
    # chain
    box(c, 72, 250, 130, 56, BOX_GREEN, "Root CA", "self-signed")
    box(c, 241, 250, 130, 56, BOX_BLUE, "Intermediate", "signed by root")
    box(c, 410, 250, 130, 56, BOX_ORANGE, "Leaf", "example.com")
    arrow(c, 202, 278, 239, 278, color=ACCENT, label="signs")
    arrow(c, 371, 278, 408, 278, color=ACCENT, label="signs")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Hashing: Fingerprints for Data",
                       "One-way functions — easy to compute, impossible to reverse.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 12)
    c.drawString(72, y, '"password123"')
    arrow(c, 220, y - 4, 300, y - 4, color=ACCENT, label="SHA-256")
    c.setFillColor(MUTED); c.setFont(MONO_FONT, 9)
    c.drawString(72, y - 30, "ef92b778bafe771e89245b89ecbc08a44a4e166")
    c.drawString(72, y - 46, "c06659911881f383d4473e94f")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 80,
        ["Deterministic: same input → same hash, always.",
         "Avalanche: one bit changes → ~half the output bits flip.",
         "One-way: can't reconstruct input from the hash.",
         "Passwords: store salted hashes (bcrypt/argon2), never plaintext, never plain SHA-256."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Where Each Primitive Lives",
                       "The crypto stack in one view.")
    rows = [("TLS", "ECDHE key exchange → AES-GCM bulk encryption → certs for auth", BOX_GREEN),
            ("Passwords", "Argon2/bcrypt salted hashes; never reversible encryption", BOX_BLUE),
            ("Code signing", "Developer signs with private key; OS verifies with public", BOX_ORANGE),
            ("End-to-end chat", "Double-ratchet (Signal): forward secrecy per message", BOX_TEAL)]
    yy = y
    for name, desc, fill in rows:
        box(c, 72, yy - 54, 468, 58, fill, name, desc, font_size=11)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "PKI & Encryption — Remember",
                 ["Symmetric (AES) is fast for bulk data; asymmetric (RSA/ECC) solves key distribution.",
                  "Encrypt with PUBLIC, decrypt with PRIVATE. Sign with PRIVATE, verify with PUBLIC.",
                  "Certificates bind a public key to an identity, vouched for by a CA chain.",
                  "Hashes are one-way fingerprints — salt and stretch them for passwords (Argon2).",
                  "Real systems are hybrid: asymmetric handshake, symmetric bulk, hashes for integrity."],
                 pg)
    c.save(); print("wrote", path)


def pdf_oauth(path):
    c = new_canvas(path); pg = 1
    title_page(c, "OAuth 2.0 &\nAuthentication Flows",
               "'Log in with Google' —\nhow delegated auth works without sharing passwords.",
               "Security", None); pg += 1

    y = section_header(c, 1, 6, "The Problem OAuth Solves",
                       "Apps need access to your stuff — without your password.")
    box(c, 72, 400, 150, 70, BOX_BLUE, "You", "")
    box(c, 246, 400, 150, 70, BOX_ORANGE, "Photo App", "wants your photos")
    box(c, 420, 400, 92, 70, BOX_GREEN, "Google", "has your photos")
    c.setStrokeColor(RED); c.setLineWidth(2)
    c.line(222, 470, 222, 400); c.line(222, 400, 246, 400)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawString(72, 350, "✗ Don't give the app your Google password!")
    c.setFillColor(GREEN); c.setFont(TITLE_FONT, 11)
    c.drawString(72, 328, "✓ Give it a scoped, revocable token instead.")
    note(c, 72, 240, 468, "OAuth 2.0 = delegated AUTHORIZATION. OpenID Connect (OIDC) adds authentication on top.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Roles in the Dance",
                       "Four actors, each with a job.")
    roles = [("Resource Owner", "You — the human granting access", BOX_BLUE),
             ("Client", "The app requesting access (photo editor)", BOX_ORANGE),
             ("Authorization Server", "Issues tokens (Google's auth)", BOX_GREEN),
             ("Resource Server", "Holds the data (Google Photos API)", BOX_TEAL)]
    yy = y
    for name, desc, fill in roles:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=12)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Authorization Code Flow (the secure one)",
                       "The front channel carries a code; the back channel trades it for tokens.")
    box(c, 72, 460, 110, 56, BOX_BLUE, "Browser", "")
    box(c, 216, 460, 110, 56, BOX_ORANGE, "App", "")
    box(c, 360, 460, 150, 56, BOX_GREEN, "Google Auth", "")
    steps = [("1. → Google: 'user wants to log in'", 420), ("2. ← login + consent screen", 390),
             ("3. → app: authorization CODE", 360), ("4. app → Google (back channel): code + secret", 330),
             ("5. ← access + refresh tokens", 300)]
    c.setFont(BODY_FONT, 9.5); c.setFillColor(INK)
    for txt, yy2 in steps:
        c.drawString(72, yy2, txt)
    c.setFillColor(BOX_RED); c.roundRect(72, 230, 468, 48, 8, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(88, 258, "Why the code? Tokens never touch the browser URL — the code is single-use, short-lived,")
    c.drawString(88, 244, "and the secret exchange happens server-to-server. PKCE adds proof for public clients.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Tokens: Access vs Refresh vs ID",
                       "Three tokens, three jobs.")
    toks = [("Access token", "Short-lived (minutes–hours). 'Bearer' — whoever holds it gets in. Sent per API call.", BOX_GREEN),
            ("Refresh token", "Long-lived. Gets NEW access tokens without bothering the user. Guard it well.", BOX_ORANGE),
            ("ID token (OIDC)", "JWT with who the user is: sub, email, name. For authentication, not API auth.", BOX_BLUE)]
    yy = y
    for name, desc, fill in toks:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    c.setFillColor(INK); c.setFont(MONO_FONT, 9)
    c.drawString(72, yy - 10, "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxMjM0IiwiZW1haWwiOiJ5b3VAbWFpbCJ9…")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9)
    c.drawString(72, yy - 26, "JWT = header.payload.signature — verifiable without a database lookup.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Scopes & Consent",
                       "Least privilege applies to tokens too.")
    box(c, 72, 420, 468, 60, BOX_TEAL, "scope=photos.read", "can list and view — NOT delete, NOT read email")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 360,
        ["The consent screen shows exactly what's requested — read it before clicking Allow.",
         "Apps should request minimum scopes; users can revoke anytime from the provider.",
         "Over-scoped tokens are a breach multiplier — a leaked token can only do what its scopes allow."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Hardening Checklist",
                       "OAuth done wrong is worse than passwords done right.")
    checks = [("Always use Authorization Code + PKCE", "Never implicit flow in new apps.", BOX_GREEN),
              ("Validate everything", "Issuer, audience, expiry, signature on every token.", BOX_BLUE),
              ("Short-lived access tokens", "Minutes, not days. Rotate refresh tokens.", BOX_ORANGE),
              ("Protect the secret", "Confidential clients keep secrets server-side only.", BOX_RED)]
    yy = y
    for name, desc, fill in checks:
        c.setFillColor(GREEN); c.circle(96, yy - 27, 9, fill=1, stroke=0)
        c.setFillColor(white); c.setFont(TITLE_FONT, 10); c.drawCentredString(96, yy - 23, "✓")
        box(c, 116, yy - 54, 424, 58, fill, name, desc, font_size=11)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "OAuth 2.0 — Remember",
                 ["OAuth delegates authorization without sharing passwords; OIDC adds authentication.",
                  "Authorization Code + PKCE is the flow to use — code in front, tokens in back.",
                  "Access tokens are short-lived bearers; refresh tokens renew them; ID tokens say who you are.",
                  "Scopes enforce least privilege — request minimum, display honestly, allow revocation.",
                  "Validate issuer/audience/expiry/signature; keep access tokens short-lived."],
                 pg)
    c.save(); print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    pdf_zero_trust(os.path.join(out, "bbg-zero-trust.pdf"))
    pdf_pki(os.path.join(out, "bbg-pki-encryption.pdf"))
    pdf_oauth(os.path.join(out, "bbg-oauth-flows.pdf"))
