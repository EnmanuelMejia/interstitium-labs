"""Batch 1: System Design PDFs — Load Balancing, Caching/CDN, Microservices."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


def pdf_load_balancing(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Load Balancing\nVisual Guide",
               "How traffic gets distributed across servers\nfor scale, speed, and survival.",
               "System Design", None); pg += 1

    # Step 1: the problem
    y = section_header(c, 1, 6, "The Problem: One Server Can't Handle It All",
                       "A single server is a single point of failure — and a bottleneck.")
    box(c, 226, 380, 160, 90, BOX_RED, "Web Server", "CPU 100% — overloaded")
    arrow(c, 306, 560, 306, 475, color=RED, label="10,000 req/s")
    note(c, 72, 280, 468, "One server receiving all traffic: slow responses, crashes under load, zero fault tolerance.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 2: add the load balancer
    y = section_header(c, 2, 6, "Insert a Load Balancer",
                       "A reverse proxy in front that spreads requests across N servers.")
    box(c, 226, 480, 160, 70, BOX_BLUE, "Load Balancer", "distributes traffic")
    arrow(c, 306, 640, 306, 555, color=ACCENT, label="10,000 req/s")
    for i, bx in enumerate([106, 226, 346]):
        box(c, bx, 300, 100, 70, BOX_GREEN, f"Server {i+1}", "~3.3k req/s")
        arrow(c, 306, 478, bx + 50, 372, color=GREEN)
    note(c, 72, 200, 468, "Each backend now handles a fraction. Add servers to scale horizontally.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 3: algorithms
    y = section_header(c, 3, 6, "Distribution Algorithms",
                       "How the balancer picks the next server.")
    algos = [("Round Robin", "1 → 2 → 3 → 1 → 2 → 3 …", BOX_BLUE),
             ("Least Connections", "Send to the server with fewest active conns", BOX_GREEN),
             ("IP Hash", "Same client → same server (sticky sessions)", BOX_ORANGE),
             ("Weighted", "Bigger servers get proportionally more traffic", BOX_TEAL)]
    yy = y
    for name, desc, fill in algos:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=12)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    # Step 4: health checks
    y = section_header(c, 4, 6, "Health Checks: Route Around Failure",
                       "The balancer probes backends and stops sending traffic to dead ones.")
    box(c, 226, 480, 160, 70, BOX_BLUE, "Load Balancer", "health checker")
    box(c, 106, 300, 100, 70, BOX_GREEN, "Server 1", "healthy ✓")
    box(c, 256, 300, 100, 70, BOX_RED, "Server 2", "DOWN ✗")
    box(c, 406, 300, 100, 70, BOX_GREEN, "Server 3", "healthy ✓")
    arrow(c, 270, 478, 156, 372, color=GREEN)
    arrow(c, 342, 478, 456, 372, color=GREEN)
    c.setStrokeColor(RED); c.setLineWidth(2); c.setDash(4, 3)
    c.line(306, 478, 306, 372); c.setDash()
    note(c, 72, 200, 468, "Failed probes remove Server 2 from rotation automatically. Traffic keeps flowing.")
    footer(c, pg); c.showPage(); pg += 1

    # Step 5: layers
    y = section_header(c, 5, 6, "L4 vs L7 Load Balancing",
                       "Two layers, different superpowers.")
    box(c, 72, y - 60, 225, 120, BOX_BLUE, "Layer 4", "TCP/UDP — fast, dumb", font_size=13)
    box(c, 315, y - 60, 225, 120, BOX_GREEN, "Layer 7", "HTTP — smart routing", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    l4 = ["Routes by IP + port", "No request inspection", "Very high throughput", "Example: NLB, HAProxy TCP"]
    l7 = ["Routes by URL, header, cookie", "TLS termination, rewrites", "Content-based rules", "Example: ALB, nginx, Envoy"]
    yy = y - 90
    for t in l4:
        c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 90
    for t in l7:
        c.drawString(331, yy, "• " + t); yy -= 18
    footer(c, pg); c.showPage(); pg += 1

    # Step 6: global
    y = section_header(c, 6, 6, "Going Global: DNS + Anycast",
                       "Multiple regions, each with its own balancer tier.")
    box(c, 72, 480, 120, 60, BOX_ORANGE, "US-East", "LB + servers")
    box(c, 246, 480, 120, 60, BOX_ORANGE, "EU-West", "LB + servers")
    box(c, 420, 480, 120, 60, BOX_ORANGE, "AP-South", "LB + servers")
    box(c, 226, 330, 160, 60, BOX_BLUE, "Global DNS / Anycast", "routes to nearest")
    for bx in [132, 306, 480]:
        arrow(c, 306, 328, bx, 478, color=ACCENT)
    arrow(c, 306, 560, 306, 392, color=ACCENT, label="user request")
    note(c, 72, 230, 468, "Global load balancing sends each user to the closest healthy region — lower latency, disaster resilience.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Load Balancing — Remember",
                 ["A load balancer spreads traffic so no single server is a bottleneck or single point of failure.",
                  "Algorithms: round robin (simple), least connections (dynamic), IP hash (sticky), weighted (heterogeneous).",
                  "Health checks automatically route around dead backends.",
                  "L4 is fast packet routing; L7 understands HTTP and routes on content.",
                  "Global LB (DNS/anycast) directs users to the nearest healthy region."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_caching_cdn(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Caching & CDNs\nVisual Guide",
               "Serve it once, serve it fast — everywhere.\nHow caches cut latency and cost.",
               "System Design", None); pg += 1

    y = section_header(c, 1, 6, "The Problem: Every Request Hits Origin",
                       "Without caching, each request travels the full path and recomputes everything.")
    box(c, 106, 400, 110, 70, BOX_BLUE, "User", "browser")
    box(c, 396, 400, 110, 70, BOX_RED, "Origin", "database + app")
    arrow(c, 220, 435, 392, 435, color=RED, label="every request")
    arrow(c, 392, 415, 220, 415, color=RED, label="slow response")
    note(c, 72, 290, 468, "Origin does redundant work per request. Latency = distance + compute, every single time.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Cache-Aside: Check the Cache First",
                       "The classic pattern — look it up before you compute it.")
    box(c, 72, 480, 120, 60, BOX_BLUE, "App", "")
    box(c, 246, 480, 120, 60, BOX_GREEN, "Cache", "Redis / Memcached")
    box(c, 420, 480, 120, 60, BOX_ORANGE, "Database", "")
    c.setFont(BODY_FONT, 10); c.setFillColor(INK)
    steps = ["1. App asks cache for key", "2a. HIT → return instantly",
             "2b. MISS → query database", "3. Store result in cache (TTL)", "4. Return to caller"]
    yy = 400
    for s in steps:
        c.drawString(90, yy, s); yy -= 22
    arrow(c, 192, 510, 242, 510, color=ACCENT)
    arrow(c, 250, 478, 250, 440, color=ACCENT)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Cache Invalidation Strategies",
                       "The two hard problems: naming things, cache invalidation, off-by-one errors.")
    items = [("TTL Expiry", "Entries auto-expire after N seconds. Simple; serves stale briefly.", BOX_GREEN),
             ("Write-Through", "Write to cache AND db together. Always fresh; slower writes.", BOX_BLUE),
             ("Write-Behind", "Write to cache now, db later. Fast; risk of loss.", BOX_ORANGE),
             ("Eviction (LRU/LFU)", "Full cache? Drop least-recently / least-frequently used.", BOX_TEAL)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=12)
        yy -= 72
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "CDN: Cache at the Edge",
                       "Push static content to servers near every user on Earth.")
    box(c, 246, 520, 120, 60, BOX_RED, "Origin", "")
    for i, (bx, lbl) in enumerate([(72, "NYC Edge"), (246, "London Edge"), (420, "Tokyo Edge")]):
        box(c, bx, 380, 120, 60, BOX_GREEN, lbl, "cached copy")
        arrow(c, 306, 518, bx + 60, 442, color=GREEN)
    box(c, 246, 250, 120, 60, BOX_BLUE, "User in Tokyo", "")
    arrow(c, 480, 378, 330, 312, color=ACCENT, label="8 ms")
    c.setStrokeColor(RED); c.setDash(4, 3); c.setLineWidth(1.5)
    c.line(300, 280, 300, 520); c.setDash()
    c.setFont(BODY_FONT, 9); c.setFillColor(RED)
    c.drawString(308, 400, "would-be 180 ms to origin")
    note(c, 72, 150, 468, "Edge caches serve 90%+ of static traffic locally. Origin only sees cache misses.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Cache Hit Ratio: The Scoreboard",
                       "Hit ratio = hits / (hits + misses). Higher is better.")
    # bar chart
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y, "Hit ratio by content type")
    bars = [("Static assets", 0.97, GREEN), ("API responses", 0.72, ACCENT),
            ("Personalized", 0.25, ORANGE), ("Real-time", 0.05, RED)]
    yy = y - 30
    for lbl, ratio, col in bars:
        c.setFont(BODY_FONT, 10); c.setFillColor(INK)
        c.drawString(72, yy, lbl)
        c.setFillColor(col); c.rect(200, yy - 6, 280 * ratio, 16, fill=1, stroke=0)
        c.setFillColor(INK); c.drawString(490, yy, f"{int(ratio*100)}%")
        yy -= 32
    note(c, 72, yy - 60, 468, "Static assets cache beautifully. Personalized and real-time data barely cache at all — design accordingly.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Full-Stack Caching Layers",
                       "Cache at every layer of the stack.")
    layers = [("Browser", "Cache-Control, ETag, service workers", BOX_BLUE),
              ("CDN Edge", "PoPs worldwide, static + some dynamic", BOX_GREEN),
              ("Load Balancer", "Occasionally caches at L7", BOX_TEAL),
              ("Application", "In-memory / Redis cache-aside", BOX_ORANGE),
              ("Database", "Query cache, read replicas", BOX_RED)]
    yy = y
    for name, desc, fill in layers:
        arrow(c, 306, yy - 8, 306, yy - 34, color=MUTED, width=1.5)
        box(c, 156, yy - 62, 300, 46, fill, name, desc, font_size=11)
        yy -= 74
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Caching & CDNs — Remember",
                 ["Cache-aside: check cache first; on miss, load from DB and populate with a TTL.",
                  "Invalidation choices: TTL (simple, briefly stale), write-through (fresh, slower), write-behind (fast, risky).",
                  "CDNs push content to edge locations — users fetch from nearby, not from origin.",
                  "Hit ratio tells you if caching is working; static assets hit 95%+, personalized data far less.",
                  "Layer your caches: browser → CDN → app → database."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_microservices(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Microservices\nArchitecture",
               "Decompose the monolith.\nIndependent services, independent scaling, independent deploys.",
               "System Design", None); pg += 1

    y = section_header(c, 1, 6, "The Monolith: One Deployable",
                       "All features in one codebase, one database, one release train.")
    box(c, 156, 380, 300, 140, BOX_ORANGE, "Monolith", "UI + Auth + Orders + Payments + Search")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    feats = ["Single codebase — simple to start", "One database — easy transactions",
             "One deploy — everything ships together", "Scales as a unit — wasteful"]
    yy = 340
    for f in feats:
        c.drawString(176, yy, "• " + f); yy -= 20
    note(c, 72, 200, 468, "Great for small teams. Painful when teams and scale grow — every change risks everything.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Decompose by Business Capability",
                       "Split along domain boundaries — each service owns its data.")
    svcs = [("Auth", BOX_BLUE, 72), ("Orders", BOX_GREEN, 196),
            ("Payments", BOX_ORANGE, 320), ("Search", BOX_TEAL, 444)]
    for name, fill, bx in svcs:
        box(c, bx, 440, 96, 70, fill, name, "own DB")
    box(c, 226, 300, 160, 60, BOX_PURP, "API Gateway", "single entry point")
    for bx in [120, 244, 368, 492]:
        arrow(c, bx, 438, 306, 362, color=ACCENT, width=1.5)
    arrow(c, 306, 560, 306, 362, color=ACCENT, label="client requests")
    note(c, 72, 200, 468, "Each service deploys independently and scales independently. The gateway routes and composes.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Communication: Sync vs Async",
                       "Services talk via REST/gRPC (sync) or events (async).")
    box(c, 72, y - 56, 225, 100, BOX_BLUE, "Synchronous", "REST / gRPC", font_size=12)
    box(c, 315, y - 56, 225, 100, BOX_GREEN, "Asynchronous", "Events / queues", font_size=12)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    sy = ["Request → wait → response", "Simple, familiar", "Caller blocked; cascading failures"]
    ay = ["Publish event → move on", "Decoupled, resilient", "Eventual consistency"]
    yy = y - 86
    for t in sy: c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 86
    for t in ay: c.drawString(331, yy, "• " + t); yy -= 18
    # mini event diagram
    box(c, 72, 200, 110, 50, BOX_GREEN, "Order svc", "")
    box(c, 251, 200, 110, 50, BOX_ORANGE, "Event bus", "Kafka")
    box(c, 430, 200, 110, 50, BOX_TEAL, "Email svc", "")
    arrow(c, 182, 225, 249, 225, color=ACCENT, label="order.created")
    arrow(c, 361, 225, 428, 225, color=ACCENT, label="consume")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Service Discovery & Resilience",
                       "Find services dynamically; fail fast and gracefully.")
    items = [("Service Registry", "Services register on boot; callers discover addresses (Consul, Eureka, k8s DNS).", BOX_BLUE),
             ("Circuit Breaker", "After N failures, stop calling for a cooldown — fail fast instead of piling up.", BOX_RED),
             ("Retries + Backoff", "Retry transient failures with exponential backoff + jitter.", BOX_GREEN),
             ("Bulkheads", "Isolate resources per dependency so one slow service can't sink the ship.", BOX_ORANGE)]
    yy = y
    for name, desc, fill in items:
        box(c, 72, yy - 58, 468, 62, fill, name, desc, font_size=11.5)
        yy -= 78
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Data: Database per Service",
                       "No shared databases — each service owns its schema.")
    box(c, 72, 420, 130, 60, BOX_BLUE, "Orders svc", "")
    box(c, 72, 340, 130, 60, BOX_BLUE, "Orders DB", "private")
    box(c, 241, 420, 130, 60, BOX_GREEN, "Payments svc", "")
    box(c, 241, 340, 130, 60, BOX_GREEN, "Pay DB", "private")
    box(c, 410, 420, 130, 60, BOX_ORANGE, "Search svc", "")
    box(c, 410, 340, 130, 60, BOX_ORANGE, "Search idx", "private")
    c.setStrokeColor(RED); c.setLineWidth(2); c.setDash(5, 4)
    c.line(137, 338, 306, 338); c.line(306, 338, 475, 338); c.setDash()
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(306, 312, "✗ NO direct cross-service DB access")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 290, "Share via APIs and events — never via the database.")
    note(c, 72, 200, 468, "The saga pattern coordinates multi-service transactions with compensating actions instead of 2PC.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Observability: See the Whole System",
                       "Distributed tracing, metrics, and logs — correlated by request ID.")
    box(c, 72, 440, 468, 60, BOX_TEAL, "Trace: req-abc123", "gateway → auth (12ms) → orders (48ms) → payments (210ms ⚠)")
    # span bars
    spans = [("gateway", 0, 270, ACCENT), ("auth", 5, 12, GREEN),
             ("orders", 20, 48, ACCENT2), ("payments", 70, 210, RED)]
    yy = 400
    c.setFont(BODY_FONT, 10)
    for name, start, dur, col in spans:
        c.setFillColor(INK); c.drawString(72, yy, name)
        c.setFillColor(col); c.rect(160 + start, yy - 6, dur, 14, fill=1, stroke=0)
        yy -= 28
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(72, 210, "One slow span (payments) explains the whole slow request. Metrics + logs + traces = the three pillars.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Microservices — Remember",
                 ["Decompose by business capability; each service owns its code, data, and deploys.",
                  "Communicate via sync APIs (simple) or async events (resilient) — choose per interaction.",
                  "Resilience: service discovery, circuit breakers, retries with backoff, bulkheads.",
                  "Database-per-service; coordinate with sagas, never shared tables.",
                  "Observability is mandatory: distributed tracing with one request ID across services."],
                 pg)
    c.save()
    print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    pdf_load_balancing(os.path.join(out, "bbg-load-balancing.pdf"))
    pdf_caching_cdn(os.path.join(out, "bbg-caching-cdn.pdf"))
    pdf_microservices(os.path.join(out, "bbg-microservices.pdf"))
