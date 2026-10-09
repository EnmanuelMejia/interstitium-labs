#!/usr/bin/env python3
"""
Topic hub page generator — 12 themed topic hubs + topics index.
Reuses site chrome (head from cinema/, pillnav from index.html, footer from cinema/).
"""
import os, re, html

DOCS = "/home/hatch/workspace/apex-audit/docs"
BC = "/home/hatch/workspace/cert-bootcamps/site/bootcamps"

TOPICS = [
 dict(slug="cybersecurity", theme="mr-robot", name="Cybersecurity",
      tag="Think like an attacker. Defend like an engineer.",
      desc="Zero trust, endpoint defense, SOC operations, pentesting, and secure engineering — from first principles to ThreatLocker mastery.",
      courses=["il-06-cybersecurity-secure-engineering","il-11-zero-trust-endpoint-defense",
               "il-24-threatlocker-assessment-prep-cbt","il-25-cybersecurity-professional-certificate",
               "il-27-it-infrastructure-specialist-threatlocker-mastery","il-29-threatlocker-ai-cybersecurity-mastery"],
      bcs=["acad-cyber","zero-trust","zerotrust","soc-analyst","secops-blue-team","pentest",
           "cissp","cism","sc-200","sc-300","comptia-security-plus","comptia-cyber",
           "tl-interview","tl-endpoint-ops","active-directory-defense","hackers-arise",
           "nsa-codebreaker","dod-8140","nice-framework","ai-agent-sec","ml-defense","security-graphs"],
      pdf="#security"),
 dict(slug="system-design", theme="cyberpunk", name="System Design",
      tag="Design systems that survive scale.",
      desc="Distributed systems, consensus, caching, load balancing, and architecture patterns — the engineering behind planet-scale software.",
      courses=["il-08-algorithms-compilers-distributed-formal","il-05-cloud-devsecops-platform-sre"],
      bcs=["sre-platform","sre-practices","platform-engineering","full-spectrum-dominance","alan-turing"],
      pdf="#system-design"),
 dict(slug="networking", theme="tron", name="Networking",
      tag="Packets in, understanding out.",
      desc="TCP/IP, DNS, routing, TLS, and modern network architecture — from the wire up to the cloud edge.",
      courses=["il-04-systems-linux-windows-networks"],
      bcs=["cisco-ccna","comptia-network-plus","az-700","systems-cs"],
      pdf="#networking"),
 dict(slug="cloud-devops", theme="steampunk", name="Cloud & DevOps",
      tag="Ship it. Scale it. Sleep at night.",
      desc="AWS, Azure, Kubernetes, Terraform, CI/CD, and SRE — production infrastructure done right.",
      courses=["il-05-cloud-devsecops-platform-sre","il-14-sre-devops-cloud-security-interview-prep",
               "il-19-multicloud-devops-ai-bootcamp","il-28-devsecops-cloud-infrastructure-mastery"],
      bcs=["acad-cloud","aws-saa","aws-dop","aws-clf","aws-cloud-practitioner-plus","az-104","az-305",
           "cka","ckad","kubernetes-sre","docker","terraform","iac-terraform-gitops","devops-zero-to-hire",
           "devsecops-mastery","git-devops","azure-developer","oracle-oci","k8s-associate","k8s-cka-exceed",
           "openshift","sre-practices","sre-platform","vault-consul","aws-soa","aws-scs","aws-data","aws-ml"],
      pdf="#cloud-&-devops"),
 dict(slug="ai-ml", theme="exmachina", name="AI & Machine Learning",
      tag="Machines that learn. Engineers who understand.",
      desc="Neural networks, transformers, LLMs, agents, and MLOps — from backprop to production AI systems.",
      courses=["il-12-ai-engineering","il-16-machine-learning-ai-engineering",
               "il-17-agentic-ai-engineering","il-07-data-engineering-analytics-ai"],
      bcs=["il12-ai-engineering","llm-engineering","nlp-engineering","nlp-advanced","deep-learning",
           "datascience-ml","neuroai","nvidia-ai","ai-lab","ai-product","alan-turing","ai-agent-sec"],
      pdf="#ai-ml"),
 dict(slug="data-eng", theme="oceandeep", name="Data Engineering",
      tag="Data is the current. Ride it.",
      desc="Pipelines, warehouses, streaming, and analytics — turn raw data into decisions.",
      courses=["il-07-data-engineering-analytics-ai","il-15-data-engineering-analytics-interview-prep",
               "il-26-data-analyst-certification-senior-mastery"],
      bcs=["acad-data","data-engineering","data-analyst","data-analyst-to-ml","data-science-certs",
           "dp-203","sql","mongodb","oracle-sql","oracle-db","aws-data"],
      pdf="#data-engineering"),
 dict(slug="programming", theme="hackers95", name="Programming",
      tag="Write code that matters.",
      desc="Languages, algorithms, and software craft — from Python to systems programming to interview mastery.",
      courses=["il-03-programming-language-forge","il-08-algorithms-compilers-distributed-formal",
               "il-13-software-engineering-interview-prep"],
      bcs=["acad-forge","python","python-systems","python-web","java","c-lang","cpp","dsa","dotnet",
           "spring","react-frontend","fullstack","android-interview","ios-interview","enochian-programming",
           "creative-code","fullstack-desk"],
      pdf="#programming-&-cs"),
 dict(slug="databases", theme="alexandria", name="Databases",
      tag="The library of all knowledge, queryable.",
      desc="SQL, NoSQL, indexing, transactions, and distributed data — the foundation everything stands on.",
      courses=["il-07-data-engineering-analytics-ai"],
      bcs=["sql","mongodb","oracle-sql","oracle-db"],
      pdf="#databases"),
 dict(slug="linux-systems", theme="industrial", name="Linux & Systems",
      tag="Own the machine.",
      desc="Linux internals, administration, virtualization, and bare-metal operations — RHEL-grade systems skill.",
      courses=["il-04-systems-linux-windows-networks"],
      bcs=["acad-systems","linux-essentials","rhcsa","rhce","windows-admin","m365","m365-endpoint-admin",
           "comptia-a-plus","comptia-core","comptia-infra","embedded-interview"],
      pdf="#linux-&-systems"),
 dict(slug="math", theme="sacredgeo", name="Mathematics",
      tag="The language the universe is written in.",
      desc="Discrete math, linear algebra, probability, and statistics — the prerequisite power behind all engineering.",
      courses=["il-02-mathematical-maturity-engine","il-20-mathematics"],
      bcs=["acad-math","aleks-ops-math","math-tech","quant-finance-math","quant-finance-ladder"],
      pdf="#mathematics"),
 dict(slug="web-dev", theme="vaporwave", name="Web Development",
      tag="Build for the open web.",
      desc="Frontend, backend, and full-stack web development — from React to APIs to deployment.",
      courses=["il-03-programming-language-forge"],
      bcs=["react-frontend","python-web","fullstack"],
      pdf="#web-&-mobile"),
 dict(slug="blockchain", theme="goldrush", name="Blockchain",
      tag="Trust, engineered.",
      desc="Distributed ledgers, smart contracts, and decentralized systems — from Bitcoin to frontier research.",
      courses=["il-23-frontier-knowledge"],
      bcs=["blockchain-dev"],
      pdf="#blockchain"),
]

