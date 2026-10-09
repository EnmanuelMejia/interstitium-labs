#!/usr/bin/env python3
"""Generate original SVG concept/architecture diagrams for bootcamp domains
lacking media[] coverage (template/embed 1000% expansion, 2026-10-09).

Writes: ~/workspace/cert-bootcamps/site/bootcamps/<slug>/assets/diagrams/<domain_id>.svg
Emits:  manifest JSON -> diagram-manifest-20261009.json (media[] entries for wiring step)

All diagrams: 600x400 viewBox, dark-theme, self-contained, original work.
"""
import json, os, html

BASE = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps")
HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "diagram-manifest-20261009.json")

def esc(s):
    return html.escape(str(s), quote=True)

def open_svg(title, desc):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400" role="img">\n'
        '  <title>%s</title>\n  <desc>%s</desc>\n'
        '  <defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#7d8fb0"/></marker></defs>\n'
        '  <rect x="0" y="0" width="600" height="400" fill="#0b1220"/>\n'
        % (esc(title), esc(desc)))

CLOSE = '</svg>\n'

def heading(s, title, kicker=None):
    s.append('  <text x="28" y="34" font-family="sans-serif" font-size="19" font-weight="700" fill="#f2f6fc">%s</text>' % esc(title))
    if kicker:
        s.append('  <text x="28" y="54" font-family="sans-serif" font-size="11" fill="#7f93b3" letter-spacing="2">%s</text>' % esc(kicker.upper()))

def box(s, x, y, w, h, label, sub=None, accent="#3b82f6", fs=12.5):
    s.append('  <rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="#141d33" stroke="%s" stroke-width="2"/>' % (x, y, w, h, accent))
    lines = [label] + ([sub] if sub else [])
    cy = y + h / 2 - (len(lines) - 1) * 9
    for i, ln in enumerate(lines):
        fill = "#eef3fa" if i == 0 else "#9fb0c8"
        weight = ' font-weight="700"' if i == 0 else ""
        fsize = fs if i == 0 else 10.5
        s.append('  <text x="%d" y="%d" text-anchor="middle" font-family="sans-serif" font-size="%s"%s fill="%s">%s</text>'
                 % (x + w / 2, cy + i * 18 + 4, fsize, weight, fill, esc(ln)))

def circle_node(s, cx, cy, r, label, sub=None, accent="#3b82f6"):
    s.append('  <circle cx="%d" cy="%d" r="%d" fill="#141d33" stroke="%s" stroke-width="2"/>' % (cx, cy, r, accent))
    lines = [label] + ([sub] if sub else [])
    oy = cy - (len(lines) - 1) * 9
    for i, ln in enumerate(lines):
        fill = "#eef3fa" if i == 0 else "#9fb0c8"
        weight = ' font-weight="700"' if i == 0 else ""
        s.append('  <text x="%d" y="%d" text-anchor="middle" font-family="sans-serif" font-size="12"%s fill="%s">%s</text>'
                 % (cx, oy + i * 17 + 4, weight, fill, esc(ln)))

def edge(s, x1, y1, x2, y2, label=None, dashed=False):
    dash = ' stroke-dasharray="6,5"' if dashed else ""
    s.append('  <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#7d8fb0" stroke-width="1.8" marker-end="url(#arr)"%s/>'
             % (x1, y1, x2, y2, dash))
    if label:
        s.append('  <text x="%d" y="%d" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#8fa3c4">%s</text>'
                 % ((x1 + x2) / 2, (y1 + y2) / 2 - 6, esc(label)))

def plain_line(s, x1, y1, x2, y2, dashed=False):
    dash = ' stroke-dasharray="5,5"' if dashed else ""
    s.append('  <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#55688c" stroke-width="1.5"%s/>' % (x1, y1, x2, y2, dash))

# ---------------- layouts ----------------
def hub(title, desc, center, sats, accent, kicker=None):
    s = [open_svg(title, desc)]
    heading(s, title, kicker)
    import math
    cx, cy, rx, ry = 300, 212, 200, 118
    for i, (label, sub) in enumerate(sats):
        a = math.radians(-90 + i * 360 / len(sats))
        sx, sy = cx + rx * math.cos(a), cy + ry * math.sin(a)
        plain_line(s, cx, cy, sx, sy)
    box(s, cx - 85, cy - 30, 170, 60, center[0], center[1] if len(center) > 1 else None, accent, fs=13)
    for i, (label, sub) in enumerate(sats):
        a = math.radians(-90 + i * 360 / len(sats))
        sx, sy = cx + rx * math.cos(a), cy + ry * math.sin(a)
        box(s, sx - 64, sy - 24, 128, 48, label, sub, "#3f587e", fs=11.5)
    s.append(CLOSE)
    return "".join(s)

def layers(title, desc, items, accent, kicker=None):
    s = [open_svg(title, desc)]
    heading(s, title, kicker)
    n = len(items)
    h = 44 if n <= 5 else 36
    gap = 14 if n <= 5 else 8
    y = 74
    for i, (label, sub) in enumerate(items):
        s.append('  <rect x="56" y="%d" width="488" height="%d" rx="9" fill="#141d33" stroke="#2b3a5c" stroke-width="1.6"/>' % (y, h))
        s.append('  <rect x="56" y="%d" width="7" height="%d" fill="%s"/>' % (y, h, accent))
        s.append('  <text x="78" y="%d" font-family="sans-serif" font-size="13.5" font-weight="700" fill="#eef3fa">%s</text>' % (y + h / 2 - (4 if sub else -2), esc(label)))
        if sub:
            s.append('  <text x="78" y="%d" font-family="sans-serif" font-size="11" fill="#9fb0c8">%s</text>' % (y + h / 2 + 14, esc(sub)))
        if i < n - 1:
            s.append('  <line x1="300" y1="%d" x2="300" y2="%d" stroke="#7d8fb0" stroke-width="1.8" marker-end="url(#arr)"/>' % (y + h + 1, y + h + gap - 1))
        y += h + gap
    s.append(CLOSE)
    return "".join(s)

def flow(title, desc, steps, accent, kicker=None):
    s = [open_svg(title, desc)]
    heading(s, title, kicker)
    n = len(steps)
    if n <= 4:
        w = (520 - (n - 1) * 34) / n
        y = 160
        for i, (label, sub) in enumerate(steps):
            x = 40 + i * (w + 34)
            box(s, x, y, w, 92, label, sub, accent, fs=11.5)
            if i < n - 1:
                edge(s, x + w + 2, y + 46, x + w + 32, y + 46)
    else:
        h = min(52, (300 - (n - 1) * 14) / n)
        y = 72
        for i, (label, sub) in enumerate(steps):
            box(s, 170, y, 260, h, label, sub, accent, fs=12)
            if i < n - 1:
                edge(s, 300, y + h + 1, 300, y + h + 13)
            y += h + 14
    s.append(CLOSE)
    return "".join(s)

def grid(title, desc, cards, accent, kicker=None):
    s = [open_svg(title, desc)]
    heading(s, title, kicker)
    for i, (label, sub) in enumerate(cards):
        r, c = divmod(i, 3)
        x, y = 40 + c * 180, 76 + r * 150
        box(s, x, y, 160, 128, label, sub, accent, fs=12.5)
    s.append(CLOSE)
    return "".join(s)

