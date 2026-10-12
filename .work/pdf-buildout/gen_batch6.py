"""Batch 6: Data Engineering PDFs — ETL Pipelines, Stream Processing, Warehouses."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


def pdf_etl(path):
    c = new_canvas(path); pg = 1
    title_page(c, "ETL Data Pipelines\nVisual Guide",
               "Extract, Transform, Load —\nhow raw data becomes trusted analytics.",
               "Data Engineering", None); pg += 1

    y = section_header(c, 1, 6, "The Pipeline: E → T → L",
                       "Three stages, one direction: raw → clean → queryable.")
    box(c, 72, 420, 140, 80, BOX_BLUE, "Extract", "APIs, DBs, files,\nevents")
    box(c, 246, 420, 140, 80, BOX_ORANGE, "Transform", "clean, join,\naggregate")
    box(c, 420, 420, 120, 80, BOX_GREEN, "Load", "warehouse\ntables")
    arrow(c, 212, 460, 244, 460, color=ACCENT, width=2.5)
    arrow(c, 386, 460, 418, 460, color=ACCENT, width=2.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 370, "Raw: messy, nested, duplicated.  →  Clean: typed, deduped, conformed.  →  Modeled: star schema, ready for BI.")
    note(c, 72, 270, 468, "ELT variant: Load raw first, Transform inside the warehouse (dbt). Better for huge data + cheap compute.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Extract: Getting Data Out",
                       "Every source has a personality.")
    srcs = [("Databases (CDC)", "Change-data-capture streams row changes (Debezium) — no polling.", BOX_BLUE),
            ("APIs", "REST/GraphQL pulls; respect rate limits, paginate, backfill.", BOX_GREEN),
            ("Files", "CSV/Parquet drops in S3; watch for schema drift.", BOX_ORANGE),
            ("Events", "Clickstreams, IoT — high volume, append-only.", BOX_TEAL)]
    yy = y
    for name, desc, fill in srcs:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11.5)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Transform: The Real Work",
                       "Where data quality is made or broken.")
    tx = [("Clean", "nulls, dupes, bad types", BOX_GREEN),
          ("Join", "customers ⨝ orders", BOX_BLUE),
          ("Aggregate", "daily revenue by region", BOX_ORANGE),
          ("Validate", "tests on every run", BOX_RED)]
    bx = 72
    for name, desc, fill in tx:
        box(c, bx, 440, 108, 70, fill, name, desc, font_size=10)
        if bx > 72:
            arrow(c, bx - 12, 475, bx, 475, color=ACCENT, width=1.5)
        bx += 120
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, 380,
        ["Idempotent transforms: re-running produces the same result (no double-counting).",
         "dbt: SQL models with tests, docs, and lineage — versioned in git.",
         "Slowly-changing dimensions: track history (Type 2) vs overwrite (Type 1)."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Orchestration: DAGs Run the Show",
                       "Dependencies as a directed acyclic graph.")
    box(c, 72, 460, 120, 56, BOX_BLUE, "extract_users", "")
    box(c, 246, 460, 120, 56, BOX_BLUE, "extract_orders", "")
    box(c, 156, 360, 140, 56, BOX_ORANGE, "dbt_transform", "")
    box(c, 350, 360, 140, 56, BOX_GREEN, "data_quality", "")
    box(c, 216, 260, 180, 56, BOX_PURP, "publish_marts", "")
    arrow(c, 132, 458, 200, 418, color=ACCENT, width=1.5)
    arrow(c, 306, 458, 240, 418, color=ACCENT, width=1.5)
    arrow(c, 226, 358, 300, 358, color=ACCENT, width=1.5)
    arrow(c, 420, 358, 330, 318, color=ACCENT, width=1.5)
    arrow(c, 296, 358, 280, 318, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 210, "Airflow / Dagster / Prefect: schedule, retry, alert, backfill. A failed task retries; downstream waits.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Data Quality Tests",
                       "Trust is earned per run.")
    tests = [("Freshness", "Did today's data arrive? (SLA breach → alert)", BOX_GREEN),
             ("Volume", "Row counts within expected bands (no silent drops)", BOX_BLUE),
             ("Schema", "Columns and types match the contract", BOX_ORANGE),
             ("Uniqueness", "Keys are actually unique; no fan-out joins", BOX_RED)]
    yy = y
    for name, desc, fill in tests:
        c.setFillColor(GREEN); c.circle(96, yy - 26, 9, fill=1, stroke=0)
        c.setFillColor(white); c.setFont(TITLE_FONT, 10); c.drawCentredString(96, yy - 22, "✓")
        box(c, 116, yy - 52, 424, 56, fill, name, desc, font_size=11)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Medallion Architecture",
                       "Bronze → Silver → Gold: progressive refinement.")
    box(c, 72, 420, 140, 80, HexColor("#CD7F32"), "Bronze", "raw\nimmutable")
    box(c, 246, 420, 140, 80, HexColor("#C0C0C0"), "Silver", "cleaned\nconformed")
    box(c, 420, 420, 120, 80, HexColor("#FFD700"), "Gold", "business\nmarts")
    arrow(c, 212, 460, 244, 460, color=ACCENT, width=2.5, label="clean")
    arrow(c, 386, 460, 418, 460, color=ACCENT, width=2.5, label="model")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 370, "Bronze: keep everything raw — you can always re-derive. Never delete source truth.")
    c.drawString(72, 352, "Gold: curated, documented, SLAd — the only layer analysts touch.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "ETL Pipelines — Remember",
                 ["Extract from DBs (CDC), APIs, files, events — each with its own quirks.",
                  "Transform idempotently; dbt brings software practices to SQL.",
                  "Orchestrate with DAGs: dependencies, retries, backfills, alerts.",
                  "Test every run: freshness, volume, schema, uniqueness.",
                  "Medallion: bronze (raw) → silver (clean) → gold (business-ready)."],
                 pg)
    c.save(); print("wrote", path)


def pdf_streaming(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Stream Processing\nVisual Guide",
               "Data in motion —\nfrom batch thinking to real-time thinking.",
               "Data Engineering", None); pg += 1

    y = section_header(c, 1, 6, "Batch vs Stream",
                       "Same questions, different freshness.")
    box(c, 72, y - 70, 225, 120, BOX_BLUE, "Batch", "hourly / daily jobs", font_size=13)
    box(c, 315, y - 70, 225, 120, BOX_GREEN, "Stream", "milliseconds", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    ba = ["'What happened yesterday?'", "Complete data, simple logic", "High latency by design"]
    st = ["'What's happening NOW?'", "Infinite data, windowed logic", "Low latency, harder ops"]
    yy = y - 100
    for t in ba: c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 100
    for t in st: c.drawString(331, yy, "• " + t); yy -= 18
    note(c, 72, 200, 468, "Lambda: batch + stream paths (complex). Kappa: stream-only, reprocess from the log (simpler).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "The Log: Foundation of Streaming",
                       "An append-only, replayable sequence — Kafka's big idea.")
    # log segments
    for i in range(8):
        col = BOX_GREEN if i < 6 else BOX_ORANGE
        box(c, 72 + i * 60, 420, 54, 60, col, f"{i+1}", "", font_size=10)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 380, "Immutable, ordered, partitioned. Consumers track their own offset — replay anytime.")
    c.drawString(72, 362, "Retention (days–forever) decouples producers from consumers in TIME as well as space.")
    box(c, 72, 280, 220, 56, BOX_BLUE, "Producer", "appends events")
    box(c, 320, 280, 220, 56, BOX_TEAL, "Consumers", "each keeps its own offset")
    arrow(c, 292, 308, 318, 308, color=ACCENT, width=2)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Windows: Taming Infinity",
                       "You can't aggregate 'all data ever' — slice time into windows.")
    wins = [("Tumbling", "Fixed, non-overlapping: every 5 min. Simple counts.", BOX_BLUE),
            ("Sliding", "Overlapping: every 1 min over last 5. Smoother.", BOX_GREEN),
            ("Session", "Gaps define boundaries: user activity bursts.", BOX_ORANGE)]
    yy = y
    for name, desc, fill in wins:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11.5)
        yy -= 70
    # mini timeline
    c.setStrokeColor(MUTED); c.line(72, 180, 540, 180)
    c.setFillColor(ACCENT)
    for i, xx in enumerate([100, 160, 200, 280, 340, 420, 480]):
        c.circle(xx, 180, 5, fill=1, stroke=0)
    c.setStrokeColor(GREEN); c.setLineWidth(2)
    c.rect(90, 160, 120, 40, fill=0, stroke=1)
    c.rect(270, 160, 120, 40, fill=0, stroke=1)
    c.setFillColor(GREEN); c.setFont(BODY_FONT, 9)
    c.drawString(95, 148, "tumbling windows")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Event Time vs Processing Time",
                       "When it happened vs when you saw it — they differ.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(72, y, "Event time: the timestamp IN the event (phone's clock).")
    c.drawString(72, y - 26, "Processing time: when your system received it (server's clock).")
    note(c, 72, y - 90, 468, "Late data: events arriving after their window closed. Watermarks declare 'we've seen everything up to T' — then fire the window, with allowed lateness for stragglers.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 170,
        ["Use event time for correctness (billing, analytics).",
         "Use processing time only when approximate is fine (dashboards).",
         "Exactly-once: idempotent sinks + transactional writes (Kafka transactions, Flink checkpoints)."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Exactly-Once Semantics",
                       "The holy grail: no duplicates, no loss.")
    levels = [("At-most-once", "May lose. Fire and forget.", BOX_RED),
              ("At-least-once", "May duplicate. Retry until acked.", BOX_ORANGE),
              ("Exactly-once", "Idempotent consumers + transactional commits.", BOX_GREEN)]
    yy = y
    for name, desc, fill in levels:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11.5)
        yy -= 70
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, yy - 20, "Recipe: deterministic IDs + idempotent sinks (upserts by key) + checkpointed offsets.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "The Streaming Stack",
                       "Pieces that fit together.")
    box(c, 72, 440, 200, 56, BOX_BLUE, "Kafka / Redpanda", "the log")
    box(c, 300, 440, 200, 56, BOX_GREEN, "Flink / Spark Streaming", "compute")
    box(c, 72, 350, 200, 56, BOX_ORANGE, "Schema Registry", "contracts")
    box(c, 300, 350, 200, 56, BOX_TEAL, "Sink connectors", "to warehouse/DB")
    arrow(c, 272, 468, 298, 468, color=ACCENT, width=1.5)
    arrow(c, 172, 438, 172, 408, color=ACCENT, width=1.5)
    arrow(c, 400, 438, 400, 408, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 300, "Schema Registry prevents 'field renamed, pipeline broke at 2am' — compatibility checked at publish.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Stream Processing — Remember",
                 ["The log (Kafka) is the foundation: immutable, ordered, replayable.",
                  "Windows slice infinity: tumbling, sliding, session — pick per question.",
                  "Event time = correctness; watermarks handle lateness.",
                  "Exactly-once = idempotent sinks + transactional offsets.",
                  "Schema Registry keeps producers and consumers in contract."],
                 pg)
    c.save(); print("wrote", path)


def pdf_warehouse(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Data Warehouses\n& Lakehouses",
               "Where analytics lives:\nfrom star schemas to open table formats.",
               "Data Engineering", None); pg += 1

    y = section_header(c, 1, 6, "OLTP vs OLAP",
                       "Two workloads, two architectures.")
    box(c, 72, y - 70, 225, 120, BOX_BLUE, "OLTP", "transactions", font_size=13)
    box(c, 315, y - 70, 225, 120, BOX_GREEN, "OLAP", "analytics", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    oltp = ["Many small writes", "Row-oriented, normalized", "Current state", "Ex: Postgres, MySQL"]
    olap = ["Few huge reads", "Columnar, denormalized", "Historical trends", "Ex: Snowflake, BigQuery"]
    yy = y - 100
    for t in oltp: c.drawString(88, yy, "• " + t); yy -= 18
    yy = y - 100
    for t in olap: c.drawString(331, yy, "• " + t); yy -= 18
    note(c, 72, 200, 468, "Never run analytics on your production OLTP — one bad query locks the checkout flow. Replicate to OLAP.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Star Schema: Facts & Dimensions",
                       "The lingua franca of analytics modeling.")
    box(c, 226, 380, 160, 80, BOX_ORANGE, "fact_orders", "keys + measures")
    dims = [("dim_customer", 72, 500), ("dim_product", 246, 500),
            ("dim_date", 420, 500), ("dim_region", 156, 260)]
    for name, bx, by in dims:
        box(c, bx, by, 140, 56, BOX_BLUE, name, "descriptive attrs")
        arrow(c, bx + 70, by if by > 380 else by + 56, 306, 380 if by > 380 else 460, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, 200, "Facts: measurable events (revenue, quantity). Dimensions: who/what/when/where.")
    c.drawString(72, 182, "Denormalized dimensions = fast joins = happy analysts.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Columnar Storage: Read Less, Go Faster",
                       "Analytics touches few columns of many rows — store by column.")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, y, "Row store (OLTP):")
    c.setFont(MONO_FONT, 9); c.setFillColor(MUTED)
    c.drawString(72, y - 22, "[id:1,name:A,amt:50] [id:2,name:B,amt:30] [id:3,name:C,amt:70] …")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, y - 52, "Columnar (OLAP):")
    c.setFont(MONO_FONT, 9); c.setFillColor(MUTED)
    c.drawString(72, y - 74, "ids:   [1,2,3,…]   names: [A,B,C,…]   amts: [50,30,70,…]")
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    yy = bullet_list(c, 72, y - 110,
        ["Query 'SUM(amt)': read ONE column, skip the rest — 10-100× less I/O.",
         "Same-type values compress beautifully (run-length, dictionary encoding).",
         "Parquet/ORC: the open columnar file formats. Partition by date for pruning."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Lakehouse: Lake + Warehouse",
                       "Cheap object storage with warehouse superpowers.")
    box(c, 72, 440, 468, 60, BOX_TEAL, "Object Storage (S3)", "all data, all formats, dirt cheap")
    box(c, 72, 350, 468, 60, BOX_BLUE, "Open Table Format (Delta / Iceberg / Hudi)",
        "ACID transactions • time travel • schema evolution — on the lake", font_size=10.5)
    box(c, 72, 260, 225, 60, BOX_GREEN, "BI & SQL", "warehouse queries")
    box(c, 315, 260, 225, 60, BOX_ORANGE, "ML & Python", "direct dataframe access")
    arrow(c, 306, 348, 306, 322, color=ACCENT, width=2)
    arrow(c, 184, 258, 184, 200, color=ACCENT, width=1.5)
    arrow(c, 427, 258, 427, 200, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawCentredString(306, 170, "One copy of data serving both SQL analysts and ML engineers.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Time Travel & Schema Evolution",
                       "Superpowers tables didn't used to have.")
    feats = [("Time travel", "Query data AS OF last Tuesday. Debug, audit, recover from bad writes.", BOX_BLUE),
             ("Schema evolution", "Add/rename columns without rewriting petabytes.", BOX_GREEN),
             ("Partition evolution", "Change partition layout without breaking old queries (Iceberg).", BOX_ORANGE),
             ("ACID", "Concurrent writers don't corrupt readers. Snapshots isolate.", BOX_TEAL)]
    yy = y
    for name, desc, fill in feats:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11.5)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Choosing Your Platform",
                       "Match the tool to the job.")
    plats = [("Cloud warehouses", "Snowflake, BigQuery, Redshift — serverless SQL, separate storage/compute.", BOX_BLUE),
             ("Lakehouse", "Databricks, open Iceberg/Delta on your own storage — engine freedom.", BOX_TEAL),
             ("Self-managed", "ClickHouse, DuckDB, Trino — control + cost at scale.", BOX_GREEN)]
    yy = y
    for name, desc, fill in plats:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, yy - 10, "Start simple (one warehouse). Add lakehouse when ML + BI must share data at scale.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Warehouses & Lakehouses — Remember",
                 ["OLTP = transactions (rows); OLAP = analytics (columns). Never mix the workloads.",
                  "Star schemas: central facts, surrounding dimensions — denormalize for speed.",
                  "Columnar storage (Parquet) reads only needed columns — massive I/O savings.",
                  "Lakehouse = warehouse features (ACID, time travel) on cheap object storage.",
                  "One data copy can serve both SQL analysts and ML pipelines."],
                 pg)
    c.save(); print("wrote", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out, exist_ok=True)
    pdf_etl(os.path.join(out, "bbg-etl-pipelines.pdf"))
    pdf_streaming(os.path.join(out, "bbg-stream-processing.pdf"))
    pdf_warehouse(os.path.join(out, "bbg-data-warehouses.pdf"))
