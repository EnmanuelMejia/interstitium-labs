"""IL-27 Track B: Networking (IL27-M05..M10)."""

MODULES_B = [
{
"id": "IL27-M05",
"code": "IL-27",
"title": "TCP/IP & Subnetting Mastery",
"summary": "The full networking core: OSI/TCP-IP models, IPv4/IPv6, CIDR, subnetting fluency, TCP vs UDP, ports, NAT, and reading a packet's journey. Interview-critical - whiteboard-ready. You need this for -> every networking and security module.",
"objectives": [
"Map protocols to OSI and TCP/IP layers and explain encapsulation.",
"Subnet IPv4 by hand: network, broadcast, usable range, host count for any prefix.",
"Contrast TCP (reliable, handshake, flow control) vs UDP (fast, connectionless) and pick correctly.",
"Name the 12 essential ports/services and their protocols from memory.",
"Explain NAT (source, destination, PAT) and IPv6 addressing basics."
],
"notes": [
{"title": "Models and encapsulation: where everything lives",
"body": "OSI (7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application) is the reference vocabulary; TCP/IP (Link, Internet, Transport, Application) is what actually runs. Troubleshooting flows top-down or bottom-up: 'no link light' is Layer 1, 'no DHCP' is Layer 3/7, 'page won't load but ping works' is Layer 7.\n\nEncapsulation: each layer wraps the payload - HTTP data gets a TCP header (segment), IP header (packet), Ethernet header/trailer (frame). Decapsulation reverses it. MTU (usually 1500 bytes) caps frame size; larger payloads fragment at Layer 3. A Wireshark capture shows you every layer of one packet - learn to read top (frame) to bottom (data).\n\nKey devices by layer: hub (L1, repeats everything - obsolete), switch (L2, forwards by MAC), router (L3, forwards by IP), firewall (L3/L4/L7, policy). 'It's a Layer 8 problem' is engineer slang for user error - funny once, unprofessional twice."
},
{"title": "IPv4, CIDR, and subnetting fluency",
"body": "IPv4: 32 bits, 4 octets, dotted decimal. CIDR /N = N network bits. Classes (A/8, B/16, C/24) are legacy - CIDR replaced them, but 'Class C' still means /24 in conversation. Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16; APIPA 169.254.0.0/16 (seeing APIPA = DHCP failed); loopback 127.0.0.0/8.\n\nSubnetting drill method: (1) interesting octet = first non-255/0 mask octet; (2) block size = 256 - mask octet; (3) subnets step by block size; (4) broadcast = next network - 1; (5) usable = network+1 to broadcast-1. Do 20 of these and it becomes reflex - the interview whiteboard expects reflex.\n\nIPv6: 128 bits, hex, 8 hextets (2001:db8::/32). :: compresses one run of zeros. Link-local fe80::/10 (like APIPA but functional), unique local fc00::/7 (like private v4), global unicast 2000::/3. No broadcast - uses multicast; no NAT needed (address space is effectively infinite); SLAAC lets hosts self-configure. You must be able to recognize and compress/expand addresses even if you don't subnet v6 daily."
},
{"title": "TCP vs UDP, ports, and NAT",
"body": "TCP: connection-oriented, 3-way handshake (SYN, SYN-ACK, ACK), sequence numbers, acknowledgments, retransmission, flow control (windowing), ordered delivery. Cost: latency and overhead. Use for: HTTP/S, email, file transfer, SSH - anything where correctness beats speed.\n\nUDP: fire-and-forget datagrams, no handshake, no ordering, no retransmission. Cost: unreliability. Use for: DNS queries, DHCP, streaming, VoIP, gaming - where speed beats perfection (apps handle loss themselves).\n\nPorts: 16-bit, 0-65535. Well-known 0-1023 (need privilege to bind). Memorize: 22 SSH, 25 SMTP, 53 DNS, 67/68 DHCP, 80 HTTP, 110 POP3, 143 IMAP, 443 HTTPS, 3389 RDP, 445 SMB, 389 LDAP, 636 LDAPS. 'Connection refused on 443' + 'ping works' = service down or firewall, not routing.\n\nNAT: PAT (overload) maps many private IPs to one public IP via source-port tracking - your home router. Static NAT/DNAT maps one public IP:port to an internal server (port forwarding). NAT breaks end-to-end (a feature for hiding, a bug for P2P/VoIP) - IPv6's vast space is the long-term fix."
}
],
"cards": [
{"front": "OSI layers 1-7 mnemonic order", "back": "Physical, Data Link, Network, Transport, Session, Presentation, Application."},
{"front": "Private IPv4 ranges", "back": "10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16."},
{"front": "Seeing 169.254.x.x means?", "back": "APIPA - DHCP failed; check DHCP server/scope/link."},
{"front": "TCP 3-way handshake", "back": "SYN -> SYN-ACK -> ACK."},
{"front": "Ports: SSH, DNS, DHCP, HTTP, HTTPS, RDP, SMB", "back": "22, 53, 67/68, 80, 443, 3389, 445."},
{"front": "Why UDP for DNS and streaming?", "back": "Speed over reliability; single query/response or loss-tolerant media."},
{"front": "PAT (NAT overload) in one line", "back": "Many private IPs share one public IP, distinguished by source port."},
{"front": "IPv6 link-local and its v4 analogy", "back": "fe80::/10 - auto-configured like APIPA, but fully functional on-link."}
],
"quiz": [
{"q": "Ping works but the web page won't load. Most likely layer?", "choices": ["Layer 7 (application) - routing/L3 is fine", "Layer 1", "Layer 2", "Layer 3"], "answer": 0, "index": 0, "explain": "Ping proves L1-L3; HTTP failing above that is app/service."},
{"q": "Network address of 172.16.88.200/20?", "choices": ["172.16.80.0", "172.16.88.0", "172.16.64.0", "172.16.96.0"], "answer": 0, "index": 0, "explain": "Mask 255.255.240.0, block 16 in 3rd octet; 88 in 80-block."},
{"q": "Usable hosts in 192.168.7.0/25?", "choices": ["126", "128", "254", "62"], "answer": 0, "index": 0, "explain": "2^7 - 2 = 126."},
{"q": "Which needs TCP, not UDP?", "choices": ["HTTPS file download", "DNS query", "Live VoIP", "DHCP discover"], "answer": 0, "index": 0, "explain": "File integrity demands TCP's reliability."},
{"q": "A SYN flood attacks:", "choices": ["TCP handshake state - half-open connections exhaust the server", "DNS cache", "DHCP scope", "BGP tables"], "answer": 0, "index": 0, "explain": "SYN without ACK leaves half-open sessions consuming resources."},
{"q": "Expand 2001:db8::1 fully:", "choices": ["2001:0db8:0000:0000:0000:0000:0000:0001", "2001:db8:0:0:0:0:0:1 is already valid compressed; full = 2001:0db8:0000:0000:0000:0000:0000:0001", "2001:db8:1", "2001:db8::0:1"], "answer": 1, "index": 1, "explain": ":: fills one zero run; full form pads each hextet to 4 digits."},
{"q": "Port forwarding a web server is which NAT type?", "choices": ["Static NAT / DNAT", "PAT overload", "NAT64", "No NAT"], "answer": 0, "index": 0, "explain": "Fixed public IP:port -> internal server mapping."},
{"q": "MTU 1500 means:", "choices": ["Max frame payload size before fragmentation", "Minimum packet size", "TCP window size", "Cable length limit"], "answer": 0, "index": 0, "explain": "Larger payloads fragment at L3 to fit the MTU."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M06", "IL27-M07", "IL27-M08", "IL27-M10"],
"drills": [
{"id": "m05-drill-subnet", "title": "Subnet Sprint (whiteboard reps)",
"items": [
{"prompt": "10.10.10.100/22: network?", "answer": "10.10.8.0", "explain": "Block 4; 10 in 8-block."},
{"prompt": "10.10.10.100/22: broadcast?", "answer": "10.10.11.255", "explain": "Next network 10.10.12.0 minus 1."},
{"prompt": "Usable hosts in /20?", "answer": "4094", "explain": "2^12 - 2."},
{"prompt": "Port for LDAPS?", "answer": "636", "explain": "LDAP 389, LDAPS 636."},
{"prompt": "TCP or UDP: DHCP?", "answer": "UDP (67/68)", "explain": "Broadcast discover can't handshake first."},
{"prompt": "Compress 2001:0db8:0000:0000:0000:ff00:0042:8329", "answer": "2001:db8::ff00:42:8329", "explain": "One :: for the longest zero run; drop leading zeros."}
]}
],
"handsOnLab": {
"id": "m05-lab",
"title": "Packet Journey: trace and subnet a real network",
"brief": "Map your home/lab network end to end: addressing plan, path analysis, and a subnetting redesign.",
"steps": [
"Document your current network: your IP, mask, gateway, DNS (ipconfig /all or ip addr). Identify the prefix and usable range.",
"Run tracert/traceroute to 8.8.8.8 and to your gateway; note hop count and where latency jumps.",
"Capture 60 seconds with Wireshark (or pktmon): find one TCP handshake, one DNS query, one DHCP packet; screenshot each.",
"Redesign: carve your /24 into 4 subnets (servers, users, IoT, guest); list each subnet's range and gateway.",
"Write the firewall intent for the redesign: which subnets may initiate to which (one sentence each).",
"Present: 5-minute whiteboard talk explaining your design to a peer (or record yourself)."
],
"deliverable": "Network map + captures with annotations + subnetting redesign + firewall intent + whiteboard recording.",
"checkpoint": "You can subnet any prefix on a whiteboard and narrate a packet's full journey."
},
"mockTask": {"id": "m05-mock", "type": "choice",
"q": "Interview whiteboard: 'Host 192.168.15.90/21 - give me network, broadcast, and usable range.'",
"choices": ["Network 192.168.8.0, broadcast 192.168.15.255, usable .8.1-.15.254", "Network 192.168.15.0, broadcast 192.168.15.255, usable .1-.254", "Network 192.168.0.0, broadcast 192.168.31.255", "Network 192.168.8.0, broadcast 192.168.8.255"],
"answer": 0, "explain": "/21: mask 255.255.248.0, block 8 in 3rd octet; 15 in 8-block (.8-.15)."},
"crossLinks": ["il04-networking"],
"videos": "VIDEOS_M05",
"estimatedMinutes": 330,
"fastTrackEligible": True
},
{
"id": "IL27-M06",
"code": "IL-27",
"title": "DNS & DHCP Deep Dive",
"summary": "The two services users notice only when broken: resolution hierarchy, record types, zones, and the DORA dance - plus diagnosing both like a pro. You need this for -> M14, M10, and half of all 'internet is down' tickets.",
"objectives": [
"Trace a DNS query from stub resolver through root, TLD, and authoritative servers.",
"Choose and read A, AAAA, CNAME, MX, TXT, NS, PTR, SRV, SOA records.",
"Explain the DHCP DORA process and what each packet carries.",
"Diagnose with nslookup/dig, ipconfig /all, and DHCP lease analysis.",
"Implement DNS security basics: DNSSEC concept, DoH/DoT, and rogue-DHCP defense."
],
"notes": [
{"title": "DNS: the hierarchy and the records",
"body": "Resolution path: stub resolver (your PC) -> recursive resolver (usually ISP or 1.1.1.1/8.8.8.8) -> root servers ('.') -> TLD servers (.com) -> authoritative servers (example.com's NS). Caching happens at every level with TTLs - 'DNS hasn't propagated' almost always means a cached old record, not propagation delay.\n\nRecords: A (v4 address), AAAA (v6), CNAME (alias -> canonical name; never at the zone apex), MX (mail exchangers, with preference), TXT (SPF/DKIM/verification strings), NS (authoritative servers), PTR (reverse: IP -> name, in in-addr.arpa), SRV (service location: _ldap._tcp.dc._msdcs - how AD clients find domain controllers), SOA (zone authority: serial, refresh, retry - increment serial on every zone change or secondaries never update).\n\nSplit-brain/split-horizon DNS serves different answers inside vs outside (intranet.company.com resolves privately internally). Conditional forwarders send queries for specific domains to specific servers - the standard AD + public DNS coexistence pattern."
},
{"title": "DHCP: DORA and lease lifecycle",
"body": "DORA: Discover (client broadcasts 'any DHCP server?'), Offer (server proposes IP + options), Request (client accepts), Acknowledge (server confirms). All broadcast until the client has an address; the server is UDP 67, client UDP 68. Lease = temporary ownership with T1 (50%: try to renew with the original server) and T2 (87.5%: broadcast rebind to any server).\n\nScope options that matter: 003 Router (gateway), 006 DNS Servers, 015 DNS Domain Name, 051 Lease Time, 066/067 (PXE boot server/file - imaging depends on these). Reservations pin IPs to MACs (printers, servers); exclusions carve ranges out of the scope. Rogue DHCP defense: DHCP snooping on switches (trust only uplink ports), 802.1X.\n\n'No internet' triage: ipconfig /all - APIPA (169.254.x.x) = DHCP failed: check link, scope exhaustion (event log), rogue server, or relay (ip helper-address) missing on the router for cross-subnet DHCP."
},
{"title": "Diagnosing like a pro",
"body": "DNS diagnosis order: (1) Is it DNS at all? ping the IP vs the name - IP works + name fails = DNS. (2) Which resolver? Check configured DNS (ipconfig /all). (3) What does IT say? nslookup name, then nslookup name <specific-server> to bypass the local resolver. dig +trace shows the full hierarchy walk. (4) Cache? ipconfig /flushdns, then check TTL on the record - you may just need to wait out the TTL.\n\nCommon DNS failures: stale cache, wrong forwarder, expired delegation (NS glue), DNSSEC validation failure (looks like 'random sites down'), and the classic - the DC's own DNS pointing at the ISP instead of itself (AD breaks: SRV lookups fail, logons fail).\n\nDHCP diagnosis: scope full (check % in use - 80% is the warning line), lease duration too long for guest VLANs (8-day leases on a coffee-shop VLAN = exhaustion), duplicate IPs from static assignments inside the scope (exclude statics!), and time sync - Kerberos dies if clocks drift >5 min, and DHCP option 042 (NTP) or domain hierarchy keeps them aligned."
}
],
"cards": [
{"front": "DNS resolution order", "back": "Stub -> recursive -> root -> TLD -> authoritative, caching at each level."},
{"front": "Which record finds domain controllers?", "back": "SRV (_ldap._tcp.dc._msdcs)."},
{"front": "CNAME restriction", "back": "Never at the zone apex (use ALIAS/ANAME or A records there)."},
{"front": "DORA expansion", "back": "Discover, Offer, Request, Acknowledge."},
{"front": "DHCP ports", "back": "Server UDP 67, client UDP 68."},
{"front": "T1 and T2 timers", "back": "T1 = 50% lease: renew with original server. T2 = 87.5%: broadcast rebind."},
{"front": "APIPA range and meaning", "back": "169.254.0.0/16 - DHCP failed."},
{"front": "nslookup vs dig +trace", "back": "nslookup: quick query. dig +trace: walks the full hierarchy (root to authoritative)."}
],
"quiz": [
{"q": "IP pings but the name doesn't resolve. First conclusion?", "choices": ["DNS issue - L3 works, resolution fails", "Routing issue", "Cable unplugged", "Firewall blocking all"], "answer": 0, "index": 0, "explain": "IP reachability proves the path; names failing isolates DNS."},
{"q": "After a zone change, secondaries don't update. Likely?", "choices": ["SOA serial not incremented", "Wrong TTL", "CNAME at apex", "IPv6 disabled"], "answer": 0, "index": 0, "explain": "Secondaries compare serials; unchanged serial = no transfer."},
{"q": "DORA: which packet carries the proposed IP, mask, gateway, DNS?", "choices": ["Offer", "Discover", "Request", "Acknowledge"], "answer": 0, "index": 0, "explain": "Offer proposes; Request accepts; ACK confirms."},
{"q": "Guest VLAN exhausts its scope daily. Best fix?", "choices": ["Shorten lease time (e.g., 1-4 hours) for high-churn scopes", "Add more DNS servers", "Disable DHCP", "Longer leases"], "answer": 0, "index": 0, "explain": "Short leases recycle addresses as guests leave."},
{"q": "AD logons failing; DC's DNS points to the ISP. Why?", "choices": ["SRV lookups for DC location fail - DC must use itself/AD DNS", "ISP is slow", "Passwords expired", "Time sync"], "answer": 0, "index": 0, "explain": "AD is DNS-dependent; the DC needs AD-integrated DNS first."},
{"q": "Defense against rogue DHCP servers?", "choices": ["DHCP snooping - trust only uplink ports", "Longer leases", "More scopes", "Disable ARP"], "answer": 0, "index": 0, "explain": "Snooping drops DHCP offers from untrusted ports."},
{"q": "dig +trace is used to:", "choices": ["Walk the DNS hierarchy from root to authoritative", "Flush the cache", "Renew DHCP", "Test TCP"], "answer": 0, "index": 0, "explain": "It shows each delegation step - ideal for delegation failures."},
{"q": "DHCP option 003, 006, 015 are:", "choices": ["Router, DNS servers, DNS domain name", "NTP, WINS, PXE", "Lease, T1, T2", "Vendor, class, client ID"], "answer": 0, "index": 0, "explain": "The three options every client needs to get online."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M14", "IL27-M10"],
"drills": [
{"id": "m06-drill-dns", "title": "DNS/DHCP Triage Drill",
"items": [
{"prompt": "IP works, name fails", "answer": "DNS: check resolver, nslookup, flush cache", "explain": "Isolates resolution from routing."},
{"prompt": "Client has 169.254.x.x", "answer": "DHCP failed: link, scope full, rogue, relay", "explain": "APIPA = no lease obtained."},
{"prompt": "New DNS record not visible", "answer": "Check TTL/cache; verify on authoritative directly", "explain": "'Propagation' is usually cache."},
{"prompt": "Duplicate IP conflicts", "answer": "Static IP inside DHCP scope - exclude statics", "explain": "Scope must not hand out static addresses."},
{"prompt": "Kerberos logons failing site-wide", "answer": "Check time sync (5-min skew kills Kerberos)", "explain": "Clock drift breaks ticket validation."},
{"prompt": "Find which server answered a query", "answer": "nslookup with explicit server / dig @server", "explain": "Bypass local resolver to test a specific server."}
]}
],
"handsOnLab": {
"id": "m06-lab",
"title": "DNS & DHCP Lab: build, break, diagnose",
"brief": "Run DNS and DHCP services in your lab, then diagnose scripted failures.",
"steps": [
"On a Linux VM or Windows Server: install a DNS server (BIND/dnsmasq/Windows DNS); create a forward zone for lab.local with A, CNAME, MX, TXT records.",
"Install DHCP (isc-dhcp-server/Windows DHCP); create a scope with options 003/006/015 and one reservation.",
"Verify: client gets lease, resolves lab.local names, dig +trace works.",
"Break 1: stop DHCP; observe APIPA on client; diagnose with the triage order; fix.",
"Break 2: poison the zone with a wrong A record; practice flush + TTL reasoning; fix and verify with direct authoritative query.",
"Document both incidents as KB articles (M04 format)."
],
"deliverable": "Working DNS+DHCP lab + two incident KBs with diagnosis timelines.",
"checkpoint": "You can build both services and diagnose any 'can't get online' ticket systematically."
},
"mockTask": {"id": "m06-mock", "type": "choice",
"q": "Interview: 'Half the office lost internet but can ping 8.8.8.8. What's your diagnosis path?'",
"choices": ["DNS: verify with nslookup, check the resolver config, test the DNS server directly, check forwarder/DNSSEC issues", "Replace the firewall", "Reboot all PCs", "Call the ISP immediately"],
"answer": 0, "index": 0, "explain": "Pingable IP + dead names = DNS; work resolver -> server -> forwarders."},
"crossLinks": ["il04-networking"],
"videos": "VIDEOS_M06",
"estimatedMinutes": 300,
"fastTrackEligible": True
},
{
"id": "IL27-M07",
"code": "IL-27",
"title": "Switching, VLANs & Ethernet",
"summary": "How switches learn, why VLANs segment, trunking, STP, and the access-layer security that stops the easy attacks. You need this for -> M29 microsegmentation and any office network design.",
"objectives": [
"Explain MAC learning, flooding, and the CAM table.",
"Design VLAN segmentation (data, voice, guest, IoT, management) and configure access vs trunk ports.",
"Describe 802.1Q tagging and native VLAN risks.",
"Explain STP's purpose and the cost of getting it wrong.",
"Apply port security, BPDU guard, and DHCP snooping concepts."
],
"notes": [
{"title": "How a switch thinks: MAC learning and forwarding",
"body": "A switch learns by reading source MACs: frame arrives on port 3 from AA:BB:CC -> CAM table records 'AA:BB:CC lives on port 3'. To forward, it looks up the DESTINATION MAC: known -> send out that port only; unknown -> flood out all ports except the source (unknown unicast flooding). This is why the first packet to a new host is broadcast-ish and later ones are switched.\n\nCollision domains died with hubs; every switch port is its own collision domain (full duplex). Broadcast domains are the new boundary: ARP, DHCP, and broadcast storms hit every port in the VLAN. A /24 with 500 chatty IoT devices is a broadcast problem, not a bandwidth problem.\n\nSpeed/duplex: autonegotiation usually works; hardcode only when it doesn't (mismatched manual/auto = duplex mismatch = late collisions and terrible throughput). Check interface counters: CRC errors = Layer 1 (cable/NIC); runts/giants = duplex/mtu issues."
},
{"title": "VLANs: segmentation without new hardware",
"body": "A VLAN is a logical broadcast domain on shared switches. Design pattern: VLAN 10 users, 20 voice, 30 guest, 40 IoT, 99 management, 1 unused (never use VLAN 1 for traffic). Benefits: broadcast containment, security policy boundaries, and QoS per VLAN (voice gets priority).\n\nAccess ports carry ONE untagged VLAN (endpoints). Trunk ports carry MANY tagged VLANs via 802.1Q (4-byte tag inserted in the frame; switch-to-switch and switch-to-AP/router). Native VLAN = the one untagged VLAN on a trunk; mismatch it and traffic leaks between VLANs - set it to an unused VLAN and prune allowed VLANs to only what's needed.\n\nInter-VLAN routing: traffic between VLANs must hit a Layer 3 device (router or L3 switch SVI) - this is where your firewall/ACL policy lives. 'Same VLAN can talk, different VLANs route' is the whole game, and it's the on-prem ancestor of microsegmentation."
},
{"title": "STP and access-layer defense",
"body": "Spanning Tree (STP/RSTP) prevents switching loops: it elects a root bridge and blocks redundant ports. A loop without STP = broadcast storm = network meltdown in seconds. Cost of misconfiguration: a user plugging both ends of a cable into wall jacks creates a loop - BPDU Guard shuts down ports that receive BPDUs unexpectedly (access ports should never speak STP).\n\nPort security: limit MACs per port (1 for user ports), sticky-learn the first MAC, violation = shutdown or restrict. This kills casual rogue-device plug-ins and MAC flooding (which overflows the CAM table and turns the switch into a hub - an eavesdropper's trick).\n\nDHCP snooping + Dynamic ARP Inspection: the switch builds a binding table (MAC/IP/port/VLAN) from trusted DHCP, then drops DHCP offers from untrusted ports (rogue server defense) and validates ARP packets against bindings (ARP spoofing defense). These three - port security, BPDU guard, snooping/DAI - are the access-layer Zero Trust baseline."
}
],
"cards": [
{"front": "Unknown unicast flooding", "back": "Destination MAC not in CAM -> flood out all ports except source."},
{"front": "Access vs trunk port", "back": "Access: one untagged VLAN (endpoints). Trunk: many tagged VLANs via 802.1Q (switch/AP/router links)."},
{"front": "Native VLAN risk", "back": "Untagged on trunk; mismatch leaks traffic - set to unused VLAN, prune allowed list."},
{"front": "What does STP prevent?", "back": "Switching loops -> broadcast storms; blocks redundant ports, elects root bridge."},
{"front": "BPDU Guard purpose", "back": "Shut down access ports that receive BPDUs - users must never introduce switches/STP."},
{"front": "MAC flooding attack and defense", "back": "Overflow CAM -> switch floods like hub. Defense: port security (limit/sticky MACs)."},
{"front": "DHCP snooping + DAI stop what?", "back": "Rogue DHCP servers and ARP spoofing, via the DHCP binding table."},
{"front": "Where does inter-VLAN policy live?", "back": "At the L3 boundary (router/L3 switch SVI/firewall) between VLANs."}
],
"quiz": [
{"q": "A switch receives a frame for an unknown destination MAC. It:", "choices": ["Floods it out all ports except the source port", "Drops it", "Sends it to the gateway", "Buffers it forever"], "answer": 0, "index": 0, "explain": "Unknown unicast flooding - the learning mechanism."},
{"q": "Best native VLAN practice on trunks?", "choices": ["Set to an unused VLAN and prune allowed VLANs", "Leave as VLAN 1 everywhere", "Tag the native VLAN too", "Disable trunking"], "answer": 0, "index": 0, "explain": "VLAN 1 + mismatched native = hopping/leak risk."},
{"q": "User plugs both cable ends into two wall jacks; network dies. Cause and fix?", "choices": ["Switching loop; STP/BPDU Guard should have blocked it - enable BPDU Guard on access ports", "DHCP exhaustion", "Bad cable", "Virus"], "answer": 0, "index": 0, "explain": "Classic loop -> broadcast storm; BPDU Guard is the guardrail."},
{"q": "Voice VLAN's main benefit besides segmentation?", "choices": ["QoS priority for call quality", "Faster internet", "Free calls", "Hides phones"], "answer": 0, "index": 0, "explain": "Voice gets priority queuing to prevent jitter."},
{"q": "CRC errors climbing on a switch port indicate:", "choices": ["Layer 1 issue - cable, NIC, or duplex mismatch", "VLAN misconfig", "STP loop", "DHCP problem"], "answer": 0, "index": 0, "explain": "CRC = corrupted frames = physical layer."},
{"q": "Two devices in different VLANs need to communicate. Required?", "choices": ["Inter-VLAN routing via L3 device", "A bigger switch", "Same VLAN", "A hub"], "answer": 0, "index": 0, "explain": "VLANs are separate broadcast domains; L3 routes between them."},
{"q": "Port security with sticky MAC, violation shutdown, stops:", "choices": ["Rogue devices and MAC flooding on access ports", "STP loops", "DHCP starvation", "Routing loops"], "answer": 0, "index": 0, "explain": "Limits/learns MACs per port; violations shut the port."},
{"q": "802.1Q tag is:", "choices": ["4 bytes inserted into the Ethernet frame identifying the VLAN", "An IP header", "A routing protocol", "A cable type"], "answer": 0, "index": 0, "explain": "The tag carries the VLAN ID on trunks."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M08", "IL27-M29"],
"drills": [
{"id": "m07-drill-switch", "title": "Switching Drill",
"items": [
{"prompt": "Design VLANs for office: name 5", "answer": "Users, voice, guest, IoT, management (VLAN 1 unused)", "explain": "Standard segmentation pattern."},
{"prompt": "AP connects to switch: port type?", "answer": "Trunk (carries multiple SSID VLANs tagged)", "explain": "APs need multiple VLANs = trunk."},
{"prompt": "PC connects to switch: port type?", "answer": "Access, single data VLAN (+ voice VLAN for phone)", "explain": "Endpoints get untagged access ports."},
{"prompt": "Storm after new cable run", "answer": "Loop: check STP, enable BPDU Guard on access ports", "explain": "New loop = broadcast storm."},
{"prompt": "Guest can reach servers", "answer": "Inter-VLAN ACL/firewall missing - add deny rules at L3 boundary", "explain": "Segmentation needs policy at the routed boundary."},
{"prompt": "Unknown MAC flooding risk", "answer": "Port security: limit 1-2 MACs, sticky, violation shutdown", "explain": "Stops CAM overflow attacks."}
]}
],
"handsOnLab": {
"id": "m07-lab",
"title": "VLAN Lab: segment a virtual office",
"brief": "Build a 3-VLAN office in Packet Tracer/GNS3/EVE-NG (or a managed switch) with routing and ACLs.",
"steps": [
"Create VLANs 10 (users), 30 (guest), 99 (mgmt) on a virtual switch.",
"Configure access ports for 2 PCs in VLAN 10, 1 in VLAN 30; trunk to the router.",
"Configure inter-VLAN routing (router-on-a-stick or SVIs); verify user-to-user ping works.",
"Add ACL: guest VLAN can reach internet only, not VLAN 10 or management; verify with pings.",
"Simulate a loop (connect two access ports together); observe the storm, then enable STP/RSTP + BPDU Guard and verify recovery.",
"Document the addressing, port assignments, and ACLs as a network diagram."
],
"deliverable": "Working VLAN lab + ACL verification + loop test notes + network diagram.",
"checkpoint": "You can segment, route, and protect an office network's access layer."
},
"mockTask": {"id": "m07-mock", "type": "choice",
"q": "Interview: 'How would you segment a 200-person office network?'",
"choices": ["VLANs for users/voice/guest/IoT/management, inter-VLAN routing with ACLs at the L3 boundary, BPDU Guard + port security on access ports", "One flat /24 for simplicity", "A VLAN per person", "No segmentation - firewalls are enough"],
"answer": 0, "explain": "Standard enterprise pattern: segment, route with policy, harden the edge."},
"crossLinks": ["il04-networking"],
"videos": "VIDEOS_M07",
"estimatedMinutes": 260,
"fastTrackEligible": False
},
{
"id": "IL27-M08",
"code": "IL-27",
"title": "Routing, VPN & WAN",
"summary": "How packets cross networks: routing tables, static vs dynamic (OSPF/BGP concepts), VPN types, and WAN options. You need this for -> M29, site connectivity, and remote-access design.",
"objectives": [
"Read a routing table and predict a packet's path (longest-prefix match).",
"Contrast static routing vs OSPF vs BGP and state where each belongs.",
"Compare VPN types: site-to-site IPsec, remote-access, SSL/TLS VPN, WireGuard, and Always On VPN concept.",
"Explain WAN options: internet, MPLS concept, SD-WAN, and LTE/5G backup.",
"Diagnose with traceroute, ping, and route print."
],
"notes": [
{"title": "Routing: tables, longest match, and protocols",
"body": "A router forwards by longest-prefix match: for destination 10.1.5.9 with routes 10.0.0.0/8 and 10.1.0.0/16, the /16 wins (more specific). Default route (0.0.0.0/0) is the gateway of last resort. route print (Windows) / ip route (Linux) shows the table; administrative distance/metric breaks ties.\n\nStatic routes: hand-written, fine for small/stub networks, zero protocol overhead, but no failover intelligence. Dynamic: OSPF (link-state, interior, fast convergence, areas) for inside your org; BGP (path-vector, exterior) for between orgs and the internet - BGP is how the internet itself routes, and also how cloud hybrid connections (Azure ExpressRoute, AWS Direct Connect) exchange routes.\n\nFirst-hop redundancy: HSRP/VRRP give one virtual gateway IP across two routers - clients never reconfigure when a router dies. Asymmetric routing (out one path, back another) breaks stateful firewalls; design symmetric paths or stateless policy."
},
{"title": "VPNs: the four patterns",
"body": "Site-to-site IPsec: always-on tunnel between firewalls/routers connecting whole networks (branch <-> HQ). IKEv2 negotiates; ESP encrypts. Remote-access VPN: client software dials in (user laptops) - being displaced by Zero Trust Network Access in modern designs, but still everywhere.\n\nSSL/TLS VPN (clientless or client): browser or lightweight client, good through restrictive firewalls (looks like HTTPS). WireGuard: modern, tiny codebase, fast - increasingly the default for new builds. Always On VPN (Windows): device-tunnel + user-tunnel auto-connecting before logon - the enterprise answer to 'VPN but users forget'.\n\nSplit tunneling: only corporate traffic goes through the VPN (fast, less load) vs full tunnel (all traffic inspected - secure, slower, privacy questions). For a Zero Trust company, the direction is identity-aware access per app rather than network-wide tunnels - but you must still operate the VPNs in the meantime."
},
{"title": "WAN options and diagnosis",
"body": "Internet VPN: cheap, variable. MPLS: private, SLA-backed, expensive - the old enterprise standard, now often replaced by SD-WAN. SD-WAN: overlays multiple links (broadband + LTE), picks paths per app by live quality, central policy - the current enterprise default. LTE/5G: backup path or primary for pop-up sites; mind data caps.\n\nDiagnosis path: (1) Is it local? ping gateway. (2) Is it the WAN? ping past the edge, traceroute to see where hops die. (3) Is it the tunnel? Check VPN status/phase 1 (IKE) vs phase 2 (IPsec) - phase 1 down = peer/auth/network; phase 2 down = interesting-traffic/ACL mismatch. (4) Is it MTU? VPN overhead + 1500 MTU = fragmentation; ping -f -l 1472 tests DF-bit path MTU.\n\nDocument every WAN link: provider, circuit ID, bandwidth, SLA, support number, and the failover order. At 2 AM, this page is worth more than any certification."
}
],
"cards": [
{"front": "Longest-prefix match example", "back": "10.1.5.9 matches 10.1.0.0/16 over 10.0.0.0/8 - most specific wins."},
{"front": "OSPF vs BGP placement", "back": "OSPF: interior (inside org). BGP: exterior (between orgs/internet/cloud)."},
{"front": "VPN phase 1 vs phase 2 down", "back": "Phase 1 (IKE): peer/auth/network. Phase 2 (IPsec): interesting-traffic/ACL mismatch."},
{"front": "Split tunnel vs full tunnel", "back": "Split: only corp traffic via VPN. Full: all traffic via VPN (inspected, slower)."},
{"front": "HSRP/VRRP purpose", "back": "Virtual gateway IP across routers - first-hop redundancy without client changes."},
{"front": "SD-WAN in one line", "back": "Overlay across multiple links; per-app path selection by live quality; central policy."},
{"front": "ping -f -l 1472 tests what?", "back": "Path MTU with Don't-Fragment - finds VPN fragmentation issues."},
{"front": "WireGuard's advantages", "back": "Tiny auditable codebase, fast, modern crypto - default for new builds."}
],
"quiz": [
{"q": "Routes: 10.0.0.0/8 via R1, 10.1.0.0/16 via R2. Packet to 10.1.5.9 goes via:", "choices": ["R2 (longest match /16)", "R1", "Both", "Neither"], "answer": 0, "index": 0, "explain": "Most specific prefix wins."},
{"q": "Branch-to-HQ always-on network connection uses:", "choices": ["Site-to-site IPsec VPN", "Remote-access VPN", "Dial-up", "Bluetooth"], "answer": 0, "index": 0, "explain": "Site-to-site connects whole networks persistently."},
{"q": "VPN shows phase 1 up, phase 2 down. Check:", "choices": ["Interesting traffic ACLs / proxy IDs on both ends", "The ISP", "User passwords", "DNS"], "answer": 0, "index": 0, "explain": "Phase 2 negotiates the traffic selectors; mismatch = no tunnel."},
{"q": "Asymmetric routing breaks:", "choices": ["Stateful firewalls (return path differs)", "DNS", "DHCP", "ARP"], "answer": 0, "index": 0, "explain": "Stateful devices must see both directions."},
{"q": "SD-WAN's core value over single-link internet VPN?", "choices": ["Multi-link with per-app path selection by live quality", "It's cheaper hardware", "No encryption needed", "Unlimited bandwidth"], "answer": 0, "index": 0, "explain": "Quality-based steering across links is the differentiator."},
{"q": "Traceroute dies at hop 3 (your edge). Likely?", "choices": ["Edge/WAN issue - check VPN/WAN status past your router", "Target server down", "DNS failure", "PC firewall"], "answer": 0, "index": 0, "explain": "Dying at the edge implicates the WAN/tunnel, not the far end."},
{"q": "Always On VPN's device tunnel exists so:", "choices": ["The device connects before user logon (GPO, management)", "Users browse faster", "It replaces antivirus", "Passwords sync"], "answer": 0, "index": 0, "explain": "Pre-logon connectivity enables management and domain logon off-network."},
{"q": "BGP is used for:", "choices": ["Routing between organizations and the internet", "Inside a single office", "Switching", "Wi-Fi roaming"], "answer": 0, "index": 0, "explain": "Path-vector exterior protocol - the internet's routing language."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M29"],
"drills": [
{"id": "m08-drill-wan", "title": "Routing & VPN Drill",
"items": [
{"prompt": "Packet to 10.2.9.9; routes 10.0.0.0/8, 10.2.0.0/16", "answer": "Via 10.2.0.0/16 (longest match)", "explain": "/16 beats /8."},
{"prompt": "VPN tunnel won't establish at all", "answer": "Phase 1: check peer IP, PSK/certs, UDP 500/4500, NAT-T", "explain": "IKE needs reachability + auth."},
{"prompt": "Tunnel up but no traffic flows", "answer": "Phase 2: interesting-traffic/ACL mismatch or firewall rules", "explain": "Tunnel exists; selectors or policy block."},
{"prompt": "Big file transfers stall over VPN", "answer": "MTU/fragmentation: test ping -f -l 1472, consider MSS clamping", "explain": "VPN overhead + 1500 MTU fragments."},
{"prompt": "Need branch failover without client changes", "answer": "HSRP/VRRP virtual gateway", "explain": "First-hop redundancy."},
{"prompt": "Choose: MPLS vs SD-WAN for 20 branches", "answer": "SD-WAN usually: cheaper, app-aware, multi-link; MPLS only for strict SLA needs", "explain": "Cost + agility favor SD-WAN today."}
]}
],
"handsOnLab": {
"id": "m08-lab",
"title": "Tunnel Lab: site-to-site VPN between virtual sites",
"brief": "Build two virtual sites and connect them with a VPN tunnel; break and diagnose it.",
"steps": [
"Create two virtual networks (pfSense/OPNsense VMs or cloud VPCs) as 'HQ' and 'Branch' with distinct subnets.",
"Configure a site-to-site IPsec (or WireGuard) tunnel; verify with ping across the tunnel.",
"Document the phase 1/phase 2 parameters on both ends.",
"Break it: change the PSK on one end; diagnose using the phase framework; fix.",
"Break it: misconfigure interesting traffic; diagnose; fix.",
"Write the WAN runbook page: circuit info, tunnel params, diagnosis order."
],
"deliverable": "Working tunnel + two break/fix incident notes + WAN runbook page.",
"checkpoint": "You can build, diagnose (phase 1 vs 2), and document a site-to-site VPN."
},
"mockTask": {"id": "m08-mock", "type": "choice",
"q": "Interview: 'Branch office can't reach HQ over the site-to-site VPN. Walk me through it.'",
"choices": ["Check tunnel status: phase 1 (peer/auth) then phase 2 (traffic selectors), then routing past the tunnel, then MTU", "Reboot both firewalls immediately", "Blame the ISP", "Rebuild the tunnel from scratch"],
"answer": 0, "explain": "Layered diagnosis: IKE, IPsec, routing, MTU - in order."},
"crossLinks": ["il04-networking"],
"videos": [],
"estimatedMinutes": 240,
"fastTrackEligible": False
},
{
"id": "IL27-M09",
"code": "IL-27",
"title": "Wireless Networking",
"summary": "Wi-Fi that actually works: bands, channels, SSIDs, roaming, WPA3, and the site survey basics. You need this for -> office deployments and the endless 'Wi-Fi is slow' tickets.",
"objectives": [
"Contrast 2.4/5/6 GHz bands: range, speed, congestion trade-offs.",
"Plan channels (1/6/11 on 2.4 GHz) and explain co-channel interference.",
"Design SSIDs: corporate (WPA3-Enterprise/802.1X), guest (isolated), IoT (PSK, segmented).",
"Explain roaming (BSS transition) and what breaks it.",
"Diagnose with signal strength, SNR, and utilization - not just 'bars'."
],
"notes": [
{"title": "Bands, channels, and the physics you can't negotiate",
"body": "2.4 GHz: long range, wall-penetrating, crowded (Bluetooth, microwaves, every IoT gadget), max ~3 non-overlapping 20MHz channels (1, 6, 11). 5 GHz: faster, more channels, shorter range. 6 GHz (Wi-Fi 6E/7): huge clean spectrum, shortest range - glorious in open offices, useless through concrete.\n\nChannel planning: on 2.4 GHz use ONLY 1/6/11 at 20MHz width - 40MHz 'wide' channels on 2.4 just create interference. On 5 GHz, use 20/40/80MHz thoughtfully; wider isn't always better in dense offices (fewer clean channels). Co-channel interference (same channel nearby) is managed by CSMA/CA taking turns; adjacent-channel interference (overlapping like ch 3 vs 1) is pure noise - worse.\n\ndBm, not bars: -30 excellent, -67 the VoIP/real-time floor, -70 usable data, -80 barely. SNR = signal minus noise floor; 25dB+ is healthy. 'Slow Wi-Fi' with -82dBm isn't a Wi-Fi problem, it's a coverage problem."
},
{"title": "SSID design and WPA3",
"body": "One SSID per purpose, each mapped to a VLAN: CORP (WPA3-Enterprise with 802.1X/RADIUS - per-user credentials, no shared PSK to leak), GUEST (open or PSK, client isolation, rate-limited, internet-only ACL), IOT (WPA3-Personal or WPA2 PSK, dedicated VLAN, no internet except required endpoints).\n\nWPA3: SAE handshake replaces WPA2's vulnerable 4-way handshake (no more offline dictionary attacks on captures); WPA3-Enterprise adds 192-bit mode. Transition mode (WPA3/WPA2 mixed) during migration. Never WEP (broken in minutes), never open for corporate, and treat PSKs as shared secrets with an expiry/rotation plan.\n\n802.1X: the AP becomes an authenticator, RADIUS (NPS/Entra) authenticates against AD - the wireless equivalent of 'no anonymous access'. Machine + user auth (EAP-TLS with certs) is the gold standard: the device proves itself before the user even logs on."
},
{"title": "Roaming, surveys, and diagnosis",
"body": "Roaming: clients decide when to roam (sticky clients cling to weak APs). 802.11k (neighbor reports), 802.11v (BSS transition management), 802.11r (fast roaming - key caching) help; without r, VoIP calls drop during roams. Power levels matter more than AP count: too loud = clients won't roam; tune 5GHz slightly lower than 2.4 to encourage 5GHz use.\n\nSite survey basics: predictive (Ekahau-style modeling from floor plans) then validation (walk with a survey tool, measure -dBm and SNR per room). AP placement: ceiling-center of coverage cells, 20-30% cell overlap, away from microwaves/elevators/metal. Document AP names, channels, power, and switch ports.\n\nDiagnosis order: (1) signal/SNR at the spot (-67 floor for real-time), (2) channel utilization (busy airtime = everyone's slow), (3) client capability (old 802.11n client drags the cell), (4) DHCP/DNS/roaming (is it even Wi-Fi? or the wire behind it?). 'Wi-Fi is slow in the conference room at 2 PM' is usually 30 clients on one AP - capacity, not coverage."
}
],
"cards": [
{"front": "2.4 GHz non-overlapping channels", "back": "1, 6, 11 (20MHz only)."},
{"front": "dBm floors: excellent / VoIP floor / barely usable", "back": "-30 / -67 / -80."},
{"front": "WPA3's key improvement over WPA2", "back": "SAE handshake - resistant to offline dictionary attacks."},
{"front": "802.1X in one line", "back": "Port-based auth: AP asks RADIUS, RADIUS checks AD - per-user wireless auth."},
{"front": "802.11k/v/r do what?", "back": "k: neighbor reports. v: BSS transition mgmt. r: fast roaming (key caching)."},
{"front": "Why not max power on all APs?", "back": "Too loud = sticky clients won't roam; cells must overlap modestly."},
{"front": "Guest SSID essentials", "back": "Isolated VLAN, client isolation, rate limit, internet-only ACL."},
{"front": "'Slow Wi-Fi' diagnosis order", "back": "Signal/SNR -> channel utilization -> client capability -> DHCP/DNS/wire behind."}
],
"quiz": [
{"q": "Conference room Wi-Fi dies daily at 2 PM. Most likely?", "choices": ["Capacity: 30 clients on one AP saturating airtime", "Broken AP", "Solar flare", "Wrong password"], "answer": 0, "index": 0, "explain": "Time-correlated + location = capacity, not coverage."},
{"q": "On 2.4 GHz you should use:", "choices": ["Channels 1, 6, 11 at 20MHz", "Channel 3 for variety", "40MHz everywhere", "Auto and hope"], "answer": 0, "index": 0, "explain": "Only 1/6/11 don't overlap; 40MHz on 2.4 causes interference."},
{"q": "A VoIP phone needs at least what signal?", "choices": ["-67 dBm", "-80 dBm", "-50 dBm exactly", "-90 dBm"], "answer": 0, "index": 0, "explain": "-67dBm is the real-time floor."},
{"q": "WPA3-Enterprise with EAP-TLS gives you:", "choices": ["Per-device cert auth before logon - no shared PSK", "Faster internet", "Free roaming", "Longer range"], "answer": 0, "index": 0, "explain": "Certificate-based machine+user auth is the gold standard."},
{"q": "Clients cling to a distant AP instead of roaming. Fix?", "choices": ["Tune power levels; enable 802.11k/v/r", "Add more SSIDs", "Max all AP power", "Disable 5 GHz"], "answer": 0, "index": 0, "explain": "Sticky clients need power tuning + roaming assistance."},
{"q": "Adjacent-channel interference is worse than co-channel because:", "choices": ["Overlapping channels are pure noise; co-channel at least takes turns (CSMA/CA)", "It's louder", "It uses more power", "It breaks WPA3"], "answer": 0, "index": 0, "explain": "Same-channel devices coordinate; overlapping ones just jam."},
{"q": "IoT SSID best practice?", "choices": ["Dedicated VLAN, PSK, no internet except required endpoints", "Same as CORP", "Open, no password", "Hidden SSID only"], "answer": 0, "index": 0, "explain": "Segment and least-privilege the untrustworthy devices."},
{"q": "Hidden SSID as a security measure is:", "choices": ["Ineffective - SSIDs are easily discovered; use WPA3 instead", "Sufficient", "Required for WPA3", "Illegal"], "answer": 0, "index": 0, "explain": "Obscurity isn't security; probe responses leak it."}
],
"weight": 1,
"prerequisiteFor": [],
"drills": [
{"id": "m09-drill-wifi", "title": "Wi-Fi Triage Drill",
"items": [
{"prompt": "'Slow Wi-Fi' in one room at peak hours", "answer": "Capacity: check client count + channel utilization", "explain": "Time/location-correlated = capacity."},
{"prompt": "Dead spot in a corner office", "answer": "Coverage: measure dBm; add/tune AP", "explain": "-80dBm = coverage problem."},
{"prompt": "VoIP calls drop while walking", "answer": "Roaming: check 802.11r/k/v, power tuning", "explain": "Roam-time gaps drop calls."},
{"prompt": "Guest users reach servers", "answer": "Guest VLAN missing isolation/ACLs", "explain": "Segment + client isolation + internet-only ACL."},
{"prompt": "PSK leaked (ex-employee knows it)", "answer": "Rotate PSK; better: move corp to 802.1X", "explain": "Shared secrets need rotation; 1X removes the problem."},
{"prompt": "Interference suspected near kitchen", "answer": "Microwaves/Bluetooth on 2.4 GHz; move clients to 5 GHz", "explain": "2.4 GHz is the crowded band."}
]}
],
"handsOnLab": {
"id": "m09-lab",
"title": "Wi-Fi Survey: measure your own airspace",
"brief": "Survey your home/lab Wi-Fi with free tools and produce a mini heatmap + improvement plan.",
"steps": [
"Install a Wi-Fi analyzer (phone or laptop); record SSIDs, channels, dBm, and band in 4 locations.",
"Identify: overlapping 2.4 GHz channels, your dBm at each spot, and the noisiest band.",
"Check your AP's channel settings; propose a 1/6/11 (or 5 GHz) plan for your environment.",
"Design SSIDs for a 20-person office: CORP/GUEST/IOT with auth method + VLAN each.",
"Measure before/after if you change a channel; document the dBm/SNR delta.",
"Write the one-page Wi-Fi standard you'd deploy (bands, channels, SSIDs, minimums)."
],
"deliverable": "Survey table + heatmap sketch + channel plan + office SSID design + Wi-Fi standard doc.",
"checkpoint": "You can measure, explain, and fix real Wi-Fi problems with numbers, not bars."
},
"mockTask": {"id": "m09-mock", "type": "choice",
"q": "Interview: 'Users complain Wi-Fi is slow everywhere at 9 AM. Your approach?'",
"choices": ["Measure: dBm/SNR, channel utilization, client count per AP - distinguish capacity vs coverage vs backhaul, then tune/add APs or stagger", "Buy more APs immediately", "Tell users to use Ethernet", "Reboot the controller"],
"answer": 0, "index": 0, "explain": "Measure first: 9 AM = login-storm capacity until proven otherwise."},
"crossLinks": ["il04-networking"],
"videos": [],
"estimatedMinutes": 200,
"fastTrackEligible": False
},
{
"id": "IL27-M10",
"code": "IL-27",
"title": "Network Troubleshooting Methodology + Wireshark",
"summary": "The systematic method (OSI layered approach), the essential toolkit, and reading packets in Wireshark. Interview-critical - 'walk me through a network outage' lives here. You need this for -> M30 and every incident.",
"objectives": [
"Apply the OSI layered troubleshooting method top-down and bottom-up.",
"Use ping, traceroute, nslookup/dig, netstat/ss, arp, and route print in a structured flow.",
"Capture and filter in Wireshark: display filters, follow TCP stream, IO graphs.",
"Identify from a capture: handshake failures, retransmissions, DNS issues, DHCP problems.",
"Document findings as an evidence-based incident timeline."
],
"notes": [
{"title": "The methodology: layered, not random",
"body": "Two valid approaches: bottom-up (Physical -> up: link light? IP? gateway? DNS? app?) and top-down (app -> down). Bottom-up wins for 'nothing works'; top-down for 'one app broken'. Either beats random: each layer you verify eliminates a class of causes.\n\nThe 7-question flow: (1) What exactly fails, for whom, since when? (2) Link? (light, ipconfig/ip addr shows address?) (3) Local? (ping gateway) (4) Routing? (ping past gateway, traceroute) (5) Name resolution? (nslookup) (6) Service? (Test-NetConnection port / telnet) (7) What changed? (updates, config, new device). Question 7 solves 50% of tickets alone.\n\nDivide and conquer: ping works but app fails = above L3. One VLAN fails = that VLAN's path. All sites fail = common element (core, firewall, ISP). Always compare against a known-good: 'does it work from my phone hotspot?' isolates the corporate network in 30 seconds."
},
{"title": "Wireshark: capture, filter, read",
"body": "Capture: pick the right interface, use capture filters (host x, port 53) to keep files small, stop early - a 10-second capture of the problem beats a 10-minute ocean. Promiscuous mode + SPAN/mirror port to see others' traffic; on your own machine you see your own.\n\nDisplay filters (the real skill): ip.addr==10.0.0.5, tcp.port==443, dns, dhcp, http, tcp.flags.syn==1, tcp.analysis.retransmission. Follow > TCP Stream rebuilds the conversation. IO Graphs show throughput/loss over time - a picture of 'slow'.\n\nReading: 3-way handshake present? (SYN with no SYN-ACK = server/firewall). Retransmissions (black/red) = loss. RST = refused/killed. DNS: query with no response = resolver issue. DHCP: discover with no offer = server/scope. TLS handshake failing after ClientHello = cert/cipher mismatch. Learn these five patterns and you read 80% of captures."
},
{"title": "Evidence-based incident documentation",
"body": "A network incident report: timeline (14:02 first report, 14:05 confirmed scope, 14:11 root cause, 14:20 fix, 14:35 verified), scope (who/what), evidence (traceroute output, capture excerpt with the smoking-gun packet numbers, log lines), root cause (one sentence), fix, and prevention (monitoring + config change with owner/date).\n\nPacket evidence discipline: note the capture filter, interface, and exact time; highlight frame numbers ('frames 142-148 show SYN with no SYN-ACK'); never share full captures with payloads externally (passwords/PII hide in packets - sanitize or summarize). Screenshots of the relevant 10 packets beat a 500MB pcap every time.\n\nThe debrief question that prevents repeats: 'What would have caught this in 60 seconds?' - usually a ping monitor, a DHCP scope alert, or a log rule. Every incident should produce exactly one monitoring improvement."
}
],
"cards": [
{"front": "Bottom-up vs top-down: when each?", "back": "Bottom-up: nothing works. Top-down: one app broken."},
{"front": "The 7-question flow (first 3)", "back": "What/who/when? Link? Local (ping gateway)?"},
{"front": "Wireshark: SYN with no SYN-ACK means?", "back": "Server not responding or firewall dropping - check service + path."},
{"front": "Display filter for retransmissions", "back": "tcp.analysis.retransmission."},
{"front": "DHCP discover, no offer: suspects?", "back": "Server down, scope exhausted, relay missing, L2 issue."},
{"front": "Fastest corporate-network isolation test", "back": "'Does it work from my phone hotspot?' - 30 seconds."},
{"front": "Why sanitize captures before sharing?", "back": "Passwords/PII hide in payloads; share excerpts, not full pcaps."},
{"front": "Every incident should produce what?", "back": "One monitoring improvement that would catch it in 60 seconds."}
],
"quiz": [
{"q": "All sites down simultaneously. First suspect?", "choices": ["Common element: core, firewall, ISP", "One user's PC", "A printer", "Wi-Fi channel"], "answer": 0, "index": 0, "explain": "Shared scope = shared dependency."},
{"q": "Capture shows repeated SYNs, no SYN-ACKs, to port 443. Meaning?", "choices": ["Server/firewall not completing handshake - check service and path", "DNS failure", "Success", "DHCP issue"], "answer": 0, "index": 0, "explain": "Handshake stalls at step 1: far end or middlebox."},
{"q": "Black/red retransmission storm in a capture indicates:", "choices": ["Packet loss on the path", "Normal operation", "Encryption", "VLAN hopping"], "answer": 0, "index": 0, "explain": "Retransmissions = segments not arriving."},
{"q": "Best first question for any network ticket?", "choices": ["What exactly fails, for whom, since when?", "What's your password?", "Have you tried Linux?", "Is it plugged in?"], "answer": 0, "index": 0, "explain": "Scope + timeline focuses everything after."},
{"q": "Wireshark IO graph is best for showing:", "choices": ["Throughput/loss over time - a picture of 'slow'", "Passwords", "MAC addresses", "CPU usage"], "answer": 0, "index": 0, "explain": "Graphs make patterns (drops, bursts) visible."},
{"q": "TLS fails right after ClientHello. Likely?", "choices": ["Cert/cipher mismatch", "DNS", "DHCP", "ARP"], "answer": 0, "index": 0, "explain": "Handshake dies at negotiation = crypto disagreement."},
{"q": "Capture filter vs display filter?", "choices": ["Capture: limits what's recorded. Display: limits what's shown.", "Same thing", "Display is faster", "Capture is for Wi-Fi only"], "answer": 0, "index": 0, "explain": "Capture filters keep files small; display filters analyze."},
{"q": "'What changed?' solves ~50% of tickets because:", "choices": ["Most outages follow a change (update, config, new device)", "Users lie", "Networks are random", "It's a trick question"], "answer": 0, "index": 0, "explain": "Change correlation is the highest-yield diagnostic question."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M30"],
"drills": [
{"id": "m10-drill-method", "title": "Methodology Drill",
"items": [
{"prompt": "'Nothing works' - approach?", "answer": "Bottom-up: link, IP, gateway, route, DNS, app", "explain": "Total failure = start at Layer 1."},
{"prompt": "'One app broken' - approach?", "answer": "Top-down: app, then down the stack", "explain": "Isolated app = start at Layer 7."},
{"prompt": "Filter: show only DNS traffic", "answer": "dns", "explain": "Protocol display filter."},
{"prompt": "Filter: traffic to/from 10.0.0.5", "answer": "ip.addr==10.0.0.5", "explain": "Bidirectional address filter."},
{"prompt": "Rebuild a web session", "answer": "Follow > TCP Stream", "explain": "Reconstructs the conversation."},
{"prompt": "Prove it wasn't the network", "answer": "Hotspot test + timeline + captures", "explain": "Known-good comparison isolates scope."}
]}
],
"handsOnLab": {
"id": "m10-lab",
"title": "Outage Simulation: run a full incident",
"brief": "Script three network failures in your lab; diagnose each with the methodology and write incident reports.",
"steps": [
"Failure 1: break DNS (point client at dead resolver). Diagnose with the 7-question flow; capture the failing queries in Wireshark.",
"Failure 2: block port 443 outbound (firewall rule). Diagnose: ping ok, handshake fails; find it in the capture.",
"Failure 3: exhaust the DHCP scope (shorten + fill). Diagnose via APIPA + scope stats.",
"For each: timeline, scope, evidence (frame numbers!), root cause, fix, prevention.",
"Write the '60-second monitor' for each: what alert would have caught it?",
"Present one incident as a 5-minute debrief."
],
"deliverable": "Three incident reports with packet evidence + three monitoring improvements + debrief recording.",
"checkpoint": "You run network incidents like a professional: method, evidence, timeline, prevention."
},
"mockTask": {"id": "m10-mock", "type": "choice",
"q": "Interview: 'The CEO's video calls freeze but email works. Walk me through it.'",
"choices": ["Top-down: app-specific -> check real-time traffic needs (jitter/loss), capture during a call, look for retransmissions/jitter, check Wi-Fi airtime and QoS, verify with wired test", "Reinstall Teams", "It's the ISP - escalate", "Buy a new laptop for the CEO"],
"answer": 0, "index": 0, "explain": "Real-time apps expose loss/jitter that email hides; measure, don't guess."},
"crossLinks": ["il04-networking", "il06-defensive"],
"videos": [],
"estimatedMinutes": 300,
"fastTrackEligible": True
}
]