def cycle(title, desc, steps, accent, kicker=None):
    s = [open_svg(title, desc)]
    heading(s, title, kicker)
    import math
    n = len(steps)
    cx, cy, r = 300, 216, 122
    pts = []
    for i in range(n):
        a = math.radians(-90 + i * 360 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        sx, sy = x1 + dx / d * 56, y1 + dy / d * 56
        ex, ey = x2 - dx / d * 62, y2 - dy / d * 62
        edge(s, sx, sy, ex, ey)
    for (x, y), (label, sub) in zip(pts, steps):
        box(s, x - 62, y - 26, 124, 52, label, sub, accent, fs=11.5)
    s.append(CLOSE)
    return "".join(s)

def topo(title, desc, nodes, edges, accent, kicker=None):
    s = [open_svg(title, desc)]
    heading(s, title, kicker)
    for (i, j, label) in edges:
        n1, n2 = nodes[i], nodes[j]
        x1, y1 = n1["x"] + n1["w"] / 2, n1["y"] + n1["h"] / 2
        x2, y2 = n2["x"] + n2["w"] / 2, n2["y"] + n2["h"] / 2
        import math
        d = math.hypot(x2 - x1, y2 - y1) or 1
        sx, sy = x1 + (x2 - x1) / d * (n1["w"] / 2 + 2), y1 + (y2 - y1) / d * (n1["h"] / 2 + 2)
        ex, ey = x2 - (x2 - x1) / d * (n2["w"] / 2 + 6), y2 - (y2 - y1) / d * (n2["h"] / 2 + 6)
        edge(s, sx, sy, ex, ey, label)
    for nd in nodes:
        if nd.get("shape") == "circle":
            circle_node(s, nd["x"] + nd["w"] / 2, nd["y"] + nd["h"] / 2, nd["w"] / 2,
                        nd["label"], nd.get("sub"), nd.get("accent", accent))
        else:
            box(s, nd["x"], nd["y"], nd["w"], nd["h"], nd["label"], nd.get("sub"),
                nd.get("accent", accent), fs=nd.get("fs", 11.5))
    s.append(CLOSE)
    return "".join(s)

def tree(title, desc, root, children, accent, kicker=None):
    s = [open_svg(title, desc)]
    heading(s, title, kicker)
    n = len(children)
    box(s, 230, 70, 140, 56, root[0], root[1] if len(root) > 1 else None, accent, fs=13)
    cw = min(150, 540 / n)
    y2 = 190
    for i, (cl, cs, gcs) in enumerate(children):
        x = 30 + i * (560 / n) + (560 / n - cw) / 2
        plain_line(s, 300, 126, x + cw / 2, y2)
        box(s, x, y2, cw, 60, cl, cs, "#3f587e", fs=11.5)
        if gcs:
            gh = 34
            gy = y2 + 60 + 12
            bus = gy - 8
            plain_line(s, x + cw / 2, y2 + 60, x + cw / 2, bus)
            gw = cw / len(gcs)
            plain_line(s, x + gw / 2, bus, x + cw - gw / 2, bus)
            for j, g in enumerate(gcs):
                gx = x + j * gw
                plain_line(s, gx + gw / 2, bus, gx + gw / 2, gy)
                s.append('  <rect x="%d" y="%d" width="%d" height="%d" rx="7" fill="#101829" stroke="#33456b" stroke-width="1.4"/>'
                         % (gx + 2, gy, gw - 4, gh))
                s.append('  <text x="%d" y="%d" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#c4d2e8">%s</text>'
                         % (gx + gw / 2, gy + gh / 2 + 3.5, esc(g)))
    s.append(CLOSE)
    return "".join(s)

def neural(title, desc, accent, kicker=None):
    s = [open_svg(title, desc)]
    heading(s, title, kicker)
    import math
    layerspec = [("Input", 3, 110), ("Hidden 1", 5, 240), ("Hidden 2", 5, 360), ("Output", 2, 490)]
    pts = []
    for name, cnt, x in layerspec:
        col = []
        for i in range(cnt):
            y = 216 + (i - (cnt - 1) / 2) * 52
            col.append((x, y))
        pts.append((name, col))
    for a in range(len(pts) - 1):
        for (x1, y1) in pts[a][1]:
            for (x2, y2) in pts[a + 1][1]:
                s.append('  <line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#2c3d61" stroke-width="1"/>' % (x1, y1, x2, y2))
    for name, col in pts:
        for (x, y) in col:
            s.append('  <circle cx="%d" cy="%d" r="15" fill="#141d33" stroke="%s" stroke-width="2"/>' % (x, y, accent))
        s.append('  <text x="%d" y="%d" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="700" fill="#9fb0c8">%s</text>' % (col[0][0], 356, esc(name)))
    s.append('  <text x="300" y="386" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#7f93b3">Forward pass: weighted sums + activation; training adjusts weights via backpropagation.</text>')
    s.append(CLOSE)
    return "".join(s)

SPECS = []
def spec(slug, domain_id, layout, title, caption, payload, alt=None):
    SPECS.append({"slug": slug, "domain_id": domain_id, "layout": layout,
                  "title": title, "caption": caption,
                  "alt": alt or (title + ". Diagram."),
                  "payload": payload})

# ================= SPEC PART 1: acad-*, active-directory, adaptive, ai-lab, turing, aleks, android, aws, ccna, comptia =================
R = "#e5484d"
spec("acad-career","acad-career","hub","The career system: skills in, offers out",
 "Six moving parts turn skills into signed offers: portfolio proves, resume filters, network opens doors, interviews convert, offers compare, growth compounds.",
 (("Career","system"),[("Portfolio","proof of work"),("Resume","ATS filter"),("Networking","warm intros"),("Interviews","conversion"),("Offers","compare"),("Growth","compound")]), alt="Hub diagram: Career system at center with Portfolio, Resume, Networking, Interviews, Offers, Growth around it.")
spec("acad-cloud","acad-cloud","layers","Cloud stack: five layers of the shared-responsibility model",
 "Every cloud workload rests on five layers; you own more of the lower layers in IaaS and less in SaaS.",
 [("Edge & CDN","cache close to users"),("Compute","VMs and containers"),("Storage","object and block"),("Networking","VPCs and routing"),("Identity & security","who can touch what")],)
spec("acad-command","acad-command","flow","The command cycle: intent to adaptation",
 "Command is a loop, not a moment: set intent, plan, direct, monitor the result, adapt the plan.",
 [("Intent","commander's goal"),("Plan","course of action"),("Direct","issue orders"),("Monitor","track effects"),("Adapt","revise plan")],)
spec("acad-cyber","acad-cyber","layers","Cyber defense in depth: five concentric layers",
 "Attackers must defeat every layer; defenders only need one layer to catch them.",
 [("Perimeter","firewalls and gateways"),("Network","segmentation and IDS"),("Endpoint","EDR and hardening"),("Application","secure code and WAF"),("Data","encryption and DLP")],)
spec("acad-data","acad-data","flow","The data pipeline: raw events to decisions",
 "Data work is a pipeline: collect events, store them durably, transform into models, analyze, serve decisions.",
 [("Collect","events and logs"),("Store","warehouse / lake"),("Transform","clean and model"),("Analyze","statistics"),("Serve","dashboards")],)
spec("acad-forge","acad-forge","layers","The forge: from idea to hardened ship",
 "Forge discipline: ideate small, build, test against reality, harden, then ship.",
 [("Ideate","problem first"),("Build","smallest slice"),("Test","real users"),("Harden","security pass"),("Ship","production")],)
spec("acad-hermetica","acad-hermetica","hub","The Hermetic corpus and its six branches",
 "Hermetica studies the Corpus Hermeticum and the traditions that grew from it across two millennia.",
 (("Hermetic","corpus"),[("Alchemy","transmutation"),("Astrology","celestial order"),("Kabbalah","tree of life"),("Theurgy","divine work"),("Tarot","arcana"),("Rosicrucian","manifestos")]), alt="Hub diagram of Hermetic traditions around the Hermetic corpus.")
spec("acad-math","acad-math","grid","The six pillars of working mathematics",
 "Six pillars carry every technical track: algebra manipulates, calculus measures change, linear algebra structures data, probability and statistics reason under uncertainty, discrete math counts structures.",
 [("Algebra","equations"),("Calculus","change"),("Linear algebra","vectors"),("Probability","chance"),("Statistics","inference"),("Discrete math","structures")],)
spec("acad-systems","acad-systems","hub","Systems thinking: six lenses on any system",
 "Systems thinking reads feedback, stocks, emergence, boundaries, delays, and leverage points instead of isolated parts.",
 (("Systems","thinking"),[("Feedback","loops"),("Stocks & flows","accumulation"),("Emergence","whole > parts"),("Boundaries","scope"),("Delays","lag effects"),("Leverage","intervention")]), alt="Hub diagram of six systems-thinking lenses.")
spec("acad-theory","acad-theory","grid","Theory: six formal foundations",
 "Six formal foundations underlie computing: what is computable, what information is, what is hard, what follows, what machines recognize, what stays secret.",
 [("Computation","Turing"),("Information","Shannon"),("Complexity","P vs NP"),("Logic","proof"),("Automata","machines"),("Cryptography","secrets")],)

spec("active-directory-defense","active-directory-defense","tree","AD forest anatomy: the unit you must defend",
 "The forest is the security boundary. Defend tier 0 first: domain controllers and privileged accounts decide every breach.",
 (("Forest","security boundary"),
  [("Domain: corp","Kerberos realm",["Workstations","Servers","Admins"]),
   ("Domain: branch","child domain",["Users","Laptops"]),
   ("Tier 0","privileged access",["DCs","AD admins"])]),)
spec("active-directory-defense","adfind-recon-hunting","flow","Hunting AdFind-style recon: from enumeration to response",
 "Attackers enumerate with LDAP queries before they strike; hunters baseline normal AD shape and investigate deviations.",
 [("Enumerate","AdFind / LDAP"),("Baseline","normal AD shape"),("Detect","anomalies"),("Hunt","hypothesis"),("Respond","contain")],)

spec("adaptive-foundations","adaptive-foundations","cycle","Adaptive learning loop",
 "Adaptive study is a loop: assess where you are, adapt the plan, practice deliberately, measure, repeat.",
 [("Assess","diagnose gaps"),("Adapt","tune plan"),("Practice","deliberate reps"),("Measure","track mastery"),("Repeat","next cycle")],)

spec("ai-lab","ai-lab","flow","Engineering around the model: the AI lab loop",
 "AI engineering is prompt, call, tools, evaluate, iterate — the model is a component, not the product.",
 [("Prompt","design"),("Model","call API"),("Tools","function use"),("Evaluate","score output"),("Iterate","improve")],)

spec("alan-turing","alan-turing","hub","Alan Turing (1912-1954): six contributions",
 "Turing defined computation, broke Enigma traffic, designed early computers, asked whether machines think, and modeled biological pattern formation.",
 (("Turing","1912-1954"),[("Turing machine","1936"),("Bombe","Enigma"),("ACE","computer design"),("Turing test","machine thought"),("Morphogenesis","patterns"),("Church-Turing","thesis")]), alt="Hub diagram of Alan Turing's six major contributions.")

spec("aleks-ops-math","aleks-ops-math","grid","Operations math: six skill blocks",
 "Six blocks carry operations math: whole numbers, fractions, ratios, percents, measurement, and word problems that combine them.",
 [("Whole numbers","arithmetic"),("Fractions","parts"),("Ratios","comparison"),("Percents","per hundred"),("Measurement","units"),("Word problems","applied")],)

A = "#3ddc84"
spec("android-interview","android-kotlin-core","grid","Kotlin core: six interview pillars",
 "Kotlin interviews probe null safety, data and sealed classes, extensions, lambdas, and generics.",
 [("Null safety","? and !!"),("Data classes","value types"),("Sealed classes","restricted hierarchies"),("Extensions","add functions"),("Lambdas","closures"),("Generics","type params")],)
spec("android-interview","android-framework","hub","Android framework: six moving parts",
 "The framework is activities and fragments with lifecycles, intents for navigation, services for background work, receivers for broadcasts, and permissions guarding it all.",
 (("Android","framework"),[("Activities","screens"),("Fragments","reusable UI"),("Intents","navigation"),("Services","background"),("Receivers","broadcasts"),("Permissions","guards")]), alt="Hub diagram of Android framework components.")
spec("android-interview","android-coroutines","flow","Coroutines: from launch to collect",
 "Coroutines suspend instead of blocking: launch a scope, suspend in functions, dispatch threads, expose Flow, collect results.",
 [("launch","start scope"),("suspend","non-blocking"),("Dispatchers","threads"),("Flow","stream"),("collect","consume")],)
spec("android-interview","android-persistence","layers","Android persistence stack",
 "UI state flows down: repository abstracts Room over SQLite, with DataStore and files for preferences and blobs.",
 [("UI state","ViewModel"),("Repository","single source"),("Room","ORM"),("SQLite","on-device DB"),("DataStore / files","prefs & blobs")],)
spec("android-interview","android-architecture","layers","MVVM on Android: unidirectional data flow",
 "MVVM keeps UI dumb: the view observes the ViewModel, which asks the repository, which reads data sources.",
 [("UI layer","observes state"),("ViewModel","holds state"),("Repository","mediates"),("Data sources","network / DB")],)
spec("android-interview","android-guided-build","flow","Guided build: scaffold to test",
 "Build in slices: scaffold the project, compose the UI, wire state, connect data, then test.",
 [("Scaffold","project setup"),("UI","Compose screens"),("State","ViewModel"),("Data","repository"),("Test","unit + UI")],)
spec("android-interview","android-mock-circuit","cycle","Mock interview circuit",
 "The circuit runs warm-up, coding, system design, behavioral, then debrief — the same loop as a real onsite.",
 [("Warm-up","introductions"),("Coding","live problem"),("System design","architecture"),("Behavioral","stories"),("Debrief","feedback")],)

spec("aws-cloud-practitioner-plus","aws-cloud-practitioner-plus","flow","Cloud migration: the six-phase path",
 "Migrations move through discover, assess, plan, migrate, validate, operate — strategy before servers.",
 [("Discover","inventory"),("Assess","readiness"),("Plan","wave plan"),("Migrate","move"),("Validate","test"),("Operate","run")],)

C = "#1ba0d7"
spec("cisco-ccna","fundamentals","layers","The OSI model: five layers that move your packet",
 "OSI in five: applications speak, transport segments, network routes, data link frames, physical transmits bits.",
 [("Application","HTTP, DNS"),("Transport","TCP, UDP"),("Network","IP, routing"),("Data link","Ethernet, MAC"),("Physical","bits, media")],)
spec("cisco-ccna","access","topo","Campus access: hosts to the wire",
 "Access switches connect endpoints on access ports; uplinks trunk VLANs toward the router.",
 {"nodes":[
   {"x":36,"y":120,"w":100,"h":56,"label":"PC-A","sub":"VLAN 10"},
   {"x":36,"y":230,"w":100,"h":56,"label":"PC-B","sub":"VLAN 20"},
   {"x":220,"y":170,"w":140,"h":66,"label":"Access switch","sub":"L2"},
   {"x":420,"y":150,"w":90,"h":90,"label":"Router","sub":"gateway","shape":"circle"},
   {"x":520,"y":178,"w":64,"h":44,"label":"WAN","fs":10}],
  "edges":[(0,2,"access"),(1,2,"access"),(2,3,"trunk"),(3,4,"route")]},)
spec("cisco-ccna","ip-connectivity","topo","IP connectivity: routing between networks",
 "Routers forward by longest-prefix match; each hop consults its routing table to pick the exit interface.",
 {"nodes":[
   {"x":24,"y":200,"w":96,"h":56,"label":"PC","sub":"192.168.1.10"},
   {"x":180,"y":180,"w":96,"h":96,"label":"R1","sub":"routing table","shape":"circle"},
   {"x":340,"y":180,"w":96,"h":96,"label":"R2","sub":"routing table","shape":"circle"},
   {"x":496,"y":200,"w":88,"h":56,"label":"Server","sub":"172.16.0.5"}],
  "edges":[(0,1,"192.168.1.0/24"),(1,2,"10.0.0.0/30"),(2,3,"172.16.0.0/24")]},)
spec("cisco-ccna","ip-services","grid","IP services: six protocols that keep networks usable",
 "DHCP assigns, DNS resolves, NAT translates, NTP synchronizes, QoS prioritizes, SNMP monitors.",
 [("DHCP","addressing"),("DNS","names"),("NAT","translation"),("NTP","time"),("QoS","priority"),("SNMP","monitoring")],)
spec("cisco-ccna","sec-fund","layers","Network security fundamentals: five controls",
 "Harden devices, control access, encrypt transit, monitor everything, write it down as policy.",
 [("Device hardening","disable unused"),("Access control","AAA"),("VPN & encryption","secure transit"),("Monitoring","logs, NetFlow"),("Policy","written rules")],)
spec("cisco-ccna","automation","flow","Network automation: intent to telemetry",
 "Automation turns intent into config: a controller pushes via NETCONF/REST, devices report telemetry back.",
 [("Intent","desired state"),("Controller","orchestrate"),("NETCONF/REST","push config"),("Device","enforce"),("Telemetry","verify")],)

P = "#e8442e"
spec("comptia-a-plus","hardware","grid","A+ hardware: six component families",
 "Know the six families cold: CPU computes, RAM stages, storage persists, motherboard connects, PSU powers, peripherals extend.",
 [("CPU","compute"),("RAM","working memory"),("Storage","SSD / HDD"),("Motherboard","backbone"),("PSU","power"),("Peripherals","I/O")],)
spec("comptia-a-plus","networking","topo","SOHO network: from ISP to printer",
 "A SOHO chain: ISP modem hands off to the router, which serves the switch, PCs, and the shared printer.",
 {"nodes":[
   {"x":30,"y":190,"w":92,"h":56,"label":"ISP modem","fs":10.5},
   {"x":170,"y":180,"w":100,"h":76,"label":"Router","sub":"DHCP/NAT","shape":"circle"},
   {"x":320,"y":186,"w":104,"h":64,"label":"Switch","sub":"L2"},
   {"x":470,"y":120,"w":100,"h":52,"label":"PC","fs":11},
   {"x":470,"y":230,"w":100,"h":52,"label":"Printer","fs":11}],
  "edges":[(0,1,"WAN"),(1,2,"LAN"),(2,3,""),(2,4,"")]},)
spec("comptia-a-plus","operating-systems","layers","OS anatomy: four layers from silicon to app",
 "Hardware is abstracted upward: the kernel manages resources, system services expose APIs, applications consume them.",
 [("Hardware","CPU, RAM, disk"),("Kernel","scheduling, drivers"),("System services","APIs"),("Applications","user software")],)
spec("comptia-a-plus","security","hub","A+ security: six control families",
 "Entry-level security is malware defense, access control, encryption, backups, physical security, and best practices.",
 (("Security","A+"),[("Malware","AV / EDR"),("Access control","least privilege"),("Encryption","data at rest"),("Backups","3-2-1"),("Physical","locks"),("Best practice","updates")]), alt="Hub diagram of six A+ security control families.")
spec("comptia-a-plus","troubleshooting","flow","CompTIA six-step troubleshooting",
 "CompTIA's method: identify, theorize, test, plan, implement, then verify and document.",
 [("Identify","gather info"),("Theorize","probable cause"),("Test","validate theory"),("Plan","action + effects"),("Implement","apply fix"),("Verify","document")] ,)
spec("comptia-a-plus","procedures","cycle","Operational procedures cycle",
 "Procedures are a cycle: safety first, communicate professionally, document, control changes, stay compliant, dispose properly.",
 [("Safety","ESD, power"),("Professionalism","communicate"),("Documentation","ticket notes"),("Change control","approvals"),("Compliance","licensing"),("Disposal","e-waste")],)

N = "#2e9de8"
spec("comptia-network-plus","concepts","layers","Networking concepts: the layered model",
 "Packets travel down the stack to send and up the stack to receive; each layer adds its own header.",
 [("Application","user data"),("Transport","segments"),("Network","packets, IP"),("Data link","frames, MAC"),("Physical","signals")],)
spec("comptia-network-plus","implementation","topo","Enterprise implementation: three-tier with VLANs",
 "Three tiers: core routes fast, distribution enforces policy, access connects users on separate VLANs.",
 {"nodes":[
   {"x":250,"y":80,"w":110,"h":56,"label":"Core","sub":"fast routing"},
   {"x":120,"y":180,"w":110,"h":56,"label":"Distribution","sub":"policy","fs":10.5},
   {"x":380,"y":180,"w":110,"h":56,"label":"Distribution","sub":"policy","fs":10.5},
   {"x":60,"y":290,"w":120,"h":56,"label":"Access: VLAN 10","fs":10.5},
   {"x":240,"y":290,"w":120,"h":56,"label":"Access: VLAN 20","fs":10.5},
   {"x":420,"y":290,"w":120,"h":56,"label":"Access: VLAN 30","fs":10.5}],
  "edges":[(0,1,""),(0,2,""),(1,3,"trunk"),(1,4,"trunk"),(2,4,"trunk"),(2,5,"trunk")]},)
spec("comptia-network-plus","operations","flow","Network operations: the run loop",
 "Operations is a run loop: monitor baselines, analyze deviations, optimize, maintain.",
 [("Monitor","baselines"),("Analyze","deviations"),("Optimize","tune"),("Maintain","patch")] ,)
spec("comptia-network-plus","net-security","layers","Network security: five control layers",
 "Segment the network, filter at the firewall, watch with IDS, encrypt remote access, secure wireless, govern with policy.",
 [("Segmentation","VLANs, zones"),("Firewall & IDS","filter, detect"),("VPN","encrypted remote"),("Wireless security","WPA3, rogue APs"),("Policy","acceptable use")],)
spec("comptia-network-plus","net-troubleshoot","flow","Network troubleshooting: seven steps",
 "Wired method: identify symptoms, theorize, test, plan, implement, verify, document.",
 [("Identify","symptoms"),("Theorize","cause"),("Test","hypothesis"),("Plan","roll back ready"),("Implement","change"),("Verify","full function"),("Document","lessons")] ,)

S = "#f0a832"
spec("comptia-security-plus","concepts","grid","Security concepts: six foundations",
 "Foundations: CIA triad, AAA, zero trust, cryptography, risk, and the controls that enforce them.",
 [("CIA triad","C-I-A"),("AAA","auth*3"),("Zero trust","never trust"),("Cryptography","ciphers"),("Risk","likelihood x impact"),("Controls","preventive...")],)
spec("comptia-security-plus","threats","hub","Threat landscape: six attack families",
 "Threats arrive as malware, social engineering, network attacks, application exploits, wireless attacks, and physical access.",
 (("Threats","landscape"),[("Malware","payloads"),("Social eng.","phishing"),("Network","MitM, DoS"),("Application","injection"),("Wireless","evil twin"),("Physical","tailgating")]), alt="Hub diagram of six threat families.")
spec("comptia-security-plus","architecture","layers","Security architecture: defense in depth",
 "Six concentric controls: physical barriers, perimeter filtering, network segmentation, hardened hosts, secure applications, encrypted data.",
 [("Physical","badges, locks"),("Perimeter","firewall"),("Network","segmentation"),("Host","hardening"),("Application","SDLC"),("Data","encryption")],)
spec("comptia-security-plus","operations","flow","Incident response lifecycle",
 "Respond in order: detect, analyze scope, contain, eradicate, recover — then lessons learned.",
 [("Detect","alert"),("Analyze","scope"),("Contain","isolate"),("Eradicate","remove"),("Recover","restore")],)
spec("comptia-security-plus","governance","grid","Governance: six program pillars",
 "Programs run on policies, risk management, compliance, privacy, audits, and training.",
 [("Policies","written rules"),("Risk mgmt","assess, treat"),("Compliance","frameworks"),("Privacy","data rights"),("Audit","verify"),("Training","awareness")],)

# ================= SPEC PART 2: cybernetics .. ios-interview =================
spec("cybernetics","cybernetics","cycle","The cybernetic loop: sense, compare, act",
 "Cybernetics is the science of control through feedback: sense the state, compare to the goal, act, observe the effect.",
 [("Sense","measure state"),("Compare","vs goal"),("Act","intervene"),("Feedback","observe effect"),("Steer","correct")] ,)

spec("data-analyst-to-ml","data-analyst-to-ml","flow","Analyst to ML: the skill ladder",
 "Analysts climb to ML through SQL, statistics, Python, modeling, then deployment.",
 [("SQL","query"),("Statistics","inference"),("Python","pandas"),("Modeling","regression+"),("Deploy","serve")] ,)

spec("data-science-certs","data-science-certs","hub","Data science: six cert-ready pillars",
 "Cert prep spans statistics, programming, machine learning, visualization, domain knowledge, and communication.",
 (("Data science","pillars"),[("Statistics","inference"),("Programming","Python/R"),("ML","models"),("Visualization","charts"),("Domain","context"),("Communication","story")]), alt="Hub diagram of six data science pillars.")

spec("deep-learning","deep-learning","neural","Neural network: input to output",
 "A feedforward network: inputs flow through two hidden layers to outputs; training tunes every weight by backpropagation.",
 None, alt="Neural network diagram: 3 input neurons, two hidden layers of 5, 2 outputs, fully connected.")

spec("deep-work","deep-work","flow","Deep work day: the time-blocking flow",
 "Attention is scheduled like money: shut down yesterday, plan, block deep hours, batch shallow work, review.",
 [("Shutdown","close loops"),("Plan","time blocks"),("Deep block","90+ min"),("Shallow batch","email/admin"),("Review","score day")] ,)

D = "#e5484d"
spec("devops-zero-to-hire","devops-zero-to-hire","flow","CI/CD pipeline: commit to production",
 "DevOps hiring signal is a working pipeline: code, build, test, release, deploy, monitor.",
 [("Code","commit"),("Build","artifact"),("Test","automated"),("Release","versioned"),("Deploy","rollout"),("Monitor","observe")] ,)
spec("devops-zero-to-hire","devops-zero-to-hire-d2","cycle","DevOps infinity loop: plan to monitor",
 "The infinity loop: plan, code, build, test, release, deploy, operate, monitor — then plan again.",
 [("Plan","backlog"),("Code","commit"),("Build","CI"),("Test","QA"),("Release","CD"),("Deploy","prod"),("Operate","run"),("Monitor","metrics")] ,)

spec("devsecops-mastery","devsecops-mastery","flow","Shift-left pipeline: security at every gate",
 "DevSecOps embeds checks in the pipeline: SAST on commit, SCA on build, DAST on deploy, monitoring always.",
 [("Commit","SAST"),("Build","SCA"),("Deploy","DAST"),("Runtime","RASP"),("Monitor","SIEM")] ,)

spec("edward-bernays","edward-bernays","hub","Bernays: engineering consent",
 "Bernays (1891-1995) founded public relations on group psychology: symbols, third-party authorities, and media channels shape opinion.",
 (("Bernays","1891-1995"),[("Group psych.","crowds"),("Symbols","meaning"),("Authorities","third party"),("Media","channels"),("Crystallizing","1923 book"),("Propaganda","1928 book")]), alt="Hub diagram of Edward Bernays' public-relations methods.")

E = "#f59e0b"
spec("electrician-apprentice","electrician-apprentice","hub","Electrical foundations: six apprentice pillars",
 "The etA entrance rests on Ohm's law relationships — voltage, current, resistance, power — plus safety and code.",
 (("Electrical","foundations"),[("Voltage","push"),("Current","flow"),("Resistance","opposition"),("Power","V x I"),("Safety","LOTO, PPE"),("NEC","code")]), alt="Hub diagram of six electrical apprentice pillars.")

M = "#e8a33d"
spec("embedded-interview","embedded-c-memory","layers","MCU memory map: where your bytes live",
 "Firmware lives in flash (.text), constants in flash, initialized data copied to RAM, BSS zeroed, heap grows up, stack grows down.",
 [("Flash: .text","code"),("Flash: constants","rodata"),("RAM: .data","initialized"),("RAM: .bss","zeroed"),("Heap","malloc, grows up"),("Stack","frames, grows down")],)
spec("embedded-interview","embedded-rtos","hub","RTOS: six primitives",
 "Real-time kernels schedule tasks and synchronize them with queues, semaphores, mutexes, timers, and ISRs.",
 (("RTOS","kernel"),[("Scheduler","priorities"),("Tasks","threads"),("Queues","messages"),("Semaphores","signaling"),("Timers","ticks"),("ISRs","interrupts")]), alt="Hub diagram of six RTOS primitives.")
spec("embedded-interview","embedded-drivers","flow","Driver stack: app to silicon",
 "Drivers abstract silicon: the app calls the HAL, the driver programs registers, the peripheral acts.",
 [("App","logic"),("HAL","abstract API"),("Driver","register code"),("Registers","MMIO"),("Peripheral","hardware")] ,)
spec("embedded-interview","embedded-concurrency","cycle","Interrupt-driven concurrency loop",
 "Concurrency without threads: the interrupt fires, the ISR flags, the task processes, the system sleeps.",
 [("Interrupt","event"),("ISR","flag it"),("Queue","defer work"),("Task","process"),("Sleep","low power")] ,)
spec("embedded-interview","embedded-debugging","flow","Embedded debugging: six disciplined steps",
 "Debug hardware like software: reproduce, instrument, trace, find root cause, fix, verify on target.",
 [("Reproduce","reliable trigger"),("Instrument","GPIO/log"),("Trace","logic analyzer"),("Root cause","5 whys"),("Fix","minimal change"),("Verify","on target")] ,)
spec("embedded-interview","embedded-capstone","topo","Capstone: wireless sensor node",
 "A sensor node: the sensor feeds the MCU, the radio links the gateway, the gateway reaches the cloud.",
 {"nodes":[
   {"x":30,"y":190,"w":96,"h":60,"label":"Sensor","sub":"I2C/SPI","fs":11},
   {"x":170,"y":180,"w":110,"h":80,"label":"MCU","sub":"firmware","shape":"circle"},
   {"x":330,"y":196,"w":96,"h":48,"label":"Radio","sub":"LoRa/BLE","fs":10.5},
   {"x":466,"y":190,"w":104,"h":60,"label":"Gateway","sub":"to cloud","fs":11}],
  "edges":[(0,1,"sample"),(1,2,"UART/SPI"),(2,3,"wireless")]},)
spec("embedded-interview","embedded-mock-circuit","cycle","Mock interview circuit",
 "Embedded onsites loop warm-up, C/debugging, systems design, behavioral, debrief.",
 [("Warm-up","background"),("C / debug","live code"),("Systems","design"),("Behavioral","stories"),("Debrief","feedback")] ,)

spec("enochian-programming","enochian-programming","grid","Enochian system: six study areas",
 "Dee and Kelley's received system: the Calls, the Great Table, the Aethyrs, sigils, scrying practice, and the underlying ciphers.",
 [("Calls","19 keys"),("Great Table","watchtowers"),("Aethyrs","30 levels"),("Sigils","seals"),("Scrying","vision"),("Ciphers","letter tables")],)

spec("entrepreneurship","entrepreneurship","cycle","The lean loop: build, measure, learn",
 "Entrepreneurship is validated learning: build the smallest thing, measure real behavior, learn, repeat.",
 [("Build","MVP"),("Measure","metrics"),("Learn","insight"),("Pivot?","decide"),("Repeat","next loop")] ,)

spec("fde-training","fde-training","layers","Full-disk encryption: five protective layers",
 "FDE stacks: data encrypted at rest, volumes unlocked at boot, keys sealed in the TPM, policies pushed by MDM.",
 [("Data","encrypted at rest"),("Volume","AES-XTS"),("Boot auth","PIN / key"),("TPM","sealed keys"),("Policy","MDM enforcement")],)

spec("frontier-path","frontier-path","flow","The frontier path: five stages",
 "The path runs foundations, core skills, specialization, building proof, then launch.",
 [("Foundations","first principles"),("Core skills","daily reps"),("Specialize","deep track"),("Build","portfolio proof"),("Launch","ship")] ,)

spec("fullstack-desk","fullstack-desk","layers","Service desk: the ticket journey",
 "Tickets flow down the desk: user reports, ticketing triages, L1/L2/L3 resolve, the knowledge base remembers.",
 [("User","reports issue"),("Ticketing","intake"),("Triage","prioritize"),("L1 / L2 / L3","resolve"),("Knowledge base","document")] ,)

H = "#14b8a6"
spec("humanmetrics","humanmetrics","grid","Humanmetrics: four dichotomies",
 "The assessment sorts four preferences: energy source, information style, decision basis, and lifestyle orientation.",
 [("E / I","energy"),("S / N","information"),("T / F","decisions"),("J / P","lifestyle")],)

spec("iac-terraform-gitops","iac-terraform-gitops","flow","Terraform GitOps: PR to applied",
 "GitOps for infra: code the change, open a PR, plan shows the diff, apply converges, state records truth, drift detection watches.",
 [("Code","HCL"),("PR","review"),("Plan","diff"),("Apply","converge"),("State","truth"),("Drift","detect")] ,)
spec("iac-terraform-gitops","iac-terraform-gitops-d2","flow","ArgoCD GitOps: push to healthy",
 "Push to git, ArgoCD syncs, Kubernetes reconciles, health checks gate, rollback is a revert.",
 [("Push","git"),("Sync","ArgoCD"),("Reconcile","K8s"),("Health","checks"),("Rollback","revert")] ,)

spec("il12-ai-engineering","il12-ai-engineering","hub","AI engineering: six production concerns",
 "Shipping AI means prompts, retrieval, agents, evals, deployment, and guardrails — not just the model.",
 (("AI eng.","production"),[("Prompts","contracts"),("RAG","grounding"),("Agents","tool loops"),("Evals","regression"),("Deploy","serve"),("Guardrails","safety")]), alt="Hub diagram of six AI engineering production concerns.")

I = "#0a84ff"
spec("ios-interview","ios-swift-core","grid","Swift core: six interview pillars",
 "Swift interviews probe optionals, protocols, generics, closures, value semantics, and ARC.",
 [("Optionals","? and !"),("Protocols","contracts"),("Generics","type params"),("Closures","captures"),("Struct vs class","value semantics"),("ARC","memory")],)
spec("ios-interview","ios-ui-frameworks","hub","iOS UI: UIKit and SwiftUI",
 "iOS UI spans UIKit lifecycles and SwiftUI state, with Auto Layout, navigation, lists, and animation over both.",
 (("iOS UI","frameworks"),[("UIKit","view controllers"),("SwiftUI","declarative"),("Auto Layout","constraints"),("Navigation","stacks"),("Lists","cells/rows"),("Animation","motion")]), alt="Hub diagram of iOS UI framework topics.")
spec("ios-interview","ios-concurrency","flow","Swift concurrency: task to UI update",
 "Structured concurrency: start a task, await suspension points, isolate state in actors, hop to MainActor for UI.",
 [("Task","start"),("await","suspend"),("Actor","isolate"),("MainActor","UI hop"),("Update","render")] ,)
spec("ios-interview","ios-persistence","layers","iOS persistence stack",
 "Repository abstracts Core Data or SwiftData over SQLite, with files and Keychain for blobs and secrets.",
 [("UI state","@State"),("Repository","single source"),("Core Data","object graph"),("SQLite","store"),("Files / Keychain","blobs, secrets")],)
spec("ios-interview","ios-architecture","layers","MVVM on iOS: unidirectional flow",
 "Views observe view models, which drive repositories, which read services.",
 [("View","SwiftUI/UIKit"),("ViewModel","state"),("Repository","mediates"),("Services","network/DB")],)
spec("ios-interview","ios-guided-build","flow","Guided build: scaffold to test",
 "Slice the build: scaffold, compose UI, wire state, connect data, test.",
 [("Scaffold","Xcode project"),("UI","screens"),("State","view models"),("Data","services"),("Test","XCTest")] ,)
spec("ios-interview","ios-mock-circuit","cycle","Mock interview circuit",
 "iOS onsites loop warm-up, coding, architecture, behavioral, debrief.",
 [("Warm-up","background"),("Coding","live problem"),("Architecture","app design"),("Behavioral","stories"),("Debrief","feedback")] ,)

# ================= SPEC PART 3: isc2-cc .. zero-trust =================
Q = "#35c48d"
spec("isc2-cc","principles","grid","Security principles: six ideas everything rests on",
 "First principles: confidentiality, integrity, availability, least privilege, defense in depth, and risk thinking.",
 [("Confidentiality","secrecy"),("Integrity","accuracy"),("Availability","uptime"),("Least privilege","minimum access"),("Defense in depth","layers"),("Risk","manage it")],)
spec("isc2-cc","bcdr","flow","Continuity & response: from BIA to lessons",
 "Resilience is planned: assess impact, write the plan, test it, respond, recover, learn.",
 [("BIA","impact"),("Plan","BCP/DRP"),("Test","exercise"),("Respond","incident"),("Recover","restore"),("Learn","improve")] ,)
spec("isc2-cc","access-control","hub","Access control: the four A's plus models",
 "Access control identifies, authenticates, authorizes, and audits — enforced through DAC, MAC, or RBAC models.",
 (("Access","control"),[("Identify","claim"),("Authenticate","prove"),("Authorize","permit"),("Account","audit"),("RBAC","roles"),("DAC/MAC","owner/system")]), alt="Hub diagram of access-control concepts.")
spec("isc2-cc","network-security","layers","Network security: five controls",
 "Secure the wire: segment, filter, encrypt remote, harden wireless, govern with policy.",
 [("Segmentation","zones"),("Firewalls","filter"),("VPN","remote encrypt"),("Wireless","WPA3"),("Policy","rules")],)
spec("isc2-cc","sec-operations","flow","Security operations: the SOC loop",
 "SOC work loops: monitor, triage, investigate, contain, report.",
 [("Monitor","SIEM"),("Triage","prioritize"),("Investigate","scope"),("Contain","isolate"),("Report","document")] ,)

spec("k8s-cka-exceed","k8s-cka-exceed","hub","Kubernetes control plane: six components",
 "Advanced administration starts at the control plane: API server, etcd, scheduler, controller manager, kubelet, and the network/storage plugins.",
 (("Kubernetes","control plane"),[("API server","front door"),("etcd","state"),("Scheduler","placement"),("Controllers","reconcile"),("kubelet","node agent"),("CNI / CSI","net/storage")]), alt="Hub diagram of Kubernetes control-plane components.")
spec("k8s-cka-exceed","k8s-cka-exceed-d2","layers","Kubernetes security (CKS): six hardening layers",
 "Harden bottom-up: trusted images, pod security, network policy, RBAC, sealed secrets, runtime detection.",
 [("Images","scan & sign"),("Pod security","standards"),("NetworkPolicy","microsegment"),("RBAC","least privilege"),("Secrets","sealed"),("Runtime","detect")] ,)

spec("kubernetes-sre","kubernetes-sre","hub","SRE on Kubernetes: six practices",
 "SRE makes reliability a feature: SLIs, SLOs, error budgets, automation, incident response, capacity planning.",
 (("SRE","reliability"),[("SLIs","measure"),("SLOs","targets"),("Error budgets","risk"),("Automation","toil < 50%"),("Incidents","blameless"),("Capacity","plan")]), alt="Hub diagram of six SRE practices.")
spec("kubernetes-sre","kubernetes-sre-d2","cycle","Reliability practice loop",
 "Practice loops: define the SLO, measure SLIs, spend the budget deliberately, respond to incidents, improve.",
 [("Define SLO","target"),("Measure","SLIs"),("Budget","spend"),("Respond","incidents"),("Improve","postmortem")] ,)

T = "#0078d4"
spec("m365-endpoint-admin","deploy","flow","Windows client deployment: procure to validate",
 "Modern deployment: procure, Autopilot-provision, enroll in Intune, push configuration, validate compliance.",
 [("Procure","hardware"),("Autopilot","zero-touch"),("Enroll","Intune"),("Configure","profiles"),("Validate","compliance")] ,)
spec("m365-endpoint-admin","identity","hub","Entra ID: six identity controls",
 "Identity is the perimeter: users and groups, MFA, Conditional Access, PIM for admins, SSO for apps.",
 (("Entra ID","identity"),[("Users","accounts"),("Groups","membership"),("MFA","phishing-resistant"),("Cond. Access","policy"),("PIM","just-in-time"),("SSO","apps")]), alt="Hub diagram of six Entra ID identity controls.")
spec("m365-endpoint-admin","manage-devices","flow","Device lifecycle: enroll to retire",
 "Manage the fleet: enroll, check compliance, push config, protect with Defender, retire cleanly.",
 [("Enroll","Intune"),("Compliance","policies"),("Configure","baselines"),("Protect","Defender"),("Retire","wipe")] ,)
spec("m365-endpoint-admin","apps","flow","App management: package to monitor",
 "Apps flow: package, assign to groups, deploy, update on a ring schedule, monitor installs.",
 [("Package","wrap"),("Assign","groups"),("Deploy","push"),("Update","rings"),("Monitor","install state")] ,)

spec("neuroai","neuroai","hub","NeuroAI: six brain principles in silicon",
 "NeuroAI ports brain principles — neurons, plasticity, attention, memory systems, predictive coding, neuromorphic hardware — into computing.",
 (("NeuroAI","brain x machine"),[("Neurons","units"),("Plasticity","learning"),("Attention","selection"),("Memory","systems"),("Predictive","coding"),("Neuromorphic","chips")]), alt="Hub diagram of six NeuroAI brain principles.")

spec("nlp-advanced","nlp-advanced","flow","Transformer pipeline: tokens to evaluation",
 "Advanced NLP runs tokenize, embed, attend, generate, evaluate — the transformer stack end to end.",
 [("Tokenize","subwords"),("Embed","vectors"),("Attend","self-attention"),("Generate","decode"),("Evaluate","benchmarks")] ,)
spec("nlp-engineering","nlp-engineering","flow","NLP engineering: corpus to serving",
 "Production NLP: curate the corpus, preprocess, train or fine-tune, evaluate rigorously, serve with monitoring.",
 [("Corpus","curate"),("Preprocess","clean"),("Train","fine-tune"),("Evaluate","metrics"),("Serve","monitor")] ,)

spec("occult-esoteric","occult-esoteric","hub","Esoteric traditions: eight currents",
 "Eight currents of Western esotericism: Kabbalah, Hermeticism, alchemy, astrology, tarot, Rosicrucianism, Theosophy, and Enochian magic.",
 (("Esoteric","traditions"),[("Kabbalah","tree of life"),("Hermeticism","corpus"),("Alchemy","transmutation"),("Astrology","celestial"),("Tarot","arcana"),("Rosicrucian","manifestos"),("Theosophy","wisdom"),("Enochian","angelic")]), alt="Hub diagram of eight esoteric traditions.")

spec("philosophy","philosophy","grid","Philosophy: six branches",
 "Six branches: metaphysics asks what is, epistemology what we know, ethics what is right, logic what follows, aesthetics what is beautiful, political philosophy how we live together.",
 [("Metaphysics","being"),("Epistemology","knowledge"),("Ethics","right action"),("Logic","valid inference"),("Aesthetics","beauty"),("Political","justice")],)

spec("platform-engineering","platform-engineering","layers","Internal developer platform: five layers",
 "Platforms abstract upward: developers meet a portal, backed by CI/CD, IaC, Kubernetes, and cloud.",
 [("Developer portal","self-service"),("CI/CD","delivery"),("IaC","environments"),("Kubernetes","runtime"),("Cloud","substrate")],)

spec("python-systems","python-systems","hub","Python for systems: six toolkits",
 "Systems Python leans on subprocess, sockets, filesystem APIs, threading/asyncio, packaging, and profiling.",
 (("Python","systems"),[("Subprocess","processes"),("Sockets","network"),("Filesystem","os/shutil"),("Async","asyncio"),("Packaging","wheels"),("Profiling","cProfile")]), alt="Hub diagram of six Python systems toolkits.")

spec("quant-finance-ladder","quant-finance-ladder","flow","Quant ladder: math to live trading",
 "The ladder climbs math, statistics, programming, markets, strategies, then live trading with risk controls.",
 [("Math","foundations"),("Statistics","inference"),("Programming","Python/C++"),("Markets","microstructure"),("Strategies","backtest"),("Live","risk-managed")] ,)
spec("quant-finance-math","quant-finance-math","grid","Quant math: six toolkits",
 "Quantitative finance runs on calculus, linear algebra, probability, stochastic processes, optimization, and time series.",
 [("Calculus","change"),("Linear algebra","matrices"),("Probability","measure"),("Stochastic","random processes"),("Optimization","extrema"),("Time series","sequences")],)

spec("quantum","quantum","hub","Quantum computing: the qubit and beyond",
 "Quantum computing: qubits in superposition, entanglement as resource, gates as operations, algorithms like Shor and Grover, error correction, and the post-quantum crypto transition.",
 (("Qubit","quantum bit"),[("Superposition","0 and 1"),("Entanglement","correlation"),("Gates","unitary ops"),("Algorithms","Shor, Grover"),("Error corr.","logical qubits"),("PQC","crypto future")]), alt="Hub diagram of quantum computing concepts around the qubit.")

spec("roles-library","roles-library","grid","IT roles library: six career lanes",
 "Six lanes to compare: help desk, SOC analyst, cloud engineer, data analyst, DevOps, network admin — duties, skills, and certs side by side.",
 [("Help desk","support"),("SOC analyst","defend"),("Cloud engineer","build"),("Data analyst","insights"),("DevOps","deliver"),("Network admin","connect")],)

spec("secops-blue-team","secops-blue-team","flow","Blue team operations: harden to hunt",
 "Blue teams harden first, then monitor, detect, respond, and hunt proactively.",
 [("Harden","baselines"),("Monitor","telemetry"),("Detect","alerts"),("Respond","contain"),("Hunt","hypothesis")] ,)
spec("secops-blue-team","exposed-portal-initial-access","flow","Ransomware path: exposed portal to encryption",
 "A common ransomware path: an exposed portal falls to credential attacks, giving initial access, lateral movement, then encryption.",
 [("Exposed portal","internet-facing"),("Credential attack","stuffing/spray"),("Initial access","foothold"),("Lateral move","spread"),("Encrypt","impact")] ,)

spec("security-graphs","security-graphs","topo","Security graph: entities and relationships",
 "Graph-powered defense links users, hosts, IPs, and files; attack paths are traversals across these relationships.",
 {"nodes":[
   {"x":60,"y":90,"w":110,"h":52,"label":"User","sub":"alice@corp"},
   {"x":250,"y":70,"w":110,"h":52,"label":"Host","sub":"WS-042"},
   {"x":420,"y":90,"w":110,"h":52,"label":"IP","sub":"203.0.113.7"},
   {"x":150,"y":240,"w":110,"h":52,"label":"File","sub":"payload.exe","fs":10.5},
   {"x":360,"y":240,"w":120,"h":52,"label":"Domain","sub":"evil.example","fs":10.5}],
  "edges":[(0,1,"LOGGED_IN"),(1,2,"CONN_TO"),(1,3,"WROTE"),(2,4,"RESOLVES"),(3,4,"BEACONS")],
  },)

spec("sre-practices","sre-practices","hub","SRE practices: six disciplines",
 "SRE disciplines: SLIs that measure, SLOs that promise, error budgets that permit risk, blameless postmortems that teach, automation that removes toil, capacity planning that stays ahead.",
 (("SRE","practices"),[("SLIs","indicators"),("SLOs","objectives"),("Error budgets","policy"),("Postmortems","blameless"),("Automation","no toil"),("Capacity","forecast")]), alt="Hub diagram of six SRE disciplines.")

spec("study-protocol","study-protocol","cycle","The deep work study protocol",
 "Study in loops: preview the terrain, focus deeply, recall from memory, space repetitions, review weekly.",
 [("Preview","survey"),("Focus","deep block"),("Recall","active"),("Space","intervals"),("Review","weekly")] ,)
spec("study-protocol","sequences","flow","Lesson sequences: gated progression",
 "Sequences gate progress: master A, unlock B, master B, unlock C — no skipping the foundation.",
 [("Sequence A","foundations"),("Gate","mastery check"),("Sequence B","core"),("Gate","mastery check"),("Sequence C","advanced")] ,)

spec("vendor-map","vendor-map","grid","Vendor landscape: six categories",
 "Map the market by category: cloud platforms, security vendors, identity providers, DevOps tooling, data platforms, endpoint suites.",
 [("Cloud","hyperscalers"),("Security","detection"),("Identity","SSO/MFA"),("DevOps","CI/CD"),("Data","warehouse"),("Endpoint","EDR")],)

spec("windows-admin","windows-admin","hub","Windows administration: six domains",
 "Windows admins live in AD and Group Policy, PowerShell, services, storage, networking, and security baselines.",
 (("Windows","admin"),[("AD / GPO","directory"),("PowerShell","automation"),("Services","daemons"),("Storage","disks"),("Networking","TCP/IP"),("Security","baselines")]), alt="Hub diagram of six Windows administration domains.")

spec("zero-trust","zero-trust","layers","Zero trust: five pillars (IL-11)",
 "IL-11 zero trust verifies explicitly: identity, device, network, application, data — never trust, always verify.",
 [("Identity","verify who"),("Device","healthy"),("Network","microsegment"),("Application","least privilege"),("Data","classify, encrypt")],)
spec("zero-trust","zerotrust","hub","Zero trust architecture: six principles",
 "Assume breach, verify explicitly, grant least privilege, microsegment, monitor continuously, encrypt everything.",
 (("Zero trust","never trust"),[("Verify identity","explicit"),("Least privilege","JIT"),("Assume breach","blast radius"),("Microsegment","zones"),("Monitor","continuous"),("Encrypt","everywhere")]), alt="Hub diagram of six zero-trust principles.")


def main():
    accents = {}
    for sp in SPECS:
        d = json.load(open(os.path.join(BASE, sp["slug"], "content.json")))
        accents.setdefault(sp["slug"], d.get("accent") or "#3b82f6")
    manifest = []
    for sp in SPECS:
        slug, did = sp["slug"], sp["domain_id"]
        accent = accents[slug]
        layout, payload = sp["layout"], sp["payload"]
        title = sp["title"]
        desc = sp["caption"]
        if layout == "hub":
            svg = hub(title, desc, payload[0], payload[1], accent, kicker=slug.replace("-", " "))
        elif layout == "layers":
            svg = layers(title, desc, payload, accent, kicker=slug.replace("-", " "))
        elif layout == "flow":
            svg = flow(title, desc, payload, accent, kicker=slug.replace("-", " "))
        elif layout == "grid":
            svg = grid(title, desc, payload, accent, kicker=slug.replace("-", " "))
        elif layout == "cycle":
            svg = cycle(title, desc, payload, accent, kicker=slug.replace("-", " "))
        elif layout == "topo":
            svg = topo(title, desc, payload["nodes"], payload["edges"], accent, kicker=slug.replace("-", " "))
        elif layout == "tree":
            svg = tree(title, desc, payload[0], payload[1], accent, kicker=slug.replace("-", " "))
        elif layout == "neural":
            svg = neural(title, desc, accent, kicker=slug.replace("-", " "))
        else:
            raise ValueError("bad layout " + layout)
        outdir = os.path.join(BASE, slug, "assets", "diagrams")
        os.makedirs(outdir, exist_ok=True)
        fname = did + ".svg"
        with open(os.path.join(outdir, fname), "w") as f:
            f.write(svg)
        manifest.append({
            "slug": slug,
            "entry": {
                "id": did,
                "kind": "diagram",
                "title": title,
                "svg": "assets/diagrams/" + fname,
                "lesson_ref": "c-" + did,
                "caption": sp["caption"],
                "alt": sp["alt"],
            },
        })
    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=1)
        f.write("\n")
    print("generated:", len(manifest), "diagrams")
    print("manifest:", MANIFEST)

if __name__ == "__main__":
    main()
