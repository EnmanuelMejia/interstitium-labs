"""Batch 2: Networking PDFs — TCP 3-Way Handshake, DNS Resolution, TLS Handshake."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


def _tcp_endpoints(c, y_top, client_label="Client", server_label="Server"):
    box(c, 72, y_top, 130, 56, BOX_BLUE, client_label, "")
    box(c, 410, y_top, 130, 56, BOX_GREEN, server_label, "")
    return 137, 475  # x positions


def _tcp_arrow(c, x1, x2, y, label, color=ACCENT, dashed=False):
    if dashed:
        c.setDash(4, 3)
    arrow(c, x1, y, x2, y, color=color, width=2, label=label)
    if dashed:
        c.setDash()


def pdf_tcp_handshake(path):
    c = new_canvas(path); pg = 1
    title_page(c, "TCP 3-Way Handshake\nVisual Guide",
               "How two machines agree to talk reliably\nbefore a single byte of data flows.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 6, "Why a Handshake at All?",
                       "TCP is reliable: ordered, acknowledged, connection-oriented. That starts with agreement.")
    box(c, 72, 380, 200, 80, BOX_BLUE, "Client", "wants to talk")
    box(c, 340, 380, 200, 80, BOX_GREEN, "Server", "listening on :443")
    c.setStrokeColor(MUTED); c.setDash(4, 3); c.setLineWidth(1.5)
    c.line(276, 420, 336, 420); c.setDash()
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 400, "no connection yet")
    note(c, 72, 280, 468, "UDP just fires datagrams. TCP negotiates first — sequence numbers, windows, options — so nothing is lost or duplicated.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Step 1 — SYN: 'Can we talk?'",
                       "Client picks a random initial sequence number (ISN) and sends SYN.")
    cx, sx = _tcp_endpoints(c, 480)
    yy = 420
    _tcp_arrow(c, cx + 65, sx - 65, yy, "SYN  seq=1000", ACCENT)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 360, "SYN = synchronize sequence numbers.")
    c.drawString(72, 342, "Client says: 'I will number my bytes starting at 1000.'")
    box(c, 72, 260, 468, 56, BOX_BLUE, "Packet: SYN", "seq=1000  •  SYN flag set  •  no data", font_size=11)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Step 2 — SYN-ACK: 'Yes, and here's my number'",
                       "Server acknowledges the SYN and sends its own ISN.")
    cx, sx = _tcp_endpoints(c, 480)
    yy = 420
    _tcp_arrow(c, cx + 65, sx - 65, yy + 30, "SYN  seq=1000", color=MUTED, dashed=True)
    _tcp_arrow(c, sx - 65, cx + 65, yy, "SYN-ACK  seq=5000  ack=1001", GREEN)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 360, "ack=1001 means: 'I expect your next byte to be #1001.'")
    c.drawString(72, 342, "seq=5000 means: 'I will number MY bytes starting at 5000.'")
    box(c, 72, 260, 468, 56, BOX_GREEN, "Packet: SYN-ACK", "seq=5000  ack=1001  •  SYN+ACK flags", font_size=11)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Step 3 — ACK: 'Got it, we're connected'",
                       "Client acknowledges the server's SYN. Connection: ESTABLISHED.")
    cx, sx = _tcp_endpoints(c, 480)
    yy = 420
    _tcp_arrow(c, cx + 65, sx - 65, yy + 60, "SYN", color=MUTED, dashed=True)
    _tcp_arrow(c, sx - 65, cx + 65, yy + 30, "SYN-ACK", color=MUTED, dashed=True)
    _tcp_arrow(c, cx + 65, sx - 65, yy, "ACK  seq=1001  ack=5001", ACCENT2)
    c.setFillColor(GREEN); c.roundRect(216, 280, 180, 44, 22, fill=1, stroke=0)
    c.setFillColor(white); c.setFont(TITLE_FONT, 13)
    c.drawCentredString(306, 296, "ESTABLISHED ✓")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 250, "Both sides agreed on sequence numbers. Data can now flow.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "After the Handshake: Reliable Data Flow",
                       "Every byte numbered, every segment acknowledged.")
    cx, sx = _tcp_endpoints(c, 480)
    _tcp_arrow(c, cx + 65, sx - 65, 420, "'Hello'  seq=1001 (5 bytes)", ACCENT)
    _tcp_arrow(c, sx - 65, cx + 65, 380, "ACK  ack=1006", GREEN)
    _tcp_arrow(c, sx - 65, cx + 65, 340, "'Hi!'  seq=5001 (3 bytes)", ACCENT)
    _tcp_arrow(c, cx + 65, sx - 65, 300, "ACK  ack=5004", GREEN)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 240, "Lost a packet? The sender retransmits after a timeout.")
    c.drawString(72, 222, "Arrived out of order? The receiver reorders by sequence number.")
    c.drawString(72, 204, "Receiver overwhelmed? The window size tells the sender to slow down (flow control).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Closing: The 4-Way Goodbye",
                       "Each side closes independently with FIN.")
    cx, sx = _tcp_endpoints(c, 480)
    _tcp_arrow(c, cx + 65, sx - 65, 420, "FIN  (I'm done sending)", ORANGE)
    _tcp_arrow(c, sx - 65, cx + 65, 390, "ACK", MUTED)
    _tcp_arrow(c, sx - 65, cx + 65, 360, "FIN  (I'm done too)", ORANGE)
    _tcp_arrow(c, cx + 65, sx - 65, 330, "ACK", MUTED)
    note(c, 72, 230, 468, "TIME_WAIT: the closer waits 2×MSL so stray packets die before the port is reused. Prevents old data corrupting new connections.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "TCP Handshake — Remember",
                 ["SYN → SYN-ACK → ACK: both sides agree on initial sequence numbers before data flows.",
                  "ack=N means 'I expect byte N next'; seq=N numbers the sender's bytes.",
                  "Reliability = sequence numbers + acknowledgments + retransmission + flow control.",
                  "Closing takes 4 steps (FIN/ACK each way); TIME_WAIT guards against stray packets.",
                  "Cost: 1 round-trip before any data — the reason for TCP Fast Open and QUIC."],
                 pg)
    c.save(); print("wrote", path)


def pdf_dns(path):
    c = new_canvas(path); pg = 1
    title_page(c, "DNS Resolution\nVisual Guide",
               "From example.com to 93.184.216.34\nin milliseconds — the phonebook of the internet.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 6, "The Problem: Humans Hate Numbers",
                       "You type a name; the network needs an IP address.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 20)
    c.drawCentredString(306, 460, "example.com")
    arrow(c, 306, 430, 306, 380, color=ACCENT, label="DNS")
    c.setFillColor(INK); c.setFont(MONO_FONT, 20)
    c.drawCentredString(306, 340, "93.184.216.34")
    note(c, 72, 240, 468, "DNS is a hierarchical, distributed database mapping names → IPs (and more). ~trillions of queries per day.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Step 1 — Check the Cache",
                       "Resolution starts locally and climbs only as needed.")
    box(c, 72, 460, 180, 60, BOX_BLUE, "Browser cache", "seconds–minutes")
    box(c, 72, 380, 180, 60, BOX_GREEN, "OS cache", "from /etc/hosts + stub")
    box(c, 72, 300, 180, 60, BOX_ORANGE, "Resolver cache", "ISP / 8.8.8.8")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(280, 490, "← 1st: did we look this up recently?")
    c.drawString(280, 410, "← 2nd: OS-level cache")
    c.drawString(280, 330, "← 3rd: recursive resolver's cache")
    note(c, 72, 220, 468, "Most queries never leave the cache. TTLs control how long answers are kept — short TTL = flexible, long TTL = fast.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Step 2 — Ask the Root",
                       "On a cache miss, the recursive resolver walks the hierarchy top-down.")
    box(c, 216, 500, 180, 60, BOX_PURP, "Recursive Resolver", "does the walking")
    box(c, 216, 400, 180, 60, BOX_BLUE, "Root Servers", "\".\" — 13 logical clusters")
    arrow(c, 306, 498, 306, 462, color=ACCENT, label="who handles .com?")
    arrow(c, 400, 430, 400, 470, color=GREEN, label="ask the .com TLD")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 340, "Root doesn't know example.com — but it knows who runs .com.")
    c.drawString(72, 322, "It answers with a REFERRAL, not the final answer.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Steps 3–4 — TLD, Then Authoritative",
                       "Each level refers down until someone is authoritative.")
    box(c, 72, 460, 150, 60, BOX_BLUE, ".com TLD", "referral")
    box(c, 231, 460, 150, 60, BOX_GREEN, "Authoritative", "example.com NS")
    box(c, 390, 460, 150, 60, BOX_ORANGE, "Answer", "93.184.216.34")
    arrow(c, 222, 490, 231, 490, color=ACCENT)
    arrow(c, 381, 490, 390, 490, color=ACCENT)
    arrow(c, 465, 458, 350, 380, color=GREEN, label="caches + returns")
    box(c, 216, 320, 180, 56, BOX_PURP, "Resolver", "caches the answer")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 260, "1. Resolver → .com TLD: 'who is authoritative for example.com?'")
    c.drawString(72, 242, "2. Resolver → authoritative NS: 'what is the A record?'")
    c.drawString(72, 224, "3. Authoritative answers; resolver caches it for the TTL.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Record Types: DNS Does More Than A Records",
                       "One system, many jobs.")
    recs = [("A / AAAA", "Hostname → IPv4 / IPv6", BOX_BLUE),
            ("CNAME", "Alias: www → example.com", BOX_GREEN),
            ("MX", "Where mail goes (+ priority)", BOX_ORANGE),
            ("TXT", "SPF, DKIM, verification strings", BOX_TEAL),
            ("NS / SOA", "Delegation and zone authority", BOX_PURP)]
    yy = y
    for name, desc, fill in recs:
        box(c, 72, yy - 48, 468, 52, fill, name, desc, font_size=12)
        yy -= 66
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Security: DNS Is Traditionally Plaintext",
                       "Anyone on the path can see and spoof queries — hence the upgrades.")
    items = [("DNSSEC", "Cryptographic signatures prove answers weren't tampered with (not encryption).", BOX_GREEN),
             ("DoT (port 853)", "DNS over TLS — encrypted channel to the resolver.", BOX_BLUE),
             ("DoH (port 443)", "DNS over HTTPS — queries blend in with web traffic.", BOX_TEAL),
             ("Cache Poisoning", "Attack: trick a resolver into caching a fake answer. DNSSEC defeats it.", BOX_RED)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 54, 468, 58, fill, name, desc, font_size=11.5)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "DNS — Remember",
                 ["Resolution order: browser → OS → resolver cache → root → TLD → authoritative.",
                  "Roots and TLDs give referrals; only authoritative servers give final answers.",
                  "Everything is cached by TTL — DNS is fast because most queries never walk the tree.",
                  "Record types: A/AAAA (addresses), CNAME (aliases), MX (mail), TXT (metadata), NS/SOA (delegation).",
                  "Classic DNS is plaintext; DNSSEC adds authenticity, DoT/DoH add encryption."],
                 pg)
    c.save(); print("wrote", path)


def pdf_tls(path):
    c = new_canvas(path); pg = 1
    title_page(c, "TLS Handshake\nVisual Guide",
               "How HTTPS builds a private tunnel\non a public internet — in ~2 round trips.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 6, "The Goal: Private + Authenticated",
                       "Three guarantees before any application data flows.")
    goals = [("Confidentiality", "Nobody can read the traffic (encryption).", BOX_GREEN),
             ("Integrity", "Nobody can tamper with it undetected (MAC/AEAD).", BOX_BLUE),
             ("Authentication", "You really are talking to example.com (certificates).", BOX_ORANGE)]
    yy = y
    for name, desc, fill in goals:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=12)
        yy -= 72
    note(c, 72, yy - 40, 468, "TLS sits between TCP and HTTP. HTTPS = HTTP inside a TLS tunnel.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Step 1 — ClientHello",
                       "Client offers what it supports.")
    box(c, 72, 400, 200, 70, BOX_BLUE, "Client", "")
    box(c, 340, 400, 200, 70, BOX_GREEN, "Server", "")
    arrow(c, 272, 435, 340, 435, color=ACCENT, label="ClientHello")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    items = ["• TLS versions it speaks (1.2, 1.3)", "• Cipher suites, ranked by preference",
             "• Random bytes (anti-replay)", "• SNI: the hostname it wants (for virtual hosting)"]
    yy = 340
    for it in items:
        c.drawString(90, yy, it); yy -= 22
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Step 2 — ServerHello + Certificate",
                       "Server picks parameters and proves its identity.")
    box(c, 72, 400, 200, 70, BOX_BLUE, "Client", "")
    box(c, 340, 400, 200, 70, BOX_GREEN, "Server", "")
    arrow(c, 340, 450, 272, 450, color=GREEN, label="ServerHello")
    arrow(c, 340, 420, 272, 420, color=GREEN, label="Certificate chain")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(90, 340, "Certificate contains: domain, public key, issuer signature, expiry.")
    c.drawString(90, 318, "Client verifies: signature chains to a trusted CA + name matches + not expired.")
    box(c, 90, 240, 432, 56, BOX_ORANGE, "Chain of trust", "leaf cert → intermediate CA → root CA (in OS/browser store)", font_size=10)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Step 3 — Key Exchange",
                       "Agree on session keys without ever sending them.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 12)
    c.drawString(72, y, "TLS 1.3: Ephemeral Diffie-Hellman (ECDHE)")
    yy = bullet_list(c, 72, y - 30,
        ["Each side generates a one-time (ephemeral) key pair and sends the public half.",
         "Both combine their private half with the other's public half → same shared secret.",
         "An eavesdropper sees only public values — deriving the secret requires solving discrete log.",
         "Ephemeral = forward secrecy: stealing the server's long-term key later can't decrypt past sessions."],
        font_size=10.5, gap=26)
    box(c, 72, 170, 468, 60, BOX_TEAL, "Result: symmetric session keys",
        "AES-GCM or ChaCha20-Poly1305 — fast bulk encryption + integrity", font_size=11)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Steps 4–5 — Finished, Then Encrypted Data",
                       "Both sides confirm, then the tunnel carries HTTP.")
    box(c, 72, 420, 200, 60, BOX_BLUE, "Client", "")
    box(c, 340, 420, 200, 60, BOX_GREEN, "Server", "")
    arrow(c, 272, 460, 340, 460, color=ACCENT, label="Finished (encrypted)")
    arrow(c, 340, 440, 272, 440, color=GREEN, label="Finished (encrypted)")
    c.setFillColor(GREEN); c.roundRect(206, 340, 200, 44, 22, fill=1, stroke=0)
    c.setFillColor(white); c.setFont(TITLE_FONT, 13)
    c.drawCentredString(306, 356, "TUNNEL UP ✓")
    arrow(c, 272, 310, 340, 310, color=ACCENT2, width=2.5, label="GET /  (encrypted HTTP)")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 270, "From here on, everything — headers, cookies, body — is encrypted.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "TLS 1.3 vs 1.2 + Session Resumption",
                       "Faster handshakes for returning visitors.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    rows = [("Handshake RTTs", "TLS 1.2: 2 RTT  →  TLS 1.3: 1 RTT", BOX_GREEN),
            ("0-RTT resumption", "Repeat visitors can send data with the first flight (replay risk — use carefully).", BOX_BLUE),
            ("Removed", "1.3 dropped RSA key exchange, CBC modes, renegotiation — smaller, safer.", BOX_ORANGE),
            ("Certificates", "Still X.509; automation via ACME/Let's Encrypt made HTTPS ubiquitous.", BOX_TEAL)]
    yy = y
    for name, desc, fill in rows:
        box(c, 72, yy - 54, 468, 58, fill, name, desc, font_size=11)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "TLS Handshake — Remember",
                 ["ClientHello offers parameters; ServerHello + certificate picks them and proves identity.",
                  "Certificates chain to trusted roots; the client checks signature, name, and expiry.",
                  "ECDHE key exchange creates session keys no eavesdropper can derive — with forward secrecy.",
                  "Finished messages confirm; then HTTP flows inside the encrypted tunnel.",
                  "TLS 1.3: 1-RTT handshake, 0-RTT resumption, and a trimmed, safer cipher list."],
                 pg)
    c.save(); print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    pdf_tcp_handshake(os.path.join(out, "bbg-tcp-handshake.pdf"))
    pdf_dns(os.path.join(out, "bbg-dns-resolution.pdf"))
    pdf_tls(os.path.join(out, "bbg-tls-handshake.pdf"))