def course_title(slug):
    import json
    p = os.path.join(DOCS, "university/data/courses", slug + ".json")
    try:
        return json.load(open(p)).get("title", slug)
    except Exception:
        return slug

def bc_exists(slug):
    return os.path.isdir(os.path.join(BC, slug))

# ---- extract chrome ----
cinema_head = open(os.path.join(DOCS, "cinema/index.html")).read().split("</head>")[0] + "</head>"
# pill nav block from index.html
idx = open(os.path.join(DOCS, "index.html")).read()
m = re.search(r'<!-- Floating pill nav -->.*?</nav>', idx, re.S)
pillnav = m.group(0)
# footer from cinema
cin = open(os.path.join(DOCS, "cinema/index.html")).read()
m2 = re.search(r'<footer class="il-footer-canonical">.*', cin, re.S)
footer = m2.group(0)

def head_for(title, desc, canon):
    h = cinema_head
    h = h.replace('<link rel="stylesheet" href="/assets/il-unified.css"/>',
                  '<link rel="stylesheet" href="/assets/il-unified.css"/>\n<link rel="stylesheet" href="/assets/il-topic-themes.css"/>', 1)
    h = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', h, count=1)
    h = re.sub(r'<meta name="description" content=".*?"',
               f'<meta name="description" content="{html.escape(desc)}"', h, count=1)
    h = re.sub(r'<link rel="canonical" href=".*?"',
               f'<link rel="canonical" href="{canon}"', h, count=1)
    h = re.sub(r'<meta property="og:title" content=".*?"',
               f'<meta property="og:title" content="{html.escape(title)}"', h, count=1)
    h = re.sub(r'<meta property="og:description" content=".*?"',
               f'<meta property="og:description" content="{html.escape(desc)}"', h, count=1)
    h = re.sub(r'<meta property="og:url" content=".*?"',
               f'<meta property="og:url" content="{canon}"', h, count=1)
    return h

