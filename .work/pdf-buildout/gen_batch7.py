"""Batch 7: System Design PDFs (byte-byte-go style) — 25 guides.

Each PDF: title_page + 5-7 numbered step pages with original diagrams
built from bbg_style primitives (box/arrow/note/bullet_list) + raw
reportlab shapes + summary_page with takeaways. All diagrams original.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


# ---------- small shared drawing helpers (original) ----------
def _node_dot(c, cx, cy, r, fill, label, fsize=10, txt=white, dy=-3.5):
    c.setFillColor(fill); c.circle(cx, cy, r, fill=1, stroke=0)
    c.setStrokeColor(INK); c.setLineWidth(1.1); c.circle(cx, cy, r, fill=0, stroke=1)
    c.setFillColor(txt); c.setFont(TITLE_FONT, fsize)
    c.drawCentredString(cx, cy + dy, label)
    return cx, cy


def _ring(c, cx, cy, r, color=ACCENT, width=3):
    c.setStrokeColor(color); c.setLineWidth(width)
    c.circle(cx, cy, r, fill=0, stroke=1)


def _on_ring(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)),
            cy + r * math.sin(math.radians(deg)))


def _ring_node(c, cx, cy, r, deg, color, label):
    x, y = _on_ring(cx, cy, r, deg)
    _node_dot(c, x, y, 15, color, label, fsize=10)
    return x, y


def _caption(c, x, y, text, size=10):
    c.setFillColor(MUTED); c.setFont(BODY_FONT, size)
    c.drawString(x, y, text)


def _row_of_boxes(c, y, items, x0=72, w=468, h=72):
    """items: list of (label, sublabel, fill). Returns y below row."""
    n = len(items); gap = 14
    bw = (w - gap * (n - 1)) / n
    for i, (lab, sub, fill) in enumerate(items):
        x = x0 + i * (bw + gap)
        box(c, x, y - h, bw, h, fill, lab, sub, font_size=11)
        if i:
            arrow(c, x - gap + 2, y - h / 2, x - 2, y - h / 2, color=ACCENT, width=1.8)
    return y - h


# =============================================================
# 1. Consistent Hashing
# =============================================================
def pdf_consistent_hashing(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Consistent Hashing\nVisual Guide",
               "Distribute keys across nodes so\nscaling barely moves any data.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "The Resizing Problem",
                       "Naive hashing breaks when the cluster changes size.")
    box(c, 72, y - 120, 468, 100, BOX_RED, "hash(key) mod N",
        "N = 3: keys spread fine. N = 4 after adding a node:", font_size=12)
    c.setFillColor(INK); c.setFont(MONO_FONT, 10)
    c.drawString(72, y - 150, "key1 -> node 1    key2 -> node 0    key3 -> node 2    (N=3)")
    c.setFillColor(RED); c.setFont(MONO_FONT, 10)
    c.drawString(72, y - 170, "key1 -> node 2    key2 -> node 1    key3 -> node 3    (N=4, almost EVERYTHING moves)")
    note(c, 72, y - 250, 468, "mod N remaps ~N-1/N of all keys on every resize. At scale that is a full data migration.",
         fill=BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "The Hash Ring",
                       "Keys AND nodes live on one ring; keys walk clockwise to their owner.")
    _ring(c, 306, y - 190, 130)
    _ring_node(c, 306, y - 190, 130, 90, ACCENT, "A")
    _ring_node(c, 306, y - 190, 130, 210, GREEN, "B")
    _ring_node(c, 306, y - 190, 130, 330, ORANGE, "C")
    for deg, kl, col in [(30, "k1", RED), (70, "k2", RED), (160, "k3", RED), (250, "k4", RED), (300, "k5", RED)]:
        x, kk = _on_ring(306, y - 190, 130, deg)
        _node_dot(c, x, kk, 8, col, kl, fsize=7, dy=-2.5)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 10)
    c.drawCentredString(306, y - 345, "k1 -> A (first node clockwise)     k4 -> B     k5 -> C")
    note(c, 72, y - 420, 468, "hash(key) and hash(node) share the same space (e.g. 2^32 points on the ring).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Adding a Node Moves Little",
                       "Only keys between the new node and its predecessor relocate.")
    _ring(c, 306, y - 190, 130)
    _ring_node(c, 306, y - 190, 130, 90, ACCENT, "A")
    _ring_node(c, 306, y - 190, 130, 210, GREEN, "B")
    _ring_node(c, 306, y - 190, 130, 330, ORANGE, "C")
    dx, dy2 = _ring_node(c, 306, y - 190, 130, 140, TEAL, "D")
    c.setFillColor(TEAL); c.setFont(TITLE_FONT, 11)
    c.drawString(dx - 8, dy2 + 22, "NEW")
    x1, y1 = _on_ring(306, y - 190, 130, 160)
    _node_dot(c, x1, y1, 8, RED, "k3", fsize=7, dy=-2.5)
    c.setStrokeColor(RED); c.setLineWidth(2)
    c.line(x1, y1 - 12, x1 + 30, y1 - 44)
    c.setFillColor(RED); c.setFont(BODY_FONT, 9.5)
    c.drawString(x1 + 34, y1 - 48, "k3 remaps B -> D")
    note(c, 72, y - 420, 468, "Only ~1/N of keys move per node added. Everyone else's keys stay put. Zero downtime.", fill=BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Removing a Node",
                       "Keys fall forward to the next surviving node.")
    _ring(c, 306, y - 190, 130)
    _ring_node(c, 306, y - 190, 130, 90, ACCENT, "A")
    _ring_node(c, 306, y - 190, 130, 210, GREEN, "B")
    xb, yb = _on_ring(306, y - 190, 130, 330)
    c.setStrokeColor(RED); c.setLineWidth(2)
    c.line(xb - 15, yb - 15, xb + 15, yb + 15); c.line(xb - 15, yb + 15, xb + 15, yb - 15)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 10); c.drawString(xb - 40, yb + 24, "C DOWN")
    x1, y1 = _on_ring(306, y - 190, 130, 300)
    _node_dot(c, x1, y1, 8, RED, "k5", fsize=7, dy=-2.5)
    xa, ya = _on_ring(306, y - 190, 130, 90)
    arrow(c, x1 + 10, y1 + 10, xa - 22, ya - 6, color=RED, width=2, label="reassign")
    note(c, 72, y - 420, 468, "k5's next-clockwise node is gone, so it walks on to A. With replication (RF=3), copies shift the same way.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Virtual Nodes Fix Balance",
                       "Real rings are lumpy: one node can own 3x its share. Vnodes smooth it out.")
    _ring(c, 306, y - 190, 130)
    vA = [80, 95, 110]; vB = [200, 215, 230]; vC = [320, 335, 350]
    for d in vA:
        x, yy2 = _on_ring(306, y - 190, 130, d); _node_dot(c, x, yy2, 7, ACCENT, "", fsize=6)
    for d in vB:
        x, yy2 = _on_ring(306, y - 190, 130, d); _node_dot(c, x, yy2, 7, GREEN, "", fsize=6)
    for d in vC:
        x, yy2 = _on_ring(306, y - 190, 130, d); _node_dot(c, x, yy2, 7, ORANGE, "", fsize=6)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawCentredString(306, y - 345, "Each physical node = many virtual points (e.g. 100-200 vnodes)")
    yy = bullet_list(c, 72, y - 380,
        ["Each vnode is an independent range of the ring: load spreads evenly even with few physical nodes.",
         "Heterogeneous hardware: give bigger machines MORE vnodes.",
         "Cassandra calls them vnodes; Dynamo used the same trick."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Where It Runs in Production",
                       "The workhorse of distributed storage.")
    uses = [("DynamoDB", "key -> partition via MD5 ring", BOX_BLUE),
            ("Cassandra", "vnodes (default 16/node), RF copies", BOX_GREEN),
            ("Memcached clients", "consistent hashing picks the server", BOX_ORANGE),
            ("CDNs", "URL -> edge PoP on the ring", BOX_TEAL)]
    yy = y
    for name, desc, fill in uses:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11.5)
        yy -= 70
    note(c, 72, yy - 60, 468, "Bonus: the ring also shards requests, not just storage -- any client can compute the owner locally.", fill=BOX_PURP)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Consistent Hashing — Remember",
                 ["mod N hashing remaps ~everything on resize; consistent hashing remaps only ~1/N keys.",
                  "Keys and nodes share one hash ring; each key walks clockwise to its owner node.",
                  "Adding/removing a node disturbs only the key range adjacent to it.",
                  "Virtual nodes (many ring points per machine) fix uneven load and honor hardware size.",
                  "DynamoDB, Cassandra, memcached clients, and CDNs all use it to place data and requests."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 2. CAP Theorem
# =============================================================
def pdf_cap(path):
    c = new_canvas(path); pg = 1
    title_page(c, "CAP Theorem\nVisual Guide",
               "Consistency, Availability, Partition tolerance:\nwhy distributed systems must pick two.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "The Three Properties",
                       "Every distributed data store promises some of each.")
    _row_of_boxes(c, y,
        [("C", "every read sees the latest write", BOX_BLUE),
         ("A", "every request gets a response", BOX_GREEN),
         ("P", "works despite network splits", BOX_ORANGE)])
    yy = bullet_list(c, 72, y - 120,
        ["Consistency (linearizability): all nodes agree, always -- like one machine.",
         "Availability: the system answers every request, even if some nodes are sick.",
         "Partition tolerance: a network split cannot stop the system from operating."],
        font_size=10.5, gap=26)
    note(c, 72, yy - 70, 468, "These are guarantees about BEHAVIOR during failures, not features you toggle.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Pick Two",
                       "During a partition, you can only guarantee two of the three.")
    tx, ty, s = 306, y - 210, 150
    pts = [(tx, ty + 105, "C", BOX_BLUE), (tx - 130, ty - 75, "A", BOX_GREEN), (tx + 130, ty - 75, "P", BOX_ORANGE)]
    for i in range(3):
        x1, y1, _, _ = pts[i]; x2, y2, _, _ = pts[(i + 1) % 3]
        c.setStrokeColor(ACCENT); c.setLineWidth(2.5); c.line(x1, y1, x2, y2)
    for x, yy2, lab, fill in pts:
        _node_dot(c, x, yy2, 34, fill, lab, fsize=20, txt=INK, dy=-7)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(tx, ty - 8, "CA / CP / AP")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawCentredString(tx, ty - 28, "choose the edge you can live on")
    note(c, 72, y - 430, 468, "CA (no P) exists only if you deny partitions happen -- true of a single node, not a distributed system.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Partitions Are Not Optional",
                       "Networks WILL split. The question is what you sacrifice when they do.")
    box(c, 72, y - 110, 200, 90, BOX_BLUE, "Replica 1", "has write W", font_size=12)
    box(c, 340, y - 110, 200, 90, BOX_BLUE, "Replica 2", "never saw W", font_size=12)
    c.setStrokeColor(RED); c.setLineWidth(3)
    for yy2 in range(int(y - 100), int(y - 30), 14):
        c.line(292, yy2, 318, yy2 + 8)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(306, y - 116, "SPLIT")
    yy = bullet_list(c, 72, y - 240,
        ["Choice 1 (CP): Replica 2 REFUSES reads until it can confirm W -- availability lost.",
         "Choice 2 (AP): Replica 2 answers from stale data -- consistency lost.",
         "There is no third choice. The partition forces your hand."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "CP Systems: Consistency First",
                       "Block or fail rather than serve a stale answer.")
    cps = [("etcd / ZooKeeper", "consensus quorum; minority partition stops writes", BOX_BLUE),
           ("HBase", "single region-server per range; split = unavailable", BOX_TEAL),
           ("MongoDB (majority)", "writes need majority ack; stale reads rejected", BOX_GREEN)]
    yy = y
    for name, desc, fill in cps:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    note(c, 72, yy - 60, 468, "Use CP for: leader election, config, financial ledgers -- anywhere wrong data beats no data.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "AP Systems: Availability First",
                       "Answer always; reconcile conflicts later.")
    aps = [("Cassandra", "tunable consistency; hinted handoff replays writes", BOX_GREEN),
           ("DynamoDB", "leaderless replication, vector clocks, sloppy quorum", BOX_BLUE),
           ("CouchDB", "multi-master; conflicts kept as document revisions", BOX_ORANGE)]
    yy = y
    for name, desc, fill in aps:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    note(c, 72, yy - 60, 468, "Use AP for: shopping carts, feeds, session state -- anywhere downtime costs more than staleness.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "PACELC: The Missing Half",
                       "CAP only covers partitions. PACELC asks: what about normal operation?")
    box(c, 72, y - 100, 468, 90, BOX_PURP, "P A C E L C",
        "Partition? -> A or C.   Else -> Latency or Consistency.", font_size=12)
    yy = bullet_list(c, 72, y - 150,
        ["Even with NO partition, synchronous replication costs latency on every write.",
         "Systems like Dynamo choose Latency: async replication, stale reads possible even when healthy.",
         "Systems like Spanner choose Consistency: TrueTime waits out clock uncertainty (small latency tax).",
         "So the real trade-off is four-way: partition behavior AND steady-state latency vs consistency."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "CAP Theorem — Remember",
                 ["C = every read sees the latest write; A = every request answered; P = survives network splits.",
                  "During a partition you keep exactly two: CP blocks rather than lie, AP answers possibly-stale.",
                  "Partitions are inevitable, so 'CA' only describes a single machine -- not a distributed system.",
                  "PACELC completes the picture: with no partition, you trade Latency against Consistency.",
                  "Choose by workload: ledgers and locks want CP; carts and feeds want AP."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 3. Database Sharding
# =============================================================
def pdf_sharding(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Database Sharding\nVisual Guide",
               "Split one database into many:\nscale writes past a single machine.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Horizontal Partitioning",
                       "Rows are divided across shards; each shard is a full, independent DB.")
    _row_of_boxes(c, y,
        [("Shard 1", "users A-F", BOX_BLUE),
         ("Shard 2", "users G-M", BOX_GREEN),
         ("Shard 3", "users N-Z", BOX_ORANGE)])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 130, "App -> router -> shard(owner of key). Each shard holds a DISJOINT slice of rows.")
    yy = bullet_list(c, 72, y - 165,
        ["Vertical partitioning splits COLUMNS (rare). Sharding splits ROWS (the scaling move).",
         "Each shard has its own CPU, disk, and connections: write throughput multiplies by shard count.",
         "Trade-off: cross-shard joins and transactions get painful -- design the shard key first."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "The Shard Key Decides Everything",
                       "Pick the column every query path can route on.")
    keys = [("Hash key", "shard = hash(user_id) mod S -- even spread, no range scans", BOX_GREEN),
            ("Range key", "shard by created_at or last name -- range queries stay local", BOX_BLUE),
            ("Geo key", "shard by region -- data lives near its users", BOX_TEAL),
            ("Directory", "lookup service maps key -> shard -- flexible, extra hop", BOX_ORANGE)]
    yy = y
    for name, desc, fill in keys:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Good key: high cardinality, evenly distributed, present in most queries. user_id beats country_code.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Hotspots: The Celebrity Problem",
                       "Even hashing cannot save you when one KEY gets all the traffic.")
    _row_of_boxes(c, y,
        [("Shard 1", "normal load", BOX_GREEN),
         ("Shard 2", "VIRAL user\n100x traffic", BOX_RED),
         ("Shard 3", "normal load", BOX_GREEN)])
    yy = bullet_list(c, 72, y - 130,
        ["A hot KEY overloads its shard while siblings idle -- adding shards does not help.",
         "Fixes: split the hot key (suffix buckets: user_123#1..#N), cache the hot read path heavily,",
         "or isolate hot tenants onto dedicated shards (noisy-neighbor quarantine)."],
        font_size=10.5, gap=26)
    note(c, 72, yy - 66, 468, "Monitor per-shard QPS, not just the cluster average. Averages hide hotspots.", fill=BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Rebalancing: Moving the Data",
                       "Shards fill unevenly over time; you must split or migrate ranges.")
    box(c, 72, y - 80, 130, 70, BOX_RED, "Shard 2", "90% full", font_size=11)
    arrow(c, 204, y - 45, 236, y - 45, color=ACCENT, width=2.5, label="split")
    box(c, 238, y - 80, 130, 70, BOX_GREEN, "Shard 2a", "45% full", font_size=11)
    box(c, 380, y - 80, 130, 70, BOX_GREEN, "Shard 2b", "45% full", font_size=11)
    yy = bullet_list(c, 72, y - 130,
        ["Range shards: split the range in two, update the routing table. Hash shards: add a shard, remap (consistent hashing).",
         "Online migration: dual-write to old+new, backfill, then flip reads -- never stop the world.",
         "Vitess, Citus, and MongoDB's balancer automate this; DIY sharding means YOU build the mover."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Sharding vs Replication",
                       "They scale different things. Most systems need both.")
    box(c, 72, y - 90, 225, 110, BOX_BLUE, "Replication", "copies of the SAME data\nscales READS + availability", font_size=11)
    box(c, 315, y - 90, 225, 110, BOX_ORANGE, "Sharding", "PARTS of the data per node\nscales WRITES + capacity", font_size=11)
    yy = bullet_list(c, 72, y - 230,
        ["Read-heavy? Replicas (leader + followers) are simpler and keep joins intact.",
         "Write-heavy or data too big for one disk? Shard. Then replicate EACH shard for durability.",
         "Rule of thumb: replicate first (cheap), shard when one node cannot hold the write load."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Query Fan-Out (Scatter-Gather)",
                       "No shard key in the query? Ask every shard and merge.")
    box(c, 216, y - 70, 180, 56, BOX_PURP, "Router", "SELECT ... WHERE age > 30", font_size=10)
    for i, sx in enumerate([72, 216, 360]):
        box(c, sx, y - 190, 160, 64, BOX_BLUE, f"Shard {i+1}", "partial results", font_size=10)
        arrow(c, 306, y - 70, sx + 80, y - 126, color=ACCENT, width=1.6)
    arrow(c, 306, y - 126, 306, y - 70 + 6, color=GREEN, width=2, label="merge")
    note(c, 72, y - 300, 468, "Fan-out latency = SLOWEST shard. One straggler punishes every cross-shard query -- keep them rare.", fill=BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Database Sharding — Remember",
                 ["Sharding splits ROWS across independent databases to scale writes and capacity.",
                  "The shard key is the whole design: high-cardinality, even, present in hot queries.",
                  "Hotspots come from hot KEYS, not bad hashing -- split, cache, or quarantine them.",
                  "Rebalance online (dual-write + backfill); replicate each shard for durability.",
                  "Replication scales reads, sharding scales writes; fan-out queries pay the slowest-shard tax."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 4. Replication Strategies
# =============================================================
def pdf_replication(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Replication Strategies\nVisual Guide",
               "Keep copies of data on many nodes:\ndurability, availability, and locality.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Why Replicate",
                       "Three reasons, all about surviving reality.")
    _row_of_boxes(c, y,
        [("Durability", "disk dies, data lives", BOX_GREEN),
         ("Availability", "serve during outages", BOX_BLUE),
         ("Locality", "reads near the user", BOX_TEAL)])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 120, "Replication factor (RF): how many copies. RF=3 is the industry default.")
    yy = bullet_list(c, 72, y - 150,
        ["Every strategy below is a different answer to: who takes writes, and how do copies converge?",
         "More copies = more durability, but every copy is a consistency problem to manage."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Leader / Follower (Single Leader)",
                       "One writer, many readers. Simple, ordered, the default.")
    box(c, 216, y - 70, 180, 60, ACCENT, "LEADER", "takes all writes", font_size=11)
    for i, fx in enumerate([72, 216, 360]):
        box(c, fx, y - 190, 160, 60, BOX_BLUE, f"Follower {i+1}", "replay log", font_size=10)
        arrow(c, 306, y - 70, fx + 80, y - 130, color=ACCENT, width=1.8)
    arrow(c, 120, y - 40, 216, y - 40, color=GREEN, width=2, label="write")
    note(c, 72, y - 300, 468, "Writes are totally ordered by the leader -- no write conflicts ever. Reads scale by adding followers.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Multi-Leader",
                       "Write locally anywhere; leaders sync with each other.")
    _row_of_boxes(c, y - 20,
        [("Leader US", "local writes", BOX_BLUE),
         ("Leader EU", "local writes", BOX_GREEN),
         ("Leader APAC", "local writes", BOX_TEAL)])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 140, "US <-> EU <-> APAC replicate asynchronously. Low write latency on every continent.")
    yy = bullet_list(c, 72, y - 170,
        ["The price: concurrent writes to the same key CONFLICT -- you need resolution (last-write-wins, CRDTs, app merge).",
         "Topology matters: star, ring, or all-to-all changes failover behavior.",
         "Use when: offline-first apps, geo-distributed writes, low-latency local writes."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Leaderless (Dynamo-Style)",
                       "No leader at all: any node accepts the write.")
    box(c, 72, y - 70, 130, 64, BOX_BLUE, "Node A", "", font_size=10)
    box(c, 216, y - 70, 130, 64, BOX_BLUE, "Node B", "", font_size=10)
    box(c, 360, y - 70, 130, 64, BOX_BLUE, "Node C", "", font_size=10)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 160, "Client writes to any W nodes, reads from any R nodes. No failover -- there is no leader to lose.")
    yy = bullet_list(c, 72, y - 190,
        ["Availability win: the cluster keeps accepting writes even when nodes are down.",
         "Consistency work moves to the CLIENT: version vectors detect concurrent writes, app merges siblings.",
         "Cassandra and DynamoDB live here; quorums (next page) decide what 'enough' means."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Synchronous vs Asynchronous",
                       "Wait for the copy, or trust it will catch up?")
    box(c, 72, y - 100, 225, 110, BOX_RED, "Synchronous", "leader waits for follower ack\nslower, no data loss", font_size=11)
    box(c, 315, y - 100, 225, 110, BOX_GREEN, "Asynchronous", "leader acks, replicates after\nfast, may lose recent writes", font_size=11)
    yy = bullet_list(c, 72, y - 240,
        ["Semi-sync (the middle path): wait for ONE follower -- bounded loss, modest latency (MySQL semi-sync).",
         "Chain replication: writes flow leader -> f1 -> f2, reads from the tail -- ordered AND fast reads.",
         "Durability is a spectrum, not a switch: pick the point your SLA can afford."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Read / Write Quorums",
                       "The math that makes leaderless replication consistent.")
    box(c, 72, y - 110, 468, 110, BOX_PURP, "R + W > N  =>  strong consistency",
        "N=3 replicas, W=2, R=2: every read overlaps a write quorum", font_size=12)
    yy = bullet_list(c, 72, y - 150,
        ["W + R > N guarantees read-write overlap: a read quorum always contains the latest write.",
         "W + W > N prevents write-write conflicts without a leader.",
         "Tune it: W=1,R=3 (fast writes, slow reads) ... W=3,R=1 (slow writes, fast reads) ... W=2,R=2 (balanced).",
         "Sloppy quorum: if a replica is down, write to a stand-in and hand it off later."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Replication Strategies — Remember",
                 ["Leader/follower: one writer, totally ordered, simple -- the default for most systems.",
                  "Multi-leader: local writes everywhere, but concurrent writes need conflict resolution.",
                  "Leaderless: any node takes writes; quorums (R + W > N) restore consistency without a leader.",
                  "Sync replication buys durability with latency; async buys speed with potential loss.",
                  "Replicate each shard, tune W/R to your read-write ratio, and RF=3 is the sane default."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 5. Caching Strategies
# =============================================================
def pdf_caching_strategies(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Caching Strategies\nVisual Guide",
               "Trade memory for speed:\nread/write paths, TTLs, eviction, and stampedes.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Cache-Aside (Lazy Loading)",
                       "The app owns the logic; the cache is just a fast shelf.")
    box(c, 72, y - 70, 120, 64, BOX_BLUE, "App", "", font_size=11)
    box(c, 246, y - 70, 120, 64, BOX_GREEN, "Cache", "check first", font_size=11)
    box(c, 420, y - 70, 120, 64, BOX_ORANGE, "DB", "on miss", font_size=11)
    arrow(c, 192, y - 38, 244, y - 38, color=ACCENT, width=1.8, label="1. get")
    arrow(c, 366, y - 52, 418, y - 52, color=RED, width=1.8, label="2. miss -> load")
    arrow(c, 366, y - 24, 244, y - 24, color=GREEN, width=1.8, label="3. fill")
    yy = bullet_list(c, 72, y - 170,
        ["Hit: serve from cache. Miss: load from DB, write to cache, then serve.",
         "Writes go straight to the DB and invalidate (or update) the cache entry.",
         "Pros: cache holds only hot data; a dead cache never blocks reads. Cons: first read is slow, stale window on write."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Read/Write-Through",
                       "The cache sits IN the path and owns the data flow.")
    box(c, 72, y - 70, 120, 64, BOX_BLUE, "App", "", font_size=11)
    box(c, 246, y - 70, 120, 64, BOX_GREEN, "Cache", "single API", font_size=11)
    box(c, 420, y - 70, 120, 64, BOX_ORANGE, "DB", "", font_size=11)
    arrow(c, 192, y - 38, 244, y - 38, color=ACCENT, width=2, label="read/write")
    arrow(c, 366, y - 38, 418, y - 38, color=ACCENT, width=2, label="through")
    yy = bullet_list(c, 72, y - 170,
        ["Read-through: cache loads from DB on miss (app code stays simple).",
         "Write-through: every write lands in cache AND DB before ack -- always consistent, write latency doubles.",
         "Best when the same data is read and written through one layer (ORM-style caches)."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Write-Back (Write-Behind)",
                       "Acknowledge fast, persist lazily. Speed with a risk window.")
    box(c, 72, y - 70, 140, 64, BOX_BLUE, "App", "write -> ack", font_size=11)
    box(c, 266, y - 70, 140, 64, BOX_GREEN, "Cache", "dirty entries", font_size=11)
    box(c, 420, y - 70, 120, 64, BOX_RED, "DB", "flushed later", font_size=11)
    arrow(c, 212, y - 38, 264, y - 38, color=GREEN, width=2, label="fast ack")
    arrow(c, 406, y - 52, 418, y - 52, color=ORANGE, width=2, label="batch flush")
    note(c, 72, y - 180, 468, "Crash before flush = data loss. Use only where loss is tolerable or the log is durable (write-ahead log).", fill=BOX_RED)
    yy = bullet_list(c, 72, y - 260,
        ["Wins: absorbs write bursts, coalesces repeated writes to the same key.",
         "CPUs do this (L1/L2 caches); databases do NOT for user data -- durability first."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "TTL: Freshness on a Timer",
                       "Every entry carries an expiry; staleness becomes a knob.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 20, "Short TTL (seconds)                    Long TTL (hours)")
    box(c, 72, y - 100, 200, 60, BOX_GREEN, "fresh, low hit rate", "", font_size=10)
    box(c, 340, y - 100, 200, 60, BOX_ORANGE, "stale risk, high hit rate", "", font_size=10)
    yy = bullet_list(c, 72, y - 140,
        ["TTL bounds staleness: the worst case is 'data as of TTL seconds ago' -- a real SLA.",
         "Jitter TTLs (+/- 10%) so a million keys do not expire in the same second.",
         "Event-driven invalidation (publish 'user:42 changed') beats short TTLs for correctness-critical data."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Eviction: LRU and LFU",
                       "Memory is finite; the policy picks the victim.")
    box(c, 72, y - 100, 225, 100, BOX_BLUE, "LRU", "evict Least Recently Used\nrecency wins", font_size=11)
    box(c, 315, y - 100, 225, 100, BOX_TEAL, "LFU", "evict Least Frequently Used\nfrequency wins", font_size=11)
    yy = bullet_list(c, 72, y - 230,
        ["LRU: great for recency workloads (sessions, feeds). Weakness: a full scan poisons the cache.",
         "LFU: great for popularity skew (viral content). Weakness: stale favorites never leave (needs aging).",
         "Redis: volatile-lru / allkeys-lfu / TinyLFU admission -- pick by workload, measure hit ratio."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Thundering Herd (Dogpile)",
                       "A hot key expires; ten thousand requests hit the DB at once.")
    box(c, 72, y - 70, 150, 64, BOX_RED, "Key expires", "cache empty", font_size=10)
    arrow(c, 222, y - 38, 254, y - 38, color=RED, width=2.5, label="10k misses")
    box(c, 256, y - 70, 150, 64, BOX_RED, "DB", "crushed", font_size=11)
    box(c, 72, y - 190, 200, 64, BOX_GREEN, "Fix: single-flight", "1 loads, rest wait", font_size=10)
    box(c, 300, y - 190, 240, 64, BOX_GREEN, "Fix: stale-while-revalidate", "serve old, refresh async", font_size=10)
    note(c, 72, y - 300, 468, "Probabilistic early refresh (x-fetch): recompute BEFORE expiry with p rising as TTL nears.", fill=BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Caching Strategies — Remember",
                 ["Cache-aside: app checks cache, loads on miss -- simple, cache holds only hot data.",
                  "Write-through keeps cache and DB in lockstep; write-back is fast but risks loss on crash.",
                  "TTL turns staleness into a tunable SLA; jitter expiries to avoid synchronized stampedes.",
                  "LRU favors recency, LFU favors popularity -- match the policy to the workload.",
                  "Defeat thundering herds with single-flight, stale-while-revalidate, or early refresh."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 6. Message Queues
# =============================================================
def pdf_message_queues(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Message Queues\nVisual Guide",
               "Decouple producers from consumers:\nbuffers, ordering, and delivery guarantees.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Producer / Consumer Decoupling",
                       "A durable buffer between 'work created' and 'work done'.")
    box(c, 72, y - 70, 120, 64, BOX_BLUE, "Producers", "fire & forget", font_size=11)
    box(c, 246, y - 100, 120, 124, BOX_ORANGE, "Queue", "durable\nbuffer", font_size=11)
    box(c, 420, y - 70, 120, 64, BOX_GREEN, "Consumers", "own pace", font_size=11)
    arrow(c, 192, y - 38, 244, y - 38, color=ACCENT, width=2.5, label="publish")
    arrow(c, 366, y - 38, 418, y - 38, color=ACCENT, width=2.5, label="poll")
    yy = bullet_list(c, 72, y - 200,
        ["Absorbs bursts: producers spike at 10x, consumers drain steadily -- the queue is the shock absorber.",
         "Decouples in time: consumer can be down for hours; messages wait. Decouples in space: neither side knows the other.",
         "Backpressure done right: slow consumers show as queue DEPTH (a metric), not as timeouts upstream."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Kafka: Partitions and Offsets",
                       "The log is the queue; partitions are the parallelism.")
    box(c, 72, y - 70, 468, 56, BOX_BLUE, "Topic: orders", "split into partitions", font_size=11)
    for i, px in enumerate([72, 222, 372]):
        box(c, px, y - 200, 130, 90, BOX_ORANGE, f"P{i}", "offset 0..n", font_size=11)
        for o in range(4):
            c.setFillColor(ACCENT); c.rect(px + 12 + o * 28, y - 165, 22, 18, fill=1, stroke=0)
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 8.5)
        c.drawString(px + 12, y - 182, "0  1  2  3")
    arrow(c, 306, y - 70, 306, y - 110, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 240, "Ordering guaranteed WITHIN a partition only. Same key -> same partition -> ordered.")
    note(c, 72, y - 320, 468, "Consumers track their own offset per partition: replay by rewinding. The broker never deletes what you have not read.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Consumer Groups Scale the Work",
                       "One partition -> one consumer in a group: add consumers, add throughput.")
    box(c, 72, y - 70, 130, 60, BOX_ORANGE, "P0", "", font_size=11)
    box(c, 222, y - 70, 130, 60, BOX_ORANGE, "P1", "", font_size=11)
    box(c, 372, y - 70, 130, 60, BOX_ORANGE, "P2", "", font_size=11)
    box(c, 72, y - 190, 130, 60, BOX_GREEN, "C1", "", font_size=11)
    box(c, 222, y - 190, 130, 60, BOX_GREEN, "C2", "", font_size=11)
    box(c, 372, y - 190, 130, 60, BOX_GREEN, "C3", "", font_size=11)
    for i in range(3):
        arrow(c, 137 + i * 150, y - 70, 137 + i * 150, y - 130, color=ACCENT, width=1.8)
    note(c, 72, y - 300, 468, "Ceiling: a group cannot out-consume its partition count. Need more parallelism? Add partitions (careful: key ordering).")
    yy = bullet_list(c, 72, y - 380,
        ["Rebalance: when a consumer joins/dies, partitions are reassigned -- expect a brief pause.",
         "Two groups on one topic = the same data feeding two pipelines independently."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "RabbitMQ: Exchanges and Routing",
                       "The exchange decides WHO gets the message; queues just hold them.")
    box(c, 216, y - 70, 180, 60, BOX_PURP, "Exchange", "routing rules", font_size=11)
    for i, (qx, qn) in enumerate([(72, "Q: alerts"), (216, "Q: billing"), (360, "Q: logs")]):
        box(c, qx, y - 190, 160, 60, BOX_TEAL, qn, "", font_size=10)
        arrow(c, 306, y - 70, qx + 80, y - 130, color=ACCENT, width=1.6)
    yy = bullet_list(c, 72, y - 280,
        ["Fanout: broadcast to every bound queue. Direct: exact routing-key match.",
         "Topic: pattern match (orders.* vs orders.eu.#). Headers: match on message attributes.",
         "Contrast Kafka: RabbitMQ routes smartly to queues; Kafka keeps one dumb log and lets consumers choose."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Delivery Semantics",
                       "What 'guaranteed delivery' actually promises.")
    sems = [("At-most-once", "fire and forget -- may LOSE messages (metrics, logs)", BOX_RED),
            ("At-least-once", "ack required, retry on timeout -- may DUPLICATE (the default)", BOX_ORANGE),
            ("Exactly-once", "effect applied once -- needs idempotent consumers + transactions", BOX_GREEN)]
    yy = y
    for name, desc, fill in sems:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    note(c, 72, yy - 60, 468, "Practical exactly-once = at-least-once delivery + idempotent receiver. See the Idempotency guide.", fill=BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Dead Letters and Poison Messages",
                       "Some messages will never succeed. Plan their funeral.")
    box(c, 72, y - 70, 150, 64, BOX_RED, "Poison msg", "fails 5x", font_size=11)
    arrow(c, 222, y - 38, 254, y - 38, color=RED, width=2, label="max retries")
    box(c, 256, y - 70, 150, 64, BOX_ORANGE, "DLQ", "quarantine", font_size=11)
    yy = bullet_list(c, 72, y - 170,
        ["Retry with backoff first; after N failures route to the Dead-Letter Queue -- never block the main queue.",
         "DLQ is an inbox for humans: inspect, fix, replay. Alert on DLQ depth, not just consumer lag.",
         "Poison messages (malformed, giant) deserve a schema registry + size limits so they never enter."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Message Queues — Remember",
                 ["Queues decouple producers and consumers in time and space; depth is your backpressure metric.",
                  "Kafka: partitioned append-only logs, per-partition ordering, consumer offsets enable replay.",
                  "Consumer groups parallelize to the partition count; rebalances pause consumption briefly.",
                  "RabbitMQ exchanges route (fanout/direct/topic); Kafka keeps one log and lets consumers filter.",
                  "Default to at-least-once + idempotent consumers; quarantine poison messages in a DLQ."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 7. Event-Driven Architecture
# =============================================================
def pdf_event_driven(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Event-Driven Architecture\nVisual Guide",
               "Systems that react to facts:\nevents, choreography, sourcing, and CQRS.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Events vs Commands",
                       "A fact about the past vs a request for the future -- never confuse them.")
    box(c, 72, y - 100, 225, 110, BOX_GREEN, "EVENT", "OrderPlaced { id, total }\npast tense, immutable fact", font_size=11)
    box(c, 315, y - 100, 225, 110, BOX_BLUE, "COMMAND", "PlaceOrder { items }\nimperative, can be rejected", font_size=11)
    yy = bullet_list(c, 72, y - 240,
        ["Events are broadcast: zero or many listeners. Commands target ONE handler that may say no.",
         "Naming rule: events in past tense (PaymentCaptured), commands as verbs (CapturePayment).",
         "Event-carried state: include enough payload that listeners skip a callback query."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Choreography: No Conductor",
                       "Each service reacts to events and emits its own -- the flow emerges.")
    box(c, 72, y - 70, 150, 60, BOX_BLUE, "Orders", "emits OrderPlaced", font_size=10)
    box(c, 360, y - 70, 150, 60, BOX_GREEN, "Payments", "emits Paid", font_size=10)
    box(c, 216, y - 190, 150, 60, BOX_ORANGE, "Shipping", "on Paid -> ships", font_size=10)
    arrow(c, 222, y - 40, 358, y - 40, color=ACCENT, width=1.8, label="OrderPlaced")
    arrow(c, 360, y - 70, 300, y - 130, color=ACCENT, width=1.8, label="Paid")
    yy = bullet_list(c, 72, y - 280,
        ["Pros: maximally decoupled -- add a Fraud service by subscribing, touching nothing.",
         "Cons: the business flow lives NOWHERE -- debugging means tracing events across services.",
         "Rule of thumb: choreography for simple flows (3 or fewer steps); orchestrate beyond that."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Orchestration: A Conductor",
                       "One saga orchestrator tells each service what to do next.")
    box(c, 216, y - 70, 180, 60, BOX_PURP, "Orchestrator", "the flow, in code", font_size=11)
    for i, (sx, sn) in enumerate([(72, "Payments"), (216, "Inventory"), (360, "Shipping")]):
        box(c, sx, y - 190, 160, 60, BOX_BLUE, sn, "", font_size=10)
        arrow(c, 306, y - 70, sx + 80, y - 130, color=ACCENT, width=1.6, label="cmd")
        arrow(c, sx + 100, y - 130, 316, y - 70, color=GREEN, width=1.2, label="evt")
    note(c, 72, y - 300, 468, "The flow is explicit and testable -- but the orchestrator is a coupling point and a scaling bottleneck.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Event Sourcing",
                       "Store the events, not the current state. State is a left-fold over history.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10)
    evs = ["#1 AccountOpened { owner }", "#2 Deposited { 500 }", "#3 Withdrew { 120 }", "#4 Deposited { 80 }"]
    yy = y
    for e in evs:
        c.drawString(72, yy - 20, e); yy -= 24
    arrow(c, 72, yy - 10, 200, yy - 10, color=ACCENT, width=2, label="replay")
    box(c, 230, yy - 46, 180, 60, BOX_GREEN, "Balance = 460", "derived, rebuildable", font_size=11)
    yy = bullet_list(c, 72, yy - 90,
        ["Audit trail for free: every state change is recorded with cause and time.",
         "Time travel: rebuild state as of any event. New projections from old events.",
         "Costs: event schema evolution, ever-growing log (snapshots bound replay), unfamiliar modeling."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "CQRS: Split Reads from Writes",
                       "One model to change the world, another to query it.")
    box(c, 72, y - 70, 225, 90, BOX_BLUE, "Write model", "commands, validation\nnormalized, strict", font_size=11)
    box(c, 315, y - 70, 225, 90, BOX_GREEN, "Read model", "denormalized views\nper query, fast", font_size=11)
    arrow(c, 297, y - 25, 313, y - 25, color=ACCENT, width=2, label="events")
    yy = bullet_list(c, 72, y - 200,
        ["Write side enforces invariants; read side is a materialized view built from its events.",
         "Reads and writes scale INDEPENDENTLY -- and the read model can be rebuilt from scratch.",
         "Do NOT start here: CQRS doubles your models. Earn it with real read/write asymmetry."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Pitfalls of Event-Driven Systems",
                       "The tax you pay for all that decoupling.")
    pits = [("Ordering", "events can arrive out of order -- design for it (versions, idempotency)", BOX_RED),
            ("Duplicates", "at-least-once delivery -- every handler must be idempotent", BOX_ORANGE),
            ("Schema evolution", "old events live forever -- version payloads, never break readers", BOX_BLUE),
            ("Observability", "correlate with causation IDs across services, or go blind", BOX_TEAL)]
    yy = y
    for name, desc, fill in pits:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Event-Driven Architecture — Remember",
                 ["Events are immutable facts (past tense); commands are requests one handler may reject.",
                  "Choreography decouples via reactions; orchestration centralizes the flow -- choreograph simple, orchestrate complex.",
                  "Event sourcing stores history and derives state; CQRS splits write and read models.",
                  "Every event handler must be idempotent and tolerant of out-of-order, duplicated events.",
                  "Version event schemas forever; trace with causation IDs or lose the plot."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 8. API Gateways
# =============================================================
def pdf_api_gateway(path):
    c = new_canvas(path); pg = 1
    title_page(c, "API Gateways\nVisual Guide",
               "One front door for your APIs:\nrouting, auth, limits, and aggregation.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "The Single Entry Point",
                       "Clients talk to the gateway; the gateway knows the service map.")
    box(c, 72, y - 70, 120, 64, BOX_BLUE, "Clients", "web/mobile", font_size=11)
    box(c, 246, y - 70, 120, 64, BOX_PURP, "Gateway", "routes", font_size=11)
    for i, (sx, sn) in enumerate([(72, "users"), (216, "orders"), (360, "search")]):
        box(c, sx, y - 200, 160, 60, BOX_GREEN, sn, "/api/" + sn, font_size=10)
        arrow(c, 306, y - 70, sx + 80, y - 140, color=ACCENT, width=1.6)
    arrow(c, 192, y - 38, 244, y - 38, color=ACCENT, width=2.5)
    note(c, 72, y - 310, 468, "Path-based (/api/orders/*), host-based (orders.api.com), or header-based routing -- one public surface, many backends.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Auth Termination at the Edge",
                       "Validate identity once; backends trust the gateway's verdict.")
    box(c, 72, y - 70, 130, 64, BOX_BLUE, "Client", "JWT", font_size=11)
    arrow(c, 202, y - 38, 244, y - 38, color=ACCENT, width=2, label="token")
    box(c, 246, y - 70, 150, 64, BOX_PURP, "Gateway", "verify signature\ncheck scopes", font_size=10)
    arrow(c, 396, y - 38, 438, y - 38, color=GREEN, width=2, label="X-User-Id")
    box(c, 440, y - 70, 100, 64, BOX_GREEN, "Service", "trusted", font_size=10)
    yy = bullet_list(c, 72, y - 170,
        ["Terminate TLS here, validate JWTs (JWKS), enforce OAuth2 scopes -- once, centrally.",
         "Forward identity as headers (X-User-Id, X-Roles); services stay dumb about auth.",
         "Central policy = one place to rotate keys, revoke tokens, and audit access."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Rate Limiting Protects Backends",
                       "The gateway is the bouncer: quotas per key, per route, per user.")
    box(c, 72, y - 80, 200, 80, BOX_GREEN, "Under quota", "200 OK\nX-RateLimit-Remaining: 42", font_size=10)
    box(c, 340, y - 80, 200, 80, BOX_RED, "Over quota", "429 Too Many Requests\nRetry-After: 60", font_size=10)
    yy = bullet_list(c, 72, y - 200,
        ["Tiers: free 100/min, pro 10k/min -- limits are a product feature and a cost control.",
         "Distributed counting (Redis) so every gateway replica enforces the same budget.",
         "Always return headers + Retry-After: a limit clients cannot see is a limit they will fight."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Request Aggregation",
                       "One client call becomes many backend calls -- merged at the edge.")
    box(c, 72, y - 70, 120, 64, BOX_BLUE, "Mobile", "1 request", font_size=11)
    arrow(c, 192, y - 38, 244, y - 38, color=ACCENT, width=2.5, label="fan-out")
    box(c, 246, y - 70, 120, 64, BOX_PURP, "Gateway", "parallel calls", font_size=10)
    for i, (sx, sn) in enumerate([(72, "user"), (216, "orders"), (360, "recs")]):
        box(c, sx, y - 200, 160, 60, BOX_GREEN, sn, "", font_size=10)
        arrow(c, 306, y - 70, sx + 80, y - 140, color=ACCENT, width=1.4)
    note(c, 72, y - 310, 468, "Cuts mobile round-trips (latency, battery) but the gateway now owns partial-failure semantics: fail whole or degrade?")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "BFF: Backend for Frontend",
                       "One tailored gateway per client type -- not one gateway to rule them all.")
    box(c, 72, y - 70, 140, 70, BOX_BLUE, "Web BFF", "rich payloads", font_size=11)
    box(c, 236, y - 70, 140, 70, BOX_GREEN, "Mobile BFF", "slim payloads", font_size=11)
    box(c, 400, y - 70, 140, 70, BOX_TEAL, "Partner BFF", "stable contract", font_size=11)
    for bx in [142, 306, 470]:
        arrow(c, bx, y - 70, bx, y - 110, color=ACCENT, width=1.8)
    box(c, 216, y - 200, 180, 60, BOX_ORANGE, "Services", "shared core", font_size=11)
    yy = bullet_list(c, 72, y - 290,
        ["Each BFF shapes data for its client's needs; teams evolve UI contracts independently.",
         "Cost: more services to run. Start with one gateway; split into BFFs when client needs truly diverge."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Cross-Cutting Superpowers",
                       "Everything every service needs, done once.")
    feats = [("Observability", "one place for access logs, tracing spans, metrics", BOX_TEAL),
             ("Caching", "cache GETs at the edge -- kill duplicate backend hits", BOX_GREEN),
             ("Transformation", "version translation: v1 clients, v2 services", BOX_BLUE),
             ("Resilience", "timeouts, retries, circuit breakers per route", BOX_ORANGE)]
    yy = y
    for name, desc, fill in feats:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Warning: the gateway is a single point of failure -- run it multi-AZ, keep its logic stateless.", fill=BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "API Gateways — Remember",
                 ["The gateway is the single public entry: routing, TLS, and a stable contract over many services.",
                  "Terminate auth at the edge -- validate tokens once, forward identity as headers.",
                  "Rate limit per key/route/user; communicate quotas with headers and 429 + Retry-After.",
                  "Aggregate backend calls for chatty clients; split into BFFs when client needs diverge.",
                  "Centralize logging, tracing, caching, and resilience -- but keep the gateway stateless and redundant."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 9. Service Mesh
# =============================================================
def pdf_service_mesh(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Service Mesh\nVisual Guide",
               "Networking as infrastructure:\nsidecars, mTLS, and traffic policy without code changes.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "The Sidecar Pattern",
                       "Every service instance gets a proxy roommate that owns its network.")
    for i, (px, sn) in enumerate([(72, "Service A"), (216, "Service B"), (360, "Service C")]):
        box(c, px, y - 110, 160, 90, BOX_BLUE, sn, "business logic", font_size=10)
        box(c, px + 18, y - 96, 124, 30, BOX_PURP, "sidecar proxy", "", font_size=8.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 240, "App code talks to localhost; the sidecar talks to the world. Zero library changes.")
    yy = bullet_list(c, 72, y - 270,
        ["Retries, timeouts, TLS, metrics -- all implemented once in the proxy, applied to every service.",
         "Cost: an extra hop per call (small latency), plus proxy CPU/memory per pod."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Envoy: The Data Plane",
                       "The proxy that actually moves bytes (Istio, Linkerd's linkerd2-proxy, and friends).")
    box(c, 72, y - 70, 130, 64, BOX_PURP, "Inbound", "listener", font_size=10)
    arrow(c, 202, y - 38, 234, y - 38, color=ACCENT, width=2)
    box(c, 236, y - 100, 140, 124, BOX_BLUE, "Envoy", "filters -> routes\n-> clusters -> TLS", font_size=10)
    arrow(c, 376, y - 38, 408, y - 38, color=ACCENT, width=2)
    box(c, 410, y - 70, 130, 64, BOX_PURP, "Outbound", "upstream", font_size=10)
    yy = bullet_list(c, 72, y - 250,
        ["Filter chain: auth, rate limit, transform -- then route by path/header to a cluster of endpoints.",
         "Outlier detection: Envoy ejects sick hosts automatically (passive circuit breaking).",
         "Hot-reloadable config: the control plane pushes new routes without dropping connections."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Istio: The Control Plane",
                       "The brain that programs ten thousand sidecars as one.")
    box(c, 216, y - 70, 180, 70, ACCENT, "istiod", "config + certs", font_size=11)
    for i, px in enumerate([72, 246, 420]):
        box(c, px, y - 210, 120, 60, BOX_PURP, f"proxy {i+1}", "", font_size=10)
        arrow(c, 306, y - 70, px + 60, y - 150, color=ACCENT, width=1.6, label="xDS")
    yy = bullet_list(c, 72, y - 300,
        ["xDS APIs stream config: listeners, routes, clusters, endpoints -- eventually consistent, fast.",
         "Citadel (now in istiod): issues and rotates workload certificates for mTLS.",
         "You declare INTENT (VirtualService, DestinationRule); the mesh compiles it to proxy config."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "mTLS: Zero-Trust Between Services",
                       "Every hop authenticated and encrypted -- identity from the platform, not passwords.")
    box(c, 72, y - 70, 150, 64, BOX_BLUE, "svc-a", "cert: spiffe://a", font_size=9.5)
    arrow(c, 222, y - 52, 318, y - 52, color=GREEN, width=2.5, label="mutual TLS")
    arrow(c, 318, y - 24, 222, y - 24, color=GREEN, width=2.5)
    box(c, 320, y - 70, 150, 64, BOX_GREEN, "svc-b", "cert: spiffe://b", font_size=9.5)
    yy = bullet_list(c, 72, y - 170,
        ["Both sides present certificates: no more 'internal network = trusted' thinking.",
         "AuthorizationPolicy: allow payments -> db ONLY from checkout -- enforced in the proxy.",
         "Permissive mode lets you migrate: plaintext today, strict mTLS tomorrow, per namespace."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Traffic Policies Without Deploys",
                       "Shift, split, and protect traffic by editing config.")
    pols = [("Canary", "v1 90% / v2 10% -- promote by weight, not by deploy", BOX_GREEN),
            ("Retries + timeouts", "retry 2x on 5xx, 3s timeout -- per route, in the mesh", BOX_BLUE),
            ("Circuit breaking", "max 100 concurrent to payments -- shed load before it cascades", BOX_ORANGE),
            ("Fault injection", "delay 10% of calls 2s -- chaos drills in production config", BOX_RED)]
    yy = y
    for name, desc, fill in pols:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Telemetry for Free",
                       "Every proxy emits the golden signals -- no instrumentation needed.")
    _row_of_boxes(c, y,
        [("Latency", "p50/p99 per route", BOX_BLUE),
         ("Traffic", "req/s per service", BOX_GREEN),
         ("Errors", "5xx rate, by source", BOX_RED),
         ("Saturation", "queue depth, cpu", BOX_ORANGE)])
    yy = bullet_list(c, 72, y - 130,
        ["Distributed tracing: the proxy propagates trace headers even if the app ignores them.",
         "Service graph: who calls whom, how often, how slowly -- generated from proxy telemetry.",
         "This is the mesh's killer app for many teams: observability without begging every team to instrument."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Service Mesh — Remember",
                 ["Sidecars own the network: app talks to localhost, the proxy handles retries, TLS, metrics.",
                  "Data plane (Envoy) moves bytes; control plane (istiod) programs all proxies via xDS.",
                  "mTLS gives every workload a cryptographic identity -- zero-trust inside the cluster.",
                  "Canary weights, retries, circuit breaking, and fault injection become config, not code.",
                  "Uniform proxy telemetry yields tracing and service graphs without per-team instrumentation."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 10. Circuit Breakers
# =============================================================
def pdf_circuit_breaker(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Circuit Breakers\nVisual Guide",
               "Fail fast instead of piling on:\nstates, thresholds, fallbacks, and bulkheads.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Cascading Failures",
                       "A slow dependency turns every caller into a queue of doomed threads.")
    box(c, 72, y - 70, 130, 64, BOX_BLUE, "API", "", font_size=11)
    arrow(c, 202, y - 38, 244, y - 38, color=ACCENT, width=2.5, label="calls pile up")
    box(c, 246, y - 70, 130, 64, BOX_RED, "Slow DB", "30s timeouts", font_size=11)
    box(c, 420, y - 70, 120, 64, BOX_RED, "API dies", "thread pool\nexhausted", font_size=10)
    arrow(c, 376, y - 38, 418, y - 38, color=RED, width=2.5)
    note(c, 72, y - 180, 468, "The caller's threads block waiting; new requests queue behind them. One slow service kills the healthy ones.", fill=BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "CLOSED: Normal Operation",
                       "Requests flow; the breaker counts failures in a rolling window.")
    box(c, 72, y - 70, 150, 70, BOX_GREEN, "CLOSED", "traffic flows", font_size=12)
    arrow(c, 222, y - 35, 254, y - 35, color=ACCENT, width=2.5, label="requests")
    box(c, 256, y - 70, 150, 70, BOX_BLUE, "Dependency", "ok / fail", font_size=11)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 180, "Failure counter: 5 failures in 10s (or 50% of 20 requests) -> TRIP the breaker.")
    yy = bullet_list(c, 72, y - 210,
        ["Thresholds need volume minimums: 2 failures out of 2 requests should NOT trip (noise).",
         "Rolling window (not cumulative): old failures age out; recovery is possible."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "OPEN: Fail Fast",
                       "The breaker rejects calls immediately -- no doomed threads.")
    box(c, 72, y - 70, 150, 70, BOX_RED, "OPEN", "reject instantly", font_size=12)
    arrow(c, 222, y - 35, 254, y - 35, color=RED, width=2.5, label="blocked")
    box(c, 256, y - 70, 150, 70, BOX_ORANGE, "Fallback", "cached / default", font_size=11)
    yy = bullet_list(c, 72, y - 180,
        ["Fail fast in milliseconds instead of waiting out a 30s timeout -- threads stay free.",
         "Serve the fallback: stale cache, default value, degraded feature -- 'something' beats 'nothing'.",
         "Stay open for a cooldown (e.g. 30s): hammering a sick service during recovery kills it again."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "HALF-OPEN: Probing Recovery",
                       "After cooldown, let a trickle through to test the waters.")
    box(c, 72, y - 70, 150, 70, BOX_ORANGE, "HALF-OPEN", "probe requests", font_size=11)
    arrow(c, 222, y - 35, 254, y - 35, color=ORANGE, width=2.5, label="1 probe")
    box(c, 256, y - 70, 150, 70, BOX_BLUE, "Dependency", "healthy?", font_size=11)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 180, "Probe succeeds -> CLOSED (resume). Probe fails -> OPEN (another cooldown).")
    note(c, 72, y - 260, 468, "Limit probes to ONE at a time: ten half-open callers each sending a probe is still a stampede.", fill=BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Fallbacks: Graceful Degradation",
                       "Decide in advance what 'broken but useful' looks like.")
    fbs = [("Cached", "serve last-known-good data with a 'stale' badge", BOX_GREEN),
           ("Default", "empty recommendations, static content -- the page still renders", BOX_BLUE),
           ("Degraded", "disable the feature flag; core flow keeps working", BOX_ORANGE),
           ("Fail loudly", "when there is no safe default: clear error, fast", BOX_RED)]
    yy = y
    for name, desc, fill in fbs:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Bulkheads + Retry Discipline",
                       "Breakers stop the pile-up; bulkheads and retries stop the spark.")
    box(c, 72, y - 90, 225, 100, BOX_TEAL, "Bulkhead", "separate thread pools\nper dependency", font_size=11)
    box(c, 315, y - 90, 225, 100, BOX_PURP, "Retry", "backoff + jitter\nmax 2-3 tries", font_size=11)
    yy = bullet_list(c, 72, y - 230,
        ["Bulkhead (the ship metaphor): a flooded compartment cannot sink the ship -- cap each dependency's threads.",
         "Retry ONLY idempotent ops, with exponential backoff AND jitter (no synchronized retry storms).",
         "Retry budgets: cap retries at ~10% of traffic so a sick dependency is not drowned in retries.",
         "Layer them: retry (brief) -> breaker (sustained) -> bulkhead (isolation) -> fallback (UX)."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Circuit Breakers — Remember",
                 ["Cascading failures happen when callers queue behind a slow dependency -- breakers fail fast instead.",
                  "CLOSED counts failures in a rolling window; trip on rate + minimum volume, not on noise.",
                  "OPEN rejects instantly and serves fallbacks; HALF-OPEN probes with a single request before resuming.",
                  "Design fallbacks up front: cached, default, degraded, or a fast honest error.",
                  "Combine with bulkheads (isolated pools) and jittered, budgeted retries for full resilience."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 11. Rate Limiting
# =============================================================
def pdf_rate_limiting(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Rate Limiting\nVisual Guide",
               "Protect shared resources:\nbuckets, windows, distributed counters, and headers.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Why Limit",
                       "Every shared resource has a capacity; limits turn overload into a polite 'no'.")
    _row_of_boxes(c, y,
        [("Fairness", "one user cannot starve others", BOX_BLUE),
         ("Protection", "survive abuse & bugs", BOX_RED),
         ("Cost", "API calls = money", BOX_GREEN),
         ("Product", "tiers: free vs paid", BOX_ORANGE)])
    note(c, 72, y - 160, 468, "Limit at the EDGE (gateway/CDN) so rejected traffic never reaches expensive backends.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Token Bucket",
                       "Tokens refill over time; each request spends one. Bursts allowed up to bucket size.")
    box(c, 72, y - 110, 200, 110, BOX_BLUE, "Bucket", "capacity 10\nrefill 2/sec", font_size=11)
    for i in range(5):
        c.setFillColor(ACCENT); c.circle(110 + i * 26, y - 60, 9, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(300, y - 40, "request arrives:")
    c.drawString(300, y - 62, "- token available -> allow, remove token")
    c.drawString(300, y - 84, "- bucket empty -> reject (429)")
    c.drawString(300, y - 120, "Steady rate 2/sec, but a burst of 10 passes instantly.")
    yy = bullet_list(c, 72, y - 180,
        ["Two knobs: RATE (sustained) and BURST (bucket size) -- tune them separately.",
         "The classic for APIs: friendly to bursty human traffic, strict on sustained abuse."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Leaky Bucket",
                       "Requests queue and drain at a FIXED rate -- smooth output, no bursts downstream.")
    box(c, 72, y - 110, 200, 110, BOX_TEAL, "Bucket", "queue\nleak 2/sec", font_size=11)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(300, y - 40, "burst of 20 arrives:")
    c.drawString(300, y - 62, "- queued, drained at exactly 2/sec")
    c.drawString(300, y - 84, "- queue full -> reject the excess")
    c.drawString(300, y - 120, "Use when the CONSUMER needs smooth flow (webhooks, worker queues).")
    note(c, 72, y - 210, 468, "Token bucket shapes the SENDER (allow bursts); leaky bucket shapes the RECEIVER (enforce smooth).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Fixed vs Sliding Window",
                       "Counting requests per time window -- watch the boundary.")
    box(c, 72, y - 90, 225, 100, BOX_RED, "Fixed window", "100/min per key\nspike at :59 + :01 = 200", font_size=10.5)
    box(c, 315, y - 90, 225, 100, BOX_GREEN, "Sliding window", "last 60s rolling\nno boundary spike", font_size=10.5)
    yy = bullet_list(c, 72, y - 230,
        ["Fixed window flaw: 100 requests at 12:00:59 + 100 at 12:01:01 = 200 in 2 seconds, all 'allowed'.",
         "Sliding window log: exact, but stores every timestamp. Sliding window counter: approximate, cheap (Redis-friendly).",
         "Fixed windows are fine for coarse quotas (per-day API plans); use sliding for per-second protection."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Distributed Limiting with Redis",
                       "One counter per key, shared by all gateway replicas.")
    box(c, 72, y - 70, 130, 64, BOX_BLUE, "Gateway 1", "", font_size=10)
    box(c, 216, y - 70, 130, 64, BOX_BLUE, "Gateway 2", "", font_size=10)
    box(c, 360, y - 70, 130, 64, BOX_BLUE, "Gateway 3", "", font_size=10)
    box(c, 216, y - 200, 130, 64, BOX_RED, "Redis", "INCR + EXPIRE", font_size=10)
    for gx in [137, 281, 425]:
        arrow(c, gx, y - 70, 281, y - 136, color=ACCENT, width=1.4)
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, y - 300, "count = INCR rl:{user}:{minute}  |  EXPIRE ... 60  |  allow if count <= 100")
    note(c, 72, y - 380, 468, "Lua script the check+increment atomically. For huge scale, shard counters or accept approximate local limits.", fill=BOX_TEAL)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Communicate the Limit",
                       "A limit clients can see is a limit they respect.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10)
    c.drawString(72, y - 30, "X-RateLimit-Limit: 100")
    c.drawString(72, y - 52, "X-RateLimit-Remaining: 37")
    c.drawString(72, y - 74, "X-RateLimit-Reset: 1718006400")
    c.drawString(72, y - 108, "429 Too Many Requests")
    c.drawString(72, y - 130, "Retry-After: 42")
    yy = bullet_list(c, 72, y - 170,
        ["Send quota headers on EVERY response, not just rejections -- clients budget proactively.",
         "429 + Retry-After is the contract; exponential backoff on the client completes it.",
         "Log rejections per key: your best abuse-detection signal lives in the 429 stream."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Rate Limiting — Remember",
                 ["Limit at the edge for fairness, protection, cost control, and tiered products.",
                  "Token bucket: refill over time, allows bursts up to capacity -- the API classic.",
                  "Leaky bucket: fixed drain rate, smooths bursts -- for consumers that need steady flow.",
                  "Fixed windows spike at boundaries; sliding windows cost more but stay accurate.",
                  "Share counters in Redis (atomic Lua), and always tell clients the quota via headers + 429."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 12. Saga Pattern
# =============================================================
def pdf_saga_pattern(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Saga Pattern\nVisual Guide",
               "Distributed transactions without 2PC:\nsequences, compensation, and failure handling.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Why Not 2PC",
                       "Two-phase commit locks every participant until ALL agree -- across services, that blocks.")
    box(c, 72, y - 90, 225, 110, BOX_RED, "2PC", "prepare: lock rows\ncommit: apply\nlocks held throughout", font_size=10.5)
    box(c, 315, y - 90, 225, 110, BOX_GREEN, "Saga", "local txn + event\nnext step starts\nnothing locks globally", font_size=10.5)
    yy = bullet_list(c, 72, y - 230,
        ["2PC across microservices: one slow participant holds everyone's locks; a coordinator crash blocks everything.",
         "Saga insight: each step commits its LOCAL transaction immediately, then triggers the next step.",
         "Atomicity becomes 'all steps complete OR all completed steps are undone' -- via compensation."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "The Saga Sequence",
                       "A trip booking: each step commits locally and publishes an event.")
    steps = [("Book flight", BOX_BLUE), ("Book hotel", BOX_GREEN),
             ("Charge card", BOX_ORANGE), ("Confirm trip", BOX_TEAL)]
    _row_of_boxes(c, y, [(s, "local txn", f) for s, f in steps])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 120, "flight OK -> hotel OK -> card OK -> confirm. Each arrow is an event; each box already committed.")
    note(c, 72, y - 200, 468, "There is no isolation between steps: other transactions can SEE the booked flight before the trip confirms.", fill=BOX_ORANGE)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Choreography Saga",
                       "Services listen for events and run their step -- no central brain.")
    box(c, 72, y - 70, 140, 60, BOX_BLUE, "Flight svc", "on Start -> book", font_size=10)
    box(c, 240, y - 70, 140, 60, BOX_GREEN, "Hotel svc", "on FlightBooked", font_size=10)
    box(c, 400, y - 70, 140, 60, BOX_ORANGE, "Card svc", "on HotelBooked", font_size=10)
    arrow(c, 212, y - 40, 238, y - 40, color=ACCENT, width=1.8, label="FlightBooked")
    arrow(c, 380, y - 40, 398, y - 40, color=ACCENT, width=1.8, label="HotelBooked")
    yy = bullet_list(c, 72, y - 170,
        ["Pros: no orchestrator to build or scale; services stay autonomous.",
         "Cons: the saga's logic is scattered -- 'what happens after hotel fails?' lives in five codebases.",
         "Cyclic risk: A listens to B listens to A -- draw the event graph or it will surprise you."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Orchestration Saga",
                       "One coordinator runs the script: command, wait, decide.")
    box(c, 216, y - 70, 180, 60, BOX_PURP, "Saga orchestrator", "state machine", font_size=11)
    for i, (sx, sn) in enumerate([(72, "Flight"), (216, "Hotel"), (360, "Card")]):
        box(c, sx, y - 190, 160, 60, BOX_BLUE, sn, "", font_size=10)
        arrow(c, 306, y - 70, sx + 80, y - 130, color=ACCENT, width=1.6, label="cmd")
        arrow(c, sx + 100, y - 130, 316, y - 70, color=GREEN, width=1.2, label="ok/fail")
    yy = bullet_list(c, 72, y - 280,
        ["The flow is explicit code: easy to read, test, and reason about failures.",
         "The orchestrator holds saga STATE (durable: survive its own crash -- use a workflow engine).",
         "Temporal / Camunda / AWS Step Functions exist so you do not hand-roll this state machine."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Compensating Actions",
                       "You cannot roll back a committed local txn -- you run its semantic UNDO.")
    box(c, 72, y - 70, 200, 70, BOX_GREEN, "book_flight()", "forward action", font_size=11)
    arrow(c, 272, y - 35, 304, y - 35, color=ACCENT, width=2, label="pairs with")
    box(c, 306, y - 70, 200, 70, BOX_RED, "cancel_flight()", "compensating action", font_size=11)
    yy = bullet_list(c, 72, y - 180,
        ["Every step needs a compensating twin: charge -> refund, reserve -> release, send email -> send correction.",
         "Compensation runs BACKWARD through completed steps (LIFO): undo card, then hotel, then flight.",
         "Some actions are un-compensatable (email sent) -- design forward recovery or human steps for those."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Failure Handling",
                       "Step 3 of 5 fails. Now what?")
    box(c, 72, y - 70, 150, 64, BOX_GREEN, "Steps 1-2", "committed", font_size=11)
    box(c, 246, y - 70, 150, 64, BOX_RED, "Step 3", "FAILED", font_size=11)
    box(c, 420, y - 70, 120, 64, BOX_ORANGE, "Steps 4-5", "never ran", font_size=10)
    yy = bullet_list(c, 72, y - 170,
        ["Backward recovery: run compensations for steps 1-2 (the classic rollback).",
         "Forward recovery: retry step 3, or reroute (book a different hotel) and continue.",
         "Make every action IDEMPOTENT: compensations and retries will execute more than once.",
         "Durable saga log: record each step's outcome so a crashed orchestrator resumes, never restarts."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Saga Pattern — Remember",
                 ["Sagas replace 2PC's global locks with local transactions chained by events or commands.",
                  "Choreography: services react to events (decoupled, scattered logic). Orchestration: a coordinator runs the script.",
                  "Committed steps cannot roll back -- each needs a compensating action that semantically undoes it.",
                  "On failure: compensate backward (undo) or recover forward (retry/reroute); make everything idempotent.",
                  "Durably log saga state -- the orchestrator must survive its own crash mid-saga."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 13. Consensus: Paxos & Raft
# =============================================================
def pdf_consensus(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Consensus: Paxos & Raft\nVisual Guide",
               "Getting unreliable machines to agree:\nelections, logs, and quorums.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "The Agreement Problem",
                       "N machines, some may crash, messages may delay: still pick ONE value.")
    for i, px in enumerate([72, 246, 420]):
        box(c, px, y - 90, 120, 70, BOX_BLUE, f"Node {i+1}", "proposes?", font_size=10)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 200, "Without consensus: split-brain -- two 'leaders', divergent data, silent corruption.")
    yy = bullet_list(c, 72, y - 230,
        ["FLP impossibility: in a fully async network, no deterministic algorithm guarantees consensus -- so real systems add",
         "timeouts/randomization (Raft) or stable leadership to make agreement practical.",
         "Safety (never disagree) is non-negotiable; liveness (eventually decide) is best-effort."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Raft: Leader Election",
                       "Terms, votes, and the rule that only one leader wins a term.")
    box(c, 72, y - 70, 120, 64, BOX_ORANGE, "Candidate", "term 5\nvote for me", font_size=10)
    box(c, 246, y - 70, 120, 64, BOX_GREEN, "Voter", "grants vote", font_size=10)
    box(c, 420, y - 70, 120, 64, BOX_GREEN, "Voter", "grants vote", font_size=10)
    arrow(c, 192, y - 38, 244, y - 38, color=ACCENT, width=2, label="RequestVote")
    yy = bullet_list(c, 72, y - 170,
        ["Election timeout (randomized 150-300ms): followers who hear nothing become candidates -- randomization prevents ties.",
         "One vote per node per term; majority wins. A new leader's first act: establish authority (no-op log entry).",
         "Leaders send heartbeats; a partitioned old leader steps down when it sees a higher term."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Raft: Log Replication",
                       "The leader's log is truth; followers copy it entry by entry.")
    box(c, 216, y - 70, 180, 60, ACCENT, "Leader", "append entry", font_size=11)
    for i, px in enumerate([72, 246, 420]):
        box(c, px, y - 190, 120, 60, BOX_BLUE, f"F{i+1}", "[1][2][3]", font_size=10)
        arrow(c, 306, y - 70, px + 60, y - 130, color=ACCENT, width=1.6, label="AppendEntries")
    yy = bullet_list(c, 72, y - 280,
        ["Entries carry (term, index): followers reject appends that do not match their log prefix -- logs stay identical.",
         "Commit rule: an entry is COMMITTED once a majority has it; then the leader applies it and tells followers.",
         "Leader completeness: any elected leader holds all committed entries -- committed data is never lost."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Quorums: Majorities Decide",
                       "With 2f+1 nodes, any two majorities overlap -- that overlap is the safety.")
    for i, px in enumerate([72, 187, 302, 417]):
        box(c, px, y - 80, 100, 64, BOX_GREEN if i < 3 else BOX_BLUE, f"N{i+1}", "", font_size=10)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 180, "5 nodes tolerate 2 failures. Write needs 3 acks; election needs 3 votes.")
    yy = bullet_list(c, 72, y - 210,
        ["Majority intersection: no two majorities can disagree, so no two leaders commit conflicting entries.",
         "Even node counts are wasteful: 4 nodes tolerate 1 failure, same as 3 -- always use odd cluster sizes.",
         "Witness/arbiter nodes vote without storing data -- cheap quorum members."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Paxos: Roles and Phases",
                       "The classic: proposers, acceptors, learners -- two phases to agree on one value.")
    _row_of_boxes(c, y,
        [("Proposers", "suggest values", BOX_BLUE),
         ("Acceptors", "vote, quorum", BOX_GREEN),
         ("Learners", "learn outcome", BOX_TEAL)])
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 130, "Phase 1 (prepare): proposer asks acceptors to promise. Phase 2 (accept): proposer sends the value.")
    yy = bullet_list(c, 72, y - 160,
        ["Promise rule: acceptors ignore lower-numbered proposals -- the highest proposal always wins cleanly.",
         "Multi-Paxos: elect a stable leader once, then skip phase 1 -- this is what Raft essentially streamlined.",
         "Paxos is the theory; Raft is Paxos made teachable. Same safety, friendlier story."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Where Consensus Lives",
                       "You rarely implement it -- you operate systems built on it.")
    uses = [("etcd", "Raft; Kubernetes' brain -- every cluster state change is a consensus round", BOX_BLUE),
            ("ZooKeeper", "ZAB (Paxos-like); config, locks, leader election", BOX_GREEN),
            ("CockroachDB / TiKV", "Raft per range/shard -- consensus at data scale", BOX_ORANGE),
            ("Blockchains", "BFT consensus -- agreement with ADVERSARIES, not just crashes", BOX_RED)]
    yy = y
    for name, desc, fill in uses:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Consensus: Paxos & Raft — Remember",
                 ["Consensus lets crash-prone machines agree on one value; safety (never disagree) beats liveness.",
                  "Raft elects a leader per term by majority vote; randomized timeouts prevent election ties.",
                  "The leader replicates its log; an entry commits once a majority holds it -- committed = durable.",
                  "Majority quorums intersect, so conflicting decisions cannot both commit; use odd cluster sizes.",
                  "Paxos (proposers/acceptors/learners) is the theory; Raft is the operable telling; etcd/ZooKeeper run your world on it."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 14. Vector Clocks
# =============================================================
def pdf_vector_clocks(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Vector Clocks\nVisual Guide",
               "Track causality without a global clock:\nhappens-before, concurrency, and conflict resolution.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "No Global Clock",
                       "Wall clocks skew; NTP lies by milliseconds. Ordering needs something else.")
    box(c, 72, y - 70, 150, 64, BOX_BLUE, "Node A", "10:00:01", font_size=11)
    box(c, 390, y - 70, 150, 64, BOX_BLUE, "Node B", "10:00:00?", font_size=11)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(306, y - 38, "whose write was first?")
    yy = bullet_list(c, 72, y - 170,
        ["Two writes 'one millisecond apart' on different machines prove nothing -- clocks disagree by more than that.",
         "Lamport's insight: track CAUSALITY (did X know about Y?), not wall time.",
         "Vector clocks: one counter per node -- a version stamp that captures 'who has seen what'."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "The Vector",
                       "Each node keeps [A, B, C]: its own counter plus the latest it has seen from others.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 12)
    c.drawString(72, y - 40, "A writes:  [1, 0, 0]      B writes:  [0, 1, 0]")
    c.drawString(72, y - 70, "A sees B's write, then writes:  [2, 1, 0]")
    yy = bullet_list(c, 72, y - 110,
        ["Rule: on a local event, increment YOUR counter. On receiving, take max of each position, then increment yours.",
         "The vector is a summary of causal history: '[2,1,0]' means 'I have seen 2 of A's events and 1 of B's'.",
         "No coordinator, no synchronized clocks -- just counters piggybacked on every message."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Happens-Before",
                       "Compare vectors position by position -- the dominance rule.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 11)
    c.drawString(72, y - 40, "V1 = [1, 0, 0]   V2 = [2, 1, 0]")
    c.setFillColor(GREEN); c.setFont(BODY_FONT, 11)
    c.drawString(72, y - 66, "V1 < V2 on EVERY position  =>  V1 happened-before V2")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 100, "V2's author had seen V1's event: V2 causally follows V1. Safe to overwrite -- no conflict.")
    note(c, 72, y - 190, 468, "If every counter in V1 is at most V2's, with at least one strictly smaller, V1 precedes V2. The later write wins legitimately.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Detecting Concurrent Updates",
                       "Neither vector dominates: the writes are concurrent -- a real conflict.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 11)
    c.drawString(72, y - 40, "V1 = [1, 0, 0]   V2 = [0, 1, 0]")
    c.setFillColor(RED); c.setFont(BODY_FONT, 11)
    c.drawString(72, y - 66, "V1 not <= V2, V2 not <= V1  =>  CONCURRENT")
    yy = bullet_list(c, 72, y - 100,
        ["Neither author saw the other's write: both updated from the same ancestor independently.",
         "The system CANNOT pick a winner -- timestamps would just be guessing.",
         "Honest answer: keep BOTH versions (siblings) and let the reader reconcile."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Dynamo-Style Conflict Resolution",
                       "Return siblings; the client merges and writes back the resolution.")
    box(c, 72, y - 70, 130, 64, BOX_BLUE, "Replica", "[1,0,0]", font_size=10)
    box(c, 246, y - 70, 130, 64, BOX_BLUE, "Replica", "[0,1,0]", font_size=10)
    arrow(c, 202, y - 38, 244, y - 38, color=ACCENT, width=1.6)
    box(c, 420, y - 70, 120, 64, BOX_ORANGE, "Client", "gets BOTH", font_size=10)
    arrow(c, 376, y - 38, 418, y - 38, color=ACCENT, width=1.6, label="siblings")
    yy = bullet_list(c, 72, y - 170,
        ["Read returns both versions with their vectors: the app (or user) merges them.",
         "Merged write carries a vector dominating both ([2,2,0]-style): descendants subsume ancestors.",
         "Shopping cart: union the items. Last-writer-wins is a policy choice -- vector clocks just expose the truth."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Costs and Limits",
                       "Vectors grow with the cluster -- and never shrink on their own.")
    yy = bullet_list(c, 72, y,
        ["Size: one counter per node EVER -- 1000 nodes = 1000 counters on every version stamp.",
         "Pruning: drop entries for dead nodes (risky) or use dotted version vectors (one entry per writer).",
         "Do not confuse with version NUMBERS: a single integer cannot detect concurrency -- that is the whole point.",
         "Modern use: DynamoDB, Riak, Cassandra (lightly), and CRDT metadata -- anywhere merges must be honest."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Vector Clocks — Remember",
                 ["Wall clocks cannot order distributed events; vector clocks track causality with per-node counters.",
                  "Increment yours locally; merge with max on receive -- the vector summarizes causal history.",
                  "V1 <= V2 everywhere means V1 happened-before V2 (safe overwrite); otherwise the writes are concurrent.",
                  "Concurrent writes become siblings: return both, let the reader merge, write back a dominating vector.",
                  "Vectors grow with cluster size -- prune carefully or use dotted versions."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 15. Bloom Filters
# =============================================================
def pdf_bloom_filters(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Bloom Filters\nVisual Guide",
               "Ask 'is it in the set?' in constant memory:\nbits, hashes, and honest false positives.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "The Membership Question",
                       "Billions of keys, megabytes of RAM: 'have we seen this?' without storing it.")
    box(c, 72, y - 80, 225, 90, BOX_RED, "HashSet", "stores every key\nGBs of RAM", font_size=11)
    box(c, 315, y - 80, 225, 90, BOX_GREEN, "Bloom filter", "bit array\nKBs of RAM", font_size=11)
    yy = bullet_list(c, 72, y - 200,
        ["Use when: the SET is huge, memory is scarce, and 'maybe' is an acceptable first answer.",
         "The deal: 'definitely not' is certain; 'probably yes' needs a (rare) double-check against the real store."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Bit Array + k Hashes",
                       "Add: hash the item k times, set those bits. Query: check those bits.")
    nbits = 18
    bx, by, bs = 72, y - 90, 24
    for i in range(nbits):
        c.setFillColor(BOX_BLUE); c.rect(bx + i * (bs + 2), by, bs, bs, fill=1, stroke=0)
        c.setStrokeColor(INK); c.setLineWidth(0.8); c.rect(bx + i * (bs + 2), by, bs, bs, fill=0, stroke=1)
    for i in [2, 7, 13]:
        c.setFillColor(ACCENT); c.rect(bx + i * (bs + 2), by, bs, bs, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 130, "add('apple'): h1=2, h2=7, h3=13 -> set bits 2, 7, 13")
    c.drawString(72, y - 152, "query('apple'): bits 2,7,13 all set -> PRESENT (maybe)")
    c.drawString(72, y - 174, "query('mango'): bit 5 unset -> ABSENT (certain)")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "False Positives, Never False Negatives",
                       "Bits set by OTHER items can fake a 'present' -- but an unset bit never lies.")
    box(c, 72, y - 90, 225, 100, BOX_RED, "False positive", "'mango' hashes to bits\nset by apple+pear\n-> wrong 'maybe'", font_size=10.5)
    box(c, 315, y - 90, 225, 100, BOX_GREEN, "Never false negative", "any unset bit\n-> definitely absent\n-> mathematically certain", font_size=10.5)
    yy = bullet_list(c, 72, y - 230,
        ["Adding never UNSETS bits, so a true member's bits are always all set: negatives are impossible to miss.",
         "False positive rate is tunable: more bits per item and optimal k drive it down exponentially.",
         "Design pattern: bloom says 'maybe' -> check the database; bloom says 'no' -> skip the I/O entirely."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Sizing Math",
                       "Two knobs: bits per item (m/n) and hash count (k).")
    c.setFillColor(INK); c.setFont(MONO_FONT, 11)
    c.drawString(72, y - 40, "p ~= (1 - e^(-k*n/m))^k        k_opt = (m/n) * ln 2")
    yy = bullet_list(c, 72, y - 80,
        ["m/n = bits per element. 10 bits/item with optimal k ~= 7 -> p ~= 1% false positives.",
         "Want 0.1%? Use ~15 bits/item. 1% is plenty for 'skip a disk read'.",
         "Rule of thumb: 10 bits per item, k=7 -- memorize it, it covers most designs.",
         "k too HIGH: you fill the array faster (more FPs). k too LOW: you do not use the bits well."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Cassandra and BigTable Use",
                       "One bloom filter per SSTable: skip disk reads for keys that are not there.")
    box(c, 72, y - 70, 130, 64, BOX_BLUE, "Query", "key K", font_size=11)
    for i, sx in enumerate([246, 396]):
        box(c, sx, y - 70, 120, 64, BOX_ORANGE, f"SSTable {i+1}", "bloom: no", font_size=10)
    arrow(c, 202, y - 52, 244, y - 52, color=RED, width=2, label="skip")
    arrow(c, 202, y - 24, 394, y - 24, color=RED, width=2, label="skip")
    box(c, 246, y - 190, 150, 60, BOX_GREEN, "Memtable", "bloom: maybe -> read", font_size=10)
    arrow(c, 202, y - 100, 300, y - 130, color=GREEN, width=2, label="maybe")
    note(c, 72, y - 300, 468, "A read touches MANY SSTables; without blooms every read fans out to disk. Blooms make misses nearly free.", fill=BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Beyond the Classic",
                       "When you need deletes, counting, or fewer hashes.")
    exts = [("Counting Bloom", "counters instead of bits -- decrement on delete (4x memory)", BOX_BLUE),
            ("Cuckoo filter", "supports delete, smaller for low FP rates, needs bucketed table", BOX_GREEN),
            ("Quotient filter", "cache-friendly, mergeable -- for LSM-tree metadata", BOX_TEAL),
            ("XOR filter", "static sets only, but ~1.23x smaller and faster than Bloom", BOX_ORANGE)]
    yy = y
    for name, desc, fill in exts:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Bloom Filters — Remember",
                 ["A bit array + k hashes answers set membership in tiny constant memory.",
                  "False positives are possible and tunable; false negatives are impossible by construction.",
                  "Size it: ~10 bits/item and k=7 gives ~1% false positives -- the standard recipe.",
                  "LSM stores keep one filter per SSTable so reads skip disk for absent keys.",
                  "Need deletes or smaller footprints? Counting Bloom, Cuckoo, and XOR filters extend the idea."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 16. LSM Trees
# =============================================================
def pdf_lsm_trees(path):
    c = new_canvas(path); pg = 1
    title_page(c, "LSM Trees\nVisual Guide",
               "Log-Structured Merge trees:\nturn random writes into sequential ones.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "The Write Problem",
                       "B-trees do random disk writes per update -- disks (and SSDs) hate random writes.")
    box(c, 72, y - 90, 225, 100, BOX_RED, "B-tree write", "seek + rewrite page\nrandom I/O per update", font_size=11)
    box(c, 315, y - 90, 225, 100, BOX_GREEN, "LSM write", "append to log\nsequential I/O only", font_size=11)
    yy = bullet_list(c, 72, y - 230,
        ["Sequential writes are 10-100x faster than random ones on spinning disks -- and kinder to SSDs.",
         "LSM insight: buffer writes in memory, then flush them to disk as big SORTED chunks.",
         "Trade-off accepted: reads get harder (check several places) to make writes blazing fast."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "The Memtable",
                       "An in-memory sorted structure (skiplist): all writes land here first.")
    box(c, 72, y - 110, 200, 110, BOX_BLUE, "Memtable", "sorted skiplist\nkey -> value", font_size=11)
    box(c, 300, y - 110, 200, 110, BOX_ORANGE, "WAL", "write-ahead log\ncrash recovery", font_size=11)
    arrow(c, 272, y - 55, 298, y - 55, color=ACCENT, width=2, label="log first")
    yy = bullet_list(c, 72, y - 250,
        ["Write path: append to WAL (durability), insert into memtable (speed). Both are sequential/in-memory.",
         "Reads check the memtable FIRST -- the freshest data lives here.",
         "When the memtable fills (e.g. 64MB), it freezes and a new empty one takes over."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Immutable SSTables",
                       "Frozen memtables flush to disk as Sorted String Tables -- never modified again.")
    box(c, 72, y - 80, 140, 70, BOX_BLUE, "Memtable", "frozen", font_size=11)
    arrow(c, 212, y - 45, 244, y - 45, color=ACCENT, width=2.5, label="flush")
    box(c, 246, y - 80, 140, 70, BOX_GREEN, "SSTable", "sorted, immutable\n+ bloom filter", font_size=10)
    yy = bullet_list(c, 72, y - 190,
        ["Immutability is the superpower: no locks, no torn writes, trivially cacheable and shareable.",
         "Each SSTable carries an index + bloom filter: 'is key K in this file?' without reading it.",
         "Deletes are tombstones: a marker 'K deleted' that shadows older copies until compaction."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Compaction",
                       "Merge SSTables, drop overwritten keys and tombstones, keep levels tidy.")
    box(c, 72, y - 70, 130, 60, BOX_ORANGE, "L0 file", "K=3 (old)", font_size=10)
    box(c, 216, y - 70, 130, 60, BOX_ORANGE, "L0 file", "K=3 (new)", font_size=10)
    arrow(c, 202, y - 40, 214, y - 40, color=ACCENT, width=1.8)
    box(c, 372, y - 70, 130, 60, BOX_GREEN, "L1 file", "K=3 (newest)\nold dropped", font_size=10)
    arrow(c, 346, y - 40, 370, y - 40, color=GREEN, width=2, label="merge")
    yy = bullet_list(c, 72, y - 170,
        ["Levels grow 10x per level (L0 -> L1 -> L2): deeper levels hold older, larger, fully-sorted runs.",
         "Compaction is background I/O: it costs write amplification (rewriting data) to buy read speed.",
         "Leveled (RocksDB) vs tiered (Cassandra STCS): fewer, bigger merges vs many small ones."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "The Read Path",
                       "Newest first: memtable, then L0, then deeper levels -- first hit wins.")
    box(c, 72, y - 70, 110, 60, BOX_BLUE, "Memtable", "", font_size=10)
    arrow(c, 182, y - 40, 204, y - 40, color=ACCENT, width=1.8, label="miss")
    box(c, 206, y - 70, 110, 60, BOX_ORANGE, "L0", "", font_size=10)
    arrow(c, 316, y - 40, 338, y - 40, color=ACCENT, width=1.8, label="miss")
    box(c, 340, y - 70, 110, 60, BOX_GREEN, "L1..Ln", "", font_size=10)
    yy = bullet_list(c, 72, y - 170,
        ["Tombstones checked at every level: a delete marker shadows the old value until compacted away.",
         "Bloom filters short-circuit most levels: 'definitely not here' without touching disk.",
         "Read amplification is the LSM tax: one logical read may probe several files."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "LevelDB and RocksDB",
                       "The engines that made LSM the default for write-heavy stores.")
    uses = [("LevelDB", "Google's embeddable LSM (2011) -- the reference design", BOX_BLUE),
            ("RocksDB", "Meta's fork: tuned for SSDs, multi-threaded compaction, column families", BOX_GREEN),
            ("Cassandra / ScyllaDB", "LSM per node + distributed layer -- planet-scale writes", BOX_ORANGE),
            ("CockroachDB (Pebble)", "RocksDB-inspired Go engine under a distributed SQL layer", BOX_TEAL)]
    yy = y
    for name, desc, fill in uses:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "LSM Trees — Remember",
                 ["LSMs turn random writes into sequential ones: buffer in a memtable, flush sorted SSTables.",
                  "WAL first for durability; frozen memtables flush immutable -- locks disappear from the write path.",
                  "Compaction merges levels, drops overwritten keys and tombstones, at the cost of write amplification.",
                  "Reads go newest-first (memtable -> L0 -> deeper), using bloom filters to skip absent keys.",
                  "RocksDB/LevelDB/Cassandra prove it: for write-heavy workloads, LSM beats B-trees."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 17. B-Trees & Indexing
# =============================================================
def pdf_btrees(path):
    c = new_canvas(path); pg = 1
    title_page(c, "B-Trees & Indexing\nVisual Guide",
               "The data structure behind every database index:\nwide, shallow, and always balanced.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Why Not Binary Trees",
                       "Disks read in PAGES (4-16KB). A binary tree wastes 99% of each page.")
    box(c, 72, y - 90, 225, 100, BOX_RED, "Binary tree", "1 key per node\n30 levels for 1B keys\n30 disk reads", font_size=10.5)
    box(c, 315, y - 90, 225, 100, BOX_GREEN, "B-tree", "100s of keys per node\n3-4 levels for 1B keys\n3-4 disk reads", font_size=10.5)
    note(c, 72, y - 230, 468, "Design for the STORAGE medium: one node = one page = one I/O. Fan-out is everything.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Balanced Multi-Way Trees",
                       "Hundreds of keys per node, children between keys -- height stays tiny.")
    box(c, 216, y - 70, 180, 56, BOX_BLUE, "root: [20 | 50 | 80]", "", font_size=10)
    for i, (sx, lab) in enumerate([(72, "<20"), (216, "20-50"), (360, "50-80+")]):
        box(c, sx, y - 180, 160, 56, BOX_GREEN, lab, "child node", font_size=10)
        arrow(c, 306, y - 70, sx + 80, y - 124, color=ACCENT, width=1.6)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 270, "Search: compare within the node, descend to the child between the keys. O(log n) page reads.")
    note(c, 72, y - 350, 468, "Branching factor 100-1000: height = log_base(keys). A billion rows fits in 3-4 levels.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Node Splits Keep It Balanced",
                       "Full node? Split in two, push the middle key up -- the tree grows at the root.")
    box(c, 72, y - 70, 200, 64, BOX_ORANGE, "[10|20|30|40] FULL", "insert 25", font_size=10)
    arrow(c, 272, y - 38, 304, y - 38, color=ACCENT, width=2, label="split")
    box(c, 306, y - 100, 100, 60, BOX_GREEN, "[10|20]", "", font_size=10)
    box(c, 420, y - 100, 100, 60, BOX_GREEN, "[30|40]", "", font_size=10)
    box(c, 340, y - 30, 100, 44, BOX_BLUE, "25 up", "to parent", font_size=10)
    yy = bullet_list(c, 72, y - 190,
        ["Splits propagate upward only when parents are full too -- amortized, rare at the top.",
         "The tree stays PERFECTLY balanced: every leaf is the same depth, so worst case = average case.",
         "Underflow on delete merges siblings (the reverse) -- same invariant, opposite direction."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "B+ Trees: Data in the Leaves",
                       "Internal nodes hold KEYS ONLY; all values live in a linked list of leaves.")
    box(c, 216, y - 70, 180, 56, BOX_BLUE, "internal: keys only", "narrow, more fan-out", font_size=10)
    for i, sx in enumerate([72, 216, 360]):
        box(c, sx, y - 180, 160, 56, BOX_GREEN, f"leaf {i+1}", "keys + row pointers", font_size=9.5)
        arrow(c, 306, y - 70, sx + 80, y - 124, color=ACCENT, width=1.4)
        if i < 2:
            arrow(c, sx + 160, y - 152, sx + 174, y - 152, color=GREEN, width=1.8)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 270, "Range scan (WHERE age BETWEEN 20 AND 30): find the start leaf, then walk the linked list.")
    note(c, 72, y - 350, 468, "This is why databases use B+ trees, not plain B-trees: sequential scans never climb back up.", fill=BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Why Databases Use Them",
                       "Predictable I/O for point lookups AND range scans, with ordered iteration.")
    yy = bullet_list(c, 72, y,
        ["Logarithmic reads AND writes: 3-4 page I/Os for a billion-row table, worst case.",
         "Order preserved: ORDER BY, BETWEEN, prefix LIKE 'abc%' all walk the leaf chain.",
         "Self-maintaining: splits/merges keep balance without a DBA rebuilding anything.",
         "Page-aligned: nodes sized to disk/buffer-pool pages -- the cache loves them."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "The Costs",
                       "No free lunch: writes amplify and pages fragment.")
    yy = bullet_list(c, 72, y,
        ["Write amplification: one row update rewrites a whole page (and the WAL, and maybe splits).",
         "Random inserts fragment pages (half-empty leaves) -- REINDEX/VACUUM exists for a reason.",
         "For write-mostly workloads, LSM trees (previous guide) trade read cost for write speed.",
         "Choose B+ tree when: reads dominate, range queries matter, data fits the update pattern."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "B-Trees & Indexing — Remember",
                 ["One node = one disk page: fan-out of hundreds keeps billion-row trees 3-4 levels deep.",
                  "Full nodes split and push the middle key up -- the tree stays perfectly balanced forever.",
                  "B+ trees keep values only in leaves linked together: range scans walk the list, never climb.",
                  "Logarithmic point lookups, ordered iteration, self-maintenance -- the database default.",
                  "Costs: page-sized write amplification and fragmentation; LSM trees win write-heavy cases."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 18. Connection Pooling
# =============================================================
def pdf_connection_pooling(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Connection Pooling\nVisual Guide",
               "Databases hate connection churn:\nreuse, size, and multiplex connections.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Connections Are Expensive",
                       "Each one costs a TCP + TLS handshake, auth, and megabytes of server memory.")
    box(c, 72, y - 70, 150, 70, BOX_RED, "New conn", "handshake\nauth\nfork backend", font_size=10)
    arrow(c, 222, y - 35, 254, y - 35, color=RED, width=2, label="~ms each")
    box(c, 256, y - 70, 150, 70, BOX_RED, "Postgres", "~10MB per backend\n500 conns = 5GB", font_size=10)
    yy = bullet_list(c, 72, y - 180,
        ["At 1000 requests/sec, opening a connection per request = 1000 handshakes/sec of pure overhead.",
         "Server-side, each backend is a PROCESS (Postgres): context switches and memory explode past a few hundred.",
         "Client-side, TIME_WAIT sockets and port exhaustion bite first -- the pool fixes both ends."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "The Pool",
                       "Open N connections once; check them out, use them, return them.")
    box(c, 72, y - 70, 150, 110, BOX_BLUE, "Pool", "min 5 / max 20\nidle timeout 60s", font_size=10)
    box(c, 266, y - 70, 130, 110, BOX_GREEN, "App threads", "checkout ->\nuse ->\ncheckin", font_size=10)
    arrow(c, 222, y - 30, 264, y - 30, color=ACCENT, width=2, label="borrow")
    arrow(c, 264, y - 80, 222, y - 80, color=GREEN, width=2, label="return")
    box(c, 420, y - 70, 120, 110, BOX_ORANGE, "Database", "20 conns\ntotal", font_size=10)
    arrow(c, 396, y - 55, 418, y - 55, color=ACCENT, width=2)
    yy = bullet_list(c, 72, y - 220,
        ["Checkout with a TIMEOUT: waiting forever for a connection is a hung request with extra steps.",
         "Validate on checkout (cheap ping) or pay with stale-connection errors after DB restarts.",
         "The pool is per PROCESS: 50 app replicas x 20 = 1000 DB connections. Do the multiplication!"],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Pool Sizing Math",
                       "Little's Law: connections = throughput x query latency.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 11)
    c.drawString(72, y - 40, "pool_size = (queries/sec) x (avg seconds/query)")
    c.drawString(72, y - 66, "example:  500 qps x 0.02 s  =  10 connections")
    yy = bullet_list(c, 72, y - 106,
        ["Measure YOUR latency: 500 qps at 20ms needs 10 conns; at 200ms it needs 100.",
         "Start small and grow: an idle connection still costs server memory.",
         "Postgres sweet spot is often cores x 2 + spare -- beyond that, throughput DROPS (contention)."],
        font_size=10.5, gap=26)
    note(c, 72, y - 260, 468, "Bigger is not better: past the knee, extra connections just queue inside the DB and slow everyone.", fill=BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "PgBouncer: Transaction Pooling",
                       "The proxy that multiplexes thousands of clients onto tens of server connections.")
    box(c, 72, y - 70, 150, 70, BOX_BLUE, "1000 clients", "idle most\nof the time", font_size=10)
    arrow(c, 222, y - 35, 254, y - 35, color=ACCENT, width=2.5, label="multiplex")
    box(c, 256, y - 70, 150, 70, BOX_PURP, "PgBouncer", "assigns server\nconn per TXN", font_size=10)
    arrow(c, 406, y - 35, 438, y - 35, color=ACCENT, width=2.5)
    box(c, 440, y - 70, 100, 70, BOX_GREEN, "20 conns", "to Postgres", font_size=10)
    yy = bullet_list(c, 72, y - 180,
        ["Transaction mode: a server connection is borrowed per TRANSACTION, not per client -- idle clients hold nothing.",
         "Session mode (default): one server conn per client -- safe for LISTEN/NOTIFY, temp tables, prepared statements.",
         "Statement mode: per query -- fastest multiplexing, breaks multi-statement transactions."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "The Connection Storm",
                       "Every app replica restarts at once; the DB drowns in handshakes.")
    box(c, 72, y - 70, 150, 64, BOX_RED, "Deploy", "50 pods\nrestart", font_size=11)
    arrow(c, 222, y - 38, 254, y - 38, color=RED, width=2.5, label="50 x 20 conns")
    box(c, 256, y - 70, 150, 64, BOX_RED, "DB", "1000 handshakes\nOOM risk", font_size=10)
    yy = bullet_list(c, 72, y - 170,
        ["Defenses: a proxy tier (PgBouncer/RDS Proxy) absorbs the storm; rolling restarts spread it out.",
         "Serverless trap: 1000 Lambda invocations x cold pool = 1000 connections -- proxy or perish.",
         "Set max_connections on the DB as a CIRCUIT BREAKER, not a target."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Timeouts and Health",
                       "A pool without timeouts is a distributed deadlock kit.")
    yy = bullet_list(c, 72, y,
        ["checkout_timeout (2s): fail fast when the pool is exhausted -- surface the queue, do not hide it.",
         "idle_timeout / max_lifetime (5-30 min): recycle connections before the DB, LB, or NAT kills them silently.",
         "Health check on checkout: SELECT 1 is cheap; a stale half-open connection is expensive.",
         "Metrics that matter: pool wait time, checkout failures, idle vs active -- alert on wait time first."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Connection Pooling — Remember",
                 ["Connections cost handshakes, auth, and ~10MB server-side each -- never open per request.",
                  "Pools lend connections out and take them back; size with Little's Law (qps x latency).",
                  "Pool count multiplies by app replicas -- a proxy tier (PgBouncer) multiplexes thousands to tens.",
                  "Transaction pooling borrows per transaction; session mode keeps per-client state safe.",
                  "Timeouts on checkout, lifetime caps, and wait-time metrics keep the pool honest."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 19. Database Indexing
# =============================================================
def pdf_db_indexing(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Database Indexing\nVisual Guide",
               "Find rows without scanning tables:\nindex types, composite keys, and the write tax.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "The Index Idea",
                       "A table of contents for your table: sorted pointers to rows.")
    box(c, 72, y - 70, 200, 70, BOX_BLUE, "Table", "1M rows\nheap, unsorted", font_size=11)
    arrow(c, 272, y - 35, 304, y - 35, color=ACCENT, width=2, label="index on email")
    box(c, 306, y - 70, 200, 70, BOX_GREEN, "Index", "email -> row ptr\nsorted B+ tree", font_size=10)
    yy = bullet_list(c, 72, y - 180,
        ["No index: full table scan -- read all 1M rows to find one email. With index: 3-4 page reads.",
         "The index is a SEPARATE structure the planner may use; the table (heap) stays untouched.",
         "Indexes speed reads and SLOW writes: every INSERT/UPDATE/DELETE maintains each index."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "B-tree vs Hash vs GIN",
                       "Different structures for different questions.")
    idxs = [("B-tree (default)", "equality + ranges + ORDER BY -- the all-rounder", BOX_BLUE),
            ("Hash", "equality only, no ordering -- niche, rarely better than B-tree", BOX_TEAL),
            ("GIN", "inverted index: full-text search, JSONB keys, arrays", BOX_GREEN),
            ("GiST / BRIN", "geo shapes, or huge naturally-ordered tables (time series)", BOX_ORANGE)]
    yy = y
    for name, desc, fill in idxs:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "Default to B-tree. Reach for GIN when you query INSIDE a document (JSONB) or text. Reach for BRIN for append-only time data.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Composite Indexes",
                       "One index on (last_name, first_name): order of columns is the whole game.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 11)
    c.drawString(72, y - 40, "CREATE INDEX ON users (last_name, first_name);")
    yy = bullet_list(c, 72, y - 80,
        ["Leftmost prefix rule: the index serves WHERE last_name=? AND first_name=?, and WHERE last_name=? alone.",
         "It does NOT serve WHERE first_name=? alone -- the leading column must be constrained.",
         "Put the most selective / most-queried column first; equality columns before range columns.",
         "Example: (tenant_id, created_at) -- equality on tenant, range on time: perfect for SaaS queries."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Covering Indexes",
                       "INCLUDE the columns the query needs: answer without touching the table.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10.5)
    c.drawString(72, y - 40, "SELECT name FROM users WHERE email = ?;")
    c.drawString(72, y - 64, "CREATE INDEX ON users (email) INCLUDE (name);")
    box(c, 72, y - 150, 225, 70, BOX_RED, "No covering", "index -> heap fetch\nrandom I/O per row", font_size=10.5)
    box(c, 315, y - 150, 225, 70, BOX_GREEN, "Covering", "index-only scan\nno heap visit", font_size=10.5)
    note(c, 72, y - 260, 468, "EXPLAIN shows 'Index Only Scan'. Watch visibility-map staleness: recently updated pages still force heap checks.", fill=BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "The Write Tax",
                       "Every index is a second (third, fourth) thing to maintain per write.")
    box(c, 72, y - 70, 150, 70, BOX_BLUE, "1 INSERT", "into table", font_size=11)
    arrow(c, 222, y - 35, 254, y - 35, color=RED, width=2.5, label="x N indexes")
    box(c, 256, y - 70, 150, 70, BOX_RED, "N index writes", "+ WAL for each", font_size=10)
    yy = bullet_list(c, 72, y - 180,
        ["5 indexes = ~6x the write I/O of the bare row (plus lock contention on hot index pages).",
         "Unused indexes are pure tax: find them (pg_stat_user_indexes: zero scans) and drop them.",
         "Bulk loads: drop indexes, load, rebuild -- 10x faster than maintaining them row by row.",
         "Partial indexes (WHERE active) index only hot rows: smaller, faster, cheaper to maintain."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Reading EXPLAIN",
                       "The planner tells you which index it chose -- and its cost math.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, y - 40, "Seq Scan on users  (cost=0.00..1834.00 rows=1)")
    c.drawString(72, y - 62, "  Filter: (email = 'a@b.com')   <- BAD: scanning")
    c.drawString(72, y - 96, "Index Scan using users_email_idx (cost=0.42..8.44)")
    c.drawString(72, y - 118, "  Index Cond: (email = 'a@b.com') <- GOOD: seeking")
    yy = bullet_list(c, 72, y - 158,
        ["Seq Scan on a big table with a selective filter = missing index (usually).",
         "Rows estimate vs actual (EXPLAIN ANALYZE): bad stats -> bad plans -> run ANALYZE.",
         "Index Cond vs Filter: Cond seeks the tree; Filter scans and discards -- Cond is what you want."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Database Indexing — Remember",
                 ["Indexes are separate sorted structures: 3-4 page reads instead of full table scans.",
                  "B-tree is the default; GIN for documents/text/arrays; BRIN for append-only time data.",
                  "Composite indexes obey the leftmost-prefix rule -- order columns by query pattern.",
                  "Covering indexes (INCLUDE) answer queries without visiting the heap.",
                  "Every index taxes writes: drop unused ones, use partial indexes, and verify with EXPLAIN."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 20. Query Optimization
# =============================================================
def pdf_query_optimization(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Query Optimization\nVisual Guide",
               "From SQL text to fast execution:\nplanners, joins, statistics, and traps.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Planner vs Executor",
                       "You write WHAT; the planner picks HOW; the executor runs it.")
    box(c, 72, y - 70, 130, 64, BOX_BLUE, "Parse", "SQL -> tree", font_size=10)
    arrow(c, 202, y - 38, 224, y - 38, color=ACCENT, width=1.8)
    box(c, 226, y - 70, 150, 64, BOX_PURP, "Planner", "costs plans", font_size=10)
    arrow(c, 376, y - 38, 398, y - 38, color=ACCENT, width=1.8)
    box(c, 400, y - 70, 140, 64, BOX_GREEN, "Executor", "runs winner", font_size=10)
    yy = bullet_list(c, 72, y - 170,
        ["The planner enumerates strategies (join orders, scan types) and COSTS each using table statistics.",
         "Cheapest estimated plan wins -- the planner is only as good as its statistics.",
         "Cost is in abstract units (page reads + CPU), not seconds: compare plans relatively, then measure."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Reading EXPLAIN",
                       "The plan is a tree: leaves scan, nodes join, root returns.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, y - 40, "Hash Join  (cost=.... rows=100)")
    c.drawString(72, y - 62, "  ->  Seq Scan on orders")
    c.drawString(72, y - 84, "  ->  Hash  ->  Index Scan on users")
    yy = bullet_list(c, 72, y - 124,
        ["Read bottom-up: scans feed joins feed sorts. Indentation = data flow.",
         "cost=startup..total: startup matters for LIMIT queries (cheap start wins).",
         "rows: the planner's estimate. EXPLAIN ANALYZE shows actual rows + real milliseconds -- trust actuals.",
         "Huge estimate error (100 vs 1M) = stale statistics: ANALYZE the table."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Join Strategies",
                       "Three algorithms; the planner picks by size and indexes.")
    joins = [("Nested loop", "for each outer row, probe inner -- wins when outer is TINY and inner is indexed", BOX_BLUE),
             ("Hash join", "build hash table of smaller side, probe with larger -- the big-table workhorse", BOX_GREEN),
             ("Merge join", "both sides sorted (or index-ordered) -- streams, tiny memory", BOX_TEAL)]
    yy = y
    for name, desc, fill in joins:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    note(c, 72, yy - 60, 468, "A nested loop over 1M x 1M rows is a trillion probes -- if you see it on big tables, add the missing index.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Statistics Drive Everything",
                       "ANALYZE samples the table: row counts, distinct values, histograms, correlations.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 30, "planner believes: status='active' matches 90% of rows")
    c.drawString(72, y - 52, "reality after a purge: it matches 2% of rows")
    arrow(c, 72, y - 66, 300, y - 66, color=RED, width=2, label="stale stats -> seq scan chosen")
    yy = bullet_list(c, 72, y - 106,
        ["Stale stats make the planner choose seq scans for selective filters and nested loops for huge joins.",
         "Autovacuum usually keeps up; after bulk loads/deletes, ANALYZE manually.",
         "Histograms matter for skewed columns (status, country): default stats assume uniformity."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Selectivity: Filter Early",
                       "Apply the most selective predicate first -- shrink rows before joining.")
    box(c, 72, y - 70, 200, 70, BOX_RED, "Join then filter", "1M x 1M\nintermediate", font_size=10.5)
    arrow(c, 272, y - 35, 304, y - 35, color=GREEN, width=2, label="better")
    box(c, 306, y - 70, 200, 70, BOX_GREEN, "Filter then join", "100 x 1M\nintermediate", font_size=10.5)
    yy = bullet_list(c, 72, y - 180,
        ["Push predicates down: WHERE on one table should filter BEFORE the join, not after.",
         "The planner usually does this -- unless views, CTEs (materialized), or functions block it.",
         "Covering indexes on the filter columns turn 'filter' into 'index-only seek'."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Common Traps",
                       "Queries that LOOK fine and run terribly.")
    traps = [("N+1", "1 query for users + N queries for their orders -- batch with a join or IN (...)", BOX_RED),
             ("Functions on columns", "WHERE YEAR(created_at)=2024 kills the index -- use a range predicate", BOX_ORANGE),
             ("Implicit casts", "WHERE phone = 123 on a text column -- cast blocks the index", BOX_ORANGE),
             ("SELECT *", "drags LOBs across the wire, defeats covering indexes -- name columns", BOX_BLUE)]
    yy = y
    for name, desc, fill in traps:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Query Optimization — Remember",
                 ["The planner costs candidate plans using statistics; the executor runs the cheapest estimate.",
                  "Read EXPLAIN bottom-up; EXPLAIN ANALYZE reveals estimate-vs-actual lies.",
                  "Nested loop (tiny+indexed), hash join (big tables), merge join (sorted streams) -- match to shape.",
                  "Stale statistics are the #1 cause of bad plans: ANALYZE after bulk changes.",
                  "Filter early, avoid N+1, never wrap indexed columns in functions, and name your columns."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 21. Horizontal vs Vertical Scaling
# =============================================================
def pdf_scaling(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Horizontal vs Vertical Scaling\nVisual Guide",
               "Bigger box or more boxes:\nstateless design, load balancers, and sharding.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Scale Up (Vertical)",
                       "Bigger machine: more CPU, RAM, disk. Simple -- until physics says no.")
    box(c, 72, y - 100, 200, 110, BOX_BLUE, "Small box", "4 CPU / 16GB", font_size=11)
    arrow(c, 272, y - 45, 304, y - 45, color=ACCENT, width=2.5, label="upgrade")
    box(c, 306, y - 100, 200, 110, BOX_GREEN, "Big box", "64 CPU / 512GB", font_size=11)
    yy = bullet_list(c, 72, y - 150,
        ["Pros: zero architecture change, no distributed-systems pain, great for databases (for a while).",
         "Cons: hard ceiling (biggest SKU), downtime to resize, cost grows superlinearly, single point of failure.",
         "Always scale up FIRST: it is cheaper than re-architecting until you truly outgrow one box."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Scale Out (Horizontal)",
                       "More machines behind a load balancer: capacity grows with count.")
    box(c, 216, y - 70, 180, 60, BOX_PURP, "Load balancer", "distributes", font_size=11)
    for i, px in enumerate([72, 246, 420]):
        box(c, px, y - 190, 120, 60, BOX_GREEN, f"App {i+1}", "identical", font_size=10)
        arrow(c, 306, y - 70, px + 60, y - 130, color=ACCENT, width=1.6)
    yy = bullet_list(c, 72, y - 280,
        ["Pros: near-linear capacity, no single point of failure, commodity hardware, elastic (add/remove).",
         "Cons: your app must be STATELESS, sessions externalized, deploys coordinated.",
         "The load balancer is now critical infra: run it redundant, health-check backends."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Stateless: The Hard Requirement",
                       "Any request can hit any server -- so servers may remember nothing.")
    box(c, 72, y - 90, 225, 100, BOX_RED, "Stateful", "session in RAM\nserver 2 does not\nknow your login", font_size=10.5)
    box(c, 315, y - 90, 225, 100, BOX_GREEN, "Stateless", "session in Redis/cookie\nany server serves you", font_size=10.5)
    yy = bullet_list(c, 72, y - 230,
        ["Externalize: sessions -> Redis, uploads -> object storage, jobs -> queue.",
         "Sticky sessions are a crutch: they break even balancing and complicate failover -- avoid.",
         "12-factor rule: processes are disposable; all state lives in backing services."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "The Load Balancer's Job",
                       "More than a traffic cop: health, routing smarts, and TLS.")
    lbs = [("Algorithms", "round-robin, least-connections, consistent-hash (for caches)", BOX_BLUE),
           ("Health checks", "pull sick backends out of rotation automatically", BOX_GREEN),
           ("TLS termination", "decrypt once at the edge; plain HTTP inside (or re-encrypt)", BOX_TEAL),
           ("L4 vs L7", "L4 routes packets (fast); L7 routes HTTP (path/host-aware, smarter)", BOX_ORANGE)]
    yy = y
    for name, desc, fill in lbs:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Scaling the Data Layer",
                       "App servers scale out easily. The DATABASE is the hard part.")
    box(c, 72, y - 90, 225, 110, BOX_BLUE, "Reads", "add replicas\nleader -> followers", font_size=11)
    box(c, 315, y - 90, 225, 110, BOX_ORANGE, "Writes", "shard the data\nsplit by key", font_size=11)
    yy = bullet_list(c, 72, y - 230,
        ["Reads scale horizontally with replicas (eventual consistency accepted).",
         "Writes scale by sharding -- or by choosing a store that shards natively (Cassandra, DynamoDB).",
         "Caching in front buys 10x headroom: the cheapest scale-out is not hitting the DB at all."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Auto-Scaling",
                       "Add capacity on signal, remove on calm -- with hysteresis.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 30, "scale OUT when:  CPU > 70% for 5 min   (or queue depth, or p99 latency)")
    c.drawString(72, y - 54, "scale IN when:   CPU < 30% for 15 min  (slower -- avoid flapping)")
    yy = bullet_list(c, 72, y - 94,
        ["Cooldowns prevent thrash: scaling takes minutes (new nodes, warm caches).",
         "Scale on the RIGHT signal: queue depth and latency beat CPU for bursty workloads.",
         "Pre-scale for known peaks (Black Friday); keep headroom for unknown ones."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Horizontal vs Vertical Scaling — Remember",
                 ["Scale up first: simpler and cheaper until one machine truly cannot cope.",
                  "Scale out with identical stateless servers behind a redundant load balancer.",
                  "Statelessness is mandatory: sessions, files, and jobs live in backing services.",
                  "Reads scale via replicas, writes via sharding; caching buys headroom for both.",
                  "Auto-scale on meaningful signals with cooldowns -- and pre-scale for known peaks."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 22. Idempotency
# =============================================================
def pdf_idempotency(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Idempotency\nVisual Guide",
               "Make retries safe:\nkeys, dedupe, and exactly-once effects.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "The Retry Problem",
                       "The network failed AFTER the work was done. Was it processed? Unknown.")
    box(c, 72, y - 70, 150, 64, BOX_BLUE, "Client", "POST /pay", font_size=11)
    arrow(c, 222, y - 38, 254, y - 38, color=ACCENT, width=2, label="charged!")
    box(c, 256, y - 70, 150, 64, BOX_GREEN, "Server", "charged $50", font_size=10)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(340, y - 110, "response LOST")
    arrow(c, 222, y - 130, 254, y - 130, color=RED, width=2, label="retry?")
    yy = bullet_list(c, 72, y - 190,
        ["Timeout does NOT mean failure: the server may have completed the work and died sending the reply.",
         "Blind retry = double charge. Never retry = lost payment. The escape: idempotency.",
         "Idempotent: f(f(x)) = f(x) -- doing it twice has the same effect as doing it once."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Idempotency Keys",
                       "The client generates a unique key per INTENT; the server dedupes on it.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10.5)
    c.drawString(72, y - 40, "POST /pay   Idempotency-Key: 7f3a-...-c91d")
    box(c, 72, y - 130, 200, 70, BOX_BLUE, "First attempt", "key unseen\nprocess + store\nresult", font_size=10)
    arrow(c, 272, y - 95, 304, y - 95, color=ACCENT, width=2, label="retry, same key")
    box(c, 306, y - 130, 200, 70, BOX_GREEN, "Retry", "key seen\nreturn STORED\nresult, no rework", font_size=10)
    note(c, 72, y - 240, 468, "Stripe's pattern: keys scoped per account, stored 24h+. Same key + different payload = 422 (client bug, surfaced).", fill=BOX_GREEN)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Safe Retries",
                       "Retry storms are safe when every handler dedupes.")
    yy = bullet_list(c, 72, y,
        ["Client: generate the key ONCE per user intent (button click), reuse it across all retries.",
         "Server: check-then-act must be ATOMIC -- store the key and the result in one transaction.",
         "In-flight dedupe: second request with the same key while the first runs should WAIT, not double-process.",
         "Key TTL: keep keys long enough to cover your max retry window (hours/days, not seconds)."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Exactly-Once Effects",
                       "You cannot have exactly-once DELIVERY -- but you can have exactly-once EFFECT.")
    box(c, 72, y - 90, 225, 110, BOX_ORANGE, "At-least-once", "delivery may\nduplicate", font_size=11)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 14); c.drawCentredString(306, y - 35, "+")
    box(c, 315, y - 90, 225, 110, BOX_GREEN, "Idempotent receiver", "duplicates\nabsorbed", font_size=11)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawCentredString(306, y - 130, "= exactly-once EFFECT")
    note(c, 72, y - 220, 468, "This is the industry's practical answer: Kafka transactions + idempotent consumers, SQS + dedupe keys.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Naturally Idempotent Design",
                       "Some operations are idempotent by construction -- prefer them.")
    nats = [("PUT /users/42", "set state to X -- repeating sets the same state", BOX_GREEN),
            ("DELETE /sessions/9", "ensure gone -- already gone is fine", BOX_GREEN),
            ("Upserts", "INSERT ... ON CONFLICT DO NOTHING -- key-based dedupe in SQL", BOX_BLUE),
            ("State machines", "transition only from expected state -- replays are no-ops", BOX_TEAL)]
    yy = y
    for name, desc, fill in nats:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11)
        yy -= 70
    note(c, 72, yy - 60, 468, "POST (create) is the dangerous one: 'create order' twice = two orders, unless a key dedupes it.", fill=BOX_RED)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Limits and Sharp Edges",
                       "Idempotency is a design contract, not magic.")
    yy = bullet_list(c, 72, y,
        ["Non-idempotent by nature: 'increment counter', 'send email' -- wrap them in dedupe keys or accept duplicates.",
         "Key scope matters: per-user keys prevent cross-user collisions; per-intent keys prevent double-clicks.",
         "Clock risk: keys expire -- a retry AFTER expiry replays the work. Size TTLs generously.",
         "Test it: chaos-test duplicate delivery in staging; every handler should prove it dedupes."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Idempotency — Remember",
                 ["Timeouts are ambiguous: the work may have completed -- never blind-retry, never give up.",
                  "Idempotency keys: client-generated per intent, server dedupes atomically and replays stored results.",
                  "Exactly-once EFFECT = at-least-once delivery + idempotent receiver -- the practical standard.",
                  "Prefer naturally idempotent shapes: PUT, DELETE, upserts, state-machine transitions.",
                  "Size key TTLs generously, scope keys per user+intent, and chaos-test duplicate delivery."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 23. Consistency Models
# =============================================================
def pdf_eventual_consistency(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Consistency Models\nVisual Guide",
               "A spectrum from strong to eventual:\nguarantees you can actually promise users.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "The Spectrum",
                       "Strong consistency is expensive; eventual is cheap. Most systems live between.")
    box(c, 72, y - 70, 150, 80, BOX_BLUE, "Strong", "linearizable\nall see same\norder", font_size=10)
    box(c, 236, y - 70, 150, 80, BOX_TEAL, "Causal+", "session\nguarantees", font_size=10)
    box(c, 400, y - 70, 140, 80, BOX_GREEN, "Eventual", "converges\n'soon'", font_size=10)
    arrow(c, 222, y - 30, 234, y - 30, color=ACCENT, width=1.8)
    arrow(c, 386, y - 30, 398, y - 30, color=ACCENT, width=1.8)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 190, "Stronger -> more coordination -> higher latency, lower availability. Weaker -> the reverse.")
    note(c, 72, y - 270, 468, "Eventual consistency only promises CONVERGENCE: if writes stop, all replicas eventually agree. 'Eventually' is doing a lot of work there.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Read-Your-Writes",
                       "After I write, I must see my own write -- even on a replica.")
    box(c, 72, y - 70, 150, 64, BOX_BLUE, "You", "POST photo", font_size=11)
    arrow(c, 222, y - 38, 254, y - 38, color=ACCENT, width=2, label="write -> leader")
    box(c, 256, y - 70, 150, 64, BOX_GREEN, "Leader", "has it", font_size=10)
    box(c, 420, y - 70, 120, 64, BOX_ORANGE, "Replica", "not yet!", font_size=10)
    yy = bullet_list(c, 72, y - 170,
        ["The classic violation: post a photo, refresh, it is GONE (read hit a stale replica) -- users call this a bug.",
         "Fixes: route the writer's reads to the leader for a window, or version-stamp and wait.",
         "This is a SESSION guarantee: it only constrains what YOU see, not what everyone sees."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Monotonic Reads",
                       "Once you have seen version 5, you never go back to version 3.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10.5)
    c.drawString(72, y - 40, "read 1 -> v5 (replica A)     read 2 -> v3 (replica B)   <- VIOLATION")
    c.drawString(72, y - 64, "read 1 -> v5 (replica A)     read 2 -> v5 (replica A)   <- OK")
    yy = bullet_list(c, 72, y - 104,
        ["Time going backwards confuses users AND breaks logic (a deleted item reappears).",
         "Fix: sticky reads per session (same replica), or track a version watermark per client.",
         "Cheap to provide, embarrassing to lack -- include it in every session-consistency bundle."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Causal Consistency",
                       "If A caused B, everyone sees A before B. Unrelated writes may interleave.")
    box(c, 72, y - 70, 200, 70, BOX_BLUE, "Comment posted", "cause", font_size=11)
    arrow(c, 272, y - 35, 304, y - 35, color=ACCENT, width=2, label="causes")
    box(c, 306, y - 70, 200, 70, BOX_GREEN, "Reply notification", "effect", font_size=11)
    yy = bullet_list(c, 72, y - 180,
        ["The violation: you get notified of a reply to a comment you cannot see yet -- causality broken.",
         "Stronger than eventual, cheaper than linearizable: track causal deps (vector clocks!) not total order.",
         "The sweet spot for social feeds, chat, and collaboration: conversations stay coherent."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Bounded Staleness",
                       "Eventual consistency with an SLA: 'no older than X seconds or Y versions'.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 30, "Cosmos DB style: pick staleness bound per workload.")
    box(c, 72, y - 110, 225, 70, BOX_TEAL, "Time bound", "reads lag at most\n5 seconds", font_size=10.5)
    box(c, 315, y - 110, 225, 70, BOX_BLUE, "Version bound", "reads lag at most\n100 writes", font_size=10.5)
    yy = bullet_list(c, 72, y - 210,
        ["Turns 'eventually' into a number you can put in an SLA and alert on.",
         "Implementation: replicas reject reads older than the bound (or the writer waits).",
         "Strong session: read-your-writes + monotonic reads bundled -- the pragmatic default."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Choosing Your Model",
                       "Match the guarantee to the cost of being wrong.")
    yy = bullet_list(c, 72, y,
        ["Money, inventory, locks: strong consistency -- being wrong costs real dollars.",
         "Feeds, profiles, catalogs: eventual + read-your-writes -- staleness is invisible here.",
         "Chat, comments, collaboration: causal -- conversations must make sense.",
         "Dashboards, analytics: bounded staleness -- '5 minutes old' is a fine SLA.",
         "Rule: buy the WEAKEST consistency your UX tolerates; spend the savings on availability."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Consistency Models — Remember",
                 ["Strong = total order for everyone; eventual = convergence with no timeline -- most systems need the middle.",
                  "Read-your-writes: your own writes are immediately visible to you (route writers to the leader).",
                  "Monotonic reads: never show older data after newer -- time must not go backwards.",
                  "Causal consistency: causes precede effects for everyone -- the social-feed sweet spot.",
                  "Bounded staleness puts an SLA on 'eventually'; buy the weakest model your UX tolerates."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 24. Two-Phase Commit
# =============================================================
def pdf_2pc(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Two-Phase Commit\nVisual Guide",
               "Atomic commits across nodes:\nprepare, decide, and the blocking flaw.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "The Atomicity Need",
                       "Move $100 from A (node 1) to B (node 2): both updates or NEITHER.")
    box(c, 72, y - 70, 200, 70, BOX_BLUE, "Node 1", "A -= 100", font_size=11)
    box(c, 340, y - 70, 200, 70, BOX_BLUE, "Node 2", "B += 100", font_size=11)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(306, y - 35, "crash between = money vanishes")
    yy = bullet_list(c, 72, y - 170,
        ["One node committing while the other aborts = corruption no retry can fix.",
         "2PC's answer: a COORDINATOR runs a vote, then tells everyone the unanimous verdict.",
         "Assumption: nodes fail by crashing (not lying) -- this is crash-fault atomic commit."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "Phase 1: Prepare (Voting)",
                       "Coordinator: 'can everyone commit?' Each participant votes YES or NO.")
    box(c, 216, y - 70, 180, 60, ACCENT, "Coordinator", "PREPARE?", font_size=11)
    for i, px in enumerate([72, 246, 420]):
        box(c, px, y - 190, 120, 60, BOX_BLUE, f"P{i+1}", "vote YES\n(lock rows)", font_size=9.5)
        arrow(c, 306, y - 70, px + 60, y - 130, color=ACCENT, width=1.6, label="?")
        arrow(c, px + 70, y - 130, 316, y - 70, color=GREEN, width=1.2, label="YES")
    note(c, 72, y - 300, 468, "Voting YES means: 'I have locked everything and PROMISE to commit if told.' Locks are held from here on.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "Phase 2: Commit or Abort",
                       "Unanimous YES -> COMMIT everywhere. Any NO (or timeout) -> ABORT everywhere.")
    box(c, 72, y - 70, 200, 70, BOX_GREEN, "All YES", "-> COMMIT\nall apply", font_size=11)
    box(c, 340, y - 70, 200, 70, BOX_RED, "Any NO", "-> ABORT\nall roll back", font_size=11)
    yy = bullet_list(c, 72, y - 180,
        ["The coordinator's decision is written to stable storage BEFORE announcing -- it must survive its own crash.",
         "Participants that voted YES must OBEY the verdict: that promise is what makes it atomic.",
         "Once decided, the outcome is inevitable: stragglers learn it on recovery and comply."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "The Blocking Problem",
                       "Coordinator crashes after votes, before the verdict: participants wait FOREVER.")
    box(c, 216, y - 70, 180, 60, BOX_RED, "Coordinator", "CRASHED", font_size=11)
    for i, px in enumerate([72, 246, 420]):
        box(c, px, y - 190, 120, 60, BOX_ORANGE, f"P{i+1}", "voted YES\nLOCKED\nwaiting...", font_size=9)
    yy = bullet_list(c, 72, y - 280,
        ["Locked rows stay locked: no other transaction can touch them. Throughput dies, not just this txn.",
         "Participants cannot unilaterally decide: a peer might have heard COMMIT before the crash.",
         "Recovery needs the coordinator's log -- or a human. This BLOCKING is 2PC's fatal flaw."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "Why Sagas Replaced It",
                       "Availability beats atomicity when the participants are independent services.")
    box(c, 72, y - 90, 225, 110, BOX_RED, "2PC", "locks across services\nblocks on coordinator\nno autonomy", font_size=10.5)
    box(c, 315, y - 90, 225, 110, BOX_GREEN, "Saga", "local txns\ncompensate on failure\nservices stay free", font_size=10.5)
    yy = bullet_list(c, 72, y - 230,
        ["Microservices own their data: holding their rows locked for a stranger's coordinator is unacceptable.",
         "Saga trade: give up isolation (others see partial progress), gain availability (nothing blocks).",
         "3PC adds a pre-commit phase to reduce blocking -- but cannot eliminate it (and adds messages)."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Where 2PC Still Lives",
                       "Narrow, controlled, single-vendor -- the places blocking is tolerable.")
    yy = bullet_list(c, 72, y,
        ["Single-database XA: Postgres/MySQL as participants under one transaction manager -- same trust domain.",
         "Spanner-style: 2PC OVER Paxos -- the coordinator is replicated, so 'coordinator crash' stops blocking.",
         "Rule: 2PC is fine when participants and coordinator share fate (one team, one DC, replicated log).",
         "Across companies, clouds, or autonomous services: saga. Every time."],
        font_size=10.5, gap=28)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Two-Phase Commit — Remember",
                 ["2PC gives atomic commit across crash-prone nodes: prepare/vote, then commit/abort on unanimous verdict.",
                  "Voting YES is a promise: rows stay locked until the coordinator's decision arrives.",
                  "The fatal flaw is blocking: a dead coordinator leaves participants locked indefinitely.",
                  "Sagas replaced 2PC across services -- local transactions plus compensation, no global locks.",
                  "2PC survives where coordinator and participants share fate: single-DB XA and replicated coordinators."],
                 pg)
    c.save(); print("wrote", path)


# =============================================================
# 25. CRDTs
# =============================================================
def pdf_crdts(path):
    c = new_canvas(path); pg = 1
    title_page(c, "CRDTs\nVisual Guide",
               "Conflict-free Replicated Data Types:\nconvergence without coordination.",
               "System Design", None); pg += 1
    TOTAL = 6

    y = section_header(c, 1, TOTAL, "Convergence Without Coordination",
                       "Replicas merge whenever they meet -- and ALWAYS agree, with no leader, no locks.")
    box(c, 72, y - 70, 130, 64, BOX_BLUE, "Replica A", "+1, +1", font_size=10)
    box(c, 246, y - 70, 130, 64, BOX_GREEN, "Replica B", "+1", font_size=10)
    arrow(c, 202, y - 38, 244, y - 38, color=ACCENT, width=1.8, label="merge")
    arrow(c, 376, y - 38, 418, y - 38, color=ACCENT, width=1.8, label="merge")
    box(c, 420, y - 70, 120, 64, BOX_PURP, "Both = 3", "always", font_size=10)
    yy = bullet_list(c, 72, y - 170,
        ["The math requirement: merge must be commutative, associative, idempotent -- order and duplicates do not matter.",
         "Offline-first dream: edit on a plane, sync later, no conflicts EVER (for CRDT-shaped data).",
         "Price: only certain data shapes qualify -- counters, sets, registers, text. Not arbitrary SQL."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, TOTAL, "State-Based vs Operation-Based",
                       "Ship the whole state, or ship just the operation?")
    box(c, 72, y - 90, 225, 110, BOX_BLUE, "State-based (CvRDT)", "merge full states\nneeds idempotent merge\ntolerates duplication", font_size=10.5)
    box(c, 315, y - 90, 225, 110, BOX_GREEN, "Op-based (CmRDT)", "broadcast ops\nneeds reliable delivery\nsmaller messages", font_size=10.5)
    yy = bullet_list(c, 72, y - 230,
        ["State-based: simple and robust (Riak-style) -- but state can be large to ship.",
         "Op-based: tiny messages ('increment by 1') -- but the channel must deliver each op exactly once, in causal order.",
         "Delta-state: the modern hybrid -- ship only the CHANGED part of the state. Best of both."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, TOTAL, "G-Counter: The Simplest CRDT",
                       "Grow-only counter: one slot per replica, value = sum of slots.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 11)
    c.drawString(72, y - 40, "A: [2, 0, 0]      B: [0, 1, 0]      merge -> [2, 1, 0]  =  3")
    yy = bullet_list(c, 72, y - 80,
        ["Each replica increments ONLY its own slot -- no coordination, no lost updates.",
         "Merge = take max per slot: concurrent increments never overwrite each other.",
         "PN-Counter adds a second grow-only counter for decrements: value = plus - minus.",
         "Use: like counts, vote tallies, retry-safe metrics -- anywhere 'count up' is the job."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, TOTAL, "Sets: Harder Than They Look",
                       "Add is easy. Remove + concurrent add = the classic CRDT puzzle.")
    box(c, 72, y - 90, 225, 110, BOX_BLUE, "G-Set", "add-only\nmerge = union\ntrivially safe", font_size=10.5)
    box(c, 315, y - 90, 225, 110, BOX_RED, "2P-Set", "add set + tombstone set\nremove wins forever\ncannot re-add!", font_size=10.5)
    yy = bullet_list(c, 72, y - 230,
        ["2P-Set flaw: once removed, an element can NEVER return -- the tombstone outlives everything.",
         "OR-Set (observed-remove): tag each ADD uniquely; remove deletes only observed tags -- re-add works.",
         "Rule: 'remove' must mean 'remove what I have seen', never 'remove forever'."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, TOTAL, "LWW Registers",
                       "Last-writer-wins: attach a timestamp, highest wins -- simple, lossy, honest about it.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10.5)
    c.drawString(72, y - 40, "A sets name='Al' @t=5      B sets name='Bo' @t=7")
    c.drawString(72, y - 64, "merge -> 'Bo' (higher timestamp wins, 'Al' is LOST)")
    yy = bullet_list(c, 72, y - 104,
        ["Timestamps must be trustworthy: hybrid logical clocks beat wall clocks here.",
         "Data loss is BY DESIGN: concurrent writes to one register cannot both survive.",
         "Use for: display names, status fields -- single values where 'latest intention' is the semantics.",
         "Need both values kept? That is a multi-value register -- see vector clocks + siblings."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, TOTAL, "Collaborative Editing",
                       "Google Docs / Figma: CRDTs (or OT) under the hood.")
    box(c, 72, y - 70, 150, 70, BOX_BLUE, "You", "type 'hi'", font_size=11)
    box(c, 360, y - 70, 150, 70, BOX_GREEN, "Teammate", "type 'yo'", font_size=11)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawCentredString(306, y - 38, "sequence CRDT (Yjs / Automerge)")
    c.drawString(72, y - 180, "Characters are list elements with stable IDs; concurrent inserts interleave deterministically.")
    yy = bullet_list(c, 72, y - 210,
        ["Both editors converge to the SAME document with no server merging logic -- the data structure does it.",
         "Yjs and Automerge package this: local-first apps with sync as a side effect.",
         "OT (operational transform) is the older cousin: needs a central server to transform ops; CRDTs do not."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "CRDTs — Remember",
                 ["CRDTs guarantee replicas converge with no coordination: merge must be commutative, associative, idempotent.",
                  "State-based ships full state (robust); op-based ships operations (small); delta-state splits the difference.",
                  "G-Counter: per-replica slots, merge by max -- concurrent increments never lost.",
                  "Sets need care: OR-Set's tagged adds make remove-then-re-add work; 2P-Set forbids re-adding.",
                  "LWW registers keep the latest timestamp (lossy by design); sequence CRDTs power collaborative editors."],
                 pg)
    c.save(); print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    pdf_consistent_hashing(os.path.join(out, "bbg-consistent-hashing.pdf"))
    pdf_cap(os.path.join(out, "bbg-cap-theorem.pdf"))
    pdf_sharding(os.path.join(out, "bbg-db-sharding.pdf"))
    pdf_replication(os.path.join(out, "bbg-replication.pdf"))
    pdf_caching_strategies(os.path.join(out, "bbg-caching-strategies.pdf"))
    pdf_message_queues(os.path.join(out, "bbg-message-queues.pdf"))
    pdf_event_driven(os.path.join(out, "bbg-event-driven.pdf"))
    pdf_api_gateway(os.path.join(out, "bbg-api-gateway.pdf"))
    pdf_service_mesh(os.path.join(out, "bbg-service-mesh.pdf"))
    pdf_circuit_breaker(os.path.join(out, "bbg-circuit-breaker.pdf"))
    pdf_rate_limiting(os.path.join(out, "bbg-rate-limiting.pdf"))
    pdf_saga_pattern(os.path.join(out, "bbg-saga-pattern.pdf"))
    pdf_consensus(os.path.join(out, "bbg-consensus.pdf"))
    pdf_vector_clocks(os.path.join(out, "bbg-vector-clocks.pdf"))
    pdf_bloom_filters(os.path.join(out, "bbg-bloom-filters.pdf"))
    pdf_lsm_trees(os.path.join(out, "bbg-lsm-trees.pdf"))
    pdf_btrees(os.path.join(out, "bbg-btrees.pdf"))
    pdf_connection_pooling(os.path.join(out, "bbg-connection-pooling.pdf"))
    pdf_db_indexing(os.path.join(out, "bbg-db-indexing.pdf"))
    pdf_query_optimization(os.path.join(out, "bbg-query-optimization.pdf"))
    pdf_scaling(os.path.join(out, "bbg-scaling.pdf"))
    pdf_idempotency(os.path.join(out, "bbg-idempotency.pdf"))
    pdf_eventual_consistency(os.path.join(out, "bbg-eventual-consistency.pdf"))
    pdf_2pc(os.path.join(out, "bbg-2pc.pdf"))
    pdf_crdts(os.path.join(out, "bbg-crdts.pdf"))
