"""Batch 8: Networking PDFs — 22 visual guides, OSI through DNS Security."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


def pdf_osi(path):
    c = new_canvas(path); pg = 1
    title_page(c, "The OSI Model\nVisual Guide",
               "Seven layers of networking —\nwhat each layer does and where the work happens.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 6, "The 7 Layers, Top to Bottom",
                       "Upper layers = apps & data meaning. Lower layers = moving bits.")
    layers = [
        ("7 · Application", "HTTP, DNS, SMTP — what users touch", BOX_BLUE),
        ("6 · Presentation", "Encoding, TLS, compression, formats", BOX_PURP),
        ("5 · Session", "Dialogs, checkpoints, sessions", BOX_TEAL),
        ("4 · Transport", "TCP/UDP — ports, segments, reliability", BOX_GREEN),
        ("3 · Network", "IP — routing, addresses, packets", BOX_ORANGE),
        ("2 · Data Link", "MAC, frames, switches, Ethernet", BOX_RED),
        ("1 · Physical", "Cables, signals, bits", MUTED),
    ]
    yy = y
    for name, desc, fill in layers:
        box(c, 116, yy - 44, 380, 50, fill, name, desc, font_size=11)
        yy -= 58
    note(c, 72, 60, 468, "Mnemonic: 'All People Seem To Need Data Processing' (7→1). Most real work happens at 2, 3, 4, and 7.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Encapsulation: Headers All the Way Down",
                       "Each layer wraps the payload from above and adds its own header.")
    units = [("L7 Data", "payload", BOX_BLUE),
             ("L4 Segment", "+ TCP header", BOX_GREEN),
             ("L3 Packet", "+ IP header", BOX_ORANGE),
             ("L2 Frame", "+ MAC header/trailer", BOX_RED),
             ("L1 Bits", "onto the wire", BOX_PURP)]
    xx = 72
    for name, desc, fill in units:
        box(c, xx, 420, 92, 90, fill, name, desc, font_size=10)
        if xx > 72:
            arrow(c, xx - 12, 465, xx, 465, color=ACCENT, width=1.8)
        xx += 100
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 370,
        ["Sending: Application data descends; every layer ADDS control info (headers, sometimes trailers).",
         "Receiving: the peer's matching layer reads and STRIPS its own header, then passes up.",
         "The unit changes name per layer: message → segment → packet → frame → bits."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "What Each Header Carries",
                       "Control information is how layers coordinate with their peer.")
    hdrs = [("L2: MAC header/trailer", "src/dst MAC, frame check sequence (CRC)", BOX_RED),
            ("L3: IP header", "src/dst IP, TTL, protocol — routes the packet", BOX_ORANGE),
            ("L4: TCP header", "src/dst ports, seq/ack numbers, flags, window", BOX_GREEN),
            ("L5-7: app headers", "HTTP headers, TLS records, MIME types — app semantics", BOX_BLUE)]
    yy = y
    for name, desc, fill in hdrs:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 74
    note(c, 72, 180, 468, "Overhead is real: a tiny payload can carry 40+ bytes of TCP/IP headers plus Ethernet framing. Header compression (ROHC, HPACK) exists for a reason.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Decapsulation on Arrival",
                       "The reverse trip: strip, check, pass up.")
    box(c, 72, 460, 220, 70, BOX_BLUE, "Sender stack", "app → wire")
    box(c, 320, 460, 220, 70, BOX_BLUE, "Receiver stack", "wire → app")
    arrow(c, 292, 495, 318, 495, color=ACCENT, width=2.5, label="bits on wire")
    yy = y - 90
    steps = ["1. NIC receives frame — CRC checked, MAC trailer stripped (L2)",
             "2. IP stack reads header — dst IP matches? TTL decremented (L3)",
             "3. TCP reassembles segments — ordering, retransmits, ports (L4)",
             "4. App reads the stream — parses HTTP, renders the page (L5-7)"]
    for s in steps:
        c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
        c.drawString(72, yy, s); yy -= 28
    note(c, 72, 120, 468, "A device only processes the layers it needs: a switch stops at L2, a router at L3, a firewall often at L4 — end hosts go all the way up.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Which Devices Live Where",
                       "Networking gear is named by the highest layer it understands.")
    devs = [("Hub / Repeater (L1)", "Repeats bits. One collision domain — obsolete.", BOX_PURP),
            ("Switch (L2)", "Forwards frames by MAC table. One broadcast domain per VLAN.", BOX_RED),
            ("Router (L3)", "Forwards packets by IP routing table. Connects networks.", BOX_ORANGE),
            ("L4+ devices", "Firewalls, load balancers, proxies — ports, sessions, content.", BOX_GREEN)]
    yy = y
    for name, desc, fill in devs:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 74
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 200, "Rule of thumb: a device that must READ a layer's header to do its job operates at that layer.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "OSI vs the Real TCP/IP Stack",
                       "The internet runs TCP/IP — a leaner 4-layer cousin.")
    box(c, 72, 420, 220, 150, BOX_BLUE, "OSI (reference)", "7 layers:\nApp / Pres / Sess /\nTransport / Network /\nData Link / Physical")
    box(c, 320, 420, 220, 150, BOX_GREEN, "TCP/IP (deployed)", "4 layers:\nApplication /\nTransport / Internet /\nLink")
    arrow(c, 292, 495, 318, 495, color=ACCENT, width=2, label="maps to")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 360,
        ["OSI is a teaching/reference model; TCP/IP is what actually ships.",
         "TCP/IP folds 5-7 into 'Application' and 1-2 into 'Link' — same ideas, fewer boxes.",
         "Engineers still say 'L3 switch' or 'L7 load balancer' — OSI numbering is the shared vocabulary."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "OSI Model — Remember",
                 ["7 layers: App, Presentation, Session, Transport, Network, Data Link, Physical.",
                  "Encapsulation: every layer adds its header on send, strips it on receive.",
                  "Units rename per layer: message → segment → packet → frame → bits.",
                  "Devices are named by the highest layer they read: switch (L2), router (L3).",
                  "The internet runs TCP/IP's 4 layers, but OSI numbering is the shared vocabulary."],
                 pg)
    c.save(); print("wrote", path)


def pdf_tcp_teardown(path):
    c = new_canvas(path); pg = 1
    title_page(c, "TCP Teardown\n& Reliability",
               "Closing connections cleanly —\nand the machinery that makes TCP trustworthy.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "The FIN/ACK Close Sequence",
                       "A graceful goodbye is a 4-way handshake.")
    box(c, 72, 460, 160, 60, BOX_BLUE, "Client", "initiator")
    box(c, 380, 460, 160, 60, BOX_GREEN, "Server", "responder")
    seq = [("FIN", 152, 300, "I'm done sending"),
           ("ACK", 460, 340, "Got it"),
           ("FIN", 460, 300, "I'm done too"),
           ("ACK", 152, 340, "Bye")]
    yy = 420
    for label, x1, x2, note_t in seq:
        arrow(c, x1, yy, x2, yy, color=ACCENT, width=2, label=label)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8.5)
        c.drawCentredString(306, yy - 14, note_t)
        yy -= 40
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 220, "Each side closes its half-duplex direction independently — a connection is two one-way streams.")
    note(c, 72, 130, 468, "Simultaneous close: both sides send FIN at once — the sequence still converges, with a slightly different ACK pattern.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "TIME_WAIT: Why the Wait?",
                       "The side that sends the final ACK lingers for 2×MSL (~60s).")
    box(c, 72, 420, 468, 70, BOX_ORANGE, "TIME_WAIT state", "socket held 2×MSL after final ACK — then fully closed")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 380,
        ["Reason 1 — lost final ACK: if the last ACK is dropped, the peer retransmits FIN; without TIME_WAIT nobody would answer, and the peer would RST.",
         "Reason 2 — delayed segments: old duplicate packets from this connection could corrupt a NEW connection reusing the same ports; the wait lets them die.",
         "Cost: ports held in TIME_WAIT can't be reused — busy servers tune this (SO_REUSEADDR, shorter MSL) and watch for port exhaustion."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Retransmission: Timers & Fast Recovery",
                       "No ACK in time? Send it again — but smartly.")
    box(c, 72, 460, 468, 60, BOX_RED, "RTO — Retransmission Timeout", "per-segment timer; on expiry, resend and back off exponentially")
    box(c, 72, 380, 468, 60, BOX_GREEN, "Fast retransmit", "3 duplicate ACKs → resend NOW, don't wait for the timer")
    box(c, 72, 300, 468, 60, BOX_BLUE, "SACK — Selective ACK", "receiver says exactly which blocks arrived; resend only the gaps")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 260, "RTO is computed from measured RTT (smoothed) — too short wastes bandwidth, too long stalls the connection.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Sliding Window: Flow Control",
                       "The receiver throttles the sender — never overflow a slow reader.")
    box(c, 72, 460, 200, 70, BOX_BLUE, "Sender", "may send up to\nwindow size")
    box(c, 340, 460, 200, 70, BOX_GREEN, "Receiver", "advertises window\nin every ACK")
    arrow(c, 272, 495, 338, 495, color=ACCENT, width=2.5, label="window = 64KB")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 400,
        ["Window = free buffer space at the receiver; advertised in every ACK header.",
         "Window slides forward as data is ACKed — the sender keeps the pipe full without drowning the receiver.",
         "Zero window = 'stop!' — sender probes periodically until the window reopens. A stuck zero window = stalled connection."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Congestion Control: CUBIC",
                       "Flow control protects the receiver; congestion control protects the NETWORK.")
    box(c, 72, 460, 468, 60, BOX_ORANGE, "Slow start", "cwnd doubles per RTT — exponential probe for capacity")
    box(c, 72, 380, 468, 60, BOX_RED, "Loss event", "packet loss = congestion signal → cut cwnd sharply")
    box(c, 72, 300, 468, 60, BOX_TEAL, "CUBIC growth", "window grows as a cubic function of time since last loss — fast recovery, gentle near the ceiling")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 260, "CUBIC is the Linux/macOS default: it finds high-bandwidth paths quickly and fairly shares with other flows.")
    note(c, 72, 150, 468, "BBR is the modern alternative: models the bottleneck's bandwidth and RTT instead of reacting to loss — better on lossy links.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "TCP Teardown & Reliability — Remember",
                 ["Graceful close is a 4-way FIN/ACK exchange — two independent half-closes.",
                  "TIME_WAIT (2×MSL) guards against lost final ACKs and zombie segments.",
                  "Retransmission: RTO timers, fast retransmit on 3 dup-ACKs, SACK for precision.",
                  "Sliding window = receiver-driven flow control; zero window means stop.",
                  "Congestion control (CUBIC) protects the network: slow start, then cubic growth after loss."],
                 pg)
    c.save(); print("wrote", path)


def pdf_udp(path):
    c = new_canvas(path); pg = 1
    title_page(c, "UDP\nVisual Guide",
               "Connectionless datagrams —\nfast, simple, and honest about it.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "Connectionless by Design",
                       "No handshake, no session, no promises.")
    box(c, 72, 420, 200, 90, BOX_GREEN, "UDP sender", "fire datagram\nand forget")
    box(c, 340, 420, 200, 90, BOX_BLUE, "UDP receiver", "gets it…\nor doesn't")
    arrow(c, 272, 465, 338, 465, color=GREEN, width=2.5, label="datagram")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 370,
        ["No connection setup: the first packet IS the data — zero round-trip overhead.",
         "No ordering, no retransmission, no flow control: packets may arrive late, duplicated, or never.",
         "The app takes responsibility for anything it actually needs (retries, sequencing) — or doesn't need it at all."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "The 8-Byte Header",
                       "The smallest transport header in common use — TCP's is 20+ bytes.")
    fields = [("Source port", "16 bits", BOX_BLUE), ("Dest port", "16 bits", BOX_GREEN),
              ("Length", "16 bits", BOX_ORANGE), ("Checksum", "16 bits", BOX_RED)]
    xx = 72
    for name, desc, fill in fields:
        box(c, xx, 440, 114, 70, fill, name, desc, font_size=10)
        xx += 120
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 380,
        ["That's the ENTIRE header: two ports, total length, checksum. Nothing else.",
         "No sequence numbers, no ACKs, no window — the fields TCP needs simply don't exist.",
         "Checksum is optional in IPv4 (often zeroed) but mandatory in IPv6."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Where UDP Wins",
                       "Real protocols that chose speed and simplicity.")
    uses = [("DNS", "One question, one answer — a handshake would double the latency.", BOX_BLUE),
            ("Gaming & VoIP", "A late packet is useless; drop it and move on. Jitter buffers smooth arrival.", BOX_GREEN),
            ("Live video (RTP)", "Losing a frame beats freezing the stream waiting for a retransmit.", BOX_ORANGE),
            ("QUIC / HTTP/3", "Reliability rebuilt in user space on top of UDP — the best of both.", BOX_TEAL)]
    yy = y
    for name, desc, fill in uses:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 74
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "UDP vs TCP: The Decision",
                       "Choose by what your app actually needs.")
    box(c, 72, y - 60, 225, 120, BOX_BLUE, "Pick TCP when", "correctness first:\nfiles, web APIs,\nemail, DB")
    box(c, 315, y - 60, 225, 120, BOX_GREEN, "Pick UDP when", "timeliness first:\nDNS, voice, games,\nlive media")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 220,
        ["Can you tolerate loss? Yes → UDP is on the table. No → TCP.",
         "Do stale packets hurt more than missing ones? (voice, games) → UDP.",
         "Want TCP reliability without TCP's head-of-line blocking? → QUIC over UDP."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "UDP's Sharp Edges",
                       "Know the trade-offs before you commit.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y,
        ["No congestion control: a UDP flood doesn't back off — it can starve TCP flows on the same link.",
         "Middlebox trouble: some firewalls and NATs treat UDP harshly; idle mappings expire fast (keep-alives needed).",
         "Amplification abuse: spoofed-source UDP services (DNS, NTP) power DDoS reflection — run with care, rate-limit responses.",
         "MTU matters: oversized datagrams fragment, and one lost fragment kills the whole datagram — stay under ~1400 bytes."],
        font_size=10.5, gap=28)
    note(c, 72, 130, 468, "Rule of thumb: UDP is a toolkit, not a transport with opinions. The reliability you skip must be consciously skipped — or rebuilt above it.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "UDP — Remember",
                 ["Connectionless: no handshake, no ordering, no retransmission — first packet is data.",
                  "8-byte header: source/dest ports, length, checksum. That's everything.",
                  "Wins where timeliness beats completeness: DNS, gaming, VoIP, live video, QUIC.",
                  "Choose UDP when stale data is worse than missing data.",
                  "Sharp edges: no congestion control, NAT timeouts, amplification abuse, fragmentation."],
                 pg)
    c.save(); print("wrote", path)


def pdf_dhcp(path):
    c = new_canvas(path); pg = 1
    title_page(c, "DHCP\nVisual Guide",
               "Dynamic Host Configuration —\nhow devices get an IP without anyone typing one.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "DORA: The Four-Step Dance",
                       "Discover → Offer → Request → Acknowledge.")
    box(c, 72, 460, 160, 60, BOX_BLUE, "Client", "no IP yet")
    box(c, 380, 460, 160, 60, BOX_GREEN, "DHCP Server", "owns the pool")
    msgs = [("DISCOVER", 152, 300, "broadcast: 'any DHCP out there?'"),
            ("OFFER", 460, 340, "'here's 192.168.1.50'"),
            ("REQUEST", 152, 300, "broadcast: 'I'll take it'"),
            ("ACK", 460, 340, "'it's yours for 24h'")]
    yy = 425
    for label, x1, x2, note_t in msgs:
        arrow(c, x1, yy, x2, yy, color=ACCENT, width=2, label=label)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8.5)
        c.drawCentredString(306, yy - 14, note_t)
        yy -= 42
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 220, "Early messages are BROADCASTS (255.255.255.255) — the client has no IP to be reached at yet.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Leases: Nothing Is Forever",
                       "IPs are rented, not owned — with renewal timers built in.")
    box(c, 72, 440, 468, 60, BOX_ORANGE, "Lease granted: 24 hours", "T1 = 12h (50%) → try to RENEW with original server")
    box(c, 72, 360, 468, 60, BOX_RED, "T2 = 21h (87.5%)", "no answer? REBIND — broadcast to ANY server")
    box(c, 72, 280, 468, 60, BOX_PURP, "Expiry", "lease lapses → stop using the IP, restart DORA")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 240, "Renewal is graceful: the client keeps its address across renewals — users never notice.")
    note(c, 72, 130, 468, "Short leases (hours) for guest Wi-Fi and hot-desks; long leases (days/weeks) for stable desktops and printers.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Relay Agents: Crossing Subnets",
                       "Broadcasts don't cross routers — so the router forwards for you.")
    box(c, 72, 420, 140, 80, BOX_BLUE, "Client", "subnet A")
    box(c, 236, 420, 140, 80, BOX_ORANGE, "Router +\nRelay agent", "converts broadcast\nto unicast")
    box(c, 400, 420, 140, 80, BOX_GREEN, "DHCP Server", "subnet B")
    arrow(c, 212, 460, 234, 460, color=ACCENT, width=2, label="broadcast")
    arrow(c, 376, 460, 398, 460, color=ACCENT, width=2, label="unicast (giaddr)")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 370,
        ["The relay stamps the giaddr field with the client's subnet so the server picks the right pool.",
         "One central DHCP server can serve dozens of VLANs — no server per subnet needed.",
         "'ip helper-address' on the router interface is the classic config line."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "DHCP Options: More Than an IP",
                       "The ACK carries the whole network bootstrap kit.")
    opts = [("Option 3 — Router", "default gateway: the way out of the subnet", BOX_BLUE),
            ("Option 6 — DNS", "name servers the client should query", BOX_GREEN),
            ("Option 51 — Lease time", "how long the address is valid", BOX_ORANGE),
            ("Option 66/67 — Boot", "TFTP server + boot file for PXE booting", BOX_TEAL),
            ("Option 15 — Domain", "DNS search suffix for short names", BOX_PURP)]
    yy = y
    for name, desc, fill in opts:
        box(c, 72, yy - 50, 468, 54, fill, name, desc, font_size=11)
        yy -= 66
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 190, "Options are TLV (type-length-value) — extensible without changing the protocol.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Rogue Servers & Hardening",
                       "DHCP trusts whoever answers first — that's the attack.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y,
        ["Rogue DHCP: an attacker answers DISCOVER first and hands out THEIR gateway — classic man-in-the-middle setup.",
         "DHCP snooping: switches allow DHCP replies only on trusted uplink ports; client-port replies are dropped.",
         "Starvation: attacker requests every address in the pool so legit clients get nothing — snooping + rate limits help.",
         "Reservations: bind critical hosts (printers, servers) to fixed IPs by MAC — still managed centrally."],
        font_size=10.5, gap=28)
    note(c, 72, 120, 468, "DHCPv6 exists but IPv6 leans on SLAAC for address assignment — DHCPv6 mainly delivers DNS and other options.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "DHCP — Remember",
                 ["DORA: Discover (broadcast) → Offer → Request → Ack — the client starts with no IP.",
                  "Leases expire; clients renew at 50% (T1) and rebind at 87.5% (T2).",
                  "Relay agents forward broadcasts across subnets with giaddr stamped in.",
                  "Options deliver gateway, DNS, lease time, boot info — a full bootstrap kit.",
                  "Harden with DHCP snooping: trust only uplink ports for server replies."],
                 pg)
    c.save(); print("wrote", path)


def pdf_nat(path):
    c = new_canvas(path); pg = 1
    title_page(c, "NAT\nVisual Guide",
               "Network Address Translation —\nhow one public IP serves a whole network.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "Private vs Public",
                       "RFC 1918 carved out addresses that never route on the internet.")
    box(c, 72, 440, 220, 90, BOX_BLUE, "Private (RFC 1918)", "10.0.0.0/8\n172.16.0.0/12\n192.168.0.0/16")
    box(c, 320, 440, 220, 90, BOX_GREEN, "Public", "globally unique\nroutable everywhere")
    arrow(c, 292, 485, 318, 485, color=ACCENT, width=2.5, label="NAT translates")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["Private addresses are reusable: every home can have 192.168.1.0/24 — they never collide because they never leave.",
         "NAT at the edge rewrites private → public on the way out, and reverses it on the way back.",
         "This is why IPv4 survived: billions of devices share a shrinking pool of public addresses."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "PAT: Port Address Translation",
                       "One public IP, thousands of sessions — ports are the multiplexing key.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, y, "Inside (private)                                          Outside (public)")
    box(c, 72, 400, 200, 60, BOX_BLUE, "192.168.1.10:5001", "laptop")
    box(c, 72, 320, 200, 60, BOX_BLUE, "192.168.1.11:5001", "phone")
    box(c, 340, 360, 200, 100, BOX_ORANGE, "NAT table", "1.10:5001 ↔ 203.0.113.7:61001\n1.11:5001 ↔ 203.0.113.7:61002")
    arrow(c, 272, 430, 338, 410, color=ACCENT, width=1.8)
    arrow(c, 272, 350, 338, 390, color=ACCENT, width=1.8)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 280,
        ["Outbound: source IP:port rewritten to the router's public IP + a unique port.",
         "Inbound reply: destination port looked up in the table → translated back to the private host.",
         "The 5-tuple (proto, src/dst IP, src/dst port) is the session key — 65k ports per public IP per protocol."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "The NAT Traversal Problem",
                       "NAT is stateful and one-directional: outsiders can't initiate in.")
    box(c, 72, 430, 200, 70, BOX_BLUE, "Your device", "behind NAT")
    box(c, 340, 430, 200, 70, BOX_RED, "Peer", "wants to connect")
    arrow(c, 272, 465, 338, 465, color=RED, width=2.5, label="blocked — no mapping")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 380,
        ["Inbound packets with no matching table entry are dropped — there's nowhere to deliver them.",
         "Workarounds: port forwarding (static mapping), UPnP (apps request mappings), hole punching (STUN).",
         "Last resort: TURN relay — both peers connect OUT to a relay that bridges them (costs bandwidth).",
         "This is why P2P apps, VoIP, and games fight NAT — and why IPv6's end-to-end model is appealing."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "CGNAT: NAT at ISP Scale",
                       "Carrier-Grade NAT — your ISP NATs you before you reach the internet.")
    box(c, 72, 420, 140, 80, BOX_BLUE, "You", "100.64.x.x\n(shared space)")
    box(c, 236, 420, 140, 80, BOX_ORANGE, "ISP CGNAT", "100.64/10 →\npublic pool")
    box(c, 400, 420, 140, 80, BOX_GREEN, "Internet", "sees ISP's IP")
    arrow(c, 212, 460, 234, 460, color=ACCENT, width=2)
    arrow(c, 376, 460, 398, 460, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 370,
        ["ISPs ran out of IPv4 too — CGNAT lets hundreds of customers share one public address (100.64.0.0/10 is the shared space).",
         "Double NAT (your router + CGNAT) breaks port forwarding entirely — no inbound services from home.",
         "Port quotas per customer are tight — heavy P2P/gaming users feel it first."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "NAT Types & Behavior",
                       "Not all NATs treat new sessions the same.")
    nats = [("Full cone", "Any external host can reply once an outbound mapping exists — most permissive.", BOX_GREEN),
            ("Restricted cone", "Only hosts you've already contacted can send inbound.", BOX_ORANGE),
            ("Port-restricted", "Only the exact IP:port you've contacted can reply.", BOX_RED),
            ("Symmetric", "Different external port PER destination — hardest to traverse.", BOX_PURP)]
    yy = y
    for name, desc, fill in nats:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 74
    note(c, 72, 130, 468, "STUN discovers your NAT type and public mapping — the first step every WebRTC call takes before hole punching.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "NAT — Remember",
                 ["Private (RFC 1918) addresses never route publicly; NAT rewrites them at the edge.",
                  "PAT multiplexes thousands of sessions onto one public IP using source ports.",
                  "NAT is one-directional: inbound needs a mapping — hence port forwarding, STUN, TURN.",
                  "CGNAT stacks a second NAT at the ISP; home port forwarding stops working.",
                  "NAT types (full cone → symmetric) determine how hard traversal is."],
                 pg)
    c.save(); print("wrote", path)


def pdf_subnets(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Subnets & CIDR\nVisual Guide",
               "Carving address space —\nmask math, subnet design, and VPC layouts.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 6, "Mask Math: Bits Decide",
                       "The mask splits 32 bits into network part and host part.")
    c.setFont(MONO_FONT, 10); c.setFillColor(INK)
    c.drawString(72, y,     "IP:   192.168.1.130  =  11000000.10101000.00000001.10000010")
    c.drawString(72, y - 24, "Mask: 255.255.255.0  =  11111111.11111111.11111111.00000000  (/24)")
    c.drawString(72, y - 48, "AND → 192.168.1.0    =  network address (host bits zeroed)")
    c.setFillColor(ACCENT); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y - 80, "Prefix length = number of 1-bits. /24 means the first 24 bits are network.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 116,
        ["CIDR /n is just shorthand for the mask — /24 = 255.255.255.0, /16 = 255.255.0.0.",
         "Hosts = 2^(32-n) − 2 (subtract network + broadcast). /24 → 254 usable hosts.",
         "Bitwise AND of IP and mask always gives the network address."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Subnetting a Block: Worked Example",
                       "Split 192.168.1.0/24 into 4 equal subnets — borrow 2 bits.")
    box(c, 72, 420, 468, 60, BOX_BLUE, "192.168.1.0/24 — 256 addresses", "borrow 2 host bits → 4 × /26 (64 addresses each)")
    subs = [("192.168.1.0/26", ".1 – .62", "host .63 bcast", BOX_GREEN),
            ("192.168.1.64/26", ".65 – .126", "host .127 bcast", BOX_TEAL),
            ("192.168.1.128/26", ".129 – .190", "host .191 bcast", BOX_ORANGE),
            ("192.168.1.192/26", ".193 – .254", "host .255 bcast", BOX_PURP)]
    yy = 400
    for name, rng, bc, fill in subs:
        box(c, 72, yy - 48, 468, 52, fill, name, rng + "   •   " + bc, font_size=10.5)
        yy -= 62
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Network, Broadcast, Usable",
                       "Two addresses in every subnet are spoken for.")
    box(c, 72, 440, 140, 80, BOX_RED, "Network", "all host bits 0\n.0 — identifies\nthe subnet")
    box(c, 236, 440, 140, 80, BOX_GREEN, "Usable", ".1 – .254\nassigned to\nhosts")
    box(c, 400, 440, 140, 80, BOX_ORANGE, "Broadcast", "all host bits 1\n.255 — every\nhost on subnet")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["Routers use the network address in routing tables; hosts never configure it on an interface.",
         "Broadcast reaches every host in the subnet — DHCP DISCOVER and ARP rely on it.",
         "First usable (.1) is the conventional gateway address — convention, not law."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "The CIDR Cheat Sheet",
                       "Memorize the common ones; derive the rest.")
    rows = [("/32", "1", "single host route", BOX_RED),
            ("/30", "4 (2 usable)", "point-to-point links", BOX_ORANGE),
            ("/29", "8 (6 usable)", "tiny subnets", BOX_ORANGE),
            ("/28", "16 (14 usable)", "small VLANs", BOX_TEAL),
            ("/24", "256 (254 usable)", "the classic LAN", BOX_GREEN),
            ("/16", "65,536", "large org / B-class", BOX_BLUE),
            ("/8", "16.7M", "huge (10.0.0.0/8)", BOX_PURP)]
    yy = y
    for prefix, addrs, use, fill in rows:
        box(c, 72, yy - 44, 110, 48, fill, prefix, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
        c.drawString(200, yy - 18, addrs + " addresses  —  " + use)
        yy -= 58
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "VPC Subnet Design",
                       "Cloud networks are subnets with extra rules.")
    box(c, 72, 430, 468, 70, BOX_BLUE, "VPC 10.0.0.0/16", "your private cloud network — you carve it up")
    box(c, 72, 330, 225, 70, BOX_GREEN, "public 10.0.1.0/24", "route to internet\ngateway")
    box(c, 315, 330, 225, 70, BOX_ORANGE, "private 10.0.2.0/24", "NAT gateway only\nno inbound")
    box(c, 72, 230, 225, 70, BOX_TEAL, "AZ-a copies", "repeat per\navailability zone")
    box(c, 315, 230, 225, 70, BOX_PURP, "AZ-b copies", "survive zone\nfailure")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 190, "Reserve space: subnets can't be resized later — leave gaps (10.0.10.0/24, 10.0.20.0/24…) for growth.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Supernetting & Route Aggregation",
                       "CIDR works in reverse too — combine routes to shrink tables.")
    box(c, 72, 440, 140, 70, BOX_GREEN, "10.0.1.0/24", "")
    box(c, 236, 440, 140, 70, BOX_GREEN, "10.0.2.0/24", "")
    box(c, 400, 440, 140, 70, BOX_GREEN, "10.0.3.0/24", "")
    arrow(c, 142, 438, 200, 400, color=ACCENT, width=1.5)
    arrow(c, 306, 438, 270, 400, color=ACCENT, width=1.5)
    arrow(c, 470, 438, 340, 400, color=ACCENT, width=1.5)
    box(c, 156, 320, 300, 70, BOX_BLUE, "10.0.0.0/22", "one summary route\ncovers all three")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 280, "Internet routers hold ~1M routes only because ISPs aggregate — without it the table would be billions of rows.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Subnets & CIDR — Remember",
                 ["The mask splits bits: /n = first n bits are network; hosts = 2^(32−n) − 2.",
                  "Subnet by borrowing host bits: /24 → four /26s of 64 addresses each.",
                  "Network (all-0) and broadcast (all-1) addresses are never assigned to hosts.",
                  "VPC design: public/private subnets per AZ, with gaps left for growth.",
                  "Supernetting aggregates routes — it's why the global routing table stays near ~1M entries."],
                 pg)
    c.save(); print("wrote", path)


def pdf_routing(path):
    c = new_canvas(path); pg = 1
    title_page(c, "BGP & OSPF\nVisual Guide",
               "How the internet routes —\nlink-state inside, path-vector between networks.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 6, "IGP vs EGP: Two Different Jobs",
                       "Inside your network vs between networks — different problems, different protocols.")
    box(c, 72, y - 60, 225, 130, BOX_BLUE, "IGP", "Interior Gateway\nOSPF, IS-IS, EIGRP\none admin domain\nfast convergence")
    box(c, 315, y - 60, 225, 130, BOX_GREEN, "EGP", "Exterior Gateway\nBGP — the ONLY one\nbetween ASes\npolicy over speed")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 230,
        ["IGP: you control every router — optimize for speed and shortest path.",
         "EGP: you control nothing beyond your border — optimize for POLICY (who you peer with, what you announce).",
         "An Autonomous System (AS) is a network under one admin — the internet is ~75k ASes stitched by BGP."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "OSPF: Link-State & Areas",
                       "Every router learns the whole map, then runs Dijkstra.")
    box(c, 196, 440, 220, 70, BOX_BLUE, "Area 0 — Backbone", "all areas connect\nhere")
    box(c, 72, 320, 160, 70, BOX_GREEN, "Area 1", "office")
    box(c, 380, 320, 160, 70, BOX_GREEN, "Area 2", "datacenter")
    arrow(c, 152, 358, 250, 438, color=ACCENT, width=1.5)
    arrow(c, 460, 358, 360, 438, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 280,
        ["Link-state: routers flood link costs; each builds an identical topology map and computes shortest paths locally.",
         "Areas contain the flooding — Area 0 (backbone) ties them together; ABRs summarize between areas.",
         "Converges in seconds; metric is cost (bandwidth-based). Hello packets maintain neighbor adjacencies."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "BGP: Path Vector",
                       "BGP doesn't compute paths — it ANNOUNCES them, AS by AS.")
    box(c, 72, 430, 120, 70, BOX_BLUE, "AS 100", "origin")
    box(c, 216, 430, 120, 70, BOX_GREEN, "AS 200", "")
    box(c, 360, 430, 120, 70, BOX_ORANGE, "AS 300", "")
    arrow(c, 192, 465, 214, 465, color=ACCENT, width=2, label="100")
    arrow(c, 336, 465, 358, 465, color=ACCENT, width=2, label="100 200")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10)
    c.drawString(72, 380, "AS 300 learns:  'prefix P reachable via AS-path [300←200←100]'")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 340,
        ["AS-path = the list of ASes an announcement traversed; loop prevention is free (drop paths containing your own AS).",
         "Shortest AS-path usually wins — but policy (local-pref, MED) can override it.",
         "BGP runs over TCP/179 between border routers; full table is ~1M prefixes."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "How a Packet Crosses the Internet",
                       "Hop by AS, decision by decision.")
    hops = [("Your ISP (AS 1)", "OSPF inside; default route outward", BOX_BLUE),
            ("Transit provider", "BGP picks cheapest policy-compliant path", BOX_GREEN),
            ("Peer / IX", "settlement-free peering at exchange points", BOX_TEAL),
            ("Destination AS", "announces the prefix; delivers to host", BOX_ORANGE)]
    yy = y; xx = 72
    for name, desc, fill in hops:
        box(c, xx, yy - 60, 108, 90, fill, name, desc, font_size=9)
        if xx > 72:
            arrow(c, xx - 12, yy - 15, xx, yy - 15, color=ACCENT, width=2)
        xx += 120
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, yy - 110,
        ["Each AS makes its own independent routing decision — there is no central internet routing brain.",
         "Hot-potato routing: hand the packet to the next AS as quickly as possible.",
         "Traceroute shows this path router-by-router (when ICMP isn't filtered)."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "BGP Route Selection",
                       "Longest match first, then policy, then shortest path.")
    steps = [("1. Longest prefix match", "most specific route always wins", BOX_BLUE),
             ("2. Highest local-pref", "your policy: prefer this exit", BOX_GREEN),
             ("3. Shortest AS-path", "fewest AS hops", BOX_ORANGE),
             ("4. Lowest MED / IGP cost", "tie-breakers toward the exit", BOX_TEAL)]
    yy = y
    for name, desc, fill in steps:
        box(c, 72, yy - 50, 468, 54, fill, name, desc, font_size=11)
        yy -= 66
    note(c, 72, 170, 468, "BGP hijack: announce someone else's prefix with a better path — traffic diverts to the attacker. RPKI/ROA validation is the defense.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Convergence: When Things Break",
                       "Routing protocols heal — at different speeds.")
    box(c, 72, 420, 225, 90, BOX_GREEN, "OSPF", "link-state flood\nconverges in\nSECONDS")
    box(c, 315, 420, 225, 90, BOX_ORANGE, "BGP", "path exploration\nconverges in\nMINUTES")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 380,
        ["Link failure inside your network: OSPF floods the change, all routers recompute — done in seconds.",
         "BGP failure: withdrawals propagate AS by AS; routers explore alternate paths — can take minutes globally.",
         "Design for it: redundant links, BFD for fast failure detection, anycast for instant failover."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "BGP & OSPF — Remember",
                 ["IGP (OSPF) routes inside one admin domain; EGP (BGP) routes between Autonomous Systems.",
                  "OSPF: link-state — every router maps the topology and runs Dijkstra; areas contain flooding.",
                  "BGP: path-vector — AS-path announcements; loop-free by construction, policy-driven.",
                  "Route selection: longest match → local-pref → shortest AS-path → tie-breakers.",
                  "OSPF converges in seconds; BGP failover can take minutes — design redundancy accordingly."],
                 pg)
    c.save(); print("wrote", path)


def pdf_http2_http3(path):
    c = new_canvas(path); pg = 1
    title_page(c, "HTTP/2 & HTTP/3\nVisual Guide",
               "Beyond HTTP/1.1 —\nmultiplexing, header compression, and QUIC.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "HTTP/1.1: Head-of-Line Blocking",
                       "One request at a time per connection — the browser opens 6+ to cope.")
    for i in range(4):
        box(c, 72 + i * 120, 440, 108, 60, BOX_BLUE if i == 0 else BOX_PURP, f"req {i+1}", "waiting…" if i else "in flight")
    arrow(c, 72, 420, 540, 420, color=RED, width=2.5, label="one at a time — requests queue behind each other")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 380,
        ["Text protocol, one request per connection at a time — a slow asset blocks everything behind it.",
         "Workarounds: domain sharding, spriting, inlining — hacks to dodge the protocol's limits.",
         "Keep-alive reuses connections but doesn't fix the queueing. Pipelining was broken in practice."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "HTTP/2: Multiplexing",
                       "Many streams, one connection — binary framing kills the queue.")
    box(c, 72, 430, 468, 50, BOX_BLUE, "single TCP connection", "all streams share it")
    cols = [BOX_GREEN, BOX_ORANGE, BOX_TEAL]
    for i in range(3):
        box(c, 72 + i * 160, 350, 148, 60, cols[i], f"stream {i+1}", "interleaved frames")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 310,
        ["Binary framing: requests split into frames, multiplexed by stream ID — no head-of-line blocking between streams.",
         "Server push (mostly abandoned) and stream priorities: the browser hints what matters first.",
         "One catch: TCP-level head-of-line blocking remains — one lost TCP packet stalls ALL streams. That's what HTTP/3 fixes."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "HPACK & QPACK: Header Compression",
                       "HTTP headers are repetitive — stop resending them.")
    box(c, 72, 440, 468, 60, BOX_ORANGE, "HPACK (HTTP/2)", "dynamic table: 'user-agent: …' sent once, referenced by index after")
    box(c, 72, 360, 468, 60, BOX_TEAL, "QPACK (HTTP/3)", "same idea, redesigned for QUIC's out-of-order streams")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 320,
        ["Typical savings: hundreds of bytes per request → a few. Huge on mobile and high-request pages.",
         "Static table covers common headers; the dynamic table learns per-connection patterns.",
         "CRIME-style attacks taught a lesson: compression + attacker-controlled input needs careful design."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "HTTP/3: QUIC Transport",
                       "Drops TCP entirely — runs over UDP with TLS 1.3 baked in.")
    box(c, 72, 440, 468, 60, BOX_BLUE, "HTTP/1.1", "TCP + (optional) TLS — 3+ RTT to first byte")
    box(c, 72, 360, 468, 60, BOX_GREEN, "HTTP/2", "TCP + TLS 1.2/1.3 — multiplexed, still TCP-limited")
    box(c, 72, 280, 468, 60, BOX_ORANGE, "HTTP/3", "QUIC over UDP — 0/1-RTT handshake, per-stream independence")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 240, "A lost packet stalls only ITS stream now — TCP's shared fate is gone. Connection migration survives IP changes (Wi-Fi → cellular).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "The Upgrade Path",
                       "Negotiation is automatic — servers and browsers agree on the best version.")
    box(c, 72, 440, 140, 70, BOX_BLUE, "h1", "fallback")
    box(c, 236, 440, 140, 70, BOX_GREEN, "h2", "ALPN picks")
    box(c, 400, 440, 140, 70, BOX_ORANGE, "h3", "Alt-Svc advertises")
    arrow(c, 212, 475, 234, 475, color=ACCENT, width=2)
    arrow(c, 376, 475, 398, 475, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["TLS ALPN negotiates h2 during the handshake; Alt-Svc headers advertise h3/QUIC availability.",
         "Deployment: enable h2/h3 on your CDN or load balancer first — origin can lag behind safely.",
         "Measure: multiplexing helps most on high-latency, lossy, or asset-heavy pages."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "HTTP/2 & HTTP/3 — Remember",
                 ["HTTP/1.1 serializes requests per connection — head-of-line blocking forced hacks like sharding.",
                  "HTTP/2 multiplexes binary-framed streams over one TCP connection.",
                  "HPACK/QPACK compress repetitive headers to a few bytes via indexed tables.",
                  "HTTP/3 replaces TCP with QUIC over UDP: 0/1-RTT, per-stream loss independence, connection migration.",
                  "Negotiation is automatic (ALPN, Alt-Svc) — deploy at the edge first."],
                 pg)
    c.save(); print("wrote", path)


def pdf_vpns(path):
    c = new_canvas(path); pg = 1
    title_page(c, "VPNs\nVisual Guide",
               "Tunnels through the internet —\nprivate networks over public wires.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "The Tunneling Concept",
                       "Wrap private packets inside public ones — the internet sees only the tunnel.")
    box(c, 72, 420, 130, 80, BOX_BLUE, "Your device", "10.0.0.5")
    box(c, 410, 420, 130, 80, BOX_GREEN, "Office net", "10.1.0.0/16")
    c.setFillColor(BOX_ORANGE); c.roundRect(222, 410, 168, 100, 8, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 10)
    c.drawCentredString(306, 480, "encrypted tunnel")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9)
    c.drawCentredString(306, 464, "internet sees only")
    c.drawCentredString(306, 450, "outer endpoints")
    c.drawCentredString(306, 436, "payload hidden")
    arrow(c, 202, 460, 220, 460, color=ACCENT, width=2)
    arrow(c, 390, 460, 408, 460, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 370,
        ["Encapsulation: the original packet becomes the PAYLOAD of a new outer packet.",
         "Encryption + authentication: confidentiality plus proof nobody tampered in transit.",
         "To your apps, the tunnel looks like a local network interface (tun0)."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "IPsec vs WireGuard vs OpenVPN",
                       "Three generations of tunneling.")
    protos = [("IPsec", "IETF standard, kernel-level. IKEv2 key exchange. Complex but ubiquitous — site-to-site default.", BOX_BLUE),
              ("OpenVPN", "TLS-based, user space. Very flexible, very configurable — and slower for it.", BOX_GREEN),
              ("WireGuard", "Modern, ~4k lines. ChaCha20/Noise. Roams across networks; connects in milliseconds.", BOX_ORANGE)]
    yy = y
    for name, desc, fill in protos:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=11)
        yy -= 78
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 200, "New deployments default to WireGuard unless compliance or legacy gear demands IPsec.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Site-to-Site vs Remote Access",
                       "Two topologies, two use cases.")
    box(c, 72, y - 60, 225, 120, BOX_BLUE, "Site-to-site", "router ↔ router\nwhole networks joined\nalways-on (IPsec)")
    box(c, 315, y - 60, 225, 120, BOX_GREEN, "Remote access", "device ↔ gateway\none user at a time\non-demand client")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 220,
        ["Site-to-site: branch offices behave as one LAN — printers, file shares, internal DNS all reachable.",
         "Remote access: the traveling laptop joins the office net; split-tunnel keeps Netflix local, full-tunnel routes everything.",
         "Zero-trust trend: per-app authenticated access is replacing 'VPN = inside the castle' thinking."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "What a VPN Packet Looks Like",
                       "Headers inside headers — each layer adds its envelope.")
    c.setFont(MONO_FONT, 9.5); c.setFillColor(INK)
    c.drawString(72, y,     "[ outer IP | ESP header | inner IP | TCP | app data | ESP trailer/auth ]")
    c.drawString(72, y - 26, "  └─ routable ─┘ └──── encrypted + authenticated ────┘")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 62,
        ["ESP (Encapsulating Security Payload) provides the encryption and integrity in IPsec tunnel mode.",
         "An observer sees: tunnel endpoints, packet sizes, timing — NOT contents. Traffic analysis is still possible.",
         "MTU shrinks: the tunnel eats 40-80 bytes — clamp MSS or fragment to avoid black-hole stalls."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Encryption Overhead & Gotchas",
                       "Security costs something — budget for it.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y,
        ["Throughput: encryption is cheap on modern CPUs (AES-NI); the bottleneck is usually the tunnel endpoint's bandwidth.",
         "Latency: +1 RTT-ish for crypto plus the detour via the VPN gateway — pick nearby exit points.",
         "DNS leaks: a VPN that doesn't tunnel DNS exposes every lookup — verify with a leak test.",
         "Kill switch: if the tunnel drops, block traffic rather than silently sending it in the clear."],
        font_size=10.5, gap=28)
    note(c, 72, 130, 468, "A consumer VPN hides traffic from the local network/ISP — but the VPN provider sees it all. Trust is the real protocol.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "VPNs — Remember",
                 ["Tunneling = private packets wrapped as payload inside public, encrypted packets.",
                  "IPsec (site-to-site standard), OpenVPN (flexible TLS), WireGuard (modern default).",
                  "Site-to-site joins networks; remote access joins individual devices.",
                  "Observers still see endpoints, sizes, timing — encryption hides contents, not metadata.",
                  "Watch MTU shrinkage, DNS leaks, and always run a kill switch."],
                 pg)
    c.save(); print("wrote", path)


def pdf_firewalls(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Firewalls\nVisual Guide",
               "Drawing the line —\nstateless vs stateful, zones, and rule craft.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "Stateless vs Stateful",
                       "Amnesia vs memory — the fundamental divide.")
    box(c, 72, y - 60, 225, 130, BOX_RED, "Stateless", "each packet judged\nalone: src/dst/port\nno memory of before")
    box(c, 315, y - 60, 225, 130, BOX_GREEN, "Stateful", "tracks connections\nin a state table\nreply traffic auto-\nallowed")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 230,
        ["Stateless: fast, simple — but return traffic needs explicit mirror rules, and it's blind to context.",
         "Stateful: remembers the 5-tuple of every connection; ACKs for known sessions pass automatically.",
         "Modern firewalls are stateful by default; stateless survives in high-speed ACLs and DDoS scrubbing."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Zones: Trust Has Geography",
                       "Segment the network so one breach doesn't own everything.")
    box(c, 72, 400, 130, 90, BOX_RED, "Internet", "untrusted")
    box(c, 226, 400, 130, 90, BOX_ORANGE, "DMZ", "public servers\nweb, mail")
    box(c, 380, 400, 130, 90, BOX_GREEN, "Internal", "workstations\ntrusted")
    arrow(c, 202, 445, 224, 445, color=ACCENT, width=2)
    arrow(c, 356, 445, 378, 445, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 360,
        ["DMZ hosts are reachable from the internet but isolated from the interior — a compromised web server can't pivot freely.",
         "Default flows: internet → DMZ (limited ports), internal → anywhere, DMZ → internal (almost nothing).",
         "Cloud version: public subnets, private subnets, and security groups per tier — same idea, new names."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Rule Ordering Matters",
                       "First match wins — order is the policy.")
    rules = [("1. ALLOW established", "return traffic for known connections", BOX_GREEN),
             ("2. ALLOW 443 → web DMZ", "public HTTPS in", BOX_BLUE),
             ("3. ALLOW internal → any", "outbound browsing", BOX_TEAL),
             ("4. DENY all", "implicit — the safety net", BOX_RED)]
    yy = y
    for name, desc, fill in rules:
        box(c, 72, yy - 50, 468, 54, fill, name, desc, font_size=11)
        yy -= 66
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 220, "A broad ALLOW above a narrow DENY silently defeats it — audit top-down, most specific first.")
    note(c, 72, 130, 468, "Default-deny: if no rule matches, DROP. Every firewall policy should end with an explicit deny-all.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "iptables Chain Flow",
                       "Packets walk chains; each chain is an ordered rule list.")
    box(c, 72, 440, 120, 60, BOX_BLUE, "PREROUTING", "DNAT here")
    box(c, 216, 440, 120, 60, BOX_GREEN, "INPUT", "to this host")
    box(c, 360, 440, 120, 60, BOX_ORANGE, "FORWARD", "routed thru")
    box(c, 216, 330, 120, 60, BOX_TEAL, "OUTPUT", "from this host")
    box(c, 360, 330, 120, 60, BOX_PURP, "POSTROUTING", "SNAT here")
    arrow(c, 192, 470, 214, 470, color=ACCENT, width=1.8)
    arrow(c, 336, 470, 358, 470, color=ACCENT, width=1.8)
    arrow(c, 276, 438, 276, 392, color=ACCENT, width=1.8, label="local?")
    arrow(c, 420, 438, 420, 392, color=ACCENT, width=1.8, label="transit")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 290, "nftables unifies this into one engine, but the chain mental model carries over.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Beyond Packets: NGFW & WAF",
                       "Modern firewalls read up the stack.")
    feats = [("Next-gen firewall (NGFW)", "App-aware: 'allow Slack, block BitTorrent' — not just ports. TLS inspection, IDS/IPS built in.", BOX_BLUE),
             ("WAF", "HTTP-layer: blocks SQLi, XSS, and OWASP Top-10 patterns before they reach the app.", BOX_GREEN),
             ("Egress filtering", "Control what's allowed OUT — malware phones home; don't let it.", BOX_ORANGE)]
    yy = y
    for name, desc, fill in feats:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=11)
        yy -= 78
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 220, "Defense in depth: packet filter at the edge, WAF in front of apps, host firewall on every machine.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Firewalls — Remember",
                 ["Stateless judges packets alone; stateful tracks connections and auto-allows replies.",
                  "Zones (internet / DMZ / internal) contain breaches — limit DMZ→internal to near zero.",
                  "Rules are first-match-wins: order most-specific first, end with explicit deny-all.",
                  "iptables chains: PREROUTING → INPUT/FORWARD → OUTPUT → POSTROUTING.",
                  "Layer up: NGFW for apps, WAF for HTTP attacks, egress filtering for exfiltration."],
                 pg)
    c.save(); print("wrote", path)


def pdf_proxies(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Forward & Reverse\nProxies",
               "The middlemen of the web —\nwho they serve, and what they rewrite.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "Forward Proxy: For the Client",
                       "Sits in front of CLIENTS, fetching on their behalf.")
    box(c, 72, 430, 120, 70, BOX_BLUE, "Clients", "")
    box(c, 216, 430, 140, 70, BOX_ORANGE, "Forward\nproxy", "acts as the\nclient")
    box(c, 380, 430, 160, 70, BOX_GREEN, "Internet", "sees the proxy's\nIP, not yours")
    arrow(c, 192, 465, 214, 465, color=ACCENT, width=2)
    arrow(c, 356, 465, 378, 465, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["Use cases: corporate web filtering, caching, anonymity, bypassing geo-blocks.",
         "The server never sees the real client — the proxy's IP is the source.",
         "CONNECT method tunnels TLS through it; the proxy sees the destination, not the content."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Reverse Proxy: For the Server",
                       "Sits in front of SERVERS, presenting one face to the world.")
    box(c, 72, 430, 160, 70, BOX_BLUE, "Internet", "one public IP")
    box(c, 256, 430, 140, 70, BOX_ORANGE, "Reverse\nproxy", "routes,\ncaches, shields")
    box(c, 420, 430, 120, 70, BOX_GREEN, "App\nservers", "hidden")
    arrow(c, 232, 465, 254, 465, color=ACCENT, width=2)
    arrow(c, 396, 465, 418, 465, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["Use cases: TLS termination, caching, request routing, hiding backend topology.",
         "Clients never learn backend IPs — the proxy is the only public surface.",
         "nginx, HAProxy, Envoy, Cloudflare: all primarily reverse proxies."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Header Surgery: X-Forwarded-For",
                       "Proxies rewrite identity — headers carry the truth (if you trust them).")
    c.setFont(MONO_FONT, 9.5); c.setFillColor(INK)
    c.drawString(72, y,     "X-Forwarded-For: 203.0.113.7, 198.51.100.23")
    c.drawString(72, y - 24, "X-Forwarded-Proto: https")
    c.drawString(72, y - 48, "Forwarded: for=203.0.113.7; proto=https  (RFC 7239, the standard)")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 84,
        ["Each proxy APPENDS the client IP it saw — leftmost is the original client (usually).",
         "Spoofable: anyone can inject X-Forwarded-For — only trust it from YOUR proxies (strip at the edge).",
         "Apps behind proxies must read these headers for real IPs, correct redirects (http→https), and rate limiting."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Transparent Proxy",
                       "Intercepts traffic without the client knowing — or consenting to config.")
    box(c, 72, 430, 140, 70, BOX_BLUE, "Client", "no proxy\nsettings")
    box(c, 236, 430, 160, 70, BOX_RED, "Intercepting\nproxy", "traffic diverted\nby the network")
    box(c, 420, 430, 120, 70, BOX_GREEN, "Internet", "")
    arrow(c, 212, 465, 234, 465, color=RED, width=2, label="redirected")
    arrow(c, 396, 465, 418, 465, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["Deployed by ISPs and enterprises: port-80/443 traffic steered via routing or WCCP.",
         "HTTPS interception requires a trusted CA on the client — effectively a sanctioned MITM.",
         "Controversial for privacy; common for malware scanning and data-loss prevention."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Load Balancer as Reverse Proxy",
                       "Every load balancer is a reverse proxy with a scheduling algorithm.")
    box(c, 72, 440, 140, 70, BOX_BLUE, "Clients", "")
    box(c, 236, 440, 140, 70, BOX_ORANGE, "LB", "least-conn /\nround-robin")
    box(c, 400, 60, 60, 70, BOX_GREEN, "web-1", "")
    box(c, 400, 150, 60, 70, BOX_GREEN, "web-2", "")
    box(c, 400, 240, 60, 70, BOX_GREEN, "web-3", "")
    arrow(c, 212, 475, 234, 475, color=ACCENT, width=2)
    arrow(c, 376, 500, 398, 500, color=ACCENT, width=1.5)
    arrow(c, 376, 475, 398, 475, color=ACCENT, width=1.5)
    arrow(c, 376, 450, 398, 450, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["Health checks: dead backends are pulled from rotation automatically.",
         "Sticky sessions: route the same client to the same backend when state is local.",
         "L4 (TCP) vs L7 (HTTP): L7 can route by path/host header; L4 just spreads connections."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Proxies — Remember",
                 ["Forward proxy serves clients (filtering, caching, anonymity); reverse proxy serves servers (TLS, routing, shielding).",
                  "X-Forwarded-For carries the real client IP — append-only, spoofable, trust only your own proxies.",
                  "Transparent proxies intercept without client config — powerful, privacy-sensitive.",
                  "A load balancer is a reverse proxy that distributes: health checks, algorithms, L4 vs L7.",
                  "The proxy is a trust boundary: it sees destinations (forward) or full requests (reverse) — choose operators accordingly."],
                 pg)
    c.save(); print("wrote", path)


def pdf_websockets(path):
    c = new_canvas(path); pg = 1
    title_page(c, "WebSockets\nVisual Guide",
               "Full-duplex over HTTP's bones —\nreal-time messaging for the web.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "The Upgrade Handshake",
                       "Starts as HTTP, then both sides agree to stop speaking HTTP.")
    c.setFont(MONO_FONT, 9.5); c.setFillColor(INK)
    c.drawString(72, y,     "GET /chat HTTP/1.1")
    c.drawString(72, y - 22, "Upgrade: websocket      Connection: Upgrade")
    c.drawString(72, y - 44, "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==")
    c.drawString(72, y - 76, "HTTP/1.1 101 Switching Protocols")
    c.drawString(72, y - 98, "Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 134,
        ["The handshake is plain HTTP — so it passes through existing proxies and firewalls.",
         "101 Switching Protocols: from here the TCP connection speaks the WebSocket framing protocol.",
         "The accept key proves the server understands WebSocket (SHA-1 of key + magic GUID)."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Frames: The Wire Format",
                       "Lightweight envelopes — ~2 bytes overhead per message.")
    box(c, 72, 430, 90, 60, BOX_BLUE, "FIN+opcode", "text/binary\nping/pong")
    box(c, 162, 430, 90, 60, BOX_GREEN, "mask+len", "client→server\nmasked")
    box(c, 252, 430, 120, 60, BOX_ORANGE, "mask key", "4 bytes\n(XOR)")
    box(c, 372, 430, 168, 60, BOX_TEAL, "payload", "the message")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["Opcodes: text (0x1), binary (0x2), close (0x8), ping (0x9), pong (0xA).",
         "Client frames are MASKED with a random key — defeats cache-poisoning attacks on proxies.",
         "Ping/pong keep idle connections alive through NATs and load balancers."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Full-Duplex Messaging",
                       "Either side sends anytime — no request/response turn-taking.")
    box(c, 72, 430, 160, 70, BOX_BLUE, "Browser", "")
    box(c, 380, 430, 160, 70, BOX_GREEN, "Server", "")
    arrow(c, 232, 480, 378, 480, color=ACCENT, width=2, label='{"type":"chat"}')
    arrow(c, 378, 450, 232, 450, color=GREEN, width=2, label='{"type":"typing"}')
    arrow(c, 232, 420, 378, 420, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 380,
        ["Chat, live dashboards, multiplayer games, collaborative editing — anywhere latency matters.",
         "Message-based, not stream-based: each frame is a discrete message your app handles.",
         "One persistent connection replaces constant polling — far less header overhead."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "WebSocket vs SSE vs Long-Polling",
                       "Three ways to push — pick by direction and complexity.")
    opts = [("Long-polling", "Client holds a request open; server answers when data arrives. Simple, works everywhere, chatty.", BOX_PURP),
            ("SSE", "Server→client text stream over HTTP. Auto-reconnect, simple — but one-directional.", BOX_BLUE),
            ("WebSocket", "True bidirectional binary/text messaging. Most capable, most connection state to manage.", BOX_GREEN)]
    yy = y
    for name, desc, fill in opts:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 74
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 220, "Decision: need client→server pushes? WebSocket. Server→client feed only? SSE is simpler.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Scaling WebSockets",
                       "Stateful connections change your architecture.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y,
        ["Sticky sessions or a pub/sub backplane (Redis): a message for user X must reach the server holding X's socket.",
         "Connection counts: 100k idle sockets is normal — tune file descriptors, use event loops (not thread-per-connection).",
         "Proxies must support Upgrade (most do now); set generous idle timeouts or send heartbeats.",
         "Auth once at handshake (token in query/header) — then trust the socket, but revalidate on sensitive actions."],
        font_size=10.5, gap=28)
    note(c, 72, 130, 468, "wss:// (TLS) everywhere in production — ws:// leaks everything and mixed-content rules will block it anyway.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "WebSockets — Remember",
                 ["HTTP Upgrade handshake → 101 Switching Protocols → persistent framed connection.",
                  "Frames carry opcodes (text/binary/ping/pong); client frames are masked.",
                  "Full-duplex: either side sends anytime — ideal for chat, live data, games.",
                  "SSE for server→client feeds; long-polling for max compatibility; WebSocket for bidirectional.",
                  "Scale with a pub/sub backplane, heartbeats, and wss:// always."],
                 pg)
    c.save(); print("wrote", path)


def pdf_grpc(path):
    c = new_canvas(path); pg = 1
    title_page(c, "gRPC\nVisual Guide",
               "Contract-first RPC —\nprotobuf, HTTP/2, and four calling patterns.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "Protobuf: The IDL",
                       "Define the contract once — generate clients and servers in any language.")
    c.setFont(MONO_FONT, 9.5); c.setFillColor(INK)
    c.drawString(72, y,     "service Greeter {")
    c.drawString(72, y - 22, "  rpc SayHello (HelloReq) returns (HelloReply);")
    c.drawString(72, y - 44, "}")
    c.drawString(72, y - 76, "message HelloReq { string name = 1; }   // binary, typed, versioned")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 112,
        ["Binary serialization: far smaller and faster than JSON — field numbers, not names, on the wire.",
         "Backward compatible: add fields (never reuse numbers); old clients ignore what they don't know.",
         "Codegen: protoc emits typed stubs for 10+ languages — the contract IS the documentation."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "HTTP/2 Under the Hood",
                       "gRPC rides multiplexed HTTP/2 streams — not websockets, not custom TCP.")
    box(c, 72, 430, 468, 50, BOX_BLUE, "one HTTP/2 connection", "many concurrent RPCs as streams")
    box(c, 72, 350, 140, 60, BOX_GREEN, "headers", ":path, grpc-\nstatus…")
    box(c, 236, 350, 140, 60, BOX_ORANGE, "protobuf", "binary\nmessages")
    box(c, 400, 350, 140, 60, BOX_TEAL, "trailers", "final status\ncode")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 310,
        ["Trailers carry the final gRPC status code — the RPC isn't done until trailers arrive.",
         "Multiplexing: hundreds of RPCs share one connection — no head-of-line blocking between calls.",
         "TLS is standard; plaintext (h2c) exists but is rare outside the datacenter."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Four Calling Patterns",
                       "Streaming in either or both directions.")
    pats = [("Unary", "one request → one response. The classic RPC.", BOX_BLUE),
            ("Server streaming", "one request → stream of responses. Live feeds, search results.", BOX_GREEN),
            ("Client streaming", "stream of requests → one response. Uploads, telemetry ingestion.", BOX_ORANGE),
            ("Bidirectional", "both sides stream independently. Chat, real-time collaboration.", BOX_TEAL)]
    yy = y
    for name, desc, fill in pats:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 74
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 200, "Backpressure is built in: HTTP/2 flow control paces fast producers against slow consumers.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "gRPC vs REST",
                       "Contracts and speed vs ubiquity and debuggability.")
    box(c, 72, y - 60, 225, 130, BOX_BLUE, "gRPC wins", "internal services\npolyglot backends\nstreaming needs\nhigh throughput")
    box(c, 315, y - 60, 225, 130, BOX_GREEN, "REST wins", "public APIs\nbrowser clients\nhuman-debuggable\ncaching (HTTP)")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 230,
        ["gRPC payloads are binary — curl can't read them; grpcurl and proxies fill the gap.",
         "Browsers can't speak gRPC natively — grpc-web needs a translating proxy.",
         "Many teams run both: gRPC inside, REST/JSON at the edge."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Production Realities",
                       "What running gRPC at scale teaches you.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y,
        ["Load balancing: one long-lived HTTP/2 connection defeats round-robin LBs — use client-side LB or proxies (Envoy).",
         "Deadlines propagate: set per-RPC timeouts and pass them down the call chain — don't let one slow call hang the mesh.",
         "Interceptors = middleware: auth, logging, retries, and metrics hook in uniformly.",
         "Health checking + reflection: standard probes keep orchestrators happy; reflection aids debugging."],
        font_size=10.5, gap=28)
    note(c, 72, 130, 468, "Retries need idempotency: safe to retry unary reads; think twice before retrying non-idempotent writes.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "gRPC — Remember",
                 ["Protobuf IDL: binary, typed, versioned contracts with generated stubs.",
                  "Transport is HTTP/2: multiplexed streams, trailers carry the status code.",
                  "Four patterns: unary, server-streaming, client-streaming, bidirectional.",
                  "gRPC for internal polyglot services; REST for public APIs and browsers.",
                  "Mind L7 load balancing, deadline propagation, and retry idempotency."],
                 pg)
    c.save(); print("wrote", path)


def pdf_graphql(path):
    c = new_canvas(path); pg = 1
    title_page(c, "GraphQL\nVisual Guide",
               "Ask for exactly what you need —\nschemas, resolvers, and the N+1 trap.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "Schema & Types: The Contract",
                       "A typed graph of everything clients may ask for.")
    c.setFont(MONO_FONT, 9.5); c.setFillColor(INK)
    c.drawString(72, y,     "type User { id: ID!  name: String!  posts: [Post!]! }")
    c.drawString(72, y - 24, "type Post { id: ID!  title: String!  author: User! }")
    c.drawString(72, y - 48, "type Query { user(id: ID!): User }")
    c.drawString(72, y - 72, "type Mutation { createPost(title: String!): Post }")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 108,
        ["The schema is the API: strongly typed, introspectable — clients explore it like documentation.",
         "'!' means non-null; the type system validates every query BEFORE execution.",
         "One endpoint (/graphql); the query itself selects resources — no REST-style URL sprawl."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Queries & Mutations",
                       "Read with queries, write with mutations — shaped exactly as requested.")
    c.setFont(MONO_FONT, 9.5); c.setFillColor(INK)
    c.drawString(72, y,     "query { user(id: 7) { name  posts { title } } }")
    c.drawString(72, y - 26, "→ { \"user\": { \"name\": \"Ada\", \"posts\": [{\"title\": \"…\"}] } }")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 62,
        ["No over-fetching: the response mirrors the query's field selection — mobile clients love this.",
         "No under-fetching: nested data in ONE round trip — the REST 'fetch user, then fetch posts' dance disappears.",
         "Mutations run serially (in order); queries run in parallel — the spec guarantees it."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Resolvers: Field-Level Functions",
                       "Every field is resolved by a function — the query walks the graph.")
    box(c, 72, 430, 140, 70, BOX_BLUE, "Query.user", "fetch user 7")
    box(c, 236, 430, 140, 70, BOX_GREEN, "User.posts", "fetch posts\nfor user 7")
    box(c, 400, 430, 140, 70, BOX_ORANGE, "Post.title", "already in\nrow")
    arrow(c, 212, 465, 234, 465, color=ACCENT, width=2)
    arrow(c, 376, 465, 398, 465, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["Resolvers compose: parent results feed child resolvers — each level only fetches what was asked.",
         "Default resolvers just read properties; custom ones hit databases, services, caches.",
         "This elegance hides a performance trap — next page."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "The N+1 Problem & DataLoader",
                       "Naive resolvers query per row — batching fixes it.")
    box(c, 72, 440, 468, 60, BOX_RED, "N+1: 1 query for users + N queries for each user's posts", "100 users → 101 round trips")
    arrow(c, 306, 438, 306, 408, color=ACCENT, width=2.5, label="fix")
    box(c, 72, 340, 468, 60, BOX_GREEN, "DataLoader: batch + cache per request", "100 users → 2 round trips (WHERE user_id IN …)")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 300,
        ["DataLoader collects keys during a tick, fires ONE batched query, and maps results back.",
         "Per-request cache: the same entity fetched twice in one query hits the cache, not the DB.",
         "Also cap query depth/complexity — malicious clients can craft exponentially expensive queries."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "GraphQL vs REST",
                       "Flexibility for clients vs simplicity for servers.")
    box(c, 72, y - 60, 225, 130, BOX_BLUE, "GraphQL wins", "diverse clients\nrapid UI iteration\nnested data\ntyped contracts")
    box(c, 315, y - 60, 225, 130, BOX_GREEN, "REST wins", "HTTP caching\nsimple mental model\nfile uploads\nrate-limit clarity")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 230,
        ["Caching is harder: one endpoint + POST means HTTP caches don't help — plan persisted queries or app-level caching.",
         "Versioning: evolve the schema (deprecate fields) instead of /v1, /v2 — but removals still break clients.",
         "Many teams expose GraphQL as a gateway over REST/gRPC microservices."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "GraphQL — Remember",
                 ["Schema = typed contract; introspection makes it self-documenting.",
                  "Queries shape the response exactly — no over/under-fetching, one round trip.",
                  "Resolvers compose field-by-field; watch for the N+1 trap.",
                  "DataLoader batches and caches per request — 101 queries become 2.",
                  "GraphQL for flexible clients; REST when HTTP caching and simplicity win."],
                 pg)
    c.save(); print("wrote", path)


def pdf_rest(path):
    c = new_canvas(path); pg = 1
    title_page(c, "REST API Design\nVisual Guide",
               "Resources, verbs, and status codes —\nAPIs that feel inevitable.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 6, "Resources & URIs",
                       "Nouns, not verbs — the URL names the THING.")
    c.setFont(MONO_FONT, 10); c.setFillColor(INK)
    c.drawString(72, y,     "GET  /orders/42            ← a resource")
    c.drawString(72, y - 26, "GET  /orders/42/items      ← a sub-resource")
    c.drawString(72, y - 52, "GET  /getOrder?id=42       ← RPC smell: avoid")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 88,
        ["Plural nouns, kebab-case: /users, /order-items — consistent everywhere.",
         "Hierarchy for ownership: /users/7/orders — but don't nest deeper than 2 levels.",
         "Filtering/sorting via query params: /orders?status=paid&sort=-created."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "HTTP Verbs: Meaningful Methods",
                       "The verb says what; the URL says what to.")
    verbs = [("GET", "read — safe, idempotent, cacheable", BOX_GREEN),
             ("POST", "create (or action) — neither safe nor idempotent", BOX_BLUE),
             ("PUT", "replace whole resource — idempotent", BOX_ORANGE),
             ("PATCH", "partial update — idempotent if designed so", BOX_TEAL),
             ("DELETE", "remove — idempotent (deleting twice = deleted)", BOX_RED)]
    yy = y
    for name, desc, fill in verbs:
        box(c, 72, yy - 46, 110, 50, fill, name, "", font_size=12)
        c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
        c.drawString(200, yy - 20, desc)
        yy -= 60
    note(c, 72, 120, 468, "Idempotency keys on POST: clients retry safely — the server dedupes by key. Essential for payments.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Status Codes: Speak HTTP",
                       "The code is the first thing clients read — choose precisely.")
    codes = [("2xx — success", "200 OK, 201 Created (+ Location), 204 No Content", BOX_GREEN),
             ("4xx — client error", "400 bad input, 401 unauthenticated, 403 forbidden, 404 not found, 409 conflict, 429 slow down", BOX_ORANGE),
             ("5xx — server error", "500 bug, 502 bad gateway, 503 overloaded (+ Retry-After)", BOX_RED)]
    yy = y
    for name, desc, fill in codes:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 74
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 220, "Never 200-with-error-body: intermediaries, monitors, and client libraries all key off the status code.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Pagination: Never Dump the Table",
                       "Unbounded lists are a DoS you wrote yourself.")
    box(c, 72, 430, 225, 70, BOX_BLUE, "offset/limit", "?page=3&size=50\nsimple, drifts on\nwrites")
    box(c, 315, 430, 225, 70, BOX_GREEN, "cursor", "?after=abc123\nstable, preferred\nfor feeds")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["Always paginate list endpoints — default page size, max cap (e.g. 100).",
         "Cursor pagination survives inserts/deletes; offset skips or duplicates rows on live data.",
         "Return metadata: total count (when cheap), next cursor, and Link headers for discoverability."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Versioning Strategies",
                       "APIs are promises — evolve without breaking them.")
    vers = [("URL versioning", "/v1/orders — explicit, obvious, most common", BOX_BLUE),
            ("Header versioning", "Accept: application/vnd.api.v2+json — clean URLs, harder to debug", BOX_GREEN),
            ("Evolve, don't version", "additive changes only; deprecate with Sunset headers", BOX_TEAL)]
    yy = y
    for name, desc, fill in vers:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 74
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 220, "Rule: never remove or retype a field in a shipped version — additive only, deprecate loudly.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "HATEOAS: Hypermedia Controls",
                       "Responses that teach clients what to do next.")
    c.setFont(MONO_FONT, 9.5); c.setFillColor(INK)
    c.drawString(72, y,     '{ "id": 42, "status": "paid",')
    c.drawString(72, y - 22, '  "_links": { "self": "/orders/42",')
    c.drawString(72, y - 44, '              "refund": "/orders/42/refund" } }')
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 80,
        ["Links encode valid state transitions — clients discover actions instead of hardcoding URLs.",
         "Full HATEOAS is rare in practice; link relations on key resources capture most of the value.",
         "Pairs well with versioning-by-evolution: clients follow links, not versioned URL templates."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "REST API Design — Remember",
                 ["Resources are nouns in the URL; verbs carry the action (GET/POST/PUT/PATCH/DELETE).",
                  "Status codes are the contract — never 200-with-error-body.",
                  "Paginate everything; prefer cursor pagination for live data.",
                  "Version explicitly or evolve additively — never break a shipped field.",
                  "HATEOAS links let clients discover next actions instead of hardcoding URLs."],
                 pg)
    c.save(); print("wrote", path)


def pdf_anycast(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Anycast\nVisual Guide",
               "One IP, many places —\nhow the internet finds the nearest you.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "One IP Announced Everywhere",
                       "The same prefix advertised from dozens of locations at once.")
    box(c, 196, 430, 220, 70, BOX_BLUE, "203.0.113.53", "announced from\nEVERY site")
    sites = [("New York", 72, 300), ("London", 236, 300), ("Tokyo", 400, 300)]
    for name, bx, by in sites:
        box(c, bx, by, 140, 60, BOX_GREEN, name, "same IP here")
        arrow(c, bx + 70, by + 60, 306, 428, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 260, "BGP sees multiple equal origins for one prefix — and picks the nearest per viewer.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "BGP Nearest-Wins",
                       "Each network's routers choose the closest announcement.")
    box(c, 72, 430, 140, 70, BOX_BLUE, "You (US)", "")
    box(c, 236, 430, 140, 70, BOX_GREEN, "NY site", "2 AS hops")
    box(c, 400, 430, 140, 70, BOX_ORANGE, "Tokyo site", "6 AS hops")
    arrow(c, 212, 465, 234, 465, color=GREEN, width=2.5, label="chosen")
    arrow(c, 400, 430, 300, 430, color=RED, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["'Nearest' = fewest AS hops by BGP policy — usually, but not always, geographic.",
         "No client configuration: the routing system makes the decision transparently.",
         "Return path may differ (asymmetric routing) — design stateless services accordingly."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "DNS Roots & CDNs Run on Anycast",
                       "The internet's most critical services share this trick.")
    uses = [("DNS root servers", "13 logical IPs, 1000+ physical instances — a root is always nearby.", BOX_BLUE),
            ("Authoritative DNS", "Cloudflare, Route53, NS1 — anycasted DNS survives regional outages.", BOX_GREEN),
            ("CDNs", "One IP per edge PoP cluster — users land on the closest cache.", BOX_ORANGE),
            ("DDoS absorption", "Attack traffic splits across sites instead of drowning one.", BOX_RED)]
    yy = y
    for name, desc, fill in uses:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 74
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Unicast vs Anycast vs Multicast",
                       "Three ways to address 'them'.")
    casts = [("Unicast", "one → one. A specific host. The default.", BOX_BLUE),
             ("Anycast", "one → nearest-of-many. Same IP, many sites.", BOX_GREEN),
             ("Multicast", "one → many-subscribers. IPTV, OSPF hellos (224.0.0.0/4).", BOX_ORANGE),
             ("Broadcast", "one → everyone on the LAN. Dies at the router.", BOX_RED)]
    yy = y
    for name, desc, fill in casts:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11.5)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Anycast Gotchas",
                       "Nearest isn't always stable — plan for flapping.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y,
        ["Route flaps can move a client mid-session to a different site — keep services stateless or share session state.",
         "TCP + anycast: generally fine while routes are stable; pathological flapping breaks long connections.",
         "Debugging is harder: 'which site answered?' needs per-site identifiers in responses.",
         "Not for stateful backends: anycast the stateless edge, unicast the databases behind it."],
        font_size=10.5, gap=28)
    note(c, 72, 130, 468, "Anycast + health checks: withdraw the announcement from a sick site and traffic drains away — failover without DNS TTL waits.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Anycast — Remember",
                 ["Anycast = one IP announced from many sites; BGP routes each client to the nearest.",
                  "Zero client config — the routing system decides transparently.",
                  "Powers DNS roots, authoritative DNS, CDNs, and DDoS absorption.",
                  "Unicast = one host; anycast = nearest of many; multicast = subscribers; broadcast = LAN-only.",
                  "Keep anycasted services stateless; withdraw sick sites via BGP for instant failover."],
                 pg)
    c.save(); print("wrote", path)


def pdf_ipv4_ipv6(path):
    c = new_canvas(path); pg = 1
    title_page(c, "IPv4 vs IPv6\nVisual Guide",
               "Running out, then starting over —\naddress math, headers, and transition.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "Address Space Math",
                       "The reason IPv6 exists, in one comparison.")
    box(c, 72, y - 60, 225, 120, BOX_RED, "IPv4: 2^32", "4.3 billion\naddresses\n~1 per person\nEXHAUSTED")
    box(c, 315, y - 60, 225, 120, BOX_GREEN, "IPv6: 2^128", "340 undecillion\n~5×10^28 per person\neffectively infinite")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 220,
        ["IPv4's 32 bits seemed vast in 1981 — NAT and address markets are the expensive workaround.",
         "IPv6 restores the end-to-end model: every device CAN have a globally unique address again.",
         "Writing IPv6: 2001:db8::1 — '::' compresses one run of zero groups. /64 per LAN is the norm."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Header Simplification",
                       "IPv6 didn't just widen addresses — it cleaned house.")
    box(c, 72, 440, 225, 90, BOX_RED, "IPv4 header", "20+ bytes\n12+ fields\nchecksum,\nfragmentation")
    box(c, 315, 440, 225, 90, BOX_GREEN, "IPv6 header", "40 bytes fixed\n8 fields\nno checksum,\nno hop frag")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 400,
        ["Dropped: header checksum (links already check), in-path fragmentation (sender handles via PMTU).",
         "Fixed 40-byte header: routers parse faster — no variable-length options in the fast path.",
         "Extension headers chain optional features (routing, IPsec) without complicating the base header."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Dual-Stack: Running Both",
                       "The pragmatic transition — every host speaks two protocols.")
    box(c, 72, 430, 200, 70, BOX_BLUE, "IPv4 stack", "legacy net\nNAT as needed")
    box(c, 340, 430, 200, 70, BOX_GREEN, "IPv6 stack", "native addrs\nno NAT")
    arrow(c, 272, 465, 338, 465, color=ACCENT, width=2, label="same host")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["DNS returns both A and AAAA records; Happy Eyeballs races them and picks the working winner.",
         "Dual-stack doubles firewall rules, monitoring, and troubleshooting surface — budget the ops cost.",
         "Most cloud and mobile networks are dual-stack today; IPv6-only is growing (with NAT64 for legacy)."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Transition Mechanisms",
                       "Bridges for the long migration.")
    mechs = [("NAT64 + DNS64", "IPv6-only clients reach IPv4 servers: DNS synthesizes AAAA, NAT64 translates. T-Mobile US runs this.", BOX_BLUE),
             ("6to4 / Teredo", "Tunneling IPv6 over IPv4 — legacy transition hacks, largely retired.", BOX_ORANGE),
             ("464XLAT", "Double translation for IPv6-only mobile networks with IPv4 apps.", BOX_TEAL)]
    yy = y
    for name, desc, fill in mechs:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=11)
        yy -= 78
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 220, "There is no flag day: IPv4 and IPv6 will coexist for decades — design for both.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "IPv6 Addressing in Practice",
                       "What you'll actually configure.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y,
        ["SLAAC: hosts self-configure from router advertisements — no DHCP needed for addresses (DHCPv6 still gives DNS).",
         "Link-local (fe80::/10): every interface has one — neighbor discovery (ARP's replacement) uses it.",
         "Privacy extensions: hosts rotate temporary addresses so the interface ID doesn't track them.",
         "ULA (fc00::/7): the IPv6 'private' range — for internal use, not globally routed."],
        font_size=10.5, gap=28)
    note(c, 72, 130, 468, "Firewall IPv6 explicitly: 'no NAT = no protection' is a myth, but an unfiltered v6 path is a real hole. Filter both stacks.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "IPv4 vs IPv6 — Remember",
                 ["IPv4: 4.3B addresses, exhausted — NAT is the workaround. IPv6: 2^128, effectively infinite.",
                  "IPv6 headers are fixed 40 bytes, 8 fields — no checksum, no in-path fragmentation.",
                  "Dual-stack runs both; Happy Eyeballs picks the working protocol per connection.",
                  "NAT64/DNS64 bridges IPv6-only clients to the IPv4 internet.",
                  "SLAAC autoconfigures addresses; firewall the v6 path as carefully as v4."],
                 pg)
    c.save(); print("wrote", path)


def pdf_arp_icmp(path):
    c = new_canvas(path); pg = 1
    title_page(c, "ARP & ICMP\nVisual Guide",
               "Finding neighbors, testing paths —\nthe helper protocols of IP.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "ARP: Who Has This IP?",
                       "IP needs a MAC to send a frame — ARP asks the LAN.")
    box(c, 72, 430, 160, 70, BOX_BLUE, "Host A", "knows IP\nneeds MAC")
    box(c, 380, 430, 160, 70, BOX_GREEN, "Host B", "192.168.1.20")
    arrow(c, 232, 480, 378, 480, color=ORANGE, width=2, label="broadcast: 'who has .20?'")
    arrow(c, 378, 440, 232, 440, color=GREEN, width=2, label="unicast: 'I do — MAC aa:bb…'")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["ARP request is broadcast — every host on the LAN hears it; only the owner replies.",
         "Results are cached in the ARP table (minutes) — repeat traffic needs no new broadcast.",
         "Proxy ARP: a router answers for distant hosts — useful, and a classic misconfiguration smell."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Gratuitous ARP",
                       "Announcing yourself without being asked.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y,
        ["A host broadcasts 'I am 192.168.1.20 at aa:bb:cc' unprompted — updates everyone's cache.",
         "Legit uses: failover (new active node claims the virtual IP), duplicate-address detection on boot.",
         "Dark side: ARP spoofing uses the same mechanism maliciously — switches fight back with Dynamic ARP Inspection.",
         "No authentication in ARP at all — on untrusted LANs, that's the vulnerability."],
        font_size=10.5, gap=28)
    note(c, 72, 180, 468, "ARP is IPv4-only. IPv6 replaced it with Neighbor Discovery (NDP) over ICMPv6 — same job, better design.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "ICMP: The Network's Messenger",
                       "Control messages about the network itself — not user data.")
    box(c, 72, 430, 225, 70, BOX_GREEN, "Echo request", "type 8\n'are you there?'")
    box(c, 315, 430, 225, 70, BOX_BLUE, "Echo reply", "type 0\n'yes, in 12ms'")
    arrow(c, 297, 465, 313, 465, color=ACCENT, width=2, label="ping")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["Ping measures reachability + RTT — the first diagnostic for 'is it up?'.",
         "ICMP also carries: Destination Unreachable, Time Exceeded, Redirect, and PMTU 'packet too big'.",
         "Don't block all ICMP: killing 'packet too big' breaks Path MTU Discovery and causes mystery stalls."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Traceroute: TTL Tricks",
                       "Map the path by expiring packets on purpose.")
    box(c, 72, 440, 468, 60, BOX_BLUE, "TTL=1 → router 1 replies 'Time Exceeded' — hop 1 revealed", "")
    box(c, 72, 360, 468, 60, BOX_GREEN, "TTL=2 → dies at router 2 — hop 2 revealed", "")
    box(c, 72, 280, 468, 60, BOX_ORANGE, "TTL=3 → dies at router 3 … until the destination answers", "")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 240,
        ["Every router decrements TTL; at zero it sends ICMP Time Exceeded back — that reply IS the hop.",
         "Three probes per TTL: RTT variance per hop hints at congestion or asymmetric paths.",
         "Stars (* * *) = filtered ICMP or rate-limited routers — common, not necessarily failure."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Reading the Diagnostics",
                       "What ping and traceroute actually tell you.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y,
        ["Ping loss with clean traceroute: endpoint or last-mile issue — not the path.",
         "Latency jump at one hop that persists downstream: that link is the bottleneck.",
         "Latency jump that VANISHES downstream: the router was slow to answer ICMP, not to forward — ignore it.",
         "Asymmetric paths mean forward and reverse can differ — diagnose both directions."],
        font_size=10.5, gap=28)
    note(c, 72, 130, 468, "mtr blends both tools: continuous ping per hop — the fastest way to localize packet loss on a path.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "ARP & ICMP — Remember",
                 ["ARP maps IP→MAC via broadcast request + cached replies; IPv6 uses NDP instead.",
                  "Gratuitous ARP announces ownership — legit for failover, abused for spoofing.",
                  "ICMP carries echo (ping), unreachable, time-exceeded, and MTU signals.",
                  "Traceroute reveals hops by expiring TTLs on purpose; stars mean filtered ICMP.",
                  "A latency spike that disappears downstream is slow ICMP, not a slow path."],
                 pg)
    c.save(); print("wrote", path)


def pdf_vlans(path):
    c = new_canvas(path); pg = 1
    title_page(c, "VLANs\nVisual Guide",
               "Virtual LANs —\ncarving one switch into many networks.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "Broadcast Domain Segmentation",
                       "One physical switch, several logical networks that can't hear each other.")
    box(c, 72, 380, 225, 90, BOX_BLUE, "VLAN 10 — Eng", "ports 1-8\nbroadcasts stay\nhere")
    box(c, 315, 380, 225, 90, BOX_GREEN, "VLAN 20 — Sales", "ports 9-16\nisolated from\nVLAN 10")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 340,
        ["A broadcast in VLAN 10 never reaches VLAN 20 — same isolation as separate switches, zero extra hardware.",
         "Security + sanity: HR, guests, IoT, and servers each get their own broadcast domain.",
         "VLANs are L2: devices in different VLANs need a ROUTER (L3) to talk — by design."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "802.1Q Tagging",
                       "A 4-byte tag in the Ethernet header says which VLAN a frame belongs to.")
    c.setFont(MONO_FONT, 9.5); c.setFillColor(INK)
    c.drawString(72, y,     "[ dst MAC | src MAC | 802.1Q TAG | EtherType | payload | CRC ]")
    c.drawString(72, y - 26, "                              └─ TPID 0x8100 + VLAN ID (12 bits: 1–4094)")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 62,
        ["The tag is inserted between source MAC and EtherType — 12-bit VLAN ID = 4094 usable VLANs.",
         "Tags are added/removed at trunk ports; end hosts never see them (usually).",
         "Double-tagging (Q-in-Q) stacks tags for service providers carrying customer VLANs."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Access vs Trunk Ports",
                       "Edge ports speak untagged; uplinks carry everything tagged.")
    box(c, 72, 420, 225, 90, BOX_GREEN, "Access port", "ONE vlan\nuntagged\nend hosts:\nPCs, printers")
    box(c, 315, 420, 225, 90, BOX_BLUE, "Trunk port", "MANY vlans\ntagged\nswitch↔switch\nswitch↔router")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 380,
        ["Access: the switch assigns the VLAN — the device doesn't know or care.",
         "Trunk: frames carry tags so the far switch sorts them into the right VLANs.",
         "Native VLAN: the one untagged VLAN allowed on a trunk — keep it unused and prune it."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Inter-VLAN Routing",
                       "VLANs isolate — routers (or L3 switches) reconnect selectively.")
    box(c, 72, 430, 140, 70, BOX_BLUE, "VLAN 10", "")
    box(c, 400, 430, 140, 70, BOX_GREEN, "VLAN 20", "")
    box(c, 236, 320, 140, 70, BOX_ORANGE, "Router /\nL3 switch", "sub-interfaces\nor SVIs")
    arrow(c, 212, 445, 250, 390, color=ACCENT, width=1.8)
    arrow(c, 400, 445, 360, 390, color=ACCENT, width=1.8)
    arrow(c, 250, 350, 200, 430, color=ACCENT, width=1.8)
    arrow(c, 360, 350, 410, 430, color=ACCENT, width=1.8)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 280, "Router-on-a-stick: one trunk to the router, sub-interfaces per VLAN. Modern: L3 switch with SVIs — routing at wire speed.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "VLAN Hopping & Hardening",
                       "Tags are trusted — misconfigurations are the attack.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y,
        ["Double-tagging attack: crafted frames hop to another VLAN — defeated by proper native-VLAN hygiene.",
         "Never leave ports in trunk-auto: explicitly set access vs trunk; disable unused ports.",
         "Prune trunks: carry only the VLANs each link actually needs.",
         "Voice VLANs: phones tag voice traffic separately — QoS for calls without a second cable."],
        font_size=10.5, gap=28)
    note(c, 72, 130, 468, "VLANs segment, they don't encrypt: traffic between VLANs is still plaintext on the wire without additional protection.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "VLANs — Remember",
                 ["VLANs split one switch into isolated broadcast domains — security without extra hardware.",
                  "802.1Q inserts a 4-byte tag (VLAN ID 1–4094) into the Ethernet header.",
                  "Access ports = one untagged VLAN (hosts); trunk ports = many tagged VLANs (uplinks).",
                  "Inter-VLAN traffic must route — router-on-a-stick or L3 switch SVIs.",
                  "Harden: explicit port modes, prune trunks, keep the native VLAN unused."],
                 pg)
    c.save(); print("wrote", path)


def pdf_sdn(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Software-Defined\nNetworking",
               "Control plane, meet software —\nnetworks programmed like code.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "Control Plane vs Data Plane",
                       "Deciding where packets go vs actually moving them — SDN splits the two.")
    box(c, 72, y - 60, 225, 120, BOX_BLUE, "Control plane", "DECIDES:\nrouting, policy\n'send web traffic\nvia link B'")
    box(c, 315, y - 60, 225, 120, BOX_GREEN, "Data plane", "FORWARDS:\nmatches tables,\nforwards at\nline rate")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 220,
        ["Traditional routers bundle both: every box runs OSPF/BGP and forwards — distributed, autonomous, hard to coordinate.",
         "SDN centralizes DECISIONS in a controller; switches become fast, dumb forwarding engines.",
         "Result: network-wide policy from one program instead of box-by-box CLI."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "The SDN Architecture",
                       "Three layers, two APIs.")
    box(c, 156, 440, 300, 70, BOX_BLUE, "Applications", "firewall app, load-balancer app, monitor…")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9)
    c.drawCentredString(306, 420, "northbound API (REST)")
    box(c, 156, 340, 300, 70, BOX_GREEN, "Controller", "global view\ncomputes flows")
    c.drawCentredString(306, 320, "southbound API (OpenFlow)")
    box(c, 72, 240, 140, 70, BOX_ORANGE, "Switch A", "flow tables")
    box(c, 236, 240, 140, 70, BOX_ORANGE, "Switch B", "flow tables")
    box(c, 400, 240, 140, 70, BOX_ORANGE, "Switch C", "flow tables")
    arrow(c, 306, 438, 306, 412, color=ACCENT, width=1.5)
    arrow(c, 306, 338, 306, 312, color=ACCENT, width=1.5)
    arrow(c, 306, 238, 142, 238, color=ACCENT, width=1.5)
    arrow(c, 306, 238, 306, 238, color=ACCENT, width=1.5)
    arrow(c, 306, 238, 470, 238, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 200, "Apps express intent northbound; the controller programs flow tables southbound.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "OpenFlow: Programming the Switch",
                       "Flow tables are match → action rules installed by the controller.")
    c.setFont(MONO_FONT, 9.5); c.setFillColor(INK)
    c.drawString(72, y,     "match: { in_port: 1, eth_type: IPv4, tcp_dst: 80 }")
    c.drawString(72, y - 24, "action: forward → port 3        // a 'flow'")
    c.drawString(72, y - 48, "match: { in_port: 1, * }")
    c.drawString(72, y - 72, "action: send → controller       // unknown: ask the brain")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 108,
        ["First packet of a new flow goes to the controller ('packet-in'); the rule it installs handles the rest.",
         "Flows have timeouts and counters — the controller sees traffic stats per rule.",
         "Reactive (learn as traffic arrives) vs proactive (pre-install known policies)."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Traditional vs SDN",
                       "Same packets, different brains.")
    box(c, 72, y - 60, 225, 120, BOX_PURP, "Traditional", "distributed\ncontrol per box\nCLI per device\nslow global\nchanges")
    box(c, 315, y - 60, 225, 120, BOX_BLUE, "SDN", "centralized\ncontroller view\nprogrammatic\ninstant global\npolicy")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 220,
        ["SDN strength: consistent policy, automation, global optimization (traffic engineering).",
         "SDN risk: the controller is a single point of failure AND attack — cluster it, secure it.",
         "Reality check: most 'SDN' in production is overlay-based (VXLAN) or intent APIs, not pure OpenFlow."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Where SDN Actually Won",
                       "The ideas succeeded even where OpenFlow didn't.")
    uses = [("Datacenter fabrics", "Clos topologies with centralized routing — every hyperscaler runs this.", BOX_BLUE),
            ("SD-WAN", "Policy-based path selection across internet/MPLS — branch offices without telco lock-in.", BOX_GREEN),
            ("Cloud overlays", "VPCs are SDN: virtual networks programmed over shared physical fabric (VXLAN).", BOX_ORANGE),
            ("5G / telco", "Network slicing and programmable forwarding in carrier cores.", BOX_TEAL)]
    yy = y
    for name, desc, fill in uses:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 74
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SDN — Remember",
                 ["SDN separates the control plane (decisions) from the data plane (forwarding).",
                  "Controller has the global view; switches hold flow tables programmed via OpenFlow.",
                  "Apps express intent northbound; flows are match→action rules with counters.",
                  "Wins: consistent policy, automation, global optimization — at the cost of controller risk.",
                  "SDN's real victories: datacenter fabrics, SD-WAN, and cloud VPC overlays."],
                 pg)
    c.save(); print("wrote", path)


def pdf_quic(path):
    c = new_canvas(path); pg = 1
    title_page(c, "QUIC\nVisual Guide",
               "The UDP transport that grew up —\nfast handshakes, migration, and HTTP/3.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "A Transport Over UDP",
                       "Reliability rebuilt in user space — deployable without kernel updates.")
    box(c, 72, 430, 140, 80, BOX_BLUE, "TCP", "kernel\nslow to\nevolve")
    box(c, 236, 430, 140, 80, BOX_GREEN, "QUIC", "user space\nover UDP\nships with\nthe app")
    box(c, 400, 430, 140, 80, BOX_ORANGE, "TLS 1.3", "baked IN\nnot layered\non")
    arrow(c, 212, 470, 234, 470, color=ACCENT, width=2, label="replaces")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["TCP changes need OS upgrades across the world; QUIC ships inside Chrome/servers — iteration in weeks.",
         "Encryption is mandatory and integrated: almost the entire packet (incl. handshake) is encrypted.",
         "Middleboxes see only UDP — they can't ossify or mangle what they can't parse."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "0-RTT Resumption",
                       "Come back to a server you've seen — send data with the FIRST packet.")
    box(c, 72, 430, 468, 60, BOX_BLUE, "First visit: 1-RTT handshake", "crypto + transport negotiated together — TCP+TLS needed 3+")
    box(c, 72, 350, 468, 60, BOX_GREEN, "Return visit: 0-RTT", "cached keys → application data in the very first UDP datagram")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 310,
        ["TCP+TLS 1.3 needs ~2-3 RTTs before data; QUIC does it in 1, then 0 on repeat visits.",
         "Replay caution: 0-RTT data can be replayed by attackers — servers must gate non-idempotent requests.",
         "Matters most on high-latency links: each saved RTT is hundreds of milliseconds on mobile."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Connection Migration",
                       "Your connection has an ID — not an IP:port pair.")
    box(c, 72, 430, 200, 70, BOX_BLUE, "Wi-Fi\n192.0.2.10", "streaming…")
    box(c, 340, 430, 200, 70, BOX_GREEN, "Cellular\n198.51.100.7", "…still streaming")
    arrow(c, 272, 465, 338, 465, color=ACCENT, width=2.5, label="same conn ID")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["TCP dies when your IP changes (Wi-Fi → cellular) — the 4-tuple IS the connection.",
         "QUIC's connection ID survives IP/port changes — the session migrates seamlessly.",
         "NAT rebinding? Same story: the ID persists while the mapping shifts underneath."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Streams Without Head-of-Line Blocking",
                       "Independent streams over one connection — loss affects only its stream.")
    box(c, 72, 430, 468, 50, BOX_BLUE, "one QUIC connection", "streams multiplexed, independently flow-controlled")
    for i, (nm, fill) in enumerate([("stream A", BOX_GREEN), ("stream B ✕ lost pkt", BOX_RED), ("stream C", BOX_TEAL)]):
        box(c, 72 + i * 160, 350, 148, 60, fill, nm, "others unaffected" if i != 1 else "only B stalls")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 310, "HTTP/2 over TCP: one lost packet froze EVERY stream. QUIC: only the unlucky stream waits.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "QUIC Is HTTP/3's Foundation",
                       "The protocol stack, bottom to top.")
    layers = [("UDP", "datagrams across the internet", BOX_PURP),
              ("QUIC", "reliability, crypto, streams, migration", BOX_GREEN),
              ("HTTP/3", "semantics on QUIC streams (QPACK headers)", BOX_ORANGE)]
    yy = y
    for name, desc, fill in layers:
        box(c, 116, yy - 50, 380, 56, fill, name, desc, font_size=11.5)
        yy -= 68
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 220, "QUIC is transport-agnostic in theory — in practice it's the engine under HTTP/3, DNS-over-QUIC, and more.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "QUIC — Remember",
                 ["QUIC = TCP-like reliability + TLS 1.3, in user space over UDP.",
                  "0-RTT resumption: repeat visits send data in the first packet (mind replay).",
                  "Connection IDs survive IP changes — Wi-Fi→cellular migration without drops.",
                  "Per-stream loss independence kills TCP's head-of-line blocking.",
                  "QUIC is the transport foundation HTTP/3 is built on."],
                 pg)
    c.save(); print("wrote", path)


def pdf_dns_security(path):
    c = new_canvas(path); pg = 1
    title_page(c, "DNS Security\nVisual Guide",
               "Trusting names —\npoisoning, DNSSEC, and encrypted DNS.",
               "Networking", None); pg += 1

    y = section_header(c, 1, 5, "Cache Poisoning: The Attack",
                       "Race the real answer — whoever replies first wins the cache.")
    box(c, 72, 430, 160, 70, BOX_BLUE, "Resolver", "asked for\nbank.com")
    box(c, 380, 430, 160, 70, BOX_GREEN, "Real server", "slow truth")
    box(c, 226, 300, 160, 70, BOX_RED, "Attacker", "fast lie:\n'bank.com =\nevil IP'")
    arrow(c, 232, 445, 300, 372, color=RED, width=2, label="forged reply")
    arrow(c, 380, 445, 300, 372, color=GREEN, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 260,
        ["Classic DNS runs over UDP with a 16-bit query ID — guessable, spoofable, first-reply-wins.",
         "Poisoned cache redirects EVERY client of that resolver until the TTL expires.",
         "Kaminsky (2008) made it devastating: poison the NS records, own the whole domain. Source-port randomization was the emergency fix."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "DNSSEC: Chain of Trust",
                       "Cryptographic signatures from the root down — tampering is detectable.")
    box(c, 196, 440, 220, 60, BOX_BLUE, "Root (.)", "signed — trust anchor")
    box(c, 72, 340, 160, 60, BOX_GREEN, ".com", "DS record\nvouches for child")
    box(c, 380, 340, 160, 60, BOX_GREEN, "example.com", "DNSKEY signs\nits records")
    arrow(c, 306, 438, 152, 402, color=ACCENT, width=1.5)
    arrow(c, 306, 438, 460, 402, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 300,
        ["Each zone signs its records (RRSIG); the parent publishes a DS hash of the child's key — a chain to the root.",
         "Validators reject forged answers — poisoning becomes cryptographically infeasible.",
         "Limits: DNSSEC signs but doesn't ENCRYPT (queries still visible); deployment is still partial."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "DoT & DoH: Encrypted DNS",
                       "Hide queries from snoopers on the path.")
    box(c, 72, 430, 225, 90, BOX_BLUE, "DoT (port 853)", "DNS over TLS\ndedicated port\neasy to identify\n& block")
    box(c, 315, 430, 225, 90, BOX_GREEN, "DoH (port 443)", "DNS over HTTPS\nblends with web\ntraffic\nhard to block")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 390,
        ["Both encrypt queries between stub resolver and recursive resolver — ISPs and Wi-Fi snoopers go blind.",
         "Trust shifts: your DoH provider (Cloudflare, Google, Quad9) now sees all your queries — choose deliberately.",
         "Enterprise tension: encrypted DNS bypasses local filtering/monitoring — split-horizon and policy configs answer it."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Response Validation Checklist",
                       "What a careful resolver verifies.")
    checks = [("Bailiwick check", "is this server AUTHORITATIVE for the answer? Out-of-bailiwick data gets dropped.", BOX_BLUE),
              ("DNSSEC validation", "signature chain verifies against the trust anchor?", BOX_GREEN),
              ("0x20 randomization", "mixed-case query echoed exactly — cheap spoofing tripwire.", BOX_ORANGE),
              ("Response sanity", "reply matches query ID, port, and question section.", BOX_TEAL)]
    yy = y
    for name, desc, fill in checks:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 74
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 5, "Defense in Depth for DNS",
                       "No single fix — layer them.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y,
        ["Run a validating resolver (Unbound, BIND) with DNSSEC on — validate everything you can.",
         "Use DoT/DoH to a provider you trust; keep a fallback for captive portals.",
         "Short TTLs on critical records limit poisoning blast radius (at a caching cost).",
         "Monitor: unexpected record changes and DNS tunneling patterns in query logs.",
         "Register defensively: lock transfers (AXFR), DNSSEC-sign your own zones, monitor CT logs for lookalike domains."],
        font_size=10.5, gap=28)
    note(c, 72, 120, 468, "DNS is plaintext metadata about everything you do online — treat its privacy and integrity as first-class requirements.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "DNS Security — Remember",
                 ["Cache poisoning races forged UDP replies into resolvers — first reply wins.",
                  "DNSSEC builds a signature chain from the root: tampering becomes detectable.",
                  "DoT (port 853) and DoH (port 443) encrypt queries — trust shifts to your provider.",
                  "Resolvers validate: bailiwick, DNSSEC, 0x20 case, query/port matching.",
                  "Layer defenses: validating resolver + encrypted transport + signed zones + monitoring."],
                 pg)
    c.save(); print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    builders = [
        (pdf_osi, "bbg-osi-model.pdf"),
        (pdf_tcp_teardown, "bbg-tcp-teardown.pdf"),
        (pdf_udp, "bbg-udp.pdf"),
        (pdf_dhcp, "bbg-dhcp.pdf"),
        (pdf_nat, "bbg-nat.pdf"),
        (pdf_subnets, "bbg-subnets-cidr.pdf"),
        (pdf_routing, "bbg-routing-protocols.pdf"),
        (pdf_http2_http3, "bbg-http2-http3.pdf"),
        (pdf_vpns, "bbg-vpns.pdf"),
        (pdf_firewalls, "bbg-firewalls.pdf"),
        (pdf_proxies, "bbg-proxies.pdf"),
        (pdf_websockets, "bbg-websockets.pdf"),
        (pdf_grpc, "bbg-grpc.pdf"),
        (pdf_graphql, "bbg-graphql.pdf"),
        (pdf_rest, "bbg-rest-design.pdf"),
        (pdf_anycast, "bbg-anycast.pdf"),
        (pdf_ipv4_ipv6, "bbg-ipv4-ipv6.pdf"),
        (pdf_arp_icmp, "bbg-arp-icmp.pdf"),
        (pdf_vlans, "bbg-vlans.pdf"),
        (pdf_sdn, "bbg-sdn.pdf"),
        (pdf_quic, "bbg-quic.pdf"),
        (pdf_dns_security, "bbg-dns-security.pdf"),
    ]
    for fn, name in builders:
        fn(os.path.join(out, name))
    print(f"done: {len(builders)} PDFs")