def nav_for(active_slug=None):
    n = pillnav
    # add Topics link after Paths in desktop links
    n = n.replace('<a href="/paths/">Paths</a>',
                  '<a href="/paths/">Paths</a>\n      <a href="/topics/">Topics</a>', 1)
    # add to menu sheet (first occurrence area)
    n = n.replace('<a href="/paths/">Paths</a>\n          <a href="/paths/roles/">Role Tracks</a>',
                  '<a href="/paths/">Paths</a>\n          <a href="/topics/">Topics</a>\n          <a href="/paths/roles/">Role Tracks</a>', 1)
    return n

def hero_html(t):
    slug, theme = t["slug"], t["theme"]
    first_course = t["courses"][0] if t["courses"] else None
    cta1 = (f'<a class="il-btn il-btn--gold" href="/university/course?course={first_course}">Start learning</a>'
            if first_course else '<a class="il-btn il-btn--gold" href="/university/">Start learning</a>')
    return f'''<!-- Hero -->
<header class="il-hero" data-topic-theme="{theme}">
  <div class="il-hero__bg" aria-hidden="true">
    <video class="il-hero__video" autoplay muted loop playsinline preload="auto" poster="/assets/topics/{slug}-hero.jpg" disablepictureinpicture aria-hidden="true" tabindex="-1"><source src="/assets/topics/{slug}-hero.mp4" type="video/mp4"/></video>
  </div>
  <div class="il-hero__scrim" aria-hidden="true"></div>
  <div class="il-wrap">
    <p class="th-badge" style="margin-bottom:1rem">Topic Hub</p>
    <h1 class="il-h">{html.escape(t["name"])}</h1>
    <p class="il-hero__sub">{html.escape(t["tag"])} {html.escape(t["desc"])}</p>
    <div class="il-hero__cta">
      {cta1}
      <a class="il-btn il-btn--ghost" href="/pdf-library/{t["pdf"]}">Visual guides</a>
    </div>
    <p class="il-hero__motto">SCIENTIA OMNIA VINCIT</p>
    <p class="il-hero__caption" style="margin-top:.9rem;font-size:.68rem;letter-spacing:.05em;color:rgba(242,237,225,.55)">Background motion: the {html.escape(t["name"])} themed loop (muted, no audio).</p>
  </div>
</header>'''

def card_grid(items):
    out = ['<div class="il-grid">']
    for title, url, blurb in items:
        out.append(f'''<article class="th-card">
  <h3 style="margin:0 0 .4rem;font-size:1.05rem"><a href="{url}" style="color:inherit">{html.escape(title)}</a></h3>
  <p style="margin:0;font-size:.9rem;opacity:.85">{html.escape(blurb)}</p>
</article>''')
    out.append('</div>')
    return "\n".join(out)

def topic_page(t):
    slug = t["slug"]
    courses = [(course_title(c), f"/university/course?course={c}", "Full course — guided path, labs, and assessments.")
               for c in t["courses"]]
    bcs = [(b.replace("-", " ").title(), f"/bootcamps/{b}/", "Interactive certification prep bootcamp.")
           for b in t["bcs"] if bc_exists(b)][:12]
    sections = []
    if courses:
        sections.append(f'<section class="il-section"><div class="il-wrap"><h2 class="th-header">Courses</h2>{card_grid(courses)}</div></section>')
    if bcs:
        sections.append(f'<section class="il-section"><div class="il-wrap"><h2 class="th-header">Bootcamps</h2>{card_grid(bcs)}</div></section>')
    sections.append(f'''<section class="il-section"><div class="il-wrap"><h2 class="th-header">Media &amp; Guides</h2>
<div class="il-grid">
<article class="th-card"><h3 style="margin:0 0 .4rem;font-size:1.05rem"><a href="/pdf-library/{t["pdf"]}" style="color:inherit">Visual guides</a></h3><p style="margin:0;font-size:.9rem;opacity:.85">Byte-byte-go style animated guides for {html.escape(t["name"])}.</p></article>
<article class="th-card"><h3 style="margin:0 0 .4rem;font-size:1.05rem"><a href="/cinema/" style="color:inherit">Cinema</a></h3><p style="margin:0;font-size:.9rem;opacity:.85">Watch the cinematic reels.</p></article>
<article class="th-card"><h3 style="margin:0 0 .4rem;font-size:1.05rem"><a href="/noah/" style="color:inherit">Noah AI</a></h3><p style="margin:0;font-size:.9rem;opacity:.85">Train with the AI coach on {html.escape(t["name"])}.</p></article>
</div></div></section>''')
    body = f'''<body class="min-h-dvh bg-void text-paper" data-topic-theme="{t["theme"]}">
<a class="il-skip" href="#main">Skip to content</a>
{nav_for(slug)}
<nav class="il-breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li><a href="/topics/">Topics</a></li><li aria-current="page">{html.escape(t["name"])}</li></ol></nav>
{hero_html(t)}
<main id="main">
{chr(10).join(sections)}
</main>
{footer}
</body>
</html>'''
    h = head_for(f'{t["name"]} — Interstitium Labs', f'{t["tag"]} {t["desc"]}',
                 f'https://interstitiumlabs.dev/topics/{slug}/')
    return "<!DOCTYPE html>\n<html lang=\"en\" class=\"antialiased\">\n" + h + "\n" + body

