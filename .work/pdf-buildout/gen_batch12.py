"""Batch 12: Data Engineering PDFs — 20 topics, original diagrams."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *

CATEGORY = "Data Engineering"


def pdf_elt(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "ELT vs ETL\nVisual Guide",
               "Where does the transform happen?\nThe pipeline choice that shapes modern data stacks.",
               CATEGORY, None); pg += 1

    # 1: the classic ETL
    y = section_header(c, 1, 6, "The Classic ETL Pipeline",
                       "Extract → Transform → Load. Transform happens BEFORE the warehouse.")
    box(c, 72, 440, 120, 70, BOX_BLUE, "Sources", "APIs, DBs, files")
    box(c, 232, 440, 140, 70, BOX_ORANGE, "ETL Engine", "clean, join, aggregate")
    box(c, 412, 440, 120, 70, BOX_GREEN, "Warehouse", "curated tables")
    arrow(c, 192, 475, 230, 475, label="extract")
    arrow(c, 372, 475, 410, 475, label="load clean")
    note(c, 72, 330, 468, "ETL transforms in a separate engine (Informatica, SSIS). The warehouse only ever sees polished, schema-fixed data.")
    bullet_list(c, 72, 290, [
        "Raw data is discarded or archived before loading",
        "Schema must be decided upfront (schema-on-write)",
        "Transform engine is a separate cluster to buy and maintain"])
    footer(c, pg); c.showPage(); pg += 1

    # 2: ELT flip
    y = section_header(c, 2, 6, "ELT: Flip the Order",
                       "Extract → Load → Transform. Land raw data first, transform inside the warehouse.")
    box(c, 72, 440, 120, 70, BOX_BLUE, "Sources", "APIs, DBs, files")
    box(c, 232, 440, 140, 70, BOX_GREEN, "Warehouse", "raw landing zone")
    box(c, 412, 440, 120, 70, BOX_TEAL, "SQL / dbt", "transform here")
    arrow(c, 192, 475, 230, 475, label="load raw")
    arrow(c, 372, 475, 410, 475, label="curated")
    note(c, 72, 330, 468, "ELT lands raw data first (bronze), then transforms with warehouse compute into silver/gold layers.")
    bullet_list(c, 72, 290, [
        "Raw data is always preserved — re-transform anytime",
        "Schema-on-read: decide the shape when you query it",
        "One system to maintain instead of two"])
    footer(c, pg); c.showPage(); pg += 1

    # 3: pushdown
    y = section_header(c, 3, 6, "Pushdown: The Warehouse Does the Work",
                       "Cloud warehouses have massive elastic compute — use it.")
    box(c, 72, 480, 200, 70, BOX_RED, "ETL approach", "small transform cluster")
    box(c, 340, 480, 200, 70, BOX_GREEN, "ELT approach", "warehouse scales out")
    arrow(c, 272, 515, 338, 515, color=RED)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(88, 440, "Transform engine sized for peak load,")
    c.drawString(88, 424, "idle most of the time = wasted spend.")
    c.drawString(356, 440, "Transform runs where the data lives,")
    c.drawString(356, 424, "on elastic compute that scales to zero.")
    note(c, 72, 320, 468, "Pushdown compute means no data movement for transforms — the engine comes to the data, not the other way around.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: comparison
    y = section_header(c, 4, 6, "When Each Wins",
                       "No universal winner — match the pattern to the constraint.")
    wins = [("ETL wins", "Heavy PII scrubbing before storage", "Regulated data that must never land raw", "Legacy on-prem warehouses (Teradata, Oracle)", BOX_ORANGE),
            ("ELT wins", "Exploratory analytics, ML features", "Re-processing history with new logic", "Cloud warehouses (Snowflake, BigQuery)", BOX_GREEN)]
    yy = y
    for name, p1, p2, p3, fill in wins:
        box(c, 72, yy - 110, 468, 116, fill, name, "", font_size=14)
        c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
        c.drawString(92, yy - 48, "• " + p1)
        c.drawString(92, yy - 68, "• " + p2)
        c.drawString(92, yy - 88, "• " + p3)
        yy -= 132
    footer(c, pg); c.showPage(); pg += 1

    # 5: bronze/silver/gold
    y = section_header(c, 5, 6, "ELT in Practice: Medallion Layers",
                       "Raw → cleaned → business-ready, all inside the platform.")
    box(c, 72, 460, 128, 70, BOX_ORANGE, "Bronze", "raw, append-only")
    box(c, 242, 460, 128, 70, BOX_BLUE, "Silver", "cleaned, typed")
    box(c, 412, 460, 128, 70, BOX_GREEN, "Gold", "aggregated, BI-ready")
    arrow(c, 200, 495, 240, 495, label="dedupe")
    arrow(c, 370, 495, 410, 495, label="model")
    note(c, 72, 350, 468, "The medallion (bronze/silver/gold) architecture is ELT's signature: every stage is just SQL on warehouse tables.")
    bullet_list(c, 72, 310, [
        "Bronze: exact copy of source, partitioned by ingestion time",
        "Silver: one row per entity, types fixed, PII tagged",
        "Gold: star schemas and aggregates the business queries"])
    footer(c, pg); c.showPage(); pg += 1

    # 6: decision
    y = section_header(c, 6, 6, "The Decision Framework",
                       "Ask these questions before picking a pattern.")
    qs = ["Must raw data NEVER be stored? → ETL (or ELT with in-flight masking)",
          "Do analysts need to re-shape history? → ELT keeps raw forever",
          "Is your warehouse elastic cloud? → ELT uses pushdown compute",
          "Small team, one stack? → ELT is simpler to operate"]
    y = bullet_list(c, 72, y, qs, font_size=11.5, gap=30)
    note(c, 72, 340, 468, "Modern default: ELT on a cloud warehouse, with ETL-style scrubbing only for data that legally cannot land raw.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "ELT vs ETL — Remember",
                 ["ETL transforms before loading; ELT loads raw first and transforms inside the warehouse.",
                  "ELT's superpower: raw data is preserved, so history can be re-transformed with new logic.",
                  "Pushdown compute runs transforms on elastic warehouse capacity — no separate engine to size.",
                  "ETL still wins when regulations forbid storing raw data (PII scrubbing before landing).",
                  "Medallion layers (bronze/silver/gold) are the standard ELT shape for raw → clean → business-ready."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_kafka_deep(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Kafka Deep Dive\nVisual Guide",
               "Partitions, offsets, groups, and exactly-once.\nHow the distributed log actually works.",
               CATEGORY, None); pg += 1

    # 1: topic anatomy
    y = section_header(c, 1, 6, "Topic Anatomy: Partitions & Offsets",
                       "A topic is a partitioned, append-only log. Order is guaranteed only within a partition.")
    for i, px in enumerate([72, 232, 392]):
        box(c, px, 460, 148, 90, BOX_BLUE, f"Partition {i}", "offset 0 → N", font_size=11)
        c.setFillColor(ACCENT); c.setFont(MONO_FONT, 8)
        c.drawString(px + 10, 480, "[ rec0 | rec1 | rec2 | … ]")
    arrow(c, 146, 620, 146, 552, color=ACCENT, label="producer")
    arrow(c, 306, 620, 306, 552, color=ACCENT, label="producer")
    arrow(c, 466, 620, 466, 552, color=ACCENT, label="producer")
    box(c, 232, 600, 148, 44, BOX_GREEN, "Topic: orders", "3 partitions")
    note(c, 72, 340, 468, "Each record lands in one partition (by key hash or round-robin) and gets a sequential offset — its position in that partition.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: consumer groups
    y = section_header(c, 2, 6, "Consumer Groups & Rebalancing",
                       "Within a group, each partition is read by exactly one consumer — parallelism equals partition count.")
    box(c, 72, 480, 200, 60, BOX_BLUE, "Group: analytics", "3 consumers")
    box(c, 340, 480, 200, 60, BOX_GREEN, "Group: fraud", "2 consumers")
    box(c, 72, 340, 120, 60, BOX_ORANGE, "P0", "→ C1")
    box(c, 232, 340, 120, 60, BOX_ORANGE, "P1", "→ C2")
    box(c, 392, 340, 120, 60, BOX_ORANGE, "P2", "→ C3")
    arrow(c, 172, 478, 132, 402, color=ACCENT)
    arrow(c, 172, 478, 292, 402, color=ACCENT)
    arrow(c, 172, 478, 452, 402, color=ACCENT)
    note(c, 72, 240, 468, "Two groups each get EVERY record independently. Add a consumer and partitions rebalance — a brief pause while ownership is reassigned.")
    bullet_list(c, 72, 200, [
        "Max useful consumers in a group = partition count",
        "A consumer crash triggers rebalance; its partitions move to survivors",
        "Sticky assignment minimizes partition movement between rebalances"])
    footer(c, pg); c.showPage(); pg += 1

    # 3: ISR
    y = section_header(c, 3, 6, "Replication: ISR Keeps Data Safe",
                       "Every partition has a leader and followers. The In-Sync Replica set is what protects you.")
    box(c, 226, 480, 160, 70, BOX_BLUE, "Leader (P0)", "handles all reads/writes")
    box(c, 72, 340, 140, 70, BOX_GREEN, "Follower A", "in-sync ✓")
    box(c, 236, 340, 140, 70, BOX_GREEN, "Follower B", "in-sync ✓")
    box(c, 400, 340, 140, 70, BOX_RED, "Follower C", "lagging ✗")
    arrow(c, 280, 478, 142, 412, color=GREEN)
    arrow(c, 330, 478, 306, 412, color=GREEN)
    c.setStrokeColor(RED); c.setLineWidth(2); c.setDash(4, 3)
    c.line(370, 478, 470, 412); c.setDash()
    note(c, 72, 240, 468, "A write is 'committed' when all ISR members have it. If the leader dies, an in-sync follower is elected — no committed data lost.")
    bullet_list(c, 72, 200, [
        "min.insync.replicas: minimum ISR size before a write is accepted",
        "acks=all: producer waits for full ISR acknowledgment",
        "Out-of-sync followers can rejoin by catching up from the leader"])
    footer(c, pg); c.showPage(); pg += 1

    # 4: delivery semantics
    y = section_header(c, 4, 6, "Delivery Semantics: The Trio",
                       "At-most-once, at-least-once, exactly-once — pick your guarantee.")
    sems = [("At-most-once", "Commit offset BEFORE processing. Crash = lost record.", BOX_RED),
            ("At-least-once", "Commit offset AFTER processing. Crash = duplicate record.", BOX_ORANGE),
            ("Exactly-once", "Idempotent producer + transactions. One effect, even on retry.", BOX_GREEN)]
    yy = y
    for name, desc, fill in sems:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=12)
        yy -= 76
    note(c, 72, yy - 20, 468, "Exactly-once in Kafka = idempotent producer (dedupe by sequence) + transactional writes (atomic commit of records + offsets).")
    footer(c, pg); c.showPage(); pg += 1

    # 5: retention & compaction
    y = section_header(c, 5, 6, "Retention & Log Compaction",
                       "Kafka is storage, not just a pipe. Old segments age out — or compact to the latest key.")
    box(c, 72, 480, 225, 80, BOX_BLUE, "Time retention", "delete segments older than N days")
    box(c, 315, 480, 225, 80, BOX_TEAL, "Log compaction", "keep only the latest value per key")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9)
    c.drawString(88, 430, "k1=v1  k1=v2  k2=a  k1=v3")
    c.setFillColor(ACCENT); c.setFont(TITLE_FONT, 11)
    c.drawString(88, 408, "→  k2=a  k1=v3")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(331, 430, "Changelog topics: rebuild")
    c.drawString(331, 414, "current state from the log.")
    note(c, 72, 320, 468, "Compaction turns a topic into a durable key-value snapshot — the foundation of Kafka Streams state stores and CDC sinks.")
    footer(c, pg); c.showPage(); pg += 1

    # 6: key design
    y = section_header(c, 6, 6, "Keys: Order Where It Matters",
                       "Same key → same partition → ordered processing per entity.")
    box(c, 72, 460, 140, 70, BOX_BLUE, "key=user-42", "→ Partition 1")
    box(c, 252, 460, 140, 70, BOX_BLUE, "key=user-42", "→ Partition 1")
    box(c, 432, 460, 108, 70, BOX_ORANGE, "key=null", "round-robin")
    arrow(c, 142, 458, 322, 458, color=ACCENT)
    arrow(c, 322, 458, 142, 430, color=ACCENT)
    note(c, 72, 340, 468, "Keyed records give per-entity ordering (all events for user-42 processed in order). Null keys spread load evenly but sacrifice ordering.")
    bullet_list(c, 72, 300, [
        "Choose the key from the entity you must serialize on",
        "Changing partition count re-hashes keys — plan partition counts upfront",
        "Hot keys create hot partitions: split the key or accept the skew"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Kafka Deep Dive — Remember",
                 ["Topics are partitioned append-only logs; ordering holds within a partition, not across them.",
                  "A consumer group splits partitions across consumers — add partitions to scale, not just consumers.",
                  "The ISR (in-sync replicas) is the durability contract: committed = replicated to all ISR members.",
                  "Exactly-once = idempotent producer plus transactions; at-least-once is the practical default.",
                  "Log compaction keeps the latest value per key, turning topics into replayable state snapshots."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_spark(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Apache Spark\nVisual Guide",
               "From RDDs to DataFrames, DAGs to shuffles.\nHow Spark turns your code into distributed execution.",
               CATEGORY, None); pg += 1

    # 1: RDD vs DataFrame
    y = section_header(c, 1, 6, "RDDs vs DataFrames",
                       "Two APIs, one engine. DataFrames win for almost everything today.")
    box(c, 72, y - 130, 225, 130, BOX_ORANGE, "RDD", "resilient distributed dataset", font_size=13)
    box(c, 315, y - 130, 225, 130, BOX_GREEN, "DataFrame", "distributed table + schema", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    rdd = ["Low-level, row = Java object", "No schema → no optimization", "Use for: custom partitioning, legacy code"]
    df = ["Schema-aware (Catalyst optimizer)", "Tungsten: off-heap, whole-stage codegen", "Use for: everything analytical"]
    yy = y - 34
    for t in rdd:
        c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 34
    for t in df:
        c.drawString(331, yy, "• " + t); yy -= 18
    note(c, 72, y - 190, 468, "DataFrames let the Catalyst optimizer rewrite your query plan; RDDs execute exactly what you wrote. Datasets sit in between (typed + optimized).")
    footer(c, pg); c.showPage(); pg += 1

    # 2: lazy evaluation
    y = section_header(c, 2, 6, "Lazy Evaluation: Nothing Runs Until an Action",
                       "Transformations build a plan. Actions trigger execution.")
    box(c, 72, 480, 120, 60, BOX_BLUE, ".filter()", "transformation")
    box(c, 232, 480, 120, 60, BOX_BLUE, ".groupBy()", "transformation")
    box(c, 392, 480, 120, 60, BOX_GREEN, ".count()", "ACTION")
    arrow(c, 192, 510, 230, 510, label="plan")
    arrow(c, 352, 510, 390, 510, color=GREEN, label="EXECUTE")
    note(c, 72, 380, 468, "Spark records transformations as a DAG and optimizes the whole plan before running anything — predicate pushdown, column pruning, join reordering.")
    bullet_list(c, 72, 340, [
        "Transformations: map, filter, join — lazy, return new DataFrames",
        "Actions: count, collect, write — eager, trigger jobs",
        "Why lazy: the optimizer sees the full query before choosing a plan"])
    footer(c, pg); c.showPage(); pg += 1

    # 3: DAG stages
    y = section_header(c, 3, 6, "DAG Scheduler: Stages & Tasks",
                       "Narrow transformations pipeline in one stage; shuffles split stages.")
    box(c, 72, 500, 180, 60, BOX_GREEN, "Stage 1", "map → filter (narrow)")
    box(c, 360, 500, 180, 60, BOX_GREEN, "Stage 2", "reduce (after shuffle)")
    arrow(c, 252, 530, 358, 530, color=RED, width=3, label="SHUFFLE")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 460, "Narrow: each output partition needs one input partition (map, filter).")
    c.drawString(72, 442, "Wide: each output partition needs MANY inputs (groupBy, join) → shuffle.")
    c.drawString(72, 424, "One stage = one set of tasks, no data exchange between tasks.")
    note(c, 72, 330, 468, "The DAGScheduler cuts the plan at every shuffle boundary. Fewer shuffles = fewer stages = faster jobs.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: shuffle deep
    y = section_header(c, 4, 6, "The Shuffle: Spark's Expensive Habit",
                       "All-to-all data exchange across the network — the #1 performance killer.")
    box(c, 72, 480, 140, 70, BOX_BLUE, "Map side", "writes shuffle files")
    box(c, 400, 480, 140, 70, BOX_BLUE, "Reduce side", "fetches + merges")
    c.setStrokeColor(RED); c.setLineWidth(2)
    for sx in [120, 160]:
        for dx in [430, 490]:
            c.line(sx, 478, dx, 548)
    c.setFillColor(RED); c.setFont(TITLE_FONT, 10)
    c.drawCentredString(306, 515, "NETWORK + DISK I/O")
    note(c, 72, 380, 468, "Every shuffle writes intermediate files to disk and pulls them across the network. Sort-merge join, repartition, and distinct all shuffle.")
    bullet_list(c, 72, 340, [
        "Avoid: unnecessary groupBy, repartition on huge keys",
        "Prefer: broadcast joins for small tables (no shuffle)",
        "Tune: spark.sql.shuffle.partitions (default 200 is often wrong)"])
    footer(c, pg); c.showPage(); pg += 1

    # 5: partitioning
    y = section_header(c, 5, 6, "Partitioning: Data Layout Is Performance",
                       "Right-sized partitions keep every core busy without drowning in overhead.")
    box(c, 72, 470, 140, 70, BOX_RED, "Too few", "huge partitions, idle cores")
    box(c, 236, 470, 140, 70, BOX_GREEN, "Just right", "128MB–1GB each")
    box(c, 400, 470, 140, 70, BOX_RED, "Too many", "tiny tasks, scheduler overhead")
    note(c, 72, 370, 468, "Aim for partitions ~2–4x the number of cores. Skew (one giant partition) is worse than count — salt hot keys to break it up.")
    bullet_list(c, 72, 330, [
        "repartition(n): full shuffle, use to increase parallelism",
        "coalesce(n): narrow, use to shrink partitions before writing",
        "Skew fix: salt the hot key (key + random suffix), then de-salt"])
    footer(c, pg); c.showPage(); pg += 1

    # 6: tuning checklist
    y = section_header(c, 6, 6, "Tuning Checklist",
                       "The highest-leverage knobs, in order.")
    items = ["Cache reused DataFrames (.persist) — but unpersist when done",
             "Broadcast small tables (<10MB default) to kill shuffle joins",
             "Partition pruning: filter on the partition column first",
             "Avoid UDFs — they block Catalyst optimization; use native functions",
             "Write fewer, larger files: coalesce before writing to storage"]
    y = bullet_list(c, 72, y, items, font_size=11.5, gap=30)
    note(c, 72, 300, 468, "Measure first: the Spark UI's SQL tab shows which stage shuffles and how long each takes — tune the red stages, not the green ones.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Apache Spark — Remember",
                 ["DataFrames beat RDDs: schema-aware plans get Catalyst optimization and whole-stage codegen.",
                  "Nothing runs until an action — laziness lets the optimizer see and rewrite the full plan.",
                  "The DAG splits into stages at shuffle boundaries; narrow transforms pipeline, wide ones shuffle.",
                  "Shuffles are the dominant cost: all-to-all network + disk I/O. Design them away with broadcast joins.",
                  "Right-size partitions (128MB–1GB), salt skewed keys, and let the Spark UI tell you where time goes."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_snowflake(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Snowflake & BigQuery\nVisual Guide",
               "Decoupled storage and compute.\nHow cloud warehouses scale elastically.",
               CATEGORY, None); pg += 1

    # 1: decoupled architecture
    y = section_header(c, 1, 6, "Decoupled Storage & Compute",
                       "The core idea: store once cheaply, spin compute up and down independently.")
    box(c, 72, 460, 468, 80, BOX_BLUE, "Shared Storage Layer", "S3 / GCS — all data, all formats, pay per byte")
    box(c, 72, 340, 140, 70, BOX_GREEN, "Warehouse S", "1 node")
    box(c, 236, 340, 140, 70, BOX_GREEN, "Warehouse M", "4 nodes")
    box(c, 400, 340, 140, 70, BOX_GREEN, "Warehouse XL", "16 nodes")
    for bx in [142, 306, 470]:
        arrow(c, bx, 458, bx, 412, color=GREEN)
    note(c, 72, 240, 468, "Compute clusters (virtual warehouses) attach to the same storage, run the query, then suspend. No data to move, no cluster to keep warm.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: micro-partitions
    y = section_header(c, 2, 6, "Micro-Partitions: Automatic Layout",
                       "Snowflake slices tables into ~16MB immutable, columnar micro-partitions with metadata.")
    box(c, 72, 470, 105, 60, BOX_TEAL, "MP-1", "min/max")
    box(c, 187, 470, 105, 60, BOX_TEAL, "MP-2", "min/max")
    box(c, 302, 470, 105, 60, BOX_TEAL, "MP-3", "min/max")
    box(c, 417, 470, 105, 60, BOX_TEAL, "MP-4", "min/max")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Each micro-partition stores column min/max, null counts, distinct counts.")
    c.drawString(72, 412, "Query: WHERE date = '2026-10-01' → the optimizer skips")
    c.drawString(72, 394, "partitions whose range can't match. No manual partitioning needed.")
    note(c, 72, 300, 468, "Automatic partition pruning from metadata — but it only works if data is clustered. ORDER BY at load or clustering keys keep ranges tight.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: BigQuery slots
    y = section_header(c, 3, 6, "BigQuery: Slots, Not Servers",
                       "BigQuery abstracts compute into slots — you think in query capacity, not machines.")
    box(c, 72, 470, 468, 70, BOX_GREEN, "Slot Pool", "thousands of parallel workers behind one API")
    box(c, 72, 370, 140, 60, BOX_BLUE, "Query A", "uses 500 slots")
    box(c, 236, 370, 140, 60, BOX_BLUE, "Query B", "uses 200 slots")
    box(c, 400, 370, 140, 60, BOX_BLUE, "Query C", "queued…")
    arrow(c, 142, 468, 142, 432, color=ACCENT)
    arrow(c, 306, 468, 306, 432, color=ACCENT)
    note(c, 72, 270, 468, "On-demand: pay per byte scanned. Flat-rate/reservations: buy slot capacity for predictable workloads. Either way, zero cluster management.")
    bullet_list(c, 72, 230, [
        "Columnar Capacitor storage + automatic sharding",
        "Dry-run queries to see bytes billed before running",
        "Partition + cluster tables to cut scanned bytes (and cost)"])
    footer(c, pg); c.showPage(); pg += 1

    # 4: zero-copy clone
    y = section_header(c, 4, 6, "Zero-Copy Cloning",
                       "Instant, storage-free copies of tables, schemas, even whole databases.")
    box(c, 72, 470, 180, 70, BOX_BLUE, "prod.orders", "1 TB")
    box(c, 360, 470, 180, 70, BOX_GREEN, "dev.orders_clone", "0 bytes new")
    arrow(c, 252, 505, 358, 505, color=GREEN, width=3, label="CLONE (metadata only)")
    note(c, 72, 370, 468, "A clone shares the underlying micro-partitions; only changed blocks consume new storage. CREATE TABLE … CLONE runs in seconds regardless of size.")
    bullet_list(c, 72, 330, [
        "Dev/test environments on full production data, instantly",
        "Safe schema experiments: clone, alter, validate, swap",
        "Drops are cheap — clones inherit the retention window"])
    footer(c, pg); c.showPage(); pg += 1

    # 5: time travel
    y = section_header(c, 5, 6, "Time Travel & Data Sharing",
                       "Query the past, share without copying.")
    box(c, 72, 470, 225, 70, BOX_TEAL, "Time Travel", "AS OF timestamp / offset")
    box(c, 315, 470, 225, 70, BOX_PURP, "Secure Data Sharing", "no copies, no ETL")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9)
    c.drawString(88, 430, "SELECT * FROM orders")
    c.drawString(88, 416, "  AT(OFFSET => -3600);")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(331, 430, "Share a live table with a partner")
    c.drawString(331, 414, "account — they query, you govern.")
    note(c, 72, 320, 468, "Time travel (up to 90 days) makes 'oops' recoverable: undrop tables, audit history, reproduce yesterday's report exactly.")
    footer(c, pg); c.showPage(); pg += 1

    # 6: cost discipline
    y = section_header(c, 6, 6, "Cost Discipline",
                       "Elastic compute is a superpower and a bill shock. Guardrails matter.")
    items = ["Auto-suspend warehouses after minutes of idle — always",
             "Separate warehouses per workload (BI vs ETL vs data science)",
             "Resource monitors: alert and auto-suspend at spend caps",
             "BigQuery: partition/cluster tables, avoid SELECT *",
             "Right-size: start small, scale up only when queries queue"]
    y = bullet_list(c, 72, y, items, font_size=11.5, gap=30)
    note(c, 72, 300, 468, "The #1 cloud-warehouse failure mode is an XL warehouse left running over the weekend. Automation beats willpower.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Snowflake & BigQuery — Remember",
                 ["Storage and compute scale independently: cheap shared storage, elastic compute that suspends to zero.",
                  "Micro-partitions with min/max metadata give automatic pruning — clustering keeps ranges tight.",
                  "BigQuery's slots abstract away servers entirely; you manage query capacity, not clusters.",
                  "Zero-copy clones create instant dev/test copies with no extra storage until data diverges.",
                  "Time travel recovers mistakes; secure sharing distributes data without copies. Guard the spend with auto-suspend."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_delta_lake(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Delta Lake\nVisual Guide",
               "ACID transactions on your data lake.\nReliability without giving up cheap storage.",
               CATEGORY, None); pg += 1

    # 1: the lake problem
    y = section_header(c, 1, 6, "The Data Lake Reliability Problem",
                       "Parquet on object storage is cheap — but concurrent writes corrupt it.")
    box(c, 72, 460, 180, 70, BOX_BLUE, "Writer A", "writing part-0001")
    box(c, 360, 460, 180, 70, BOX_BLUE, "Writer B", "writing part-0001")
    box(c, 196, 340, 220, 70, BOX_RED, "s3://lake/orders/", "which files are valid?!")
    arrow(c, 162, 458, 280, 412, color=RED)
    arrow(c, 450, 458, 330, 412, color=RED)
    note(c, 72, 240, 468, "Two writers, no coordination: partial files, duplicate rows, readers seeing half-written data. Lakes need a transaction layer.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: transaction log
    y = section_header(c, 2, 6, "The Transaction Log: The Source of Truth",
                       "Delta adds a _delta_log/ of ordered JSON commits on top of Parquet.")
    box(c, 72, 520, 468, 60, BOX_GREEN, "_delta_log/", "000000.json → 000001.json → 000002.json …")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9)
    c.drawString(88, 486, '{"add": {"path": "part-0007.parquet", "rows": 10000}}')
    c.drawString(88, 470, '{"remove": {"path": "part-0003.parquet"}}')
    box(c, 72, 380, 468, 60, BOX_BLUE, "Parquet data files", "immutable; never modified in place")
    arrow(c, 306, 518, 306, 442, color=ACCENT, label="log references")
    note(c, 72, 280, 468, "Writes are atomic: new Parquet files land first, then ONE log entry commits them. Readers replay the log to know exactly which files are current.")
    bullet_list(c, 72, 240, [
        "Optimistic concurrency: conflicting writers retry automatically",
        "Checkpoints (every 10 commits) keep log replay fast",
        "The log is the table — files alone are meaningless"])
    footer(c, pg); c.showPage(); pg += 1

    # 3: ACID demo
    y = section_header(c, 3, 6, "ACID on Object Storage",
                       "Serializable isolation and atomic multi-file commits — on S3/ADLS/GCS.")
    box(c, 72, 470, 140, 70, BOX_GREEN, "Atomicity", "all files or none")
    box(c, 236, 470, 140, 70, BOX_GREEN, "Consistency", "schema enforced")
    box(c, 400, 470, 140, 70, BOX_GREEN, "Isolation", "snapshot reads")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 420, "Readers always see a consistent snapshot: a query starting at commit 42")
    c.drawString(72, 402, "never sees commit 43's partial state. Schema enforcement rejects bad writes;")
    c.drawString(72, 384, "schema evolution allows deliberate, versioned changes.")
    note(c, 72, 290, 468, "This is what turns a 'data swamp' into a lakehouse: concurrent pipelines can safely read and write the same tables.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: time travel
    y = section_header(c, 4, 6, "Time Travel",
                       "Every commit is a version. Query any of them.")
    box(c, 72, 500, 120, 60, BOX_TEAL, "v0", "initial")
    box(c, 216, 500, 120, 60, BOX_TEAL, "v1", "+10k rows")
    box(c, 360, 500, 120, 60, BOX_TEAL, "v2", "delete bad day")
    arrow(c, 192, 530, 214, 530, color=ACCENT)
    arrow(c, 336, 530, 358, 530, color=ACCENT)
    c.setFillColor(INK); c.setFont(MONO_FONT, 10)
    c.drawString(72, 450, "SELECT * FROM orders VERSION AS OF 1;")
    c.drawString(72, 430, "SELECT * FROM orders TIMESTAMP AS OF '2026-10-01';")
    note(c, 72, 330, 468, "Audits, reproducible ML training sets, and one-command rollback: RESTORE TABLE orders TO VERSION AS OF 1.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: Z-order + optimize
    y = section_header(c, 5, 6, "Z-Ordering & OPTIMIZE",
                       "Co-locate related data so queries skip more files.")
    box(c, 72, 480, 225, 70, BOX_ORANGE, "Scattered", "customer rows in every file")
    box(c, 315, 480, 225, 70, BOX_GREEN, "Z-Ordered", "same customer, adjacent files")
    c.setFillColor(INK); c.setFont(MONO_FONT, 10)
    c.drawString(72, 430, "OPTIMIZE orders")
    c.drawString(72, 414, "  ZORDER BY (customer_id);")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(331, 430, "Compacts small files +")
    c.drawString(331, 414, "multi-dimensional clustering.")
    note(c, 72, 320, 468, "Streaming writes create thousands of tiny files (the 'small file problem'). OPTIMIZE compacts them; ZORDER clusters by the columns you filter on.")
    footer(c, pg); c.showPage(); pg += 1

    # 6: merge
    y = section_header(c, 6, 6, "MERGE: Upserts Done Right",
                       "Atomic insert/update/delete in one statement — CDC's best friend.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, y, "MERGE INTO orders t USING updates s")
    c.drawString(72, y - 20, "  ON t.id = s.id")
    c.drawString(72, y - 40, "WHEN MATCHED THEN UPDATE SET *")
    c.drawString(72, y - 60, "WHEN NOT MATCHED THEN INSERT *;")
    note(c, 72, y - 150, 468, "One atomic commit applies the whole change set — no partial upserts, no torn reads. This is how CDC streams land cleanly into lakehouse tables.")
    bullet_list(c, 72, y - 190, [
        "Change data feed: row-level change history for downstream consumers",
        "Deletes land as tombstones, then VACUUM reclaims old files",
        "Retention: keep 7+ days of history for time travel before vacuuming"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Delta Lake — Remember",
                 ["The _delta_log/ transaction log turns Parquet files into an ACID table: atomic commits, snapshot isolation.",
                  "Writers stage immutable Parquet files, then commit with a single log entry — readers replay the log.",
                  "Time travel queries any version; RESTORE rolls back bad writes in one command.",
                  "OPTIMIZE compacts small files; ZORDER BY co-locates related rows for faster skipping.",
                  "MERGE gives atomic upserts — the clean landing pattern for CDC streams."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_dbt(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "dbt\nVisual Guide",
               "Analytics engineering: SQL models,\ntests, and docs — with software discipline.",
               CATEGORY, None); pg += 1

    # 1: models
    y = section_header(c, 1, 6, "Models: SQL + Jinja",
                       "Each model is a SELECT that builds one table or view.")
    box(c, 72, 480, 220, 80, BOX_BLUE, "models/orders.sql", "{{ ref('stg_orders') }}")
    box(c, 340, 480, 200, 80, BOX_GREEN, "orders (table)", "built by dbt run")
    arrow(c, 292, 520, 338, 520, color=ACCENT, label="dbt run")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, 430, "SELECT id, total FROM {{ ref('stg_orders') }}")
    c.drawString(72, 414, "WHERE total > 0")
    note(c, 72, 320, 468, "ref() wires dependencies automatically — dbt builds the DAG from your SQL. Jinja adds loops, macros, and environment-aware logic.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: DAG
    y = section_header(c, 2, 6, "The Model DAG",
                       "dbt resolves refs into an execution graph and runs it in dependency order.")
    box(c, 72, 500, 120, 60, BOX_BLUE, "stg_orders", "staging")
    box(c, 72, 400, 120, 60, BOX_BLUE, "stg_users", "staging")
    box(c, 246, 450, 140, 60, BOX_TEAL, "orders", "marts")
    box(c, 420, 450, 120, 60, BOX_GREEN, "revenue", "marts")
    arrow(c, 192, 530, 244, 480, color=ACCENT)
    arrow(c, 192, 430, 244, 480, color=ACCENT)
    arrow(c, 386, 480, 418, 480, color=ACCENT)
    note(c, 72, 300, 468, "Independent models run in parallel; dependents wait. dbt run --select orders+ builds a model and everything downstream of it.")
    bullet_list(c, 72, 260, [
        "Staging: 1:1 with sources, light cleaning only",
        "Intermediate: reusable business logic",
        "Marts: one model per business entity, the BI layer"])
    footer(c, pg); c.showPage(); pg += 1

    # 3: materializations
    y = section_header(c, 3, 6, "Materializations",
                       "How each model is persisted — pick per model.")
    mats = [("view", "Always fresh, zero storage. Slow for heavy logic.", BOX_BLUE),
            ("table", "Rebuilt fully each run. Simple, expensive at scale.", BOX_ORANGE),
            ("incremental", "Only new/changed rows appended. The workhorse.", BOX_GREEN),
            ("ephemeral", "CTE in downstream models. Never persisted.", BOX_TEAL)]
    yy = y
    for name, desc, fill in mats:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=12)
        yy -= 72
    note(c, 72, yy - 20, 468, "Incremental models need an is_incremental() filter and a unique key — get those wrong and you silently duplicate rows.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: tests
    y = section_header(c, 4, 6, "Tests: Contracts on Your Data",
                       "Generic and custom tests run after every build.")
    tests = [("unique", "No duplicate keys", "not_null", "No missing values"),
             ("accepted_values", "Status in a known set", "relationships", "FK actually exists")]
    yy = y
    for n1, d1, n2, d2 in tests:
        box(c, 72, yy - 56, 225, 60, BOX_GREEN, n1, d1, font_size=11)
        box(c, 315, yy - 56, 225, 60, BOX_GREEN, n2, d2, font_size=11)
        yy -= 76
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, yy, "models:\n  - name: orders\n    tests:\n      - unique:\n          column_name: id")
    note(c, 72, yy - 100, 468, "Tests are queries that must return zero rows. dbt test fails the run on violations — bad data never reaches the marts silently.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: docs
    y = section_header(c, 5, 6, "Docs Generation",
                       "Documented models become a searchable data catalog for free.")
    box(c, 72, 480, 468, 70, BOX_PURP, "dbt docs generate", "static site from model + column descriptions")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, 430, 'description: "One row per completed order"')
    c.drawString(72, 414, "columns:\n  - name: total\n    description: 'USD, tax included'")
    note(c, 72, 320, 468, "Descriptions live next to the SQL in YAML — the docs site renders the DAG, column lineage, and tests together. Documentation that can't drift.")
    footer(c, pg); c.showPage(); pg += 1

    # 6: CI
    y = section_header(c, 6, 6, "CI for Analytics Code",
                       "Pull requests build and test changed models on a schedule-safe clone.")
    box(c, 72, 480, 140, 60, BOX_BLUE, "PR opened", "feature branch")
    box(c, 252, 480, 140, 60, BOX_ORANGE, "Slim CI", "build changed + downstream")
    box(c, 432, 480, 108, 60, BOX_GREEN, "Merge", "tests green")
    arrow(c, 212, 510, 250, 510, color=ACCENT)
    arrow(c, 392, 510, 430, 510, color=ACCENT)
    note(c, 72, 380, 468, "Slim CI (state:modified+) builds only what the PR touches plus downstream — fast feedback without rebuilding the warehouse.")
    bullet_list(c, 72, 340, [
        "dbt build = run + test + snapshot + seed in dependency order",
        "Snapshots capture slowly-changing dimensions over time",
        "Seeds version-control small CSVs (mappings, lookups)"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "dbt — Remember",
                 ["Models are SELECT statements; ref() builds the dependency DAG automatically.",
                  "Layer models: staging (raw 1:1) → intermediate (logic) → marts (business entities).",
                  "Choose materializations deliberately: views for freshness, incremental for scale.",
                  "Tests are zero-row queries that fail the build — data contracts enforced in CI.",
                  "Docs generate from YAML next to the SQL; slim CI tests only what changed."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_airflow(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Airflow Orchestration\nVisual Guide",
               "DAGs, operators, sensors, and backfills.\nHow pipelines get scheduled and supervised.",
               CATEGORY, None); pg += 1

    # 1: DAG anatomy
    y = section_header(c, 1, 6, "DAG Anatomy",
                       "A Directed Acyclic Graph: tasks with dependencies, no cycles.")
    box(c, 72, 500, 110, 60, BOX_BLUE, "extract", "task 1")
    box(c, 232, 500, 110, 60, BOX_BLUE, "transform", "task 2")
    box(c, 392, 500, 110, 60, BOX_GREEN, "load", "task 3")
    box(c, 232, 380, 110, 60, BOX_ORANGE, "notify", "on failure")
    arrow(c, 182, 530, 230, 530, color=ACCENT)
    arrow(c, 342, 530, 390, 530, color=ACCENT)
    arrow(c, 447, 498, 342, 412, color=RED)
    c.setFillColor(RED); c.setFont(BODY_FONT, 9)
    c.drawString(360, 450, "trigger rule")
    note(c, 72, 280, 468, "Edges are dependencies: transform waits for extract. Trigger rules (all_success, one_failed…) control when a task fires.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: operators
    y = section_header(c, 2, 6, "Operators: The Building Blocks",
                       "Each task is an operator — a template for a unit of work.")
    ops = [("BashOperator", "Run a shell command", "PythonOperator", "Call a Python function"),
           ("SQLOperator", "Execute SQL in a database", "Sensor", "Wait for a condition (file, partition)")]
    yy = y
    for n1, d1, n2, d2 in ops:
        box(c, 72, yy - 56, 225, 60, BOX_BLUE, n1, d1, font_size=11)
        box(c, 315, yy - 56, 225, 60, BOX_TEAL, n2, d2, font_size=11)
        yy -= 76
    note(c, 72, yy - 20, 468, "Deferrable operators (async) free the worker slot while waiting — critical at scale. Prefer them over polling sensors.")
    bullet_list(c, 72, yy - 60, [
        "Providers add 100+ operators: S3, Snowflake, dbt, Kubernetes…",
        "TaskFlow API (@task) wires XComs with plain Python returns",
        "Keep tasks idempotent — Airflow WILL retry them"])
    footer(c, pg); c.showPage(); pg += 1

    # 3: sensors
    y = section_header(c, 3, 6, "Sensors: Wait Smartly",
                       "Sensors pause a DAG until the world is ready.")
    box(c, 72, 480, 180, 70, BOX_ORANGE, "FileSensor", "wait for landing file")
    box(c, 292, 480, 180, 70, BOX_ORANGE, "ExternalTaskSensor", "wait for upstream DAG")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "poke_interval: check every N seconds.")
    c.drawString(72, 412, "mode='reschedule': release the worker slot between pokes —")
    c.drawString(72, 394, "a poking sensor should never hold a slot hostage.")
    note(c, 72, 300, 468, "Reschedule mode (or deferrable sensors) is the difference between a healthy cluster and one deadlocked by waiting tasks.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: scheduling & backfill
    y = section_header(c, 4, 6, "Scheduling & Backfill",
                       "Airflow schedules at the END of each interval — and can replay history.")
    box(c, 72, 500, 140, 60, BOX_BLUE, "data interval", "Jan 1 → Jan 2")
    box(c, 252, 500, 140, 60, BOX_GREEN, "run fires", "at Jan 2 00:00")
    arrow(c, 212, 530, 250, 530, color=ACCENT)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 450, "A @daily DAG's Jan-1 run starts when Jan 1's data is complete —")
    c.drawString(72, 432, "at the START of Jan 2. This confuses everyone exactly once.")
    note(c, 72, 340, 468, "Backfill: airflow dags backfill --start-date 2026-01-01 replays every missed interval — how you rebuild history after a logic fix.")
    bullet_list(c, 72, 300, [
        "catchup=True (default): missed intervals queue up on deploy",
        "Set catchup=False for DAGs that should only run forward",
        "Timetables: cron, deltas, or custom dataset-driven schedules"])
    footer(c, pg); c.showPage(); pg += 1

    # 5: XComs
    y = section_header(c, 5, 6, "XComs: Passing Small Data",
                       "Cross-communication: tasks share small values via the metadata DB.")
    box(c, 72, 480, 180, 70, BOX_BLUE, "task: get_date", 'return "2026-10-09"')
    box(c, 360, 480, 180, 70, BOX_GREEN, "task: load", 'ti.xcom_pull("get_date")')
    arrow(c, 252, 515, 358, 515, color=ACCENT, label="XCom")
    note(c, 72, 380, 468, "XComs are for small values (IDs, dates, row counts) — NOT dataframes. Push big data to storage and pass the path.")
    bullet_list(c, 72, 340, [
        "TaskFlow: `return` auto-pushes; function args auto-pull",
        "Custom XCom backends (S3/GCS) lift the size limit",
        "Never pass credentials via XCom — use Connections"])
    footer(c, pg); c.showPage(); pg += 1

    # 6: lifecycle
    y = section_header(c, 6, 6, "Task Lifecycle & Retries",
                       "Every task moves through states — design for the red ones.")
    states = [("queued → running → success", BOX_GREEN),
              ("failed → up_for_retry → running", BOX_ORANGE),
              ("upstream_failed / skipped", BOX_RED)]
    yy = y
    for label, fill in states:
        box(c, 72, yy - 48, 468, 52, fill, label, "", font_size=12)
        yy -= 68
    note(c, 72, yy - 20, 468, "retries + retry_delay + exponential backoff turn transient failures (API hiccups) into non-events. Alert only on final failure.")
    bullet_list(c, 72, yy - 60, [
        "SLAs: alert when a task runs longer than expected",
        "Pools: cap concurrency for fragile external systems",
        "on_failure_callback: page the human, with context"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Airflow Orchestration — Remember",
                 ["DAGs declare task dependencies; the scheduler executes them in topological order.",
                  "Operators are task templates; sensors wait for conditions — use reschedule/deferrable modes.",
                  "Runs fire at the END of each data interval; backfill replays history after logic fixes.",
                  "XComs pass small values between tasks; big data goes through storage, not the metadata DB.",
                  "Make tasks idempotent and retryable — retries with backoff absorb transient failures."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_data_quality(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Data Quality\nVisual Guide",
               "Trust your tables.\nChecks, anomalies, SLAs, and quarantine patterns.",
               CATEGORY, None); pg += 1

    # 1: dimensions
    y = section_header(c, 1, 6, "The Six Dimensions of Quality",
                       "If you can't name the dimension, you can't measure it.")
    dims = [("Accuracy", "Values reflect reality", BOX_GREEN),
            ("Completeness", "No missing critical fields", BOX_BLUE),
            ("Consistency", "Same fact, same value everywhere", BOX_TEAL),
            ("Timeliness", "Fresh enough for the decision", BOX_ORANGE),
            ("Validity", "Conforms to format/domain rules", BOX_PURP),
            ("Uniqueness", "No unintended duplicates", BOX_RED)]
    yy = y
    for i in range(0, 6, 2):
        box(c, 72, yy - 56, 225, 60, dims[i][2], dims[i][0], dims[i][1], font_size=11)
        box(c, 315, yy - 56, 225, 60, dims[i+1][2], dims[i+1][0], dims[i+1][1], font_size=11)
        yy -= 76
    note(c, 72, yy - 20, 468, "Every check you write maps to one of these. A 'data quality program' is just these six, measured continuously.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: GE checks
    y = section_header(c, 2, 6, "Expectation Checks",
                       "Declarative assertions on every batch — the Great Expectations pattern.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, y, 'expect_column_values_to_not_be_null("user_id")')
    c.drawString(72, y - 22, 'expect_column_values_to_be_between("age", 0, 120)')
    c.drawString(72, y - 44, 'expect_column_values_to_be_unique("order_id")')
    c.drawString(72, y - 66, 'expect_table_row_count_to_be_between(9000, 11000)')
    box(c, 72, y - 140, 225, 56, BOX_GREEN, "All pass ✓", "promote batch")
    box(c, 315, y - 140, 225, 56, BOX_RED, "Any fail ✗", "quarantine batch")
    arrow(c, 183, y - 84, 183, y - 138, color=ACCENT)
    arrow(c, 427, y - 84, 427, y - 138, color=ACCENT)
    note(c, 72, y - 210, 468, "Expectations run as part of the pipeline (dbt tests, Soda, GE). A failing suite blocks promotion — quality as a gate, not a report.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: anomaly detection
    y = section_header(c, 3, 6, "Anomaly Detection",
                       "Rules catch known bad; statistics catch unknown bad.")
    box(c, 72, 480, 468, 70, BOX_BLUE, "Row counts over time", "7-day rolling mean ± 3σ")
    c.setStrokeColor(ACCENT); c.setLineWidth(2)
    xs = [90 + i * 52 for i in range(9)]
    vals = [500, 510, 495, 505, 520, 498, 512, 180, 505]
    for i in range(8):
        c.line(xs[i], 430 + vals[i] * 0.08, xs[i+1], 430 + vals[i+1] * 0.08)
    c.setFillColor(RED)
    c.circle(xs[7], 430 + vals[7] * 0.08, 6, fill=1, stroke=0)
    c.setFont(BODY_FONT, 9); c.setFillColor(RED)
    c.drawString(xs[7] - 20, 430 + vals[7] * 0.08 - 18, "ANOMALY")
    note(c, 72, 330, 468, "Track volume, null rates, and distribution drift per table. A sudden dip often means an upstream source broke — hours before anyone notices.")
    bullet_list(c, 72, 290, [
        "Freshness monitors: alert when a table misses its SLA",
        "Schema drift detection: new/removed columns break silent contracts",
        "Seasonality-aware baselines beat fixed thresholds"])
    footer(c, pg); c.showPage(); pg += 1

    # 4: SLAs
    y = section_header(c, 4, 6, "Data SLAs",
                       "A contract between producers and consumers: what, when, how good.")
    box(c, 72, 470, 468, 100, BOX_TEAL, "orders table SLA", "")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(92, 540, "• Freshness: landed by 06:00 ET daily")
    c.drawString(92, 520, "• Completeness: ≥ 99.5% of source rows")
    c.drawString(92, 500, "• Validity: 100% of amounts ≥ 0, ISO currency codes")
    note(c, 72, 370, 468, "SLAs turn vague complaints ('the data feels off') into measurable breaches with owners and escalation paths.")
    bullet_list(c, 72, 330, [
        "Each SLA names an owner — unowned SLAs are wishes",
        "Breach → incident: page the producer, notify consumers",
        "Review quarterly: stale SLAs erode trust in all of them"])
    footer(c, pg); c.showPage(); pg += 1

    # 5: quarantine
    y = section_header(c, 5, 6, "Quarantine Pattern",
                       "Bad rows go somewhere — not into production, not into the void.")
    box(c, 72, 480, 140, 70, BOX_BLUE, "Incoming", "raw batch")
    box(c, 252, 480, 120, 70, BOX_ORANGE, "Validate", "expectations")
    box(c, 412, 480, 128, 70, BOX_GREEN, "Clean", "promote → marts")
    box(c, 252, 340, 120, 70, BOX_RED, "Quarantine", "bad rows + reasons")
    arrow(c, 212, 515, 250, 515, color=ACCENT, label="pass")
    arrow(c, 372, 515, 410, 515, color=ACCENT, label="pass")
    arrow(c, 312, 478, 312, 412, color=RED, label="fail")
    note(c, 72, 240, 468, "Quarantine tables keep the evidence: the row, the failed rule, the timestamp. Producers fix the source; analysts see what's excluded and why.")
    footer(c, pg); c.showPage(); pg += 1

    # 6: observability loop
    y = section_header(c, 6, 6, "The Quality Loop",
                       "Detect → triage → fix → prevent. Quality compounds.")
    box(c, 72, 480, 105, 60, BOX_RED, "Detect", "monitors")
    box(c, 197, 480, 105, 60, BOX_ORANGE, "Triage", "impact?")
    box(c, 322, 480, 105, 60, BOX_BLUE, "Fix", "source/pipeline")
    box(c, 447, 480, 93, 60, BOX_GREEN, "Prevent", "new check")
    for a, b in [(177, 195), (302, 320), (427, 445)]:
        arrow(c, a, 510, b, 510, color=ACCENT)
    arrow(c, 493, 478, 493, 440, color=GREEN)
    arrow(c, 493, 440, 120, 440, color=GREEN)
    arrow(c, 120, 440, 120, 478, color=GREEN)
    note(c, 72, 340, 468, "Every incident should produce a new automated check. A quality program that doesn't grow checks from incidents is just monitoring theater.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Data Quality — Remember",
                 ["Measure the six dimensions: accuracy, completeness, consistency, timeliness, validity, uniqueness.",
                  "Expectation checks (dbt tests, Soda, GE) gate promotion — bad data fails the build.",
                  "Anomaly detection on volume, null rates, and drift catches unknown-unknowns.",
                  "Data SLAs make quality contractual: named owners, measurable targets, breach escalation.",
                  "Quarantine bad rows with reasons attached; every incident should birth a new check."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_schema_evolution(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Schema Evolution\nVisual Guide",
               "Change your data shape without breaking\nproducers or consumers.",
               CATEGORY, None); pg += 1

    # 1: the problem
    y = section_header(c, 1, 6, "The Problem: Schemas Change",
                       "Add a field, rename a column — and every consumer breaks at 2 AM.")
    box(c, 72, 480, 180, 70, BOX_BLUE, "Producer v2", "adds 'loyalty_tier'")
    box(c, 360, 480, 180, 70, BOX_RED, "Consumer v1", "expects old schema ✗")
    arrow(c, 252, 515, 358, 515, color=RED, width=3, label="BREAKS")
    note(c, 72, 380, 468, "Without a compatibility contract, every schema change is a coordinated deployment across teams — or an outage.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: compatibility modes
    y = section_header(c, 2, 6, "Compatibility Modes",
                       "Avro and Protobuf define exactly which changes are safe.")
    modes = [("BACKWARD", "New readers read old data. Add optional fields freely.", BOX_GREEN),
             ("FORWARD", "Old readers read new data. Only remove optional fields.", BOX_BLUE),
             ("FULL", "Both directions. Safest, most restrictive.", BOX_TEAL),
             ("NONE", "No guarantees. Chaos mode — never in production.", BOX_RED)]
    yy = y
    for name, desc, fill in modes:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=12)
        yy -= 76
    note(c, 72, yy - 20, 468, "Default to BACKWARD: consumers upgrade first, then producers start writing new fields. Old consumers ignore what they don't know.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: schema registry
    y = section_header(c, 3, 6, "Schema Registry: The Gatekeeper",
                       "A central service that versions schemas and enforces compatibility.")
    box(c, 226, 500, 160, 70, BOX_PURP, "Schema Registry", "versions 1…N")
    box(c, 72, 360, 140, 70, BOX_BLUE, "Producer", "registers v3")
    box(c, 400, 360, 140, 70, BOX_GREEN, "Consumer", "fetches v3")
    arrow(c, 180, 395, 280, 500, color=ACCENT, label="check compat")
    arrow(c, 406, 500, 470, 432, color=ACCENT, label="fetch")
    note(c, 72, 260, 468, "Producer registers the new schema; the registry REJECTS it if it breaks compatibility with the previous version. Bad schemas never reach the wire.")
    bullet_list(c, 72, 220, [
        "Wire format carries only a schema ID — tiny payloads",
        "Consumers cache schemas locally, fetch on unknown ID",
        "One registry per organization, not per team"])
    footer(c, pg); c.showPage(); pg += 1

    # 4: safe changes
    y = section_header(c, 4, 6, "Safe vs Unsafe Changes",
                       "The cheat sheet for evolving Avro/Protobuf schemas.")
    box(c, 72, y - 130, 225, 130, BOX_GREEN, "SAFE ✓", "", font_size=14)
    box(c, 315, y - 130, 225, 130, BOX_RED, "UNSAFE ✗", "", font_size=14)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    safe = ["Add optional field (with default)", "Remove optional field", "Widen: int → long"]
    unsafe = ["Rename a field (it's add+remove!)", "Change type: string → int", "Remove a required field"]
    yy = y - 34
    for t in safe:
        c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 34
    for t in unsafe:
        c.drawString(331, yy, "• " + t); yy -= 18
    note(c, 72, y - 190, 468, "Renaming is the classic trap: to consumers it's a deletion plus an addition. Deprecate the old field, add the new one, remove later.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: migration recipe
    y = section_header(c, 5, 6, "The Safe Migration Recipe",
                       "Expand, migrate, contract — never a big bang.")
    box(c, 72, 480, 130, 60, BOX_GREEN, "1. Expand", "add new field")
    box(c, 242, 480, 130, 60, BOX_BLUE, "2. Migrate", "dual-write/read")
    box(c, 412, 480, 128, 60, BOX_ORANGE, "3. Contract", "drop old field")
    arrow(c, 202, 510, 240, 510, color=ACCENT)
    arrow(c, 372, 510, 410, 510, color=ACCENT)
    note(c, 72, 380, 468, "Each phase is independently deployable and rollback-safe. The old field stays until every consumer has migrated — measure before contracting.")
    bullet_list(c, 72, 340, [
        "Phase 1: producers write both fields; consumers read old",
        "Phase 2: consumers switch to new; keep dual-write",
        "Phase 3: stop writing old; registry retires it"])
    footer(c, pg); c.showPage(); pg += 1

    # 6: Protobuf vs Avro
    y = section_header(c, 6, 6, "Avro vs Protobuf",
                       "Two ecosystems, same discipline.")
    box(c, 72, y - 120, 225, 120, BOX_BLUE, "Avro", "schema travels with data", font_size=13)
    box(c, 315, y - 120, 225, 120, BOX_TEAL, "Protobuf", "code-generated stubs", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    avro = ["JSON schemas, dynamic", "Hadoop/Spark/Kafka native", "Reader/writer schema resolution"]
    pb = ["IDL + generated classes", "gRPC ecosystem standard", "Field numbers = identity"]
    yy = y - 30
    for t in avro:
        c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 30
    for t in pb:
        c.drawString(331, yy, "• " + t); yy -= 18
    note(c, 72, y - 180, 468, "Protobuf field numbers are forever — never reuse a retired number. Avro resolves by name — never rename casually. Both rules prevent silent corruption.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Schema Evolution — Remember",
                 ["Compatibility modes (backward/forward/full) define exactly which schema changes are safe.",
                  "A schema registry versions schemas and rejects incompatible ones before they reach the wire.",
                  "Safe: add optional fields with defaults. Unsafe: renames and type changes.",
                  "Migrate with expand → migrate → contract; never big-bang a schema change.",
                  "Protobuf: never reuse field numbers. Avro: fields are resolved by name."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_cdc(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Change Data Capture\nVisual Guide",
               "Stream every insert, update, and delete.\nLog-based CDC with Debezium and the outbox pattern.",
               CATEGORY, None); pg += 1

    # 1: why CDC
    y = section_header(c, 1, 6, "Why Capture Changes?",
                       "Batch ETL re-reads whole tables. CDC streams only what changed.")
    box(c, 72, 480, 225, 70, BOX_RED, "Batch", "SELECT * nightly — 10M rows")
    box(c, 315, 480, 225, 70, BOX_GREEN, "CDC", "stream 50k changed rows")
    note(c, 72, 380, 468, "CDC gives near-real-time freshness at a fraction of the source load — and captures deletes, which batch snapshots miss entirely.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: three approaches
    y = section_header(c, 2, 6, "Three CDC Approaches",
                       "Polling, triggers, and log-based — only one scales cleanly.")
    appr = [("Polling (timestamps)", "WHERE updated_at > last_run. Misses deletes; late-arriving rows slip.", BOX_ORANGE),
            ("Triggers", "DB trigger writes to a shadow table. Correct but slows every write.", BOX_RED),
            ("Log-based", "Read the DB's replication log. No impact on writes, captures everything.", BOX_GREEN)]
    yy = y
    for name, desc, fill in appr:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=12)
        yy -= 76
    note(c, 72, yy - 20, 468, "Log-based CDC piggybacks on the mechanism databases already use for replication — it's the only approach with near-zero source overhead.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: Debezium architecture
    y = section_header(c, 3, 6, "Debezium: Log-Based CDC in Practice",
                       "A Kafka Connect source connector that tails the database log.")
    box(c, 72, 500, 130, 70, BOX_BLUE, "Postgres", "WAL (write-ahead log)")
    box(c, 252, 500, 140, 70, BOX_ORANGE, "Debezium", "Kafka Connect")
    box(c, 442, 500, 98, 70, BOX_GREEN, "Kafka", "topics")
    arrow(c, 202, 535, 250, 535, color=ACCENT, label="tails WAL")
    arrow(c, 392, 535, 440, 535, color=ACCENT, label="emits events")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9)
    c.drawString(72, 450, '{"op": "u", "before": {...}, "after": {...}}')
    c.drawString(72, 434, "op: c=create, u=update, d=delete, r=snapshot read")
    note(c, 72, 340, 468, "Each event carries before/after images and the source position. One topic per table; consumers replay from any offset for reprocessing.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: outbox pattern
    y = section_header(c, 4, 6, "The Outbox Pattern",
                       "Atomically publish domain events from a transactional service.")
    box(c, 72, 480, 200, 70, BOX_BLUE, "Service", "1 txn: update + outbox row")
    box(c, 340, 480, 200, 70, BOX_GREEN, "Outbox table", "unpublished events")
    arrow(c, 272, 515, 338, 515, color=ACCENT, label="same txn")
    box(c, 226, 340, 160, 60, BOX_ORANGE, "Relay (Debezium)", "publishes → Kafka")
    arrow(c, 440, 478, 380, 402, color=ACCENT)
    note(c, 72, 240, 468, "The dual-write problem: updating the DB and publishing to Kafka can't both be atomic — unless the 'publish' is a row in the same transaction. The relay does the actual publishing.")
    bullet_list(c, 72, 200, [
        "Outbox rows are deleted (or marked) after publishing",
        "Consumers must be idempotent — at-least-once delivery",
        "The pattern works for any service that owns a database"])
    footer(c, pg); c.showPage(); pg += 1

    # 5: ordering & exactly-once
    y = section_header(c, 5, 6, "Ordering & Delivery Guarantees",
                       "What CDC promises — and what it doesn't.")
    bullet_list(c, 72, y, [
        "Per-row ordering: events for one row arrive in commit order (same topic partition)",
        "Cross-table ordering: NOT guaranteed — join carefully downstream",
        "Snapshots: initial consistent snapshot before streaming (no missed rows)",
        "At-least-once delivery: sinks must dedupe on (table, key, position)",
        "Schema changes in source propagate — pin consumer schemas deliberately"], font_size=11, gap=28)
    note(c, 72, 300, 468, "Design sinks for idempotent upserts keyed on the source primary key — replays become safe instead of scary.")
    footer(c, pg); c.showPage(); pg += 1

    # 6: landing
    y = section_header(c, 6, 6, "Landing CDC into the Lakehouse",
                       "From Kafka topics to queryable tables.")
    box(c, 72, 480, 130, 60, BOX_BLUE, "Kafka", "CDC topics")
    box(c, 242, 480, 130, 60, BOX_ORANGE, "Stream job", "Spark/Flink")
    box(c, 412, 480, 128, 60, BOX_GREEN, "Delta table", "MERGE upserts")
    arrow(c, 202, 510, 240, 510, color=ACCENT)
    arrow(c, 372, 510, 410, 510, color=ACCENT)
    note(c, 72, 380, 468, "The canonical landing: streaming MERGE INTO the Delta table on primary key, handling c/u/d ops. Deletes become tombstones; late data replays cleanly.")
    bullet_list(c, 72, 340, [
        "Bronze: raw CDC events, append-only (audit trail)",
        "Silver: current state via MERGE (queryable)",
        "Monitor lag: source position vs consumer offset per table"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Change Data Capture — Remember",
                 ["CDC streams only changed rows — fresher than batch, lighter on the source, and it captures deletes.",
                  "Log-based CDC (Debezium tailing the WAL) has near-zero write impact, unlike polling or triggers.",
                  "The outbox pattern makes event publishing atomic with the business transaction.",
                  "Expect at-least-once delivery and per-row (not cross-table) ordering — sinks must be idempotent.",
                  "Land with streaming MERGE: bronze keeps the raw event history, silver holds current state."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_data_governance(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Data Governance\nVisual Guide",
               "Who owns the data, who can see it,\nand how PII stays protected.",
               CATEGORY, None); pg += 1

    # 1: why
    y = section_header(c, 1, 6, "Why Governance Exists",
                       "Data without governance is a liability with a query engine.")
    box(c, 72, 480, 140, 70, BOX_RED, "Breach", "PII exposed")
    box(c, 236, 480, 140, 70, BOX_RED, "Fine", "GDPR/CCPA")
    box(c, 400, 480, 140, 70, BOX_RED, "Distrust", "nobody believes reports")
    note(c, 72, 380, 468, "Governance isn't bureaucracy — it's the system that lets you say YES to data access safely, instead of defaulting to NO.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: ownership
    y = section_header(c, 2, 6, "Ownership: Every Dataset Has an Owner",
                       "If everyone owns it, no one does.")
    box(c, 72, 480, 225, 70, BOX_BLUE, "Data Owner", "accountable executive/team")
    box(c, 315, 480, 225, 70, BOX_GREEN, "Data Steward", "day-to-day quality & definitions")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Owner: decides who gets access, signs off on classification.")
    c.drawString(72, 412, "Steward: maintains definitions, monitors quality, triages issues.")
    c.drawString(72, 394, "Custodian (platform team): operates the storage and tooling.")
    note(c, 72, 300, 468, "The RACI for data: owner accountable, steward responsible, consumers informed. Write it down per domain — tribal knowledge doesn't scale.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: classification
    y = section_header(c, 3, 6, "Classification Tiers",
                       "Not all data is equal — label it, then enforce per tier.")
    tiers = [("Public", "Marketing copy, published stats — no restrictions", BOX_GREEN),
             ("Internal", "Dashboards, aggregates — employees only", BOX_BLUE),
             ("Confidential", "Salaries, contracts — named access", BOX_ORANGE),
             ("Restricted / PII", "SSN, health, biometrics — masked by default", BOX_RED)]
    yy = y
    for name, desc, fill in tiers:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=12)
        yy -= 72
    note(c, 72, yy - 20, 468, "Classification drives everything downstream: masking rules, retention, who approves access. Auto-classify with scanners; humans confirm.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: access policies
    y = section_header(c, 4, 6, "Access Policies",
                       "From coarse roles to fine-grained, policy-as-code control.")
    box(c, 72, 500, 468, 60, BOX_BLUE, "RBAC", "analysts → read marts; engineers → read/write staging")
    box(c, 72, 410, 468, 60, BOX_TEAL, "ABAC / row-column security", "region = user's region; salary column masked")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(88, 448, "GRANT SELECT ON marts.orders TO ROLE analyst;")
    c.drawString(88, 376, "MASKING POLICY ssn_mask AS (val) RETURNS ...")
    note(c, 72, 310, 468, "Prefer group/role-based grants over per-user grants, and define masking in the warehouse — not in each BI tool — so policy is inescapable.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: PII handling
    y = section_header(c, 5, 6, "PII Handling Toolkit",
                       "Four techniques, from reversible to destructive.")
    techs = [("Masking", "Show ***-**-1234 to unauthorized roles — data stays, visibility shrinks", BOX_ORANGE),
             ("Tokenization", "Replace with random tokens; mapping vaulted separately", BOX_BLUE),
             ("Hashing", "One-way for joins/analytics; salt it or it's reversible", BOX_TEAL),
             ("Deletion", "Right-to-be-forgotten: hard delete + purge backups on schedule", BOX_RED)]
    yy = y
    for name, desc, fill in techs:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=12)
        yy -= 76
    note(c, 72, yy - 20, 468, "Mask by default, reveal by exception with approval and audit trail. Every unmasking should answer: who, why, and for how long.")
    footer(c, pg); c.showPage(); pg += 1

    # 6: audit
    y = section_header(c, 6, 6, "Audit & Lineage Close the Loop",
                       "Prove who touched what, when — and where it flowed.")
    box(c, 72, 480, 140, 70, BOX_PURP, "Access logs", "who queried what")
    box(c, 252, 480, 140, 70, BOX_PURP, "Lineage", "where PII flowed")
    box(c, 432, 480, 108, 70, BOX_PURP, "Reviews", "quarterly recert")
    arrow(c, 212, 515, 250, 515, color=ACCENT)
    arrow(c, 392, 515, 430, 515, color=ACCENT)
    note(c, 72, 380, 468, "Access reviews recertify grants quarterly — stale access is the #1 finding in every audit. Lineage proves PII handling end-to-end for regulators.")
    bullet_list(c, 72, 340, [
        "Log every query against restricted tables (who, when, how many rows)",
        "Alert on anomalous access: bulk exports, off-hours reads",
        "Retention policies: delete data you no longer need — you can't leak what you don't have"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Data Governance — Remember",
                 ["Every dataset needs a named owner (accountable) and steward (day-to-day) — unowned data rots.",
                  "Classify into tiers (public → restricted); classification drives masking, retention, and approvals.",
                  "Grant via roles, mask in the warehouse, and prefer policy-as-code over ticket-driven access.",
                  "PII toolkit: masking, tokenization, hashing, deletion — mask by default, reveal by exception.",
                  "Audit logs plus lineage prove compliance; recertify access quarterly and delete what you don't need."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_data_catalogs(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Data Catalogs\nVisual Guide",
               "Find the right dataset in minutes,\nnot Slack threads.",
               CATEGORY, None); pg += 1

    # 1: discovery problem
    y = section_header(c, 1, 6, "The Discovery Problem",
                       "The average analyst spends a day a week just finding data.")
    box(c, 72, 460, 140, 70, BOX_RED, "orders", "3 versions?!")
    box(c, 236, 460, 140, 70, BOX_RED, "orders_v2", "deprecated?")
    box(c, 400, 460, 140, 70, BOX_RED, "orders_final_FINAL", "abandoned")
    note(c, 72, 360, 468, "Without a catalog: duplicate tables, tribal knowledge, and the same 'which orders table?' question every onboarding.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: catalog anatomy
    y = section_header(c, 2, 6, "Catalog Anatomy",
                       "What a catalog records about every dataset.")
    parts = [("Technical metadata", "Schema, types, partitions, storage location — harvested automatically", BOX_BLUE),
             ("Business context", "Owner, description, glossary terms, SLAs — curated by humans", BOX_GREEN),
             ("Usage signals", "Query counts, popular columns, downstream dashboards — computed", BOX_ORANGE),
             ("Quality signals", "Freshness, test status, incident history — from monitors", BOX_TEAL)]
    yy = y
    for name, desc, fill in parts:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=12)
        yy -= 76
    note(c, 72, yy - 20, 468, "Automation harvests the technical layer; humans add the meaning. A catalog with only auto-harvested metadata is a phone book with no names.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: search
    y = section_header(c, 3, 6, "Search That Actually Works",
                       "Analysts search like humans — the catalog must rank like one.")
    box(c, 72, 480, 468, 60, BOX_BLUE, '"monthly revenue by region"', "natural-language search")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Ranking signals: name match < description match < glossary term <")
    c.drawString(72, 412, "certified badge < usage popularity. The most-queried, certified")
    c.drawString(72, 394, "table should win — not the alphabetically first duplicate.")
    note(c, 72, 300, 468, "Certification badges ('verified by data team') are the strongest trust signal. Uncertified tables get a warning, not a ban.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: glossary
    y = section_header(c, 4, 6, "Business Glossary",
                       "One definition per term, agreed once, referenced everywhere.")
    box(c, 72, 480, 225, 70, BOX_PURP, '"Active customer"', "purchased in last 12 months")
    box(c, 315, 480, 225, 70, BOX_PURP, '"Revenue"', "recognized, net of refunds, USD")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Terms link to the columns and tables that implement them.")
    c.drawString(72, 412, "Two teams, one definition of 'revenue' — the end of")
    c.drawString(72, 394, "dueling dashboards in the exec meeting.")
    note(c, 72, 300, 468, "The glossary is a social contract first, a feature second. Get finance and product to sign the definitions before encoding them.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: popularity
    y = section_header(c, 5, 6, "Popularity Signals",
                       "Usage data tells you what's trusted — and what's dead.")
    box(c, 72, 470, 140, 70, BOX_GREEN, "Hot", "queried daily, many users")
    box(c, 236, 470, 140, 70, BOX_ORANGE, "Cooling", "usage declining")
    box(c, 400, 470, 140, 70, BOX_RED, "Dead", "zero queries, 90 days")
    note(c, 72, 370, 468, "Popularity drives deprecation: announce, migrate consumers, then drop. It also surfaces the 'golden' tables new hires should start from.")
    bullet_list(c, 72, 330, [
        "Track: distinct users, query volume, downstream dashboard count",
        "Dead tables still cost storage and confuse search — deprecate them",
        "Lineage + popularity: deprecating a table shows every affected dashboard"])
    footer(c, pg); c.showPage(); pg += 1

    # 6: adoption
    y = section_header(c, 6, 6, "Making the Catalog Stick",
                       "A catalog nobody opens is shelfware.")
    items = ["Embed in the workflow: catalog links in BI tools, SQL editors, Slack",
             "Make owners curate: descriptions and certification are part of 'done'",
             "Seed with the top 50 tables — coverage of everything can wait",
             "Measure: search success rate, time-to-first-query for new hires",
             "Treat the catalog as a product with a roadmap, not a project"]
    y = bullet_list(c, 72, y, items, font_size=11.5, gap=30)
    note(c, 72, 300, 468, "Start where the pain is: the 20 tables everyone asks about. A thin catalog people use beats a complete one they ignore.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Data Catalogs — Remember",
                 ["Catalogs solve discovery: one searchable place for technical metadata, business context, and trust signals.",
                  "Automate the technical harvest; humans curate descriptions, owners, and glossary terms.",
                  "Rank search by meaning and popularity, and badge certified tables as the trusted choice.",
                  "A shared business glossary ends definition wars — get sign-off before encoding.",
                  "Popularity signals drive deprecation; embed the catalog where analysts already work."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_dimensional_modeling(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Dimensional Modeling\nVisual Guide",
               "Facts, dimensions, grain, and SCDs.\nDesign tables humans can actually query.",
               CATEGORY, None); pg += 1

    # 1: facts vs dimensions
    y = section_header(c, 1, 6, "Facts vs Dimensions",
                       "The two table types everything else is built from.")
    box(c, 72, 470, 225, 120, BOX_BLUE, "Fact table", "measurements of events", font_size=13)
    box(c, 315, 470, 225, 120, BOX_GREEN, "Dimension table", "descriptive context", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    facts = ["Long and narrow: billions of rows", "Numeric measures: amount, qty", "Foreign keys to dimensions"]
    dims = ["Short and wide: thousands of rows", "Text attributes: name, category", "Surrogate primary keys"]
    yy = y - 30
    for t in facts:
        c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 30
    for t in dims:
        c.drawString(331, yy, "• " + t); yy -= 18
    note(c, 72, y - 170, 468, "Facts answer 'how much / how many'; dimensions answer 'by what'. Keep measures additive and dimensions denormalized.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: grain
    y = section_header(c, 2, 6, "Grain: The Most Important Decision",
                       "Grain = what one row represents. Declare it before modeling anything.")
    box(c, 72, 500, 468, 60, BOX_ORANGE, '"One row per order line item"', "the grain statement")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 450, "Too coarse (one row per order): you can't analyze products.")
    c.drawString(72, 432, "Too fine (one row per scan event): billions of rows nobody queries.")
    c.drawString(72, 414, "Mixed grain in one fact: measures stop being comparable — never do this.")
    note(c, 72, 320, 468, "If you can't state the grain in one sentence, you don't understand the business process yet. Go back and ask.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: star
    y = section_header(c, 3, 6, "The Star: Fact in the Center",
                       "One fact table joined directly to denormalized dimensions.")
    box(c, 226, 430, 160, 70, BOX_BLUE, "fact_orders", "order_id, amounts, FKs")
    box(c, 72, 560, 130, 60, BOX_GREEN, "dim_customer", "")
    box(c, 410, 560, 130, 60, BOX_GREEN, "dim_product", "")
    box(c, 72, 300, 130, 60, BOX_GREEN, "dim_date", "")
    box(c, 410, 300, 130, 60, BOX_GREEN, "dim_store", "")
    for x1, y1, x2, y2 in [(200, 560, 280, 500), (470, 560, 330, 500),
                            (200, 360, 280, 430), (470, 360, 330, 430)]:
        arrow(c, x1, y1, x2, y2, color=ACCENT)
    note(c, 72, 200, 468, "Single-hop joins make star schemas fast and obvious — BI tools generate correct SQL from them with minimal configuration.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: SCD intro
    y = section_header(c, 4, 6, "Slowly Changing Dimensions",
                       "Customers move, products get rebranded. How do you keep history?")
    box(c, 72, 480, 140, 70, BOX_BLUE, "Type 1", "overwrite — no history")
    box(c, 236, 480, 140, 70, BOX_GREEN, "Type 2", "new row — full history")
    box(c, 400, 480, 140, 70, BOX_TEAL, "Type 3", "new column — limited history")
    note(c, 72, 380, 468, "Type 1 for corrections ('the name was misspelled'). Type 2 for real history ('she moved from FL to MA'). Type 3 when you only need previous vs current.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: SCD2 detail
    y = section_header(c, 5, 6, "Type 2 in Detail",
                       "New row per change, with effective dates and a current flag.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 8.5)
    hdr = "sk   | cust_id | city        | eff_from   | eff_to     | current"
    rows = ["101  | C-42    | Orlando     | 2024-01-01 | 2026-09-30 | N",
            "102  | C-42    | Boston      | 2026-10-01 | 9999-12-31 | Y"]
    c.drawString(72, y, hdr)
    c.drawString(72, y - 18, rows[0])
    c.drawString(72, y - 36, rows[1])
    note(c, 72, y - 110, 468, "Surrogate key (sk) is the dimension's PK; the natural key (cust_id) repeats. Facts join on sk to pin the historically-correct version.")
    bullet_list(c, 72, y - 150, [
        "dbt snapshots automate Type 2 with timestamp or check strategies",
        "Current flag + eff_to = 9999-12-31 makes 'as of now' queries trivial",
        "Point-in-time joins: fact date BETWEEN eff_from AND eff_to"])
    footer(c, pg); c.showPage(); pg += 1

    # 6: conformed dimensions
    y = section_header(c, 6, 6, "Conformed Dimensions",
                       "One dim_date shared by every fact = consistent reporting.")
    box(c, 226, 450, 160, 60, BOX_GREEN, "dim_date", "shared everywhere")
    box(c, 72, 560, 140, 60, BOX_BLUE, "fact_orders", "")
    box(c, 400, 560, 140, 60, BOX_BLUE, "fact_returns", "")
    box(c, 226, 330, 160, 60, BOX_BLUE, "fact_inventory", "")
    for x1, y1, x2, y2 in [(142, 558, 280, 512), (470, 558, 330, 512), (306, 448, 306, 392)]:
        arrow(c, x1, y1, x2, y2, color=ACCENT)
    note(c, 72, 230, 468, "Conformed dimensions are the enterprise bus: 'month' means the same in sales, finance, and marketing. Build them once, reuse forever.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Dimensional Modeling — Remember",
                 ["Facts hold measurable events; dimensions hold descriptive context. Facts are long, dimensions are wide.",
                  "Declare the grain in one sentence before modeling — mixed grain breaks comparability.",
                  "Star schemas join facts directly to denormalized dimensions: fast, simple, BI-friendly.",
                  "SCD Type 1 overwrites, Type 2 versions history with effective dates, Type 3 keeps previous values.",
                  "Conformed dimensions (one dim_date for all facts) keep the whole warehouse speaking one language."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_star_schema(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Star vs Snowflake Schema\nVisual Guide",
               "Denormalize or normalize?\nThe trade-off at the heart of analytics modeling.",
               CATEGORY, None); pg += 1

    # 1: star diagram
    y = section_header(c, 1, 6, "The Star Schema",
                       "Denormalized dimensions, single-hop joins.")
    box(c, 226, 430, 160, 70, BOX_BLUE, "fact_sales", "center")
    box(c, 72, 560, 130, 60, BOX_GREEN, "dim_product", "category inlined")
    box(c, 410, 560, 130, 60, BOX_GREEN, "dim_customer", "region inlined")
    box(c, 72, 300, 130, 60, BOX_GREEN, "dim_date", "")
    box(c, 410, 300, 130, 60, BOX_GREEN, "dim_store", "")
    for x1, y1, x2, y2 in [(200, 560, 280, 500), (470, 560, 330, 500),
                            (200, 360, 280, 430), (470, 360, 330, 430)]:
        arrow(c, x1, y1, x2, y2, color=ACCENT)
    note(c, 72, 200, 468, "Dimension attributes are flattened into the dimension table — category lives IN dim_product. Redundant storage, trivial queries.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: snowflake diagram
    y = section_header(c, 2, 6, "The Snowflake Schema",
                       "Normalized dimensions, multi-hop joins.")
    box(c, 226, 400, 160, 70, BOX_BLUE, "fact_sales", "center")
    box(c, 226, 540, 160, 60, BOX_GREEN, "dim_product", "")
    box(c, 72, 620, 130, 55, BOX_TEAL, "dim_category", "")
    box(c, 410, 620, 130, 55, BOX_TEAL, "dim_brand", "")
    arrow(c, 306, 538, 306, 472, color=ACCENT)
    arrow(c, 200, 618, 280, 602, color=TEAL)
    arrow(c, 412, 618, 330, 602, color=TEAL)
    note(c, 72, 300, 468, "dim_product now points to dim_category and dim_brand. Storage is lean, but 'sales by category' needs two joins — and BI tools must model the chain.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: trade-offs
    y = section_header(c, 3, 6, "The Trade-Off Matrix",
                       "What you gain and pay with each shape.")
    box(c, 72, y - 130, 225, 130, BOX_GREEN, "Star wins", "", font_size=13)
    box(c, 315, y - 130, 225, 130, BOX_TEAL, "Snowflake wins", "", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    star = ["Simple, fast queries", "BI-tool friendly", "Storage is cheap anyway"]
    snow = ["No update anomalies", "Enforced hierarchies", "Huge shared dimensions"]
    yy = y - 30
    for t in star:
        c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 30
    for t in snow:
        c.drawString(331, yy, "• " + t); yy -= 18
    note(c, 72, y - 190, 468, "In cloud warehouses storage is the cheapest resource — star's redundancy costs pennies while its simplicity saves engineering hours.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: query patterns
    y = section_header(c, 4, 6, "Query Pattern Comparison",
                       "Same question, different SQL.")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 10)
    c.drawString(72, y, "Star: one join")
    c.setFont(MONO_FONT, 9)
    c.drawString(72, y - 22, "SELECT p.category, SUM(f.amount)")
    c.drawString(72, y - 38, "FROM fact_sales f JOIN dim_product p")
    c.drawString(72, y - 54, "  ON f.product_sk = p.product_sk GROUP BY 1;")
    c.setFont(TITLE_FONT, 10)
    c.drawString(72, y - 90, "Snowflake: two joins")
    c.setFont(MONO_FONT, 9)
    c.drawString(72, y - 112, "SELECT c.name, SUM(f.amount)")
    c.drawString(72, y - 128, "FROM fact_sales f")
    c.drawString(72, y - 144, "JOIN dim_product p ON f.product_sk = p.product_sk")
    c.drawString(72, y - 160, "JOIN dim_category c ON p.category_sk = c.category_sk")
    c.drawString(72, y - 176, "GROUP BY 1;")
    note(c, 72, y - 240, 468, "Multiply this by every analyst, every dashboard, every ad-hoc question. Join chains are a tax paid forever.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: when to snowflake
    y = section_header(c, 5, 6, "When Snowflaking Makes Sense",
                       "Exceptions to the star default.")
    items = ["Massive shared hierarchies (a 10M-row geography tree) where duplication hurts",
             "Strict write integrity: one place to update a category name",
             "Source-system fidelity: staging mirrors the OLTP schema before modeling",
             "Many-to-many bridges (product ↔ promotion) still need bridge tables even in stars"]
    y = bullet_list(c, 72, y, items, font_size=11.5, gap=30)
    note(c, 72, 300, 468, "Rule of thumb: model the marts as stars; let staging stay normalized. Snowflake the exception, not the default.")
    footer(c, pg); c.showPage(); pg += 1

    # 6: galaxy
    y = section_header(c, 6, 6, "Beyond: Galaxy / Constellation",
                       "Multiple fact tables sharing conformed dimensions.")
    box(c, 72, 500, 140, 60, BOX_BLUE, "fact_orders", "")
    box(c, 400, 500, 140, 60, BOX_BLUE, "fact_shipments", "")
    box(c, 226, 380, 160, 60, BOX_GREEN, "dim_customer", "conformed")
    box(c, 226, 280, 160, 60, BOX_GREEN, "dim_date", "conformed")
    for x1, y1, x2, y2 in [(142, 498, 280, 442), (470, 498, 330, 442),
                            (200, 498, 280, 342), (412, 498, 330, 342)]:
        arrow(c, x1, y1, x2, y2, color=ACCENT)
    note(c, 72, 180, 468, "Real warehouses are constellations: many fact tables (each a star) sharing conformed dimensions. Drill-across queries work because 'customer' means the same thing everywhere.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Star vs Snowflake Schema — Remember",
                 ["Star: denormalized dimensions, single-hop joins — simple queries, BI-friendly, tiny storage cost.",
                  "Snowflake: normalized dimensions, multi-hop joins — lean storage, complex queries.",
                  "In cloud warehouses, storage is cheap: default to star for marts.",
                  "Snowflake the exceptions: giant shared hierarchies, strict write integrity, source-faithful staging.",
                  "Real warehouses are constellations — multiple star facts sharing conformed dimensions."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_olap_oltp(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "OLAP vs OLTP\nVisual Guide",
               "Transactions vs analytics.\nTwo workload shapes, two storage philosophies.",
               CATEGORY, None); pg += 1

    # 1: workload shapes
    y = section_header(c, 1, 6, "Two Workload Shapes",
                       "OLTP: many tiny writes. OLAP: few giant reads.")
    box(c, 72, 470, 225, 120, BOX_BLUE, "OLTP", "online transaction processing", font_size=13)
    box(c, 315, 470, 225, 120, BOX_GREEN, "OLAP", "online analytical processing", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    oltp = ["Thousands of small transactions/sec", "Read + write one row at a time", "Needs: ACID, low latency, concurrency"]
    olap = ["Few queries, each scans millions of rows", "Read-mostly, bulk loads", "Needs: throughput, compression, aggregation"]
    yy = y - 30
    for t in oltp:
        c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 30
    for t in olap:
        c.drawString(331, yy, "• " + t); yy -= 18
    note(c, 72, y - 170, 468, "Example: the checkout page is OLTP (one order, milliseconds). The 'revenue by quarter' dashboard is OLAP (ten million orders, seconds).")
    footer(c, pg); c.showPage(); pg += 1

    # 2: row vs columnar
    y = section_header(c, 2, 6, "Row vs Columnar Storage",
                       "Storage layout follows the access pattern.")
    box(c, 72, 500, 225, 80, BOX_BLUE, "Row store", "Postgres, MySQL")
    box(c, 315, 500, 225, 80, BOX_GREEN, "Columnar", "Snowflake, BigQuery, Redshift")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9)
    c.drawString(88, 470, "[r1: id,name,amt]")
    c.drawString(88, 456, "[r2: id,name,amt]  → whole rows together")
    c.drawString(331, 470, "[id: 1,2,3…]")
    c.drawString(331, 456, "[amt: 9,4,7…]  → one column together")
    c.setFont(BODY_FONT, 10.5); c.setFillColor(INK)
    c.drawString(72, 420, "OLTP reads whole rows (SELECT * WHERE id=…) → row storage wins.")
    c.drawString(72, 402, "OLAP reads few columns over many rows (SUM(amt)) → columnar")
    c.drawString(72, 384, "skips 90% of the data and compresses 10x better.")
    note(c, 72, 290, 468, "Same data, opposite layouts. This is why one database can't serve both workloads well.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: why separate
    y = section_header(c, 3, 6, "Why You Can't Have One Database",
                       "Running analytics on the transactional DB breaks both.")
    box(c, 72, 480, 200, 70, BOX_BLUE, "Orders DB", "serving checkouts")
    box(c, 340, 480, 200, 70, BOX_RED, "Analyst query", "full table scan!")
    arrow(c, 340, 515, 274, 515, color=RED, width=3, label="locks & load")
    note(c, 72, 380, 468, "The classic outage: a BI query locks the orders table and checkout latency spikes. Separation is an operational requirement, not a preference.")
    bullet_list(c, 72, 340, [
        "Analytical scans evict hot transactional data from memory",
        "Schema optimized for writes fights the schema optimized for reads",
        "Solution: replicate (CDC) into a dedicated analytical store"])
    footer(c, pg); c.showPage(); pg += 1

    # 4: HTAP
    y = section_header(c, 4, 6, "HTAP: Both in One System?",
                       "Hybrid transactional/analytical processing tries to serve both.")
    box(c, 72, 480, 200, 70, BOX_BLUE, "Row engine", "transactions")
    box(c, 340, 480, 200, 70, BOX_GREEN, "Columnar replica", "analytics")
    arrow(c, 272, 515, 338, 515, color=ACCENT, label="async sync")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Systems: SingleStore, TiDB, AlloyDB, Snowflake Unistore.")
    c.drawString(72, 412, "Trick: one logical database, two physical engines with")
    c.drawString(72, 394, "replication between them. Fresh analytics without ETL lag.")
    note(c, 72, 300, 468, "HTAP shines for operational analytics ('live fraud scores on fresh transactions'). For heavy historical analysis, a dedicated warehouse still wins.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: choosing
    y = section_header(c, 5, 6, "Choosing Your Stores",
                       "Match the store to the workload, then connect them.")
    box(c, 72, 500, 140, 60, BOX_BLUE, "OLTP", "Postgres / MySQL")
    box(c, 232, 500, 140, 60, BOX_GREEN, "OLAP", "Warehouse / lakehouse")
    box(c, 392, 500, 148, 60, BOX_TEAL, "HTAP", "SingleStore / TiDB")
    arrow(c, 212, 530, 230, 530, color=ACCENT, label="CDC")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 450, "The standard pipeline: OLTP → CDC → warehouse. Fresh")
    c.drawString(72, 432, "enough for dashboards (minutes), isolated enough to never")
    c.drawString(72, 414, "threaten checkout latency.")
    note(c, 72, 320, 468, "Start boring: Postgres for transactions, a cloud warehouse for analytics, Debezium between them. Add HTAP only when ETL lag is the bottleneck.")
    footer(c, pg); c.showPage(); pg += 1

    # 6: summary matrix
    y = section_header(c, 6, 6, "The Comparison Matrix",
                       "One page to settle every 'which database' debate.")
    rows = [("Query pattern", "Point lookups, small writes", "Full scans, aggregations"),
            ("Storage", "Row-oriented", "Columnar"),
            ("Schema", "Highly normalized (3NF)", "Denormalized (star)"),
            ("Concurrency", "Thousands of users", "Dozens of analysts"),
            ("Example", "Postgres, MySQL", "Snowflake, BigQuery")]
    yy = y
    c.setFillColor(ACCENT2); c.setFont(TITLE_FONT, 10)
    c.drawString(72, yy, "Dimension"); c.drawString(232, yy, "OLTP"); c.drawString(392, yy, "OLAP")
    yy -= 24
    c.setFont(BODY_FONT, 10); c.setFillColor(INK)
    for dim, o1, o2 in rows:
        c.setFont(TITLE_FONT, 10); c.drawString(72, yy, dim)
        c.setFont(BODY_FONT, 10); c.drawString(232, yy, o1); c.drawString(392, yy, o2)
        yy -= 24
    note(c, 72, yy - 30, 468, "HTAP exists for the overlap — but 'one database for everything' is still a trap for most teams. Separate, then integrate.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "OLAP vs OLTP — Remember",
                 ["OLTP: many tiny transactions, row storage, normalized schema — built for checkout-speed writes.",
                  "OLAP: few massive scans, columnar storage, star schemas — built for analytical throughput.",
                  "Never run analytics on the transactional DB: scans lock tables and evict hot data.",
                  "The standard bridge is CDC: OLTP → warehouse, minutes-fresh and fully isolated.",
                  "HTAP (one system, two engines) fits operational analytics; heavy history still belongs in a warehouse."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_timeseries(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Time-Series Databases\nVisual Guide",
               "Metrics, sensors, and ticks.\nBuilt for data that never stops arriving.",
               CATEGORY, None); pg += 1

    # 1: shape of TS data
    y = section_header(c, 1, 6, "The Shape of Time-Series Data",
                       "Timestamp + tags + fields. Append-only, almost never updated.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, y, "cpu,host=web-01,region=us-east usage=42.1 1728400000")
    c.drawString(72, y - 22, "cpu,host=web-02,region=us-east usage=38.7 1728400000")
    c.drawString(72, y - 44, "cpu,host=web-01,region=us-east usage=44.0 1728400060")
    box(c, 72, y - 120, 140, 56, BOX_BLUE, "Timestamp", "the primary key")
    box(c, 232, y - 120, 140, 56, BOX_GREEN, "Tags", "indexed dimensions")
    box(c, 392, y - 120, 148, 56, BOX_ORANGE, "Fields", "measured values")
    note(c, 72, y - 200, 468, "Tags (host, region) are indexed for filtering; fields (usage) are the values you aggregate. Cardinality of tags is the scaling cliff — watch it.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: why special
    y = section_header(c, 2, 6, "Why Not Just Use Postgres?",
                       "Time-series workloads break general-purpose databases at scale.")
    bullet_list(c, 72, y, [
        "Write rate: millions of points/sec — B-tree indexes can't keep up",
        "Queries: time-range scans + downsampling, not point lookups",
        "Data value decays: last week's per-second data is worth less than last year's per-hour",
        "Compression: sorted-by-time numeric series compress 10-20x with delta encoding"], font_size=11, gap=28)
    note(c, 72, 300, 468, "TSDBs trade general query power for insane ingest and time-range performance: LSM trees, columnar chunks, time-partitioned storage.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: InfluxDB vs Timescale
    y = section_header(c, 3, 6, "InfluxDB vs TimescaleDB",
                       "Purpose-built engine vs Postgres superpowers.")
    box(c, 72, y - 130, 225, 130, BOX_TEAL, "InfluxDB", "purpose-built TSDB", font_size=13)
    box(c, 315, y - 130, 225, 130, BOX_BLUE, "TimescaleDB", "Postgres extension", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    inf = ["Flux/SQL query language", "Built-in retention + downsampling", "Best for: metrics, IoT at scale"]
    ts = ["Full SQL + joins to relational data", "Hypertables auto-partition by time", "Best for: teams that live in Postgres"]
    yy = y - 30
    for t in inf:
        c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 30
    for t in ts:
        c.drawString(331, yy, "• " + t); yy -= 18
    note(c, 72, y - 190, 468, "Choose InfluxDB for pure time-series scale; TimescaleDB when time-series is one workload among many and you want real SQL joins.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: downsampling
    y = section_header(c, 4, 6, "Downsampling: Rollups Over Time",
                       "Keep full resolution briefly, aggregates forever.")
    box(c, 72, 480, 140, 70, BOX_BLUE, "Raw: 1s", "7 days")
    box(c, 252, 480, 140, 70, BOX_GREEN, "1-min avg", "90 days")
    box(c, 432, 480, 108, 70, BOX_TEAL, "1-hour avg", "2 years")
    arrow(c, 212, 515, 250, 515, color=ACCENT, label="rollup")
    arrow(c, 392, 515, 430, 515, color=ACCENT, label="rollup")
    note(c, 72, 380, 468, "Continuous aggregates (Timescale) or tasks (InfluxDB) compute rollups on ingest. Dashboards query the rollup — raw data is for forensics.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: retention
    y = section_header(c, 5, 6, "Retention Policies",
                       "Data expires by policy, not by accident.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, y, "CREATE RETENTION POLICY '30d' ON metrics")
    c.drawString(72, y - 22, "  DURATION 30d REPLICATION 1;")
    bullet_list(c, 72, y - 60, [
        "Tier by age: hot (SSD, full resolution) → warm → cold (object storage)",
        "Retention runs per measurement — different series, different lifespans",
        "Legal hold overrides: compliance data ignores default expiry",
        "Dropping whole time-partitions is O(1) — never DELETE old rows one by one"], font_size=11, gap=26)
    note(c, 72, 280, 468, "Retention is a cost control: per-second data for 30 days, then rollups. Without policies, cardinality and storage grow until the bill does.")
    footer(c, pg); c.showPage(); pg += 1

    # 6: compression
    y = section_header(c, 6, 6, "Compression: Why TSDBs Are Tiny",
                       "Time-ordered numerics compress absurdly well.")
    box(c, 72, 480, 225, 70, BOX_BLUE, "Delta-of-delta", "timestamps: store diffs of diffs")
    box(c, 315, 480, 225, 70, BOX_GREEN, "Gorilla / XOR", "floats: store changed bits only")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Regular 60s timestamps: deltas are constant → near-zero bits.")
    c.drawString(72, 412, "Slowly-changing floats: XOR with previous value leaves")
    c.drawString(72, 394, "mostly zeros. Result: 10-20x smaller than raw.")
    note(c, 72, 300, 468, "Compression is why TSDBs can hold years of metrics cheaply — but it depends on time-ordered writes. Out-of-order ingestion costs you.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Time-Series Databases — Remember",
                 ["Time-series data = timestamp + tags (indexed) + fields (measured); append-only and high-volume.",
                  "TSDBs beat general databases on ingest rate, time-range scans, and automatic lifecycle management.",
                  "InfluxDB for pure TS scale; TimescaleDB when you need real SQL and joins to relational data.",
                  "Downsample aggressively: raw for days, minute-aggregates for months, hourly for years.",
                  "Retention policies + time-ordered compression (delta, Gorilla) keep years of data affordable."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_graph_db(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Graph Databases\nVisual Guide",
               "When relationships ARE the data.\nNeo4j, traversals, and Cypher.",
               CATEGORY, None); pg += 1

    # 1: property graph
    y = section_header(c, 1, 6, "The Property Graph Model",
                       "Nodes, relationships, and properties on both.")
    box(c, 226, 480, 160, 70, BOX_BLUE, "(:Person)", "name: 'Ana'")
    box(c, 72, 340, 140, 60, BOX_GREEN, "(:Person)", "name: 'Ben'")
    box(c, 400, 340, 140, 60, BOX_GREEN, "(:Company)", "name: 'Acme'")
    arrow(c, 210, 400, 250, 480, color=ACCENT, label="KNOWS")
    arrow(c, 386, 515, 402, 402, color=ACCENT, label="WORKS_AT")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(300, 430, "since: 2020")
    note(c, 72, 240, 468, "Relationships are first-class: typed, directed, and carrying their own properties. No join tables — the connection is stored, not computed.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: vs relational joins
    y = section_header(c, 2, 6, "Why Graphs Beat Joins Here",
                       "Multi-hop queries explode in SQL, stay constant in a graph.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y, "SQL: friends-of-friends-of-friends = 3 self-joins over a")
    c.drawString(72, y - 20, "100M-row edge table. Each join multiplies the working set.")
    c.drawString(72, y - 50, "Graph: follow pointers from the start node. Cost depends on")
    c.drawString(72, y - 70, "the neighborhood size, not the total graph size.")
    box(c, 72, y - 150, 225, 60, BOX_RED, "SQL multi-hop", "O(joins × table size)")
    box(c, 315, y - 150, 225, 60, BOX_GREEN, "Graph traversal", "O(visited nodes)")
    note(c, 72, y - 230, 468, "Index-free adjacency: each node physically points to its neighbors. Traversal is pointer-chasing, not index lookups.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: Cypher basics
    y = section_header(c, 3, 6, "Cypher Basics",
                       "ASCII-art query language: draw the pattern you want.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, y, "MATCH (a:Person {name:'Ana'})-[:KNOWS]->(friend)")
    c.drawString(72, y - 22, "RETURN friend.name;")
    c.drawString(72, y - 54, "MATCH (a:Person)-[:KNOWS*2..3]->(fof)")
    c.drawString(72, y - 76, "WHERE a.name = 'Ana'")
    c.drawString(72, y - 98, "RETURN DISTINCT fof.name;")
    note(c, 72, y - 170, 468, "(a)-[:KNOWS]->(b) literally draws the relationship. *2..3 means '2 to 3 hops'. Variable-length paths are one line in Cypher, pages of SQL.")
    bullet_list(c, 72, y - 210, [
        "CREATE builds nodes and relationships in one statement",
        "MERGE = get-or-create (idempotent writes)",
        "PROFILE shows the traversal plan — watch for cartesian products"])
    footer(c, pg); c.showPage(); pg += 1

    # 4: traversals
    y = section_header(c, 4, 6, "Traversal Patterns",
                       "The queries graphs were born for.")
    pats = [("Path finding", "Shortest path between two nodes — fraud rings, routing", BOX_BLUE),
            ("Neighborhood", "Everything within N hops — recommendations, blast radius", BOX_GREEN),
            ("Pattern matching", "Find subgraphs shaped like X — money-laundering motifs", BOX_ORANGE),
            ("Centrality", "PageRank, betweenness — who matters in the network", BOX_PURP)]
    yy = y
    for name, desc, fill in pats:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=12)
        yy -= 76
    note(c, 72, yy - 20, 468, "Graph Data Science library adds 65+ algorithms (community detection, embeddings) runnable directly on the stored graph.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: when graphs win
    y = section_header(c, 5, 6, "When Graphs Win (and Don't)",
                       "Reach for a graph when the question is about connections.")
    box(c, 72, y - 130, 225, 130, BOX_GREEN, "GRAPHS WIN", "", font_size=13)
    box(c, 315, y - 130, 225, 130, BOX_RED, "SKIP GRAPHS", "", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    win = ["Fraud / AML networks", "Recommendations", "Knowledge graphs, IAM"]
    skip = ["Simple CRUD with few joins", "Heavy aggregations over facts", "Tabular reporting"]
    yy = y - 30
    for t in win:
        c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 30
    for t in skip:
        c.drawString(331, yy, "• " + t); yy -= 18
    note(c, 72, y - 190, 468, "Graphs are bad at what warehouses are good at: scanning millions of rows and summing them. Use both — graph for connections, warehouse for aggregates.")
    footer(c, pg); c.showPage(); pg += 1

    # 6: modeling tips
    y = section_header(c, 6, 6, "Graph Modeling Tips",
                       "Model for the questions you'll ask.")
    items = ["Relationships over properties: 'WORKS_AT' beats employer_name string",
             "Keep graphs shallow: 2-4 hop queries are fast; 10-hop scans everything",
             "Index the starting points — traversals begin with a lookup",
             "Time-version relationships (since/until) instead of deleting history",
             "Supernodes (a node with millions of edges) kill traversals — split them"]
    y = bullet_list(c, 72, y, items, font_size=11.5, gap=30)
    note(c, 72, 300, 468, "The #1 graph performance bug: starting a traversal without an indexed anchor node. Always MATCH the start node by indexed property first.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Graph Databases — Remember",
                 ["Property graphs store nodes, typed relationships, and properties — connections are stored, not joined.",
                  "Index-free adjacency makes multi-hop traversals constant in neighborhood size, not table size.",
                  "Cypher draws patterns as ASCII art; variable-length paths are one line.",
                  "Reach for graphs for fraud, recommendations, and knowledge — not for aggregations or CRUD.",
                  "Model relationships explicitly, keep traversals shallow, and always start from an indexed node."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_elasticsearch(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Elasticsearch\nVisual Guide",
               "Search at scale.\nInverted indexes, shards, and relevance.",
               CATEGORY, None); pg += 1

    # 1: inverted index
    y = section_header(c, 1, 6, "The Inverted Index",
                       "Like a book index: term → list of documents containing it.")
    box(c, 72, 500, 200, 60, BOX_BLUE, "Doc 1", "'fast electric car'")
    box(c, 292, 500, 200, 60, BOX_BLUE, "Doc 2", "'fast red car'")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, 450, "fast     → [doc1, doc2]")
    c.drawString(72, 432, "electric → [doc1]")
    c.drawString(72, 414, "car      → [doc1, doc2]")
    c.drawString(72, 396, "red      → [doc2]")
    note(c, 72, 300, 468, "Search = look up each query term's posting list, intersect, rank. No table scans — that's why full-text search is instant at billions of docs.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: analysis
    y = section_header(c, 2, 6, "Analysis: Text In, Terms Out",
                       "The analyzer pipeline decides what gets indexed.")
    box(c, 72, 480, 120, 60, BOX_BLUE, "Character", "strip HTML")
    box(c, 212, 480, 120, 60, BOX_TEAL, "Tokenizer", "split words")
    box(c, 352, 480, 120, 60, BOX_GREEN, "Filters", "lowercase, stem")
    arrow(c, 192, 510, 210, 510, color=ACCENT)
    arrow(c, 332, 510, 350, 510, color=ACCENT)
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, 430, '"Running Shoes!" → running | shoes')
    c.drawString(72, 414, '              → run | shoe   (stemmed, lowercased)')
    note(c, 72, 320, 468, "Query and index MUST use the same analyzer or terms won't match. Custom analyzers per language/field are the norm in production.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: shards & replicas
    y = section_header(c, 3, 6, "Shards & Replicas",
                       "An index is split into shards; each shard has replicas.")
    for i, sx in enumerate([72, 212, 352]):
        box(c, sx, 480, 120, 70, BOX_BLUE, f"Shard {i}", "primary")
        box(c, sx, 390, 120, 70, BOX_GREEN, f"Replica {i}", "copy")
    note(c, 72, 290, 468, "Shards = horizontal scale (more shards, more parallel search). Replicas = availability + read throughput. Rule: shards sized 10-50GB each.")
    bullet_list(c, 72, 250, [
        "Too many shards: overhead per shard kills the cluster (shard sprawl)",
        "Replicas never sit on the same node as their primary",
        "Rollover: time-based indices (logs-2026.10.09) keep shards right-sized"])
    footer(c, pg); c.showPage(); pg += 1

    # 4: relevance
    y = section_header(c, 4, 6, "Relevance Scoring (BM25)",
                       "Not just matching — ranking by what matters most.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y, "BM25 scores each doc on three signals:")
    y = bullet_list(c, 72, y - 30, [
        "Term frequency: more mentions = more relevant (with diminishing returns)",
        "Inverse document frequency: rare terms ('elasticsearch') weigh more than common ones ('the')",
        "Field length: a match in a short title beats a match in a long body"], font_size=11, gap=28)
    note(c, 72, y - 30, 468, "Tune with field boosts (title^3) and function scores (recency, popularity). Relevance is a product decision — A/B test it like one.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: mappings
    y = section_header(c, 5, 6, "Mappings: Schema for Search",
                       "Define field types deliberately — dynamic mapping guesses wrong.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9)
    c.drawString(72, y, '{"mappings": {"properties": {')
    c.drawString(72, y - 20, '  "title":   {"type": "text"},')
    c.drawString(72, y - 40, '  "status":   {"type": "keyword"},')
    c.drawString(72, y - 60, '  "price":    {"type": "scaled_float"},')
    c.drawString(72, y - 80, '  "location": {"type": "geo_point"}')
    c.drawString(72, y - 100, '}}}')
    note(c, 72, y - 170, 468, "text = analyzed, full-text search. keyword = exact match, aggregations, sorting. Pick wrong and your filters silently return nothing.")
    bullet_list(c, 72, y - 210, [
        "Multi-fields: index a name as both text and keyword",
        "Changing a mapping usually means reindexing — plan for it",
        "Index templates auto-apply mappings to new time-based indices"])
    footer(c, pg); c.showPage(); pg += 1

    # 6: aggregations
    y = section_header(c, 6, 6, "Aggregations: Analytics on Search",
                       "Facets, histograms, and metrics — computed across shards.")
    box(c, 72, 480, 225, 70, BOX_ORANGE, "Bucket aggs", "terms, date_histogram, ranges")
    box(c, 315, 480, 225, 70, BOX_BLUE, "Metric aggs", "avg, sum, percentiles")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "One request returns search hits AND 'avg price by brand' AND")
    c.drawString(72, 412, "'histogram over time'. This is how faceted navigation")
    c.drawString(72, 394, "(Amazon's sidebar filters) works at scale.")
    note(c, 72, 300, 468, "Aggregations run distributed: each shard computes partials, the coordinator merges. Deep pagination + huge cardinality = memory pressure — use composite aggs.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Elasticsearch — Remember",
                 ["The inverted index maps terms to documents — search is posting-list intersection, not table scans.",
                  "Analyzers (character → tokenizer → filters) must match between index and query time.",
                  "Shards scale search horizontally (10-50GB each); replicas add availability and read throughput.",
                  "BM25 ranks by term frequency, rarity (IDF), and field length — boost fields deliberately.",
                  "Map text vs keyword correctly; aggregations turn search into real-time analytics."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_partitioning(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Data Partitioning\nVisual Guide",
               "Divide data to conquer scale.\nStrategies, pruning, and skew.",
               CATEGORY, None); pg += 1

    # 1: why partition
    y = section_header(c, 1, 6, "Why Partition?",
                       "One giant table is one giant problem. Partitioning divides it into manageable pieces.")
    box(c, 72, 480, 468, 70, BOX_BLUE, "orders (10B rows)", "one table")
    box(c, 72, 360, 140, 70, BOX_GREEN, "2026-09", "partition")
    box(c, 236, 360, 140, 70, BOX_GREEN, "2026-10", "partition")
    box(c, 400, 360, 140, 70, BOX_GREEN, "2026-11", "partition")
    arrow(c, 200, 478, 142, 432, color=ACCENT)
    arrow(c, 306, 478, 306, 432, color=ACCENT)
    arrow(c, 412, 478, 470, 432, color=ACCENT)
    note(c, 72, 260, 468, "Partitions are independent units: query one, drop one, compact one — without touching the rest. Operations scale with the partition, not the table.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: strategies
    y = section_header(c, 2, 6, "Partitioning Strategies",
                       "Range, hash, and list — pick by query pattern.")
    strat = [("Range", "By value intervals: date, id ranges. Great for time queries.", BOX_BLUE),
             ("Hash", "hash(key) mod N: even spread, no ordering. Great for point lookups.", BOX_GREEN),
             ("List", "Explicit value sets: region = 'EU'. Great for known categories.", BOX_ORANGE)]
    yy = y
    for name, desc, fill in strat:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=12)
        yy -= 76
    note(c, 72, yy - 20, 468, "Composite: range by date, then hash by id within each — time pruning plus even distribution. Most large tables end up composite.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: pruning
    y = section_header(c, 3, 6, "Partition Pruning",
                       "The optimizer skips partitions that can't match — the whole point.")
    box(c, 72, 480, 105, 60, BOX_TEAL, "Sep", "scanned?")
    box(c, 197, 480, 105, 60, BOX_TEAL, "Oct", "SCANNED ✓")
    box(c, 322, 480, 105, 60, BOX_TEAL, "Nov", "scanned?")
    c.setStrokeColor(RED); c.setLineWidth(2)
    c.line(72, 478, 177, 542); c.line(72, 542, 177, 478)
    c.line(322, 478, 427, 542); c.line(322, 542, 427, 478)
    c.setFillColor(INK); c.setFont(MONO_FONT, 10)
    c.drawString(72, 430, "WHERE order_date BETWEEN '2026-10-01' AND '2026-10-31'")
    note(c, 72, 330, 468, "Pruning only works when the filter is on the partition key with a sargable predicate. Filter on a non-partition column and every partition gets scanned.")
    bullet_list(c, 72, 290, [
        "Partition key should be your most common filter",
        "Avoid functions on the partition column: WHERE year(d) = 2026 kills pruning",
        "Check EXPLAIN: partitions scanned should be << total partitions"])
    footer(c, pg); c.showPage(); pg += 1

    # 4: skew
    y = section_header(c, 4, 6, "Skew: The Partition Killer",
                       "One giant partition ruins parallelism — every worker waits for the slowest.")
    box(c, 72, 480, 140, 70, BOX_GREEN, "P: US-East", "small ✓")
    box(c, 236, 480, 140, 70, BOX_RED, "P: US-West", "HUGE ✗")
    box(c, 400, 480, 140, 70, BOX_GREEN, "P: EU", "small ✓")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Hash partitioning on a low-cardinality or Zipf-distributed key")
    c.drawString(72, 412, "creates hot partitions. Fixes:")
    y = bullet_list(c, 72, 380, [
        "Salting: append random suffix to hot keys, split across sub-partitions",
        "Composite keys: (region, user_id) instead of region alone",
        "Isolate the hot key: its own partition + special handling"], font_size=11, gap=26)
    note(c, 72, y - 30, 468, "Measure skew first: rows per partition. If the max is 10x the median, you have a skew problem regardless of strategy.")
    footer(c, pg); c.showPage(); pg += 1

    # 5: file sizing
    y = section_header(c, 5, 6, "Partition & File Sizing",
                       "Right-sized partitions keep the engine happy.")
    box(c, 72, 470, 140, 70, BOX_RED, "Too small", "10k tiny files — metadata meltdown")
    box(c, 236, 470, 140, 70, BOX_GREEN, "Right", "128MB–1GB files")
    box(c, 400, 470, 140, 70, BOX_RED, "Too big", "GBs — no parallelism")
    note(c, 72, 370, 468, "Too many partitions: the Hive metastore / file listing becomes the bottleneck. Too few: no pruning benefit. Aim for partitions ≥ 1GB with a few files each.")
    bullet_list(c, 72, 330, [
        "Don't partition by high-cardinality columns (user_id with 100M values)",
        "Date + one low-cardinality key is the sweet spot for most tables",
        "Compaction (OPTIMIZE) merges small files within partitions"])
    footer(c, pg); c.showPage(); pg += 1

    # 6: hidden partitioning
    y = section_header(c, 6, 6, "Hidden Partitioning (Iceberg-style)",
                       "Partition by transform, query by column — no more partition-column gymnastics.")
    c.setFillColor(INK); c.setFont(MONO_FONT, 9.5)
    c.drawString(72, y, "PARTITIONED BY (days(order_ts))   -- you write:")
    c.drawString(72, y - 24, "WHERE order_ts >= '2026-10-01'     -- no partition column!")
    note(c, 72, y - 90, 468, "Iceberg/Delta map your filter to partitions automatically. Evolve partitioning later (days → hours) without rewriting data or queries.")
    bullet_list(c, 72, y - 130, [
        "No more year=/month=/day= path rituals in queries",
        "Partition evolution: change layout without breaking readers",
        "The table format handles the mapping — you think in columns"])
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Data Partitioning — Remember",
                 ["Partitioning splits tables into independent units — operations scale with the partition, not the table.",
                  "Range for time/ordered queries, hash for even spread, list for known categories; composite for both.",
                  "Partition pruning is the payoff: filter on the partition key or every partition gets scanned.",
                  "Skew kills parallelism — salt hot keys, use composite keys, measure rows per partition.",
                  "Size partitions ≥ 1GB with few files each; hidden partitioning (Iceberg) removes the path rituals."],
                 pg)
    c.save()
    print("wrote", path)


def pdf_data_lineage(path):
    c = new_canvas(path)
    pg = 1
    title_page(c, "Data Lineage\nVisual Guide",
               "Where did this number come from?\nColumn-level tracking and impact analysis.",
               CATEGORY, None); pg += 1

    # 1: the question
    y = section_header(c, 1, 6, "The Question Lineage Answers",
                       "Every data incident starts with 'where did this come from?'")
    box(c, 196, 480, 220, 70, BOX_RED, "Dashboard: revenue = $0?!", "the 9 AM panic")
    box(c, 72, 340, 180, 70, BOX_BLUE, "Upstream?", "which table broke")
    box(c, 360, 340, 180, 70, BOX_BLUE, "Downstream?", "who else is wrong")
    arrow(c, 306, 478, 180, 412, color=ACCENT, label="trace back")
    arrow(c, 306, 478, 430, 412, color=ACCENT, label="blast radius")
    note(c, 72, 240, 468, "Without lineage: hours of Slack archaeology. With lineage: click the metric, see the full upstream chain and every downstream consumer.")
    footer(c, pg); c.showPage(); pg += 1

    # 2: levels
    y = section_header(c, 2, 6, "Lineage Granularity Levels",
                       "Table-level tells you what; column-level tells you why.")
    box(c, 72, 500, 468, 60, BOX_BLUE, "Table-level", "orders → revenue_mart (coarse, easy)")
    box(c, 72, 410, 468, 60, BOX_GREEN, "Column-level", "orders.total → revenue_mart.gross_revenue (precise, hard)")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 360, "Column-level lineage parses SQL to map each output column to its")
    c.drawString(72, 342, "source columns through every transform — including through")
    c.drawString(72, 324, "CASE statements, joins, and aggregations.")
    note(c, 72, 230, 468, "Column-level is what makes impact analysis trustworthy: 'we're renaming total' → exactly which dashboards break, not 'everything downstream of orders'.")
    footer(c, pg); c.showPage(); pg += 1

    # 3: capture methods
    y = section_header(c, 3, 6, "How Lineage Is Captured",
                       "Parse it, instrument it, or declare it.")
    meth = [("SQL parsing", "Parse query text into column mappings. Works on any SQL, struggles with dynamic SQL.", BOX_BLUE),
            ("Framework instrumentation", "Spark/dbt emit lineage events (OpenLineage). Precise, needs integration.", BOX_GREEN),
            ("Manual declaration", "Humans document flows. Accurate once, rots immediately.", BOX_ORANGE)]
    yy = y
    for name, desc, fill in meth:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=12)
        yy -= 76
    note(c, 72, yy - 20, 468, "Best practice: OpenLineage events from orchestrators (Airflow, Spark, dbt) into a central catalog — automatic, versioned, and queryable.")
    footer(c, pg); c.showPage(); pg += 1

    # 4: impact analysis
    y = section_header(c, 4, 6, "Impact Analysis: Before You Change Anything",
                       "Lineage turns 'can I drop this column?' into a 10-second query.")
    box(c, 72, 480, 180, 70, BOX_ORANGE, "Drop column total?", "proposed change")
    box(c, 340, 480, 200, 70, BOX_RED, "3 dashboards + 2 models break", "lineage says no")
    arrow(c, 252, 515, 338, 515, color=RED, width=3, label="impact query")
    note(c, 72, 380, 468, "Forward lineage (downstream) for impact analysis; backward lineage (upstream) for root-cause. CI can block breaking changes automatically.")
    bullet_list(c, 72, 340, [
        "Deprecation workflow: announce → migrate → verify zero consumers → drop",
        "Schema-change CI: fail the PR if a dropped column has downstream readers",
        "Blast-radius estimates for incident severity"])
    footer(c, pg); c.showPage(); pg += 1

    # 5: incident debugging
    y = section_header(c, 5, 6, "Incident Debugging with Lineage",
                       "Walk the graph from symptom to cause.")
    box(c, 72, 500, 110, 55, BOX_RED, "Metric wrong", "symptom")
    box(c, 222, 500, 110, 55, BOX_ORANGE, "mart table", "stale?")
    box(c, 372, 500, 110, 55, BOX_ORANGE, "staging", "schema drift?")
    box(c, 222, 390, 110, 55, BOX_BLUE, "source API", "ROOT CAUSE")
    arrow(c, 182, 527, 220, 527, color=ACCENT)
    arrow(c, 332, 527, 370, 527, color=ACCENT)
    arrow(c, 277, 498, 277, 447, color=RED, width=3)
    note(c, 72, 290, 468, "The debugging walk: check freshness at each hop, find the first broken node. Lineage plus data-quality signals usually point at the culprit in minutes.")
    bullet_list(c, 72, 250, [
        "Annotate nodes with freshness + test status — the graph becomes a health map",
        "Common culprits: missed SLA upstream, schema drift, silent filter change",
        "Post-incident: the fix should add a check at the hop that failed"])
    footer(c, pg); c.showPage(); pg += 1

    # 6: governance link
    y = section_header(c, 6, 6, "Lineage × Governance",
                       "Lineage is how PII policies and audits actually work.")
    box(c, 72, 480, 225, 70, BOX_PURP, "PII propagation", "ssn flows into 14 tables")
    box(c, 315, 480, 225, 70, BOX_PURP, "Compliance proof", "GDPR deletion = all copies")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 430, "Tag a source column as PII → lineage propagates the tag")
    c.drawString(72, 412, "downstream automatically. Masking policies follow the tag,")
    c.drawString(72, 394, "not the table name.")
    note(c, 72, 300, 468, "Right-to-erasure without lineage is a guess. With column-level lineage, 'delete this user's data everywhere' is a precise, auditable operation.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Data Lineage — Remember",
                 ["Lineage answers 'where did this come from' and 'who breaks if I change this' — the two incident questions.",
                  "Column-level lineage maps each output column through every transform; table-level is a coarse start.",
                  "Capture automatically: OpenLineage events from Spark/dbt/Airflow beat manual documentation.",
                  "Forward lineage drives impact analysis and safe deprecation; backward lineage drives root-cause debugging.",
                  "Lineage powers governance: PII tags propagate downstream, and erasure becomes auditable."],
                 pg)
    c.save()
    print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    pdf_elt(os.path.join(out, "bbg-elt.pdf"))
    pdf_kafka_deep(os.path.join(out, "bbg-kafka-deep.pdf"))
    pdf_spark(os.path.join(out, "bbg-spark.pdf"))
    pdf_snowflake(os.path.join(out, "bbg-snowflake.pdf"))
    pdf_delta_lake(os.path.join(out, "bbg-delta-lake.pdf"))
    pdf_dbt(os.path.join(out, "bbg-dbt.pdf"))
    pdf_airflow(os.path.join(out, "bbg-airflow.pdf"))
    pdf_data_quality(os.path.join(out, "bbg-data-quality.pdf"))
    pdf_schema_evolution(os.path.join(out, "bbg-schema-evolution.pdf"))
    pdf_cdc(os.path.join(out, "bbg-cdc.pdf"))
    pdf_data_governance(os.path.join(out, "bbg-data-governance.pdf"))
    pdf_data_catalogs(os.path.join(out, "bbg-data-catalogs.pdf"))
    pdf_dimensional_modeling(os.path.join(out, "bbg-dimensional-modeling.pdf"))
    pdf_star_schema(os.path.join(out, "bbg-star-schema.pdf"))
    pdf_olap_oltp(os.path.join(out, "bbg-olap-oltp.pdf"))
    pdf_timeseries(os.path.join(out, "bbg-timeseries.pdf"))
    pdf_graph_db(os.path.join(out, "bbg-graph-db.pdf"))
    pdf_elasticsearch(os.path.join(out, "bbg-elasticsearch.pdf"))
    pdf_partitioning(os.path.join(out, "bbg-partitioning.pdf"))
    pdf_data_lineage(os.path.join(out, "bbg-data-lineage.pdf"))
    print("batch 12 complete: 20 PDFs")
