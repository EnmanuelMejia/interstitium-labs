"""Batch 14: Databases PDFs — SQL, NoSQL, internals, operations."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bbg_style import *


def code_block(c, x, y_top, lines, w=468, lh=16, font_size=10):
    """Light code panel with Courier lines. Returns bottom y."""
    h = len(lines) * lh + 18
    y = y_top - h
    c.setFillColor(LIGHT_BG); c.roundRect(x, y, w, h, 6, fill=1, stroke=0)
    c.setStrokeColor(MUTED); c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=0, stroke=1)
    c.setFillColor(INK); c.setFont(MONO_FONT, font_size)
    ty = y_top - 20
    for ln in lines:
        c.drawString(x + 12, ty, ln); ty -= lh
    return y


def pdf_sql_fundamentals(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SQL Fundamentals\nVisual Guide",
               "How queries are read, ordered, and executed --\nthe mental model every developer needs.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "SELECT Anatomy",
                       "A query is six clauses snapped together in written order.")
    cb = code_block(c, 72, y, [
        "SELECT   dept, AVG(salary) AS avg_pay",
        "FROM     employees",
        "WHERE    hired > '2023-01-01'",
        "GROUP BY dept",
        "HAVING   AVG(salary) > 90000",
        "ORDER BY avg_pay DESC",
        "LIMIT    10;"])
    labels = [("SELECT", "columns / expressions", BOX_BLUE),
              ("FROM", "tables + joins", BOX_PURP),
              ("WHERE", "row filter", BOX_RED),
              ("GROUP BY", "bucket rows", BOX_ORANGE),
              ("HAVING", "group filter", BOX_TEAL),
              ("ORDER BY / LIMIT", "sort + trim", BOX_GREEN)]
    yy = cb - 24
    bx = 72
    for name, desc, fill in labels:
        box(c, bx, yy, 148, 52, fill, name, desc, font_size=10)
        bx += 160
        if bx > 72 + 3 * 160:
            bx = 72; yy -= 66
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Logical Execution Order",
                       "The engine runs your query in a DIFFERENT order than you wrote it.")
    order = [("1  FROM / JOIN", "gather the tables", BOX_PURP),
             ("2  WHERE", "filter rows", BOX_RED),
             ("3  GROUP BY", "form buckets", BOX_ORANGE),
             ("4  HAVING", "filter buckets", BOX_TEAL),
             ("5  SELECT", "compute columns", BOX_BLUE),
             ("6  ORDER BY", "sort", BOX_GREEN),
             ("7  LIMIT", "trim", BOX_GREEN)]
    yy = y
    for name, desc, fill in order:
        box(c, 132, yy - 48, 348, 52, fill, name, desc, font_size=11)
        if yy < y:
            arrow(c, 306, yy + 4, 306, yy - 8, color=ACCENT, width=1.5)
        yy -= 62
    note(c, 72, 96, 468, "This is why a SELECT alias (avg_pay) cannot be used in WHERE -- WHERE runs before SELECT.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Filtering: WHERE vs HAVING",
                       "Row filters and group filters live at different stages.")
    box(c, 72, y - 90, 225, 110, BOX_RED, "WHERE", "filters ROWS", font_size=13)
    box(c, 315, y - 90, 225, 110, BOX_TEAL, "HAVING", "filters GROUPS", font_size=13)
    arrow(c, 297, y - 35, 315, y - 35, color=ACCENT, width=2, label="GROUP BY")
    cb = code_block(c, 72, y - 130, [
        "-- rows first: only 2024 hires enter the buckets",
        "WHERE hired >= '2024-01-01'",
        "-- groups second: only big departments survive",
        "HAVING COUNT(*) > 50"])
    note(c, 72, cb - 60, 468, "Golden rule: filter with WHERE whenever possible -- fewer rows grouped means less work.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "GROUP BY & Aggregates",
                       "Many rows in, one row per group out.")
    box(c, 72, y - 70, 140, 130, BOX_BLUE, "Input rows", "one row per\nemployee", font_size=11)
    arrow(c, 212, y - 5, 250, y - 5, color=ACCENT, width=2.5, label="GROUP BY dept")
    box(c, 250, y - 70, 130, 130, BOX_ORANGE, "Groups", "Eng / Sales /\nSupport", font_size=11)
    arrow(c, 380, y - 5, 418, y - 5, color=ACCENT, width=2.5, label="AVG()")
    box(c, 418, y - 70, 122, 130, BOX_GREEN, "Result", "one row per\ndept", font_size=11)
    cb = code_block(c, 72, y - 230, [
        "SELECT dept, COUNT(*), AVG(salary)",
        "FROM employees",
        "GROUP BY dept;",
        "-- every SELECT column must be grouped or aggregated"])
    note(c, 72, cb - 60, 468, "HAVING is WHERE for groups: it runs after aggregation, so it can use AVG()/COUNT().")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Window Functions: Intro",
                       "Aggregate-style math WITHOUT collapsing rows.")
    cb = code_block(c, 72, y, [
        "SELECT name, dept, salary,",
        "  ROW_NUMBER() OVER (PARTITION BY dept",
        "                     ORDER BY salary DESC) AS rank_in_dept",
        "FROM employees;"])
    fns = [("ROW_NUMBER()", "unique rank", BOX_BLUE),
           ("RANK()", "rank w/ ties", BOX_BLUE),
           ("LAG() / LEAD()", "prev / next row", BOX_GREEN),
           ("SUM() OVER", "running total", BOX_ORANGE)]
    yy = cb - 24
    bx = 72
    for name, desc, fill in fns:
        box(c, bx, yy, 222, 56, fill, name, desc, font_size=11)
        bx += 234
        if bx > 72 + 234:
            bx = 72; yy -= 70
    note(c, 72, yy - 16, 468, "Windows are computed AFTER WHERE / GROUP BY / HAVING -- they see the final row set, then add columns.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SQL Fundamentals -- Remember",
                 ["Written order (SELECT...FROM...WHERE) differs from execution order (FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT).",
                  "WHERE filters rows, HAVING filters groups -- push filters into WHERE to do less work.",
                  "GROUP BY collapses rows to one per group; every selected column must be grouped or aggregated.",
                  "Window functions (ROW_NUMBER, RANK, LAG/LEAD) add per-row math without collapsing rows.",
                  "SELECT aliases are invisible to WHERE -- it runs before SELECT."],
                 pg)
    c.save(); print("wrote", path)


def pdf_joins(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SQL Joins\nVisual Guide",
               "Inner, outer, semi, anti --\nand what the engine actually does underneath.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "INNER JOIN: The Overlap",
                       "Only rows with a match on BOTH sides survive.")
    c.setFillAlpha(0.45)
    c.setFillColor(BOX_BLUE); c.circle(250, 470, 95, fill=1, stroke=0)
    c.setFillColor(BOX_GREEN); c.circle(362, 470, 95, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setStrokeColor(INK); c.setLineWidth(1.5)
    c.circle(250, 470, 95, fill=0, stroke=1); c.circle(362, 470, 95, fill=0, stroke=1)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 12)
    c.drawCentredString(200, 474, "A"); c.drawCentredString(412, 474, "B")
    c.setFont(BODY_FONT, 10); c.drawCentredString(306, 430, "kept")
    cb = code_block(c, 72, 340, [
        "SELECT * FROM orders o",
        "INNER JOIN customers c ON o.cust_id = c.id;",
        "-- drops orders with no customer AND customers with no orders"])
    note(c, 72, cb - 60, 468, "The default JOIN. If a side has no match, its rows vanish from the result.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "LEFT / RIGHT: Keep One Side",
                       "Every row from the kept side appears at least once.")
    c.setFillAlpha(0.45)
    c.setFillColor(BOX_BLUE); c.circle(250, 470, 95, fill=1, stroke=0)
    c.setStrokeColor(INK); c.setLineWidth(1.5)
    c.setFillAlpha(1)
    c.circle(250, 470, 95, fill=0, stroke=1); c.circle(362, 470, 95, fill=0, stroke=1)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 12)
    c.drawCentredString(200, 474, "A"); c.drawCentredString(412, 474, "B")
    cb = code_block(c, 72, 340, [
        "SELECT * FROM customers c",
        "LEFT JOIN orders o ON o.cust_id = c.id;",
        "-- all customers; order columns are NULL where no order exists"])
    note(c, 72, cb - 60, 468, "RIGHT JOIN is the mirror image. Most teams standardize on LEFT only -- direction stays readable.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "FULL OUTER JOIN",
                       "Keep EVERYTHING from both sides.")
    c.setFillAlpha(0.45)
    c.setFillColor(BOX_BLUE); c.circle(250, 470, 95, fill=1, stroke=0)
    c.setFillColor(BOX_GREEN); c.circle(362, 470, 95, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setStrokeColor(INK); c.setLineWidth(1.5)
    c.circle(250, 470, 95, fill=0, stroke=1); c.circle(362, 470, 95, fill=0, stroke=1)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 12)
    c.drawCentredString(200, 474, "A"); c.drawCentredString(412, 474, "B")
    cb = code_block(c, 72, 340, [
        "SELECT * FROM a FULL OUTER JOIN b ON a.id = b.id;",
        "-- unmatched rows kept, missing side filled with NULLs"])
    note(c, 72, cb - 60, 468, "Rare in app code, common in reconciliation: find rows present in one system but not the other.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Semi & Anti Joins",
                       "Existence checks -- no row multiplication.")
    box(c, 72, y - 100, 225, 120, BOX_BLUE, "SEMI JOIN", "EXISTS / IN", font_size=13)
    box(c, 315, y - 100, 225, 120, BOX_RED, "ANTI JOIN", "NOT EXISTS", font_size=13)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, y - 130, "Keep A rows that HAVE a match.")
    c.drawString(315, y - 130, "Keep A rows that have NO match.")
    cb = code_block(c, 72, y - 160, [
        "-- semi: customers who placed at least one order",
        "SELECT * FROM customers c",
        "WHERE EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.id);",
        "",
        "-- anti: customers with zero orders (NOT IN is NULL-unsafe!)",
        "SELECT * FROM customers c",
        "WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.cust_id = c.id);"])
    note(c, 72, cb - 60, 468, "Semi/anti joins never duplicate A rows -- unlike a real JOIN, one A row yields at most one output row.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Join Algorithms",
                       "Three strategies the planner picks between.")
    algos = [("Nested Loop", "for each A row, scan B -- best when A is tiny / B indexed", BOX_BLUE),
             ("Hash Join", "hash B into memory, probe with A -- best for big equijoins", BOX_GREEN),
             ("Merge Join", "both sides sorted, zip together -- best when inputs pre-sorted", BOX_ORANGE)]
    yy = y
    for name, desc, fill in algos:
        box(c, 72, yy - 64, 468, 68, fill, name, desc, font_size=11.5)
        yy -= 84
    note(c, 72, yy - 10, 468, "EXPLAIN shows the choice. A hash join spilling to disk (work_mem too small) is a classic slowdown.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 6, 6, "Venn Diagrams, Done Right",
                       "What the circles actually mean -- and what they hide.")
    yy = bullet_list(c, 72, y, [
        "The circles are ROW SETS, not tables: each circle = the rows that table contributes.",
        "The overlap = rows surviving an INNER join. The rest = rows only outer joins keep.",
        "What Venn hides: DUPLICATES. One A row matching three B rows yields three output rows.",
        "Venn also hides the join key -- circles say nothing about WHICH columns matched.",
        "Use Venn for 'which rows survive', then read the ON clause for 'how they matched'."],
        font_size=11, gap=30)
    note(c, 72, 150, 468, "Mental model: Venn answers survival, the ON clause answers pairing, and cardinality answers row counts.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SQL Joins -- Remember",
                 ["INNER keeps only matches; LEFT keeps all of the left side (NULLs fill gaps); FULL OUTER keeps everything.",
                  "Semi (EXISTS) and anti (NOT EXISTS) joins test existence without multiplying rows.",
                  "Engines join via nested loop (small side), hash join (big equijoins), or merge join (sorted inputs).",
                  "Venn shows row survival, not duplicates or join keys -- always check the ON clause.",
                  "Prefer NOT EXISTS over NOT IN: NOT IN breaks silently when the subquery returns NULLs."],
                 pg)
    c.save(); print("wrote", path)


def pdf_acid(path):
    c = new_canvas(path); pg = 1
    title_page(c, "ACID Transactions\nVisual Guide",
               "Atomicity, Consistency, Isolation, Durability --\nand the machinery that delivers them.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "Atomicity & Durability",
                       "All-or-nothing execution, then surviving a crash.")
    box(c, 72, y - 70, 140, 70, BOX_BLUE, "BEGIN", "start txn", font_size=11)
    box(c, 246, y - 70, 140, 70, BOX_GREEN, "COMMIT", "all changes\nvisible", font_size=11)
    box(c, 420, y - 70, 120, 70, BOX_RED, "ROLLBACK", "nothing\nvisible", font_size=11)
    arrow(c, 212, y - 35, 244, y - 35, color=ACCENT, width=2)
    arrow(c, 386, y - 35, 418, y - 35, color=RED, width=2, label="on error")
    cb = code_block(c, 72, y - 170, [
        "-- durability: COMMIT appends to the Write-Ahead Log first",
        "-- crash recovery replays the WAL: committed txns restored,",
        "-- uncommitted txns rolled back. No torn writes."])
    box(c, 72, cb - 90, 468, 60, BOX_TEAL, "Write-Ahead Log (WAL)",
        "append-only log of every change -- the source of truth after a crash", font_size=11.5)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Read Phenomena",
                       "The three anomalies isolation levels defend against.")
    phen = [("Dirty Read", "read UNCOMMITTED data -- may be rolled back", BOX_RED),
            ("Non-Repeatable Read", "same row read twice, values differ", BOX_ORANGE),
            ("Phantom Read", "re-run query, NEW rows appear in the range", BOX_ORANGE)]
    yy = y
    for name, desc, fill in phen:
        box(c, 72, yy - 64, 468, 68, fill, name, desc, font_size=11.5)
        yy -= 84
    note(c, 72, yy - 10, 468, "Stronger isolation eliminates more phenomena -- at the cost of concurrency and throughput.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Isolation Levels",
                       "Four levels, from fastest to strictest.")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(300, y + 6, "Dirty read"); c.drawString(390, y + 6, "Non-rep.")
    c.drawString(472, y + 6, "Phantom")
    lvls = [("READ UNCOMMITTED", [RED, RED, RED], "rarely used"),
            ("READ COMMITTED", [GREEN, RED, RED], "Postgres / Oracle default"),
            ("REPEATABLE READ", [GREEN, GREEN, RED], "MySQL / InnoDB default"),
            ("SERIALIZABLE", [GREEN, GREEN, GREEN], "strictest, slowest")]
    yy = y
    for name, cols, note_t in lvls:
        box(c, 72, yy - 56, 210, 60, BOX_BLUE, name, note_t, font_size=10)
        xx = 300
        for col in cols:
            c.setFillColor(col); c.circle(xx + 22, yy - 26, 14, fill=1, stroke=0)
            c.setFillColor(white); c.setFont(TITLE_FONT, 9)
            c.drawCentredString(xx + 22, yy - 23, "no" if col == GREEN else "yes")
            xx += 90
        yy -= 76
    c.setFillColor(INK); c.setFont(BODY_FONT, 10)
    c.drawString(72, yy - 6, "Green = phenomenon prevented. Red = phenomenon possible.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "MVCC: Readers Never Block Writers",
                       "Every row carries versions; each transaction sees a snapshot.")
    box(c, 72, y - 60, 130, 56, BOX_BLUE, "v1", "xmin=10", font_size=10)
    box(c, 216, y - 60, 130, 56, BOX_ORANGE, "v2", "xmin=42 xmax=10", font_size=10)
    box(c, 360, y - 60, 130, 56, BOX_GREEN, "v3", "xmin=77 (live)", font_size=10)
    arrow(c, 202, y - 32, 214, y - 32, color=ACCENT, width=1.5)
    arrow(c, 346, y - 32, 358, y - 32, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 100, "UPDATE writes a NEW version; the old one stays until no snapshot needs it (VACUUM reclaims).")
    box(c, 72, y - 200, 468, 76, BOX_TEAL, "Snapshot Isolation",
        "txn starting at T sees versions committed before T -- writers never block readers", font_size=11)
    note(c, 72, y - 300, 468, "Cost: bloat. Dead versions pile up under long-running transactions -- keep txns short.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Locking",
                       "When MVCC is not enough, locks serialize access.")
    locks = [("Row locks", "UPDATE / DELETE take them automatically; SELECT ... FOR UPDATE takes them explicitly", BOX_BLUE),
             ("Table locks", "DDL (ALTER TABLE) blocks writers -- the classic deploy outage", BOX_RED),
             ("Advisory locks", "application-level mutexes (pg_advisory_lock) -- no table involved", BOX_GREEN)]
    yy = y
    for name, desc, fill in locks:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=11)
        yy -= 80
    box(c, 72, yy - 70, 225, 74, BOX_RED, "Deadlock", "T1 holds A waits B;\nT2 holds B waits A", font_size=11)
    box(c, 315, yy - 70, 225, 74, BOX_GREEN, "Fix", "lock in a fixed\norder; keep txns short", font_size=11)
    arrow(c, 297, yy - 33, 313, yy - 33, color=ACCENT, width=2)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "ACID Transactions -- Remember",
                 ["Atomicity: COMMIT makes everything visible, ROLLBACK makes nothing visible.",
                  "Durability comes from the WAL: committed data survives crashes via replay.",
                  "Isolation is a spectrum: dirty reads -> non-repeatable reads -> phantoms, eliminated level by level.",
                  "MVCC gives readers a snapshot so writers never block them -- at the cost of version bloat.",
                  "Locks serialize what MVCC cannot; lock tables in a fixed order and keep transactions short."],
                 pg)
    c.save(); print("wrote", path)

def pdf_normalization(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Normalization\nVisual Guide",
               "1NF to BCNF --\nkill redundancy without killing performance.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "The Problem: Anomalies",
                       "One table holding too much truth corrupts itself.")
    anoms = [("Update anomaly", "change a department's city in 50 rows -- miss one, data lies", BOX_RED),
             ("Insert anomaly", "cannot add a department with no employees yet", BOX_ORANGE),
             ("Delete anomaly", "delete the last employee, lose the department", BOX_ORANGE)]
    yy = y
    for name, desc, fill in anoms:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=11.5)
        yy -= 80
    note(c, 72, yy - 10, 468, "Normalization splits tables so each fact lives in exactly one place.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "1NF: Atomic Values",
                       "Every cell holds ONE value. No lists, no nested tables.")
    cb = code_block(c, 72, y, [
        "BAD  (1NF violation):",
        "  employees(id, name, phones)  ->  phones = '555-0142, 555-7781'",
        "",
        "GOOD (1NF): one row per phone",
        "  employee_phones(emp_id, phone)",
        "    (7, '555-0142')   (7, '555-7781')"])
    yy = bullet_list(c, 72, cb - 28, [
        "Test: can you query 'who has phone X' without string-splitting? If no, not 1NF.",
        "Repeating groups (phone1, phone2, phone3) are the classic smell."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "2NF: No Partial Dependencies",
                       "Every non-key column must depend on the WHOLE key.")
    cb = code_block(c, 72, y, [
        "BAD:  order_lines(order_id, product_id, product_name, qty)",
        "  key = (order_id, product_id), but product_name needs only product_id",
        "",
        "GOOD: split it",
        "  order_lines(order_id, product_id, qty)",
        "  products(product_id, product_name)"])
    box(c, 72, cb - 76, 468, 56, BOX_RED, "Partial dependency",
        "product_name depends on part of the key -- update it in one row, the others lie", font_size=10.5)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "3NF & BCNF: No Transitive Dependencies",
                       "Non-key columns must depend on the key, the whole key, nothing but the key.")
    cb = code_block(c, 72, y, [
        "BAD:  employees(id, name, dept_id, dept_city)",
        "  dept_city depends on dept_id, which is not the key (transitive)",
        "",
        "GOOD (3NF):",
        "  employees(id, name, dept_id)   departments(dept_id, dept_city)"])
    box(c, 72, cb - 76, 468, 60, BOX_PURP, "BCNF (stricter than 3NF)",
        "every determinant must be a candidate key -- fixes edge cases 3NF misses", font_size=11)
    note(c, 72, cb - 140, 468, "Most production schemas stop at 3NF/BCNF. 4NF/5NF exist but rarely pay off in app databases.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Denormalize Deliberately",
                       "Break the rules on purpose -- with a sync strategy.")
    dens = [("Read-heavy counters", "store comment_count on posts; update via trigger or job", BOX_GREEN),
            ("Hot join paths", "embed author_name in articles to skip the join", BOX_BLUE),
            ("Reporting snapshots", "flattened tables the warehouse owns outright", BOX_ORANGE)]
    yy = y
    for name, desc, fill in dens:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=11.5)
        yy -= 80
    note(c, 72, yy - 10, 468, "Rule: denormalize only measured hot paths, and own the invalidation story (triggers, CDC, or jobs).")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Normalization -- Remember",
                 ["Anomalies (update/insert/delete) are the disease; normalization is the cure.",
                  "1NF: atomic cells. 2NF: no partial key dependencies. 3NF/BCNF: no transitive dependencies.",
                  "Each normal form removes a class of redundancy -- stop at 3NF/BCNF for most apps.",
                  "Denormalize only for measured hot paths, and always own the sync/invalidation story.",
                  "A fact should live in exactly one place -- every copy is a future inconsistency."],
                 pg)
    c.save(); print("wrote", path)


def pdf_nosql_types(path):
    c = new_canvas(path); pg = 1
    title_page(c, "NoSQL Types\nVisual Guide",
               "Document, key-value, columnar, graph --\nfour data models, four superpowers.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 5, "Key-Value Stores",
                       "The simplest model: a giant distributed hash map.")
    box(c, 72, y - 60, 220, 56, BOX_BLUE, '"user:8421"', "-> blob", font_size=11)
    box(c, 306, y - 60, 220, 56, BOX_BLUE, '"cart:9910"', "-> blob", font_size=11)
    box(c, 72, y - 132, 220, 56, BOX_BLUE, '"session:ab12"', "-> blob", font_size=11)
    box(c, 306, y - 132, 220, 56, BOX_GREEN, "O(1) lookup", "by key only", font_size=11)
    yy = bullet_list(c, 72, y - 190, [
        "Strengths: blazing reads/writes, trivial sharding, tiny operational surface.",
        "Weakness: no queries by value, no joins -- you must know the key.",
        "Examples: Redis, DynamoDB, Riak. Home of sessions, carts, feature flags, counters."],
        font_size=11, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 5, "Document Stores",
                       "JSON-like documents, indexed and queryable.")
    cb = code_block(c, 72, y, [
        '{ "_id": "u8421", "name": "Ada",',
        '  "tags": ["pro", "beta"],',
        '  "address": { "city": "Lima", "zip": "15001" } }'])
    yy = bullet_list(c, 72, cb - 28, [
        "Strengths: flexible schema, nested data, rich secondary indexes, aggregation pipelines.",
        "Weakness: joins are awkward, cross-document transactions cost more.",
        "Examples: MongoDB, Couchbase, Firestore. Home of catalogs, profiles, CMS content."],
        font_size=11, gap=26)
    note(c, 72, 130, 468, "Embed what you read together; reference what grows unboundedly (comments, events).")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 5, "Columnar / Wide-Column Stores",
                       "Rows keyed by partition, columns grouped in families, built for massive scale.")
    box(c, 72, y - 70, 468, 90, BOX_TEAL, "Partition key: sensor-42",
        "timestamp -> {temp, humidity}   timestamp -> {temp, humidity}   ...", font_size=11)
    box(c, 72, y - 180, 468, 90, BOX_BLUE, "Partition key: sensor-43",
        "timestamp -> {temp, humidity}   timestamp -> {temp, humidity}   ...", font_size=11)
    yy = bullet_list(c, 72, y - 220, [
        "Strengths: linear write scale-out, cheap time-ordered scans, tunable consistency.",
        "Weakness: query patterns must be designed up front; ad-hoc joins are painful.",
        "Examples: Cassandra, ScyllaDB, HBase. Home of time series, IoT, messaging inboxes."],
        font_size=11, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 5, "Graph Stores",
                       "Nodes and edges as first-class citizens.")
    c.setFillColor(BOX_PURP)
    for (nx, ny, lbl) in [(180, 500, "Ada"), (430, 500, "Grace"), (305, 400, "DB-101")]:
        c.circle(nx, ny, 42, fill=1, stroke=0)
        c.setStrokeColor(INK); c.setLineWidth(1.2); c.circle(nx, ny, 42, fill=0, stroke=1)
        c.setFillColor(INK); c.setFont(TITLE_FONT, 10); c.drawCentredString(nx, ny - 4, lbl)
        c.setFillColor(BOX_PURP)
    arrow(c, 222, 500, 388, 500, color=ACCENT2, width=2, label="FOLLOWS")
    arrow(c, 205, 465, 280, 430, color=ACCENT2, width=2, label="TOOK")
    arrow(c, 405, 465, 330, 430, color=ACCENT2, width=2, label="TOOK")
    yy = bullet_list(c, 72, 300, [
        "Strengths: multi-hop traversals ('friends of friends who took DB-101') in milliseconds.",
        "Weakness: sharding graphs is hard; poor fit for bulk tabular analytics.",
        "Examples: Neo4j, Neptune. Home of fraud rings, recommendations, knowledge graphs."],
        font_size=11, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "NoSQL Types -- Remember",
                 ["Key-value: fastest lookups by key, zero query flexibility -- sessions, caches, counters.",
                  "Document: flexible JSON + real queries -- catalogs, profiles, content.",
                  "Wide-column: massive write scale with pre-designed access patterns -- time series, IoT.",
                  "Graph: relationships as data -- fraud, recommendations, knowledge graphs.",
                  "Choose by access pattern, not hype: model the queries first, then pick the store."],
                 pg)
    c.save(); print("wrote", path)


def pdf_mongodb(path):
    c = new_canvas(path); pg = 1
    title_page(c, "MongoDB\nVisual Guide",
               "Documents, pipelines, replica sets, sharding --\nthe document database in depth.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "The Document Model",
                       "Rich JSON documents replace rows.")
    cb = code_block(c, 72, y, [
        '{ _id: ObjectId("..."), sku: "KB-42",',
        '  name: "Keyboard", price: 129,',
        '  specs: { switches: "tactile", layout: "75%" },',
        '  reviews: [ {user: "ada", stars: 5}, ... ] }'])
    box(c, 72, cb - 80, 225, 60, BOX_GREEN, "Embed", "read together:\nreviews in product", font_size=10.5)
    box(c, 315, cb - 80, 225, 60, BOX_BLUE, "Reference", "grows forever:\norders -> users", font_size=10.5)
    note(c, 72, cb - 144, 468, "One document ~ one read. If a query needs two collections, reconsider the embedding.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Aggregation Pipeline",
                       "Documents flow through stages, each reshaping the stream.")
    stages = [("$match", "filter", BOX_RED), ("$group", "aggregate", BOX_ORANGE),
              ("$sort", "order", BOX_BLUE), ("$limit", "trim", BOX_GREEN),
              ("$project", "reshape", BOX_PURP)]
    bx = 72
    for name, desc, fill in stages:
        box(c, bx, y - 90, 86, 70, fill, name, desc, font_size=9.5)
        if bx > 72:
            arrow(c, bx - 10, y - 55, bx, y - 55, color=ACCENT, width=1.5)
        bx += 96
    cb = code_block(c, 72, y - 140, [
        "db.orders.aggregate([",
        "  { $match:  { status: 'paid' } },",
        "  { $group:  { _id: '$region', total: { $sum: '$amount' } } },",
        "  { $sort:   { total: -1 } },",
        "  { $limit:  5 }",
        "])"])
    note(c, 72, cb - 60, 468, "Pipeline rule: $match early. Filtering first shrinks every downstream stage.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Replica Sets",
                       "One primary, N secondaries, automatic failover.")
    box(c, 216, y - 80, 180, 70, BOX_GREEN, "PRIMARY", "all writes", font_size=12)
    box(c, 72, y - 210, 150, 70, BOX_BLUE, "SECONDARY", "replica", font_size=11)
    box(c, 246, y - 210, 150, 70, BOX_BLUE, "SECONDARY", "replica", font_size=11)
    box(c, 420, y - 210, 120, 70, BOX_BLUE, "SECONDARY", "replica", font_size=11)
    arrow(c, 270, y - 82, 150, y - 138, color=ACCENT, width=2, label="oplog")
    arrow(c, 342, y - 82, 320, y - 138, color=ACCENT, width=2)
    arrow(c, 396, y - 82, 470, y - 138, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 270, "Heartbeat every 2s. Primary down >10s: election, a secondary promotes itself.")
    note(c, 72, 150, 468, "Writes go to the primary only. Secondaries are for failover -- and optionally stale-tolerant reads.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Sharding",
                       "Distribute documents across shards by shard key.")
    box(c, 216, y - 70, 180, 60, BOX_PURP, "mongos", "query router", font_size=11)
    box(c, 216, y - 160, 180, 60, BOX_TEAL, "config servers", "metadata", font_size=11)
    arrow(c, 306, y - 72, 306, y - 98, color=ACCENT, width=2)
    shards = [("Shard 1", "key 0-33"), ("Shard 2", "key 34-66"), ("Shard 3", "key 67-99")]
    bx = 72
    for name, desc in shards:
        box(c, bx, y - 260, 148, 70, BOX_BLUE, name, desc, font_size=10.5)
        arrow(c, 306, y - 162, bx + 74, y - 188, color=ACCENT, width=1.5)
        bx += 160
    note(c, 72, 130, 468, "Shard key choice is forever-ish: high cardinality, even distribution, aligned with queries.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Consistency Knobs",
                       "Tune durability and freshness per operation.")
    box(c, 72, y - 90, 225, 110, BOX_ORANGE, "writeConcern", "w:1 / w:majority /\nw:all + journal", font_size=11)
    box(c, 315, y - 90, 225, 110, BOX_TEAL, "readPreference", "primary / secondary /\nnearest", font_size=11)
    cb = code_block(c, 72, y - 140, [
        "// strong: acknowledged by a majority, read from primary",
        "db.orders.insertOne(doc, { writeConcern: { w: 'majority' } })"])
    note(c, 72, cb - 60, 468, "Default (w:1, read primary) is fast. Majority writes + primary reads = linearizable-ish safety.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "MongoDB -- Remember",
                 ["Model as documents: embed what you read together, reference what grows unboundedly.",
                  "Aggregation pipelines reshape streams stage by stage -- always $match early.",
                  "Replica sets give automatic failover via elections; writes go to the primary.",
                  "Sharding scales horizontally but the shard key decision is nearly permanent.",
                  "writeConcern and readPreference let you trade speed for durability per operation."],
                 pg)
    c.save(); print("wrote", path)


def pdf_redis(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Redis\nVisual Guide",
               "Data structures, persistence, pub/sub --\nthe in-memory Swiss army knife.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "Data Structures",
                       "Not just strings -- a toolkit of types.")
    ds = [("Strings", "SET / GET -- cache values, counters (INCR)", BOX_BLUE),
          ("Hashes", "HSET user:1 name Ada -- objects, field-level ops", BOX_GREEN),
          ("Lists / Sets", "LPUSH / SADD -- queues, feeds, tags, dedupe", BOX_ORANGE),
          ("Sorted Sets", "ZADD leaderboard 1500 ada -- rankings, rate limits", BOX_PURP),
          ("Streams", "XADD events * -- durable log, consumer groups", BOX_TEAL)]
    yy = y
    for name, desc, fill in ds:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=10.5)
        yy -= 70
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Persistence: RDB vs AOF",
                       "Memory is fast; disks remember.")
    box(c, 72, y - 120, 225, 140, BOX_BLUE, "RDB", "point-in-time\nsnapshot", font_size=13)
    box(c, 315, y - 120, 225, 140, BOX_GREEN, "AOF", "append-only log\nof every write", font_size=13)
    yy = bullet_list(c, 72, y - 170, [
        "RDB: compact, fast restarts -- but lose minutes of data on crash.",
        "AOF (fsync everysec): lose ~1s max -- bigger files, slower rewrites.",
        "Production default: BOTH. RDB for fast boot, AOF for durability."],
        font_size=11, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Pub/Sub & Streams",
                       "Fire-and-forget messaging vs durable logs.")
    box(c, 72, y - 80, 150, 70, BOX_ORANGE, "Publisher", "PUBLISH", font_size=11)
    box(c, 276, y - 80, 120, 70, BOX_PURP, "Channel", "news", font_size=11)
    box(c, 450, y - 80, 90, 70, BOX_BLUE, "Sub x N", "", font_size=11)
    arrow(c, 222, y - 45, 274, y - 45, color=ACCENT, width=2)
    arrow(c, 396, y - 45, 448, y - 45, color=ACCENT, width=2)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 130, "Pub/Sub: no persistence -- offline subscribers MISS messages.")
    box(c, 72, y - 230, 468, 80, BOX_TEAL, "Streams (XADD / XREADGROUP)",
        "durable append-only log + consumer groups -- Kafka-lite inside Redis", font_size=11.5)
    note(c, 72, 140, 468, "Need guaranteed delivery? Streams. Need live fan-out? Pub/Sub.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Caching Patterns",
                       "Cache-aside: the workhorse pattern.")
    box(c, 72, y - 70, 110, 60, BOX_BLUE, "App", "", font_size=11)
    box(c, 246, y - 70, 110, 60, BOX_ORANGE, "Redis", "TTL", font_size=11)
    box(c, 420, y - 70, 120, 60, BOX_GREEN, "Database", "truth", font_size=11)
    arrow(c, 182, y - 50, 244, y - 50, color=ACCENT, width=2, label="1 GET")
    arrow(c, 356, y - 50, 418, y - 50, color=RED, width=2, label="2 miss")
    arrow(c, 418, y - 30, 356, y - 30, color=GREEN, width=2, label="3 fill")
    yy = bullet_list(c, 72, y - 170, [
        "Read: check cache -> miss -> read DB -> SET with TTL.",
        "Write: update DB, then DELETE the cache key (invalidate, don't update).",
        "Thundering herd: one miss x 10k requests -- use locks or request coalescing."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Operating Redis",
                       "Eviction, expiry, and clustering.")
    ops = [("Eviction policies", "allkeys-lru / volatile-ttl / noeviction -- pick per use case", BOX_RED),
           ("TTL everything", "keys without expiry are memory leaks with extra steps", BOX_ORANGE),
           ("Cluster hash slots", "16384 slots sharded across nodes -- multi-key ops must share a slot", BOX_BLUE)]
    yy = y
    for name, desc, fill in ops:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=11)
        yy -= 80
    note(c, 72, yy - 10, 468, "Monitor used_memory + evicted_keys: evictions climbing means the working set outgrew RAM.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Redis -- Remember",
                 ["Pick the right structure: strings, hashes, sets, sorted sets, streams -- each is a tool.",
                  "Persist with RDB + AOF together: fast restarts plus ~1s durability.",
                  "Streams give durable consumer-group messaging; pub/sub is ephemeral fan-out.",
                  "Cache-aside: read-through on miss, invalidate (not update) on write, TTL everything.",
                  "Watch memory: eviction policy + TTLs decide whether Redis stays fast or starts shedding."],
                 pg)
    c.save(); print("wrote", path)

def pdf_cassandra(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Cassandra\nVisual Guide",
               "Wide-column storage, tunable consistency, gossip --\nbuilt for write scale.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "The Wide-Column Model",
                       "Partition key decides the node; clustering key orders rows inside.")
    cb = code_block(c, 72, y, [
        "CREATE TABLE readings (",
        "  sensor_id text,                 -- PARTITION KEY: which node",
        "  ts timestamp,                   -- CLUSTERING KEY: order within partition",
        "  temp float, humidity float,",
        "  PRIMARY KEY (sensor_id, ts) );"])
    box(c, 72, cb - 90, 468, 70, BOX_TEAL, "Partition: sensor-42",
        "ts rows stored sorted together -- one partition = one fast sequential read", font_size=11)
    note(c, 72, cb - 154, 468, "Design rule: model around queries. Each query should ideally hit ONE partition.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Partitioning & the Token Ring",
                       "Every node owns token ranges; data is hashed onto the ring.")
    c.setStrokeColor(ACCENT); c.setLineWidth(2)
    c.circle(306, 440, 120, fill=0, stroke=1)
    nodes = [(306, 560, "N1"), (426, 440, "N2"), (306, 320, "N3"), (186, 440, "N4")]
    for nx, ny, lbl in nodes:
        c.setFillColor(BOX_BLUE); c.circle(nx, ny, 30, fill=1, stroke=0)
        c.setStrokeColor(INK); c.setLineWidth(1.2); c.circle(nx, ny, 30, fill=0, stroke=1)
        c.setFillColor(INK); c.setFont(TITLE_FONT, 10); c.drawCentredString(nx, ny - 4, lbl)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, 270, "hash(partition key) -> token -> owning node. Vnodes split each node into many small ranges.")
    note(c, 72, 150, 468, "Replication factor 3: each partition lives on 3 nodes around the ring -- no single point of loss.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Tunable Consistency",
                       "Choose per query: how many replicas must agree?")
    cons = [("ONE", "fastest, weakest -- 1 replica ack", BOX_GREEN),
            ("QUORUM", "majority -- the sane default", BOX_BLUE),
            ("LOCAL_QUORUM", "majority within the datacenter", BOX_TEAL),
            ("ALL", "every replica -- slowest, strongest", BOX_RED)]
    yy = y
    for name, desc, fill in cons:
        box(c, 72, yy - 52, 468, 56, fill, name, desc, font_size=11.5)
        yy -= 70
    box(c, 72, yy - 66, 468, 60, BOX_ORANGE, "The quorum rule: R + W > N",
        "read replicas + write replicas > replication factor = strong consistency", font_size=11.5)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Gossip Protocol",
                       "No master: nodes gossip state to each other.")
    c.setFillColor(BOX_PURP)
    gnodes = [(150, 480), (300, 520), (450, 480), (225, 400), (375, 400)]
    for nx, ny in gnodes:
        c.circle(nx, ny, 28, fill=1, stroke=0)
        c.setStrokeColor(INK); c.setLineWidth(1); c.circle(nx, ny, 28, fill=0, stroke=1)
        c.setFillColor(BOX_PURP)
    arrow(c, 178, 480, 272, 510, color=ACCENT2, width=1.5)
    arrow(c, 328, 510, 422, 490, color=ACCENT2, width=1.5)
    arrow(c, 300, 492, 240, 428, color=ACCENT2, width=1.5)
    arrow(c, 422, 462, 388, 428, color=ACCENT2, width=1.5)
    yy = bullet_list(c, 72, 330, [
        "Every second, each node gossips its state (up/down, load, schema) to random peers.",
        "Failure detection is decentralized: silence for a timeout = suspected down.",
        "Seed nodes bootstrap new joiners; after that every node is equal."],
        font_size=11, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Compaction",
                       "Writes are fast because they are append-only -- compaction cleans up.")
    box(c, 72, y - 70, 150, 70, BOX_GREEN, "Memtable", "in memory", font_size=11)
    arrow(c, 222, y - 35, 260, y - 35, color=ACCENT, width=2, label="flush")
    box(c, 260, y - 70, 120, 70, BOX_BLUE, "SSTable", "on disk", font_size=11)
    box(c, 400, y - 70, 120, 70, BOX_BLUE, "SSTable", "on disk", font_size=11)
    arrow(c, 320, y - 72, 320, y - 110, color=ACCENT, width=2)
    arrow(c, 460, y - 72, 430, y - 110, color=ACCENT, width=2)
    box(c, 246, y - 180, 220, 70, BOX_ORANGE, "Compaction", "merge + drop\ntombstones", font_size=11)
    yy = bullet_list(c, 72, y - 230, [
        "LSM-tree: writes hit memtable, flush to immutable SSTables -- never random writes.",
        "Compaction merges SSTables, evicts deleted data (tombstones) and expired TTLs.",
        "Strategies: STCS (default), LCS (read-heavy), TWCS (time series). Pick per table."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Cassandra -- Remember",
                 ["Model per query: partition key picks the node, clustering key orders rows inside it.",
                  "Consistent hashing on a token ring spreads data; RF=3 keeps every partition on three nodes.",
                  "Consistency is tunable per query -- QUORUM is the sane default; R + W > N gives strong reads.",
                  "Gossip replaces the master: decentralized membership and failure detection.",
                  "LSM writes are append-only fast; compaction merges SSTables and reclaims tombstones."],
                 pg)
    c.save(); print("wrote", path)


def pdf_dynamodb(path):
    c = new_canvas(path); pg = 1
    title_page(c, "DynamoDB\nVisual Guide",
               "Keys, indexes, capacity, single-table design --\nserverless NoSQL at scale.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "Partition Keys & Sort Keys",
                       "The primary key IS the scaling strategy.")
    box(c, 72, y - 80, 225, 100, BOX_BLUE, "PK only", "user_id ->\none item", font_size=11)
    box(c, 315, y - 80, 225, 100, BOX_GREEN, "PK + SK", "user_id +\norder_date -> many", font_size=11)
    cb = code_block(c, 72, y - 120, [
        "-- PK=user:8421, SK=order#2026-10-01  (item collection)",
        "-- PK=user:8421, SK=order#2026-10-02",
        "-- PK=user:8421, SK=profile           (different entity, same user)",
        "-- Query(PK=user:8421) returns ALL of them, sorted by SK"])
    note(c, 72, cb - 60, 468, "Sort keys turn one partition into an ordered collection -- the most powerful DynamoDB pattern.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "How Partitioning Works",
                       "hash(PK) assigns items to partitions -- automatically split as you grow.")
    box(c, 72, y - 70, 140, 70, BOX_PURP, "hash(PK)", "partition\nassignment", font_size=10.5)
    arrow(c, 212, y - 35, 250, y - 35, color=ACCENT, width=2)
    for i, lbl in enumerate(["P1", "P2", "P3"]):
        box(c, 250 + i * 100, y - 70, 90, 70, BOX_BLUE, lbl, "10GB /\n3k RCU", font_size=10)
    yy = bullet_list(c, 72, y - 180, [
        "Partitions split automatically past ~10GB or throughput limits -- no ops work.",
        "HOT PARTITION: one PK getting all traffic throttles while others idle -- design keys for spread.",
        "Adaptive capacity helps bursts, but a bad key design is still a bad key design."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "GSIs & LSIs",
                       "Alternate query paths over the same data.")
    box(c, 72, y - 90, 468, 80, BOX_BLUE, "Base table", "PK=user_id, SK=order_date", font_size=11.5)
    arrow(c, 200, y - 92, 200, y - 120, color=ACCENT, width=2)
    arrow(c, 412, y - 92, 412, y - 120, color=ACCENT, width=2)
    box(c, 72, y - 200, 225, 80, BOX_GREEN, "GSI", "any PK/SK;\nown throughput", font_size=11)
    box(c, 315, y - 200, 225, 80, BOX_ORANGE, "LSI", "same PK, alt SK;\ncreated at birth", font_size=11)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 230, "GSI example: PK=status, SK=created_at -- 'all pending orders, newest first'.")
    note(c, 72, 150, 468, "GSIs are eventually consistent and cost write throughput. LSIs are strongly consistent but must be defined at table creation.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Capacity Modes",
                       "Pay for what you provision, or pay per request.")
    box(c, 72, y - 110, 225, 130, BOX_BLUE, "Provisioned", "RCU / WCU\nreserved", font_size=12)
    box(c, 315, y - 110, 225, 130, BOX_GREEN, "On-demand", "pay per\nrequest", font_size=12)
    yy = bullet_list(c, 72, y - 160, [
        "1 RCU = 1 strongly-consistent 4KB read/sec. 1 WCU = 1 1KB write/sec.",
        "Provisioned + auto-scaling wins for steady traffic; on-demand for spiky/unknown.",
        "Throttling (ProvisionedThroughputExceeded) = raise capacity or fix hot keys."],
        font_size=11, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Single-Table Design",
                       "One table, many entity types, access patterns first.")
    cb = code_block(c, 72, y, [
        "Table: app  (PK, SK hold EVERYTHING)",
        "  PK=USER#8421   SK=PROFILE#8421      -> user profile",
        "  PK=USER#8421   SK=ORDER#2026-10-01  -> an order",
        "  PK=ORDER#9910  SK=USER#8421         -> inverted lookup (via GSI)",
        "-- each access pattern = one Query on PK (+ optional SK prefix)"])
    yy = bullet_list(c, 72, cb - 28, [
        "List every access pattern BEFORE modeling: 'get user', 'user's orders', 'orders by status'.",
        "Overloaded keys with prefixes (USER#, ORDER#) let GSIs re-index the same items.",
        "Trade-off: brilliant reads, but the model is opaque -- document patterns in code."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "DynamoDB -- Remember",
                 ["The key schema is the database: PK spreads load, SK builds ordered collections.",
                  "Partitions split automatically; hot partitions throttle -- design keys for even spread.",
                  "GSIs add new query paths (eventual, extra cost); LSIs are same-PK alternates fixed at creation.",
                  "Provisioned suits steady traffic, on-demand suits spiky -- know your RCU/WCU math.",
                  "Single-table design: enumerate access patterns first, then overload one table with prefixed keys."],
                 pg)
    c.save(); print("wrote", path)


def pdf_postgres(path):
    c = new_canvas(path); pg = 1
    title_page(c, "PostgreSQL Advanced\nVisual Guide",
               "JSONB, extensions, partitioning, full-text search --\nthe database that does everything.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "JSONB: Documents in a Row",
                       "Schema-flexible columns with real indexing.")
    cb = code_block(c, 72, y, [
        "CREATE TABLE products (id serial PRIMARY KEY,",
        "  attrs jsonb);",
        "-- query inside the document:",
        "SELECT * FROM products",
        "WHERE attrs @> '{\"color\": \"red\"}';",
        "-- index it: CREATE INDEX ON products USING gin (attrs);"])
    yy = bullet_list(c, 72, cb - 28, [
        "Operators: -> (field), ->> (field as text), @> (contains), ? (has key).",
        "GIN indexes make containment queries fast -- jsonb without GIN is a table scan.",
        "Rule: JSONB for flexible payloads, real columns for fields you filter/join on."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Extensions",
                       "CREATE EXTENSION turns Postgres into something new.")
    exts = [("PostGIS", "geometry/geography types -- the serious GIS database", BOX_GREEN),
            ("pgvector", "vector type + HNSW/IVFFlat -- embeddings search in SQL", BOX_PURP),
            ("pg_trgm", "trigram similarity -- fuzzy text matching", BOX_BLUE),
            ("uuid-ossp / pgcrypto", "UUIDs, hashing, encryption primitives", BOX_ORANGE)]
    yy = y
    for name, desc, fill in exts:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    note(c, 72, yy - 10, 468, "Managed clouds allowlist extensions -- verify PostGIS/pgvector availability before designing around them.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Table Partitioning",
                       "One logical table, many physical children.")
    box(c, 196, y - 70, 220, 60, BOX_PURP, "events (parent)", "PARTITION BY RANGE (ts)", font_size=11)
    arrow(c, 306, y - 72, 150, y - 110, color=ACCENT, width=1.5)
    arrow(c, 306, y - 72, 306, y - 110, color=ACCENT, width=1.5)
    arrow(c, 306, y - 72, 462, y - 110, color=ACCENT, width=1.5)
    for i, lbl in enumerate(["events_2026_08", "events_2026_09", "events_2026_10"]):
        box(c, 72 + i * 160, y - 180, 148, 70, BOX_BLUE, lbl, "child table", font_size=10)
    yy = bullet_list(c, 72, y - 230, [
        "Partition pruning: WHERE ts >= '2026-10-01' touches only matching children.",
        "Drop old partitions in milliseconds instead of DELETEing billions of rows.",
        "Range (time), list (region), hash (even spread) -- pick by query pattern."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Full-Text Search",
                       "Real search without an external engine -- for moderate scale.")
    box(c, 72, y - 70, 140, 70, BOX_BLUE, "to_tsvector", "doc ->\nlexemes", font_size=10.5)
    arrow(c, 212, y - 35, 250, y - 35, color=ACCENT, width=2)
    box(c, 250, y - 70, 140, 70, BOX_GREEN, "GIN index", "lexeme ->\ndocs", font_size=10.5)
    arrow(c, 390, y - 35, 428, y - 35, color=ACCENT, width=2)
    box(c, 428, y - 70, 112, 70, BOX_ORANGE, "tsquery", "ranked\nresults", font_size=10.5)
    cb = code_block(c, 72, y - 120, [
        "SELECT title FROM articles",
        "WHERE to_tsvector('english', body) @@ to_tsquery('postgres & search')",
        "ORDER BY ts_rank(to_tsvector('english', body),",
        "                 to_tsquery('postgres & search')) DESC;"])
    note(c, 72, cb - 60, 468, "Handles stemming, stop words, ranking. Outgrown it? Replicate to OpenSearch/Typesense.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Performance Toolkit",
                       "Built-in instruments for slow queries.")
    tools = [("EXPLAIN (ANALYZE, BUFFERS)", "the actual plan + real timings -- always start here", BOX_BLUE),
             ("pg_stat_statements", "which queries burn the most total time -- the hit list", BOX_GREEN),
             ("autovacuum", "reclaims dead tuples; never disable it, tune it", BOX_ORANGE),
             ("pg_stat_user_tables", "seq scans vs index scans per table -- missing-index radar", BOX_TEAL)]
    yy = y
    for name, desc, fill in tools:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "PostgreSQL Advanced -- Remember",
                 ["JSONB + GIN gives document flexibility inside a relational engine -- index what you query.",
                  "Extensions (PostGIS, pgvector, pg_trgm) turn Postgres into GIS, vector, and fuzzy-search stores.",
                  "Partition large tables by time/range: pruning speeds queries, dropping beats deleting.",
                  "Full-text search with tsvector/tsquery covers moderate scale before you need a search cluster.",
                  "EXPLAIN ANALYZE, pg_stat_statements, and autovacuum are the core performance loop."],
                 pg)
    c.save(); print("wrote", path)


def pdf_query_planning(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Query Planning\nVisual Guide",
               "EXPLAIN ANALYZE, index selection, join order --\nthink like the planner.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "Reading EXPLAIN ANALYZE",
                       "A tree of nodes: read bottom-up, inside-out.")
    cb = code_block(c, 72, y, [
        "Hash Join  (cost=...) (actual rows=8421 loops=1)",
        "  ->  Seq Scan on orders      (actual rows=50000)",
        "  ->  Hash  (actual rows=1200)",
        "        ->  Index Scan on customers (actual rows=1200)"])
    yy = bullet_list(c, 72, cb - 28, [
        "Indentation = execution order: children run before parents.",
        "actual rows vs estimated rows: a 10x gap means stale statistics.",
        "loops > 1: the node ran repeatedly -- multiply cost by loops.",
        "ANALYZE runs the query (use EXPLAIN without ANALYZE to avoid executing)."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Index Selection",
                       "The planner is a cost accountant, not a rule follower.")
    box(c, 72, y - 80, 225, 100, BOX_GREEN, "Index Scan", "selective:\n1% of rows", font_size=11)
    box(c, 315, y - 80, 225, 100, BOX_ORANGE, "Seq Scan", "unselective:\n80% of rows", font_size=11)
    yy = bullet_list(c, 72, y - 130, [
        "An index is skipped when the planner expects to read most of the table anyway.",
        "Random page cost vs seq page cost: indexes win on selectivity, lose on bulk.",
        "Functions on columns (WHERE lower(email)=...) defeat indexes -- index the expression instead."],
        font_size=10.5, gap=26)
    note(c, 72, 150, 468, "The planner can be wrong: if it misestimates selectivity, it picks the wrong scan. Fix the stats, not the query.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Join Ordering",
                       "Join the most selective tables first.")
    box(c, 72, y - 70, 130, 70, BOX_BLUE, "orders", "50k rows", font_size=11)
    box(c, 216, y - 70, 130, 70, BOX_GREEN, "customers", "1.2k filtered", font_size=11)
    box(c, 360, y - 70, 130, 70, BOX_ORANGE, "items", "200k rows", font_size=11)
    arrow(c, 202, y - 35, 214, y - 35, color=GREEN, width=2.5, label="good")
    arrow(c, 346, y - 35, 358, y - 35, color=RED, width=2.5, label="late")
    yy = bullet_list(c, 72, y - 180, [
        "Small intermediate results keep hash tables in memory -- join order is memory order.",
        "The planner reorders joins freely (join_collapse_limit); FROM order is a hint at best.",
        "Cross joins (missing ON clause) explode cardinality -- the classic accidental cartesian product."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Statistics",
                       "The planner only knows what ANALYZE told it.")
    box(c, 72, y - 70, 150, 70, BOX_BLUE, "ANALYZE", "samples\ntables", font_size=11)
    arrow(c, 222, y - 35, 260, y - 35, color=ACCENT, width=2)
    box(c, 260, y - 70, 150, 70, BOX_GREEN, "pg_stats", "histograms +\nndistinct", font_size=11)
    arrow(c, 410, y - 35, 448, y - 35, color=ACCENT, width=2)
    box(c, 448, y - 70, 92, 70, BOX_ORANGE, "planner", "cost\nchoices", font_size=11)
    yy = bullet_list(c, 72, y - 180, [
        "Stale stats after bulk loads: run ANALYZE manually, don't wait for autovacuum.",
        "Skewed columns (status='active' 99%) need higher statistics targets.",
        "Correlated columns (city, zip) fool single-column stats -- extended statistics help."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Fixing Slow Queries",
                       "A checklist, in order.")
    fixes = [("1. EXPLAIN ANALYZE", "find the node eating time -- don't guess", BOX_BLUE),
             ("2. Missing index?", "high-cost seq scan on a selective filter", BOX_GREEN),
             ("3. Wrong data type", "joining text to int defeats indexes and hashes", BOX_RED),
             ("4. N+1 queries", "one query per row in a loop -- batch or JOIN it", BOX_ORANGE)]
    yy = y
    for name, desc, fill in fixes:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Query Planning -- Remember",
                 ["Read EXPLAIN bottom-up: children execute first; compare actual vs estimated rows.",
                  "The planner picks scans by cost: selective filters get indexes, bulk reads get seq scans.",
                  "Join selective tables first -- small intermediates keep hash joins in memory.",
                  "Statistics drive every decision: ANALYZE after bulk loads, raise targets on skewed columns.",
                  "Fix slow queries in order: EXPLAIN, missing index, type mismatches, N+1 patterns."],
                 pg)
    c.save(); print("wrote", path)

def pdf_replication(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Database Replication\nVisual Guide",
               "Streaming, lag, failover --\nkeeping copies in sync and surviving the primary's death.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "Streaming vs Logical Replication",
                       "Two ways to ship changes to a replica.")
    box(c, 72, y - 70, 150, 70, BOX_GREEN, "PRIMARY", "writes", font_size=11)
    arrow(c, 222, y - 35, 280, y - 35, color=ACCENT, width=2.5, label="WAL")
    box(c, 280, y - 70, 150, 70, BOX_BLUE, "REPLICA", "byte-identical", font_size=11)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y - 100, "Physical (streaming): ships WAL bytes -- replica is a block-level clone.")
    box(c, 72, y - 210, 150, 70, BOX_GREEN, "PUBLISHER", "writes", font_size=11)
    arrow(c, 222, y - 175, 280, y - 175, color=TEAL, width=2.5, label="row changes")
    box(c, 280, y - 210, 150, 70, BOX_TEAL, "SUBSCRIBER", "table subset", font_size=11)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
    c.drawString(72, y - 240, "Logical: decodes row changes -- selective tables, cross-version, transforms possible.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Synchronous vs Asynchronous",
                       "Durability and latency are the same dial.")
    box(c, 72, y - 110, 225, 130, BOX_GREEN, "Synchronous", "commit waits for\nreplica ack", font_size=12)
    box(c, 315, y - 110, 225, 130, BOX_ORANGE, "Asynchronous", "commit returns\nimmediately", font_size=12)
    yy = bullet_list(c, 72, y - 160, [
        "Sync: zero data loss on failover -- but every write pays replica round-trip latency.",
        "Async: fast writes -- but a crash can lose the last seconds of transactions.",
        "Middle ground: sync to ONE nearby replica, async to the rest (quorum-style)."],
        font_size=11, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Lag Monitoring",
                       "A replica is only useful if it is current.")
    lags = [("Replay lag (time)", "how far behind in seconds -- alert at your RPO threshold", BOX_RED),
            ("WAL bytes behind", "volume of un-applied changes -- spikes signal trouble", BOX_ORANGE),
            ("Connection state", "streaming / catchup / down -- dead replicas page loudly", BOX_BLUE)]
    yy = y
    for name, desc, fill in lags:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=11)
        yy -= 80
    note(c, 72, yy - 10, 468, "Causes of lag: long-running queries on the replica, under-provisioned I/O, network partitions.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Failover & Promotion",
                       "The primary dies. Now what -- in order.")
    steps = [("1. Confirm", "primary truly dead, not partitioned -- avoid split-brain", BOX_RED),
             ("2. Promote", "replica becomes primary (pg_ctl promote / managed failover)", BOX_GREEN),
             ("3. Repoint", "apps connect to the new primary -- via proxy or DNS", BOX_BLUE),
             ("4. Rebuild", "old primary rejoins as a replica -- or a fresh one is built", BOX_ORANGE)]
    yy = y
    for name, desc, fill in steps:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    note(c, 72, yy - 10, 468, "Practice this quarterly. Failover you have never rehearsed is failover that fails.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Read Scaling with Replicas",
                       "Offload reads -- carefully.")
    box(c, 72, y - 70, 150, 70, BOX_GREEN, "PRIMARY", "all writes", font_size=11)
    box(c, 306, y - 70, 110, 70, BOX_BLUE, "Replica 1", "reads", font_size=10.5)
    box(c, 430, y - 70, 110, 70, BOX_BLUE, "Replica 2", "reads", font_size=10.5)
    arrow(c, 222, y - 35, 304, y - 35, color=ACCENT, width=2, label="WAL")
    c.setFillColor(INK); c.setFont(BODY_FONT, 11)
    c.drawString(246, y - 35, "app writes"); c.drawString(360, y - 110, "app reads")
    yy = bullet_list(c, 72, y - 180, [
        "Route analytics/reporting to replicas; keep transactional reads on the primary.",
        "Replica lag means read-your-write breaks: a user may not see their own update.",
        "Connection proxies (PgBouncer, ProxySQL) split read/write traffic transparently."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Database Replication -- Remember",
                 ["Physical replication clones WAL bytes; logical replication ships decoded row changes selectively.",
                  "Synchronous = zero loss but slower writes; asynchronous = fast but can lose recent commits.",
                  "Monitor replay lag in seconds AND bytes behind -- alert at your RPO threshold.",
                  "Failover order: confirm death, promote, repoint apps, rebuild -- and rehearse it quarterly.",
                  "Read replicas scale reads, but lag breaks read-your-write -- route wisely."],
                 pg)
    c.save(); print("wrote", path)


def pdf_sharding_practice(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Sharding in Practice\nVisual Guide",
               "Shard keys, resharding, Vitess, Citus --\nscaling out without losing your mind.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "When to Shard",
                       "Sharding is the last resort -- recognize the real signals.")
    sigs = [("Write volume", "single primary cannot keep up, even with bigger hardware", BOX_RED),
            ("Data size", "dataset exceeds what one node holds / backs up sanely", BOX_ORANGE),
            ("Connection limits", "thousands of app connections overwhelm one server", BOX_BLUE)]
    yy = y
    for name, desc, fill in sigs:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=11.5)
        yy -= 80
    note(c, 72, yy - 10, 468, "Try first: bigger instance, read replicas, caching, partitioning. Shard when those are exhausted.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Choosing a Shard Key",
                       "The most permanent decision in the design.")
    box(c, 72, y - 110, 225, 130, BOX_GREEN, "Good: tenant_id", "high cardinality,\neven spread,\nqueries filter by it", font_size=11)
    box(c, 315, y - 110, 225, 130, BOX_RED, "Bad: country", "3 values ->\n3 hot shards", font_size=11)
    yy = bullet_list(c, 72, y - 160, [
        "Cardinality: thousands+ distinct values so shards fill evenly.",
        "Locality: queries should hit ONE shard (avoid scatter-gather fan-out).",
        "Stability: keys that never change -- re-keying means moving data."],
        font_size=11, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Resharding Strategies",
                       "Moving data while the system stays up.")
    box(c, 72, y - 70, 200, 70, BOX_BLUE, "Old shards", "serving reads", font_size=11)
    box(c, 340, y - 70, 200, 70, BOX_GREEN, "New shards", "filling up", font_size=11)
    arrow(c, 272, y - 35, 338, y - 35, color=ACCENT, width=2.5, label="dual-write")
    yy = bullet_list(c, 72, y - 180, [
        "Dual-write: new writes go to both; backfill copies history in batches.",
        "Verify counts/checksums per shard, then flip reads, then retire old shards.",
        "Range splits (split one hot shard) beat full rehashes -- less data moves."],
        font_size=10.5, gap=26)
    note(c, 72, 150, 468, "Resharding is a migration project, not a config change -- plan verification like a deploy.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Vitess Architecture",
                       "Sharded MySQL behind a smart proxy.")
    box(c, 216, y - 70, 180, 60, BOX_PURP, "vtgate", "query router", font_size=11)
    box(c, 72, y - 180, 150, 70, BOX_BLUE, "vttablet", "shard 1", font_size=11)
    box(c, 246, y - 180, 150, 70, BOX_BLUE, "vttablet", "shard 2", font_size=11)
    box(c, 420, y - 180, 120, 70, BOX_BLUE, "vttablet", "shard 3", font_size=11)
    arrow(c, 306, y - 72, 150, y - 108, color=ACCENT, width=1.5)
    arrow(c, 306, y - 72, 320, y - 108, color=ACCENT, width=1.5)
    arrow(c, 306, y - 72, 480, y - 108, color=ACCENT, width=1.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 230, "Apps speak MySQL protocol to vtgate; it routes, fans out, and reassembles. Battle-tested at YouTube scale.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Citus Architecture",
                       "Sharded Postgres with a coordinator.")
    box(c, 216, y - 70, 180, 60, BOX_PURP, "Coordinator", "metadata +\nreference tables", font_size=11)
    box(c, 72, y - 180, 150, 70, BOX_GREEN, "Worker 1", "shards", font_size=11)
    box(c, 246, y - 180, 150, 70, BOX_GREEN, "Worker 2", "shards", font_size=11)
    box(c, 420, y - 180, 120, 70, BOX_GREEN, "Worker 3", "shards", font_size=11)
    arrow(c, 306, y - 72, 150, y - 108, color=ACCENT, width=1.5)
    arrow(c, 306, y - 72, 320, y - 108, color=ACCENT, width=1.5)
    arrow(c, 306, y - 72, 480, y - 108, color=ACCENT, width=1.5)
    yy = bullet_list(c, 72, y - 230, [
        "CREATE TABLE ... DISTRIBUTED BY (tenant_id) -- Postgres extension, not a fork.",
        "Co-located joins on the distribution key run fully on workers -- fast.",
        "Reference tables (small, replicated everywhere) avoid cross-shard joins."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Sharding in Practice -- Remember",
                 ["Shard last: exhaust bigger instances, replicas, caching, and partitioning first.",
                  "Shard keys need cardinality, even spread, query locality, and stability -- choose once, carefully.",
                  "Reshard with dual-writes + batched backfill + checksum verification, never a flag flip.",
                  "Vitess shards MySQL behind a vtgate router; Citus distributes Postgres via coordinator + workers.",
                  "Design queries to hit one shard -- scatter-gather across all shards kills the benefit."],
                 pg)
    c.save(); print("wrote", path)


def pdf_backup(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Backup & Recovery\nVisual Guide",
               "Full, incremental, PITR --\nbackups you can actually restore from.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "Backup Types",
                       "Three flavors, one timeline.")
    box(c, 72, y - 70, 140, 70, BOX_BLUE, "FULL", "everything\n(Sunday)", font_size=11)
    box(c, 246, y - 70, 140, 70, BOX_GREEN, "INCREMENTAL", "since last\nbackup", font_size=11)
    box(c, 420, y - 70, 120, 70, BOX_ORANGE, "DIFFERENTIAL", "since last\nFULL", font_size=11)
    arrow(c, 212, y - 35, 244, y - 35, color=ACCENT, width=2)
    arrow(c, 386, y - 35, 418, y - 35, color=ACCENT, width=2)
    yy = bullet_list(c, 72, y - 180, [
        "Full: slowest, simplest restore -- one file, no chain to break.",
        "Incremental: fast backups, but restore replays the whole chain -- one corrupt link kills it.",
        "Differential: middle ground -- one full + one diff covers any day since."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "PITR with WAL Archiving",
                       "Restore to ANY second, not just backup time.")
    box(c, 72, y - 70, 180, 70, BOX_BLUE, "Base backup", "Sunday 02:00", font_size=11)
    arrow(c, 252, y - 35, 290, y - 35, color=ACCENT, width=2, label="+ WAL")
    box(c, 290, y - 70, 250, 70, BOX_GREEN, "WAL segments", "every change since", font_size=11)
    arrow(c, 306, y - 72, 306, y - 110, color=RED, width=2.5)
    box(c, 196, y - 180, 220, 70, BOX_RED, "Restore point", "Wed 14:32:17", font_size=11)
    yy = bullet_list(c, 72, y - 230, [
        "Archive every WAL segment off the primary (archive_command) -- gaps mean unrecoverable time.",
        "Recovery replays: base backup + WAL up to your target timestamp.",
        "Test the archive stream continuously -- a silent archiving failure voids all PITR promises."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Backup Storage: 3-2-1",
                       "Where backups live matters as much as taking them.")
    r321 = [("3 copies", "primary + backup + offsite", BOX_BLUE),
            ("2 media types", "disk + object storage (S3-class)", BOX_GREEN),
            ("1 offsite", "different region -- survives the datacenter fire", BOX_ORANGE)]
    yy = y
    for name, desc, fill in r321:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11.5)
        yy -= 76
    note(c, 72, yy - 10, 468, "Encrypt backups at rest. A stolen backup is a stolen database -- keys managed separately.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Restore Testing Discipline",
                       "An untested backup is a rumor.")
    steps = [("1. Automate", "nightly restore into a scratch environment", BOX_BLUE),
             ("2. Verify", "row counts, checksums, app smoke tests", BOX_GREEN),
             ("3. Time it", "measure real RTO -- hope is not a metric", BOX_ORANGE),
             ("4. Document", "runbook anyone can follow at 3 AM", BOX_PURP)]
    yy = y
    for name, desc, fill in steps:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "RTO & RPO",
                       "Two numbers that define your whole strategy.")
    box(c, 72, y - 110, 225, 130, BOX_RED, "RTO", "how LONG to\nrestore\n(downtime budget)", font_size=12)
    box(c, 315, y - 110, 225, 130, BOX_ORANGE, "RPO", "how MUCH data\nto lose\n(backup frequency)", font_size=12)
    yy = bullet_list(c, 72, y - 160, [
        "RPO 5 min + RTO 1 hr demands: continuous WAL archiving + rehearsed restores.",
        "Tighter targets cost real money -- get the business to sign the numbers.",
        "Your ACTUAL RTO is whatever the last restore drill measured, not the SLA slide."],
        font_size=11, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Backup & Recovery -- Remember",
                 ["Full backups restore simply; incremental chains are fragile -- pick deliberately.",
                  "PITR = base backup + continuous WAL archiving -- restores to any second, if the stream is healthy.",
                  "3-2-1: three copies, two media, one offsite -- encrypted, keys separate.",
                  "Restore on a schedule: automated, verified, timed, documented -- or it doesn't count.",
                  "RTO/RPO are business decisions -- but only the last drill proves you meet them."],
                 pg)
    c.save(); print("wrote", path)


def pdf_migrations(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Schema Migrations\nVisual Guide",
               "Expand/contract, zero-downtime deploys --\nchange the database without stopping the world.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "The Zero-Downtime Problem",
                       "Old code and new schema must coexist during a deploy.")
    box(c, 72, y - 70, 200, 70, BOX_BLUE, "App v1 (old)", "running", font_size=11)
    box(c, 340, y - 70, 200, 70, BOX_GREEN, "App v2 (new)", "deploying", font_size=11)
    box(c, 196, y - 180, 220, 70, BOX_ORANGE, "One database", "shared!", font_size=11)
    arrow(c, 172, y - 72, 260, y - 108, color=ACCENT, width=1.5)
    arrow(c, 440, y - 72, 350, y - 108, color=ACCENT, width=1.5)
    note(c, 72, y - 280, 468, "During rolling deploys both versions hit the same DB. Every migration must be compatible with BOTH.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "The Expand/Contract Pattern",
                       "Three phases, zero breakage.")
    box(c, 72, y - 80, 468, 70, BOX_GREEN, "1. EXPAND",
        "add new column/table as NULLABLE -- old code ignores it, nothing breaks", font_size=11.5)
    arrow(c, 306, y - 82, 306, y - 110, color=ACCENT, width=2)
    box(c, 72, y - 180, 468, 70, BOX_BLUE, "2. MIGRATE",
        "deploy code writing BOTH, backfill old rows, switch reads to new", font_size=11.5)
    arrow(c, 306, y - 182, 306, y - 210, color=ACCENT, width=2)
    box(c, 72, y - 280, 468, 70, BOX_ORANGE, "3. CONTRACT",
        "drop the old column -- only after NO code references it", font_size=11.5)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Backfill Strategies",
                       "Filling the new column on millions of rows.")
    backs = [("Batched updates", "UPDATE ... WHERE id BETWEEN x AND y LIMIT 10000 -- small txns, no lock storms", BOX_BLUE),
             ("Throttled jobs", "pause between batches; watch replica lag", BOX_GREEN),
             ("Idempotent + resumable", "track progress; crashes resume, never restart from zero", BOX_ORANGE)]
    yy = y
    for name, desc, fill in backs:
        box(c, 72, yy - 64, 468, 68, fill, name, desc, font_size=11)
        yy -= 84
    note(c, 72, yy - 10, 468, "Never backfill in one giant transaction -- it locks the table and bloats the WAL.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Dangerous Operations",
                       "These lock, rewrite, or break -- handle with care.")
    dangs = [("Rename column", "breaks old code instantly -- use expand/contract instead", BOX_RED),
             ("ADD COLUMN ... NOT NULL", "rewrites the table without a default -- add nullable, backfill, then constrain", BOX_RED),
             ("DROP COLUMN / TABLE", "irreversible without a restore -- contract phase only, after code is clean", BOX_RED)]
    yy = y
    for name, desc, fill in dangs:
        box(c, 72, yy - 64, 468, 68, fill, name, desc, font_size=11)
        yy -= 84
    note(c, 72, yy - 10, 468, "DDL takes strong locks. On big tables, even 'fast' ALTERs deserve a maintenance window or online tooling.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Migration Tools",
                       "Versioned, reviewable, reversible.")
    tools = [("Flyway / Liquibase", "SQL-first versioned migrations -- the enterprise standard", BOX_BLUE),
             ("Alembic", "SQLAlchemy's companion -- autogenerate diffs, review them", BOX_GREEN),
             ("Prisma / Django", "ORM-managed -- great until you need raw SQL escape hatches", BOX_PURP)]
    yy = y
    for name, desc, fill in tools:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=11)
        yy -= 80
    yy = bullet_list(c, 72, yy - 10, [
        "Every migration: versioned in git, reviewed like code, runnable forward AND back.",
        "CI runs migrations against a scratch DB -- broken SQL never reaches production."],
        font_size=10.5, gap=24)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Schema Migrations -- Remember",
                 ["Rolling deploys mean old and new code share one DB -- every migration must suit both.",
                  "Expand/contract: add nullable, dual-write + backfill, then drop the old -- never rename in place.",
                  "Backfill in small throttled batches; make it idempotent and resumable.",
                  "Renames, NOT NULL without defaults, and DROPs are the dangerous trio -- plan them explicitly.",
                  "Version migrations in git, review them, test them in CI, keep them reversible."],
                 pg)
    c.save(); print("wrote", path)

def pdf_indexing_deep(path):
    c = new_canvas(path); pg = 1
    title_page(c, "Indexing Deep Dive\nVisual Guide",
               "Composite ordering, covering indexes, BRIN --\nbeyond 'just add an index'.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "How B-Tree Indexes Work",
                       "Sorted structure, logarithmic lookups.")
    box(c, 246, y - 70, 120, 60, BOX_PURP, "Root", "", font_size=11)
    arrow(c, 306, y - 72, 160, y - 110, color=ACCENT, width=1.5)
    arrow(c, 306, y - 72, 452, y - 110, color=ACCENT, width=1.5)
    box(c, 100, y - 170, 120, 60, BOX_BLUE, "Branch", "", font_size=11)
    box(c, 392, y - 170, 120, 60, BOX_BLUE, "Branch", "", font_size=11)
    arrow(c, 160, y - 172, 120, y - 210, color=ACCENT, width=1.5)
    arrow(c, 160, y - 172, 200, y - 210, color=ACCENT, width=1.5)
    arrow(c, 452, y - 172, 412, y - 210, color=ACCENT, width=1.5)
    arrow(c, 452, y - 172, 492, y - 210, color=ACCENT, width=1.5)
    for i, lx in enumerate([72, 172, 364, 464]):
        box(c, lx, y - 270, 76, 60, BOX_GREEN, "Leaf", "sorted", font_size=10)
    yy = bullet_list(c, 72, y - 320, [
        "Leaves hold sorted keys + row pointers; lookups walk root -> branch -> leaf: O(log n).",
        "Writes pay for index maintenance -- every index slows INSERT/UPDATE.",
        "Rule of thumb: index foreign keys, WHERE filters, and ORDER BY columns you actually use."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Composite Index Ordering",
                       "Column order decides which queries the index serves.")
    cb = code_block(c, 72, y, [
        "CREATE INDEX ON orders (customer_id, status, created_at);",
        "-- serves:  WHERE customer_id = ?",
        "-- serves:  WHERE customer_id = ? AND status = ?",
        "-- serves:  WHERE customer_id = ? AND status = ? AND created_at > ?",
        "-- MISSES:  WHERE status = ?   (leading column absent)"])
    yy = bullet_list(c, 72, cb - 28, [
        "Leftmost-prefix rule: the index works from the first column onward.",
        "Equality columns first, range/sort columns LAST -- a range stops the prefix.",
        "High-selectivity first is a myth for B-trees; equality-first ordering is what matters."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Covering Indexes",
                       "Answer the query from the index alone -- never touch the table.")
    box(c, 72, y - 70, 200, 70, BOX_BLUE, "Index", "(email)\nINCLUDE (name)", font_size=11)
    arrow(c, 272, y - 35, 330, y - 35, color=GREEN, width=2.5, label="index-only")
    box(c, 330, y - 70, 210, 70, BOX_GREEN, "Result", "no heap fetch", font_size=11)
    cb = code_block(c, 72, y - 120, [
        "CREATE INDEX ON users (email) INCLUDE (name);",
        "SELECT name FROM users WHERE email = ?;  -- Index Only Scan"])
    note(c, 72, cb - 60, 468, "INCLUDE adds payload columns without sorting by them -- wider index, but zero table lookups.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Partial Indexes",
                       "Index only the rows you query.")
    cb = code_block(c, 72, y, [
        "CREATE INDEX ON orders (created_at)",
        "WHERE status = 'pending';",
        "-- tiny index: only pending rows",
        "-- queries with the same WHERE clause use it automatically"])
    yy = bullet_list(c, 72, cb - 28, [
        "Perfect for skewed predicates: active users, open tickets, unpaid invoices.",
        "Smaller index = faster writes, less memory, cheaper maintenance.",
        "The query's WHERE must imply the index predicate, or the planner ignores it."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "BRIN for Time-Series",
                       "Block Range INdexes: tiny summaries for naturally ordered data.")
    for i in range(4):
        box(c, 72 + i * 120, y - 70, 108, 70, BOX_TEAL, "Block %d" % (i + 1),
            "min..max", font_size=10.5)
    c.setFillColor(INK); c.setFont(BODY_FONT, 10.5)
    c.drawString(72, y - 110, "BRIN stores one min/max per block -- KBs of index for TBs of data.")
    yy = bullet_list(c, 72, y - 160, [
        "Brilliant for append-only time series: each block's range is tight and ordered.",
        "Useless for random-ordered columns -- ranges overlap and nothing is pruned.",
        "B-tree on 1B rows: GBs. BRIN: KBs. The trade is precision for size."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "Indexing Deep Dive -- Remember",
                 ["B-trees give O(log n) lookups; every index taxes writes -- index deliberately.",
                  "Composite order: equality columns first, range/sort last; leftmost prefix rules.",
                  "Covering indexes (INCLUDE) answer queries without touching the table.",
                  "Partial indexes shrink the index to the rows you actually query.",
                  "BRIN indexes time-series in kilobytes where B-trees need gigabytes."],
                 pg)
    c.save(); print("wrote", path)


def pdf_sql_vs_nosql(path):
    c = new_canvas(path); pg = 1
    title_page(c, "SQL vs NoSQL\nVisual Guide",
               "A decision framework --\nmap your workload to the right store.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "Know Your Workload",
                       "Four axes decide the answer before any product name appears.")
    axes = [("Structure", "fixed schema + relations, or flexible/evolving shapes?", BOX_BLUE),
            ("Scale", "GBs on one node, or TBs across many?", BOX_GREEN),
            ("Consistency", "must every read see the latest write?", BOX_ORANGE),
            ("Query patterns", "ad-hoc joins, or known key lookups?", BOX_PURP)]
    yy = y
    for name, desc, fill in axes:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11.5)
        yy -= 76
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Choose SQL When...",
                       "Relational strengths, honestly stated.")
    sq = [("Relationships are the product", "orders JOIN customers JOIN items -- joins are the query", BOX_BLUE),
          ("ACID is non-negotiable", "money movement, inventory -- no partial writes", BOX_GREEN),
          ("Queries are ad-hoc", "analysts ask questions you didn't pre-model", BOX_TEAL),
          ("One operational brain", "your team knows Postgres -- boring is reliable", BOX_ORANGE)]
    yy = y
    for name, desc, fill in sq:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "Choose NoSQL When...",
                       "Scale and shape flexibility, honestly stated.")
    ns = [("Write scale exceeds one node", "millions of writes/sec -- shard by design", BOX_GREEN),
          ("Schema evolves constantly", "each document carries its own shape", BOX_PURP),
          ("Access patterns are known", "key lookups you can enumerate up front", BOX_BLUE),
          ("Special structure fits", "graphs, time series, vectors -- native models win", BOX_TEAL)]
    yy = y
    for name, desc, fill in ns:
        box(c, 72, yy - 56, 468, 60, fill, name, desc, font_size=11)
        yy -= 76
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Consistency vs Availability",
                       "The trade you are actually making.")
    box(c, 72, y - 90, 225, 110, BOX_BLUE, "CP", "consistent +\npartition-tolerant", font_size=12)
    box(c, 315, y - 90, 225, 110, BOX_GREEN, "AP", "available +\npartition-tolerant", font_size=12)
    yy = bullet_list(c, 72, y - 140, [
        "During a network partition you pick: refuse writes (CP) or accept divergence (AP).",
        "Most systems live in the middle: tunable consistency (Cassandra), sync/async replicas.",
        "Ask: 'what breaks if two users see different data for 5 seconds?' -- that is your answer."],
        font_size=11, gap=26)
    note(c, 72, 150, 468, "CAP is about partitions. Day-to-day, the real dial is latency vs consistency -- PACELC.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Polyglot Persistence",
                       "Real systems use several stores -- each for its strength.")
    box(c, 216, y - 70, 180, 60, BOX_PURP, "App", "writes + reads", font_size=11)
    stores = [("Postgres", "orders\n(truth)", BOX_BLUE), ("Redis", "sessions\n(speed)", BOX_ORANGE),
              ("OpenSearch", "catalog\n(search)", BOX_GREEN), ("Warehouse", "history\n(analytics)", BOX_TEAL)]
    bx = 72
    for name, desc, fill in stores:
        box(c, bx, y - 190, 108, 80, fill, name, desc, font_size=10)
        arrow(c, 306, y - 72, bx + 54, y - 108, color=ACCENT, width=1.5)
        bx += 120
    note(c, 72, 150, 468, "Polyglot is powerful and expensive: every store is a backup, monitoring, and expertise bill.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "SQL vs NoSQL -- Remember",
                 ["Decide on workload axes first: structure, scale, consistency needs, query patterns.",
                  "SQL wins on relationships, ACID guarantees, ad-hoc queries, and operational familiarity.",
                  "NoSQL wins on write scale, flexible schemas, known access patterns, and native data models.",
                  "Consistency vs availability is a per-partition trade -- most systems tune the middle.",
                  "Polyglot persistence is normal at scale -- but every added store is an operational bill."],
                 pg)
    c.save(); print("wrote", path)


def pdf_newsql(path):
    c = new_canvas(path); pg = 1
    title_page(c, "NewSQL\nVisual Guide",
               "Spanner, CockroachDB --\nrelational guarantees at planetary scale.",
               "Databases", None); pg += 1

    y = section_header(c, 1, 6, "The NewSQL Promise",
                       "Why not just use NoSQL?")
    box(c, 72, y - 90, 225, 110, BOX_BLUE, "SQL", "joins, ACID,\nknown tooling", font_size=12)
    box(c, 315, y - 90, 225, 110, BOX_GREEN, "NoSQL scale", "sharded,\nresilient", font_size=12)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 13)
    c.drawCentredString(306, y - 130, "+")
    box(c, 156, y - 240, 300, 90, BOX_PURP, "NewSQL", "both: distributed SQL\nwith real transactions", font_size=12)
    arrow(c, 184, y - 92, 240, y - 148, color=ACCENT, width=2)
    arrow(c, 428, y - 92, 372, y - 148, color=ACCENT, width=2)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 2, 6, "Spanner & TrueTime",
                       "Globally consistent reads via synchronized clocks.")
    box(c, 72, y - 70, 140, 70, BOX_BLUE, "Atomic\nclocks", "", font_size=11)
    box(c, 236, y - 70, 140, 70, BOX_GREEN, "GPS\nreceivers", "", font_size=11)
    arrow(c, 212, y - 35, 234, y - 35, color=ACCENT, width=2)
    arrow(c, 376, y - 35, 398, y - 35, color=ACCENT, width=2)
    box(c, 398, y - 70, 142, 70, BOX_PURP, "TrueTime", "time +\nuncertainty", font_size=11)
    yy = bullet_list(c, 72, y - 180, [
        "TrueTime returns now as an INTERVAL [earliest, latest] -- uncertainty is explicit.",
        "Transactions commit-wait out the uncertainty: everyone agrees on order globally.",
        "Result: EXTERNAL CONSISTENCY -- the system behaves as if one machine, worldwide."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 3, 6, "CockroachDB",
                       "Spanner's ideas, open source, no atomic clocks.")
    box(c, 72, y - 80, 468, 70, BOX_BLUE, "Data split into Ranges (~512MB)",
        "each range replicated via Raft across 3+ nodes", font_size=11.5)
    arrow(c, 306, y - 82, 306, y - 110, color=ACCENT, width=2)
    box(c, 72, y - 180, 225, 70, BOX_GREEN, "Leaseholder", "serves reads\nfor its range", font_size=11)
    box(c, 315, y - 180, 225, 70, BOX_ORANGE, "HLC timestamps", "hybrid logical clock\norders txns", font_size=11)
    yy = bullet_list(c, 72, y - 230, [
        "Raft consensus per range: a majority ack makes a write durable.",
        "HLC (physical + logical time) orders transactions without TrueTime hardware.",
        "Node death: ranges re-replicate automatically -- self-healing by default."],
        font_size=10.5, gap=26)
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 4, 6, "Distributed SQL Architecture",
                       "Three layers, cleanly separated.")
    layers = [("SQL layer", "parses, plans, optimizes -- stateless, scales horizontally", BOX_PURP),
              ("Distributed KV", "ranges/rows sharded across nodes -- the storage fabric", BOX_BLUE),
              ("Consensus", "Raft/Paxos per shard -- every write agreed by majority", BOX_GREEN)]
    yy = y
    for name, desc, fill in layers:
        box(c, 72, yy - 64, 468, 68, fill, name, desc, font_size=11.5)
        if yy < y:
            arrow(c, 306, yy + 4, 306, yy - 8, color=ACCENT, width=1.5)
        yy -= 84
    note(c, 72, yy - 10, 468, "Stateless SQL nodes can be added freely; the consensus layer is where the hard scaling lives.")
    footer(c, pg); c.showPage(); pg += 1

    y = section_header(c, 5, 6, "Trade-offs",
                       "Honest costs of planetary consistency.")
    tos = [("Latency", "consensus needs cross-node round trips -- single-digit ms at best", BOX_ORANGE),
           ("Operational complexity", "multi-region clusters are not 'set and forget'", BOX_RED),
           ("Cost", "3x replication minimum -- durability is never free", BOX_BLUE)]
    yy = y
    for name, desc, fill in tos:
        box(c, 72, yy - 60, 468, 64, fill, name, desc, font_size=11.5)
        yy -= 80
    note(c, 72, yy - 10, 468, "Use NewSQL when you need global ACID (payments, inventory). Otherwise Postgres + replicas is simpler.")
    footer(c, pg); c.showPage(); pg += 1

    summary_page(c, "NewSQL -- Remember",
                 ["NewSQL keeps SQL semantics and ACID while sharding like NoSQL.",
                  "Spanner's TrueTime turns clock uncertainty into global external consistency.",
                  "CockroachDB replicates data ranges with Raft and orders transactions via hybrid logical clocks.",
                  "Architecture: stateless SQL layer, distributed KV fabric, per-shard consensus.",
                  "Costs are real: consensus latency, operational complexity, 3x replication -- use when global ACID pays."],
                 pg)
    c.save(); print("wrote", path)


BUILDERS = [
    ("bbg-sql-fundamentals", pdf_sql_fundamentals),
    ("bbg-joins", pdf_joins),
    ("bbg-acid", pdf_acid),
    ("bbg-normalization", pdf_normalization),
    ("bbg-nosql-types", pdf_nosql_types),
    ("bbg-mongodb", pdf_mongodb),
    ("bbg-redis", pdf_redis),
    ("bbg-cassandra", pdf_cassandra),
    ("bbg-dynamodb", pdf_dynamodb),
    ("bbg-postgres", pdf_postgres),
    ("bbg-query-planning", pdf_query_planning),
    ("bbg-db-replication", pdf_replication),
    ("bbg-db-sharding-practice", pdf_sharding_practice),
    ("bbg-db-backup", pdf_backup),
    ("bbg-migrations", pdf_migrations),
    ("bbg-indexing-deep", pdf_indexing_deep),
    ("bbg-sql-vs-nosql", pdf_sql_vs_nosql),
    ("bbg-newsql", pdf_newsql),
]


if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(outdir, exist_ok=True)
    for slug, fn in BUILDERS:
        fn(os.path.join(outdir, slug + ".pdf"))
    print("done:", len(BUILDERS), "pdfs")