def index_page():
    cards = []
    for t in TOPICS:
        n_bcs = sum(1 for b in t["bcs"] if bc_exists(b))
        cards.append(f'''<article class="th-card" data-topic-theme="{t["theme"]}">
  <div style="height:120px;border-radius:8px;margin:-0.25rem -0.5rem 0.9rem;background:url('/assets/topics/{t["slug"]}-hero.jpg') center/cover"></div>
  <h3 style="margin:0 0 .4rem;font-size:1.15rem"><a href="/topics/{t["slug"]}/" style="color:inherit">{html.escape(t["name"])}</a></h3>
  <p style="margin:0 0 .6rem;font-size:.9rem;opacity:.85">{html.escape(t["tag"])}</p>
  <p style="margin:0;font-size:.78rem;opacity:.65">{len(t["courses"])} courses · {n_bcs} bootcamps</p>
</article>''')
    body = f'''<body class="min-h-dvh bg-void text-paper">
<a class="il-skip" href="#main">Skip to content</a>
{nav_for()}
<nav class="il-breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">Topics</li></ol></nav>
<header class="il-hero">
  <div class="il-hero__bg" aria-hidden="true">
    <video class="il-hero__video" autoplay muted loop playsinline preload="auto" poster="/assets/chrome/hero-cinematic-poster.jpg" disablepictureinpicture aria-hidden="true" tabindex="-1"><source src="/assets/chrome/hero-cinematic-loop.mp4" type="video/mp4"/><img src="/assets/chrome/sigil-decor.webp" alt="" decoding="async"/></video>
  </div>
  <div class="il-hero__scrim" aria-hidden="true"></div>
  <div class="il-wrap">
    <h1 class="il-h">Twelve worlds. One OS.</h1>
    <p class="il-hero__sub">Every topic gets its own cinematic hub — themed courses, bootcamps, videos, and visual guides.</p>
    <p class="il-hero__motto">SCIENTIA OMNIA VINCIT</p>
  </div>
</header>
<main id="main">
<section class="il-section"><div class="il-wrap">
<div class="il-grid">
{chr(10).join(cards)}
</div>
</div></section>
</main>
{footer}
</body>
</html>'''
    h = head_for("Topics — Interstitium Labs",
                 "Twelve themed topic hubs: cybersecurity, system design, networking, cloud, AI, data, programming, databases, Linux, math, web, blockchain.",
                 "https://interstitiumlabs.dev/topics/")
    return "<!DOCTYPE html>\n<html lang=\"en\" class=\"antialiased\">\n" + h + "\n" + body

def main():
    base = os.path.join(DOCS, "topics")
    for t in TOPICS:
        d = os.path.join(base, t["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(topic_page(t))
        print("wrote", t["slug"])
    os.makedirs(base, exist_ok=True)
    open(os.path.join(base, "index.html"), "w").write(index_page())
    print("wrote topics/index")
    # patch homepage nav: add Topics to pillnav links + menu sheet
    p = os.path.join(DOCS, "index.html")
    s = open(p).read()
    if 'href="/topics/"' not in s:
        s = s.replace('<a href="/paths/">Paths</a>\n      <a href="/paths/roles/">Role Tracks</a>',
                      '<a href="/paths/">Paths</a>\n      <a href="/topics/">Topics</a>\n      <a href="/paths/roles/">Role Tracks</a>', 1)
        s = s.replace('<a href="/paths/">Paths</a>\n          <a href="/paths/roles/">Role Tracks</a>',
                      '<a href="/paths/">Paths</a>\n          <a href="/topics/">Topics</a>\n          <a href="/paths/roles/">Role Tracks</a>', 1)
        open(p, "w").write(s)
        print("patched index.html nav")
    else:
        print("index.html nav already has Topics")

if __name__ == "__main__":
    main()
